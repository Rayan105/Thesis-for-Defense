# CVD MULTIMODAL RESEARCH OPERATING SYSTEM

## Cover page

**Approved research title:** An Explainable Multimodal Framework for Early Cardiovascular Disease Risk Prediction Using Clinical, ECG, Laboratory, and Lifestyle Data.

| Field | Value |
|---|---|
| Document | CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md |
| Type | Project-specific research governance and Q1-grade operational handbook |
| Version / date | v1.0.0 / 2026-11-20 |
| Status | Complete planning document; proposed operating policies awaiting human ratification; research execution NOT VERIFIED |
| Institution | Daffodil International University, Department of Computer Science and Engineering (proposal approval form) |
| Report context | Course Code: CSE499; Title: FYDP (Title Defense); Proposal Approval Form; Semester: Summer 2026; Date: 09.07.2026 |
| Researchers | Rayan Ahmed, ID 232-15-847 (1st Member); Mohammad Nafis Sadiq, ID 232-15-895 (2nd Member) |
| Supervisor | Md. Mizanur Rahman, Senior Lecturer (proposal approval form; signed 09.07.26) |
| Co-supervisor | None listed on the supplied Proposal Approval Form |
| Operational owner | Research team; named task owners, hospital data custodian, and qualified cardiologist/clinical adjudicator remain to be assigned |
| Scientific authority | [FYDP Title Proposal](./fydp_title_proposal.pdf) (6-page scanned Proposal Approval Form and Detailed Proposal, SHA-256 recorded in [Appendix F](#appendix-f)), interpreted within the approved scope and Q1 methodological standards |
| Execution companion | [CVD Multimodal Project Execution Blueprint](./CVD_MULTIMODAL_PROJECT_EXECUTION_BLUEPRINT.md) |
| Intended output | Reproducible explainable multimodal CVD risk-prediction framework, FYDP thesis, Q1-grade journal manuscript (TRIPOD+AI compliant), and research decision-support prototype; supplementary research aid, NOT validated clinical diagnosis or clinical deployment |

The signed Proposal Approval Form on page 1 endorses the FYDP proposal and title for departmental progression and states that the students will attach it to their FYDP Title Phase Evaluation Report. It does **not** constitute Institutional Review Board (IRB) or ethical approval, hospital data-collection permission, informed consent/waiver, a clinical validation study, a finalized variable/endpoint ontology, or ratification of the new operational policies introduced here. No such approval is inferred.

## Version history

| Version | Date | Change | Approval state |
|---|---|---|---|
| v1.0.0 | 2026-11-20 | Initial proposal-grounded CVD multimodal handbook and aligned 17-stage, 50-step, 17-gate Q1 execution architecture | Proposed; no execution gates passed |

Record subsequent changes with author, reason, affected decisions, affected steps, and approval evidence. A title or scope change requires formal supervisor review (note that section IV "Updated Title" on p.1 is currently blank); a typographical correction does not silently alter scientific commitments.

## Table of contents

1. [Executive summary](#executive-summary)
2. [1. Project constitution and source authority](#os-01)
3. [2. Repository architecture and folder contracts](#os-02)
4. [3. Literature and research-question workflow](#os-03)
5. [4. Cohort collection, multimodal preprocessing, and leakage-safe splitting](#os-04)
6. [5. Clinical endpoint, four-modality schema, and ground-truth QA](#os-05)
7. [6. Multimodal modeling, Transformer fusion, and experiment operating system](#os-06)
8. [7. Evaluation, calibration, statistical inference, and clinical utility protocol](#os-07)
9. [8. Explainable AI (XAI) governance, faithfulness, and clinical plausibility](#os-08)
10. [9. Research prototype, reproducibility, and optional defense interface](#os-09)
11. [10. Q1 journal and FYDP thesis writing and submission operating system](#os-10)
12. [11. Version control, PHI security, and tiered artifact storage](#os-11)
13. [12. Roles, human decisions, and AI-assisted task contracts](#os-12)
14. [13. Daily research operations and Q1 risk governance](#os-13)
15. [14. Quality gates and completion](#os-14)
16. [15. Template library](#os-15)
17. [Appendix A. Canonical definitions](#appendix-a)
18. [Appendix B. Registry catalog and schemas](#appendix-b)
19. [Appendix C. Stage map and dependency chain](#appendix-c)
20. [Appendix D. Glossary](#appendix-d)
21. [Appendix E. Acronyms](#appendix-e)
22. [Appendix F. Source coverage and self-review](#appendix-f)

<a id="executive-summary"></a>
## Executive summary

This handbook governs ethical cohort acquisition, four-modality data curation, clinical endpoint adjudication, leakage-free preprocessing, unimodal and multimodal baseline benchmarking, Transformer-based multimodal fusion training, validation selection, held-out testing, probability calibration, statistical inference, quantitative Explainable AI (SHAP) evaluation, and Q1-grade manuscript preparation for early cardiovascular disease (CVD) risk prediction. The four approved data modalities are **clinical data**, **electrocardiogram (ECG) signals**, **laboratory test results**, and **lifestyle information**. The mandatory evaluation metrics explicitly specified in the proposal are **Accuracy, Precision, Recall, F1-Score, ROC-AUC, and Confusion Matrix**.

To meet **Q1 medical-AI and biomedical-informatics journal standards** (such as *IEEE Journal of Biomedical and Health Informatics*, *Computers in Biology and Medicine*, *Artificial Intelligence in Medicine*, *Journal of Biomedical Informatics*, *Information Fusion*, or *npj Digital Medicine*), this operating system preserves every proposal commitment while systematically closing the six methodological failure modes that cause Q1 desk rejection:

1. **Zero-bibliography proposal:** The supplied 6-page proposal contains no formal citations or reference list. Literature review must be executed systematically from primary databases to test—and if necessary narrow or refute—the proposal's five gap claims (`PG1–PG5`).
2. **Workflow leakage trap:** The proposal's Workflow Diagram (p.5) draws Data Preprocessing (Box 2) and Feature Extraction (Box 3) visually before Train/Validation/Test Split (Box 4). This handbook preserves the conceptual workflow while enforcing strict leakage isolation: only deterministic record-local cleaning precedes patient-level splitting; all dataset-fitted imputation, scaling, encoding, resampling, and learned feature extraction happen exclusively on the training partition after splitting.
3. **Clinical endpoint and temporal ambiguity:** "Early CVD risk prediction" requires an exact operational outcome definition (prospective longitudinal incidence vs cross-sectional early-stage/diagnostic detection), an explicit index time ($t_0$), and a modality synchronization window ($\Delta t$) to eliminate post-diagnosis and treatment leakage.
4. **Baseline and ablation rigor:** A Q1 paper cannot rely on one Transformer model compared against a weak single-modality baseline. This plan mandates fair unimodal baselines across all four modalities (including Logistic Regression, Random Forest, SVM, XGBoost, and deep ECG architectures such as CNN, LSTM, and Transformer mentioned on pp.2–3), simple early/late fusion baselines, optional clinical risk-score benchmarks, Leave-One-Modality-Out and progressive modality ablations, missing-modality robustness tests, and multi-seed variance reporting.
5. **Beyond raw accuracy:** Alongside all six mandatory proposal metrics, this plan recommends Q1 clinical prediction essentials (explicitly tagged as `PLANNING RECOMMENDATION` / `UD` adoption): PR-AUC, Specificity/NPV, probability calibration (Brier score, ECE, calibration slope/intercept), Decision Curve Analysis (DCA), patient-level bootstrap 95% confidence intervals, paired DeLong/McNemar testing with multiple-comparison correction, subgroup fairness, and TRIPOD+AI / PROBAST-AI compliance.
6. **Quantitative XAI rigor:** Producing SHAP summary plots alone is insufficient for Q1 publication. This plan governs multimodal SHAP engineering (tabular + ECG + modality-level attribution), objective faithfulness testing (deletion/insertion perturbation curves, AOPC, concordance with modality ablation), multi-seed stability, spurious-shortcut auditing, and qualified clinician plausibility review—while forbidding unproven "increased clinician trust" claims without a separate IRB-approved reader study.

This is a **planning document**, not an account of completed research. All 17 gates (`G01–G17`) initially have status **NOT ASSESSED**, which blocks dependent work just as a failed gate does. Empty registries, proposed checks, and this document's self-review are not evidence that data has been collected, IRB approved, models trained, or scientific gates passed.

<a id="os-01"></a>
# 1. Project constitution and source authority

## 1.1 Authority and evidence labels

Use the following epistemic labels consistently across all decisions, registries, experiment reports, thesis chapters, and Q1 manuscript drafts:

- **PROPOSAL FACT:** content explicitly present in the supplied [fydp_title_proposal.pdf](./fydp_title_proposal.pdf), with physical PDF page and section/figure locator. A proposal assertion about existing literature (e.g., in Background Study or Gap Analysis) is a fact about what the proposal *claims*, not independent verification of the literature.
- **PLANNING RECOMMENDATION:** a proposed scientific, statistical, XAI, or operational standard introduced by this handbook (including Q1 methodological extensions such as calibration, DCA, DeLong testing, faithfulness benchmarks, and TRIPOD+AI compliance). It becomes an adopted project policy only when the responsible human records approval; it is never falsely attributed to the proposal.
- **Unresolved / Human Decision Required:** missing, ambiguous, unverified, or resource/ethics-dependent information requiring a named decision owner and documented evidence before its blocking milestone.

Authority order: approved FYDP proposal and scope (`fydp_title_proposal.pdf`); recorded supervisor-approved clarifications and institutional IRB/ethics determinations within that scope; this handbook; the companion execution blueprint; verified implementation configurations. Structural inspiration from prior research operating system patterns governs operational discipline only; no scientific domain assumptions, architectures, or platform mandates from unrelated projects are inherited. If an implementation conflicts with a governing policy, stop dependent work, record the conflict, and repair the code or formally amend the policy without retroactively reinterpreting historical results.

## 1.2 Source-grounded facts ledger

Physical page numbers below run from page 1 (signed Proposal Approval Form) to page 6 (Expected Outcomes and Conclusion). Every page in `fydp_title_proposal.pdf` is a scanned document image with zero embedded text layer; all six pages were visually inspected in full during authoring.

| ID | PROPOSAL FACT | Locator | Operational implication |
|---|---|---|---|
| RF01 | Approved title: "An Explainable Multimodal Framework for Early Cardiovascular Disease Risk Prediction Using Clinical, ECG, Laboratory, and Lifestyle Data"; Updated Title field is blank | p.1, Sections III–IV | Preserve title verbatim across project records unless formally amended by supervisor |
| RF02 | Institution: Daffodil International University, Dept. of CSE; Course: CSE499 FYDP (Title Defense); Semester: Summer 2026; Approval Date: 09.07.2026; Supervisor: Md. Mizanur Rahman (Senior Lecturer, signed 09.07.26); Members: Rayan Ahmed (232-15-847) and Mohammad Nafis Sadiq (232-15-895) | p.1, Header and Sections I–II, Signature block | Record exact institutional identity; note that approval form will be attached to Title Phase Evaluation Report and is not IRB or dataset permission |
| RF03 | Main objective: develop an explainable multimodal framework for early CVD prediction integrating clinical information, ECG signals, laboratory test results, and lifestyle factors, incorporating XAI to explain predictions and support AI-assisted clinical decision-making | p.2, Section V.1 (Objective) | Core scope requires four-modality integration plus XAI; clinical trust/utility remains an aspiration requiring separate human study if claimed |
| RF04 | Motivation notes CVD as a leading cause of death worldwide, including in Bangladesh, and cites two motivational challenges: single-modality reliance and "black box" AI opacity reducing clinician confidence | p.2, Section V.2 (Motivation) | Contextualizes Bangladesh clinical relevance; empirical epidemiology statistics must be sourced from verified literature, not unreferenced prose |
| RF05 | Background Study mentions traditional ML models (Logistic Regression, Random Forest, SVM, XGBoost) for clinical datasets, deep learning models (CNNs, LSTMs, Transformer-based architectures) especially for ECG analysis, multimodal learning (including medical images in general literature), and XAI methods (SHAP, LIME) | pp.2–3, Section V.3 (Background Study) | Defines natural baseline comparator families; note that medical imaging is contextual literature only and NOT one of this study's four modalities |
| RF06 | The supplied 6-page proposal contains **zero formal references, citations, or bibliography** and **no examiner feedback sheet** | pp.1–6 (entire document) | Systematic literature search must be built from scratch; confirm under UD01 whether a separate Title Phase Evaluation Report or examiner feedback exists |
| RF07 | Gap Analysis proposes five limitations (`PG1–PG5`): (PG1) most studies use one healthcare data type; (PG2) multimodal systems often combine only two sources; (PG3) many AI models do not explain predictions; (PG4) lifestyle information is often ignored; (PG5) few studies build an explainable multimodal framework combining multiple sources | p.3, Section V.4 (Gap Analysis) | Treat `PG1–PG5` strictly as falsifiable hypotheses to test against direct and contradicting literature in STEP-004–009 |
| RF08 | Proposed Techniques and Tools list: Python, TensorFlow / PyTorch, Scikit-learn, Pandas, NumPy, Matplotlib, SHAP for Explainable AI, and Transformer-based Multimodal Fusion Network | p.4, Section V.5 (Techniques and Tools) | Framework choice (PyTorch vs TensorFlow) is unresolved; Transformer-based multimodal fusion and SHAP are core methodological anchors |
| RF09 | Primary dataset is proposed to be collected from hospitals or diagnostic centers **after obtaining required ethical approval** | p.4, Section V.5 (Data Collection) | Zero data is currently acquired; IRB/ethics approval and hospital agreements are hard prerequisites before any collection or intake |
| RF10 | Four proposed data modalities and examples: Clinical Data (Age, Gender, BMI, Blood Pressure, Medical History); ECG Signals; Laboratory Test Results (Blood Glucose, Cholesterol, Creatinine, etc.); Lifestyle Information (Smoking, Diet, Physical Activity, Sleep, Family History) | p.4, Section V.5 (Data Collection) | Examples are not a complete clinical variable dictionary, unit specification, ECG acquisition format, or outcome definition; Family History placement requires explicit schema documentation |
| RF11 | Data Analysis specifies processing each modality separately to extract meaningful features and combining them via multimodal fusion for disease prediction, followed by SHAP to explain feature contributions | pp.4–5, Section V.5 (Data Analysis) | Supports modality-specific encoders + fusion + multimodal attribution; exact fusion level and ECG representation remain unresolved |
| RF12 | Required performance metrics listed in text: Accuracy, Precision, Recall, F1-Score, ROC-AUC, and Confusion Matrix | p.4, Section V.5 (Data Analysis) | All six are mandatory in final reporting, including unfavorable results; operating threshold and class-imbalance caveats must be documented |
| RF13 | Workflow Diagram specifies 9 steps: (1) Primary Data Collection → (2) Data Preprocessing (clean, normalize, handle missing data) → (3) Feature Extraction (from each modality) → (4) Train/Validation/Test Split → (5) Multimodal Data Fusion → (6) Explainable AI Model Training → (7) CVD Risk Prediction → (8) Explainability Analysis (SHAP) → (9) Performance Evaluation (Accuracy, Precision, Recall, F1-score, ROC-AUC) | p.5, Figure: Workflow Diagram | Preserves conceptual lifecycle; **critical methodological safeguard required:** dataset-dependent normalization, imputation, and learned feature extraction MUST be fit strictly after patient-level splitting to prevent data leakage |
| RF14 | Workflow Diagram does not specify train/validation/test split proportions, cross-validation strategy, sample size, CVD clinical outcome criteria, prediction time horizon, or ECG signal format | p.5, Figure: Workflow Diagram; pp.4–5 | All missing methodological parameters are tracked as explicit blocking unknowns in Section 1.6 |
| RF15 | Expected Outcomes state expected higher accuracy and reliability vs traditional single-modal models, XAI identification of influential risk factors, potential support for faster/more informed clinical decisions, and contribution to trustworthy explainable medical AI | p.6, Section V.6 (Expected Outcomes) | Treat superiority over unimodal baselines as an empirical hypothesis to test, not an assumed result; prohibit unproven clinical-speed/trust claims |
| RF16 | Conclusion frames the expected output as a reliable decision-support system assisting healthcare professionals in early detection and prevention of CVD | p.6, Section V.7 (Conclusion) | Bounds output as a research decision-support prototype; clinical deployment and autonomous medical advice remain strictly out of scope |
| RF17 | No compute hardware, dataset size, class prevalence, model hyperparameter values, numeric accuracy/AUC target, or target journal venue is fixed in the proposal | pp.1–6 | Must be resolved transparently through feasibility audits and human decisions without arbitrary fabrication |
| RF18 | Proposal Approval Form explicitly anticipates attaching the form to a future FYDP Title Phase Evaluation Report | p.1, Approval paragraph | Confirm whether additional evaluation-report constraints or supervisor comments supersede or refine initial proposal statements (UD01) |

## 1.3 Binding scope and exclusions

**In scope:** Systematic literature review and gap verification; IRB/ethics-approved primary 4-modality cohort collection from hospitals/diagnostic centers (clinical, ECG, laboratory, lifestyle) plus optional compatible external public cohort validation for Q1 generalizability; clinical endpoint definition and qualified adjudication; leakage-safe patient/site-level splitting and modality-specific preprocessing; unimodal baselines (LR, RF, SVM, XGBoost, CNN, LSTM, Transformer), simple fusion baselines, optional clinical risk-score benchmarks, and Transformer-based multimodal fusion modeling; systematic modality and architectural ablations; mandatory proposal metrics plus adopted Q1 calibration, statistical inference, and clinical-utility evaluations; multimodal SHAP explanation generation, quantitative faithfulness/stability benchmarking, shortcut auditing, and clinical plausibility review; reproducible research prototype (with optional defense interface under UD22); FYDP thesis and Q1 journal manuscript preparation compliant with TRIPOD+AI.

**Outside the present approved study:** Medical imaging modalities (echocardiography, cardiac MRI, coronary CT angiography, chest X-ray) as primary input modalities (they may appear only as contextual literature); autonomous clinical diagnosis; individualized medication or treatment prescription; unapproved clinical deployment in live hospital workflows; claiming proven reduction in clinician decision time, improved patient survival, or statistically proven clinician trust without conducting a separate IRB-approved prospective clinical reader/impact trial.

**Clinical safety & interpretation boundaries:**
- A low predicted risk score is **never** proof of absence of cardiovascular disease; a high predicted risk score is a statistical risk estimate, not a definitive diagnosis.
- Raw neural network logits/softmax outputs are uncalibrated model scores unless explicitly calibrated on validation data and verified on held-out test data.
- SHAP values explain *how the model used its inputs*, NOT biological causality. Attributing causal risk-factor status from observational SHAP values is strictly prohibited in Q1 writing.

## 1.4 Objectives and candidate research questions

The proposal's core objective (`RF03`, `RF11–RF15`) is decomposed into four operational objectives (`O1–O4`) aligned to Q1 publishability:

| Objective | Operational interpretation (PLANNING RECOMMENDATION) | Evidence required |
|---|---|---|
| O1: Ethical 4-modality cohort curation & preprocessing | Curate a synchronized, adjudicated, PHI-safe dataset combining clinical, ECG, laboratory, and lifestyle modalities under leakage-free preprocessing and patient-level splitting | IRB/ethics approval, data dictionary/CRF, adjudication QA, missingness/alignment report, immutable `SPLIT`/`PP`/`REL` hashes |
| O2: Transformer-based multimodal fusion vs rigorous baselines | Design and train a Transformer-based multimodal fusion network capable of integrating heterogeneous tabular and ECG representations (including missing-modality handling) and benchmark it fairly against unimodal, simple-fusion, and optional clinical baselines | Registered configs, multi-seed training logs, `MODEL` cards, Leave-One-Modality-Out and progressive modality ablations |
| O3: Clinical-grade predictive evaluation & calibration | Evaluate the frozen champion model on a sealed held-out test set (and external cohort if adopted) using all 6 required metrics plus adopted calibration, statistical significance, clinical utility (DCA), and subgroup/robustness audits | Frozen protocol, test coverage ledger, metrics, calibration curves, DeLong/bootstrap CIs, DCA, subgroup/error reports |
| O4: Faithfully evaluated multimodal XAI & Q1 dissemination | Generate global, local, and modality-level SHAP explanations, validate them via objective faithfulness/stability tests and cardiologist plausibility review, and deliver a reproducible prototype, FYDP thesis, and TRIPOD+AI-compliant Q1 manuscript | SHAP provenance, deletion/insertion AOPC, multi-seed stability, shortcut audit, clinician review, clean reproducibility audit, thesis & Q1 submission records |

**Candidate primary research question (awaiting G03 approval):** *Under a patient-level, leakage-controlled, and ethically adjudicated evaluation protocol, how accurately, reliably (in discrimination and probability calibration), and transparently (in quantitative faithfulness, stability, and clinical plausibility) can a Transformer-based multimodal fusion framework integrating clinical, ECG, laboratory, and lifestyle data predict early cardiovascular disease risk compared to unimodal and simpler fusion baselines?*

**Candidate subordinate questions (PLANNING RECOMMENDATION, awaiting G03):**
- **RQ1 (Multimodal gain & modality synergy):** Does integrating all four modalities via Transformer-based multimodal fusion achieve statistically significant gains in discrimination (ROC-AUC, PR-AUC, F1), calibration (Brier/ECE), and net clinical benefit (DCA) over unimodal models, simple early/late fusion baselines, and (where feasible) established clinical risk scores?
- **RQ2 (Incremental value of lifestyle & robustness to missing modalities):** What is the marginal predictive contribution of lifestyle, laboratory, and ECG modalities in progressive addition and Leave-One-Modality-Out ablations, and how gracefully does the fusion model degrade under realistic partial/missing-modality inference?
- **RQ3 (Quantitative XAI faithfulness, stability & clinical plausibility):** Are the multimodal SHAP attributions (across tabular features, ECG signal segments/features, and modality shares) quantitatively faithful under perturbation testing, stable across random seeds/resamples, free of spurious dataset shortcuts, and clinically plausible under qualified cardiologist review?
- **RQ4 (Subgroup fairness & generalizability):** How consistent are discrimination, calibration, and explanation patterns across demographic subgroups (age, sex), recruitment sites, and (if adopted) an external validation cohort?

Assign permanent RQ identifiers at `STEP-009` (`G03`). None of these questions presupposes a positive outcome; null or negative findings (e.g., if a tuned GBDT early-fusion baseline matches or outperforms a Transformer on a small cohort) are scientifically valid Q1 results when rigorously analyzed.

## 1.5 Research principles, biomedical ethics, and Q1 integrity standards

1. **Protocol before data/compute:** Approve the endpoint definition, leakage-free split, baseline hierarchy, statistical analysis plan, and XAI evaluation protocol before training or opening final test data.
2. **Absolute ethical and PHI discipline:** No hospital or diagnostic-center data collection begins before documented IRB/institutional ethical approval, site permission, and informed consent or IRB-documented waiver. Strip all Protected Health Information (PHI)—including names, national IDs, phone numbers, exact birthdates, hospital MRNs, and **burned-in ECG waveform headers/PDF metadata**—before analytical use. Maintain linkage keys in a separate encrypted vault.
3. **End-to-end provenance:** Trace every reported number, curve, and SHAP plot to exact `DS`, `ADJ`, `SPLIT`, `PP`, `REL`, `EXP`, `CKPT`, `MODEL`, `EVAL`, `XAI`, code commit, and SHA-256 hashes.
4. **Zero leakage tolerance:** Never fit imputers, scalers, encoders, oversamplers, feature selectors, or calibrators using validation or test information; never split multiple encounters of the same patient across partitions; never use post-diagnosis labs/ECGs/medications as predictors of the diagnosis itself.
5. **Preserve negative and null results:** Keep every failed, diverged, overfit, or inferior baseline/ablation run permanently registered. Never cherry-pick seeds, thresholds, or flattering SHAP patient examples.
6. **Honest uncertainty and bounded claims:** Never invent citations, sample sizes, IRB numbers, clinical validation claims, or causal interpretations of SHAP values.
7. **Q1 reporting discipline:** Align study design, bias self-assessment, and manuscript reporting with **TRIPOD+AI (2024)** and **PROBAST / PROBAST-AI** (adopted under UD23).
8. **Qualified clinical oversight:** Clinical endpoint definitions, ECG interpretation, outcome adjudication, and XAI clinical plausibility require qualified medical/cardiology input—never AI self-certification.

## 1.6 Unresolved decision register at initialization

Every row below is **Unresolved / Human Decision Required**. The canonical operational ledger is `01_Project_Management/decisions.csv`, backed by individual `01_Project_Management/decision_log/DEC####.md` records. `STEP-001` assigns owners and deadlines; it does not prematurely fabricate scientific choices.

| ID | Decision / missing evidence | Owner role | Resolve before | Required resolution evidence |
|---|---|---|---|---|
| UD01 | Confirm scope interpretation, operational owners, whether an Updated Title (p.1 §IV) or separate FYDP Title Phase Evaluation Report / examiner feedback exists | Researchers + supervisor | G01 / STEP-001 | Signed scope record; actual evaluation report/feedback or written confirmation none exists |
| UD02 | Exact clinical CVD endpoint definition, diagnostic/ascertainment criteria (ICD-10/clinical gold standard), binary vs multi-class/ordinal target, and prediction horizon (prospective follow-up vs cross-sectional early-stage detection) | Cardiologist + supervisor + researchers | G05 / STEP-014 | Written clinical endpoint charter preventing outcome-horizon mismatch |
| UD03 | Index time ($t_0$) definition and maximum allowable synchronization window ($\Delta t$) across Clinical, ECG, Lab, and Lifestyle records to prevent post-diagnosis/treatment leakage | Cardiologist + data lead | G05 / STEP-014 | Temporal alignment specification with explicit lookback/exclusion rules |
| UD04 | Participating hospital(s)/diagnostic center(s) in Bangladesh, recruitment mechanism (prospective vs retrospective, consecutive vs convenience), spectrum-bias controls, and target sample size / Events-Per-Variable (EPV) power analysis | Researchers + hospital custodian + supervisor | G04 / STEP-010–011 | Site list, sampling protocol, and formal sample-size/EPV calculation |
| UD05 | Institutional IRB / Ethics Committee approval, hospital administrative authorization, informed consent form or retrospective waiver, PHI de-identification, and data retention/sharing terms | Institution IRB + hospital custodian | Before ANY data collection; G04 / STEP-011 | Written IRB approval letter/protocol ID, site MOU/permission, consent/waiver documentation |
| UD06 | Whether an external public multimodal/CVD cohort (e.g., MIMIC-IV + MIMIC-IV-ECG, PTB-XL, UK Biobank, Framingham, NHANES — strictly candidate options requiring access/compatibility review) will be adopted for external validation or pretraining alongside primary hospital data | Researchers + supervisor | G04 / STEP-010–011 | Feasibility, licensing, modality-compatibility, and ethical access decision |
| UD07 | Exact ECG signal representation: raw digital 12-lead waveform (format e.g. XML/DICOM/WFDB/CSV, sampling rate, duration), single-lead digital waveform, extracted ECG tabular intervals, or digitized paper ECG (with digitization validation) | Clinical/ECG lead + hospital custodian | G04–G05 / STEP-013–015 | Sample file inspection, format specification, and signal-quality acceptance rules |
| UD08 | Finalized variable dictionary for Clinical, Laboratory, and Lifestyle modalities (exact variables, units, valid ranges, measurement instruments/CRF, resolution of Family History grouping, medication/treatment exclusion list) | Cardiologist + researchers | G05 / STEP-014–015 | Approved `04_Outcome_Schema_QA/variables.csv` and versioned CRF/extraction manual |
| UD09 | Outcome adjudication & data-abstraction QA plan: abstractor/clinician qualifications, pilot sample size, double-entry/inter-rater metrics ($\kappa$/ICC), acceptance thresholds, and discrepancy adjudication workflow | Cardiologist + researchers | G05 / STEP-015 (before pilot STEP-016) | Prospective QA protocol with named clinical adjudicator |
| UD10 | Patient/encounter/site grouping keys, duplicate detection rules, and missing-modality policy (complete-case inclusion threshold vs partial-modality cohort inclusion + missingness indicators) | Data lead + cardiologist | G06–G07 / STEP-018–020 | Grouping audit and explicit inclusion/missing-modality specification |
| UD11 | Operational split design: Train/Val/Test ratios vs nested cross-validation (crucial if primary $N$ is small), temporal or leave-one-site-out external holdout, stratification keys, and random seed | Researchers + supervisor + biostatistics reviewer | G07 / STEP-020 | Reproducible patient-level split specification and approval |
| UD12 | Preprocessing & feature-extraction choices: record-local ECG filtering (e.g., 50 Hz notch / bandpass verified for ST-T preservation), training-only imputation method (median/MICE/missForest/masking), scaling/transforms, categorical encoding, and tabular/ECG feature extraction | Implementer + clinical/ECG lead | G08 / STEP-019–022 | Geometry/morphology fidelity check, leakage-isolation audit, and approved `PP` config |
| UD13 | Deep learning framework choice (**PyTorch vs TensorFlow**, both listed on p.4), library versions, compute hardware (local GPU/institutional server/approved cloud), storage tiers, encryption, and Git remote/access policy | Researchers + institution IT/supervisor | G02 (storage & `environment/data/`); G09 (`environment/model/`) | Access/PHI-compliance decision and pinned environment locks |
| UD14 | Transformer-based multimodal fusion architecture design (modality encoders, token projection, cross-modal attention, missing-modality token/masking, pretraining strategy) and exact baseline suite (LR, RF, SVM, XGBoost/GBDT, 1D-CNN, LSTM, ECG Transformer, early/late fusion, optional clinical risk score) | Model lead + supervisor | G09 / STEP-023–025 | Candidate review, architectural specification, and baseline parity plan |
| UD15 | Training protocol: random seeds (minimum recommended $\ge 3$–$5$ for Q1 variance), hyperparameter search space/budget (validation-only), early-stopping criterion, class-imbalance strategy (loss weighting vs focal loss; caution on synthetic SMOTE), and checkpoint retention | Model lead + supervisor | G09 / STEP-025; each STEP-028 | Approved `experiment_plan.md` with resolved configuration contract |
| UD16 | Operating-threshold selection rule (for Accuracy, Precision, Recall, F1, Confusion Matrix — e.g., Youden's $J$, F1-optimal, or target sensitivity $\ge X\%$ on validation) and post-hoc probability calibration method (Platt/temperature scaling/isotonic on validation/OOF) | Evaluation lead + cardiologist + supervisor | G09 / STEP-025; freeze at G11 | Preregistered selection and calibration protocol |
| UD17 | Adoption of Q1 extended evaluation metrics (PR-AUC, Specificity, NPV, Balanced Accuracy, Brier score, ECE, calibration slope/intercept, Decision Curve Analysis threshold range) alongside the 6 mandatory proposal metrics | Evaluation lead + supervisor | G09 / STEP-025; freeze at G11 | Preregistered evaluation protocol distinguishing mandatory vs adopted Q1 metrics |
| UD18 | Statistical inference plan: patient-level bootstrap repetitions ($B$), confidence interval method (BCa/percentile), paired comparison tests (DeLong for ROC-AUC, paired bootstrap/McNemar), multiple-comparison correction method, and subgroup stratification definitions | Biostatistics reviewer + supervisor | G09 / STEP-025; freeze at G11 | Preregistered statistical analysis plan |
| UD19 | Multimodal SHAP specification: exact explainer algorithm(s) for Transformer fusion and tree baselines, training-only background sample size/stratification, ECG attribution granularity (waveform patches/beats/leads vs extracted ECG features), modality-share aggregation, and optional LIME/IG comparator | XAI lead + model lead | G09 / STEP-025; freeze at G11 | Technical XAI protocol verifying additivity, runtime feasibility, and leakage safety |
| UD20 | Quantitative XAI faithfulness & stability benchmarks: perturbation baseline (mean/marginal/conditional), deletion/insertion curve metrics (AOPC/comprehensiveness/sufficiency), multi-seed rank-correlation metrics, and shortcut-audit criteria | XAI lead + supervisor | G09 / STEP-025; freeze at G11 | Approved XAI verification protocol before interpreting explanations |
| UD21 | Clinical XAI plausibility review design: cardiologist sampling strategy (stratified TP/FP/TN/FN), structured rubric, and whether an IRB-approved clinician reader/usability study will be conducted (or explicitly excluded from claims) | Cardiologist + supervisor | G09 / STEP-025; executed at STEP-040 | Approved clinical review rubric and explicit claim-boundary decision |
| UD22 | Research prototype interface (CLI/script vs local interactive dashboard vs optional hosted web demo for FYDP defense), permitted synthetic/de-identified demo inputs, disclaimer wording, and hosting/privacy controls if web-hosted | Researchers + supervisor + custodian | STEP-041 (early decision if web demo wanted) | Prototype interface & disclosure decision; never clinical deployment |
| UD23 | Q1 target journal shortlist, reporting checklist adoption (**TRIPOD+AI 2024**, **PROBAST-AI**, **PRISMA** for lit search), FYDP thesis institutional format/deadlines, authorship order, and publication timeline/disposition | Researchers + supervisor | STEP-043; refined before G16 | Actual university format guide, journal author guidelines, and signed author agreement |
| UD24 | Quantitative scientific success/utility criteria (if supervisor requires a minimum benchmark or non-inferiority margin), explicitly distinguished from technical gate validity | Supervisor + researchers | G09 / STEP-025 | Grounded rationale; low/null performance remains scientifically reportable |
| UD25 | Release licensing (code vs pretrained weights vs de-identified metadata/summary statistics), controlled-access data-availability statement for Q1 journal, post-project custodian ownership, and retention/destruction schedule | Researchers + hospital custodian + IRB | STEP-049; permissions checked before any upload | Tiered release/retention agreement complying with IRB and Q1 journal policies |
| UD26 | Compute-budget contingency and small-$N$ regularization fallback (e.g., frozen pretrained ECG encoder / transfer learning, parameter-efficient cross-modal fusion, or nested CV) if primary hospital enrollment is smaller than expected | Researchers + supervisor | G04 / STEP-013; reviewed at G09 | Prospective contingency rule avoiding post-hoc architectural fishing on test data |

New unknowns receive sequential `UD##` IDs. The companion blueprint references this register verbatim; a software library default never resolves a blocking `UD##`.

<a id="os-02"></a>
# 2. Repository architecture and folder contracts

## 2.1 Proposed repository layout

Only the two planning documents are created at this planning stage alongside the user's supplied `fydp_title_proposal.pdf`. The directory layout below is the **future project repository contract**, instantiated at `STEP-002` and `STEP-003`. Listed paths are contracts, not assertions that files currently exist.

```text
workspace/
  fydp_title_proposal.pdf                    # preserved immutable source proposal
  CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md
  CVD_MULTIMODAL_PROJECT_EXECUTION_BLUEPRINT.md
  README.md
  CHANGELOG.md
  CONTRIBUTING.md
  LICENSE                                    # created only after UD25 approval
  .gitignore
  .gitattributes
  environment/
    data/                                    # minimal data/ECG/registry tooling lock (STEP-002)
    model/                                   # PyTorch/TF + SHAP + stats lock (STEP-024)
  src/cvd_mm/                                # reusable Python package; thin CLI callers
  tests/                                     # unit/leakage/metric/XAI tests on synthetic fixtures
  01_Project_Management/                     # scope, decisions, risks, gates, diary, meetings
  02_Literature/                             # searches, screening, summaries, gaps, claims, bib
  03_Datasets_Cohort/                        # sites, IRB/DUA pointers, raw/ (restricted), QC, splits, releases
  04_Outcome_Schema_QA/                      # endpoint charter, variables.csv, CRF, adjudication, pilot/QA
  05_Preprocessing_Alignment/                # alignment specs, ECG filters, fitted states, processed/ (restricted)
  06_Models_Fusion/                          # candidates, architectures, baseline plan, model cards
  07_Experiments/                            # experiment_plan, registry, immutable EXP#### bundles
  08_Checkpoints/                            # checkpoint_policy, registry, hashes, artifact pointers
  09_Evaluation_Stats/                       # protocol, freeze, EVAL#### metrics, calibration, DCA, stats, subgroups
  10_Explainability_XAI/                     # xai_protocol, XAI#### SHAP, faithfulness, stability, clinician review
  11_Figures_Tables/                         # Q1 specs, source data, scripts, rendered vector/high-DPI assets
  12_Writing/                                # writing_registry, thesis/, paper_q1/, checklists/, reviews/
  13_Documentation/                          # installation, pipeline, prototype_guide, reproduce, data_access
  14_Automation/                             # thin CLI commands for audits, checks, figure generation
  15_Templates_Prompts/                      # blank templates T01-T32 and AI prompt templates
  16_Archive/                                # immutable ARCH#### snapshots, receipts, restoration proof
  prototype_ui/                              # optional thin defense interface ONLY if approved under UD22
```

## 2.2 Folder contracts

Every materialized domain folder contains a `README.md` (`T01`) specifying purpose, owner, inputs, outputs, PHI sensitivity, commands/workflow, and governing handbook sections. Do not populate unused frameworks merely to fill folders.

| Home | Writes / reads | Allowed contents and contract | Forbidden / validation |
|---|---|---|---|
| `environment/` | Implementer / all executors | `data/` lock + `verification.md` (STEP-002); `model/` lock + `versions.md` + hardware record (STEP-024) | No untested speculative pins; no credentials or tokens |
| `src/cvd_mm/` | Implementer / pipeline users | Modular Python code for intake, ECG signal checks, tabular schema checks, grouped splitting, leakage-safe preprocessing, unimodal/fusion/Transformer models, calibration, metrics, stats, SHAP/faithfulness, prototype inference | No patient records, raw ECGs, trained weight binaries, hardcoded clinical paths, or hidden hyperparameters |
| `tests/` | Implementer / reviewer | Synthetic-fixture tests for leakage guards, ECG morphology preservation, patient-grouped splits, all 6+ metrics, calibration, DeLong/bootstrap, SHAP additivity & perturbation, prototype error handling | Zero real patient records or identifiable ECG snippets |
| `01_Project_Management/` | Researchers / all roles | `scope.md`, `decisions.csv`, `decision_log/DEC####.md`, `risk_register.csv`, `gates.csv`, `reviews/G##_*.md`, `diary/`, `meetings/`, `dashboard.md`, `timeline.md` | No fabricated IRB/supervisor approvals; no PHI linkage |
| `02_Literature/` | Literature lead / modeling & writing | `searches/`, `papers.csv`, `screening.csv`, permitted `papers/`, `summaries/P####.md`, `gaps.csv`, `gap_notes/`, `claims.csv`, `references.bib`, `synthesis.md`, `research_questions.md` | No redistributing paywalled PDFs in public Git; no unread citations |
| `03_Datasets_Cohort/` | Data steward / preprocessing & modeling | `sites.csv`, `datasets.csv`, `releases.csv`, `irb_permissions/` (restricted pointers), restricted `raw/`, `manifests/`, `reports/` (QC, missingness, cohort cards), `splits/SPLIT####/` | Raw patient/ECG bytes immutable and strictly excluded from Git; PHI linkage key vault isolated separately |
| `04_Outcome_Schema_QA/` | Clinical schema lead / data & evaluation | `endpoint_charter.md`, `variables.csv`, `crf/`, `ecg_contract.md`, `adjudication_registry.csv`, `reviews/` (pilot & production QA), restricted `adjudications/` | No silent endpoint drift, undocumented unit conversion, or unreviewed labels termed ground truth |
| `05_Preprocessing_Alignment/` | Implementer / modeling & evaluation | `preprocessing_registry.csv`, `specs/`, versioned `configs/`, `reports/` (alignment, ECG filter fidelity, leakage checks); restricted `fitted_states/` and `processed/` | Reusable logic stays in `src/cvd_mm/`; no raw overwrites; no pre-split fitted parameters |
| `06_Models_Fusion/` | Model lead / experiments & evaluation | `candidates.csv`, `model_registry.csv`, `baseline_plan.md`, `architectures/`, `cards/MODEL####.md`, artifact pointers | No anonymous weights, undocumented pretrained encoders, or unverified licenses |
| `07_Experiments/` | Experiment lead / evaluation & writing | `experiment_plan.md`, `experiment_registry.csv`, `EXP####/config.yaml`, `README.md`, `run_manifest.json`, logs, observations, failure reports | Never edit a launched config; never delete failed/diverged/negative runs |
| `08_Checkpoints/` | Experiment lead / recovery & inference | `checkpoint_policy.md`, `checkpoint_registry.csv`, `manifests/`, checksums and artifact-store pointers | Model binaries live in approved artifact tier, not ordinary Git |
| `09_Evaluation_Stats/` | Evaluation lead / XAI & writing | `protocol.md`, `freeze.md`, `evaluation_registry.csv`, `EVAL####/` (safe aggregate metrics, calibration, DCA, stats, subgroup/robustness reports, error & PROBAST-AI reviews; restricted per-patient predictions in artifact tier) | No test-driven threshold/calibrator/model tuning; no per-patient PHI in Git |
| `10_Explainability_XAI/` | XAI lead / clinical review & writing | `xai_protocol.md`, `xai_registry.csv`, `XAI####/` (global/modality SHAP aggregates, faithfulness AOPC curves, multi-seed stability, shortcut audit, cardiologist plausibility summaries; restricted patient-level plots in artifact tier) | No cherry-picked patient explanations; no causal claims from observational SHAP; no test-set background data |
| `11_Figures_Tables/` | Analysts / writing | `assets.csv`, `specs/`, `data/` (safe aggregated plot data), `rendered/` (PDF/SVG/300–600 DPI PNG), captions, generator commands | No hand-edited plot values; no identifiable patient/ECG headers in rendered figures |
| `12_Writing/` | Authors / reviewers | `writing_registry.csv`, `writing_plan.md`, `thesis/`, `paper_q1/`, `checklists/` (`TRIPOD_AI.csv`, `PROBAST_AI.md`, `PRISMA.md`), `reviews/` (supervisor & journal peer-review rebuttals), submission receipts | No unsupported clinical/novelty claims; single canonical bibliography derived from `02_Literature/references.bib` |
| `13_Documentation/` | Implementer & researchers / reproducer | `installation.md`, `pipeline.md`, `prototype_guide.md`, `reproduce.md`, `reproducibility_audit.md`, `data_access.md` | No duplicated scientific policy; no untested reproduction promises |
| `14_Automation/` | Implementer / all roles | Thin entry-point scripts for registry validation, leakage checks, hash audits, figure rendering, and pipeline dispatch | No hidden model defaults or automated gate sign-offs |
| `15_Templates_Prompts/` | Researchers / all roles | Blank versioned templates `T01–T32`, planning/implementation/review prompt library, version log | Filled instances live in owning domain folders; zero PHI or secrets in prompts |
| `16_Archive/` | Release owner / authorized readers | `archive_manifest.csv`, immutable `ARCH####` metadata snapshots, submission receipts, restoration test proofs, retention policy | Never overwrite released snapshots; never publicly archive restricted clinical data |
| `prototype_ui/` *(optional)* | Prototype owner / defense examiners | Created ONLY if UD22 selects an interactive/hosted defense interface: thin wrapper calling `src/cvd_mm/` frozen inference + SHAP path, parity report, disclaimer | Never reimplements preprocessing/thresholds/calibrators; never stores uploaded patient data without approval; never produces evaluation evidence |

## 2.3 Artifact placement and multimodal data lineage

All reusable scientific code lives in `src/cvd_mm/`. Domain folders store specifications, versioned configs, CSV registries, review records, and safe aggregated summaries. Notebooks, if used for exploration or plotting, are thin callers that never hold the sole copy of scientific logic.

Maintain unbroken, hash-verified lineage from primary hospital collection to Q1 publication:

```text
Hospital/Site (SITE) + IRB/Consent → Raw Cohort (DS) → Endpoint & Schema Adjudication (ADJ)
→ Patient/Site-Level Split (SPLIT) → Training-Only Fitted Preprocessing & Modality Alignment (PP)
→ Prepared Multimodal Release (REL) → Controlled Experiments (EXP / RUN) → Checkpoints & Models (CKPT / MODEL)
→ Frozen Evaluation, Calibration & Stats (EVAL) → Multimodal XAI Faithfulness & Clinical Review (XAI)
→ Publication Figures & Tables (FIG / TAB) → Claim Ledger (CLAIM) → Thesis & Q1 Paper (WR) → Immutable Archive (ARCH)
```

Every pipeline transition consumes explicit parent manifest hashes and emits a child manifest recording parent IDs, SHA-256 digests, patient/encounter counts, variable-schema hash, split hash, and software commit. Downstream consumers must fail loudly on any mismatched variable dictionary, class/outcome map, split hash, or fitted-preprocessor digest.

<a id="os-03"></a>
# 3. Literature and research-question workflow

## 3.1 Zero-seed multi-database search design

**PROPOSAL FACT (`RF06`):** `fydp_title_proposal.pdf` contains no bibliography or references. Consequently, the literature foundation cannot rely on proposal seed citations and must be built transparently from scratch using PRISMA-aligned search governance.

**PLANNING RECOMMENDATION:** Search both biomedical/cardiology and computer-science/engineering databases: **PubMed/MEDLINE**, **IEEE Xplore**, **Scopus**, **Web of Science Core Collection**, **ACM Digital Library**, and supplementary searches via **Google Scholar**, **PhysioNet**, and backward/forward citation snowballing from seminal included studies. Document actual institutional access; record inaccessible databases honestly as search-coverage limitations rather than implying exhaustive coverage.

Seed Boolean queries (adapt syntax per database and log verbatim):

```text
Query A (Multimodal CVD Risk Prediction):
("cardiovascular disease" OR "coronary artery disease" OR "heart disease" OR CVD OR "myocardial infarction" OR "heart failure")
AND ("multimodal" OR "multi-modal" OR "data fusion" OR "cross-modal" OR "feature fusion")
AND (ECG OR electrocardiogram OR electrocardiography)
AND (clinical OR "electronic health record" OR EHR OR laboratory OR biomarker OR lifestyle)
AND ("risk prediction" OR prognosis OR "early detection" OR screening)

Query B (Transformer Multimodal Fusion & Missing Modalities in Healthcare/Cardiology):
(transformer OR "cross-attention" OR "multimodal fusion" OR "attention fusion")
AND (cardiovascular OR cardiology OR ECG OR "tabular")
AND ("missing modality" OR "incomplete modality" OR "heterogeneous" OR "clinical prediction")

Query C (Explainable AI Faithfulness & SHAP in Multimodal CVD Prediction):
(SHAP OR "Shapley" OR LIME OR "explainable AI" OR XAI OR interpretable)
AND (cardiovascular OR ECG OR "multimodal")
AND (faithfulness OR fidelity OR stability OR "clinical plausibility" OR "decision support" OR calibration)
```

Actively search for **contradicting and strong competing studies**—specifically large-scale multimodal CVD studies combining 3+ modalities (e.g., UK Biobank clinical + ECG + blood biomarkers + lifestyle, MIMIC-IV + MIMIC-IV-ECG multimodal transformers, and recent *IEEE JBHI* / *npj Digital Medicine* / *Nature Medicine* / *Information Fusion* papers). Never set an arbitrary paper-count quota or exclude recent studies simply because they challenge the proposal's novelty narrative.

## 3.2 Intake, screening, and structured extraction

1. **Register before reading:** Export raw search results, assign `P####` IDs after deduplicating by DOI, PMID, normalized title, and preprint-to-journal linkage (link preprints to published versions; never count both as independent evidence).
2. **Two-stage screening:** Screen title/abstract, then full text, against prospectively approved eligibility criteria (`STEP-004`). Separate **Direct Multimodal CVD Comparators** (ECG + tabular clinical/lab/lifestyle prediction) from **Contextual Literature** (unimodal ECG deep learning, unimodal tabular CVD risk models, cardiac imaging multimodal fusion, general XAI methodology, and clinical risk calculators like Framingham/SCORE2/WHO South Asia charts). Record one explicit exclusion reason per full-text exclusion in `02_Literature/screening.csv`.
3. **Full-text verification:** Verify bibliographic metadata against publisher records/DOIs. Never rely solely on an abstract or secondary review to report a study's metrics, modality count, or sample size.
4. **Q1 methodological extraction (`T05`):** For every included direct study extract: dataset origin & country/ethnicity; sample size & event count/prevalence; clinical endpoint & time horizon (prospective vs cross-sectional); exact modalities included (clinical, ECG format/leads, lab, lifestyle, imaging); missing-modality strategy; split level (patient vs record, internal vs external/temporal validation); leakage/PROBAST risk-of-bias indicators (e.g., pre-split SMOTE/scaling, unclear index time); model & fusion architecture; baselines compared; reported metrics (Accuracy, P/R/F1, ROC-AUC, PR-AUC, calibration, DCA, statistical tests); XAI technique AND whether faithfulness/stability/clinician review were actually evaluated; code/data availability; author-stated vs reviewer-identified limitations. Write `not reported` when absent—never infer defaults.
5. **Traceable locators:** Attach exact page/table/figure locators to every extracted numerical value. Reconcile extraction disagreements through documented human review.

## 3.3 Research-gap verification (`PG1–PG5`)

Retain the proposal's five gap bullets on p.3 (`RF07`) as source labels `PG1–PG5`; operational gap records use `GAP####` with a `ProposalGap` column.

| Proposal gap | What the systematic review must test | Possible honest Q1 outcome |
|---|---|---|
| PG1: Most studies use only one healthcare data type | Prevalence and quality of unimodal vs multimodal CVD studies in recent Q1 literature | Likely broadly true historically, though multimodal ECG+EHR literature has grown rapidly; quantify rather than overgeneralize |
| PG2: Existing multimodal systems often combine only two data sources | Whether 3- and 4-modality CVD studies already exist (e.g., EHR + ECG + labs + lifestyle in UK Biobank or MIMIC-IV) | If 3–4 modality studies exist, **narrow the gap** honestly (e.g., scarcity of synchronized 4-modality cohorts in South Asian/Bangladeshi populations, lack of missing-modality robust Transformer fusion, or lack of rigorous incremental modality ablations) |
| PG3: Many AI models do not explain their predictions | Whether existing multimodal CVD models already apply SHAP/LIME/attention—and whether they actually evaluate XAI faithfulness, stability, and calibration | Simple SHAP plots are common; the **true Q1 gap** is often the lack of *quantitatively faithful, stable, modality-decomposed XAI paired with calibrated clinical utility and shortcut auditing* |
| PG4: Lifestyle information is often ignored | Which multimodal ECG+clinical studies explicitly model lifestyle factors and test their incremental predictive value over clinical/lab data | Test empirically in RQ2 rather than assuming lifestyle always improves AUC; reporting incremental value (positive or marginal) is Q1-worthy |
| PG5: Few studies build an explainable multimodal framework combining multiple sources | Direct prior explainable 4-modality Transformer CVD frameworks, their leakage controls, external validity, and reproducibility | Position contribution accurately against verified SOTA without claiming "first ever" unless exhaustively defensible |

Classify each `GAP####` as `proposed`, `supported-within-search`, `narrowed`, `refuted`, or `unresolved` with explicit `SupportingPapers` and `ContradictingPapers`. **Critical Q1 rule:** Narrowing or refining an overly broad FYDP gap claim into a sharp, defensible Q1 research gap (e.g., South Asian primary 4-modality cohort + leakage-free missing-modality Transformer fusion + calibration/DCA + quantitative multimodal SHAP faithfulness) **strengthens** publication chances; defending a refuted novelty claim guarantees peer-review rejection.

## 3.4 Question approval and living review

At `STEP-009` (`G03`), approve the final RQ-to-objective-to-experiment-to-metric map linking `O1–O4`, `GAP####`, dataset/schema requirements, baseline/ablation matrix, evaluation/XAI metrics, and claim boundaries. Re-run targeted update searches prior to final modeling (`STEP-023`) and prior to Q1 manuscript submission (`STEP-048`), recording exact search cutoff dates in both thesis and manuscript.

<a id="os-04"></a>
# 4. Cohort collection, multimodal preprocessing, and leakage-safe splitting

## 4.1 Lifecycle, ethics/IRB, and cohort discovery

```text
Feasibility & EPV Power Analysis → Site / External Cohort Selection → IRB, Hospital Permission & Consent/Waiver
→ Controlled PHI-De-Identified Intake → Raw Immutable Lock → Four-Modality Quality & Alignment Audit (G04)
→ Endpoint & Variable Schema Freeze (G05) → Pilot & Production Adjudication QA (G06)
→ Patient/Site-Level Leakage-Safe Split (G07) → Training-Only Fitted Preprocessing & Alignment (G08) → Prepared Release (REL)
```

**Primary cohort governance (Bangladesh hospitals/diagnostic centers, `RF09`):**
- **Hard prerequisite:** Zero patient data collection, chart abstraction, or ECG export may occur until written IRB/ethics committee approval, hospital administrative authorization, and approved informed consent (or IRB-documented retrospective waiver) are logged under `UD05`.
- **Spectrum-bias & recruitment control:** Record exact hospital/diagnostic-center department(s), enrollment period, inclusion/exclusion criteria, and sampling mechanism (consecutive clinical cohort preferred over extreme case-control recruitment). If CVD cases come from a cardiology inpatient unit while controls come from an outpatient wellness clinic, document the resulting spectrum/site bias and mitigate via site-matched recruitment or sensitivity analyses.
- **Prospective sample-size and EPV feasibility (`UD04`, `UD26`):** Before finalizing deep Transformer capacity, compute expected total sample size $N$, CVD event count $E$, event prevalence, and effective Events-Per-Variable (EPV) using established clinical prediction sample-size principles (e.g., Riley et al. criteria for binary prediction models). If primary $N$ is modest (e.g., a few hundred to low-thousand patients), invoke `UD26` prospectively (e.g., compact/regularized modality encoders, pretrained ECG representations, nested cross-validation, and/or external public cohort validation) rather than overfitting a massive Transformer from scratch.
- **Optional external/secondary public cohort (`UD06`, PLANNING RECOMMENDATION for Q1):** To maximize Q1 acceptance, assess whether a lawful, compatible public benchmark (such as MIMIC-IV + MIMIC-IV-ECG, PTB-XL, Framingham, or NHANES, subject to credentialed access and modality overlap) can serve for (a) external validation of overlapping modalities, (b) ECG encoder pretraining, or (c) multi-cohort generalization demonstration. Never assume access or merge incompatible populations silently.

## 4.2 Controlled intake, PHI de-identification, and four-modality linkage

1. **Pseudonymous hierarchy:** Assign `SITE####` (hospital/center), `PAT########` (unique individual patient), and `ENC########` (index clinical encounter/visit). Store the PHI-to-`PAT########` linkage key **exclusively** in an encrypted, access-restricted offline/institutional linkage vault outside the Git repository and analytical directories.
2. **PHI scrubbing across ALL modalities:** Remove names, national IDs, phone numbers, addresses, hospital MRNs, exact dates of birth (retain age in years or approved age bands), free-text clinician notes containing identifiers, and **ECG file headers/DICOM tags/burned-in PDF banners** containing patient names, IDs, or exact timestamps that enable re-identification. Replace calendar dates with relative day offsets from `IndexDate` ($t_0$) where longitudinal timing is needed.
3. **Strict index-time ($t_0$) and alignment window ($\Delta t$, `UD03`):** Define the exact index encounter $t_0$ at which CVD risk prediction is intended to operate. Enforce a prospectively approved alignment window (e.g., Clinical, ECG, Laboratory, and Lifestyle data collected within $\pm \Delta t$ around $t_0$, and **strictly prior to** post-diagnosis therapeutic interventions or acute-event confirmatory markers that leak the label!). Flag and quarantine any modality record collected outside $\Delta t$ or after outcome ascertainment.
4. **Immutable raw lock:** Compute SHA-256 hashes of every raw tabular export and raw ECG waveform/file on intake into restricted `03_Datasets_Cohort/raw/DS####/`. Raw files are read-only forever; every cleaning or unit-harmonization step produces a versioned derived artifact.

## 4.3 Four-modality quality and missingness inspection

Before schema freezing and splitting (`STEP-013`, `G04`), audit each modality systematically using automated read-only checks plus qualified clinical spot-review:

| Modality | Mandatory quality & integrity checks | Critical Q1 failure modes to catch |
|---|---|---|
| **Clinical Data** (`RF10`: Age, Gender, BMI, BP, Medical History, etc.) | Physiologic plausibility bounds (e.g., SBP > DBP, realistic BMI/age ranges), categorical consistency, exact unit checks (cm/m, kg/lb, mmHg), duplicate encounters, medical-history coding separating pre-existing baseline history from target CVD outcome | Including prior/current CVD diagnosis or cardiac-specific post-diagnosis medications inside "Medical History" causes direct **target leakage**! |
| **ECG Signals** (`RF10`, `UD07`) | Format verification (waveform vs extracted features vs scanned strips), sampling rate consistency, lead count/names (e.g., standard 12-lead), duration, missing/flatline leads, saturation/clipping, baseline wander, **50 Hz Bangladesh powerline noise** (or 60 Hz in external cohorts), electrode/motion artifacts, signal-to-noise ratio (SNR), and cardiologist visual sample review | Feeding raw scanned ECG images without digitization validation, mixing 250 Hz and 500 Hz without resampling, or leaving patient names burned into ECG headers |
| **Laboratory Results** (`RF10`: Blood Glucose, Cholesterol, Creatinine, etc.) | Explicit unit harmonization (mg/dL vs mmol/L for glucose/lipids; mg/dL vs $\mu$mol/L for creatinine), fasting vs random glucose distinction, assay/reference-range differences across diagnostic centers, censored values (`<0.01`, `>500`), extreme analytical outliers, and **Missing Not At Random (MNAR)** ordering patterns | Mixing mg/dL and mmol/L across two diagnostic centers; ignoring that missing troponin/HbA1c/lipid tests reflect clinical suspicion (MNAR) |
| **Lifestyle Information** (`RF10`: Smoking, Diet, Physical Activity, Sleep, Family History) | Questionnaire instrument consistency, missing/refused response codes separated from `0`, smoking pack-year/status consistency, sleep-hour plausibility, structured diet/activity scales, and explicit schema mapping of Family History | Treating "not asked / missing" as "non-smoker = 0"; recall bias and unstandardized free-text diet entries |

**Count reconciliation:** `Screened patients = Enrolled/Extracted + Ineligible + Declined/Excluded + Quarantined`, with exact per-modality availability counts (`Clinical`, `ECG`, `Lab`, `Lifestyle`, all-4-complete, 3-of-4, etc.) reported transparently for the future CONSORT/STARD-style cohort flow diagram.

## 4.4 Leakage-safe splitting and reconciliation of Proposal Workflow Diagram

**CRITICAL RECONCILIATION OF PROPOSAL DIAGRAM (`RF13`):** Page 5 of `fydp_title_proposal.pdf` depicts `2. Data Preprocessing` and `3. Feature Extraction` before `4. Train / Validation / Test Split`. Executing dataset-wide normalization, imputation, or learned feature extraction before splitting introduces **severe data leakage** and invalidates Q1 peer review. Therefore, this operating system preserves all nine conceptual stages while enforcing the following strict operational separation:

- **Allowed BEFORE split (`STEP-019` pre-split stage, strictly record-local & deterministic):** Schema validation, unit harmonization (`mg/dL ↔ mmol/L`), physiological range flagging, deterministic patient/encounter linkage, and fixed-parameter record-local ECG signal standardization (e.g., deterministic resampling to uniform target Hz and fixed-coefficient filtering verified not to distort clinical ECG morphology—zero parameters learned from any cohort distribution!).
- **Locked Split (`STEP-020`, `G07`):**
  - **Connected patient-level grouping:** Every encounter, repeated ECG, and derived record belonging to the same `PAT########` (or identified near-duplicate pair) MUST reside in exactly one partition. Zero patient overlap across Train, Validation, and Test is an absolute requirement.
  - **Stratification:** Stratify by the primary CVD outcome (and, where sample size permits, recruitment site and sex/age stratum) while strictly preserving patient groups.
  - **Small-$N$ vs Large-$N$ strategy (`UD11`):** Because the proposal leaves split ratios unspecified (`RF14`), resolve `UD11` based on measured cohort size $N$ and event count $E$:
    - *Option A (Sufficient $N$/$E$):* Stratified patient-grouped Train / Validation / Test split (e.g., 70/15/15 or 60/20/20) PLUS optional temporal or leave-one-site-out external holdout.
    - *Option B (Modest $N$/$E$ — strongly recommended for Q1 if hospital $N < 1{,}500$):* Stratified patient-grouped **held-out final test set** (or **repeated nested $K$-fold cross-validation**, e.g., 5-fold outer × 5-fold inner) so that tuning, calibration, and threshold selection stay strictly inside inner folds while outer folds provide low-variance, leakage-free performance estimates.
  - **Test-set seal:** Once `G07` passes, the final test partition is sealed against all model training, hyperparameter tuning, feature selection, imputation fitting, threshold picking, calibrator fitting, and error-driven architecture edits until `G11` PASS.

## 4.5 Leakage-free preprocessing, imputation, and ECG signal contracts

All dataset-dependent operations execute **strictly AFTER split locking** (and inside each CV training fold if nested CV is used):

1. **Missing data & missing-modality handling (`UD10`, `UD12`):**
   - Fit numerical/categorical imputers (e.g., median/mode, Iterative/MICE, KNN) **exclusively on the training partition**, serialize the fitted state (`FitStateHash`), and apply unchanged to validation and test.
   - **Mandatory Q1 safeguard for MNAR clinical data:** Retain explicit binary **feature-level and modality-level missingness indicator masks** where missingness is non-trivial, AND audit during XAI (`STEP-040`) whether the model is exploiting missingness artifacts as spurious shortcuts!
   - For missing entire modalities (if partial-modality patients are retained under `UD10`), provide clean **modality presence masks** for the Transformer fusion network (e.g., learnable `[MISSING_MODALITY]` tokens / masked cross-attention) rather than imputing fake raw ECG waveforms!
2. **Scaling & encoding:** Fit scalers (StandardScaler, RobustScaler, QuantileTransformer) and categorical encoders (one-hot/ordinal/target-free encoding) strictly on training data. Verify zero `NaN`/`Inf` outputs.
3. **ECG signal preprocessing & morphology verification (`UD07`, `UD12`):**
   - Document exact resampling rate, lead ordering, amplitude unit (mV), window/beat segmentation, baseline-wander removal (e.g., high-pass $\le 0.5\text{ Hz}$ or wavelet/median filter), powerline notch filter (50 Hz for Bangladesh clinical recordings; 60 Hz for US external datasets), and per-lead/per-record vs training-fitted amplitude normalization.
   - **Morphology fidelity audit (Mandatory for G08):** A qualified clinician/ECG reviewer must visually inspect paired raw-vs-processed ECG waveforms across normal and abnormal recordings to verify that filtering does **not** attenuate or distort clinically diagnostic **ST-segment elevation/depression, T-wave inversions, Q-waves, or P-wave morphology**!
4. **Class-imbalance caution (`UD15`):** Never apply SMOTE or oversampling prior to splitting! Even inside training folds, prefer **class-weighted losses, focal loss, or threshold optimization on calibrated probabilities** over naive synthetic oversampling of multimodal clinical/ECG vectors (which distorts true risk probabilities and ruins calibration!). If oversampling is tested as an ablation, keep it strictly inside training folds and re-calibrate probabilities on unresampled validation data.

## 4.6 Versioned prepared releases (`REL####`) and change control

An immutable `REL####` manifest binds `DS####`, `ADJ####`, `variables.csv` hash, `SPLIT####`, `PP####` config + `FitStateHash`, code commit, exact patient/encounter/modality counts, and restricted storage paths. Never overwrite an existing `REL####`.

| Change type | Required governance action |
|---|---|
| Outcome label or clinical adjudication correction | New `ADJ####` version with affected `ENC` IDs and clinician rationale → new `REL####` → invalidate dependent comparisons; if post-test, disclose and evaluate frozen model under new `EVAL` without hidden retraining |
| Variable schema or unit-mapping change | New `variables.csv` version → reassess `G05–G08` and invalidate affected `REL`/`EXP` |
| Patient grouping or split modification | New `SPLIT####` and `REL####` → reassess `G07` onward; disclose any prior test exposure |
| ECG filter, imputation, or scaling change | New `PP####` and `REL####` → rerun ECG morphology & leakage tests (`G08`) → new `EXP####` for fair comparison |
| Discovery of unconsented or PHI-leaking record | Halt immediately, isolate/remediate under institutional IRB/custodian protocol, reissue clean `DS`/`REL`, invalidate affected claims |

<a id="os-05"></a>
# 5. Clinical endpoint, four-modality schema, and ground-truth QA

*(Clinical endpoint adjudication, index-time alignment, and four-modality variable standardization form the ground-truth validity foundation of multimodal CVD risk prediction.)*

## 5.1 Clinical endpoint ontology and adjudication charter

The proposal targets "early cardiovascular disease risk prediction" (`RF01`, `RF03`) without specifying clinical criteria (`RF14`). `UD02` must resolve and freeze the following in `04_Outcome_Schema_QA/endpoint_charter.md` before `G05`:

1. **Exact CVD target definition:** Enumerate qualifying conditions with standard clinical codes (e.g., ICD-10-CM/WHO codes for coronary artery disease/ischemic heart disease, acute coronary syndrome/MI, heart failure, cerebrovascular disease/stroke, peripheral arterial disease, or clinically defined early-stage CVD). Define non-CVD / control eligibility explicitly (e.g., confirmed absence of CVD under documented clinical workup, NOT merely "absence of a billing code").
2. **Prediction horizon & study design honesty:** Explicitly classify the study as one of:
   - *Longitudinal / Prospective risk prediction:* baseline CVD-free patients at $t_0$ followed for $T$ months/years for incident CVD (requires documented follow-up duration, loss-to-follow-up/right-censoring rules, and time-dependent metrics if censoring is substantial); OR
   - *Cross-sectional early-stage / diagnostic risk stratification:* baseline clinical/ECG/lab/lifestyle profiles evaluated against concurrently adjudicated early/established CVD status (e.g., cardiologist diagnosis, angiography, echocardiography, or stress-test reference standard). In this case, thesis and Q1 manuscript wording **must transparently state** cross-sectional diagnostic/risk-stratification design and frame longitudinal prognostic validation as future work!
3. **Reference-standard independence (avoiding incorporation bias):** Document what evidence the adjudicator uses to assign the CVD label. Critically evaluate **incorporation bias** (PROBAST domain 3): if the ECG or a specific lab test (e.g., high-sensitivity troponin) was itself the primary diagnostic criterion used to assign the label, disclose this explicitly and run a **sensitivity analysis** excluding incorporation-biased predictors where appropriate!
4. **Ambiguous/borderline cases:** Record `uncertain / needs_adjudication` as an explicit review state, never silently coercing borderline patients into `0` or `1`.

## 5.2 Four-modality variable dictionary, CRF, and ECG contract

Freeze `04_Outcome_Schema_QA/variables.csv` (`G05`) containing every candidate predictor across all four modalities with: `VarID`, `Modality` (`Clinical`, `ECG`, `Laboratory`, `Lifestyle`), `VariableName`, `DataType`, `Unit`, `ValidRange`, `CodingMap`, `CollectionInstrument`, `TimingRelativeToIndex`, `IncorporationBiasRisk`, `MissingPolicy`, `PROBASTNotes`, and `Approver`.

- **Family History mapping (`RF10`):** The proposal lists `Family History` under Lifestyle Information (p.4). Retain transparent traceability to the proposal while documenting clearly in `variables.csv` and the manuscript whether it is kept in the Lifestyle/Personal-History block (matching proposal) or analyzed in sensitivity groupings alongside Clinical History.
- **Standardized Case Report Form (CRF) for primary collection:** For prospective hospital/diagnostic-center collection, version a structured CRF (with standardized validated items where feasible—e.g., standardized smoking status/pack-years, physical activity intensity/duration, dietary pattern items, sleep duration/quality) so enumerators collect uniform, reproducible variables rather than unstructured free text.
- **ECG Contract (`04_Outcome_Schema_QA/ecg_contract.md`):** Pin exact acquisition device/export types, lead set, sampling rate, recording length, digital file schema, and whether raw waveforms, clinically extracted intervals (HR, PR, QRS, QT/QTc, axes), or both are stored. If both raw ECG waveforms and tabular ECG measurements exist, document how they are prevented from duplicating information inconsistently across ablations.

## 5.3 Pilot abstraction, inter-rater agreement, and production QA

1. **Pilot QA (`STEP-016`):** Before full-scale primary collection or chart abstraction, run a prospectively defined pilot (`UD09`) with independent dual abstraction/entry on a stratified sample covering CVD-positive, CVD-negative, multi-comorbidity, and noisy-ECG cases. Compute inter-abstractor agreement (Cohen's $\kappa$ for categorical variables and outcome flags; Intraclass Correlation Coefficient [ICC] and exact mismatch rates for continuous clinical/lab values; ECG quality-grading agreement).
2. **Adjudication & threshold enforcement:** The qualified cardiologist/clinical adjudicator resolves pilot disagreements, refines ambiguous CRF/coding rules, and signs off against prospectively set QA thresholds. Never lower QA thresholds post hoc after observing noisy abstraction.
3. **Tracked production batches (`STEP-017`):** Organize primary collection/curation into numbered batches (`CRFB####` / `ADJB####`) tracking collector/abstractor, hospital site, protocol version, dual-verification sample membership, adjudication counts, and unresolved queries.
4. **Release freeze (`STEP-018`, `G06`):** Run automated schema/range/unit/linkage/ECG-readability audits plus stratified clinical spot-review; freeze immutable `ADJ####` hashes. If qualified clinical adjudication is unavailable for a proposed target or hospital subset, mark `Unresolved / Human Decision Required` and halt labeling of that subset rather than substituting unverified guesses.

<a id="os-06"></a>
# 6. Multimodal modeling, Transformer fusion, and experiment operating system

## 6.1 Implementation discovery and Q1 baseline hierarchy

The proposal specifies Python, TensorFlow/PyTorch, Scikit-learn, Pandas, NumPy, Matplotlib, SHAP, and a **Transformer-based Multimodal Fusion Network** (`RF08`), while referencing Logistic Regression, Random Forest, SVM, XGBoost, CNNs, LSTMs, and Transformers in background context (`RF05`). Resolve framework selection (`PyTorch` vs `TensorFlow`, `UD13`) based on ECG-Transformer ecosystem maturity, reproducible determinism support, SHAP integration, and available hardware—recording exact package versions, commits, and licenses.

**Q1 Mandatory Four-Tier Comparator Hierarchy (PLANNING RECOMMENDATION, finalized under `UD14`):**

| Tier | Comparator family | Scientific role in a Q1 paper |
|---|---|---|
| **Tier 1: Unimodal Baselines** | **Clinical-only**, **Laboratory-only**, **Lifestyle-only** (LR, RF, SVM, XGBoost/LightGBM/CatBoost, MLP/FT-Transformer); **ECG-only** (1D-CNN/ResNet-1D, BiLSTM/CNN-LSTM, ECG Transformer) | Directly tests whether multimodal integration actually beats strong, properly tuned single-modality models (`RF15`, `PG1`) |
| **Tier 2: Clinical Risk Score Benchmark** *(optional UD14)* | Established clinical score (e.g., Framingham, WHO South Asia CVD chart, ASCVD PCE, SCORE2 — only if endpoint & predictors are clinically compatible!) | Anchors AI performance against current real-world cardiology practice—highly valued by Q1 clinical reviewers |
| **Tier 3: Simple Multimodal Fusion Baselines** | **Early fusion** (concatenated tabular + ECG features/embeddings → XGBoost & MLP); **Late fusion** (weighted/stacked ensemble of unimodal calibrated probabilities); **Gated/Bilinear fusion** | Prevents the classic Q1 criticism that a complex Transformer is unnecessary when simple concatenation + XGBoost or late ensembling achieves equal or better performance |
| **Tier 4: Proposed Transformer-based Multimodal Fusion Network** | Modality-specific encoders (e.g., tabular tokenizer/MLP/FT-Transformer embeddings for Clinical, Lab, Lifestyle + 1D-CNN/ResNet/Patch-Transformer encoder for ECG) → projection to common dimension $d$ → **cross-modal Transformer fusion** (self/cross-attention with modality-type embeddings + learnable missing-modality masks/tokens) → risk prediction head | Core proposed method (`RF08`); evaluated honestly on accuracy, calibration, missing-modality robustness, and interpretability |

**Fair comparison invariants:** Every model across Tiers 1–4 MUST share identical `REL####` patient splits, identical outcome labels, identical validation-only tuning rules, identical matched hyperparameter search budgets (documented per model family), identical multi-seed policy, and identical evaluation/calibration protocol. Never tune the proposed Transformer extensively while leaving XGBoost or unimodal baselines at untuned defaults!

## 6.2 Configuration contract

Every executable experiment (`EXP####`) has an immutable `config.yaml` with **zero unresolved `null` fields** for executable settings, capturing both requested and effective library defaults:

- **Identity:** `EXP####`, RQ link, comparison tier/role, parent baseline `EXP`, code commit, timestamp, plan approval record.
- **Data:** `REL####`, `DS####`, `ADJ####`, `SPLIT####`, `PP####` + `FitStateHash`, `variables.csv` hash, active modality mask (`Clinical`, `ECG`, `Lab`, `Lifestyle`), partition paths.
- **Model:** Framework & exact version, architecture/hyperparameters for every modality encoder and fusion block, parameter count, pretrained encoder provenance/hash/license (if used), missing-modality masking rule.
- **Training:** Fixed seed(s), determinism flags, optimizer, learning-rate schedule, batch size, epochs/max budget, dropout/weight decay, class-imbalance loss settings, gradient clipping, early-stopping monitor (validation metric + patience), mixed precision settings.
- **Calibration & Evaluation:** Validation protocol hash, calibration candidate rule, metric suite.
- **Runtime & Storage:** OS, Python, framework, CUDA/cuDNN/CPU hardware record, dependency lock hash, checkpoint retention, artifact destination.

An automated config validator (`src/cvd_mm/`) rejects missing fields, unresolved placeholders, mismatched parent hashes, or any accidental test-partition reference before launch. Modifying any scientific parameter creates a **new `EXP####`**.

## 6.3 Training lifecycle, multi-seed policy, and tuning isolation

`Register EXP → Verify gates (G08–G09) & input hashes → Validate effective config → Train on Train fold/partition only → Monitor Validation only → Save checkpoints/logs → Audit completion (G10) → Register eligible MODEL`

- **Smoke test (`STEP-027`):** Run a prospectively labeled diagnostic smoke test on a tiny training/validation slice confirming 4-modality batch alignment, finite losses/gradients, missing-modality mask behavior, checkpoint save/reload, and metric output—with zero final-test access.
- **Multi-seed discipline (Q1 requirement):** Report mean ± SD (and min/max) across all planned seeds (recommended $S \ge 3$–$5$, `UD15`) for neural/stochastic models. Never report only the best seed or drop poorly converged seeds. Prefer separate `EXP####` IDs (or explicitly linked child `RUN####` records under a preapproved multi-seed design) for complete auditability.
- **Hyperparameter tuning isolation:** All architectural and hyperparameter search uses validation (or inner CV folds) strictly. Record total tuning trials and search space to satisfy TRIPOD+AI transparency and guard against subtle validation overfitting.
- **Failure preservation:** Log and preserve OOM errors, NaN divergence, mode collapse, and underperforming runs permanently with `T15` failure reports.

## 6.4 Checkpoint and exact-resume management

Assign immutable `CKPT####` IDs embedding `EXP`, `RUN`, epoch/step, and role (`best_val`, `last`, `periodic`). Store SHA-256 digests, byte size, model weights, optimizer state, scheduler state, AMP scaler (if used), epoch/step, RNG states (Python, NumPy, framework CPU/GPU), and validation monitor score.

Verify interruption recovery before long runs (`STEP-027`): interrupt a short diagnostic run, restore from backup in the exact environment, verify state continuity and hash integrity, and document any exact-resume limitations (e.g., GPU nondeterminism). Never reconstruct missing loss curves or fabricate completed epochs.

## 6.5 Controlled Q1 experiment and ablation matrix

Plan the complete controlled comparison matrix prospectively in `07_Experiments/experiment_plan.md` (`STEP-025`) before launching full runs:

1. **Block A — Unimodal Benchmarks:** Clinical-only, ECG-only, Laboratory-only, Lifestyle-only (best classical ML + deep architectures per modality).
2. **Block B — Clinical Risk Score Comparator** *(if adopted under UD14)*.
3. **Block C — Multimodal Fusion Benchmarks:** Early fusion (GBDT + MLP), Late fusion ensemble, Gated fusion, and Proposed Transformer-based Multimodal Fusion Network.
4. **Block D — Modality Ablations (Testing `PG1`, `PG2`, `PG4`):**
   - *Progressive Modality Addition:* Clinical → Clinical+Lab → Clinical+Lab+Lifestyle → Clinical+Lab+Lifestyle+ECG (and Clinical+ECG → +Lab → +Lifestyle).
   - *Leave-One-Modality-Out (LOMO):* Full 4-modality minus Clinical; minus ECG; minus Lab; minus Lifestyle.
5. **Block E — Architectural & Design Ablations:** Cross-modal Transformer attention vs simple concatenation; with vs without missing-modality masking; ECG raw-waveform encoder vs extracted tabular ECG features (if both exist); regularization/pretraining ablation.
6. **Block F — Sensitivity & Robustness Runs:** Multi-seed variance repeats; incorporation-bias exclusion sensitivity (if applicable); missing-modality dropout stress tests at inference time (simulating 10%–50% or complete single-modality unavailability at test time without retraining, evaluated on validation first and finalized after freeze).

Every qualifying experiment requires a `G10` PASS and a registered `MODEL####` card (`T17`) linking exact `EXP`/`RUN`/`CKPT`/`REL`, parameter count, training cost, and intended research use.

<a id="os-07"></a>
# 7. Evaluation, calibration, statistical inference, and clinical utility protocol

## 7.1 Protocol before training; freeze before final testing

Draft `09_Evaluation_Stats/protocol.md` at `STEP-025` (`G09`) and **freeze** every element at `STEP-032` (`G11`) prior to generating any final-test predictions:

- Frozen champion `MODEL####` (and pre-selected comparator models for final test comparison, all chosen **strictly on validation / inner CV**);
- Frozen `PP####` + `FitStateHash` + `REL####` + `variables.csv` hash;
- Frozen **post-hoc probability calibrator** (e.g., temperature scaling, Platt scaling, or isotonic regression fitted strictly on validation / OOF predictions under `UD16`);
- Frozen **binary/multi-class operating threshold(s)** chosen strictly on validation (`UD16`, e.g., Youden's $J$, F1-maximizing, or clinically motivated target sensitivity);
- Frozen statistical tests, bootstrap seed, subgroup definitions, and DCA threshold grid.

Audit the test-set access log at `G11`. Any prior test-set leakage invalidates clean held-out claims and triggers disclosure and redesign.

## 7.2 Mandatory proposal metrics and mathematical contracts

All six proposal metrics (`RF12`, `RF13`) MUST be reported for the frozen champion and key comparators on the sealed test partition (and external cohort if adopted), accompanied by exact confusion counts and operating thresholds:

| Mandatory metric | Exact definition & reporting requirement | Accompanying metadata required |
|---|---|---|
| **Accuracy** | $(\text{TP} + \text{TN}) / (\text{TP} + \text{TN} + \text{FP} + \text{FN})$ | Event prevalence, majority-class baseline accuracy, frozen operating threshold $\tau$ |
| **Precision (PPV)** | $\text{TP} / (\text{TP} + \text{FP})$ | Denominator $(\text{TP}+\text{FP})$, `N/A` if denominator is 0; macro/weighted/binary averaging if multi-class |
| **Recall (Sensitivity)** | $\text{TP} / (\text{TP} + \text{FN})$ | Denominator $(\text{TP}+\text{FN})$, `N/A` if denominator is 0; clinical false-negative context |
| **F1-Score** | $2 \cdot \text{Precision} \cdot \text{Recall} / (\text{Precision} + \text{Recall})$ | Threshold $\tau$, averaging convention if multi-class |
| **ROC-AUC (AUROC)** | Area under Receiver Operating Characteristic curve across all continuous predicted risk scores | Exact trapezoidal/Mann-Whitney implementation, 95% CI, raw vs calibrated invariance note |
| **Confusion Matrix** | Exact raw integer counts `[TN, FP; FN, TP]` (or full $K \times K$ matrix) | Total evaluated patients $N_{\text{test}}$, failed/excluded prediction count (must be 0 or explicitly reported), threshold $\tau$ |

Never tune the operating threshold $\tau$ on final test predictions to inflate F1 or Accuracy! Store per-patient coverage separately so every scheduled test patient is accounted for.

## 7.3 Q1 clinical prediction extensions (Calibration, PR-AUC, Clinical Utility)

**PLANNING RECOMMENDATION (adopt formally under `UD16–UD17` — essential for Q1 medical AI acceptance and TRIPOD+AI compliance):**

1. **Imbalance-sensitive discrimination:** Report **PR-AUC (AUPRC)** alongside the cohort's positive-class prevalence (the no-skill PR baseline), plus **Specificity**, **Negative Predictive Value (NPV)**, and **Balanced Accuracy** / **Matthews Correlation Coefficient (MCC)**.
2. **Probability calibration (critical for "Risk Prediction"):**
   - **Brier Score** (and Brier Skill Score relative to prevalence baseline);
   - **Expected Calibration Error (ECE)** with explicitly documented bin count and binning scheme (equal-width vs quantile);
   - **Calibration Slope** (ideal = 1.0) and **Calibration-in-the-Large / Intercept** (ideal = 0.0) via logistic recalibration model, accompanied by **reliability diagrams** with confidence bands (reported both pre- and post-validation-fitted calibration!).
3. **Clinical Utility — Decision Curve Analysis (DCA):** Plot **Net Benefit** across a clinically justified range of risk threshold probabilities $p_t$ (chosen with the cardiologist under `UD17`), comparing the proposed multimodal Transformer against **"Treat/Screen All"**, **"Treat/Screen None"**, and the best unimodal baseline. DCA demonstrates whether improved AUC/calibration translates into superior clinical decision utility without falsely claiming a prospective hospital trial!

## 7.4 Statistical uncertainty and comparative inference

**PLANNING RECOMMENDATION (adopt under `UD18`):**

1. **Confidence intervals:** Compute **patient-level stratified bootstrap 95% CIs** ($B \ge 1{,}000$–$2{,}000$ resamples, fixed seed, resampling patients with replacement) for ROC-AUC, PR-AUC, Accuracy, Precision, Recall, F1, Specificity, Brier, and ECE. Clearly separate **finite-sample test uncertainty** (bootstrap 95% CIs) from **training stochasticity** (multi-seed mean ± SD).
2. **Paired statistical hypothesis tests:**
   - **DeLong's test** (two-sided, paired) for comparing correlated ROC-AUCs between the proposed multimodal Transformer and each prespecified baseline on the exact same test patients.
   - **Paired patient-level bootstrap difference test** for PR-AUC, F1, Brier score, and DCA Net Benefit differences (reporting $\Delta$, 95% CI of $\Delta$, and two-sided $p$-value).
   - **McNemar's exact test** for paired binary classification discordance at the frozen operating threshold.
3. **Multiple-comparison control:** When comparing against multiple unimodal and fusion baselines simultaneously, apply **Holm-Bonferroni** or **Benjamini-Hochberg FDR** adjustment across prespecified primary comparisons and report both raw and adjusted $p$-values plus effect sizes. Never claim "statistically significant superiority" from overlapping point estimates alone!

## 7.5 Subgroup fairness, missing-modality robustness, error analysis, and PROBAST-AI

At `STEP-037` (`G13`):

1. **Subgroup fairness audit:** Report discrimination and calibration stratified by **Sex/Gender**, **Age groups**, **Hospital/Diagnostic site** (if multi-site), and **Modality-completeness tier**, disclosing subgroup sample sizes and small-$N$ uncertainty. Flag any clinically meaningful performance disparity.
2. **Missing-modality stress test:** Evaluate the frozen Transformer fusion model when 1 or more non-clinical modalities (e.g., ECG unavailable, Lab unavailable, Lifestyle unavailable) are systematically masked at test time, comparing graceful degradation against unimodal fallbacks.
3. **Systematic qualitative error analysis (`T19`):** Using a prospectively defined sampling rule, inspect **True Positives, False Positives, True Negatives, and False Negatives** with qualified clinical input. Categorize observable error drivers (e.g., atypical ECG presentation, borderline laboratory values, missing modality, high-noise ECG, comorbidity confounding, or uncertain reference label) without inventing unsupported causal claims.
4. **PROBAST-AI Risk-of-Bias Self-Audit:** Critically evaluate all four PROBAST domains (**Participants**, **Predictors**, **Outcome**, **Analysis**) to surface residual biases honestly in the manuscript's Limitations section before Q1 peer reviewers find them.

<a id="os-08"></a>
# 8. Explainable AI (XAI) governance, faithfulness, and clinical plausibility

*(Because "Explainable" is a pillar of the approved title [`RF01`, `RF03`, `RF08`, `RF11`], Q1 publication demands rigorous engineering and objective verification of explanations—never decorative post-hoc plots.)*

## 8.1 Multimodal SHAP and attribution engineering (`UD19`)

1. **Explainer-to-architecture contract:** Specify the exact SHAP estimator per model family:
   - For tree baselines (XGBoost/RF): exact `TreeSHAP` (interventional or path-dependent, explicitly documented).
   - For the **Transformer-based Multimodal Fusion Network**: mathematically compatible neural Shapley approximation (e.g., `GradientSHAP`, `DeepSHAP`, `KernelSHAP`/`PartitionSHAP` over semantic feature/ECG-patch coalitions, or Integrated Gradients with verified completeness), explicitly checking **local additivity / efficiency error** ($\sum_i \phi_i + \phi_0 \approx f(x)$ within predeclared tolerance!).
   - **Explicit warning:** Raw Transformer self/cross-attention weights may be inspected for architectural diagnostics, but **attention weights must NEVER be presented as faithful feature attributions** without independent verification.
2. **Leakage-free background reference set:** Construct the SHAP background distribution **exclusively from the training partition** (stratified representative sample with fixed seed and recorded hash). Never build background baselines from test data.
3. **Three levels of multimodal explanation:**
   - **Modality-level attribution:** Aggregate Shapley contributions across the four modality blocks (`Clinical %`, `ECG %`, `Laboratory %`, `Lifestyle %`) both globally across the test cohort and locally for individual patients, showing *which data sources drove a specific patient's risk score*.
   - **Tabular feature-level attribution:** Global beeswarm/bar importance and dependence plots (capturing non-linear risk curves and feature interactions—e.g., Age × BP, Glucose × BMI, Smoking × Cholesterol) plus patient-level waterfall/force plots.
   - **ECG-level attribution:** Depending on `UD07`, map ECG attributions onto meaningful clinical structures (either waveform time-segments/P-QRS-ST-T complexes and specific leads for raw ECG encoders, or interpretable ECG intervals/features), visually overlaying attribution intensity onto de-identified ECG waveforms.
4. **Cross-method sanity check (optional `UD19`):** Compare SHAP against LIME (mentioned in Background Study, p.3) or Integrated Gradients on a sample of test cases to document inter-explainer agreement and divergence honestly.

## 8.2 Quantitative XAI faithfulness and stability protocol (`UD20`)

Before making any interpretability claim in the thesis or Q1 paper, run objective mathematical benchmarks on the frozen test set (`STEP-039`):

1. **Perturbation Faithfulness (Deletion & Insertion Curves / AOPC):**
   - **Deletion (Comprehensiveness):** Progressively mask/replace top-$k$ positively attributed tabular features and ECG segments with training-distribution baseline/conditional values and measure predicted risk drop (Area Over the Perturbation Curve [AOPC] / Area Under Deletion Curve). Compare against **random feature masking** and **reverse-importance masking** as negative controls!
   - **Insertion (Sufficiency):** Start from baseline and progressively insert top-$k$ attributed features/ECG segments, measuring how rapidly the model recovers its full prediction.
2. **Modality-Attribution vs Empirical-Ablation Concordance:** Compare the mean absolute **modality-level SHAP shares** (`Clinical`, `ECG`, `Lab`, `Lifestyle`) against the empirical **Leave-One-Modality-Out (LOMO) performance drops** ($\Delta\text{ROC-AUC}$ / $\Delta\text{Brier}$). Document concordance or discrepancy (e.g., correlated redundancy between Clinical BP and Lab/ECG features) honestly!
3. **Attribution Stability & Robustness:**
   - **Multi-seed stability:** Compute Spearman rank correlation ($\rho$), Kendall's $\tau$, and Top-$k$ Jaccard overlap of global and local feature rankings across independently trained random seeds.
   - **Input-perturbation (local Lipschitz) stability:** Verify that clinically negligible noise added to continuous lab/ECG inputs produces bounded, non-erratic shifts in local SHAP rankings.
4. **Spurious-Shortcut & Confounder Audit (Mandatory for G14):** Explicitly inspect top global and local SHAP drivers for **non-clinical shortcuts**—such as hospital/site proxies, missingness indicator flags dominating true physiological predictors, ECG powerline/baseline artifacts, or post-diagnosis leakage variables! Any detected shortcut triggers immediate root-cause investigation before writing.

## 8.3 Clinical plausibility review and bounded XAI claims (`UD21`)

1. **Qualified cardiologist plausibility review (`STEP-040`):** Present a prospectively sampled, balanced set of de-identified local explanation packets (patient summary + calibrated risk score + modality share + top tabular SHAP waterfall + ECG attribution overlay) covering **TP, FP, TN, and FN** cases (plus global SHAP summary) to a qualified cardiologist/clinician using a structured rubric (`T20`): (a) concordance of top risk drivers with cardiovascular pathophysiology, (b) clinical actionability/intelligibility of explanations, and (c) identification of clinically implausible or contradictory attributions.
2. **Strict Q1 claim boundaries:**
   - **Permitted (when evidenced):** "The multimodal SHAP explanations demonstrated high perturbation faithfulness (AOPC vs random baseline), multi-seed rank stability, concordance with modality ablation, absence of major missingness/site shortcuts, and alignment with established clinical risk factors under structured cardiologist review."
   - **Prohibited (unless a separate IRB-approved clinician reader study is actually conducted):** "Our framework increases doctors' trust," "enables faster hospital decision-making," or "proves that [feature X] causes CVD."

<a id="os-09"></a>
# 9. Research prototype, reproducibility, and optional defense interface

## 9.1 Minimal research decision-support prototype contract

Implement a reproducible research inference and explanation entry point (`src/cvd_mm/prototype.py` + thin CLI under `14_Automation/`) that accepts structured 4-modality input (including explicit missing-modality handling), validates schema/ranges/ECG integrity, loads the hash-verified frozen `PP####` fitted state, `MODEL####`, calibrator, and SHAP background reference, and outputs:
- Calibrated CVD risk probability + frozen threshold classification;
- Explicit modality-availability status (flagging any missing modality and associated uncertainty caveat);
- Modality-level SHAP shares + top tabular feature contributions + optional ECG attribution overlay;
- Full provenance metadata (`MODEL ID`, `PP ID`, `REL ID`, calibrator/threshold hash, code commit);
- Persistent **research-only non-diagnostic disclaimer**.

Handle invalid inputs, out-of-range units, corrupted ECG files, missing-model hash mismatches, and missing-all-modalities failures with explicit structured errors—never silent fallback zeros.

## 9.2 Reproducibility levels and clean-environment audit

Distinguish three reproducibility tiers explicitly in `13_Documentation/reproducibility_audit.md`:
- **Level A (Deterministic Replay):** Reloading frozen `PP`, `MODEL`, calibrator, and SHAP background in a clean environment to reproduce test predictions, all 6+ metrics, calibration/DCA curves, statistical CIs, and SHAP tables/figures within strict numeric tolerance.
- **Level B (Full Retraining Replay):** Retraining the champion and key baselines from `REL####` using exact locked configs and seeds, reporting observed variance under documented hardware/GPU nondeterminism.
- **Level C (External/Conclusion Robustness):** Whether core scientific conclusions (multimodal gain, calibration, XAI faithfulness) hold across seeds and (if adopted) external validation.

Execute `STEP-042` (`G15`) in a genuinely fresh environment following only written installation and execution instructions (`13_Documentation/reproduce.md`). Where primary hospital data cannot be publicly redistributed due to IRB/privacy restrictions, publish lawful controlled-access instructions, complete code, synthetic end-to-end demo data reproducing pipeline execution, and restricted internal audit evidence.

## 9.3 Optional interactive demonstration interface for defense (`UD22`)

Unlike a mandatory cloud deployment, `fydp_title_proposal.pdf` does not mandate a hosted website. If the supervisor or research team elects under `UD22` to showcase the research prototype through a local interactive dashboard or hosted web interface at the FYDP defense:
1. It must live in `prototype_ui/` as a thin presentation layer importing the exact frozen `STEP-041` entry point—never duplicating preprocessing, calibration, thresholds, or SHAP logic.
2. It must serve ONLY the `G11`-frozen, `G12`/`G14`-evaluated champion model with startup SHA-256 hash verification, display a persistent research-only disclaimer, accept ONLY synthetic or IRB/disclosure-approved de-identified sample profiles (zero persistent storage of uploaded PHI), pass an output-parity check against `STEP-041`, and maintain a rehearsed offline local fallback.
3. Interface screenshots are illustrative system outputs only and never substitute for evaluation evidence. If `UD22` declines a web/GUI interface, record that disposition cleanly; `G15` and `G17` do not penalize a CLI/script-only research prototype.

<a id="os-10"></a>
# 10. Q1 journal and FYDP thesis writing and submission operating system

## 10.1 Evidence-first writing and claim traceability

Maintain one canonical claim ledger (`02_Literature/claims.csv`) and one writing registry (`12_Writing/writing_registry.csv`). Every empirical number, comparative assertion, statistical claim, and clinical interpretation in both thesis and Q1 manuscript must trace to verified `P####`, `DS####`/`ADJ####`, `EXP####`, `EVAL####`, `XAI####`, or `FIG####`/`TAB####` records. Use `Evidence pending` during early drafting; **zero** placeholder numbers or unresolved `Evidence pending` markers may survive into `G16`.

## 10.2 Dual-track structure: FYDP Thesis vs Q1 Journal Manuscript

Use **one single frozen evidence base** to author both deliverables:

1. **FYDP Thesis (`12_Writing/thesis/`):** Follows Daffodil International University CSE499 institutional formatting (`UD23`), covering full engineering detail, complete literature synthesis, CRF/ECG specs, full baseline/ablation logs, prototype design, and appendices.
2. **Q1 Journal Manuscript (`12_Writing/paper_q1/`):** Concise, high-impact scientific narrative structured for top-tier biomedical-AI venues (e.g., *IEEE JBHI*, *Computers in Biology and Medicine*, *Artificial Intelligence in Medicine*, *Journal of Biomedical Informatics*, *Information Fusion*, *npj Digital Medicine* — exact venue decided under `UD23`):

| Q1 Manuscript Section | Mandatory Q1 evidence & TRIPOD+AI elements | Anti-rejection guardrail |
|---|---|---|
| **Abstract (Structured)** | Objective, cohort/setting ($N$, events, modalities), fusion & XAI methods, primary held-out results (AUC + 95% CI, PR-AUC, F1, calibration, DeLong $p$), XAI faithfulness summary, bounded clinical implication | Exact agreement with main tables; zero overstated clinical claims |
| **Introduction** | Verified CVD burden (including South Asia/Bangladesh citations), verified synthesis of multimodal ECG+clinical+lab+lifestyle literature, sharpened evidence-backed gap, explicit RQs & contributions | No unverified "first ever" claim; no uncited proposal assertions |
| **Materials & Methods** | IRB/consent/setting, inclusion/exclusion + cohort flow diagram, exact CVD endpoint & horizon, $t_0$/$\Delta t$ alignment, 4-modality schema & ECG specs, patient-level split, leakage-free preprocessing/imputation, 4-tier baselines + Transformer architecture, calibration/threshold/statistical/DCA plan, quantitative XAI faithfulness/stability/clinician-review plan | Explicitly document leakage prevention (resolving proposal diagram order) and TRIPOD+AI item locations |
| **Results** | Cohort baseline characteristics table (CVD+ vs CVD−, missingness, per-modality availability); Tier 1–4 main comparison table (all 6 proposal metrics + PR-AUC + Brier/ECE + 95% CIs + DeLong $p$); progressive & LOMO modality ablation; missing-modality stress test; ROC/PR/Calibration/DCA multi-panel figure; subgroup fairness table; global/modality/local SHAP + ECG overlay figures; quantitative deletion/insertion AOPC & stability results; cardiologist review summary | Include all negative/null findings and multi-seed variance; zero selective reporting |
| **Discussion & Limitations** | Clinical interpretation of multimodal synergy (and lifestyle/ECG marginal value), honest comparison with prior literature (acknowledging dataset/endpoint non-comparability), XAI faithfulness & shortcut findings, **explicit PROBAST-AI risk-of-bias & limitations discussion** (sample size, cross-sectional vs longitudinal horizon, single/local-region external validity, incorporation bias, lack of prospective clinical impact trial), future work | Separate observed findings from biological hypotheses; never infer causality from SHAP |
| **Declarations & Supplements** | Ethics/IRB approval number & consent statement, Data & Code Availability Statement (lawful controlled access + public code/synthetic demo), Competing Interests, Funding, Author Contributions (CRediT), completed **TRIPOD+AI (2024) checklist** (`12_Writing/checklists/TRIPOD_AI.csv`), **PROBAST-AI self-audit** | Complete transparency required by all Q1 biomedical journals |

## 10.3 Publication-grade Q1 figures, tables, and citation integrity

Assign `FIG####` and `TAB####` IDs in `11_Figures_Tables/assets.csv` with source `EVAL`/`XAI`/`DS` hash, generating script/command, vector/high-resolution output (PDF/SVG/EPS + 300–600 DPI TIFF/PNG), colorblind-safe palette, units, error bars/CI bands, and captions. Recommended core Q1 visual suite:
- `FIG0001`: Cohort recruitment, exclusion, modality-availability, and patient-level split flow diagram (STARD/CONSORT-style).
- `FIG0002`: Leakage-safe Transformer-based Multimodal Fusion & XAI architecture schematic (showing 4 modality encoders, missing-modality masking, cross-modal attention, calibration, and SHAP layer).
- `FIG0003`: Multi-panel held-out evaluation figure (ROC curves with 95% CI bands, Precision-Recall curves, Calibration Reliability Diagrams, and Decision Curve Analysis Net Benefit comparing Champion vs Unimodal & Fusion baselines).
- `FIG0004`: Modality Ablation (Progressive Addition + Leave-One-Modality-Out) & Missing-Modality Degradation curves.
- `FIG0005`: Multimodal Explainability figure (Modality-level SHAP share, Global tabular beeswarm/dependence plots, and de-identified representative TP/FP/FN local waterfall + ECG waveform attribution overlays).
- `FIG0006`: Quantitative XAI Faithfulness (Deletion/Insertion perturbation curves vs random control) & Multi-Seed Stability analysis.

Verify 100% of citations in `02_Literature/references.bib` against original publisher records/DOIs. Never copy unverified bibliographic strings or cite unread articles.

## 10.4 Peer-review rebuttal workflow and document-scoped submission gates

Track both supervisor feedback and future Q1 journal peer-review comments in `12_Writing/reviews/` (`T25`) with exact comment, categorization (editorial vs methodological vs new experiment), response, manuscript diff location, and evidence. Any new experiment requested by journal reviewers re-enters `STEP-028–030` under new `EXP`/`EVAL` IDs without overwriting prior submitted evidence.

**Document-scoped G16 readiness:**
- `G16 / thesis` (`STEP-046`) gates FYDP thesis submission (`STEP-047`) independently of Q1 journal drafting.
- `G16 / paper` (`STEP-048`) gates Q1 manuscript submission (requiring complete manuscript, TRIPOD+AI & PROBAST-AI supplements, verified claims/citations/figures, venue compliance, and all authors' + supervisor sign-off). If Q1 submission is formally deferred past FYDP completion, record an explicit approved disposition under `UD23` rather than asserting a false `G16 / paper` PASS. Project completion (`G17`) never depends on uncertain external journal acceptance, only on evidenced fulfillment of the approved submission or disposition obligation.

<a id="os-11"></a>
# 11. Version control, PHI security, and tiered artifact storage

## 11.1 Git discipline and clinical privacy protection

Use Git for source code (`src/cvd_mm/`, `tests/`), non-sensitive configs, CSV registries, literature notes, safe aggregated metrics/SHAP summaries, figure specs, documentation, and manuscript sources. Use a protected `main` branch with short-lived reviewed feature branches and semantic commits (`docs:`, `lit:`, `cohort:`, `schema:`, `prep:`, `model:`, `exp:`, `eval:`, `xai:`, `writing:`, `fix:`) referencing entity/step IDs.

**Zero-PHI-in-Git rule:** Inspect every diff before committing or pushing. Never commit raw clinical spreadsheets, raw ECG waveforms/PDFs, patient linkage maps, free-text clinical notes, individual patient predictions, patient-level SHAP plots containing identifiers, credentials, or model weight binaries. Remember `.gitignore` does not remove files once accidentally tracked; any accidental PHI commit triggers immediate institutional breach/history-remediation protocol (`Section 11.4`).

## 11.2 Four-tier storage model

| Tier | Contents | Security & persistence policy |
|---|---|---|
| **Tier 1: Source Control (Git)** | Code, tests, templates, safe CSV registries, configs, aggregate tables/metrics, literature notes, manuscripts, artifact pointers/hashes | Private/access-controlled repository per `UD13`; diff-audited before push |
| **Tier 2A: PHI Linkage Vault** | Patient real identities ↔ `PAT########` / `ENC########` lookup tables, signed consent forms, raw unstripped hospital dumps | Encrypted offline or hospital/institution-controlled vault; strictly isolated from analytical compute and never accessible to training scripts |
| **Tier 2B: Restricted De-Identified Clinical Tier** | De-identified raw/processed tabular cohorts, raw/filtered ECG waveforms, native adjudication logs, restricted per-patient predictions & local XAI packets | Access-controlled encrypted institutional/local storage; excluded from ordinary Git; regular encrypted backups verified by SHA-256 |
| **Tier 3: Versioned Research Artifacts** | Trained checkpoints (`CKPT`), exported models, fitted preprocessors/calibrators, full SHAP tensor arrays, complete run logs | Approved versioned artifact store with SHA-256 manifests and verified retrieval; ephemeral notebook/cloud disks are never the sole copy |
| **Tier 4: Immutable Release & Q1 Archive** | Submitted thesis & Q1 manuscript snapshots, submission receipts, source tag, TRIPOD+AI checklists, public-permitted code + synthetic demo bundle, restricted restoration manifest | Immutable snapshots (`ARCH####`); public sharing strictly limited to IRB-permitted non-PHI artifacts |

## 11.3 Two-phase environment readiness

- **Phase 1 (`environment/data/`, `STEP-002`, verified at `G02`):** Minimal pinned environment for registry validation, CSV/schema inspection, unit checks, read-only ECG signal parsing, splitting, and preprocessing tests on synthetic fixtures—without prematurely locking a deep learning framework or GPU stack.
- **Phase 2 (`environment/model/`, `STEP-024`, verified at `G09`):** Full modeling, calibration, statistical inference, and SHAP environment pinned after `UD13` (PyTorch vs TensorFlow) and hardware verification. Preserve `environment/data/` untouched; if shared library upgrades alter preprocessing outputs, re-verify `G08` with a new `PP`/`REL` version before training.

## 11.4 Synchronization, backups, and incident recovery

Verify code commit, config hash, input `REL` hash, storage quota, and PHI compliance of the compute host before every training session (never upload hospital clinical/ECG data to an unapproved public cloud or unapproved third-party AI API!). Persist checkpoints and logs continuously during runs and verify SHA-256 digests on transfer. If PHI leaks or an artifact corrupts: freeze distribution immediately, notify supervisor and hospital custodian/IRB per institutional rules, rotate affected credentials, quarantine corrupted binaries, and restore only from hash-verified backups—never silently fabricating lost training history.

<a id="os-12"></a>
# 12. Roles, human decisions, and AI-assisted task contracts

Roles define accountability boundaries; in a two-student FYDP team, Rayan Ahmed and Mohammad Nafis Sadiq share operational roles explicitly assigned at `STEP-001`, while clinical, ethical, and supervisory sign-offs strictly remain with qualified humans.

| Role | Responsibility | Non-negotiable decision boundary |
|---|---|---|
| **Researchers (Rayan Ahmed & Mohammad Nafis Sadiq)** | Literature review, cohort curation, preprocessing, baseline & Transformer modeling, calibration, stats, XAI engineering, thesis & Q1 drafting | Propose choices and execute approved protocols; cannot self-certify IRB approval or clinical diagnosis/plausibility |
| **Supervisor (Md. Mizanur Rahman)** | Scope ratification, RQ/contribution positioning, methodology/ablation review, thesis & Q1 manuscript approval | Ratifies scientific scope, split/evaluation freeze, and submission readiness |
| **IRB / Hospital Data Custodian** | Ethical review, hospital data-collection authorization, consent/waiver verification, PHI security & retention rules | Sole authority permitting human-subjects healthcare data use |
| **Qualified Cardiologist / Clinical Adjudicator** | CVD endpoint charter, variable clinical validity, ECG filter-morphology fidelity, outcome adjudication, error & XAI clinical plausibility review | Sole clinical authority; AI tools never replace medical judgment |
| **Implementer** | Clean modular code in `src/cvd_mm/`, leakage/unit tests, reproducibility packaging | Cannot silently alter split rules, class/outcome maps, preprocessing fits, or frozen thresholds |
| **Evaluation & Biostatistics Reviewer** | Freeze verification (`G11`), metric/calibration/DCA/DeLong correctness, PROBAST-AI audit | Strictly barred from test-informed tuning or selective reporting |
| **XAI Reviewer** | SHAP additivity, faithfulness (AOPC), stability, shortcut auditing, claim-boundary enforcement | Bars decorative XAI and unproven causal/trust claims |
| **Writing & Q1 Release Owner** | Claim/citation audit, TRIPOD+AI checklist, thesis & Q1 submission packages, immutable archive | Distinguishes drafted, ready, submitted, and accepted states strictly by receipt |

**Human handoff contract:** Present the decision question (`UD##`), source facts, options with Q1/clinical tradeoffs, blocking gate, exact file path to record `DEC####`, and verification method. Pause only dependent steps while independent literature/documentation work continues.

**AI-assisted task contract:** Every AI-assisted planning, coding, or drafting prompt specifies exact inputs, allowed paths, prohibited actions, uncertainty labels, verification tests, and human sign-off boundaries. **Strict prohibition:** NEVER paste raw patient data, clinical charts, PHI, or raw hospital ECG files into external unapproved AI prompts or chat interfaces.

<a id="os-13"></a>
# 13. Daily research operations and Q1 risk governance

- **Session Start:** Check `dashboard.md`, previous session diary (`T03`), current gate states (`gates.csv`), open blocking `UD##` items, Git status, and storage availability. Select one bounded step or batch whose prerequisite gates are `PASS`.
- **Session Execution:** Run planning/review check before implementation; log repetitive literature extraction, chart abstraction/adjudication, multi-seed experiments, and chapter drafting using dated batch/RUN IDs.
- **Session Close:** Verify outputs and hashes, preserve failed attempts, update owning registries/risks, push only PHI-free Tier 1 files, and log the exact next unblocked action.
- **Weekly & Milestone Reviews (`T30`):** Audit RQ alignment, hospital recruitment/IRB progress, missing-modality rates, compute budget, invalidated/STALE gates, TRIPOD+AI gaps, and backup integrity. Update provisional timelines from observed enrollment and compute rates—never invent completion dates.

**Initial Domain-Specific Q1 Risk Themes (scored by team in `risk_register.csv`):**
1. *IRB/hospital approval delay or insufficient enrollment* → Mitigate via early `STEP-011` submission, multi-center planning, and prospective `UD06`/`UD26` external cohort & compact-model contingency.
2. *Cross-sectional vs longitudinal endpoint mismatch* → Mitigate via strict `UD02` endpoint charter and honest diagnostic/risk-stratification framing.
3. *Post-diagnosis or pre-split data leakage* → Mitigate via strict $t_0/\Delta t$ index-time audit, automated leakage unit tests, and mandatory post-split fitting (`G07–G08`).
4. *Heterogeneous/noisy ECG formats or filter distortion of ST-T waves* → Mitigate via early `UD07` format audit and cardiologist raw-vs-filtered morphology check (`G08`).
5. *Small-$N$ Transformer overfitting vs GBDT baselines* → Mitigate via EPV sizing, regularization/transfer learning, nested CV, and honest Q1 reporting regardless of winner.
6. *Uncalibrated risk probabilities or spurious MNAR/site shortcuts in SHAP* → Mitigate via validation-only calibration, DCA, and mandatory `G14` faithfulness + shortcut audit.
7. *PHI leakage or artifact loss* → Mitigate via Tier 2A/2B isolation, pre-push diff inspection, and hash-verified backup restore tests.
8. *Unsubstantiated novelty or missing TRIPOD+AI items causing Q1 desk rejection* → Mitigate via zero-seed systematic review (`G03`) and full TRIPOD+AI / PROBAST-AI compliance (`G16`).

<a id="os-14"></a>
# 14. Quality gates and completion

## 14.1 Assessment semantics

Every gate (`G01–G17`) evaluates to **PASS** or **FAIL** when formally assessed. Initial state `NOT ASSESSED` and invalidated state `STALE` block all dependent work identically to `FAIL`. Passing requires 100% of mandatory criteria satisfied with file paths, SHA-256 hashes, entity versions, assessor/date, and named human approval. Missing evidence is always `FAIL`, never "conditional PASS." Record every assessment in `01_Project_Management/gates.csv` and `01_Project_Management/reviews/G##_assessment_<date>.md` (`T22`). Any material change to a parent entity marks all downstream gates `STALE` until reassessed. **Crucial scientific distinction:** A technically valid negative result (e.g., multimodal fusion giving modest gain over a strong unimodal baseline) can still **PASS** all scientific gates (`G10–G17`) when rigorously executed and honestly reported.

## 14.2 Canonical gate matrix (`G01–G17`)

| Gate / owning step | PASS evidence and mandatory criteria | FAIL / blocked transition | Human reviewer |
|---|---|---|---|
| **G01** Scope & decision charter / `001` | Verbatim approved title; `RF01–RF18` verified against `fydp_title_proposal.pdf`; scope & exclusions adopted; all `UD01–UD26` assigned owners/deadlines; evaluation-report/feedback status confirmed | Scope drift or invented approvals; blocks repository adoption and research protocols | Supervisor + researchers |
| **G02** Repository, PHI storage & minimal tooling / `003` | Canonical folders, READMEs, blank templates `T01–T32`, Appendix B CSV registries, PHI ignore/vault policy verified, and tested `environment/data/` lock | Missing homes, unsafe PHI handling, or untested data runtime; blocks operational intake | Research lead |
| **G03** Systematic literature & Q1 RQs / `009` | Reproducible multi-database search logs, PRISMA screening counts, original-full-text verified extractions, `PG1–PG5` tested with counterevidence, approved RQ-to-evaluation map | Unverified citations, biased search, or refuted novelty kept intact; blocks final cohort design | Supervisor |
| **G04** Ethics/IRB, cohort intake & 4-modality quality / `013` | Written IRB/ethics approval & hospital permissions, consent/waiver, EPV feasibility, immutable raw hashes, PHI de-identification audit, 4-modality quality/ECG/missingness report, approved cohort card | Missing IRB/permission, PHI exposure, irreconcilable counts, or unusable ECG/data; blocks production curation | IRB/custodian + supervisor + researchers |
| **G05** Endpoint ontology, 4-modality schema & QA protocol / `015` | Approved `endpoint_charter.md` ($t_0$, $\Delta t$, horizon, ICD/clinical criteria), finalized `variables.csv`, CRF & ECG contract, incorporation-bias review, prospective pilot/QA thresholds & named cardiologist | Ambiguous CVD endpoint, unstandardized units/ECG format, or missing clinical authority; blocks pilot | Cardiologist + supervisor |
| **G06** Pilot & frozen adjudicated cohort/label release / `018` | Accepted pilot agreement ($\kappa$/ICC), tracked production batches, resolved adjudications, structural/unit/linkage/ECG-readability QA, frozen `ADJ####` hashes | Unresolved label errors, failed agreement thresholds, or unreviewed labels; blocks splitting | Cardiologist + data lead |
| **G07** Leakage-safe patient/site-level split / `020` | Zero patient/encounter/duplicate overlap across partitions, deterministic split manifest/seed, target vs actual prevalence/subgroup balance, documented CV/holdout design, sealed test-set custody | Cross-partition patient overlap or unsealed test access; blocks preprocessing fit & training | Supervisor + data/biostats lead |
| **G08** Preprocessing, ECG fidelity & release integrity / `022` | Raw unchanged; record-local ECG filtering passed cardiologist morphology check (ST-T preserved); all imputers/scalers/encoders fit strictly on Train (`FitStateHash`); zero `NaN`/`Inf`; immutable `REL####` manifest & hashes | Pre-split fitting leakage, distorted ECG waveforms, or unit/schema mismatch; blocks baseline modeling | Clinical/ECG lead + implementer |
| **G09** Runtime, experiment/eval/XAI plan & recovery readiness / `027` | Approved PyTorch/TF & baseline/Transformer design (`UD13–UD14`); pinned tested `environment/model/`; approved experiment/ablation, calibration/stats/DCA, and SHAP/faithfulness protocols (`UD15–UD21`); passing unit/leakage/metric tests; diagnostic smoke run & verified checkpoint interruption/restore | Unresolved config fields, unverified metric/SHAP code, or failed recovery proof; blocks full experiments | Supervisor + method/eval reviewer |
| **G10** Experiment completion & model eligibility / `030` (repeated at `031`) | Valid stopping, complete logs/config/seeds, hash-verified checkpoints, all failed attempts preserved, `MODEL####` card registered | Incomplete logs, altered config post-launch, or undocumented failure; blocks candidate eligibility | Experiment reviewer |
| **G11** Validation-only selection & final-test freeze / `032` | Completed Tier 1–4 & ablation validation matrix; champion & comparators selected strictly on validation; frozen operating threshold $\tau$, calibrator, stats/XAI plans & hashes; test-access log verified clean | Test-informed selection, unfrozen threshold/calibrator, or test contamination; blocks test inference | Supervisor + evaluation reviewer |
| **G12** Final evaluation, calibration, stats & DCA / `036` | Complete test coverage; all 6 mandatory proposal metrics + adopted PR-AUC, Specificity/NPV, Brier/ECE/slope, DCA, bootstrap 95% CIs, paired DeLong/McNemar with multiple-testing adjustment; all unfavorable results preserved | Missing mandatory metric, threshold tuned on test, missing CIs/calibration, or invalid evaluator; blocks quantitative claims | Evaluation & biostats reviewer |
| **G13** Subgroup fairness, robustness, error & PROBAST-AI audit / `037` | Sex/age/site subgroup metrics, missing-modality degradation audit, systematic TP/FP/TN/FN error review with clinical input, completed PROBAST-AI self-audit & bounded limitations | Cherry-picked cases, hidden subgroup disparity, or overstated clinical utility; blocks final conclusions | Cardiologist + supervisor |
| **G14** Multimodal XAI faithfulness, stability & clinical review / `040` | Training-only SHAP background, verified additivity, global/local/modality-share + ECG attributions, deletion/insertion AOPC vs random control, LOMO concordance, multi-seed stability, shortcut audit clean (or disclosed/remediated), cardiologist plausibility review & bounded XAI claims | Decorative SHAP without faithfulness/stability, test-set background leakage, unaddressed shortcut, or causal/trust overclaiming; blocks XAI claims | XAI reviewer + cardiologist + supervisor |
| **G15** Research prototype & clean reproducibility audit / `042` | Tested frozen inference + SHAP prototype (plus parity/privacy/fallback proof if optional `UD22` demo built); fresh-environment artifact retrieval, hash verification, and replay within tolerances; declared reproducibility level & lawful access limits | Unreproducible metrics/SHAP, missing artifacts, or PHI leak in demo; blocks submission readiness | Reproduction reviewer |
| **G16** Document-specific submission readiness / `046` (thesis); `048` (Q1 paper) | Complete target document & supplements (`TRIPOD_AI.csv`, `PROBAST_AI.md` for Q1 paper), 100% original-source verified citations, claim-to-evidence parity, figure provenance, institutional/journal format checks, resolved reviews, and author/supervisor sign-off — assessed separately per document | Missing evidence blocks only that document; thesis does not wait on Q1 paper; approved paper deferral is a disposition, never a false PASS | Supervisor + authors |
| **G17** Final project completion & archive handover / `050` | All applicable prior gates current PASS; FYDP thesis submission receipt; Q1 paper submission receipt or approved disposition; immutable `ARCH####` snapshot respecting IRB/PHI tiers; verified restore test; deliverable handover | Missing submission receipt/disposition, unverified restore, or stale gate; blocks completion declaration | Researchers + supervisor |

## 14.3 Failure recovery and project completion definition

On any gate `FAIL`, log exact failed items, root cause, owner, and remediation plan, return to the earliest responsible parent step, preserve the failed assessment permanently, and append a new `AssessmentID` upon re-audit. Project completion (`G17`) means evidenced fulfillment of all approved deliverables, ethical/reproducibility standards, and honest scientific conclusions—never contingent on positive superiority hypotheses or uncertain external journal acceptance.

<a id="os-15"></a>
# 15. Template library

## 15.1 Template contract

Templates `T01–T32` are materialized blank in `15_Templates_Prompts/` at `STEP-003`. Every template carries the common metadata header: `TemplateID, template_version, entity_id, owner, date, status, source_inputs, governing_section, phi_sensitivity, reviewer`. Filled instances reside in their owning domain folders; unresolved fields remain explicitly `Unresolved / Human Decision Required` and absent source facts remain `not reported`.

## 15.2 Operational templates (`T01–T32`)

| ID / template | Purpose / instance location | Required body fields | Verification / common mistake |
|---|---|---|---|
| T01 `readme.md` | Folder contract / each materialized folder | Purpose; owner; inputs; contents; workflow/commands; outputs; PHI sensitivity; governing sections | Reflects actual contents; never duplicates handbook |
| T02 `decision.md` | Resolve `UD##` / `01_Project_Management/decision_log/DEC####.md` | UD ref; question; proposal facts; options; Q1/clinical tradeoffs; recommendation; actual human decision; date; approver; rejected options; affected gates; review trigger | Never invent decisions; preserve superseded DECs |
| T03 `session.md` | Daily log / `01_Project_Management/diary/` | Step/batch; objective; prerequisites; planned vs actual outputs; checks; blockers; decisions; sync status; next action | Separate planned work from completed evidence |
| T04 `search.md` | Reproducible lit search / `02_Literature/searches/` | Database; verbatim query; date; date/language filters; retrieved count; export hash/pointer; dedup rule; limitations | Exact syntax logged; never fabricate counts |
| T05 `paper_summary.md` | Grounded paper extraction / `02_Literature/summaries/P####.md` | Verified DOI/citation; country/cohort; $N$/events; endpoint/horizon; exact modalities & ECG format; split/leakage/PROBAST risk; fusion model; baselines; metrics/calibration/DCA; XAI faithfulness/clinician review; locators; limitations; critique | Every number has page/table locator; unread text never guessed |
| T06 `gap.md` | Test `PG1–PG5` / `02_Literature/gap_notes/GAP####.md` | ProposalGap; proposed statement; search coverage; supporting & contradicting `P####` IDs; sharpened Q1 framing; status; RQ links | Absence in small search is not proof of novelty |
| T07 `claim.md` | Claim traceability / `02_Literature/claim_notes/CLAIM####.md` | Statement; scope; evidence IDs/locators; counterevidence; uncertainty; permitted clinical/XAI wording; writing locations | Never cite a hypothesis or SHAP plot as causal proof |
| T08 `site_irb.md` | Hospital/IRB authorization / `03_Datasets_Cohort/irb_permissions/SITE####.md` | Site ID/department; IRB approval ID/date; consent/waiver; recruitment protocol; permitted modalities; PHI de-identification; retention/sharing terms | Signed originals stay in restricted tier; never assume IRB |
| T09 `cohort_card.md` | Cohort & quality card / `03_Datasets_Cohort/reports/DS####_card.md` | Origin/version; IRB/DUA ref; enrollment dates; $N$ patients/encounters/events; 4-modality availability & missingness; ECG specs/QC; demographics; spectrum/selection bias; hashes; access instructions | Reconciled counts; never infer uncollected demographics |
| T10 `endpoint_charter.md` | Clinical CVD target / `04_Outcome_Schema_QA/endpoint_charter.md` | Exact CVD definition & ICD/clinical codes; control criteria; prospective vs cross-sectional horizon; index time $t_0$; $\Delta t$ alignment window; incorporation-bias assessment; uncertain case rule; cardiologist sign-off | No horizon mismatch; no post-diagnosis predictors |
| T11 `crf_ecg_protocol.md` | Collection & ECG contract / `04_Outcome_Schema_QA/ecg_contract.md` | Variable dictionary version; CRF items/coding; lab assay/unit harmonization; ECG device/leads/Hz/duration/schema; PHI header scrubbing; QA sampling & $\kappa$/ICC thresholds | Units and ECG format pinned before collection |
| T12 `adjudication_batch.md` | Curation/adjudication QA / `04_Outcome_Schema_QA/reviews/ADJB####.md` | Batch encounter membership; site; abstractor/adjudicator; protocol version; dual-entry $\kappa$/ICC; ECG quality rejections; discrepancies resolved; native/verified hashes | No batch closed without required clinical review |
| T13 `preprocessing.md` | Modality PP & fit report / `05_Preprocessing_Alignment/reports/PP####.md` | Rationale; record-local vs training-fitted ops; ECG filter parameters & cardiologist morphology check; imputation/missing-mask rules; scaling/encoding; `FitStateHash`; leakage-test proof; output hashes | Zero validation/test leakage; ST-T morphology verified |
| T14 `split.md` | Leakage-safe split report / `03_Datasets_Cohort/splits/SPLIT####/report.md` | Input hash; patient/site grouping keys; connected-component audit; algorithm/seed; CV vs fixed split ratios; outcome/site/sex support per partition; zero-overlap assertion; test-seal custody; approval | Never split one patient across partitions |
| T15 `failure.md` | Failure/anomaly record / owning entity `failure_report.md` | Timestamp; affected IDs; observed symptoms; logs; suspected cause (labeled); impact; recovery; lost work; prevention; status | Never delete failed/diverged/negative runs |
| T16 `experiment.md` | Plan & run report / `07_Experiments/EXP####/README.md` | RQ/tier/hypothesis; changed vs fixed factor; `REL`/hashes; config; seeds/budget/stopping; `RUN` IDs; validation metrics; anomalies; actual conclusion; next action | Planned outcome never prefilled as observed |
| T17 `model_card.md` | Bounded model card / `06_Models_Fusion/cards/MODEL####.md` | Tier/architecture/params; framework/pretrained provenance; `EXP`/`CKPT`/`REL`/`PP` hashes; modality dependencies & missing-modality behavior; calibration/threshold; `EVAL`/`XAI` IDs; intended research use & exclusions | No clinical approval or causal claim inferred from AUC |
| T18 `checkpoint.md` | Checkpoint & restore manifest / `08_Checkpoints/manifests/CKPT####.md` | `CKPT`/`EXP`/`RUN`; role/epoch; saved state components; config/model hashes; storage path/SHA-256/bytes; backup pointer; restore-test evidence | Weights-only file is not exact-resumable |
| T19 `evaluation.md` | Quantitative eval report / `09_Evaluation_Stats/EVAL####/report.md` | Freeze/model/calibrator/threshold/data hashes; test coverage; 6 mandatory metrics + PR-AUC/Spec/NPV; Brier/ECE/slope; DCA; bootstrap 95% CIs; DeLong/McNemar + multiplicity adj; subgroup & missing-modality tables; deviations | All numbers trace to raw frozen outputs; zero test tuning |
| T20 `error_probast.md` | Error & PROBAST-AI review / `09_Evaluation_Stats/EVAL####/error_probast.md` | Stratified TP/FP/TN/FN sampling rule; reviewed case patterns; clinical error vs label uncertainty; missing-modality failure modes; 4-domain PROBAST-AI risk-of-bias table; bounded limitations | Balanced sampling; no cherry-picking or causal leaps |
| T21 `xai_audit.md` | Multimodal XAI audit / `10_Explainability_XAI/XAI####/report.md` | `MODEL`/`EVAL`/training-background hashes; SHAP explainer & additivity check; modality-share vs LOMO concordance; deletion/insertion AOPC vs random control; multi-seed/perturbation stability; shortcut audit; cardiologist plausibility rubric summary; permitted wording | Faithfulness & shortcut checks mandatory before claiming explainability |
| T22 `gate_audit.md` | Gate PASS/FAIL audit / `01_Project_Management/reviews/G##_assessment_<date>.md` | Gate/entity versions; itemized mandatory criteria; evidence path + SHA-256; PASS/FAIL; corrective actions; assessor/date; human reviewer approval; invalidated descendants | Missing evidence = FAIL; no prechecked boxes |
| T23 `figure_table.md` | Q1 asset spec / `11_Figures_Tables/specs/FIG####.md` or `TAB####.md` | Purpose; source `EVAL`/`XAI`/`DS` hashes; exact generator command/script; axes/units/CIs/DPI; caption; PHI/permission check; visual review; thesis/paper locations | Zero manual editing of plotted numbers |
| T24 `reproduce.md` | Clean-environment audit / `13_Documentation/reproducibility_audit.md` | Environment lock; artifact retrieval & SHA-256 check; exact replay commands; prospective tolerances; observed metric/SHAP agreement; declared Level A/B/C; lawful data-access limits | Distinguish replay from full retraining honestly |
| T25 `review_response.md` | Supervisor / Q1 peer-review log / `12_Writing/reviews/` | Reviewer/date; verbatim comment; type (editorial/method/new EXP); action; manuscript diff locator; evidence ID; point-by-point response; status | Re-enter gated steps for new experiments; preserve history |
| T26 `writing_unit.md` | Thesis/paper section / `12_Writing/` | `WR####`; document (`thesis`/`paper_q1`); RQs; `CLAIM`/`P`/`EXP`/`EVAL`/`XAI`/`FIG`/`TAB` links; draft; TRIPOD+AI item tags; pending evidence; review state | No invented metrics or citations |
| T27 `tripod_ai_checklist.md` | Q1 TRIPOD+AI compliance / `12_Writing/checklists/TRIPOD_AI.csv` | Item number; TRIPOD+AI domain/requirement; applicability; exact manuscript page/section locator; verified evidence ID; reviewer check | Complete 100% of applicable items before `G16 / paper` |
| T28 `submission.md` | Submission & disposition / `12_Writing/<doc>/submission.md` | Target university/journal; actual author guidelines; compiled file SHA-256s; supplements; CRediT authorship; IRB/ethics/COI declarations; `G16` PASS ID; submission date & receipt OR approved deferral disposition | Never equate drafted with submitted, or submitted with accepted |
| T29 `archive.md` | Immutable handover / `16_Archive/ARCH####.md` | Release tag; full artifact/hash inventory; PHI tier segregation; public vs restricted subset; licenses; retention/destruction schedule; verified restore proof; custodian/owner handover | Never bundle PHI into public archive |
| T30 `risk_meeting.md` | Weekly/milestone review / `01_Project_Management/meetings/` | Attendees; gate/enrollment/compute evidence; risk triggers & mitigations; actual supervisor feedback; decisions; owners/dates; revised provisional forecast | Forecasts provisional; never fabricate meeting records |
| T31 `prompt.md` | AI task prompt / `15_Templates_Prompts/` | Role; objective; inputs; allowed paths; prohibited changes; uncertainty/PHI rules; verification checks; human boundary; version | Zero PHI/patient data in any prompt |
| T32 `config.yaml` | Executable multimodal EXP config / `07_Experiments/EXP####/config.yaml` | All Section 6.2 fields fully resolved (4 modalities, encoders, fusion, imbalance, calibration, seeds, runtime, outputs) | Validator rejects any `null` executable field or test-set path |

## 15.3 Copy-ready decision, gate, and multimodal configuration skeletons

```markdown
# DEC#### — [Decision Question]
Status: Unresolved / Human Decision Required
UD reference: UD##
Owner / approver / due gate:
Proposal facts and locators (RF##):
Options considered and Q1/clinical tradeoffs:
Recommendation and rejected alternatives:
Actual human decision / date / approval evidence:
Affected entity versions, steps, gates, and claims:
Reassessment trigger and recovery path:
```

```markdown
# G## Assessment — [Entity IDs & Versions]
Initial status: NOT ASSESSED
Assessor / date / named human reviewer:
| Mandatory criterion | Evidence path and SHA-256 | PASS/FAIL | Corrective action |
|---|---|---|---|
Overall outcome: [PASS only if 100% of mandatory criteria evidenced; otherwise FAIL]
Invalidated downstream gates/artifacts:
Reassessment record:
```

```yaml
# Planning template T32 only. Null values prohibit execution.
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
  missing_modality_policy: null
model:
  framework: null              # pytorch | tensorflow (UD13)
  framework_version: null
  architecture_name: null
  modality_encoders:
    clinical: null
    ecg: null
    laboratory: null
    lifestyle: null
  fusion_module: null          # e.g., cross_modal_transformer_fusion
  pretrained_weights_sha256: null
  license_record: null
training:
  seed: null
  deterministic_mode: null
  epochs_or_budget: null
  batch_size: null
  optimizer_and_schedule: null
  loss_and_imbalance_policy: null
  regularization: null
  early_stopping_monitor: null
evaluation_and_calibration:
  protocol_sha256: null
  validation_only_tuning: true
  calibration_candidate: null
  threshold_rule: null
  mandatory_metrics: [accuracy, precision, recall, f1, roc_auc, confusion_matrix]
  adopted_q1_metrics: null
xai_hooks:
  explainer_type: null
  background_partition: train  # NEVER validation or test
runtime:
  environment_lock_sha256: null
  hardware_record: null
checkpoint_policy: null
artifact_destination: null
```

Expand `T32` to the exact resolved hyperparameter schema of the chosen framework and baseline/Transformer implementation at `STEP-025–026`.

<a id="appendix-a"></a>
# Appendix A. Canonical definitions

## A.1 Identifiers and naming

Assign stable, zero-padded IDs serially. Never recycle an ID; supersede or retire obsolete entities with explicit links. `STEP-001`–`STEP-050`, `S01`–`S17`, `G01`–`G17`, `UD01`–`UD26`, `RF01`–`RF18`, `PG1`–`PG5`, and `T01`–`T32` are defined at planning time.

| Entity | ID pattern | Canonical record |
|---|---|---|
| Paper / screening record | `P####` / `SCR####` | Papers / Screening registries |
| Research gap / claim | `GAP####` / `CLAIM####` | Gaps / Claims registries |
| Decision / risk | `DEC####` / `RISK####` | Decisions / Risk registries |
| Clinical site / cohort dataset | `SITE####` / `DS####` | Sites / Datasets registries |
| Pseudonymous patient / encounter | `PAT########` / `ENC########` | Restricted cohort linkage & analytical manifests |
| Variable / adjudication release / batch | `VAR####` / `ADJ####` / `ADJB####` | Variable dictionary; Adjudication registry & batch logs |
| Split / preprocessing / prepared release | `SPLIT####` / `PP####` / `REL####` | Split manifests; Preprocessing & Releases registries |
| Model candidate / trained model | `MC####` / `MODEL####` | Model Candidates / Model registries |
| Experiment / run attempt / checkpoint | `EXP####` / `RUN####` / `CKPT####` | Experiment Registry; per-EXP run manifest; Checkpoint Registry |
| Evaluation / XAI audit | `EVAL####` / `XAI####` | Evaluation / XAI registries |
| Figure / table / writing unit | `FIG####` / `TAB####` / `WR####` | Assets / Writing registries |
| Archived release | `ARCH####` | Archive manifest |

Use `snake_case` for general filenames; keep ID prefixes uppercase. Never place patient names, MRNs, phone numbers, or national IDs in filenames or analytical CSVs. Use ISO 8601 timestamps with timezone and SHA-256 for all checksums. Units (mg/dL, mmol/L, mmHg, mV, Hz, ms, beats/min) must be explicit in schemas and figure axes.

## A.2 Versioning and immutability

Use `vMAJOR.MINOR.PATCH` for documents, schemas, and code. Scientific entities (`DS`, `ADJ`, `SPLIT`, `PP`, `REL`, `EXP`, `CKPT`, `MODEL`, `EVAL`, `XAI`) are immutable once frozen: any scientifically material alteration creates a new versioned ID linked to its parent and triggers reassessment of downstream gates. Preserve failed, diverged, and inferior runs permanently.

## A.3 Universal Definition of Done (DoD)

A step is **Done** only when: (1) its objective and specified outputs exist; (2) all inputs, parent hashes, and execution procedures are logged; (3) verification checklists pass with recorded evidence; (4) applicable quality gates are current `PASS`; (5) required human decisions (`DEC####`) are documented; (6) owning registries and documentation are updated; (7) permitted files are cleanly committed to Git and restricted/binary artifacts are durably backed up with SHA-256 verification; and (8) another researcher can pick up the exact handoff. `STEP-001` may store initial scope/decision records prior to full repository creation, which `STEP-002` brings under version control.

## A.4 Registry conventions

All registries use UTF-8 CSV with one header row, standard quoting, semicolon-delimited multi-ID cells, and six appended common governance fields: `Owner,Version,Status,Created,Updated,EvidencePath`. Zero (`0`) means a measured numeric zero—never use `0` to encode missing data, `not reported`, `unknown`, or `Unresolved / Human Decision Required`. Initialize registries header-only (except evidenced `STEP-001` decisions and `RF` provenance); never insert placeholder or fabricated scientific rows.

<a id="appendix-b"></a>
# Appendix B. Registry catalog and schemas

Append the six common fields (`Owner,Version,Status,Created,Updated,EvidencePath`) once to every schema below. These are the sole canonical paths referenced identically by the companion blueprint.

| Registry / canonical path | Key / owner | Required domain columns beyond key and common fields |
|---|---|---|
| Decisions — `01_Project_Management/decisions.csv` | `DEC` / research lead | `UD,Question,Decision,Approver,ApprovalDate,BlocksStep,OptionsEvidence,Supersedes,AffectedGates` |
| Risks — `01_Project_Management/risk_register.csv` | `RISK` / research lead | `Description,Category,Trigger,Probability,Impact,Mitigation,Contingency,ReviewDate` |
| Gates — `01_Project_Management/gates.csv` | `AssessmentID` / reviewer | `GateID,DocumentOrEntityScope,EntityVersions,Outcome,CriteriaReport,Assessor,HumanApprover,AssessmentDate,Supersedes,Invalidates` |
| Papers — `02_Literature/papers.csv` | `P` / literature lead | `Title,Authors,Year,Venue,DOI,PMID,SourceURL,Access,FullTextPath,MetadataVerified,ReadingStatus,CohortCountry,SampleSize,Modalities,ECGFormat,EndpointHorizon,FusionModel,XAIUsed,XAIEvaluated,PROBASTRisk,CitationKey` |
| Screening — `02_Literature/screening.csv` | `SCR` / literature lead | `PaperID,SearchRecord,Stage,RelevanceGroup,Decision,ExclusionReason,Reviewer,ConflictResolution,DuplicateOf` |
| Research Gaps — `02_Literature/gaps.csv` | `GAP` / literature lead | `ProposalGap,Statement,SupportingPapers,ContradictingPapers,SearchCoverage,SharpenedQ1Framing,Feasibility,ApprovedRQ,DecisionRecord` |
| Claims — `02_Literature/claims.csv` | `CLAIM` / writing lead | `Statement,Scope,PaperIDs,SourceLocators,ExperimentIDs,EvaluationIDs,XAIIDs,AssetIDs,Contradictions,Uncertainty,Verification,WritingIDs` |
| Clinical Sites & External Sources — `03_Datasets_Cohort/sites.csv` | `SITE` / data steward | `Name,SourceType,Country,RecruitmentMode,IRBApprovalID,PermissionRecord,ConsentOrWaiver,ModalitiesAvailable,ECGFormat,EstimatedN,SelectionDecision` |
| Cohorts / Datasets — `03_Datasets_Cohort/datasets.csv` | `DS` / data steward | `SiteIDs,SourceVersion,IRBRecord,DUARecord,ManifestHash,PatientCount,EncounterCount,EventCount,Prevalence,Complete4ModalityCount,ECGQualityPassCount,CardPath,RestrictedLocation` |
| Prepared Releases — `03_Datasets_Cohort/releases.csv` | `REL` / data lead | `DatasetID,AdjudicationID,VariablesHash,SplitID,PreprocessingID,FitStateHash,ManifestHash,PatientCount,EncounterCount,EventCount,ModalitiesIncluded,RestrictedLocation,ParentRelease,ChangeReason` |
| Variables Dictionary — `04_Outcome_Schema_QA/variables.csv` | `VAR` / clinical schema lead | `Modality,VariableName,DataType,Unit,ValidRange,CodingMap,Instrument,TimingRelativeToIndex,IncorporationBiasRisk,MissingPolicy,PROBASTNotes,Approver` |
| Adjudication Releases — `04_Outcome_Schema_QA/adjudication_registry.csv` | `ADJ` / clinical schema lead | `DatasetID,EndpointCharterVersion,VariablesHash,ECGContractVersion,BatchIDs,Abstractors,CardiologistReviewer,PilotKappa,PilotICC,AdjudicatedCount,UncertainExcludedCount,NativeHash,VerifiedHash,QAReport,ParentVersion` |
| Preprocessing & Fit States — `05_Preprocessing_Alignment/preprocessing_registry.csv` | `PP` / implementer | `InputManifest,RecordLocalOps,TrainFittedOps,ECGFilterSpec,ECGMorphologyApprover,ImputationRule,MissingMaskPolicy,ConfigPath,ConfigHash,FitPartition,FitStateHash,CodeRevision,LeakageTestReport,OutputManifest` |
| Model Candidates — `06_Models_Fusion/candidates.csv` | `MC` / model lead | `Tier,ModelFamily,Framework,FrameworkVersion,Architecture,ModalityInputs,PretrainedOrigin,License,ComputeFeasibility,MissingModalitySupport,Limitations,SelectionDecision` |
| Models — `06_Models_Fusion/model_registry.csv` | `MODEL` / model lead | `CandidateID,Tier,ExperimentID,RunID,CheckpointID,ReleaseID,VariablesHash,PreprocessingID,FitStateHash,ParamCount,CalibratorHash,ThresholdVal,ArtifactLocation,CardPath,EvaluationIDs,XAIIDs,IntendedUse` |
| Experiments — `07_Experiments/experiment_registry.csv` | `EXP` / experiment lead | `RQ,ComparisonBlock,Tier,ParentBaselineEXP,ActiveModalities,ReleaseID,ModelCandidate,ConfigPath,ConfigHash,SourceCommit,Seed,RunIDs,Start,End,StoppingReason,ValROCAUC,ValPRAUC,ValBrier,FailureReport,Conclusion` |
| Checkpoints — `08_Checkpoints/checkpoint_registry.csv` | `CKPT` / experiment lead | `ExperimentID,RunID,EpochStep,Role,StateComponents,ConfigHash,ModelHash,ArtifactPath,SHA256,Bytes,BackupPath,RestoreEvidence` |
| Evaluations — `09_Evaluation_Stats/evaluation_registry.csv` | `EVAL` / evaluation lead | `ExperimentID,ModelID,CheckpointID,ReleaseID,Partition,ProtocolHash,FreezeRecord,CalibratorHash,ThresholdUsed,PredictionHash,MetricPath,CalibrationPath,DCAPath,StatsPath,SubgroupPath,ErrorPROBASTPath,ReportPath,Deviations,ParentEvaluation` |
| XAI Audits — `10_Explainability_XAI/xai_registry.csv` | `XAI` / XAI lead | `ModelID,EvaluationID,ReleaseID,ExplainerType,BackgroundPartition,BackgroundHash,AdditivityError,DeletionAOPC,InsertionAOPC,RandomControlAOPC,LOMOConcordance,SeedStabilityRho,ShortcutAuditOutcome,ClinicianReviewPath,ReportPath` |
| Assets — `11_Figures_Tables/assets.csv` | `FIG` or `TAB` / analyst | `Kind,SourceIDs,DataHash,SpecPath,GeneratorCommand,CodeRevision,OutputPath,ResolutionFormat,Caption,Units,PHICheck,VisualReview,WritingIDs` |
| Writing — `12_Writing/writing_registry.csv` | `WR` / author | `Document,Section,Topic,ClaimIDs,PaperIDs,EvaluationIDs,XAIIDs,AssetIDs,TRIPODItems,DraftPath,Reviewer,ReviewState,Revision,MissingEvidence` |
| Archive — `16_Archive/archive_manifest.csv` | `ArchiveItemID` / release owner | `ArchiveID,ReleaseTag,ItemType,SourcePath,StoredLocation,Version,SHA256,Bytes,PHISensitivity,License,Retention,RestoreEvidence,SubmissionReceipt` |

Subordinate manifests (not competing master registries):
- `03_Datasets_Cohort/splits/SPLIT####/manifest.csv`: `EncounterID,PatientID,SiteID,Partition,OuterFold,OutcomeStratum,SourceHash,AssignmentReason` (restricted analytical tier).
- `07_Experiments/EXP####/run_manifest.json`: per-attempt `RUN####`, start/end timestamps, hardware, resume checkpoint, effective defaults, exit status, and log hashes.

Foreign-key traceability rules: every `REL` resolves `DS`/`ADJ`/`SPLIT`/`PP`/`variables.csv`; every `EXP` resolves `REL`/`MC`/config/commit; every `MODEL` resolves `EXP`/`CKPT`/`REL`/`PP`; every `EVAL` resolves `MODEL`/`REL`/protocol/freeze; every `XAI` resolves `MODEL`/`EVAL`/training-background; every `FIG`/`TAB` resolves source hashes; every empirical `CLAIM` resolves `EVAL` or `XAI`; every `WR` resolves `CLAIM` and `TRIPODItems`. Any unresolved foreign key fails verification.

<a id="appendix-c"></a>
# Appendix C. Stage map and dependency chain

This 17-stage, 50-step, 17-gate map is canonical. The [companion blueprint](./CVD_MULTIMODAL_PROJECT_EXECUTION_BLUEPRINT.md#stage-map) mirrors it verbatim for navigation.

| Stage | Steps | Governing handbook sections | Exit gate(s) |
|---|---|---|---|
| S01 Foundation and unresolved-decision charter | 001 | §1, §12 | G01 |
| S02 Repository, PHI storage policy, templates and minimal tooling | 002–003 | §2, §11, §15, A–B | G02 |
| S03 Zero-seed systematic literature search, screening and extraction | 004–007 | §3 | Feeds G03 |
| S04 Proposal-gap verification (`PG1–PG5`) and Q1 RQ approval | 008–009 | §1, §3 | G03 |
| S05 Ethics/IRB, hospital acquisition, external cohort screening and intake | 010–012 | §4, §11 | IRB before intake; feeds G04 |
| S06 Four-modality quality, ECG signal integrity and cohort approval | 013 | §4 | G04 |
| S07 Clinical endpoint ontology, 4-modality schema and QA protocol | 014–015 | §5 | G05 |
| S08 Pilot abstraction, clinical adjudication and cohort-label QA | 016–018 | §5 | G06 |
| S09 Leakage-safe splitting, modality preprocessing and prepared release | 019–022 | §4 | G07 (020), G08 (022) |
| S10 Framework/architecture selection, runtime lock and pipeline readiness | 023–027 | §6, §7, §8, §11 | G09 |
| S11 Controlled Q1 experiments, unimodal/fusion baselines and ablations | 028–031 | §6 | G10 per qualifying EXP |
| S12 Validation-only selection, calibration fit and final-test freeze | 032–033 | §7 | G11 (032) before test |
| S13 Final discrimination, calibration, statistical inference and DCA | 034–036 | §7 | G12 |
| S14 Subgroup fairness, missing-modality robustness, errors and PROBAST-AI | 037 | §7 | G13 |
| S15 Multimodal XAI (SHAP), quantitative faithfulness, stability and clinical review | 038–040 | §8 | G14 |
| S16 Research prototype, optional defense demo and reproducibility audit | 041–042 | §9, §11 | G15 |
| S17 FYDP thesis, Q1 journal manuscript (TRIPOD+AI), archive and completion | 043–050 | §10, §11, §14 | G16 (thesis 046; paper 048), G17 (050) |

```text
001/G01 → 002–003/G02 → 004–009/G03
→ 010–011(IRB) → 012–013/G04 → 014–015/G05 → 016–018/G06
→ 019(design) → 020/G07(split & seal) → 021(train-only fit) → 022/G08(REL)
→ 023–027/G09 → [028 → 029 → 030/G10] → 031(full Tier 1–4 + LOMO/progressive/multi-seed loop)
→ 032/G11(val-only selection, calibrator, threshold freeze) → 033(frozen test inference)
→ [034 metrics+calibration + 035 DeLong/bootstrap/DCA] → 036/G12
→ 037/G13(subgroups, missing-modality, error & PROBAST-AI)
→ 038(SHAP) → 039(faithfulness+stability) → 040/G14(shortcut+cardiologist review)
→ 041(prototype [+ optional UD22 demo]) → 042/G15(clean reproducibility audit)
→ 043–046/G16(thesis) → 047(thesis submission)
→ 048(Q1 manuscript + TRIPOD+AI + G16(paper) + submission/rebuttal OR approved disposition)
→ 049(tiered immutable archive & restore) → 050/G17(project completion)
```

Limited parallelism is permitted only where explicitly stated in a blueprint step and never crosses an unmet/stale gate. Corrections return to the earliest invalid parent step with new IDs and reassess downstream gates.

<a id="appendix-d"></a>
# Appendix D. Glossary

- **Cardiovascular disease (CVD):** Spectrum of heart and blood-vessel disorders defined operationally by exact ICD-10/clinical criteria in `endpoint_charter.md` (`UD02`).
- **Index time ($t_0$):** The exact clinical reference timestamp at which risk prediction is made; all predictors must originate at or before $t_0$ (within $\Delta t$) to prevent post-diagnosis leakage.
- **Incorporation bias:** Bias occurring when a predictor (e.g., ECG or troponin) was itself used to establish the reference outcome label, artificially inflating apparent model accuracy.
- **Spectrum bias:** Bias arising when recruited positive and negative cases represent unrepresentative clinical extremes (e.g., acute CCU patients vs healthy young volunteers) rather than the intended target screening population.
- **Events Per Variable (EPV):** Ratio of outcome events to model predictor degrees of freedom; critical for controlling overfitting in clinical prediction models.
- **Missing Not At Random (MNAR):** Missingness whose probability depends on unobserved clinical state or clinician suspicion (e.g., labs/ECGs ordered selectively for symptomatic patients).
- **Patient-level leakage:** Splitting multiple visits/ECGs of the same patient across train and test, or fitting scalers/imputers/encoders/SMOTE prior to splitting.
- **Multimodal fusion:** Combining heterogeneous representations (here Clinical, ECG, Laboratory, Lifestyle) via early concatenation, late ensembling, gated fusion, or cross-modal Transformer attention.
- **Calibration (Brier, ECE, Slope/Intercept):** Agreement between predicted probabilities and true observed outcome frequencies; distinct from rank discrimination (ROC-AUC).
- **Decision Curve Analysis (DCA):** Evaluation of clinical Net Benefit across risk decision thresholds compared to default treat-all and treat-none strategies.
- **DeLong's test:** Nonparametric test comparing two correlated ROC-AUCs evaluated on the exact same patient cohort.
- **SHAP (SHapley Additive exPlanations):** Game-theoretic attribution decomposing a prediction into additive feature/modality contributions relative to a background distribution; explains model behavior, NOT biological causality.
- **XAI Faithfulness (AOPC / Deletion-Insertion):** Objective measurement of whether perturbing top-attributed features/ECG segments degrades model predictions significantly faster than random perturbations.
- **Spurious shortcut:** Predictive reliance on non-clinical artifacts (site ID, missingness flags, ECG powerline noise, post-diagnosis medication) rather than true cardiovascular pathophysiology.
- **TRIPOD+AI (2024):** International Q1 reporting standard for multivariable clinical prediction models using machine learning/AI.
- **PROBAST / PROBAST-AI:** Structured tool assessing risk of bias across Participants, Predictors, Outcome, and Analysis in clinical prediction studies.

<a id="appendix-e"></a>
# Appendix E. Acronyms

| Acronym | Meaning |
|---|---|
| CVD | Cardiovascular Disease |
| ECG | Electrocardiogram |
| XAI | Explainable Artificial Intelligence |
| SHAP | SHapley Additive exPlanations |
| LIME | Local Interpretable Model-agnostic Explanations |
| FYDP | Final Year Design Project |
| IRB | Institutional Review Board |
| PHI | Protected Health Information |
| CRF | Case Report Form |
| EHR | Electronic Health Record |
| EPV | Events Per Variable |
| MNAR / MAR | Missing Not At Random / Missing At Random |
| ROC-AUC / AUROC | Area Under the Receiver Operating Characteristic Curve |
| PR-AUC / AUPRC | Area Under the Precision-Recall Curve |
| PPV / NPV | Positive Predictive Value / Negative Predictive Value |
| ECE | Expected Calibration Error |
| DCA | Decision Curve Analysis |
| AOPC | Area Over the Perturbation Curve |
| LOMO | Leave-One-Modality-Out |
| GBDT | Gradient Boosted Decision Trees (XGBoost, LightGBM, CatBoost) |
| CNN / LSTM | Convolutional Neural Network / Long Short-Term Memory |
| ICC | Intraclass Correlation Coefficient |
| CI / FDR | Confidence Interval / False Discovery Rate |
| TRIPOD+AI | Transparent Reporting of a multivariable prediction model for Individual Prognosis Or Diagnosis — AI extension |
| PROBAST-AI | Prediction model Risk Of Bias ASsessment Tool — AI extension |
| PRISMA | Preferred Reporting Items for Systematic Reviews and Meta-Analyses |
| DUA / MOU | Data Use Agreement / Memorandum of Understanding |
| CLI / API | Command-Line Interface / Application Programming Interface |
| CSV / YAML | Comma-Separated Values / YAML Configuration Format |
| DOI / PMID | Digital Object Identifier / PubMed Identifier |
| OOM / RNG | Out of Memory / Random Number Generator |

<a id="appendix-f"></a>
# Appendix F. Source coverage and self-review

## F.1 Source inspection and cryptographic provenance

The supplied FYDP proposal (`fydp_title_proposal.pdf`) was inspected in full before drafting. All 6 physical pages are scanned CamScanner images with zero embedded text layer; every page was rendered and visually verified in full, including the signed Proposal Approval Form, all proposal sections, the bulleted Gap Analysis, Methodology lists, and the 9-box Workflow Diagram. No temporary extraction files were added to the workspace.

| Physical PDF page | Material visually inspected | Treatment in this handbook |
|---|---|---|
| p.1 | DIU CSE CSE499 Proposal Approval Form; Members Rayan Ahmed (232-15-847) & Mohammad Nafis Sadiq (232-15-895); Summer 2026; Date 09.07.2026; Title verbatim; blank Updated Title; Supervisor Md. Mizanur Rahman (Senior Lecturer, signed 09.07.26) | Cover page; `RF01–RF02`, `RF18`; approval scope strictly bounded (not IRB/hospital permission) |
| p.2 | Section V.1 Objective, V.2 Motivation (including Bangladesh context), start of V.3 Background Study (LR, RF, SVM, XGBoost, CNN, LSTM) | `RF03–RF05`; operationalized into `O1–O4`, Tier 1 baselines, and clinical claim boundaries |
| p.3 | Continuation of V.3 Background Study (Transformers, multimodal learning, SHAP, LIME) & V.4 Gap Analysis (5 bullets `PG1–PG5`); zero citations | `RF05–RF07`; zero-seed systematic review (`§3`); `PG1–PG5` treated strictly as falsifiable hypotheses |
| p.4 | Section V.5 Methodology: Techniques & Tools (Python, TensorFlow/PyTorch, Scikit-learn, Pandas, NumPy, Matplotlib, SHAP, Transformer-based Multimodal Fusion Network); Data Collection (primary hospital/diagnostic data post-ethical approval, 4 modalities with example variables); Data Analysis (separate modality feature extraction, multimodal fusion, 6 required metrics) | `RF08–RF12`; `UD04–UD14`; mandatory 6-metric contract + Q1 extensions cleanly distinguished |
| p.5 | SHAP analysis sentence and 9-box Figure: Workflow Diagram | `RF13–RF14`; explicit leakage-prevention reconciliation separating record-local cleaning from post-split fitted preprocessing/feature extraction (`§4.4–4.5`) |
| p.6 | Section V.6 Expected Outcomes & V.7 Conclusion | `RF15–RF16`; hypothesis-testing framing and strict prohibition on unproven clinical/trust claims |

Recorded SHA-256 checksum of the primary scientific source (verified 2026-11-20):

```text
fydp_title_proposal.pdf
BA7DD0EF21C8A2CA77B2E1BAFC2AC5A0E1FEC584E221C848085A971EAACEEFA8
```

## F.2 Planning-document self-review

Review scope: consistency, source fidelity, Q1 methodological soundness, zero cross-project topic contamination, and alignment between this handbook and the companion execution blueprint. This review does **not** constitute `G01–G17` research execution evidence.

| Verification check | Planning disposition |
|---|---|
| Verbatim approved title & institutional metadata | Preserved verbatim (`RF01–RF02`) |
| Epistemic separation (`PROPOSAL FACT` vs `PLANNING RECOMMENDATION` vs `UD##`) | Enforced via `RF01–RF18`, explicit Q1 recommendation labels, and `UD01–UD26` |
| Zero-bibliography proposal addressed | Zero-seed PRISMA-aligned systematic literature workflow (`§3`, `STEP-004–009`) |
| Workflow Diagram leakage trap resolved | Record-local pre-split operations strictly separated from post-split training-only fits (`§4.4–4.5`, `G07–G08`) |
| Four-modality domain specificity | Clinical, ECG waveforms/features, Laboratory assays, and Lifestyle CRFs governed individually and jointly (`§4–§6`) |
| Q1 methodological rigor beyond FYDP minimum | 4-tier comparator baselines, LOMO/progressive ablations, missing-modality tests, calibration (Brier/ECE/slope), DCA, DeLong/bootstrap CIs, subgroup fairness, PROBAST-AI, quantitative SHAP faithfulness (AOPC) & stability, shortcut audit, and TRIPOD+AI compliance |
| Shared canonical architecture | 17 stages (`S01–S17`), 50 steps (`STEP-001–050`), 17 gates (`G01–G17`), 26 UDs (`UD01–UD26`), 32 templates (`T01–T32`), and 22 CSV registries aligned 1:1 with companion blueprint |
| No fabricated data, citations, approvals, or results | All gates begin `NOT ASSESSED`; zero synthetic results or invented references |

**Initial project state:** Two complete Q1-grade planning deliverables; zero research execution claimed. Begin execution at [STEP-001](./CVD_MULTIMODAL_PROJECT_EXECUTION_BLUEPRINT.md#step-001).

*End of CVD Multimodal Research Operating System — v1.0.0.*
