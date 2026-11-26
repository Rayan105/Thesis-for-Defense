"""
Schema, Leakage-Prevention, and Multi-Format ECG Contract Validators (STEP-015).

Pure-Python standard library helpers enforcing:
1. Appendix B variables.csv contract and PROBAST Tier A (no Troponin-I) / target-leakage exclusion.
2. Digital 12-lead WFDB .hea/.dat signal validation (lead order, Hz, PHI comments, flatline, clipping).
3. CARDIO-ML-ED ECG image validation and RISK0012 stem/format normalization.
"""

from __future__ import annotations

import csv
import re
import struct
from typing import Iterable

CANONICAL_12_LEADS = ("I", "II", "III", "AVR", "AVL", "AVF", "V1", "V2", "V3", "V4", "V5", "V6")

LEAKAGE_FORBIDDEN_NAMES = frozenset({
    "cvd risk score",
    "cvd_risk_score_derived",
    "blood pressure category",
    "bp_category_derived",
    "initial diagnosis",
    "final diagnosis",
    "death",
    "cause of death",
    "patient status on discharge",
    "method of referral",
    "scp_codes",
    "ecg labels",
    "ecg_labels_diagnostic_text",
    "initial_final_diagnosis_and_death",
    "cardio",
    "cvd risk level",
})

TROPONIN_ALIASES = frozenset({
    "troponine - i (q)",
    "troponin_i_quant_censored",
    "troponin_i",
    "var0032",
})


def load_variable_dictionary(csv_path: str) -> list[dict[str, str]]:
    """Load variables.csv and validate required non-empty core schema metadata."""
    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        raise ValueError("variables.csv contains no rows.")
    required = ("VAR", "Modality", "VariableName", "Unit", "ValidRange", "IncorporationBiasRisk")
    for idx, row in enumerate(rows, start=1):
        for col in required:
            if not (row.get(col) or "").strip():
                raise ValueError(f"Row {idx} missing required field '{col}'.")
    return rows


def assert_no_leakage_predictors(
    feature_names: Iterable[str],
    var_rows: list[dict[str, str]] | None = None,
    tier: str = "A",
) -> None:
    """
    Reject target/composite leakage columns and enforce PROBAST Tier A Troponin-I exclusion.
    Raises ValueError on any prohibited feature.
    """
    excluded_from_dict = set()
    if var_rows is not None:
        for row in var_rows:
            if row["Modality"] == "Excluded_Target_Leak" or row["Modality"] == "Metadata_Key":
                excluded_from_dict.add(row["VariableName"].strip().lower())
                excluded_from_dict.add(row["VAR"].strip().lower())

    for raw_name in feature_names:
        norm = raw_name.strip().lower()
        if norm in LEAKAGE_FORBIDDEN_NAMES or norm in excluded_from_dict:
            raise ValueError(f"Prohibited leakage/metadata column in predictor set: '{raw_name}'")
        if tier.upper() == "A" and norm in TROPONIN_ALIASES:
            raise ValueError(
                f"Troponin predictor '{raw_name}' is prohibited under Tier A (no incorporation bias)."
            )


