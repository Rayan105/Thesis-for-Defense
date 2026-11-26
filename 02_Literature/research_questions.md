# Q1-Aligned Research Questions & Traceability Matrix (`STEP-009` / `G03` Candidate Final)

| Metadata | Value |
|---|---|
| Document | `02_Literature/research_questions.md` |
| Version | v1.0.0 (`Candidate Final — Pending Supervisor G03 Sign-Off`) |
| Supersedes | v0.1.0 (`STEP-004` Provisional Draft) |
| Step | STEP-009 (`Stage S04`) |
| Target Gate | **`G03`** (`Systematic Literature & Q1 RQs`; Human Approver: Md. Mizanur Rahman) |
| Authors | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Supervisor | Md. Mizanur Rahman (Senior Lecturer, Dept. of CSE, DIU) |
| Initial Search Cutoff Date | **`2026-11-25`** (`SEARCH-SCHOLAR-20261125`: `5` queries, `83` full-text screened $\rightarrow$ `42` extracted) |
| Mandatory Living-Review Updates | Prior to `STEP-023` (Modeling Lock) and prior to `STEP-048` (Q1 Manuscript Submission) |
| Linked Decision Record | [DEC0002](../01_Project_Management/decision_log/DEC0002.md) |
| Governing Sections | OS §1.3, §1.4, §3.3, §3.4, §6–§8, §14.2 (`G03`); Blueprint `STEP-009` |
| PHI Sensitivity | Tier 1 (Public / Git-safe) |

---

## 1. Context, Literature Grounding, and Epistemic Mandate

This document locks the operational Research Questions (`RQ0` Primary + `RQ1–RQ4` Subordinate) grounded in the zero-seed PRISMA review (`protocol.md`, `SEARCH_SCHOLAR_2026-11-25.md`, `screening_summary.md`), verified full-text extraction of all `42` included studies (`P0001–P0042`, `100%` `MetadataVerified=yes`), systematic gap testing (`GAP0001–GAP0005`), and cross-study synthesis (`synthesis.md`).

All five proposal research gaps (`PG1–PG5`) were tested rigorously against contradicting literature:
- **`PG1` (`GAP0001`)** & **`PG2` (`GAP0002`)** were **narrowed**: `14/29` original studies combine $\ge 3$ streams (`P0002, P0013, P0016, P0020–P0023, P0025, P0030–P0032, P0036–P0038`), so broad *"unimodal only"* or *"max 2 modalities"* statements are falsified. The verified gap is the **absence of leakage-free cross-modal Transformer fusion integrating the 4 accessible non-imaging screening modalities (`Clinical + 12-lead ECG waveforms + Laboratory assays + Structured Lifestyle`)**.
- **`PG3` (`GAP0003`)**, **`PG4` (`GAP0004`)**, & **`PG5` (`GAP0005`)** were **supported-within-search**: while `17/29` plot qualitative XAI and `4/42` (`P0028, P0029, P0032, P0038`) run partial or CMR/text clinical XAI audits, `0/42` combines multimodal SHAP deletion/insertion AOPC vs random controls, multi-seed rank stability, shortcut auditing, and blinded cardiologist plausibility on `C+E+L+S` data; `0/29` quantifies structured lifestyle incremental Net Benefit via LOMO ablation; and `0/29` validates an end-to-end leakage-free 4-modality pipeline on a Bangladeshi/South Asian clinical cohort.

> [!IMPORTANT]
> **Null / Negative Findings Policy (`STEP-009` Mandatory Contract, OS §1.4 & §14.1):**
> Every RQ is formulated as a **falsifiable hypothesis**. Null, neutral, or negative findings — for example, if a rigorously tuned GBDT/early-fusion baseline matches or outperforms the cross-modal Transformer on primary hospital $N$, if structured lifestyle predictors contribute marginal or zero $\Delta\text{ROC-AUC}$ / $\Delta\text{Net Benefit}$ beyond clinical + ECG + laboratory features, or if SHAP perturbation AOPC reveals non-trivial feature redundancy — remain **100% scientifically valid, publishable Q1 contributions** and pass Gates `G10–G17` when executed without leakage and reported honestly.

---

## 2. Locked Q1 Research Questions (`RQ0`, `RQ1–RQ4`)

