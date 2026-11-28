# MODEL0014 — GatedAttentionFusion (`MC0014`, SimpleFusion_GatedAttention)

| Field | Value |
|---|---|
| TemplateID | T17 (model_card.md) |
| template_version | v1.0.0 |
| entity_id | `MODEL0014` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-28` |
| status | `G10_Audited_Comparator` |
| source_inputs | `REL0001` (`Train/Val` Only; `SPLIT0001`, `PP0001`, `FitStateHash=d9ccfbf40b2b...`) |
| governing_section | OS §6.3, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Model Overview
- **Model ID:** `MODEL0014` (`MC0014` — `Tier_3_Simple_Fusion`)
- **Architecture:** Per-Modality Linear Proj + Sigmoid Gating Weights (alpha_m) (`PyTorch`)
- **Parameter / Artifact Budget:** `201756`
- **Primary Experiment:** `EXP0014`
- **Checkpoints (`G10` SHA-256 Verified):** `CKPT0010`

## 2. Intended Use & Clinical Boundaries
- **Intended Domain:** Research multimodal clinical decision-support for early CVD risk stratification (`DS0001–DS0004`).
- **Out-of-Scope Use:** Autonomous clinical diagnosis or emergency rule-out without qualified physician adjudication (`DEC0005` / `DEC0010`).
- **Known Limitations:** Tests gating without multi-head cross-attention

## 3. Inputs & Modality Policy
- **Modalities Handled:** `Clinical; ECG; Lab; Lifestyle`
- **Missing-Modality Handling:** `Mask gated weight alpha=0` (`ZERO` cross-cohort patient stitching per `DEC0004`/`DEC0006`).

## 4. Validation Performance & Frozen Calibration Summary (`Test = SEALED_UNTIL_G11`)
| Cohort | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp (T) | Tau_Youden | Tau_Sens85 |
|---|---|---|---|---|---|---|---|---|
| `ALL_COHORTS` | `0.826350` | `0.836795` | `0.746393` | `0.169738` | `0.027732` | `1.1` | `0.51` | `0.37` |
| `DS0001` | `0.933613` | `0.956884` | `0.872900` | `0.106296` | `0.065490` | `1.575` | `0.45` | `0.38` |
| `DS0002` | `0.681050` | `0.795072` | `0.666667` | `0.236524` | `0.155730` | `3.0` | `0.78` | `0.425` |
| `DS0003` | `0.824899` | `0.835169` | `0.697674` | `0.167541` | `0.070651` | `1.025` | `0.64` | `0.315` |
| `DS0004` | `0.802502` | `0.784417` | `0.728112` | `0.180527` | `0.020111` | `0.95` | `0.485` | `0.35` |
