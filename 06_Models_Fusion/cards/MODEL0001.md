# MODEL0001 — LogisticRegression (`MC0001`, Tabular_CLS_Logistic)

| Field | Value |
|---|---|
| TemplateID | T17 (model_card.md) |
| template_version | v1.0.0 |
| entity_id | `MODEL0001` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-28` |
| status | `G10_Audited_Comparator` |
| source_inputs | `REL0001` (`Train/Val` Only; `SPLIT0001`, `PP0001`, `FitStateHash=d9ccfbf40b2b...`) |
| governing_section | OS §6.3, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Model Overview
- **Model ID:** `MODEL0001` (`MC0001` — `Tier_1_Unimodal`)
- **Architecture:** L2 Regularized Linear Classifier (C tuned on Val) (`scikit-learn`)
- **Parameter / Artifact Budget:** `Non-serialized deterministic fit (seed=20261127)`
- **Primary Experiment:** `EXP0001`
- **Checkpoints (`G10` SHA-256 Verified):** `None (Deterministic CPU refit from EXP config)`

## 2. Intended Use & Clinical Boundaries
- **Intended Domain:** Research multimodal clinical decision-support for early CVD risk stratification (`DS0001–DS0004`).
- **Out-of-Scope Use:** Autonomous clinical diagnosis or emergency rule-out without qualified physician adjudication (`DEC0005` / `DEC0010`).
- **Known Limitations:** Linear only unless interaction terms added

## 3. Inputs & Modality Policy
- **Modalities Handled:** `Clinical; Lab; Lifestyle`
- **Missing-Modality Handling:** `Per-cohort schema` (`ZERO` cross-cohort patient stitching per `DEC0004`/`DEC0006`).

## 4. Validation Performance & Frozen Calibration Summary (`Test = SEALED_UNTIL_G11`)
| Cohort | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp (T) | Tau_Youden | Tau_Sens85 |
|---|---|---|---|---|---|---|---|---|
| `DS0001` | `0.761719` | `0.805238` | `0.740318` | `0.200566` | `0.075073` | `1.05` | `0.485` | `0.365` |
| `DS0002` | `0.724781` | `0.831570` | `0.619718` | `0.211773` | `0.175313` | `0.9` | `0.655` | `0.345` |
| `DS0003` | `0.811404` | `0.788888` | `0.729064` | `0.177863` | `0.134837` | `0.775` | `0.515` | `0.375` |
| `DS0004` | `0.791132` | `0.767259` | `0.727201` | `0.187469` | `0.038748` | `1.025` | `0.46` | `0.365` |
