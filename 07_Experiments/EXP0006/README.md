# EXP0006 — TabularModalityMLP_Unimodal (`Block_A`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0006` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | **`COMPLETED`** (`STEP-029/030` Kaggle CUDA Validation Audited; Test Remains Sealed) |
| source_inputs | `REL0001` (`Train/Val` Only — Test Sealed until `G11`) |
| governing_section | OS §6.2, §11, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe config & manifest) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Scientific Objective
- **Experiment ID:** `EXP0006`
- **Research Question:** `RQ1` | **Block:** `Block_A`
- **Comparator Tier:** `unimodal` | **Parent Baseline:** `EXP0004`
- **Active Modalities:** `clinical, laboratory, lifestyle` (`missing_modality_policy=indicator`)
- **Primary Hypothesis:** Compact neural tabular MLP matching CVDMMTransformer encoder depth.

## 2. Data & Model Setup
- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`)
- **Model Candidate:** `MC0006` (`TabularModalityMLP_Unimodal` / `pytorch`)
- **Config Path:** [config.yaml](./config.yaml)
- **Config SHA-256:** `11a976b3963db5b290856c1dc17af35904de5fedce3c0a10b98d7d9adf82c728`
- **Source Git Commit:** `8994dea`

## 3. Pre-Launch Custody & Execution Targets
- **Canonical Primary Seed:** `20261127` (Block F expands across `[20261127..20261201]`)
- **Hardware Target:** `kaggle_t4_gpu` | **Tier 3 Artifact Path:** `08_Checkpoints/binaries/EXP0006`
- **Test Partition Status:** Strictly `SEALED_UNTIL_G11` (`0` Test reads permitted in Stage S11).
- **Execution Status:** Registered `READY` for `STEP-029` training launch via Kaggle GPU / CLI.


## 4. Observed Stage S11 Validation Outcomes (`REL0001` Val Only, `Test = 0` Reads)
- **Executed Git Revision:** `19249e5` (`CVD_Multimodal_Kaggle_Training_Pipeline.ipynb` on Kaggle CUDA GPU)
- **Saved Checkpoints:** `In-session deterministic fit (no .pt/.pkl serialized)`
- **Conclusion:** PASS Stage S11 Validation Executed (4 evaluated cohort slice(s), Test=0 reads)

| Cohort | Seed | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp | Tau_Youden |
|---|---|---|---|---|---|---|---|---|
| `DS0001` | `20261127` | `0.761141` | `0.806719` | `0.740861` | `0.204646` | `0.087959` | `1.075` | `0.49` |
| `DS0002` | `20261127` | `0.632070` | `0.747522` | `0.393443` | `0.228755` | `0.152552` | `0.35` | `0.695` |
| `DS0003` | `20261127` | `0.809295` | `0.797723` | `0.750000` | `0.180778` | `0.090232` | `0.3` | `0.395` |
| `DS0004` | `20261127` | `0.801989` | `0.783322` | `0.727218` | `0.180411` | `0.009060` | `0.975` | `0.48` |
