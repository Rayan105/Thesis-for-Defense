# G03 Assessment — Systematic Literature Search and Q1 Research Questions

| Field | Value |
|---|---|
| TemplateID | T22 (gate_audit.md) |
| template_version | v1.0.0 |
| entity_id | G03-20261126-01 |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | 2026-11-26 |
| status | Open (`Awaiting Supervisor Decision & Sign-Off`) |
| source_inputs | `02_Literature/` (`protocol.md`, `SEARCH_SCHOLAR_2026-11-25.md`, `screening_summary.md`, `papers.csv`, `screening.csv`, `references.bib`, `summaries/P0001–P0042.md`, `comparative_matrix.md`, `gaps.csv`, `gap_notes/GAP0001–0005.md`, `synthesis.md`, `claims.csv`, `research_questions.md`); `01_Project_Management/decision_log/DEC0002.md` |
| governing_section | OS §1.4, §3.1–§3.4, §14.1, §14.2 (`G03`); Blueprint `STEP-004`–`STEP-009` |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman (Supervisor) |

---

# G03 Assessment — Systematic Literature & Q1 Research Questions (`v1.0.0`)

| Field | Value |
|---|---|
| AssessmentID | `G03-20261126-01` |
| GateID | `G03` |
| DocumentOrEntityScope | `02_Literature/research_questions.md`, `02_Literature/synthesis.md`, `02_Literature/gaps.csv`, `02_Literature/claims.csv`, `02_Literature/papers.csv`, `02_Literature/screening.csv`, `02_Literature/references.bib`, `02_Literature/searches/`, `01_Project_Management/decision_log/DEC0002.md`, `DEC0004.md` |
| EntityVersions | `protocol.md` v1.0.0; `SEARCH_SCHOLAR_2026-11-25.md` v1.0.0; `screening_summary.md` v1.0.0; `papers.csv` v1.0.0; `gaps.csv` v1.1.0 (`DEC0004` sync); `claims.csv` v1.1.0; `synthesis.md` v1.0.0; `research_questions.md` v1.1.0 (`DEC0004` sync); `DEC0002.md` v1.0.0; `DEC0004.md` v1.0.0 |
| Outcome | **`NOT ASSESSED`** *(Documentary & computational evidence complete; awaiting Supervisor decision under `DEC0002` and signed `G03` approval)* |
| Assessor | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Human Approver | Md. Mizanur Rahman (Supervisor, Senior Lecturer, Dept. of CSE, DIU) |
| Assessment Date | `2026-11-26` *(Pending Human Sign-Off)* |

---

## 1. Mandatory Criteria Audit Matrix

