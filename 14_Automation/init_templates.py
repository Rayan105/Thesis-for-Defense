"""
Script to materialize all 32 blank templates (T01-T32) in 15_Templates_Prompts/
and all 22 Appendix B CSV registries across domain folders.
"""

import os

TEMPLATES_DIR = "e:/FYDP/15_Templates_Prompts"
REPO_ROOT = "e:/FYDP"

COMMON_HEADER = """# {title}

| Field | Value |
|---|---|
| TemplateID | {template_id} ({template_name}) |
| template_version | v1.0.0 |
| entity_id | Unresolved / Human Decision Required |
| owner | Rayan Ahmed (232-15-847), Mohammad Nafis Sadiq (232-15-895) |
| date | 2026-11-20 |
| status | Template / Blank |
| source_inputs | not reported |
| governing_section | {governing_section} |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---
"""

TEMPLATES = [
    ("T01_readme.md", "T01", "readme.md", "OS §2.2, §15.2", "Domain Folder Contract", """
## 1. Purpose & Scope
[Describe the primary objective and scientific scope of this domain folder]

## 2. Ownership & Accountability
- Primary Lead: [Researcher Name]
- Reviewer / Supervisor: [Name]

## 3. Inputs & Prerequisites
[List all incoming data sources, dependencies, and prerequisite entities]

## 4. Allowed Contents & Artifacts
[List authorized files, schemas, and subdirectories]

## 5. Prohibited Contents & PHI Sensitivity
- PHI Sensitivity Tier: Tier 1
- Forbidden: [List strictly excluded formats, e.g., raw clinical records, patient identifiers, unverified weights]

## 6. Workflow & Automation Commands
[List CLI commands or reproduction scripts operating within this directory]
"""),

    ("T02_decision.md", "T02", "decision.md", "OS §12.1, §15.2, §15.3", "Unresolved Decision Record (DEC####)", """
# DEC#### — [Decision Title]

## 1. Decision Question
[Clear, concise decision statement resolving UD##]

## 2. Proposal Facts and Locators
- Source reference: [RF## / Proposal locator]
- Established constraint: [Fact description]

## 3. Options Considered & Tradeoffs
### Option A: [Description]
- Pros & Scientific Tradeoffs:
- Risks & Limitations:

### Option B: [Description]
- Pros & Scientific Tradeoffs:
- Risks & Limitations:

## 4. Recommendation & Rejected Alternatives
- Recommendation: [Selected path]
- Rejected Alternatives: [Reason for rejection]

## 5. Actual Human Decision & Approval
- Status: Unresolved / Human Decision Required
- Approver: [Named Reviewer / Supervisor]
- Approval Date: Pending
- Evidence Path: [Pointer to meeting minutes or sign-off document]

## 6. Affected Entities & Steps
- Blocks Step: [STEP-###]
- Affected Gates: [G##]
- Downstream Entities: [List affected registries or code modules]
"""),

    ("T03_session.md", "T03", "session.md", "OS §13, §15.2", "Daily Research Session Log", """
# SESS-YYYYMMDD-### — [Session Title]

## 1. Objective & Target Step
- Step ID: [STEP-###]
- Stage ID: [S##]
- Goal: [Target accomplishment for this session]

## 2. Prerequisites & Input Verification
- [ ] Prerequisite gates verified PASS
- [ ] Required input files and SHA-256 hashes confirmed

## 3. Planned vs Actual Outputs
| Deliverable | Canonical Path | Status | SHA-256 / Notes |
|---|---|---|---|
| [Output 1] | [Path] | [Done / Blocked] | [Hash or reason] |

## 4. Observations & Anomalies
[Record technical observations, unexpected data distributions, or runtime warnings]

## 5. Blockers & Human Actions Required
| Blocker ID | Description | Responsible Party | Next Action |
|---|---|---|---|
| [BLK-##] | [Details] | [Owner] | [Action] |

## 6. Next Action & Step Handover
[Exact unblocked action for the following session]
"""),

    ("T04_search.md", "T04", "search.md", "OS §3.1, §15.2", "Systematic Literature Search Record", """
## 1. Search Identification
- Search ID: `SEARCH-YYYYMMDD-###`
- Database / Engine: [PubMed / IEEE Xplore / Scopus / Google Scholar / arXiv]
- Date Executed: YYYY-MM-DD
- Search Query String (Verbatim):
```text
[Insert exact boolean query string with all search tags]
```

## 2. Filters & Inclusion Boundaries
- Date Range: [e.g., 2018-01-01 to 2026-11-20]
- Language: English
- Document Types: Journal articles, peer-reviewed conference proceedings

## 3. Quantitative Yield & Deduplication
- Total Records Retrieved: [Count]
- Export File Path: `02_Literature/searches/exports/SEARCH-###.csv`
- SHA-256 Checksum: [Checksum]
- Unique Records Post-Deduplication: [Count]

## 4. Search Limitations
[Document query truncation, syntax adjustments, or API rate limitations]
"""),

    ("T05_paper_summary.md", "T05", "paper_summary.md", "OS §3.2, §15.2", "Grounded Paper Extraction Summary (P####)", """
# P#### — [Paper Title]

## 1. Bibliographic Provenance
- Citation Key: [AuthorYear]
- DOI: [DOI link]
- PubMed ID (PMID): [PMID or None]
- Authors: [Author list]
- Venue & Year: [Journal/Conference, Year]
- Reading Status: Full-Text Verified

## 2. Study Design & Cohort Characteristics
- Setting & Country: [Setting]
- Sample Size ($N$): [Total patients, encounters]
- Event Count & Prevalence: [Event count, %]
- Endpoint Definition & Horizon: [e.g., 5-year CVD incidence, in-hospital mortality]

## 3. Modality & Technical Architecture
- Modalities Included: [Clinical, ECG, Lab, Lifestyle]
- ECG Format & Sampling: [e.g., 12-lead, 500 Hz, raw waveform vs intervals]
- Model Families: [LR, XGBoost, CNN, Transformer, etc.]
- Fusion Strategy: [Early, Late, Cross-Attention]

## 4. Quantitative Results & Evaluation Rigor
- Primary Discrimination: ROC-AUC = [Value] (95% CI: [Low-High])
- Secondary Metrics: PR-AUC = [Value], F1 = [Value], Brier Score = [Value]
- Calibration Evaluated: [Yes / No / ECE reported]
- Statistical Significance Testing: [DeLong test / Paired bootstrap]

## 5. Explainability & Bias Audit
- XAI Methods: [SHAP / LIME / Attention weights]
- XAI Faithfulness Benchmarked: [Yes / No / Not Reported]
- PROBAST Risk of Bias Rating: [Low / High / Unclear]
- Specific Limitations & Failure Modes: [Details with page locators]
"""),

    ("T06_gap.md", "T06", "gap.md", "OS §3.3, §15.2", "Proposal Research Gap Verification Record (GAP####)", """
# GAP#### — [Gap Title]

## 1. Proposal Gap Baseline
- Proposal Gap Identifier: [PG1 / PG2 / PG3 / PG4 / PG5]
- Proposal Statement (Verbatim): "[Insert statement from proposal p.3]"

## 2. Systematic Evidence Audit
- Search Coverage: [Databases surveyed]
- Supporting Literature (`P####` IDs): [List studies confirming the gap]
- Contradicting Literature (`P####` IDs): [List studies demonstrating prior art]

## 3. Sharpened Q1 Scientific Positioning
- Refined Q1 Research Gap: [Precise, falsifiable formulation of the gap]
- Primary Research Question Link: [RQ#]
- Feasibility Assessment: [Feasibility in Bangladesh cohort setting]
"""),

    ("T07_claim.md", "T07", "claim.md", "OS §10.1, §15.2", "Claim Traceability Record (CLAIM####)", """
# CLAIM#### — [Claim Statement]

## 1. Claim Formulation
- Claim Statement: "[Precise scientific assertion]"
- Claim Scope: [Methodological / Empirical Performance / Explainability / Clinical Safety]
- Target Documents: [Thesis Section #, Paper Section #]

## 2. Supporting Evidence Chain
- Literature Grounding (`P####`): [Paper IDs]
- Dataset & Release (`REL####`): [Release ID]
- Experiment & Run (`EXP####`): [Experiment ID]
- Evaluation Audit (`EVAL####`): [Evaluation ID]
- Asset Pointers (`FIG####` / `TAB####`): [Figure / Table IDs]

## 3. Counterevidence, Uncertainty & Bounded Phrasing
- Potential Counterevidence / Limitations: [Details]
- Permitted Manuscript Phrasing: "[Approved wording respecting clinical boundaries]"
- Prohibited Overclaims: "[Forbidden causal assertions or unproven clinical claims]"
"""),

    ("T08_site_irb.md", "T08", "site_irb.md", "OS §4.1, §11, §15.2", "Hospital Site & IRB Authorization Record (SITE####)", """
# SITE#### — [Hospital / Clinical Site Name]

## 1. Site Metadata & Administrative Authorization
- Site Name: [Name of Hospital / Diagnostic Center]
- Country & Region: Bangladesh, [District]
- Site Type: [Tertiary Academic Hospital / Specialized Cardiac Center / Diagnostic Lab]
- Administrative Permission Document: `03_Datasets_Cohort/irb_permissions/SITE####_permission.pdf`

## 2. Institutional Review Board (IRB) Approval
- IRB Protocol / Approval Number: [Protocol ID]
- IRB Authority: [Ethics Review Committee Name]
- Approval Date & Validity: YYYY-MM-DD to YYYY-MM-DD
- Consent Framework: [Informed Written Consent / Approved Retrospective Waiver]

## 3. Data Modalities & PHI Security Contract
- Permitted Modalities: [Clinical, 12-lead ECG, Laboratory, Lifestyle]
- PHI De-identification Standard: [Strict stripping of direct identifiers prior to Tier 2B transfer]
- Data Retention & Destruction Schedule: [Retention terms]
"""),

    ("T09_cohort_card.md", "T09", "cohort_card.md", "OS §4.2, §15.2", "Cohort & Dataset Quality Card (DS####)", """
# DS#### — [Cohort Dataset Name]

## 1. Provenance & Administration
- Dataset ID: `DS####`
- Clinical Sites (`SITE####`): [Site IDs]
- IRB Protocol Reference: [IRB ID]
- Recruitment Window: YYYY-MM-DD to YYYY-MM-DD
- Target Population: [Description of screening population]

## 2. Quantitative Summary
- Total Patient Count: [N]
- Total Clinical Encounters: [N]
- Cardiovascular Events (CVD+): [Count, %]
- Controls (CVD-): [Count, %]
- Complete 4-Modality Cases: [Count, %]

## 3. Modality Availability & Missingness
| Modality | Available Encounters | Missing Rate (%) | Primary Acquisition Device / Instrument |
|---|---|---|---|
| Clinical Records | [Count] | [%] | Hospital EHR / Case Report Form |
| 12-Lead ECG | [Count] | [%] | Digital ECG Machine (XML/DICOM/WFDB) |
| Laboratory Assays | [Count] | [%] | Serum Biochemistry Analyzer |
| Lifestyle Profiles | [Count] | [%] | Structured Patient Questionnaire |

## 4. Signal Integrity & Quality Checks
- ECG Quality Pass Rate: [% passing SNR and baseline wander checks]
- Raw File Manifest Hash (SHA-256): [Checksum]
- Tier 2B Storage Location: `E:/FYDP_SECURE_VAULT/Tier2B/DS####/`
"""),

    ("T10_endpoint_charter.md", "T10", "endpoint_charter.md", "OS §5.1, §15.2", "Clinical Endpoint & Ascertainment Charter", """
# Clinical Endpoint Charter — CVD Risk Prediction Target

## 1. Operational CVD Definition & Target Construct
- Target Name: Early Cardiovascular Disease Event / High Risk
- Classification Type: Binary Classification (0 = Non-CVD / Low Risk, 1 = Documented CVD Event / High Risk)
- Diagnostic Ascertainment Criteria: [Exact ICD-10 codes / Clinical adjudication rubric]

## 2. Temporal Anchoring & Leakage Prevention
- Index Timestamp ($t_0$): [Exact clinical reference point, e.g. admission or initial screening]
- Maximum Permissible Modality Window ($\Delta t$): [e.g., within 24 hours of $t_0$]
- Lookback Horizon: [Predictors originating strictly $\le t_0$]
- Lookahead / Prediction Horizon: [e.g., in-hospital, 1-year, or cross-sectional early risk]

## 3. Incorporation Bias Controls
- Predictor Exclusion Rule: Predictors used to define the gold standard outcome are strictly excluded from input feature spaces.

## 4. Cardiologist Approval Block
- Reviewing Cardiologist: [Name, MD/FCPS]
- Affiliation: [Cardiology Department / Hospital]
- Approval Date: Pending
"""),

    ("T11_crf_ecg_protocol.md", "T11", "crf_ecg_protocol.md", "OS §5.2, §15.2", "Case Report Form (CRF) & 12-Lead ECG Acquisition Contract", """
# CRF & 12-Lead ECG Technical Protocol

## 1. Case Report Form (CRF) Items
- Clinical Variables: Age, Sex, Systolic BP, Diastolic BP, Heart Rate, BMI, Hypertension History, Diabetes History
- Laboratory Assays: Total Cholesterol, LDL-C, HDL-C, Triglycerides, Fasting Plasma Glucose, Serum Creatinine, Troponin
- Lifestyle Factors: Smoking status (pack-years), Physical activity level, Dietary risk score, Alcohol intake

## 2. 12-Lead ECG Standard Specifications
- Standard Lead Set: I, II, III, aVR, aVL, aVF, V1, V2, V3, V4, V5, V6
- Sampling Frequency: 500 Hz (minimum allowable 250 Hz)
- Recording Duration: Standard 10 seconds
- Voltage Calibration: 10 mm/mV (0.1 mV resolution)
- Raw File Format: [WFDB / XML / DICOM / CSV array]

## 3. Pre-Analysis Quality Thresholds
- High-frequency powerline interference ($50$ Hz) rejection
- Baseline wander removal ($< 0.5$ Hz) with ST-T complex geometry preservation
- Lead detachment / flatline detection
"""),

    ("T12_adjudication_batch.md", "T12", "adjudication_batch.md", "OS §5.3, §15.2", "Outcome Adjudication Batch Record (ADJB####)", """
# ADJB#### — Adjudication Batch Log

## 1. Batch Metadata
- Batch ID: `ADJB####`
- Cohort Dataset ID: `DS####`
- Encounter Membership: [List of ENC IDs]
- Abstractors: [Abstractor 1, Abstractor 2]
- Clinical Adjudicator: [Qualified Cardiologist Name]

## 2. Inter-Rater Reliability & Concordance
- Double-Entry Sample Size: [N]
- Cohen's Kappa ($\kappa$) for Binary Target: [Value]
- Intraclass Correlation Coefficient (ICC) for Continuous Markers: [Value]
- Discrepancy Resolution: [Summary of resolved discordant classifications]

## 3. Cryptographic Hashes
- Raw Batch File Hash (SHA-256): [Checksum]
- Verified Adjudicated Batch Hash (SHA-256): [Checksum]
"""),

    ("T13_preprocessing.md", "T13", "preprocessing.md", "OS §4.4, §4.5, §15.2", "Preprocessing & Fit State Report (PP####)", """
# PP#### — Preprocessing & Transformation Report

## 1. Pipeline Identification
- Preprocessing ID: `PP####`
- Release Input: `REL####` / `SPLIT####`
- Configuration File: `05_Preprocessing_Alignment/configs/PP####_config.yaml`
- Configuration Hash (SHA-256): [Checksum]

## 2. Decoupled Transformation Steps
### A. Record-Local Operations (Independent of Splitting)
- ECG 50 Hz notch filter (Q-factor = 30)
- ECG baseline wander correction (0.5 Hz highpass FIR filter)
- Unit standardizations (e.g., mg/dL to mmol/L harmonization)

### B. Training-Fitted Operations (Strictly Fit on Train Partition)
- Continuous tabular median imputation (learned on Train fold)
- Robust/Standard scaling parameters (learned on Train fold)
- Categorical one-hot / target encoding maps (learned on Train fold)

## 3. Data Leakage Audit
- Fit State SHA-256 Hash: [Checksum]
- Train/Validation/Test Partition Leakage Check: PASS (Zero leakage confirmed)
- Cardiologist Morphology Check: PASS (ST-T preservation verified)
"""),

    ("T14_split.md", "T14", "split.md", "OS §4.3, §15.2", "Patient-Grouped Split Report (SPLIT####)", """
# SPLIT#### — Leakage-Free Dataset Split Report

## 1. Split Specification
- Split ID: `SPLIT####`
- Source Dataset ID: `DS####`
- Grouping Key: `PatientID` (Strict patient-level isolation)
- Partitioning Scheme: [e.g., Train 70%, Validation 15%, Test 15% / 5-Fold Nested CV]
- Random Seed: [e.g., 42]
- Stratification Factors: Outcome CVD event status, Clinical Site, Sex

## 2. Partition Demographics & Event Prevalence
| Partition | Patient Count ($N$) | Encounter Count | CVD Events (%) | Male / Female (%) |
|---|---|---|---|---|
| Train | [N] | [Count] | [%] | [% / %] |
| Validation | [N] | [Count] | [%] | [% / %] |
| Test (Held-Out) | [N] | [Count] | [%] | [% / %] |

## 3. Verification of Zero Patient Overlap
- Overlap Check: `len(set(Train_Patients) & set(Val_Patients) & set(Test_Patients)) == 0`
- Assertion Result: PASS (Zero cross-partition patient overlap)
- Test Partition Sealed Custody: [Custody details]
"""),

    ("T15_failure.md", "T15", "failure.md", "OS §13, §15.2", "Failure & Anomaly Incident Report", """
# FAIL-YYYYMMDD-### — [Failure Title]

## 1. Incident Overview
- Timestamp: YYYY-MM-DDTHH:MM:SS+06:00
- Affected Steps / Entities: [e.g., STEP-028 / EXP0004]
- Severity: [Critical / Major / Minor]

## 2. Observed Symptoms & Error Traces
```text
[Insert exact console trace or system error log]
```

## 3. Root Cause Investigation
- Mechanism: [Data schema mismatch / Out-Of-Memory / Gradient divergence / Leakage detection]
- Underlying Cause: [Technical explanation]

## 4. Remediation, Lost Work & Prevention
- Lost Computation: [e.g., 4 epochs lost]
- Remediation Executed: [Fix details]
- Permanent Prevention Protocol: [Automated test or guard added]
- Incident Status: Resolved
"""),

    ("T16_experiment.md", "T16", "experiment.md", "OS §6.2, §15.2", "Experiment Execution Report (EXP####)", """
# EXP#### — [Experiment Title]

## 1. Scientific Objective
- Experiment ID: `EXP####`
- Research Question: [RQ#]
- Comparator Tier: [Tier 1 Unimodal / Tier 2 Clinical Score / Tier 3 Early Fusion / Tier 4 Transformer Fusion / Ablation]
- Primary Hypothesis: [Falsifiable performance hypothesis]

## 2. Data & Model Setup
- Prepared Release: `REL####`
- Split ID: `SPLIT####`
- Model Candidate: `MC####`
- Config Path: `07_Experiments/EXP####/config.yaml`
- Configuration Hash (SHA-256): [Checksum]
- Source Code Git Commit: [Commit Hash]

## 3. Training & Validation Execution
- Random Seed: [Seed]
- Optimization / Budget: [Optimizer, Learning Rate, Epochs, Batch Size]
- Early Stopping Criterion: Validation ROC-AUC (patience = 10)
- Validation Discrimination: ROC-AUC = [Value], PR-AUC = [Value]
- Validation Calibration: Brier Score = [Value]

## 4. Checkpoints & Artifact Pointers
- Best Checkpoint: `CKPT####`
- Artifact Storage Location: `E:/FYDP_SECURE_VAULT/Tier3/EXP####/`
- Outcome / Conclusion: [Summary of observed experimental findings]
"""),

    ("T17_model_card.md", "T17", "model_card.md", "OS §6.3, §15.2", "Bounded Model Card (MODEL####)", """
# MODEL#### — Bounded Model Card

## 1. Model Overview
- Model ID: `MODEL####`
- Architecture Family: [e.g., Cross-Modal Transformer Fusion Network]
- Framework: [PyTorch / TensorFlow]
- Parameter Count: [Total parameters]
- Training Experiment: `EXP####`
- Best Checkpoint: `CKPT####`

## 2. Intended Use & Boundaries
- Intended Domain: Research clinical decision-support for early CVD risk prediction
- Primary Users: Medical researchers and clinical AI evaluators
- Out-of-Scope Use: Autonomous diagnostic decisions, emergency triage without doctor review

## 3. Inputs & Modalities Handled
- Modality Encoders:
  - Clinical: Multi-layer Perceptron (MLP)
  - ECG: 1D-ResNet / Convolutional Transformer
  - Laboratory: Tabular embedding layer
  - Lifestyle: Tabular embedding layer
- Missing-Modality Behavior: Masked cross-attention token imputation

## 4. Performance & Calibration Summary
- Held-Out ROC-AUC: [Value] (95% CI: [Low-High])
- Operating Decision Threshold ($\tau$): [Threshold Value]
- Post-Hoc Calibrator: [Platt Scaling / Isotonic Regression]
"""),

    ("T18_checkpoint.md", "T18", "checkpoint.md", "OS §11.2, §15.2", "Checkpoint Manifest Record (CKPT####)", """
# CKPT#### — Model Checkpoint Manifest

## 1. Checkpoint Provenance
- Checkpoint ID: `CKPT####`
- Experiment ID: `EXP####`
- Run Attempt: `RUN####`
- Epoch / Step: [Epoch #]
- Trigger Reason: Best Validation ROC-AUC

## 2. Stored State Components
- [x] Model weights (state_dict)
- [x] Optimizer state
- [x] Learning rate scheduler state
- [x] Random Number Generator (RNG) seeds (Python, NumPy, Framework)

## 3. Storage & Integrity Audit
- File Format: [e.g., .pt / .ckpt]
- File Size: [Bytes]
- Cryptographic SHA-256 Checksum: [Checksum]
- Tier 3 Storage Path: `E:/FYDP_SECURE_VAULT/Tier3/checkpoints/CKPT####.pt`
- Restore Verification Test: PASS (Exact inference reproduction verified)
"""),

    ("T19_evaluation.md", "T19", "evaluation.md", "OS §7.1, §15.2", "Quantitative Evaluation Report (EVAL####)", """
# EVAL#### — Quantitative Held-Out Evaluation Report

## 1. Evaluation Protocol & Freeze
- Evaluation ID: `EVAL####`
- Evaluated Model: `MODEL####`
- Test Partition Release: `REL####` (Sealed Test Set)
- Test Freeze Protocol Hash: [Checksum]
- Operating Threshold ($\tau$): [Threshold] (Frozen on validation)

## 2. Primary Discrimination & Classification Metrics
| Metric | Value | 95% Bootstrap CI | Proposal Mandatory |
|---|---|---|---|
| ROC-AUC | [Value] | [[Low] - [High]] | Yes |
| Precision-Recall AUC (PR-AUC) | [Value] | [[Low] - [High]] | Q1 Adopted |
| Accuracy | [Value] | [[Low] - [High]] | Yes |
| Sensitivity (Recall) | [Value] | [[Low] - [High]] | Yes |
| Specificity | [Value] | [[Low] - [High]] | Q1 Adopted |
| Positive Predictive Value (Precision) | [Value] | [[Low] - [High]] | Yes |
| Negative Predictive Value (NPV) | [Value] | [[Low] - [High]] | Q1 Adopted |
| F1-Score | [Value] | [[Low] - [High]] | Yes |

## 3. 2x2 Confusion Matrix
```text
                 Observed CVD-    Observed CVD+
Predicted Low:       [TN]             [FN]
Predicted High:      [FP]             [TP]
```

## 4. Probability Calibration & Clinical Utility
- Brier Score: [Value] (Lower is better)
- Expected Calibration Error (ECE): [Value]
- Calibration Slope: [Value] (Target = 1.0)
- Calibration Intercept: [Value] (Target = 0.0)
- Decision Curve Analysis (DCA): Superior Net Benefit across risk thresholds [Range]
"""),

    ("T20_error_probast.md", "T20", "error_probast.md", "OS §7.3, §15.2", "Systematic Error Analysis & PROBAST-AI Bias Review", """
# Error & PROBAST-AI Audit — EVAL####

## 1. Stratified Error Review
- False Positive (FP) Case Analysis: [Common patterns, e.g., borderline hypertension + high cholesterol]
- False Negative (FN) Case Analysis: [Common patterns, e.g., atypical presentation or missing lifestyle markers]
- Label Uncertainty vs Model Error: [Review with clinical adjudicator]

## 2. PROBAST-AI (Prediction Model Risk of Bias Assessment)
| Domain | Risk of Bias Rating | Key Considerations & Mitigations |
|---|---|---|
| Domain 1: Participants | [Low / High / Unclear] | Consecutive clinical cohort, clear eligibility criteria |
| Domain 2: Predictors | [Low / High / Unclear] | Blinded predictor assessment, zero post-diagnosis predictors |
| Domain 3: Outcome | [Low / High / Unclear] | Objective CVD definition, blind adjudication, no incorporation bias |
| Domain 4: Analysis | [Low / High / Unclear] | Patient-level splits, post-split fitting, EPV sizing, calibration reported |
| **Overall Risk of Bias** | **[Low / High]** | **Overall study rating** |
"""),

    ("T21_xai_audit.md", "T21", "xai_audit.md", "OS §8.1, §8.2, §15.2", "Multimodal Explainability Audit (XAI####)", """
# XAI#### — Multimodal SHAP & Faithfulness Audit

## 1. Explainer Setup & Additivity
- Explainer Type: [TreeSHAP / GradientSHAP / KernelSHAP]
- Background Distribution: Training partition stratified sample ($N = 200$)
- Local Additivity Error: PASS ($\sum \phi_i + \phi_0 - f(x) < 10^{-4}$)

## 2. Multimodal Modality-Share Contributions
- Clinical Modality Share: [%]
- 12-Lead ECG Modality Share: [%]
- Laboratory Modality Share: [%]
- Lifestyle Modality Share: [%]
- Modality-Ablation Concordance: Correlates with empirical Leave-One-Modality-Out drops

## 3. Quantitative Faithfulness Benchmarks
- Deletion AOPC (Comprehensiveness): [Value] (Significantly degrades faster than random masking, $p < 0.001$)
- Insertion AOPC (Sufficiency): [Value] (Recovers prediction faster than random insertion)
- Multi-Seed Ranking Stability: Spearman $\rho = [Value]$ across independent random seeds

## 4. Spurious-Shortcut & Clinical Plausibility Audit
- Shortcut Detection: Negative (Site IDs, powerline noise, missingness flags show negligible attribution)
- Cardiologist Rubric: Pathophysiological plausibility confirmed for top clinical risk drivers
"""),

    ("T22_gate_audit.md", "T22", "gate_audit.md", "OS §14.1, §15.2, §15.3", "Quality Gate Assessment Record (G##)", """
# G## Assessment — [Gate Title]

| Field | Value |
|---|---|
| AssessmentID | G##-YYYYMMDD-## |
| GateID | G## |
| DocumentOrEntityScope | [Evaluated entity paths] |
| EntityVersions | [Evaluated versions] |
| Outcome | [PASS / FAIL / NOT ASSESSED / STALE] |
| Assessor | [Assessor Name] |
| Human Approver | [Supervisor / Qualified Human Reviewer] |
| Assessment Date | YYYY-MM-DD |

---

## 1. Mandatory Criteria Audit Matrix
| Criterion # | Mandatory Criterion | Required Evidence Path | Current Evidence State & SHA-256 | PASS / FAIL |
|---|---|---|---|---|
| C1 | [Description] | [Path] | [Hash / State] | [PASS / FAIL] |
| C2 | [Description] | [Path] | [Hash / State] | [PASS / FAIL] |

## 2. Gate Outcome Determination
- Overall Outcome: [PASS only if 100% evidenced; otherwise FAIL]
- Rationale: [Justification]

## 3. Dependent Work & Corrective Actions
- Unblocked Next Steps: [List unblocked steps]
- Invalidated Downstream Gates (if FAIL/STALE): [List gates]
- Required Remediation: [Actions]
"""),

    ("T23_figure_table.md", "T23", "figure_table.md", "OS §10.3, §15.2", "Publication Asset Specification (FIG#### / TAB####)", """
# FIG#### / TAB#### — [Asset Title]

## 1. Asset Metadata
- Asset ID: `FIG####` / `TAB####`
- Target Venue: [Thesis Chapter # / Q1 Manuscript Figure #]
- Kind: [Vector Diagram / Multi-Panel Plot / Summary Table]
- Generation Script: `11_Figures_Tables/scripts/generate_FIG####.py`
- Source Data Hash (SHA-256): [Checksum]

## 2. Visual & Formatting Requirements
- Dimensions / Aspect Ratio: [Width x Height, e.g., 180 mm wide]
- Resolution: Vector PDF/SVG (or 300-600 DPI TIFF)
- Color Palette: Colorblind-friendly (e.g., ColorBrewer / Viridis)
- Explicit Units: All axes, table headers, and error bars must state physical units

## 3. Human Visual Inspection & PHI Check
- PHI / Identifier Check: PASS (Zero identifiable patient data)
- Legibility & Alignment Check: PASS
"""),

    ("T24_reproduce.md", "T24", "reproduce.md", "OS §9.2, §15.2", "Clean-Environment Reproducibility Audit", """
# Reproducibility Audit — Stage S16 Verification

## 1. Audit Setup
- Audit Date: YYYY-MM-DD
- Execution Host: Clean virtual environment / Fresh container
- Environment Lock Hash: [Checksum]
- Evaluator: [Evaluator Name]

## 2. Replay Commands & Execution
```bash
# Exact commands executed to reproduce study findings
git clone https://github.com/Rayan105/Thesis-for-Defense.git
cd Thesis-for-Defense
pip install -r environment/data/requirements.txt
python 14_Automation/reproduce_study.py --release REL0001
```

## 3. Numerical Tolerance Agreement
| Target Metric | Original Reported Value | Replayed Value | Absolute Difference | Within Tolerance ($< 10^{-4}$)? |
|---|---|---|---|---|
| Held-out ROC-AUC | [Value] | [Value] | [Diff] | PASS |
| Held-out PR-AUC | [Value] | [Value] | [Diff] | PASS |
| Brier Score | [Value] | [Value] | [Diff] | PASS |

## 4. Declared Reproducibility Level
- Level A (Deterministic Replay): Evidenced and Verified
- Controlled Data Access Statement: Lawful access protocol documented for external researchers
"""),

    ("T25_review_response.md", "T25", "review_response.md", "OS §10.4, §15.2", "Reviewer & Supervisor Response Ledger", """
# Review Response Log — [Review Round]

## 1. Review Overview
- Review Round: [Supervisor Milestone Review / Q1 Journal Review Round 1]
- Document: [Thesis / Q1 Journal Manuscript]
- Date Received: YYYY-MM-DD

## 2. Point-by-Point Response Matrix
### Comment 1: [Reviewer Comment Summary]
- Verbatim Comment: "[Insert verbatim text]"
- Categorization: [Methodological / Editorial / Additional Experiment]
- Response & Scientific Rationale: [Detailed response]
- Manuscript Diff Location: [Page #, Section #, Line #]
- Evidence Pointer: `EVAL####` / `EXP####`
- Status: Resolved
"""),

    ("T26_writing_unit.md", "T26", "writing_unit.md", "OS §10.2, §15.2", "Manuscript Writing Unit (WR####)", """
# WR#### — [Writing Unit Title]

## 1. Unit Metadata
- Unit ID: `WR####`
- Target Document: [FYDP Thesis / Q1 Journal Manuscript]
- Chapter / Section: [e.g., Section 3.2 Multimodal Fusion Network]
- Primary Author: [Author Name]
- Reviewer: [Reviewer Name]

## 2. Evidence Grounding & Claim Links
- Linked Claims (`CLAIM####`): [List Claim IDs]
- Literature Citations (`P####`): [List Paper IDs]
- Evaluation Results (`EVAL####`): [List Evaluation IDs]
- Visual Assets (`FIG####` / `TAB####`): [List Asset IDs]
- Applicable TRIPOD+AI Items: [Item numbers]

## 3. Drafting Content
[Insert section draft here, ensuring zero unevidenced numbers or causal overclaims]
"""),

    ("T27_tripod_ai_checklist.md", "T27", "tripod_ai_checklist.md", "OS §10.2, §15.2", "TRIPOD+AI (2024) Compliance Checklist Record", """
# TRIPOD+AI Compliance Audit Record

| Item # | TRIPOD+AI Domain & Checklist Requirement | Applicable? | Manuscript Section & Page Locator | Evidenced Entity ID | Compliance Check |
|---|---|---|---|---|---|
| 1 | Title identifying the study as developing/validating an AI prediction model | Yes | Title Page (p.1) | `WR0001` | PASS |
| 2 | Structured abstract covering objectives, data, methods, results, conclusions | Yes | Abstract (p.2) | `WR0002` | PASS |
| 3a | Scientific background, medical context, and clinical rationale | Yes | Introduction (pp.3-4) | `WR0003` | PASS |
| 3b | Specific research objectives and target prediction horizon | Yes | Introduction (p.4) | `WR0004` | PASS |
| 4a | Source of data, study setting, clinical sites, and eligibility criteria | Yes | Methods (p.5) | `SITE0001`, `DS0001` | PASS |
| 5a | Definition and operationalization of clinical outcome target | Yes | Methods (pp.5-6) | `endpoint_charter.md` | PASS |
| 6a | Candidate predictors across all 4 modalities and measurement protocols | Yes | Methods (pp.6-7) | `variables.csv` | PASS |
| 7a | Sample size and Events Per Variable (EPV) power considerations | Yes | Methods (p.7) | `DS0001` | PASS |
| 8a | Missing data handling and imputation mechanisms | Yes | Methods (p.8) | `PP0001` | PASS |
| 9a | Model architectures, baseline comparator hierarchy, and training details | Yes | Methods (pp.8-10) | `MC0001`, `EXP0001` | PASS |
| 10a | Evaluation metrics, probability calibration, and statistical methods | Yes | Methods (pp.10-11) | `EVAL0001` | PASS |
| 11a | Explainability (XAI) methodology and quantitative validation | Yes | Methods (pp.11-12) | `XAI0001` | PASS |
"""),

    ("T28_submission.md", "T28", "submission.md", "OS §10.2, §15.2", "Submission & Administrative Disposition Record", """
# SUB-YYYYMMDD-### — Submission & Handover Record

## 1. Submission Target
- Target Type: [FYDP Defense Final Submission / Q1 Journal Manuscript]
- Venue Name: [Daffodil International University CSE499 / Targeted Journal Name]
- Submission Date: YYYY-MM-DD

## 2. Deliverable Package & Hashes
- Primary Document File: `12_Writing/thesis/final_thesis.pdf` (or `manuscript.pdf`)
- Primary Document Hash (SHA-256): [Checksum]
- Supplementary Checklists: Completed TRIPOD+AI, PROBAST-AI audit
- Source Code Release Tag: [e.g., v1.0.0]

## 3. Institutional Sign-Off & Verification
- Author Declarations: Rayan Ahmed, Mohammad Nafis Sadiq
- Supervisor Sign-Off: Md. Mizanur Rahman
- Official Submission Receipt / Confirmation ID: [Receipt Number]
"""),

    ("T29_archive.md", "T29", "archive.md", "OS §11.2, §15.2", "Immutable Release Archive Record (ARCH####)", """
# ARCH#### — Immutable Research Release Archive

## 1. Archive Manifest
- Archive ID: `ARCH####`
- Release Tag: `v1.0.0`
- Timestamp: YYYY-MM-DDTHH:MM:SS+06:00
- Custodian: Academic Department / Lead Researchers

## 2. Preserved Artifacts & Cryptographic Checksums
| Component | Storage Path | Format | SHA-256 Checksum | PHI Sensitivity Tier |
|---|---|---|---|---|
| Complete Git Repository | `16_Archive/ARCH####/repo_snapshot.bundle` | Git Bundle | [Checksum] | Tier 1 |
| Final Thesis & Supplements | `16_Archive/ARCH####/thesis_final.pdf` | PDF | [Checksum] | Tier 1 |
| Q1 Manuscript & Checklist | `16_Archive/ARCH####/manuscript_q1.pdf` | PDF | [Checksum] | Tier 1 |
| Frozen Trained Weights | `Tier3/ARCH####/checkpoints/` | PyTorch Binary | [Checksum] | Tier 3 |
| De-Identified Test Cohort | `Tier2B/ARCH####/cohort/` | Encrypted CSV/WFDB | [Checksum] | Tier 2B |

## 3. Restoration Test Evidence
- Clean Restore Test Date: YYYY-MM-DD
- Replay Status: PASS (100% hash and output reproduction confirmed)
"""),

    ("T30_risk_meeting.md", "T30", "risk_meeting.md", "OS §13, §15.2", "Milestone & Risk Governance Meeting Minutes", """
# MEET-YYYYMMDD-### — Milestone & Risk Review Meeting

## 1. Meeting Overview
- Date & Time: YYYY-MM-DDTHH:MM:SS+06:00
- Attendees: Md. Mizanur Rahman (Supervisor), Rayan Ahmed, Mohammad Nafis Sadiq
- Objective: Gate Review & Domain Risk Assessment

## 2. Gate & Milestone Progress Audit
- Current Stage: [Stage ID]
- Recent Gates Evaluated: [Gate ID - Outcome]
- Upcoming Blockers: [List blocking items]

## 3. Domain Risk Register Review
- High-Risk Review: [Discuss IRB progress, data intake, compute budget]
- Updated Risk Mitigations: [Document adjusted contingency plans]

## 4. Supervisor Feedback & Directives
- Feedback Summary: [Key recommendations from supervisor]
- Action Items Assigned: [Owner - Task - Due Date]
"""),

    ("T31_prompt.md", "T31", "prompt.md", "OS §12, §15.2", "AI Task Prompt Specification Contract", """
# PROMPT-### — [AI Task Role & Prompt Contract]

## 1. Role & Task Boundary
- Assigned AI Role: [e.g., Code Implementer / Literature Review Assistant / Statistical Analyst]
- Task Objective: [Specific bounded task]
- Governing Handbook Sections: [OS §#]

## 2. Authorized Inputs & Paths
- Allowed Read Paths: [List explicit file paths]
- Allowed Write Paths: [List explicit file paths]
- Prohibited Modifications: Core governance files, immutable releases, sealed test sets

## 3. Strict Biomedical & Ethical Guardrails
- **PROHIBITION:** Never paste patient identifiers, raw hospital charts, or PHI into prompts.
- **ZERO FABRICATION:** If data or literature citations are missing, mark `not reported` or `Unresolved / Human Decision Required`.
- **HUMAN BOUNDARY:** Clinical definitions and gate sign-offs strictly require qualified human review.
"""),

    ("T32_config.yaml", "T32", "config.yaml", "OS §6.2, §15.2, §15.3", "Executable Multimodal Experiment Configuration Skeleton", """# Multimodal Experiment Configuration Template (T32)
# Null values strictly prohibit execution. All fields must be resolved prior to launch.

experiment_id: null
research_question_id: null
comparator_tier: null          # unimodal | clinical_score | simple_fusion | transformer_fusion | ablation
approval_record: null
source_commit: null

data:
  release_id: null
  dataset_id: null
  adjudication_id: null
  split_id: null
  preprocessing_id: null
  fit_state_sha256: null
  variables_sha256: null
  active_modalities: [clinical, ecg, laboratory, lifestyle]
  missing_modality_policy: null # complete_case | mask_token | indicator

model:
  framework: null              # pytorch | tensorflow (UD13)
  framework_version: null
  architecture_name: null
  modality_encoders:
    clinical: null
    ecg: null
    laboratory: null
    lifestyle: null
  fusion_module: null          # cross_modal_transformer_fusion | early_concat | late_ensemble
  pretrained_weights_sha256: null
  license_record: null

training:
  seed: null
  deterministic_mode: true
  epochs_or_budget: null
  batch_size: null
  optimizer_and_schedule: null
  loss_and_imbalance_policy: null
  regularization: null
  early_stopping_monitor: val_roc_auc

evaluation_and_calibration:
  protocol_sha256: null
  validation_only_tuning: true
  calibration_candidate: null # platt | isotonic | temperature
  threshold_rule: null        # youden_j | f1_optimal | sensitivity_target
  mandatory_metrics: [accuracy, precision, recall, f1, roc_auc, confusion_matrix]
  adopted_q1_metrics: [pr_auc, specificity, npv, brier_score, ece, dca]

xai_hooks:
  explainer_type: null        # tree_shap | gradient_shap | partition_shap
  background_partition: train # NEVER validation or test

runtime:
  environment_lock_sha256: null
  hardware_record: null
checkpoint_policy: best_validation_loss_and_auc
artifact_destination: null
""")
]

def main():
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    for filename, t_id, name, gov, title, body in TEMPLATES:
        path = os.path.join(TEMPLATES_DIR, filename)
        if filename.endswith(".yaml"):
            content = body.strip() + "\n"
        else:
            header = COMMON_HEADER.format(
                title=title,
                template_id=t_id,
                template_name=name,
                governing_section=gov
            )
            content = (header + body).strip() + "\n"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created template: {filename}")

if __name__ == "__main__":
    main()
