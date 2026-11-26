# Clinical Label Reconciliation, Pilot QA & Agreement Protocol (`STEP-015`)

| Field | Value |
|---|---|
| TemplateID | T11-QA (`qa_protocol`) |
| template_version | v1.0.0 |
| entity_id | QA-PROTOCOL-v1.0.0 (`UD09`) |
| owner | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |
| date | 2026-11-27 |
| status | Approved (`DEC0005 Option A` — Prospective Thresholds Frozen `2026-11-27`) |
| source_inputs | `04_Outcome_Schema_QA/endpoint_charter.md`, `04_Outcome_Schema_QA/variables.csv`, `04_Outcome_Schema_QA/ecg_contract.md`, `01_Project_Management/decision_log/DEC0005.md`, `OS §5.3` |
| governing_section | OS §5.3, §14.2 (`G05`, `G06`), Appendix A; Blueprint `STEP-015`–`STEP-018` |
| phi_sensitivity | Tier 1 (Public / Git-safe protocol; restricted pilot outputs saved in Tier 2B) |
| reviewer | Md. Mizanur Rahman + Qualified Cardiologist (`TBD` per `scope.md §8.2`) |

---

## 1. Adaptation of Stage `S08` QA to Secondary Cohorts (`DEC0004 Option B`)
Because `DS0001–DS0004` are published de-identified archives (`PTB-XL`, `CARDIO-ML-ED`, `CAIR-CVD-2025`, `Kaggle sulianova`), primary hospital chart abstraction from raw paper folders is replaced (`DEC0004`) by **independent dual programmatic-vs-clinical verification of extraction, unit harmonization, outlier quarantine, ambiguous outcome resolution, and ECG image/signal quality grading** prior to locking immutable adjudication release `ADJ####` (`STEP-018 / G06`).

---

## 2. Prospective Pilot Sample Design (`Locked Before STEP-016 Execution`)
A deterministic stratified pilot sample of **`N_pilot = 60` encounters** (fixed RNG seed `20261127`, logged in `STEP-016`) will be drawn across the four cohorts:
1. **`DS0001` (`PTB-XL`, `n = 20`):** Stratified across `5` SCP superclasses (`MI, STTC, HYP, CD, NORM`), including `>= 4` noisy/artifact-flagged waveforms (`static_noise` / `baseline_drift` / `electrodes_problems`) plus explicit positive control check on `ecg_id=12722` and `<18y` bounds.
2. **`DS0002` (`CARDIO-ML-ED`, `n = 20`):** Stratified across `Initial Cardiac (10)` vs `Noncardiac (10)`, multi-encounter repeated `Col1` patients, elevated `Troponin-I` (`>= 0.05`) cases, missing `Final diagnosis` cases, prior `CABG` cases, **`>= 2` `.jpg` quarantine controls**, and `-1/-2` suffix normalizations.
3. **`DS0003` (`CAIR-CVD-2025`, `n = 10`):** Stratified across `HIGH/INTERMEDIARY/LOW`, explicitly including `SBP <= DBP` anomaly cases and `Estimated LDL < 0` negative values.
4. **`DS0004` (`Kaggle sulianova`, `n = 10`):** Balanced `cardio 0/1`, explicitly including physiological BP anomalies (`ap_hi <= ap_lo` / negative BPs) and discordant duplicate pairs.

---

## 3. Dual Verification & Blinding Workflow
- **Independent Stream A (Schema Script):** Automated Python extraction (`crf_manual_v1.0.0.md` rules) executed blindly to outcome labels.
- **Independent Stream B (Human Clinical/Research Audit):** Second researcher (and Qualified Cardiologist on ECG images + diagnostic edge cases) independently evaluates eligibility, target class assignment (`endpoint_charter.md`), ambiguous cases (`Elevated BP`, `Electrolyte-imbalance`, `missing Final diagnosis`), and ECG visual readability **without viewing Stream A outputs first**.
- **Blinding & Storage:** Both independent pilot sheets (`pilot_stream_a`, `pilot_stream_b`) stay preserved separately and immutably inside Tier 2B `04_Outcome_Schema_QA/adjudications/pilot/` prior to consensus reconciliation.

---

## 4. Prospectively Locked Quantitative PASS Thresholds (`UD09`)
Per `OS §5.3`, these thresholds are frozen **before running `STEP-016`** and may never be lowered post hoc:

| Quality Domain | Metric | Minimum Acceptance Threshold (`PASS`) | Failure Action |
|---|---|---|---|
| **Binary / Categorical Target & Disposition** | Cohen's $\kappa$ + % Exact Agreement | **$\kappa \ge 0.85$** (discretionary ambiguity cases) and **$\ge 99.0\%$** deterministic rule agreement | Revise `endpoint_charter.md` rules, re-train reviewer, re-run independent pilot |
| **Continuous Lab / Clinical Harmonization** | Intraclass Correlation (`ICC`) + Relative Error | **$\text{ICC} \ge 0.99$**, **0%** unit-conversion errors (`0` wrong scaling on `age_days`, `Height(m)`), max discrepancy $\le 10^{-4}$ | Fix CRF unit rule & audit every downstream transform |
| **ECG Signal & Image Quality Grading** | Cohen's $\kappa$ (Clean vs Artifact/Quarantine) | **$\kappa \ge 0.85$** across `.dat` / `.png` / `.jpg` triage checks | Refine visual/signal rejection boundary (`ecg_contract.md v1.1.0`) |
| **Uncertain / Ambiguous Handling** | Zero Silent Coercion Check | `100%` of ambiguous/typo rows flagged `uncertain / excluded` (zero forced `0`/`1`) | Halt batch & repair exclusion flags before `ADJ####` freeze |

---

## 5. Production Batch & Immutable `ADJ####` Freeze Protocol (`STEP-017`–`STEP-018`)
- Curate production label releases cleanly in traceable batches (`ADJB0001`–`ADJB0004`, one per cohort `DS0001`–`DS0004`).
- `G06` freeze checks require: `0` unresolved `uncertain` leaks into `0`/`1`, `0` leakage predictors inside predictor manifests, verified SHA-256 `NativeHash` & `VerifiedHash` logged in `04_Outcome_Schema_QA/adjudication_registry.csv`, and Qualified Cardiologist approval.
