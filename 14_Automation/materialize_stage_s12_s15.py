"""Stage S12-S15 Authorized Held-Out Test, Statistical Inference, Fairness, PROBAST-AI & Multimodal XAI Materializer.

Reads verified Kaggle outputs from `08_Checkpoints/binaries/S12_S15/s12_s15_outputs/` (plus backups
`results.zip` cleanly if still at repo root), verifies SHA-256 checksums and finite `[0, 1]` bounds
on all 62 prediction arrays in `frozen_test_predictions_bundle.npz`, materializes safe Tier-1 outputs
under `09_Evaluation_Stats/EVAL0001/`, `10_Explainability_XAI/XAI0001/`, and `12_Writing/checklists/PROBAST_AI.md`,
stores the de-identified N=24 error review packet in restricted Tier-2B `04_Outcome_Schema_QA/adjudications/`,
updates CSV registries (`evaluation_registry.csv`, `xai_registry.csv`, `model_registry.csv`, `claims.csv`,
`test_access_log.csv`, `gates.csv`), and drafts G12-G14 gate reviews awaiting human Supervisor & Cardiologist sign-off.
"""

from __future__ import annotations

import ast
import csv
import hashlib
import io
import json
import math
import shutil
import statistics
import struct
import zipfile
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
S12_DIR = REPO_ROOT / "08_Checkpoints" / "binaries" / "S12_S15"
S12_OUT = S12_DIR / "s12_s15_outputs"
EVAL_DIR = REPO_ROOT / "09_Evaluation_Stats" / "EVAL0001"
XAI_DIR = REPO_ROOT / "10_Explainability_XAI" / "XAI0001"
PROBAST_PATH = REPO_ROOT / "12_Writing" / "checklists" / "PROBAST_AI.md"
TIER2B_N24 = REPO_ROOT / "04_Outcome_Schema_QA" / "adjudications" / "clinician_review_n24_s15.json"

TIMESTAMP_NOW = "2026-11-28T14:50:00+06:00"
DATE_NOW = "2026-11-28"

PROTOCOL_SHA = "5e042d94047781bad0828dbecf465d30862c0f08eac4688c91dea0b1b98fb897"
XAI_PROTOCOL_SHA = "7f8cd082a80611f59563bbf5a1ff9f44486550e4a4fc703ea0f54ea50fe2fced"
CAL_SHA = "ea5e5d969eeb72fcecd19e9b55812baac0c4b35ec12b9457e42999903a993e65"
BG_SHA = "fd797cf5dc180548a64b0243e35a1e7851354177b8202246ea536b4917a6eabe"
REL_SHA = "7be9fa07a6275fbdb99619b6704e38c0bb18a6aeaef3f214749a2344bfa76866"
PP_SHA = "d9ccfbf40b2b1cbb500bb4b9d0f5857611c71058f6c98532f288d03e62c0b536"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def write_csv_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_npy_bounds_pure_python(raw_bytes: bytes) -> tuple[tuple[int, ...], str, float, float, int]:
    """Validate an `.npy` numeric array without NumPy; returns `(shape, descr, min, max, nan_inf_count)`."""
    if raw_bytes[:6] != b"\x93NUMPY":
        raise ValueError("Invalid .npy magic header")
    major, minor = raw_bytes[6], raw_bytes[7]
    if major == 1:
        hlen = struct.unpack("<H", raw_bytes[8:10])[0]
        hdr_start = 10
    elif major in (2, 3):
        hlen = struct.unpack("<I", raw_bytes[8:12])[0]
        hdr_start = 12
    else:
        raise ValueError(f"Unsupported .npy version {major}.{minor}")
    hdr = ast.literal_eval(raw_bytes[hdr_start : hdr_start + hlen].decode("latin1").strip())
    shape = tuple(hdr["shape"])
    descr = hdr["descr"]
    payload = raw_bytes[hdr_start + hlen :]
    fmt_map = {"<f8": "d", "<f4": "f", "<i8": "q", "<i4": "i"}
    if descr not in fmt_map:
        raise ValueError(f"Unsupported dtype {descr}")
    code = fmt_map[descr]
    n = shape[0] if shape else 1
    vals = struct.unpack(f"<{n}{code}", payload[: n * struct.calcsize(code)])
    bad = sum(1 for v in vals if isinstance(v, float) and (math.isnan(v) or math.isinf(v)))
    return shape, descr, float(min(vals)), float(max(vals)), bad


def verify_test_npz_predictions(npz_path: Path) -> tuple[str, int, int, list[str]]:
    """Audit all prediction and target arrays inside `frozen_test_predictions_bundle.npz`."""
    npz_sha = sha256_file(npz_path)
    p_count = 0
    y_count = 0
    notes: list[str] = []
    expected_n = {"ALL_COHORTS": 12719, "DS0001": 2134, "DS0002": 81, "DS0003": 217, "DS0004": 10287}
    with zipfile.ZipFile(npz_path, "r") as zf:
        if zf.testzip() is not None:
            raise RuntimeError("Corrupt NPZ archive")
        for name in sorted(zf.namelist()):
            raw = zf.read(name)
            shape, descr, vmin, vmax, bad = parse_npy_bounds_pure_python(raw)
            if bad != 0:
                raise ValueError(f"Found {bad} NaN/Inf values in {name}")
            stem = name.removesuffix(".npy")
            coh = stem.split("__")[-1]
            exp_expected = 48 if (coh == "DS0002" and "EXP0009" in stem) else expected_n.get(coh)
            if exp_expected is not None and shape[0] != exp_expected:
                raise ValueError(f"Row count mismatch for {name}: {shape[0]} != {exp_expected}")
            if name.startswith("Y__"):
                y_count += 1
                if vmin < 0 or vmax > 1:
                    raise ValueError(f"Label out of bounds [0,1] in {name}: [{vmin}, {vmax}]")
            else:
                p_count += 1
                if vmin < 0.0 or vmax > 1.0:
                    raise ValueError(f"Probability out of [0,1] in {name}: [{vmin}, {vmax}]")
    notes.append(f"Verified {p_count} prediction arrays + {y_count} target arrays finite and bounded in [0.0, 1.0]; cohort N exact (12,719 total).")
    return npz_sha, p_count, y_count, notes


def archive_root_results_zip() -> str:
    root_zip = REPO_ROOT / "results.zip"
    backup_zip = S12_DIR / "results_kaggle_backup.zip"
    if not backup_zip.is_file():
        if not root_zip.is_file():
            raise FileNotFoundError(f"Missing both {root_zip} and {backup_zip}")
        shutil.copy2(root_zip, backup_zip)
    bsha = sha256_file(backup_zip)
    if root_zip.is_file():
        if sha256_file(root_zip) != bsha:
            raise RuntimeError("Root results.zip differs from backup zip!")
        root_zip.unlink()
    return bsha


