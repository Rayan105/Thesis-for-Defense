# Cohort Cards — `DS0001` to `DS0004` (`DEC0004` Option B Intake)

| Field | Value |
|---|---|
| TemplateID | T09 (cohort_card.md) |
| template_version | v1.0.0 |
| entity_id | DS0001; DS0002; DS0003; DS0004 |
| owner | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |
| date | 2026-11-26 |
| status | Intake Audited (`DS0002` Partial Blocker `RISK0011`; `G04` NOT ASSESSED) |
| source_inputs | `03_Datasets_Cohort/datasets.csv`, `03_Datasets_Cohort/sites.csv`, `03_Datasets_Cohort/manifests/*.csv`, `14_Automation/audit_cohort_quality.py` |
| governing_section | OS §4.1–§4.3, §14.2 (`G04`), §15.2 (`T09`); Blueprint `STEP-012`–`STEP-013` |
| phi_sensitivity | Tier 1 (Public / Git-safe aggregates only; raw archives in `.gitignore` `Dataset/`) |
| reviewer | Md. Mizanur Rahman (Supervisor) |

---

## Card 1 — `DS0001`: PTB-XL v1.0.1 (`SITE0001`)

### 1. Provenance & Administration
- **Dataset / Site:** `DS0001` (`SITE0001`) — PTB-XL Large Publicly Available Electrocardiography Dataset, `v1.0.1` (`PTB` Berlin, Germany; retrieved via Kaggle `khyeh0719/ptb-xl-dataset`).
- **License / Authorization Record:** `CC BY 4.0` ([SITE0001.md](../irb_permissions/SITE0001.md)); Supervisor `DEC0004` ratification pending.
- **Local Storage (Gitignored Tier 2B):** `Dataset/1. DS0001_ptbxl (PTB-XL, Kaggle)/ptb-xl-a-large-publicly-available-electrocardiography-dataset-1.0.1` (`87,354` files, `3,031.50 MiB` verified in `SHA256SUMS.txt`).
- **Checksums:**
  - Vendor `SHA256SUMS.txt` SHA-256: `2be684997575c9e8a006a6bc15ba0eb89a1b7ddfd585be39c19b103c7eb56ea3` (`87,353` verified files: `0` missing, `0` mismatches).
  - Non-waveform metadata manifest ([DS0001_ptbxl_metadata_manifest.csv](../manifests/DS0001_ptbxl_metadata_manifest.csv)): `2052c00f19e556fad43994af033b4b9510709f65dea42ede43fd17e17b7a770f`.

### 2. Quantitative Summary
- **Unique Patients (`patient_id`):** `18,885` | **Total Encounters / ECGs:** `21,837` | **Fold Partitioning:** Official patient-disjoint `strat_fold 1–10` (`0` patients across `>1` fold; Fold counts `2177, 2184, 2194, 2175, 2176, 2178, 2178, 2179, 2193, 2203`).
- **Diagnostic Outcomes (SCP Likelihood > 0):** `12,306` (`56.35%`) non-NORM diagnostic ECGs (`MI: 5,486`, `STTC: 5,123`, `HYP: 2,655`, `CD: 4,907` multilabel), `9,111` NORM-only, `420` without diagnostic statement.
- **Demographics:** Sex `{0: 11,379, 1: 10,458}` (`0` missing); Age `min 2.0`, `max 95.0` (`133` `<18y`, `0` `>120y`, `89` missing).

### 3. Modality Availability & Missingness (`DS0001`)
| Modality | Available? | Variables / Format | Missingness / Caveats |
|---|---|---|---|
| **Clinical** | **Partial (`C_partial`)** | `age, sex, height, weight, scp_codes`, recording meta | Missing: `age: 89`, `height: 14,854`, `weight: 12,408`; `sex: 0`; **`133` `<18y` require adult filter** |
| **ECG** | **Full Digital (`E`)** | `12-lead` WFDB `.hea/.dat` at `500 Hz` & `100 Hz` (`10s`, `16-bit`, `I–V6`) | `21,837` paired LR+HR files (`21,836/21,837` zero-flatline LR pass) |
| **Laboratory** | **Absent (`0`)** | None (`[MISSING_LAB]`) | `100%` cohort-missing; never stitched to external CSVs |
| **Lifestyle** | **Absent (`0`)** | None (`[MISSING_LIFESTYLE]`) | `100%` cohort-missing; never stitched to external CSVs |

### 4. Signal Integrity & Quality Checks
- **WFDB Header & PHI Scan:** `0` malformed headers across `43,674` `.hea` files (`100 Hz` LR & `500 Hz` HR); `0` `#` PHI comment lines found across `43,674` headers.
- **Signal Quality (`21,837` LR scan):** `0` `int16` saturation/clipping records; **`1` flatline lead record isolated:** `ecg_id=12722` (`patient_id=2818.0`, `records100/12000/12722_lr`, `strat_fold=2`, lead `V5=0`, matching vendor annotation `electrodes_problems='v4, v5'`). Metadata flags: `static_noise=3,262`, `extra_beats=1,954`, `baseline_drift=1,607`, `burst_noise=612`, `pacemaker=293`, `electrodes_problems=30`.

