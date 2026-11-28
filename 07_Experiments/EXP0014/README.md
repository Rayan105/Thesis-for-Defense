# EXP0014 — GatedAttentionFusionNet (`Block_C`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0014` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | **`COMPLETED`** (`STEP-029/030` Kaggle CUDA Validation Audited; Test Remains Sealed) |
| source_inputs | `REL0001` (`Train/Val` Only — Test Sealed until `G11`) |
| governing_section | OS §6.2, §11, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe config & manifest) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Scientific Objective
- **Experiment ID:** `EXP0014`
- **Research Question:** `RQ1` | **Block:** `Block_C`
- **Comparator Tier:** `simple_fusion` | **Parent Baseline:** `EXP0013`
- **Active Modalities:** `clinical, ecg, laboratory, lifestyle` (`missing_modality_policy=key_padding_mask`)
- **Primary Hypothesis:** Sigmoid gated fusion compares scalar attention weighting against multi-head Transformer fusion.

## 2. Data & Model Setup
- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`)
- **Model Candidate:** `MC0014` (`GatedAttentionFusionNet` / `pytorch`)
- **Config Path:** [config.yaml](./config.yaml)
- **Config SHA-256:** `7f89affe0ec120f53442299464a35e4f3651f96d6b92c13bc9691be52aa35428`
- **Source Git Commit:** `8994dea`

## 3. Pre-Launch Custody & Execution Targets
- **Canonical Primary Seed:** `20261127` (Block F expands across `[20261127..20261201]`)
- **Hardware Target:** `kaggle_t4_gpu` | **Tier 3 Artifact Path:** `08_Checkpoints/binaries/EXP0014`
- **Test Partition Status:** Strictly `SEALED_UNTIL_G11` (`0` Test reads permitted in Stage S11).
- **Execution Status:** Registered `READY` for `STEP-029` training launch via Kaggle GPU / CLI.


## 4. Observed Stage S11 Validation Outcomes (`REL0001` Val Only, `Test = 0` Reads)
- **Executed Git Revision:** `19249e5` (`CVD_Multimodal_Kaggle_Training_Pipeline.ipynb` on Kaggle CUDA GPU)
- **Saved Checkpoints:** `CKPT0010`
- **Conclusion:** PASS Stage S11 Validation Executed (5 evaluated cohort slice(s), Test=0 reads)

| Cohort | Seed | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp | Tau_Youden |
|---|---|---|---|---|---|---|---|---|
| `ALL_COHORTS` | `20261127` | `0.826350` | `0.836795` | `0.746393` | `0.169738` | `0.027732` | `1.1` | `0.51` |
| `DS0001` | `20261127` | `0.933613` | `0.956884` | `0.872900` | `0.106296` | `0.065490` | `1.575` | `0.45` |
| `DS0002` | `20261127` | `0.681050` | `0.795072` | `0.666667` | `0.236524` | `0.155730` | `3.0` | `0.78` |
| `DS0003` | `20261127` | `0.824899` | `0.835169` | `0.697674` | `0.167541` | `0.070651` | `1.025` | `0.64` |
| `DS0004` | `20261127` | `0.802502` | `0.784417` | `0.728112` | `0.180527` | `0.020111` | `0.95` | `0.485` |
