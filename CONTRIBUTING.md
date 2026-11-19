# Contributing & Research Governance Guidelines

Welcome to the **CVD Multimodal Risk Prediction Framework** research repository. This project is governed by strict biomedical ethics, Q1 publication standards (TRIPOD+AI 2024), and reproducible software engineering practices.

All contributors (researchers, implementers, reviewers) must strictly adhere to the policies outlined below.

---

## 1. Core Principles

1. **Zero Fabrication:** Never fabricate citations, sample sizes, patient counts, clinical approvals, or benchmark numbers. Missing evidence is always documented as `Unresolved / Human Decision Required` or `not reported`.
2. **Zero PHI in Version Control:** Never commit patient identifiers, hospital MRNs, raw spreadsheets, unstripped ECG waveforms/PDFs, or patient-level linkage tables to Git.
3. **Zero Pre-Split Leakage:** Never fit scalers, imputers, encoders, or oversamplers using validation or test set information. All training-fitted parameters must belong strictly to the training fold.
4. **Preserve Negative Results:** Never discard inferior baselines, failed convergence runs, or negative ablation results. All valid experiments remain permanently registered.
5. **Qualified Medical Oversight:** Endpoint definitions, ECG filter fidelity, and explanation clinical plausibility require qualified cardiologist review.

---

## 2. Branching & Commit Discipline

- **Branching Model:**
  - `main`: Protected production branch containing verified, gate-passed research artifacts.
  - Feature branches: `feat/<step-id>-<short-description>` (e.g., `feat/step-004-prisma-search`).
- **Semantic Commit Messages:**
  - `docs:` Documentation, scope charters, session logs, guidelines.
  - `lit:` Systematic literature search, screening, and extractions.
  - `cohort:` Cohort intake manifests, de-identification audits, split definitions.
  - `schema:` Variable dictionaries, endpoint charters, ECG contracts.
  - `prep:` Preprocessing pipelines, filter specifications, fitted states.
  - `model:` Architectures, candidate implementations, training scripts.
  - `exp:` Experiment registrations, configurations, run manifests.
  - `eval:` Metric evaluations, calibration analysis, DCA, statistical tests.
  - `xai:` SHAP attributions, faithfulness benchmarks, stability audits.
  - `writing:` Thesis chapters, Q1 manuscript sections, rebuttal responses.
  - `fix:` Bug fixes, schema corrections, refactoring.

**Commit format:**
```text
<type>(<step-id>): <short imperative description>

[Optional longer explanation referencing DEC####, Gate ID, or entity ID]
```

---

## 3. Universal Definition of Done (DoD)

A research step or task is marked **Done** only when:
1. Its objective and all required outputs exist in their canonical folder paths.
2. All input files, parent hashes, and commands are recorded in `01_Project_Management/diary/`.
3. Verification checklists and automated tests pass with clean exit codes.
4. Applicable quality gates (`G01–G17`) evaluate to `PASS` with named human sign-off.
5. All required human decisions are documented in `01_Project_Management/decisions.csv` and `decision_log/`.
6. Relevant registries (Appendix B CSV files) are updated.
7. Only safe Tier 1 files are staged and committed to Git.
8. Another researcher can pick up the exact handoff without ambiguity.

---

## 4. Protected Health Information (PHI) Breach Protocol

If any sensitive health data, patient identifiers, or credentials are accidentally committed:
1. **Immediately freeze** pushing to the remote repository.
2. Notify the research leads (Rayan Ahmed, Mohammad Nafis Sadiq) and supervisor (Md. Mizanur Rahman).
3. Follow the history scrubbing protocol using `git-filter-repo` or BFG Repo-Cleaner to permanently excise the blob from Git history.
4. Verify repository tree clean state before resuming development.
