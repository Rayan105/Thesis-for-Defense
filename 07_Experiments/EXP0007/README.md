# EXP0007 — CompactResNet1D_WFDB (`Block_A`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0007` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | **`COMPLETED`** (`STEP-029/030` Kaggle CUDA Validation Audited; Test Remains Sealed) |
| source_inputs | `REL0001` (`Train/Val` Only — Test Sealed until `G11`) |
| governing_section | OS §6.2, §11, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe config & manifest) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Scientific Objective
- **Experiment ID:** `EXP0007`
- **Research Question:** `RQ1` | **Block:** `Block_A`
- **Comparator Tier:** `unimodal` | **Parent Baseline:** `None`
- **Active Modalities:** `ecg` (`missing_modality_policy=complete_case`)
- **Primary Hypothesis:** 12-lead WFDB SE-ResNet-1D achieves strong unimodal ECG discrimination on PTB-XL.

## 2. Data & Model Setup
- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`)
- **Model Candidate:** `MC0007` (`CompactResNet1D_WFDB` / `pytorch`)
- **Config Path:** [config.yaml](./config.yaml)
- **Config SHA-256:** `8e0d4af875ca319729485fd84dc2a2f28ed27f64ae7cd7d7a9bad34b571e8033`
- **Source Git Commit:** `8994dea`

## 3. Pre-Launch Custody & Execution Targets
- **Canonical Primary Seed:** `20261127` (Block F expands across `[20261127..20261201]`)
- **Hardware Target:** `kaggle_t4_gpu` | **Tier 3 Artifact Path:** `08_Checkpoints/binaries/EXP0007`
- **Test Partition Status:** Strictly `SEALED_UNTIL_G11` (`0` Test reads permitted in Stage S11).
- **Execution Status:** Registered `READY` for `STEP-029` training launch via Kaggle GPU / CLI.


## 4. Observed Stage S11 Validation Outcomes (`REL0001` Val Only, `Test = 0` Reads)
- **Executed Git Revision:** `19249e5` (`CVD_Multimodal_Kaggle_Training_Pipeline.ipynb` on Kaggle CUDA GPU)
- **Saved Checkpoints:** `CKPT0006`
- **Conclusion:** PASS Stage S11 Validation Executed (1 evaluated cohort slice(s), Test=0 reads)

| Cohort | Seed | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp | Tau_Youden |
|---|---|---|---|---|---|---|---|---|
| `DS0001` | `20261127` | `0.934585` | `0.957120` | `0.867188` | `0.101334` | `0.036353` | `1.15` | `0.485` |
