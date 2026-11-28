# MODEL0013 — LateEnsemble_Stacking (`MC0013`, SimpleFusion_LateOOF_Stacking)

| Field | Value |
|---|---|
| TemplateID | T17 (model_card.md) |
| template_version | v1.0.0 |
| entity_id | `MODEL0013` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-28` |
| status | `G10_Audited_Comparator` |
| source_inputs | `REL0001` (`Train/Val` Only; `SPLIT0001`, `PP0001`, `FitStateHash=d9ccfbf40b2b...`) |
| governing_section | OS §6.3, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Model Overview
- **Model ID:** `MODEL0013` (`MC0013` — `Tier_3_Simple_Fusion`)
- **Architecture:** OOF Logistic Stacker Over Unimodal Probabilities (`scikit-learn`)
- **Parameter / Artifact Budget:** `6-dim Logistic Stacker over OOF XGB + ECG logits`
- **Primary Experiment:** `EXP0013`
- **Checkpoints (`G10` SHA-256 Verified):** `None (Deterministic CPU refit from EXP config)`

## 2. Intended Use & Clinical Boundaries
- **Intended Domain:** Research multimodal clinical decision-support for early CVD risk stratification (`DS0001–DS0004`).
- **Out-of-Scope Use:** Autonomous clinical diagnosis or emergency rule-out without qualified physician adjudication (`DEC0005` / `DEC0010`).
- **Known Limitations:** Zero cross-modal feature interaction by construction

## 3. Inputs & Modality Policy
- **Modalities Handled:** `C+E+L+S Prob Outputs`
- **Missing-Modality Handling:** `Available-branch reweighting` (`ZERO` cross-cohort patient stitching per `DEC0004`/`DEC0006`).

## 4. Validation Performance & Frozen Calibration Summary (`Test = SEALED_UNTIL_G11`)
| Cohort | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp (T) | Tau_Youden | Tau_Sens85 |
|---|---|---|---|---|---|---|---|---|
| `ALL_COHORTS` | `0.827367` | `0.837537` | `0.745958` | `0.168936` | `0.020825` | `1.025` | `0.485` | `0.335` |
