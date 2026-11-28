# EXP0011 — WHOFraminghamContextScorer (`Block_B`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0011` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | **`COMPLETED`** (`STEP-029/030` Kaggle CUDA Validation Audited; Test Remains Sealed) |
| source_inputs | `REL0001` (`Train/Val` Only — Test Sealed until `G11`) |
| governing_section | OS §6.2, §11, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe config & manifest) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Scientific Objective
- **Experiment ID:** `EXP0011`
- **Research Question:** `RQ1` | **Block:** `Block_B`
- **Comparator Tier:** `clinical_score` | **Parent Baseline:** `EXP0001`
- **Active Modalities:** `clinical, laboratory, lifestyle` (`missing_modality_policy=indicator`)
- **Primary Hypothesis:** Interpretable clinical baseline sets diagnostic context bar on DS0003/DS0004.

## 2. Data & Model Setup
- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`)
- **Model Candidate:** `MC0011` (`WHOFraminghamContextScorer` / `custom_score`)
- **Config Path:** [config.yaml](./config.yaml)
- **Config SHA-256:** `592aee0e2aa5d16237669a6ba8e28c3036e923be9e1435fbdedda898f2886f41`
- **Source Git Commit:** `8994dea`

## 3. Pre-Launch Custody & Execution Targets
- **Canonical Primary Seed:** `20261127` (Block F expands across `[20261127..20261201]`)
- **Hardware Target:** `local_cpu` | **Tier 3 Artifact Path:** `08_Checkpoints/binaries/EXP0011`
- **Test Partition Status:** Strictly `SEALED_UNTIL_G11` (`0` Test reads permitted in Stage S11).
- **Execution Status:** Registered `READY` for `STEP-029` training launch via Kaggle GPU / CLI.


## 4. Observed Stage S11 Validation Outcomes (`REL0001` Val Only, `Test = 0` Reads)
- **Executed Git Revision:** `19249e5` (`CVD_Multimodal_Kaggle_Training_Pipeline.ipynb` on Kaggle CUDA GPU)
- **Saved Checkpoints:** `In-session deterministic fit (no .pt/.pkl serialized)`
- **Conclusion:** PASS (Clinical score near chance on BD DS0003 [0.5004] and 0.6486 on DS0004; ML/DL beats by +0.15 to +0.35)

| Cohort | Seed | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp | Tau_Youden |
|---|---|---|---|---|---|---|---|---|
| `DS0003` | `20261127` | `0.500422` | `0.474757` | `0.548673` | `0.250918` | `0.117382` | `3.0` | `0.465` |
| `DS0004` | `20261127` | `0.648564` | `0.623121` | `0.571398` | `0.236726` | `0.053225` | `1.2` | `0.46` |
