# Controlled Q1 Experiment & Ablation Plan (`STEP-025` / `UD15`)

| Field | Value |
|---|---|
| Document | `07_Experiments/experiment_plan.md` |
| Version | v1.0.0 (`Frozen Pre-Training Preregistration`) |
| Step / Stage | `STEP-025` / `Stage S10` (`G09` Prereq) |
| Date | `2026-11-27` |
| Owners | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Reviewer | Md. Mizanur Rahman |
| Source Release | `REL0001` (`91,781` Encounters: `66,338` Train / `12,724` Val / `12,719` Sealed Test) |
| Candidates Spec | [candidates.csv](../06_Models_Fusion/candidates.csv), [baseline_plan.md](../06_Models_Fusion/baseline_plan.md), [transformer_fusion_spec.md](../06_Models_Fusion/architectures/transformer_fusion_spec.md) |
| Governing Section | OS §6.5, §12.1 (`UD15`); Blueprint `STEP-025` |

---

## 1. Fair Comparison Invariants (`OS §6.2 & §6.5`)
1. **Identical Partition Custody:** Every single experiment in Blocks `A–F` trains strictly on `REL0001 Train` (`66,338`) and selects hyperparameters/checkpoints strictly on `REL0001 Val` (`12,724`). **`REL0001 Test` (`12,719`) remains sealed (`0` reads) until Gate `G11` PASS.**
2. **Balanced Validation Budgets (`Q1 Fairness Guard`):**
   - Classical ML & GBDT (`LR, RF, SVM, XGBoost, LightGBM`): Up to **`25` validation trials** per cohort block via deterministic grid/random search (`Stratified 5-Fold Train CV` / fixed `Val` score).
   - Deep Neural Models (`MLP, ResNet1D, CNN-BiLSTM, CompactCNN2D, PatchTransformer, GatedFusion, CVD-MM-Transformer`): Matched max budget (`max_epochs = 40`, AdamW cosine schedule, early stopping `patience = 7` on **`val_roc_auc`** with `val_bce` tie-break) + matched HPO cap (`<= 12` structured validation configs).
3. **Imbalance & Seed Rules:**
   - **Zero Pre-Split or Uncalibrated SMOTE:** Every model uses exact cohort **`Train pos_weight`** (`DS0001: 0.7368`, `DS0002: 0.6738`, `DS0003: 1.0903`, `DS0004: 1.0212`) or `class_weight='balanced'`.
   - **Canonical Multi-Seed Array (`S = 5`):** `[20261127, 20261128, 20261129, 20261130, 20261201]`. Smoke run uses seed `20261127`.
   - **Failure Preservation Rule:** Failed, diverged, or null-result runs are NEVER deleted or hidden from `experiment_registry.csv`.

---

## 2. Complete Controlled Comparison Matrix (`Blocks A–F`)

### Block A — Tier 1 Unimodal Benchmarks (`RQ1` Foundation)
Tests every standalone modality across all proposal model families (`LR`, `RF`, `SVM`, `XGBoost`, `LightGBM`, `MLP`, `ResNet-1D`, `Conv1D-BiLSTM`, `Compact 2D-CNN`, `ECG Patch Transformer`):
- **`EXP-A1..A6` (`Tabular C, L, S Separate & Combined Tabular`):** `MC0001 (LR)`, `MC0002 (RF)`, `MC0003 (SVM)`, `MC0004 (XGBoost)`, `MC0005 (LightGBM)`, `MC0006 (Tabular MLP)` evaluated individually on **`C`-only**, **`L`-only**, and **`S`-only** (`DS0001–04`).
- **`EXP-A7..A10` (`ECG-Only Deep Encoders`):**
  - `DS0001 PTB-XL WFDB`: `MC0007 (ResNet1D_ECG)`, `MC0008 (CNN_BiLSTM_ECG)`, `MC0010 (ECGPatchTransformer)`.
  - `DS0002 CARDIO-ML-ED PNG (n_train=231 paired)`: `MC0009 (CompactCNN2D_PNG)` + `5`-fold Train CV.

