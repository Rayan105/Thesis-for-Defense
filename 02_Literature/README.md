# 02_Literature

| Metadata | Value |
|---|---|
| TemplateID | T01 (readme.md) |
| Purpose | Zero-seed PRISMA-aligned systematic literature search, screening logs, paper extraction summaries, gap synthesis, and claim ledgers |
| Owner | Literature Lead: Rayan Ahmed (`232-15-847`) |
| Inputs | Multi-database queries (PubMed, IEEE Xplore, Scopus, Google Scholar, arXiv), proposal gaps `PG1–PG5` |
| Outputs | `searches/*.md`, `papers.csv`, `screening.csv`, `summaries/P####.md`, `gaps.csv`, `gap_notes/*.md`, `claims.csv`, `references.bib`, `synthesis.md` |
| PHI Sensitivity | Tier 1 (Public / Git-safe). Note: Paywalled full-text PDFs are excluded from Git via `.gitignore`. |
| Governing Sections | OS §3; Blueprint Stages S03, S04 (`STEP-004`–`STEP-009`) |

## Folder Contract
- All literature searches must record verbatim query syntax, timestamps, filters, and count exports in `searches/`.
- Every paper extraction (`P####.md`) must verify original full text and cite exact page/table numbers.
- No citations or benchmark claims may be fabricated.
- Research gaps (`GAP####.md`) must rigorously evaluate proposal gaps `PG1–PG5` against counterevidence.
