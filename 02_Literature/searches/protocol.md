# PRISMA-Aligned Systematic Literature Search, Screening, and Appraisal Protocol

| Metadata | Value |
|---|---|
| Document | `02_Literature/searches/protocol.md` |
| Protocol Version | v1.0.0 |
| Step | STEP-004 |
| Target Gate | Feeds G03 (Stage S03 / S04) |
| Date | 2026-11-20 |
| Literature Lead | Rayan Ahmed (`232-15-847`) |
| Co-Investigator | Mohammad Nafis Sadiq (`232-15-895`) |
| Supervisor | Md. Mizanur Rahman (Senior Lecturer, Dept. of CSE, DIU) |
| Status | Approved Working Protocol |
| Governing Sections | CVD Multimodal Research OS §1.3, §3.1–§3.3; Blueprint STEP-004 |
| PHI Sensitivity | Tier 1 (Public / Git-safe) |

---

## 1. Rationale and Foundational Context

### 1.1 The Zero-Seed Mandate (`RF06`)
The primary scientific proposal document (`fydp_title_proposal.pdf`, SHA-256: `BA7DD0EF21C8A2CA77B2E1BAFC2AC5A0E1FEC584E221C848085A971EAACEEFA8`) contains **zero bibliographic citations** or references. 

To ensure Q1-grade rigor and adhere to international standards (**PRISMA 2020** statement and **TRIPOD+AI 2024** item 3), the literature foundation cannot rely on informal seeds. It must be established through a reproducible, transparent, and multi-database systematic search designed from scratch.

### 1.2 Primary Objective
Identify, screen, extract, and synthesize all peer-reviewed studies and relevant preprints evaluating:
1. Multimodal machine learning combining **12-lead ECG waveforms or intervals** with **tabular clinical, laboratory, and lifestyle data** for cardiovascular disease (CVD) risk prediction.
2. Transformer-based cross-modal attention fusion in clinical cardiology, specifically addressing missing or heterogeneous modalities.
3. Explainable AI (XAI) applications (especially SHAP) in multimodal CVD prediction that evaluate **quantitative faithfulness, ranking stability, probability calibration, and clinical plausibility**.
4. Empirical evidence testing and potentially falsifying proposal gaps `PG1–PG5`.

---

## 2. Eligibility Criteria (PECOS / PICOTS Framework)

| Component | Inclusion Criteria (In-Scope) | Exclusion Criteria (Out-of-Scope) |
|---|---|---|
| **Population ($P$)** | Human adults ($\ge 18$ years) screened, evaluated, or hospitalized for cardiovascular disease (CAD, MI, HF, Arrhythmia, Stroke, Hypertensive CVD, or general CVD risk). | Pediatric cohorts ($< 18$ y), non-human/animal models, cellular/in-vitro assays. |
| **Exposure / Predictors ($E$)** | Multimodal predictor sets combining at least **ECG** (raw digital, digitized paper, or extracted features) with at least one **tabular modality** (clinical vitals/demographics, serum laboratory assays, or lifestyle/behavioral factors). | Studies utilizing only one modality (unless serving as a seminal unimodal baseline); studies utilizing cardiac imaging (echo/MRI/CT) without ECG or tabular data. |
| **Comparator ($C$)** | Unimodal models (ECG-only, tabular-only), classical clinical risk scores (Framingham, SCORE2, ASCVD, QRISK), or standard machine learning baselines (LR, RF, SVM, GBDT). | Studies lacking baseline comparisons or internal validation. |
| **Outcome ($O$)** | Objective CVD event incidence, diagnosis, mortality, or risk classification explicitly defined via clinical criteria or ICD codes. | Non-cardiovascular endpoints; subjective self-reported symptoms without clinical ascertainment. |
| **Study Design ($S$)** | Observational cohorts, electronic health record (EHR) studies, clinical trials, or secondary analyses of open medical databases (e.g., UK Biobank, MIMIC-IV, PTB-XL). | Editorials, commentaries, non-systematic opinion reviews, extended abstracts without numerical data. |
| **Timing & Setting ($T$)** | Publications from **January 1, 2018 to November 20, 2026** (reflecting modern deep multimodal learning era) plus seminal historical risk score papers. | Studies published prior to 2018 unless seminal risk score benchmarks. |
| **Language** | English full-text available. | Non-English publications without verified English translation. |

