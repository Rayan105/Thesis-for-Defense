"""
Whole-Cohort Structural/Clinical QA Audit & Immutable ADJ0001-ADJ0004 Release Freezer (STEP-018).

Reads the four curated ADJB0001-ADJB0004 batches in Tier 2B, executes exhaustive cross-cohort
integrity checks, freezes immutable `ADJ0001..ADJ0004` releases inside gitignored
`04_Outcome_Schema_QA/adjudications/ADJ####/`, computes STARD/CONSORT flow counts, missingness
matrices (UD10), and prints exact SHA-256 hashes for `adjudication_registry.csv` & G06 audit.
"""

from __future__ import annotations

import collections
import csv
import hashlib
import os
import shutil
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ADJ_ROOT = os.path.join(REPO_ROOT, "04_Outcome_Schema_QA", "adjudications")
DATASET_ROOT = os.path.join(REPO_ROOT, "Dataset")


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def audit_and_freeze_one(batch_id: str, adj_id: str, ds_id: str, target_col: str) -> dict[str, object]:
    src_dir = os.path.join(ADJ_ROOT, batch_id)
    dst_dir = os.path.join(ADJ_ROOT, adj_id)
    os.makedirs(dst_dir, exist_ok=True)

    src_nat = os.path.join(src_dir, "native_snapshot.csv")
    src_ver = os.path.join(src_dir, "verified_curated.csv")
    dst_nat = os.path.join(dst_dir, "native_snapshot.csv")
    dst_ver = os.path.join(dst_dir, "verified_curated.csv")

    with open(src_ver, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    # 1. Whole-cohort uniqueness & grouping invariants
    rec_ids = [r["RecordID"] for r in rows]
    assert len(rec_ids) == len(set(rec_ids)), f"{adj_id}: Duplicate RecordID found!"

    # Check eligible vs excluded strict invariants
    eligible = [r for r in rows if r["CurationStatus"] == "Eligible_Included"]
    quarantined = [r for r in rows if r["CurationStatus"] != "Eligible_Included"]

    violations = 0
    for r in eligible:
        if r[target_col] not in ("0", "1"):
            violations += 1
        if not r["TemporalAlignmentStatus"].startswith("PASS_"):
            violations += 1
        if ds_id in ("DS0001", "DS0002", "DS0004"):
            if not r["age_years"] or float(r["age_years"]) < 18.0:
                violations += 1
        elif r["age_years"] and float(r["age_years"]) < 18.0:
            violations += 1
        if r.get("sbp_mmhg") and r.get("dbp_mmhg"):
            sbp, dbp = float(r["sbp_mmhg"]), float(r["dbp_mmhg"])
            sbp_max = 280.0 if ds_id == "DS0002" else 250.0
            if sbp <= dbp or sbp < 50.0 or sbp > sbp_max or dbp < 30.0 or dbp > 180.0:
                violations += 1
        if r.get("ldl_estimated_mgdl") and float(r["ldl_estimated_mgdl"]) < 0.0:
            violations += 1

    # Zero coerced uncertain targets in quarantined rows
    for r in quarantined:
        assert r[target_col] == "UNCERTAIN_EXCLUDED", f"{adj_id}: Quarantined row coerced to {r[target_col]}!"

    # Check DS0001 fold grouping (no patient spanning multiple strat_folds)
    fold_cross = 0
    if ds_id == "DS0001":
        pfolds = collections.defaultdict(set)
        for r in eligible:
            pfolds[r["PatientGroupID"]].add(r["StratFold"])
        fold_cross = sum(1 for s in pfolds.values() if len(s) > 1)
        assert fold_cross == 0, f"{adj_id}: {fold_cross} patients span >1 strat_fold!"

    # Check DS0002 PNG paths exist if C+E_png+L
    orphan_png = 0
    if ds_id == "DS0002":
        ecg_dir = os.path.join(DATASET_ROOT, "3. DS0003_cardiomled (CARDIO-ML-ED, Mendeley Official CC BY 4.0)", "ECGS")
        for r in eligible:
            if r["ModalitiesPresent"] == "C+E_png+L" and int(r["LinkedPNGCount"]) < 1:
                orphan_png += 1
        assert os.path.isdir(ecg_dir) and orphan_png == 0

    # Copy ONLY verified eligible rows cleanly into frozen verified_eligible_only.csv as well as full release
    dst_el = os.path.join(dst_dir, "verified_eligible_only.csv")
    shutil.copy2(src_nat, dst_nat)
    shutil.copy2(src_ver, dst_ver)
    with open(dst_el, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(eligible)

    nat_hash = sha256_file(dst_nat)
    ver_hash = sha256_file(dst_ver)
    el_hash = sha256_file(dst_el)

    # Missingness summary across key clinical/lab columns inside Eligible rows
    el_miss = {}
    for col in rows[0].keys():
        m = sum(1 for r in eligible if r[col] == "")
        if m > 0:
            el_miss[col] = f"{m} ({m*100.0/len(eligible):.1f}%)"

    u_all = len(set(r["PatientGroupID"] for r in rows))
    u_el = len(set(r["PatientGroupID"] for r in eligible))
    pos = sum(1 for r in eligible if r[target_col] == "1")
    neg = sum(1 for r in eligible if r[target_col] == "0")
    q_break = dict(collections.Counter(r["CurationStatus"] for r in quarantined))

    return {
        "adj_id": adj_id, "batch_id": batch_id, "ds_id": ds_id,
        "total_rows": len(rows), "unique_all": u_all,
        "eligible_rows": len(eligible), "unique_el": u_el,
        "pos": pos, "neg": neg, "quarantined": len(quarantined),
        "quarantine_breakdown": q_break,
        "violations": violations, "fold_cross": fold_cross,
        "nat_hash": nat_hash, "ver_hash": ver_hash, "el_hash": el_hash,
        "eligible_missingness": el_miss,
    }


def main() -> None:
    specs = [
        ("ADJB0001", "ADJ0001", "DS0001", "Target_y_ptb_nonnorm"),
        ("ADJB0002", "ADJ0002", "DS0002", "Target_y_ed_initial"),
        ("ADJB0003", "ADJ0003", "DS0003", "Target_y_cair_high"),
        ("ADJB0004", "ADJ0004", "DS0004", "Target_y_sul_cardio"),
    ]
    results = []
    tot_all = tot_el = tot_q = tot_pos = tot_neg = 0
    for b, a, d, t in specs:
        res = audit_and_freeze_one(b, a, d, t)
        results.append(res)
        tot_all += res["total_rows"]
        tot_el += res["eligible_rows"]
        tot_q += res["quarantined"]
        tot_pos += res["pos"]
        tot_neg += res["neg"]
        print(f"\n=== [{res['adj_id']} / {res['ds_id']}] Whole-Cohort QA & Freeze ===")
        print(f"Screened={res['total_rows']} (pts={res['unique_all']}) -> Eligible={res['eligible_rows']} (pts={res['unique_el']}; pos={res['pos']}, neg={res['neg']}) | Quarantined={res['quarantined']} {res['quarantine_breakdown']}")
        print(f"Invariant violations={res['violations']} | Cross-fold patient leaks={res['fold_cross']}")
        print(f"Eligible missingness (>0): {res['eligible_missingness']}")
        print(f"NativeHash={res['nat_hash']}")
        print(f"FullReleaseHash(VerifiedHash)={res['ver_hash']}")
        print(f"EligibleOnlyHash={res['el_hash']}")

    print(f"\n=== CUMULATIVE CONSORT FLOW (ADJ0001-ADJ0004) ===")
    print(f"Total Screened={tot_all} | Clean Eligible={tot_el} (CVD+={tot_pos}, Neg={tot_neg}) | Excluded/Quarantined={tot_q} | Violations={sum(r['violations'] for r in results)}")

    # Print current G05 frozen input hashes
    for p in ("04_Outcome_Schema_QA/endpoint_charter.md", "04_Outcome_Schema_QA/variables.csv", "04_Outcome_Schema_QA/ecg_contract.md", "04_Outcome_Schema_QA/qa_protocol.md"):
        print(f"SchemaHash {p}: {sha256_file(os.path.join(REPO_ROOT, p))}")


if __name__ == "__main__":
    main()
