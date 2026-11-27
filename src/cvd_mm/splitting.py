"""
Deterministic Patient-Grouped Stratified Splitting Module (STEP-020 / G07).

Guarantees strict zero-leakage isolation by `PatientGroupID`:
- Uses official `StratFold` (1-8 Train / 9 Val / 10 Test) for `DS0001 PTB-XL` while verifying
  zero cross-fold patient leakage.
- Executes deterministic, seed-locked stratified patient-group assignment (`70% Train / 15% Val / 15% Test`)
  plus deterministic 5-fold grouped cross-validation indices inside `train` for `DS0002-DS0004`.
- Preserves both encounter-level strata (CVD outcome, sex, modality/ECG availability) and atomic
  connected patient groups (repeated ED encounters stay strictly in one partition).
"""

from __future__ import annotations

import collections
import hashlib
import re
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

DEFAULT_SPLIT_SEED = 20261127
PARTITION_RATIOS: dict[str, float] = {"train": 0.70, "val": 0.15, "test": 0.15}
PARTITION_ORDER = ("train", "val", "test")

COHORT_SPLIT_SPECS: tuple[dict[str, str], ...] = (
    {"adj_id": "ADJ0001", "ds_id": "DS0001", "name": "PTB-XL", "target_col": "Target_y_ptb_nonnorm"},
    {"adj_id": "ADJ0002", "ds_id": "DS0002", "name": "CARDIO-ML-ED", "target_col": "Target_y_ed_initial"},
    {"adj_id": "ADJ0003", "ds_id": "DS0003", "name": "CAIR-CVD-2025", "target_col": "Target_y_cair_high"},
    {"adj_id": "ADJ0004", "ds_id": "DS0004", "name": "Kaggle sulianova", "target_col": "Target_y_sul_cardio"},
)


@dataclass(frozen=True)
class PatientGroup:
    group_key: str
    ds_id: str
    patient_group_id: str
    row_indices: tuple[int, ...]
    size: int
    pos_count: int
    has_ecg: int
    sex_mode: str
    stratum: tuple[Any, ...]
    sort_digest: str


def _deterministic_digest(seed: int, ds_id: str, patient_group_id: str) -> str:
    payload = f"{seed}|{ds_id}|{patient_group_id}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _parse_modality_flags(modalities_present: str) -> tuple[int, int, int, int]:
    """Parse exact `[C, E, L, S]` tokens cleanly without matching `MISSING` substrings."""
    cleaned = re.sub(r"_\[MISSING_[^\]]+\]", "", str(modalities_present or ""))
    tokens = {tok.strip() for tok in cleaned.split("+") if tok.strip()}
    has_c = 1 if any(tok == "C" or tok.startswith("C_") for tok in tokens) else 0
    has_e = 1 if any(tok == "E" or tok.startswith("E_") for tok in tokens) else 0
    has_l = 1 if any(tok == "L" or tok.startswith("L_") for tok in tokens) else 0
    has_s = 1 if any(tok == "S" or tok.startswith("S_") for tok in tokens) else 0
    return has_c, has_e, has_l, has_s


def _parse_has_ecg(modalities_present: str) -> int:
    return _parse_modality_flags(modalities_present)[1]


def _build_patient_groups(
    rows: Sequence[Mapping[str, Any]],
    ds_id: str,
    target_col: str,
    seed: int,
) -> list[PatientGroup]:
    grouped_idxs: dict[str, list[int]] = collections.defaultdict(list)
    for idx, row in enumerate(rows):
        pid = str(row["PatientGroupID"]).strip()
        if not pid:
            raise ValueError(f"{ds_id} row index {idx} has empty PatientGroupID.")
        grouped_idxs[pid].append(idx)

    groups: list[PatientGroup] = []
    for pid, idxs in grouped_idxs.items():
        pos_cnt = sum(1 for i in idxs if str(rows[i][target_col]).strip() == "1")
        has_ecg = 1 if any(_parse_has_ecg(rows[i].get("ModalitiesPresent", "")) for i in idxs) else 0
        sex_vals = [str(rows[i].get("sex", "")).strip() or "U" for i in idxs]
        sex_mode = collections.Counter(sex_vals).most_common(1)[0][0]
        any_pos = 1 if pos_cnt > 0 else 0
        stratum = (has_ecg, any_pos, sex_mode)
        groups.append(
            PatientGroup(
                group_key=f"{ds_id}::{pid}",
                ds_id=ds_id,
                patient_group_id=pid,
                row_indices=tuple(idxs),
                size=len(idxs),
                pos_count=pos_cnt,
                has_ecg=has_ecg,
                sex_mode=sex_mode,
                stratum=stratum,
                sort_digest=_deterministic_digest(seed, ds_id, pid),
            )
        )
    return groups


