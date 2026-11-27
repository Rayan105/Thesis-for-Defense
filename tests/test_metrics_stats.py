"""Analytical unit tests for metrics, Validation calibration custody & statistics (STEP-026)."""

from __future__ import annotations

import unittest

from src.cvd_mm.calibrate import (
    IsotonicCalibrator,
    PlattLogisticCalibrator,
    TemperatureScalingCalibrator,
    select_validation_thresholds,
)
from src.cvd_mm.metrics import compute_all_metrics
from src.cvd_mm.stats import (
    bh_fdr_adjust,
    bootstrap_patient_metric_ci,
    compute_dca_curve,
    delong_paired_roc_test,
    holm_bonferroni_adjust,
    mcnemar_exact_test,
)


class TestMetricsCalibrationStats(unittest.TestCase):
    def test_all_mandatory_metrics_exact(self) -> None:
        # 8 items at threshold 0.5: TP=3, FP=1, FN=1, TN=3
        y_true = [1, 1, 1, 1, 0, 0, 0, 0]
        y_prob = [0.9, 0.8, 0.7, 0.3, 0.6, 0.2, 0.1, 0.05]
        m = compute_all_metrics(y_true, y_prob, threshold=0.5)
        self.assertEqual(m["confusion_matrix"], [[3, 1], [1, 3]])
        self.assertAlmostEqual(m["accuracy"], 0.75, places=6)
        self.assertAlmostEqual(m["precision"], 0.75, places=6)
        self.assertAlmostEqual(m["recall"], 0.75, places=6)
        self.assertAlmostEqual(m["f1"], 0.75, places=6)
        self.assertAlmostEqual(m["specificity"], 0.75, places=6)
        # Positive rank comparisons against 4 negatives: 0.9>4, 0.8>4, 0.7>4, 0.3>3 => U=15/16=0.9375
        self.assertAlmostEqual(m["roc_auc"], 0.9375, places=6)
        self.assertGreater(m["pr_auc"], 0.90)
        self.assertTrue(0.0 <= m["ece_quantile_15"] <= 1.0)
        self.assertGreater(m["brier_skill_score"], 0.0)

    def test_validation_only_calibrator_leakage_guards_and_fit(self) -> None:
        y_val = [1, 1, 1, 0, 0, 0]
        logits = [6.0, 4.0, 2.0, -2.0, -4.0, -6.0]
        probs = [0.95, 0.85, 0.70, 0.25, 0.15, 0.05]

        with self.assertRaisesRegex(PermissionError, "CALIBRATION_LEAKAGE_VIOLATION"):
            TemperatureScalingCalibrator().fit(y_val, logits, split_tags=["val"] * 5 + ["test"])
        with self.assertRaisesRegex(PermissionError, "CALIBRATION_LEAKAGE_VIOLATION"):
            PlattLogisticCalibrator().fit(y_val, logits, split_tags=["train"] * 6)
        with self.assertRaisesRegex(PermissionError, "CALIBRATION_LEAKAGE_VIOLATION"):
            select_validation_thresholds(y_val, probs, split_tags=["test"] * 6)

        val_tags = ["val"] * len(y_val)
        ts = TemperatureScalingCalibrator().fit(y_val, logits, split_tags=val_tags)
        pl = PlattLogisticCalibrator().fit(y_val, logits, split_tags=val_tags)
        iso = IsotonicCalibrator().fit(y_val, probs, split_tags=val_tags)

        cal_iso = iso.transform([0.05, 0.50, 0.95])
        self.assertLessEqual(cal_iso[0], cal_iso[1])
        self.assertLessEqual(cal_iso[1], cal_iso[2])
        self.assertEqual(len(ts.transform(logits)), len(logits))
        self.assertEqual(len(pl.transform(logits)), len(logits))

        thrs = select_validation_thresholds(y_val, probs, split_tags=val_tags, min_sensitivity=0.85)
        sens_achieved = sum(1 for y, p in zip(y_val, probs) if y == 1 and p >= thrs["tau_sens_target"]) / sum(y_val)
        self.assertGreaterEqual(sens_achieved, 0.85)

    def test_dca_delong_mcnemar_bootstrap_and_multiplicity(self) -> None:
        y_true = [1] * 25 + [0] * 25
        # Strong model (AUC=1.0) vs clearly weaker overlapping model (AUC ~0.65)
        prob_a = [0.88 - 0.005 * i for i in range(25)] + [0.12 + 0.005 * i for i in range(25)]
        prob_b = [0.68 - 0.015 * i for i in range(25)] + [0.35 + 0.015 * i for i in range(25)]

        dca = compute_dca_curve(y_true, prob_a, thresholds=[0.1, 0.25, 0.4])
        self.assertEqual(len(dca), 3)
        self.assertGreater(dca[1]["net_benefit_model"], dca[1]["net_benefit_all"])

        dl_diff = delong_paired_roc_test(y_true, prob_a, prob_b)
        self.assertGreater(dl_diff["auc_a"], dl_diff["auc_b"])
        self.assertLess(dl_diff["p_value"], 0.01)

        dl_same = delong_paired_roc_test(y_true, prob_a, prob_a)
        self.assertEqual(dl_same["delta_auc"], 0.0)
        self.assertEqual(dl_same["p_value"], 1.0)

        preds_a = [1] * 24 + [0] + [0] * 24 + [1]
        preds_b = [1] * 14 + [0] * 11 + [0] * 15 + [1] * 10
        mc = mcnemar_exact_test(y_true, preds_a, preds_b)
        self.assertLess(mc["p_value"], 0.01)

        pids = [f"P{i:03d}" for i in range(50)]
        boot = bootstrap_patient_metric_ci(
            y_true,
            pids,
            lambda idxs, _: sum(prob_a[i] >= 0.5 for i in idxs if y_true[i] == 1) / max(1, sum(y_true[i] for i in idxs)),
            n_boot=200,
            seed=42,
        )
        self.assertLessEqual(boot["ci_low"], boot["point"])
        self.assertLessEqual(boot["point"], boot["ci_high"])

        adj_holm = holm_bonferroni_adjust([0.001, 0.04, 0.03])
        self.assertEqual(adj_holm[0], 0.003)
        self.assertGreaterEqual(adj_holm[1], adj_holm[2])
        adj_bh = bh_fdr_adjust([0.001, 0.04, 0.03])
        self.assertLess(adj_bh[0], adj_bh[2])


if __name__ == "__main__":
    unittest.main()
