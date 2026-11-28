# EXP0018 — CVDMMTransformer_NoKeyMask (`Block_E`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0018` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | **`COMPLETED`** (`STEP-029/030` Kaggle CUDA Validation Audited; Test Remains Sealed) |
| source_inputs | `REL0001` (`Train/Val` Only — Test Sealed until `G11`) |
| governing_section | OS §6.2, §11, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe config & manifest) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Scientific Objective
- **Experiment ID:** `EXP0018`
- **Research Question:** `RQ1` | **Block:** `Block_E`
- **Comparator Tier:** `ablation` | **Parent Baseline:** `EXP0015`
- **Active Modalities:** `clinical, ecg, laboratory, lifestyle` (`missing_modality_policy=zero_fill`)
- **Primary Hypothesis:** Explicit ~ModalityMask_CELS padding improves robustness over naive zero-padding.

## 2. Data & Model Setup
- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`)
- **Model Candidate:** `MC0015` (`CVDMMTransformer_NoKeyMask` / `pytorch`)
- **Config Path:** [config.yaml](./config.yaml)
- **Config SHA-256:** `227d9b24cff8543cfdb0e1e09995501b385dd66daab4081e2cde0491a34df11e`
- **Source Git Commit:** `8994dea`

## 3. Pre-Launch Custody & Execution Targets
- **Canonical Primary Seed:** `20261127` (Block F expands across `[20261127..20261201]`)
- **Hardware Target:** `kaggle_t4_gpu` | **Tier 3 Artifact Path:** `08_Checkpoints/binaries/EXP0018`
- **Test Partition Status:** Strictly `SEALED_UNTIL_G11` (`0` Test reads permitted in Stage S11).
- **Execution Status:** Registered `READY` for `STEP-029` training launch via Kaggle GPU / CLI.


## 4. Observed Stage S11 Validation Outcomes (`REL0001` Val Only, `Test = 0` Reads)
- **Executed Git Revision:** `19249e5` (`CVD_Multimodal_Kaggle_Training_Pipeline.ipynb` on Kaggle CUDA GPU)
- **Saved Checkpoints:** `CKPT0012`
- **Conclusion:** PASS ABLATION (key_padding_mask macro 0.8169 / DS0002 0.7353 vs zero_fill macro 0.8093 / DS0002 0.6939)

| Cohort | Seed | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp | Tau_Youden |
|---|---|---|---|---|---|---|---|---|
| `ALL_COHORTS` | `20261127` | `0.825597` | `0.835582` | `0.746542` | `0.169797` | `0.020257` | `1.025` | `0.45` |
| `DS0001` | `20261127` | `0.929540` | `0.953539` | `0.856762` | `0.107161` | `0.039446` | `1.1` | `0.495` |
| `DS0002` | `20261127` | `0.693878` | `0.774787` | `0.635294` | `0.219472` | `0.109144` | `1.775` | `0.49` |
| `DS0003` | `20261127` | `0.814524` | `0.810179` | `0.719212` | `0.177774` | `0.102881` | `0.725` | `0.505` |
| `DS0004` | `20261127` | `0.799420` | `0.777169` | `0.725133` | `0.182009` | `0.026496` | `1.025` | `0.44` |
