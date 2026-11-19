# 10_Explainability_XAI

| Metadata | Value |
|---|---|
| TemplateID | T01 (readme.md) |
| Purpose | Multimodal SHAP protocols, game-theoretic attributions, quantitative faithfulness benchmarks (Deletion/Insertion AOPC), multi-seed stability audits, and cardiologist plausibility reviews |
| Owner | XAI Lead: Rayan Ahmed (`232-15-847`) |
| Clinical Reviewer | Qualified Cardiologist / Clinical Adjudicator |
| Inputs | Frozen champion model, training partition background sample, held-out test cohort |
| Outputs | `xai_protocol.md`, `xai_registry.csv`, `XAI####/report.md`, modality shares, beeswarm/waterfall specs |
| PHI Sensitivity | Tier 1 (Safe global attributions and de-identified case figures). Full per-patient SHAP tensor arrays reside in Tier 3. |
| Governing Sections | OS §8; Blueprint Stage S15 (`STEP-038`–`STEP-040`) |

## Folder Contract
- SHAP background distribution must be constructed exclusively from the Training partition.
- Explanations must undergo quantitative faithfulness benchmarking (AOPC vs random control) and shortcut audits before making interpretability claims.
- Never assert causal biological claims or "increased clinical trust" from SHAP values without an actual IRB-approved clinician reader trial.
