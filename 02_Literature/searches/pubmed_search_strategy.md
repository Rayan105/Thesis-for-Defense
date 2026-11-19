# Systematic Literature Search Record — PubMed / MEDLINE

| Field | Value |
|---|---|
| TemplateID | T04 (search.md) |
| template_version | v1.0.0 |
| entity_id | SEARCH-PUBMED-01 |
| owner | Rayan Ahmed (`232-15-847`) |
| date | 2026-11-20 |
| status | Ready for Execution |
| source_inputs | OS §3.1, `02_Literature/searches/protocol.md` |
| governing_section | OS §3.1; Blueprint STEP-004, STEP-005 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

## 1. Search Identification & Database Metadata
- Database Engine: PubMed / MEDLINE (National Library of Medicine)
- Search Target: Biomedical, clinical cardiology, and translational AI literature
- Date Window: 2018/01/01 to 2026/11/20
- Language Filter: English (`English[lang]`)
- Document Types: Journal Articles, Clinical Studies, Comparative Studies, Multicenter Studies

## 2. Verbatim Boolean Query String
```text
(
  "Cardiovascular Diseases"[Mesh] OR "Heart Diseases"[Mesh] OR "Myocardial Infarction"[Mesh] OR 
  "Heart Failure"[Mesh] OR "cardiovascular disease*"[tiab] OR "coronary artery disease*"[tiab] OR 
  "heart disease*"[tiab] OR "CVD"[tiab] OR "myocardial infarction"[tiab] OR "heart failure"[tiab]
)
AND
(
  "Multimodal Learning"[Mesh] OR "multimodal"[tiab] OR "multi-modal"[tiab] OR 
  "data fusion"[tiab] OR "cross-modal"[tiab] OR "feature fusion"[tiab] OR "hybrid deep learning"[tiab]
)
AND
(
  "Electrocardiography"[Mesh] OR "ECG"[tiab] OR "electrocardiogram*"[tiab] OR 
  "electrocardiograph*"[tiab] OR "12-lead"[tiab]
)
AND
(
  "Electronic Health Records"[Mesh] OR "Biomarkers"[Mesh] OR "Life Style"[Mesh] OR 
  "clinical"[tiab] OR "laboratory"[tiab] OR "biomarker*"[tiab] OR "lifestyle"[tiab] OR 
  "EHR"[tiab] OR "vital signs"[tiab]
)
AND
(
  "Risk Assessment"[Mesh] OR "risk prediction"[tiab] OR "early detection"[tiab] OR 
  "screening"[tiab] OR "prognosis"[tiab] OR "diagnosis"[tiab]
)
AND
("2018/01/01"[Date - Publication] : "2026/11/20"[Date - Publication])
AND (English[lang])
```

## 3. Execution Plan & Export Target
- Raw Export Target: `02_Literature/searches/exports/pubmed_raw_export.csv`
- Deduplication Protocol: Match by PMID and DOI against other database yields
- Expected Yield Handling: All candidate records registered into `02_Literature/papers.csv` and `screening.csv` in STEP-005.
