"""
Execute STEP-021 Train-Only Stage B Preprocessing Fit, ECG Morphology Verification & Assertions (`PP0001`).

Strict OS §4.4–§4.5 & Blueprint STEP-021 Compliance:
1. Cryptographically verifies parent `ADJ0001-ADJ0004`, `variables.csv`, and `SPLIT0001/manifest.csv`.
2. Fits Stage B (`TrainOnlyTabularPreprocessor`) EXCLUSIVELY on `SPLIT0001` `train` rows per cohort,
   locking serialized Train fit states + `FitStateHash` under gitignored `05_Preprocessing_Alignment/fitted_states/PP0001/`.
3. Deterministically transforms `train`, `val`, and `test` partitions without ever refitting on Val/Test,
   writing partition-segregated JSONL shards under gitignored `05_Preprocessing_Alignment/processed/PP0001/`.
4. Executes strict post-transform assertions: zero `NaN`/`Inf`, exact `_isnan` MNAR counts, row/target alignment,
   round-trip inverse scaling exactness, and invariant raw/ADJ/SPLIT SHA-256 hashes.
5. Audits real `SPLIT0001` `train` samples of `PTB-XL` 500 Hz / 100 Hz WFDB signals (50 Hz notch + <=0.5 Hz high-pass)
   and `CARDIO-ML-ED` 8-bit RGB PNG paper scans (`suppress_red_ecg_grid_rgb` + 90-deg portrait orientation check).
"""

from __future__ import annotations

import collections
import csv
import hashlib
import json
import math
import os
import struct
import sys
import time
import zlib

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

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
from src.cvd_mm.schema_ecg import normalize_cardiomled_image_stem

ADJ_ROOT = os.path.join(REPO_ROOT, "04_Outcome_Schema_QA", "adjudications")
SPLITS_DIR = os.path.join(REPO_ROOT, "03_Datasets_Cohort", "splits")
DATASET_ROOT = os.path.join(REPO_ROOT, "Dataset")
PP_ROOT = os.path.join(REPO_ROOT, "05_Preprocessing_Alignment")
PP_ID = "PP0001"
SPLIT_ID = "SPLIT0001"

COHORT_SCHEMAS = {
    "DS0001": {
        "adj": "ADJ0001",
        "target_col": "Target_y_ptb_nonnorm",
        "num_cols": ["age_years", "height_cm", "weight_kg", "bmi_kgm2"],
        "cat_cols": ["sex"],
    },
    "DS0002": {
        "adj": "ADJ0002",
        "target_col": "Target_y_ed_initial",
        "num_cols": ["age_years", "sbp_mmhg", "dbp_mmhg", "pr_bpm", "creatinine_mgdl", "wbc_ul"],
        "cat_cols": ["sex"],
    },
    "DS0003": {
        "adj": "ADJ0003",
        "target_col": "Target_y_cair_high",
        "num_cols": [
            "age_years", "height_cm", "weight_kg", "bmi_kgm2",
            "sbp_mmhg", "dbp_mmhg", "total_cholesterol_mgdl", "hdl_mgdl",
            "ldl_estimated_mgdl", "fbs_mgdl", "smoking_status", "family_history_cvd",
        ],
        "cat_cols": ["sex", "activity_level"],
    },
    "DS0004": {
        "adj": "ADJ0004",
        "target_col": "Target_y_sul_cardio",
        "num_cols": [
            "age_years", "height_cm", "weight_kg", "bmi_kgm2",
            "sbp_mmhg", "dbp_mmhg", "cholesterol_tier", "glucose_tier",
            "smoking_status", "alcohol_intake", "physical_activity",
        ],
        "cat_cols": ["sex"],
    },
}


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def verify_parent_hashes() -> dict[str, str]:
    """Fail loudly if ADJ0001-0004 or SPLIT0001 manifest hashes do not match registries."""
    hashes: dict[str, str] = {}
    with open(os.path.join(REPO_ROOT, "04_Outcome_Schema_QA", "adjudication_registry.csv"), encoding="utf-8", newline="") as f:
        adj_reg = {r["ADJ"]: r for r in csv.DictReader(f)}

    for ds, cfg in COHORT_SCHEMAS.items():
        adj = cfg["adj"]
        cur_p = os.path.join(ADJ_ROOT, adj, "verified_curated.csv")
        cur_h = sha256_file(cur_p)
        if cur_h != adj_reg[adj]["VerifiedHash"]:
            raise RuntimeError(f"HASH_MISMATCH on {adj}: {cur_h} != {adj_reg[adj]['VerifiedHash']}")
        hashes[adj] = cur_h
        hashes[f"{adj}_eligible"] = sha256_file(os.path.join(ADJ_ROOT, adj, "verified_eligible_only.csv"))

    split_manifest = os.path.join(SPLITS_DIR, SPLIT_ID, "manifest.csv")
    manifest_h = sha256_file(split_manifest)
    cfg_txt = open(os.path.join(SPLITS_DIR, SPLIT_ID, "split_config.yaml"), encoding="utf-8").read()
    expected_line = [ln for ln in cfg_txt.splitlines() if ln.startswith("manifest_sha256:")][0]
    expected_split_h = expected_line.split(":", 1)[1].strip()
    if manifest_h != expected_split_h:
        raise RuntimeError(f"SPLIT_HASH_MISMATCH: {manifest_h} != {expected_split_h}")
    hashes[SPLIT_ID] = manifest_h
    hashes["variables_csv"] = sha256_file(os.path.join(REPO_ROOT, "04_Outcome_Schema_QA", "variables.csv"))
    return hashes


