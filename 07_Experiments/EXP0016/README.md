# EXP0016 — ProgressiveModalGain_CLS (`Block_D`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0016` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | **`COMPLETED`** (`STEP-029/030` Kaggle CUDA Validation Audited; Test Remains Sealed) |
| source_inputs | `REL0001` (`Train/Val` Only — Test Sealed until `G11`) |
| governing_section | OS §6.2, §11, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe config & manifest) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Scientific Objective
- **Experiment ID:** `EXP0016`
- **Research Question:** `RQ2` | **Block:** `Block_D`
- **Comparator Tier:** `ablation` | **Parent Baseline:** `EXP0004`
- **Active Modalities:** `clinical, ecg, laboratory, lifestyle` (`missing_modality_policy=indicator`)
- **Primary Hypothesis:** Adding Laboratory (L) and Structured Lifestyle (S) yields significant incremental AUROC & Net Benefit.

## 2. Data & Model Setup
- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`)
- **Model Candidate:** `MC0004` (`ProgressiveModalGain_CLS` / `xgboost`)
- **Config Path:** [config.yaml](./config.yaml)
- **Config SHA-256:** `b790d195613647c4725e130cf54ee666343bcd6bd87d4d115e5c7456c551c1a8`
- **Source Git Commit:** `8994dea`

## 3. Pre-Launch Custody & Execution Targets
- **Canonical Primary Seed:** `20261127` (Block F expands across `[20261127..20261201]`)
- **Hardware Target:** `kaggle_t4_gpu` | **Tier 3 Artifact Path:** `08_Checkpoints/binaries/EXP0016`
- **Test Partition Status:** Strictly `SEALED_UNTIL_G11` (`0` Test reads permitted in Stage S11).
- **Execution Status:** Registered `READY` for `STEP-029` training launch via Kaggle GPU / CLI.


## 4. Observed Stage S11 Validation Outcomes (`REL0001` Val Only, `Test = 0` Reads)
- **Executed Git Revision:** `19249e5` (`CVD_Multimodal_Kaggle_Training_Pipeline.ipynb` on Kaggle CUDA GPU)
- **Saved Checkpoints:** `In-session deterministic fit (no .pt/.pkl serialized)`
- **Conclusion:** PASS RQ2 PROOF (DS0003 C=0.5864 -> C+L=0.6633 -> C+L+S=0.8220 [+0.1587 lifestyle gain!]; DS0004 0.7874 -> 0.7999)

| Cohort | Seed | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp | Tau_Youden |
|---|---|---|---|---|---|---|---|---|
| `DS0003_C_only` | `20261127` | `0.586370` | `0.565047` | `0.661765` | `0.245595` | `0.117750` | `3.0` | `0.39` |
| `DS0003_C_plus_L` | `20261127` | `0.663293` | `0.671562` | `0.622642` | `0.227736` | `0.117812` | `2.975` | `0.495` |
| `DS0003_C_plus_L_plus_S` | `20261127` | `0.822031` | `0.820870` | `0.762376` | `0.170365` | `0.101968` | `1.575` | `0.515` |
| `DS0004_C_only` | `20261127` | `0.787383` | `0.768920` | `0.698977` | `0.186987` | `0.017590` | `1.075` | `0.535` |
| `DS0004_C_plus_L` | `20261127` | `0.797836` | `0.779141` | `0.718878` | `0.182343` | `0.011935` | `1.05` | `0.485` |
| `DS0004_C_plus_L_plus_S` | `20261127` | `0.799926` | `0.778612` | `0.724682` | `0.181278` | `0.018050` | `1.05` | `0.495` |
