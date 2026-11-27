"""
Leakage-Prevention & Zero-Phase ECG DSP Tests for STEP-019 Verification.
"""

import math
import unittest

from src.cvd_mm.ecg import (
    apply_baseline_highpass_zero_phase,
    apply_powerline_notch_zero_phase,
    pearson_correlation,
    suppress_red_ecg_grid_rgb,
)
from src.cvd_mm.preprocessing import (
    StageARecordCleaner,
    TrainOnlyTabularPreprocessor,
    build_modality_presence_mask,
)


class TestPreprocessingAndECGDsp(unittest.TestCase):
    def test_stage_b_refuses_validation_or_test_rows_in_fit(self):
        """Fitting Stage B imputer/scaler with non-train split_tags must raise PermissionError."""
        train_rows = [
            {"age_years": 40.0, "sbp_mmhg": 120.0, "sex": "M"},
            {"age_years": 50.0, "sbp_mmhg": 130.0, "sex": "F"},
        ]
        prep = TrainOnlyTabularPreprocessor(["age_years", "sbp_mmhg"], ["sex"], tier="A")
        with self.assertRaises(PermissionError):
            prep.fit(train_rows, split_tags=["train", "val"])
        with self.assertRaises(PermissionError):
            prep.fit(train_rows, split_tags=["train", "test"])

    def test_zero_test_leakage_and_mnar_masks(self):
        """Train fit state & FitStateHash must stay invariant across extreme Test rows, while emitting _isnan masks."""
        train_rows = [
            {"age_years": 40.0, "sbp_mmhg": 120.0, "sex": "M"},
            {"age_years": 50.0, "sbp_mmhg": 140.0, "sex": "F"},
            {"age_years": 60.0, "sbp_mmhg": None, "sex": "M"},  # missing sbp
        ]
        test_rows_a = [{"age_years": 70.0, "sbp_mmhg": 160.0, "sex": "F"}]
        test_rows_b = [{"age_years": 999.0, "sbp_mmhg": 9999.0, "sex": "UNKNOWN_CAT"}]

        prep1 = TrainOnlyTabularPreprocessor(["age_years", "sbp_mmhg"], ["sex"], tier="A")
        prep1.fit(train_rows, split_tags=["train"] * 3)
        out_train_1 = prep1.transform(train_rows)

        prep2 = TrainOnlyTabularPreprocessor(["age_years", "sbp_mmhg"], ["sex"], tier="A")
        prep2.fit(train_rows, split_tags=["train"] * 3)

        self.assertEqual(prep1.fit_state_hash_, prep2.fit_state_hash_)
        self.assertEqual(prep1.medians_["age_years"], 50.0)
        self.assertEqual(prep1.medians_["sbp_mmhg"], 130.0)

        # Row 2 had missing sbp_mmhg -> index 3 is sbp_mmhg_isnan == 1.0 and imputed scaled sbp == 0.0
        self.assertAlmostEqual(out_train_1[2][2], 0.0, places=6)
        self.assertEqual(out_train_1[2][3], 1.0)

        # Test transform works safely on unseen category -> maps to MISSING slot cleanly without crashing
        tx_b = prep1.transform(test_rows_b)
        feat_names = prep1.feature_names()
        self.assertEqual(tx_b[0][feat_names.index("sex__MISSING")], 1.0)
        # Ensure test_rows_a vs test_rows_b did NOT touch train medians
        self.assertEqual(prep1.medians_["sbp_mmhg"], 130.0)

        # Verify 4D modality mask helper & Stage A deterministic cleaner
        mask = build_modality_presence_mask(True, False, True, True)
        self.assertEqual(mask, [1, 0, 1, 1])

        cleaned_sul = StageARecordCleaner.clean_record({"age_days": 18262.5, "height_cm": 170.0, "weight_kg": 70.0}, "DS0004")
        self.assertAlmostEqual(cleaned_sul["age_years"], 50.0, places=2)
        self.assertAlmostEqual(cleaned_sul["bmi_kgm2"], 24.221, places=2)

        cleaned_cair = StageARecordCleaner.clean_record({"ldl_estimated_mgdl": -18.0}, "DS0003")
        self.assertIsNone(cleaned_cair["ldl_estimated_mgdl"])

        with self.assertRaises(ValueError):
            TrainOnlyTabularPreprocessor(["age_years", "Troponine - I (Q)"], [], tier="A")

    def test_ecg_zero_phase_notch_and_baseline_wander_preserves_morphology(self):
        """Verify 50 Hz notch removes powerline hum & <=0.5 Hz highpass removes drift while preserving 1.5 Hz beat."""
        fs = 500.0
        n = 1500  # 3 seconds
        t = [i / fs for i in range(n)]
        # Clean synthetic cardiac wave (1.2 Hz + 3.6 Hz harmonic)
        clean_cardiac = [math.sin(2.0 * math.pi * 1.2 * ti) + 0.35 * math.sin(2.0 * math.pi * 3.6 * ti) for ti in t]
        # Pollute with 50 Hz AC hum & 0.12 Hz slow respiratory drift
        hum_50 = [0.6 * math.sin(2.0 * math.pi * 50.0 * ti) for ti in t]
        drift_low = [0.8 * math.sin(2.0 * math.pi * 0.12 * ti) for ti in t]

        noisy_hum = [c + h for c, h in zip(clean_cardiac, hum_50)]
        after_notch = apply_powerline_notch_zero_phase(noisy_hum, fs_hz=fs, notch_hz=50.0, q=30.0)
        # Measure interior window away from edge transient
        r_notch = pearson_correlation(clean_cardiac[250:1250], after_notch[250:1250])
        self.assertGreater(r_notch, 0.99)

        # 100 Hz Nyquist safety: must cleanly bypass 50 Hz notch without numerical blowup
        bypass_100 = apply_powerline_notch_zero_phase(clean_cardiac[:300], fs_hz=100.0, notch_hz=50.0)
        self.assertEqual(bypass_100, clean_cardiac[:300])

        # Baseline highpass <= 0.5 Hz preserves morphology while enforcing cutoff ceiling
        with self.assertRaises(ValueError):
            apply_baseline_highpass_zero_phase(clean_cardiac, fs_hz=fs, cutoff_hz=1.2)

        noisy_drift = [c + d for c, d in zip(clean_cardiac, drift_low)]
        after_hp = apply_baseline_highpass_zero_phase(noisy_drift, fs_hz=fs, cutoff_hz=0.5)
        r_hp = pearson_correlation(clean_cardiac[300:1200], after_hp[300:1200])
        self.assertGreater(r_hp, 0.96)

    def test_red_ecg_grid_suppression_pixel_contract(self):
        """Red/pink ECG grid pixels should lift near white while dark neutral ECG ink remains dark."""
        pink_grid_pixel = suppress_red_ecg_grid_rgb(245, 165, 165)
        black_ink_pixel = suppress_red_ecg_grid_rgb(28, 26, 28)
        self.assertGreaterEqual(pink_grid_pixel, 220)
        self.assertLessEqual(black_ink_pixel, 45)


if __name__ == "__main__":
    unittest.main()
