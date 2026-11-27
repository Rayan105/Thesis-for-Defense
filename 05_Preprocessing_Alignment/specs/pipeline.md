# Multimodal Leakage-Free Preprocessing & Signal Contract (`STEP-019`)

| Field | Value |
|---|---|
| Document | `05_Preprocessing_Alignment/specs/pipeline.md` |
| Version | v1.0.0 (`UD12` Architecture Spec) |
| Step / Stage | `STEP-019` / `Stage S09` (Preparation for `STEP-020–022` / `G07–G08`) |
| Date | `2026-11-27` |
| Authors | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Reviewer | Md. Mizanur Rahman + Clinical/ECG Reviewer (`TBD` prior to `G08`) |
| Source Releases | `ADJ0001–ADJ0004` (`91,781` Clean Eligible Encounters), `variables.csv v1.0.1`, `ecg_contract.md v1.0.0` |
| Config Reference | `05_Preprocessing_Alignment/configs/pp_v1_0_0_spec.yaml` |
| Reusable Modules | `src/cvd_mm/preprocessing.py`, `src/cvd_mm/ecg.py`, `src/cvd_mm/schema_ecg.py` |
| Kaggle Companion | `05_Preprocessing_Alignment/notebooks/CVD_Multimodal_Kaggle_Preprocessing_Pipeline.ipynb` |

---

## 1. Reconciliation of Proposal Diagram (`RF13`) vs Operational Leakage Wall (`OS §4.4`)

Proposal Figure 1 (`fydp_title_proposal.pdf`, p. 5) conceptually places *Data Preprocessing* and *Feature Extraction* prior to *Train / Validation / Test Split*. Because fitting any population scaler, imputer, encoder, or oversampler on combined data leaks validation/test distributions into training parameters (an automatic PROBAST-AI high-risk failure mode), this specification strictly decouples every operation into **Stage A (Pre-Split Record-Local)** and **Stage B (Post-Split Training-Only)**:

```text
ADJ0001..ADJ0004 (Verified Eligible Records, N=91,781 across 4 cohorts)
   │
   ▼  [STAGE A — Strictly Record-Local Deterministic Ops ONLY (STEP-019)]
   │  • Zero dataset-level means, medians, variances, quantiles, or encoders computed
   │  • Unit transforms (age_days / 365.25; Height_m * 100), BMI formula, schema guards
   │  • WFDB mV gain decode + fixed zero-phase 50 Hz notch + <=0.5 Hz baseline removal
   │  • CARDIO-ML-ED PNG 90-deg rotate + RGB red-grid removal + letterbox resize
   │  • Tier-A leakage barrier (rejects Troponin-I Tier-B, CVD Risk Score, outcomes)
   │
   ▼  [LOCKED PATIENT-GROUPED SPLIT — STEP-020 / Gate G07]
   │  • Partition by PatientGroupID (zero patient overlap; PTB-XL strat_fold 1-8/9/10)
   │  • Final Test partition formally SEALED (0 reads permitted during fitting/tuning)
   │
   ▼  [STAGE B — Training-Partition-Only Fitted Ops (STEP-021)]
   │  • Generate feature missingness masks (_isnan) BEFORE imputing (MNAR signal)
   │  • Fit Imputers (Median / Iterative MICE), RobustScaler, OneHotEncoder ONLY on Train
   │  • Serialize fitted parameters -> FitStateHash (SHA-256)
   │  • Apply frozen transforms unchanged to Val & Test (.transform only)
   │  • Emit 4D Modality Presence Mask: [has_clinical, has_ecg, has_lab, has_lifestyle]
   │  • Zero pre-split SMOTE (use Train-computed class_weight / pos_weight in S10-S11)
```

---

## 2. Modality-Specific Technical Pipeline Details

### 2.1 Modality 1 (`Clinical`) & Modality 3 (`Laboratory`) & Modality 4 (`Lifestyle`)
1. **Stage A (Record-Local):**
   - `age_years`: `age_days / 365.25` (`DS0004`); native years verified `>= 18.0` (`DS0001–03`).
   - `bmi_kgm2`: `weight_kg / (height_m ** 2)` whenever valid anthropometric bounds hold.
   - `sex`: standardized `'F'` / `'M'` (`DS0004: 1 -> F, 2 -> M`).
   - **Prohibited Features Enforced (`assert_no_leakage_predictors`):** `CVD Risk Score`, `Blood Pressure Category`, `Initial diagnosis`, `Final diagnosis`, `Death`, `ECG Labels`, `scp_codes`, `Troponine - I (Q)` under primary **`Tier A`**, plus grouping keys (`RecordID`, `PatientGroupID`).
   - **Unit Isolation Invariant:** Continuous lipid/glucose values in `DS0003 CAIR` (`mg/dL`) are kept cleanly separated from coarse ordinal tiers `1–3` in `DS0004 sulianova` (`never conflated into shared scaler columns`).