### Primary Research Question (`RQ0` — Overall Mandate, OS §1.4)
- **Formulation:** Under a patient-level, leakage-controlled, and clinically adjudicated evaluation protocol on a primary Bangladeshi cohort (and compatible external benchmark if adopted under `UD06`), how accurately, reliably (in discrimination, probability calibration, and Decision Curve Net Benefit), transparently (in quantitative SHAP AOPC faithfulness, multi-seed stability, and blinded cardiologist plausibility), and robustly (across demographic subgroups and missing-modality scenarios) can a Transformer-based multimodal fusion framework integrating **Clinical data, 12-lead ECG signals, Laboratory assays, and Structured Lifestyle behaviors** predict early cardiovascular disease risk compared to unimodal, clinical-score, and simpler fusion comparators?
- **Governing Objectives:** `O1–O4`
- **Addressed Gaps & Claims:** `GAP0001–GAP0005` (`PG1–PG5`); `CLAIM0001–CLAIM0013`
- **Linked Human Decisions Required Downstream:** `UD02–UD26`

---

### `RQ1` — Four-Modality Transformer Synergy vs Tiered Unimodal, Clinical & Simple-Fusion Baselines
- **Formulation:** Does integrating all four accessible screening modalities (**Clinical vitals/history, 12-lead ECG signals, Laboratory assays, and Structured Lifestyle predictors**) through a cross-modal attention Transformer network yield statistically significant improvements in held-out discrimination (`ROC-AUC`, `PR-AUC`, `F1-Score`), probability calibration (`Brier Score`, `ECE`), and clinical Net Benefit (`DCA`) compared to:
  1. **Tier 1 (Unimodal Baselines):** Tuned Clinical-only, Lab-only, Lifestyle-only (`LR, RF, SVM, XGBoost/LightGBM/CatBoost, MLP`) and ECG-only (`1D-CNN/ResNet-1D, BiLSTM/CNN-LSTM, ECG Transformer`) models;
  2. **Tier 2 (Clinical Risk Scores, optional per `UD02/UD14`):** Established scores (`Framingham, SCORE2, WHO South Asia Risk Chart`) where endpoint and predictors are clinically compatible;
  3. **Tier 3 (Simple Multimodal Fusion):** Early concatenation (`GBDT / MLP`), calibrated late-fusion ensembles, and gated/bilinear fusion on identical patient splits?
- **Hypotheses:**
  - $H_0$: On paired patient-level held-out evaluation, cross-modal Transformer fusion yields $\Delta\text{ROC-AUC} \le 0$ and $\Delta\text{Net Benefit} \le 0$ relative to the strongest Tier 1 unimodal or Tier 3 simple-fusion baseline.
  - $H_1$: Cross-modal Transformer fusion achieves statistically significant improvement (two-sided paired DeLong $p < 0.05$ with Holm-Bonferroni/FDR control) or superior calibrated clinical Net Benefit over Tier 1–3 comparators.
- **Governing Objectives:** `O1`, `O2`, `O3`
- **Linked Gaps & Claims:** `GAP0001` (`PG1` Narrowed), `GAP0002` (`PG2` Narrowed), `GAP0005` (`PG5`); `CLAIM0006, CLAIM0010, CLAIM0013`

---

### `RQ2` — Incremental Predictive & Clinical Utility of Structured Lifestyle and Modality Ablations / Dropout
- **Formulation:** In controlled progressive modality-addition and Leave-One-Modality-Out (LOMO) ablations on identical patient partitions, what is the quantified marginal contribution ($\Delta\text{ROC-AUC}, \Delta\text{PR-AUC}, \Delta\text{Brier}, \Delta\text{Net Benefit}$) of the structured **Lifestyle** modality (smoking pack-years, physical activity, dietary pattern, sleep, and documented family-history sensitivity grouping per `UD08`)—as well as ECG and Laboratory branches—and how gracefully does cross-modal fusion with missing-modality masking degrade when one or more non-clinical modalities are unavailable at inference time (`10%–50%` and complete branch dropout)?
- **Hypotheses:**
  - $H_0$: Adding the structured Lifestyle modality yields no statistically significant incremental discrimination or clinical utility ($\Delta\text{ROC-AUC} \le 0$, $\Delta\text{Net Benefit} \le 0$ vs Clinical+ECG+Lab 3-modality model).
  - $H_1$: Adding Lifestyle provides a measurable, statistically significant improvement in discrimination, calibration, or DCA Net Benefit, OR empirical redundancy patterns with Clinical/Lab factors are cleanly quantified alongside missing-modality retention bounds.
