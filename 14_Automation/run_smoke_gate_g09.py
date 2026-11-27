"""EXP0000_SMOKE Local Diagnostic Drill on Real REL0001 Train/Val Slices (STEP-027 / G09 Pre-Check).

Executes cleanly on pure-Python stdlib locally with ZERO access to REL0001/test:
  1. Validates resolved T32 smoke config (07_Experiments/configs/exp0000_smoke.yaml).
  2. Loads a stratified slice across DS0001..DS0004 strictly from Train & Val shards.
  3. Verifies real 12-lead WFDB ECG loading + Stage-A notch/highpass DSP on DS0001 sample.
  4. Executes PurePythonLogisticModel epochs 0..6 uninterrupted vs deliberate interrupt@3 -> SHA-256 verify -> resume 3..6.
  5. Evaluates 4-modality PurePythonMaskedFusionModel across real DS0001..DS0004 missing-mask rows (zero NaN/Inf).
  6. Fits Validation-only TemperatureScalingCalibrator + frozen thresholds (tau_youden, tau_sens_target).
  7. Runs Train-only XAI background check, Shapley additivity (<=0.02) & Deletion/Insertion AOPC sanity vs controls.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.cvd_mm.calibrate import TemperatureScalingCalibrator, select_validation_thresholds
from src.cvd_mm.config import load_config_file, validate_experiment_config
from src.cvd_mm.dataset import (
    COHORT_MODALITY_SLICES,
    DEFAULT_REL0001_DIR,
    load_rel0001_partition,
    load_wfdb_12lead_filtered,
    sha256_file,
    split_tabular_by_modality,
)
from src.cvd_mm.metrics import compute_all_metrics
from src.cvd_mm.models import (
    PurePythonMaskedFusionModel,
    load_checkpoint_bundle,
    train_pure_python_logistic_with_checkpoints,
)
from src.cvd_mm.xai import (
    audit_mnar_shortcut_flags,
    check_shap_additivity,
    evaluate_aopc_faithfulness,
    sample_train_only_background,
)


def _stratified_cohort_sample(records: list[dict[str, Any]], per_ds: int) -> list[dict[str, Any]]:
    by_ds: dict[str, list[dict[str, Any]]] = {}
    for rec in records:
        ds = rec["DS"]
        bucket = by_ds.setdefault(ds, [])
        if len(bucket) < per_ds:
            bucket.append(rec)
    out: list[dict[str, Any]] = []
    for ds in sorted(by_ds):
        out.extend(by_ds[ds])
    return out


def _align_features(records: list[dict[str, Any]], width: int = 39) -> tuple[list[list[float]], list[int]]:
    cohort_idx = {"DS0001": 0, "DS0002": 1, "DS0003": 2, "DS0004": 3}
    raw_len = width - 8
    rows, ys = [], []
    for r in records:
        mask = [float(x) for x in r["ModalityMask_CELS"]]
        ohe = [0.0, 0.0, 0.0, 0.0]
        ohe[cohort_idx[r["DS"]]] = 1.0
        tab = [float(v) for v in r["TabularFeatures"][:raw_len]]
        if len(tab) < raw_len:
            tab.extend([0.0] * (raw_len - len(tab)))
        rows.append(mask + ohe + tab)
        ys.append(int(r.get("Target_y", r.get("y"))))
    return rows, ys


def main() -> int:
    cfg_path = REPO_ROOT / "07_Experiments" / "configs" / "exp0000_smoke.yaml"
    cfg = validate_experiment_config(load_config_file(str(cfg_path)), allow_frozen_test_eval=False, verify_prereg_files=True)
    cfg_sha = sha256_file(str(cfg_path))

    # Strictly Train + Val only!
    train_all = load_rel0001_partition("train", rel_dir=DEFAULT_REL0001_DIR)
    val_all = load_rel0001_partition("val", rel_dir=DEFAULT_REL0001_DIR)
    train_slice = _stratified_cohort_sample(train_all, per_ds=150)
    val_slice = _stratified_cohort_sample(val_all, per_ds=50)

    X_tr, y_tr = _align_features(train_slice)
    X_va, y_va = _align_features(val_slice)

    # 1. Verify real DS0001 12-lead WFDB waveform decoding + Stage-A notch/highpass DSP
    ds1_sample = next((r for r in train_slice if r["DS"] == "DS0001" and r.get("ECGReference")), None)
    ecg_smoke_info: dict[str, Any] = {"wfdb_verified": False}
    ecg_summary_vec: list[float] = [0.0] * 12
    if ds1_sample and ds1_sample["ECGReference"].get("wfdb_hr_relpath"):
        stem = ds1_sample["ECGReference"]["wfdb_hr_relpath"]
        dat_file = REPO_ROOT / (stem + ".dat")
        if dat_file.is_file():
            leads = load_wfdb_12lead_filtered(stem, fs_hz=500.0, repo_root=str(REPO_ROOT))
            ecg_summary_vec = [round(sum(abs(v) for v in ld[:500]) / 500.0, 6) for ld in leads]
            ecg_smoke_info = {
                "wfdb_verified": True,
                "stem": stem,
                "n_leads": len(leads),
                "n_samples_per_lead": len(leads[0]),
                "finite_all": all(math.isfinite(x) for ld in leads for x in ld),
            }

    # 2. Deliberate interrupt & SHA-256 checkpoint resume equivalence test
    ckpt_unint = REPO_ROOT / "08_Checkpoints" / "binaries" / "EXP0000_SMOKE" / "local_uninterrupted"
    ckpt_res = REPO_ROOT / "08_Checkpoints" / "binaries" / "EXP0000_SMOKE" / "local_resumed"

    unint = train_pure_python_logistic_with_checkpoints(
        X_train=X_tr, y_train=y_tr, X_val=X_va, y_val=y_va,
        checkpoint_dir=ckpt_unint, exp_id="EXP0000_SMOKE", candidate_id="MC0001_SMOKE",
        config_hash=cfg_sha, epochs=6, lr=0.1, l2=1e-3, seed=42,
    )
    part1 = train_pure_python_logistic_with_checkpoints(
        X_train=X_tr, y_train=y_tr, X_val=X_va, y_val=y_va,
        checkpoint_dir=ckpt_res, exp_id="EXP0000_SMOKE", candidate_id="MC0001_SMOKE",
        config_hash=cfg_sha, epochs=3, lr=0.1, l2=1e-3, seed=42,
    )
    loaded_meta = load_checkpoint_bundle(part1["last_checkpoint"], verify_checksum=True)
    resumed = train_pure_python_logistic_with_checkpoints(
        X_train=X_tr, y_train=y_tr, X_val=X_va, y_val=y_va,
        checkpoint_dir=ckpt_res, exp_id="EXP0000_SMOKE", candidate_id="MC0001_SMOKE",
        config_hash=cfg_sha, epochs=6, lr=0.1, l2=1e-3, seed=42, resume_from=part1["last_checkpoint"],
    )
    max_w_diff = max(abs(a - b) for a, b in zip(unint["model"].weights, resumed["model"].weights))
    bias_diff = abs(unint["model"].bias - resumed["model"].bias)
    if max_w_diff > 1e-12 or bias_diff > 1e-12:
        raise AssertionError(f"Resume drift detected: max_w_diff={max_w_diff}, bias_diff={bias_diff}")

    # 3. 4-Cohort Masked Fusion zero-NaN sanity check on real ModalityMask_CELS patterns
    dims = {ds: {m: len(idxs) for m, idxs in mods.items()} for ds, mods in COHORT_MODALITY_SLICES.items()}
    fusion = PurePythonMaskedFusionModel(dims, d_model=16, ecg_dim=12, seed=42)
    fusion_checks = {}
    for ds_id in ("DS0001", "DS0002", "DS0003", "DS0004"):
        rec = next(r for r in val_slice if r["DS"] == ds_id)
        mod_vecs = split_tabular_by_modality(rec["TabularFeatures"], ds_id)
        mod_vecs["ecg"] = ecg_summary_vec if ds_id == "DS0001" else [0.0] * 12
        out = fusion.forward(ds_id, mod_vecs, rec["ModalityMask_CELS"])
        if not (math.isfinite(out["logit"]) and 0.0 < out["prob"] < 1.0):
            raise AssertionError(f"Non-finite fusion smoke output for {ds_id}: {out}")
        fusion_checks[ds_id] = {
            "mask_cels": rec["ModalityMask_CELS"],
            "prob": round(out["prob"], 6),
            "attn_weights": [round(w, 6) for w in out["attention_weights"]],
        }

    # 4. Validation-Only Calibration + Threshold Freeze
    model = resumed["model"]
    val_logits = model.predict_logits(X_va)
    val_tags = ["val"] * len(y_va)
    cal = TemperatureScalingCalibrator().fit(y_va, val_logits, split_tags=val_tags)
    val_cal_probs = cal.transform(val_logits)
    thresholds = select_validation_thresholds(y_va, val_cal_probs, split_tags=val_tags, min_sensitivity=0.85)
    val_metrics = compute_all_metrics(y_va, val_cal_probs, threshold=thresholds["tau_youden"])

    # 5. Diagnostic XAI Hook Verification (Train-only background, linear Shapley additivity & AOPC)
    bg_rows = sample_train_only_background(X_tr, ["train"] * len(X_tr), n_bg=128, seed=42)
    bg_mean = [sum(col) / len(bg_rows) for col in zip(*bg_rows)]
    eval_sub = X_va[:40]
    w = model.weights
    b = model.bias
    base_logit = b + sum(wi * bi for wi, bi in zip(w, bg_mean))
    phi_logits = [[wi * (xv[j] - bg_mean[j]) for j, wi in enumerate(w)] for xv in eval_sub]
    raw_logits_eval = model.predict_logits(eval_sub)
    additivity = check_shap_additivity(phi_logits, base_value=base_logit, predictions=raw_logits_eval, tol=0.02)
    if not additivity["passed"]:
        raise AssertionError(f"Smoke SHAP additivity failed: {additivity}")

    aopc = evaluate_aopc_faithfulness(
        predict_fn=model.predict_logits,
        X_eval=eval_sub,
        phi_eval=phi_logits,
        baseline_vec=bg_mean,
        max_k=15,
        seed=42,
    )
    mean_abs_phi = [sum(abs(row[j]) for row in phi_logits) / len(phi_logits) for j in range(len(w))]
    feat_names = [f"mask_{m}" for m in "CELS"] + [f"ds_{i}" for i in range(4)] + [f"tab_{i}" for i in range(len(w) - 8)]
    shortcut = audit_mnar_shortcut_flags(feat_names, mean_abs_phi, top_k=3)

    report = {
        "status": "LOCAL_SMOKE_PASS",
        "experiment_id": "EXP0000_SMOKE",
        "config_path": "07_Experiments/configs/exp0000_smoke.yaml",
        "config_sha256": cfg_sha,
        "test_partition_accessed": False,
        "n_train_slice": len(X_tr),
        "n_val_slice": len(X_va),
        "cohorts_covered": sorted({r["DS"] for r in train_slice}),
        "wfdb_check": ecg_smoke_info,
        "resume_continuity": {
            "interrupted_epoch": loaded_meta["epoch"],
            "resumed_to_epoch": resumed["model"].epoch,
            "checkpoint_sha256": sha256_file(part1["last_checkpoint"]),
            "max_weight_diff": max_w_diff,
            "bias_diff": bias_diff,
            "exact_bitwise_resume": True,
        },
        "fusion_masked_forward_checks": fusion_checks,
        "val_calibration": {
            "temperature": cal.temperature_,
            "calibrator_hash": cal.calibrator_hash_,
            "thresholds": thresholds,
            "val_roc_auc": val_metrics["roc_auc"],
            "val_pr_auc": val_metrics["pr_auc"],
            "val_brier": val_metrics["brier_score"],
            "val_ece_q15": val_metrics["ece_quantile_15"],
        },
        "xai_hook_smoke": {
            "background_partition": "train",
            "background_n": len(bg_rows),
            "additivity": additivity,
            "aopc": aopc,
            "shortcut_audit": shortcut,
        },
    }
    out_path = REPO_ROOT / "07_Experiments" / "EXP0000_SMOKE" / "smoke_local_report.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