2. **Stage B (Train-Only Fitted):**
   - **MNAR Missingness Masks:** Compute binary `{col}_isnan` (`1.0` if missing, `0.0` if observed) BEFORE imputation so clinical lab-ordering patterns (`e.g. missing Cr 20.4% or WBC 17.1% in ADJ0002`) stay explicit and auditable at `G14` SHAP shortcut checks.
   - **Imputation:** Fit `IterativeImputer` (`MICE` on continuous labs/vitals in Kaggle/Phase-2) and exact **Train Median** fallback (`src/cvd_mm/preprocessing.py`) strictly on `Train`. Missing whole modalities are NEVER filled with synthetic medians inside unseen cohorts — instead gated cleanly by `modality_mask = 0`.
   - **Scaling:** Fit **`RobustScaler` (`(x - median_train) / IQR_train`)** on Train numeric features (`resists heavy clinical lab skew better than z-score`) + Train-only categorical `OneHotEncoder(handle_unknown='ignore')` (`Family History` kept in `Lifestyle` per `RF10` with sensitivity ablation index).

### 2.2 Modality 2A — Digital 12-Lead WFDB Signals (`DS0001 PTB-XL`)
1. **ADC Decoding:** Raw `int16` little-endian `.dat` buffers scaled deterministically using `.hea` per-lead gain (`mV`).
2. **Zero-Phase 50 Hz Powerline Notch:** Second-order IIR biquad notch filter ($f_0 = 50.0\text{ Hz}$, quality factor $Q = 30.0$, zero-phase forward-backward `filtfilt`), removing AC mains hum across `500 Hz` waveforms (and safely no-oping at `100 Hz` Nyquist $= 50\text{ Hz}$ where aliasing/cutoff sits at Nyquist edge — explicitly handled by condition `fs_hz > 2.2 * notch_hz` so Nyquist instability never triggers!).
3. **ST-T Morphology-Safe Baseline Wander Removal:** Zero-phase `2nd-order` high-pass filter at **`0.5 Hz` (`<= 0.5 Hz` cutoff ceiling per `OS §4.5`)**, removing low-frequency respiratory drift (`~0.1–0.3 Hz`) **without** attenuating diagnostic ST-segment elevation/depression, J-point shifts, or T-wave inversions (which frequencies near `1–2 Hz` high-pass filters visibly distort).
4. **Normalization:** Record-local robust/z-score amplitude normalization OR Train-only per-lead scale (`UD12 Option A`: per-record standardization inside fixed dynamic clip `[-10 mV, +10 mV]` so lead voltage morphology across channels remains preserved while avoiding batch leakage).

### 2.3 Modality 2B — Digitized 12-Row Paper ECG Images (`DS0002 CARDIO-ML-ED`)
1. **Isolated Clean Scope (`RISK0012`):** Strictly uses verified cropped `.png` images (`329` eligible encounters / `323` unique patients); the `8` uncropped `.jpg` 6-lead strips stay excluded.
2. **Deterministic Geometric & Color Cleaning (`Stage A`):**
   - **Orientation Check:** Because `.png` scans are portrait-rotated (`height > width`), apply deterministic `90°` counter-clockwise rotation (`cv2.ROTATE_90_COUNTERCLOCKWISE`) so time progresses left-to-right across all 12 trace rows.
   - **Red-Grid Ink Isolation:** Suppress red/pink millimeter graph paper pixels (`high R relative to G & B`) while preserving dark trace ink via luminance/chromatic separation (`suppress_red_ecg_grid_rgb`), turning paper background clean light while keeping QRS complexes dark and high-contrast.
   - **Aspect-Preserving Letterbox Resize:** Pad and resize uniformly (e.g., `256 × 768` or `224 × 672` RGB/grayscale) without squishing cardiac timing ratios, followed by Train-only channel normalization in Stage B.

### 2.4 Missing-Modality Cross-Attention Mask & Imbalance Rule (`UD10 / UD12`)
- Every patient tensor exports **`modality_mask = [has_clinical, has_ecg, has_lab, has_lifestyle]`**:
  - `ADJ0001` (`PTB-XL`): `[1, 1, 0, 0]` (`ECG + partial Clinical`)
  - `ADJ0002` (`CARDIO-ML-ED`): `[1, 1, 1, 0]` (`329 C+E_png+L` rows) or `[1, 0, 1, 0]` (`226 C+L [MISSING_ECG]`)
  - `ADJ0003` (`CAIR-CVD-2025`): `[1, 0, 1, 1]` (`BD C+L+S [MISSING_ECG]`)
  - `ADJ0004` (`sulianova`): `[1, 0, 1, 1]` (`70K-clean C+L_ord+S [MISSING_ECG]`)
- **Zero Pre-Split Oversampling:** `SMOTE` is barred prior to `STEP-020`. Training models use validation-tuned class weights (`pos_weight = n_neg_train / n_pos_train`) preserving calibrated baseline risk priors (`OS §4.5 #4`).
