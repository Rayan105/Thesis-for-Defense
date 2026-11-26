# G05 Assessment — Clinical Endpoint Charter, 4-Modality Schema, ECG Contract & QA Protocol

| Field | Value |
|---|---|
| TemplateID | T22 (gate_audit.md) |
| template_version | v1.0.0 |
| AssessmentID | `G05-20261127-01` |
| GateID | `G05` |
| DocumentOrEntityScope | `endpoint_charter.md`, `variables.csv`, `crf_manual_v1.0.0.md`, `ecg_contract.md`, `qa_protocol.md`, `src/cvd_mm/schema_ecg.py`, `tests/test_schema_ecg.py`, `DEC0005.md` |
| EntityVersions | `endpoint_charter.md` v1.0.0; `variables.csv` v1.0.0 (`53` rows); `crf_manual_v1.0.0.md` v1.0.0; `ecg_contract.md` v1.0.0; `qa_protocol.md` v1.0.0; `DEC0005.md` v1.0.0 |
| Outcome | **`NOT ASSESSED`** *(100% technical schemas, ECG contracts, prospective QA thresholds, SHA-256 hashes & unit tests (`6/6` pass) prepared and verified; **`PASS` awaits Qualified Cardiologist engagement & Supervisor ratification of `DEC0005` / `G05` per `OS §14.2`**)* |
| Assessor | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Human Approver | Qualified Cardiologist (`TBD` per `scope.md §8.2`) + Md. Mizanur Rahman (`Supervisor`) |
| Assessment Date | `2026-11-27` *(Pending Clinical Sign-Off)* |
| Governing References | OS §5.1–§5.3, §14.1, §14.2 (`G05`); Blueprint `STEP-014`–`STEP-015` |
| PHI Sensitivity | Tier 1 (Public / Git-safe governance audit) |

---

## 1. Mandatory Criteria Audit Matrix (`OS §14.2 G05`)

| Criterion # | Mandatory Criterion | Evidence Path & Verified SHA-256 Checksum | Automated / Documentary Audit | Corrective Action Required |
|---|---|---|---|---|
| **C1** | **Clinical CVD endpoint charter (`endpoint_charter.md`, `UD02–UD03`):** Target definitions, cross-sectional/acute ED horizon honesty, $t_0/\Delta t$, and PROBAST Domain 3 `Troponin-I` (`Tier A` vs `Tier B`) separation. | `04_Outcome_Schema_QA/endpoint_charter.md`: `7a2053325c36e4c725f5207ad385873edacee4ba4c079a9074efad399e9d5c27`<br>`04_Outcome_Schema_QA/crf/crf_manual_v1.0.0.md`: `1adc12b33a925c8dd9925bd2abfd062f50848428f3b8c27640ace8f5980b74de` | **PASS (TECHNICAL EVIDENCE)** | Pending Cardiologist confirmation of borderlines (`DEC0005`). |
| **C2** | **4-Modality variable dictionary (`variables.csv`, `UD08`):** Exact units, bounds, missingness masks, `Family History` placement (`RF10`), and hard target-leakage exclusion rules (`VAR0047–0050`). | `04_Outcome_Schema_QA/variables.csv`: `20f39b7410740c61b7baf81f6235c9d8dc04f80f2fbba15979114073988f3bc8` | **PASS (TECHNICAL EVIDENCE)** | Validate against automated unit suite (`C4`). |
| **C3** | **12-Lead ECG multi-representation contract (`ecg_contract.md`, `UD07`):** Dual WFDB digital (`100/500 Hz`) & cropped `12`-row PNG scan specs, lead ordering (`I–V6`), flatline/saturation rejection (`ecg_id=12722`), red-grid normalization & `8` JPG quarantine (`RISK0012`). | `04_Outcome_Schema_QA/ecg_contract.md`: `975e36f65c01c347ba1f148dbea525089d6c257145070bd27e6f4a88153213c4` | **PASS (TECHNICAL EVIDENCE)** | Confirm `.jpg` isolation policy in `DEC0005`. |
| **C4** | **Prospective pilot QA design & parser unit tests (`qa_protocol.md`, `UD09`):** Locked `N_pilot = 60` stratified protocol, `kappa >= 0.85` / `ICC >= 0.99` before execution, plus automated schema/ECG unit tests. | `04_Outcome_Schema_QA/qa_protocol.md`: `c365ebb2f63530e77be5b3afdc778a92b712acafdbc4e235d59cbf70a3475a20`<br>`src/cvd_mm/schema_ecg.py`: `89d3e280e378a0c8002ec7d1c50f7432743298065ba2d60f44a8c5e68d820339`<br>`tests/test_schema_ecg.py`: `f3c3d5d9aea88f50f8cedfc167927df23be832584a126910a08c5cadbd81e9ee` | **PASS (`6/6` TESTS OK)** | None |
| **C5** | **Named Qualified Cardiologist + Supervisor `G05` approval (`DEC0005`):** Written clinical sign-off authorizing Stage `S08` adjudication/release (`STEP-016`–`018`). | `01_Project_Management/decision_log/DEC0005.md`: `87e0390376ff806e5804d9b73038a9507e6537bb556df82b266b792f1e8b7109`<br>Named Cardiologist in `scope.md §8.2` currently `TBD`. | **AWAITING HUMAN APPROVAL** | Engage & log Qualified Cardiologist (`MD/FCPS`) + Supervisor sign-off on `DEC0005` / `G05`. |

---

## 2. Gate Outcome Determination & Unblocking Path
- **Overall Outcome:** **`NOT ASSESSED`** *(Blocks transition of frozen `ADJ####` release `G06` and production adjudication until clinical ratification; per `OS §14.1` AI self-certification never substitutes for qualified clinical sign-off).*
- **Corrective Action to Flip `G05 -> PASS`:**
  1. Name the reviewing Qualified Cardiologist (`scope.md §8.2`) and obtain clinical + supervisor approval of [DEC0005.md](../decision_log/DEC0005.md) (`Option A Recommended`).
  2. Reassess cleanly as `G05-2026MMDD-02` transitioning **`G05 -> PASS`**, then run the **`STEP-016`–`STEP-018`** deterministic adjudication pilot & production release (`ADJ####`).
