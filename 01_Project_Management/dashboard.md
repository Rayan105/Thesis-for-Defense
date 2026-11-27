# CVD Multimodal Research Executive Dashboard

| Metric | Current Status |
|---|---|
| **Project Title** | An Explainable Multimodal Framework for Early Cardiovascular Disease Risk Prediction Using Clinical, ECG, Laboratory, and Lifestyle Data |
| **Institution / Term** | Daffodil International University / Summer 2026 (CSE499) |
| **Research Leads** | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| **Supervisor** | Md. Mizanur Rahman (Senior Lecturer, Dept. of CSE, DIU) |
| **Active Stage** | Stage S09 (`STEP-019` Leakage-Free Preprocessing Design & Kaggle Notebook Complete; `G06` Sign-Off -> `STEP-020` Next) |
| **Current Step** | `STEP-019` Spec, Modules & Kaggle `.ipynb` Ready (`11/11` tests pass; [Pipeline Spec](../05_Preprocessing_Alignment/specs/pipeline.md)) |
| **Next Step** | 👉 Confirm `G06` (`DEC0006 UD10`) -> [STEP-020](../STEP_TRACKER.md#next-step-details-confirm-g06--execute-step-020-patientgrouped-split--kaggle-run) (**Nafis: `PatientGroupID` Splits & Stage B Run**) |
| **Master Step Tracker** | [STEP_TRACKER.md](../STEP_TRACKER.md) |
| **Last Updated** | 2026-11-27T11:35:00+06:00 |

---

## 1. Quality Gates Status Overview (`G01–G17`)

| Gate | Title / Domain | Assessor / Approver | Status | Evidence Document |
|---|---|---|---|---|
| **G01** | Scope & Decision Charter | Md. Mizanur Rahman | **NOT ASSESSED** | [G01_assessment_2026-11-26.md](file:///e:/FYDP/01_Project_Management/reviews/G01_assessment_2026-11-26.md) *(`C1,C3–C6` PASS via Supervisor sign-off; local `fydp_title_proposal.pdf` missing for `C2`)* |
| **G02** | Repository, PHI Storage & Tooling | Rayan Ahmed | **PASS** | [G02_assessment_2026-11-20.md](file:///e:/FYDP/01_Project_Management/reviews/G02_assessment_2026-11-20.md) *(100% verified via automated validator)* |
| **G03** | Systematic Literature & Q1 RQs | Md. Mizanur Rahman | **PASS** | [G03_assessment_2026-11-26_reassessment.md](file:///e:/FYDP/01_Project_Management/reviews/G03_assessment_2026-11-26_reassessment.md) *(Approved `DEC0002 Option A` + `DEC0004 Option B` `2026-11-26`)* |
| **G04** | Ethics/IRB, Cohort Intake & QC | Custodian + Supervisor | **PASS** | [G04_assessment_2026-11-26_reassessment.md](file:///e:/FYDP/01_Project_Management/reviews/G04_assessment_2026-11-26_reassessment.md) *(All `87,353 + 411 + 1 + 1` files hashed, `408` `ECGS/` verified, `DEC0004` signed)* |
| **G05** | Endpoint Charter & 4-Modality Schema | Md. Mizanur Rahman (Ext Cardiologist TBD) | **PASS** | [G05_assessment_2026-11-27_reassessment.md](file:///e:/FYDP/01_Project_Management/reviews/G05_assessment_2026-11-27_reassessment.md) *(`DEC0005 OptA` approved `2026-11-27`; Ext Cardiologist TBD for `G08/G14`)* |
| **G06** | Pilot & Adjudicated Label Release | Md. Mizanur Rahman + Data Lead | **NOT ASSESSED** | [G06_assessment_2026-11-27.md](file:///e:/FYDP/01_Project_Management/reviews/G06_assessment_2026-11-27.md) *(`C1–C3` PASS [`0` violations]; `DEC0006 UD10` sign-off pending)* |
| **G07** | Patient-Level Leakage-Free Split | Biostatistics Reviewer | **BLOCKED** | Pending Stage S09 execution (`STEP-019`–`020`) |
| **G08** | Preprocessing & ECG Filter Integrity | Clinical Lead + Implementer | **BLOCKED** | Pending Stage S09 execution (`STEP-021`–`022`) |
| **G09** | Architecture, Runtime & Smoke Test | Supervisor + Evaluator | **BLOCKED** | Pending Stage S10 execution (`STEP-023`–`027`) |
| **G10** | Controlled Experiment Completion | Experiment Reviewer | **BLOCKED** | Pending Stage S11 execution (`STEP-028`–`031`) |
| **G11** | Validation-Only Selection & Freeze | Supervisor + Evaluator | **BLOCKED** | Pending Stage S12 execution (`STEP-032`–`033`) |
| **G12** | Test Evaluation, Calibration & DCA | Biostatistics Reviewer | **BLOCKED** | Pending Stage S13 execution (`STEP-034`–`036`) |
| **G13** | Subgroup Fairness & PROBAST-AI | Clinical Lead + Supervisor | **BLOCKED** | Pending Stage S14 execution (`STEP-037`) |
| **G14** | Multimodal XAI Faithfulness (AOPC) | XAI Reviewer + Cardiologist | **BLOCKED** | Pending Stage S15 execution (`STEP-038`–`040`) |
| **G15** | Clean Reproducibility Audit | Reproduction Reviewer | **BLOCKED** | Pending Stage S16 execution (`STEP-041`–`042`) |
| **G16** | Submission Readiness (Thesis/Paper) | Supervisor + Authors | **BLOCKED** | Pending Stage S17 execution (`STEP-046`, `STEP-048`) |
| **G17** | Final Project Completion & Archive | Researchers + Supervisor | **BLOCKED** | Pending Stage S17 execution (`STEP-050`) |

---

## 2. Governance & Registry Health

- **Template Library:** 32 / 32 blank templates materialized (`15_Templates_Prompts/`) — **PASS**
- **Appendix B Registries:** 22 / 22 canonical CSV files validated — **PASS**
- **Automated Validation:** `14_Automation/validate_repo.py` passes with zero errors — **PASS**
- **Test Suite:** `tests/test_synthetic_smoke.py`, `tests/test_schema_ecg.py` & `tests/test_preprocessing_leakage.py` pass (11/11 unit tests clean) — **PASS**
- **PHI Exclusions:** Git status verified clean; raw data and binary models strictly ignored — **PASS**

---

## 3. Storage Tier Allocation

| Tier | Status | Current Content |
|---|---|---|
| **Tier 1 (Git)** | Active (`main` branch) | Source code, templates, safe CSV registries, documentation, test fixtures |
| **Tier 2A (Vault)** | Configured / Air-gapped | Offline encrypted storage designated for patient linkage keys |
| **Tier 2B (Clinical)** | Configured / Ignored | Designated for de-identified tables and ECG signals (`03_Datasets_Cohort/`) |
| **Tier 3 (Artifacts)** | Configured / Ignored | Designated for checkpoints and SHAP tensor arrays (`08_Checkpoints/`) |
| **Tier 4 (Archive)** | Configured | Designated for immutable snapshots (`16_Archive/`) |
