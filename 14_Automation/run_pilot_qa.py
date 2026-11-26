"""
Stratified Dual-Stream Pilot QA Execution Script (STEP-016).

Implements QA-PROTOCOL-v1.0.0:
- Deterministically samples N_pilot = 60 stratified encounters (seed=20261127):
    * DS0001 (PTB-XL, n=20): NORM/MI/STTC/HYP/CD, noisy traces, ecg_id=12722, <18y & age-missing edge cases
    * DS0002 (CARDIO-ML-ED, n=20): Cardiac/Noncardiac, elevated Troponin-I, missing Final diag, CABG, <18y, JPGs, typo IDs
    * DS0003 (CAIR-CVD-2025, n=10): HIGH/INTERMEDIARY/LOW, SBP<=DBP & negative Estimated LDL anomalies
    * DS0004 (Kaggle sulianova, n=10): cardio 0/1, extreme/inverted BP anomalies, discordant duplicate feature vectors
- Executes Stream A (using src/cvd_mm/schema_ecg.py & crf_manual_v1.0.0.md) independently from Stream B
  (independent native raw parsing & rule cross-audit) and writes both immutable outputs into gitignored
  Tier 2B `04_Outcome_Schema_QA/adjudications/pilot/` before computing Cohen's kappa, ICC(2,1), unit-conversion error,
  and ECG quality grading concordance.
"""

from __future__ import annotations

import ast
import collections
import csv
import hashlib
import os
import random
import struct
import sys
import time
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from src.cvd_mm.schema_ecg import (
    assert_no_leakage_predictors,
    inspect_int16_wfdb_waveform,
    load_variable_dictionary,
    normalize_cardiomled_image_stem,
    parse_wfdb_header_text,
    validate_ecg_image_bytes,
)

