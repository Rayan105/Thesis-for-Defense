# Systematic Literature Search Record — arXiv, Google Scholar & PhysioNet

| Field | Value |
|---|---|
| TemplateID | T04 (search.md) |
| template_version | v1.0.0 |
| entity_id | SEARCH-PREPRINT-01 |
| owner | Rayan Ahmed (`232-15-847`) |
| date | 2026-11-20 |
| status | Ready for Execution |
| source_inputs | OS §3.1, `02_Literature/searches/protocol.md` |
| governing_section | OS §3.1; Blueprint STEP-004, STEP-005 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Search Identification & Metadata
- Databases: arXiv (cs.LG, eess.SP, q-bio.QM), Google Scholar, PhysioNet (MIMIC-IV-ECG, PTB-XL literature)
- Target: Preprints (2024–2026), open multimodal Transformer benchmarks, and seminal clinical trial risk calculators
- Date Window: 2018 to 2026

## 2. Search Strategy & API Queries
### arXiv API Query:
```text
http://export.arxiv.org/api/query?search_query=all:"multimodal"+AND+all:"ECG"+AND+all:"cardiovascular"+AND+(all:"tabular"+OR+all:"EHR")+AND+(all:"transformer"+OR+all:"fusion")&start=0&max_results=100
```

### Google Scholar Snowballing Queries:
```text
"multimodal" "ECG" ("clinical" OR "EHR") ("laboratory" OR "lifestyle") "cardiovascular disease" "risk prediction" "transformer"
```

## 3. Preprint-to-Journal Deduplication Protocol
- Every arXiv/bioRxiv preprint retrieved is actively cross-referenced against Scopus and PubMed to detect whether a final peer-reviewed journal version exists.
- If a journal version exists, the peer-reviewed version is registered as primary (`P####`) and the preprint locator is logged as secondary evidence.