| Criterion # | Mandatory Criterion (`OS §14.2` & `STEP-009`) | Required Evidence Path | Current Evidence State & SHA-256 Checksum | Automated / Documentary Audit | Corrective Action Required |
|---|---|---|---|---|---|
| **C1** | **Reproducible literature search logs & cutoff date (`OS §3.1, §3.4`):** Multi-database search strings, yield counts, deduplication, and explicit search cutoff date logged. | `02_Literature/searches/protocol.md`, `SEARCH_SCHOLAR_2026-11-25.md`, `research_questions.md` (§4), `DEC0002.md` | `protocol.md`: `aa1ff3ecc6e5fe491a017c0bcc51210f27f491fc55664b13c3d1e7a22572e371`<br>`SEARCH_SCHOLAR_2026-11-25.md`: `444cdb549d1254f8fb827aa842f9041b155af52fd80b745c697de66791e687f6`<br>Google Scholar `5`-query suite (`SEARCH-SCHOLAR-Q1`..`Q5`, cutoff `2026-11-25`) executed cleanly. **Open scope caveat:** `PubMed`, `IEEE Xplore`, `Scopus`, and `arXiv` strategies remain at `Ready for Execution` without structured exports (`DEC0002`). | **EVIDENCE PREPARED (SCOPE CAVEAT)** | Supervisor resolves `DEC0002` Option A (accept bounded Scholar wave + updates at `STEP-023/048`) vs Option B (run supplementary `PubMed/IEEE/Scopus` before `G03 PASS`). |
| **C2** | **PRISMA screening counts reconciled (`OS §3.2`):** Deterministic arithmetic reconciliation (`identified − duplicates = screened; screened − excluded = included`) with explicit exclusion codes (`EX-*`). | `02_Literature/searches/screening_summary.md`, `02_Literature/screening.csv` | `screening_summary.md`: `a760cb41daf1cb59ecf46bd4336e0cbef1e78e4f206406dd0c739cb792cedada`<br>`screening.csv`: `3a3573949cbfb78cbad8aa92ee4f69402d0d8db284d3bf68cad7785476ded1a0`<br>`128` query hits `− 45` overlaps `= 83` unique PDFs; `83 − 41` excluded (`8` EX codes) `= 42` included; `0` status/decision mismatches, `0` duplicate DOIs/titles. | **PASS (VERIFIED)** | None |
| **C3** | **Original full-text verified extractions & citations (`OS §3.2, §10.3`):** `100%` of included references verified against original full texts (`MetadataVerified=yes`) with exact page/table/figure locators and BibTeX parity. | `02_Literature/papers.csv`, `references.bib`, `summaries/P0001.md`–`P0042.md`, `comparative_matrix.md` | `papers.csv`: `6b80baacfc41c5ab6dc46deb37788f9620c418bd6bb8318d2479306719974226`<br>`references.bib`: `27b10827c836fe0bb6ba9ea0bb63db6310fb8c193209b8a495d62f9b0ab05d4e`<br>`comparative_matrix.md`: `a09ce8b7ae838f86b7adf61eb42c3c2362954d5d60d884650cbf2f80bb1a0d59`<br>`42/42` `P####.md` summaries completed (`pp. 1–last`); `42/42` `MetadataVerified=yes`; `42/42` `ReadingStatus=Extracted`; `42/42` BibTeX key parity (`P0001` DOI noted honestly as `not reported` in source PDF, traced via ScienceDirect PII URL); `20/24` false `XAIEvaluated` flags rectified. | **PASS (VERIFIED)** | None |
| **C4** | **`PG1–PG5` tested rigorously with counterevidence (`OS §3.3`):** Both supporting and contradicting `P####` studies documented honestly; zero unsupported `"first ever"` claims; search limitations stated transparently. | `02_Literature/gaps.csv`, `gap_notes/GAP0001.md`–`GAP0005.md`, `synthesis.md`, `claims.csv` | `gaps.csv`: `6eaf44587ca5a3a22a34aa94bb1d93f9070c468b54bcf7909eefebfc65746a38`<br>`synthesis.md`: `44c9fe7b546904264cc2159b99d423fc7da0a2699b7044977bae03f70b300115`<br>`claims.csv`: `799cc0d0d56c4d928c75a9819940a21273b400c3a3ae4cea84d56a8d0f19d429`<br>`PG1–PG2` narrowed against `14` $\ge 3$-stream comparators (`P0002, P0013, P0016, P0020–P0023, P0025, P0030–P0032, P0036–P0038`); `PG3–PG5` supported-within-search noting `4` partial/clinical XAI studies (`P0028, P0029, P0032, P0038`) and Low-PROBAST CMR comparator `P0038`; `CLAIM0001–CLAIM0013` linked with locators and contradictions. | **PASS (VERIFIED)** | None |
| **C5** | **Approved falsifiable RQ-to-evaluation map (`STEP-009`):** `RQ0, RQ1–RQ4` mapped cleanly to `O1–O4`, `GAP0001–0005`, `UD02–UD26`, 4-tier comparators, metrics, stats, XAI AOPC, claim boundaries, and null-result publishability contract. | `02_Literature/research_questions.md`, `01_Project_Management/decision_log/DEC0002.md`, `DEC0004.md` | `research_questions.md` (`v1.1.0`): `dc5a770e7089aeea36e3a4744f2c1cc3f555ec24767403c2f06b64e688c06ced`<br>`DEC0002.md`: `e2826cef8ee9d8e3c2efd9e3af2c8fc843d0c2ef23a308c7b6254b7df43ee30c`<br>`DEC0004.md`: `fe8f54a30cd677f8daa06cd39eb164e5e52c528925f9882e5e44ddf2613a2424`<br>Full traceability table completed (`RQ1–RQ4` + `RQ0`), explicit Null/Negative Findings Contract documented, `RQ4` adapted for secondary-cohort scope (`DEC0004`), search cutoff `2026-11-25` recorded. | **EVIDENCE PREPARED (AWAITING DECISION)** | Supervisor confirms RQ framing (`v1.1.0`), secondary-data scope pivot (`DEC0004`), bounded Q1 contributions (`C1–C4`), and Null/Negative Findings Contract (`DEC0002`). |
| **C6** | **Dated Supervisor human sign-off (`OS §14.1, §14.2`):** Named Supervisor Md. Mizanur Rahman approves RQs, gap positioning, search disposition, and signs `G03`. | Signature blocks in `research_questions.md`, `DEC0002.md`, and meeting minute | Currently unsigned (`Unresolved / Human Decision Required`). Per `OS §14.1`, AI assessment cannot substitute for human supervisor ratification. | **AWAITING HUMAN APPROVAL** | Conduct Supervisor alignment review with Md. Mizanur Rahman and record dated signature. |

