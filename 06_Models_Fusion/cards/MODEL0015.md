# MODEL0015 — CVD_MM_Transformer (`MC0015`, Proposed_CVDMMTransformer)

| Field | Value |
|---|---|
| TemplateID | T17 (model_card.md) |
| template_version | v1.0.0 |
| entity_id | `MODEL0015` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-28` |
| status | `Champion_Frozen_G11_Candidate` |
| source_inputs | `REL0001` (`Train/Val` Only; `SPLIT0001`, `PP0001`, `FitStateHash=d9ccfbf40b2b...`) |
| governing_section | OS §6.3, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Model Overview
- **Model ID:** `MODEL0015` (`MC0015` — `Tier_4_Proposed_Fusion`)
- **Architecture:** Modality Adapters + Dual ResNet1D/Conv2D + 2L/4H Cross-Modal Transformer (d=64, <250K) (`PyTorch`)
- **Parameter / Artifact Budget:** `266587`
- **Primary Experiment:** `EXP0015` & `EXP0020` (5 seeds + stress)
- **Checkpoints (`G10` SHA-256 Verified):** `CKPT0011; CKPT0013; CKPT0014; CKPT0015; CKPT0016`

## 2. Intended Use & Clinical Boundaries
- **Intended Domain:** Research multimodal clinical decision-support for early CVD risk stratification (`DS0001–DS0004`).
- **Out-of-Scope Use:** Autonomous clinical diagnosis or emergency rule-out without qualified physician adjudication (`DEC0005` / `DEC0010`).
- **Known Limitations:** Requires careful regularization on N_train=390 DS0002

## 3. Inputs & Modality Policy
- **Modalities Handled:** `Clinical+ECG(1D/2D)+Lab+Lifestyle`
- **Missing-Modality Handling:** `Native ~ModalityMask_CELS key_padding_mask` (`ZERO` cross-cohort patient stitching per `DEC0004`/`DEC0006`).

## 4. Validation Performance & Frozen Calibration Summary (`Test = SEALED_UNTIL_G11`)
| Cohort | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp (T) | Tau_Youden | Tau_Sens85 |
|---|---|---|---|---|---|---|---|---|
| `ALL_COHORTS` | `0.823691` | `0.835141` | `0.748990` | `0.170535` | `0.016904` | `1.2` | `0.48` | `0.36` |
| `DS0001` | `0.933255` | `0.955011` | `0.867295` | `0.109070` | `0.072693` | `1.475` | `0.405` | `0.355` |
| `DS0002` | `0.735277` | `0.812470` | `0.666667` | `0.208410` | `0.142264` | `1.425` | `0.52` | `0.365` |
| `DS0003` | `0.799679` | `0.805265` | `0.684783` | `0.186603` | `0.101137` | `1.075` | `0.66` | `0.405` |
| `DS0004` | `0.799192` | `0.781431` | `0.727435` | `0.182031` | `0.018970` | `1.125` | `0.475` | `0.355` |
