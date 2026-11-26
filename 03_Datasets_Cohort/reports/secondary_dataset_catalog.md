# Curated Secondary Public & Kaggle Dataset Catalog (`DEC0004` — Option B)

| Metadata | Value |
|---|---|
| Document | `03_Datasets_Cohort/reports/secondary_dataset_catalog.md` |
| Version | v1.0.0 |
| Step | STEP-010 / `DEC0004` Dataset Selection (`feeds STEP-011`) |
| Authors | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Reviewer | Md. Mizanur Rahman |
| Target Raw Storage (`.gitignore`) | `03_Datasets_Cohort/raw/` (Tier 2B — NEVER committed to Git) |
| Helper Automation | [prepare_secondary_intake.py](../../14_Automation/prepare_secondary_intake.py) |

---

## 1. Open Public Datasets Audited in Our 42 Curated Papers (`P0001–P0042`)

Every `Public Open` dataset appearing inside the 42 included studies was checked for Kaggle/Mendeley/PhysioNet open availability and modality fitness (`note: MIMIC-IV, EchoNext, ARIC, and UK Biobank are excluded here because they require PhysioNet CITI/DUA, BioLINCC, or paid UKB MTA`):

| Dataset Name | Paper ID(s) | Sample Size & Provenance | Modalities Present | Kaggle / Open Host | Option B Decision |
|---|---|---|---|---|---|
| **`PTB-XL`** (`SITE0001`) | `P0014`, `P0016` | `21,837` 12-lead 10s WFDB ECGs (`500/100 Hz`), `18,885` pts, Germany (`CC BY 4.0`) | **Raw 12-lead ECG** + Clinical (`age, sex, height, weight`, SCP diagnoses); **0 Labs, 0 Lifestyle** | **Kaggle:** `kaggle.com/datasets/khyeh0719/ptb-xl-dataset` (`PhysioNet` canonical) | ✅ **KEEP (Primary Raw ECG + Pretraining)** |
| **`CAIR-CVD-2025`** (`SITE0007`) | `P0022` | `1,529` pts from **Jamalpur Medical College Hospital, Bangladesh** (`CC BY 4.0`) | **Clinical** + **Labs** (`Chol, HDL, LDL, FBS, DM`) + **Lifestyle** (`Smoking, Activity, FamHx`); **0 Raw ECG** | **Mendeley (`10.17632/d9scg7j8fp.1`)** & Kaggle search | ✅ **KEEP (BD `C+L+S` Missing-ECG Branch)** *(Fixes `P0022` leak!)* |
| **`Khan ECG Images`** (`SITE0008`) | `P0028` | `929` pts / `11,148` scanned ECG images (`4` classes; **0 patient meta**) | **Raster ECG Images ONLY** (0 Clinical/Lab/Lifestyle) | Kaggle mirrors & Mendeley | ⚠️ **Optional Secondary ECG Image Test Only** (`PROBAST` patient split caveat) |
| **`UCI Heart Disease`** (`Cleveland / Hungary`) | `P0022` | `303`–`918` rows; classic tabular clinical + scalar resting ECG category | Clinical + Chol/FBS + **scalar `restecg/oldpeak` ONLY** (0 waveforms, 0 Lifestyle) | Widely on Kaggle (`Heart Disease Dataset`) | ⚠️ **Tabular Baseline Comparator Only** (Too small / scalar ECG only) |
| **`MITHSDB / CinC 2016`** | `P0004`, `P0015` | `121`–`388` synchronized single-lead ECG + PCG recordings | **1L ECG + Heart Sound (PCG)** only | PhysioNet Open / Kaggle mirrors | ❌ **Exclude** (PCG only; 0 Clinical/Lab/Lifestyle) |
| **`PulseDB` (`MIMIC-III + VitalDB`)** | `P0006` | Paired 10s PPG + single-lead ECG waveforms | **1L ECG + PPG** only | PhysioNet / GitHub / Kaggle mirrors | ❌ **Exclude** (No Lab/Lifestyle; 1L ECG+PPG) |
| **`PhysioNet CVES`** | `P0032` | `64` subjects (`2L ECG, EMG, BP, Resp`) | Physiological signals only (chronic stroke) | PhysioNet Open | ❌ **Exclude** (Tiny N, stroke signals only) |
| **`CODE-15%`** | `P0033` | `15%` subset of Brazilian `CODE` 12-lead ECGs + `age, sex, survival` | **12L ECG** + mortality target only | Zenodo Open (`CC BY 4.0`) | ⚠️ **Optional Pretraining Only** (0 Lab/Lifestyle) |

