# 05_Preprocessing_Alignment

| Metadata | Value |
|---|---|
| TemplateID | T01 (readme.md) |
| Purpose | Alignment specifications, ECG filter contracts, training-only fitted transformation states, and leakage test reports |
| Owner | Preprocessing Lead: Rayan Ahmed (`232-15-847`) |
| Clinical Reviewer | Qualified Cardiologist (for ECG filter morphology and ST-T segment preservation) |
| Inputs | Frozen split partitions (`SPLIT####`), variable definitions (`variables.csv`), raw signal configurations |
| Outputs | `preprocessing_registry.csv`, `specs/*`, `configs/*`, `reports/PP####.md`, fitted states in Tier 2B / Tier 3 |
| PHI Sensitivity | Tier 1 (Code & configs); Tier 2B (restricted processed tables and fitted transform parameters excluded from Git). |
| Governing Sections | OS §4.4, §4.5; Blueprint Stage S09 (`STEP-021`–`STEP-022`) |

## Folder Contract
- Record-local cleaning (e.g. ECG notch filtering) is strictly separated from training-fitted operations.
- All scalers, imputers, and categorical encoders must be fitted strictly on the Training partition; fitting on validation or test partitions is prohibited.
- Reusable transformation logic resides in `src/cvd_mm/preprocess.py`.