---

## 2. Gate Outcome Determination

- **Overall Outcome:** **`NOT ASSESSED`** *(Awaiting Supervisor Review & Sign-Off under `DEC0002`)*
- **Rationale:**
  1. All computational, bibliographic, extraction (`42/42`), PRISMA reconciliation (`83 -> 42`), gap verification (`GAP0001–GAP0005`), claim grounding (`CLAIM0001–CLAIM0013`), and Q1 RQ traceability (`research_questions.md v1.0.0`) deliverables are complete, internally reconciled, and SHA-256 verified.
  2. Two items strictly require **Supervisor Md. Mizanur Rahman's** formal determination (`OS §14.1` prohibits AI self-certification):
     - **Human Sign-Off (`C6`):** Written confirmation of `RQ0/RQ1–RQ4`, narrowed `PG1–PG2` / `C1–C4` framing, and the Null/Negative Findings Publishability Contract (`STEP-009` procedure #3).
     - **Search Scope Determination (`C1` / `DEC0002`):** Confirming whether the initial Google Scholar search wave (`5` queries, `83` full-text PDFs, cutoff `2026-11-25`) suffices for `G03 PASS` (with `PubMed / IEEE Xplore / Scopus` deferred to scheduled `STEP-023` and `STEP-048` update runs) OR whether supplementary `PubMed/IEEE/Scopus` verification exports must execute before `G03 PASS`.
  3. Notice structural validator (`validate_repo.py`) and smoke tests remain green; zero PHI or copyrighted PDFs are tracked in Git.

---

## 3. Dependent Work & Corrective Actions

- **Blocked Transition (`OS §14.2`):** Formal lock of cohort endpoint/schema design (`G04–G05`) and institutional IRB filing (`STEP-011`) strictly require both **`G01 PASS`** and **`G03 PASS`**.
- **Permitted Preparatory Work:** While scheduling Supervisor review for `G01` & `G03`, non-human-blocked planning computation in `STEP-010` (prospective sample-size / Riley et al. EPV mathematical sizing formulas and external public-cohort compatibility screening) may be drafted provisionally and clearly tagged pending `G03` sign-off.
- **Invalidated Downstream Gates:** None (`G04–G17` remain `Blocked`).
- **Reassessment Plan:** Upon receiving Supervisor Md. Mizanur Rahman's signed `DEC0002` (plus supplementary PubMed/IEEE/Scopus runs if Option B is chosen), issue `G03-2026MMDD-02` with dated approval evidence and transition `gates.csv` row `G03` to **`PASS`**.
