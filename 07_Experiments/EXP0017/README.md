# EXP0017 — CVDMMTransformer_LOMO (`Block_D`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0017` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | **`COMPLETED`** (`STEP-029/030` Kaggle CUDA Validation Audited; Test Remains Sealed) |
| source_inputs | `REL0001` (`Train/Val` Only — Test Sealed until `G11`) |
| governing_section | OS §6.2, §11, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe config & manifest) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Scientific Objective
- **Experiment ID:** `EXP0017`
- **Research Question:** `RQ2` | **Block:** `Block_D`
- **Comparator Tier:** `ablation` | **Parent Baseline:** `EXP0015`
- **Active Modalities:** `clinical, ecg, laboratory, lifestyle` (`missing_modality_policy=key_padding_mask`)
- **Primary Hypothesis:** Leave-One-Modality-Out performance drops correlate positively with mean modality |SHAP| shares.

## 2. Data & Model Setup
- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`)
- **Model Candidate:** `MC0015` (`CVDMMTransformer_LOMO` / `pytorch`)
- **Config Path:** [config.yaml](./config.yaml)
- **Config SHA-256:** `62c301b153d21f91e3e981d11ddc1528bc1bd69b051ef087c79589dadd580d4c`
- **Source Git Commit:** `8994dea`

## 3. Pre-Launch Custody & Execution Targets
- **Canonical Primary Seed:** `20261127` (Block F expands across `[20261127..20261201]`)
- **Hardware Target:** `kaggle_t4_gpu` | **Tier 3 Artifact Path:** `08_Checkpoints/binaries/EXP0017`
- **Test Partition Status:** Strictly `SEALED_UNTIL_G11` (`0` Test reads permitted in Stage S11).
- **Execution Status:** Registered `READY` for `STEP-029` training launch via Kaggle GPU / CLI.


## 4. Observed Stage S11 Validation Outcomes (`REL0001` Val Only, `Test = 0` Reads)
- **Executed Git Revision:** `19249e5` (`CVD_Multimodal_Kaggle_Training_Pipeline.ipynb` on Kaggle CUDA GPU)
- **Saved Checkpoints:** `In-session deterministic fit (no .pt/.pkl serialized)`
- **Conclusion:** PASS LOMO (Full 0.8237 -> drop_Clinical 0.6885, drop_ECG 0.7891, drop_Lab 0.8166, drop_Lifestyle 0.8217)

| Cohort | Seed | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp | Tau_Youden |
|---|---|---|---|---|---|---|---|---|
| `ALL_LOMO_drop_Clinical` | `20261127` | `0.688528` | `0.708955` | `0.543220` | `0.215917` | `0.030047` | `1.35` | `0.505` |
| `ALL_LOMO_drop_ECG` | `20261127` | `0.789115` | `0.778720` | `0.723511` | `0.187284` | `0.017247` | `1.15` | `0.48` |
| `ALL_LOMO_drop_Lab` | `20261127` | `0.816602` | `0.829082` | `0.732742` | `0.174218` | `0.018455` | `1.3` | `0.49` |
| `ALL_LOMO_drop_Lifestyle` | `20261127` | `0.821682` | `0.833476` | `0.740789` | `0.171409` | `0.014786` | `1.25` | `0.49` |
