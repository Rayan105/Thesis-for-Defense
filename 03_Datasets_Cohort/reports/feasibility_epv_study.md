# Sample-Size Feasibility, Riley EPV Power Study, Site Selection Criteria & External Cohort Screening (`STEP-010`)

| Metadata | Value |
|---|---|
| Document | `03_Datasets_Cohort/reports/feasibility_epv_study.md` |
| Version | v1.0.0 (`Preparatory Technical Memo — Pending UD04/UD06/UD26 Resolution & G01/G03 Sign-Off`) |
| Step | STEP-010 (`Stage S05`) |
| Target Gate | Feeds **`G04`** (`Ethics/IRB, Cohort Intake & 4-Modality Quality`; requires `G01` & `G03` PASS prior to live patient intake) |
| Authors | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |
| Supervisor | Md. Mizanur Rahman (Senior Lecturer, Dept. of CSE, DIU) |
| Linked Decision Record | [DEC0003](../../01_Project_Management/decision_log/DEC0003.md) |
| Reproducibility Script | [compute_epv_feasibility.py](../../14_Automation/compute_epv_feasibility.py) |
| Governing Sections | OS §4.1–§4.5, §13 (`RISK0001, RISK0004, RISK0005`); Blueprint `STEP-010` |
| PHI Sensitivity | Tier 1 (Public / Git-safe) — Zero patient records or unapproved clinical data acquired |

---

## 1. Purpose and Epistemic Constraints

Per `RF09` (`fydp_title_proposal.pdf`, p. 4) and `OS §4.1`, zero primary hospital data may be collected or touched before IRB/ethics approval and site authorization (`STEP-011`). Because exact participating Bangladesh hospital(s), recruitment mechanism (`UD04`), ECG format (`UD07`), and observed prevalence remain **Unresolved / Human Decision Required**, this study executes:
1. Exact **Riley et al. (2020) `pmsampsize` and Hanley & McNeil (1982)** sample-size/precision calculations parameterized across realistic primary-screening and cardiology-outpatient regimes (`Section 2`).
2. Strict **Bangladesh Hospital & Diagnostic-Center Eligibility, ECG Format, and Spectrum-Bias Mitigation Criteria** (`Section 3`) — zero invented hospital counts or fake site approvals.
3. Systematic **Screening of `8` Published External Cohorts (`SITE0001–SITE0008` in [sites.csv](../sites.csv))** under `UD06` using verified `STEP-007` metadata (`Section 4`).
4. Prospective **Small-$N$ & Compute Contingency Thresholds (`UD26`)** protecting against deep Transformer overfitting on modest local enrollment (`Section 5`).

---

## 2. Prospective Sample Size, EPV & Statistical Power Analysis

### 2.1 Riley et al. (2020) Minimum Sample Size Calculations (`compute_epv_feasibility.py`)

Using Riley et al. (*BMJ* 2020;368:m441; *Stat Med* 2021) executed via [compute_epv_feasibility.py](../../14_Automation/compute_epv_feasibility.py), minimum required development cohort size $N_{\text{dev}} = \max(n_1, n_2, n_3)$ enforces:
- **$n_1$ (Global shrinkage $S \ge 0.90$):** Controls overfitting/predictor coefficient shrinkage: $n_1 = \lceil P / [(S-1)\ln(1 - R^2_{CS}/S)] \rceil$.
- **$n_2$ (Optimism $\le 0.05$ in Nagelkerke $R^2$):** Limits apparent-vs-adjusted $R^2$ inflation.
- **$n_3$ (Outcome proportion precision $\pm 0.05$):** Ensures 95% CI half-width $\le 0.05$ around prevalence $\phi$.

Anticipated **leakage-free discrimination** is anchored to our `STEP-008` literature synthesis (`synthesis.md` §5.2: `AUC 0.75–0.85` across Patient-Level / Unclear-or-Low PROBAST cohorts `P0005, P0025, P0038`), NOT the inflated `0.97–1.00` values from leaked High-PROBAST papers. Candidate predictor degrees of freedom $P$ span:
- **$P = 15$:** Compact Clinical + Lab + Lifestyle core / compressed unimodal summary tokens.
- **$P = 25$:** Realistic 4-modality screening dictionary + compact pretrained ECG risk projection (`~20` tabular df + `5` ECG embedding/interval df).
- **$P = 35$–$45$:** Rich tabular interactions/nonlinear splines + higher-rank multimodal fusion projection (`high-df` clinical + ECG features).

