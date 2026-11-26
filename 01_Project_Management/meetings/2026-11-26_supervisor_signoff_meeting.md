# MEET-20261126-001 — Supervisor Ratification & Secondary Cohort Gate Review Meeting

| Field | Value |
|---|---|
| TemplateID | T30 (risk_meeting.md) |
| template_version | v1.0.0 |
| entity_id | MEET-20261126-001 |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | 2026-11-26 |
| status | Approved / Logged (`Team-Reported Physical Supervisor Sign-Off 2026-11-26`) |
| source_inputs | `DEC0001.md`, `DEC0002.md`, `DEC0004.md`, `scope.md` (`v1.1.0`), `02_Literature/research_questions.md` (`v1.1.0`), `03_Datasets_Cohort/reports/cohort_cards_DS0001_to_DS0004.md` |
| governing_section | OS §1.4, §3, §4, §12.1, §13, §14.1–§14.2, §15.2 (`T30`) |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman (Supervisor) |

---

## 1. Meeting Overview
- **Date:** `2026-11-26` (Time of repository logging: `23:33:00+06:00`)
- **Attendees:** Md. Mizanur Rahman (Supervisor, Senior Lecturer, Dept. of CSE, DIU), Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`)
- **Provenance Note:** Physical/supervisor ratification obtained by researchers on `2026-11-26` and logged into workspace governance files per `OS §12.1` and `§14.1` (physical signed hardcopy / PDF artifacts retained offline by team; `fydp_title_proposal.pdf` local root hash check for `G01 C2` tracked separately).

---

## 2. Ratified Decisions & Gate Progress Audit
1. **`DEC0001` (`UD01`) — Option B Approved:** Confirmed signed Proposal Approval Form (`09.07.2026`) is sole Title Phase baseline authority (modified solely by `DEC0004` regarding secondary data cohorts).
2. **`DEC0002` (`UD02–UD26`) — Option A Approved (`G03`):** Approved Q1 Research Questions (`RQ0, RQ1–RQ4`), narrowed `GAP0001–GAP0002` / supported `GAP0003–GAP0005` positioning, Null/Negative-Result Publishability Policy, and initial `2026-11-25` Google Scholar PRISMA corpus (`83 -> 42` full texts verified) with mandatory `PubMed`, `IEEE Xplore`, and `Scopus` update runs scheduled at `STEP-023` & `STEP-048`. Unblocks **`G03 PASS` (`G03-20261126-02`)**.
3. **`DEC0004` (`UD01, UD04, UD05, UD06`) — Option B Approved (`Scope v1.1.0` & `G04`):** Ratified scope transition from hospital primary collection (`RF09`) to verified secondary open multi-cohort datasets (`DS0001 PTB-XL`, `DS0002 CARDIO-ML-ED` + extracted `408` `ECGS/` images, `DS0003 CAIR-CVD-2025`, `DS0004 Kaggle sulianova`) under strict zero-stitching missing-modality rules (`Complete4ModalityCount=0`), bounding prospective Bangladesh hospital validation explicitly as Future Work. Combined with full `408`-image extraction/PHI audit in `DS0002`, unblocks **`G04 PASS` (`G04-20261126-02`)**.
4. **Pending External Engagement (`Stage S07` / `G05`):** Engage a qualified Cardiologist / Clinical Adjudicator (`scope.md §8.2`, `UD02/UD03/UD08/UD09`) to ratify `STEP-014` (`endpoint_charter.md`, `variables.csv`) and `STEP-015` (`ecg_contract.md`, `G05`) prior to clinical adjudication release (`G06`).

---

## 3. Domain Risk Register Directives
- **`RISK0011` Resolved:** `CARDIO-ML-ED` multi-part `.rar` volumes (`ECGS.part01..21.rar`) extracted locally (`400 .png` + `8 .jpg` = `408` non-corrupt images hashed and PHI-inspected).
- **`RISK0012` Opened:** Address visually observed `CARDIO-ML-ED` image heterogeneity (`.png` cropped 12-row strips still retain red millimeter paper grid despite `README.txt` claim, whereas `8` `.jpg` files contain uncropped 6-lead margins) and `2` typo ID discrepancies (`140354/1403354`, `148679/148676`) in Stage `S07–S09`.
- **Retain local `fydp_title_proposal.pdf` (`G01 C2`):** Copy scanned `fydp_title_proposal.pdf` (matching `BA7DD0EF...`, already `.gitignore`d) into `e:\FYDP\` to close `G01` Criterion `C2` (`G01` otherwise approved via `DEC0001`/`DEC0004`).