- **Governing Objectives:** `O2`, `O3`
- **Linked Gaps & Claims:** `GAP0002` (`PG2`), `GAP0004` (`PG4`), `GAP0005` (`PG5`); `CLAIM0007, CLAIM0013`

---

### `RQ3` — Quantitative Multimodal XAI Faithfulness, Multi-Seed Stability, Shortcut Audit & Cardiologist Plausibility
- **Formulation:** On the frozen champion model using strictly training-partition SHAP background distributions, do multimodal SHAP attributions (modality-level shares, tabular risk drivers, and ECG waveform/interval attributions per `UD07/UD19`) satisfy quantitative explainability verification:
  1. **Local Additivity & Perturbation Faithfulness (`UD20`):** Verified SHAP additivity error within predeclared tolerance, plus statistically greater **Deletion/Insertion AOPC** (and comprehensiveness/sufficiency) under progressive top-$k$ masking compared to **random** and **reverse-importance** negative controls;
  2. **LOMO Concordance & Multi-Seed Stability (`UD20`):** Consistency between global modality SHAP shares and empirical LOMO $\Delta\text{AUC}$/$\Delta\text{Brier}$ drops, plus rank stability (`Spearman ρ`, `Kendall τ`, `top-k Jaccard`) across $S \ge 3$–$5$ independent random seeds and local input perturbations;
  3. **Spurious-Shortcut Audit (`G14`):** Absence (or remediation/disclosure) of shortcut reliance on site IDs, missingness indicators (`MNAR`), ECG powerline/filter artifacts, or post-diagnosis confounders;
  4. **Blinded Cardiologist Plausibility (`UD21`):** Inter-rater concordance ($\kappa$/ICC) and structured clinical plausibility scoring across balanced `TP/FP/TN/FN` local packets reviewed by qualified cardiologists?
- **Hypotheses & Safety Boundary:**
  - $H_0$: Multimodal SHAP deletion/insertion AOPC does not outperform random feature/patch perturbation controls ($\Delta\text{AOPC} \le 0$).
  - $H_1$: Multimodal SHAP perturbation AOPC significantly exceeds random/reverse controls with stable multi-seed rankings and verified clinical plausibility.
  - **Clinical Boundary (`OS §1.3, §8.3`):** Attributions explain *model predictive behavior*, **not** biological causality; *"increased clinician trust"* or *"faster clinical decision time"* claims are strictly forbidden without a separate IRB-approved reader impact trial (`UD21`).
- **Governing Objectives:** `O4`
- **Linked Gaps & Claims:** `GAP0003` (`PG3`), `GAP0005` (`PG5`); `CLAIM0008, CLAIM0009, CLAIM0012, CLAIM0013`

---

### `RQ4` — Probability Calibration, Subgroup Fairness, PROBAST-AI Integrity & Cohort Generalizability
- **Formulation:** Across demographic strata (biological sex; age groups `<50, 50–65, >65`), clinical recruitment sites (`SITE####`), modality-completeness tiers (`UD10`), and (if adopted under `UD06`) compatible external validation datasets (`MIMIC-IV+ECG` / `PTB-XL` overlapping subsets), how well-calibrated (`Brier Score, ECE, Calibration Slope/Intercept` pre- and post-validation calibration under `UD16`), clinically useful (`DCA` across cardiologist threshold grid `UD17`), equitable across subgroups, and bias-resistant (4-domain `PROBAST-AI` audit across patient-grouped splits `UD11` and incorporation-bias sensitivity analyses `UD02/UD08`) is early CVD risk prediction on a **South Asian / Bangladeshi clinical cohort (`UD04/UD05/UD26`)**?
- **Governing Objectives:** `O1`, `O3`, `O4`
- **Linked Gaps & Claims:** `GAP0001` (`PG1`), `GAP0005` (`PG5`); `CLAIM0001–CLAIM0005, CLAIM0011, CLAIM0013`

---

## 3. Complete RQ-to-Experiment-to-Metric Traceability Matrix (`STEP-009` Audit Core)