---

## 3. Exclusion Taxonomy & Screening Codes

Every screened paper excluded at Title/Abstract or Full-Text stage must be assigned an explicit exclusion code in `02_Literature/screening.csv`:

| Code | Reason Description | Example |
|---|---|---|
| **EX-POP** | Ineligible population | Pediatric cohort ($<18$), animal study, or non-human data. |
| **EX-UNIMODAL** | Single modality only | ECG-only classification or EHR-tabular-only model without multimodal fusion comparison. |
| **EX-NO-ECG** | Multimodal without ECG | Combination of clinical + genomic or clinical + imaging without ECG. |
| **EX-IMAGING-ONLY** | Primary imaging focus | Cardiac MRI / CT / Echocardiogram segmentation without primary tabular/ECG early risk focus. |
| **EX-OUTCOME** | Ineligible or subjective outcome | Non-CVD disease (e.g., sepsis, cancer, COVID-19 alone); subjective wellness without CVD endpoint. |
| **EX-NO-EVAL** | Inadequate quantitative evaluation | Conceptual framework, narrative review, or no reported discrimination metrics (ROC-AUC, F1). |
| **EX-LANG** | Non-English text | Foreign language without accessible authoritative English version. |
| **EX-NO-FULLTEXT** | Full text unobtainable | Abstract-only conference poster, broken DOI, or unresolvable institutional request. |
| **EX-DUP** | Duplicate publication | Duplicate record, or preprint completely identical to a later peer-reviewed journal version. |

---

## 4. Relevance Taxonomy (Categorization of Included Studies)

Included studies will be classified into four distinct relevance groups in `02_Literature/screening.csv` and `papers.csv`:

1. **Group 1: Direct Multimodal CVD Comparators (Core SOTA):**
   - Studies predicting CVD using 3 or 4 synchronized modalities (Clinical + ECG + Lab + Lifestyle), or 2 modalities (ECG + Clinical/Lab) using deep fusion or Transformers.
   - Primary target for extraction into `summaries/P####.md`.
2. **Group 2: Methodological / Architectural Comparators:**
   - Studies introducing multimodal Transformer fusion, cross-modal attention, or missing-modality imputation mechanisms in biomedical applications.
3. **Group 3: Multimodal Explainability & Faithfulness Benchmarks:**
   - Studies applying SHAP, Integrated Gradients, or LIME to multimodal healthcare models and quantitatively benchmarking perturbation faithfulness (AOPC), stability, or clinician plausibility.
4. **Group 4: Contextual & Clinical Baseline Benchmarks:**
   - Seminal clinical risk score calculators (Framingham, SCORE2, WHO South Asia charts) and established unimodal ECG/tabular SOTA models.

---

## 5. Multi-Database Search Strategies & Verbatim Query Strings

### Query Concept Formulation:
- **Concept 1: Cardiovascular Disease Target:** CVD, CAD, Myocardial Infarction, Heart Failure, Arrhythmia, Cardiac Risk.
- **Concept 2: Multimodal / Fusion Paradigm:** Multimodal, Multi-modal, Data Fusion, Cross-Modal, Deep Fusion, Hybrid.
- **Concept 3: Electrocardiogram Modality:** ECG, Electrocardiogram, Electrocardiography, 12-lead.
- **Concept 4: Tabular / Auxiliary Modalities:** Clinical, EHR, Electronic Health Record, Laboratory, Biomarker, Lifestyle, Risk Factor.
- **Concept 5: Prediction / Decision Support:** Risk prediction, Early detection, Prognosis, Classification, Screening.

---

### Database 1: PubMed / MEDLINE
**Target:** Biomedical, clinical cardiology, and translational AI literature.  
**Syntax:** MeSH terms and Title/Abstract (`[tiab]`) fields.

