# EXP0019 — CVDMMTransformer_PROBAST_Sens (`Block_E`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0019` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | **`READY`** (`STEP-028` Pre-Launch Immutable Bundle Verified) |
| source_inputs | `REL0001` (`Train/Val` Only — Test Sealed until `G11`) |
| governing_section | OS §6.2, §11, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe config & manifest) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Scientific Objective
- **Experiment ID:** `EXP0019`
- **Research Question:** `RQ3` | **Block:** `Block_E`
- **Comparator Tier:** `ablation` | **Parent Baseline:** `EXP0015`
- **Active Modalities:** `clinical, ecg, laboratory` (`missing_modality_policy=key_padding_mask`)
- **Primary Hypothesis:** Incorporation-bias audit compares primary Tier A vs exploratory Tier B Troponin & CABG/FH sensitivity.

## 2. Data & Model Setup
- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`)
- **Model Candidate:** `MC0015` (`CVDMMTransformer_PROBAST_Sens` / `pytorch`)
- **Config Path:** [config.yaml](./config.yaml)
- **Config SHA-256:** `9c7fc75e8fe8a7ac493f79da23ed914a6accc496fcd438feaf3eb42644b33a6b`
- **Source Git Commit:** `8994dea`

## 3. Pre-Launch Custody & Execution Targets
- **Canonical Primary Seed:** `20261127` (Block F expands across `[20261127..20261201]`)
- **Hardware Target:** `kaggle_t4_gpu` | **Tier 3 Artifact Path:** `08_Checkpoints/binaries/EXP0019`
- **Test Partition Status:** Strictly `SEALED_UNTIL_G11` (`0` Test reads permitted in Stage S11).
- **Execution Status:** Registered `READY` for `STEP-029` training launch via Kaggle GPU / CLI.
