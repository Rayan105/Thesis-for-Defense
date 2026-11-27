# Phase 2 Runtime Lock & Host Verification Record (`environment/model/versions.md`, `STEP-024`)

| Metadata | Value |
|---|---|
| Document | `environment/model/versions.md` |
| Step | STEP-024 (`Stage S10`) |
| Target Gate | Feeds `G09` |
| Date | `2026-11-27` |
| Framework Policy (`DEC0009` / `UD13`) | **PyTorch** + `scikit-learn` + `XGBoost` / `LightGBM` |
| Owners | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Reviewer | Md. Mizanur Rahman |

---

## 1. Local Workstation Audit (`Observed Live — Zero Fabricated Specs`)

Inspected directly on local host via `Win32_OperatingSystem` / `Win32_Processor` / `Win32_VideoController` and `14_Automation/verify_model_runtime.py`:

| Component | Observed Local Host Value | Note |
|---|---|---|
| **OS** | `Microsoft Windows 11 Pro 64-bit` (`Windows-11-10.0.26200-SP0`) | Local governance, deterministic preprocessing & unit-test workstation |
| **CPU** | `AMD Ryzen 5 5600G with Radeon Graphics` | CPU-only locally |
| **GPU / CUDA Driver** | `AMD Radeon(TM) Graphics` (**No local NVIDIA CUDA GPU / no `nvidia-smi`**) | Heavy DL/GPU runs hosted on **Kaggle Private Cloud GPU** |
| **Visible RAM** | `14,570,452 KB` (~`13.9 GB`) | Clean for data orchestration & stdlib unit tests |
| **Local Python** | `3.13.18` (`AMD64`, stdlib-only sandbox) | `15/15` pure-Python tests PASS (`torch/sklearn/xgboost/shap` absent locally) |

---

## 2. Primary Model Execution Platform & IRB Compliance (`UD05` / `DEC0004 Option B`)
- **Why Kaggle Cloud GPU Is IRB-Compliant Here:** Under ratified [DEC0004 Option B](../../01_Project_Management/decision_log/DEC0004.md), all four cohorts (`PTB-XL`, `CARDIO-ML-ED`, `CAIR-CVD-2025`, `Kaggle sulianova`) are **public, open, de-identified secondary releases (`0` Bangladesh hospital PHI or linkage keys)**. Private Kaggle notebooks (`Sharing: Private`) comply fully with `UD05` data-residency governance.
- **Target Accelerator:** Kaggle **`GPU T4 x2 / P100`** (`CUDA`-accelerated PyTorch + XGBoost/LightGBM) running exact pinned libraries in [requirements.txt](./requirements.txt) / [environment.yml](./environment.yml).

---

## 3. Pinned Phase 2 Dependencies & Version Compatibility Policy

> [!NOTE]
> **Why `shap` & `captum` are pinned now in `STEP-024`:** Pinning `shap>=0.45.0,<0.47.0` and `captum>=0.7.0,<0.9.0` alongside `torch>=2.1.0,<2.7.0` and `numpy>=1.26.0,<2.0.0` at `STEP-024` prevents NumPy 2.x / PyTorch hook ABI breakage later when saving checkpoints (`Stage S11`) and reloading them for explainability (`Stage S15`). **No XAI computation executes in `STEP-024`; Stage S15 handles XAI after training completes.**

| Role | Package | Locked Version Spec | Phase-2 Execution Target |
|---|---|---|---|
| **Deep Learning (`UD13`)** | `torch`, `torchvision` | `>=2.1.0,<2.7.0` / `>=0.16.0,<0.22.0` | Kaggle Private GPU / `.venv` |
| **Tabular ML & GBDT** | `scikit-learn`, `xgboost`, `lightgbm`, `joblib` | `>=1.4,<1.7` / `>=2.0.3,<3.0` / `>=4.3,<5.0` | Kaggle GPU / CPU |
| **Calibration & Stats** | `numpy`, `scipy`, `pandas`, `statsmodels` | `<2.0` / `>=1.12,<2.0` / `>=2.2,<3.0` / `>=0.14.1,<0.15` | Stage S12–S13 Evaluation |
| **XAI Compat Pin (`S15`)** | `shap`, `captum` | `>=0.45,<0.47` / `>=0.7,<0.9` | **Deferred execution to `Stage S15`** (`STEP-038–040`) |
| **ECG / Visual / Test** | `wfdb`, `opencv-python-headless`, `matplotlib`, `seaborn`, `pyyaml`, `pytest` | Locked per `requirements.txt` | Shared I/O & Validation |

---

## 4. Phase 1 `environment/data/` Preservation Proof (SHA-256)
Verified untouched cleanly by `14_Automation/verify_model_runtime.py`:
- `environment/data/environment.yml`: `3fb87a8d00a50397bbebc68e3bee801c94ee9a9c80f11c2ef71159797dc746b2`
- `environment/data/requirements.txt`: `da3fe35f82644343fc283d4f2831ef1c6667621185c7c82874d7a18ec58419`
- `environment/data/verification.md`: `edcc53a6c9625afaf81a171ab3af9d774d191f3db9b64a17a0a0e813a134a088`
- **Smoke Execution Status:** Local host verified **`LOCAL_STDLIB_GOVERNANCE_ONLY`** + `REL0001` (`91,781` encounters) integrity; Kaggle GPU runtime runs `python 14_Automation/verify_model_runtime.py` (`FULL_PHASE2_SMOKE_PASS`) inside Stage S10 training notebooks prior to `EXP0000_SMOKE` (`G09`).
