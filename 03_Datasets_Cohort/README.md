# 03_Datasets_Cohort

| Metadata | Value |
|---|---|
| TemplateID | T01 (readme.md) |
| Purpose | Clinical site documentation, IRB authorization pointers, cohort intake manifests, quality cards, and patient-level leakage-free split manifests |
| Owner | Cohort & IRB Lead: Mohammad Nafis Sadiq (`232-15-895`) |
| Custodian | Hospital Data Custodian / Qualified Clinical Partner |
| Inputs | Approved IRB protocol, hospital DUA/MOU, de-identified primary hospital intake tables, 12-lead ECG signals |
| Outputs | `sites.csv`, `datasets.csv`, `releases.csv`, `reports/*_card.md`, `splits/SPLIT####/` (split manifests and reports) |
| PHI Sensitivity | Tier 1 for metadata/manifests; Tier 2B for local de-identified cohorts (`raw/`, `processed/` excluded from Git); Tier 2A isolated offline. |
| Governing Sections | OS §4, §11; Blueprint Stages S05, S06, S09 (`STEP-010`–`013`, `STEP-019`–`020`) |

## Folder Contract
- Raw hospital clinical tables and raw ECG waveforms must remain completely immutable once hashed.
- All patient-level splits must enforce zero patient/encounter/record overlap between train, validation, and test partitions.
- Never commit identifiable patient data or linkage tables to Git.
