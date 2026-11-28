# MODEL0006 — TabularMLP (`MC0006`, Tabular_CLS_MLP)

| Field | Value |
|---|---|
| TemplateID | T17 (model_card.md) |
| template_version | v1.0.0 |
| entity_id | `MODEL0006` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-28` |
| status | `G10_Audited_Comparator` |
| source_inputs | `REL0001` (`Train/Val` Only; `SPLIT0001`, `PP0001`, `FitStateHash=d9ccfbf40b2b...`) |
| governing_section | OS §6.3, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Model Overview
- **Model ID:** `MODEL0006` (`MC0006` — `Tier_1_Unimodal`)
- **Architecture:** Compact 2-Layer MLP (64->32->1, LayerNorm+Dropout 0.3) (`PyTorch`)
- **Parameter / Artifact Budget:** `Compact PyTorch 2-Layer MLP`
- **Primary Experiment:** `EXP0006`
- **Checkpoints (`G10` SHA-256 Verified):** `None (Deterministic CPU refit from EXP config)`

## 2. Intended Use & Clinical Boundaries
- **Intended Domain:** Research multimodal clinical decision-support for early CVD risk stratification (`DS0001–DS0004`).
- **Out-of-Scope Use:** Autonomous clinical diagnosis or emergency rule-out without qualified physician adjudication (`DEC0005` / `DEC0010`).
- **Known Limitations:** Measures neural vs GBDT tabular gap

## 3. Inputs & Modality Policy
- **Modalities Handled:** `Clinical; Lab; Lifestyle`
- **Missing-Modality Handling:** `Exact tabular tokenizer parity` (`ZERO` cross-cohort patient stitching per `DEC0004`/`DEC0006`).

## 4. Validation Performance & Frozen Calibration Summary (`Test = SEALED_UNTIL_G11`)
| Cohort | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp (T) | Tau_Youden | Tau_Sens85 |
|---|---|---|---|---|---|---|---|---|
| `DS0001` | `0.761141` | `0.806719` | `0.740861` | `0.204646` | `0.087959` | `1.075` | `0.49` | `0.345` |
| `DS0002` | `0.632070` | `0.747522` | `0.393443` | `0.228755` | `0.152552` | `0.35` | `0.695` | `0.35` |
| `DS0003` | `0.809295` | `0.797723` | `0.750000` | `0.180778` | `0.090232` | `0.3` | `0.395` | `0.315` |
| `DS0004` | `0.801989` | `0.783322` | `0.727218` | `0.180411` | `0.009060` | `0.975` | `0.48` | `0.33` |