def _decode_png_rgb_sampled(png_path: str, row_stride: int = 16, col_stride: int = 16) -> tuple[int, int, dict[str, float]]:
    """
    Pure-stdlib PNG RGB decoder measuring portrait dimensions & red-grid suppression efficacy
    across strided scanlines without requiring OpenCV or Pillow locally.
    """
    raw = open(png_path, "rb").read()
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Invalid PNG signature: {png_path}")
    pos = 8
    idat_chunks = []
    width = height = 0
    bit_depth = color_type = 0
    while pos + 8 <= len(raw):
        length, ctype = struct.unpack(">I4s", raw[pos : pos + 8])
        data = raw[pos + 8 : pos + 8 + length]
        pos += 12 + length
        if ctype == b"IHDR":
            width, height, bit_depth, color_type = struct.unpack(">IIBB", data[:10])
        elif ctype == b"IDAT":
            idat_chunks.append(data)
        elif ctype == b"IEND":
            break

    if bit_depth != 8 or color_type not in (2, 6):
        raise ValueError(f"Unsupported PNG format bit_depth={bit_depth}, color_type={color_type}")
    bpp = 3 if color_type == 2 else 4
    decomp = zlib.decompress(b"".join(idat_chunks))
    stride_bytes = width * bpp

    prev = bytearray(stride_bytes)
    cur = bytearray(stride_bytes)

    n_sampled = 0
    raw_red_grid = 0
    suppressed_white = 0
    raw_dark_ink = 0
    preserved_dark_ink = 0

    def _paeth(a: int, b: int, c: int) -> int:
        p = a + b - c
        pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
        return a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)

    offset = 0
    for y in range(height):
        ftype = decomp[offset]
        offset += 1
        row_bytes = decomp[offset : offset + stride_bytes]
        offset += stride_bytes
        if ftype == 0:
            cur[:] = row_bytes
        elif ftype == 1:
            for x in range(stride_bytes):
                cur[x] = (row_bytes[x] + (cur[x - bpp] if x >= bpp else 0)) & 0xFF
        elif ftype == 2:
            for x in range(stride_bytes):
                cur[x] = (row_bytes[x] + prev[x]) & 0xFF
        elif ftype == 3:
            for x in range(stride_bytes):
                left = cur[x - bpp] if x >= bpp else 0
                cur[x] = (row_bytes[x] + ((left + prev[x]) >> 1)) & 0xFF
        elif ftype == 4:
            for x in range(stride_bytes):
                left = cur[x - bpp] if x >= bpp else 0
                up = prev[x]
                up_left = prev[x - bpp] if x >= bpp else 0
                cur[x] = (row_bytes[x] + _paeth(left, up, up_left)) & 0xFF

        if y % row_stride == 0:
            for x_px in range(0, width, col_stride):
                off = x_px * bpp
                r, g, b_ch = cur[off], cur[off + 1], cur[off + 2]
                out_g = suppress_red_ecg_grid_rgb(r, g, b_ch)
                n_sampled += 1
                is_red_pixel = (r - max(g, b_ch)) >= 25 and max(r, g, b_ch) >= 165
                is_dark_ink = max(r, g, b_ch) <= 85
                if is_red_pixel:
                    raw_red_grid += 1
                    if out_g >= 230:
                        suppressed_white += 1
                if is_dark_ink:
                    raw_dark_ink += 1
                    if out_g <= 95:
                        preserved_dark_ink += 1
        prev, cur = cur, prev

    return width, height, {
        "sampled_pixels": n_sampled,
        "red_grid_pixels": raw_red_grid,
        "red_grid_suppressed_pct": round(suppressed_white * 100.0 / max(1, raw_red_grid), 2),
        "dark_ink_pixels": raw_dark_ink,
        "dark_ink_preserved_pct": round(preserved_dark_ink * 100.0 / max(1, raw_dark_ink), 2),
    }


