"""Immutable Experiment Bundle Generator & Validator (`STEP-028` / Blocks A-F).

Generates schema-compliant `07_Experiments/EXP####/{config.yaml,README.md,run_manifest.json}`
for all 20 preregistered experiments (`EXP0001-EXP0020`) spanning Blocks A-F, verifies
parent hashes against `REL0001` and `preregistration_hashes.json`, confirms `G08` & `G09`
are current PASS, enforces zero test-partition access, and registers `Status=READY` entries
in `07_Experiments/experiment_registry.csv`.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.cvd_mm.config import load_config_file, validate_experiment_config
from src.cvd_mm.dataset import DEFAULT_REL0001_DIR, sha256_file


CANONICAL_SEED = 20261127
CREATED_AT = "2026-11-27T21:58:00+06:00"

EXPERIMENT_MATRIX: list[dict[str, Any]] = [
    # Block A — Tier 1 Unimodal Benchmarks (RQ1 Foundation)
    {"exp": "EXP0001", "block": "Block_A", "rq": "RQ1", "tier": "unimodal", "parent": "None", "mc": "MC0001", "fw": "sklearn", "fw_ver": ">=1.4.0,<1.7.0", "arch": "LogisticRegression_Balanced", "scope": "ALL_COHORTS", "mods": ["clinical", "laboratory", "lifestyle"], "miss": "indicator", "mod_drop": 0.0, "opt": "lbfgs", "sched": "none", "epochs": 1000, "batch": "full_tabular", "policy": "class_weight_balanced_no_smote", "xai": "linear_shap", "enc": ("TabularLinear", "none", "TabularLinear", "TabularLinear"), "fusion": "none", "hw": "kaggle_cpu_or_t4", "hyp": "C=1.0 L2 Logistic baseline on Train-scaled [C,L,S] features"},
    {"exp": "EXP0002", "block": "Block_A", "rq": "RQ1", "tier": "unimodal", "parent": "EXP0001", "mc": "MC0002", "fw": "sklearn", "fw_ver": ">=1.4.0,<1.7.0", "arch": "RandomForest_Balanced300", "scope": "ALL_COHORTS", "mods": ["clinical", "laboratory", "lifestyle"], "miss": "indicator", "mod_drop": 0.0, "opt": "tree_exact", "sched": "none", "epochs": 300, "batch": "full_tabular", "policy": "class_weight_balanced_no_smote", "xai": "tree_shap", "enc": ("RandomForest300", "none", "RandomForest300", "RandomForest300"), "fusion": "none", "hw": "kaggle_cpu_or_t4", "hyp": "300-tree RandomForest with balanced subsample weights captures non-linear interactions"},
    {"exp": "EXP0003", "block": "Block_A", "rq": "RQ1", "tier": "unimodal", "parent": "EXP0001", "mc": "MC0003", "fw": "sklearn", "fw_ver": ">=1.4.0,<1.7.0", "arch": "SVM_RBF_Balanced", "scope": "ALL_COHORTS", "mods": ["clinical", "laboratory", "lifestyle"], "miss": "indicator", "mod_drop": 0.0, "opt": "lbfgs", "sched": "none", "epochs": 1000, "batch": "full_tabular", "policy": "class_weight_balanced_no_smote", "xai": "kernel_shap", "enc": ("SVM_RBF", "none", "SVM_RBF", "SVM_RBF"), "fusion": "none", "hw": "kaggle_cpu_or_t4", "hyp": "RBF Kernel SVM (N<=15K subset/cohort CV) tests smooth margin classification"},
    {"exp": "EXP0004", "block": "Block_A", "rq": "RQ1", "tier": "unimodal", "parent": "EXP0001", "mc": "MC0004", "fw": "xgboost", "fw_ver": ">=2.0.3,<3.0.0", "arch": "XGBoost_Hist_PosWeight", "scope": "ALL_COHORTS", "mods": ["clinical", "laboratory", "lifestyle"], "miss": "indicator", "mod_drop": 0.0, "opt": "hist", "sched": "none", "epochs": 400, "batch": "full_tabular", "policy": "train_pos_weight_no_smote", "xai": "tree_shap", "enc": ("XGBoost400", "none", "XGBoost400", "XGBoost400"), "fusion": "none", "hw": "kaggle_t4_gpu", "hyp": "Primary Tier 1 GBDT tabular anchor trained with exact Train pos_weight"},
    {"exp": "EXP0005", "block": "Block_A", "rq": "RQ1", "tier": "unimodal", "parent": "EXP0004", "mc": "MC0005", "fw": "lightgbm", "fw_ver": ">=4.3.0,<5.0.0", "arch": "LightGBM_Leaf31_PosWeight", "scope": "ALL_COHORTS", "mods": ["clinical", "laboratory", "lifestyle"], "miss": "indicator", "mod_drop": 0.0, "opt": "hist", "sched": "none", "epochs": 400, "batch": "full_tabular", "policy": "train_pos_weight_no_smote", "xai": "tree_shap", "enc": ("LightGBM400", "none", "LightGBM400", "LightGBM400"), "fusion": "none", "hw": "kaggle_cpu_or_t4", "hyp": "Companion GBDT histogram comparator validating tree family stability"},
    {"exp": "EXP0006", "block": "Block_A", "rq": "RQ1", "tier": "unimodal", "parent": "EXP0004", "mc": "MC0006", "fw": "pytorch", "fw_ver": ">=2.1.0,<2.7.0", "arch": "TabularModalityMLP_Unimodal", "scope": "ALL_COHORTS", "mods": ["clinical", "laboratory", "lifestyle"], "miss": "indicator", "mod_drop": 0.0, "opt": "adamw", "sched": "cosine", "epochs": 40, "batch": 256, "policy": "bce_train_pos_weight_no_smote", "xai": "gradient_shap", "enc": ("TabularMLP", "none", "TabularMLP", "TabularMLP"), "fusion": "none", "hw": "kaggle_t4_gpu", "hyp": "Compact neural tabular MLP matching CVDMMTransformer encoder depth"},
    {"exp": "EXP0007", "block": "Block_A", "rq": "RQ1", "tier": "unimodal", "parent": "None", "mc": "MC0007", "fw": "pytorch", "fw_ver": ">=2.1.0,<2.7.0", "arch": "CompactResNet1D_WFDB", "scope": "DS0001", "mods": ["ecg"], "miss": "complete_case", "mod_drop": 0.0, "opt": "adamw", "sched": "cosine", "epochs": 40, "batch": 64, "policy": "bce_train_pos_weight_no_smote", "xai": "gradient_shap", "enc": ("none", "CompactResNet1D", "none", "none"), "fusion": "none", "hw": "kaggle_t4_gpu", "hyp": "12-lead WFDB SE-ResNet-1D achieves strong unimodal ECG discrimination on PTB-XL"},
    {"exp": "EXP0008", "block": "Block_A", "rq": "RQ1", "tier": "unimodal", "parent": "EXP0007", "mc": "MC0008", "fw": "pytorch", "fw_ver": ">=2.1.0,<2.7.0", "arch": "Conv1DBiLSTM_WFDB", "scope": "DS0001", "mods": ["ecg"], "miss": "complete_case", "mod_drop": 0.0, "opt": "adamw", "sched": "cosine", "epochs": 40, "batch": 64, "policy": "bce_train_pos_weight_no_smote", "xai": "gradient_shap", "enc": ("none", "Conv1DBiLSTMEncoder", "none", "none"), "fusion": "none", "hw": "kaggle_t4_gpu", "hyp": "Hybrid Conv1D + Bidirectional LSTM baseline fulfilling proposal LSTM track"},
    {"exp": "EXP0009", "block": "Block_A", "rq": "RQ1", "tier": "unimodal", "parent": "None", "mc": "MC0009", "fw": "pytorch", "fw_ver": ">=2.1.0,<2.7.0", "arch": "CompactCNN2D_PNG", "scope": "DS0002", "mods": ["ecg"], "miss": "complete_case", "mod_drop": 0.0, "opt": "adamw", "sched": "cosine", "epochs": 40, "batch": 32, "policy": "bce_train_pos_weight_no_smote", "xai": "gradient_shap", "enc": ("none", "CompactCNN2DPNG", "none", "none"), "fusion": "none", "hw": "kaggle_t4_gpu", "hyp": "EPV-safe depthwise 2D-CNN isolates diagnostic QRS signal from DS0002 paper ECG scans"},
    {"exp": "EXP0010", "block": "Block_A", "rq": "RQ1", "tier": "unimodal", "parent": "EXP0007", "mc": "MC0010", "fw": "pytorch", "fw_ver": ">=2.1.0,<2.7.0", "arch": "ECGPatchTransformer_WFDB", "scope": "DS0001", "mods": ["ecg"], "miss": "complete_case", "mod_drop": 0.0, "opt": "adamw", "sched": "cosine", "epochs": 40, "batch": 64, "policy": "bce_train_pos_weight_no_smote", "xai": "gradient_shap", "enc": ("none", "ECGPatchTransformer", "none", "none"), "fusion": "none", "hw": "kaggle_t4_gpu", "hyp": "Self-attention ECG patch tokenizer decouples within-ECG attention from cross-modal fusion"},
    # Block B — Tier 2 Clinical Risk Score Context
    {"exp": "EXP0011", "block": "Block_B", "rq": "RQ1", "tier": "clinical_score", "parent": "EXP0001", "mc": "MC0011", "fw": "custom_score", "fw_ver": "v1.0.0", "arch": "WHOFraminghamContextScorer", "scope": "ALL_COHORTS", "mods": ["clinical", "laboratory", "lifestyle"], "miss": "indicator", "mod_drop": 0.0, "opt": "none", "sched": "none", "epochs": 1, "batch": "full_tabular", "policy": "no_training_calibrated_on_val", "xai": "linear_shap", "enc": ("FraminghamWHO_Covariates", "none", "FraminghamWHO_Covariates", "FraminghamWHO_Covariates"), "fusion": "none", "hw": "local_cpu", "hyp": "Interpretable clinical baseline sets diagnostic context bar on DS0003/DS0004"},
    # Block C — Tier 3 Simple Fusion vs Tier 4 CVD-MM-Transformer (RQ1 Primary Test)
    {"exp": "EXP0012", "block": "Block_C", "rq": "RQ1", "tier": "simple_fusion", "parent": "EXP0004", "mc": "MC0012", "fw": "xgboost", "fw_ver": ">=2.0.3,<3.0.0", "arch": "EarlyConcat_XGB_MLP", "scope": "ALL_COHORTS", "mods": ["clinical", "ecg", "laboratory", "lifestyle"], "miss": "zero_fill", "mod_drop": 0.0, "opt": "hist", "sched": "none", "epochs": 400, "batch": "full_tabular", "policy": "train_pos_weight_no_smote", "xai": "tree_shap", "enc": ("XGB_EarlyConcat", "ResNet1D_Embed", "XGB_EarlyConcat", "XGB_EarlyConcat"), "fusion": "early_concat", "hw": "kaggle_t4_gpu", "hyp": "Early feature concatenation establishes non-attention multimodal fusion baseline"},
    {"exp": "EXP0013", "block": "Block_C", "rq": "RQ1", "tier": "simple_fusion", "parent": "EXP0012", "mc": "MC0013", "fw": "sklearn", "fw_ver": ">=1.4.0,<1.7.0", "arch": "LateOOFStacker", "scope": "ALL_COHORTS", "mods": ["clinical", "ecg", "laboratory", "lifestyle"], "miss": "indicator", "mod_drop": 0.0, "opt": "lbfgs", "sched": "none", "epochs": 80, "batch": "full_tabular", "policy": "class_weight_balanced_no_smote", "xai": "linear_shap", "enc": ("UnimodalProb_C", "UnimodalProb_E", "UnimodalProb_L", "UnimodalProb_S"), "fusion": "late_stacking", "hw": "kaggle_cpu_or_t4", "hyp": "Level-1 OOF logit stacker quantifies multimodal gain without cross-modal feature interaction"},
    {"exp": "EXP0014", "block": "Block_C", "rq": "RQ1", "tier": "simple_fusion", "parent": "EXP0013", "mc": "MC0014", "fw": "pytorch", "fw_ver": ">=2.1.0,<2.7.0", "arch": "GatedAttentionFusionNet", "scope": "ALL_COHORTS", "mods": ["clinical", "ecg", "laboratory", "lifestyle"], "miss": "key_padding_mask", "mod_drop": 0.15, "opt": "adamw", "sched": "cosine", "epochs": 40, "batch": 128, "policy": "bce_train_pos_weight_no_smote", "xai": "gradient_shap", "enc": ("TabularModalityMLP", "CompactResNet1D", "TabularModalityMLP", "TabularModalityMLP"), "fusion": "gated_attention", "hw": "kaggle_t4_gpu", "hyp": "Sigmoid gated fusion compares scalar attention weighting against multi-head Transformer fusion"},
    {"exp": "EXP0015", "block": "Block_C", "rq": "RQ1", "tier": "transformer_fusion", "parent": "EXP0014", "mc": "MC0015", "fw": "pytorch", "fw_ver": ">=2.1.0,<2.7.0", "arch": "CVDMMTransformer", "scope": "ALL_COHORTS", "mods": ["clinical", "ecg", "laboratory", "lifestyle"], "miss": "key_padding_mask", "mod_drop": 0.15, "opt": "adamw", "sched": "cosine", "epochs": 40, "batch": 128, "policy": "bce_train_pos_weight_no_smote", "xai": "gradient_shap", "enc": ("TabularModalityMLP", "CompactResNet1D_and_CNN2D", "TabularModalityMLP", "TabularModalityMLP"), "fusion": "cross_modal_transformer_fusion", "hw": "kaggle_t4_gpu", "hyp": "Proposed CVDMMTransformer outperforms unimodal & simple fusion comparators on AUROC, PR-AUC & DCA"},
    # Block D — Progressive & LOMO Modality Ablations (RQ2 / PG4)
    {"exp": "EXP0016", "block": "Block_D", "rq": "RQ2", "tier": "ablation", "parent": "EXP0004", "mc": "MC0004", "fw": "xgboost", "fw_ver": ">=2.0.3,<3.0.0", "arch": "ProgressiveModalGain_CLS", "scope": "ALL_COHORTS", "mods": ["clinical", "ecg", "laboratory", "lifestyle"], "miss": "indicator", "mod_drop": 0.0, "opt": "hist", "sched": "none", "epochs": 400, "batch": "full_tabular", "policy": "train_pos_weight_no_smote", "xai": "tree_shap", "enc": ("XGBoost_C", "CNN2D_DS0002", "XGBoost_CL", "XGBoost_CLS"), "fusion": "early_concat", "hw": "kaggle_t4_gpu", "hyp": "Adding Laboratory (L) and Structured Lifestyle (S) yields significant incremental AUROC & Net Benefit"},
    {"exp": "EXP0017", "block": "Block_D", "rq": "RQ2", "tier": "ablation", "parent": "EXP0015", "mc": "MC0015", "fw": "pytorch", "fw_ver": ">=2.1.0,<2.7.0", "arch": "CVDMMTransformer_LOMO", "scope": "ALL_COHORTS", "mods": ["clinical", "ecg", "laboratory", "lifestyle"], "miss": "key_padding_mask", "mod_drop": 0.15, "opt": "adamw", "sched": "cosine", "epochs": 40, "batch": 128, "policy": "bce_train_pos_weight_no_smote", "xai": "gradient_shap", "enc": ("TabularModalityMLP", "CompactResNet1D_and_CNN2D", "TabularModalityMLP", "TabularModalityMLP"), "fusion": "cross_modal_transformer_fusion", "hw": "kaggle_t4_gpu", "hyp": "Leave-One-Modality-Out performance drops correlate positively with mean modality |SHAP| shares"},
    # Block E — Architectural & Incorporation-Bias Sensitivity Ablations (RQ1 / PROBAST)
    {"exp": "EXP0018", "block": "Block_E", "rq": "RQ1", "tier": "ablation", "parent": "EXP0015", "mc": "MC0015", "fw": "pytorch", "fw_ver": ">=2.1.0,<2.7.0", "arch": "CVDMMTransformer_NoKeyMask", "scope": "ALL_COHORTS", "mods": ["clinical", "ecg", "laboratory", "lifestyle"], "miss": "zero_fill", "mod_drop": 0.15, "opt": "adamw", "sched": "cosine", "epochs": 40, "batch": 128, "policy": "bce_train_pos_weight_no_smote", "xai": "gradient_shap", "enc": ("TabularModalityMLP", "CompactResNet1D_and_CNN2D", "TabularModalityMLP", "TabularModalityMLP"), "fusion": "cross_modal_transformer_fusion", "hw": "kaggle_t4_gpu", "hyp": "Explicit ~ModalityMask_CELS padding improves robustness over naive zero-padding"},
    {"exp": "EXP0019", "block": "Block_E", "rq": "RQ3", "tier": "ablation", "parent": "EXP0015", "mc": "MC0015", "fw": "pytorch", "fw_ver": ">=2.1.0,<2.7.0", "arch": "CVDMMTransformer_PROBAST_Sens", "scope": "DS0002", "mods": ["clinical", "ecg", "laboratory"], "miss": "key_padding_mask", "mod_drop": 0.15, "opt": "adamw", "sched": "cosine", "epochs": 40, "batch": 32, "policy": "bce_train_pos_weight_no_smote", "xai": "gradient_shap", "enc": ("TabularModalityMLP", "CompactCNN2DPNG", "TabularModalityMLP", "none"), "fusion": "cross_modal_transformer_fusion", "hw": "kaggle_t4_gpu", "allow_trop": True, "hyp": "Incorporation-bias audit compares primary Tier A vs exploratory Tier B Troponin & CABG/FH sensitivity"},
    # Block F — Multi-Seed Variance & Missing-Modality Stress Tests (RQ4)
    {"exp": "EXP0020", "block": "Block_F", "rq": "RQ4", "tier": "ablation", "parent": "EXP0015", "mc": "MC0015", "fw": "pytorch", "fw_ver": ">=2.1.0,<2.7.0", "arch": "CVDMMTransformer_MultiSeed_Stress", "scope": "ALL_COHORTS", "mods": ["clinical", "ecg", "laboratory", "lifestyle"], "miss": "key_padding_mask", "mod_drop": 0.15, "opt": "adamw", "sched": "cosine", "epochs": 40, "batch": 128, "policy": "bce_train_pos_weight_no_smote", "xai": "gradient_shap", "enc": ("TabularModalityMLP", "CompactResNet1D_and_CNN2D", "TabularModalityMLP", "TabularModalityMLP"), "fusion": "cross_modal_transformer_fusion", "hw": "kaggle_t4_gpu", "hyp": "Champion retains graceful degradation under 10-100% synthetic masking & DS0002 [MISSING_ECG] across 5 seeds"},
]


def _git_head_short() -> str:
    try:
        res = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "--short", "HEAD"],
            check=True, capture_output=True, text=True,
        )
        return res.stdout.strip()
    except Exception:
        return "HEAD"


def _assert_gates_current() -> None:
    gates_csv = REPO_ROOT / "01_Project_Management" / "gates.csv"
    outcomes: dict[str, str] = {}
    with open(gates_csv, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            outcomes[row["GateID"]] = row["Outcome"].strip()
    for required in ("G02", "G03", "G04", "G05", "G06", "G07", "G08", "G09"):
        if outcomes.get(required) != "PASS":
            raise RuntimeError(f"Gate {required} must be PASS before STEP-028 registration, got {outcomes.get(required)}")


def _yaml_scalar(v: Any) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        return "[" + ", ".join(str(x) for x in v) + "]"
    s = str(v)
    if any(ch in s for ch in (":", ">", "<", "#", ";")) or s == "":
        return f'"{s}"'
    return s


def _render_yaml(row: dict[str, Any], hashes: dict[str, str], commit_sha: str) -> str:
    is_dl = row["fw"] == "pytorch"
    d_model = 64 if is_dl else None
    num_layers = 2 if is_dl else None
    nhead = 4 if is_dl else None
    dim_ff = 128 if is_dl else None
    dropout = 0.1 if is_dl else None
    budget = 250000 if is_dl else None
    pt_sha = "none_from_scratch" if is_dl else None
    lr = 0.001 if is_dl else None
    wd = 0.0001 if is_dl else None
    patience = 7 if is_dl else None
    allow_trop = bool(row.get("allow_trop", False))
    c_enc, e_enc, l_enc, s_enc = row["enc"]

    lines = [
        f"# Immutable Experiment Configuration Bundle ({row['exp']} — STEP-028 / {row['block']})",
        "# Preregistered against experiment_plan.md & SEALED Test custody (Gate G11).",
        "",
        f"experiment_id: {row['exp']}",
        f"comparison_block: {row['block']}",
        f"research_question_id: {row['rq']}",
        f"comparator_tier: {row['tier']}",
        f"candidate_id: {row['mc']}",
        'approval_record: "DEC0009; DEC0010; DEC0011; DEC0012"',
        f"source_commit: {commit_sha}",
        "",
        "data:",
        "  release_id: REL0001",
        f"  dataset_scope: {row['scope']}",
        "  adjudication_ids: [ADJ0001, ADJ0002, ADJ0003, ADJ0004]",
        "  split_id: SPLIT0001",
        f"  split_manifest_sha256: {hashes['split_manifest_sha256']}",
        "  preprocessing_id: PP0001",
        f"  fit_state_sha256: {hashes['fit_state_sha256']}",
        f"  variables_sha256: {hashes['variables_sha256']}",
        f"  active_modalities: {_yaml_scalar(row['mods'])}",
        f"  missing_modality_policy: {row['miss']}",
        f"  modality_dropout_prob: {row['mod_drop']}",
        f"  allow_troponin_tier_b: {_yaml_scalar(allow_trop)}",
        "",
        "model:",
        f"  framework: {row['fw']}",
        f'  framework_version: "{row["fw_ver"]}"',
        f"  architecture_name: {row['arch']}",
        f"  d_model: {_yaml_scalar(d_model)}",
        f"  num_layers: {_yaml_scalar(num_layers)}",
        f"  nhead: {_yaml_scalar(nhead)}",
        f"  dim_feedforward: {_yaml_scalar(dim_ff)}",
        f"  dropout: {_yaml_scalar(dropout)}",
        f"  max_trainable_params_budget: {_yaml_scalar(budget)}",
        "  modality_encoders:",
        f"    clinical: {c_enc}",
        f"    ecg: {e_enc}",
        f"    laboratory: {l_enc}",
        f"    lifestyle: {s_enc}",
        f"  fusion_module: {row['fusion']}",
        f"  pretrained_weights_sha256: {_yaml_scalar(pt_sha)}",
        "  license_record: MIT_Custom_Project",
        "",
        "training:",
        f"  seed: {CANONICAL_SEED}",
        "  deterministic_mode: true",
        f"  max_epochs_or_estimators: {row['epochs']}",
        f"  batch_size: {row['batch']}",
        f"  learning_rate: {_yaml_scalar(lr)}",
        f"  weight_decay: {_yaml_scalar(wd)}",
        f"  scheduler: {row['sched']}",
        f"  optimizer: {row['opt']}",
        f"  loss_and_imbalance_policy: {row['policy']}",
        f"  early_stopping_patience: {_yaml_scalar(patience)}",
        "  early_stopping_monitor: val_roc_auc",
        "",
        "evaluation_and_calibration:",
        f"  experiment_plan_sha256: {hashes['experiment_plan_sha256']}",
        f"  eval_protocol_sha256: {hashes['eval_protocol_sha256']}",
        f"  xai_protocol_sha256: {hashes['xai_protocol_sha256']}",
        "  validation_only_tuning: true",
        "  test_partition_access: SEALED_UNTIL_G11",
        "  calibration_candidates: [uncalibrated, temperature, platt, isotonic]",
        "  threshold_rule: youden_j",
        "  bootstrap_resamples: 2000",
        "  mandatory_metrics: [accuracy, precision, recall, f1, roc_auc, confusion_matrix]",
        "  adopted_q1_metrics: [pr_auc, specificity, npv, balanced_accuracy, mcc, brier_score, ece, calibration_slope, calibration_intercept, dca]",
        "",
        "xai_hooks:",
        "  execute_in_step: STEP-038_TO_040_ONLY",
        f"  explainer_type: {row['xai']}",
        "  background_partition: train",
        "  background_sample_size: 256",
        "  additivity_error_tol: 0.02",
        "",
        "runtime:",
        "  environment_lock_path: environment/model/requirements.txt",
        f"  environment_lock_sha256: {hashes['environment_lock_sha256']}",
        f"  hardware_target: {row['hw']}",
        "  checkpoint_policy: best_val_roc_auc_and_loss",
        f"  artifact_destination: 08_Checkpoints/binaries/{row['exp']}",
        "",
    ]
    return "\n".join(lines)


def _render_readme(row: dict[str, Any], cfg_sha: str, commit_sha: str) -> str:
    mods_str = ", ".join(row["mods"])
    return "\n".join([
        f"# {row['exp']} — {row['arch']} (`{row['block']}`)",
        "",
        "| Field | Value |",
        "|---|---|",
        "| TemplateID | T16 (experiment.md) |",
        "| template_version | v1.0.0 |",
        f"| entity_id | `{row['exp']}` |",
        "| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |",
        "| date | `2026-11-27` |",
        "| status | **`READY`** (`STEP-028` Pre-Launch Immutable Bundle Verified) |",
        f"| source_inputs | `REL0001` (`Train/Val` Only — Test Sealed until `G11`) |",
        "| governing_section | OS §6.2, §11, §15.2 |",
        "| phi_sensitivity | Tier 1 (Public / Git-safe config & manifest) |",
        "| reviewer | Md. Mizanur Rahman |",
        "",
        "---",
        "",
        "## 1. Scientific Objective",
        f"- **Experiment ID:** `{row['exp']}`",
        f"- **Research Question:** `{row['rq']}` | **Block:** `{row['block']}`",
        f"- **Comparator Tier:** `{row['tier']}` | **Parent Baseline:** `{row['parent']}`",
        f"- **Active Modalities:** `{mods_str}` (`missing_modality_policy={row['miss']}`)",
        f"- **Primary Hypothesis:** {row['hyp']}.",
        "",
        "## 2. Data & Model Setup",
        "- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`)",
        f"- **Model Candidate:** `{row['mc']}` (`{row['arch']}` / `{row['fw']}`)",
        f"- **Config Path:** [config.yaml](./config.yaml)",
        f"- **Config SHA-256:** `{cfg_sha}`",
        f"- **Source Git Commit:** `{commit_sha}`",
        "",
        "## 3. Pre-Launch Custody & Execution Targets",
        f"- **Canonical Primary Seed:** `{CANONICAL_SEED}` (Block F expands across `[20261127..20261201]`)",
        f"- **Hardware Target:** `{row['hw']}` | **Tier 3 Artifact Path:** `08_Checkpoints/binaries/{row['exp']}`",
        "- **Test Partition Status:** Strictly `SEALED_UNTIL_G11` (`0` Test reads permitted in Stage S11).",
        "- **Execution Status:** Registered `READY` for `STEP-029` training launch via Kaggle GPU / CLI.",
        "",
    ])


def main() -> int:
    _assert_gates_current()
    commit_sha = _git_head_short()

    with open(Path(DEFAULT_REL0001_DIR) / "rel0001_manifest.json", encoding="utf-8") as mf:
        rel_man = json.load(mf)
    with open(REPO_ROOT / "07_Experiments" / "preregistration_hashes.json", encoding="utf-8") as pf:
        prereg = json.load(pf)["files"]

    hashes = {
        "split_manifest_sha256": rel_man["lineage"]["split_manifest_sha256"],
        "fit_state_sha256": rel_man["lineage"]["fit_state_hash"],
        "variables_sha256": rel_man["lineage"]["variables_hash"],
        "experiment_plan_sha256": prereg["07_Experiments/experiment_plan.md"],
        "eval_protocol_sha256": prereg["09_Evaluation_Stats/protocol.md"],
        "xai_protocol_sha256": prereg["10_Explainability_XAI/xai_protocol.md"],
        "environment_lock_sha256": sha256_file(str(REPO_ROOT / "environment" / "model" / "requirements.txt")),
    }
    assert hashes["variables_sha256"] == sha256_file(str(REPO_ROOT / "04_Outcome_Schema_QA" / "variables.csv"))

    schema = json.loads((REPO_ROOT / "07_Experiments" / "configs" / "exp_t32_schema_v1.json").read_text(encoding="utf-8"))

    reg_path = REPO_ROOT / "07_Experiments" / "experiment_registry.csv"
    with open(reg_path, encoding="utf-8", newline="") as rf:
        rows_existing = list(csv.reader(rf))
    header = rows_existing[0]
    preserved_rows = [r for r in rows_existing[1:] if r and r[0] == "EXP0000_SMOKE"]

    new_csv_rows: list[list[str]] = []
    for row in EXPERIMENT_MATRIX:
        exp_dir = REPO_ROOT / "07_Experiments" / row["exp"]
        exp_dir.mkdir(parents=True, exist_ok=True)
        cfg_path = exp_dir / "config.yaml"
        cfg_text = _render_yaml(row, hashes, commit_sha)
        cfg_path.write_text(cfg_text, encoding="utf-8")

        parsed = load_config_file(str(cfg_path))
        validated = validate_experiment_config(parsed, allow_frozen_test_eval=False, verify_prereg_files=True)
        for req_top in schema["required"]:
            assert req_top in validated, f"Missing schema section {req_top} in {row['exp']}"

        cfg_sha = sha256_file(str(cfg_path))
        readme_path = exp_dir / "README.md"
        readme_path.write_text(_render_readme(row, cfg_sha, commit_sha), encoding="utf-8")

        manifest = {
            "experiment_id": row["exp"],
            "comparison_block": row["block"],
            "research_question_id": row["rq"],
            "comparator_tier": row["tier"],
            "parent_baseline_exp": row["parent"],
            "candidate_id": row["mc"],
            "active_modalities": row["mods"],
            "config_path": f"07_Experiments/{row['exp']}/config.yaml",
            "config_sha256": cfg_sha,
            "source_commit": commit_sha,
            "seed": CANONICAL_SEED,
            "gates_verified_current": ["G02", "G03", "G04", "G05", "G06", "G07", "G08", "G09"],
            "test_partition_access": "SEALED_UNTIL_G11",
            "status": "READY",
            "registered_at": CREATED_AT,
        }
        (exp_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        new_csv_rows.append([
            row["exp"],
            row["rq"],
            row["block"],
            row["tier"],
            row["parent"],
            "; ".join(row["mods"]),
            "REL0001",
            row["mc"],
            f"07_Experiments/{row['exp']}/config.yaml",
            cfg_sha,
            commit_sha,
            str(CANONICAL_SEED),
            "Pending_STEP029",
            "Pending",
            "Pending",
            "Pending",
            "Pending",
            "Pending",
            "Pending",
            "None",
            f"Pre-launch validated READY ({row['hyp']})",
            "Rayan Ahmed",
            "v1.0.0",
            "READY",
            CREATED_AT,
            CREATED_AT,
            f"07_Experiments/{row['exp']}/README.md",
        ])

    with open(reg_path, "w", encoding="utf-8", newline="") as wf:
        writer = csv.writer(wf)
        writer.writerow(header)
        writer.writerows(preserved_rows)
        writer.writerows(new_csv_rows)

    print(f"Registered & validated {len(new_csv_rows)} immutable Stage S11 bundles (EXP0001..EXP0020) at commit {commit_sha}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
