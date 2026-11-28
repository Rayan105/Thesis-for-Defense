# EXP0003 — SVM_RBF_Balanced (`Block_A`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0003` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | **`COMPLETED`** (`STEP-029/030` Kaggle CUDA Validation Audited; Test Remains Sealed) |
| source_inputs | `REL0001` (`Train/Val` Only — Test Sealed until `G11`) |
| governing_section | OS §6.2, §11, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe config & manifest) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Scientific Objective
- **Experiment ID:** `EXP0003`
- **Research Question:** `RQ1` | **Block:** `Block_A`
- **Comparator Tier:** `unimodal` | **Parent Baseline:** `EXP0001`
- **Active Modalities:** `clinical, laboratory, lifestyle` (`missing_modality_policy=indicator`)
- **Primary Hypothesis:** RBF Kernel SVM (N<=15K subset/cohort CV) tests smooth margin classification.

## 2. Data & Model Setup
- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`)
- **Model Candidate:** `MC0003` (`SVM_RBF_Balanced` / `sklearn`)
- **Config Path:** [config.yaml](./config.yaml)
- **Config SHA-256:** `e30dd019a14a01fb3789df5b470211258d3675d72fa1ba13a5a809731b122fdf`
- **Source Git Commit:** `8994dea`

## 3. Pre-Launch Custody & Execution Targets
- **Canonical Primary Seed:** `20261127` (Block F expands across `[20261127..20261201]`)
- **Hardware Target:** `kaggle_cpu_or_t4` | **Tier 3 Artifact Path:** `08_Checkpoints/binaries/EXP0003`
- **Test Partition Status:** Strictly `SEALED_UNTIL_G11` (`0` Test reads permitted in Stage S11).
- **Execution Status:** Registered `READY` for `STEP-029` training launch via Kaggle GPU / CLI.


## 4. Observed Stage S11 Validation Outcomes (`REL0001` Val Only, `Test = 0` Reads)
- **Executed Git Revision:** `19249e5` (`CVD_Multimodal_Kaggle_Training_Pipeline.ipynb` on Kaggle CUDA GPU)
- **Saved Checkpoints:** `In-session deterministic fit (no .pt/.pkl serialized)`
- **Conclusion:** PASS Stage S11 Validation Executed (4 evaluated cohort slice(s), Test=0 reads)

| Cohort | Seed | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp | Tau_Youden |
|---|---|---|---|---|---|---|---|---|
| `DS0001` | `20261127` | `0.733360` | `0.764760` | `0.749702` | `0.205800` | `0.050973` | `1.075` | `0.46` |
| `DS0002` | `20261127` | `0.685714` | `0.782539` | `0.484848` | `0.217504` | `0.113360` | `0.775` | `0.735` |
| `DS0003` | `20261127` | `0.823549` | `0.830479` | `0.755760` | `0.171698` | `0.093269` | `0.825` | `0.4` |
| `DS0004` | `20261127` | `0.787800` | `0.767956` | `0.711157` | `0.186465` | `0.031474` | `0.975` | `0.53` |
