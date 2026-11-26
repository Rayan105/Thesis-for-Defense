# Four-Modality Quality, Missingness & ECG Signal Audit (`STEP-013`)

| Metadata | Value |
|---|---|
| Document | `03_Datasets_Cohort/reports/four_modality_qc_and_ecg_audit.md` |
| Version | v1.0.0 |
| Step | `STEP-013` (Four-Modality Quality, Signal Integrity & Pre-`G04` Audit) |
| Date | `2026-11-26` |
| Authors | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Reviewer | Md. Mizanur Rahman (Supervisor) |
| Audit Script | [audit_cohort_quality.py](../../14_Automation/audit_cohort_quality.py) (`stdlib` read-only execution) |
| PHI Sensitivity | Tier 1 (Public / Git-safe summary report) |

---

## 1. Executive QC Verdict & Gate `G04` Readiness

Across the **4 local secondary datasets** (`93,947` total encounter rows across `PTB-XL`, `CARDIO-ML-ED`, `CAIR-CVD-2025`, and `Kaggle sulianova`), extraction and exhaustive automated auditing now cover **`100%` of files across all 4 cohorts (`87,354 + 411 + 1 + 1` hashed non-archive files)**:

1. **`RISK0011` Resolved — `DS0002 ECGS/` Extracted & Verified (`408/408` Images):** Multi-part RAR volumes (`ECGS.part01..21.rar`) downloaded from official Drive extracted cleanly (`400 .png` + `8 .jpg` = `408` images, `4,297,745,117` B / `4,098.65 MiB`, `0` corrupt headers). Visual inspection confirmed **zero burned-in patient names/MRNs (`PHI PASS`)**, while uncovering important formatting heterogeneity (`RISK0012`: cropped `.png` strips still carry red paper grids contrary to `README.txt`, and `8` `.jpg` files contain uncropped 6-lead strips). Combined with verified `PTB-XL` waveforms (`21,836/21,837` clean, `ecg_id=12722` quarantined) and Supervisor Md. Mizanur Rahman ratification of `DEC0004` (`2026-11-26`), Gate **`G04`** unblocks to **`PASS` (`G04-20261126-02`)** with mandatory preprocessing/schema rules handed off to `STEP-014`–`STEP-021`.

---

## 2. Multi-Cohort 4-Modality Coverage & Anti-Stitching Matrix (`DEC0004`)

| Cohort | Clinical (`C`) | 12-Lead ECG (`E`) | Laboratory (`L`) | Lifestyle (`S`) | Same-Patient Overlap Role |
|---|---|---|---|---|---|
| **`DS0001`** (`PTB-XL`, `N=21,837` ECGs / `18,885` pts) | ⚠️ Partial (`age, sex, height, weight, SCP`) | ✅ **Raw Digital WFDB (`100/500 Hz`)** | ❌ `0%` (`[MISSING_LAB]`) | ❌ `0%` (`[MISSING_LIFESTYLE]`) | Unimodal ECG Tier 1 benchmark & `UD26` waveform pretraining |
| **`DS0002`** (`CARDIO-ML-ED`, `N=581` rows / `569` unique IDs) | ✅ ED Vitals, Demog, Triage | ✅ **`408` Scans (`400` PNG + `8` JPG)** + Labels (`344` pts linked; `327` adults $\ge 18$) | ✅ `61`-col ED panels (`CBC, CMP, Trop-I, ABG, CRP`) | ❌ `0%` (`[MISSING_LIFESTYLE]`; `0` smoking/alcohol in history) | Same-patient **`C + E_img + L`** Tier B multimodal anchor (`DEC0004`) |
| **`DS0003`** (`CAIR-CVD-2025`, `N=1,529` pts) | ✅ Age, Sex, BMI, Abd Circ, BP | ❌ `0%` (`[MISSING_ECG]`) | ✅ `TC, HDL, LDL, FBS, DM` | ✅ `Smoking, Activity, FamHx` | Bangladeshi `C+L+S` Missing-ECG branch (`RQ2`/`RQ4`) |
| **`DS0004`** (`sulianova`, `N=70,000` rows) | ✅ Age(days), Sex, Ht, Wt, SBP/DBP | ❌ `0%` (`[MISSING_ECG]`) | ⚠️ Ordinal (`chol 1-3, gluc 1-3`) | ✅ `smoke, alco, active` | Large-scale `C+L_ord+S` Missing-ECG lifestyle power (`RQ2`) |