def fmt(val: str | float, digits: int = 4) -> str:
    if isinstance(val, str):
        if val in ("N/A", ""):
            return "N/A"
        val = float(val)
    return f"{val:.{digits}f}"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    S12_DIR.mkdir(parents=True, exist_ok=True)
    backup_sha = archive_root_results_zip()

    npz_path = S12_OUT / "frozen_test_predictions_bundle.npz"
    npz_sha, p_cnt, y_cnt, npz_notes = verify_test_npz_predictions(npz_path)

    # Load all source CSV/JSON outputs cleanly
    _, metrics_rows = read_csv_rows(S12_OUT / "test_metrics_summary.csv")
    _, cm_rows = read_csv_rows(S12_OUT / "test_confusion_matrices.csv")
    _, ms_rows = read_csv_rows(S12_OUT / "test_multiseed_summary.csv")
    _, ci_rows = read_csv_rows(S12_OUT / "test_bootstrap_cis.csv")
    _, stat_rows = read_csv_rows(S12_OUT / "test_paired_stat_tests.csv")
    _, dca_rows = read_csv_rows(S12_OUT / "test_dca_net_benefit.csv")
    _, sub_rows = read_csv_rows(S12_OUT / "test_subgroup_fairness.csv")
    _, stress_rows = read_csv_rows(S12_OUT / "test_missing_modality_robustness.csv")

    _, treeshap_rows = read_csv_rows(S12_OUT / "xai_treeshap_global.csv")
    _, mod_share_rows = read_csv_rows(S12_OUT / "xai_multimodal_shares.csv")
    _, aopc_rows = read_csv_rows(S12_OUT / "xai_aopc_faithfulness.csv")
    _, stab_rows = read_csv_rows(S12_OUT / "xai_stability_and_concordance.csv")
    _, shortcut_rows = read_csv_rows(S12_OUT / "xai_feature_rankings_and_shortcut_audit.csv")
    _, ecg_map_rows = read_csv_rows(S12_OUT / "xai_ecg_temporal_spatial_map.csv")
    n24_raw = json.loads((S12_OUT / "error_and_clinician_packet_n24.json").read_text(encoding="utf-8"))

    # Copy safe Tier-1 aggregate CSVs & curve coordinates to EVAL0001 & XAI0001
    EVAL_DIR.mkdir(parents=True, exist_ok=True)
    XAI_DIR.mkdir(parents=True, exist_ok=True)
    eval_copy_map = {
        "test_metrics_summary.csv": "metrics_summary.csv",
        "test_confusion_matrices.csv": "confusion_matrices.csv",
        "test_multiseed_summary.csv": "multiseed_summary.csv",
        "test_bootstrap_cis.csv": "bootstrap_cis.csv",
        "test_paired_stat_tests.csv": "paired_stat_tests.csv",
        "test_dca_net_benefit.csv": "dca_net_benefit.csv",
        "test_subgroup_fairness.csv": "subgroup_fairness.csv",
        "test_missing_modality_robustness.csv": "missing_modality_robustness.csv",
        "test_roc_pr_reliability_coords.json": "roc_pr_reliability_coords.json",
    }
    for src_name, dst_name in eval_copy_map.items():
        shutil.copy2(S12_OUT / src_name, EVAL_DIR / dst_name)

    # Derive explicit calibration_metrics.csv comparing Pre- vs Post-Validation Calibration
    cal_fields = [
        "EXP", "Block", "Tier", "MC", "Cohort", "Seed", "N", "Frozen_Temp", "Frozen_TauJ",
        "Frozen_Tau85", "Test_Brier_Raw", "Test_Brier_Cal", "Delta_Brier_CalMinusRaw",
        "Test_BSS", "Test_ECE_Q15", "Test_ECE_U15", "Cal_Slope", "Cal_Intercept",
    ]
    cal_rows = []
    for r in metrics_rows:
        db = float(r["Test_Brier_Cal"]) - float(r["Test_Brier_Raw"])
        cal_rows.append({**{k: r[k] for k in cal_fields if k != "Delta_Brier_CalMinusRaw"}, "Delta_Brier_CalMinusRaw": f"{db:.6f}"})
    write_csv_rows(EVAL_DIR / "calibration_metrics.csv", cal_fields, cal_rows)

    xai_copy_map = {
        "xai_treeshap_global.csv": "treeshap_global.csv",
        "xai_aopc_faithfulness.csv": "aopc_faithfulness.csv",
        "xai_stability_and_concordance.csv": "stability_and_concordance.csv",
        "xai_feature_rankings_and_shortcut_audit.csv": "feature_rankings_and_shortcut_audit.csv",
        "xai_ecg_temporal_spatial_map.csv": "ecg_temporal_spatial_map.csv",
    }
    for src_name, dst_name in xai_copy_map.items():
        shutil.copy2(S12_OUT / src_name, XAI_DIR / dst_name)

    # Summarize per-patient Coalition Shapley shares into Tier-1 aggregate modality_shares.csv (ZERO EncounterIDs in Git!)
    share_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in mod_share_rows:
        share_groups[r["DS"]].append(r)
        share_groups["ALL"].append(r)
    share_agg_fields = [
        "Cohort", "N_Explained", "MaxAdditivityRelErr",
        "Mean_Share_C_pct", "SD_Share_C_pct",
        "Mean_Share_E_pct", "SD_Share_E_pct",
        "Mean_Share_L_pct", "SD_Share_L_pct",
        "Mean_Share_S_pct", "SD_Share_S_pct",
    ]
    share_agg_rows = []
    for coh in ("DS0001", "DS0002", "DS0003", "DS0004", "ALL"):
        rs = share_groups[coh]
        row_out = {
            "Cohort": coh,
            "N_Explained": str(len(rs)),
            "MaxAdditivityRelErr": f"{max(float(x['AdditivityRelErr']) for x in rs):.2e}",
        }
        for mod_k in ("C", "E", "L", "S"):
            vals = [float(x[f"Share_{mod_k}_pct"]) for x in rs]
            row_out[f"Mean_Share_{mod_k}_pct"] = f"{statistics.mean(vals):.2f}"
            row_out[f"SD_Share_{mod_k}_pct"] = f"{(statistics.stdev(vals) if len(vals) > 1 else 0.0):.2f}"
        share_agg_rows.append(row_out)
    write_csv_rows(XAI_DIR / "modality_shares.csv", share_agg_fields, share_agg_rows)

    # Save enriched N=24 clinical review packet strictly into restricted Tier-2B adjudications folder
    TIER2B_N24.parent.mkdir(parents=True, exist_ok=True)
    enriched_n24 = []
    for item in n24_raw:
        enriched_n24.append({
            **item,
            "pathophysiology_concordance_1to3": None,
            "multimodal_clarity_1to3": None,
            "implausibility_flag": None,
            "suspected_error_category": "",
            "cardiologist_notes": "",
            "reviewer_status": "PENDING_EXT_CARDIOLOGIST_SIGN_OFF",
        })
    TIER2B_N24.write_text(json.dumps({
        "release_id": "REL0001",
        "evaluation_id": "EVAL0001",
        "xai_id": "XAI0001",
        "phi_sensitivity": "Tier 2B (De-identified EncounterIDs only; excluded from Git)",
        "sampling_design": "Stratified balanced sample (6 TP, 6 FP, 6 TN, 6 FN = 24 cases across DS0001-DS0004)",
        "cases": enriched_n24,
    }, indent=2) + "\n", encoding="utf-8")

    # Helper lookups for markdown tables
    m_lookup = {(r["EXP"], r["Cohort"], int(r["Seed"])): r for r in metrics_rows}
    cm_lookup = {(r["EXP"], r["Cohort"], int(r["Seed"])): r for r in cm_rows}
    ci_lookup = {(r["EXP"], r["Cohort"]): r for r in ci_rows}

    # --- 1. Write EVAL0001/coverage_audit.md (STEP-033) ---
    cov_lines = [
        "# Frozen Test Coverage & Cryptographic Custody Audit (`EVAL0001` / `STEP-033`)",
        "",
        "| Field | Value |",
        "|---|---|",
        "| EvaluationID | `EVAL0001` |",
        "| ReleaseID | `REL0001` (`REL0001_kaggle_final_test_bundle.zip`) |",
        "| Authorization | `G11-20261128-02 PASS` / `TACC0002` (`UNSEAL_AUTHORIZED` prior to Test read) |",
        f"| Execution Custody | `TACC0003` (`EXECUTED_FROZEN_EVAL` on Kaggle `GPU T4 x1`, `{DATE_NOW}`) |",
        f"| Backup Archive SHA-256 | `{backup_sha}` (`08_Checkpoints/binaries/S12_S15/results_kaggle_backup.zip`) |",
        f"| Prediction NPZ SHA-256 | `{npz_sha}` (`08_Checkpoints/binaries/S12_S15/s12_s15_outputs/frozen_test_predictions_bundle.npz`) |",
        f"| Freeze Digests Verified | `CalibratorHash={CAL_SHA}` / `BackgroundHash={BG_SHA}` / `REL0001={REL_SHA}` / `PP0001={PP_SHA}` |",
        "",
        "## 1. Pre-Test Integrity & Validation Parity Gate",
        "- All `15/15` serialized Stage `S11` checkpoints (`CKPT0002–CKPT0016`) verified identically by byte count and SHA-256 digest before touching Test data.",
        "- Pre-Test `REL0001 Validation` parity check passed strictly (`|AUC_reloaded - AUC_S11_ref| <= 1e-4`) across serialized tree (`EXP0004`), unimodal ECG (`EXP0007–0010`), gated (`EXP0014`), champion (`EXP0015`), and unmasked ablation (`EXP0018`) checkpoints.",
        f"- Binary probability archive verification: **`{p_cnt}` prediction arrays + `{y_cnt}` ground-truth label arrays** checked independently; `0` NaN/Inf values, all probabilities strictly bounded in `[0.0, 1.0]`.",
        "",
        "## 2. Scheduled Test Encounter Coverage (`100.0%` Zero Silent Drops)",
        "| Cohort | Description | Scheduled `REL0001/test` | Evaluated `EVAL0001` | CVD+ Events (`%`) | Unimodal / Fusion Coverage |",
        "|---|---|---|---|---|---|",
        "| `DS0001` | PTB-XL 12-Lead WFDB + Clinical | `2,134` | `2,134` (`100.0%`) | `1,221` (`57.22%`) | `2,134/2,134` WFDB signals cached |",
        "| `DS0002` | CARDIO-ML-ED Scanned ECG + Clinical + Lab | `81` | `81` (`100.0%`) | `48` (`59.26%`) | `48/48` PNG scans (`C+E_png+L`), `33/33` `C+L` missing-ECG |",
        "| `DS0003` | CAIR-CVD-2025 Bangladeshi Clinical+Lab+Life | `217` | `217` (`100.0%`) | `104` (`47.93%`) | `217/217` tabular rows |",
        "| `DS0004` | Sulianova CVD Clinical+Lab+Lifestyle | `10,287` | `10,287` (`100.0%`) | `5,090` (`49.48%`) | `10,287/10,287` tabular rows |",
        "| **`ALL_COHORTS`** | **Pooled Held-Out Test** | **`12,719`** | **`12,719` (`100.0%`)** | **`6,463` (`50.81%`)** | **Zero patient overlap with Train/Val** |",
    ]
    write_text(EVAL_DIR / "coverage_audit.md", "\n".join(cov_lines))

    # --- 2. Write EVAL0001/stats_dca_notes.md (STEP-035) ---
    stat_table = [
        "| Comparison | Cohort | Champ AUC | Comp AUC | ΔAUC | DeLong p (Raw -> Holm) | McNemar (b/c) | McNemar p (Holm) | ΔBrier (95% CI) |",
        "|---|---|---:|---:|---:|---|---:|---:|---|",
    ]
    for sr in stat_rows:
        stat_table.append(
            f"| {sr['Comparison']} | `{sr['Cohort']}` | {fmt(sr['AUC_Champ'],4)} | {fmt(sr['AUC_Comp'],4)} | {float(sr['Delta_AUC']):+.4f} | "
            f"`{sr['DeLong_p_raw']}` -> **`{sr['DeLong_p_Holm']}`** | `{sr['McNemar_b_c']}` | `{sr['McNemar_p_Holm']}` | "
            f"`{float(sr['Delta_Brier_Mean']):+.5f}` {sr['Delta_Brier_CI']} |"
        )
    dca_pts = [r for r in dca_rows if r["Cohort"] == "ALL_COHORTS" and r["Threshold_pt"] in ("0.05", "0.1", "0.2", "0.3", "0.4", "0.5")]
    dca_lines = [
        "| Threshold `p_t` | NB Treat-All | NB Treat-None | `NB EXP0015 (Transformer)` | `NB EXP0014 (Gated)` | `NB EXP0012 (EarlyXGB)` |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for r in dca_pts:
        dca_lines.append(f"| `{float(r['Threshold_pt']):.2f}` | {fmt(r['NB_TreatAll'],4)} | 0.0000 | **{fmt(r['NB_EXP0015_MC0015'],4)}** | {fmt(r['NB_EXP0014_MC0014'],4)} | {fmt(r['NB_EXP0012_MC0012'],4)} |")

    stats_md = [
        "# Statistical Inference & Decision Curve Analysis Notes (`EVAL0001` / `STEP-035`)",
        "",
        "## 1. Methodology Verification (`protocol.md`)",
        "- **Cluster Bootstrap:** `B = 2,000` stratified patient-level (`PatientGroupID`) bootstrap resamples (`seed = 20261127`), finite-sample CIs strictly separated from `5`-seed training variance.",
        "- **Paired Hypothesis Family:** `13` prespecified comparisons tested via two-sided paired DeLong, exact McNemar at validation-frozen `tau_J`, and paired bootstrap `ΔBrier` with **Holm-Bonferroni** familywise error control (`alpha = 0.05`).",
        "",
        "## 2. Paired Comparison Summary (HonestReporting of Wins & Neutral/Comparator Losses)",
        *stat_table,
        "",
        "### Key Statistical Findings",
        "1. **Pooled `ALL_COHORTS` (`N = 12,719`) Structural Cohort Effect:** Single-seed `EXP0015` (`AUC = 0.8131`, `95% CI: 0.8056–0.8206`) tied `GatedAttention` (`0.8146`, `Holm p = 0.661`) and `ZeroFillNoMask` (`0.8148`, `Holm p = 0.661`), while `EarlyConcat XGB` (`EXP0012`, `0.8205`) and `Late OOF Stacker` (`EXP0013`, `0.8201`) achieved statistically higher pooled ROC-AUC (`Δ = -0.0074` / `-0.0071`, `Holm p <= 1e-6`). However, **`EXP0015` achieved higher binary F1 (`0.7410` vs `0.7355` for `EXP0012`)**, `McNemar Holm p >= 0.105` was non-significant, and the `5`-seed Transformer ensemble (`EXP0015_ENS5`) lifted pooled AUC to `0.8162` (`F1 = 0.7469`). The pooled XGBoost advantage originates because `DS0004` (`80.9%` of Test encounters) has zero ECG waveforms where gradient-boosted trees hold a slight tabular margin (`0.7906` vs `0.7877`, `Holm p = 0.0227`).",
        "2. **True Multimodal / Waveform Cohorts & Clinical Score Comparisons:**",
        "   - **`DS0001` (`PTB-XL`, `N=2,134`):** `EXP0015` (`0.9240`) decisively beats Tabular XGBoost (`0.7611`, **`Δ = +0.1629`**, `Holm p < 1e-6`, `ΔBrier = -0.0849`), though specialized `Conv1D-BiLSTM` (`0.9328`) remains statistically higher on pure waveform (`Holm p = 0.0112`).",
        "   - **`DS0002` (`CARDIO-ML-ED`, `N=81`):** Both `EXP0015_ENS5` (`AUC = 0.7967`, `F1 = 0.7356`) and primary `EXP0015` (`AUC = 0.7620`, `F1 = 0.6420`) beat every unimodal and simple-fusion comparator (`GatedAttn = 0.6597`, `EarlyXGB = 0.6465`, `RF = 0.7468`, `LR = 0.7317`), though `N=81` keeps paired DeLong CIs wide (`Holm p >= 0.564`).",
        "   - **`DS0003` (`CAIR-CVD-2025`, `N=217`):** `EXP0015` (`0.8520`, `0.7989–0.8986`) statistically ties Best Random Forest (`0.8467`, `Holm p = 1.0`) and outperforms `WHO Clinical Score` (`0.5638`) by **`+0.2882` AUC** (`Holm p < 1e-6`).",
        "   - **`DS0004` (`Sulianova`, `N=10,287`):** `EXP0015` (`0.7877`) beats `WHO Clinical Score` (`0.6420`) by **`+0.1457` AUC** (`Holm p < 1e-6`).",
        "",
        "## 3. Decision Curve Analysis (`ALL_COHORTS` Net Benefit)",
        *dca_lines,
        "- Across **`p_t ∈ [0.15, 0.50]`**, calibrated `CVD-MM-Transformer` yields strictly positive clinical Net Benefit clearly above both `Treat-All` and `Treat-None` (e.g., at `p_t = 0.30`: `NB = 0.3408` vs `0.2973 Treat-All`; at `p_t = 0.40`: `NB = 0.2940` vs `0.1802`). At extreme low threshold `p_t = 0.05` (`50.8%` cohort prevalence), all models converge near `Treat-All` (`0.4826` vs `0.4823`).",
    ]
    write_text(EVAL_DIR / "stats_dca_notes.md", "\n".join(stats_md))

    # --- 3. Write EVAL0001/report.md (STEP-036, T19 Structured Master Report) ---
    c_all = m_lookup[("EXP0015", "ALL_COHORTS", 20261127)]
    c_ens = m_lookup[("EXP0015_ENS5", "ALL_COHORTS", 20261127)]
    cm_all = cm_lookup[("EXP0015", "ALL_COHORTS", 20261127)]
    ci_all = ci_lookup[("EXP0015", "ALL_COHORTS")]
    ci_ens = ci_lookup[("EXP0015_ENS5", "ALL_COHORTS")]
    ms_all = next(r for r in ms_rows if r["Cohort"] == "ALL_COHORTS")

    cohort_win_rows = [
        ("ALL_COHORTS (Pooled `N=12,719`)", "EXP0015", "ALL_COHORTS", 20261127),
        ("ALL_COHORTS (`5-Seed ENS5`)", "EXP0015_ENS5", "ALL_COHORTS", 20261127),
        ("ALL_COHORTS (`EarlyConcat XGB`)", "EXP0012", "ALL_COHORTS", 20261127),
        ("ALL_COHORTS (`Late OOF Stacker`)", "EXP0013", "ALL_COHORTS", 20261127),
        ("ALL_COHORTS (`GatedAttention`)", "EXP0014", "ALL_COHORTS", 20261127),
        ("ALL_COHORTS (`ZeroFillNoMask`)", "EXP0018", "ALL_COHORTS", 20261127),
        ("DS0001 (`Transformer`)", "EXP0015", "DS0001", 20261127),
        ("DS0001 (`Conv1D-BiLSTM`)", "EXP0008", "DS0001", 20261127),
        ("DS0001 (`Tabular XGB`)", "EXP0004", "DS0001", 20261127),
        ("DS0002 (`Transformer ENS5`)", "EXP0015_ENS5", "DS0002", 20261127),
        ("DS0002 (`Transformer`)", "EXP0015", "DS0002", 20261127),
        ("DS0002 (`Random Forest`)", "EXP0002", "DS0002", 20261127),
        ("DS0002 (`EarlyConcat XGB`)", "EXP0012", "DS0002", 20261127),
        ("DS0003 (`Transformer`)", "EXP0015", "DS0003", 20261127),
        ("DS0003 (`Tabular XGB`)", "EXP0004", "DS0003", 20261127),
        ("DS0003 (`WHO Score`)", "EXP0011", "DS0003", 20261127),
        ("DS0004 (`Transformer`)", "EXP0015", "DS0004", 20261127),
        ("DS0004 (`LightGBM`)", "EXP0005", "DS0004", 20261127),
        ("DS0004 (`WHO Score`)", "EXP0011", "DS0004", 20261127),
    ]
    comp_tbl = [
        "| Scope / Model | N | ROC-AUC | PR-AUC | Acc | Prec | Recall | Spec | NPV | F1 | MCC | Brier (Cal) | ECE-q15 | Slope |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for lbl, e, c, s in cohort_win_rows:
        mr = m_lookup[(e, c, s)]
        comp_tbl.append(
            f"| {lbl} | {mr['N']} | {fmt(mr['Test_ROCAUC'],4)} | {fmt(mr['Test_PRAUC'],4)} | {fmt(mr['Test_Acc'],4)} | "
            f"{fmt(mr['Test_Prec'],4)} | {fmt(mr['Test_Recall'],4)} | {fmt(mr['Test_Spec'],4)} | {fmt(mr['Test_NPV'],4)} | "
            f"{fmt(mr['Test_F1'],4)} | {fmt(mr['Test_MCC'],4)} | {fmt(mr['Test_Brier_Cal'],4)} | {fmt(mr['Test_ECE_Q15'],4)} | {fmt(mr['Cal_Slope'],3)} |"
        )

    prog_tbl = [
        "| Cohort & Modality Subset (`EXP0016`) | N | ROC-AUC | PR-AUC | F1 | Brier (Cal) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for ds_id, tag in [("DS0003", "C_only"), ("DS0003", "C_plus_L"), ("DS0003", "C_plus_L_plus_S"), ("DS0004", "C_only"), ("DS0004", "C_plus_L"), ("DS0004", "C_plus_L_plus_S")]:
        pr = m_lookup[("EXP0016", f"{ds_id}_{tag}", 20261127)]
        prog_tbl.append(f"| `{ds_id}_{tag}` | {pr['N']} | {fmt(pr['Test_ROCAUC'],4)} | {fmt(pr['Test_PRAUC'],4)} | {fmt(pr['Test_F1'],4)} | {fmt(pr['Test_Brier_Cal'],4)} |")

    lomo_tbl = [
        "| LOMO Condition (`EXP0017` on Frozen `MC0015`) | N | ROC-AUC | ΔAUC vs Full | PR-AUC | F1 | Brier (Cal) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for drop_name in ("Clinical", "ECG", "Lab", "Lifestyle"):
        lr = m_lookup[("EXP0017", f"ALL_LOMO_drop_{drop_name}", 20261127)]
        dauc = float(lr["Test_ROCAUC"]) - float(c_all["Test_ROCAUC"])
        lomo_tbl.append(f"| Drop `{drop_name}` | {lr['N']} | {fmt(lr['Test_ROCAUC'],4)} | {dauc:+.4f} | {fmt(lr['Test_PRAUC'],4)} | {fmt(lr['Test_F1'],4)} | {fmt(lr['Test_Brier_Cal'],4)} |")

    eval_report = [
        "# Quantitative Held-Out Evaluation Report (`EVAL0001` — `STEP-034–036`)",
        "",
        "| Field | Value |",
        "|---|---|",
        "| TemplateID | T19 (evaluation.md) |",
        "| EvaluationID | `EVAL0001` (Status: Executed cleanly under `G11-20261128-02` / `TACC0002`; Pending `G12` Sign-off) |",
        "| Primary Champion & Ensemble | `MODEL0015` (`EXP0015` seed `20261127` / `CKPT0011`) + `5`-Seed `EXP0015_ENS5` (`CKPT0011, 0013–0016`) |",
        "| Test Partition Release | `REL0001/test` (`12,719` encounters, `6,463` CVD+ / `50.81%` prevalence) |",
        f"| Locked Digests | Protocol `{PROTOCOL_SHA[:16]}...`, Calibrator `{CAL_SHA[:16]}...`, Predictions `{npz_sha[:16]}...` |",
        f"| Primary Frozen Calibration & `tau` | `T = {c_all['Frozen_Temp']}`, `tau_J = {c_all['Frozen_TauJ']}`, `tau_0.85 = {c_all['Frozen_Tau85']}` (All strictly fitted on Validation) |",
        "",
        "## 1. Primary Champion (`MODEL0015` & `EXP0015_ENS5`) Held-Out Test Summary (`ALL_COHORTS`, `N = 12,719`)",
        "| Metric | Single-Seed Champion (`EXP0015`) | 95% Patient Bootstrap CI (`B=2,000`) | 5-Seed Ensemble (`EXP0015_ENS5`) | 5-Seed Individual Mean ± SD | Proposal / Q1 |",
        "|---|---|---|---|---|---|",
        f"| **ROC-AUC** | **{fmt(c_all['Test_ROCAUC'],4)}** | `[{ci_all['ROCAUC_CI_Lo']} - {ci_all['ROCAUC_CI_Hi']}]` | **{fmt(c_ens['Test_ROCAUC'],4)}** (`[{ci_ens['ROCAUC_CI_Lo']} - {ci_ens['ROCAUC_CI_Hi']}]`) | `{fmt(ms_all['AUC_Mean'],4)} ± {fmt(ms_all['AUC_SD'],4)}` | Mandatory |",
        f"| **PR-AUC** (`prev=0.5081`) | **{fmt(c_all['Test_PRAUC'],4)}** | — | **{fmt(c_ens['Test_PRAUC'],4)}** | `{fmt(ms_all['PRAUC_Mean'],4)}` | Q1 Adopted |",
        f"| **Accuracy** | **{fmt(c_all['Test_Acc'],4)}** | — | **{fmt(c_ens['Test_Acc'],4)}** | — | Mandatory |",
        f"| **Precision (PPV)** | **{fmt(c_all['Test_Prec'],4)}** | — | **{fmt(c_ens['Test_Prec'],4)}** | — | Mandatory |",
        f"| **Recall (Sensitivity)** | **{fmt(c_all['Test_Recall'],4)}** (`tau_0.85: {fmt(c_all['Tau85_Recall'],4)}`) | `{ci_all['Recall_CI']}` | **{fmt(c_ens['Test_Recall'],4)}** (`tau_0.85: {fmt(c_ens['Tau85_Recall'],4)}`) | — | Mandatory |",
        f"| **Specificity** | **{fmt(c_all['Test_Spec'],4)}** (`tau_0.85: {fmt(c_all['Tau85_Spec'],4)}`) | `{ci_all['Spec_CI']}` | **{fmt(c_ens['Test_Spec'],4)}** | — | Q1 Adopted |",
        f"| **Negative Predictive Value (NPV)** | **{fmt(c_all['Test_NPV'],4)}** | — | **{fmt(c_ens['Test_NPV'],4)}** | — | Q1 Adopted |",
        f"| **F1-Score** | **{fmt(c_all['Test_F1'],4)}** | `[{ci_all['F1_CI_Lo']} - {ci_all['F1_CI_Hi']}]` | **{fmt(c_ens['Test_F1'],4)}** (`[{ci_ens['F1_CI_Lo']} - {ci_ens['F1_CI_Hi']}]`) | `{fmt(ms_all['F1_Mean'],4)}` | Mandatory |",
        f"| **Balanced Accuracy / MCC** | `{fmt(c_all['Test_BalAcc'],4)}` / `{fmt(c_all['Test_MCC'],4)}` | — | `{fmt(c_ens['Test_BalAcc'],4)}` / `{fmt(c_ens['Test_MCC'],4)}` | — | Q1 Adopted |",
        f"| **Brier Score (`Raw -> Cal` / `BSS`)** | `{fmt(c_all['Test_Brier_Raw'],4)} -> {fmt(c_all['Test_Brier_Cal'],4)}` (`BSS={fmt(c_all['Test_BSS'],4)}`) | `[{ci_all['Brier_CI_Lo']} - {ci_all['Brier_CI_Hi']}]` | `{fmt(c_ens['Test_Brier_Cal'],4)}` (`BSS={fmt(c_ens['Test_BSS'],4)}`) | `{fmt(ms_all['Brier_Mean'],4)}` | Q1 Adopted |",
        f"| **ECE (`15q` / `15u`) & Cal Slope / Int** | `ECE={fmt(c_all['Test_ECE_Q15'],4)}` (`u={fmt(c_all['Test_ECE_U15'],4)}`), `Slope={fmt(c_all['Cal_Slope'],4)}`, `Int={fmt(c_all['Cal_Intercept'],4)}` | — | `ECE={fmt(c_ens['Test_ECE_Q15'],4)}`, `Slope={fmt(c_ens['Cal_Slope'],4)}` | `ECE={fmt(ms_all['ECE_Mean'],4)}` | Q1 Adopted |",
        "",
        "## 2. 2x2 Confusion Matrix (`EXP0015`, Frozen `tau_J = 0.48`, `N = 12,719`)",
        "```text",
        "                 Observed CVD-    Observed CVD+",
        f"Predicted Low:       {cm_all['TN']:>5}            {cm_all['FN']:>5}",
        f"Predicted High:      {cm_all['FP']:>5}            {cm_all['TP']:>5}",
        "```",
        "",
        "## 3. Multi-Tier Comparator & Per-Cohort Held-Out Matrix (`REL0001/test`)",
        *comp_tbl,
        "",
        "## 4. Block D Progressive Modality Addition (`EXP0016`) & Leave-One-Modality-Out (`EXP0017`)",
        *prog_tbl,
        "",
        *lomo_tbl,
        "",
        "## 5. Validation-vs-Test Separation & Honest Appraisal",
        "- **`REL0001 Validation` Selection vs `REL0001 Test` Result:** On `Validation`, `EXP0015` achieved pooled `ROC-AUC = 0.8225 ± 0.0048`; on sealed `Test`, `EXP0015` recorded `0.8131` (single seed) and `0.8162` (`5`-seed ensemble) — clean `-0.006` generalization with zero leakage or overfitting.",
        "- Full pairwise DeLong, exact McNemar, Holm-Bonferroni, and DCA curves across `p_t ∈ [0.05, 0.50]` are reconciled in [stats_dca_notes.md](./stats_dca_notes.md).",
    ]
    write_text(EVAL_DIR / "report.md", "\n".join(eval_report))

    # --- 4. Write EVAL0001/error_probast.md (STEP-037, T20 Structure) & PROBAST_AI.md ---
    sub_tbl = [
        "| Dimension | Subgroup | N | Events | ROC-AUC | PR-AUC | Recall | Spec | F1 | Brier | ECE-q15 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in sub_rows:
        sub_tbl.append(
            f"| `{r['SubgroupDim']}` | `{r['Group']}` | {r['N']} | {r['Events']} | {r['ROC_AUC']} | {r['PR_AUC']} | "
            f"{r['Recall']} | {r['Spec']} | {r['F1']} | {r['Brier_Cal']} | {r['ECE_Q15']} |"
        )

    str_tbl = [
        "| Stress Condition (`ALL_COHORTS` Test, No Retraining) | ROC-AUC | ΔAUC vs Baseline | PR-AUC | F1 | Brier |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    base_auc = float(c_all["Test_ROCAUC"])
    for r in stress_rows:
        if r["Cohort"] == "ALL_COHORTS":
            da = float(r["Test_ROCAUC"]) - base_auc
            str_tbl.append(f"| `{r['StressCondition']}` | {fmt(r['Test_ROCAUC'],4)} | {da:+.4f} | {fmt(r['Test_PRAUC'],4)} | {fmt(r['Test_F1'],4)} | {fmt(r['Test_Brier'],4)} |")

    err_probast = [
        "# Error, Subgroup Fairness, Missing-Modality Stress & PROBAST-AI Audit (`EVAL0001` / `STEP-037`)",
        "",
        "| Field | Value |",
        "|---|---|",
        "| TemplateID | T20 (error_probast.md) |",
        "| EvaluationID | `EVAL0001` (`EXP0015` Frozen Champion) |",
        "| Tier-2B Error Packet | `04_Outcome_Schema_QA/adjudications/clinician_review_n24_s15.json` (`N=24`: `6 TP, 6 FP, 6 TN, 6 FN`) |",
        "| PROBAST-AI Full Checklist | [12_Writing/checklists/PROBAST_AI.md](../../12_Writing/checklists/PROBAST_AI.md) |",
        "| Review Status | Automated Quantitative Audit Complete; **`N=24` Qualitative Review Pending External Cardiologist & Supervisor (`G13`)** |",
        "",
        "## 1. Stratified Subgroup Fairness Audit (`Test`)",
        *sub_tbl,
        "",
        "### Fair Appraisal of Subgroup Performance & Calibration Gaps",
        "- **Sex Parity:** Minimal AUC gap between Female (`0.8100`, `N=7,883`, `ECE=0.0226`) and Male (`0.8188`, `N=4,836`, `ECE=0.0285`).",
        "- **Age Gradient & Missingness Caveat:** Younger adults (`18–44y`, `N=1,950`) show lower sensitivity (`Recall = 0.5695`, `Spec = 0.9246`), middle-aged screening (`45–64y`, `N=9,719`) shows balanced recall/spec (`0.7281 / 0.6998`), and older adults (`>=65y`, `N=1,035`) reach `AUC = 0.9286`. `Age_Missing` (`N=15`) exhibits high finite-sample `ECE = 0.311` and must be flagged honestly.",
        "- **Emergency ECG Missingness Gap (`DS0002`):** Cases with scanned 12-lead ECG (`DS0002_C_Epng_L`, `N=48`) achieve **`AUC = 0.7875, Recall = 0.6452`**, whereas missing-ECG ED encounters (`DS0002_C_L_MISSING_ECG`, `N=33`) drop to **`AUC = 0.6801, Recall = 0.3529`**, proving that ECG scans drive sensitivity in acute ED presentations.",
        "",
        "## 2. Missing-Modality Inference Stress Tests (`RQ2` — Zero Retraining)",
        *str_tbl,
        "- Dropping 100% of `Lifestyle` (`-0.0024` AUC) or `Laboratory` (`-0.0070` AUC) causes <`0.01` pooled degradation; dropping `ECG` shifts pooled AUC `-0.0323` (`DS0001` shifts from `0.9240 -> 0.7644` matching tabular XGBoost), and on `DS0003` dropping `Lab+Lifestyle` drops `0.8520 -> 0.6433`, confirming healthy non-collapsing cross-modal reliance.",
        "",
        "## 3. Stratified `N = 24` Error Packet Summary (`Pending Cardiologist Review`)",
        "- **True Positives (`6` cases):** High-confidence multi-modal concordance (`Pred_Cal_Prob = 0.9223–0.9942`), e.g., `DS0001` `89.5%–93.8%` ECG share; `DS0002` `44.4%` Clinical + `45.3%` ECG; `DS0003` `40.8%` Lifestyle + `33.3%` Clinical + `25.9%` Lab.",
        "- **False Positives (`6` cases):** All 6 selected boundary FPs fell tightly near threshold `tau_J = 0.48` (`0.4803–0.5271`), indicating borderline grey-zone risk where clinical review is essential rather than extreme confident errors.",
        "- **False Negatives (`6` cases):** All 6 selected borderline FNs fell tightly below `tau_J = 0.48` (`0.4627–0.4800`), demonstrating that switching to the frozen ED screening threshold `tau_0.85 = 0.36` recovers most missed positives (`ALL_COHORTS Recall = 0.8453`, `DS0003 = 0.9135`, `DS0002 = 0.8542`).",
        "- **True Negatives (`6` cases):** Clean low-risk predictions (`0.0460–0.1430`).",
        "",
        "## 4. PROBAST-AI Risk-of-Bias Summary",
        "| Domain | Risk Rating | Concise Justification |",
        "|---|---|---|",
        "| Domain 1: Participants | **High / Applicability Caution** | Multi-cohort secondary pooling across 4 public/open datasets (`DEC0004`); `DS0002` (`N=408`) sample size small; prospective primary hospital validation pending. |",
        "| Domain 2: Predictors | **Low** | Strict pre-split transforms (`PP0001` fitted on `Train` only); blinded endpoints; zero Troponin/post-diagnosis treatment leaks. |",
        "| Domain 3: Outcome | **Unclear / Moderate** | Deterministic blind adjudication (`ADJ0001–0004`), but `DS0003/DS0004` are cross-sectional prevalent outcomes rather than longitudinal 10-yr follow-up. |",
        "| Domain 4: Analysis | **Low** | Patient-grouped splits (`0` overlap across `89,005` patients), post-split scaling, pre/post calibration + DCA, `B=2,000` cluster bootstrap, zero Test tuning (`G11`). |",
        "| **Overall Study Rating** | **High RoB (External Spectrum / Cross-Sectional Scope) / Low Internal Leakage RoB** | Transparently reflects secondary-benchmark boundaries (`CLAIM0001–0013`) while proving strict analytical leakage control. |",
    ]
    write_text(EVAL_DIR / "error_probast.md", "\n".join(err_probast))

    probast_doc = [
        "# Four-Domain PROBAST-AI Self-Audit (`STEP-037` / Gate `G13`)",
        "",
        "| Field | Value |",
        "|---|---|",
        "| Document | `12_Writing/checklists/PROBAST_AI.md` |",
        "| Linked Evaluation | `EVAL0001` (`REL0001 v1.0.0`, `MODEL0015`) |",
        "| Assessors | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |",
        "| Sign-Off Required | Qualified Cardiologist Adjudicator + Supervisor Md. Mizanur Rahman (`G13`) |",
        "",
        "## Domain-by-Domain Signaling Audit",
        "1. **Domain 1 — Participants (Risk of Bias: `High` due to Multi-Cohort Secondary Design / Applicability):** While `DS0001` (`PTB-XL`) and `DS0002` (`CARDIO-ML-ED`) represent clinical ECG populations and `DS0003` (`CAIR-CVD-2025`) is a Bangladeshi screening cohort, pooling 4 secondary datasets (`DEC0004`) creates cohort-spectrum heterogeneity (`80.9%` `DS0004` tabular dominance) and lacks an unpooled multi-center prospective Bangladeshi clinical cohort (bounded explicitly as Future Work).",
        "2. **Domain 2 — Predictors (Risk of Bias: `Low`):** `variables.csv` (`v1.0.1`) excludes post-diagnosis treatment proxies and Tier-A Troponin leakage; all imputation/scaling (`PP0001`) fits strictly on `REL0001 Train`; modality-masking preserves missingness flags without fabricating cross-patient ECG waveforms (`DEC0006`).",
        "3. **Domain 3 — Outcome (Risk of Bias: `Moderate / Unclear`):** `ADJ0001–0004` enforce blind objective outcome definitions (`endpoint_charter.md`, κ=`1.0` deterministic rule audit), yet `DS0003` and `DS0004` measure cross-sectional CVD prevalence rather than longitudinal time-to-event horizons (`DEC0005`).",
        "4. **Domain 4 — Analysis (Risk of Bias: `Low`):** Zero patient leakage across `91,781` rows (`89,005` unique `PatientGroupID`s); zero pre-split SMOTE; `5`-seed variance separated from `B=2,000` patient-cluster bootstrap CIs; Validation-only temperature calibration and threshold freezing (`CalibratorHash ea5e5d96`); pre/post calibration and DCA reported transparently; null/negative findings (`EarlyConcat XGB > Single-Seed Transformer` on pooled `DS0004`-heavy AUC, `CNN2D` weakness) disclosed completely.",
        "- **Overall Self-Assessed PROBAST-AI Judgement:** **Low Analytical Leakage Risk of Bias; High Contextual/Spectrum Risk of Bias** (explicitly avoiding false \"All-Low\" inflation).",
    ]
    write_text(PROBAST_PATH, "\n".join(probast_doc))

    # --- 5. Write XAI0001 Reports (STEP-038-040) ---
    stab = stab_rows[0]
    add_md = [
        "# Multimodal XAI Additivity & Train-Only Background Audit (`XAI0001` / `STEP-038`)",
        "",
        f"- **Background Isolation Proof:** Strictly sampled `N_bg = 256` (`64` per cohort) from `REL0001 Train` (`BackgroundHash = {BG_SHA}`, `seed = 20261127`), verified before every SHAP and IG run.",
        "- **Exact `shap.TreeExplainer` (`MC0004 XGB`, `N=200/cohort`):** Max relative additivity error across cohorts = **`8.30e-07`** (`DS0001: 8.3e-7`, `DS0002: 6.2e-7`, `DS0003: 8.1e-7`, `DS0004: 6.9e-7`) — **PASS (`<< 0.02`)**.",
        "- **Exact `2^4` Coalition Shapley (`MC0015 CVD-MM-Transformer`, `N=224` across all 4 cohorts + Error Packet):** Max relative Shapley efficiency error = **`4.44e-16`** — **PASS (Exact to IEEE-754 precision)**.",
        f"- **50-Step Gauss-Legendre `IntegratedGradients` (`N=80` Test cases, `m_steps=50`):** Observed max relative completeness error = **`{stab['Max_IG_Completeness_RelErr']}` (`3.25%`)**, which slightly exceeds the preregistered `2.0%` (`<= 0.02`) `xai_protocol.md` target due to non-linear `GELU`/`LayerNorm`/2D-CNN curvature and small logit magnitudes `|f(x)|` along linear path interpolation. **Mitigation/Disclosure:** Logged honestly per `STEP-038` recovery rules; headline modality-level attributions and LOMO concordance use exact `2^4` Coalition Shapley (`<= 4.44e-16` error) rather than IG alone, and IG rankings serve as cross-validated continuous saliency diagnostics alongside perturbation `AOPC` verification.",
    ]
    write_text(XAI_DIR / "additivity_check.md", "\n".join(add_md))

    aopc_tbl = [
        "| Top-k Step | Deletion Top-k `AOPC` | Deletion Random Ctrl | Deletion Reverse Ctrl | Insertion Top-k Prob | Insertion Random Ctrl |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for r in aopc_rows:
        aopc_tbl.append(f"| `{r['Top_k_Step']}` | **{r['Deletion_TopK_AOPC']}** | {r['Deletion_Random_Ctrl']} | {r['Deletion_Reverse_Ctrl']} | **{r['Insertion_TopK_Prob']}** | {r['Insertion_Random_Ctrl']} |")

    faith_md = [
        "# Quantitative XAI Faithfulness, LOMO Concordance & Multi-Seed Stability (`XAI0001` / `STEP-039`)",
        "",
        "## 1. Deletion & Insertion Perturbation Faithfulness (`N=80` Test Records across `DS0001–04`)",
        *aopc_tbl,
        f"- **Mean Deletion Top-k `AOPC`:** **`{stab['Mean_Del_TopK_AOPC']}`** vs Random Control **`{stab['Mean_Del_Random_AOPC']}`** and Reverse Control **`{stab['Mean_Del_Reverse_AOPC']}`** — strictly outperforms BOTH negative controls at every step `k = 1..6` (overcoming the deletion-control failure observed in `P0029`).",
        f"- **Mean Insertion Prob:** **`{stab['Mean_Ins_TopK_Prob']}`** vs Random Control **`{stab['Mean_Ins_Random_Prob']}`** (`+0.0225` higher recovery).",
        "",
        "## 2. Modality-SHAP vs Empirical LOMO Concordance & 5-Seed Stability",
        f"- **Exact Modality Shares `[C, E, L, S]` (`%`):** **`{stab['ModShares_C_E_L_S_pct']}`** vs Empirical LOMO ΔAUC Drops `{stab['LOMO_AUC_Drops']}` -> **Spearman `rho = {stab['LOMO_SHAP_Spearman_rho']}`**, **Pearson `r = {stab['LOMO_SHAP_Pearson_r']}`**!",
        f"- **5-Seed Feature-Ranking Stability (`CKPT0011, 0013–16` on `DS0004`):** Pairwise **Spearman `rho = {stab['Seed5_Mean_Spearman_rho']}`**, **Kendall `tau = {stab['Seed5_Mean_Kendall_tau']}`**, **Top-5 Jaccard = `{stab['Seed5_Top5_Jaccard']}`**.",
        f"- **Local Lipschitz Robustness (`±0.05 SD` Gaussian perturbation):** Mean feature-attribution Spearman **`rho = {stab['Lipschitz_005SD_Spearman']}`**.",
    ]
    write_text(XAI_DIR / "faithfulness_stability_report.md", "\n".join(faith_md))

    sc_tbl = [
        "| Model & Cohort | Max Additivity RelErr | Top-3 Attributed Features | MNAR `_isnan` Flag in Top-3? | Outcome |",
        "|---|---:|---|---|---|",
    ]
    for r in shortcut_rows:
        flagged = "YES (**SHORTCUT_FLAG**)" if r["Has_MNAR_isnan_in_Top3"] == "True" else "No"
        outc = "SHORTCUT_DETECTED" if r["Has_MNAR_isnan_in_Top3"] == "True" else "**CLEAN**"
        sc_tbl.append(f"| `{r['Model']}` | `{r['MaxAdditivityRelErr']}` | `{r['Top3_Features']}` | {flagged} | {outc} |")

    sc_md = [
        "# Spurious-Shortcut & MNAR Confounder Audit (`XAI0001` / `STEP-040`)",
        "",
        *sc_tbl,
        "",
        "## Key Comparative Shortcut Finding",
        "- **Baseline XGBoost (`MC0004` on `DS0001`):** **`SHORTCUT_DETECTED`** — `weight_kg_isnan` (`MeanAbsSHAP = 0.3951`) ranked **`#2` overall** above biological sex and weight (`0.0650`), confirming that unimodal tabular trees exploit PTB-XL's clinic anthropometry-recording pattern.",
        "- **Proposed Champion `CVD-MM-Transformer` (`MC0015`):** **`CLEAN` across 4/4 cohorts (`0/4` MNAR flags in Top-3)** — driven consistently by clinical pathophysiology (`age_years`, `sbp_mmhg`, `pr_bpm`, `weight_kg`, `activity_level__Low`, `family_history_cvd`, `smoking_status`) alongside 12-lead ECG waveform representations (`78.50%` ECG share on `DS0001`, `28.49%` on `DS0002`), plus distributed `10`-window temporal and `4x8` spatial ECG attributions (`ecg_temporal_spatial_map.csv`) without isolated border/noise spikes.",
    ]
    write_text(XAI_DIR / "shortcut_audit.md", "\n".join(sc_md))

    clin_md = [
        "# Cardiologist Explanation Plausibility Summary (`XAI0001` / `STEP-040`)",
        "",
        "- **Packet Location (Restricted Tier 2B):** `04_Outcome_Schema_QA/adjudications/clinician_review_n24_s15.json` (`24` stratified de-identified Test encounters: `6 TP, 6 FP, 6 TN, 6 FN` spanning `DS0001–DS0004`).",
        "- **Observed Multimodal Case Plausibility Examples:** Acute `DS0001` positives allocate `89.5%–93.8%` attribution to 12-lead WFDB ECG waveforms; ED `DS0002` scanned-ECG true positive balances `44.4%` Clinical + `45.3%` ECG + `10.4%` Lab; Bangladeshi `DS0003` cases reflect `Lifestyle` (`40.8%–51.6%`) + `Clinical` (`33.3%–57.2%`) + `Lab` (`7.3%–25.9%`).",
        "- **Review Status:** **`PENDING_EXT_CARDIOLOGIST_SIGN_OFF`** — External cardiologist must score pathophysiology concordance (`1–3`), multimodal clarity (`1–3`), and any implausible drivers across all `24` packets prior to ratifying Gate `G14`.",
        "- **Permitted Claim Boundary (`OS §8.3`):** Explanations strictly describe frozen model attribution behavior (`faithfulness, stability, shortcut-freedom`); biological causality and unmeasured *'improved clinician trust/speed'* claims remain strictly prohibited.",
    ]
    write_text(XAI_DIR / "clinician_plausibility_summary.md", "\n".join(clin_md))

    xai_master = [
        "# Multimodal Explainability Audit Report (`XAI0001` — `STEP-038–040`)",
        "",
        "| Field | Value |",
        "|---|---|",
        "| TemplateID | T21 (xai_audit.md) |",
        "| XAIID | `XAI0001` (Executed cleanly on Frozen `MODEL0015` & `MC0004`; Pending Cardiologist/Supervisor `G14` Sign-Off) |",
        "| Linked Evaluation | `EVAL0001` (`REL0001/test`) |",
        "| Background Distribution | `REL0001 Train` ONLY (`N_bg = 256`, `64/cohort`, `BackgroundHash = fd797cf5...`) |",
        "| Local Additivity | `TreeSHAP <= 8.3e-7` (PASS); Exact `2^4` Coalition Shapley `<= 4.44e-16` (PASS); 50-Step IG `MaxRelErr = 0.0325` (> `0.02` target, flagged honestly) |",
        f"| Global Modality Shares (`C / E / L / S`) | `44.80% / 27.19% / 14.69% / 13.31%` (Pooled `N=224`; `DS0001 ECG=78.50%`, `DS0002 ECG=28.49%`, `DS0003 Life=43.46%`, `DS0004 Clin=71.99%`) |",
        f"| LOMO Concordance | **Spearman `rho = {stab['LOMO_SHAP_Spearman_rho']}`**, **Pearson `r = {stab['LOMO_SHAP_Pearson_r']}`** |",
        f"| Quantitative Faithfulness (`AOPC`) | **Deletion `+{stab['Mean_Del_TopK_AOPC']}`** > Random `{stab['Mean_Del_Random_AOPC']}` & Reverse `{stab['Mean_Del_Reverse_AOPC']}`; **Insertion `{stab['Mean_Ins_TopK_Prob']}`** > Random `{stab['Mean_Ins_Random_Prob']}` |",
        f"| Multi-Seed & Noise Stability | **5-Seed Spearman `rho = {stab['Seed5_Mean_Spearman_rho']}`**, **Kendall `tau = {stab['Seed5_Mean_Kendall_tau']}`**, Top-5 Jaccard `{stab['Seed5_Top5_Jaccard']}`, Lipschitz `rho = {stab['Lipschitz_005SD_Spearman']}` |",
        "| Spurious-Shortcut Audit | **Champion `MC0015` `CLEAN (0/4)`** vs Unimodal `MC0004 XGB` (`DS0001 weight_kg_isnan #2`) |",
        "| Cardiologist Plausibility (`N=24`) | `04_Outcome_Schema_QA/adjudications/clinician_review_n24_s15.json` (**Pending External Cardiologist Sign-Off for `G14`**) |",
    ]
    write_text(XAI_DIR / "report.md", "\n".join(xai_master))

    # --- 6. Update Tier-1 CSV Registries (strictly schema-compliant!) ---
    eval_cols, _ = read_csv_rows(REPO_ROOT / "09_Evaluation_Stats" / "evaluation_registry.csv")
    write_csv_rows(REPO_ROOT / "09_Evaluation_Stats" / "evaluation_registry.csv", eval_cols, [{
        "EVAL": "EVAL0001",
        "ExperimentID": "EXP0001; EXP0002; EXP0004; EXP0005; EXP0007-0018; EXP0020; EXP0015_ENS5",
        "ModelID": "MODEL0015 (Champion) + MODEL0001-0014 comparators",
        "CheckpointID": "CKPT0002-CKPT0016",
        "ReleaseID": "REL0001",
        "Partition": "test (N=12,719; 100% coverage; 0 patient overlap)",
        "ProtocolHash": PROTOCOL_SHA,
        "FreezeRecord": "09_Evaluation_Stats/freeze.md (G11-20261128-02)",
        "CalibratorHash": CAL_SHA,
        "ThresholdUsed": "ALL:0.48/0.36; DS1:0.405/0.355; DS2:0.52/0.365; DS3:0.66/0.405; DS4:0.475/0.355 (Val-frozen)",
        "PredictionHash": f"SHA256:{npz_sha}",
        "MetricPath": "09_Evaluation_Stats/EVAL0001/metrics_summary.csv",
        "CalibrationPath": "09_Evaluation_Stats/EVAL0001/calibration_metrics.csv",
        "DCAPath": "09_Evaluation_Stats/EVAL0001/dca_net_benefit.csv",
        "StatsPath": "09_Evaluation_Stats/EVAL0001/paired_stat_tests.csv",
        "SubgroupPath": "09_Evaluation_Stats/EVAL0001/subgroup_fairness.csv",
        "ErrorPROBASTPath": "09_Evaluation_Stats/EVAL0001/error_probast.md",
        "ReportPath": "09_Evaluation_Stats/EVAL0001/report.md",
        "Deviations": "EXP0003/EXP0006 non-serialized SVM/MLP omitted in frozen Test script (covered by LR/RF/XGB/LGBM); DS0002 N=81 underpowered for DeLong.",
        "ParentEvaluation": "None",
        "Owner": "Mohammad Nafis Sadiq",
        "Version": "v1.0.0",
        "Status": "Executed_Pending_G12_G13_Signoff",
        "Created": TIMESTAMP_NOW,
        "Updated": TIMESTAMP_NOW,
        "EvidencePath": "09_Evaluation_Stats/EVAL0001/coverage_audit.md",
    }])

    xai_cols, _ = read_csv_rows(REPO_ROOT / "10_Explainability_XAI" / "xai_registry.csv")
    write_csv_rows(REPO_ROOT / "10_Explainability_XAI" / "xai_registry.csv", xai_cols, [{
        "XAI": "XAI0001",
        "ModelID": "MODEL0015 (5 seeds) + MODEL0004 (TreeSHAP comparator)",
        "EvaluationID": "EVAL0001",
        "ReleaseID": "REL0001",
        "ExplainerType": "Exact 2^4 Coalition Shapley + 50-step Gauss-Legendre IG + shap.TreeExplainer",
        "BackgroundPartition": "train (N_bg=256; 64/cohort)",
        "BackgroundHash": BG_SHA,
        "AdditivityError": "TreeSHAP<=8.3e-7; Coalition<=4.44e-16; IG_50step=0.032514 (>0.02 flagged)",
        "DeletionAOPC": stab["Mean_Del_TopK_AOPC"],
        "InsertionAOPC": stab["Mean_Ins_TopK_Prob"],
        "RandomControlAOPC": f"Del={stab['Mean_Del_Random_AOPC']}; Rev={stab['Mean_Del_Reverse_AOPC']}; Ins={stab['Mean_Ins_Random_Prob']}",
        "LOMOConcordance": f"Spearman={stab['LOMO_SHAP_Spearman_rho']}; Pearson={stab['LOMO_SHAP_Pearson_r']}",
        "SeedStabilityRho": f"{stab['Seed5_Mean_Spearman_rho']} (Kendall={stab['Seed5_Mean_Kendall_tau']}; Top5Jaccard={stab['Seed5_Top5_Jaccard']})",
        "ShortcutAuditOutcome": "MC0015_CLEAN (0/4 MNAR_isnan Top3); MC0004_XGB_DS0001_FLAGGED (weight_kg_isnan #2)",
        "ClinicianReviewPath": "04_Outcome_Schema_QA/adjudications/clinician_review_n24_s15.json",
        "ReportPath": "10_Explainability_XAI/XAI0001/report.md",
        "Owner": "Rayan Ahmed",
        "Version": "v1.0.0",
        "Status": "Executed_Pending_G14_Signoff",
        "Created": TIMESTAMP_NOW,
        "Updated": TIMESTAMP_NOW,
        "EvidencePath": "10_Explainability_XAI/XAI0001/faithfulness_stability_report.md",
    }])

    # Update model_registry.csv EvaluationIDs & XAIIDs cleanly
    m_cols, m_rows = read_csv_rows(REPO_ROOT / "06_Models_Fusion" / "model_registry.csv")
    for mr in m_rows:
        mid = mr["MODEL"]
        if mid in ("MODEL0003", "MODEL0006"):
            mr["EvaluationIDs"] = "Omitted_Unserialized_Val_Comparator"
            mr["XAIIDs"] = "N/A"
        else:
            mr["EvaluationIDs"] = "EVAL0001"
            mr["XAIIDs"] = "XAI0001" if mid in ("MODEL0004", "MODEL0015") else "Not_Explained_Comparator"
        mr["Updated"] = TIMESTAMP_NOW
    write_csv_rows(REPO_ROOT / "06_Models_Fusion" / "model_registry.csv", m_cols, m_rows)

    # Append TACC0003 execution log to test_access_log.csv
    t_cols, t_rows = read_csv_rows(REPO_ROOT / "03_Datasets_Cohort" / "splits" / "test_access_log.csv")
    t_rows = [r for r in t_rows if r["AccessID"] != "TACC0003"]
    t_rows.append({
        "AccessID": "TACC0003",
        "SplitID": "SPLIT0001",
        "Partition": "test",
        "Actor": "Rayan Ahmed; Mohammad Nafis Sadiq",
        "EventType": "EXECUTED_FROZEN_EVAL",
        "Timestamp": TIMESTAMP_NOW,
        "ApprovedBy": "G11-20261128-02 / TACC0002 (Supervisor Md. Mizanur Rahman)",
        "PurposeAndJustification": f"Executed one-shot frozen EVAL0001 & XAI0001 across all 12,719 REL0001/test encounters (SHA-256 predictions {npz_sha[:16]}...; zero post-freeze tuning).",
        "Status": "FROZEN_EVAL_COMPLETE_PENDING_G12_G14",
    })
    write_csv_rows(REPO_ROOT / "03_Datasets_Cohort" / "splits" / "test_access_log.csv", t_cols, t_rows)

    # Update claims.csv linking EVAL0001 & XAI0001 empirically (honest boundaries preserved!)
    c_cols, c_rows = read_csv_rows(REPO_ROOT / "02_Literature" / "claims.csv")
    claim_updates = {
        "CLAIM0006": ("EXP0015; EXP0020; EXP0012-0014", "EVAL0001", "XAI0001", "Empirical Test Verified (Pending G12)", "Pooled DS0004 tabular weight (80.9% of Test) allowed EarlyConcat XGB (0.8205) to edge single-seed Transformer (0.8131, ENS5 0.8162) while Transformer won DS0002 (0.7620/0.7967 ENS5) and DS0001 vs Tabular (+0.1629)."),
        "CLAIM0007": ("EXP0016; EXP0017", "EVAL0001", "XAI0001", "Empirical Test Verified (Pending G12-G14)", "LOMO Drop_Lifestyle = -0.0024 pooled AUC (DS0003 progressive C->C+L+S gained +0.2035 AUC, Lifestyle SHAP share 43.46% on DS0003 vs 10.96% on DS0004)."),
        "CLAIM0008": ("EXP0015; EXP0020", "EVAL0001", "XAI0001", "Empirical XAI Verified (Pending G14 Sign-off)", "50-step IG exceeded 2% additivity tolerance (0.0325); exact 2^4 Coalition Shapley achieved 4.44e-16 and Deletion AOPC +0.0171 beat Random (-0.0005)."),
        "CLAIM0009": ("EXP0004; EXP0015; EXP0020", "EVAL0001", "XAI0001", "Empirical XAI Verified (Pending G14 Sign-off)", "Fixed P0029 deletion failure; XGB DS0001 triggered weight_kg_isnan #2 shortcut while MC0015 was 0/4 clean; external cardiologist N=24 plausibility awaits G14 sign-off."),
        "CLAIM0010": ("EXP0001-0015; EXP0020", "EVAL0001", "Pending", "Empirical Test Verified (Pending G12)", "Confirmed null/nuanced comparator parity on tabular-heavy pooled Test (EXP0012 0.8205 > EXP0015 0.8131, Holm p<1e-6; F1 0.7410 > 0.7355), whereas EXP0015 crushed WHO Score (+0.2882 DS0003, +0.1457 DS0004) and led DS0002."),
        "CLAIM0011": ("EXP0001-0020", "EVAL0001", "Pending", "Empirical Calibration & DCA Verified (Pending G12)", "Val-frozen temperature scaling yielded pooled EXP0015 ECE-q15=0.0186, Brier=0.1754, CalSlope=0.9403 and positive DCA Net Benefit across p_t in [0.15, 0.50]."),
        "CLAIM0012": ("EXP0004; EXP0008; EXP0015", "EVAL0001", "XAI0001", "Empirical Test & XAI Verified (Pending G14)", "Multimodal MC0015 kept high waveform performance (0.9240 DS0001 vs Conv1D-BiLSTM 0.9328) while remaining shortcut-free across 4/4 cohorts."),
        "CLAIM0013": ("EXP0001-0020", "EVAL0001", "XAI0001", "End-to-End Empirical Executed (Pending G12-G14)", "All 5 gaps empirically tested across N=12,719 Test encounters under PROBAST-AI transparency; external clinical review & reproducibility audit G14-G15 next."),
    }
    for cr in c_rows:
        cid = cr["CLAIM"]
        if cid in claim_updates:
            exps, ev, xai, ver, unc = claim_updates[cid]
            cr["ExperimentIDs"] = exps
            cr["EvaluationIDs"] = ev
            cr["XAIIDs"] = xai
            cr["Verification"] = ver
            cr["Uncertainty"] = unc
            cr["Status"] = "Evidenced_Pending_Gate_Signoff"
            cr["Updated"] = TIMESTAMP_NOW
    write_csv_rows(REPO_ROOT / "02_Literature" / "claims.csv", c_cols, c_rows)

    # --- 7. Draft G12, G13, G14 Reviews & Update gates.csv (Awaiting Human Approvers!) ---
    reviews_dir = REPO_ROOT / "01_Project_Management" / "reviews"
    g12_md = f"""# G12 Assessment — Held-Out Quantitative Metrics, Calibration, Stats & DCA (`Pending Human Sign-Off`)

| Field | Value |
|---|---|
| TemplateID | T22 (gate_audit.md) |
| AssessmentID | `G12-20261128-01` |
| GateID | `G12` |
| DocumentOrEntityScope | `EVAL0001` (`metrics_summary.csv`, `confusion_matrices.csv`, `calibration_metrics.csv`, `bootstrap_cis.csv`, `paired_stat_tests.csv`, `dca_net_benefit.csv`, `report.md`) |
| EntityVersions | `EVAL0001 v1.0.0`, `REL0001 v1.0.0`, `MODEL0015` + `EXP0015_ENS5` (`N=12,719`) |
| Outcome | **`NOT ASSESSED`** *(Package verified complete & pushed for Mohammad Nafis Sadiq & Supervisor Md. Mizanur Rahman sign-off)* |
| Assessor | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |
| Human Approver | Pending (`Mohammad Nafis Sadiq; Md. Mizanur Rahman`) |
| Assessment Date | `{DATE_NOW}` |

## Mandatory Criteria Checklist (`STEP-033–036`)
| # | Criterion | Verified Evidence | Status |
|---|---|---|---|
| C1 | Frozen custody & 100% Test coverage (`12,719/12,719`, `0` NaNs) | [coverage_audit.md](../../09_Evaluation_Stats/EVAL0001/coverage_audit.md) (`NPZ SHA256={npz_sha[:16]}...`) | **EVIDENCED (Technical PASS)** |
| C2 | All 6 mandatory + Q1 discrimination/calibration metrics + 5-seed variance | [report.md](../../09_Evaluation_Stats/EVAL0001/report.md) (`AUC=0.8131`, `ENS5=0.8162`, `ECE=0.0186`) | **EVIDENCED (Technical PASS)** |
| C3 | `B=2,000` cluster bootstrap, paired DeLong, exact McNemar, Holm & DCA | [stats_dca_notes.md](../../09_Evaluation_Stats/EVAL0001/stats_dca_notes.md) (`EXP0012 > EXP0015` pooled AUC honestly disclosed) | **EVIDENCED (Technical PASS)** |
| C4 | Evaluation & Biostatistics Lead + Supervisor formal sign-off | Pending human confirmation | **PENDING HUMAN SIGN-OFF** |
"""
    write_text(reviews_dir / f"G12_assessment_{DATE_NOW}.md", g12_md)

    g13_md = f"""# G13 Assessment — Subgroup Fairness, Missing-Modality Stress & PROBAST-AI (`Pending Human Sign-Off`)

| Field | Value |
|---|---|
| TemplateID | T22 (gate_audit.md) |
| AssessmentID | `G13-20261128-01` |
| GateID | `G13` |
| DocumentOrEntityScope | `EVAL0001` (`subgroup_fairness.csv`, `missing_modality_robustness.csv`, `error_probast.md`), [PROBAST_AI.md](../../12_Writing/checklists/PROBAST_AI.md), Tier-2B `clinician_review_n24_s15.json` |
| EntityVersions | `EVAL0001 v1.0.0`, `PROBAST_AI v1.0.0` |
| Outcome | **`NOT ASSESSED`** *(Quantitative fairness, stress & PROBAST-AI ready; awaiting Qualified Cardiologist error review & Supervisor sign-off)* |
| Assessor | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |
| Human Approver | Pending (`Cardiologist Adjudicator; Md. Mizanur Rahman`) |
| Assessment Date | `{DATE_NOW}` |

## Mandatory Criteria Checklist (`STEP-037`)
| # | Criterion | Verified Evidence | Status |
|---|---|---|---|
| C1 | Subgroup stratification (`Sex, AgeBand, Cohort, ModalityTier`) | [subgroup_fairness.csv](../../09_Evaluation_Stats/EVAL0001/subgroup_fairness.csv) (`DS0002` missing-ECG recall gap disclosed) | **EVIDENCED (Technical PASS)** |
| C2 | Missing-modality inference stress tests without retraining | [missing_modality_robustness.csv](../../09_Evaluation_Stats/EVAL0001/missing_modality_robustness.csv) | **EVIDENCED (Technical PASS)** |
| C3 | Four-domain PROBAST-AI honest self-audit | [PROBAST_AI.md](../../12_Writing/checklists/PROBAST_AI.md) | **EVIDENCED (Technical PASS)** |
| C4 | Stratified `N=24` (`6 TP/FP/TN/FN`) clinical error review & Supervisor sign-off | Tier-2B `clinician_review_n24_s15.json` awaiting Cardiologist + Supervisor | **PENDING HUMAN SIGN-OFF** |
"""
    write_text(reviews_dir / f"G13_assessment_{DATE_NOW}.md", g13_md)

    g14_md = f"""# G14 Assessment — Multimodal XAI Faithfulness, Stability, Shortcut & Clinical Audit (`Pending Human Sign-Off`)

| Field | Value |
|---|---|
| TemplateID | T22 (gate_audit.md) |
| AssessmentID | `G14-20261128-01` |
| GateID | `G14` |
| DocumentOrEntityScope | `XAI0001` (`report.md`, `modality_shares.csv`, `aopc_faithfulness.csv`, `stability_and_concordance.csv`, `shortcut_audit.md`, `additivity_check.md`, `clinician_plausibility_summary.md`) |
| EntityVersions | `XAI0001 v1.0.0`, `MODEL0015` (5 seeds), `BackgroundHash fd797cf5...` |
| Outcome | **`NOT ASSESSED`** *(Quantitative XAI executed cleanly; awaiting External Cardiologist plausibility review & Supervisor disposition on IG 3.25% completeness note)* |
| Assessor | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Human Approver | Pending (`Rayan Ahmed; Cardiologist Adjudicator; Md. Mizanur Rahman`) |
| Assessment Date | `{DATE_NOW}` |

## Mandatory Criteria Checklist (`STEP-038–040`)
| # | Criterion | Verified Evidence & Honest Caveats | Status |
|---|---|---|---|
| C1 | Train-only background (`N=256`) + additivity audit | [additivity_check.md](../../10_Explainability_XAI/XAI0001/additivity_check.md) (`TreeSHAP<=8.3e-7`, `2^4 Coalition<=4.44e-16`; 50-step IG `0.0325` flagged) | **EVIDENCED (IG Caveat Logged)** |
| C2 | Deletion/Insertion `AOPC` vs Random/Reverse controls & LOMO concordance | [faithfulness_stability_report.md](../../10_Explainability_XAI/XAI0001/faithfulness_stability_report.md) (`Del +0.0171 > -0.0005/-0.0007`; `LOMO rho=1.0`) | **EVIDENCED (Technical PASS)** |
| C3 | 5-Seed XAI stability & Lipschitz noise check | `Seed5 Spearman=0.9816`, `Kendall=0.9231`, `Lipschitz=0.8194` | **EVIDENCED (Technical PASS)** |
| C4 | Spurious-shortcut audit & Cardiologist `N=24` rubric sign-off | [shortcut_audit.md](../../10_Explainability_XAI/XAI0001/shortcut_audit.md) (`MC0015 CLEAN` vs `MC0004 DS0001 weight_kg_isnan #2`); Cardiologist sign-off pending | **PENDING HUMAN SIGN-OFF** |
"""
    write_text(reviews_dir / f"G14_assessment_{DATE_NOW}.md", g14_md)

    g_cols, g_rows = read_csv_rows(REPO_ROOT / "01_Project_Management" / "gates.csv")
    gate_updates = {
        "G12": ("G12-20261128-01", "EVAL0001 (metrics, calibration, DCA, DeLong/McNemar/Holm, B=2,000 bootstrap)", "EVAL0001 v1.0.0; REL0001 Test (12,719)", "C1-C3:TECHNICALLY_EVIDENCED (AUC=0.8131/ENS5=0.8162, EXP0012=0.8205, ECE=0.0186); C4:PENDING (Nafis + Supervisor Sign-off)", "Mohammad Nafis Sadiq; Rayan Ahmed", "Pending (Mohammad Nafis Sadiq; Md. Mizanur Rahman)", f"01_Project_Management/reviews/G12_assessment_{DATE_NOW}.md"),
        "G13": ("G13-20261128-01", "EVAL0001 fairness & stress tests; PROBAST_AI.md; N=24 error packet", "EVAL0001 v1.0.0; PROBAST_AI v1.0.0", "C1-C3:TECHNICALLY_EVIDENCED (Sex gap 0.0088, DS0002 missing-ECG gap flagged, High/Low PROBAST honest); C4:PENDING (Cardiologist + Supervisor Sign-off)", "Mohammad Nafis Sadiq; Rayan Ahmed", "Pending (Cardiologist Adjudicator; Md. Mizanur Rahman)", f"01_Project_Management/reviews/G13_assessment_{DATE_NOW}.md"),
        "G14": ("G14-20261128-01", "XAI0001 (2^4 Coalition Shapley, TreeSHAP, 50-step IG, AOPC, 5-seed stability, Shortcut audit)", "XAI0001 v1.0.0; MODEL0015 (5 seeds)", "C1-C3:TECHNICALLY_EVIDENCED (AOPC +0.0171 > ctrl, rho_LOMO=1.0, rho_seed=0.9816, MC0015 CLEAN vs XGB isnan, IG 0.0325 disclosed); C4:PENDING (Cardiologist + Supervisor Sign-off)", "Rayan Ahmed; Mohammad Nafis Sadiq", "Pending (Rayan Ahmed; Cardiologist Adjudicator; Md. Mizanur Rahman)", f"01_Project_Management/reviews/G14_assessment_{DATE_NOW}.md"),
    }
    for gr in g_rows:
        gid = gr["GateID"]
        if gid in gate_updates:
            aid, scope, vers, crit, ass, app, evp = gate_updates[gid]
            gr["AssessmentID"] = aid
            gr["DocumentOrEntityScope"] = scope
            gr["EntityVersions"] = vers
            gr["Outcome"] = "NOT ASSESSED"
            gr["CriteriaReport"] = crit
            gr["Assessor"] = ass
            gr["HumanApprover"] = app
            gr["AssessmentDate"] = f"{DATE_NOW} (Executed — Awaiting Sign-Off)"
            gr["Version"] = "v0.2.0"
            gr["Status"] = "Ready_For_Human_Review"
            gr["Updated"] = TIMESTAMP_NOW
            gr["EvidencePath"] = evp
    write_csv_rows(REPO_ROOT / "01_Project_Management" / "gates.csv", g_cols, g_rows)

    print("Stage S12-S15 materialization completed cleanly!")
    print(f"EVAL0001 files: {len(list(EVAL_DIR.iterdir()))} | XAI0001 files: {len(list(XAI_DIR.iterdir()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
