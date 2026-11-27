# Four-Tier Baseline & Comparator Suite Specification (`STEP-023` / `UD14`)

| Field | Value |
|---|---|
| Document | `06_Models_Fusion/baseline_plan.md` |
| Version | v1.0.0 (`UD14` Approved Comparator Plan) |
| Step / Stage | `STEP-023` / `Stage S10` (`G09` Pre-Execution Lock) |
| Date | `2026-11-27` |
| Framework Lock (`UD13`) | **PyTorch (`torch >= 2.1`)** + `scikit-learn` + `xgboost` (`LightGBM` companion) |
| Source Release | `REL0001` (`91,781` encounters / `89,005` patients; `66,338` Train / `12,724` Val / `12,719` Test) |
| Governing Section | OS §6.2–§6.5, §12.1 (`UD13`, `UD14`); Blueprint `STEP-023` |
| PHI Sensitivity | Tier 1 (Public / Git-safe) |

---

## 1. Literature Audit Basis (`P0001–P0042` Comparative Synthesis)
Across our `42` verified papers (`29` Original Empirical Studies + `13` Reviews):
- **Classical ML & Tabular Baselines (`P0001, P0005, P0010, P0020, P0021, P0031, P0040`):** Logistic Regression, Random Forest (`pooled AUC 0.865` in `P0010`), SVM, and XGBoost remain competitive on structured Clinical/Lab EHR features and are mandatory baselines before claiming any deep learning gain.
- **ECG Encoders (`P0001–P0029, P0033, P0041`):** 1D-CNN / ResNet-1D (`57.6%` of DL-ECG studies in `P0041`; e.g., `P0003`, `P0005` SEER, `P0011`, `P0020`), Conv-BiLSTM-Attention (`P0002`, `P0007`), 2D ViT / MedCLIP (`P0006`, `P0008`, `P0021` for 12-lead ECG images), `S4` (`P0024`), and $\beta$-VAE (`P0023`, `P0031`, `P0033`).
- **Fusion Trends (`P0017`, `P0012–P0016`, `P0036–P0039`):** Late score fusion dominates (`10/15` studies in `P0017`), followed by simple feature concatenation (`P0002, P0003, P0020, P0031`) and cross-modal attention (`P0012` CaMPNet, `P0014` MAF-Net, `P0016` ChemoCardioNet, `P0038` MAIS).
- **Critical Flaws Avoided (`25/29` PROBAST High Risk):** Our suite enforces **zero pre-split SMOTE/scaling**, **strict `PatientGroupID` isolation**, **explicit calibration (`Brier`, `ECE`, `Slope`) + DCA**, and **quantitatively faithful SHAP (`AOPC` + multi-seed stability + cardiologist plausibility)** — fixing the exact failures found across `86.2%` of reviewed primary papers!

---

## 2. Canonical Four-Tier Model Suite (`Block A–F` Parity)

### Tier 1 — Unimodal Baselines (Proposal Families + Literature Backbones)
Trained separately per available modality (`Clinical-only`, `Lab-only`, `Lifestyle-only`, `ECG-only`) using identical `REL0001` `Train` (`66,338`) and `Val` (`12,724`) partitions (`Train pos_weight`, **no SMOTE**):
1. **`MC0001` Logistic Regression (`L2`):** Interpretable clinical linear baseline on tabular blocks (`DS0001–04`).
2. **`MC0002` Random Forest (`n_estimators=300`, balanced class weight):** Non-linear tree ensemble with exact `TreeSHAP` reference.
3. **`MC0003` SVM (`RBF Kernel` + Validation Platt Calibration):** Non-linear margin baseline matching proposal spec (`RF08`).
4. **`MC0004` XGBoost (`binary:logistic`, `scale_pos_weight=pos_weight`) + `MC0005` LightGBM:** Primary gradient-boosted tabular comparators cleanly consuming `_isnan` MNAR flags.
5. **`MC0006` Unimodal Tabular MLP:** Compact PyTorch dense network matching fusion tokenizer capacity (`hidden=[64, 32]`, Dropout `0.3`).
6. **`MC0007` Compact 1D-ResNet (`PyTorch`):** Unimodal digital ECG baseline for `DS0001 PTB-XL` (`(12, 5000)` / `(12, 1000)` WFDB waveforms).
7. **`MC0008` Conv1D-BiLSTM (`PyTorch`):** Sequential recurrent ECG baseline fulfilling proposal `LSTM` requirement (`P0002/P0007` comparator).
8. **`MC0009` Compact 2D-CNN / ResNet-18 Image Encoder (`PyTorch`):** Unimodal ECG vision encoder for `DS0002 CARDIO-ML-ED` cleaned `.png` scans (`(1, 256, 768)`).
9. **`MC0010` ECG Temporal Patch Transformer (`PyTorch`):** Unimodal ECG self-attention baseline isolating whether Transformer gains come from ECG self-attention alone vs cross-modal fusion.

