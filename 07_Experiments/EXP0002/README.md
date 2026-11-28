# EXP0002 — RandomForest_Balanced300 (`Block_A`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0002` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | **`COMPLETED`** (`STEP-029/030` Kaggle CUDA Validation Audited; Test Remains Sealed) |
| source_inputs | `REL0001` (`Train/Val` Only — Test Sealed until `G11`) |
| governing_section | OS §6.2, §11, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe config & manifest) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Scientific Objective
- **Experiment ID:** `EXP0002`
- **Research Question:** `RQ1` | **Block:** `Block_A`
- **Comparator Tier:** `unimodal` | **Parent Baseline:** `EXP0001`
- **Active Modalities:** `clinical, laboratory, lifestyle` (`missing_modality_policy=indicator`)
- **Primary Hypothesis:** 300-tree RandomForest with balanced subsample weights captures non-linear interactions.

## 2. Data & Model Setup
- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`)
- **Model Candidate:** `MC0002` (`RandomForest_Balanced300` / `sklearn`)
- **Config Path:** [config.yaml](./config.yaml)
- **Config SHA-256:** `a1416261e21e766a52ef03bb04315b94529bb4065f2977e07638d0e693accacc`
- **Source Git Commit:** `8994dea`

## 3. Pre-Launch Custody & Execution Targets
- **Canonical Primary Seed:** `20261127` (Block F expands across `[20261127..20261201]`)
- **Hardware Target:** `kaggle_cpu_or_t4` | **Tier 3 Artifact Path:** `08_Checkpoints/binaries/EXP0002`
- **Test Partition Status:** Strictly `SEALED_UNTIL_G11` (`0` Test reads permitted in Stage S11).
- **Execution Status:** Registered `READY` for `STEP-029` training launch via Kaggle GPU / CLI.


## 4. Observed Stage S11 Validation Outcomes (`REL0001` Val Only, `Test = 0` Reads)
- **Executed Git Revision:** `19249e5` (`CVD_Multimodal_Kaggle_Training_Pipeline.ipynb` on Kaggle CUDA GPU)
- **Saved Checkpoints:** `In-session deterministic fit (no .pt/.pkl serialized)`
- **Conclusion:** PASS Stage S11 Validation Executed (4 evaluated cohort slice(s), Test=0 reads)

| Cohort | Seed | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp | Tau_Youden |
|---|---|---|---|---|---|---|---|---|
| `DS0001` | `20261127` | `0.746127` | `0.777678` | `0.738687` | `0.205373` | `0.080551` | `1.1` | `0.49` |
| `DS0002` | `20261127` | `0.676968` | `0.781298` | `0.542857` | `0.217281` | `0.150710` | `0.9` | `0.68` |
| `DS0003` | `20261127` | `0.852311` | `0.855270` | `0.762376` | `0.156468` | `0.079544` | `0.4` | `0.455` |
| `DS0004` | `20261127` | `0.799660` | `0.778419` | `0.725960` | `0.181519` | `0.015506` | `0.975` | `0.47` |
