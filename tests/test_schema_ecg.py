"""
Unit Tests for Clinical Schema, Leakage Controls & Dual-Track ECG Contracts (STEP-015).
"""

import os
import struct
import unittest

from src.cvd_mm.schema_ecg import (
    assert_no_leakage_predictors,
    inspect_int16_wfdb_waveform,
    load_variable_dictionary,
    normalize_cardiomled_image_stem,
    parse_wfdb_header_text,
    validate_ecg_image_bytes,
)

# Also verify pilot QA statistical agreement functions when automation scripts run
from importlib.util import module_from_spec, spec_from_file_location

_pilot_spec = spec_from_file_location("run_pilot_qa", os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "14_Automation", "run_pilot_qa.py"))
_pilot_mod = module_from_spec(_pilot_spec)
_pilot_spec.loader.exec_module(_pilot_mod)

_pkg_spec = spec_from_file_location("package_kaggle_ecg_assets", os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "14_Automation", "package_kaggle_ecg_assets.py"))
_pkg_mod = module_from_spec(_pkg_spec)
_pkg_spec.loader.exec_module(_pkg_mod)

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class TestSchemaAndECGContract(unittest.TestCase):
    def test_variables_csv_schema_and_leakage_guards(self):
        """Verify variables.csv loads cleanly and blocks target leakage & Tier-A Troponin."""
        var_csv = os.path.join(REPO_ROOT, "04_Outcome_Schema_QA", "variables.csv")
        rows = load_variable_dictionary(var_csv)
        self.assertGreaterEqual(len(rows), 50)

        # Clean Tier A clinical+lab+lifestyle subset must pass
        assert_no_leakage_predictors(
            ["age_years", "sex", "sbp_mmhg", "total_cholesterol_mgdl", "smoking_status"],
            var_rows=rows,
            tier="A",
        )

        # Leakage features must fail
        for bad_col in ["CVD Risk Score", "Blood Pressure Category", "Initial diagnosis", "patient_id_harmonized"]:
            with self.assertRaises(ValueError):
                assert_no_leakage_predictors(["age_years", bad_col], var_rows=rows, tier="A")

        # Troponin-I must fail in Tier A but be allowed cleanly in Tier B sensitivity
        with self.assertRaises(ValueError):
            assert_no_leakage_predictors(["age_years", "Troponine - I (Q)"], var_rows=rows, tier="A")
        assert_no_leakage_predictors(["age_years", "Troponine - I (Q)"], var_rows=rows, tier="B")

    def test_wfdb_header_phi_and_signal_integrity(self):
        """Verify 12-lead WFDB header parsing, PHI rejection, flatline & clipping detection."""
        valid_hea = "\n".join(
            ["00001_lr 12 100 1000"]
            + [
                f"00001_lr.dat 16 1000/mV 16 0 0 0 0 {lead}"
                for lead in ["I", "II", "III", "AVR", "AVL", "AVF", "V1", "V2", "V3", "V4", "V5", "V6"]
            ]
        )
        parsed = parse_wfdb_header_text(valid_hea)
        self.assertEqual(parsed["num_leads"], 12)
        self.assertEqual(parsed["sampling_hz"], 100.0)
        self.assertEqual(parsed["num_samples"], 1000)

        # Reject PHI comment line
        with self.assertRaises(ValueError):
            parse_wfdb_header_text(valid_hea + "\n# Patient Name: John Doe")

        # Build clean synthetic signal (varying values on all 12 leads, 1000 samples)
        clean_samples = [(s % 200) - 100 + lead for s in range(1000) for lead in range(12)]
        clean_bytes = struct.pack("<" + "h" * len(clean_samples), *clean_samples)
        clean_report = inspect_int16_wfdb_waveform(clean_bytes, num_leads=12, num_samples=1000)
        self.assertTrue(clean_report["passed_clean"])

        # Inject flatline on lead V5 (index 10) matching PTB-XL ecg_id=12722 defect
        flat_samples = list(clean_samples)
        for s in range(1000):
            flat_samples[s * 12 + 10] = 0
        flat_report = inspect_int16_wfdb_waveform(
            struct.pack("<" + "h" * len(flat_samples), *flat_samples),
            num_leads=12,
            num_samples=1000,
        )
        self.assertFalse(flat_report["passed_clean"])
        self.assertEqual(flat_report["flatline_leads"], ["V5"])

        # Inject int16 saturation clipping on lead I (index 0)
        clip_samples = list(clean_samples)
        clip_samples[0] = 32767
        clip_report = inspect_int16_wfdb_waveform(
            struct.pack("<" + "h" * len(clip_samples), *clip_samples),
            num_leads=12,
            num_samples=1000,
        )
        self.assertFalse(clip_report["passed_clean"])
        self.assertEqual(clip_report["clipped_leads"], ["I"])

    def test_cardiomled_image_contract_and_stem_normalization(self):
        """Verify CARDIO-ML-ED filename normalization and RISK0012 PNG vs JPG isolation."""
        self.assertEqual(normalize_cardiomled_image_stem("150753 "), "150753")
        self.assertEqual(normalize_cardiomled_image_stem("136883(2)"), "136883-2")
        self.assertEqual(normalize_cardiomled_image_stem("126035-1"), "126035-1")
        for bad_raw, expected in [("150793 .png", "150793.png"), ("150821 .png", "150821.png"), ("150874 .png", "150874.png")]:
            self.assertEqual(_pkg_mod.sanitize_kaggle_filename(bad_raw), expected)

        # Minimal valid PNG with IHDR (width=1535, height=4490, bd=8, ct=2) and IEND chunk
        ihdr_data = struct.pack(">IIBBBBB", 1535, 4490, 8, 2, 0, 0, 0)
        fake_png = b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + ihdr_data + b"0000" + b"\x00\x00\x00\x00IEND\xaeB`\x82"
        png_res = validate_ecg_image_bytes(fake_png, "1.png")
        self.assertTrue(png_res["eligible_12row_encoder"])
        self.assertEqual(png_res["width"], 1535)
        self.assertEqual(png_res["height"], 4490)

        # JPG uncropped strip must pass byte check but remain quarantined (eligible=False)
        fake_jpg = b"\xff\xd8\xff\xe0\x00\x10JFIF\xff\xd9"
        jpg_res = validate_ecg_image_bytes(fake_jpg, "126035-1.jpg")
        self.assertFalse(jpg_res["eligible_12row_encoder"])

        with self.assertRaises(ValueError):
            validate_ecg_image_bytes(b"NOT_A_PNG", "bad.png")

    def test_pilot_kappa_and_icc_agreement_math(self):
        """Verify Cohen's kappa and ICC(2,1) calculation on non-trivial discordant inputs."""
        k_perf, acc_perf = _pilot_mod.cohen_kappa(["A", "B", "A", "B"], ["A", "B", "A", "B"])
        self.assertAlmostEqual(k_perf, 1.0, places=6)
        self.assertAlmostEqual(acc_perf, 1.0, places=6)

        k_part, acc_part = _pilot_mod.cohen_kappa(["A", "A", "B", "B", "A"], ["A", "B", "B", "B", "A"])
        self.assertAlmostEqual(acc_part, 0.8, places=6)
        self.assertLess(k_part, 0.8)  # Kappa adjusts cleanly for chance agreement

        icc_perf, rel_perf = _pilot_mod.icc_two_way([120.0, 140.0, 160.0], [120.0, 140.0, 160.0])
        self.assertAlmostEqual(icc_perf, 1.0, places=6)
        self.assertAlmostEqual(rel_perf, 0.0, places=9)

        icc_noisy, rel_noisy = _pilot_mod.icc_two_way([120.0, 140.0, 160.0], [122.0, 138.0, 161.0])
        self.assertGreater(icc_noisy, 0.98)
        self.assertGreater(rel_noisy, 0.0)


if __name__ == "__main__":
    unittest.main()
