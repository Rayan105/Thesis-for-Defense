# Explainable Multimodal Early Cardiovascular Disease Risk Prediction

[![TRIPOD+AI](https://img.shields.io/badge/Compliance-TRIPOD%2BAI%202024-blue)](https://www.tripod-statement.org/)
[![Reproducibility](https://img.shields.io/badge/Reproducibility-Q1--Grade%20Audit-success)](#reproducibility)
[![Status](https://img.shields.io/badge/Status-Stage%20S02%20Initialized-orange)](#master-pipeline)
[![PHI Security](https://img.shields.io/badge/PHI%20Security-Four--Tier%20Vault-red)](#phi-and-biomedical-ethics)

Official research repository for the Final Year Design Project (FYDP) and companion Q1 journal study:

> **"An Explainable Multimodal Framework for Early Cardiovascular Disease Risk Prediction Using Clinical, ECG, Laboratory, and Lifestyle Data"**

- **Institution:** Daffodil International University (DIU), Department of Computer Science and Engineering
- **Academic Term:** Summer 2026 (CSE499 Final Year Design Project)
- **Primary Scientific Authority:** Scanned Proposal Approval Form and Detailed Proposal (`fydp_title_proposal.pdf`, SHA-256: `BA7DD0EF21C8A2CA77B2E1BAFC2AC5A0E1FEC584E221C848085A971EAACEEFA8`)
- **Research Team:**
  - **Rayan Ahmed** (ID: `232-15-847`) — Literature, ECG Engineering, Transformer Modeling, XAI, Q1 Manuscript Lead
  - **Mohammad Nafis Sadiq** (ID: `232-15-895`) — Cohort Intake, IRB/DUA, Tabular Engineering, Evaluation & Statistics, FYDP Thesis Lead
- **Supervisor:** **Md. Mizanur Rahman** (Senior Lecturer, Dept. of CSE, DIU)

---

## 1. Project Overview

Early detection of cardiovascular disease (CVD) requires synthesizing multiple complementary physiological windows: clinical history and vitals, 12-lead electrocardiograms (ECG), serum laboratory biomarkers, and lifestyle behaviors. 

This repository implements a rigorous, leakage-safe multimodal machine learning framework combining:
1. **Four Heterogeneous Modalities:** Clinical records, ECG waveforms/intervals, Laboratory assays, and Lifestyle risk factors.
2. **Deep Multimodal Architecture:** Transformer-based cross-modal attention fusion network compared against rigorous unimodal and tabular baselines (LR, RF, SVM, XGBoost, 1D-CNN, LSTM).
3. **Quantitative Explainability (XAI):** Game-theoretic SHAP attributions audited for mathematical additivity, perturbation faithfulness (Deletion/Insertion AOPC vs random controls), multi-seed stability, and cardiologist plausibility.
4. **Clinical Prediction Rigor:** Post-hoc probability calibration (Brier score, ECE, calibration slope), Decision Curve Analysis (DCA), DeLong statistical significance tests, and full TRIPOD+AI / PROBAST-AI compliance.

---

## 2. Repository Architecture

```text
workspace/
├── .gitignore                     # Strict exclusion of PHI, datasets, papers, and checkpoints
├── .gitattributes                # Line ending and binary encoding normalization
├── README.md                      # Project root contract and overview
├── CHANGELOG.md                   # Chronological version and milestone ledger
├── CONTRIBUTING.md                # Research contribution, ethics, and DoD guidelines
├── environment/
│   ├── data/                      # Minimal data/ECG/registry tooling lock (Phase 1)
│   └── model/                     # Deep learning & XAI environment lock (Phase 2)
├── src/cvd_mm/                    # Core reproducible Python package
├── tests/                         # Leakage, unit, metric, and synthetic fixture tests
├── 01_Project_Management/         # Scope, decisions, gates, risk register, session diary
├── 02_Literature/                 # Systematic PRISMA search, screening, summaries, gaps, claims
├── 03_Datasets_Cohort/            # Cohort cards, data manifests, patient-level splits, reports
├── 04_Outcome_Schema_QA/          # Endpoint charter, variables dictionary, ECG contract, adjudication
├── 05_Preprocessing_Alignment/    # Preprocessing specs, training-only fit states, filter QA
├── 06_Models_Fusion/              # Model candidates, architectures, baseline suite, model cards
├── 07_Experiments/                # Preregistered configs, run manifests, execution logs
├── 08_Checkpoints/                # Checkpoint registry, hashes, and restore manifests
├── 09_Evaluation_Stats/           # Held-out metrics, calibration, DCA, bootstrap CIs, subgroup audit
├── 10_Explainability_XAI/         # Multimodal SHAP, faithfulness benchmarks, cardiologist rubric
├── 11_Figures_Tables/             # High-resolution vector assets, specs, generator scripts
├── 12_Writing/                    # FYDP thesis, Q1 manuscript, TRIPOD+AI checklists, reviews
├── 13_Documentation/              # Architecture, pipeline, storage policy, installation guides
├── 14_Automation/                 # CLI validation, audit runners, integrity checks
├── 15_Templates_Prompts/          # Blank templates (T01-T32) and task prompt contracts
└── 16_Archive/                    # Immutable release bundles and restoration proofs
```

---

## 3. Four-Tier PHI Security Model

To comply with international biomedical ethics (Declaration of Helsinki) and local institutional guidelines, this repository enforces a strict four-tier data segregation model:

| Tier | Name | Location | Contents & Policy |
|---|---|---|---|
| **Tier 1** | Source Control | Git / GitHub | Code, configs, safe CSV registries, aggregate metrics, documentation, vector assets. **ZERO raw health data or identifiers.** |
| **Tier 2A** | PHI Linkage Vault | Encrypted Local Vault | Patient real identities $\leftrightarrow$ pseudonymous IDs lookup tables, signed consent forms. **Strictly isolated outside Git.** |
| **Tier 2B** | Restricted Clinical Tier | Encrypted Storage | De-identified clinical tables, ECG waveforms, raw chart logs. **Excluded from Git by `.gitignore`.** |
| **Tier 3** | Research Artifacts | Artifact Storage | Model weights, optimizer states, full SHAP tensor arrays. **Tracked via SHA-256 manifests.** |
| **Tier 4** | Immutable Archive | Long-term Archive | Final thesis/paper release snapshots (`ARCH####`) with verified restore verification. |

---

## 4. Master Pipeline & Quality Gates

The research follows a sequential 17-stage, 50-step roadmap governed by 17 strict quality gates (`G01–G17`):

```text
G01 (Scope Charter) ──► G02 (Repository & PHI Lock) ──► G03 (Systematic Literature)
       │
       ▼
G04 (IRB & Cohort Intake) ──► G05 (Endpoint Charter) ──► G06 (Pilot Adjudication)
       │
       ▼
G07 (Patient-Level Split) ──► G08 (Train-Only Fit) ──► G09 (Architecture Readiness)
       │
       ▼
G10 (Controlled EXP) ──► G11 (Val-Only Freeze) ──► G12 (Final Metrics & DCA)
       │
       ▼
G13 (Fairness & PROBAST) ──► G14 (XAI Faithfulness) ──► G15 (Clean Reproducibility)
       │
       ▼
G16 (Thesis & Q1 Paper) ──► G17 (Final Archive Handover)
```

Every gate requires 100% evidenced criteria and named human sign-off; missing evidence blocks downstream execution.

---

## 5. Getting Started

See [13_Documentation/installation.md](file:///e:/FYDP/13_Documentation/installation.md) for environment setup and runtime requirements.

```bash
# Verify repository integrity and registry schemas
python 14_Automation/validate_repo.py

# Run synthetic smoke and unit tests
pytest tests/
```

---

## 6. Research Ethics & Disclaimer

> [!WARNING]
> **Research Decision-Support Disclaimer:**
> The software, models, and predictions developed in this project are strictly intended for research decision-support and academic investigation. They do **NOT** constitute medical software, medical diagnostic devices, or autonomous clinical decision systems. All risk predictions and explainability attributions must be interpreted by qualified healthcare professionals.
