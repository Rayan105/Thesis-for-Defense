# G04 Assessment — Secondary Cohort Intake, Ethics Provenance & Four-Modality Quality

| Field | Value |
|---|---|
| TemplateID | T22 (gate_audit.md) |
| template_version | v1.0.0 |
| entity_id | G04-20261126-01 |
| owner | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |
| date | 2026-11-26 |
| status | Open (`NOT ASSESSED — Blocked on DS0002 ECGS/ Download & Supervisor DEC0004 Sign-Off`) |
| source_inputs | `03_Datasets_Cohort/sites.csv`, `03_Datasets_Cohort/datasets.csv`, `03_Datasets_Cohort/irb_permissions/SITE0001.md`, `SITE0007.md`, `SITE0009.md`, `SITE0012.md`, `03_Datasets_Cohort/manifests/*.csv`, `03_Datasets_Cohort/reports/DS0001_to_DS0004_intake_summary.md`, `03_Datasets_Cohort/reports/four_modality_qc_and_ecg_audit.md`, `03_Datasets_Cohort/reports/cohort_cards_DS0001_to_DS0004.md`, `01_Project_Management/decision_log/DEC0004.md` |
| governing_section | OS §4.1–§4.3, §11, §14.1, §14.2 (`G04`); Blueprint `STEP-011`–`STEP-013` |
| phi_sensitivity | Tier 1 (Public / Git-safe governance audit) |
| reviewer | Md. Mizanur Rahman (Supervisor) |

---

# G04 Assessment — Cohort Intake & Four-Modality Quality (`v1.0.0`)

| Field | Value |
|---|---|
| AssessmentID | `G04-20261126-01` |
| GateID | `G04` |
| DocumentOrEntityScope | `DS0001` (`PTB-XL`), `DS0002` (`CARDIO-ML-ED`), `DS0003` (`CAIR-CVD-2025`), `DS0004` (`Kaggle sulianova`), `sites.csv`, `datasets.csv`, `irb_permissions/SITE*.md` |
| EntityVersions | `sites.csv` v1.2.0; `datasets.csv` v1.0.0; `DS0001_to_DS0004_intake_summary.md` v1.0.0; `four_modality_qc_and_ecg_audit.md` v1.0.0; `cohort_cards_DS0001_to_DS0004.md` v1.0.0 |
| Outcome | **`NOT ASSESSED`** *(Automated hashing & QC complete with clean quarantines; transitions blocked by missing `DS0002 ECGS/` image archive locally [`RISK0011`] and unsigned Supervisor `DEC0004` approval)* |
| Assessor | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |
| Human Approver | Md. Mizanur Rahman (Supervisor, Senior Lecturer, Dept. of CSE, DIU) |
| Assessment Date | `2026-11-26` *(Pending ECGS/ Resolution & Human Sign-Off)* |

---

## 1. Mandatory Criteria Audit Matrix (`OS §14.2 G04`)