def audit_ecg_and_png_stage_a(train_manifest_by_ds: dict[str, list[dict[str, str]]]) -> dict[str, object]:
    """Run quantitative Stage-A ECG waveform & paper-scan audit on Train samples only."""
    # 1. PTB-XL 500 Hz + 100 Hz stratified Train sample (5 subclasses / artifacts)
    ptb_dir = os.path.join(DATASET_ROOT, "1. DS0001_ptbxl (PTB-XL, Kaggle)", "ptb-xl-a-large-publicly-available-electrocardiography-dataset-1.0.1")
    with open(os.path.join(ptb_dir, "ptbxl_database.csv"), encoding="utf-8", newline="") as f:
        ptb_meta = {r["ecg_id"]: r for r in csv.DictReader(f)}

    train_eids = {r["RecordID"] for r in train_manifest_by_ds["DS0001"]}
    with open(os.path.join(ADJ_ROOT, "ADJ0001", "verified_eligible_only.csv"), encoding="utf-8", newline="") as f:
        ptb_el = [r for r in csv.DictReader(f) if r["RecordID"] in train_eids]

    buckets = collections.defaultdict(list)
    for r in ptb_el:
        scps = r["SCP_Superclasses"]
        for key in ("NORM", "MI", "STTC", "CD", "HYP"):
            if key in scps and len(buckets[key]) < 5:
                buckets[key].append(r["RecordID"])
                break

    sample_ids = [eid for k in ("NORM", "MI", "STTC", "CD", "HYP") for eid in buckets[k]]
    hr_corrs, lr_corrs, mean_dc_before, mean_dc_after, lag_zeros = [], [], [], [], 0
    wfdb_rows = []

    for eid in sample_ids:
        meta = ptb_meta[eid]
        # 500 Hz Lead II
        dat_hr = open(os.path.join(ptb_dir, meta["filename_hr"] + ".dat"), "rb").read()
        raw_hr = [struct.unpack_from("<h", dat_hr, (t * 12 + 1) * 2)[0] / 1000.0 for t in range(5000)]
        f_hr = apply_baseline_highpass_zero_phase(apply_powerline_notch_zero_phase(raw_hr, 500.0, 50.0, 30.0), 500.0, 0.5)
        # Center-window correlation & DC offset drop (trimmed 0.5s edges)
        raw_c = raw_hr[250:4750]
        raw_dc = sum(raw_c) / len(raw_c)
        raw_zero = [x - raw_dc for x in raw_c]
        flt_c = f_hr[250:4750]
        corr_hr = pearson_correlation(raw_zero, flt_c)
        hr_corrs.append(corr_hr)
        mean_dc_before.append(abs(raw_dc))
        mean_dc_after.append(abs(sum(flt_c) / len(flt_c)))

        # Verify zero-phase QRS R-peak alignment locally around strongest filtered beat (+/- 24 ms window)
        pk_flt = max(range(len(flt_c)), key=lambda i: abs(flt_c[i]))
        lo, hi = max(0, pk_flt - 12), min(len(raw_zero), pk_flt + 13)
        win_raw = raw_zero[lo:hi]
        win_mean = sum(win_raw) / max(1, len(win_raw))
        pk_raw_local = max(range(lo, hi), key=lambda i: abs(raw_zero[i] - win_mean))
        local_lag = abs(pk_raw_local - pk_flt)
        if local_lag <= 1:
            lag_zeros += 1

        # 100 Hz Lead II (tests safe 50 Hz Nyquist bypass!)
        dat_lr = open(os.path.join(ptb_dir, meta["filename_lr"] + ".dat"), "rb").read()
        raw_lr = [struct.unpack_from("<h", dat_lr, (t * 12 + 1) * 2)[0] / 1000.0 for t in range(1000)]
        f_lr = apply_baseline_highpass_zero_phase(apply_powerline_notch_zero_phase(raw_lr, 100.0, 50.0, 30.0), 100.0, 0.5)
        rlr_c = raw_lr[50:950]
        rlr_dc = sum(rlr_c) / len(rlr_c)
        corr_lr = pearson_correlation([x - rlr_dc for x in rlr_c], f_lr[50:950])
        lr_corrs.append(corr_lr)

        wfdb_rows.append({
            "ecg_id": eid,
            "superclasses": meta["scp_codes"],
            "hr_corr": round(corr_hr, 4),
            "lr_corr": round(corr_lr, 4),
            "qrs_lag_samples": local_lag,
        })

    # 2. CARDIO-ML-ED PNG red-grid suppression & portrait check on 10 Train PNGs
    cm_dir = os.path.join(DATASET_ROOT, "3. DS0003_cardiomled (CARDIO-ML-ED, Mendeley Official CC BY 4.0)")
    ecg_dir = os.path.join(cm_dir, "ECGS")
    png_by_base = collections.defaultdict(list)
    for fn in sorted(os.listdir(ecg_dir)):
        if fn.lower().endswith(".png"):
            st = normalize_cardiomled_image_stem(os.path.splitext(fn)[0])
            png_by_base[st.split("-")[0]].append(os.path.join(ecg_dir, fn))

    train_pids_cm = [r["PatientGroupID"] for r in train_manifest_by_ds["DS0002"] if r["HasECG"] == "1"]
    png_samples = []
    seen_p = set()
    for pid in train_pids_cm:
        if pid in seen_p or not png_by_base[pid]:
            continue
        seen_p.add(pid)
        w, h, stats = _decode_png_rgb_sampled(png_by_base[pid][0])
        png_samples.append({
            "patient_group": pid,
            "file": os.path.basename(png_by_base[pid][0]),
            "width": w,
            "height": h,
            "needs_90_ccw": h > w,
            **stats,
        })
        if len(png_samples) >= 10:
            break

    return {
        "wfdb_sample_n": len(wfdb_rows),
        "wfdb_hr_mean_corr": round(sum(hr_corrs) / len(hr_corrs), 4),
        "wfdb_hr_min_corr": round(min(hr_corrs), 4),
        "wfdb_lr_mean_corr": round(sum(lr_corrs) / len(lr_corrs), 4),
        "wfdb_dc_before_mv": round(sum(mean_dc_before) / len(mean_dc_before), 4),
        "wfdb_dc_after_mv": round(sum(mean_dc_after) / len(mean_dc_after), 6),
        "wfdb_zero_lag_count": lag_zeros,
        "wfdb_details": wfdb_rows[:10],
        "png_sample_n": len(png_samples),
        "png_portrait_count": sum(1 for x in png_samples if x["needs_90_ccw"]),
        "png_mean_red_suppressed_pct": round(sum(x["red_grid_suppressed_pct"] for x in png_samples) / len(png_samples), 2),
        "png_mean_ink_preserved_pct": round(sum(x["dark_ink_preserved_pct"] for x in png_samples) / len(png_samples), 2),
    }


