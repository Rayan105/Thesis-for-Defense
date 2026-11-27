# G07 Reassessment — Deterministic Patient-Grouped Split & Custody Seal (`PASS`)

| Field | Value |
|---|---|
| TemplateID | T22 (gate_audit.md) |
| template_version | v1.0.0 |
| AssessmentID | `G07-20261127-02` |
| GateID | `G07` |
| Supersedes | `G07-20261127-01` |
| DocumentOrEntityScope | `SPLIT0001`, `src/cvd_mm/splitting.py`, `tests/test_splitting.py`, `03_Datasets_Cohort/splits/SPLIT0001/report.md`, `test_access_log.csv`, `DEC0008.md` |
| EntityVersions | `ADJ0001–0004` v1.0.0; `SPLIT0001` v1.0.0; `DEC0008` v1.1.0 |
| Outcome | **`PASS`** *(Confirmation recorded `2026-11-27` for `DEC0008 Option A` [`UD11`]: hybrid official `PTB-XL StratFold 1–8/9/10` + connected `PatientGroupID` `70/15/15` splits across `DS0002–04`, nested `5`-fold Train CV, `0` patient overlap across `91,781` rows / `89,005` groups, bit-for-bit `ManifestSHA256`, and sealed Test custody)* |
| Assessor | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Human Approver | Md. Mizanur Rahman (`Supervisor`) + Rayan Ahmed (`Team-reported confirmation 2026-11-27`) |
| Assessment Date | `2026-11-27` |
| Governing References | OS §4.3–§4.4, §14.1, §14.2 (`G07`); Blueprint `STEP-020` |
| PHI Sensitivity | Tier 1 (Public / Git-safe governance audit) |

---

## 1. Mandatory Criteria Summary (`C1–C5`)
- **`C1` Zero Patient Overlap:** **PASS** (`0` overlap across Train `66,338` / Val `12,724` / Test `12,719` and internal Train CV folds; `15/15` unit tests pass).
- **`C2` Deterministic Reproducibility:** **PASS** (`seed=20261127`, `ManifestSHA256=db74cfeb8fed769c6c370e4e3b664b3ca6edc0af1b1ad20fe64e1123892cd3e6`).
- **`C3` Partition Balance & Modality Representation:** **PASS** (`SPLIT0001/report.md` audited cleanly across `DS0001–04`).
- **`C4` Sealed Test Custody & Tier-2B Isolation:** **PASS** (`test_access_log.csv` `TACC0001: SEALED`; `manifest.csv` excluded from Git).
- **`C5` Human Confirmation (`DEC0008 Option A`):** **PASS** (`2026-11-27`).
