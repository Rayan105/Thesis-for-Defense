# EXP0013 — LateOOFStacker (`Block_C`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0013` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | **`COMPLETED`** (`STEP-029/030` Kaggle CUDA Validation Audited; Test Remains Sealed) |
| source_inputs | `REL0001` (`Train/Val` Only — Test Sealed until `G11`) |
| governing_section | OS §6.2, §11, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe config & manifest) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Scientific Objective
- **Experiment ID:** `EXP0013`
- **Research Question:** `RQ1` | **Block:** `Block_C`
- **Comparator Tier:** `simple_fusion` | **Parent Baseline:** `EXP0012`
- **Active Modalities:** `clinical, ecg, laboratory, lifestyle` (`missing_modality_policy=indicator`)
- **Primary Hypothesis:** Level-1 OOF logit stacker quantifies multimodal gain without cross-modal feature interaction.

## 2. Data & Model Setup
- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`)
- **Model Candidate:** `MC0013` (`LateOOFStacker` / `sklearn`)
- **Config Path:** [config.yaml](./config.yaml)
- **Config SHA-256:** `eb1e4e670e9ce7ff83f079ed721721a556b04075f59d696b7c8d674df48b16f1`
- **Source Git Commit:** `8994dea`

## 3. Pre-Launch Custody & Execution Targets
- **Canonical Primary Seed:** `20261127` (Block F expands across `[20261127..20261201]`)
- **Hardware Target:** `kaggle_cpu_or_t4` | **Tier 3 Artifact Path:** `08_Checkpoints/binaries/EXP0013`
- **Test Partition Status:** Strictly `SEALED_UNTIL_G11` (`0` Test reads permitted in Stage S11).
- **Execution Status:** Registered `READY` for `STEP-029` training launch via Kaggle GPU / CLI.


## 4. Observed Stage S11 Validation Outcomes (`REL0001` Val Only, `Test = 0` Reads)
- **Executed Git Revision:** `19249e5` (`CVD_Multimodal_Kaggle_Training_Pipeline.ipynb` on Kaggle CUDA GPU)
- **Saved Checkpoints:** `In-session deterministic fit (no .pt/.pkl serialized)`
- **Conclusion:** PASS Stage S11 Validation Executed (1 evaluated cohort slice(s), Test=0 reads)

| Cohort | Seed | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp | Tau_Youden |
|---|---|---|---|---|---|---|---|---|
| `ALL_COHORTS` | `20261127` | `0.827367` | `0.837537` | `0.745958` | `0.168936` | `0.020825` | `1.025` | `0.485` |
