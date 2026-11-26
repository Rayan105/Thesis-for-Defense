# Evidence Synthesis & Proposal Gap Verification (STEP-008)

| Metadata | Value |
|---|---|
| Document | `02_Literature/synthesis.md` |
| Version | v1.0.0 |
| Step | STEP-008 |
| Date | 2026-11-26 |
| Leads | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Reviewer | Md. Mizanur Rahman |
| Source Files | [papers.csv](file:///e:/FYDP/02_Literature/papers.csv), [comparative_matrix.md](file:///e:/FYDP/02_Literature/comparative_matrix.md), [claims.csv](file:///e:/FYDP/02_Literature/claims.csv), [summaries/](file:///e:/FYDP/02_Literature/summaries/) (P0001–P0042) |
| PHI Sensitivity | Tier 1 (Public / Git-safe) |

---

## 1. Executive Summary

This synthesis triangulates evidence from 42 included studies (29 original + 13 reviews/meta-analyses) retrieved from Google Scholar (`5` queries `SEARCH-SCHOLAR-Q1`–`Q5`, cutoff `2026-11-25`) to rigorously test five proposal research gaps (`PG1–PG5`) against both supporting and contradicting literature. Although `14 of 29` original studies integrate $\ge 3$ data sources/signal streams (including `P0020, P0022, P0025, P0036, P0038`), **none** combines the four accessible primary screening modalities — Clinical vitals, 12-lead ECG waveforms, Laboratory assays, and Structured Lifestyle behaviors — in a leakage-free cross-modal Transformer framework with calibration, DCA, quantitatively verified multimodal SHAP faithfulness (AOPC + stability + clinician plausibility), and South Asian/Bangladeshi evaluation. All five gaps survive systematic testing as **supported-within-search**, with PG1 and PG2 narrowed to precise falsifiable formulations.

> [!IMPORTANT]
> **Zero "first ever" claims are made.** Each gap statement explicitly acknowledges contradicting evidence (P0016/P0025/P0031/P0036/P0038 for ≥3 modalities; P0028/P0029/P0032/P0038 for quantitative XAI) and states the residual gap precisely.

---

## 2. Thematic Synthesis

### 2.1 Multimodal Fusion Architectures in CVD Prediction

#### 2.1.1 Landscape of Modality Integration

The 29 original studies span a wide range of modality combinations:

| Modality Count | Studies ($n=29$) | Exact Paper IDs & Key Examples |
|---|---|---|
| **1 modality** | `3` | `P0005` (ECG-only SEER; PCE external comparator), `P0028` (ECG images across time/CWT/FFT views), `P0033` (12-lead ECG only) |
| **2 modalities** | `12` | `P0001` (ECG V4+Lab), `P0003` (ECG img+EHR), `P0004` (ECG+PCG), `P0006` (PPG+ECG), `P0007` (ECG+Age/Sex), `P0008` (ECG+CXR), `P0011` (ECG+EHR meta), `P0012` (ECG+9 int+Age/Sex), `P0014` (ECG+7 clinical), `P0015` (ECG+PCG), `P0024` (ECG+EHR), `P0029` (ECG+CXR) |
| **3 modalities** | `1` | `P0021` (12L ECG img + Clinical/EHR + Smoking; 0 labs) |
| **4+ modalities / streams** | `13` | **Clinical+ECG+Lab+Smoking/Wearable (`2`):** `P0020` (2-lead ECG+C+L+Smoking, ICI), `P0022` (C+L+Lifestyle+Wearable HR incl. BD CAIR-CVD-2025, 0 raw ECG, severe leak); **With Tertiary Imaging (`5`):** `P0016` (+Echo), `P0031` (+LGE-MRI), `P0036` (+CCTA +Smoking), `P0038` (C+L+Text+CMR, **Low PROBAST**, 0 ECG); **With Text/Genomics/Sensors (`6`):** `P0002` (C+E+L+Text), `P0013` (C+E+L+Text), `P0023` (ECG+PPG+Spiro+PRS), `P0025` (C+E+L+PRS), `P0030` (Fundus+ECG+PPG+EHR), `P0032` (ECG+EMG+BP+Resp), `P0037` (C+E+L+Text, AKI) |

**Key finding:** While `14/29` original studies combine $\ge 3$ modalities/signal streams (so broad *"only 1 or 2 modalities"* claims must be **narrowed**), **0/29** combines the four accessible primary screening modalities (**Clinical + 12-lead ECG waveforms + Laboratory assays + Structured Lifestyle**) in a leakage-free cross-modal Transformer framework without tertiary imaging/genomics or High PROBAST leakage (`P0020` uses only 2 ECG leads in cancer ICI patients without fusion SHAP; `P0022` has zero raw ECG and pre-split SMOTE leakage; `P0036` depends on CCTA and has $\pm 30$-day post-CCTA leakage; `P0038` achieves Low PROBAST gold standard but models CMR+EHR+Text without ECG waveforms or SHAP AOPC).

#### 2.1.2 Fusion Strategies

- **Late fusion** dominates: 10/15 multimodal HF studies used late fusion (P0017, p. 14). Score-level concatenation or ensemble averaging is the predominant strategy (P0001, P0004, P0005, P0021, P0025).
- **Cross-modal attention** is emerging: P0012 (CaMPNet), P0014 (MAF-Net), P0016 (ChemoCardioNet), P0036 (CGH cross-modal), and P0038 (MAIS contrastive) employ learned cross-attention, but none combines all four accessible screening modalities.
- **Joint/intermediate fusion** appears in P0003 (1D-CNN+MLP), P0020 (CNN+MLP), and P0002 (CNN-LSTM+BERT), typically via feature concatenation rather than attention-based interaction.

#### 2.1.3 ECG Encoder Architectures

| Architecture | Studies | Key Properties |
|---|---|---|
| 1D CNN/ResNet | P0001, P0003, P0005, P0007, P0011, P0020, P0025 | Standard backbone; works on raw waveforms |
| CNN-Transformer hybrid | P0012, P0014, P0016 | Cross-attention between ECG patches and clinical features |
| Vision Transformer (ViT) | P0006 (MAE-ViT), P0008 (MedCLIP ViT), P0021 (MedCLIP ViT) | Treat ECG as image; lose temporal fine-grained resolution |
| Foundation Model (ECG-FM) | P0013 (Wav2Vec 2.0-based frozen ECG-FM) | Transfer learning from pre-trained ECG foundation model |
| β-VAE latent | P0023 (M-REGLE), P0031 (DEEP RISK) | Unsupervised ECG representation; interpretability via latent traversal |
| S4 (Structured State Space) | P0024 | Long-range dependency; bidirectional; emerging architecture |

**Gap implication:** No ECG encoder has been combined with cross-modal attention over Clinical+Lab+Lifestyle branches in a single Transformer fusion model.

---

### 2.2 Lifestyle Modality: Inclusion and Incremental Value

Of `29` original studies, `22/29` completely omit lifestyle predictors (plus `P0030` unverified prose = `23/29`), while only **`6/29`** (`20.7%`) include any smoking or lifestyle variable (`P0020, P0021, P0022, P0025, P0036, P0038`):

| Study | Lifestyle Variables Included | Distinct Modality Branch? | LOMO Ablation Quantified? | PROBAST |
|---|---|---|---|---|
| `P0020` | Smoking (unquantified self-report) | No (EHR baseline / concat) | No | High |
| `P0021` | Smoking (binary EHR flag) | No (RF tabular vector; 0 labs) | No | High |
| `P0022` | Smoking, alcohol, activity (`CAIR-CVD-2025` / UCI) | No (tabular w/o raw ECG) | No | High |
| `P0025` | Current smoking (`CHARGE-AF` covariate) | No (`CRS` logistic block; 0 diet/activity) | No | Unclear |
| `P0036` | Smoking (binary EHR variable) | No (EHR tabular; requires CCTA) | No | High |
| `P0038` | Smoking (`50.4%`, EHR text risk factor) | No (serialized text; 0 ECG waveforms) | No | Low |

**Key findings:**
1. **No study treats lifestyle as a distinct modality branch** with its own encoder/embedding layer.
2. **No study performs LOMO ablation** to quantify the marginal contribution of lifestyle variables alongside ECG and laboratory data.
3. Where lifestyle variables appear, they are single binary indicators (smoking yes/no) embedded within EHR tabular columns, not comprehensive behavioral vectors (diet score, physical activity level, smoking pack-years).
4. P0022 includes the most lifestyle variables but combines them without raw ECG waveforms and under severe pre-split leakage.

**Significance for RQ2:** The absence of LOMO ablation means the incremental predictive and clinical utility of lifestyle data alongside ECG/Lab remains empirically unknown. Our RQ2 hypothesis (H₀: ΔNet Benefit ≤ 0) is genuinely untested.

---

### 2.3 PROBAST Risk of Bias: Pervasive Leakage

#### 2.3.1 Audit Results

| PROBAST Rating | Count | Percentage | Studies |
|---|---|---|---|
| **Low** | 1 | 3.4% | P0038 |
| **Unclear** | 3 | 10.3% | P0005, P0023, P0025 |
| **High** | 25 | 86.2% | All others |

This is consistent with external benchmarks: P0042 found 34.3% High Risk across 108 AI-ECG studies (Table 3 p. 9), and P0010 found 34.5% High Risk across 46 EHR-ML models (p. 10). Our higher rate (86.2%) reflects stricter full-text auditing against the PROBAST-AI checklist.

#### 2.3.2 Dominant Bias Mechanisms

1. **Pre-split data processing leakage** (most prevalent): SMOTE, MICE imputation, Z-score normalization, or feature selection applied before train/test splitting → `P0002, P0013, P0022, P0031`.
2. **Record/segment/image-level splitting** (patient overlap between train/test): `P0001, P0004, P0007, P0012, P0015, P0024, P0028`.
3. **Post-diagnosis/target leakage** (features unavailable at prediction time): `P0002, P0011, P0014, P0036, P0037`.
4. **Test-set tuning or selection bias**: `P0003, P0004`.
5. **Severe metric/provenance inconsistencies**: `P0016, P0029, P0030`.

#### 2.3.3 Implications for Our Framework

- **Patient-level splitting** is mandatory (enforced in STEP-019/020).
- **All preprocessing** (imputation, normalization, SMOTE) must be fitted on the training fold only and applied to test data as a transform — never before splitting.
- **Calibration** (Platt scaling / temperature scaling on validation set) and **DCA** must be reported alongside discrimination metrics — only 7/29 report any calibration metric (P0007 Brier only, P0013 Brier only, P0016 malformed Brier, P0021 Brier, P0025 HL counts, P0031 visual slope, P0038 IBS + DCA).

---

### 2.4 South Asian and Bangladeshi Cohort Representation

**Zero (0/29)** original empirical studies tested a leakage-free Bangladeshi or South Asian multimodal cohort combining 12-lead ECG, Clinical, Lab, and Lifestyle data.

| Evidence | Source | Key Finding |
|---|---|---|
| South Asian scarcity in PTB-XL/MIMIC-IV | P0018 §4.4 p. 34 | Explicitly cites the gap |
| 0/85 Bangladeshi DL-ECG cohorts | P0041 Fig. 1e p. 5 | Bangladeshi-led review finds zero BD data |
| 29% race reporting; 89% White; 0 SA | P0026 p. 12 | Extreme demographic skew across 102 AI-ECG studies |
| 91.2% CVD death rise in Asia 2025–2050 | P0040 p. 3 | Epidemiological urgency |
| >80% CVD deaths in LMICs | P0040 p. 3 | Resource-limited setting priority |
| CAIR-CVD-2025 (Bangladesh) | P0022 pp. 5–6 | Only BD dataset reference — but no raw ECG, High PROBAST |
| Singapore SEED Indian subgroup | P0030 p. 13 | AUC 0.94 claimed but under severe provenance anomalies |

**Significance:** The absence of validated models on South Asian populations, combined with the highest projected CVD mortality growth globally, constitutes a critical scientific and public health gap. Within our `42`-paper curated corpus, none has yet delivered a leakage-free multimodal 12-lead ECG+Clinical+Lab+Lifestyle framework evaluated on a Bangladeshi primary clinical cohort.

---

### 2.5 XAI Faithfulness: Qualitative Dominance, Quantitative Void

#### 2.5.1 XAI Methods Used Across 29 Original Studies

| XAI Approach | Studies | Quantitative Faithfulness? |
|---|---|---|
| **SHAP (qualitative only)** | P0002, P0011, P0016, P0020, P0021, P0022, P0031, P0036 | No — summary/bar/force plots only |
| **Grad-CAM / ScoreCAM (qualitative)** | P0004, P0006, P0007, P0021, P0036 | No — visual heatmaps only |
| **LIME (qualitative)** | P0003, P0004 | No — applied to baseline only (P0003) |
| **Integrated Gradients (qualitative)** | P0013 | No — bar plots only |
| **Attention weights** | P0012, P0014, P0016, P0038 | No — intrinsic but not post-hoc faithfulness |
| **EAT sanity/NMI/FGSM** | P0028 | **Partial** — sanity checks + adversarial perturbation |
| **AOPC deletion/insertion** | P0029 | **Partial** — CXR only; deletion failed vs random |
| **MEMC top-k deletion** | P0032 | **Partial** — unimodal; no AUC-based AOPC |
| **Cardiologist plausibility + shuffling** | P0038 | **Yes** — blinded ICC=0.91 + rationale ablation |
| **None** | P0005, P0008, P0015, P0023, P0024, P0025, P0033, P0037 | N/A |

#### 2.5.2 The "Qualitative SHAP Illusion"

A critical finding is the **systematic conflation of SHAP usage with XAI evaluation**. Preliminary intake tagged 24/42 papers as having "quantitative faithfulness." Full-text reading corrected **20/24 to No**. The pattern:
- Authors compute SHAP values and render summary/beeswarm/bar plots.
- No deletion/insertion AOPC comparison vs random baseline is performed.
- No multi-seed stability (Spearman ρ / Jaccard) is reported.
- No clinician review of attribution plausibility is conducted.
- Papers are nonetheless cited as "explainable AI" contributions.

#### 2.5.3 Implications for RQ3

Our RQ3 protocol must demonstrate:
1. **AOPC deletion/insertion curves** vs random controls (following P0029's methodology, but ensuring deletion actually outperforms random).
2. **Multi-seed stability** (≥5 seeds) with Spearman ρ and top-k Jaccard.
3. **Cardiologist plausibility** review (following P0038's blinded ICC methodology).
4. **Shortcut auditing** to verify attributions are not driven by data artifacts.

---

### 2.6 Calibration, Clinical Utility (DCA), and Missing-Modality Handling

#### 2.6.1 Calibration Reporting (`n = 29` Original Studies)

| Reporting Status | Studies | Count |
|---|---|---|
| **Numeric Brier / IBS / HL reported** | `P0007` (GAH fold Brier `0.127–0.141`), `P0013` (Brier `0.0269`), `P0021` (Brier `0.184`), `P0025` (HL pass counts), `P0038` (IPCW IBS `0.163` int / `0.179` LOCO) | `5/29` (`17.2%`) |
| **Baseline-only, visual, unverified prose, or malformed** | `P0002` (claimed), `P0012` (plot only), `P0016` (contradictory `0.083 vs 0.06` & step curve), `P0020` (RF baseline Platt only; fusion deferred), `P0030` (unverified prose ECE `0.037`/Brier `0.082`), `P0031` (visual slope showing overestimation after SMOTE) | `6/29` (`20.7%`) |
| **None (`not reported`)** | `P0001, P0003, P0004, P0005, P0006, P0008, P0011, P0014, P0015, P0022, P0023, P0024, P0028, P0029, P0032, P0033, P0036, P0037` | `18/29` (`62.1%`) |

Only **18/29 (`62.1%`)** omit calibration entirely, while only **`5/29` (`17.2%`)** provide clean numeric calibration metrics—and none of those pairs Brier + ECE + slope/intercept jointly on an ECG+Clinical+Lab+Lifestyle model (`P0027` similarly confirms `45%` calibration reporting across 69 DL-CVD studies, p. 28).

#### 2.6.2 Decision Curve Analysis (DCA)

Only **`2/29` (`6.9%`)** studies report valid DCA curves: **`P0038`** (`8-panel` DCA, Fig. 5 p. 8) and **`P0007`** (reported across `5%–20%` thresholds in external `Supplementary Fig. S3`, pp. 4–5). One study (**`P0016`**) prints a malformed Fig. 3 DCA plot with y-axis `-80 to 0` (p. 4). The remaining **`26/29` (`89.7%`)** omit DCA entirely.

#### 2.6.3 Missing-Modality Handling

| Study | Approach | Performance Impact |
|---|---|---|
| P0036 | Cross-modal fusion with dedicated missingness pathway | Int AUC 0.86 → Miss 0.76 (−11.6%) |
| P0038 | Contrastive missing-modal MAIS | C-index 0.6910 → −LGE 0.6694 (−3.1%) |
| P0039 (Review) | Surveys imputation, zero-filling, attention masking | 18% of 52 studies address missing data |

**Significance:** Only 2/29 original studies and 1 review address missing-modality degradation. For real-world hospital deployment where patients may lack ECG or specific labs, missing-modality robustness is essential and largely untested.

---

## 3. Proposal Gap Verification Summary (`PG1–PG5`)

| Gap | Proposal Claim | Status After Synthesis | Sharpened Q1 Formulation | GAP Record | RQ Link |
|---|---|---|---|---|---|
| **PG1** | Most studies use only one data type | **Narrowed** — `14/29` use $\ge 3$ streams, but `0/29` uses accessible C+E+L+S cleanly | No accessible 4-modality deep fusion with leakage-free design | [GAP0001](file:///e:/FYDP/02_Literature/gap_notes/GAP0001.md) | RQ1 |
| **PG2** | Only two sources combined | **Narrowed** — `14/29` combine $\ge 3$ streams, yet none with C+E+L+S Transformer | No C+E+L+S cross-attention Transformer with patient-level split | [GAP0002](file:///e:/FYDP/02_Literature/gap_notes/GAP0002.md) | RQ1, RQ2 |
| **PG3** | Models don't explain predictions | **Supported** — `4/42` show partial/clinical quantitative XAI; `0/42` full protocol | `0/42` jointly evaluates SHAP AOPC + stability + shortcut audit + cardiologist plausibility on 4-modality C+E+L+S fusion | [GAP0003](file:///e:/FYDP/02_Literature/gap_notes/GAP0003.md) | RQ3 |
| **PG4** | Lifestyle information ignored | **Supported** — `23/29` omit structured lifestyle; `6/29` flag smoking/lifestyle without LOMO | `0/29` isolates structured Lifestyle + LOMO $\Delta$Net Benefit alongside 12-lead ECG+Lab | [GAP0004](file:///e:/FYDP/02_Literature/gap_notes/GAP0004.md) | RQ2 |
| **PG5** | Few explainable multimodal frameworks | **Supported** — `P0038` is closest Low-PROBAST template but uses CMR, not ECG+Lab+Lifestyle | No end-to-end framework satisfies all 5 criteria (C+E+L+S fusion + leakage-free + XAI + missing-modality + SA cohort) | [GAP0005](file:///e:/FYDP/02_Literature/gap_notes/GAP0005.md) | RQ1–RQ4 |

> [!NOTE]
> "Supported-within-search" means the gap holds within our 42-paper curated corpus. Update searches before final submission are required per the Blueprint recovery procedure (STEP-008 §559).

---

## 4. Q1 Contribution Positioning (Bounded Within Verified Search Coverage)

Based on the gap analysis, our study positions **four falsifiable Q1 contributions** (contingent on empirical outcomes under `RQ1–RQ4`, where null or modest gains remain valid Q1 results):

1. **C1 (from GAP0001/GAP0002 → RQ1):** Evaluate a leakage-free cross-modal attention Transformer framework fusing 4 accessible screening modalities (`Clinical + 12-lead ECG waveforms + Laboratory + Structured Lifestyle`) with patient-level splitting, post-hoc calibration (Platt/Temperature/Isotonic), DCA, and fair benchmarking against 4-tier unimodal and simple-fusion baselines (`unobserved among the 42 curated studies without tertiary imaging/genomics or High PROBAST risk`).

2. **C2 (from GAP0004 → RQ2):** Conduct controlled Leave-One-Modality-Out (LOMO) and progressive ablations quantifying the incremental discrimination and clinical Net Benefit (`DCA`) of a structured lifestyle modality alongside 12-lead ECG and laboratory biomarkers, explicitly testing whether lifestyle contributes measurable marginal utility or redundancy.

3. **C3 (from GAP0003 → RQ3):** Execute a joint quantitative XAI verification suite combining multimodal SHAP deletion/insertion AOPC (vs random and reverse controls), multi-seed rank stability (`Spearman ρ` / `top-k Jaccard`), LOMO concordance, shortcut auditing, and blinded qualified cardiologist plausibility review on the 4-modality fusion model.

4. **C4 (from GAP0005 → RQ4):** Deliver and evaluate the complete explainable 4-modality screening workflow on a clinically adjudicated Bangladeshi cohort (plus optional external compatibility testing under `UD06`) with inference-time missing-modality stress tests and full `PROBAST-AI` / `TRIPOD+AI` reporting.

> [!WARNING]
> **Claim boundary:** All novelty statements strictly reflect absence within our `42`-paper Google Scholar corpus (`cutoff 2026-11-25`) and prohibit categorical *"first ever in human history"* assertions. Supplementary database verification (`PubMed/IEEE/Scopus`) at Supervisor discretion (`DEC0002`) and mandatory update searches prior to `STEP-023` (modeling) and `STEP-048` (manuscript submission) govern ongoing validity.

---

## 5. Identified Methodological Patterns from Literature

### 5.1 Lessons for Our Framework Design

| Pattern Observed | Studies | Lesson for Our Study |
|---|---|---|
| Pre-split SMOTE/MICE leakage → inflated AUC | P0002, P0013, P0022, P0031 | All preprocessing on train fold only |
| Record-level splitting with patient overlap | P0001, P0004, P0012, P0015, P0024 | Enforce strict `PatientID`-grouped splitting |
| SHAP without AOPC = no faithfulness proof | P0002, P0011, P0016, P0020, P0021, P0022, P0031, P0036 | Mandatory AOPC deletion/insertion vs random |
| External validation rare | P0017 (13/15 internal), P0027 (83% internal), P0041 (64.7% internal) | Multi-center LOCO or temporal held-out |
| Calibration / DCA rarely complete | `18/29` zero calibration; `26/29` zero DCA | Report Brier, ECE, slope/intercept, DCA |
| Missing modality untested | 27/29 original studies | Dedicated missing-modality degradation protocol |
| South Asian populations excluded | 0/29 with clean SA/BD multimodal cohort | Primary Bangladeshi cohort enrollment |

### 5.2 Benchmark Performance Ranges (from Leakage-Aware Studies Only)

| Study | Endpoint | Best AUC | PROBAST | Notes |
|---|---|---|---|---|
| P0005 (SEER) | 5y CV Mortality | 0.832 (dev); 0.781–0.825 (ext) | Unclear | ECG-only; 536K ext patients |
| P0038 (MAIS) | STEMI MACE | C-index 0.691 (int); 0.677 (LOCO) | Low | CMR+EHR+Text; 4-center |
| P0025 (ARIC AF) | Incident AF 15y | C-stat 0.810 (V3); 0.875 (V5) | Unclear | C+E+L+PRS; European only |
| P0036 (CGH) | 1y MACE | AUC 0.86 (int); 0.83 (ext) | High | C+E+L+S+CCTA; 460 pts |

**Realistic performance expectations:** AUC in the 0.75–0.85 range for genuinely leakage-free multimodal CVD prediction on adjudicated cohorts. Studies reporting AUC >0.95 universally exhibit High PROBAST risk.

---

## 6. Limitations of This Synthesis

1. **Single-database search:** Only Google Scholar was searched. PubMed, Scopus, IEEE Xplore, and Cochrane Library were not queried, limiting comprehensiveness. Recovery: supplementary searches before STEP-009/G03.
2. **Language bias:** Only English-language publications were included.
3. **Date cutoff:** Search executed 2026-11-25; studies published after this date are not captured.
4. **Review quality heterogeneity:** Among the 13 included reviews, several (P0027, P0030, P0039) contain internal errors (table count mismatches, duplicate entries, referencing errors), limiting meta-evidence reliability.
5. **PDF reading limitations:** Some supplementary materials (online-only appendices) were not accessible for P0036 and P0042, potentially missing additional methodological details.

---

## 7. Next Steps (`STEP-009` / `G03`)

1. **STEP-009 (`research_questions.md` v1.0.0 & `DEC0002`):** Present this synthesis, `GAP0001–GAP0005`, and locked `RQ0 / RQ1–RQ4` (plus null/negative-result contract) to Supervisor Md. Mizanur Rahman for `G03` ratification.
2. **Supplementary Search Disposition (`DEC0002`):** Confirm with Supervisor whether supplementary `PubMed / IEEE Xplore / Scopus` exports run prior to `G03 PASS` or during scheduled `STEP-023` (pre-modeling) and `STEP-048` (pre-submission) update searches.
3. **STEP-010+:** Begin prospective sample-size/EPV feasibility calculations and Bangladesh hospital/clinic scouting with explicit 4-modality requirements (`12-lead ECG + Clinical + Lab + Structured Lifestyle CRF`).
4. **Experiment design:** Adopt `P0038`'s Low-PROBAST design discipline (patient-level split + multi-center LOCO + blinded cardiologist review + DCA + missing-modality resilience) paired with quantitative SHAP AOPC faithfulness (`P0029/P0032` lessons) on accessible screening modalities.
