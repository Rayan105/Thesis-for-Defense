# MODEL0003 — SVM_RBF (`MC0003`, Tabular_CLS_SVM_RBF)

| Field | Value |
|---|---|
| TemplateID | T17 (model_card.md) |
| template_version | v1.0.0 |
| entity_id | `MODEL0003` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-28` |
| status | `G10_Audited_Comparator` |
| source_inputs | `REL0001` (`Train/Val` Only; `SPLIT0001`, `PP0001`, `FitStateHash=d9ccfbf40b2b...`) |
| governing_section | OS §6.3, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Model Overview
- **Model ID:** `MODEL0003` (`MC0003` — `Tier_1_Unimodal`)
- **Architecture:** RBF Kernel SVC + Validation Platt Sigmoid (`scikit-learn`)
- **Parameter / Artifact Budget:** `Non-serialized deterministic fit (seed=20261127)`
- **Primary Experiment:** `EXP0003`
- **Checkpoints (`G10` SHA-256 Verified):** `None (Deterministic CPU refit from EXP config)`

## 2. Intended Use & Clinical Boundaries
- **Intended Domain:** Research multimodal clinical decision-support for early CVD risk stratification (`DS0001–DS0004`).
- **Out-of-Scope Use:** Autonomous clinical diagnosis or emergency rule-out without qualified physician adjudication (`DEC0005` / `DEC0010`).
- **Known Limitations:** Quadratic runtime scaling on DS0004 (68K); use Nystroem/bagging if slow

## 3. Inputs & Modality Policy
- **Modalities Handled:** `Clinical; Lab; Lifestyle`
- **Missing-Modality Handling:** `Per-cohort schema` (`ZERO` cross-cohort patient stitching per `DEC0004`/`DEC0006`).

## 4. Validation Performance & Frozen Calibration Summary (`Test = SEALED_UNTIL_G11`)
| Cohort | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp (T) | Tau_Youden | Tau_Sens85 |
|---|---|---|---|---|---|---|---|---|
| `DS0001` | `0.733360` | `0.764760` | `0.749702` | `0.205800` | `0.050973` | `1.075` | `0.46` | `0.32` |
| `DS0002` | `0.685714` | `0.782539` | `0.484848` | `0.217504` | `0.113360` | `0.775` | `0.735` | `0.45` |
| `DS0003` | `0.823549` | `0.830479` | `0.755760` | `0.171698` | `0.093269` | `0.825` | `0.4` | `0.3` |
| `DS0004` | `0.787800` | `0.767956` | `0.711157` | `0.186465` | `0.031474` | `0.975` | `0.53` | `0.275` |
