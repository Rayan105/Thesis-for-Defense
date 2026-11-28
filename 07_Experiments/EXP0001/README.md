# EXP0001 — LogisticRegression_Balanced (`Block_A`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0001` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | **`COMPLETED`** (`STEP-029/030` Kaggle CUDA Validation Audited; Test Remains Sealed) |
| source_inputs | `REL0001` (`Train/Val` Only — Test Sealed until `G11`) |
| governing_section | OS §6.2, §11, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe config & manifest) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Scientific Objective
- **Experiment ID:** `EXP0001`
- **Research Question:** `RQ1` | **Block:** `Block_A`
- **Comparator Tier:** `unimodal` | **Parent Baseline:** `None`
- **Active Modalities:** `clinical, laboratory, lifestyle` (`missing_modality_policy=indicator`)
- **Primary Hypothesis:** C=1.0 L2 Logistic baseline on Train-scaled [C,L,S] features.

## 2. Data & Model Setup
- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`)
- **Model Candidate:** `MC0001` (`LogisticRegression_Balanced` / `sklearn`)
- **Config Path:** [config.yaml](./config.yaml)
- **Config SHA-256:** `9ec88cf6ddf7171862888484bdde1c3f242b8a7f806985623fd720a57dcaa9de`
- **Source Git Commit:** `8994dea`

## 3. Pre-Launch Custody & Execution Targets
- **Canonical Primary Seed:** `20261127` (Block F expands across `[20261127..20261201]`)
- **Hardware Target:** `kaggle_cpu_or_t4` | **Tier 3 Artifact Path:** `08_Checkpoints/binaries/EXP0001`
- **Test Partition Status:** Strictly `SEALED_UNTIL_G11` (`0` Test reads permitted in Stage S11).
- **Execution Status:** Registered `READY` for `STEP-029` training launch via Kaggle GPU / CLI.


## 4. Observed Stage S11 Validation Outcomes (`REL0001` Val Only, `Test = 0` Reads)
- **Executed Git Revision:** `19249e5` (`CVD_Multimodal_Kaggle_Training_Pipeline.ipynb` on Kaggle CUDA GPU)
- **Saved Checkpoints:** `In-session deterministic fit (no .pt/.pkl serialized)`
- **Conclusion:** PASS Stage S11 Validation Executed (4 evaluated cohort slice(s), Test=0 reads)

| Cohort | Seed | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp | Tau_Youden |
|---|---|---|---|---|---|---|---|---|
| `DS0001` | `20261127` | `0.761719` | `0.805238` | `0.740318` | `0.200566` | `0.075073` | `1.05` | `0.485` |
| `DS0002` | `20261127` | `0.724781` | `0.831570` | `0.619718` | `0.211773` | `0.175313` | `0.9` | `0.655` |
| `DS0003` | `20261127` | `0.811404` | `0.788888` | `0.729064` | `0.177863` | `0.134837` | `0.775` | `0.515` |
| `DS0004` | `20261127` | `0.791132` | `0.767259` | `0.727201` | `0.187469` | `0.038748` | `1.025` | `0.46` |