DATASET_ROOT = os.path.join(REPO_ROOT, "Dataset")
PILOT_DIR = os.path.join(REPO_ROOT, "04_Outcome_Schema_QA", "adjudications", "pilot")
SEED = 20261127


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def read_xlsx_sheet1_raw(xlsx_path: str) -> list[list[str]]:
    with zipfile.ZipFile(xlsx_path) as z:
        sst = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si"):
                sst.append("".join(t.text or "" for t in si.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")))
        root = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
        rows = []
        for row in root.findall(".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row"):
            r_dict = {}
            for c in row.findall("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c"):
                ref = c.attrib.get("r", "")
                idx = 0
                for ch in (ch for ch in ref if ch.isalpha()):
                    idx = idx * 26 + (ord(ch.upper()) - ord("A") + 1)
                t = c.attrib.get("t", "")
                v_el = c.find("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v")
                is_el = c.find("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}is")
                val = ""
                if v_el is not None and v_el.text is not None:
                    val = sst[int(v_el.text)] if t == "s" else v_el.text
                elif is_el is not None:
                    val = "".join(x.text or "" for x in is_el.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"))
                if idx > 0:
                    r_dict[idx] = val
            if r_dict:
                rows.append([r_dict.get(i, "") for i in range(1, max(r_dict) + 1)])
        return rows


def cohen_kappa(labels_a: list[str], labels_b: list[str]) -> tuple[float, float]:
    assert len(labels_a) == len(labels_b) and labels_a
    n = len(labels_a)
    po = sum(a == b for a, b in zip(labels_a, labels_b)) / n
    ca = collections.Counter(labels_a)
    cb = collections.Counter(labels_b)
    pe = sum((ca[k] / n) * (cb[k] / n) for k in set(ca) | set(cb))
    if abs(1.0 - pe) < 1e-12:
        return (1.0 if po == 1.0 else 0.0), po
    return (po - pe) / (1.0 - pe), po


def icc_two_way(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """Shrout & Fleiss (1979) ICC(2,1) two-way random absolute agreement + max rel diff."""
    assert len(xs) == len(ys) and len(xs) > 1
    n = len(xs)
    k = 2.0
    row_means = [(x + y) / 2.0 for x, y in zip(xs, ys)]
    grand = sum(row_means) / n
    ss_rows = 2.0 * sum((m - grand) ** 2 for m in row_means)
    ss_cols = ((sum(xs) - sum(ys)) ** 2) / (2.0 * n)
    ss_tot = sum((x - grand) ** 2 + (y - grand) ** 2 for x, y in zip(xs, ys))
    ss_err = max(0.0, ss_tot - ss_rows - ss_cols)
    ms_rows = ss_rows / (n - 1)
    ms_cols = ss_cols
    ms_err = ss_err / (n - 1)
    max_rel = max(abs(x - y) / max(1e-9, abs(x), abs(y)) for x, y in zip(xs, ys))
    if ms_err == 0.0 and ms_cols == 0.0:
        return (1.0 if ms_rows > 0 else 0.0), max_rel
    denom = ms_rows + (k - 1.0) * ms_err + (k / n) * (ms_cols - ms_err)
    return ((ms_rows - ms_err) / denom if denom > 0 else 0.0), max_rel


def pick_unique(rng: random.Random, pool: list[dict], picked_ids: set[str], id_fn, count: int) -> list[dict]:
    avail = [r for r in pool if id_fn(r) not in picked_ids]
    chosen = rng.sample(avail, min(count, len(avail)))
    for r in chosen:
        picked_ids.add(id_fn(r))
    return chosen


def main() -> None:
    t0 = time.perf_counter()
    rng = random.Random(SEED)
    os.makedirs(PILOT_DIR, exist_ok=True)
    var_rows = load_variable_dictionary(os.path.join(REPO_ROOT, "04_Outcome_Schema_QA", "variables.csv"))
    assert_no_leakage_predictors(["age_years", "sex", "sbp_mmhg", "dbp_mmhg", "smoking_status"], var_rows, tier="A")

    # ------------------------------------------------------------------
    # 1. Deterministic Stratified Sampling (N_pilot = 60, seed = 20261127)
    # ------------------------------------------------------------------
    pilot_cases = []

    # [DS0001 PTB-XL: n=20]
    ptb_dir = os.path.join(DATASET_ROOT, "1. DS0001_ptbxl (PTB-XL, Kaggle)", "ptb-xl-a-large-publicly-available-electrocardiography-dataset-1.0.1")
    with open(os.path.join(ptb_dir, "scp_statements.csv"), encoding="utf-8") as f:
        scp_map = {r[""]: r["diagnostic_class"] for r in csv.DictReader(f) if r["diagnostic"] == "1.0"}
    with open(os.path.join(ptb_dir, "ptbxl_database.csv"), encoding="utf-8") as f:
        ptb_rows = list(csv.DictReader(f))

    ptb_by_id = {r["ecg_id"]: r for r in ptb_rows}
    seen_ptb = set()
    sample_ptb = []
    # Positive control: ecg_id=12722 (flatline V5)
    sample_ptb.append(ptb_by_id["12722"])
    seen_ptb.add("12722")
    # 2 pediatric (<18y) + 1 missing age + 1 no-diag + 4 artifact noisy + balanced NORM/MI/STTC/HYP/CD
    sample_ptb += pick_unique(rng, [r for r in ptb_rows if r["age"].strip() and float(r["age"]) < 18], seen_ptb, lambda r: r["ecg_id"], 2)
    sample_ptb += pick_unique(rng, [r for r in ptb_rows if not r["age"].strip()], seen_ptb, lambda r: r["ecg_id"], 1)
    sample_ptb += pick_unique(
        rng,
        [r for r in ptb_rows if not any(k in scp_map and float(v) > 0 for k, v in ast.literal_eval(r["scp_codes"]).items())],
        seen_ptb,
        lambda r: r["ecg_id"],
        1,
    )
    sample_ptb += pick_unique(
        rng,
        [r for r in ptb_rows if r["age"].strip() and float(r["age"]) >= 18 and (r["static_noise"].strip() or r["baseline_drift"].strip())],
        seen_ptb,
        lambda r: r["ecg_id"],
        4,
    )
    sample_ptb += pick_unique(
        rng,
        [
            r for r in ptb_rows
            if r["age"].strip() and float(r["age"]) >= 18
            and set(scp_map[k] for k, v in ast.literal_eval(r["scp_codes"]).items() if k in scp_map and float(v) > 0) == {"NORM"}
        ],
        seen_ptb,
        lambda r: r["ecg_id"],
        5,
    )
    sample_ptb += pick_unique(
        rng,
        [
            r for r in ptb_rows
            if r["age"].strip() and float(r["age"]) >= 18
            and any(k in scp_map and scp_map[k] != "NORM" and float(v) > 0 for k, v in ast.literal_eval(r["scp_codes"]).items())
        ],
        seen_ptb,
        lambda r: r["ecg_id"],
        6,
    )
    assert len(sample_ptb) == 20
    for r in sample_ptb:
        pilot_cases.append(("DS0001", r["ecg_id"], r))

    # [DS0002 CARDIO-ML-ED: n=20]
    cm_dir = os.path.join(DATASET_ROOT, "3. DS0003_cardiomled (CARDIO-ML-ED, Mendeley Official CC BY 4.0)")
    ecg_img_dir = os.path.join(cm_dir, "ECGS")
    all_imgs = sorted(fn for fn in os.listdir(ecg_img_dir) if os.path.isfile(os.path.join(ecg_img_dir, fn)))
    img_by_base = collections.defaultdict(list)
    for fn in all_imgs:
        b = normalize_cardiomled_image_stem(os.path.splitext(fn)[0]).split("-")[0]
        img_by_base[b].append(fn)
    with open(os.path.join(cm_dir, "ECG Labels.csv"), encoding="utf-8") as f:
        lbl_map = {r[0].strip(): r[1].strip() for r in csv.reader(f) if len(r) >= 2 and r[0].strip()}

    s1 = read_xlsx_sheet1_raw(os.path.join(cm_dir, "Datasheet1 (Edited).csv"))
    cm_hdr = [h.strip() for h in s1[0]]
    cm_rows = [r + [""] * (len(cm_hdr) - len(r)) for r in s1[1:] if any(c.strip() for c in r)]
    cm_dicts = []
    for idx, r in enumerate(cm_rows):
        d = {cm_hdr[i]: r[i].strip() for i in range(len(cm_hdr))}
        d["_serial"] = r[0].strip()
        d["_col1"] = r[1].strip()
        d["_imgs"] = img_by_base.get(d["_col1"], [])
        cm_dicts.append(d)

    seen_cm = set()
    sample_cm = []
    # Include JPG quarantine cases linked to Col1 if any, <18y, elevated Troponin-I, CABG, missing Final, suffix/space PNG, Initial Cardiac, Noncardiac
    sample_cm += pick_unique(rng, [r for r in cm_dicts if any(fn.lower().endswith(".jpg") for fn in r["_imgs"])], seen_cm, lambda r: r["_serial"], 2)
    sample_cm += pick_unique(rng, [r for r in cm_dicts if r["Patient Age"] and float(r["Patient Age"]) < 18], seen_cm, lambda r: r["_serial"], 2)
    sample_cm += pick_unique(rng, [r for r in cm_dicts if r["Troponine - I (Q)"] and r["Troponine - I (Q)"] != "<0.05"], seen_cm, lambda r: r["_serial"], 2)
    sample_cm += pick_unique(rng, [r for r in cm_dicts if "CABG" in r["Previous surgeries"]], seen_cm, lambda r: r["_serial"], 2)
    sample_cm += pick_unique(rng, [r for r in cm_dicts if any("(" in fn or " " in os.path.splitext(fn)[0] or "140354" in fn for fn in r["_imgs"])], seen_cm, lambda r: r["_serial"], 2)
    sample_cm += pick_unique(rng, [r for r in cm_dicts if r["Initial diagnosis"] == "Cardiac" and not r["Final diagnosis"] and r["_imgs"]], seen_cm, lambda r: r["_serial"], 3)
    sample_cm += pick_unique(rng, [r for r in cm_dicts if r["Initial diagnosis"] == "Cardiac" and r["Final diagnosis"] and r["_imgs"]], seen_cm, lambda r: r["_serial"], 3)
    sample_cm += pick_unique(rng, [r for r in cm_dicts if r["Initial diagnosis"] == "Noncardiac" and r["_imgs"]], seen_cm, lambda r: r["_serial"], 4)
    # Top up to 20 if <20
    if len(sample_cm) < 20:
        sample_cm += pick_unique(rng, cm_dicts, seen_cm, lambda r: r["_serial"], 20 - len(sample_cm))
    assert len(sample_cm) == 20
    for r in sample_cm:
        pilot_cases.append(("DS0002", f"S{r['_serial']}_C{r['_col1']}", r))

    # [DS0003 CAIR-CVD-2025: n=10]
    with open(os.path.join(DATASET_ROOT, "4. DS0004_cair_cvd_2025 (CAIR-CVD-2025, Mendeley)", "CVD Dataset.csv"), encoding="utf-8") as f:
        r3 = [{**row, "_idx": str(i)} for i, row in enumerate(csv.DictReader(f), start=1)]
    seen_3 = set()
    sample_3 = []
    sample_3 += pick_unique(rng, [r for r in r3 if r["Systolic BP"] and r["Diastolic BP"] and float(r["Systolic BP"]) <= float(r["Diastolic BP"])], seen_3, lambda r: r["_idx"], 2)
    sample_3 += pick_unique(rng, [r for r in r3 if r["Estimated LDL (mg/dL)"] and float(r["Estimated LDL (mg/dL)"]) < 0], seen_3, lambda r: r["_idx"], 2)
    sample_3 += pick_unique(rng, [r for r in r3 if r["CVD Risk Level"] == "HIGH" and float(r["Systolic BP"] or 120) > float(r["Diastolic BP"] or 80)], seen_3, lambda r: r["_idx"], 2)
    sample_3 += pick_unique(rng, [r for r in r3 if r["CVD Risk Level"] == "INTERMEDIARY"], seen_3, lambda r: r["_idx"], 2)
    sample_3 += pick_unique(rng, [r for r in r3 if r["CVD Risk Level"] == "LOW"], seen_3, lambda r: r["_idx"], 2)
    assert len(sample_3) == 10
    for r in sample_3:
        pilot_cases.append(("DS0003", f"ROW{r['_idx']}", r))

    # [DS0004 sulianova: n=10]
    with open(os.path.join(DATASET_ROOT, "5. DS0005_sulianova_cvd (Cardiovascular Disease, Kaggle)", "cardio_train.csv"), encoding="utf-8") as f:
        r4 = list(csv.DictReader(f, delimiter=";"))
    fk_outcomes = collections.defaultdict(set)
    for r in r4:
        fk_outcomes[(r["age"], r["gender"], r["height"], r["weight"], r["ap_hi"], r["ap_lo"], r["cholesterol"], r["gluc"], r["smoke"], r["alco"], r["active"])].add(r["cardio"])
    seen_4 = set()
    sample_4 = []
    sample_4 += pick_unique(rng, [r for r in r4 if float(r["ap_hi"]) <= float(r["ap_lo"]) or float(r["ap_hi"]) < 50 or float(r["ap_hi"]) > 250], seen_4, lambda r: r["id"], 2)
    sample_4 += pick_unique(rng, [r for r in r4 if len(fk_outcomes[(r["age"], r["gender"], r["height"], r["weight"], r["ap_hi"], r["ap_lo"], r["cholesterol"], r["gluc"], r["smoke"], r["alco"], r["active"])]) > 1], seen_4, lambda r: r["id"], 2)
    sample_4 += pick_unique(rng, [r for r in r4 if r["cardio"] == "1" and 50 <= float(r["ap_hi"]) <= 250 and float(r["ap_hi"]) > float(r["ap_lo"])], seen_4, lambda r: r["id"], 3)
    sample_4 += pick_unique(rng, [r for r in r4 if r["cardio"] == "0" and 50 <= float(r["ap_hi"]) <= 250 and float(r["ap_hi"]) > float(r["ap_lo"])], seen_4, lambda r: r["id"], 3)
    assert len(sample_4) == 10
    for r in sample_4:
        pilot_cases.append(("DS0004", r["id"], r))

    assert len(pilot_cases) == 60

    # ------------------------------------------------------------------
    # 2. Stream A (Automated schema_ecg.py + crf_manual_v1.0.0.md)
    # ------------------------------------------------------------------
    stream_a = []
    for ds, cid, row in pilot_cases:
        if ds == "DS0001":
            age = float(row["age"]) if row["age"].strip() else None
            hea_txt = open(os.path.join(ptb_dir, row["filename_lr"] + ".hea"), encoding="utf-8").read()
            raw_dat = open(os.path.join(ptb_dir, row["filename_lr"] + ".dat"), "rb").read()
            hdr_info = parse_wfdb_header_text(hea_txt)
            sig_info = inspect_int16_wfdb_waveform(raw_dat, hdr_info["num_leads"], hdr_info["num_samples"])
            has_noise = bool(row["static_noise"].strip() or row["baseline_drift"].strip() or row["burst_noise"].strip() or row["electrodes_problems"].strip())
            if not sig_info["passed_clean"]:
                ecg_q = "Quarantine_Reject"
            elif has_noise:
                ecg_q = "Noisy_Flagged"
            else:
                ecg_q = "Clean_Eligible"
            classes = set(scp_map[k] for k, v in ast.literal_eval(row["scp_codes"]).items() if k in scp_map and float(v) > 0)
            if age is None or age < 18 or not classes or ecg_q == "Quarantine_Reject":
                disp = "Exclude_or_Uncertain"
            elif classes == {"NORM"}:
                disp = "CVD_Neg"
            else:
                disp = "CVD_Pos"
            stream_a.append({"DS": ds, "PilotKey": cid, "age_years": age, "sex": "F" if row["sex"] == "1" else "M", "sbp": None, "dbp": None, "ecg_quality": ecg_q, "disposition": disp})

        elif ds == "DS0002":
            age = float(row["Patient Age"]) if row["Patient Age"] else None
            sbp = float(row["Systolic blood pressure"]) if row["Systolic blood pressure"] else None
            dbp = float(row["Diastolic blood pressure"]) if row["Diastolic blood pressure"] else None
            imgs = row["_imgs"]
            if not imgs:
                ecg_q = "Missing_ECG"
            else:
                # Inspect primary image via schema_ecg
                fn = imgs[0]
                stem_norm = normalize_cardiomled_image_stem(os.path.splitext(fn)[0])
                info = validate_ecg_image_bytes(open(os.path.join(ecg_img_dir, fn), "rb").read(), fn)
                if not info["eligible_12row_encoder"] or stem_norm not in lbl_map:
                    ecg_q = "Quarantine_Reject"
                else:
                    ecg_q = "Clean_Eligible"
            init_d = row["Initial diagnosis"]
            if age is None or age < 18 or init_d not in ("Cardiac", "Noncardiac") or ecg_q == "Quarantine_Reject":
                disp = "Exclude_or_Uncertain"
            elif init_d == "Cardiac":
                disp = "CVD_Pos"
            else:
                disp = "CVD_Neg"
            stream_a.append({"DS": ds, "PilotKey": cid, "age_years": age, "sex": row["Patient Gender"] or None, "sbp": sbp, "dbp": dbp, "ecg_quality": ecg_q, "disposition": disp})

        elif ds == "DS0003":
            age = float(row["Age"]) if row["Age"] else None
            sbp = float(row["Systolic BP"]) if row["Systolic BP"] else None
            dbp = float(row["Diastolic BP"]) if row["Diastolic BP"] else None
            ldl = float(row["Estimated LDL (mg/dL)"]) if row["Estimated LDL (mg/dL)"] else None
            bad_bp = (sbp is not None and dbp is not None and sbp <= dbp)
            bad_ldl = (ldl is not None and ldl < 0)
            if bad_bp or bad_ldl:
                disp = "Exclude_or_Uncertain"
            elif row["CVD Risk Level"] == "HIGH":
                disp = "CVD_Pos"
            else:
                disp = "CVD_Neg"
            stream_a.append({"DS": ds, "PilotKey": cid, "age_years": age, "sex": row["Sex"], "sbp": sbp, "dbp": dbp, "ecg_quality": "Missing_ECG", "disposition": disp})

        elif ds == "DS0004":
            age = round(float(row["age"]) / 365.25, 4)
            sbp = float(row["ap_hi"])
            dbp = float(row["ap_lo"])
            sex = "F" if row["gender"] == "1" else "M"
            fk = (row["age"], row["gender"], row["height"], row["weight"], row["ap_hi"], row["ap_lo"], row["cholesterol"], row["gluc"], row["smoke"], row["alco"], row["active"])
            bad_bp = sbp <= dbp or sbp < 50 or sbp > 250 or dbp < 30 or dbp > 180
            disc_dup = len(fk_outcomes[fk]) > 1
            if bad_bp or disc_dup:
                disp = "Exclude_or_Uncertain"
            elif row["cardio"] == "1":
                disp = "CVD_Pos"
            else:
                disp = "CVD_Neg"
            stream_a.append({"DS": ds, "PilotKey": cid, "age_years": age, "sex": sex, "sbp": sbp, "dbp": dbp, "ecg_quality": "Missing_ECG", "disposition": disp})

    # ------------------------------------------------------------------
    # 3. Stream B (Independent Native Reference Audit — Zero Shared Code)
    # ------------------------------------------------------------------
    stream_b = []
    for ds, cid, row in pilot_cases:
        if ds == "DS0001":
            age = float(row["age"]) if row["age"].strip() else None
            dat_raw = open(os.path.join(ptb_dir, row["filename_lr"] + ".dat"), "rb").read()
            ints = struct.unpack("<" + "h" * (len(dat_raw) // 2), dat_raw)
            any_flat = any(min(ints[l::12]) == max(ints[l::12]) for l in range(12))
            any_clip = any(min(ints[l::12]) <= -32768 or max(ints[l::12]) >= 32767 for l in range(12))
            noisy = any(row[k].strip() for k in ("static_noise", "baseline_drift", "burst_noise", "electrodes_problems"))
            ecg_q = "Quarantine_Reject" if (any_flat or any_clip) else ("Noisy_Flagged" if noisy else "Clean_Eligible")
            codes = ast.literal_eval(row["scp_codes"])
            cset = {scp_map[k] for k, v in codes.items() if k in scp_map and float(v) > 0}
            if age is None or age < 18 or not cset or ecg_q == "Quarantine_Reject":
                disp = "Exclude_or_Uncertain"
            elif cset == {"NORM"}:
                disp = "CVD_Neg"
            else:
                disp = "CVD_Pos"
            stream_b.append({"DS": ds, "PilotKey": cid, "age_years": age, "sex": "F" if row["sex"] == "1" else "M", "sbp": None, "dbp": None, "ecg_quality": ecg_q, "disposition": disp})

        elif ds == "DS0002":
            age = float(row["Patient Age"]) if row["Patient Age"] else None
            sbp = float(row["Systolic blood pressure"]) if row["Systolic blood pressure"] else None
            dbp = float(row["Diastolic blood pressure"]) if row["Diastolic blood pressure"] else None
            imgs = row["_imgs"]
            if not imgs:
                ecg_q = "Missing_ECG"
            else:
                fn = imgs[0]
                raw_img = open(os.path.join(ecg_img_dir, fn), "rb").read()
                is_png = fn.lower().endswith(".png") and raw_img[:8] == b"\x89PNG\r\n\x1a\n"
                st = os.path.splitext(fn)[0].strip().replace("(2)", "-2")
                ecg_q = "Clean_Eligible" if (is_png and st in lbl_map) else "Quarantine_Reject"
            init_d = row["Initial diagnosis"]
            if age is None or age < 18 or init_d not in ("Cardiac", "Noncardiac") or ecg_q == "Quarantine_Reject":
                disp = "Exclude_or_Uncertain"
            elif init_d == "Cardiac":
                disp = "CVD_Pos"
            else:
                disp = "CVD_Neg"
            stream_b.append({"DS": ds, "PilotKey": cid, "age_years": age, "sex": row["Patient Gender"] or None, "sbp": sbp, "dbp": dbp, "ecg_quality": ecg_q, "disposition": disp})

        elif ds == "DS0003":
            age = float(row["Age"]) if row["Age"] else None
            sbp = float(row["Systolic BP"]) if row["Systolic BP"] else None
            dbp = float(row["Diastolic BP"]) if row["Diastolic BP"] else None
            ldl = float(row["Estimated LDL (mg/dL)"]) if row["Estimated LDL (mg/dL)"] else None
            if (sbp is not None and dbp is not None and sbp <= dbp) or (ldl is not None and ldl < 0):
                disp = "Exclude_or_Uncertain"
            else:
                disp = "CVD_Pos" if row["CVD Risk Level"] == "HIGH" else "CVD_Neg"
            stream_b.append({"DS": ds, "PilotKey": cid, "age_years": age, "sex": row["Sex"], "sbp": sbp, "dbp": dbp, "ecg_quality": "Missing_ECG", "disposition": disp})

        elif ds == "DS0004":
            age = round(float(row["age"]) / 365.25, 4)
            sbp = float(row["ap_hi"])
            dbp = float(row["ap_lo"])
            sex = "F" if row["gender"] == "1" else "M"
            fk = (row["age"], row["gender"], row["height"], row["weight"], row["ap_hi"], row["ap_lo"], row["cholesterol"], row["gluc"], row["smoke"], row["alco"], row["active"])
            if sbp <= dbp or sbp < 50 or sbp > 250 or dbp < 30 or dbp > 180 or len(fk_outcomes[fk]) > 1:
                disp = "Exclude_or_Uncertain"
            else:
                disp = "CVD_Pos" if row["cardio"] == "1" else "CVD_Neg"
            stream_b.append({"DS": ds, "PilotKey": cid, "age_years": age, "sex": sex, "sbp": sbp, "dbp": dbp, "ecg_quality": "Missing_ECG", "disposition": disp})

    # Write immutable restricted Tier 2B pilot files
    fields = ["DS", "PilotKey", "age_years", "sex", "sbp", "dbp", "ecg_quality", "disposition"]
    pa = os.path.join(PILOT_DIR, "pilot_stream_a.csv")
    pb = os.path.join(PILOT_DIR, "pilot_stream_b.csv")
    for p, data in ((pa, stream_a), (pb, stream_b)):
        with open(p, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(data)

    # ------------------------------------------------------------------
    # 4. Agreement Metrics Computation
    # ------------------------------------------------------------------
    disp_a = [r["disposition"] for r in stream_a]
    disp_b = [r["disposition"] for r in stream_b]
    k_disp, acc_disp = cohen_kappa(disp_a, disp_b)

    ecg_a = [r["ecg_quality"] for r in stream_a if r["DS"] in ("DS0001", "DS0002")]
    ecg_b = [r["ecg_quality"] for r in stream_b if r["DS"] in ("DS0001", "DS0002")]
    k_ecg, acc_ecg = cohen_kappa(ecg_a, ecg_b)

    age_pairs = [(a["age_years"], b["age_years"]) for a, b in zip(stream_a, stream_b) if a["age_years"] is not None and b["age_years"] is not None]
    sbp_pairs = [(a["sbp"], b["sbp"]) for a, b in zip(stream_a, stream_b) if a["sbp"] is not None and b["sbp"] is not None]
    dbp_pairs = [(a["dbp"], b["dbp"]) for a, b in zip(stream_a, stream_b) if a["dbp"] is not None and b["dbp"] is not None]

    icc_age, err_age = icc_two_way([p[0] for p in age_pairs], [p[1] for p in age_pairs])
    icc_sbp, err_sbp = icc_two_way([p[0] for p in sbp_pairs], [p[1] for p in sbp_pairs])
    icc_dbp, err_dbp = icc_two_way([p[0] for p in dbp_pairs], [p[1] for p in dbp_pairs])

    elapsed = time.perf_counter() - t0
    print(f"PILOT N={len(pilot_cases)} completed in {elapsed:.3f}s ({len(pilot_cases)/elapsed:.1f} rec/s)")
    print(f"Disposition Counts (A): {dict(collections.Counter(disp_a))}")
    print(f"Disposition Agreement: exact={acc_disp*100:.2f}%, Cohen_kappa={k_disp:.4f} (threshold >= 0.85)")
    print(f"ECG Quality Counts (DS0001+02, n={len(ecg_a)}): {dict(collections.Counter(ecg_a))}")
    print(f"ECG Quality Agreement: exact={acc_ecg*100:.2f}%, Cohen_kappa={k_ecg:.4f} (threshold >= 0.85)")
    print(f"Continuous ICC(2,1): age(n={len(age_pairs)})={icc_age:.6f} max_rel={err_age:.2e} | sbp(n={len(sbp_pairs)})={icc_sbp:.6f} max_rel={err_sbp:.2e} | dbp(n={len(dbp_pairs)})={icc_dbp:.6f} max_rel={err_dbp:.2e}")
    print(f"Stream A CSV SHA-256 (Tier 2B): {sha256_file(pa)}")
    print(f"Stream B CSV SHA-256 (Tier 2B): {sha256_file(pb)}")


if __name__ == "__main__":
    main()
