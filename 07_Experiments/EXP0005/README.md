# EXP0005 — LightGBM_Leaf31_PosWeight (`Block_A`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0005` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | **`COMPLETED`** (`STEP-029/030` Kaggle CUDA Validation Audited; Test Remains Sealed) |
| source_inputs | `REL0001` (`Train/Val` Only — Test Sealed until `G11`) |
| governing_section | OS §6.2, §11, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe config & manifest) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Scientific Objective
- **Experiment ID:** `EXP0005`
- **Research Question:** `RQ1` | **Block:** `Block_A`
- **Comparator Tier:** `unimodal` | **Parent Baseline:** `EXP0004`
- **Active Modalities:** `clinical, laboratory, lifestyle` (`missing_modality_policy=indicator`)
- **Primary Hypothesis:** Companion GBDT histogram comparator validating tree family stability.

## 2. Data & Model Setup
- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`)
- **Model Candidate:** `MC0005` (`LightGBM_Leaf31_PosWeight` / `lightgbm`)
- **Config Path:** [config.yaml](./config.yaml)
- **Config SHA-256:** `c6af566ddc6e339016cde0727fd333fad7465ca1383f214ca2163b74a993ec12`
- **Source Git Commit:** `8994dea`

## 3. Pre-Launch Custody & Execution Targets
- **Canonical Primary Seed:** `20261127` (Block F expands across `[20261127..20261201]`)
- **Hardware Target:** `kaggle_cpu_or_t4` | **Tier 3 Artifact Path:** `08_Checkpoints/binaries/EXP0005`
- **Test Partition Status:** Strictly `SEALED_UNTIL_G11` (`0` Test reads permitted in Stage S11).
- **Execution Status:** Registered `READY` for `STEP-029` training launch via Kaggle GPU / CLI.


## 4. Observed Stage S11 Validation Outcomes (`REL0001` Val Only, `Test = 0` Reads)
- **Executed Git Revision:** `19249e5` (`CVD_Multimodal_Kaggle_Training_Pipeline.ipynb` on Kaggle CUDA GPU)
- **Saved Checkpoints:** `In-session deterministic fit (no .pt/.pkl serialized)`
- **Conclusion:** PASS Stage S11 Validation Executed (4 evaluated cohort slice(s), Test=0 reads)

| Cohort | Seed | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp | Tau_Youden |
|---|---|---|---|---|---|---|---|---|
| `DS0001` | `20261127` | `0.754176` | `0.788339` | `0.751969` | `0.204505` | `0.080371` | `1.125` | `0.435` |
| `DS0002` | `20261127` | `0.674052` | `0.754419` | `0.689655` | `0.227003` | `0.146263` | `1.625` | `0.56` |
| `DS0003` | `20261127` | `0.831478` | `0.831454` | `0.732984` | `0.167052` | `0.051565` | `0.8` | `0.58` |
| `DS0004` | `20261127` | `0.802538` | `0.784614` | `0.725496` | `0.180048` | `0.013085` | `0.975` | `0.49` |
