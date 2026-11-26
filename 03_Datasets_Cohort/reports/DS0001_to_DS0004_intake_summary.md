# Cohort Intake Summary (`DS0001`–`DS0004` — `STEP-012`)

| Metadata | Value |
|---|---|
| Document | `03_Datasets_Cohort/reports/DS0001_to_DS0004_intake_summary.md` |
| Version | v1.0.0 |
| Step | `STEP-012` (Controlled Secondary Cohort Intake & Immutable SHA-256 Lock) |
| Date | `2026-11-26` |
| Owners | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |
| Reviewer | Md. Mizanur Rahman (Supervisor) |
| PHI Sensitivity | Tier 1 (Public / Git-safe hashes & aggregate counts only; `Dataset/` and `raw/` strictly `.gitignore`d) |

---

## 1. Canonical Dataset ID Mapping (`DS0001`–`DS0004`)

Following OS Appendix A (`serial zero-padded IDs`) while mapping cleanly to the 4 folders downloaded by the team into `e:\FYDP\Dataset\` (replacing the skipped reserve slot `2. DS0002_chapman`):

| Canonical ID | SiteID | Local Gitignored Folder (`e:\FYDP\Dataset\...`) | Manifest CSV (`03_Datasets_Cohort/manifests/`) | Manifest CSV SHA-256 | Files / Disk Size |
|---|---|---|---|---|---|
| **`DS0001`** | `SITE0001` | `1. DS0001_ptbxl (PTB-XL, Kaggle)\ptb-xl-a-large-publicly-available-electrocardiography-dataset-1.0.1` | [DS0001_ptbxl_metadata_manifest.csv](../manifests/DS0001_ptbxl_metadata_manifest.csv) | `2052c00f19e556fad43994af033b4b9510709f65dea42ede43fd17e17b7a770f` | `87,354` files (`87,353` verified against vendor `SHA256SUMS.txt`: `2be684997575c9e8a006a6bc15ba0eb89a1b7ddfd585be39c19b103c7eb56ea3`), `3,031.50 MiB` (`0` missing, `0` hash mismatches) |
| **`DS0002`** | `SITE0009` | `3. DS0003_cardiomled (CARDIO-ML-ED, Mendeley Official CC BY 4.0)` | [DS0002_cardiomled_manifest.csv](../manifests/DS0002_cardiomled_manifest.csv) | `8124a7221aeb9d5f3b459e288d0695905fa2e6695974be488c660194b6332c92` | `3` files (`Datasheet1 (Edited).csv` [XLSX bytes], `ECG Labels.csv`, `README.txt`), `491,128` bytes (**`ECGS/` PNG archive missing locally — `RISK0011`**) |
| **`DS0003`** | `SITE0007` | `4. DS0004_cair_cvd_2025 (CAIR-CVD-2025, Mendeley)` | [DS0003_cair_cvd_2025_manifest.csv](../manifests/DS0003_cair_cvd_2025_manifest.csv) | `b77ea5fb25fd8ac88c92849e4ecf65f260c080ae1c50919994841e41721f5f00` | `1` file (`CVD Dataset.csv`), `167,325` bytes |
| **`DS0004`** | `SITE0012` | `5. DS0005_sulianova_cvd (Cardiovascular Disease, Kaggle)` | [DS0004_sulianova_cvd_manifest.csv](../manifests/DS0004_sulianova_cvd_manifest.csv) | `dad4750462cf6a37d1cc243aa18ac8f37870846c8fcdbce17e39786c2a46793e` | `1` file (`cardio_train.csv`), `2,941,524` bytes |

> [!NOTE]
> `SITE0011` (`Chapman-Shaoxing`) and `SITE0013` (`Framingham`) from `DEC0004 Option B` were **not downloaded** in this local batch and remain recorded in [sites.csv](../sites.csv) as `Reserve_NotDownloaded`.

---

## 2. Quantitative Intake Reconciliation & Modality Coverage

| `DS####` | Patients | Records / Encounters | Key Outcome / Event Count | Modalities Available | Complete 4-Modality Patients | Intake Status |
|---|---|---|---|---|---|---|
| **`DS0001`** (`PTB-XL`) | `18,885` unique `patient_id` | `21,837` 10s 12L ECGs (`100 Hz` & `500 Hz` WFDB) | `12,306` non-NORM diagnostic (`MI: 5,486`, `STTC: 5,123`, `HYP: 2,655`, `CD: 4,907`), `9,111` NORM-only, `420` uncoded | `ECG` (raw digital) + `Clinical` (age, sex, height, weight, SCP codes) | `0` | **Complete & Hash-Verified** |
| **`DS0002`** (`CARDIO-ML-ED`) | `569` unique `Col1` IDs (`12` repeated rows) | `581` ED rows (`565` age $\ge 18$, `12` `<18`, `4` missing age); `408` ECG label rows (`343` Base-ID match) | `346` Initial `Cardiac` / `233` `Noncardiac`; `196` specific cardiac/electrolyte Final diagnoses (`57` ACS, `9` MI, `7` arrest, `64` HTN crisis, `24` elev BP, `18` arrhythmia, `17` elec); `10` inpatient deaths | `Clinical` + `61`-col `Lab` + `ECG Labels` *(raw `ECGS/` PNG images absent locally)* | `0` | **Partial Blocker (`RISK0011`)** |
| **`DS0003`** (`CAIR-CVD-2025`) | `1,529` (`0` exact duplicate rows) | `1,529` adult BD records (`25.0–79.0 y`) | `728` `HIGH`, `581` `INTERMEDIARY`, `220` `LOW` Risk Level | `Clinical` + `Lab` (`TC, HDL, LDL, FBS`) + `Lifestyle` (`Smoking, Activity, FamHx`) | `0` (`0` ECG) | **Complete & Hash-Verified** |
| **`DS0004`** (`sulianova CVD`) | `70,000` IDs (`24` exact duplicate feature+label rows) | `70,000` checkup records (`29.6–64.9 y`) | `34,979` `cardio=1` (`49.97%`), `35,021` `cardio=0` | `Clinical` + `Lab` (3-level `cholesterol`, `gluc`) + `Lifestyle` (`smoke, alco, active`) | `0` (`0` ECG) | **Complete (Flagged Outliers)** |

---

## 3. Immutable Storage & Git-Exposure Verification

1. **Read-Only Raw Rule (`OS §4.2`):** All files under `e:\FYDP\Dataset\` are governed as immutable input archives verified cryptographically against the manifests in [03_Datasets_Cohort/manifests/](../manifests/). Any deterministic filtering (`age >= 18`, outlier quarantining, XLSX unpacking) will write cleanly to gitignored derived workspaces during Stage `S09` (`STEP-021`), never mutating source files.
2. **Git Security Audit:** `.gitignore` explicitly blocks `Dataset/`, `dataset/`, `Datasets/`, `datasets/`, `raw/`, `*.dat`, `*.hea`, `*.zip`, `*.tar.gz`, and `*.7z`. Zero raw data rows or patient records are committed to Tier 1 Git.
3. **Zero-Stitching Enforced:** Across all 4 cohorts, zero patients span multiple `DS####` archives (`Complete4ModalityCount = 0`). The pipeline models each cohort cleanly via native modality masks under `DEC0004` (`Missing-Modality Multi-Cohort Architecture`).
