# G01 Assessment — Scope and Decision Charter

| Field | Value |
|---|---|
| AssessmentID | G01-20261120-01 |
| GateID | G01 |
| DocumentOrEntityScope | `01_Project_Management/scope.md`, `01_Project_Management/decisions.csv`, `01_Project_Management/decision_log/DEC0001.md` |
| EntityVersions | `scope.md` v1.0.0; `decisions.csv` v0.1.0; `DEC0001.md` v1.0.0 |
| Initial Status | NOT ASSESSED |
| Assessor | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Assessment Date | 2026-11-20 |
| Named Human Reviewer | Md. Mizanur Rahman (Supervisor, Senior Lecturer, Dept. of CSE, DIU) |
| Governing References | OS §1.1–§1.4, §12.1, §14.1–§14.2; Blueprint STEP-001 |
| PHI Sensitivity | Tier 1 (Public / Git-safe) |

---

## 1. Gate Criteria Evaluation Matrix

| Criterion # | Mandatory Criterion Description | Required Evidence Path | Current Evidence State & SHA-256 | Status | Corrective Action Required |
|---|---|---|---|---|---|
| **C1** | **Verbatim approved title preserved** without abbreviation, omission, or unauthorized drift across all foundational files. | `01_Project_Management/scope.md` | *An Explainable Multimodal Framework for Early Cardiovascular Disease Risk Prediction Using Clinical, ECG, Laboratory, and Lifestyle Data* verified verbatim against `RF01`. | **EVIDENCE PREPARED** | Pending physical supervisor re-confirmation. |
| **C2** | **Source facts RF01–RF18 verified** against physical `fydp_title_proposal.pdf`. | `fydp_title_proposal.pdf` (pp.1–6) | Expected SHA-256: `BA7DD0EF21C8A2CA77B2E1BAFC2AC5A0E1FEC584E221C848085A971EAACEEFA8`. File currently absent from local workspace directory. | **BLOCKED** | Place immutable copy of `fydp_title_proposal.pdf` into workspace root and execute cryptographic hash verification. |
| **C3** | **Scope and clinical exclusions charter adopted** covering 4 modalities, 6 proposal metrics, Bangladesh context, and safety boundaries. | `01_Project_Management/scope.md` | `01_Project_Management/scope.md` created; includes explicit exclusion of medical imaging as primary input and clinical decision support vs autonomous diagnostic boundary. | **EVIDENCE PREPARED** | Requires formal dated sign-off from supervisor and researchers. |
| **C4** | **All 26 Unresolved Decisions (UD01–UD26) assigned** named owners, governing sections, and blocking milestones. | `01_Project_Management/scope.md` (§7); OS §12.1 | 26 items assigned between Rayan Ahmed and Mohammad Nafis Sadiq with explicit blocking gate mappings. Zero scientific parameters prematurely guessed. | **EVIDENCE PREPARED** | Confirm workload allocation in upcoming supervisor meeting. |
| **C5** | **Title Phase Evaluation Report / examiner feedback status formally confirmed** (UD01). | `01_Project_Management/decision_log/DEC0001.md` | `DEC0001.md` drafted outlining Options A, B, and C. Status is `Unresolved / Human Decision Required`. | **AWAITING HUMAN DECISION** | Supervisor and researchers must confirm whether any written evaluation report exists. |
| **C6** | **Dated human supervisor confirmation** recorded. | Supervisor sign-off block in `scope.md` and meeting minutes | Signature block in `scope.md` is currently blank awaiting physical/digital signature. | **AWAITING HUMAN APPROVAL** | Schedule alignment session with Md. Mizanur Rahman. |

---

## 2. Gate Outcome and Determination

- **Overall Outcome:** **NOT ASSESSED** *(Blocks transition to STEP-002)*
- **Rationale:** While all documentary evidence (`scope.md`, `decisions.csv`, `DEC0001.md`) has been fully drafted and prepared according to OS §1, §14, and §15:
  1. The physical primary authority file `fydp_title_proposal.pdf` must be copied into the root workspace and hash-verified (`C2`).
  2. Supervisor Md. Mizanur Rahman has not yet provided dated written approval (`C5`, `C6`).
  
Per OS §14.1, a gate may evaluate to **PASS** only when 100% of mandatory criteria are evidenced with cryptographic hashes, file paths, and named human approval. Incomplete evidence remains **NOT ASSESSED**, which strictly prohibits proceeding to repository lock (`STEP-002`).

---

## 3. Invalidated Downstream Gates and Dependent Steps

The following steps and gates are blocked until G01 formally transitions to **PASS**:
- **Blocks Step:** `STEP-002` (Repository creation, PHI safe storage policy, minimal runtime lock)
- **Blocks Step:** `STEP-003` (Materialize all templates `T01–T32` and CSV registries)
- **Blocks Gate:** `G02` (Repository skeleton and minimal tooling verification)
- **Invalidates Downstream Entities:** No downstream entities exist yet (workspace is in initial zero-execution state).

---

## 4. Reassessment and Remediation Plan

1. **Step 1 (Researchers):** Copy `fydp_title_proposal.pdf` to `e:\FYDP\` and verify SHA-256 against `BA7DD0EF21C8A2CA77B2E1BAFC2AC5A0E1FEC584E221C848085A971EAACEEFA8`.
2. **Step 2 (Researchers & Supervisor):** Convene alignment meeting to review `scope.md`, resolve `DEC0001` (confirming absence/presence of separate evaluation report), and execute signature block.
3. **Step 3 (Assessor):** Re-audit G01 under new `AssessmentID: G01-20261120-02`, record verified file hashes, and update `01_Project_Management/gates.csv` to `PASS`.
