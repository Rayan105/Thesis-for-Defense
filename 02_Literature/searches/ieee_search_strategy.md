# Systematic Literature Search Record — IEEE Xplore

| Field | Value |
|---|---|
| TemplateID | T04 (search.md) |
| template_version | v1.0.0 |
| entity_id | SEARCH-IEEE-01 |
| owner | Rayan Ahmed (`232-15-847`) |
| date | 2026-11-20 |
| status | Ready for Execution |
| source_inputs | OS §3.1, `02_Literature/searches/protocol.md` |
| governing_section | OS §3.1; Blueprint STEP-004, STEP-005 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Search Identification & Database Metadata
- Database Engine: IEEE Xplore Digital Library
- Search Target: Biomedical engineering, signal processing, and multimodal architectures (*IEEE JBHI*, *IEEE TBME*, *IEEE Access*, EMBC)
- Date Window: 2018 to 2026
- Document Types: IEEE Journals, Transactions, and Conference Proceedings
- Language Filter: English

## 2. Verbatim Boolean Query String
```text
(
  ("Document Title":"cardiovascular" OR "Abstract":"cardiovascular" OR "Document Title":"heart disease" OR "Abstract":"heart disease" OR "Document Title":"CVD" OR "Abstract":"CVD")
  AND
  ("Document Title":"multimodal" OR "Abstract":"multimodal" OR "Document Title":"multi-modal" OR "Abstract":"multi-modal" OR "Document Title":"fusion" OR "Abstract":"fusion")
  AND
  ("Document Title":"ECG" OR "Abstract":"ECG" OR "Document Title":"electrocardiogram" OR "Abstract":"electrocardiogram")
  AND
  ("Document Title":"clinical" OR "Abstract":"clinical" OR "Document Title":"tabular" OR "Abstract":"tabular" OR "Document Title":"laboratory" OR "Abstract":"laboratory" OR "Document Title":"lifestyle" OR "Abstract":"lifestyle")
  AND
  ("Document Title":"prediction" OR "Abstract":"prediction" OR "Document Title":"detection" OR "Abstract":"detection" OR "Document Title":"risk" OR "Abstract":"risk")
)
```

## 3. Execution Plan & Export Target
- Raw Export Target: `02_Literature/searches/exports/ieee_raw_export.csv`
- Deduplication Protocol: Match by DOI and normalized title against PubMed and Scopus yields
- Registration Target: `02_Literature/papers.csv` and `screening.csv`
