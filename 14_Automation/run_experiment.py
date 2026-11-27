"""Thin CLI Experiment Dispatcher (STEP-026 / STEP-027).

Validates a T32 YAML/JSON experiment configuration strictly, loads Train/Val
partitions from REL0001 (never accessing Test before Gate G11 PASS), trains and
checkpoints the requested model deterministically, fits Validation-only
calibration + threshold selection, and writes reproducible run artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.cvd_mm.calibrate import TemperatureScalingCalibrator, select_validation_thresholds
from src.cvd_mm.config import load_config_file, validate_experiment_config
from src.cvd_mm.dataset import DEFAULT_REL0001_DIR, load_rel0001_partition
from src.cvd_mm.metrics import compute_all_metrics
from src.cvd_mm.models.train import train_pure_python_logistic_with_checkpoints


def _stable_hash(obj: Any) -> str:
    encoded = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _pad_or_align_features(records: list[dict[str, Any]], width: int | None = None) -> tuple[list[list[float]], list[int], int]:
    """Build deterministic fixed-width feature vector [4D CELS mask + 4D cohort OHE + padded TabularFeatures]."""
    cohort_idx = {"DS0001": 0, "DS0002": 1, "DS0003": 2, "DS0004": 3}
    raw_len = max(len(r.get("TabularFeatures", [])) for r in records) if width is None else width - 8
    rows: list[list[float]] = []
    labels: list[int] = []
    for rec in records:
        mask = [float(x) for x in rec.get("ModalityMask_CELS", [0, 0, 0, 0])]
        ds_ohe = [0.0, 0.0, 0.0, 0.0]
        ds_id = rec.get("DS", "DS0001")
        if ds_id in cohort_idx:
            ds_ohe[cohort_idx[ds_id]] = 1.0
        feats = [float(v) for v in rec.get("TabularFeatures", [])[:raw_len]]
        if len(feats) < raw_len:
            feats.extend([0.0] * (raw_len - len(feats)))
        rows.append(mask + ds_ohe + feats)
        labels.append(int(rec["y"]))
    return rows, labels, raw_len + 8


def run_from_config(
    config_path: str,
    *,
    rel_dir: str = DEFAULT_REL0001_DIR,
    limit: int | None = None,
    epochs_override: int | None = None,
    resume_from: str | None = None,
    checkpoint_dir: str | None = None,
    output_dir: str | None = None,
) -> dict[str, Any]:
    raw_cfg = load_config_file(config_path)
    cfg = validate_experiment_config(raw_cfg, allow_frozen_test_eval=False, verify_prereg_files=True)
    cfg_hash = _stable_hash(cfg)

    exp_id = str(cfg["experiment_id"])
    candidate_id = str(cfg["candidate_id"])
    scope = str(cfg["data"]["dataset_scope"])
    seed = int(cfg["training"]["seed"])
    epochs = int(epochs_override if epochs_override is not None else cfg["training"]["epochs"])

    # Sealed Test Custody: ONLY train & val partitions may ever be read here
    train_recs = load_rel0001_partition("train", rel_dir=rel_dir, dataset_scope=scope, limit=limit)
    val_recs = load_rel0001_partition("val", rel_dir=rel_dir, dataset_scope=scope, limit=limit)
    if not train_recs or not val_recs:
        raise RuntimeError(f"Empty train/val records for scope={scope} under {rel_dir}.")

    X_train, y_train, total_w = _pad_or_align_features(train_recs)
    X_val, y_val, _ = _pad_or_align_features(val_recs, width=total_w)

    ckpt_dir = checkpoint_dir or str(REPO_ROOT / "08_Checkpoints_Logs" / "checkpoints" / exp_id)
    out_dir = Path(output_dir or (REPO_ROOT / "08_Checkpoints_Logs" / "artifacts" / exp_id))
    out_dir.mkdir(parents=True, exist_ok=True)

    train_res = train_pure_python_logistic_with_checkpoints(
        X_train=X_train,
        y_train=y_train,
        X_val=X_val,
        y_val=y_val,
        checkpoint_dir=ckpt_dir,
        exp_id=exp_id,
        candidate_id=candidate_id,
        config_hash=cfg_hash,
        epochs=epochs,
        seed=seed,
        resume_from=resume_from,
    )

    model = train_res["model"]
    val_logits = model.predict_logits(X_val)
    val_raw_probs = model.predict_proba(X_val)
    val_tags = ["val"] * len(y_val)

    calibrator = TemperatureScalingCalibrator().fit(y_val, val_logits, split_tags=val_tags)
    val_cal_probs = calibrator.transform(val_logits)
    thresholds = select_validation_thresholds(y_val, val_cal_probs, split_tags=val_tags, min_sensitivity=0.85)

    raw_metrics = compute_all_metrics(y_val, val_raw_probs, threshold=0.5)
    cal_metrics = compute_all_metrics(y_val, val_cal_probs, threshold=thresholds["tau_youden"])

    summary = {
        "experiment_id": exp_id,
        "candidate_id": candidate_id,
        "dataset_scope": scope,
        "config_sha256": cfg_hash,
        "n_train_loaded": len(train_recs),
        "n_val_loaded": len(val_recs),
        "test_partition_accessed": False,
        "best_val_roc_auc": round(train_res["best_val_roc_auc"], 6),
        "best_checkpoint": train_res["best_checkpoint"],
        "last_checkpoint": train_res["last_checkpoint"],
        "temperature": calibrator.temperature_,
        "calibrator_hash": calibrator.calibrator_hash_,
        "frozen_thresholds": thresholds,
        "val_metrics_raw_05": raw_metrics,
        "val_metrics_cal_youden": cal_metrics,
        "history": train_res["history"],
    }
    report_path = out_dir / f"{exp_id}_val_summary.json"
    report_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    summary["report_path"] = str(report_path)
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CVD-Multimodal Config-Driven Experiment Dispatcher")
    parser.add_argument("--config", required=True, help="Path to YAML/JSON T32 experiment config")
    parser.add_argument("--rel-dir", default=DEFAULT_REL0001_DIR, help="Path to REL0001 directory")
    parser.add_argument("--limit", type=int, default=None, help="Optional per-split row limit (for smoke runs)")
    parser.add_argument("--epochs", type=int, default=None, help="Optional epoch count override")
    parser.add_argument("--resume-from", default=None, help="Optional checkpoint JSON path to resume training")
    parser.add_argument("--checkpoint-dir", default=None, help="Checkpoint output directory")
    parser.add_argument("--output-dir", default=None, help="Run artifact summary directory")
    args = parser.parse_args(argv)

    summary = run_from_config(
        args.config,
        rel_dir=args.rel_dir,
        limit=args.limit,
        epochs_override=args.epochs,
        resume_from=args.resume_from,
        checkpoint_dir=args.checkpoint_dir,
        output_dir=args.output_dir,
    )
    print(json.dumps({
        "status": "OK",
        "experiment_id": summary["experiment_id"],
        "n_train": summary["n_train_loaded"],
        "n_val": summary["n_val_loaded"],
        "best_val_roc_auc": summary["best_val_roc_auc"],
        "temperature": summary["temperature"],
        "thresholds": summary["frozen_thresholds"],
        "report_path": summary["report_path"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
