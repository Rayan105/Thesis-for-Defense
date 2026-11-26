# Scope Charter — CVD Multimodal Framework

**Status:** Proposed Amendment (`v1.1.0` — Secondary Public/Credentialed Data Pivot Pending Supervisor Ratification [`DEC0004`])  
**Version:** v1.1.0  
**Date:** 2026-11-26  
**Governing document:** [CVD Multimodal Research Operating System](../CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md), v1.0.0  

---

## 1. Verbatim Approved Title

> **An Explainable Multimodal Framework for Early Cardiovascular Disease Risk Prediction Using Clinical, ECG, Laboratory, and Lifestyle Data**

Source: `fydp_title_proposal.pdf` p.1, Section III (`RF01`). Updated Title field (Section IV) is blank.

## 2. Institutional Details

| Field | Value | Source |
|---|---|---|
| Institution | Daffodil International University, Department of Computer Science and Engineering | RF02, p.1 |
| Course | CSE499 — FYDP (Title Defense) | RF02, p.1 |
| Semester | Summer 2026 | RF02, p.1 |
| Proposal Approval Date | 09.07.2026 | RF02, p.1 |
| 1st Member | Rayan Ahmed, ID 232-15-847 | RF02, p.1 |
| 2nd Member | Mohammad Nafis Sadiq, ID 232-15-895 | RF02, p.1 |
| Supervisor | Md. Mizanur Rahman, Senior Lecturer (signed 09.07.26) | RF02, p.1 |
| Co-supervisor | None listed on supplied Proposal Approval Form | RF02, p.1 |

## 3. Source Document Provenance

| Document | Expected SHA-256 | Status |
|---|---|---|
| `fydp_title_proposal.pdf` (6-page scanned proposal) | `BA7DD0EF21C8A2CA77B2E1BAFC2AC5A0E1FEC584E221C848085A971EAACEEFA8` | **Pending workspace addition and hash verification** |
| `CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md` | To be computed at STEP-002 Git init | Present |
| `CVD_MULTIMODAL_PROJECT_EXECUTION_BLUEPRINT.md` | To be computed at STEP-002 Git init | Present |

## 4. Core Scope

This project develops a **reproducible, explainable multimodal CVD risk-prediction framework** integrating four approved data modalities via a Transformer-based fusion network with quantitatively validated SHAP explainability.

> [!NOTE]
> **Proposed Scope Amendment (`v1.1.0` / [DEC0004](./decision_log/DEC0004.md)):** While the original proposal (`RF09`, p. 4) anticipated primary hospital collection in Bangladesh, the research team requested pivoting to **verified secondary open/credentialed benchmark cohorts (Kaggle / Mendeley Data / PhysioNet)**. Verbatim approved title (`RF01`), four modalities (`RF10`), Transformer fusion (`RF08`), SHAP (`RF11`), and six mandatory metrics (`RF12`) remain **100% preserved**. Prospective primary Bangladeshi hospital validation is bounded explicitly as Future Work, pending Supervisor ratification of `DEC0004`.

It produces:

1. An ethically governed, license-verified, leakage-free secondary four-modality dataset architecture (avoiding synthetic data and unlinked patient stitching per `DEC0004`)
2. A rigorously benchmarked Transformer-based Multimodal Fusion Network (with missing-modality resilience) evaluated against 4-tier comparators
3. Quantitatively faithful, stable, and clinically reviewed multimodal SHAP explanations (`AOPC`, seed stability, shortcut audit)
4. A research decision-support prototype (`NOT` clinical deployment)
5. An FYDP thesis compliant with DIU CSE499 requirements
6. A Q1 journal manuscript compliant with TRIPOD+AI (2024)

### 4.1 Four Approved Modalities (`RF10`)

| Modality | Example Variables (from proposal p.4) | Notes |
|---|---|---|
| **Clinical Data** | Age, Gender, BMI, Blood Pressure, Medical History | Variable dictionary to be frozen at STEP-014 (`UD08`) |
| **ECG Signals** | Electrocardiogram waveforms or extracted intervals | Format (raw digital vs tabular intervals) to be resolved (`UD07`) |
| **Laboratory Results** | Blood Glucose, Cholesterol, Creatinine, etc. | Exact units and assay standardization at STEP-014 |
| **Lifestyle Information** | Smoking, Diet, Physical Activity, Sleep, Family History | Family History placement documented explicitly (`RF10`) |

### 4.2 Mandatory Performance Metrics (`RF12`)

All six must be reported on the held-out test set at frozen validation-selected thresholds:

1. Accuracy
2. Precision (PPV)
3. Recall (Sensitivity)
4. F1-Score
5. ROC-AUC
6. Confusion Matrix

Plus adopted Q1 extensions (adoption recorded under `UD16–UD17`): PR-AUC, Specificity, NPV, Brier Score, ECE, Calibration Slope/Intercept, Decision Curve Analysis, Bootstrap 95% CIs, paired DeLong/McNemar tests with Holm-Bonferroni correction.

## 5. Explicit In-Scope Items

