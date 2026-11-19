# AI Task Prompt Specification Contract

| Field | Value |
|---|---|
| TemplateID | T31 (prompt.md) |
| template_version | v1.0.0 |
| entity_id | Unresolved / Human Decision Required |
| owner | Rayan Ahmed (232-15-847), Mohammad Nafis Sadiq (232-15-895) |
| date | 2026-11-20 |
| status | Template / Blank |
| source_inputs | not reported |
| governing_section | OS §12, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

# PROMPT-### — [AI Task Role & Prompt Contract]

## 1. Role & Task Boundary
- Assigned AI Role: [e.g., Code Implementer / Literature Review Assistant / Statistical Analyst]
- Task Objective: [Specific bounded task]
- Governing Handbook Sections: [OS §#]

## 2. Authorized Inputs & Paths
- Allowed Read Paths: [List explicit file paths]
- Allowed Write Paths: [List explicit file paths]
- Prohibited Modifications: Core governance files, immutable releases, sealed test sets

## 3. Strict Biomedical & Ethical Guardrails
- **PROHIBITION:** Never paste patient identifiers, raw hospital charts, or PHI into prompts.
- **ZERO FABRICATION:** If data or literature citations are missing, mark `not reported` or `Unresolved / Human Decision Required`.
- **HUMAN BOUNDARY:** Clinical definitions and gate sign-offs strictly require qualified human review.
