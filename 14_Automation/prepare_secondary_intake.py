"""
Secondary Dataset Folder Initialization & SHA-256 Intake Manifest Generator (Option B).

Safely initializes gitignored `03_Datasets_Cohort/raw/DS####_*` folders and computes
deterministic SHA-256 checksums for `STEP-012` intake without exposing any raw data to Git.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
from datetime import datetime, timezone

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_ROOT = os.path.join(REPO_ROOT, "03_Datasets_Cohort", "raw")
MANIFEST_DIR = os.path.join(REPO_ROOT, "03_Datasets_Cohort", "manifests")

EXPECTED_DATASETS = [
    "DS0001_ptbxl",
    "DS0002_chapman",
    "DS0003_cardiomled",
    "DS0004_cair_cvd_2025",
    "DS0005_sulianova_cvd",
    "DS0006_framingham",
]


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def init_dirs() -> None:
    os.makedirs(RAW_ROOT, exist_ok=True)
    for sub in EXPECTED_DATASETS:
        p = os.path.join(RAW_ROOT, sub)
        os.makedirs(p, exist_ok=True)
        print(f"READY: {p}")


def build_manifests() -> None:
    os.makedirs(MANIFEST_DIR, exist_ok=True)
    if not os.path.isdir(RAW_ROOT):
        print("RAW_ROOT missing. Run --init-dirs first.")
        return

    timestamp = datetime.now(timezone.utc).isoformat()
    for sub in sorted(os.listdir(RAW_ROOT)):
        sub_path = os.path.join(RAW_ROOT, sub)
        if not os.path.isdir(sub_path):
            continue
        files = []
        for root, _, filenames in os.walk(sub_path):
            for fn in sorted(filenames):
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, sub_path).replace("\\", "/")
                size = os.path.getsize(full)
                digest = sha256_file(full)
                files.append((rel, size, digest, timestamp))

        out_csv = os.path.join(MANIFEST_DIR, f"{sub}_raw_manifest.csv")
        with open(out_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["RelativePath", "Bytes", "SHA256", "HashedUTC"])
            writer.writerows(files)
        print(f"{sub}: {len(files)} files hashed -> {out_csv}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Option B secondary cohort folder & hash helper")
    parser.add_argument("--init-dirs", action="store_true", help="Create raw dataset directories")
    parser.add_argument("--manifest", action="store_true", help="Hash all files in raw/* into manifests/")
    args = parser.parse_args()

    if not args.init_dirs and not args.manifest:
        parser.print_help()
        return
    if args.init_dirs:
        init_dirs()
    if args.manifest:
        build_manifests()


if __name__ == "__main__":
    main()