- Systematic PRISMA-aligned literature review and `PG1–PG5` gap verification (zero-seed, since proposal has zero citations)
- Lawfully licensed secondary public/credentialed cohorts (`Kaggle / Mendeley CC BY 4.0 / PhysioNet DUA` under `DEC0004`, with optional multi-cohort missing-modality design incorporating de-identified open regional datasets such as `CAIR-CVD-2025`, and institutional ethics exemption verification)
- Cross-cohort external validation (`UD06`) and clinical endpoint harmonization (`UD02`)
- Strict anti-stitching & leakage-safe patient-level splitting and train-only preprocessing
- 4-tier comparator benchmarking (Unimodal → Clinical Scores → Simple Fusion → Transformer)
- Progressive modality addition and Leave-One-Modality-Out (LOMO) ablations
- Missing-modality robustness testing
- Probability calibration (Brier/ECE/slope) and Decision Curve Analysis
- Bootstrap CIs, DeLong/McNemar statistical tests with multiplicity correction
- Subgroup fairness audit (sex, age, site)
- Multimodal SHAP with quantitative faithfulness (Deletion/Insertion AOPC), multi-seed stability, and shortcut auditing
- Cardiologist plausibility review of explanations
- PROBAST-AI risk-of-bias self-audit
- Research decision-support prototype with synthetic demo
- FYDP thesis (DIU CSE499 format)
- Q1 journal manuscript (TRIPOD+AI 2024 compliant)

## 6. Explicit Out-of-Scope / Exclusions

| Exclusion | Rationale |
|---|---|
| Medical imaging (echo, CT, MRI, X-ray) as primary input modality | Proposal specifies 4 modalities; imaging is contextual literature only (`RF05`) |
| Autonomous clinical diagnosis | Framework is research decision-support, not diagnostic device (`RF15–RF16`) |
| Individualized medication or treatment prescription | Outside research scope |
| Clinical deployment in live hospital workflows | Requires separate clinical validation trial |
| Claiming proven reduction in clinician decision time | Requires IRB-approved prospective reader/impact trial |
| Claiming improved patient survival | Requires longitudinal clinical outcome study |
| Claiming statistically proven clinician trust | Requires separate IRB-approved usability study (`UD21`) |
| Biological causality claims from SHAP values | SHAP explains model behavior, not pathophysiology |

## 7. Clinical Safety Boundaries

> **A low predicted risk score is NEVER proof of absence of cardiovascular disease.**

> **A high predicted risk score is a statistical risk estimate, not a definitive diagnosis.**

> **Raw neural network logits/softmax outputs are uncalibrated model scores unless explicitly calibrated on validation data and verified on held-out test data.**

> **SHAP values explain how the model used its inputs, NOT biological causality. Attributing causal risk-factor status from observational SHAP values is strictly prohibited in Q1 writing.**

## 8. Role Assignments

### 8.1 Research Team

| Responsibility Domain | Lead | Support | Notes |
|---|---|---|---|
| Literature Review & Gap Verification | Rayan Ahmed | Mohammad Nafis Sadiq | Both screen independently for dual-screening |
| Cohort/IRB Coordination | Mohammad Nafis Sadiq | Rayan Ahmed | Hospital liaison, ethics filing |
| ECG Signal Engineering | Rayan Ahmed | Mohammad Nafis Sadiq | Format verification, filtering, encoding |
| Tabular Data Engineering | Mohammad Nafis Sadiq | Rayan Ahmed | Clinical/Lab/Lifestyle schema, CRF |
| Modeling & Training | Rayan Ahmed | Mohammad Nafis Sadiq | Transformer fusion, baselines, ablations |
| Evaluation & Biostatistics | Mohammad Nafis Sadiq | Rayan Ahmed | Metrics, calibration, DeLong, DCA |
| XAI (SHAP) Engineering | Rayan Ahmed | Mohammad Nafis Sadiq | Faithfulness, stability, shortcut audit |
| Writing — FYDP Thesis | Mohammad Nafis Sadiq | Rayan Ahmed | DIU format compliance |
| Writing — Q1 Journal Paper | Rayan Ahmed | Mohammad Nafis Sadiq | TRIPOD+AI compliance |
| Prototype & Defense | Shared | Shared | Joint responsibility |

> **Note:** Both researchers share all responsibilities. Lead assignments define coordination ownership and quality accountability, not exclusive access.

### 8.2 External Roles (Pending Assignment)

| Role | Named Individual | Status |
|---|---|---|
| Hospital Data Custodian | TBD | Identify at STEP-010 |
| Qualified Cardiologist / Clinical Adjudicator | TBD | Engage before STEP-014 (`UD09`) |
| Biostatistics Reviewer (if external) | TBD | Optional; supervisor may fulfill |

## 9. Dual Deliverable Intent

This project produces **two distinct publication-quality deliverables from one frozen evidence base**:

1. **FYDP Thesis** — Full engineering detail per DIU CSE499 institutional format (`UD23`)
2. **Q1 Journal Manuscript** — Concise high-impact scientific narrative for a top-tier biomedical-AI venue (e.g., IEEE JBHI, Computers in Biology and Medicine, Artificial Intelligence in Medicine, Information Fusion, npj Digital Medicine) with TRIPOD+AI (2024) and PROBAST-AI compliance

Document-scoped `G16` gates assess each independently. Project completion (`G17`) does not depend on external journal acceptance, only on evidenced submission or approved disposition.

## 10. Evaluation Report / Examiner Feedback Status (`UD01`)

**Current status:** Unresolved / Human Decision Required

The Proposal Approval Form on p.1 (`RF18`) states that the students will attach it to their FYDP Title Phase Evaluation Report. It is currently unknown whether:

- (a) A separate Title Phase Evaluation Report or examiner feedback document exists, OR
- (b) The signed Proposal Approval Form is the sole governing authority

**Action required:** Supervisor Md. Mizanur Rahman must confirm the existence or absence of additional evaluation feedback before `G01` PASS.

**Decision record:** [DEC0001](./decision_log/DEC0001.md)

## 11. Approval Record

| Approver | Role | Date | Signature |
|---|---|---|---|
| Rayan Ahmed | 1st Member / Researcher | _____ | _____ |
| Mohammad Nafis Sadiq | 2nd Member / Researcher | _____ | _____ |
| Md. Mizanur Rahman | Supervisor | _____ | _____ |

---

*End of Scope Charter — v1.0.0*