def _choose_best_partition(
    current_counts: Mapping[str, int],
    total_target_in_stratum: int,
    ratios: Mapping[str, float],
    group_size: int,
    part_tie_rank: Mapping[str, int],
) -> str:
    """Select partition using scale-invariant midpoint fill ratio (after midpoint / quota target)."""
    denom = max(1, total_target_in_stratum)
    best_part = PARTITION_ORDER[0]
    best_score = float("inf")
    for part in PARTITION_ORDER:
        target = ratios[part] * denom
        if target <= 0:
            continue
        score = (current_counts[part] + 0.5 * group_size) / target
        if score < best_score - 1e-12 or (
            abs(score - best_score) <= 1e-12 and part_tie_rank[part] < part_tie_rank[best_part]
        ):
            best_score = score
            best_part = part
    return best_part


def assign_patient_grouped_splits(
    rows: Sequence[Mapping[str, Any]],
    ds_id: str,
    target_col: str,
    seed: int = DEFAULT_SPLIT_SEED,
    ratios: Mapping[str, float] | None = None,
    n_train_folds: int = 5,
) -> list[dict[str, Any]]:
    """
    Assign deterministic (`train`, `val`, `test`) partition and `cv_fold` (`0..n_train_folds-1`
    inside `train`, `-1` for `val`/`test`) preserving connected `PatientGroupID` integrity.
    """
    if ratios is None:
        ratios = PARTITION_RATIOS
    if abs(sum(ratios[p] for p in PARTITION_ORDER) - 1.0) > 1e-6:
        raise ValueError(f"Partition ratios must sum to 1.0, got {ratios}")
    if not rows:
        return []

    n = len(rows)
    row_partitions = [""] * n
    row_cv_folds = [-1] * n

    has_official_folds = (
        ds_id == "DS0001"
        and all(str(r.get("StratFold", "")).strip() != "" for r in rows)
    )

    if has_official_folds:
        groups = _build_patient_groups(rows, ds_id=ds_id, target_col=target_col, seed=seed)
        train_groups: list[PatientGroup] = []
        for g in groups:
            folds = {int(str(rows[i]["StratFold"]).strip()) for i in g.row_indices}
            if len(folds) != 1:
                raise AssertionError(
                    f"PTB-XL leakage invariant failed: patient {g.patient_group_id} spans folds {sorted(folds)}"
                )
            sf = next(iter(folds))
            if 1 <= sf <= 8:
                part = "train"
                train_groups.append(g)
            elif sf == 9:
                part = "val"
            elif sf == 10:
                part = "test"
            else:
                raise ValueError(f"Unexpected PTB-XL StratFold {sf} for patient {g.patient_group_id}")
            for i in g.row_indices:
                row_partitions[i] = part
    else:
        groups = _build_patient_groups(rows, ds_id=ds_id, target_col=target_col, seed=seed)
        by_stratum: dict[tuple[Any, ...], list[PatientGroup]] = collections.defaultdict(list)
        for g in groups:
            by_stratum[g.stratum].append(g)

        train_groups = []
        # Process larger connected patient groups first within sorted strata so quotas stay tight
        for stratum_key in sorted(by_stratum.keys()):
            stratum_groups = sorted(
                by_stratum[stratum_key],
                key=lambda x: (-x.size, x.sort_digest),
            )
            stratum_total_rows = sum(g.size for g in stratum_groups)
            stratum_counts = {p: 0 for p in PARTITION_ORDER}
            tie_rank = {"train": 0, "val": 1, "test": 2}
            for g in stratum_groups:
                chosen = _choose_best_partition(
                    current_counts=stratum_counts,
                    total_target_in_stratum=stratum_total_rows,
                    ratios=ratios,
                    group_size=g.size,
                    part_tie_rank=tie_rank,
                )
                stratum_counts[chosen] += g.size
                for i in g.row_indices:
                    row_partitions[i] = chosen
                if chosen == "train":
                    train_groups.append(g)

    # Deterministic 5-fold grouped cross-validation strictly inside `train`
    if n_train_folds > 1 and train_groups:
        tr_by_stratum: dict[tuple[Any, ...], list[PatientGroup]] = collections.defaultdict(list)
        for g in train_groups:
            tr_by_stratum[g.stratum].append(g)

        fold_load = [0] * n_train_folds
        for stratum_key in sorted(tr_by_stratum.keys()):
            s_groups = sorted(
                tr_by_stratum[stratum_key],
                key=lambda x: (-x.size, x.sort_digest),
            )
            for g in s_groups:
                best_fold = min(range(n_train_folds), key=lambda f_idx: (fold_load[f_idx], f_idx))
                fold_load[best_fold] += g.size
                for i in g.row_indices:
                    row_cv_folds[i] = best_fold

    manifest_rows: list[dict[str, Any]] = []
    for idx, r in enumerate(rows):
        part = row_partitions[idx]
        if part not in PARTITION_ORDER:
            raise AssertionError(f"Unassigned partition at {ds_id} row {idx}")
        age_str = str(r.get("age_years", "")).strip()
        mod_str = str(r.get("ModalitiesPresent", "")).strip()
        hc, he, hl, hs = _parse_modality_flags(mod_str)
        manifest_rows.append({
            "DS": ds_id,
            "RecordID": str(r["RecordID"]).strip(),
            "PatientGroupID": str(r["PatientGroupID"]).strip(),
            "GroupKey": f"{ds_id}::{str(r['PatientGroupID']).strip()}",
            "Partition": part,
            "CVFoldInTrain": str(row_cv_folds[idx]),
            "Target_y": str(r[target_col]).strip(),
            "Sex": str(r.get("sex", "")).strip(),
            "AgeYears": age_str,
            "ModalitiesPresent": mod_str,
            "HasClinical": str(hc),
            "HasECG": str(he),
            "HasLab": str(hl),
            "HasLifestyle": str(hs),
            "StratFoldSource": str(r.get("StratFold", "")).strip(),
        })

    assert_zero_patient_overlap(manifest_rows)
    return manifest_rows


