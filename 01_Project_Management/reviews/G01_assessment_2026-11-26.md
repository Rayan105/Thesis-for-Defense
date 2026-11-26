# G01 Assessment — Scope and Decision Charter (`Reassessment`)

| Field | Value |
|---|---|
| TemplateID | T22 (gate_audit.md) |
| template_version | v1.0.0 |
| AssessmentID | `G01-20261126-01` |
| GateID | `G01` |
| Supersedes | `G01-20261120-01` |
| DocumentOrEntityScope | `01_Project_Management/scope.md` (`v1.1.0`), `01_Project_Management/decisions.csv`, `DEC0001.md`, `DEC0004.md`, `2026-11-26_supervisor_signoff_meeting.md` |
| Outcome | **`NOT ASSESSED`** *(C1, C3, C4, C5, C6 PASS after `2026-11-26` Supervisor approval of `DEC0001 Option B` & `DEC0004 Option B`; **C2 remains BLOCKED only because physical `fydp_title_proposal.pdf` is absent from local workspace root `e:\FYDP\` for SHA-256 verification**)* |
| Assessor | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Human Approver | Md. Mizanur Rahman (Supervisor, Senior Lecturer, Dept. of CSE, DIU) |
| Assessment Date | `2026-11-26` |
| Governing References | OS §1.1–§1.4, §12.1, §14.1–§14.2 (`G01`) |
| PHI Sensitivity | Tier 1 (Public / Git-safe) |

---

## 1. Mandatory Criteria Audit Matrix

| Criterion # | Mandatory Criterion | Evidence Path & SHA-256 | Status | Corrective Action Required |
|---|---|---|---|---|
| **C1** | Verbatim approved title preserved (`RF01`). | `01_Project_Management/scope.md` (`v1.1.0`): `967b4cb80f1b93a60733c53471dba5dc7011543ad8a00d890a11d925a1d3a9c1` | **PASS** | None |
| **C2** | Source facts `RF01–RF18` locally hash-verified against physical `fydp_title_proposal.pdf`. | Expected SHA-256: `BA7DD0EF21C8A2CA77B2E1BAFC2AC5A0E1FEC584E221C848085A971EAACEEFA8`; local workspace `Test-Path e:\FYDP\fydp_title_proposal.pdf = False`. | **BLOCKED (LOCAL FILE ABSENT)** | Copy `fydp_title_proposal.pdf` (gitignored) into `e:\FYDP\` to verify SHA-256 locally. |
| **C3** | Amended Scope Charter (`v1.1.0`) & Clinical Safety Boundaries ratified. | `01_Project_Management/scope.md`: `967b4cb80f1b93a60733c53471dba5dc7011543ad8a00d890a11d925a1d3a9c1` | **PASS** | None |
| **C4** | All `UD01–UD26` assigned named owners & gating milestones. | `01_Project_Management/scope.md` (§7) | **PASS** | None |
| **C5** | Title Phase evaluation report status (`DEC0001 Option B`) & secondary-data amendment (`DEC0004 Option B`) resolved. | `DEC0001.md`: `d332822db7de53ee357c2c7d3575276e8f5851ed792ce3e615d8169dba8f22e9`<br>`DEC0004.md`: `ad967c0b2c5cb520c631c27d973d8b7fd69aecc24aebd7c49db456311fdefa32` | **PASS** | None |
| **C6** | Dated Supervisor human sign-off recorded (`2026-11-26`). | `01_Project_Management/meetings/2026-11-26_supervisor_signoff_meeting.md`: `3aee2e73f7de4e4a974a44cc865a07af99e6c7e88dbf235530f85807b0744322` | **PASS** | Retain signed hardcopy scan offline. |

---

## 2. Determination (`OS §14.1`)
- **Overall Outcome:** **`NOT ASSESSED`** *(No conditional PASS permitted under `OS §14.1` while `C2` local PDF hash check cannot run locally; flips directly to **`PASS`** once `fydp_title_proposal.pdf` is placed in `e:\FYDP\` and SHA-256 verified).*
