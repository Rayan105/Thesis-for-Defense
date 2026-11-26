# 🚀 FYDP Multimodal CVD Risk Prediction — Master Step Tracker

> **Token-Saving Handoff Document:** This file serves as the single source of truth for current project progress. Teammates and AI agents should read this file first to know the exact state, what has been completed, and what to run next without re-reading thousands of lines of background documents.

---

## ⚡ Quick Handoff Status (Current State)

| Metric | Current Value |
|---|---|
| **Last Completed Step** | **`STEP-016`** (`G05 PASS` [`DEC0005 OptA`] + Stratified `N_pilot = 60` QA Run: $\kappa = 1.0000$, $\text{ICC} = 1.000000$, `32.3 rec/s`) |
| **Last Git Commit** | `STEP-016`: `G05 PASS`, dual-stream `run_pilot_qa.py` (`N=60` PASS), `pilot_qa_review.md` & agreement unit tests |
| **Active Stage** | **`S08`** (`STEP-016` Pilot Accepted; Ready for `STEP-017` Tracked Batch Curation `ADJB0001–0004`) |
| **Next Step to Execute** | 👉 **`STEP-017`** (Run Tracked Production Curation & Label Harmonization Batches `ADJB0001–0004` into Tier 2B) |
| **Current Quality Gates** | `G01`: Not Assessed (`local PDF missing`) \| **`G02–G05`: PASS** \| `G06–G17`: Blocked (`Pending STEP-017–018`) |
| **Last Updated** | 2026-11-27T00:14:00+06:00 |

### 🤖 AI Prompt for Next Teammate / Next Session:
To resume work with minimal token cost, simply give the AI this exact prompt:
```text
Read STEP_TRACKER.md and execute the next pending step.
```

---

## 📌 Master Operational Rules (Team Protocol)

1. **Commit & Push Discipline:** 
   - প্রতি ১টি স্টেপ শেষ হওয়ার পর **১টি Git Commit** এবং **১টি Git Push** করতে হবে।
   - Remote: `https://github.com/Rayan105/Thesis-for-Defense.git` (Branch: `main`).
2. **Strict Exclusions (`.gitignore`):**
   - ❌ **No Raw Datasets / PHI:** `raw/`, `processed/`, `*.edf`, `*.xml`, `*.dcm`, `*.mat`, etc.
   - ❌ **No Paper PDFs:** `*.pdf`, `02_Literature/fulltext/`
   - ❌ **No Weight Binaries:** `*.pt`, `*.pth`, `*.ckpt`, `*.h5`
   - ✅ Plans permitted: `CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md`, `CVD_MULTIMODAL_PROJECT_EXECUTION_BLUEPRINT.md`
3. **Role Responsibilities:**
   - **Rayan Ahmed (`232-15-847`):** Literature Review, ECG Waveforms, Transformer Modeling, XAI/SHAP, Q1 Manuscript Lead.
   - **Mohammad Nafis Sadiq (`232-15-895`):** Ethics/IRB, Cohort Intake, Tabular Engineering, Evaluation/Stats, FYDP Thesis Lead.
   - **Supervisor:** Md. Mizanur Rahman.

---

## 📋 Complete 50-Step Execution Ledger (`STEP-001` to `STEP-050`)