def parse_wfdb_header_text(header_text: str) -> dict[str, object]:
    """
    Parse a 12-lead WFDB .hea header string and check PHI comments, lead count, Hz, and length.
    Raises ValueError on malformed headers or embedded '#' PHI lines.
    """
    lines = [ln.strip() for ln in header_text.splitlines() if ln.strip()]
    if not lines:
        raise ValueError("Empty WFDB header.")
    phi_lines = [ln for ln in lines if ln.startswith("#")]
    if phi_lines:
        raise ValueError(f"WFDB header contains prohibited '#' comment line(s): {phi_lines[0]}")

    first_tokens = lines[0].split()
    if len(first_tokens) < 4:
        raise ValueError(f"Malformed WFDB record line: '{lines[0]}'")
    record_name = first_tokens[0]
    n_sig = int(first_tokens[1])
    fs_hz = float(first_tokens[2])
    n_samples = int(first_tokens[3])

    if n_sig != 12:
        raise ValueError(f"Expected 12 ECG leads, got {n_sig}.")
    if fs_hz not in (100.0, 500.0):
        raise ValueError(f"Unsupported sampling frequency {fs_hz} Hz (contract allows 100 or 500 Hz).")
    if len(lines) < 1 + n_sig:
        raise ValueError(f"Expected {n_sig} signal specification lines, found {len(lines) - 1}.")

    leads = []
    for sig_line in lines[1 : 1 + n_sig]:
        leads.append(sig_line.split()[-1].upper())
    if tuple(leads) != CANONICAL_12_LEADS:
        raise ValueError(f"Lead order mismatch: got {tuple(leads)}, expected {CANONICAL_12_LEADS}.")

    return {
        "record_name": record_name,
        "num_leads": n_sig,
        "sampling_hz": fs_hz,
        "num_samples": n_samples,
        "leads": leads,
    }


def inspect_int16_wfdb_waveform(
    raw_bytes: bytes,
    num_leads: int = 12,
    num_samples: int = 1000,
) -> dict[str, object]:
    """
    Verify raw little-endian int16 interleaved WFDB .dat buffer for exact byte count,
    flatline leads (min == max), and int16 ADC saturation/clipping (-32768 / 32767).
    """
    expected_bytes = num_leads * num_samples * 2
    if len(raw_bytes) != expected_bytes:
        raise ValueError(f"Expected {expected_bytes} bytes, got {len(raw_bytes)}.")

    vals = struct.unpack("<" + "h" * (len(raw_bytes) // 2), raw_bytes)
    flatline_leads = []
    clipped_leads = []
    for idx in range(num_leads):
        lead_vals = vals[idx::num_leads]
        mn, mx = min(lead_vals), max(lead_vals)
        if mn == mx:
            flatline_leads.append(CANONICAL_12_LEADS[idx] if idx < 12 else str(idx))
        if mn <= -32768 or mx >= 32767:
            clipped_leads.append(CANONICAL_12_LEADS[idx] if idx < 12 else str(idx))

    return {
        "passed_clean": len(flatline_leads) == 0 and len(clipped_leads) == 0,
        "flatline_leads": flatline_leads,
        "clipped_leads": clipped_leads,
    }


def normalize_cardiomled_image_stem(stem: str) -> str:
    """
    Normalize CARDIO-ML-ED filename stems per CRF Manual v1.0.0:
    strips trailing spaces (e.g. '150753 ' -> '150753') and normalizes '(2)' -> '-2'.
    """
    cleaned = stem.strip()
    cleaned = re.sub(r"\((\d+)\)$", r"-\1", cleaned)
    return cleaned


def validate_ecg_image_bytes(data: bytes, filename: str) -> dict[str, object]:
    """
    Validate PNG/JPG ECG scan bytes and flag uncropped 6-lead JPG strips per RISK0012.
    """
    low = filename.lower()
    if low.endswith(".png"):
        if not data.startswith(b"\x89PNG\r\n\x1a\n") or b"IEND" not in data[-24:] or len(data) < 26:
            raise ValueError(f"Corrupt PNG header/footer in '{filename}'.")
        width, height, bit_depth, color_type = struct.unpack(">IIBB", data[16:26])
        return {
            "format": "PNG",
            "eligible_12row_encoder": True,
            "width": width,
            "height": height,
            "bit_depth": bit_depth,
            "color_type": color_type,
        }
    if low.endswith(".jpg") or low.endswith(".jpeg"):
        if not data.startswith(b"\xff\xd8") or not data.endswith(b"\xff\xd9"):
            raise ValueError(f"Corrupt JPG marker in '{filename}'.")
        return {
            "format": "JPG",
            "eligible_12row_encoder": False,  # Quarantined per RISK0012 (uncropped 6-lead strips)
        }
    raise ValueError(f"Unsupported ECG image extension for '{filename}'.")
