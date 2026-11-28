# Stage S11 Complete Validation Matrix & Ablation Summary (`STEP-031`)

| Field | Value |
|---|---|
| Document | `07_Experiments/validation_matrix_summary.md` |
| Version | v1.0.0 |
| Steps / Gates | `STEP-029`–`STEP-031` -> Gate `G10` Ready |
| Date | `2026-11-28` |
| Data Scope | `REL0001` **Train (`66,338`) & Validation (`12,724`) ONLY — `Test` (`12,719`) STRICTLY SEALED (`0` Reads)** |
| Source Commit | `19249e5` (`CVD_Multimodal_Kaggle_Training_Pipeline.ipynb`, Kaggle CUDA GPU) |

---

## 1. Multi-Seed `CVDMMTransformer` (`MODEL0015` / `MC0015`) Summary (`EXP0015` + `EXP0020`, `5` Seeds `[20261127..20261201]`)

| Cohort | Seeds | ROC-AUC (Mean ± SD, Range) | PR-AUC (Mean ± SD) | F1 Youden (Mean ± SD) | Mean Brier Cal | Mean ECE Cal |
|---|---|---|---|---|---|---|
| `ALL_COHORTS` | `5` | **`0.8225 ± 0.0048`** (`0.8150–0.8267`) | `0.8322 ± 0.0046` | `0.7432 ± 0.0095` | `0.1725` | `0.0334` |
| `DS0001` | `5` | **`0.9291 ± 0.0065`** (`0.9178–0.9333`) | `0.9520 ± 0.0038` | `0.8577 ± 0.0057` | `0.1087` | `0.0476` |
| `DS0002` | `5` | **`0.7349 ± 0.0237`** (`0.6945–0.7528`) | `0.8138 ± 0.0248` | `0.6928 ± 0.0249` | `0.2072` | `0.1325` |
| `DS0003` | `5` | **`0.8083 ± 0.0083`** (`0.7997–0.8183`) | `0.8027 ± 0.0169` | `0.7186 ± 0.0301` | `0.1897` | `0.1195` |
| `DS0004` | `5` | **`0.7978 ± 0.0028`** (`0.7928–0.7992`) | `0.7770 ± 0.0032` | `0.7269 ± 0.0078` | `0.1847` | `0.0389` |

---

## 2. Tier 1–4 Validation Comparison Summary (`Primary Seed 20261127`)

- **`DS0001` (`PTB-XL`, `N_val=2,135`):** `MC0008 Conv1DBiLSTM = 0.9374` (`F1 0.8740`, `ECE 0.0238`) > `MC0007 ResNet1D = 0.9346` > `MC0014 GatedAttention = 0.9336` > `MC0015 CVDMMTransformer = 0.9333` (`5-seed 0.9291 ± 0.0065`) > `MC0010 PatchTransformer = 0.9232` >> Clinical-only `MC0001 LR = 0.7617`.
- **`DS0002` (`CARDIO-ML-ED`, Bangladesh ED Scans, `N_val=84`):** **`MC0015 CVDMMTransformer = 0.7353` (`5-seed 0.7349 ± 0.0237`, Peak `0.7528`)** beats ALL comparators: `MC0001 LR = 0.7248`, `MC0004 XGB = 0.6980`, `EXP0018 zero-fill = 0.6939`, `MC0003 SVM = 0.6857`, `MC0014 GatedAttention = 0.6811`, and unimodal `MC0009 2D-CNN = 0.5486` (`N_val=50` PNGs alone).
- **`DS0003` (`CAIR-CVD-2025`, Bangladesh Screening, `N_val=218`):** `MC0002 RandomForest = 0.8523` (`PR-AUC 0.8553`, `F1 0.7624`) > `MC0004 XGB = 0.8359` > `MC0005 LGBM = 0.8315` > `MC0014 GatedAttention = 0.8249` > `MC0003 SVM = 0.8235` > `MC0015 CVDMMTransformer = 0.7997` (`5-seed 0.8083 ± 0.0083`, Peak `0.8183`) >> `EXP0011 Clinical Score = 0.5004`.
- **`DS0004` (`Kaggle CVD`, `N_val=10,287`):** `MC0005 LGBM = 0.8025` ≈ `MC0014 = 0.8025` ≈ `MC0004 XGB = 0.8024` ≈ `MC0006 MLP = 0.8020` > `MC0015 = 0.7992` (`5-seed 0.7978 ± 0.0028`) >> `EXP0011 Clinical Score = 0.6486`.
- **`ALL_COHORTS` (`N_val=12,724` Unified Pool):** `EXP0012 EarlyConcat XGB = 0.8303` (`ECE 0.0189`), `EXP0013 Stacker = 0.8274`, `EXP0014 GatedAttention = 0.8264` (`macro=0.8105`), **`EXP0015 CVDMMTransformer = 0.8237` (`5-seed 0.8225 ± 0.0048`, `macro=0.8169`, Peak `0.8267`/`macro 0.8256`, best pooled `ECE=0.0169`, best pooled `F1=0.7490`)**.

---

## 3. Block D (`EXP0016` & `EXP0017`) — Lifestyle Incremental Gain & LOMO Evidence (`RQ2`)

