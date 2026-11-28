# MODEL0005 — LightGBM (`MC0005`, Tabular_CLS_LightGBM)

| Field | Value |
|---|---|
| TemplateID | T17 (model_card.md) |
| template_version | v1.0.0 |
| entity_id | `MODEL0005` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-28` |
| status | `G10_Audited_Comparator` |
| source_inputs | `REL0001` (`Train/Val` Only; `SPLIT0001`, `PP0001`, `FitStateHash=d9ccfbf40b2b...`) |
| governing_section | OS §6.3, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Model Overview
- **Model ID:** `MODEL0005` (`MC0005` — `Tier_1_Unimodal`)
- **Architecture:** Histogram GBDT Comparator (`lightgbm`)
- **Parameter / Artifact Budget:** `Non-serialized deterministic fit (seed=20261127)`
- **Primary Experiment:** `EXP0005`
- **Checkpoints (`G10` SHA-256 Verified):** `None (Deterministic CPU refit from EXP config)`

## 2. Intended Use & Clinical Boundaries
- **Intended Domain:** Research multimodal clinical decision-support for early CVD risk stratification (`DS0001–DS0004`).
- **Out-of-Scope Use:** Autonomous clinical diagnosis or emergency rule-out without qualified physician adjudication (`DEC0005` / `DEC0010`).
- **Known Limitations:** Optional tabular GBDT sensitivity check

## 3. Inputs & Modality Policy
- **Modalities Handled:** `Clinical; Lab; Lifestyle`
- **Missing-Modality Handling:** `Native NaN + MNAR _isnan` (`ZERO` cross-cohort patient stitching per `DEC0004`/`DEC0006`).

## 4. Validation Performance & Frozen Calibration Summary (`Test = SEALED_UNTIL_G11`)
| Cohort | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp (T) | Tau_Youden | Tau_Sens85 |
|---|---|---|---|---|---|---|---|---|
| `DS0001` | `0.754176` | `0.788339` | `0.751969` | `0.204505` | `0.080371` | `1.125` | `0.435` | `0.36` |
| `DS0002` | `0.674052` | `0.754419` | `0.689655` | `0.227003` | `0.146263` | `1.625` | `0.56` | `0.355` |
| `DS0003` | `0.831478` | `0.831454` | `0.732984` | `0.167052` | `0.051565` | `0.8` | `0.58` | `0.35` |
| `DS0004` | `0.802538` | `0.784614` | `0.725496` | `0.180048` | `0.013085` | `0.975` | `0.49` | `0.325` |
