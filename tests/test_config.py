"""Synthetic unit tests for T32 configuration integrity and Test-custody isolation (STEP-026)."""

from __future__ import annotations

import copy
import json
import os
import tempfile
import unittest
from pathlib import Path

from src.cvd_mm.config import (
    PREREG_HASHES_PATH,
    parse_yaml_config,
    validate_experiment_config,
)
from src.cvd_mm.dataset import COHORT_MODALITY_SLICES, load_rel0001_partition, split_tabular_by_modality


def _valid_t32_config() -> dict:
    with open(PREREG_HASHES_PATH, encoding="utf-8") as pf:
        prereg = json.load(pf)["files"]
    return {
        "experiment_id": "EXP0000_SMOKE",
        "comparison_block": "SMOKE",
        "research_question_id": "RQ0",
        "comparator_tier": "unimodal",
        "candidate_id": "MC0001",
        "approval_record": "DEC0011",
        "source_commit": "HEAD",
        "data": {
            "release_id": "REL0001",
            "dataset_scope": "DS0004",
            "allow_troponin_tier_b": False,
        },
        "model": {
            "framework": "sklearn",
            "d_model": None,
            "num_layers": None,
            "nhead": None,
            "dim_feedforward": None,
            "dropout": None,
            "max_trainable_params_budget": None,
            "pretrained_weights_sha256": None,
        },
        "training": {
            "seed": 42,
            "deterministic_mode": True,
            "epochs": 5,
            "learning_rate": None,
            "weight_decay": None,
            "early_stopping_patience": None,
            "loss_and_imbalance_policy": "class_weight_balanced_no_smote",
        },
        "evaluation_and_calibration": {
            "validation_only_tuning": True,
            "test_partition_access": "SEALED_UNTIL_G11",
            "bootstrap_resamples": 2000,
            "experiment_plan_sha256": prereg["07_Experiments/experiment_plan.md"],
            "eval_protocol_sha256": prereg["09_Evaluation_Stats/protocol.md"],
            "xai_protocol_sha256": prereg["10_Explainability_XAI/xai_protocol.md"],
        },
        "xai_hooks": {
            "background_partition": "train",
        },
        "runtime": {
            "device": "cpu",
        },
    }


