# MODEL0007 — ResNet1D_ECG (`MC0007`, DS0001_WFDB_ResNet1D_SE)

| Field | Value |
|---|---|
| TemplateID | T17 (model_card.md) |
| template_version | v1.0.0 |
| entity_id | `MODEL0007` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-28` |
| status | `G10_Audited_Comparator` |
| source_inputs | `REL0001` (`Train/Val` Only; `SPLIT0001`, `PP0001`, `FitStateHash=d9ccfbf40b2b...`) |
| governing_section | OS §6.3, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Model Overview
- **Model ID:** `MODEL0007` (`MC0007` — `Tier_1_Unimodal`)
- **Architecture:** Compact 3-Block ResNet-1D + SE Attention (~78K params) (`PyTorch`)
- **Parameter / Artifact Budget:** `CompactResNet1D (~78K params; 418,565 B)`
- **Primary Experiment:** `EXP0007`
- **Checkpoints (`G10` SHA-256 Verified):** `CKPT0006`

## 2. Intended Use & Clinical Boundaries
- **Intended Domain:** Research multimodal clinical decision-support for early CVD risk stratification (`DS0001–DS0004`).
- **Out-of-Scope Use:** Autonomous clinical diagnosis or emergency rule-out without qualified physician adjudication (`DEC0005` / `DEC0010`).
- **Known Limitations:** Handles digital WFDB waveforms cleanly

## 3. Inputs & Modality Policy
- **Modalities Handled:** `ECG WFDB (12, 5000/1000)`
- **Missing-Modality Handling:** `ECG-only (DS0001)` (`ZERO` cross-cohort patient stitching per `DEC0004`/`DEC0006`).

## 4. Validation Performance & Frozen Calibration Summary (`Test = SEALED_UNTIL_G11`)
| Cohort | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp (T) | Tau_Youden | Tau_Sens85 |
|---|---|---|---|---|---|---|---|---|
| `DS0001` | `0.934585` | `0.957120` | `0.867188` | `0.101334` | `0.036353` | `1.15` | `0.485` | `0.395` |
