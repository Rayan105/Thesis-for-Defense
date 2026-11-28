# MODEL0011 — ClinicalRiskScore_WHO_FRS (`MC0011`, ClinicalScore_WHO_FRS)

| Field | Value |
|---|---|
| TemplateID | T17 (model_card.md) |
| template_version | v1.0.0 |
| entity_id | `MODEL0011` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-28` |
| status | `G10_Audited_Comparator` |
| source_inputs | `REL0001` (`Train/Val` Only; `SPLIT0001`, `PP0001`, `FitStateHash=d9ccfbf40b2b...`) |
| governing_section | OS §6.3, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Model Overview
- **Model ID:** `MODEL0011` (`MC0011` — `Tier_2_Clinical_Score`)
- **Architecture:** WHO South Asia / Framingham Compatible Covariate Index (`Custom/Stat`)
- **Parameter / Artifact Budget:** `4-covariate deterministic risk equation (0 learned weights)`
- **Primary Experiment:** `EXP0011`
- **Checkpoints (`G10` SHA-256 Verified):** `None (Deterministic CPU refit from EXP config)`

## 2. Intended Use & Clinical Boundaries
- **Intended Domain:** Research multimodal clinical decision-support for early CVD risk stratification (`DS0001–DS0004`).
- **Out-of-Scope Use:** Autonomous clinical diagnosis or emergency rule-out without qualified physician adjudication (`DEC0005` / `DEC0010`).
- **Known Limitations:** Cross-sectional horizon mismatch; discrimination context only

## 3. Inputs & Modality Policy
- **Modalities Handled:** `Age; Sex; SBP; TC/HDL/Chol; Smoke; DM`
- **Missing-Modality Handling:** `Incompatible without Labs/C` (`ZERO` cross-cohort patient stitching per `DEC0004`/`DEC0006`).

## 4. Validation Performance & Frozen Calibration Summary (`Test = SEALED_UNTIL_G11`)
| Cohort | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp (T) | Tau_Youden | Tau_Sens85 |
|---|---|---|---|---|---|---|---|---|
| `DS0003` | `0.500422` | `0.474757` | `0.548673` | `0.250918` | `0.117382` | `3.0` | `0.465` | `0.43` |
| `DS0004` | `0.648564` | `0.623121` | `0.571398` | `0.236726` | `0.053225` | `1.2` | `0.46` | `0.365` |