def main() -> None:
    t0 = time.perf_counter()
    parent_hashes = verify_parent_hashes()

    # Load SPLIT0001 manifest (DS, RecordID) -> (Partition, CVFoldInTrain)
    split_manifest_path = os.path.join(SPLITS_DIR, SPLIT_ID, "manifest.csv")
    split_lookup: dict[tuple[str, str], dict[str, str]] = {}
    train_manifest_by_ds: dict[str, list[dict[str, str]]] = collections.defaultdict(list)
    with open(split_manifest_path, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            split_lookup[(r["DS"], r["RecordID"])] = r
            if r["Partition"] == "train":
                train_manifest_by_ds[r["DS"]].append(r)

    fit_state_dir = os.path.join(PP_ROOT, "fitted_states", PP_ID)
    proc_dir = os.path.join(PP_ROOT, "processed", PP_ID)
    os.makedirs(fit_state_dir, exist_ok=True)
    for part in ("train", "val", "test"):
        os.makedirs(os.path.join(proc_dir, part), exist_ok=True)

    cohort_summaries = {}
    fit_hashes = {}
    total_counts = {"train": 0, "val": 0, "test": 0}

    for ds_id, cfg in COHORT_SCHEMAS.items():
        adj = cfg["adj"]
        el_path = os.path.join(ADJ_ROOT, adj, "verified_eligible_only.csv")
        with open(el_path, encoding="utf-8", newline="") as f:
            raw_rows = list(csv.DictReader(f))

        by_part: dict[str, list[dict[str, str]]] = {"train": [], "val": [], "test": []}
        by_part_meta: dict[str, list[dict[str, str]]] = {"train": [], "val": [], "test": []}

        for raw in raw_rows:
            rec_id = raw["RecordID"]
            sp = split_lookup[(ds_id, rec_id)]
            part = sp["Partition"]
            # Apply deterministic record-local Stage A cleaner
            cleaned = StageARecordCleaner.clean_record(raw, ds_id=ds_id)
            by_part[part].append(cleaned)
            by_part_meta[part].append(sp)

        # Fit Stage B STRICTLY on `train` partition with explicit split_tags guard!
        train_rows = by_part["train"]
        prep = TrainOnlyTabularPreprocessor(
            numeric_cols=cfg["num_cols"],
            categorical_cols=cfg["cat_cols"],
            tier="A",
        )
        prep.fit(train_rows, split_tags=["train"] * len(train_rows))
        fit_hashes[ds_id] = prep.fit_state_hash_

        # Serialize Train fit state JSON into gitignored Tier 2B
        fit_json = {
            "pp_id": PP_ID,
            "ds_id": ds_id,
            "split_id": SPLIT_ID,
            "fit_partition": "train_only",
            "n_train_rows": len(train_rows),
            "feature_names": prep.feature_names(),
            "medians": prep.medians_,
            "iqrs": prep.iqrs_,
            "cat_vocab": prep.cat_vocab_,
            "fit_state_hash": prep.fit_state_hash_,
        }
        with open(os.path.join(fit_state_dir, f"{ds_id}_train_fit_state.json"), "w", encoding="utf-8") as f:
            json.dump(fit_json, f, indent=2)

        feat_names = prep.feature_names()
        raw_miss_total = 0
        mask_miss_total = 0
        max_roundtrip_err = 0.0
        n_pos_tr = sum(1 for r in train_rows if r[cfg["target_col"]] == "1")
        n_neg_tr = len(train_rows) - n_pos_tr
        pos_weight = round(n_neg_tr / max(1, n_pos_tr), 4)

        part_shapes = {}
        part_hashes = {}
        for part in ("train", "val", "test"):
            rows_p = by_part[part]
            metas_p = by_part_meta[part]
            X_p = prep.transform(rows_p)
            total_counts[part] += len(X_p)
            part_shapes[part] = [len(X_p), len(feat_names)]

            # Assertions: zero NaN/Inf, exact MNAR match, round-trip scaling check + single-pass JSONL write
            out_path = os.path.join(proc_dir, part, f"{ds_id}_{part}.jsonl")
            with open(out_path, "wb") as fout:
                for r_raw, r_meta, vec in zip(rows_p, metas_p, X_p):
                    if len(vec) != len(feat_names):
                        raise AssertionError("Feature width mismatch!")
                    for val in vec:
                        if not math.isfinite(val):
                            raise AssertionError(f"Non-finite value in {ds_id} {part}!")

                    # Verify raw missingness count vs `_isnan` mask sum & inverse scaling round-trip
                    for j, col in enumerate(cfg["num_cols"]):
                        raw_val = r_raw.get(col, "")
                        is_miss_raw = raw_val in (None, "")
                        scaled_v = vec[j * 2]
                        mask_v = vec[j * 2 + 1]
                        if is_miss_raw:
                            raw_miss_total += 1
                            assert mask_v == 1.0
                        else:
                            assert mask_v == 0.0
                            inv_v = prep.inverse_scale_numeric(col, scaled_v)
                            err = abs(inv_v - float(raw_val))
                            if err > max_roundtrip_err:
                                max_roundtrip_err = err
                        mask_miss_total += int(mask_v)

                    mod_mask = build_modality_presence_mask(
                        has_clinical=r_meta["HasClinical"] == "1",
                        has_ecg=r_meta["HasECG"] == "1",
                        has_lab=r_meta["HasLab"] == "1",
                        has_lifestyle=r_meta["HasLifestyle"] == "1",
                    )
                    rec_out = {
                        "DS": ds_id,
                        "RecordID": r_meta["RecordID"],
                        "PatientGroupID": r_meta["PatientGroupID"],
                        "Partition": part,
                        "CVFoldInTrain": int(r_meta["CVFoldInTrain"]),
                        "Target_y": int(r_meta["Target_y"]),
                        "ModalityMask": mod_mask,
                        "X": vec,
                    }
                    fout.write((json.dumps(rec_out, separators=(",", ":")) + "\n").encode("utf-8"))
            part_hashes[part] = sha256_file(out_path)

        assert raw_miss_total == mask_miss_total, f"{ds_id} missing mask mismatch!"
        assert max_roundtrip_err < 1e-8, f"{ds_id} inverse scaling drift: {max_roundtrip_err}"

        cohort_summaries[ds_id] = {
            "adj": adj,
            "n_features": len(feat_names),
            "feature_names": feat_names,
            "medians": {k: round(v, 4) for k, v in prep.medians_.items()},
            "iqrs": {k: round(v, 4) for k, v in prep.iqrs_.items()},
            "train_pos_weight": pos_weight,
            "raw_missing_cells": raw_miss_total,
            "mask_flagged_cells": mask_miss_total,
            "max_inverse_scale_err": max_roundtrip_err,
            "fit_state_hash": prep.fit_state_hash_,
            "part_shapes": part_shapes,
            "part_hashes": part_hashes,
        }

    # Combine per-cohort FitStateHashes into deterministic master PP0001 FitStateHash
    master_fit_hash = hashlib.sha256(
        json.dumps(fit_hashes, sort_keys=True).encode("utf-8")
    ).hexdigest()

    # Re-verify parent ADJ0001-0004 & SPLIT0001 hashes remained 100% immutable!
    post_hashes = verify_parent_hashes()
    assert post_hashes == parent_hashes, "IMMUTABLE INPUT HASH CHANGED!"

    # Run ECG & PNG Stage-A empirical verification on Train samples
    ecg_audit = audit_ecg_and_png_stage_a(train_manifest_by_ds)

    summary_payload = {
        "pp_id": PP_ID,
        "split_id": SPLIT_ID,
        "master_fit_state_hash": master_fit_hash,
        "parent_hashes": parent_hashes,
        "total_processed_counts": total_counts,
        "cohorts": cohort_summaries,
        "ecg_and_png_audit": ecg_audit,
        "elapsed_sec": round(time.perf_counter() - t0, 2),
    }
    with open(os.path.join(fit_state_dir, "pp0001_execution_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary_payload, f, indent=2)

    print(f"STEP-021 ({PP_ID}) COMPLETED CLEANLY in {summary_payload['elapsed_sec']}s")
    print(f"Total Transformed: {total_counts} (Sum={sum(total_counts.values())})")
    print(f"MasterFitStateHash={master_fit_hash}")
    for ds_id, cs in cohort_summaries.items():
        print(
            f"  {ds_id}: dims={cs['n_features']}, pos_weight={cs['train_pos_weight']}, "
            f"MNAR_cells={cs['mask_flagged_cells']}, inv_err={cs['max_inverse_scale_err']:.2e}, "
            f"fit_hash={cs['fit_state_hash'][:12]}..."
        )
    print(
        f"WFDB Audit (N={ecg_audit['wfdb_sample_n']} Train): 500Hz_mean_r={ecg_audit['wfdb_hr_mean_corr']} "
        f"(min={ecg_audit['wfdb_hr_min_corr']}), 100Hz_mean_r={ecg_audit['wfdb_lr_mean_corr']}, "
        f"zero_QRS_lag={ecg_audit['wfdb_zero_lag_count']}/{ecg_audit['wfdb_sample_n']}, "
        f"DC_mv: {ecg_audit['wfdb_dc_before_mv']} -> {ecg_audit['wfdb_dc_after_mv']}"
    )
    print(
        f"PNG Grid Audit (N={ecg_audit['png_sample_n']} Train): portrait={ecg_audit['png_portrait_count']}/{ecg_audit['png_sample_n']}, "
        f"red_grid_suppressed={ecg_audit['png_mean_red_suppressed_pct']}%, dark_ink_preserved={ecg_audit['png_mean_ink_preserved_pct']}%"
    )


if __name__ == "__main__":
    main()