---

## 2. Recommended **Option B** Multi-Cohort Bundle (Open `Kaggle` + `Mendeley CC BY 4.0`)

To satisfy all 4 title modalities (`Clinical + ECG + Laboratory + Lifestyle`) **without fabricating fake merged patients** (`Zero-Stitching Rule`, `DEC0004`), combine these **5 verified open datasets** using a **Missing-Modality Cross-Attention Transformer**:

| Raw Slot (`03_Datasets_Cohort/raw/`) | Dataset (`SITE####`) | Download URL (Open License) | Modality Role in Our Pipeline | Mandatory `STEP-012/013` Audit Check |
|---|---|---|---|---|
| **`DS0001_ptbxl`** | **`PTB-XL`** (`SITE0001`, `21,837` recs / `18,885` pts) | [Kaggle: khyeh0719/ptb-xl-dataset](https://www.kaggle.com/datasets/khyeh0719/ptb-xl-dataset) or [PhysioNet PTB-XL](https://physionet.org/content/ptb-xl/) | **`E + C` Digital Waveform Anchor:** Raw 10s 12-lead ECGs (`500 Hz`) + age/sex/BMI + patient-stratified folds (`strat_fold 1–10`) for Tier 1 ECG models & `UD26` pretraining | Verify patient-stratified official folds (`1–8` train, `9` val, `10` test; no record overlap!) |
| **`DS0002_chapman`** | **`Chapman-Shaoxing 12L ECG`** (`SITE0011`, `10,646+` pts) | [Kaggle: chapman-shaoxing-12-lead-ecg-database](https://www.kaggle.com/datasets/erarayamorenzomuten/chapman-shaoxing-12-lead-ecg-database) | **`E + C` External Asian Cohort Generalization:** `500 Hz` 12-lead `.hea/.mat` + age/sex from Shaoxing Hospital (China) for cross-hospital shift (`RQ4`) | Verify `50 Hz` vs `60 Hz` noise, lead ordering compatibility with `PTB-XL`, adult age $\ge 18$ |
| **`DS0003_cardiomled`** | **`CARDIO-ML-ED`** (`SITE0009`, `574` ED pts) | [Mendeley DOI: 10.17632/zfszfmpb82.2](https://data.mendeley.com/datasets/zfszfmpb82/2) | **`C + E + L` Same-Patient Primary Multimodal Anchor:** Digitized 12-lead ECG images + `82` structured Clinical/Lab features (`Troponin-I, CBC, ABG, CRP, Coag, History`) on same patients (`UD26` Tier B) | **MUST:** filter age $\ge 18$ (`6–98` range!), inspect outcome labels & exclude incorporation-biased troponin in sensitivity runs (`OS §5.1`) |
| **`DS0004_cair_cvd_2025`** | **`CAIR-CVD-2025`** (`SITE0007`, `1,529` BD pts) | [Mendeley DOI: 10.17632/d9scg7j8fp.1](https://data.mendeley.com/datasets/d9scg7j8fp/1) *(or Kaggle search `"CAIR-CVD-2025"`)* | **`C + L + S` Bangladeshi Missing-ECG Branch:** Clinical + Cholesterol/HDL/LDL/FBS + **Smoking/Physical Activity/Family History** (`RQ2` Lifestyle + South Asian branch via `[MISSING_ECG]`) | Audit post-split strictly (`zero` pre-split SMOTE unlike `P0022`!); verify non-synthetic real distributions |
| **`DS0005_sulianova_cvd`** | **`Cardiovascular Disease`** (`SITE0012`, `70,000` pts) | [Kaggle: sulianova/cardiovascular-disease-dataset](https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset) | **`C + L + S` Large-Scale Lifestyle LOMO Power (`RQ2`):** `70,000` adults with Clinical + Cholesterol/Glucose + **Smoking/Alcohol/Physical Activity** (no ECG) | Audit & quarantine physiological BP outliers (`ap_hi <= ap_lo`, extreme heights/weights) strictly via deterministic pre-split rules; check duplicates |
| **`DS0006_framingham`** | **`Framingham Heart Study`** (`SITE0013`, `~4,240` pts) | [Kaggle search: Framingham Heart Study CSV](https://www.kaggle.com/datasets?search=framingham+heart+study) | **`C + L + S` Longitudinal 10-Yr CHD + Tier 2 Benchmark:** Classic clinical risk baseline (`totChol, glucose, cigsPerDay`) | Clean missing rows strictly inside training folds (`STEP-021`) |

> [!CAUTION]
> **Explicitly Rejected / Suspect Kaggle Entries (`RISK0010`):**
> Do **NOT** download `zara2099/multimodal-cardiovascular-risk-dataset` (or random Kaggle ZIPs claiming *"Multimodal CVD with ECG Images + Troponin + MI/History of MI/Abnormal Heartbeat"*) without verifiable hospital IRB/author provenance — those 4 classes mirror Khan et al. (`P0028`), which publicly published ECG images **without** clinical/lab tables! Always use the authentic **`CARDIO-ML-ED` (`10.17632/zfszfmpb82.2`)** directly from Mendeley Data instead!

---

## 3. How to Collect Them Locally Right Now (`STEP-011` $\rightarrow$ `STEP-012` Handoff)

Because Kaggle requires account authentication (`kaggle.json` API token is not present on this machine), collect the raw files locally into `03_Datasets_Cohort/raw/` (already gitignored!):

### Method A: Fast Kaggle CLI Download (Recommended)
1. On Kaggle (`kaggle.com/settings` $\rightarrow$ **API** $\rightarrow$ **Create New Token**), download `kaggle.json` and place it at `C:\Users\User\.kaggle\kaggle.json`.
2. Install/verify `kaggle` CLI in your data environment (`pip install kaggle`) and run:
```powershell
python 14_Automation/prepare_secondary_intake.py --init-dirs
kaggle datasets download -d khyeh0719/ptb-xl-dataset -p e:\FYDP\03_Datasets_Cohort\raw\DS0001_ptbxl --unzip
kaggle datasets download -d erarayamorenzomuten/chapman-shaoxing-12-lead-ecg-database -p e:\FYDP\03_Datasets_Cohort\raw\DS0002_chapman --unzip
kaggle datasets download -d sulianova/cardiovascular-disease-dataset -p e:\FYDP\03_Datasets_Cohort\raw\DS0005_sulianova_cvd --unzip
```
3. Download **`CARDIO-ML-ED`** directly from [Mendeley DOI 10.17632/zfszfmpb82.2](https://data.mendeley.com/datasets/zfszfmpb82/2) into `03_Datasets_Cohort\raw\DS0003_cardiomled\`, and **`CAIR-CVD-2025`** from [Mendeley DOI 10.17632/d9scg7j8fp.1](https://data.mendeley.com/datasets/d9scg7j8fp/1) into `03_Datasets_Cohort\raw\DS0004_cair_cvd_2025\`.

### Method B: Manual Browser Download
Download directly from the browser links in Section 2 into the matching `03_Datasets_Cohort\raw\DS000#_*` subfolders (`create folders first via python 14_Automation/prepare_secondary_intake.py --init-dirs`).

After placing files inside `03_Datasets_Cohort\raw\`, run:
```powershell
python 14_Automation/prepare_secondary_intake.py --manifest
```
to verify zero Git exposure and generate SHA-256 checksums for `STEP-012`!
