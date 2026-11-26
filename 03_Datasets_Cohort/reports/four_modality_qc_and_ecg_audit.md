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

Across the **4 local secondary datasets** (`93,947` total encounter rows across `PTB-XL`, `CARDIO-ML-ED`, `CAIR-CVD-2025`, and `Kaggle sulianova`), automated verification revealed high data integrity in **`DS0001` (`PTB-XL`)** and **`DS0003` (`CAIR-CVD-2025`)**, deterministic cleanable anomalies in **`DS0004` (`sulianova`)**, and **one critical Gate `G04` blocker (`RISK0011`)** in **`DS0002` (`CARDIO-ML-ED`)**:

1. **`BLOCKER — DS0002 ECGS/ Directory Absent Locally (RISK0011)`:** While `Datasheet1 (Edited).csv` (actually an XLSX workbook) and `ECG Labels.csv` (`408` rows) are present, the actual **12-lead ECG PNG image folder (`ECGS/`)** referenced in `README.txt` (`https://drive.google.com/drive/folders/1u1jzVb8r2Rekel5BSrZ2moNMh-56DKiL?usp=drive_link`) is **NOT present on disk**. Therefore, same-patient `C + E_img + L` linkage cannot yet be verified, PNG readability/burned-in PHI inspection cannot run, and Gate **`G04`** evaluates honestly as **`NOT ASSESSED`** until researchers either download `ECGS/` and pass inspection OR switch the same-patient anchor to PhysioNet Option A (`MIMIC-IV-Ext-MDS-ED`).
2. **Supervisor Approval (`DEC0004`):** Written approval from Md. Mizanur Rahman ratifying secondary-data scope shift (`RF09`) remains pending (`G01`/`G03`/`G04`).

---

## 2. Multi-Cohort 4-Modality Coverage & Anti-Stitching Matrix (`DEC0004`)

| Cohort | Clinical (`C`) | 12-Lead ECG (`E`) | Laboratory (`L`) | Lifestyle (`S`) | Same-Patient Overlap Role |
|---|---|---|---|---|---|
| **`DS0001`** (`PTB-XL`, `N=21,837` ECGs / `18,885` pts) | ⚠️ Partial (`age, sex, height, weight, SCP`) | ✅ **Raw Digital WFDB (`100/500 Hz`)** | ❌ `0%` (`[MISSING_LAB]`) | ❌ `0%` (`[MISSING_LIFESTYLE]`) | Unimodal ECG Tier 1 benchmark & `UD26` waveform pretraining |
| **`DS0002`** (`CARDIO-ML-ED`, `N=581` rows / `569` unique IDs) | ✅ ED Vitals, Demog, Triage | 🚫 **`ECGS/` PNGs Missing Locally** (`408` labels only) | ✅ `61`-col ED panels (`CBC, CMP, Trop-I, ABG, CRP`) | ❌ `0%` (`[MISSING_LIFESTYLE]`; `0` smoking/alcohol in history) | Intended `C+E_img+L` same-patient anchor (**blocked on `ECGS/`**) |
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
  - `ECG Labels.csv` contains `408` annotations (`286 Non-cardiac`, `44 Ischemia`, `11 Tachycardia`, `8 Myocardial infarction`, etc.), of which `343` match `Col1` hospital IDs once multi-ECG `-1`/`-2` suffixes are stripped.
  - **Missing Media (`FAIL` Condition for `G04`):** Zero PNG ECG images exist locally on disk (`ECGS/` absent). Must download from Mendeley author Drive archive and verify zero burned-in hospital IDs/names before `G04` PASS.

### 3.3 Modality 3 — Laboratory Assays (`L`) & Incorporation Bias
- **`DS0002`:** `Troponine - I (Q)` is populated for `385/581` (`66.3%`; missing `196` -> strong clinical ordering MNAR pattern!). Since Acute Coronary Syndrome (`ACS=57`) / `MI=9` diagnosis depends heavily on Troponin-I elevation, `STEP-014` (`Endpoint Charter`) MUST define an explicit sensitivity tier excluding Troponin-I to prevent incorporation bias (`OS §5.1`). Renal/hepatic/ABG panels show high genuine missingness (`128` Cr to `561` Total Bilirubin).
- **`DS0003`:** `TC, HDL, LDL, FBS` all stored explicitly in `mg/dL` with `67–80` missing values (`4.4–5.2%`), suitable for post-split MICE/median imputation + binary MNAR missingness masks.
- **`DS0004`:** Coarse ordinal `cholesterol` (`1, 2, 3`) and `gluc` (`1, 2, 3`), `0` missing; never harmonized blindly as raw `mg/dL`.

### 3.4 Modality 4 — Lifestyle (`S`)
- **`DS0003` (`CAIR-CVD-2025`):** Rich categorical lifestyle coverage (`Smoking Status`: `Y=789, N=740`; `Physical Activity Level`: `High=521, Moderate=512, Low=496`; `Family History of CVD`), `0` missing categoricals.
- **`DS0004` (`sulianova`):** Binary self-reported lifestyle factors (`smoke=6,169`, `alco=3,764`, `active=56,261`), `0` missing.
- **`DS0001` & `DS0002`:** Zero lifestyle attributes present (`100%` `[MISSING_LIFESTYLE]` — even `DS0002` `Previous diseases` contains `0` smoking/alcohol strings across `301` filled rows).