```text
(
  "Cardiovascular Diseases"[Mesh] OR "Heart Diseases"[Mesh] OR "Myocardial Infarction"[Mesh] OR 
  "Heart Failure"[Mesh] OR "cardiovascular disease*"[tiab] OR "coronary artery disease*"[tiab] OR 
  "heart disease*"[tiab] OR "CVD"[tiab] OR "myocardial infarction"[tiab] OR "heart failure"[tiab]
)
AND
(
  "Multimodal Learning"[Mesh] OR "multimodal"[tiab] OR "multi-modal"[tiab] OR 
  "data fusion"[tiab] OR "cross-modal"[tiab] OR "feature fusion"[tiab] OR "hybrid deep learning"[tiab]
)
AND
(
  "Electrocardiography"[Mesh] OR "ECG"[tiab] OR "electrocardiogram*"[tiab] OR 
  "electrocardiograph*"[tiab] OR "12-lead"[tiab]
)
AND
(
  "Electronic Health Records"[Mesh] OR "Biomarkers"[Mesh] OR "Life Style"[Mesh] OR 
  "clinical"[tiab] OR "laboratory"[tiab] OR "biomarker*"[tiab] OR "lifestyle"[tiab] OR 
  "EHR"[tiab] OR "vital signs"[tiab]
)
AND
(
  "Risk Assessment"[Mesh] OR "risk prediction"[tiab] OR "early detection"[tiab] OR 
  "screening"[tiab] OR "prognosis"[tiab] OR "diagnosis"[tiab]
)
AND
("2018/01/01"[Date - Publication] : "2026/11/20"[Date - Publication])
AND (English[lang])
```

---

### Database 2: IEEE Xplore Digital Library
**Target:** Biomedical engineering, signal processing, and machine learning architectures (*IEEE JBHI*, *IEEE TBME*, *IEEE Access*).  
**Syntax:** Metadata search.

```text
(
  ("Document Title":"cardiovascular" OR "Abstract":"cardiovascular" OR "Document Title":"heart disease" OR "Abstract":"heart disease" OR "Document Title":"CVD" OR "Abstract":"CVD")
  AND
  ("Document Title":"multimodal" OR "Abstract":"multimodal" OR "Document Title":"multi-modal" OR "Abstract":"multi-modal" OR "Document Title":"fusion" OR "Abstract":"fusion")
  AND
  ("Document Title":"ECG" OR "Abstract":"ECG" OR "Document Title":"electrocardiogram" OR "Abstract":"electrocardiogram")
  AND
  ("Document Title":"clinical" OR "Abstract":"clinical" OR "Document Title":"tabular" OR "Abstract":"tabular" OR "Document Title":"laboratory" OR "Abstract":"laboratory" OR "Document Title":"lifestyle" OR "Abstract":"lifestyle")
  AND
  ("Document Title":"prediction" OR "Abstract":"prediction" OR "Document Title":"detection" OR "Abstract":"detection" OR "Document Title":"risk" OR "Abstract":"risk")
)
```
*Filters: Year $\ge 2018$, Document Type: Journals & Conferences, Language: English.*

---

### Database 3: Scopus (Elsevier)
**Target:** Broad interdisciplinary coverage across medicine, computer science, and engineering (*Computers in Biology and Medicine*, *Artificial Intelligence in Medicine*, *Information Fusion*).  
**Syntax:** Title, Abstract, Keywords (`TITLE-ABS-KEY`).

```text
TITLE-ABS-KEY (
  ("cardiovascular disease" OR "coronary artery disease" OR "heart disease" OR "CVD" OR "myocardial infarction" OR "heart failure")
  AND
  ("multimodal" OR "multi-modal" OR "data fusion" OR "cross-modal" OR "feature fusion" OR "transformer fusion")
  AND
  ("ECG" OR "electrocardiogram" OR "electrocardiography" OR "12-lead")
  AND
  ("clinical" OR "EHR" OR "electronic health record" OR "laboratory" OR "biomarker" OR "lifestyle")
  AND
  ("risk prediction" OR "early detection" OR "screening" OR "prognosis")
)
AND PUBYEAR > 2017
AND LANGUAGE (english)
```

---

### Database 4: ACM Digital Library
**Target:** Applied AI, health informatics, and data mining (KDD, WebConf, CHIL, SAC).

```text
(
  "cardiovascular" OR "heart disease" OR "CVD"
)
AND
(
  "multimodal" OR "multi-modal" OR "cross-modal" OR "fusion"
)
AND
(
  "ECG" OR "electrocardiogram"
)
AND
(
  "clinical" OR "laboratory" OR "lifestyle" OR "EHR"
)
```

---

