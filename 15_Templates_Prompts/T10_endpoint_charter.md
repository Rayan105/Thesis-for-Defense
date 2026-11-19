# Clinical Endpoint & Ascertainment Charter

| Field | Value |
|---|---|
| TemplateID | T10 (endpoint_charter.md) |
| template_version | v1.0.0 |
| entity_id | Unresolved / Human Decision Required |
| owner | Rayan Ahmed (232-15-847), Mohammad Nafis Sadiq (232-15-895) |
| date | 2026-11-20 |
| status | Template / Blank |
| source_inputs | not reported |
| governing_section | OS §5.1, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

# Clinical Endpoint Charter — CVD Risk Prediction Target

## 1. Operational CVD Definition & Target Construct
- Target Name: Early Cardiovascular Disease Event / High Risk
- Classification Type: Binary Classification (0 = Non-CVD / Low Risk, 1 = Documented CVD Event / High Risk)
- Diagnostic Ascertainment Criteria: [Exact ICD-10 codes / Clinical adjudication rubric]

## 2. Temporal Anchoring & Leakage Prevention
- Index Timestamp ($t_0$): [Exact clinical reference point, e.g. admission or initial screening]
- Maximum Permissible Modality Window ($\Delta t$): [e.g., within 24 hours of $t_0$]
- Lookback Horizon: [Predictors originating strictly $\le t_0$]
- Lookahead / Prediction Horizon: [e.g., in-hospital, 1-year, or cross-sectional early risk]

## 3. Incorporation Bias Controls
- Predictor Exclusion Rule: Predictors used to define the gold standard outcome are strictly excluded from input feature spaces.

## 4. Cardiologist Approval Block
- Reviewing Cardiologist: [Name, MD/FCPS]
- Affiliation: [Cardiology Department / Hospital]
- Approval Date: Pending
