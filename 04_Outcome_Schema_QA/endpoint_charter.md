# Clinical Endpoint & Ascertainment Charter (`STEP-014`)

| Field | Value |
|---|---|
| TemplateID | T10 (endpoint_charter.md) |
| template_version | v1.0.0 |
| entity_id | ENDPOINT-CHARTER-v1.0.0 (`UD02`, `UD03`) |
| owner | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |
| date | 2026-11-26 |
| status | Draft Ready for Cardiologist Clinical Review (`Awaiting Cardiologist Sign-Off for G05`) |
| source_inputs | `01_Project_Management/scope.md` (`v1.1.0`), `01_Project_Management/decision_log/DEC0004.md`, `03_Datasets_Cohort/reports/cohort_cards_DS0001_to_DS0004.md`, `03_Datasets_Cohort/reports/four_modality_qc_and_ecg_audit.md`, `OS §5.1–§5.2` |
| governing_section | OS §1, §5.1, §5.2, §14.2 (`G05`), §15.2 (`T10`); Blueprint `STEP-014` |
| phi_sensitivity | Tier 1 (Public / Git-safe schema document) |
| reviewer | Md. Mizanur Rahman (Supervisor) + Qualified Cardiologist (`TBD`, per `scope.md §8.2`) |

---

## 1. Multi-Cohort Operational CVD Endpoint Definitions (`UD02`)

Because our approved **`DEC0004` Option B** portfolio enforces strict **Zero Fake Patient Stitching** (`Complete4ModalityCount = 0`), each cohort retains its native outcome target grounded in its verified clinical reference standard, while prohibiting cross-cohort label conflation or silent merging of uncertain cases into `0`/`1`:

| Cohort | Reference Standard & Target Construct | Positive Class (`1`) | Negative / Control Class (`0`) | Ambiguous / Excluded (`Quarantine`) | Baseline Sample Accounting (`Pre-Split Eligible`) |
|---|---|---|---|---|---|
| **`DS0001`** (`PTB-XL`) | Cardiologist consensus SCP-ECG diagnostic statements (`scp_codes`, likelihood $>0$) | **Non-NORM Diagnostic ECG (`y_ptb_nonnorm=1`):** At least one SCP superclass among `MI` (`5,486`), `STTC` (`5,123`), `HYP` (`2,655`), or `CD` (`4,907`) (`12,306` overall; secondary 5-class multi-label head retained) | **`NORM`-Only (`y_ptb_nonnorm=0`):** Exclusively `NORM` likelihood $>0$ with zero pathological superclasses (`9,111` overall) | Exclude `420` records with zero diagnostic SCP statements; exclude `133` `<18y` & `89` missing-age records for adult benchmark; quarantine `ecg_id=12722` (`V5` flatline lead) | Exact adult eligible count computed deterministically at `STEP-018/019` (`strat_fold 1–10` preserved patient-disjoint) |
| **`DS0002`** (`CARDIO-ML-ED`) | Mashhad ED physician + cardiologist consensus (`Initial diagnosis`, `Final diagnosis`, `Death`) | **Primary ED Triage Target (`y_ed_cardiac=1`):** `Initial diagnosis == 'Cardiac'` (`346` overall)<br>**Secondary Acute CVD Target (`y_ed_acute_cvd=1`):** `Final diagnosis` $\in$ `{ACS (57), MI (9), Cardiac-arrest (7), Arrhythmia (18), Hypertensive crisis (64)}` (`155` confirmed acute/hypertensive cases); secondary mortality `Death=1` (`10`) | **Primary Control (`0`):** `Initial diagnosis == 'Noncardiac'` (`233` overall)<br>**Secondary Control (`0`):** `Final diagnosis == 'Noncardiac'` (`148`) | Missing `Initial diagnosis` (`2`) -> Exclude; missing `Final diagnosis` (`237`) -> `uncertain/excluded` for secondary target (**never coerced to `0`**); `Elevated blood pressure (24)` & `Electrolyte-imbalance (17)` analyzed in sensitivity (`TBD` by Cardiologist `UD02`); exclude `12` `<18y` & `4` missing-age rows; isolate `8` `.jpg` strips & `2` typo IDs (`140354`, `148679`) per `RISK0012` | `581` clinical rows (`565` adult rows $\ge 18y$; `327` adult linked `C+E_img+L` base IDs; group repeated `12` `Col1` encounters strictly within splits) |
| **`DS0003`** (`CAIR-CVD-2025`) | Bangladeshi cross-sectional risk stratification (`CVD Risk Level`) | **Primary Binary (`y_cair_high=1`):** `CVD Risk Level == 'HIGH'` (`728`) | **Primary (`0`):** `LOW (220) + INTERMEDIARY (581)` (`801`); **Sensitivity Control:** `LOW (220)` only vs `HIGH` | Flag `65` rows with `Systolic BP <= Diastolic BP` & `13` rows with `Estimated LDL < 0` for deterministic rule-based exclusion vs train-only imputation sensitivity (`STEP-019/021`) | `1,529` adults (`25.0–79.0 y`; `0` `<18y`, `0` exact duplicate rows) |
| **`DS0004`** (`Kaggle sulianova`) | Preventive checkup clinical diagnosis flag (`cardio`) | `cardio == 1` (`34,979` raw) | `cardio == 0` (`35,021` raw) | Exclude/quarantine `1,323` implausible BP rows (`ap_hi <= ap_lo` or out-of-range), `30` extreme heights (`<100` or `>220 cm`), `7` extreme weights (`<30` or `>200 kg`), `24` exact duplicate rows (deduplicate to `1`), and `17` discordant duplicate feature-vector pairs (`34` conflicting rows excluded) | `70,000` raw adult records (`29.6–64.9 y`; clean eligible $N \approx 68{,}600+$ verified deterministically at `STEP-018`) |

