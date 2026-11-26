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

This synthesis triangulates evidence from 42 included studies (29 original + 13 reviews/meta-analyses) to rigorously test five proposal research gaps (`PG1–PG5`) against both supporting and contradicting literature. The analysis reveals that while 7 of 29 original studies integrate ≥3 data modalities, **none** combines the four accessible primary screening modalities — Clinical vitals, 12-lead ECG waveforms, Laboratory assays, and Lifestyle behaviors — in a leakage-free deep fusion framework with calibration, DCA, quantitatively verified XAI, and evaluation on South Asian or Bangladeshi cohorts. All five gaps survive systematic testing as **supported-within-search**, with PG1 and PG2 narrowed to precise falsifiable formulations.

> [!IMPORTANT]
> **Zero "first ever" claims are made.** Each gap statement explicitly acknowledges contradicting evidence (P0016/P0025/P0031/P0036/P0038 for ≥3 modalities; P0028/P0029/P0032/P0038 for quantitative XAI) and states the residual gap precisely.

---

## 2. Thematic Synthesis

### 2.1 Multimodal Fusion Architectures in CVD Prediction

#### 2.1.1 Landscape of Modality Integration

The 29 original studies span a wide range of modality combinations:

| Modality Count | Studies | Key Examples |
|---|---|---|
| **1 modality** | 6 | P0005 (ECG-only SEER), P0006 (ECG/PPG pretraining), P0028 (ECG images), P0033 (ECG ResNet vs Linear) |
| **2 modalities** | 16 | P0001 (ECG+Lab), P0003 (ECG+EHR), P0007 (ECG+Age/Sex), P0008 (ECG+CXR), P0012 (ECG+Demog), P0014 (ECG+Clinical), P0015 (ECG+PCG), P0024 (ECG+Clinical), P0029 (ECG+CXR) |
| **3 modalities** | 3 | P0020 (ECG+Lab+Smoking), P0021 (ECG+EHR+Smoking), P0023 (ECG+PPG+PRS) |
| **4+ modalities** | 4 | P0002 (C+E+L+Text), P0013 (C+E+L+Text), P0025 (C+E+L+PRS), P0036 (C+E+L+S+CCTA) |

**Key finding:** Only 7/29 studies used ≥3 modalities, and among these, **none used the accessible 4-modality combination of C+E+L+S** without tertiary imaging (CMR, CCTA, Echo) or genomics (PRS) dependencies. P0038 achieves the gold-standard experimental design (Low PROBAST, 4-center LOCO) but uses CMR+EHR+Text modalities.

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

Of 29 original studies, only **4** include any lifestyle variable:

| Study | Lifestyle Variables | As Distinct Modality? | LOMO Ablation? | PROBAST |
|---|---|---|---|---|
| P0020 | Smoking (binary) | No (EHR column) | No | High |
| P0021 | Smoking (binary) | No (EHR column) | No | High |
| P0022 | Smoking, alcohol, activity | No (tabular) | No | High |
| P0036 | Smoking (binary) | No (EHR column) | No | High |

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

**Significance:** The absence of validated models on South Asian populations, combined with the highest projected CVD mortality growth globally, constitutes a critical scientific and public health gap. Our study would be the **first leakage-free multimodal ECG+Clinical+Lab+Lifestyle framework evaluated on a Bangladeshi primary clinical cohort**.

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

#### 2.6.1 Calibration Reporting

| Metric | Studies Reporting | Total |
|---|---|---|
| Brier / IBS | P0007, P0013, P0021, P0038 | 4/29 |
| HL test | P0025 | 1/29 |
| Calibration slope/intercept | P0031 (visual only) | 1/29 |
| ECE | P0030 (prose only, unverifiable) | 1/29 |
| **None** | 22/29 | 22/29 |

Only P0038 reports both IBS and DCA. P0027's review confirms only 45% of DL-CVD studies report calibration (p. 28).

#### 2.6.2 Decision Curve Analysis (DCA)

