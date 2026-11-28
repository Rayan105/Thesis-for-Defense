# Four-Domain PROBAST-AI Self-Audit (`STEP-037` / Gate `G13`)

| Field | Value |
|---|---|
| Document | `12_Writing/checklists/PROBAST_AI.md` |
| Linked Evaluation | `EVAL0001` (`REL0001 v1.0.0`, `MODEL0015`) |
| Assessors | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |
| Sign-Off Required | Qualified Cardiologist Adjudicator + Supervisor Md. Mizanur Rahman (`G13`) |

## Domain-by-Domain Signaling Audit
1. **Domain 1 — Participants (Risk of Bias: `High` due to Multi-Cohort Secondary Design / Applicability):** While `DS0001` (`PTB-XL`) and `DS0002` (`CARDIO-ML-ED`) represent clinical ECG populations and `DS0003` (`CAIR-CVD-2025`) is a Bangladeshi screening cohort, pooling 4 secondary datasets (`DEC0004`) creates cohort-spectrum heterogeneity (`80.9%` `DS0004` tabular dominance) and lacks an unpooled multi-center prospective Bangladeshi clinical cohort (bounded explicitly as Future Work).
2. **Domain 2 — Predictors (Risk of Bias: `Low`):** `variables.csv` (`v1.0.1`) excludes post-diagnosis treatment proxies and Tier-A Troponin leakage; all imputation/scaling (`PP0001`) fits strictly on `REL0001 Train`; modality-masking preserves missingness flags without fabricating cross-patient ECG waveforms (`DEC0006`).
3. **Domain 3 — Outcome (Risk of Bias: `Moderate / Unclear`):** `ADJ0001–0004` enforce blind objective outcome definitions (`endpoint_charter.md`, κ=`1.0` deterministic rule audit), yet `DS0003` and `DS0004` measure cross-sectional CVD prevalence rather than longitudinal time-to-event horizons (`DEC0005`).
4. **Domain 4 — Analysis (Risk of Bias: `Low`):** Zero patient leakage across `91,781` rows (`89,005` unique `PatientGroupID`s); zero pre-split SMOTE; `5`-seed variance separated from `B=2,000` patient-cluster bootstrap CIs; Validation-only temperature calibration and threshold freezing (`CalibratorHash ea5e5d96`); pre/post calibration and DCA reported transparently; null/negative findings (`EarlyConcat XGB > Single-Seed Transformer` on pooled `DS0004`-heavy AUC, `CNN2D` weakness) disclosed completely.
- **Overall Self-Assessed PROBAST-AI Judgement:** **Low Analytical Leakage Risk of Bias; High Contextual/Spectrum Risk of Bias** (explicitly avoiding false "All-Low" inflation).
