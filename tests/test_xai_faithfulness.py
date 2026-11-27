"""Synthetic XAI faithfulness, additivity, stability & MNAR shortcut audit tests (STEP-026)."""

from __future__ import annotations

import math
import unittest

from src.cvd_mm.xai import (
    aggregate_modality_shares,
    audit_mnar_shortcut_flags,
    check_shap_additivity,
    evaluate_aopc_faithfulness,
    rank_stability_metrics,
    sample_train_only_background,
)


def _sigmoid(z: float) -> float:
    return 1.0 / (1.0 + math.exp(-max(-50.0, min(50.0, z))))


class TestXAIFaithfulness(unittest.TestCase):
    def test_train_only_background_enforced(self) -> None:
        recs = [{"id": i} for i in range(10)]
        with self.assertRaisesRegex(PermissionError, "XAI_BACKGROUND_LEAKAGE"):
            sample_train_only_background(recs, ["train"] * 9 + ["val"], n_bg=5)
        bg = sample_train_only_background(recs, ["train"] * 10, n_bg=5, seed=42)
        self.assertEqual(len(bg), 5)

    def test_additivity_and_modality_share_normalization(self) -> None:
        add_ok = check_shap_additivity([[0.4, -0.1, 0.2], [0.1, 0.2, 0.3]], base_value=0.25, predictions=[0.75, 0.85])
        self.assertTrue(add_ok["passed"])

        add_bad = check_shap_additivity([[0.1, 0.1, 0.1]], base_value=0.0, predictions=[0.9], tol=0.02)
        self.assertFalse(add_bad["passed"])

        shares = aggregate_modality_shares(
            abs_attributions=[3.0, 1.0, 2.0, 2.0, 5.0],
            modality_slices={"clinical": [0, 1], "ecg": [2], "laboratory": [3], "lifestyle": [4]},
            modality_mask=[1, 1, 1, 0],  # lifestyle masked out -> should receive 0.0%
        )
        self.assertEqual(shares["lifestyle"], 0.0)
        self.assertAlmostEqual(sum(shares.values()), 100.0, places=3)
        self.assertAlmostEqual(shares["clinical"], 50.0, places=3)

    def test_aopc_faithfulness_beats_random_and_reverse_controls(self) -> None:
        # Exact ground-truth monotonic weighted predictor on positive signals with 0 baseline:
        # Weight magnitudes: w = [3.5, 2.0, 0.5, 0.05] -> feature 0 is dominant causal driver!
        weights = [3.5, 2.0, 0.5, 0.05]
        X_eval = [
            [1.0, 0.8, 0.4, 0.2],
            [0.9, 1.0, 0.3, 0.1],
            [1.2, 0.7, 0.5, 0.3],
            [0.8, 0.9, 0.2, 0.4],
        ]
        # True linear Shapley decomposition phi_i = w_i * x_i relative to zero baseline
        phi_eval = [[w * x for w, x in zip(weights, row)] for row in X_eval]

        def predict_fn(batch: list[list[float]]) -> list[float]:
            return [_sigmoid(sum(w * x for w, x in zip(weights, row))) for row in batch]

        res = evaluate_aopc_faithfulness(
            predict_fn=predict_fn,
            X_eval=X_eval,
            phi_eval=phi_eval,
            baseline_vec=[0.0, 0.0, 0.0, 0.0],
            max_k=4,
            seed=42,
        )
        self.assertTrue(res["deletion_beats_random"])
        self.assertTrue(res["deletion_beats_reverse"])
        self.assertTrue(res["insertion_beats_random"])

    def test_stability_and_mnar_shortcut_audit(self) -> None:
        stab = rank_stability_metrics([0.9, 0.5, 0.3, 0.1], [0.85, 0.55, 0.25, 0.05], top_k=2)
        self.assertAlmostEqual(stab["spearman_rho"], 1.0, places=6)
        self.assertAlmostEqual(stab["top_k_jaccard"], 1.0, places=6)

        bad_audit = audit_mnar_shortcut_flags(["age", "crp_isnan", "sbp", "chol"], [0.4, 0.9, 0.3, 0.1], top_k=3)
        self.assertFalse(bad_audit["shortcut_free"])
        self.assertEqual(bad_audit["shortcut_hits_in_top_k"], ["crp_isnan"])

        good_audit = audit_mnar_shortcut_flags(["age", "crp_isnan", "sbp", "chol"], [0.9, 0.02, 0.8, 0.6], top_k=3)
        self.assertTrue(good_audit["shortcut_free"])


if __name__ == "__main__":
    unittest.main()
