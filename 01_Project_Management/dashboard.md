# CVD Multimodal Research Executive Dashboard

| Metric | Current Status |
|---|---|
| **Project Title** | An Explainable Multimodal Framework for Early Cardiovascular Disease Risk Prediction Using Clinical, ECG, Laboratory, and Lifestyle Data |
| **Institution / Term** | Daffodil International University / Summer 2026 (CSE499) |
| **Research Leads** | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| **Supervisor** | Md. Mizanur Rahman (Senior Lecturer, Dept. of CSE, DIU) |
| **Active Stage** | Stage S04 (Proposal-Gap Verification & Q1 RQs) |
| **Current Step** | STEP-008 (Completed — PG1–PG5 Verified, Synthesis Authored) |
| **Next Step** | 👉 [STEP-009](../STEP_TRACKER.md) (Lock Q1 RQs & Pass G03) |
| **Master Step Tracker** | [STEP_TRACKER.md](../STEP_TRACKER.md) |
| **Last Updated** | 2026-11-26T00:58:00+06:00 |

---

## 1. Quality Gates Status Overview (`G01–G17`)

| Gate | Title / Domain | Assessor / Approver | Status | Evidence Document |
|---|---|---|---|---|
| **G01** | Scope & Decision Charter | Md. Mizanur Rahman | **NOT ASSESSED** | [G01_assessment_2026-11-20.md](file:///e:/FYDP/01_Project_Management/reviews/G01_assessment_2026-11-20.md) *(Evidence prepared; pending supervisor sign-off)* |
| **G02** | Repository, PHI Storage & Tooling | Rayan Ahmed | **PASS** | [G02_assessment_2026-11-20.md](file:///e:/FYDP/01_Project_Management/reviews/G02_assessment_2026-11-20.md) *(100% verified via automated validator)* |
| **G03** | Systematic Literature & Q1 RQs | Md. Mizanur Rahman | **BLOCKED** | Pending Stage S03–S04 execution (`STEP-004`–`009`) |
| **G04** | Ethics/IRB, Cohort Intake & QC | Hospital Custodian + Supervisor | **BLOCKED** | Pending Stage S05–S06 execution (`STEP-010`–`013`) |
| **G05** | Endpoint Charter & 4-Modality Schema | Qualified Cardiologist | **BLOCKED** | Pending Stage S07 execution (`STEP-014`–`015`) |
| **G06** | Pilot & Adjudicated Label Release | Qualified Cardiologist | **BLOCKED** | Pending Stage S08 execution (`STEP-016`–`018`) |
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
- **Test Suite:** `tests/test_synthetic_smoke.py` passes (3/3 unit tests clean) — **PASS**
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