#### Table 1: Required Development Sample Size ($N_{\text{dev}}$) and CVD Events ($E_{\text{dev}}$) at Anticipated $\text{AUC} = 0.80$

| Setting / Outcome Prevalence ($\phi$) | Anticipated $R^2_{CS}$ (at $\text{AUC}=0.80$) | Candidate df ($P$) | $n_1$ (Shrinkage $S \ge 0.90$) | $n_2$ (Optimism $\le 0.05$) | $n_3$ (Prev $\pm 0.05$) | **$N_{\text{dev}}$ Required** | **$E_{\text{dev}}$ Events** | **Effective EPV** |
|---|---|---|---|---|---|---|---|---|
| **General Screening** ($\phi = 0.10$) | `0.1115` | `15` | `1,135` | `585` | `139` | **`1,135`** | **`114`** | `7.60` |
| **General Screening** ($\phi = 0.10$) | `0.1115` | `25` | `1,891` | `974` | `139` | **`1,891`** | **`190`** | `7.60` |
| **General Screening** ($\phi = 0.10$) | `0.1115` | `35` | `2,647` | `1,363` | `139` | **`2,647`** | **`265`** | `7.57` |
| **Preventive Clinic** ($\phi = 0.15$) | `0.1510` | `15` | `817` | `477` | `196` | **`817`** | **`123`** | `8.20` |
| **Preventive Clinic** ($\phi = 0.15$) | `0.1510` | `25` | `1,362` | `795` | `196` | **`1,362`** | **`205`** | `8.20` |
| **Preventive Clinic** ($\phi = 0.15$) | `0.1510` | `35` | `1,906` | `1,113` | `196` | **`1,906`** | **`286`** | `8.17` |
| **Cardiology OPD** ($\phi = 0.25$) | `0.2080` | `15` | `571` | `389` | `289` | **`571`** | **`143`** | `9.53` |
| **Cardiology OPD** ($\phi = 0.25$) | `0.2080` | `25` | `952` | `647` | `289` | **`952`** | **`238`** | `9.52` |
| **Cardiology OPD** ($\phi = 0.25$) | `0.2080` | `35` | `1,332` | `906` | `289` | **`1,332`** | **`333`** | `9.51` |
| **High-Risk Referral** ($\phi = 0.35$) | `0.2425` | `25` | `797` | `588` | `350` | **`797`** | **`279`** | `11.16` |
| **High-Risk Referral** ($\phi = 0.35$) | `0.2425` | `35` | `1,115` | `823` | `350` | **`1,115`** | **`391`** | `11.17` |

*(Conservative sensitivity at lower anticipated $\text{AUC} = 0.75, \phi = 0.25, P = 25$: $N_{\text{dev}} = 1{,}422$, $E_{\text{dev}} = 356$, effective $\text{EPV} = 14.24$; at optimistic $\text{AUC} = 0.85, \phi = 0.25, P = 25$: $N_{\text{dev}} = 664$, $E_{\text{dev}} = 166$. For deep neural architectures where effective parameter count exceeds tabular $P$, capacity must be strongly regularized via frozen/pretrained ECG representations, weight decay, and validation early stopping rather than counting raw neural weights against EPV.)*

### 2.2 Held-Out Test Precision & DeLong Comparison Power (`Hanley & McNeil 1982`)

#### Table 2: Held-Out Test Partition 95% CI Half-Width at $\text{ROC-AUC} = 0.80$

