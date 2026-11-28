# MODEL0010 — ECGPatchTransformer (`MC0010`, DS0001_WFDB_ECGPatchTransformer)

| Field | Value |
|---|---|
| TemplateID | T17 (model_card.md) |
| template_version | v1.0.0 |
| entity_id | `MODEL0010` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-28` |
| status | `G10_Audited_Comparator` |
| source_inputs | `REL0001` (`Train/Val` Only; `SPLIT0001`, `PP0001`, `FitStateHash=d9ccfbf40b2b...`) |
| governing_section | OS §6.3, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Model Overview
- **Model ID:** `MODEL0010` (`MC0010` — `Tier_1_Unimodal`)
- **Architecture:** Conv Stem + 2-Layer 4-Head Self-Attention (d=64) (`PyTorch`)
- **Parameter / Artifact Budget:** `ECGPatchTransformer (~70K params; 355,516 B)`
- **Primary Experiment:** `EXP0010`
- **Checkpoints (`G10` SHA-256 Verified):** `CKPT0009`

## 2. Intended Use & Clinical Boundaries
- **Intended Domain:** Research multimodal clinical decision-support for early CVD risk stratification (`DS0001–DS0004`).
- **Out-of-Scope Use:** Autonomous clinical diagnosis or emergency rule-out without qualified physician adjudication (`DEC0005` / `DEC0010`).
- **Known Limitations:** Isolates Transformer ECG self-attention from cross-modal fusion

## 3. Inputs & Modality Policy
- **Modalities Handled:** `ECG WFDB / PNG Tokens`
- **Missing-Modality Handling:** `ECG-only` (`ZERO` cross-cohort patient stitching per `DEC0004`/`DEC0006`).

## 4. Validation Performance & Frozen Calibration Summary (`Test = SEALED_UNTIL_G11`)
| Cohort | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp (T) | Tau_Youden | Tau_Sens85 |
|---|---|---|---|---|---|---|---|---|
| `DS0001` | `0.923228` | `0.947794` | `0.859227` | `0.110071` | `0.020789` | `1.375` | `0.52` | `0.43` |
