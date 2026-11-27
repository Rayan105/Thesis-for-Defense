# G07 Assessment — Deterministic Patient-Grouped Split & Sealed Test Custody (`SPLIT0001`)

| Field | Value |
|---|---|
| TemplateID | T22 (gate_audit.md) |
| template_version | v1.0.0 |
| AssessmentID | `G07-20261127-01` |
| GateID | `G07` |
| DocumentOrEntityScope | `SPLIT0001`, `src/cvd_mm/splitting.py`, `tests/test_splitting.py`, `14_Automation/run_split_generation.py`, `03_Datasets_Cohort/splits/SPLIT0001/report.md`, `split_config.yaml`, `test_access_log.csv`, `DEC0008.md` |
| EntityVersions | `ADJ0001–0004` v1.0.0; `SPLIT0001` v1.0.0; `DEC0008` v1.0.0 |
| Outcome | **`NOT ASSESSED`** *(Automated generation, deterministic reproducibility, balance audit, zero patient overlap [`0` overlaps across `89,005` patient groups / `91,781` encounters], and `test_access_log.csv` seal `100%` complete; **`PASS` awaits Supervisor/Biostatistics ratification of `DEC0008` (`UD11`) and `G07`**)* |
| Assessor | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Human Approver | Md. Mizanur Rahman (`Supervisor`) + Biostatistics Reviewer |
| Assessment Date | `2026-11-27` *(Pending Human Sign-Off)* |
| Governing References | OS §4.3–§4.4, §14.1, §14.2 (`G07`); Blueprint `STEP-020` |
| PHI Sensitivity | Tier 1 (Public / Git-safe governance audit; row-level `manifest.csv` gitignored in Tier 2B) |

---

## 1. Mandatory Criteria Audit Matrix (`OS §14.2 G07`)

| Criterion # | Mandatory Criterion | Evidence Path & Verified Checksums | Automated / Documentary Audit | Corrective Action |
|---|---|---|---|---|
| **C1** | **Zero Patient / Group / Duplicate Overlap (`OS §4.4`):** `train`, `val`, `test`, and internal Train `5`-fold CV share `0` `PatientGroupID`s. | `src/cvd_mm/splitting.py`, `tests/test_splitting.py`, `SPLIT0001/report.md` | **PASS** (`train&val=0`, `train&test=0`, `val&test=0`, `cv_fold=0` across `89,005` unique patient groups; `15/15` unit tests OK) | None |
| **C2** | **Bit-for-Bit Seed Reproducibility:** Double generation produces identical `manifest.csv` SHA-256. | `14_Automation/run_split_generation.py`, `SPLIT0001/split_config.yaml` | **PASS** (`seed=20261127`, `ManifestSHA256=db74cfeb8fed769c6c370e4e3b664b3ca6edc0af1b1ad20fe64e1123892cd3e6`) | None |
| **C3** | **Balance & Modality Representation Audit:** Outcome, sex, age, and `[C, E, L, S]` counts reported per partition across `DS0001–DS0004`. | `03_Datasets_Cohort/splits/SPLIT0001/report.md` | **PASS** (`66,338` Tr / `12,724` Va / `12,719` Te; `CVD+` `51.58% / 50.83% / 50.81%`; `DS0002` PNGs `231/50/48`) | None |
| **C4** | **Test Partition Custody Seal Initialized & Tier-2B Isolated:** `manifest.csv` gitignored; `test_access_log.csv` sealed. | `03_Datasets_Cohort/splits/test_access_log.csv`, `.gitignore` (`git status` verified) | **PASS** (`TACC0001: SEALED`; zero `manifest.csv` untracked in Git) | None |
| **C5** | **Human Approval (`UD11` / `OS §14.1 G07`):** Supervisor + Biostatistics Reviewer sign off split geometry (`DEC0008 Option A`) & minor group rounding. | [DEC0008.md](../decision_log/DEC0008.md) | **AWAITING HUMAN APPROVAL** | Confirm `DEC0008 Option A` -> promote `G07` to **`PASS`**. |

---

## 2. Determination & Unblocking Path
- **Overall Outcome:** **`NOT ASSESSED`** *(Automated split generation & overlap audits `100%` clean; confirm `DEC0008` / `G07` approval to unlock **`STEP-021` Train-Only Stage B Fitting & `STEP-022` `REL0001` / `G08`**).*