| Held-Out $N_{\text{test}}$ | $\phi = 0.15$ ($E_{\text{test}}$ / 95% CI Width) | $\phi = 0.25$ ($E_{\text{test}}$ / 95% CI Width) | $\phi = 0.35$ ($E_{\text{test}}$ / 95% CI Width) | Interpretation |
|---|---|---|---|---|
| `150` | `22` / `±0.115` (`[0.685, 0.915]`) | `38` / `±0.090` (`[0.710, 0.890]`) | `52` / `±0.080` (`[0.720, 0.880]`) | Severely underpowered for $\Delta\text{AUC} = 0.03$ |
| `250` | `38` / `±0.088` (`[0.712, 0.888]`) | `62` / `±0.071` (`[0.729, 0.871]`) | `88` / `±0.061` (`[0.739, 0.861]`) | Minimal acceptable single split with nested CV |
| **`400`** | `60` / `±0.070` (`[0.730, 0.870]`) | **`100` / `±0.056` (`[0.744, 0.856]`)** | **`140` / `±0.048` (`[0.752, 0.848]`)** | Recommended target minimum test partition |
| `600` | `90` / `±0.057` (`[0.743, 0.857]`) | `150` / `±0.045` (`[0.755, 0.845]`) | `210` / `±0.040` (`[0.760, 0.840]`) | Strong Q1 external / held-out calibration precision |

- **Combined Target Recommendation (`UD04`):** Under Cardiology OPD / Mixed Screening ($\phi \approx 0.25$), achieving $N_{\text{dev}} \approx 952$ (for $P=25$ df) plus a held-out test slice of $N_{\text{test}} \approx 300$–$400$ ($\ge 100$ test events) sets an ideal total sample target of **$N_{\text{total}} \approx 1{,}250$–$1{,}500$ unique adult patients ($E \ge 300$–$350$ confirmed CVD events)**.
- **If $N_{\text{total}} < 1{,}500$ (`OS §4.4 Option B`):** Mandatory activation of **repeated nested $K$-fold cross-validation (`5×5`)** or stratified held-out test paired with inner CV (`UD11/UD26`) so hyperparameter selection and calibration fit stay isolated without sacrificing `75%` of statistical power!

---

## 3. Primary Bangladesh Site Eligibility, Spectrum-Bias Mitigation & ECG Format Audit Protocol (`UD04`, `UD07`)

*(Zero Bangladeshi hospitals are currently approved or contracted; primary sites will be appended as `SITE0009+` in [sites.csv](../sites.csv) only after field feasibility assessment and written custodian liaison during `STEP-010–011`.)*

### 3.1 Candidate Site Types in Bangladesh & Mandatory Screening Checklist

| Candidate Site Profile | Expected Strengths | High-Risk Failure Modes to Verify Before Selection | Mandatory Pre-Selection Audit Item (`UD04 / UD07`) |
|---|---|---|---|
| **Type A: Specialized Cardiac Hospitals / Institutes** *(e.g., National Heart Foundation, NICVD, Chest/Cardiac referral OPDs)* | High CVD event volume, specialist cardiologists available for adjudication (`UD09`), likely 12-lead ECG & troponin/lipid labs | **Referral/Spectrum bias** (severe acute cases dominating, missing asymptomatic early screening controls); paper-only archived ECGs | Check if **consecutive Outpatient Cardiology / Preventive Checkup** unit has BOTH CVD+ and confirmed CVD− workups (`not` acute CCU cases vs university healthy controls!) |
| **Type B: Multi-Specialty Tertiary Medical College Hospitals** *(e.g., Medicine + Cardiology + Preventive Checkup clinics)* | Balanced spectrum across diabetes, hypertension, chest pain evaluation, and preventive checkups; IRB committees in place | Fragmented EHR vs paper charts; inconsistent ECG devices across wards | Verify ability to link `PatientID` deterministically across Medicine/Cardiology OPD, Biochemistry Lab, and ECG Machine within $\Delta t$ (`UD03`) |
| **Type C: Accredited Diagnostic & Preventive Health Screening Centers** *(Dhaka/Savar/Gazipur hubs)* | Digital LIS biochemistry (`Glucose, HbA1c, Lipid profile, Creatinine`), uniform calibration, rapid turnaround, large healthy + subclinical screening pool | Missing longitudinal clinical outcome adjudication; may only have paper/thermal ECG strips | Confirm digital ECG raw XML/PDF-vector/SCP/DICOM export capability AND arrange cardiologist outcome adjudication via echocardiogram/angiography/referral follow-up |

### 3.2 Spectrum-Bias Guardrails (PROBAST Domain 1 Compliance)

