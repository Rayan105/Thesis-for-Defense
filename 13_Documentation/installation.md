# Environment Installation & Runtime Setup Guide

This guide describes how to set up the reproducible computing environment for the **CVD Multimodal Framework** project across its two execution phases.

---

## 1. Two-Phase Environment Architecture

Per OS §11.3, runtime configuration is separated into two clean stages to avoid premature dependencies:

1. **Phase 1: Minimal Data-Tool Runtime (`environment/data/`)**
   - Active during Stages S01–S09 (`STEP-002` through `STEP-022`).
   - Lightweight: Python, Pandas, NumPy, SciPy, WFDB, PyYAML, Pytest.
   - Purpose: Cohort screening, schema checks, ECG signal inspection, leakage-safe splits, baseline preprocessing.
2. **Phase 2: Modeling & Deep Learning Runtime (`environment/model/`)**
   - Active during Stages S10–S17 (`STEP-023` through `STEP-050`).
   - Pinned after formal resolution of `UD13` (PyTorch vs TensorFlow) and hardware selection.
   - Includes GPU acceleration, Transformer modeling libraries, SHAP/XAI suites, calibration, and statistical inference tools.

---

## 2. Phase 1 Setup Instructions

### Prerequisites
- Python 3.11 or 3.12 installed on your system.
- Git (configured with your institutional credentials).

### Setup via Virtual Environment (venv)
```bash
# Clone the repository
git clone https://github.com/Rayan105/Thesis-for-Defense.git
cd Thesis-for-Defense

# Create isolated Python virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install minimal data tooling
pip install --upgrade pip
pip install -r environment/data/requirements.txt
```

### Setup via Conda
```bash
conda env create -f environment/data/environment.yml
conda activate cvd-mm-data
```

---

## 3. Environment Verification

Verify that your installation is working correctly:
```bash
# Run synthetic smoke tests
pytest tests/ -v
```
All tests should pass.

---

## 4. Phase 2 Setup Instructions (`environment/model/`, `STEP-024`)

Active during Stages **S10–S17** following framework selection (`DEC0009`: **PyTorch + Scikit-Learn + XGBoost/LightGBM**) while leaving `environment/data/` untouched:

### Kaggle GPU Execution Environment (`Primary Deep Learning Compute — DEC0004 Open Data`)
- **Accelerator:** Kaggle `GPU T4 x2` / `P100` (`CUDA` native PyTorch + `XGBoost` + `LightGBM` + `SHAP` + `Captum`).
- **Privacy Guard:** Private notebooks only; zero raw cohorts or output weights pushed to GitHub.

### Local Workstation / Full Linux/Windows Virtual Environment
```bash
# Option A: Conda (PyTorch + Conda-Forge)
conda env create -f environment/model/environment.yml
conda activate cvd-mm-model

# Option B: Pip inside clean Python 3.11/3.12 virtualenv
pip install -r environment/model/requirements.txt

# Verify runtime dependencies, Phase 1 immutability, and synthetic smoke checks
python 14_Automation/verify_model_runtime.py
```

