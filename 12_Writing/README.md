# 12_Writing

| Metadata | Value |
|---|---|
| TemplateID | T01 (readme.md) |
| Purpose | FYDP undergraduate thesis, Q1 biomedical journal manuscript, TRIPOD+AI & PROBAST-AI compliance checklists, and supervisor/peer review response ledgers |
| Owner | Writing Leads: Mohammad Nafis Sadiq (Thesis Lead), Rayan Ahmed (Q1 Paper Lead) |
| Supervisor | Md. Mizanur Rahman |
| Inputs | Claims registry (`claims.csv`), evaluation reports (`EVAL####`), XAI reports (`XAI####`), figures and tables |
| Outputs | `writing_registry.csv`, `thesis/*`, `paper_q1/*`, `checklists/TRIPOD_AI.csv`, `reviews/*` |
| PHI Sensitivity | Tier 1 (Public / Git-safe). |
| Governing Sections | OS §10; Blueprint Stage S17 (`STEP-043`–`STEP-048`) |

## Folder Contract
- Every empirical assertion, reported metric, and clinical interpretation must trace directly to a verified claim ID in `claims.csv`.
- 100% of bibliographic references in `references.bib` must be verified against original publisher DOIs.
- TRIPOD+AI (2024) checklist must be completed with exact section/page locators before manuscript submission.
