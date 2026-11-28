# EXP0015 — CVDMMTransformer (`Block_C`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0015` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | **`COMPLETED`** (`STEP-029/030` Kaggle CUDA Validation Audited; Test Remains Sealed) |
| source_inputs | `REL0001` (`Train/Val` Only — Test Sealed until `G11`) |
| governing_section | OS §6.2, §11, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe config & manifest) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Scientific Objective
- **Experiment ID:** `EXP0015`
- **Research Question:** `RQ1` | **Block:** `Block_C`
- **Comparator Tier:** `transformer_fusion` | **Parent Baseline:** `EXP0014`
- **Active Modalities:** `clinical, ecg, laboratory, lifestyle` (`missing_modality_policy=key_padding_mask`)
- **Primary Hypothesis:** Proposed CVDMMTransformer outperforms unimodal & simple fusion comparators on AUROC, PR-AUC & DCA.

## 2. Data & Model Setup
- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`)
- **Model Candidate:** `MC0015` (`CVDMMTransformer` / `pytorch`)
- **Config Path:** [config.yaml](./config.yaml)
- **Config SHA-256:** `ee6239d9fd879f1bbbe144d4194776fbb412684395fd45a2255081e073a0267f`
- **Source Git Commit:** `8994dea`

## 3. Pre-Launch Custody & Execution Targets
- **Canonical Primary Seed:** `20261127` (Block F expands across `[20261127..20261201]`)
- **Hardware Target:** `kaggle_t4_gpu` | **Tier 3 Artifact Path:** `08_Checkpoints/binaries/EXP0015`
- **Test Partition Status:** Strictly `SEALED_UNTIL_G11` (`0` Test reads permitted in Stage S11).
- **Execution Status:** Registered `READY` for `STEP-029` training launch via Kaggle GPU / CLI.


## 4. Observed Stage S11 Validation Outcomes (`REL0001` Val Only, `Test = 0` Reads)
- **Executed Git Revision:** `19249e5` (`CVD_Multimodal_Kaggle_Training_Pipeline.ipynb` on Kaggle CUDA GPU)
- **Saved Checkpoints:** `CKPT0011`
- **Conclusion:** PASS CHAMPION (ALL_COHORTS 0.8237 / macro 0.8169, best ECE=0.0169, wins DS0002=0.7353; 266,587 params [+6.6% over 250K cap for Dual Max+Avg PNG pooling])

| Cohort | Seed | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp | Tau_Youden |
|---|---|---|---|---|---|---|---|---|
| `ALL_COHORTS` | `20261127` | `0.823691` | `0.835141` | `0.748990` | `0.170535` | `0.016904` | `1.2` | `0.48` |
| `DS0001` | `20261127` | `0.933255` | `0.955011` | `0.867295` | `0.109070` | `0.072693` | `1.475` | `0.405` |
| `DS0002` | `20261127` | `0.735277` | `0.812470` | `0.666667` | `0.208410` | `0.142264` | `1.425` | `0.52` |
| `DS0003` | `20261127` | `0.799679` | `0.805265` | `0.684783` | `0.186603` | `0.101137` | `1.075` | `0.66` |
| `DS0004` | `20261127` | `0.799192` | `0.781431` | `0.727435` | `0.182031` | `0.018970` | `1.125` | `0.475` |