### Block B — Tier 2 Clinical Risk Score Context (`MC0011`)
- **`EXP-B1`:** Evaluates WHO South Asia / Framingham covariate linear score on compatible `DS0003 (CAIR-CVD-2025)` & `DS0004 (sulianova)` variables (`Age, Sex, SBP, Chol, Smoke, DM`), logged explicitly as cross-sectional discrimination & DCA reference (`never claiming 10y prognostic calibration`).

### Block C — Tier 3 Simple Fusion vs Tier 4 `CVD-MM-Transformer` (`RQ1` Primary Test)
- **`EXP-C1` (`MC0012`):** Early Concatenation (`XGBoost` & `Concat-MLP`) combining `[C, L, S]` + pooled ECG features.
- **`EXP-C2` (`MC0013`):** Late Probability OOF Stacking (`LogisticRegression` meta-learner over best unimodal Validation/OOF scores).
- **`EXP-C3` (`MC0014`):** Gated Attention Intermediate Fusion (`sigmoid alpha_m` weights without Transformer self/cross-attention).
- **`EXP-C4` (`MC0015` — Proposed Champion Candidate):** **`CVD-MM-Transformer`** (`d_model=64`, `2L/4H`, native `~ModalityMask_CELS` key-padding mask, `Modality Dropout p=0.15`) trained on:
  - Unified multi-cohort **`REL0001`** (`Train = 66,338`) with per-cohort heads & shared cross-modal attention core;
  - Dedicated cohort evaluations on **`DS0002 CARDIO-ML-ED`** (`3`-modality anchor `C+E_png+L`), **`DS0001 PTB-XL`**, **`DS0003 CAIR`**, and **`DS0004 sulianova`**.

### Block D — Progressive & LOMO Modality Ablations (`RQ2 / PG4`)
Directly tests whether **Structured Lifestyle (`S`)** and multi-source modalities yield statistically significant incremental AUROC / PR-AUC / DCA Net Benefit:
- **`EXP-D1` (`Progressive C -> C+L -> C+L+S`):** Evaluated on `DS0003` (`CAIR`) and `DS0004` (`sulianova`).
- **`EXP-D2` (`Progressive C+L -> C+E_png+L`):** Evaluated on `DS0002` (`CARDIO-ML-ED` paired PNG subset).
- **`EXP-D3` (`Leave-One-Modality-Out / LOMO` on Multi-Cohort `CVD-MM-Transformer`):** Full model vs `-Clinical`, `-ECG`, `-Laboratory`, and `-Lifestyle` (`quantifies empirical Delta ROC-AUC and Delta Net Benefit for SHAP-LOMO concordance`).

### Block E — Architectural & Incorporation-Bias Sensitivity Ablations (`RQ1 / PROBAST`)
- **`EXP-E1` (`Masking Mechanism`):** `CVD-MM-Transformer` with `~ModalityMask_CELS` key-padding mask vs naive zero-padding without attention masking.
- **`EXP-E2` (`ECG Branch Transfer`):** `Train`-only `DS0001` initialized weights vs random scratch (`never using external/Val weights`).
- **`EXP-E3` (`PROBAST Incorporation Bias & Sensitivity`):** (i) Tier B exploratory ablation adding `TierB_TroponinI_ElevatedFlag` on `DS0002` vs primary Tier A; (ii) excluding `n=5` `Prior_CABG` encounters (`VAR0019`); (iii) reassigning `Family History` from `Lifestyle` to `Clinical` (`OS §5.2 RF10`).

### Block F — Multi-Seed Variance & Missing-Modality Degradation Stress Tests (`RQ4`)
- **`EXP-F1` (`5-Seed Stability`):** Retrain Champion `MC0015` & best Tier 3 comparator across all `5` canonical seeds (`reporting mean +/- SD`).
- **`EXP-F2` (`Inference-Time Missing-Modality Degradation`):** Evaluate frozen `CVD-MM-Transformer` without retraining on: (a) `DS0002`'s real **`226` `[MISSING_ECG]` encounters** (`Train/Val` audited pre-freeze, final `81` Test evaluated at `G12`); (b) systematic `10%, 25%, 50%, 100%` random masking of `ECG`, `Lab`, and `Lifestyle` at inference!
