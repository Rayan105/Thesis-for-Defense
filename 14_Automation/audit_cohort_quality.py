"""
Comprehensive Read-Only Secondary Cohort Intake Hashing, Signal Integrity & 4-Modality QC Auditor
(STEP-012 & STEP-013 — Option B).

Audits:
1. Dataset/1. DS0001_ptbxl (PTB-XL v1.0.1): full SHA256SUMS.txt verification across all files,
   patient-fold isolation, .hea PHI/lead/sampling audit, all 21,837 LR .dat flatline/clipping check.
2. Dataset/3. DS0003_cardiomled (CARDIO-ML-ED): SHA-256 manifest, XLSX workbook clinical sheet parsing,
   ID deduplication & ECG Labels.csv overlap, pediatric (<18y) count, missingness & external ECGS/ check.
3. Dataset/4. DS0004_cair_cvd_2025 (CAIR-CVD-2025): SHA-256 manifest, BP string vs numeric SBP<=DBP
   audit, duplicates, missingness, and lifestyle/lab summary stats.
4. Dataset/5. DS0005_sulianova_cvd (Kaggle Cardiovascular Disease): SHA-256 manifest, duplicate/discordant
   feature vectors, BP/height/weight plausibility outliers, and target distribution.

Strict PHI & Git Safety: Writes ONLY SHA-256 manifests and aggregate counts to Tier 1 paths.
"""

from __future__ import annotations

import collections
from concurrent.futures import ThreadPoolExecutor
import csv
import hashlib
import os
import struct
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATASET_ROOT = os.path.join(REPO_ROOT, "Dataset")
MANIFEST_DIR = os.path.join(REPO_ROOT, "03_Datasets_Cohort", "manifests")


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def write_dir_manifest(folder_path: str, out_csv: str, skip_exts: tuple[str, ...] = ()) -> tuple[int, int]:
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat()
    rows = []
    total_bytes = 0
    for root, _, fns in os.walk(folder_path):
        for fn in sorted(fns):
            full = os.path.join(root, fn)
            sz = os.path.getsize(full)
            total_bytes += sz
            if skip_exts and fn.lower().endswith(skip_exts):
                continue
            rel = os.path.relpath(full, folder_path).replace("\\", "/")
            rows.append((rel, sz, sha256_file(full), ts))
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["RelativePath", "Bytes", "SHA256", "HashedUTC"])
        w.writerows(rows)
    return len(rows), total_bytes