def assert_zero_patient_overlap(manifest_rows: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    """
    Hard OS §4.4 / G07 invariant check:
    1. Zero `(DS, PatientGroupID)` overlap across `train`, `val`, `test`.
    2. Zero duplicate `(DS, RecordID)` rows across the entire split manifest.
    3. Zero `(DS, PatientGroupID)` overlap across internal `train` CV folds.
    """
    seen_records: set[tuple[str, str]] = set()
    groups_by_part: dict[str, set[str]] = {p: set() for p in PARTITION_ORDER}
    cv_groups: dict[str, set[str]] = collections.defaultdict(set)
    group_counts_per_key: dict[str, set[str]] = collections.defaultdict(set)

    for row in manifest_rows:
        ds = str(row["DS"]).strip()
        rec_id = str(row["RecordID"]).strip()
        g_key = str(row["GroupKey"]).strip()
        part = str(row["Partition"]).strip()
        cv_f = str(row["CVFoldInTrain"]).strip()

        if part not in PARTITION_ORDER:
            raise ValueError(f"Invalid partition tag '{part}' on {ds} record {rec_id}.")

        rec_key = (ds, rec_id)
        if rec_key in seen_records:
            raise AssertionError(f"DUPLICATE_RECORD_LEAK: {rec_key} appeared twice in split manifest!")
        seen_records.add(rec_key)

        groups_by_part[part].add(g_key)
        group_counts_per_key[g_key].add(part)

        if part == "train" and cv_f != "-1":
            cv_groups[g_key].add(cv_f)
        elif part != "train" and cv_f != "-1":
            raise AssertionError(f"NON_TRAIN_CV_FOLD_LEAK: {part} record {rec_id} received CVFoldInTrain={cv_f}")

    tr_va = groups_by_part["train"] & groups_by_part["val"]
    tr_te = groups_by_part["train"] & groups_by_part["test"]
    va_te = groups_by_part["val"] & groups_by_part["test"]
    if tr_va or tr_te or va_te:
        raise AssertionError(
            f"PATIENT_OVERLAP_LEAK: train&val={len(tr_va)}, train&test={len(tr_te)}, val&test={len(va_te)}"
        )

    multi_cv = [k for k, folds in cv_groups.items() if len(folds) > 1]
    if multi_cv:
        raise AssertionError(f"CV_FOLD_PATIENT_LEAK: {len(multi_cv)} patient groups span >1 train CV fold!")

    multi_visit_groups = sum(1 for k in group_counts_per_key if k)
    return {
        "total_records": len(seen_records),
        "unique_patient_groups": multi_visit_groups,
        "train_val_overlap": len(tr_va),
        "train_test_overlap": len(tr_te),
        "val_test_overlap": len(va_te),
        "cv_fold_overlap": len(multi_cv),
    }


def compute_balance_summary(manifest_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Compute privacy-safe aggregate partition statistics for G07 report tables."""
    buckets: dict[tuple[str, str], list[Mapping[str, Any]]] = collections.defaultdict(list)
    for r in manifest_rows:
        buckets[(str(r["DS"]), str(r["Partition"]))].append(r)
        buckets[("ALL_COHORTS", str(r["Partition"]))].append(r)

    def _stats(sub: list[Mapping[str, Any]]) -> dict[str, Any]:
        if not sub:
            return {
                "patients": 0, "encounters": 0, "pos": 0, "pos_pct": 0.0,
                "male_pct": 0.0, "female_pct": 0.0, "mean_age": None,
                "has_c": 0, "has_e": 0, "has_l": 0, "has_s": 0,
                "multi_visit_patients": 0,
            }
        pts = collections.Counter(str(r["GroupKey"]) for r in sub)
        n = len(sub)
        pos = sum(1 for r in sub if str(r["Target_y"]) == "1")
        male = sum(1 for r in sub if str(r["Sex"]) == "M")
        fem = sum(1 for r in sub if str(r["Sex"]) == "F")
        ages = [float(r["AgeYears"]) for r in sub if str(r.get("AgeYears", "")).strip() != ""]
        return {
            "patients": len(pts),
            "encounters": n,
            "pos": pos,
            "pos_pct": round(pos * 100.0 / n, 2),
            "male_pct": round(male * 100.0 / n, 2),
            "female_pct": round(fem * 100.0 / n, 2),
            "mean_age": round(sum(ages) / len(ages), 2) if ages else None,
            "has_c": sum(int(r["HasClinical"]) for r in sub),
            "has_e": sum(int(r["HasECG"]) for r in sub),
            "has_l": sum(int(r["HasLab"]) for r in sub),
            "has_s": sum(int(r["HasLifestyle"]) for r in sub),
            "multi_visit_patients": sum(1 for cnt in pts.values() if cnt > 1),
        }

    summary: dict[str, Any] = {}
    for scope in ("DS0001", "DS0002", "DS0003", "DS0004", "ALL_COHORTS"):
        if any(any(buckets[(scope, p)]) for p in PARTITION_ORDER):
            summary[scope] = {p: _stats(buckets[(scope, p)]) for p in PARTITION_ORDER}
    return summary
