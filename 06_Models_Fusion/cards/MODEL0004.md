# MODEL0004 — XGBoost (`MC0004`, Tabular_CLS_XGBoost)

| Field | Value |
|---|---|
| TemplateID | T17 (model_card.md) |
| template_version | v1.0.0 |
| entity_id | `MODEL0004` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-28` |
| status | `G10_Audited_Comparator` |
| source_inputs | `REL0001` (`Train/Val` Only; `SPLIT0001`, `PP0001`, `FitStateHash=d9ccfbf40b2b...`) |
| governing_section | OS §6.3, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Model Overview
- **Model ID:** `MODEL0004` (`MC0004` — `Tier_1_Unimodal`)
- **Architecture:** Gradient Boosted Trees (scale_pos_weight, TreeSHAP) (`xgboost`)
- **Parameter / Artifact Budget:** `232KB-245KB XGBoost JSON/Pickle (~400 trees max)`
- **Primary Experiment:** `EXP0004`
- **Checkpoints (`G10` SHA-256 Verified):** `CKPT0002; CKPT0003; CKPT0004; CKPT0005`

## 2. Intended Use & Clinical Boundaries
- **Intended Domain:** Research multimodal clinical decision-support for early CVD risk stratification (`DS0001–DS0004`).
- **Out-of-Scope Use:** Autonomous clinical diagnosis or emergency rule-out without qualified physician adjudication (`DEC0005` / `DEC0010`).
- **Known Limitations:** Tabular only unless paired with ECG embeddings

## 3. Inputs & Modality Policy
- **Modalities Handled:** `Clinical; Lab; Lifestyle`
- **Missing-Modality Handling:** `Native NaN + MNAR _isnan` (`ZERO` cross-cohort patient stitching per `DEC0004`/`DEC0006`).

## 4. Validation Performance & Frozen Calibration Summary (`Test = SEALED_UNTIL_G11`)
| Cohort | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp (T) | Tau_Youden | Tau_Sens85 |
|---|---|---|---|---|---|---|---|---|
| `DS0001` | `0.756332` | `0.794546` | `0.749103` | `0.203281` | `0.086246` | `1.1` | `0.465` | `0.36` |
| `DS0002` | `0.697959` | `0.790553` | `0.682353` | `0.220754` | `0.159188` | `1.3` | `0.57` | `0.345` |
| `DS0003` | `0.835948` | `0.836446` | `0.758294` | `0.165640` | `0.066954` | `0.725` | `0.49` | `0.385` |
| `DS0004` | `0.802356` | `0.781511` | `0.719271` | `0.180194` | `0.012176` | `0.975` | `0.505` | `0.33` |
