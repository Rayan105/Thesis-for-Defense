"""Synthetic unit tests for missing-modality masking, zero-NaN safety & checkpoint recovery (STEP-026)."""

from __future__ import annotations

import itertools
import math
import tempfile
import unittest
from pathlib import Path

from src.cvd_mm.models import (
    LateOOFStacker,
    PurePythonLogisticModel,
    PurePythonMaskedFusionModel,
    WHOFraminghamContextScorer,
    build_cels_key_padding_mask,
    load_checkpoint_bundle,
    train_pure_python_logistic_with_checkpoints,
)


class TestModelsAndMasking(unittest.TestCase):
    def test_cels_key_padding_mask_preserves_cls(self) -> None:
        # Even when all 4 modalities are absent ([0,0,0,0]), [CLS] stays False (unmasked)
        m = build_cels_key_padding_mask([0, 0, 0, 0])
        self.assertEqual(m, [False, True, True, True, True])
        self.assertEqual(build_cels_key_padding_mask([1, 0, 1, 1]), [False, False, True, False, False])

    def test_masked_fusion_zero_nan_across_all_16_mask_patterns(self) -> None:
        cohort_dims = {
            "DS0004": {"clinical": 15, "laboratory": 4, "lifestyle": 6},
        }
        model = PurePythonMaskedFusionModel(cohort_dims, d_model=16, ecg_dim=16, seed=42)
        base_inputs = {
            "clinical": [0.2 * (i + 1) for i in range(15)],
            "ecg": [-0.1 * (i + 1) for i in range(16)],
            "laboratory": [0.5, 0.0, -0.4, 0.0],
            "lifestyle": [0.1, 0.0, 1.0, 0.0, 0.2, 0.0],
        }

        for bits in itertools.product([0, 1], repeat=4):
            mask = list(bits)
            out = model.forward("DS0004", base_inputs, mask)
            self.assertFalse(math.isnan(out["logit"]) or math.isinf(out["logit"]))
            self.assertTrue(0.0 < out["prob"] < 1.0)
            weights = out["attention_weights"]
            self.assertAlmostEqual(sum(weights), 1.0, places=6)
            for idx, m_bit in enumerate(mask):
                if m_bit == 0:
                    self.assertEqual(weights[idx + 1], 0.0)

        # Invariance check: mutating a masked modality ([1, 0, 1, 0] -> mutate ECG & lifestyle)
        # MUST NOT change the predicted probability or logit at all!
        mask_ce_ls_off = [1, 0, 1, 0]
        ref_out = model.forward("DS0004", base_inputs, mask_ce_ls_off)
        corrupted_inputs = dict(base_inputs)
        corrupted_inputs["ecg"] = [9999.0] * 16
        corrupted_inputs["lifestyle"] = [-9999.0] * 6
        pert_out = model.forward("DS0004", corrupted_inputs, mask_ce_ls_off)
        self.assertAlmostEqual(ref_out["logit"], pert_out["logit"], places=12)
        self.assertAlmostEqual(ref_out["prob"], pert_out["prob"], places=12)

    def test_logistic_convergence_and_deterministic_checkpoint_resume(self) -> None:
        X_train = [[2.0, 1.5], [1.8, 1.2], [2.5, 2.0], [-2.0, -1.5], [-1.8, -1.1], [-2.4, -2.0]] * 8
        y_train = [1, 1, 1, 0, 0, 0] * 8
        X_val = [[1.9, 1.0], [2.1, 1.8], [-1.7, -1.2], [-2.2, -1.9]]
        y_val = [1, 1, 0, 0]

        with tempfile.TemporaryDirectory() as tmp1, tempfile.TemporaryDirectory() as tmp2:
            full_run = train_pure_python_logistic_with_checkpoints(
                X_train=X_train,
                y_train=y_train,
                X_val=X_val,
                y_val=y_val,
                checkpoint_dir=tmp1,
                exp_id="EXP0000_SMOKE",
                candidate_id="MC0001",
                config_hash="abc",
                epochs=6,
                lr=0.2,
                seed=42,
            )
            self.assertGreaterEqual(full_run["best_val_roc_auc"], 0.99)

            # Stop at epoch 3, verify tamper check, then resume to epoch 6
            part1 = train_pure_python_logistic_with_checkpoints(
                X_train=X_train,
                y_train=y_train,
                X_val=X_val,
                y_val=y_val,
                checkpoint_dir=tmp2,
                exp_id="EXP0000_SMOKE",
                candidate_id="MC0001",
                config_hash="abc",
                epochs=3,
                lr=0.2,
                seed=42,
            )
            resumed = train_pure_python_logistic_with_checkpoints(
                X_train=X_train,
                y_train=y_train,
                X_val=X_val,
                y_val=y_val,
                checkpoint_dir=tmp2,
                exp_id="EXP0000_SMOKE",
                candidate_id="MC0001",
                config_hash="abc",
                epochs=6,
                lr=0.2,
                seed=42,
                resume_from=part1["last_checkpoint"],
            )
            self.assertEqual(full_run["model"].weights, resumed["model"].weights)
            self.assertEqual(full_run["model"].bias, resumed["model"].bias)

            # Corrupt checkpoint payload to verify SHA-256 tamper protection
            import json
            ckpt_p = Path(resumed["last_checkpoint"])
            env = json.loads(ckpt_p.read_text(encoding="utf-8"))
            env["payload"]["epoch"] = 999
            ckpt_p.write_text(json.dumps(env, indent=2), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Checkpoint corruption"):
                load_checkpoint_bundle(ckpt_p, verify_checksum=True)

    def test_clinical_scorer_and_oof_stacker(self) -> None:
        scorer = WHOFraminghamContextScorer()
        probs = scorer.predict_proba([
            {"age_z": 1.8, "sbp_z": 1.5, "smoke": 1.0, "male": 1.0},
            {"age_z": -1.5, "sbp_z": -1.2, "smoke": 0.0, "male": 0.0},
        ])
        self.assertGreater(probs[0], probs[1])

        stacker = LateOOFStacker(n_modalities=4, seed=42)
        oof = [[0.85, 0.80, 0.0, 0.70], [0.90, 0.0, 0.80, 0.75], [0.15, 0.20, 0.10, 0.20], [0.10, 0.15, 0.0, 0.15]] * 4
        masks = [[1, 1, 0, 1], [1, 0, 1, 1], [1, 1, 1, 1], [1, 1, 0, 1]] * 4
        y = [1, 1, 0, 0] * 4
        stacker.fit(oof, masks, y)
        preds = stacker.predict_proba([[0.88, 0.85, 0.0, 0.80], [0.12, 0.15, 0.0, 0.10]], [[1, 1, 0, 1], [1, 1, 0, 1]])
        self.assertGreater(preds[0], preds[1])

    def test_cli_run_from_config_end_to_end_synthetic(self) -> None:
        import importlib.util
        import json
        from src.cvd_mm.config import PREREG_HASHES_PATH

        spec = importlib.util.spec_from_file_location("run_experiment", r"e:\FYDP\14_Automation\run_experiment.py")
        mod = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(mod)

        with open(PREREG_HASHES_PATH, encoding="utf-8") as pf:
            prereg = json.load(pf)["files"]

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rel = root / "REL0001"
            for part in ("train", "val", "test"):
                (rel / part).mkdir(parents=True, exist_ok=True)
                lines = []
                for idx in range(12):
                    y_val = 1 if idx < 6 else 0
                    feat0 = 1.5 if y_val == 1 else -1.5
                    row = {
                        "DS": "DS0004",
                        "y": y_val,
                        "ModalityMask_CELS": [1, 0, 1, 1],
                        "TabularFeatures": [feat0] + [0.1 * (idx % 3)] * 24,
                    }
                    lines.append(json.dumps(row))
                (rel / part / f"rel0001_{part}.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
            (rel / "rel0001_manifest.json").write_text(json.dumps({"partitions": {}}), encoding="utf-8")

            cfg_p = root / "smoke.json"
            cfg_p.write_text(json.dumps({
                "experiment_id": "EXP0000_SMOKE",
                "comparison_block": "SMOKE",
                "research_question_id": "RQ0",
                "comparator_tier": "unimodal",
                "candidate_id": "MC0001",
                "approval_record": "DEC0011",
                "source_commit": "HEAD",
                "data": {"release_id": "REL0001", "dataset_scope": "DS0004", "allow_troponin_tier_b": False},
                "model": {
                    "framework": "sklearn", "d_model": None, "num_layers": None, "nhead": None,
                    "dim_feedforward": None, "dropout": None, "max_trainable_params_budget": None,
                    "pretrained_weights_sha256": None,
                },
                "training": {
                    "seed": 42, "deterministic_mode": True, "epochs": 4, "learning_rate": None,
                    "weight_decay": None, "early_stopping_patience": None,
                    "loss_and_imbalance_policy": "train_pos_weight_no_smote",
                },
                "evaluation_and_calibration": {
                    "validation_only_tuning": True,
                    "test_partition_access": "SEALED_UNTIL_G11",
                    "bootstrap_resamples": 2000,
                    "experiment_plan_sha256": prereg["07_Experiments/experiment_plan.md"],
                    "eval_protocol_sha256": prereg["09_Evaluation_Stats/protocol.md"],
                    "xai_protocol_sha256": prereg["10_Explainability_XAI/xai_protocol.md"],
                },
                "xai_hooks": {"background_partition": "train"},
                "runtime": {"device": "cpu"},
            }), encoding="utf-8")

            res = mod.run_from_config(
                str(cfg_p),
                rel_dir=str(rel),
                checkpoint_dir=str(root / "ckpts"),
                output_dir=str(root / "out"),
            )
            self.assertFalse(res["test_partition_accessed"])
            self.assertGreaterEqual(res["best_val_roc_auc"], 0.9)
            self.assertTrue(Path(res["report_path"]).is_file())


if __name__ == "__main__":
    unittest.main()