| RQ | Objectives | Verified `GAP` / `PG` | Backing Verified Claims | 4-Modality & Cohort Data Needs (`UD##`) | Comparator Tier(s) & Experimental Block (`OS §6.5`) | Mandatory Proposal (`RF12`) + Adopted Q1 Metrics (`UD16–17`) | Primary Statistical Tests (`UD18`) | XAI & Faithfulness Metrics (`UD19–21`) | Permitted Claim Boundary (`OS §8.3, §10`) |
|---|---|---|---|---|---|---|---|---|---|
| **`RQ1`** | `O1, O2, O3` | `GAP0001 (PG1)` `GAP0002 (PG2)` `GAP0005 (PG5)` | `CLAIM0006` `CLAIM0010` `CLAIM0013` | Patient-grouped, IRB-approved synchronized `Clinical + 12L ECG + Lab + Lifestyle` within $t_0 \pm \Delta t$ (`UD02–05, UD07–11`) | **Block A** (Tier 1 Unimodal), **Block B** (Tier 2 Scores if compatible), **Block C** (Tier 3 Early/Late/Gated vs Tier 4 Transformer Fusion), **Block E** (`UD13–15, UD26`) | **6 Mandatory:** Acc, Prec, Rec, F1, ROC-AUC, Confusion Matrix (frozen val $\tau$) **+ Q1:** PR-AUC, Spec, NPV, MCC, Brier, ECE, Calib Slope/Int, DCA | Paired **DeLong** ROC-AUC test ($p<0.05$); paired patient bootstrap ($B\ge 1000$) $\Delta$PR-AUC/Brier/NB; **McNemar**; **Holm-Bonferroni / FDR** | Modality SHAP attribution shares supporting fusion contribution diagnostics | Report superiority **only** if statistically significant after multiplicity adjustment; equalling GBDT is reportable neutral result; no autonomous diagnosis claims |
| **`RQ2`** | `O2, O3` | `GAP0002 (PG2)` `GAP0004 (PG4)` `GAP0005 (PG5)` | `CLAIM0007` `CLAIM0013` | Distinct **Lifestyle** block (`diet, activity, smoking, sleep, fam hx` coding `UD08`) + **missing-modality masks** (`UD10, UD12`) | **Block D** (Progressive addition + LOMO ablations across all 4 modalities), **Block F** (Inference-time `10–50%` & single-branch dropout stress tests) | Full 6 mandatory + PR-AUC + Brier + ECE + **DCA $\Delta\text{Net Benefit}$** vs 3-modality minus Lifestyle & unimodal fallbacks | Paired bootstrap 95% CIs on $\Delta\text{ROC-AUC}$, $\Delta\text{Brier}$, $\Delta\text{Net Benefit}$; paired DeLong comparing 4-mod vs 3-mod (no lifestyle) | Global & local **Modality SHAP %** compared quantitatively vs empirical **LOMO $\Delta\text{AUC}$/$\Delta\text{Brier}$** rank/magnitude concordance | Distinguish predictive contribution from biological causality; null/small lifestyle gain reported honestly as evidence of ECG/lab clinical dominance or measurement noise |
| **`RQ3`** | `O4` | `GAP0003 (PG3)` `GAP0005 (PG5)` | `CLAIM0008` `CLAIM0009` `CLAIM0012` `CLAIM0013` | Train-only representative SHAP background (`UD19`); ECG patch/lead/interval schema (`UD07`); blinded cardiologist review packets (`UD21`) | Frozen Tier 4 Champion (`MODEL####`) vs TreeSHAP (`XGBoost`/`RF`) baseline (`Block C/A`) + multi-seed (`S ≥ 3–5`, `Block F`) | Prediction consistency pre/post perturbation; additivity error $\lvert \phi_0 + \sum \phi_i - f(x) \rvert$ within pre-declared tolerance | Paired comparison of **Deletion & Insertion AOPC** vs **random** & **reverse** perturbation controls (95% bootstrap CIs); multi-seed Spearman $\rho$, Kendall $\tau$, Jaccard; clinical reviewer **ICC / $\kappa$** | **Multimodal SHAP** (Modality + Tabular + ECG segments/intervals); Deletion/Insertion **AOPC**; Seed stability; Lipschitz noise check; **Shortcut Audit**; **Blinded Cardiologist Rubric** | Can claim perturbation faithfulness, stability, shortcut freedom, & clinical plausibility *only if passed*; **prohibited:** causal biological claims, "improves clinician trust/speed" (`OS §8.3`) |
| **`RQ4`** | `O1, O3, O4` | `GAP0001 (PG1)` `GAP0005 (PG5)` | `CLAIM0001–05` `CLAIM0011` `CLAIM0013` | Primary Bangladeshi site metadata (`UD04–05`), sex/age strata, completeness tiers (`UD10`), optional external cohort (`UD06`) | Frozen Champion & best comparator evaluated on **sealed test set** (`G11–G13`), subgroup strata, external test (if `UD06`), incorporation-bias sensitivity (`Block F`) | Stratified 6 mandatory + PR-AUC + **Brier, BSS, ECE, Slope/Intercept** (pre- vs post-validation calibration `UD16`) + **DCA (`p_t` grid `UD17`)** | Stratified patient-level bootstrap 95% CIs (`B ≥ 1000`); subgroup disparity flags; external vs internal shift testing; **4-domain PROBAST-AI** & **TRIPOD+AI** audit | Subgroup-stratified global SHAP profiles & TP/FP/TN/FN error patterns inspected with qualified cardiologist (`T20`) | Explicitly bound claims to target Bangladeshi clinical setting & cross-sectional vs longitudinal horizon (`UD02`); disclose residual PROBAST-AI risks & small-$N$ CI width |