class TestConfigAndCustody(unittest.TestCase):
    def test_valid_config_and_yaml_roundtrip(self) -> None:
        cfg = _valid_t32_config()
        out = validate_experiment_config(cfg, allow_frozen_test_eval=False, verify_prereg_files=True)
        self.assertEqual(out["experiment_id"], "EXP0000_SMOKE")

        yaml_text = """
experiment_id: EXP0001
comparison_block: Block_A
research_question_id: RQ1
comparator_tier: transformer_fusion
candidate_id: MC0015
approval_record: DEC0011
source_commit: abc1234
data:
  release_id: REL0001
  dataset_scope: ALL_COHORTS
  allow_troponin_tier_b: false
model:
  framework: pytorch
  d_model: 64
  num_layers: 2
  nhead: 4
  dim_feedforward: 128
  dropout: 0.1
  max_trainable_params_budget: 250000
  pretrained_weights_sha256: none_from_scratch
training:
  seed: 42
  deterministic_mode: true
  epochs: 25
  learning_rate: 0.001
  weight_decay: 0.0001
  early_stopping_patience: 6
  loss_and_imbalance_policy: train_pos_weight_no_smote
evaluation_and_calibration:
  validation_only_tuning: true
  test_partition_access: SEALED_UNTIL_G11
  bootstrap_resamples: 2000
  experiment_plan_sha256: {exp}
  eval_protocol_sha256: {ev}
  xai_protocol_sha256: {xai}
xai_hooks:
  background_partition: train
runtime:
  device: cuda
""".format(
            exp=cfg["evaluation_and_calibration"]["experiment_plan_sha256"],
            ev=cfg["evaluation_and_calibration"]["eval_protocol_sha256"],
            xai=cfg["evaluation_and_calibration"]["xai_protocol_sha256"],
        )
        parsed = parse_yaml_config(yaml_text)
        validated = validate_experiment_config(parsed)
        self.assertEqual(validated["model"]["d_model"], 64)
        self.assertTrue(validated["training"]["deterministic_mode"])

    def test_null_fields_and_missing_sections_rejected(self) -> None:
        cfg = _valid_t32_config()
        cfg["training"]["seed"] = None
        with self.assertRaisesRegex(ValueError, "CONFIG_NULL_VIOLATION"):
            validate_experiment_config(cfg)

        cfg2 = _valid_t32_config()
        del cfg2["xai_hooks"]
        with self.assertRaisesRegex(ValueError, "CONFIG_MISSING_SECTION"):
            validate_experiment_config(cfg2)

    def test_preregistration_hash_mismatch_rejected(self) -> None:
        cfg = _valid_t32_config()
        cfg["evaluation_and_calibration"]["experiment_plan_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "mismatch"):
            validate_experiment_config(cfg, verify_prereg_files=True)

    def test_leakage_smote_and_unsealed_test_blocked(self) -> None:
        cfg = _valid_t32_config()
        cfg["training"]["loss_and_imbalance_policy"] = "smote_before_split"
        with self.assertRaisesRegex(PermissionError, "LEAKAGE_POLICY_VIOLATION"):
            validate_experiment_config(cfg)

        cfg2 = _valid_t32_config()
        cfg2["evaluation_and_calibration"]["test_partition_access"] = "OPEN"
        with self.assertRaisesRegex(PermissionError, "TEST_CUSTODY_VIOLATION"):
            validate_experiment_config(cfg2, allow_frozen_test_eval=False)

        cfg3 = _valid_t32_config()
        cfg3["xai_hooks"]["background_partition"] = "val"
        with self.assertRaisesRegex(PermissionError, "XAI_LEAKAGE_VIOLATION"):
            validate_experiment_config(cfg3)

    def test_rel0001_test_partition_blocked_and_synthetic_train_loads(self) -> None:
        with self.assertRaisesRegex(PermissionError, "TEST_PARTITION_SEALED"):
            load_rel0001_partition("test")

        # Synthetic temporary REL dir verifying manifest parsing + shard reading + modality slicing
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for p in ("train", "val", "test"):
                (root / p).mkdir(parents=True, exist_ok=True)
                row = {
                    "DS": "DS0004",
                    "y": 1 if p == "train" else 0,
                    "ModalityMask_CELS": [1, 0, 1, 1],
                    "TabularFeatures": [0.1 * i for i in range(25)],
                }
                (root / p / f"rel0001_{p}.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")
            (root / "rel0001_manifest.json").write_text(json.dumps({"partitions": {}}), encoding="utf-8")

            tr = load_rel0001_partition("train", rel_dir=str(root), dataset_scope="DS0004")
            self.assertEqual(len(tr), 1)
            mods = split_tabular_by_modality(tr[0]["TabularFeatures"], "DS0004")
            self.assertEqual(len(mods["clinical"]), len(COHORT_MODALITY_SLICES["DS0004"]["clinical"]))
            self.assertEqual(len(mods["laboratory"]), len(COHORT_MODALITY_SLICES["DS0004"]["laboratory"]))
            self.assertEqual(len(mods["lifestyle"]), len(COHORT_MODALITY_SLICES["DS0004"]["lifestyle"]))

    def test_registered_stage_s11_bundles_all_valid(self) -> None:
        import hashlib
        from src.cvd_mm.config import REPO_ROOT, load_config_file

        exp_root = Path(REPO_ROOT) / "07_Experiments"
        for i in range(1, 21):
            exp_id = f"EXP{i:04d}"
            exp_dir = exp_root / exp_id
            cfg_p = exp_dir / "config.yaml"
            man_p = exp_dir / "run_manifest.json"
            self.assertTrue(cfg_p.is_file(), f"Missing {cfg_p}")
            self.assertTrue(man_p.is_file(), f"Missing {man_p}")
            self.assertTrue((exp_dir / "README.md").is_file(), f"Missing README for {exp_id}")

            cfg = validate_experiment_config(
                load_config_file(str(cfg_p)),
                allow_frozen_test_eval=False,
                verify_prereg_files=True,
            )
            self.assertEqual(cfg["experiment_id"], exp_id)
            manifest = json.loads(man_p.read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "READY")
            self.assertEqual(manifest["test_partition_access"], "SEALED_UNTIL_G11")
            actual_sha = hashlib.sha256(cfg_p.read_bytes()).hexdigest()
            self.assertEqual(manifest["config_sha256"], actual_sha)


if __name__ == "__main__":
    unittest.main()
