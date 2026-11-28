# MODEL0012 — EarlyConcat_XGB_MLP (`MC0012`, SimpleFusion_EarlyConcat_XGB)

| Field | Value |
|---|---|
| TemplateID | T17 (model_card.md) |
| template_version | v1.0.0 |
| entity_id | `MODEL0012` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-28` |
| status | `G10_Audited_Comparator` |
| source_inputs | `REL0001` (`Train/Val` Only; `SPLIT0001`, `PP0001`, `FitStateHash=d9ccfbf40b2b...`) |
| governing_section | OS §6.3, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Model Overview
- **Model ID:** `MODEL0012` (`MC0012` — `Tier_3_Simple_Fusion`)
- **Architecture:** Concat([C, L, S] + Frozen/Joint ECG Emb) -> XGB & MLP (`PyTorch+XGBoost`)
- **Parameter / Artifact Budget:** `XGBoost over C+L+S+64D frozen ECG embedding`
- **Primary Experiment:** `EXP0012`
- **Checkpoints (`G10` SHA-256 Verified):** `None (Deterministic CPU refit from EXP config)`

## 2. Intended Use & Clinical Boundaries
- **Intended Domain:** Research multimodal clinical decision-support for early CVD risk stratification (`DS0001–DS0004`).
- **Out-of-Scope Use:** Autonomous clinical diagnosis or emergency rule-out without qualified physician adjudication (`DEC0005` / `DEC0010`).
- **Known Limitations:** Requires Q1 baseline comparison before claiming attention gain

## 3. Inputs & Modality Policy
- **Modalities Handled:** `All Present Cohort Inputs`
- **Missing-Modality Handling:** `Zero-pad absent ECG emb` (`ZERO` cross-cohort patient stitching per `DEC0004`/`DEC0006`).

## 4. Validation Performance & Frozen Calibration Summary (`Test = SEALED_UNTIL_G11`)
| Cohort | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp (T) | Tau_Youden | Tau_Sens85 |
|---|---|---|---|---|---|---|---|---|
| `ALL_COHORTS` | `0.830304` | `0.840651` | `0.742352` | `0.167526` | `0.018932` | `1.075` | `0.515` | `0.335` |
