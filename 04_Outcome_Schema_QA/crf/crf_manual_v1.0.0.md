# Secondary Cohort CRF & Deterministic Extraction Manual (`v1.0.0`)

| Field | Value |
|---|---|
| TemplateID | T11-CRF (`crf_manual`) |
| template_version | v1.0.0 |
| entity_id | CRF-MANUAL-v1.0.0 (`UD08`) |
| owner | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |
| date | 2026-11-26 |
| status | Draft Ready for Stage S07 Clinical & Technical Review |
| source_inputs | `04_Outcome_Schema_QA/variables.csv`, `04_Outcome_Schema_QA/endpoint_charter.md`, `14_Automation/audit_cohort_quality.py` |
| governing_section | OS §4.3–§4.5, §5.2; Blueprint `STEP-014` |
| phi_sensitivity | Tier 1 (Public / Git-safe operational specification) |
| reviewer | Md. Mizanur Rahman + Qualified Cardiologist (`TBD`) |

---

## 1. Purpose & Deterministic Separation (`OS §4.4`)
This manual locks **record-local, zero-parameter deterministic rules** for reading, unit-harmonizing, and flagging raw records across `DS0001`–`DS0004` without computing any cohort mean, median, variance, or scaler prior to `STEP-020` split locking (`G07`).

---

## 2. Dataset-Specific Extraction & Harmonization Rules

### 2.1 `DS0001` (`PTB-XL v1.0.1`)
1. **Waveform Input Contract:** Native 12-lead WFDB (`.hea` + `.dat`) at `500 Hz` (`5,000` samples) and `100 Hz` (`1,000` samples), standard lead sequence `[I, II, III, AVR, AVL, AVF, V1, V2, V3, V4, V5, V6]`.
2. **Pediatric & Outlier Filters:** Flag/exclude `age < 18` (`133` rows) or missing `age` (`89` rows) under adult CVD scope; coerce non-physiological `height < 100 cm` (e.g., `6.0 cm`) or `weight < 25 kg` to missing (`NaN`) cleanly per-record before imputation inside Train folds.
3. **Signal Quarantine:** Hard-exclude **`ecg_id=12722`** (`records100/12000/12722_lr`, `V5` flatline = `0`). Preserve `patient_id` & official `strat_fold` (`1–10`) grouping invariants.

### 2.2 `DS0002` (`CARDIO-ML-ED`)
1. **Binary Format Parsing:** Open `Datasheet1 (Edited).csv` strictly via `zipfile` + OpenXML (`xl/sharedStrings.xml` + `xl/worksheets/sheet1.xml`), NOT `csv.reader` (`file carries XLSX ZIP magic bytes`). Strip leading/trailing whitespace from all header strings (`Initial diagnosis `, `Systolic blood pressure `, `Method of referral `).
2. **Duplicate Patient Grouping & Eligibility:** Index encounters using `Col1` (`Patient's file number` hospital ID). Keep `Col1` as group key so repeated rows (`12` pairs across `581` rows) never split across Train/Val/Test (`G07`). Exclude `age < 18` (`12` rows) and missing `age` (`4` rows).
3. **Troponin-I Censored String Parsing (`Tier B` Only):** Convert `'<0.05'` (`380` rows) to binary indicator `troponin_elevated = 0` (`>=0.05` -> `1`; missing -> `NaN` with explicit MNAR mask). Strictly omit `Troponine - I (Q)` from **`Tier A`** predictors.
4. **ECG Image Filename & Format Rules (`RISK0012`):** Normalize whitespace via `.strip()` (`'150753 '` -> `'150753'`) and map `'136883(2)'` -> `'136883-2'`; quarantine typo discrepancy IDs (`'140354'/'1403354'`, `'148679'/'148676'`) and `13` clinical-unlinked base-IDs (`111632..164603`). Isolate the `8` uncropped 6-lead `.jpg` strips from cropped `12`-row `.png` encoders in Stage `S07/S09` (`STEP-015`).

### 2.3 `DS0003` (`CAIR-CVD-2025`)
1. **Unit Harmonization:** Standardize height to centimeters (`Height (cm)`) and verify agreement against `Height (m) * 100`.
2. **Physiological Anomaly & Leakage Rules:** Flag any row where numeric `Systolic BP <= Diastolic BP` (`65` rows) and any `Estimated LDL (mg/dL) < 0` (`13` rows, `min=-18.0`) as deterministic outliers (quarantine vs Train-fold MICE sensitivity). **Hard-drop `CVD Risk Score` and `Blood Pressure Category` from predictor features.** Never apply pre-split SMOTE (`fixes P0022`).

### 2.4 `DS0004` (`Kaggle sulianova`)
1. **Delimiter & Exact Units:** Parse `cardio_train.csv` with `;` delimiter; transform `age_years = age_days / 365.25`; map `gender == 1` -> `'F'` (mean height `161.36 cm`) and `gender == 2` -> `'M'` (mean height `169.95 cm`).
2. **Deterministic Range Filter & Deduplication:** Flag/exclude `ap_hi <= ap_lo`, `ap_hi < 50 or ap_hi > 250`, `ap_lo < 30 or ap_lo > 180` (`1,323` rows), `height < 100 or height > 220` (`30` rows), and `weight < 30 or weight > 200` (`7` rows). Deduplicate `24` exact feature+label duplicates to a single instance and quarantine `17` discordant duplicate feature-vector pairs (`34` conflicting rows) strictly prior to splitting (`G07`).

---

## 3. Categorical Standardization Rules (`No Zero-for-Missing`)
- Missing or uncollected numeric/categorical fields MUST remain explicit `NaN` / `MISSING_TOKEN` paired with binary missingness masks (`_isnan`), NEVER coerced silently to `0` (`OS §A.4`).
- `Family History of CVD` is cataloged under **`Lifestyle`** (`RF10` traceability, p. 4) with a documented sensitivity switch permitting inclusion inside Clinical History ablations (`OS §5.2`).
