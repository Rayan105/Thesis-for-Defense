# EXP0016 — ProgressiveModalGain_CLS (`Block_D`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0016` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | **`READY`** (`STEP-028` Pre-Launch Immutable Bundle Verified) |
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
