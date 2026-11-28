# EXP0012 — EarlyConcat_XGB_MLP (`Block_C`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0012` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | **`COMPLETED`** (`STEP-029/030` Kaggle CUDA Validation Audited; Test Remains Sealed) |
| source_inputs | `REL0001` (`Train/Val` Only — Test Sealed until `G11`) |
| governing_section | OS §6.2, §11, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe config & manifest) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Scientific Objective
- **Experiment ID:** `EXP0012`
- **Research Question:** `RQ1` | **Block:** `Block_C`
- **Comparator Tier:** `simple_fusion` | **Parent Baseline:** `EXP0004`
- **Active Modalities:** `clinical, ecg, laboratory, lifestyle` (`missing_modality_policy=zero_fill`)
- **Primary Hypothesis:** Early feature concatenation establishes non-attention multimodal fusion baseline.

## 2. Data & Model Setup
- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`)
- **Model Candidate:** `MC0012` (`EarlyConcat_XGB_MLP` / `xgboost`)
- **Config Path:** [config.yaml](./config.yaml)
- **Config SHA-256:** `22977558e6d785d07e61807ae1a25b9b6b869797b46c024dc27dc424836a36a4`
- **Source Git Commit:** `8994dea`

## 3. Pre-Launch Custody & Execution Targets
- **Canonical Primary Seed:** `20261127` (Block F expands across `[20261127..20261201]`)
- **Hardware Target:** `kaggle_t4_gpu` | **Tier 3 Artifact Path:** `08_Checkpoints/binaries/EXP0012`
- **Test Partition Status:** Strictly `SEALED_UNTIL_G11` (`0` Test reads permitted in Stage S11).
- **Execution Status:** Registered `READY` for `STEP-029` training launch via Kaggle GPU / CLI.


## 4. Observed Stage S11 Validation Outcomes (`REL0001` Val Only, `Test = 0` Reads)
- **Executed Git Revision:** `19249e5` (`CVD_Multimodal_Kaggle_Training_Pipeline.ipynb` on Kaggle CUDA GPU)
- **Saved Checkpoints:** `In-session deterministic fit (no .pt/.pkl serialized)`
- **Conclusion:** PASS Stage S11 Validation Executed (1 evaluated cohort slice(s), Test=0 reads)

| Cohort | Seed | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp | Tau_Youden |
|---|---|---|---|---|---|---|---|---|
| `ALL_COHORTS` | `20261127` | `0.830304` | `0.840651` | `0.742352` | `0.167526` | `0.018932` | `1.075` | `0.515` |