| Criterion # | Mandatory Criterion | Required Evidence Path | Current Evidence State & SHA-256 Checksum | Automated / Documentary Audit | Corrective Action Required |
|---|---|---|---|---|---|
| **C1** | **Ethics/IRB exemption, source licensing & secondary provenance (`STEP-011`):** Documented open licenses (`CC BY 4.0` / Kaggle open terms), parent hospital origins, consent waivers, and anti-stitching rules. | `03_Datasets_Cohort/irb_permissions/SITE0001.md`, `SITE0007.md`, `SITE0009.md`, `SITE0012.md`, `sites.csv`, `DEC0004.md` | `SITE0001.md`: `5ad992df2181e6402c426754593e7f82a658b08d1c90fdf3686958fd152e6cfe`<br>`SITE0007.md`: `50775a533eb01c2a3ac675d59106dd5455450d33db573e3ab8d850dcb10f6d54`<br>`SITE0009.md`: `b4a400128b6608c015b6dcbd5ca64c473ac363ccea56a1ded9d7cfc1eb7bd915`<br>`SITE0012.md`: `3687775c8175edab3a8936ee4ab3d34fdb8f6844737814ddc228a4415939d99e`<br>`sites.csv`: `b037cc6f4395ecf15c6e54b4c9c0fdea05b8c50ea33bb601128c1b760efeec1c`<br>`DEC0004.md`: `0c5b1e3be09564a729f9097568c2c300cc610c2ddc1d85e56c339266e9fb9d64` | **EVIDENCE PREPARED (AWAITING SUPERVISOR DEC0004)** | Obtain Md. Mizanur Rahman signature on `DEC0004.md` ratifying secondary-data scope (`RF09`). |
| **C2** | **EPV feasibility & zero cross-patient stitching (`UD04/UD26`):** Reconciled sample counts honoring `UD26` Tier limits without row-stitching unrelated cohorts. | `03_Datasets_Cohort/datasets.csv`, `03_Datasets_Cohort/reports/feasibility_epv_study.md`, `DEC0004.md` | `datasets.csv`: `59bbb3d302f4c552772d42918226a73e904edb0abc8385d93afe346105039ac`<br>`DS0001`: `18,885` pts / `21,837` ECGs; `DS0002`: `569` unique IDs / `581` rows (`565` $\ge 18$y); `DS0003`: `1,529` pts; `DS0004`: `70,000` rows. `Complete4ModalityCount=0` enforces missing-modality architecture honestly. | **PASS (VERIFIED)** | None |
| **C3** | **Immutable raw intake lock & SHA-256 verification (`STEP-012`):** Complete cryptographic manifests of all local datasets without exposing raw data to Git. | `03_Datasets_Cohort/manifests/*.csv`, `DS0001_to_DS0004_intake_summary.md` | `DS0001_ptbxl_metadata_manifest.csv`: `2052c00f19e556fad43994af033b4b9510709f65dea42ede43fd17e17b7a770f` (+ vendor `SHA256SUMS.txt`: `2be684997575c9e8a006a6bc15ba0eb89a1b7ddfd585be39c19b103c7eb56ea3` verifying `87,353` files, `0` missing, `0` mismatch)<br>`DS0002_cardiomled_manifest.csv`: `8124a7221aeb9d5f3b459e288d0695905fa2e6695974be488c660194b6332c92`<br>`DS0003_cair_cvd_2025_manifest.csv`: `b77ea5fb25fd8ac88c92849e4ecf65f260c080ae1c50919994841e41721f5f00`<br>`DS0004_sulianova_cvd_manifest.csv`: `dad4750462cf6a37d1cc243aa18ac8f37870846c8fcdbce17e39786c2a46793e`<br>`DS0001_to_DS0004_intake_summary.md`: `42587b2b223a82ead0fecc9dd608c99da2d157ceb8fea6d98e2d3f22a6fd485a` | **BLOCKER (`DS0002 ECGS/` MISSING)** | Researchers download `ECGS/` PNG archive from Mendeley Drive (`README.txt`), compute SHA-256 manifest, OR re-scope `DS0002` via Option A (`MIMIC-IV-Ext-MDS-ED`). |
| **C4** | **PHI de-identification & `.gitignore` storage isolation (`OS §4.2, §11`):** Zero patient identifiers in filenames, headers, or Git staging. | `.gitignore`, `03_Datasets_Cohort/reports/four_modality_qc_and_ecg_audit.md` | `0` `#` PHI comments across all `43,674` PTB-XL `.hea` files; `0` files from `Dataset/` or `raw/` tracked/staged in Git (`git status --short` clean). Pending PHI banner audit on `DS0002` ECG PNG images once downloaded. | **PASS (LOCAL FILES) / PENDING `ECGS/` IMAGES** | Run PHI banner spot-check on `DS0002` PNGs after Drive download. |
| **C5** | **Four-modality quality, ECG signal integrity, missingness & Cohort Cards (`STEP-013`):** Automated bounds, duplicate checks, signal flatline/clipping audit, and `T09` cards. | `03_Datasets_Cohort/reports/four_modality_qc_and_ecg_audit.md`, `03_Datasets_Cohort/reports/cohort_cards_DS0001_to_DS0004.md` | `four_modality_qc_and_ecg_audit.md`: `323a3fe5010fb8e0a0abb966bf86bf1c5d79b3897dac477f808f6528453b5f96`<br>`cohort_cards_DS0001_to_DS0004.md`: `c5b80eaa111557d03bfb49dac3fd5461d454abfcd16fab31c6e95643ed763f80`<br>`21,836/21,837` PTB-XL LR clean (`ecg_id=12722` `V5` flatline isolated); `DS0002` XLSX/12 duplicate IDs/12 `<18y` flagged; `DS0003` `65` `SBP<=DBP` flagged; `DS0004` `1,323` BP anomalies & duplicates flagged. | **EVIDENCE PREPARED (PENDING `ECGS/` & CLINICAL SPOT-CHECK)** | Audit `DS0002 ECGS/` PNGs once downloaded + perform qualified ECG clinical spot-check (`OS §4.3`). |
| **C6** | **Dated Supervisor / Custodian / Clinical Human Approval (`OS §14.1`):** Human confirmation of cohort eligibility, license waivers, and signal QC. | Sign-off in `DEC0004.md` & `G04` reassessment | Currently unsigned (`Unresolved / Human Decision Required`). | **AWAITING HUMAN APPROVAL** | Md. Mizanur Rahman + clinical reviewer review `STEP-011`–`013` reports and approve. |

---

## 2. Gate Outcome Determination

- **Overall Outcome:** **`NOT ASSESSED`** *(Documentary & Automated Intake/QC Complete; `PASS` Blocked by `RISK0011` & Human Approval)*
- **Blocking Issues Preventing `PASS`:**
  1. **`DS0002` Missing Raw ECG Images (`RISK0011`):** `CARDIO-ML-ED` currently contains only metadata (`Datasheet1 (Edited).csv` XLSX + `ECG Labels.csv` + `README.txt`) because the team did not fetch the external Google Drive `ECGS/` folder yet (`https://drive.google.com/drive/folders/1u1jzVb8r2Rekel5BSrZ2moNMh-56DKiL?usp=drive_link`). Without the PNG files hashed and checked for readability/PHI, the same-patient `C+E+L` anchor cannot clear `G04`.
  2. **Human Governance Approval (`DEC0004` / `G01` / `G03` / `G04`):** Supervisor Md. Mizanur Rahman has not yet signed off on the secondary-data transition (`DEC0004`) or cohort cards.

---

## 3. Permitted Parallel Work & Reassessment Protocol

- **Blocked Transition (`OS §14.2`):** Production clinical adjudication / label release (`G06`), leakage-safe split locking (`G07`), and preprocessed release locking (`G08`) remain **Blocked** until `G04` transitions to **`PASS`** (via `G04-2026MMDD-02`).
- **Permitted Preparatory Work:** Stage `S07` planning documentation (`STEP-014` Endpoint Charter & `STEP-015` 4-Modality Variable Dictionary definitions, including Troponin-I incorporation-bias tiers and endpoint harmonization across `PTB-XL`, `CARDIO-ML-ED`, `CAIR-CVD-2025`, and `sulianova`) can be drafted provisionally while downloading `ECGS/` and meeting Supervisor Md. Mizanur Rahman.
- **Invalidated Downstream Gates:** None (`G05–G17` remain `Blocked`).
