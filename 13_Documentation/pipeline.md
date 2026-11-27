# Four-Tier Storage Architecture & PHI Security Policy

| Metadata | Value |
|---|---|
| Document | `13_Documentation/pipeline.md` |
| Version | v1.0.0 |
| Date | 2026-11-20 |
| Governing Section | CVD Multimodal Research OS §2, §11; Blueprint STEP-002 |
| Sensitivity | Tier 1 (Public / Git-safe) |
| Authors | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Supervisor | Md. Mizanur Rahman |

---

## 1. Objective and Regulatory Context

Cardiovascular research combining Electronic Health Records (EHR) and digital 12-lead Electrocardiograms (ECG) involves highly sensitive patient health data. This document establishes the mandatory **Four-Tier Storage Model** and Protected Health Information (PHI) custody policies required before any hospital or diagnostic center data intake.

This policy enforces compliance with:
- Ethical standards of the institutional Review Board (IRB) and Hospital Data Custodians.
- The Declaration of Helsinki for medical research involving human subjects.
- International reporting and safety guidelines: **TRIPOD+AI (2024)** and **PROBAST-AI**.

---

## 2. Four-Tier Storage Architecture

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        FOUR-TIER STORAGE MODEL                         │
├────────────────────────────────┬───────────────────────────────────────┤
│ Tier 1: Source Control (Git)   │ Tier 2A: PHI Linkage Vault (Isolated) │
│ - Code & Unit Tests            │ - Real Patient ID <-> Pseudonym Map   │
│ - Safe CSV Registries          │ - Signed Consent Forms                │
│ - Aggregate Metrics & Tables   │ - Raw Hospital Export with Identifiers│
│ - Documentation & Manuscripts  │ * Offline / AES-256 Encrypted Volume  │
├────────────────────────────────┼───────────────────────────────────────┤
│ Tier 2B: Restricted Clinical   │ Tier 3: Versioned Research Artifacts  │
│ - De-identified Tabular Data   │ - Trained Checkpoints (CKPT)          │
│ - Filtered/Raw ECG Waveforms   │ - Fitted Scalers/Imputers (FitState)  │
│ - Local Adjudication Logs      │ - Full SHAP Tensor Arrays             │
│ * Excluded from Git via Ignore │ * Verified via SHA-256 Manifests      │
├────────────────────────────────┴───────────────────────────────────────┤
│ Tier 4: Immutable Release & Q1 Archive (Long-Term Handover)            │
│ - Submitted Manuscript & Thesis Snapshots                              │
│ - TRIPOD+AI Verification Receipts & Restoration Proofs                 │
└────────────────────────────────────────────────────────────────────────┘
```

### Detailed Tier Specifications

| Tier | Name | Custody & Physical Location | Access Controls | Backup & Integrity |
|---|---|---|---|---|
| **Tier 1** | Git Source Control | Local working tree + Private GitHub (`Rayan105/Thesis-for-Defense`) | Research team + Supervisor. Publicly tracked files only. | Git commit history. Diff-inspected before push. |
| **Tier 2A** | PHI Linkage Vault | Designated encrypted offline drive (`E:\FYDP_SECURE_VAULT\Tier2A\`) | Hospital data custodian + Lead Researchers only. Completely air-gapped from ML training scripts. | Hardware-encrypted backup; SHA-256 verified manifests. |
| **Tier 2B** | Restricted Clinical Tier | Local filesystem (`03_Datasets_Cohort/raw/`, `03_Datasets_Cohort/processed/`) | Researchers only. Excluded from Git tracking via `.gitignore`. | Weekly encrypted mirror with SHA-256 checksums. |
| **Tier 3** | Research Artifacts | Local artifact cache (`08_Checkpoints/binaries/`, `artifacts/`) | Researchers. Excluded from Git. Pointers registered in `checkpoints.csv`. | Cold cloud / secondary drive backup. |
| **Tier 4** | Immutable Release Archive | Permanent storage (`16_Archive/ARCH####/`) | Academic department and long-term archive custodians. Read-only. | Cryptographic checksums and verified restore drill. |

---

## 3. PHI De-Identification Protocol

Before any clinical row or ECG record enters Tier 2B:

1. **Direct Identifier Scrubbing:**
   - Names, National ID (NID) numbers, phone numbers, physical addresses, and hospital MRNs must be permanently removed.
   - Assigned a pseudonymous identifier: `PAT########` for patients, `ENC########` for clinical encounters.
2. **ECG Header Sanitization:**
   - 12-lead ECG files (XML, DICOM, EDF, PDF) contain embedded header metadata that often store patient name, age, birthdate, and hospital recording room.
   - All text headers must be stripped or anonymized using automated inspection tools before waveform arrays are saved.
   - Any scanned paper ECG must have patient identifying blocks cropped out and verified by human inspection.
3. **Age & Date Masking:**
   - Exact dates of birth are converted to age in whole years. Ages $>89$ are grouped into an aggregated category (e.g., $90+$) per HIPAA standard Safe Harbor guidance.
   - Encounter timestamps are stored relative to index time ($t_0$) rather than calendar dates where applicable.

---

## 4. Leakage Prevention and Verification Checklist

- [ ] `.gitignore` contains explicit blocks for `raw/`, `processed/`, `fitted_states/`, `*.edf`, `*.xml`, `*.dcm`, `*.mat`, `*.dat`, `*.hea`, and all model weights (`*.pt`, `*.ckpt`).
- [ ] No training script has programmatic read access to Tier 2A linkage paths.
- [ ] All preprocessing estimators (scalers, imputers, encoders) are fit strictly on training splits.
- [ ] Git commit hooks and pre-push checks audit staging area for accidental CSV rows containing names or identifiers.

---

## 5. Stage S09 Decoupled Preprocessing Contract (`STEP-019`, `UD12`)

- **Specification & Code Modules:** [pipeline.md](../05_Preprocessing_Alignment/specs/pipeline.md), [pp_v1_0_0_spec.yaml](../05_Preprocessing_Alignment/configs/pp_v1_0_0_spec.yaml), [src/cvd_mm/preprocessing.py](../src/cvd_mm/preprocessing.py), [src/cvd_mm/ecg.py](../src/cvd_mm/ecg.py), [tests/test_preprocessing_leakage.py](../tests/test_preprocessing_leakage.py)
- **Kaggle Execution Companion:** [CVD_Multimodal_Kaggle_Preprocessing_Pipeline.ipynb](../05_Preprocessing_Alignment/notebooks/CVD_Multimodal_Kaggle_Preprocessing_Pipeline.ipynb)
- **Two-Stage Leakage Boundary:** **Stage A (Record-Local)** covers unit conversion, BMI derivation, fixed `50 Hz` notch (`fs > 120 Hz`), $\le 0.5\text{ Hz}$ zero-phase Butterworth baseline filter, and `CARDIO-ML-ED` `90°` CCW PNG rotation + RGB red-grid ink isolation; **Stage B (Train-Only)** executes ONLY after `STEP-020` (`G07`) splitting, computing Train-only `IterativeImputer`/median, `RobustScaler`, categorical encoding, MNAR `{col}_isnan` flags, 4D `[has_clinical, has_ecg, has_lab, has_lifestyle]` modality masks, and `FitStateHash` SHA-256 verification.