Following findings from `STEP-007/008` (`P0001, P0006, P0021, P0032` rated High PROBAST due to spectrum bias):
1. **Consecutive or Site-Matched Recruitment:** Cases (`CVD+`) and controls (`CVD−`) MUST originate from the **same target clinical pathway and recruitment window** (e.g., consecutive adult patients $\ge 18$ years undergoing diagnostic/preventive cardiovascular evaluation). **Strictly prohibited:** sampling acute inpatient CCU myocardial infarction cases alongside asymptomatic healthy student/staff volunteers!
2. **Confirmed Negative Definition:** Non-CVD controls must have verified clinical absence of CVD under documented clinical/ECG/diagnostic assessment (`not` merely *"no ICD code recorded"*).
3. **Multi-Center Advantage (`UD04`):** If two centers are accessible (`e.g.,` one tertiary cardiac OPD + one regional diagnostic screening center), reserve site stratification or Leave-One-Site-Out sensitivity (`similar to P0007 / P0038`) rather than pooling blindly with unrecorded site artifacts (which create spurious shortcuts under `G14`).

### 3.3 Early ECG Acquisition Format Check (`UD07` Pre-Screen)

| ECG Acquisition Tier | Data Quality & Q1 Viability | Mandatory Protocol If Encountered at Site |
|---|---|---|
| **Tier 1 (Preferred): Native Digital 12-Lead Waveforms** (`XML, DICOM-ECG, SCP-ECG, WFDB, CSV @ 250–500 Hz`) | Optimal (`10 s × 12 leads`); enables full 1D-CNN/ResNet/Transformer waveform learning + beat/lead SHAP overlays + `50 Hz` Bangladesh PLI verification | Inspect 5–10 anonymized sample files for header PHI (names/MRNs in XML tags!) and `50 Hz` notch behavior |
| **Tier 2 (Contingency): High-Res Scanned Paper ECG Strips** ($\ge 300\text{ DPI}$) | Requires validated digitization pipeline (`grid removal + signal tracing + calibration check`) — note `P0028` column-averaging errors and image biases | Must pass `10%` visual/quantitative correlation validation (digitized HR/QRS/QT vs machine printout) before `G04/G08`; avoid raw photo classifiers trained on hospital paper grid color! |
| **Tier 3 (Unacceptable Alone): Printout Interval Summary Numbers Only** (`HR, PR, QRS, QTc` without waveforms) | Reduces study to purely tabular EHR, undermining ECG deep learning benchmarking (`RF05`) | Reject site as standalone primary ECG source unless digital/scanned strips are obtainable; retain intervals only as secondary ablation features |

---

## 4. Screening of External Public & Credentialed Cohorts (`UD06`, Registered in `sites.csv`)

