# Preregistered Evaluation, Calibration, Statistical Inference & DCA Protocol (`STEP-025` / `UD16–UD18`, `UD24`)

| Field | Value |
|---|---|
| Document | `09_Evaluation_Stats/protocol.md` |
| Version | v1.0.0 (`Pre-Training Frozen Statistical & Clinical Utility Contract`) |
| Step / Stage | `STEP-025` / `Stage S10` (Unsealed Execution Strictly Post-`G11` at `STEP-034–036`) |
| Date | `2026-11-27` |
| Leads | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |
| Reviewer | Md. Mizanur Rahman |
| Governing Section | OS §7.1–§7.5, §12.1 (`UD16–UD18`, `UD24`); Blueprint `STEP-025` |

---

## 1. Test-Set Freeze & Zero-Tuning Rule (`OS §7.1`)
- `REL0001 Test` (`12,719` rows; SHA-256 `a01d9338fe4c...21e3d`) stays **sealed under `TACC0001`** throughout Stages `S10–S11`.
- Champion selection (`G11`), calibrator fitting, and operating threshold $\tau$ tuning run **strictly on `REL0001 Validation` (`12,724` rows) or inner `Train` OOF folds**. Never tune $\tau$ or architecture after reading Test metrics.

---

## 2. Complete Metric Hierarchy (`UD16`)

### 2.1 Mandatory Six Proposal Metrics (`RF12`)
All frozen models MUST report exact test values at frozen threshold $\tau$ (plus `[TN, FP; FN, TP]` integers):
1. **Accuracy:** $(\text{TP}+\text{TN})/(\text{TP}+\text{TN}+\text{FP}+\text{FN})$ alongside majority baseline.
2. **Precision (PPV):** $\text{TP}/(\text{TP}+\text{FP})$ (`N/A` if denominator `0`).
3. **Recall (Sensitivity):** $\text{TP}/(\text{TP}+\text{FN})$.
4. **F1-Score:** $2 \cdot \text{Precision} \cdot \text{Recall} / (\text{Precision}+\text{Recall})$.
5. **ROC-AUC (AUROC):** Mann-Whitney / trapezoidal AUROC over continuous calibrated risk scores.
6. **Confusion Matrix:** Exact raw `[[TN, FP], [FN, TP]]` covering `100%` of scheduled Test encounters (`0` silent drops).

### 2.2 Q1 Clinical & Imbalance-Sensitive Extensions
1. **Discrimination:** **PR-AUC (AUPRC)** paired with exact cohort positive prevalence baseline, **Specificity**, **NPV**, **Balanced Accuracy**, and **Matthews Correlation Coefficient (MCC)**.
2. **Probability Calibration (`Critical for Early Risk Prediction`):**
   - **Brier Score** + **Brier Skill Score (`BSS`)** vs prevalence baseline;
   - **Expected Calibration Error (`ECE`)** using **`15` quantile bins** (primary, equal sample mass per bin) plus `15` equal-width bins sensitivity;
   - **Calibration Slope** (ideal `= 1.0`) & **Calibration-in-the-Large / Intercept** (ideal `= 0.0`) via logistic recalibration $\text{logit}(y) = \alpha + \beta \cdot \text{logit}(\hat{p})$, rendered as reliability curves pre- and post-calibration.

---

## 3. Post-Hoc Calibration & Operating Threshold Rules (`UD16`, `UD24`)
- **Validation Calibrator Candidate Selection (`STEP-032`):** Compare `Uncalibrated`, `Temperature Scaling` (`1`-param scalar $T$ on validation logits), `Platt Logistic Recalibration`, and `Isotonic Regression` strictly on `REL0001 Validation` minimizing **Validation Brier Score + ECE** (`defaulting to Temperature Scaling for neural models if Validation N is tight, e.g. DS0002 N_val=84`).
- **Frozen Operating Thresholds ($\tau$):** Lock TWO prespecified operating points strictly on `Validation`:
  - **Primary Operating Threshold ($\tau_J$):** Maximizing Youden's $J = \text{Sensitivity} + \text{Specificity} - 1$ on Validation.
  - **Clinical High-Sensitivity Screening Threshold ($\tau_{0.85}$):** Minimum threshold achieving **`Sensitivity >= 0.85`** on Validation (`evaluates ED rule-out safety where missed cardiac cases carry high clinical cost`).

---

## 4. Decision Curve Analysis (`DCA` — `UD17`)
- Evaluate **Clinical Net Benefit** across threshold probabilities **$p_t \in [0.05, 0.50]$** (`step = 0.01`) on calibrated probabilities:
  $$\text{NB}(p_t) = \frac{\text{TP}(p_t)}{N} - \frac{\text{FP}(p_t)}{N} \cdot \left(\frac{p_t}{1 - p_t}\right)$$
- Compare Champion `CVD-MM-Transformer` vs best Unimodal Baseline vs Simple Fusion vs **`Treat/Screen All`** vs **`Treat/Screen None`**. *(Clinical DCA window `[5%–50%]` covers preventive `CAIR/sulianova` screening thresholds `[5%–25%]` AND acute ED `CARDIO-ML-ED` rule-in `[20%–50%]`, transparently noted for final cardiologist review at `G14`.)*

---

## 5. Statistical Uncertainty, Hypothesis Tests & Multiplicity (`UD18`)
1. **Confidence Intervals:** **`B = 2,000`** **patient-level stratified bootstrap resamples** (`resampling PatientGroupIDs with replacement`, fixed seed `20261127`) computing percentile `95%` CIs for ROC-AUC, PR-AUC, F1, Accuracy, Sensitivity, Specificity, Brier, and ECE. Explicitly keep finite-sample CIs separate from multi-seed training variance (`5` seeds mean $\pm$ SD).
2. **Paired Hypothesis Tests (Identical Test Patients):**
   - **DeLong's Two-Sided Paired Test** for ROC-AUC differences (`Champion Fusion vs Best Unimodal / Simple Fusion`).
   - **Paired Patient Bootstrap Difference Test (`B = 2,000`)** for $\Delta \text{PR-AUC}$, $\Delta \text{Brier}$, and $\Delta \text{DCA NB}(p_t)$ at primary $p_t \in \{0.10, 0.20, 0.30\}$.
   - **McNemar's Exact Test** on binary classification discordance at frozen $\tau_J$.
3. **Multiple-Comparison Control:** Apply **Holm-Bonferroni step-down adjustment** (primary family: `Champion Fusion vs each Block A/C/D comparator`, $\alpha = 0.05$) and report both raw $p$-values and adjusted $p_{\text{adj}}$! Never assert statistical superiority from point estimates alone.

---

## 6. Subgroup Fairness & PROBAST-AI Audit Plan (`STEP-037` / `G13`)
Stratify frozen Test performance and calibration cleanly across:
1. **Sex (`F` vs `M`)**; 2. **Age Bands (`18–44y`, `45–64y`, `>=65y`)**; 3. **Origin Cohort (`DS0001`–`DS0004`)**; 4. **Modality Tier (`C+E_png+L` vs `C+L_[MISSING_ECG]` in `DS0002`, `C+E_wfdb`, `C+L+S`)**, explicitly flagging small-$N$ CI uncertainty alongside **PROBAST-AI** self-audit of Domains 1–4.