---

## Card 2 — `DS0002`: CARDIO-ML-ED (`SITE0009`)

### 1. Provenance & Administration
- **Dataset / Site:** `DS0002` (`SITE0009`) — CARDIO-ML-ED Official Mendeley Release (`DOI 10.17632/zfszfmpb82.2`; Mashhad `22 Bahman` & `Ghaem` Hospitals, Iran). Local folder `Dataset/3. DS0003_cardiomled (CARDIO-ML-ED, Mendeley Official CC BY 4.0)`.
- **License / Authorization:** `CC BY 4.0` ([SITE0009.md](../irb_permissions/SITE0009.md)).
- **Manifest CSV SHA-256:** `8124a7221aeb9d5f3b459e288d0695905fa2e6695974be488c660194b6332c92` ([DS0002_cardiomled_manifest.csv](../manifests/DS0002_cardiomled_manifest.csv); `3` files, `491,128` bytes).

### 2. Quantitative Summary
- **Clinical Rows (`Sheet 1`):** `581` non-empty rows | **Unique `Col1` Hospital IDs:** `569` (`12` repeated patient IDs) | **Unique `Col0` Serial IDs:** `581`.
- **Demographics:** Gender `{F: 347, M: 233, missing: 1}`; Numeric age (`577/581`): `min 6.0`, `max 98.0`, **`<18y: 12`**, **`>=18y: 565`**, missing `4`.
- **Labels:** Initial diagnosis: `Cardiac=346`, `Noncardiac=233`, missing `2`; Final diagnosis (`237` missing!): `Noncardiac=148`, `Hypertensive crisis=64`, `ACS=57`, `Elevated BP=24`, `Arrhythmia=18`, `Electrolyte-imbalance=17`, `MI=9`, `Cardiac-arrest=7`; Death: `0=557`, `1=10`, missing `14`. `ECG Labels.csv`: `408` entries (`343` match `Col1` after stripping `-1`/`-2` suffixes; top class `Non-cardiac=286`, `Ischemia=44`).

### 3. Modality Availability & Missingness (`DS0002`)
| Modality | Available? | Variables / Format | Missingness / Critical Defect |
|---|---|---|---|
| **Clinical** | **Present (`C`)** | Demographics, vitals (`SBP/DBP/PR/RR/T/SpO2`), triage, diagnosis | Missing: `SBP: 14`, `DBP: 17`, `PR: 25`, `RR: 77`, `Final diag: 237` |
| **ECG** | **BLOCKED Locally (`0` PNGs)** | Labels present (`ECG Labels.csv`, `408` rows); **raw `ECGS/` PNG images absent** | External Google Drive download in `README.txt` not yet fetched (`RISK0011`) |
| **Laboratory** | **Present (`L`)** | `61`-col panel (`CBC, BS, Cr, Electrolytes, Troponin-I, ESR/CRP, Coag, Urine, ABG`) | Missing ranges `106` (`WBC`) to `561` (`Bilirubin Total`); **`Troponine-I`: `196` missing (`385` present)** -> incorporation-bias audit needed (`OS §5.1`) |
| **Lifestyle** | **Absent (`0`)** | `Previous diseases` (`301` present) has **`0` smoking/alcohol/diet/activity entries** | `[MISSING_LIFESTYLE]` |

### 4. Signal Integrity & Quality Checks
- **File-Format Anomaly:** `Datasheet1 (Edited).csv` (`477,004` B) is actually an `XLSX` ZIP workbook (`PK\x03\x04` magic bytes, `10` worksheets) misnamed `.csv`.
- **Mandatory `G04` Blocker (`RISK0011`):** Zero ECG PNG files are present on disk; `ECGS/` MUST be downloaded from the official Drive link and inspected for burned-in patient banners/readable tracestrips (or replaced by Option A CITI `MIMIC-IV-Ext-MDS-ED`) before `G04` can transition from `NOT ASSESSED`.
- **Physiologic & Bias Findings:** `0` rows had `SBP <= DBP`; `12` `<18y` rows must be excluded for adult scope; `12` duplicate `Col1` IDs require connected-component grouping (`G07`); `Troponin-I` (`385/581`) requires sensitivity runs excluding cardiac enzymes from predictors (`STEP-014`).

---

## Card 3 — `DS0003`: CAIR-CVD-2025 (`SITE0007`)

### 1. Provenance & Administration
- **Dataset / Site:** `DS0003` (`SITE0007`) — `CAIR-CVD-2025` (`Jamalpur Medical College Hospital`, Bangladesh; Mendeley `DOI 10.17632/d9scg7j8fp.1`). Local folder `Dataset/4. DS0004_cair_cvd_2025 (CAIR-CVD-2025, Mendeley)`.
- **License / Authorization:** `CC BY 4.0` ([SITE0007.md](../irb_permissions/SITE0007.md)).
- **Manifest CSV SHA-256:** `b77ea5fb25fd8ac88c92849e4ecf65f260c080ae1c50919994841e41721f5f00` ([DS0003_cair_cvd_2025_manifest.csv](../manifests/DS0003_cair_cvd_2025_manifest.csv); `CVD Dataset.csv`, `167,325` bytes).