### Tier 2 — Clinical Risk Score Comparator (`Context-Only Baseline`)
- **`MC0011` Framingham / WHO South Asia / ASCVD Linear Covariate Reference:** Computed on overlapping compatible clinical/lab variables (`Age, Sex, SBP, Total Cholesterol, HDL, Smoking, Diabetes`).
  - **Clinical Boundary Disclosure (`STEP-014`):** `DS0002–DS0004` endpoints are cross-sectional diagnostic/risk strata rather than longitudinal 10-year incident MI/stroke survival cohorts (`endpoint_charter.md`); therefore `MC0011` is benchmarked purely as a **discrimination & DCA contextual comparator (`ROC-AUC`, rank correlation)** without asserting calibrated 10-year prognostic horizon parity.

### Tier 3 — Simple Multimodal Fusion Baselines (`Required Q1 Ablation Gates`)
Every Q1 reviewer checks whether deep cross-attention actually outperforms simple fusion:
1. **`MC0012` Early Feature Concatenation + XGBoost / Concat-MLP:** Concatenates `Clinical + Lab + Lifestyle` tabular vectors with extracted `1D/2D ECG` pooled embeddings (`or zero-masked indicator for ECG-absent cohorts`) -> `XGBoost` & `2-layer MLP`.
2. **`MC0013` Late Probability Ensemble / Calibrated Stacking (`OOF Logistic Regression`):** Combines independent modality out-of-fold probabilities weighted cleanly by available modalities (`P0017` dominant late-fusion comparator).
3. **`MC0014` Gated Attention Intermediate Fusion:** Modality-specific linear projections + sigmoid gating weights (`alpha_m`, `P0011/P0036`-inspired) without full multi-head Transformer cross-attention.

### Tier 4 — Proposed Architecture (`MC0015`: `CVD-MM-Transformer`)
- **Cross-Modal Transformer Fusion Network** detailed in [transformer_fusion_spec.md](file:///e:/FYDP/06_Models_Fusion/architectures/transformer_fusion_spec.md) (`d_model=64`, `2` layers, `4` heads, native `ModalityMask_CELS` key-padding masking, missing-modality dropout regularization, per-cohort projection adapters, and joint `PyTorch` Captum/GradientSHAP + AOPC audit compatibility).

---

## 3. Experimental Block Mapping (`OS §6.5` Preview for `STEP-025`)
- **Block A (`Unimodal`):** `MC0001–MC0010` across `DS0001–04`.
- **Block B (`Clinical Score Context`):** `MC0011` on `DS0003` (`CAIR`) & `DS0004` (`sulianova`).
- **Block C (`Fusion Hierarchy`):** `MC0012` Early Concat, `MC0013` Late Ensemble, `MC0014` Gated Fusion vs **`MC0015` `CVD-MM-Transformer`** on paired `DS0002` (`C+E_png+L`), `DS0001` (`C+E_wfdb`), `DS0003–04` (`C+L+S`), and unified `REL0001` multi-cohort training!
- **Block D (`Progressive & LOMO Lifestyle Ablations — RQ2`):** Tests `C -> C+L -> C+L+S` (`DS0003/04`) & `C+L -> C+E+L` (`DS0002`), plus Leave-One-Modality-Out (`-Clinical`, `-ECG`, `-Lab`, `-Lifestyle`).
- **Block E & F (`Mechanism & Stress Tests`):** Missing-modality masking ablation (`with vs without mask`), multi-seed repeats (`>= 5` seeds), missing-ECG test-time stress test on `DS0002`'s `226` `C+L_[MISSING_ECG]` encounters, and `Prior_CABG` sensitivity run!
