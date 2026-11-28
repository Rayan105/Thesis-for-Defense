# MODEL0009 — CompactCNN2D_PNG (`MC0009`, DS0002_PNG_CNN2D)

| Field | Value |
|---|---|
| TemplateID | T17 (model_card.md) |
| template_version | v1.0.0 |
| entity_id | `MODEL0009` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-28` |
| status | `G10_Audited_Comparator` |
| source_inputs | `REL0001` (`Train/Val` Only; `SPLIT0001`, `PP0001`, `FitStateHash=d9ccfbf40b2b...`) |
| governing_section | OS §6.3, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Model Overview
- **Model ID:** `MODEL0009` (`MC0009` — `Tier_1_Unimodal`)
- **Architecture:** 4-Stage Depthwise Conv2D Stem (~62K params) (`PyTorch`)
- **Parameter / Artifact Budget:** `CompactCNN2DPNG Dual Max+Avg (~62K params; 231,369 B)`
- **Primary Experiment:** `EXP0009`
- **Checkpoints (`G10` SHA-256 Verified):** `CKPT0008`

## 2. Intended Use & Clinical Boundaries
- **Intended Domain:** Research multimodal clinical decision-support for early CVD risk stratification (`DS0001–DS0004`).
- **Out-of-Scope Use:** Autonomous clinical diagnosis or emergency rule-out without qualified physician adjudication (`DEC0005` / `DEC0010`).
- **Known Limitations:** EPV-safe capacity on N_train=231 paired PNGs

## 3. Inputs & Modality Policy
- **Modalities Handled:** `ECG PNG Scans (1, 256, 768)`
- **Missing-Modality Handling:** `ECG-only (DS0002 PNG)` (`ZERO` cross-cohort patient stitching per `DEC0004`/`DEC0006`).

## 4. Validation Performance & Frozen Calibration Summary (`Test = SEALED_UNTIL_G11`)
| Cohort | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp (T) | Tau_Youden | Tau_Sens85 |
|---|---|---|---|---|---|---|---|---|
| `DS0002` | `0.548611` | `0.716358` | `0.171429` | `0.256536` | `0.236816` | `3.0` | `0.48` | `0.05` |