> [!CAUTION]
> **`DEC0004` Anti-Stitching Compliance:** `Complete4ModalityCount = 0` across all `4` datasets (`no single cohort natively measures all 4 modalities simultaneously`). Zero cross-cohort synthetic patient stitching is permitted; downstream modeling MUST preserve native cohort boundaries via explicit missing-modality masking (`[MISSING_LAB]`, `[MISSING_ECG]`, `[MISSING_LIFESTYLE]`).

---

## 3. Modality-Specific Audit Findings (`OS §4.3`)

### 3.1 Modality 1 — Clinical (`C`)
- **Pediatric Scope Compliance (`adult >= 18y`):**
  - `DS0001` (`PTB-XL`): `133` recordings `<18 y` (`min 2.0`, `89` missing age) -> filter/flag `<18` at schema lock (`STEP-014`).
  - `DS0002` (`CARDIO-ML-ED`): `12` rows `<18 y` (`min 6.0`, `4` missing age) leaving `565` verified adults `>=18 y` -> filter `<18` at inclusion.
  - `DS0003` (`CAIR-CVD-2025`): `0` `<18 y` (`25.0–79.0 y`, `78` missing age).
  - `DS0004` (`sulianova`): `0` `<18 y` (`29.6–64.9 y`, encoded in days; divide by `365.25` deterministically).
- **Blood Pressure & Anthropometric Plausibility:**
  - `DS0002`: `0` rows with `SBP <= DBP`.
  - `DS0003`: `0` mismatches between `Blood Pressure (mmHg)` string and numeric `Systolic BP`/`Diastolic BP`, but **`65` rows (`4.25%`) have `Systolic BP <= Diastolic BP`** (inverted/corrupt entries requiring deterministic exclusion/imputation flagging post-split).
  - `DS0004`: **`1,323` BP anomalies** (`1,236` with `ap_hi <= ap_lo`; `1,222` outside `[50..250] / [30..180]` mmHg), `30` extreme heights (`<100` or `>220 cm`), `7` extreme weights (`<30` or `>200 kg`), `42` implausible BMIs (`<10` or `>70`).
- **Duplicate Patient / Feature Hygiene:**
  - `DS0002`: `581` rows share `569` unique `Col1` hospital IDs (`12` repeated patient encounters) -> must stay in the same connected patient group at split (`G07`).
  - `DS0003`: `0` exact duplicate rows.
  - `DS0004`: `24` exact duplicate feature+label rows and `17` identical feature vectors with conflicting `cardio` outcome labels -> deterministic duplicate quarantine mandatory prior to split (`STEP-019`).

### 3.2 Modality 2 — 12-Lead ECG Signal Integrity (`E`)
- **`DS0001` (`PTB-XL`) 100% Exhaustive Audit (`87,353 / 87,353` Files):**
  - Cryptographic parity: `0` missing files, `0` SHA-256 mismatches against vendor `SHA256SUMS.txt` (`3,031.50 MiB`).
  - Header/PHI safety: `43,674` `.hea` headers (`21,837` LR `100 Hz` + `21,837` HR `500 Hz`) verified `0` format errors and **`0` `#` PHI comment strings**.
  - Waveform integrity across all `21,837` `100 Hz` LR `.dat` recordings (`12` leads × `1000` samples, `int16`):
    - **`0`** clipped/saturated recordings (`-32768` / `32767`).
    - **`1` flatline lead recording detected (`0.0046%`):** **`ecg_id=12722`** (`patient_id=2818.0`, `records100/12000/12722_lr`, `strat_fold=2`) exhibits constant `0` signal across lead `V5` (consistent with metadata flag `electrodes_problems='v4, v5'`). **Quarantine rule:** Exclude `ecg_id=12722` from primary clean waveform modeling (or explicitly track in artifact sensitivity runs).
    - Metadata artifact prevalence logged (`static_noise=3,262`, `extra_beats=1,954`, `baseline_drift=1,607`, `burst_noise=612`, `pacemaker=293`, `electrodes_problems=30`) for `STEP-021` filtering and `G13` robustness testing.
