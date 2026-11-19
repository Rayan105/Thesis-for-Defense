# Phase 1: Minimal Data-Tool Environment Verification Record

| Metadata | Value |
|---|---|
| Document | `environment/data/verification.md` |
| Step | STEP-002 |
| Gate Target | G02 |
| Date | 2026-11-20 |
| Phase | Phase 1 (Minimal Data & Signal Tooling) |
| Framework Policy | Deep learning frameworks (PyTorch vs TensorFlow) deferred to STEP-024 (`UD13`) |
| Lead Implementer | Rayan Ahmed (`232-15-847`) |
| Reviewer | Md. Mizanur Rahman |

---

## 1. Specification & Scope

The Phase 1 runtime provides deterministic, lightweight execution for:
- Tabular clinical dataset loading and schema validation (`pandas`, `numpy`).
- 12-lead ECG waveform parsing, lead extraction, and signal inspection (`scipy`, `wfdb`).
- Appendix B CSV registries and metadata schema validation (`pyyaml`, `jsonschema`).
- Unit and leakage prevention regression testing (`pytest`).

No heavy deep-learning frameworks (PyTorch, TensorFlow, CUDA) are loaded at this stage, avoiding premature runtime lock-in.

---

## 2. Pinned Tooling Manifest

| Component | Target Version Range | Verified Status | Purpose |
|---|---|---|---|
| Python | 3.11.x / 3.12.x | Pinned (`requirements.txt`, `environment.yml`) | Base language runtime |
| numpy | `>=1.26.0, <2.0.0` | Specified | Multi-dimensional array operations, ECG buffers |
| scipy | `>=1.12.0, <2.0.0` | Specified | Signal filtering (bandpass, notch) |
| pandas | `>=2.2.0, <3.0.0` | Specified | Tabular clinical, lab, lifestyle DataFrame operations |
| wfdb | `>=4.1.2` | Specified | PhysioNet / WFDB standard 12-lead ECG reader |
| pyyaml | `>=6.0.1` | Specified | Experiment configuration parsing |
| jsonschema | `>=4.21.0` | Specified | Run manifest and split schema integrity checks |
| pytest | `>=8.0.0` | Specified | Automated unit test suite execution |

---

## 3. Verification Test Suite

Synthetic smoke tests located in `tests/test_synthetic_smoke.py`:
1. `test_tabular_fixture_integrity`: Verifies patient-level tabular schema without NaN leakage.
2. `test_synthetic_ecg_sine_wave`: Simulates 12-lead 500 Hz synthetic cardiac waveform and verifies sampling properties.
3. `test_phi_exclusion_rules`: Verifies that dummy raw data files matching `.gitignore` patterns are strictly rejected by Git status.

---

## 4. Remediation and Handoff

When provisioning a fresh machine or compute server:
```bash
# Option A: Conda environment
conda env create -f environment/data/environment.yml
conda activate cvd-mm-data

# Option B: Standard Python venv
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
pip install -r environment/data/requirements.txt
```
