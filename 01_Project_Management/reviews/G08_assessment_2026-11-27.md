# G08 Assessment — Preprocessing Integrity, ECG Filter Fidelity & Prepared Release (`REL0001`)

| Field | Value |
|---|---|
| TemplateID | T22 (gate_audit.md) |
| template_version | v1.0.0 |
| AssessmentID | `G08-20261127-01` |
| GateID | `G08` |
| DocumentOrEntityScope | `REL0001`, `PP0001`, `03_Datasets_Cohort/releases.csv`, `03_Datasets_Cohort/reports/REL0001_manifest_summary.md`, `05_Preprocessing_Alignment/reports/PP0001.md`, `DEC0007.md` |
| EntityVersions | `DS0001–04` v1.0/1.1; `ADJ0001–04` v1.0.0; `SPLIT0001` v1.0.0; `PP0001` v1.0.0; `REL0001` v1.0.0 |
| Outcome | **`NOT ASSESSED`** *(Automated release materialization, lineage verification [`91,781` rows], read-only lock & restore checksum drill, Train-only `PP0001` fit [`0` leakage / `15/15` tests OK], and quantitative WFDB/PNG audits complete; **`PASS` awaits Cardiologist/Clinical ST-T morphology review & `DEC0007` (`UD12`) sign-off**)* |
| Assessor | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Human Approver | Clinical / ECG Reviewer (`TBD`) + Rayan Ahmed (`Implementer`) + Md. Mizanur Rahman |
| Assessment Date | `2026-11-27` *(Pending Clinical Sign-Off)* |
| Governing References | OS §2, §4, §14.1, §14.2 (`G08`); Blueprint `STEP-021`–`STEP-022` |
| PHI Sensitivity | Tier 1 (Public / Git-safe governance audit; `REL0001` JSONLs locked in gitignored Tier 2B) |

---

## 1. Mandatory Criteria Audit Matrix (`OS §14.2 G08`)

| Criterion # | Mandatory Criterion | Evidence Path & Verified Checksums | Automated / Documentary Audit | Corrective Action |
|---|---|---|---|---|
| **C1** | **Raw & Adjudicated Inputs Untouched (`DS -> ADJ`):** Parent SHA-256 digests unchanged before/after processing. | `05_Preprocessing_Alignment/reports/PP0001.md`, `03_Datasets_Cohort/reports/REL0001_manifest_summary.md` | **PASS** (`0` byte mutation across `DS0001–04`, `ADJ0001–04`, `variables.csv`, `SPLIT0001`) | None |
| **C2** | **Train-Only Preprocessing Fit & Leakage Guards (`OS §4.4`):** Stage B fitted strictly on Train (`FitStateHash`), MNAR `_isnan` verified, `inv_err <= 4.55e-13`, `0` NaN/Inf. | `src/cvd_mm/preprocessing.py`, `tests/test_preprocessing_leakage.py`, `PP0001` | **PASS** (`MasterFitStateHash = d9ccfbf40b2b...`; `15/15` tests PASS) | None |
| **C3** | **Count Reconciliation & Immutable Lock (`STEP-022`):** Zero dropped/duplicate encounters across `93,947 -> 91,781 -> REL0001`, read-only locked + restore checksum PASS. | `14_Automation/materialize_release.py`, `releases.csv` (`ManifestHash = 7be9fa07a627...`) | **PASS** (`66,338 Tr / 12,724 Va / 12,719 Te = 91,781`, `89,005` unique patient groups) | None |
| **C4** | **Quantitative ECG & Paper Grid Telemetry:** `<=0.5 Hz` HP + `50 Hz` notch (`fs > 120 Hz`) + `100%` PNG red-grid suppression quantified cleanly. | `PP0001.md` §4 (`N=25` WFDB `0 ms` local QRS lag `20/25`; `N=10` PNG `100%` red-grid removal / `100%` ink preserved) | **PASS (`Technical`)** | Pending clinical eye verification. |
| **C5** | **Cardiologist / Clinical Morphology Review & `DEC0007` (`UD12`) Sign-Off:** External clinical reviewer confirms raw-vs-filtered ECG overlays preserve diagnostic ST-T/Q/P morphology. | [DEC0007.md](../decision_log/DEC0007.md), Kaggle `Cell 6` Plots | **AWAITING CLINICAL APPROVAL** | Obtain clinical/cardiologist inspection sign-off on ECG morphology plots -> promote `G08` to **`PASS`**. |

---

## 2. Determination & Unblocking Path
- **Overall Outcome:** **`NOT ASSESSED`** *(`REL0001` prepared release is cryptographically locked and reconciled cleanly across all `4` cohorts; confirm `G07`/`DEC0008` + `G08`/`DEC0007` Cardiologist ECG morphology sign-off prior to Stage `S10` qualifying runs at `G09`–`G10`).*
