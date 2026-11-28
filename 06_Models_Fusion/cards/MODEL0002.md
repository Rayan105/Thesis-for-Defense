# MODEL0002 — RandomForest (`MC0002`, Tabular_CLS_RandomForest)

| Field | Value |
|---|---|
| TemplateID | T17 (model_card.md) |
| template_version | v1.0.0 |
| entity_id | `MODEL0002` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-28` |
| status | `G10_Audited_Comparator` |
| source_inputs | `REL0001` (`Train/Val` Only; `SPLIT0001`, `PP0001`, `FitStateHash=d9ccfbf40b2b...`) |
| governing_section | OS §6.3, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Model Overview
- **Model ID:** `MODEL0002` (`MC0002` — `Tier_1_Unimodal`)
- **Architecture:** 300-Tree Bagged Ensemble (class_weight balanced) (`scikit-learn`)
- **Parameter / Artifact Budget:** `Non-serialized deterministic fit (seed=20261127)`
- **Primary Experiment:** `EXP0002`
- **Checkpoints (`G10` SHA-256 Verified):** `None (Deterministic CPU refit from EXP config)`

## 2. Intended Use & Clinical Boundaries
- **Intended Domain:** Research multimodal clinical decision-support for early CVD risk stratification (`DS0001–DS0004`).
- **Out-of-Scope Use:** Autonomous clinical diagnosis or emergency rule-out without qualified physician adjudication (`DEC0005` / `DEC0010`).
- **Known Limitations:** Calibration drift on extreme prevalence without isotonic/Platt

## 3. Inputs & Modality Policy
- **Modalities Handled:** `Clinical; Lab; Lifestyle`
- **Missing-Modality Handling:** `Per-cohort + TreeSHAP` (`ZERO` cross-cohort patient stitching per `DEC0004`/`DEC0006`).

## 4. Validation Performance & Frozen Calibration Summary (`Test = SEALED_UNTIL_G11`)
| Cohort | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp (T) | Tau_Youden | Tau_Sens85 |
|---|---|---|---|---|---|---|---|---|
| `DS0001` | `0.746127` | `0.777678` | `0.738687` | `0.205373` | `0.080551` | `1.1` | `0.49` | `0.345` |
| `DS0002` | `0.676968` | `0.781298` | `0.542857` | `0.217281` | `0.150710` | `0.9` | `0.68` | `0.41` |
| `DS0003` | `0.852311` | `0.855270` | `0.762376` | `0.156468` | `0.079544` | `0.4` | `0.455` | `0.305` |
| `DS0004` | `0.799660` | `0.778419` | `0.725960` | `0.181519` | `0.015506` | `0.975` | `0.47` | `0.33` |
