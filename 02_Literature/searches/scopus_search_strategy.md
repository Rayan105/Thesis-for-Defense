# Systematic Literature Search Record — Scopus (Elsevier)

| Field | Value |
|---|---|
| TemplateID | T04 (search.md) |
| template_version | v1.0.0 |
| entity_id | SEARCH-SCOPUS-01 |
| owner | Rayan Ahmed (`232-15-847`) |
| date | 2026-11-20 |
| status | Ready for Execution |
| source_inputs | OS §3.1, `02_Literature/searches/protocol.md` |
| governing_section | OS §3.1; Blueprint STEP-004, STEP-005 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Search Identification & Database Metadata
- Database Engine: Scopus (Elsevier)
- Search Target: Interdisciplinary medical informatics, computer science, and bioinformatics journals (*Computers in Biology and Medicine*, *Artificial Intelligence in Medicine*, *Information Fusion*)
- Date Window: 2018 to 2026 (`PUBYEAR > 2017`)
- Language Filter: English (`LANGUAGE(english)`)
- Document Types: Articles, Conference Papers, Reviews

## 2. Verbatim Boolean Query String
```text
TITLE-ABS-KEY (
  ("cardiovascular disease" OR "coronary artery disease" OR "heart disease" OR "CVD" OR "myocardial infarction" OR "heart failure")
  AND
  ("multimodal" OR "multi-modal" OR "data fusion" OR "cross-modal" OR "feature fusion" OR "transformer fusion")
  AND
  ("ECG" OR "electrocardiogram" OR "electrocardiography" OR "12-lead")
  AND
  ("clinical" OR "EHR" OR "electronic health record" OR "laboratory" OR "biomarker" OR "lifestyle")
  AND
  ("risk prediction" OR "early detection" OR "screening" OR "prognosis")
)
AND PUBYEAR > 2017
AND LANGUAGE (english)
```

## 3. Execution Plan & Export Target
- Raw Export Target: `02_Literature/searches/exports/scopus_raw_export.csv`
- Deduplication Protocol: Match by DOI, PMID, and normalized title
- Registration Target: `02_Literature/papers.csv` and `screening.csv`
