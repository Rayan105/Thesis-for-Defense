# EXP0000_SMOKE — Diagnostic End-to-End Smoke & Recovery Report (`STEP-027`)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | `EXP0000_SMOKE` |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | `2026-11-27` |
| status | Diagnostic_Smoke_Pass *(Never Reportable Research Claims)* |
| source_inputs | `REL0001` (`Train=600` / `Val=200` stratified slice across `DS0001–04`; **Test=0 reads**) |
| governing_section | OS §6.2, §11, §14.2 (`G09`), §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe summary; binaries reside strictly in Tier 3) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Scientific Objective (Diagnostic Only)
- **Experiment ID:** `EXP0000_SMOKE`
- **Research Question:** `RQ0` (`Diagnostic Readiness Verification for Gate G09`)
- **Comparator Tiers Exercised:** Tier 1 Tabular (`PurePythonLogisticModel`, `MC0004 XGBoost`) + Tier 4 Multimodal (`PurePythonMaskedFusionModel`, `MC0015 CVDMMTransformer`)
- **Governance Boundary:** Strictly diagnostic verification on `REL0001` `Train`/`Val` shards only; zero reads of `rel0001_test.jsonl` confirmed in both local and Kaggle runs.

## 2. Data & Model Configuration
- **Prepared Release:** `REL0001` (`SPLIT0001`, `PP0001`, `FitStateHash=d9ccfbf4...`)
- **Config Path:** [exp0000_smoke.yaml](file:///e:/FYDP/07_Experiments/configs/exp0000_smoke.yaml)
- **Config SHA-256:** `d2b9d1daacc78f230a1c1dd8926cd23a9139d79bb0348f36d7c1fcecdb824835`
- **Source Git Commit:** `4ace526` (Kaggle Notebook) / `6eebee0` (Local Runner)
- **`CVDMMTransformer` Parameter Budget:** `129,169` trainable parameters (`<= 250,000` ceiling verified).

## 3. Verified Execution & Recovery Results

### 3.1 Kaggle GPU CUDA Smoke Execution ([smoke_kaggle_g09_report.json](file:///e:/FYDP/07_Experiments/EXP0000_SMOKE/smoke_kaggle_g09_report.json))
- **Hardware:** Kaggle **`cuda`** GPU (`EXP0000_SMOKE_CVD_MM_Kaggle_Gate_G09`)
- **`MC0004 XGBoost` Smoke:** `Val ROC-AUC = 0.768026`; `TreeSHAP` max additivity error = **`7.15e-07`** (`<= 0.02` PASS).
- **`MC0015 CVDMMTransformer` Interrupt/Resume:**
  - Deliberately interrupted after Epoch `2`; saved full state payload (`CKPT0001_SMOKE_interrupt.pt`, `1,691,308` bytes, SHA-256 `18824d5e3c858bc52591a1ccf75a9af4998dda00bf64cfa2934e749603240b82`).
  - Restored full state (`model + optimizer + scheduler + GradScaler + Python/NumPy/Torch/CUDA RNG`) and resumed Epochs `3–4` across all 4 cohorts with **`resumed_losses_finite = true`** and **`missing_masks_zero_nan = true`** (`[1,0,1,1]`, `[1,0,0,1]`, `[1,0,0,0]`).
- **Neural SHAP Additivity Check:** `KernelExplainer` max additivity error = **`2.98e-08`** (`<= 0.02` PASS).
- **Test Partition Custody:** `test_partition_accessed = false`.

### 3.2 Local CPU Real-Data Smoke & WFDB Check ([smoke_local_report.json](file:///e:/FYDP/07_Experiments/EXP0000_SMOKE/smoke_local_report.json))
- **WFDB 12-Lead Filter Check:** Loaded real `DS0001` `00001_hr.dat` (`12` leads × `5,000` samples @ `500 Hz`), `finite_all = true`.
- **Bitwise Exact Resume:** Interrupted at Epoch `3`, restored and resumed to Epoch `6` with **`max_weight_diff = 0.0`**, **`bias_diff = 0.0`**.
- **Validation Calibration & XAI Sanity:** `temperature = 0.25`, `tau_youden = 0.527228`, `tau_sens_target = 0.430892`; `aopc_deletion_top = 0.101628 > random = 0.030764 > reverse = 0.000202`, `shortcut_free = true`.

## 4. Checkpoints & Tier 3 Archive Retrieval
- **Checkpoint Manifest:** [CKPT0001.md](file:///e:/FYDP/08_Checkpoints/manifests/CKPT0001.md)
- **Tier 3 Local Binary Location (Gitignored):** `08_Checkpoints/binaries/EXP0000_SMOKE/CKPT0001_SMOKE_interrupt.pt` + `kaggle_results_backup.zip` (SHA-256 checksum verified on extraction).