### Database 5: arXiv / Google Scholar / PhysioNet (Preprint & Open Cohort SOTA)
**Target:** Latest 2024–2026 multimodal Transformer architectures, MIMIC-IV-ECG multimodal benchmarks, and open implementations.

**arXiv Query (API / Search):**
`all:"multimodal" AND all:"ECG" AND all:"cardiovascular" AND (all:"tabular" OR all:"EHR") AND (all:"transformer" OR all:"fusion")`

**Google Scholar Target Strings:**
`"multimodal" "ECG" ("clinical" OR "EHR") ("laboratory" OR "lifestyle") "cardiovascular disease" "risk prediction" "transformer"`

---

## 6. Deduplication and PRISMA Flow Management

1. **Intake & Export:**
   - Raw records exported in standard CSV / BibTeX format and saved in `02_Literature/searches/exports/`.
   - Record search date, query string, engine, filter criteria, and raw retrieved count in `02_Literature/searches/`.
2. **Deterministic Deduplication Hierarchy:**
   - **Step 1:** Exact match on Digital Object Identifier (DOI).
   - **Step 2:** Exact match on PubMed ID (PMID).
   - **Step 3:** Normalized title match (lowercased, stripped of punctuation and whitespace) + Author surname + Publication year.
   - **Step 4:** Preprint-to-peer-reviewed version resolution (if an arXiv/bioRxiv preprint was later published in a journal, the journal DOI is preserved, preprint ID linked in notes).
3. **Registration:**
   - Deduplicated unique studies are assigned permanent `P####` IDs in `02_Literature/papers.csv`.
   - Screening decisions recorded in `02_Literature/screening.csv`.

---

## 7. PROBAST-Informed Methodological Extraction Rubric

For every included Group 1 and Group 2 study, extraction into `summaries/P####.md` (`T05`) must record:

| Section | Mandatory Extraction Fields | Methodological Trap / Audit Check |
|---|---|---|
| **Bibliographic** | `PaperID`, Title, Authors, Year, Venue, DOI, Source URL. | 100% verified against publisher landing page. |
| **Cohort & Population** | Country, clinical setting (inpatient vs outpatient), total $N$, encounter count, CVD event count, event prevalence, demographic breakdown (age, sex, ethnicity). | Check for spectrum bias (e.g., extreme CCU cases vs young healthy controls). |
| **Endpoint & Horizon** | CVD definition, ascertainment criteria (ICD-10 vs clinical diagnosis), prediction horizon (in-hospital, 1-year, 5-year, cross-sectional early risk). | Check for outcome-horizon mismatch or unclear index time $t_0$. |
| **Modality Specs** | Modalities included: Clinical, ECG format (12-lead digital raw vs intervals vs paper), Lab assays, Lifestyle indicators. | Check if lifestyle is actually modeled or just mentioned in passing. |
| **Missing Modalities** | Handling of incomplete patient visits: complete-case exclusion vs imputation vs mask token. | Document missing rate per modality. |
| **Data Splitting & Leakage** | Split level (patient-level vs record-level), Train/Val/Test ratios, cross-validation scheme. | **CRITICAL AUDIT:** Were scalers, imputers, or feature selectors fit before splitting? |
| **Model Architectures** | Baseline models compared (LR, RF, SVM, XGBoost, CNN, LSTM); multimodal fusion architecture (Early, Late, Gated, Cross-Attention Transformer). | Verify if multimodal model is compared against strong tuned unimodal baselines. |
| **Metrics & Performance** | Accuracy, Precision, Recall, F1, ROC-AUC (with 95% CI), PR-AUC, Brier score, Calibration slope/ECE, Decision Curve Analysis. | Write `not reported` for missing metrics; never guess. |
| **Statistical Rigor** | Statistical significance testing (DeLong test, paired bootstrap, McNemar) comparing multimodal vs baselines. | Note if multimodal "superiority" was tested for significance or just nominal gain. |
| **Explainability (XAI)** | XAI method used (SHAP, LIME, Attention weights); whether quantitative faithfulness (AOPC) or clinician review was evaluated. | Flag decorative SHAP (plots shown without faithfulness or clinical plausibility checks). |
| **PROBAST-AI Rating** | Overall Risk of Bias rating: Low, High, or Unclear across Participants, Predictors, Outcome, Analysis. | High risk of bias if pre-split fitting or patient-overlap leakage detected. |
