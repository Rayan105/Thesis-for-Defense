# Systematic Literature Search Record — Google Scholar Search Wave

| Field | Value |
|---|---|
| TemplateID | T04 (search.md) |
| template_version | v1.0.0 |
| entity_id | SEARCH-SCHOLAR-20261125 |
| owner | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |
| date | 2026-11-25 |
| status | Executed (Registered in `papers.csv` & `screening.csv`) |
| source_inputs | `02_Literature/searches/protocol.md`, Google Scholar 5-Theme Query Suite |
| governing_section | OS §3.1, §3.2; Blueprint STEP-005 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Rayan Ahmed, Md. Mizanur Rahman |

---

## 1. Search Identification & Database Coverage
- **Database Engine:** Google Scholar
- **Execution Date:** 2026-11-25 (`f19ebb2` intake wave)
- **Language Filter:** English full-text PDFs retrieved (`2022–2026` publication years across the 42 included studies)
- **Queries Executed (per `screening.csv` `SearchRecord` tags):**
  - `SEARCH-SCHOLAR-Q1`: Core Multimodal CVD Risk Prediction (ECG + Clinical/Lab/Lifestyle)
  - `SEARCH-SCHOLAR-Q2`: Transformer Multimodal Fusion & Missing Modalities
  - `SEARCH-SCHOLAR-Q3`: Explainable AI (SHAP / XAI Faithfulness & Calibration) in CVD
  - `SEARCH-SCHOLAR-Q4`: Lifestyle Factors & Laboratory Biomarkers Incremental Value (`PG4`)
  - `SEARCH-SCHOLAR-Q5`: Real-World Clinical Missing-Modality & Regional/South Asian Context

---

## 2. Quantitative Yield & Deduplication Reconciliation

| Query Identifier | Registered Candidate Matches | Included Portfolio Matches | Excluded Matches |
|---|---|---|---|
| `SEARCH-SCHOLAR-Q1` | 49 | 25 | 24 |
| `SEARCH-SCHOLAR-Q2` | 21 | 13 | 8 |
| `SEARCH-SCHOLAR-Q3` | 20 | 9 | 11 |
| `SEARCH-SCHOLAR-Q4` | 21 | 12 | 9 |
| `SEARCH-SCHOLAR-Q5` | 17 | 11 | 6 |
| **Total Query-Paper Tags** | **128** | **70** | **58** |
| **Multi-Query Deduplication Overlap** | **-45** | **-28** | **-17** |
| **Unique Candidate Papers Registered** | **83** (`P0001–P0083`) | **42** (`P0001–P0042`) | **41** (`P0043–P0083`) |

> [!NOTE]
> Raw unexported search-engine hit-counter totals prior to local PDF download were `not reported` at intake (`f19ebb2`). All 83 registered candidates underwent full-text PDF retrieval verification (`MetadataVerified = Verified (Full-Text PDF)`), with zero duplicate DOIs and zero duplicate normalized titles confirmed.

---

## 3. Storage & Coverage Limitations
1. **Local PDF Custody (`.gitignore` Compliance):** Downloaded PDF binaries (`papers/01_Core_Multimodal_CVD/` through `papers/05_Missing_Modality_RealWorld_Clinical/`) are stored locally outside public Git under the `.gitignore` rule `papers/`.
2. **Database Coverage Note:** This primary retrieval wave relied on Google Scholar multi-query retrieval. Standalone structured exports from PubMed/MEDLINE, IEEE Xplore, and Scopus (`protocol.md`) remain available as supplementary verification checks prior to `G03` if broader database sensitivity is required.
3. **DOI Availability:** 41 of 42 included studies carry verified DOIs; `P0001` (`Botros2024_P0001`) lists `DOI = not reported` in `papers.csv` and is tracked via its verified ScienceDirect URL in [references.bib](file:///e:/FYDP/02_Literature/references.bib).
