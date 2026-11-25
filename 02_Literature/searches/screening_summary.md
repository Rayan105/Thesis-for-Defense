# PRISMA Screening Reconciliation & Eligibility Summary (`STEP-006`)

| Metadata | Value |
|---|---|
| Document | `02_Literature/searches/screening_summary.md` |
| Version | v1.0.0 |
| Step | STEP-006 |
| Date | 2026-11-26 |
| Primary Screener | Mohammad Nafis Sadiq (`232-15-895`) |
| Audit & Reconciliation | Rayan Ahmed (`232-15-847`) |
| Reviewer / Supervisor | Md. Mizanur Rahman |
| Source Registries | [papers.csv](file:///e:/FYDP/02_Literature/papers.csv), [screening.csv](file:///e:/FYDP/02_Literature/screening.csv) |
| Governing Sections | OS §3.2; Blueprint STEP-006 |
| PHI Sensitivity | Tier 1 (Public / Git-safe) |

---

## 1. PRISMA 2020 Eligibility Flow Reconciliation

All counts below are deterministically computed from `02_Literature/papers.csv` and `02_Literature/screening.csv`:

```text
[Identification]
  Records identified across 5 Google Scholar queries (Q1–Q5): n = 128 query-paper tags
    - SEARCH-SCHOLAR-Q1: 49
    - SEARCH-SCHOLAR-Q2: 21
    - SEARCH-SCHOLAR-Q3: 20
    - SEARCH-SCHOLAR-Q4: 21
    - SEARCH-SCHOLAR-Q5: 17
  Cross-query duplicates removed: n = 45 (0 duplicate DOIs / titles remaining)
        │
        ▼
[Screening & Full-Text Eligibility]
  Unique candidate PDFs assessed at Full-Text stage: n = 83 (P0001–P0083 / SCR0001–SCR0083)
        │
        ├──► Full-Text Excluded: n = 41 (P0043–P0083)
        │
        ▼
[Included Portfolio]
  Studies included for methodological synthesis & extraction: n = 42 (P0001–P0042)
```

### Arithmetic Verification
- `128 (query hits) - 45 (cross-query overlaps) = 83 (unique candidates)`
- `83 (unique candidates) - 41 (excluded at full-text) = 42 (included portfolio)`
- `Status` (`papers.csv`) vs `Decision` (`screening.csv`) mismatches: **0** (`42 Included == 42 Include`, `41 Excluded == 41 Exclude`).

---

## 2. Full-Text Exclusion Breakdown ($n = 41$)

| Exclusion Code & Detailed Reason | Count | Excluded Paper IDs |
|---|---|---|
| **`EX-LOW-PRIORITY`**: Lower methodological relevance/rigor compared to selected top 42 portfolio | 16 | `P0045, P0050, P0056, P0057, P0064, P0065, P0066, P0067, P0068, P0069, P0073, P0077, P0079, P0080, P0082, P0083` |
| **`EX-UNIMODAL`**: Unimodal or unlinked non-patient-aligned datasets | 8 | `P0044, P0049, P0055, P0060, P0062, P0070, P0071, P0078` |
| **`EX-NO-EVAL`**: Methodological / reporting integrity red flags (`6`) or target-derived synthetic vital signs leakage (`1`) | 7 | `P0046, P0047, P0048, P0051, P0058, P0061, P0074` |
| **`EX-NO-FULLTEXT`**: Abstract-only conference supplement without full experimental protocol | 4 | `P0052, P0053, P0054, P0081` |
| **`EX-OUTCOME`**: Non-CVD target (`T2DM`, mental stress detection) | 2 | `P0072, P0075` |
| **`EX-NO-ECG`**: Explicitly ECG-free signals (`PCG-only`, nocturnal ECG-free) | 2 | `P0043, P0076` |
| **`EX-DUP`**: Correction/erratum notice for an already screened systematic review | 1 | `P0059` |
| **`EX-POP`**: Pediatric population ($< 18$ years) | 1 | `P0063` |
| **Total Excluded** | **41** | Verified (`16 + 8 + 7 + 4 + 2 + 2 + 1 + 1 = 41`) |

---

## 3. Included Corpus Taxonomy ($n = 42$)

### 3.1 By `screening.csv` Relevance Group (`protocol.md` §4)
| Relevance Group | Count | Included Paper IDs | Role in Synthesis |
|---|---|---|---|
| **Group 1: Direct Multimodal CVD Comparators** | 15 | `P0001, P0002, P0003, P0004, P0007, P0008, P0011, P0017, P0020, P0021, P0022, P0023, P0024, P0025, P0027` | Primary benchmarks for fusion design, incremental modality value, & `PG1–PG5` testing |
| **Group 2: Transformer & Cross-Modal Fusion Architecture** | 12 | `P0006, P0012, P0013, P0014, P0015, P0016, P0018, P0019, P0036, P0037, P0038, P0039` | Cross-attention, missing-modality handling, and ECG encoder design comparators |
| **Group 3: Multimodal XAI & Faithfulness Benchmarks** | 8 | `P0028, P0029, P0030, P0031, P0032, P0033, P0034, P0035` | Quantitative SHAP faithfulness (AOPC), shortcut audits, & interpretability trade-offs |
| **Group 4: Contextual Benchmarks, Reviews & Clinical Baselines** | 7 | `P0005, P0009, P0010, P0026, P0040, P0041, P0042` | Seminal ECG/EHR risk score reviews, clinical scores, & PROBAST meta-analyses |
| **Total Included** | **42** | Verified (`15 + 12 + 8 + 7 = 42`) | |

### 3.2 By Local PDF Portfolio Organization
- `01_Core_Multimodal_CVD` (`10`): `P0001–P0010`
- `02_Transformer_CrossModal_Fusion` (`9`): `P0011–P0019`
- `03_Modality_Lab_Lifestyle` (`8`): `P0020–P0027`
- `04_Multimodal_Explainability_XAI` (`8`): `P0028–P0035`
- `05_Missing_Modality_RealWorld_Clinical` (`7`): `P0036–P0042`

---

## 4. Audit Findings & Mandatory Checks Carried Into `STEP-007`

1. **Single-Screener Origin:** Initial PDF intake and screening (`f19ebb2`) were executed by Mohammad Nafis Sadiq (`Owner = Mohammad Nafis Sadiq`, `Reviewer = Automated+Human Review`). During `STEP-007`, Rayan Ahmed will independently cross-verify the direct comparators (`Group 1` & `Group 3`) against full texts.
2. **Competing 3–4 Modality & SOTA Studies Retained Honestly:** Strong studies combining 3–4 modalities or evaluating MIMIC-IV / UK Biobank / ARIC (e.g., `P0016`, `P0020`, `P0022`, `P0023`, `P0025`, `P0030`, `P0037`, `P0038`) are retained in full to prevent selective novelty bias.
3. **Preliminary Column Audit Flag (`XAIEvaluated` vs `XAIUsed`):** Automated inspection of `papers.csv` indicates several rows (`P0003`, `P0007`) where `XAIUsed` notes qualitative-only or baseline-only XAI while `XAIEvaluated` was pre-tagged `"Yes (quantitative faithfulness)"`. All 42 `XAIEvaluated` flags and `PROBASTRisk` ratings (`Pending Step 007`) MUST be reconciled directly against the full-text PDFs during `STEP-007`.
4. **PDF Availability Prerequisite for `STEP-007`:** Local `papers/` PDF binaries are currently stored on Mohammad Nafis Sadiq's machine (excluded from Git via `.gitignore`). Syncing those PDFs locally (via encrypted/shared drive outside Git) is required to extract exact sample sizes, quantitative metrics, page/table locators, and PROBAST flags into `02_Literature/summaries/P####.md`.
