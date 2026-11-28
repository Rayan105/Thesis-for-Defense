# Multimodal Explainability Audit Report (`XAI0001` — `STEP-038–040`)

| Field | Value |
|---|---|
| TemplateID | T21 (xai_audit.md) |
| XAIID | `XAI0001` (Executed cleanly on Frozen `MODEL0015` & `MC0004`; Pending Cardiologist/Supervisor `G14` Sign-Off) |
| Linked Evaluation | `EVAL0001` (`REL0001/test`) |
| Background Distribution | `REL0001 Train` ONLY (`N_bg = 256`, `64/cohort`, `BackgroundHash = fd797cf5...`) |
| Local Additivity | `TreeSHAP <= 8.3e-7` (PASS); Exact `2^4` Coalition Shapley `<= 4.44e-16` (PASS); 50-Step IG `MaxRelErr = 0.0325` (> `0.02` target, flagged honestly) |
| Global Modality Shares (`C / E / L / S`) | `44.80% / 27.19% / 14.69% / 13.31%` (Pooled `N=224`; `DS0001 ECG=78.50%`, `DS0002 ECG=28.49%`, `DS0003 Life=43.46%`, `DS0004 Clin=71.99%`) |
| LOMO Concordance | **Spearman `rho = 1.0`**, **Pearson `r = 0.9761`** |
| Quantitative Faithfulness (`AOPC`) | **Deletion `+0.017086`** > Random `-0.000544` & Reverse `-0.000746`; **Insertion `0.478866`** > Random `0.456323` |
| Multi-Seed & Noise Stability | **5-Seed Spearman `rho = 0.9816`**, **Kendall `tau = 0.9231`**, Top-5 Jaccard `0.5298`, Lipschitz `rho = 0.8194` |
| Spurious-Shortcut Audit | **Champion `MC0015` `CLEAN (0/4)`** vs Unimodal `MC0004 XGB` (`DS0001 weight_kg_isnan #2`) |
| Cardiologist Plausibility (`N=24`) | `04_Outcome_Schema_QA/adjudications/clinician_review_n24_s15.json` (**Pending External Cardiologist Sign-Off for `G14`**) |