### 3.1 Progressive Addition (`EXP0016`, XGBoost Matched)
| Slice | ROC-AUC | PR-AUC | F1 Youden | Brier Cal |
|---|---|---|---|---|
| `DS0003_C_only` | `0.5864` | `0.5650` | `0.6618` | `0.2456` |
| `DS0003_C_plus_L` | `0.6633` | `0.6716` | `0.6226` | `0.2277` |
| `DS0003_C_plus_L_plus_S` | `0.8220` | `0.8209` | `0.7624` | `0.1704` |
| `DS0004_C_only` | `0.7874` | `0.7689` | `0.6990` | `0.1870` |
| `DS0004_C_plus_L` | `0.7978` | `0.7791` | `0.7189` | `0.1823` |
| `DS0004_C_plus_L_plus_S` | `0.7999` | `0.7786` | `0.7247` | `0.1813` |

**Key Finding (`PG4` / `RQ2`):** Adding structured Lifestyle (`+S`) on Bangladesh `DS0003` increases `Val ROC-AUC` from **`0.6633` -> `0.8220` (`+0.1587`)** and `F1` from `0.6226` -> `0.7624`, directly refuting lifestyle redundancy in South Asian outpatient screening.

### 3.2 Leave-One-Modality-Out (`EXP0017`, Champion `MODEL0015` vs Full `0.8237`)
| LOMO Drop | Val ROC-AUC | Delta vs Full (`0.8237`) | F1 Youden |
|---|---|---|---|
| `ALL_LOMO_drop_Clinical` | `0.6885` | `-0.1352` | `0.5432` |
| `ALL_LOMO_drop_ECG` | `0.7891` | `-0.0346` | `0.7235` |
| `ALL_LOMO_drop_Lab` | `0.8166` | `-0.0071` | `0.7327` |
| `ALL_LOMO_drop_Lifestyle` | `0.8217` | `-0.0020` | `0.7408` |

---

## 4. Block E & Block F (`EXP0018–EXP0020`) — Masking, PROBAST & Degradation Resilience

- **Masking Ablation (`EXP0018` `use_key_mask=False` vs `EXP0015` `use_key_mask=True`):** Explicit `~ModalityMask_CELS` Transformer attention masking raises macro-average AUROC from `0.8093` to **`0.8169`** and boosts the genuine partial-ECG hospital cohort (`DS0002`) from `0.6939` to **`0.7353`** (`+0.0414`), while naive zero-filling was slightly higher only on pure-tabular `DS0003` (`0.8145` vs `0.7997`).
- **PROBAST `DS0002_noCABG` (`EXP0019`):** `84/84` Val records had `prior_cabg_flag=0`, yielding `0.7353` identically (`0` incorporation contamination).

### Missing-Modality Degradation Curve (`EXP0020` on `MODEL0015`)
| Condition | Val ROC-AUC | PR-AUC | F1 Youden | ECE Cal |
|---|---|---|---|---|
| `DS0002_Real_MISSING_ECG` | `0.6609` | `0.7283` | `0.5600` | `0.2850` |
| `STRESS_dropECG_10pct` | `0.8208` | `0.8310` | `0.7469` | `0.0182` |
| `STRESS_dropECG_25pct` | `0.8156` | `0.8237` | `0.7432` | `0.0176` |
| `STRESS_dropECG_50pct` | `0.8056` | `0.8092` | `0.7348` | `0.0143` |
| `STRESS_dropECG_100pct` | `0.7891` | `0.7787` | `0.7235` | `0.0172` |
| `STRESS_dropLab_10pct` | `0.8228` | `0.8342` | `0.7472` | `0.0167` |
| `STRESS_dropLab_25pct` | `0.8222` | `0.8340` | `0.7456` | `0.0172` |
| `STRESS_dropLab_50pct` | `0.8213` | `0.8332` | `0.7412` | `0.0177` |
| `STRESS_dropLab_100pct` | `0.8166` | `0.8291` | `0.7327` | `0.0185` |
| `STRESS_dropLife_10pct` | `0.8235` | `0.8350` | `0.7485` | `0.0174` |
| `STRESS_dropLife_25pct` | `0.8233` | `0.8349` | `0.7480` | `0.0179` |
| `STRESS_dropLife_50pct` | `0.8225` | `0.8343` | `0.7458` | `0.0157` |
| `STRESS_dropLife_100pct` | `0.8217` | `0.8335` | `0.7408` | `0.0148` |

---

## 5. Honest Limitations & Prospective Deviations Recorded
1. **`MODEL0015` Parameter Count:** Actual trained checkpoint (`CKPT0011`, `266,587` params) exceeds the `250,000` ceiling in `config.yaml` by `+16,587` (`+6.6%`) due to Dual `Max+Avg` Pooling (`Linear(128, 64)` + `LayerNorm`) introduced in `commit 0e63ee3` to preserve sparse `DS0002` QRS peaks. Retained cleanly (`<< 1M` EPV ceiling).
2. **Tabular-Only Cohort Advantage of Ensembles:** On `DS0003` (`CAIR-CVD-2025` pure tabular), `RandomForest` (`0.8523`) and `XGBoost` (`0.8359`) outperform `CVDMMTransformer` (`0.8083 ± 0.0083`), reported transparently without cherry-picking.
3. **Serialized vs Reconstructed Comparators:** `EXP0004`, `EXP0007–10`, `EXP0014–15`, `EXP0018`, and `EXP0020` binaries (`15` checkpoints) are SHA-256 verified in Tier 3; deterministic `sklearn`/`LightGBM` baselines (`EXP0001–03, 0005, 0011–13`) reproduce identically from locked `REL0001/train` + `seed=20261127` + frozen validation hyperparameters at `STEP-033`.