---

## 2. Study Horizon Classification & Temporal Anchoring ($t_0, \Delta t$, `UD03`)

- **Honest Design Declaration (`OS §5.1 #2` & `RISK0002`):** Across **`DS0001`**, **`DS0002`**, **`DS0003`**, and **`DS0004`**, the prediction construct is strictly **Cross-Sectional / Acute Index-Visit Diagnostic CVD Risk Stratification** (`NOT multi-year longitudinal incident CVD forecasting`).
- **Mandatory Manuscript Wording Guardrail:** Thesis and Q1 paper prose MUST describe outputs as *"early/index-visit multimodal CVD risk stratification and diagnostic discrimination"* and explicitly assign multi-year longitudinal follow-up + prospective Bangladesh hospital validation to Future Work.
- **Index Timestamp ($t_0$) & Alignment Window ($\Delta t$):**
  - `DS0001`: $t_0 =$ time of 10-second 12-lead ECG acquisition; clinical anthropometrics/demographics recorded at the same acquisition window ($\Delta t = 0$).
  - `DS0002`: $t_0 =$ Emergency Department arrival / triage intake; ED vitals, initial blood draw (`CBC/BMP/ABG/Troponin`), and ED 12-lead ECG belong to the same acute index ED presentation. **Strict Temporal Cutoff:** Any discharge status, inpatient death, cause of death, final ED disposition diagnosis, or post-diagnosis intervention is strictly $> t_0$ and **prohibited** from feature tensors.
  - `DS0003` & `DS0004`: $t_0 =$ single outpatient / checkup assessment visit ($\Delta t =$ concurrent physical exam + lab blood draw + lifestyle questionnaire).
- **Medical History Leakage Control (`DS0002`):** Five encounters in `Previous surgeries` contain `'CABG'` (prior coronary artery bypass graft surgery — established severe CAD!). These MUST NOT masquerade as "unremarkable baseline risk": `CABG` is audited as prior known CVD history and tested in sensitivity exclusions during Stage `S13/S14`.

---

## 3. PROBAST Domain 3 — Incorporation Bias Control (`OS §5.1 #3`)

Diagnostic endpoints in clinical datasets often depend directly on specific biomarkers or ECG interpretation:
1. **`Troponine - I (Q)` Hazard in `DS0002` (`CARDIO-ML-ED`):** Populated in `385/581` ED patients (`<0.05`: `380`; elevated quantitative `0.31–29.9`: `5`; missing `196` MNAR!). Because clinicians use Troponin-I directly to rule in `ACS`/`MI`, two mandatory benchmark regimes are locked:
   - **`Tier A (Primary No-Incorporation-Bias Predictors):`** Excludes `Troponine - I (Q)` (plus `ECG Labels.csv` diagnoses and prior `CABG` flags in sensitivity) from inputs to measure true baseline `Clinical + ECG Image + Routine Lab` predictive value cleanly.
   - **`Tier B (Sensitivity Full-Lab Panel):`** Incorporates censored/thresholded `Troponine - I (Q)` strictly for transparent comparison (`OS §5.1`).
2. **Computed / Derived Composite Columns in `DS0003` (`CAIR-CVD-2025`):**
   - **`CVD Risk Score` (`10.53–24.17`)** and **`Blood Pressure Category`** are downstream derived score/category fields overlapping the assignment of **`CVD Risk Level`**. Both are **permanently excluded** (`IncorporationBiasRisk = High/Exclude`) from predictors!
   - **Pre-Split SMOTE Prohibited:** Fixes comparator `P0022`'s leakage error cleanly (`zero` synthetic oversampling before splitting).
3. **Diagnostic Text Strings in `DS0001` & `DS0002`:** `scp_codes`, `report`, `infarction_stadium1/2`, `ECG Labels.csv`, `Initial diagnosis`, `Final diagnosis`, `Death`, `Cause of death`, `Patient Status on Discharge` are targets/metadata ONLY — **permanently barred** from input features (`variables.csv` checks enforce exclusion).

---

## 4. Qualified Cardiologist Clinical Approval Block (`UD02, UD03, UD09`)

*Per Blueprint `STEP-014` & `OS §14.2 G05`: This charter is technically complete for team review; transition of Gate `G05` to `PASS` strictly requires formal signed clinical ratification below.*

| Reviewer Role | Name & Credentials | Review Focus | Date | Status / Signature |
|---|---|---|---|---|
| **Academic Supervisor** | Md. Mizanur Rahman (DIU CSE) | Methodological alignment (`DEC0004`, `RQ1–RQ4`) | Pending `G05` | Pending `G05` clinical review |
| **Qualified Cardiologist (`UD02/03/09`)** | **Unresolved / Human Decision Required** (`TBD` per `scope.md §8.2`) | Clinical validity of `y_ed_cardiac`/`y_ed_acute_cvd` vs `y_ptb_nonnorm`, `Troponin-I Tier A/B`, `CABG` prior-CVD handling, & borderline `Elevated BP/Electrolyte` disposition | Pending | **Awaiting Cardiologist Engagement (`G05`)** |
