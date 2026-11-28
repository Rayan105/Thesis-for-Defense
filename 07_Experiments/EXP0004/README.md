# EXP0004 — XGBoost_Hist_PosWeight (`Block_A`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0004` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | **`COMPLETED`** (`STEP-029/030` Kaggle CUDA Validation Audited; Test Remains Sealed) |
| source_inputs | `REL0001` (`Train/Val` Only — Test Sealed until `G11`) |
| governing_section | OS §6.2, §11, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe config & manifest) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Scientific Objective
- **Experiment ID:** `EXP0004`
- **Research Question:** `RQ1` | **Block:** `Block_A`
- **Comparator Tier:** `unimodal` | **Parent Baseline:** `EXP0001`
- **Active Modalities:** `clinical, laboratory, lifestyle` (`missing_modality_policy=indicator`)
- **Primary Hypothesis:** Primary Tier 1 GBDT tabular anchor trained with exact Train pos_weight.

## 2. Data & Model Setup
- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`)
- **Model Candidate:** `MC0004` (`XGBoost_Hist_PosWeight` / `xgboost`)
- **Config Path:** [config.yaml](./config.yaml)
- **Config SHA-256:** `cca6e9219dfdfe1335a8a061290b39a8e1c12777b29d17aaae11e14cbece52bc`
- **Source Git Commit:** `8994dea`

## 3. Pre-Launch Custody & Execution Targets
- **Canonical Primary Seed:** `20261127` (Block F expands across `[20261127..20261201]`)
- **Hardware Target:** `kaggle_t4_gpu` | **Tier 3 Artifact Path:** `08_Checkpoints/binaries/EXP0004`
- **Test Partition Status:** Strictly `SEALED_UNTIL_G11` (`0` Test reads permitted in Stage S11).
- **Execution Status:** Registered `READY` for `STEP-029` training launch via Kaggle GPU / CLI.


## 4. Observed Stage S11 Validation Outcomes (`REL0001` Val Only, `Test = 0` Reads)
- **Executed Git Revision:** `19249e5` (`CVD_Multimodal_Kaggle_Training_Pipeline.ipynb` on Kaggle CUDA GPU)
- **Saved Checkpoints:** `CKPT0002; CKPT0003; CKPT0004; CKPT0005`
- **Conclusion:** PASS Stage S11 Validation Executed (4 evaluated cohort slice(s), Test=0 reads)

| Cohort | Seed | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp | Tau_Youden |
|---|---|---|---|---|---|---|---|---|
| `DS0001` | `20261127` | `0.756332` | `0.794546` | `0.749103` | `0.203281` | `0.086246` | `1.1` | `0.465` |
| `DS0002` | `20261127` | `0.697959` | `0.790553` | `0.682353` | `0.220754` | `0.159188` | `1.3` | `0.57` |
| `DS0003` | `20261127` | `0.835948` | `0.836446` | `0.758294` | `0.165640` | `0.066954` | `0.725` | `0.49` |
| `DS0004` | `20261127` | `0.802356` | `0.781511` | `0.719271` | `0.180194` | `0.012176` | `0.975` | `0.505` |
