# G08 Reassessment — Preprocessing Integrity, ECG Filter Fidelity & `REL0001` Release (`PASS`)

| Field | Value |
|---|---|
| TemplateID | T22 (gate_audit.md) |
| template_version | v1.0.0 |
| AssessmentID | `G08-20261127-02` |
| GateID | `G08` |
| Supersedes | `G08-20261127-01` |
| DocumentOrEntityScope | `REL0001`, `PP0001`, `03_Datasets_Cohort/releases.csv`, `REL0001_manifest_summary.md`, `PP0001.md`, `DEC0007.md` |
| EntityVersions | `DS0001–04` v1.0/1.1; `ADJ0001–04` v1.0.0; `SPLIT0001` v1.0.0; `PP0001` v1.0.0; `REL0001` v1.0.0; `DEC0007` v1.1.0 |
| Outcome | **`PASS`** *(Confirmation recorded `2026-11-27` for `DEC0007 Option A` [`UD12`] & `REL0001` [`91,781` reconciled encounters, read-only locked, restore checksum PASS, `MasterFitStateHash` locked]; External Cardiologist independent bedside/XAI review remains transparently tracked for **`G14`**)* |
| Assessor | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Human Approver | Md. Mizanur Rahman (`Supervisor`) + Rayan Ahmed (`Team-reported confirmation 2026-11-27`; External Cardiologist `TBD` for `G14`) |
| Assessment Date | `2026-11-27` |
| Governing References | OS §2, §4, §14.1, §14.2 (`G08`); Blueprint `STEP-021`–`STEP-022` |
| PHI Sensitivity | Tier 1 (Public / Git-safe governance audit) |

---

## 1. Mandatory Criteria Summary (`C1–C5`)
- **`C1` Raw & Adjudicated Inputs Untouched:** **PASS** (`0` byte mutation across `DS0001–04`, `ADJ0001–04`, `variables.csv`, `SPLIT0001`).
- **`C2` Train-Only Preprocessing & Leakage Guards:** **PASS** (`MasterFitStateHash = d9ccfbf40b2b1cbb500bb4b9d0f5857611c71058f6c98532f288d03e62c0b536`; inverse scaling error `<= 4.55e-13`; `15/15` unit tests OK).
- **`C3` Count Reconciliation & Immutable Lock (`REL0001`):** **PASS** (`93,947 -> 91,781` clean, `ManifestHash = 7be9fa07a6275fbdb99619b6704e38c0bb18a6aeaef3f214749a2344bfa76866`, read-only locked + restore checksum PASS).
- **`C4` Quantitative ECG DSP & PNG Grid Audit:** **PASS** (`500 Hz` `mean_r=0.8946`, `100 Hz` `50 Hz`-notch safe bypass `r=0.8927`, DC offset `0.011 -> 0.001324 mV`, local `0 ms` QRS peak alignment `20/25`; `100.0%` red-grid suppression / `100.0%` ink preserved on `CARDIO-ML-ED` PNGs).
- **`C5` Confirmation (`DEC0007 Option A` & `REL0001`):** **PASS** (`2026-11-27`; independent External Cardiologist co-signature retained openly on schedule for `G14` XAI plausibility).
