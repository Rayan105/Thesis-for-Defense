# 🚀 FYDP Multimodal CVD Risk Prediction — Master Step Tracker

> **Token-Saving Handoff Document:** This file serves as the single source of truth for current project progress. Teammates and AI agents should read this file first to know the exact state, what has been completed, and what to run next without re-reading thousands of lines of background documents.

---

## ⚡ Quick Handoff Status (Current State)

| Metric | Current Value |
|---|---|
| **Last Completed Step** | **`STEP-028` (`EXP0001–EXP0020` Immutable Stage S11 Bundles Registered `READY`)** (`Blocks A–F`, `33/33` Tests PASS) |
| **Last Git Commit** | `STEP-028`: Registered & hash-validated `EXP0001–EXP0020` immutable configs (`Blocks A–F`) & `experiment_registry.csv` |
| **Active Stage** | **`S11` IN PROGRESS (`STEP-028` Complete -> `STEP-029` Executing Full Controlled Training on Kaggle GPU)** |
| **Next Step to Execute** | 👉 **Execute `STEP-029` (`Train Blocks A–F Models [MC0001–MC0015] on REL0001 Train/Val via Kaggle GPU`)** |
| **Current Quality Gates** | `G01`: Not Assessed (`PDF missing`) \| **`G02–G09`: PASS** \| `G10–G17`: Blocked (`S11–S17`) |
| **Last Updated** | 2026-11-27T22:00:00+06:00 |

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
| **STEP-017** | S08 | Execute tracked production curation & adjudication batches (`ADJB0001–0004`) | Nafis & Rayan | - | ✅ **COMPLETED (`91,781` Eligible)** | [curate_batches.py](file:///e:/FYDP/14_Automation/curate_batches.py), [ADJB0001–0004](file:///e:/FYDP/04_Outcome_Schema_QA/reviews/) (`5%` Dual-QA $\kappa=1.0$) |
| **STEP-018** | S08 | Whole-cohort QA reconciliation, freeze `ADJ0001–0004`, evaluate Gate G06 (`UD10`) | Nafis & Rayan | G06 | ✅ **COMPLETED (Audit Clean / G06 Awaiting Sign-Off)** | [adjudication_registry.csv](file:///e:/FYDP/04_Outcome_Schema_QA/adjudication_registry.csv), [Release Audit](file:///e:/FYDP/04_Outcome_Schema_QA/reviews/adjudication_release_audit.md), [DEC0006](file:///e:/FYDP/01_Project_Management/decision_log/DEC0006.md), [G06 Review](file:///e:/FYDP/01_Project_Management/reviews/G06_assessment_2026-11-27.md) |
| **STEP-019** | S09 | Design leakage-free 4-modality preprocessing, ECG filtering & masking (`UD12`) | Rayan & Nafis | - | ✅ **COMPLETED (`11/11` Tests + Kaggle NB)** | [Pipeline Spec](file:///e:/FYDP/05_Preprocessing_Alignment/specs/pipeline.md), [preprocessing.py](file:///e:/FYDP/src/cvd_mm/preprocessing.py), [ecg.py](file:///e:/FYDP/src/cvd_mm/ecg.py), [Kaggle NB](file:///e:/FYDP/05_Preprocessing_Alignment/notebooks/CVD_Multimodal_Kaggle_Preprocessing_Pipeline.ipynb), [DEC0007](file:///e:/FYDP/01_Project_Management/decision_log/DEC0007.md) |
| **STEP-020** | S09 | Execute deterministic patient-grouped split, seal test partition, pass Gate G07 | Rayan Ahmed | G07 | ✅ **COMPLETED (`SPLIT0001` Locked / `G07` Awaiting Sign-Off)** | [splitting.py](file:///e:/FYDP/src/cvd_mm/splitting.py), [SPLIT0001 Report](file:///e:/FYDP/03_Datasets_Cohort/splits/SPLIT0001/report.md), [DEC0008](file:///e:/FYDP/01_Project_Management/decision_log/DEC0008.md), [G07 Review](file:///e:/FYDP/01_Project_Management/reviews/G07_assessment_2026-11-27.md) |
| **STEP-021** | S09 | Preprocessing pipeline: record-local ECG filtering vs train-only fitted transforms | Rayan Ahmed | - | ✅ **COMPLETED (`PP0001` Locked / `0` Leakage)** | [PP0001 Report](file:///e:/FYDP/05_Preprocessing_Alignment/reports/PP0001.md), [pp0001_config.yaml](file:///e:/FYDP/05_Preprocessing_Alignment/configs/pp0001_config.yaml), [run_preprocessing_pipeline.py](file:///e:/FYDP/14_Automation/run_preprocessing_pipeline.py), [Kaggle PDF Script](file:///e:/FYDP/14_Automation/build_kaggle_notebook_pdf.py) |
| **STEP-022** | S09 | Cardiologist ECG filter morphology check, release `REL####`, pass Gate G08 | Rayan & Cardiologist | G08 | ✅ **COMPLETED (`REL0001` Locked / `G08` Awaiting Clinical Sign-Off)** | [REL0001 Summary](file:///e:/FYDP/03_Datasets_Cohort/reports/REL0001_manifest_summary.md), [releases.csv](file:///e:/FYDP/03_Datasets_Cohort/releases.csv), [materialize_release.py](file:///e:/FYDP/14_Automation/materialize_release.py), [G08 Review](file:///e:/FYDP/01_Project_Management/reviews/G08_assessment_2026-11-27.md) |
| **STEP-023** | S10 | Deep learning framework selection (PyTorch vs TF under UD13) | Rayan Ahmed | - | ✅ **COMPLETED (`PyTorch UD13 + Transformer UD14`)** | [DEC0009](file:///e:/FYDP/01_Project_Management/decision_log/DEC0009.md), [DEC0010](file:///e:/FYDP/01_Project_Management/decision_log/DEC0010.md), [candidates.csv](file:///e:/FYDP/06_Models_Fusion/candidates.csv), [baseline_plan.md](file:///e:/FYDP/06_Models_Fusion/baseline_plan.md), [Transformer Spec](file:///e:/FYDP/06_Models_Fusion/architectures/transformer_fusion_spec.md), [Lit Update #1](file:///e:/FYDP/02_Literature/searches/SEARCH_UPDATE1_2026-11-27.md) |
| **STEP-024** | S10 | Lock Phase 2 modeling environment (`environment/model/`) | Rayan Ahmed | - | ✅ **COMPLETED (`environment/model/` Locked)** | [versions.md](file:///e:/FYDP/environment/model/versions.md), [requirements.txt](file:///e:/FYDP/environment/model/requirements.txt), [environment.yml](file:///e:/FYDP/environment/model/environment.yml), [verify_model_runtime.py](file:///e:/FYDP/14_Automation/verify_model_runtime.py) |
| **STEP-025** | S10 | Formalize experiment plan, ablation matrix, calibration/stats protocol | Rayan & Nafis | - | ✅ **COMPLETED (Pre-Training Protocols Frozen)** | [experiment_plan.md](file:///e:/FYDP/07_Experiments/experiment_plan.md), [eval_protocol.md](file:///e:/FYDP/09_Evaluation_Stats/protocol.md), [xai_protocol.md](file:///e:/FYDP/10_Explainability_XAI/xai_protocol.md), [DEC0011](file:///e:/FYDP/01_Project_Management/decision_log/DEC0011.md), [DEC0012](file:///e:/FYDP/01_Project_Management/decision_log/DEC0012.md) |
| **STEP-026** | S10 | Implement baseline suite (LR, RF, SVM, XGBoost, 1D-CNN, LSTM) & Transformer fusion | Rayan Ahmed | - | ✅ **COMPLETED (`src/cvd_mm/` + `32/32` Tests + Kaggle NB)** | [pipeline.md](file:///e:/FYDP/13_Documentation/pipeline.md), [run_experiment.py](file:///e:/FYDP/14_Automation/run_experiment.py), [CVD_Multimodal_Kaggle_Training_Pipeline.ipynb](file:///e:/FYDP/06_Models_Fusion/notebooks/CVD_Multimodal_Kaggle_Training_Pipeline.ipynb) |
| **STEP-027** | S10 | Diagnostic smoke run, pipeline test, checkpoint restore test, pass Gate G09 | Rayan Ahmed | G09 | ✅ **COMPLETED (`G09 PASS`)** | [EXP0000_SMOKE](file:///e:/FYDP/07_Experiments/EXP0000_SMOKE/README.md), [CKPT0001](file:///e:/FYDP/08_Checkpoints/manifests/CKPT0001.md), [G09 PASS](file:///e:/FYDP/01_Project_Management/reviews/G09_assessment_2026-11-27_reassessment.md) |
| **STEP-028** | S11 | Register & hash-validate immutable `EXP0001–EXP0020` bundles (`Blocks A–F`) | Rayan Ahmed | - | ✅ **COMPLETED (`20/20 READY` in `experiment_registry.csv`)** | [register_experiments.py](file:///e:/FYDP/14_Automation/register_experiments.py), [experiment_registry.csv](file:///e:/FYDP/07_Experiments/experiment_registry.csv), [EXP0015 README](file:///e:/FYDP/07_Experiments/EXP0015/README.md) |
| **STEP-029** | S11 | Train registered `Blocks A–F` models (`Tier 1–4`, `MC0001–MC0015`) on Train/Val | Rayan Ahmed | - | 👉 **NEXT TO EXECUTE** | Target: Kaggle GPU Full Matrix |
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

## 🎯 Next Step Details: Execute `STEP-029` (`Kaggle GPU Controlled Training Across Blocks A–F`)

- **Immutable Bundles Registered (`STEP-028` Complete):** All `20` preregistered experiment bundles ([EXP0001..EXP0020](file:///e:/FYDP/07_Experiments/experiment_registry.csv)) covering Tier 1 unimodal (`MC0001–10`), Tier 2 clinical context (`MC0011`), Tier 3 simple fusion (`MC0012–14`), Tier 4 `CVDMMTransformer` (`MC0015`), and `Blocks D–F` ablations/stress tests passed schema + SHA-256 + `G08–G09` custody checks (`Status = READY`).
- **Next Execution (`STEP-029` — Controlled Training Execution on Kaggle GPU):**
  1. Launch Kaggle GPU training runs (`Train/Val` only; `Test` sealed until `G11`) using [CVD_Multimodal_Kaggle_Training_Pipeline.ipynb](file:///e:/FYDP/06_Models_Fusion/notebooks/CVD_Multimodal_Kaggle_Training_Pipeline.ipynb) across `Blocks A–C` first (`Tier 1–2` baselines vs `Tier 3` vs `Tier 4 CVDMMTransformer`)!
  2. Export & log Validation metrics (`val_roc_auc`, `val_pr_auc`, `val_brier`, `ECE-15`) and `best_val` Tier 3 checkpoints (`CKPT####`), updating [experiment_registry.csv](file:///e:/FYDP/07_Experiments/experiment_registry.csv), [checkpoint_registry.csv](file:///e:/FYDP/08_Checkpoints/checkpoint_registry.csv), and [model_registry.csv](file:///e:/FYDP/06_Models_Fusion/model_registry.csv) in **`STEP-030` (`Gate G10`)**!