Only **P0038** presents formal DCA curves (Fig. 5 p. 8), demonstrating net benefit across threshold probabilities. P0007 mentions clinical utility qualitatively. All other studies omit DCA entirely.

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
| **PG1** | Most studies use only one data type | **Narrowed** — 7/29 use ≥3, but none with accessible C+E+L+S | No accessible 4-modality deep fusion with leakage-free design | [GAP0001](file:///e:/FYDP/02_Literature/gap_notes/GAP0001.md) | RQ1 |
| **PG2** | Only two sources combined | **Narrowed** — same 7 contradict, but none with C+E+L+S Transformer | No C+E+L+S cross-attention Transformer with patient-level split | [GAP0002](file:///e:/FYDP/02_Literature/gap_notes/GAP0002.md) | RQ1, RQ2 |
| **PG3** | Models don't explain predictions | **Supported** — 4/42 show partial quantitative XAI; 0/42 full protocol | 0/42 jointly evaluates SHAP AOPC + stability + cardiologist plausibility on 4-modality fusion | [GAP0003](file:///e:/FYDP/02_Literature/gap_notes/GAP0003.md) | RQ3 |
| **PG4** | Lifestyle information ignored | **Supported** — 4/29 include lifestyle but none quantifies via LOMO | 0 LOMO ablation quantifies lifestyle ΔNet Benefit alongside ECG+Lab | [GAP0004](file:///e:/FYDP/02_Literature/gap_notes/GAP0004.md) | RQ2 |
| **PG5** | Few explainable multimodal frameworks | **Supported** — P0038 is closest but uses CMR, not ECG+Lab+Lifestyle | No end-to-end framework satisfies all 5 criteria (C+E+L+S fusion + leakage-free + XAI + SA cohort + missing-modality) | [GAP0005](file:///e:/FYDP/02_Literature/gap_notes/GAP0005.md) | RQ1–RQ4 |

> [!NOTE]
> "Supported-within-search" means the gap holds within our 42-paper curated corpus. Update searches before final submission are required per the Blueprint recovery procedure (STEP-008 §559).

---

## 4. Q1 Contribution Positioning

Based on the gap analysis, our study positions **four novel Q1 contributions**:

1. **C1 (from GAP0001/GAP0002 → RQ1):** First leakage-free cross-modal attention Transformer framework fusing 4 accessible screening modalities (Clinical + 12-lead ECG waveforms + Laboratory + Lifestyle) with patient-level splitting, calibration (Platt/Temperature), and DCA on a clinically adjudicated cohort.

2. **C2 (from GAP0004 → RQ2):** First controlled LOMO ablation quantifying the incremental discrimination and clinical utility (ΔNet Benefit via DCA) of a structured lifestyle modality alongside ECG and laboratory data, allowing falsification of the hypothesis that lifestyle adds zero marginal value.

3. **C3 (from GAP0003 → RQ3):** First joint evaluation of multimodal SHAP deletion/insertion AOPC faithfulness (vs random controls), multi-seed attribution stability (Spearman ρ / top-k Jaccard), and blinded cardiologist plausibility review on a 4-modality deep fusion CVD model.

4. **C4 (from GAP0005 → RQ4):** First evaluation of a 4-modality explainable multimodal CVD framework on a Bangladeshi primary clinical cohort with missing-modality degradation stress tests and PROBAST-AI self-audit.

> [!WARNING]
> **Claim boundary:** These "first" claims are bounded by our 42-paper search corpus and Google Scholar coverage. Pre-submission update searches across PubMed, Scopus, IEEE Xplore, and Cochrane Library are mandatory to verify no intervening publications have appeared.

---

## 5. Identified Methodological Patterns from Literature

### 5.1 Lessons for Our Framework Design

| Pattern Observed | Studies | Lesson for Our Study |
|---|---|---|
| Pre-split SMOTE/MICE leakage → inflated AUC | P0002, P0013, P0022, P0031 | All preprocessing on train fold only |
| Record-level splitting with patient overlap | P0001, P0004, P0012, P0015, P0024 | Enforce strict `PatientID`-grouped splitting |
| SHAP without AOPC = no faithfulness proof | P0002, P0011, P0016, P0020, P0021, P0022, P0031, P0036 | Mandatory AOPC deletion/insertion vs random |
| External validation rare | P0017 (13/15 internal), P0027 (83% internal), P0041 (64.7% internal) | Multi-center LOCO or temporal held-out |
| Calibration/DCA omitted | 22/29 studies | Report Brier, ECE, slope/intercept, DCA |
| Missing modality untested | 27/29 studies | Dedicated missing-modality degradation protocol |
| South Asian populations excluded | 0/29 with SA/BD cohort | Primary Bangladeshi cohort enrollment |

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

## 7. Recommendations for Next Steps

1. **STEP-009 (G03):** Present this synthesis and GAP0001–GAP0005 to supervisor for RQ ratification. Freeze research questions after supervisor approval.
2. **Supplementary searches:** Before G03, consider a targeted PubMed/Scopus search for "multimodal ECG clinical lifestyle cardiovascular SHAP" to verify no post-cutoff publications fill our gaps.
3. **STEP-010+:** Begin hospital site selection with explicit requirements for 4-modality data availability (12-lead ECG + clinical + lab + lifestyle questionnaire).
4. **Experiment design:** Use P0038 as the gold-standard design template (patient-level split + multi-center LOCO + blinded cardiologist review + DCA + missing-modality) adapted for accessible screening modalities.
