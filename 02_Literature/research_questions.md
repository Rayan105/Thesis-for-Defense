# Provisional Research Questions & Falsifiable Hypotheses

| Metadata | Value |
|---|---|
| Document | `02_Literature/research_questions.md` |
| Version | v0.1.0 (Provisional Draft) |
| Step | STEP-004 |
| Formal Ratification Milestone | STEP-009 (`G03` Exit Gate) |
| Authors | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Supervisor | Md. Mizanur Rahman (Senior Lecturer, Dept. of CSE, DIU) |
| Status | Provisional Working Draft (Awaiting Systematic Literature Synthesis) |
| Governing Sections | CVD Multimodal Research OS §1.4, §3.3; Blueprint STEP-004, STEP-008, STEP-009 |
| PHI Sensitivity | Tier 1 (Public / Git-safe) |

---

## 1. Context and Grounding

These four candidate Research Questions (`RQ1–RQ4`) operationalize the approved project mandate and test the proposal's five research gaps (`PG1–PG5`, p.3). 

> [!IMPORTANT]
> **Falsification-Oriented Design:** None of these questions presupposes a positive or superior outcome. Null, negative, or modest findings (e.g., if a well-tuned tabular GBDT baseline matches a complex multimodal Transformer, or if lifestyle factors contribute only marginal incremental gain) constitute **fully valid Q1 scientific contributions** when rigorously executed, calibrated, and honestly reported.

---

## 2. Research Questions Matrix

### RQ1: Multimodal Synergy & Discriminative Superiority
- **Question Formulation:** Does fusing four heterogeneous data modalities (Clinical, 12-lead ECG waveforms/intervals, Laboratory assays, and Lifestyle behaviors) through a Transformer-based cross-modal attention network yield statistically significant improvements in discrimination ($\text{ROC-AUC}$, $\text{PR-AUC}$, and $\text{F1-score}$) on a held-out clinical cohort compared to:
  1. Unimodal models trained on individual data modalities?
  2. Classical clinical cardiovascular risk calculators (Framingham, SCORE2)?
  3. Optimized tree-based tabular baselines (XGBoost, CatBoost, Random Forest) trained on early-concatenated features?
- **Governing Objectives:** `O1` (Multimodal Feature Extraction), `O2` (Multimodal Fusion Modeling).
- **Addressed Proposal Gaps:** `PG1` (Unimodal dominance), `PG2` (Two-modality limit), `PG5` (Explainable multimodal frameworks).
- **Primary Statistical Tests:** Paired DeLong's test for correlated ROC-AUCs ($p < 0.05$), paired bootstrap difference testing with BCa 95% confidence intervals, and false discovery rate (FDR) multiplicity adjustments.

---

### RQ2: Incremental Value of the Lifestyle Modality
- **Question Formulation:** What is the quantified incremental predictive and clinical utility of incorporating patient lifestyle/behavioral factors (diet score, physical activity level, smoking pack-years) alongside standardized clinical vitals, laboratory tests, and ECG signals in early CVD risk prediction?
- **Governing Objectives:** `O2` (Multimodal Fusion), `O3` (Quantitative Evaluation).
- **Addressed Proposal Gaps:** `PG4` (Lifestyle data omitted in prior CVD models).
- **Hypothesis Framing:** 
  - $H_0$: Adding lifestyle factors yields no statistically significant increase in held-out discriminative performance or clinical Net Benefit ($\Delta\text{ROC-AUC} \le 0$, $\Delta\text{Net Benefit} \le 0$).
  - $H_1$: Adding lifestyle factors provides a statistically significant, non-zero incremental gain in discrimination or calibration.
- **Evaluation Methodology:** Controlled Leave-One-Modality-Out (LOMO) ablation experiments comparing $4\text{-modality}$ vs $3\text{-modality}$ (excluding lifestyle) models on identical patient partitions.

---

### RQ3: Quantitative XAI Faithfulness, Stability & Clinical Plausibility
- **Question Formulation:** Are multimodal game-theoretic SHAP attributions generated for the deep fusion network:
  1. Mathematically faithful to the model's true internal decision logic under progressive perturbation (measured via Area Over the Perturbation Curve [AOPC] for deletion and insertion compared to random controls)?
  2. Stable across independently initialized training seeds (measured via Spearman rank correlation $\rho$ and top-$k$ Jaccard overlap)?
  3. Concordant with established cardiovascular pathophysiology and clinically intelligible under structured cardiologist review?
- **Governing Objectives:** `O4` (Explainable AI via SHAP).
- **Addressed Proposal Gaps:** `PG3` (Lack of explainability), `PG5` (Explainable multimodal framework).
- **Clinical Safety Boundary:** Interpretations explain model predictive behavior; they do not infer biological causality or autonomous diagnostic certainty.

---

### RQ4: Subgroup Fairness, Calibration & Missing-Modality Robustness
- **Question Formulation:** How consistent are discrimination ($\text{ROC-AUC}$), probability calibration (Brier score, Expected Calibration Error [ECE], calibration slope/intercept), and clinical Net Benefit (Decision Curve Analysis [DCA]) across:
  1. Demographic subgroups (biological sex: male vs female; age strata: $<50$, $50-65$, $>65$)?
  2. Missing-modality scenarios (where patients lack either ECG waveforms, specific lab tests, or lifestyle responses)?
- **Governing Objectives:** `O3` (Evaluation, Calibration & Fairness).
- **Addressed Proposal Gaps:** Methodological robustness for real-world hospital deployment.
- **Evaluation Methodology:** Subgroup-stratified evaluation tables, missing-modality degradation stress tests, and formal PROBAST-AI risk of bias self-audit.

---

## 3. Mapping from Proposal Gaps to Experiments and Targets

| Proposal Gap | Operational Identifier | Target Research Question | Experimental Milestone | Primary Metric / Proof |
|---|---|---|---|---|
| Most studies use only one healthcare data type | `PG1` $\rightarrow$ `GAP0001` | **RQ1** | Stage S11 (`STEP-028`–`031`) | Multi-tier comparison table; DeLong $p < 0.05$ |
| Existing multimodal systems combine only two sources | `PG2` $\rightarrow$ `GAP0002` | **RQ1**, **RQ2** | Stage S11 (`STEP-031`) | Full 4-modality matrix vs 2-modality pairings |
| Many AI models do not explain their predictions | `PG3` $\rightarrow$ `GAP0003` | **RQ3** | Stage S15 (`STEP-038`–`040`) | Deletion/Insertion AOPC curves vs random; cardiologist rubric |
| Lifestyle information is often ignored | `PG4` $\rightarrow$ `GAP0004` | **RQ2** | Stage S11 (`STEP-031`), S13 | LOMO $\Delta\text{ROC-AUC}$, $\Delta\text{Brier}$, Decision Curve Analysis |
| Few studies build an explainable multimodal framework | `PG5` $\rightarrow$ `GAP0005` | **RQ1–RQ4** | Stages S11–S17 | End-to-end framework, reproducible prototype, Q1 manuscript |

---

## 4. Next Actions
- Execute multi-database systematic searches in `STEP-005`.
- Screen and extract direct vs contextual studies in `STEP-006` and `STEP-007`.
- Synthesize evidence against `PG1–PG5` in `STEP-008` and formally freeze these Research Questions at `STEP-009` (`G03`).
