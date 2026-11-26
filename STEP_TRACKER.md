# 🚀 FYDP Multimodal CVD Risk Prediction — Master Step Tracker

> **Token-Saving Handoff Document:** This file serves as the single source of truth for current project progress. Teammates and AI agents should read this file first to know the exact state, what has been completed, and what to run next without re-reading thousands of lines of background documents.

---

## ⚡ Quick Handoff Status (Current State)

| Metric | Current Value |
|---|---|
| **Last Completed Step** | **`STEP-008`** (Evidence Synthesis & PG1–PG5 Gap Verification — All 5 Gaps Verified) |
| **Last Git Commit** | STEP-008 synthesis commit (see below) |
| **Active Stage** | **`S04`** (Proposal-Gap Verification `PG1–PG5` & Q1 RQ Approval) |
| **Next Step to Execute** | 👉 **`STEP-009`** (Lock Q1 Research Questions & Pass Gate G03) |
| **Current Quality Gates** | `G01`: Not Assessed (Doc prepared) \| `G02`: **PASS** \| `G03`: Ready for Assessment \| `G04–G17`: Blocked |
| **Last Updated** | 2026-11-26 |

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
| **STEP-009** | S04 | Finalize & ratify Q1 Research Questions (`RQ1–RQ4`), pass Gate G03 | Supervisor | G03 | 🟡 **READY TO RUN** | Target: G03 Assessment |
| **STEP-010** | S05 | Hospital site selection, recruitment protocol, power & EPV sample calculation | Nafis Sadiq | - | ⚪ PENDING | Target: `03_Datasets_Cohort/sites.csv` |
| **STEP-011** | S05 | Institutional IRB submission, hospital data authorization & consent/waiver | Nafis Sadiq | - | ⚪ PENDING | Target: IRB Approval Record |
| **STEP-012** | S05 | Screen external public cohorts (MIMIC-IV-ECG, PTB-XL) under UD06 | Nafis & Rayan | - | ⚪ PENDING | Target: External cohort feasibility |
| **STEP-013** | S06 | De-identified cohort intake, 12-lead ECG signal QC, cohort card, pass Gate G04 | Nafis Sadiq | G04 | ⚪ PENDING | Target: G04 Assessment |
| **STEP-014** | S07 | Clinical CVD endpoint charter ($t_0$, $\Delta t$, ICD-10 criteria) with cardiologist | Cardiologist | - | ⚪ PENDING | Target: `endpoint_charter.md` |
| **STEP-015** | S07 | 4-modality variable dictionary (`variables.csv`) & ECG contract, pass Gate G05 | Nafis Sadiq | G05 | ⚪ PENDING | Target: G05 Assessment |
| **STEP-016** | S08 | Clinical chart abstraction manual & pilot double-entry protocol | Nafis Sadiq | - | ⚪ PENDING | Target: Pilot protocol |
| **STEP-017** | S08 | Pilot adjudication run, compute inter-rater agreement ($\kappa$ / ICC) | Cardiologist | - | ⚪ PENDING | Target: Pilot agreement report |
| **STEP-018** | S08 | Production adjudication release, QA verification, pass Gate G06 | Cardiologist | G06 | ⚪ PENDING | Target: G06 Assessment |
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

## 🎯 Next Step Details: `STEP-009`

- **Step Name:** Lock Q1-Aligned Research Questions and Pass Literature Gate (`G03`)
- **Owning Lead:** Supervisor (Md. Mizanur Rahman) + Rayan Ahmed (`232-15-847`)
- **Inputs Ready:** [synthesis.md](file:///e:/FYDP/02_Literature/synthesis.md), [gaps.csv](file:///e:/FYDP/02_Literature/gaps.csv) (GAP0001–GAP0005 verified), [comparative_matrix.md](file:///e:/FYDP/02_Literature/comparative_matrix.md), [research_questions.md](file:///e:/FYDP/02_Literature/research_questions.md) (provisional), [claims.csv](file:///e:/FYDP/02_Literature/claims.csv) (CLAIM0001–CLAIM0013).
- **Action Required:**
  1. Finalize primary and subordinate RQs (`RQ1–RQ4`) linking every question to `O1–O4`, verified `GAP####`, required 4-modality data fields, comparator tier, statistical test, XAI metric, and permitted claim boundary.
  2. Prepare `DEC####` decision record approving finalized RQs.
  3. Write `G03_assessment_<date>.md` and update `gates.csv` with G03 status.
  4. Set literature search cutoff date.
  5. **Human-only:** Supervisor evaluates and approves Q1 positioning within the endorsed FYDP title.