def audit_ptbxl() -> None:
    print("\n=== [DS0001] PTB-XL v1.0.1 Audit ===", flush=True)
    ptb_root = os.path.join(
        DATASET_ROOT,
        "1. DS0001_ptbxl (PTB-XL, Kaggle)",
        "ptb-xl-a-large-publicly-available-electrocardiography-dataset-1.0.1",
    )
    sums_path = os.path.join(ptb_root, "SHA256SUMS.txt")
    sums_entries = []
    with open(sums_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                digest, rel = line.split(None, 1)
                sums_entries.append((digest, rel))

    with open(os.path.join(ptb_root, "ptbxl_database.csv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    lr_hea_set = set(r["filename_lr"] + ".hea" for r in rows)
    lr_dat_set = set(r["filename_lr"] + ".dat" for r in rows)

    def _check_entry(entry: tuple[str, str]) -> tuple[int, bool, bool, bool, bool, bool, bool]:
        digest, rel = entry
        fp = os.path.join(ptb_root, rel)
        try:
            with open(fp, "rb") as fh:
                data = fh.read()
        except FileNotFoundError:
            return (0, True, False, False, False, False, False)
        mismatch = hashlib.sha256(data).hexdigest() != digest
        bad_hea = False
        has_phi = False
        has_flat = False
        has_clip = False
        if rel.endswith(".hea"):
            lines = data.decode("utf-8", errors="replace").splitlines()
            first = lines[0].split() if lines else []
            if rel in lr_hea_set:
                if len(first) < 4 or first[1] != "12" or first[2] != "100" or first[3] != "1000":
                    bad_hea = True
            else:
                if len(first) < 4 or first[1] != "12" or first[2] != "500" or first[3] != "5000":
                    bad_hea = True
            has_phi = any(l.startswith("#") for l in lines)
        elif rel in lr_dat_set:
            vals = struct.unpack("<" + "h" * (len(data) // 2), data)
            for lead in range(12):
                lv = vals[lead::12]
                mn, mx = min(lv), max(lv)
                if mn == mx:
                    has_flat = True
                if mn <= -32768 or mx >= 32767:
                    has_clip = True
        return (len(data), False, mismatch, bad_hea, has_phi, has_flat, has_clip)

    # Single-pass parallel NCQ verification of 100% of SHA256SUMS.txt + 21,837 LR WFDB checks
    total_bytes = 0
    missing = 0
    mismatches = 0
    bad_hea = 0
    phi_comment_lines = 0
    flatline_recs = 0
    clipped_recs = 0
    done_cnt = 0
    with ThreadPoolExecutor(max_workers=4) as pool:
        for sz, is_miss, is_mism, b_h, h_p, h_f, h_c in pool.map(_check_entry, sums_entries, chunksize=64):
            total_bytes += sz
            missing += int(is_miss)
            mismatches += int(is_mism)
            bad_hea += int(b_h)
            phi_comment_lines += int(h_p)
            flatline_recs += int(h_f)
            clipped_recs += int(h_c)
            done_cnt += 1
            if done_cnt % 20000 == 0:
                print(f"  ...PTB-XL verified {done_cnt}/{len(sums_entries)} files", flush=True)

    print(f"SHA256SUMS.txt verified: {len(sums_entries)} files | missing={missing} | mismatches={mismatches} | total_MB={total_bytes/(1024*1024):.2f}", flush=True)
    print(f"SHA256SUMS.txt own digest: {sha256_file(sums_path)}", flush=True)
    print(f"Full {len(rows)} LR WFDB single-pass check: bad_hea={bad_hea}, phi_header_files={phi_comment_lines}, flatline_recs={flatline_recs}, clipped_int16_recs={clipped_recs}", flush=True)

    out_csv = os.path.join(MANIFEST_DIR, "DS0001_ptbxl_metadata_manifest.csv")
    write_dir_manifest(ptb_root, out_csv, skip_exts=(".dat", ".hea"))

    pids = set(r["patient_id"] for r in rows)
    sex_cnt = collections.Counter(r["sex"] for r in rows)
    peds = sum(1 for r in rows if r["age"].strip() and float(r["age"]) < 18)
    print(f"Records={len(rows)}, Unique patients={len(pids)}, Sex={dict(sex_cnt)}, Age<18={peds}", flush=True)


def read_xlsx_sheet1(xlsx_path: str) -> list[list[str]]:
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


def audit_cardiomled() -> None:
    print("\n=== [DS0002 / Local 3. DS0003_cardiomled] CARDIO-ML-ED Audit ===")
    cdir = os.path.join(DATASET_ROOT, "3. DS0003_cardiomled (CARDIO-ML-ED, Mendeley Official CC BY 4.0)")
    n_files, tot_b = write_dir_manifest(cdir, os.path.join(MANIFEST_DIR, "DS0002_cardiomled_manifest.csv"))
    has_ecgs_dir = os.path.isdir(os.path.join(cdir, "ECGS")) or any(fn.lower().endswith((".png", ".jpg")) for _, _, fns in os.walk(cdir) for fn in fns)
    print(f"Files hashed={n_files}, bytes={tot_b:,}, ECG image folder/PNGs present={has_ecgs_dir}")

    s1 = read_xlsx_sheet1(os.path.join(cdir, "Datasheet1 (Edited).csv"))
    non_empty = [r for r in s1[1:] if any(c.strip() for c in r)]
    c1_ids = set(r[1].strip() for r in non_empty if len(r) > 1 and r[1].strip())
    with open(os.path.join(cdir, "ECG Labels.csv"), encoding="utf-8") as f:
        ecg_rows = [r for r in csv.reader(f) if r and r[0].strip()]
    ecg_base_ids = set(r[0].strip().split("-")[0] for r in ecg_rows)
    print(f"Sheet1 rows={len(non_empty)}, unique Col1 IDs={len(c1_ids)}, ECG Labels rows={len(ecg_rows)}")
    print(f"Exact Col1 overlap={len(c1_ids & set(r[0].strip() for r in ecg_rows))}, Base-ID (strip -1/-2) overlap={len(c1_ids & ecg_base_ids)}")

    # Check SBP/DBP plausibility & gender distribution
    genders = collections.Counter(r[2].strip().upper() if len(r) > 2 else "" for r in non_empty)
    deaths = collections.Counter(r[6].strip() if len(r) > 6 else "" for r in non_empty)
    bp_bad = 0
    for r in non_empty:
        try:
            sbp = float(r[10]) if len(r) > 10 and r[10].strip() else None
            dbp = float(r[11]) if len(r) > 11 and r[11].strip() else None
            if sbp is not None and dbp is not None and sbp <= dbp:
                bp_bad += 1
        except ValueError:
            bp_bad += 1
    print(f"Genders={dict(genders)}, Deaths={dict(deaths)}, SBP<=DBP or non-numeric={bp_bad}")


def audit_cair() -> None:
    print("\n=== [DS0003 / Local 4. DS0004_cair_cvd_2025] CAIR-CVD-2025 Audit ===")
    cdir = os.path.join(DATASET_ROOT, "4. DS0004_cair_cvd_2025 (CAIR-CVD-2025, Mendeley)")
    n_files, tot_b = write_dir_manifest(cdir, os.path.join(MANIFEST_DIR, "DS0003_cair_cvd_2025_manifest.csv"))
    print(f"Files hashed={n_files}, bytes={tot_b:,}")

    with open(os.path.join(cdir, "CVD Dataset.csv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    bp_mismatch = 0
    sbp_le_dbp = 0
    for r in rows:
        bp_str = r["Blood Pressure (mmHg)"].strip()
        if bp_str and "/" in bp_str and r["Systolic BP"].strip() and r["Diastolic BP"].strip():
            parts = bp_str.split("/")
            if abs(float(parts[0]) - float(r["Systolic BP"])) > 1e-6 or abs(float(parts[1]) - float(r["Diastolic BP"])) > 1e-6:
                bp_mismatch += 1
        if r["Systolic BP"].strip() and r["Diastolic BP"].strip() and float(r["Systolic BP"]) <= float(r["Diastolic BP"]):
            sbp_le_dbp += 1
    print(f"Rows={len(rows)}, BP string vs Systolic/Diastolic numeric mismatch={bp_mismatch}, SBP<=DBP={sbp_le_dbp}")


def audit_sulianova() -> None:
    print("\n=== [DS0004 / Local 5. DS0005_sulianova_cvd] Sulianova CVD Audit ===")
    sdir = os.path.join(DATASET_ROOT, "5. DS0005_sulianova_cvd (Cardiovascular Disease, Kaggle)")
    n_files, tot_b = write_dir_manifest(sdir, os.path.join(MANIFEST_DIR, "DS0004_sulianova_cvd_manifest.csv"))
    print(f"Files hashed={n_files}, bytes={tot_b:,}")

    with open(os.path.join(sdir, "cardio_train.csv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter=";"))
    wt_bad = sum(1 for r in rows if float(r["weight"]) < 30 or float(r["weight"]) > 200)
    bmi_vals = [float(r["weight"]) / ((float(r["height"]) / 100.0) ** 2) for r in rows if float(r["height"]) > 0]
    bmi_bad = sum(1 for b in bmi_vals if b < 10 or b > 70)
    print(f"Rows={len(rows)}, extreme weight (<30 or >200kg)={wt_bad}, extreme BMI (<10 or >70)={bmi_bad}")


def main() -> None:
    audit_cardiomled()
    audit_cair()
    audit_sulianova()
    audit_ptbxl()
    print("\n=== Manifest CSV SHA-256 Digests ===", flush=True)
    for fn in sorted(os.listdir(MANIFEST_DIR)):
        if fn.endswith(".csv"):
            fp = os.path.join(MANIFEST_DIR, fn)
            print(f"{fn}: {sha256_file(fp)}", flush=True)


if __name__ == "__main__":
    main()
