# G04 Reassessment — Secondary Cohort Intake, ECGS/ Extraction & Four-Modality Quality (`PASS`)

| Field | Value |
|---|---|
| TemplateID | T22 (gate_audit.md) |
| template_version | v1.0.0 |
| AssessmentID | `G04-20261126-02` |
| GateID | `G04` |
| Supersedes | `G04-20261126-01` |
| DocumentOrEntityScope | `DS0001` (`PTB-XL`), `DS0002` (`CARDIO-ML-ED` + `408` `ECGS/` scans), `DS0003` (`CAIR-CVD-2025`), `DS0004` (`Kaggle sulianova`), `sites.csv`, `datasets.csv`, `irb_permissions/SITE*.md` |
| EntityVersions | `sites.csv` v1.3.0; `datasets.csv` v1.1.0; `SITE0009.md` v1.1.0; `DS0001_to_DS0004_intake_summary.md` v1.1.0; `four_modality_qc_and_ecg_audit.md` v1.1.0; `cohort_cards_DS0001_to_DS0004.md` v1.1.0 |
| Outcome | **`PASS`** *(100% mandatory criteria resolved after extraction/hashing/PHI audit of all `408` `CARDIO-ML-ED ECGS/` images + Supervisor Md. Mizanur Rahman ratification of `DEC0004 Option B` on `2026-11-26`)* |
| Assessor | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |
| Human Approver | Md. Mizanur Rahman (Supervisor, Senior Lecturer, Dept. of CSE, DIU) |
| Assessment Date | `2026-11-26` |
| Governing References | OS §4.1–§4.3, §11, §14.1, §14.2 (`G04`); Blueprint `STEP-011`–`STEP-013` |
| PHI Sensitivity | Tier 1 (Public / Git-safe governance audit) |

---

## 1. Mandatory Criteria Audit Matrix (`OS §14.2 G04`)

| Criterion # | Mandatory Criterion | Evidence Path & Verified SHA-256 Checksum | Automated / Visual Audit | Corrective / Downstream Action |
|---|---|---|---|---|
| **C1** | **Secondary licensing, provenance & ethics exemption (`STEP-011`):** Open `CC BY 4.0`/public releases + Supervisor `DEC0004` sign-off. | `SITE0001.md`: `5ad992df2181e6402c426754593e7f82a658b08d1c90fdf3686958fd152e6cfe`<br>`SITE0007.md`: `50775a533eb01c2a3ac675d59106dd5455450d33db573e3ab8d850dcb10f6d54`<br>`SITE0009.md`: `aa47e5864777707df76f1e7fea63e2f320b5a6c076819cbb7417b82ec14f5548`<br>`SITE0012.md`: `3687775c8175edab3a8936ee4ab3d34fdb8f6844737814ddc228a4415939d99e`<br>`DEC0004.md`: `ad967c0b2c5cb520c631c27d973d8b7fd69aecc24aebd7c49db456311fdefa32` | **PASS** | None |
| **C2** | **EPV feasibility & anti-stitching architecture (`UD04/UD26`):** Reconciled sample sizes with `Complete4ModalityCount=0`. | `datasets.csv`: `8f70f108424e35832aed478f4b3001e404c71ba435dbf2fe1c4e06213cd6d407`<br>`sites.csv`: `d15ae0f9af0d40d0afd04b0220e1e40bca2add9b47c72fbd0a9188906321a16e` | **PASS** | None |
| **C3** | **Immutable raw intake lock & exhaustive SHA-256 verification (`STEP-012`):** `100%` of files across `DS0001–DS0004` hashed. | `DS0001_ptbxl_metadata_manifest.csv`: `2052c00f19e556fad43994af033b4b9510709f65dea42ede43fd17e17b7a770f` (+ vendor `SHA256SUMS.txt` `2be68499...` verifying `87,353` files, `0` errors)<br>`DS0002_cardiomled_manifest.csv`: `ed23c60e51547179d93b3d8623f84e46388bbb9402ea5d0a1b3dd2234fd4bd92` (`411` files [`408` ECGS images + 3 meta], `4,298,236,245` B)<br>`DS0003_cair_cvd_2025_manifest.csv`: `b77ea5fb25fd8ac88c92849e4ecf65f260c080ae1c50919994841e41721f5f00`<br>`DS0004_sulianova_cvd_manifest.csv`: `dad4750462cf6a37d1cc243aa18ac8f37870846c8fcdbce17e39786c2a46793e`<br>`DS0001_to_DS0004_intake_summary.md`: `e617cecba8194fb029d3495d34165b3fa869a82efcf65a7590d61d24204718f7` | **PASS** | None |
| **C4** | **PHI scrubbing & zero Git exposure (`OS §4.2, §11`):** Waveform header audit + ECG image visual PHI banner audit + `.gitignore` verification. | `.gitignore` (`Dataset/`, `raw/`, `*.rar`, `*.dat`, `*.hea`); `0` `#` PHI comments in `43,674` `PTB-XL` headers; visual inspection of `DS0002` `1.png`, `122519.png`, `126035-1.jpg` confirmed `0` patient names/MRNs/phones. | **PASS** | Keep `Dataset/` excluded from Git forever. |
| **C5** | **Four-modality QC, signal/image integrity, missingness & Cohort Cards (`STEP-013`):** Exhaustive checks & actionable quarantine list. | `four_modality_qc_and_ecg_audit.md`: `a52b210c2d50e7f954e054dd86c192e5734b29faf93328e4bd77f6d77fbfaf6b`<br>`cohort_cards_DS0001_to_DS0004.md`: `a4dc076dd77e764f3de577a7635b6c5abc316877165b8c8260a9ff57df760929` | **PASS** | Enforce Stage `S07–S09` rules: exclude `PTB-XL ecg_id=12722` (`V5` flatline), `<18y` subgroups, `DS0002` `8` `.jpg` strips / `2` typo IDs (`RISK0012`), `DS0003` `65` `SBP<=DBP`, `DS0004` BP/BMI/duplicate outliers. |
| **C6** | **Human Custodian/Supervisor Approval (`OS §14.1`):** Named Supervisor sign-off on `DEC0004` + parent dual cardiologist `CARDIO-ML-ED`/`PTB-XL` verification. | `2026-11-26_supervisor_signoff_meeting.md`: `3aee2e73f7de4e4a974a44cc865a07af99e6c7e88dbf235530f85807b0744322` | **PASS** | Engage qualified cardiologist for Stage `S07` (`STEP-014`/`STEP-015` / `G05`). |

---

## 2. Gate Outcome Determination & Unblocked Transition
- **Overall Outcome:** **`PASS`** (`G04-20261126-02` closes Stages `S05–S06` cleanly).
- **Unblocked Next Step:** Advances cleanly to **Stage `S07` / `STEP-014`** (`Define CVD clinical endpoint charter, Troponin-I incorporation-bias sensitivity tiers, and four-modality variable dictionary`).