---

## 4. Literature Search Cutoff Date & Search Governance Log (`STEP-009` / `OS §3.4`)

- **Initial Primary Search Cutoff Date:** **`2026-11-25`** (`SEARCH-SCHOLAR-20261125`).
- **Executed Search Coverage:** Google Scholar `5`-query suite (`SEARCH-SCHOLAR-Q1` through `Q5`), returning `128` query-paper hits $\rightarrow$ `83` unique PDFs full-text screened $\rightarrow$ `42` included studies (`29` original + `13` reviews/meta-analyses; `100%` `MetadataVerified=yes`, `ReadingStatus=Extracted` in `papers.csv`, `42/42` matched in `references.bib`). Note `P0001` (`Botros2024_P0001`) carries `DOI=not reported` in the source accepted-manuscript PDF and is verified via publisher ScienceDirect URL (`PII S1746809424010553`).
- **Search Coverage Limitation (`G03` Transparency Rule):** Pre-drafted query strategies for **PubMed/MEDLINE** (`SEARCH-PUBMED-01`), **IEEE Xplore** (`SEARCH-IEEE-01`), **Scopus** (`SEARCH-SCOPUS-01`), and **arXiv/PhysioNet** (`SEARCH-PREPRINT-01`) remain at status `Ready for Execution` (`02_Literature/searches/`). As logged in [DEC0002](../01_Project_Management/decision_log/DEC0002.md), Supervisor Md. Mizanur Rahman determines whether supplementary PubMed/IEEE/Scopus verification exports are required prior to `G03 PASS` or scheduled alongside the mandatory pre-modeling (`STEP-023`) and pre-submission (`STEP-048`) update searches (`OS §3.4`).
- **Update Search Schedule:**
  1. **Update Search #1 (`STEP-023`, pre-modeling freeze):** Re-run multi-database delta check for new `2026–2027` 4-modality ECG+EHR+Lab+Lifestyle CVD studies prior to locking deep architecture choices.
  2. **Update Search #2 (`STEP-048`, pre-Q1 manuscript submission):** Final living-review update across PubMed, Scopus, IEEE Xplore, and Google Scholar prior to submission to lock final bibliography cutoff date (`TRIPOD+AI` item 3 / `PRISMA`).

---

## 5. Human Ratification & `G03` Lock Record (`STEP-009`)

*All documentary evidence, gap testing (`GAP0001–GAP0005`), claim linkages (`CLAIM0001–CLAIM0013`), and full-text extraction provenance (`P0001–P0042`) are verified and locked at `v1.0.0 Candidate Final`. Transition to locked baseline and `G03 PASS` requires human review and signature below.*

| Role | Name | Decision / Action | Date | Signature |
|---|---|---|---|---|
| **1st Researcher (Lit & Modeling Lead)** | Rayan Ahmed (`232-15-847`) | Prepared & Audited `RQ0, RQ1–RQ4` | `2026-11-26` | *Prepared (`DEC0002`)* |
| **2nd Researcher (Cohort & Eval Lead)** | Mohammad Nafis Sadiq (`232-15-895`) | Screened `P0001–P0083` & Co-Audited | _____ | *Awaiting confirm* |
| **Supervisor (`G03` Approver)** | Md. Mizanur Rahman | Approves `RQ1–RQ4`, Null Policy & `G03` Disposition | _____ | **Pending (`DEC0002`)** |
