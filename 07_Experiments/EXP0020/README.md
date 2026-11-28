# EXP0020 — CVDMMTransformer_MultiSeed_Stress (`Block_F`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0020` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | **`COMPLETED`** (`STEP-029/030` Kaggle CUDA Validation Audited; Test Remains Sealed) |
| source_inputs | `REL0001` (`Train/Val` Only — Test Sealed until `G11`) |
| governing_section | OS §6.2, §11, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe config & manifest) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Scientific Objective
- **Experiment ID:** `EXP0020`
- **Research Question:** `RQ4` | **Block:** `Block_F`
- **Comparator Tier:** `ablation` | **Parent Baseline:** `EXP0015`
- **Active Modalities:** `clinical, ecg, laboratory, lifestyle` (`missing_modality_policy=key_padding_mask`)
- **Primary Hypothesis:** Champion retains graceful degradation under 10-100% synthetic masking & DS0002 [MISSING_ECG] across 5 seeds.

## 2. Data & Model Setup
- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`)
- **Model Candidate:** `MC0015` (`CVDMMTransformer_MultiSeed_Stress` / `pytorch`)
- **Config Path:** [config.yaml](./config.yaml)
- **Config SHA-256:** `f6548097ddc70c45b7a83fef19e19c9e88fe59c4babe7086a5606e11070a9e4b`
- **Source Git Commit:** `8994dea`

## 3. Pre-Launch Custody & Execution Targets
- **Canonical Primary Seed:** `20261127` (Block F expands across `[20261127..20261201]`)
- **Hardware Target:** `kaggle_t4_gpu` | **Tier 3 Artifact Path:** `08_Checkpoints/binaries/EXP0020`
- **Test Partition Status:** Strictly `SEALED_UNTIL_G11` (`0` Test reads permitted in Stage S11).
- **Execution Status:** Registered `READY` for `STEP-029` training launch via Kaggle GPU / CLI.


## 4. Observed Stage S11 Validation Outcomes (`REL0001` Val Only, `Test = 0` Reads)
- **Executed Git Revision:** `19249e5` (`CVD_Multimodal_Kaggle_Training_Pipeline.ipynb` on Kaggle CUDA GPU)
- **Saved Checkpoints:** `CKPT0013; CKPT0014; CKPT0015; CKPT0016`
- **Conclusion:** PASS 5-SEED + STRESS (ALL_COHORTS 0.8225+-0.0048; DS0002_Real_MISSING_ECG=0.6609; 100% ECG drop=0.7891 [-3.46%])

| Cohort | Seed | Val ROC-AUC | PR-AUC | F1 (Youden) | Brier Cal | ECE Cal | Temp | Tau_Youden |
|---|---|---|---|---|---|---|---|---|
| `ALL_COHORTS` | `20261128` | `0.820847` | `0.830939` | `0.748985` | `0.174369` | `0.045333` | `0.95` | `0.525` |
| `DS0001` | `20261128` | `0.929966` | `0.952628` | `0.853215` | `0.111257` | `0.066382` | `1.175` | `0.515` |
| `DS0002` | `20261128` | `0.694461` | `0.780868` | `0.666667` | `0.219989` | `0.173794` | `2.2` | `0.525` |
| `DS0003` | `20261128` | `0.810813` | `0.792868` | `0.695187` | `0.188347` | `0.136424` | `0.775` | `0.685` |
| `DS0004` | `20261128` | `0.799166` | `0.778363` | `0.727509` | `0.186007` | `0.059565` | `0.9` | `0.525` |
| `ALL_COHORTS` | `20261129` | `0.826224` | `0.836451` | `0.730019` | `0.169038` | `0.017615` | `1.075` | `0.57` |
| `DS0001` | `20261129` | `0.932611` | `0.954670` | `0.857906` | `0.104100` | `0.036541` | `1.175` | `0.635` |
| `DS0002` | `20261129` | `0.752770` | `0.848684` | `0.698795` | `0.195078` | `0.104794` | `1.25` | `0.525` |
| `DS0003` | `20261129` | `0.818320` | `0.825950` | `0.714286` | `0.175022` | `0.075283` | `0.85` | `0.58` |
| `DS0004` | `20261129` | `0.798602` | `0.776393` | `0.734886` | `0.182010` | `0.019266` | `1.075` | `0.44` |
| `ALL_COHORTS` | `20261130` | `0.826683` | `0.833846` | `0.751636` | `0.169284` | `0.022371` | `0.925` | `0.505` |
| `DS0001` | `20261130` | `0.932029` | `0.952060` | `0.856514` | `0.104022` | `0.024433` | `0.95` | `0.64` |
| `DS0002` | `20261130` | `0.741108` | `0.804820` | `0.712644` | `0.207454` | `0.119742` | `2.275` | `0.68` |
| `DS0003` | `20261130` | `0.813090` | `0.808360` | `0.752381` | `0.185278` | `0.107052` | `0.675` | `0.605` |
| `DS0004` | `20261130` | `0.799159` | `0.776190` | `0.730837` | `0.181949` | `0.019497` | `0.925` | `0.485` |
| `ALL_COHORTS` | `20261201` | `0.815000` | `0.824771` | `0.736126` | `0.179227` | `0.064997` | `1.15` | `0.57` |
| `DS0001` | `20261201` | `0.917765` | `0.945573` | `0.853403` | `0.115012` | `0.037890` | `0.9` | `0.44` |
| `DS0002` | `20261201` | `0.751020` | `0.822183` | `0.719101` | `0.205309` | `0.121740` | `1.425` | `0.645` |
| `DS0003` | `20261201` | `0.799764` | `0.781123` | `0.746544` | `0.213130` | `0.177843` | `1.275` | `0.615` |
| `DS0004` | `20261201` | `0.792788` | `0.772596` | `0.714038` | `0.191510` | `0.077116` | `1.225` | `0.57` |
| `DS0002_Real_MISSING_ECG` | `20261127` | `0.660900` | `0.728349` | `0.560000` | `0.220150` | `0.285027` | `1.725` | `0.505` |
| `STRESS_dropECG_10pct` | `20261127` | `0.820820` | `0.831000` | `0.746854` | `0.172024` | `0.018245` | `1.2` | `0.48` |
| `STRESS_dropECG_25pct` | `20261127` | `0.815583` | `0.823719` | `0.743205` | `0.174670` | `0.017560` | `1.2` | `0.48` |
| `STRESS_dropECG_50pct` | `20261127` | `0.805580` | `0.809190` | `0.734807` | `0.179527` | `0.014258` | `1.175` | `0.48` |
| `STRESS_dropECG_100pct` | `20261127` | `0.789115` | `0.778720` | `0.723511` | `0.187284` | `0.017247` | `1.15` | `0.48` |
| `STRESS_dropLab_10pct` | `20261127` | `0.822796` | `0.834243` | `0.747241` | `0.171011` | `0.016707` | `1.225` | `0.48` |
| `STRESS_dropLab_25pct` | `20261127` | `0.822196` | `0.834021` | `0.745633` | `0.171236` | `0.017174` | `1.225` | `0.48` |
| `STRESS_dropLab_50pct` | `20261127` | `0.821311` | `0.833153` | `0.741239` | `0.171788` | `0.017659` | `1.25` | `0.49` |
| `STRESS_dropLab_100pct` | `20261127` | `0.816602` | `0.829082` | `0.732742` | `0.174218` | `0.018455` | `1.3` | `0.49` |
| `STRESS_dropLife_10pct` | `20261127` | `0.823504` | `0.834955` | `0.748493` | `0.170663` | `0.017426` | `1.225` | `0.48` |
| `STRESS_dropLife_25pct` | `20261127` | `0.823345` | `0.834854` | `0.748015` | `0.170696` | `0.017906` | `1.225` | `0.48` |
| `STRESS_dropLife_50pct` | `20261127` | `0.822509` | `0.834308` | `0.745841` | `0.171005` | `0.015739` | `1.225` | `0.48` |
| `STRESS_dropLife_100pct` | `20261127` | `0.821682` | `0.833476` | `0.740789` | `0.171409` | `0.014786` | `1.25` | `0.49` |