### 2. Quantitative Summary
- **Records:** `1,529` (`0` exact duplicate rows) | **Demographics:** `Age 25.0–79.0 y` (`0` `<18y`, `78` missing); `Sex: F=773, M=756` (`0` missing).
- **Target (`CVD Risk Level`):** `HIGH=728 (47.61%)`, `INTERMEDIARY=581 (38.00%)`, `LOW=220 (14.39%)`.

### 3. Modality Availability & Missingness (`DS0003`)
| Modality | Available? | Variables / Format | Missingness / Caveats |
|---|---|---|---|
| **Clinical** | **Present (`C`)** | `Sex, Age, Weight, Height(m/cm), BMI, Abd Circ, Waist-Ht Ratio, BP str/SBP/DBP, BP Category` | Missing `64` (`BMI`) to `82` (`Diastolic BP`); categorical `Sex/BP Cat/Diabetes` complete (`0` missing) |
| **ECG** | **Absent (`0`)** | None (`[MISSING_ECG]`) | Bangladesh regional `C+L+S` branch under `DEC0004` |
| **Laboratory** | **Present (`L`)** | `Total Cholesterol (mg/dL), HDL (mg/dL), Fasting Blood Sugar (mg/dL), Estimated LDL (mg/dL), Diabetes Status` | Missing: `HDL: 80`, `TC: 73`, `LDL: 69`, `FBS: 67` |
| **Lifestyle** | **Present (`S`)** | `Smoking Status (Y=789, N=740)`, `Physical Activity Level (High=521, Mod=512, Low=496)`, `Family History of CVD` | Complete (`0` missing in categorical columns) |

### 4. Signal Integrity & Quality Checks
- `0` string-vs-numeric BP mismatches (`Blood Pressure (mmHg)` vs `Systolic BP`/`Diastolic BP`), **`65` rows have `Systolic BP <= Diastolic BP`** (requiring deterministic cleaning/quarantine at `STEP-021`). Zero pre-split SMOTE (`fixes P0022 leakage`).

---

## Card 4 — `DS0004`: Kaggle Cardiovascular Disease (`SITE0012`)

### 1. Provenance & Administration
- **Dataset / Site:** `DS0004` (`SITE0012`) — Cardiovascular Disease Dataset (`kaggle.com/datasets/sulianova/cardiovascular-disease-dataset`). Local folder `Dataset/5. DS0005_sulianova_cvd (Cardiovascular Disease, Kaggle)`.
- **License / Authorization:** Kaggle Open Public Release ([SITE0012.md](../irb_permissions/SITE0012.md)).
- **Manifest CSV SHA-256:** `dad4750462cf6a37d1cc243aa18ac8f37870846c8fcdbce17e39786c2a46793e` ([DS0004_sulianova_cvd_manifest.csv](../manifests/DS0004_sulianova_cvd_manifest.csv); `;`-delimited `cardio_train.csv`, `2,941,524` bytes).

### 2. Quantitative Summary
- **Records:** `70,000` (`id` synthetic key) | **Target (`cardio`):** `1=34,979 (49.97%)`, `0=35,021 (50.03%)`.
- **Demographics:** `age` (in days) spans `29.6–64.9 y` (`0` `<18y`); `0` missing values across all `13` columns.

### 3. Modality Availability & Missingness (`DS0004`)
| Modality | Available? | Variables / Format | Missingness / Caveats |
|---|---|---|---|
| **Clinical** | **Present (`C`)** | `age (days), gender, height (cm), weight (kg), ap_hi, ap_lo` | `0` missing; `1,323` BP anomalies (`1,236` `ap_hi <= ap_lo`; `1,222` outside `[50..250]/[30..180]`); `30` extreme heights (`<100/>220 cm`), `7` extreme weights (`<30/>200 kg`), `42` extreme BMIs (`<10/>70`) |
| **ECG** | **Absent (`0`)** | None (`[MISSING_ECG]`) | Large-scale `C+L_ordinal+S` Missing-ECG power & LOMO benchmark |
| **Laboratory** | **Ordinal Only (`L_ord`)** | `cholesterol` (1–3), `gluc` (1–3) | `0` missing; coarse ordinal screening tiers rather than exact continuous assays |
| **Lifestyle** | **Present (`S`)** | `smoke (6,169 yes)`, `alco (3,764 yes)`, `active (56,261 yes)` | `0` missing |

### 4. Signal Integrity & Quality Checks
- **Duplicate Leakage Alert (`G07`):** `24` exact duplicate feature+label rows and `17` exact feature-vector groups with discordant `cardio` outcome labels detected -> MUST perform duplicate consolidation / group-aware exclusion prior to Train/Val/Test split (`STEP-019`–`STEP-020`).
- **Deterministic Outlier Quarantine (`STEP-021`):** Record-local range filter flags `1,323` BP outliers + extreme anthropometric entries cleanly without touching outcome distributions pre-split.
