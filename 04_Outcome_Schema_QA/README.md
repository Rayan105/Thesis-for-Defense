# 04_Outcome_Schema_QA

| Metadata | Value |
|---|---|
| TemplateID | T01 (readme.md) |
| Purpose | Clinical CVD endpoint ontology, 4-modality variable dictionary, Case Report Forms (CRF), 12-lead ECG signal contract, and adjudication QA logs |
| Owner | Clinical Schema Lead: Mohammad Nafis Sadiq (`232-15-895`) |
| Clinical Reviewer | Qualified Cardiologist / Clinical Adjudicator |
| Inputs | Medical consensus definitions, ICD-10 diagnostic codes, ECG technical specs, pilot extraction batches |
| Outputs | `endpoint_charter.md`, `variables.csv`, `crf/*`, `ecg_contract.md`, `adjudication_registry.csv`, `reviews/ADJB####.md` |
| PHI Sensitivity | Tier 1 (Public / Git-safe). Restricted adjudication source charts remain in Tier 2B. |
| Governing Sections | OS §5; Blueprint Stages S07, S08 (`STEP-014`–`STEP-018`) |

## Folder Contract
- Clinical endpoint definitions ($t_0$, $\Delta t$, CVD diagnostic criteria) require formal signed cardiologist review.
- Every variable in `variables.csv` must define explicit data types, valid clinical ranges, units, and missingness policies.
- Adjudication agreement metrics (Cohen's $\kappa$, ICC) must satisfy prospective quality thresholds prior to cohort freeze.