We screened **`8` real datasets (`SITE0001–SITE0008`)** encountered across our `42`-paper curated corpus for modality overlap, clinical compatibility, access licensing, South Asian relevance, and anti-leakage hygiene (`OS §4.1, STEP-010` #3):

1. **`SITE0001` — PTB-XL (`Germany, PhysioNet Open CC-BY 4.0`, `21,837` 12-lead 500/100Hz WFDB ECGs across `18,885` pts, `P0014`):**
   - *Decision:* **`Candidate_ECG_Pretraining_Only`**. Contains clean raw 12-lead ECG + basic clinical meta (`age, sex, height, weight`), zero Lab assays, zero Lifestyle. Directly recommended under **`UD26`** for **self-supervised or multi-label supervised 12-lead ECG backbone pretraining** (and unimodal ECG fine-tuning) if primary BD cohort $N < 1{,}500$. Cannot serve as 4-modality external validation (`P0018 §4.4` explicitly cites PTB-XL's lack of South Asian diversity).
2. **`SITE0002` — MIMIC-IV + MIMIC-IV-ECG (`USA, PhysioNet Credentialed`, `127,994` pts / `385,480` ECGs in `P0024`, `10s 500Hz WFDB`):**
   - *Decision:* **`Candidate_External_Benchmark_PartialOverlap`**. Closest public dataset supporting **3 of 4 modalities** (`Clinical + 12-lead ECG + Laboratory/Biomarkers`), with `3.05%` broad Asian ethnicity (`P0024 Table 1 p. 5`), requiring CITI human-subjects training and PhysioNet DUA (`STEP-011`). **Critical limitation:** Lacks structured multi-item Lifestyle variables (Diet/Physical Activity/Sleep), represents US critical-care/ED severity rather than outpatient Bangladesh primary screening, and requires patient-level deduplication by `subject_id` (addressing `P0001` / `P0012` record-level leaks).
3. **`SITE0003` — EchoNext Mini-Model Dataset (`USA, PhysioNet Credentialed`, `100,000` ECGs, `P0011`):**
   - *Decision:* **`Deferred_LowPriority`**. Provides ECG waveforms (`12×2500`) + tabular metadata + SHD labels, but omits Labs and Lifestyle, omits unique patient counts/split proofs (`most_recent_ecg` alert in `P0011`), and narrows outcome purely to echocardiographic SHD.
4. **`SITE0004` (`BIDMC/CODE-15%`), `SITE0005` (`ARIC`), `SITE0006` (`UK Biobank`), `SITE0007` (`CAIR-CVD-2025`), `SITE0008` (`Khan ECG Images`):**
   - *Decision:* **`Rejected` for primary/external 4-modality adoption** due to unimodal-only inputs (`SITE0004, SITE0008`), paid/BioLINCC approval turnaround + `0%` South Asian ancestry (`SITE0005, SITE0006`), or complete absence of raw ECG waveforms + undisclosed provenance (`SITE0007`: `CAIR-CVD-2025` is strictly tabular clinical/lab/lifestyle with `0` raw ECG waveforms, useful only to contextualize Bangladeshi regional literature gaps in `CLAIM0003`).

> [!IMPORTANT]
> **Strict Lawful Custody Rule (`STEP-010`):** Zero datasets from `SITE0001–SITE0008` have been downloaded or unpacked into `03_Datasets_Cohort/` yet. Any credentialed dataset (`MIMIC-IV`, `EchoNext`) strictly awaits `UD06` approval and CITI/DUA verification in `STEP-011`.

---

## 5. Prospective Small-$N$ & Compute Contingency Plan (`UD26`)

Because Q1 medical-AI review penalizes post-hoc architectural switching after inspecting test scores (`Blueprint §650`), pre-register binding capacity tiers **before** seeing primary cohort splits:

| Measured Primary Cohort Regime (`UD26`) | EPV / Statistical Reality | Mandatory Modeling & Validation Contingency Protocol |
|---|---|---|
| **Tier A: $N_{\text{total}} \ge 1{,}500$ and $E \ge 350$** | Satisfies Riley `N_dev` ($P \le 35$ df) + held-out $N_{\text{test}} \ge 300$ | Stratified patient-grouped `70/15/15` (or `60/20/20`) fixed split + full Tier 1–4 Transformer fusion trained multi-seed (`S ≥ 5`) + optional `MIMIC-IV-ECG` partial-overlap benchmark |
| **Tier B: $500 \le N_{\text{total}} < 1{,}500$ or $120 \le E < 350$** *(Realistic FYDP target regime)* | Training full ECG ResNet/Transformer from scratch risks severe overfitting | **Activate `UD26-B`:** (1) Transfer-learn / pretrain ECG encoder on **`PTB-XL` (`SITE0001`, parameter-efficient fine-tuning or frozen + low-rank adapter)**; (2) Compact tabular/lifestyle token projection (`d ≤ 64`, 1–2 cross-attention layers, strong dropout/weight decay); (3) **Outer 5-fold stratified patient-grouped CV** (or `20%` sealed holdout + `5-fold` inner CV per `OS §4.4 Option B`) + explicit fair competition against tuned GBDT baselines |
| **Tier C: $N_{\text{total}} < 500$ or $E < 120$** *(Severe enrollment bottleneck)* | Single site small-$N$ cannot power deep end-to-end multimodal Transformer | **Activate `UD26-C`:** (1) Immediate multi-center recruitment expansion OR adopt `MIMIC-IV + MIMIC-IV-ECG` (`SITE0002`) under `UD06` for primary Clinical+ECG+Lab deep modeling alongside primary BD cohort validation; (2) On primary small-$N$, restrict Transformer to frozen pretrained ECG embeddings + low-dim regularized late/gated fusion benchmarked transparently against Ridge/Logistic/XGBoost with honest small-$N$ power caveats |
