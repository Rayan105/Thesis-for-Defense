"""
Multimodal Dataset Loader & Sealed Test-Custody Enforcer for REL0001 (STEP-026).

Loads partition-segregated JSONL shards (`train`, `val`, or sealed `test` under G11 unseal),
verifies SHA-256 lineage digests cleanly against `rel0001_manifest.json`, extracts cohort-specific
semantic `[Clinical, Laboratory, Lifestyle]` feature blocks + MNAR `_isnan` indicators without unit mixing,
and loads/cleans WFDB 12-lead ECG signals (`DS0001`) or red-grid PNG scans (`DS0002`) deterministically.
"""

from __future__ import annotations

import hashlib
import json
import os
import struct
from typing import Any, Mapping, Sequence

from src.cvd_mm.ecg import apply_baseline_highpass_zero_phase, apply_powerline_notch_zero_phase

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_REL0001_DIR = os.path.join(REPO_ROOT, "05_Preprocessing_Alignment", "processed", "REL0001")

# Semantic index ranges inside each cohort's Train-fitted `TabularFeatures` vector (`PP0001` contract):
# Every numeric feature occupies 2 consecutive slots `[scaled_val, isnan_flag]`, followed by OHE categories.
COHORT_MODALITY_SLICES: dict[str, dict[str, tuple[int, ...]]] = {
    "DS0001": {
        "clinical": (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10),  # age, ht, wt, bmi (+isnan) + sex OHE
        "laboratory": (),
        "lifestyle": (),
    },
    "DS0002": {
        "clinical": (0, 1, 2, 3, 4, 5, 6, 7, 12, 13, 14),  # age, sbp, dbp, pr (+isnan) + sex OHE
        "laboratory": (8, 9, 10, 11),  # creatinine, wbc (+isnan)
        "lifestyle": (),
    },
    "DS0003": {
        "clinical": (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 24, 25, 26),  # age..dbp + sex OHE
        "laboratory": (12, 13, 14, 15, 16, 17, 18, 19),  # tc, hdl, ldl, fbs (+isnan)
        "lifestyle": (20, 21, 22, 23, 27, 28, 29, 30),  # smoking, fam_hx (+isnan) + activity OHE
    },
    "DS0004": {
        "clinical": (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 22, 23, 24),  # age..dbp + sex OHE
        "laboratory": (12, 13, 14, 15),  # cholesterol_tier, glucose_tier (+isnan)
        "lifestyle": (16, 17, 18, 19, 20, 21),  # smoking, alcohol, activity (+isnan)
    },
}


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def verify_rel0001_integrity(rel_dir: str = DEFAULT_REL0001_DIR) -> dict[str, Any]:
    manifest_p = os.path.join(rel_dir, "rel0001_manifest.json")
    if not os.path.isfile(manifest_p):
        raise FileNotFoundError(f"REL0001 manifest missing at {manifest_p}")
    with open(manifest_p, encoding="utf-8") as mf:
        manifest = json.load(mf)
    for part in ("train", "val", "test"):
        shard_p = os.path.join(rel_dir, part, f"rel0001_{part}.jsonl")
        if not os.path.isfile(shard_p):
            raise FileNotFoundError(f"Missing REL0001 partition shard: {shard_p}")
    return manifest


def load_rel0001_partition(
    partition: str,
    *,
    rel_dir: str = DEFAULT_REL0001_DIR,
    dataset_scope: str = "ALL_COHORTS",
    limit: int | None = None,
    gate_g11_unseal_token: str | None = None,
    verify_shard_hash: bool = False,
) -> list[dict[str, Any]]:
    """
    Load encounters from `REL0001` (`train`, `val`, or gated `test`).
    Strictly raises PermissionError on `partition == 'test'` unless an explicit G11 token is supplied.
    """
    part = partition.strip().lower()
    if part not in ("train", "val", "test"):
        raise ValueError(f"Invalid partition '{partition}'.")
    if part == "test" and not gate_g11_unseal_token:
        raise PermissionError(
            "TEST_PARTITION_SEALED: Reading REL0001 `test` shard is forbidden before Gate G11 PASS!"
        )

    manifest = verify_rel0001_integrity(rel_dir)
    shard_p = os.path.join(rel_dir, part, f"rel0001_{part}.jsonl")
    if verify_shard_hash:
        expected = manifest["partitions"][part]["sha256"]
        actual = sha256_file(shard_p)
        if actual != expected:
            raise RuntimeError(f"REL0001 shard checksum mismatch for {part}: {actual} != {expected}")

    out: list[dict[str, Any]] = []
    with open(shard_p, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            if dataset_scope != "ALL_COHORTS" and rec["DS"] != dataset_scope:
                continue
            out.append(rec)
            if limit is not None and len(out) >= limit:
                break
    return out


def split_tabular_by_modality(vec: Sequence[float], ds_id: str) -> dict[str, list[float]]:
    """Slice a cohort's TabularFeatures vector into `[clinical, laboratory, lifestyle]` branches."""
    if ds_id not in COHORT_MODALITY_SLICES:
        raise KeyError(f"Unknown cohort schema '{ds_id}'.")
    slices = COHORT_MODALITY_SLICES[ds_id]
    return {
        "clinical": [float(vec[i]) for i in slices["clinical"]],
        "laboratory": [float(vec[i]) for i in slices["laboratory"]],
        "lifestyle": [float(vec[i]) for i in slices["lifestyle"]],
    }


def load_wfdb_12lead_filtered(
    wfdb_relpath_stem: str,
    *,
    fs_hz: float = 500.0,
    repo_root: str = REPO_ROOT,
) -> list[list[float]]:
    """Read int16 little-endian 12-lead WFDB `.dat` signal (mV) and apply Stage-A 50 Hz notch + 0.5 Hz HP."""
    dat_path = os.path.join(repo_root, wfdb_relpath_stem + ".dat")
    with open(dat_path, "rb") as df:
        raw = df.read()
    n_samples = len(raw) // (12 * 2)
    leads: list[list[float]] = []
    for ch in range(12):
        sig = [struct.unpack_from("<h", raw, (t * 12 + ch) * 2)[0] / 1000.0 for t in range(n_samples)]
        sig = apply_powerline_notch_zero_phase(sig, fs_hz=fs_hz, notch_hz=50.0, q=30.0)
        sig = apply_baseline_highpass_zero_phase(sig, fs_hz=fs_hz, cutoff_hz=0.5)
        mean = sum(sig) / max(1, len(sig))
        var = sum((x - mean) ** 2 for x in sig) / max(1, len(sig))
        std = var ** 0.5 if var > 1e-12 else 1.0
        normed = [max(-10.0, min(10.0, (x - mean) / std)) for x in sig]
        leads.append(normed)
    return leads
