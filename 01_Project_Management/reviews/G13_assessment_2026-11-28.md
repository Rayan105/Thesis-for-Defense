# G13 Assessment — Subgroup Fairness, Missing-Modality Stress & PROBAST-AI (`Pending Human Sign-Off`)

| Field | Value |
|---|---|
| TemplateID | T22 (gate_audit.md) |
| AssessmentID | `G13-20261128-01` |
| GateID | `G13` |
| DocumentOrEntityScope | `EVAL0001` (`subgroup_fairness.csv`, `missing_modality_robustness.csv`, `error_probast.md`), [PROBAST_AI.md](../../12_Writing/checklists/PROBAST_AI.md), Tier-2B `clinician_review_n24_s15.json` |
| EntityVersions | `EVAL0001 v1.0.0`, `PROBAST_AI v1.0.0` |
| Outcome | **`NOT ASSESSED`** *(Quantitative fairness, stress & PROBAST-AI ready; awaiting Qualified Cardiologist error review & Supervisor sign-off)* |
| Assessor | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |
| Human Approver | Pending (`Cardiologist Adjudicator; Md. Mizanur Rahman`) |
| Assessment Date | `2026-11-28` |

## Mandatory Criteria Checklist (`STEP-037`)
| # | Criterion | Verified Evidence | Status |
|---|---|---|---|
| C1 | Subgroup stratification (`Sex, AgeBand, Cohort, ModalityTier`) | [subgroup_fairness.csv](../../09_Evaluation_Stats/EVAL0001/subgroup_fairness.csv) (`DS0002` missing-ECG recall gap disclosed) | **EVIDENCED (Technical PASS)** |
| C2 | Missing-modality inference stress tests without retraining | [missing_modality_robustness.csv](../../09_Evaluation_Stats/EVAL0001/missing_modality_robustness.csv) | **EVIDENCED (Technical PASS)** |
| C3 | Four-domain PROBAST-AI honest self-audit | [PROBAST_AI.md](../../12_Writing/checklists/PROBAST_AI.md) | **EVIDENCED (Technical PASS)** |
| C4 | Stratified `N=24` (`6 TP/FP/TN/FN`) clinical error review & Supervisor sign-off | Tier-2B `clinician_review_n24_s15.json` awaiting Cardiologist + Supervisor | **PENDING HUMAN SIGN-OFF** |
