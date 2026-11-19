# Systematic Error Analysis & PROBAST-AI Bias Review

| Field | Value |
|---|---|
| TemplateID | T20 (error_probast.md) |
| template_version | v1.0.0 |
| entity_id | Unresolved / Human Decision Required |
| owner | Rayan Ahmed (232-15-847), Mohammad Nafis Sadiq (232-15-895) |
| date | 2026-11-20 |
| status | Template / Blank |
| source_inputs | not reported |
| governing_section | OS §7.3, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

# Error & PROBAST-AI Audit — EVAL####

## 1. Stratified Error Review
- False Positive (FP) Case Analysis: [Common patterns, e.g., borderline hypertension + high cholesterol]
- False Negative (FN) Case Analysis: [Common patterns, e.g., atypical presentation or missing lifestyle markers]
- Label Uncertainty vs Model Error: [Review with clinical adjudicator]

## 2. PROBAST-AI (Prediction Model Risk of Bias Assessment)
| Domain | Risk of Bias Rating | Key Considerations & Mitigations |
|---|---|---|
| Domain 1: Participants | [Low / High / Unclear] | Consecutive clinical cohort, clear eligibility criteria |
| Domain 2: Predictors | [Low / High / Unclear] | Blinded predictor assessment, zero post-diagnosis predictors |
| Domain 3: Outcome | [Low / High / Unclear] | Objective CVD definition, blind adjudication, no incorporation bias |
| Domain 4: Analysis | [Low / High / Unclear] | Patient-level splits, post-split fitting, EPV sizing, calibration reported |
| **Overall Risk of Bias** | **[Low / High]** | **Overall study rating** |