- **`DS0002` (`CARDIO-ML-ED`) ECG Audit:**
  - `ECGS/` Extraction & Byte Integrity: `408` image files (`400 .png` + `8 .jpg`, `4,297,745,117` B / `4,098.65 MiB`), `0` corrupt PNG/JPG headers or footers. `400 .png` scans show variable portrait resolutions (`W 814–5100 × H 2757–7020` px).
  - Visual PHI & Morphology Audit (`1.png`, `122519.png`, `126035-1.jpg`): Zero burned-in patient names/MRNs/phones (`PHI PASS`). However (`RISK0012`): (a) `.png` cropped 12-row strips still retain red millimeter background grids despite `README.txt` claiming grid removal, and are rotated `90°` portrait; (b) `8` `.jpg` images (`126035-1.jpg, 126035-2.jpg, 127578-1.jpg, 127660.jpg, 142560-1.jpg, 163401.jpg, 26.jpg, 35.jpg`) are uncropped `6`-lead paper-strip scans showing `25mm/sec` & `5mm/mV` text and vendor chart margins (`exclude/isolate jpg format in ECG contract STEP-015`).
  - Label & Clinical ID Linkage Reconciliation: `396/408` image stems match `ECG Labels.csv` verbatim (`286 Non-cardiac`, `44 Ischemia`, `11 Tachycardia`, `8 MI`, etc.); `6` match after stripping trailing spaces (`150753 ` etc.); `4` match after `(2)` vs `-1/-2` normalization (`136883`, `150776`); `2` contain numeric typos between image name and label row (`140354` vs `1403354`, `148679` vs `148676` -> quarantine). Across all `408` images, `357` normalized base patient IDs yield **`344` matches (`327` verified adults $\ge 18$y)** to `Datasheet1` `Col1`, while `13` base image IDs (`111632..164603`) have zero clinical rows in `Datasheet1`.

### 3.3 Modality 3 — Laboratory Assays (`L`) & Incorporation Bias
- **`DS0002`:** `Troponine - I (Q)` is populated for `385/581` (`66.3%`; missing `196` -> strong clinical ordering MNAR pattern!). Since Acute Coronary Syndrome (`ACS=57`) / `MI=9` diagnosis depends heavily on Troponin-I elevation, `STEP-014` (`Endpoint Charter`) MUST define an explicit sensitivity tier excluding Troponin-I to prevent incorporation bias (`OS §5.1`). Renal/hepatic/ABG panels show high genuine missingness (`128` Cr to `561` Total Bilirubin).
- **`DS0003`:** `TC, HDL, LDL, FBS` all stored explicitly in `mg/dL` with `67–80` missing values (`4.4–5.2%`), suitable for post-split MICE/median imputation + binary MNAR missingness masks.
- **`DS0004`:** Coarse ordinal `cholesterol` (`1, 2, 3`) and `gluc` (`1, 2, 3`), `0` missing; never harmonized blindly as raw `mg/dL`.

### 3.4 Modality 4 — Lifestyle (`S`)
- **`DS0003` (`CAIR-CVD-2025`):** Rich categorical lifestyle coverage (`Smoking Status`: `Y=789, N=740`; `Physical Activity Level`: `High=521, Moderate=512, Low=496`; `Family History of CVD`), `0` missing categoricals.
- **`DS0004` (`sulianova`):** Binary self-reported lifestyle factors (`smoke=6,169`, `alco=3,764`, `active=56,261`), `0` missing.
- **`DS0001` & `DS0002`:** Zero lifestyle attributes present (`100%` `[MISSING_LIFESTYLE]` — even `DS0002` `Previous diseases` contains `0` smoking/alcohol strings across `301` filled rows).