| Step ID | Stage | Description / Milestone | Owning Role | Exit Gate | Status | Evidence / Commit |
|---|---|---|---|---|---|---|
| **STEP-001** | S01 | Foundational scope charter, source facts RF01-18, UD01-26 assignment | Rayan & Nafis | G01 | **COMPLETED** | `a27310d` ([scope.md](file:///e:/FYDP/01_Project_Management/scope.md)) |
| **STEP-002** | S02 | Repository skeleton, Four-Tier PHI storage policy, minimal data runtime | Rayan Ahmed | - | **COMPLETED** | `ee7d55b` ([pipeline.md](file:///e:/FYDP/13_Documentation/pipeline.md)) |
| **STEP-003** | S02 | Materialize 32 templates (T01-32), 22 CSV registries, validate repo, pass G02 | Nafis Sadiq | G02 | **COMPLETED** | `ea8d680` ([G02 PASS](file:///e:/FYDP/01_Project_Management/reviews/G02_assessment_2026-11-20.md)) |
| **STEP-004** | S03 | Approve PRISMA zero-seed search protocol, queries, RQs (RQ1-4) | Rayan Ahmed | - | **COMPLETED** | `45ee657` ([protocol.md](file:///e:/FYDP/02_Literature/searches/protocol.md)) |
| **STEP-005** | S03 | Execute multi-database searches, deduplicate records, populate `papers.csv` | Nafis & Rayan | - | **COMPLETED** | `c71105b` ([SEARCH_SCHOLAR](file:///e:/FYDP/02_Literature/searches/SEARCH_SCHOLAR_2026-11-25.md)) |
| **STEP-006** | S03 | Two-stage PRISMA screening (Title/Abstract & Full-Text) in `screening.csv` | Nafis & Rayan | - | **COMPLETED** | `f19ebb2` + [screening_summary.md](file:///e:/FYDP/02_Literature/searches/screening_summary.md) |
| **STEP-007** | S03 | Methodological extraction of included direct comparator studies (`P####.md`) | Rayan & Nafis | - | **COMPLETED** | `42/42` [summaries](file:///e:/FYDP/02_Literature/summaries/) & [matrix](file:///e:/FYDP/02_Literature/comparative_matrix.md) |
| **STEP-008** | S04 | Synthesize evidence & test proposal research gaps (`PG1–PG5` $\rightarrow$ `GAP####`) | Rayan Ahmed | - | ✅ **COMPLETED** | [synthesis.md](file:///e:/FYDP/02_Literature/synthesis.md) & [gaps.csv](file:///e:/FYDP/02_Literature/gaps.csv) (5 GAPs verified) |
| **STEP-009** | S04 | Finalize & ratify Q1 Research Questions (`RQ1–RQ4`), pass Gate G03 | Supervisor | G03 | ✅ **COMPLETED (Docs)** | [research_questions.md](file:///e:/FYDP/02_Literature/research_questions.md), [DEC0002](file:///e:/FYDP/01_Project_Management/decision_log/DEC0002.md), [G03 Review](file:///e:/FYDP/01_Project_Management/reviews/G03_assessment_2026-11-26.md) *(Awaiting Supervisor Sign-Off)* |
| **STEP-010** | S05 | Hospital site selection, recruitment protocol, power & EPV sample calculation | Nafis Sadiq | - | ✅ **COMPLETED (Prep)** | [feasibility_epv_study.md](file:///e:/FYDP/03_Datasets_Cohort/reports/feasibility_epv_study.md), [sites.csv](file:///e:/FYDP/03_Datasets_Cohort/sites.csv), [DEC0003](file:///e:/FYDP/01_Project_Management/decision_log/DEC0003.md) *(BD Site Shortlist Pending)* |
| **STEP-011** | S05 | Secondary dataset licenses, provenance & ethics-exemption (`DEC0004`) | Nafis Sadiq | - | ✅ **COMPLETED** | [SITE0001/0007/0009/0012](file:///e:/FYDP/03_Datasets_Cohort/irb_permissions/), [sites.csv](file:///e:/FYDP/03_Datasets_Cohort/sites.csv), [Sign-Off Meeting](file:///e:/FYDP/01_Project_Management/meetings/2026-11-26_supervisor_signoff_meeting.md) |
| **STEP-012** | S05 | Immutable SHA-256 intake lock & external cohort mapping (`DS0001–04`) | Nafis & Rayan | - | ✅ **COMPLETED** | [datasets.csv](file:///e:/FYDP/03_Datasets_Cohort/datasets.csv), [manifests/](file:///e:/FYDP/03_Datasets_Cohort/manifests/) (`408` `ECGS/` images hashed), [Intake Summary](file:///e:/FYDP/03_Datasets_Cohort/reports/DS0001_to_DS0004_intake_summary.md) |
| **STEP-013** | S06 | 4-modality QC, 12-lead ECG signal/image audit, cohort cards, pass Gate G04 | Nafis Sadiq | G04 | ✅ **COMPLETED (`G04 PASS`)** | [QC Audit](file:///e:/FYDP/03_Datasets_Cohort/reports/four_modality_qc_and_ecg_audit.md), [Cohort Cards](file:///e:/FYDP/03_Datasets_Cohort/reports/cohort_cards_DS0001_to_DS0004.md), [G04 PASS](file:///e:/FYDP/01_Project_Management/reviews/G04_assessment_2026-11-26_reassessment.md) |
| **STEP-014** | S07 | Clinical CVD endpoint charter ($t_0$, $\Delta t$, Troponin tiers) & 4-modality schema | Nafis & Rayan | - | ✅ **COMPLETED (Draft Pending Cardiologist)** | [Endpoint Charter](file:///e:/FYDP/04_Outcome_Schema_QA/endpoint_charter.md), [variables.csv](file:///e:/FYDP/04_Outcome_Schema_QA/variables.csv), [CRF Manual](file:///e:/FYDP/04_Outcome_Schema_QA/crf/crf_manual_v1.0.0.md), [DEC0005](file:///e:/FYDP/01_Project_Management/decision_log/DEC0005.md) |
| **STEP-015** | S07 | ECG contract (`ecg_contract.md`), QA thresholds, unit tests & pass Gate G05 | Rayan & Nafis | G05 | ✅ **COMPLETED (`G05 PASS`)** | [ECG Contract](file:///e:/FYDP/04_Outcome_Schema_QA/ecg_contract.md), [QA Protocol](file:///e:/FYDP/04_Outcome_Schema_QA/qa_protocol.md), [test_schema_ecg.py](file:///e:/FYDP/tests/test_schema_ecg.py), [G05 PASS](file:///e:/FYDP/01_Project_Management/reviews/G05_assessment_2026-11-27_reassessment.md) |
| **STEP-016** | S08 | Stratified dual-stream pilot QA (`N_pilot=60`), compute Cohen's $\kappa$ / ICC | Nafis & Rayan | - | ✅ **COMPLETED (`Pilot PASS`)** | [run_pilot_qa.py](file:///e:/FYDP/14_Automation/run_pilot_qa.py), [pilot_qa_review.md](file:///e:/FYDP/04_Outcome_Schema_QA/reviews/pilot_qa_review.md) ($\kappa=1.0, \text{ICC}=1.0$) |
| **STEP-017** | S08 | Execute tracked production curation & adjudication batches (`ADJB0001–0004`) | Nafis & Rayan | - | 👉 **NEXT TO EXECUTE** | Target: `04_Outcome_Schema_QA/reviews/ADJB0001–0004.md` & Tier 2B batch tables |
| **STEP-018** | S08 | Production adjudication release (`ADJ####`), QA verification, pass Gate G06 | Team / Super | G06 | ⚪ PENDING | Target: G06 Assessment & `adjudication_registry.csv` |
| **STEP-019** | S09 | Leakage-safe patient-level split specification & seed definition | Nafis Sadiq | - | ⚪ PENDING | Target: Split design |
| **STEP-020** | S09 | Execute deterministic patient-grouped split, seal test partition, pass Gate G07 | Nafis Sadiq | G07 | ⚪ PENDING | Target: G07 Assessment |
| **STEP-021** | S09 | Preprocessing pipeline: record-local ECG filtering vs train-only fitted transforms | Rayan Ahmed | - | ⚪ PENDING | Target: Preprocessing configs |
| **STEP-022** | S09 | Cardiologist ECG filter morphology check, release `REL####`, pass Gate G08 | Cardiologist | G08 | ⚪ PENDING | Target: G08 Assessment |
| **STEP-023** | S10 | Deep learning framework selection (PyTorch vs TF under UD13) | Rayan Ahmed | - | ⚪ PENDING | Target: `DEC0002` / Framework Lock |
| **STEP-024** | S10 | Lock Phase 2 modeling environment (`environment/model/`) | Rayan Ahmed | - | ⚪ PENDING | Target: Modeling runtime lock |
| **STEP-025** | S10 | Formalize experiment plan, ablation matrix, calibration/stats protocol | Rayan & Nafis | - | ⚪ PENDING | Target: `experiment_plan.md` |
| **STEP-026** | S10 | Implement baseline suite (LR, RF, SVM, XGBoost, 1D-CNN, LSTM) & Transformer fusion | Rayan Ahmed | - | ⚪ PENDING | Target: `src/cvd_mm/models/` |
| **STEP-027** | S10 | Diagnostic smoke run, pipeline test, checkpoint restore test, pass Gate G09 | Rayan Ahmed | G09 | ⚪ PENDING | Target: G09 Assessment |
| **STEP-028** | S11 | Execute Tier 1 unimodal baselines & Tier 2 clinical risk scores | Rayan Ahmed | - | ⚪ PENDING | Target: Baseline runs |
| **STEP-029** | S11 | Execute Tier 3 early/late fusion models & Tier 4 Transformer fusion | Rayan Ahmed | - | ⚪ PENDING | Target: Fusion runs |
| **STEP-030** | S11 | Register model checkpoints & cards, evaluate qualifying Gate G10 | Rayan Ahmed | G10 | ⚪ PENDING | Target: G10 Assessment |
| **STEP-031** | S11 | Multi-seed runs, LOMO ablations, missing-modality degradation stress tests | Rayan Ahmed | - | ⚪ PENDING | Target: Full ablation matrix |
| **STEP-032** | S12 | Validation-only champion model selection, fit calibrator, pass Gate G11 | Nafis Sadiq | G11 | ⚪ PENDING | Target: G11 (Test set freeze) |
| **STEP-033** | S12 | Unseal held-out test partition & generate frozen test predictions | Nafis Sadiq | - | ⚪ PENDING | Target: Frozen test predictions |
| **STEP-034** | S13 | Compute 6 proposal mandatory metrics + Q1 adopted metrics (PR-AUC, Brier, ECE) | Nafis Sadiq | - | ⚪ PENDING | Target: Test evaluation metrics |
| **STEP-035** | S13 | Bootstrap 95% CIs, paired DeLong tests, Decision Curve Analysis (DCA) | Nafis Sadiq | - | ⚪ PENDING | Target: Statistical test reports |
| **STEP-036** | S13 | Compile evaluation report (`EVAL####`), pass Gate G12 | Nafis Sadiq | G12 | ⚪ PENDING | Target: G12 Assessment |
| **STEP-037** | S14 | Subgroup fairness audit, error analysis, PROBAST-AI review, pass Gate G13 | Nafis Sadiq | G13 | ⚪ PENDING | Target: G13 Assessment |
| **STEP-038** | S15 | Generate multimodal SHAP attributions (modality share, beeswarm, waterfalls) | Rayan Ahmed | - | ⚪ PENDING | Target: SHAP attributions |
| **STEP-039** | S15 | Quantitative XAI faithfulness (Deletion/Insertion AOPC) & multi-seed stability | Rayan Ahmed | - | ⚪ PENDING | Target: AOPC faithfulness curves |
| **STEP-040** | S15 | Cardiologist explanation plausibility review, shortcut audit, pass Gate G14 | Cardiologist | G14 | ⚪ PENDING | Target: G14 Assessment |
| **STEP-041** | S16 | Implement research decision-support prototype (CLI / optional defense UI) | Rayan Ahmed | - | ⚪ PENDING | Target: `src/cvd_mm/prototype.py` |
| **STEP-042** | S16 | Clean-environment reproducibility audit (Level A/B/C), pass Gate G15 | Rayan & Nafis | G15 | ⚪ PENDING | Target: G15 Assessment |
| **STEP-043** | S17 | Initialize claim ledger (`claims.csv`) & thesis/paper writing outlines | Rayan & Nafis | - | ⚪ PENDING | Target: Writing outlines |
| **STEP-044** | S17 | Draft FYDP Thesis Chapters 1–3 (Introduction, Literature, Methodology) | Nafis Sadiq | - | ⚪ PENDING | Target: Thesis draft part 1 |
| **STEP-045** | S17 | Draft FYDP Thesis Chapters 4–6 (Results, Discussion, Conclusion) | Nafis Sadiq | - | ⚪ PENDING | Target: Thesis draft part 2 |
| **STEP-046** | S17 | Finalize FYDP Thesis book, supervisor review, pass Gate G16 (Thesis) | Supervisor | G16-T | ⚪ PENDING | Target: Thesis approval |
| **STEP-047** | S17 | Submit FYDP Thesis to DIU CSE Department, log submission receipt | Nafis Sadiq | - | ⚪ PENDING | Target: Department receipt |
| **STEP-048** | S17 | Draft Q1 journal manuscript, TRIPOD+AI checklist, pass Gate G16 (Paper) | Rayan Ahmed | G16-P | ⚪ PENDING | Target: Q1 Paper approval |
| **STEP-049** | S17 | Package tiered immutable archive snapshot (`ARCH####`) & restore drill | Rayan & Nafis | - | ⚪ PENDING | Target: Immutable archive |
| **STEP-050** | S17 | Final FYDP defense, project completion handover, pass Gate G17 | Team & Super | G17 | ⚪ PENDING | Target: Final Project Sign-Off |

---

## 🎯 Next Step Details: `STEP-017` (Tracked Batch Curation & Adjudication Logs `ADJB0001–0004`)

- **Step Name:** Execute Tracked Production Curation & Label Harmonization Batches (`ADJB0001–0004`, `Stage S08`)
- **Owning Lead:** Mohammad Nafis Sadiq (`232-15-895`) & Rayan Ahmed (`232-15-847`)
- **Deliverables Planned in `STEP-017`:**
  1. Partition all `4` verified cohorts cleanly into disjoint auditable batches (`ADJB0001`: `PTB-XL 21,837`; `ADJB0002`: `CARDIO-ML-ED 581`; `ADJB0003`: `CAIR-CVD-2025 1,529`; `ADJB0004`: `sulianova 70,000`).
  2. Export cleaned, unit-harmonized, Tier-2B batch manifests (`04_Outcome_Schema_QA/adjudications/ADJB0001–0004/`, strictly gitignored!), enforcing all quarantined exclusions (`ecg_id=12722`, `<18y`, `8` `.jpg` strips, `2` typo IDs, `13` unlinked IDs, `65` `SBP<=DBP`, `13` negative `LDL`, `1,323` BP outliers, `17` discordant duplicates) and recording exact SHA-256 `NativeHash` & `VerifiedHash`.
  3. Generate aggregate-only batch summaries (`04_Outcome_Schema_QA/reviews/ADJB0001.md`–`ADJB0004.md`, Template `T12`) ready for **`STEP-018`** immutable **`ADJ####`** release lock & **`G06` PASS**.
