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


if __name__ == "__main__":
    unittest.main()
