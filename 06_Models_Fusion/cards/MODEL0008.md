# MODEL0008 — CNN_BiLSTM_ECG (`MC0008`, DS0001_WFDB_Conv1DBiLSTM)

| Field | Value |
|---|---|
| TemplateID | T17 (model_card.md) |
| template_version | v1.0.0 |
| entity_id | `MODEL0008` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-28` |
| status | `G10_Audited_Comparator` |
| source_inputs | `REL0001` (`Train/Val` Only; `SPLIT0001`, `PP0001`, `FitStateHash=d9ccfbf40b2b...`) |
| governing_section | OS §6.3, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Model Overview
- **Model ID:** `MODEL0008` (`MC0008` — `Tier_1_Unimodal`)
- **Architecture:** Conv1D Stem + 2-Layer BiLSTM(32) (~65K params) (`PyTorch`)
- **Parameter / Artifact Budget:** `Conv1DBiLSTMEncoder (~65K params; 134,881 B)`
- **Primary Experiment:** `EXP0008`
- **Checkpoints (`G10` SHA-256 Verified):** `CKPT0007`

## 2. Intended Use & Clinical Boundaries
- **Intended Domain:** Research multimodal clinical decision-support for early CVD risk stratification (`DS0001–DS0004`).
- **Out-of-Scope Use:** Autonomous clinical diagnosis or emergency rule-out without qualified physician adjudication (`DEC0005` / `DEC0010`).
- **Known Limitations:** Sequential temporal comparator fulfilling proposal LSTM

## 3. Inputs & Modality Policy
- **Modalities Handled:** `ECG WFDB (12, 5000/1000)`
- **Missing-Modality Handling:** `ECG-only (DS0001)` (`ZERO` cross-cohort patient stitching per `DEC0004`/`DEC0006`).

## 4. Validation Performance & Frozen Calibration Summary (`Test = SEALED_UNTIL_G11`)
| Cohort | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp (T) | Tau_Youden | Tau_Sens85 |
|---|---|---|---|---|---|---|---|---|
| `DS0001` | `0.937422` | `0.957955` | `0.874029` | `0.097891` | `0.023828` | `1.35` | `0.52` | `0.44` |
