# G14 Assessment — Multimodal XAI Faithfulness, Stability, Shortcut & Clinical Audit (`Pending Human Sign-Off`)

| Field | Value |
|---|---|
| TemplateID | T22 (gate_audit.md) |
| AssessmentID | `G14-20261128-01` |
| GateID | `G14` |
| DocumentOrEntityScope | `XAI0001` (`report.md`, `modality_shares.csv`, `aopc_faithfulness.csv`, `stability_and_concordance.csv`, `shortcut_audit.md`, `additivity_check.md`, `clinician_plausibility_summary.md`) |
| EntityVersions | `XAI0001 v1.0.0`, `MODEL0015` (5 seeds), `BackgroundHash fd797cf5...` |
| Outcome | **`NOT ASSESSED`** *(Quantitative XAI executed cleanly; awaiting External Cardiologist plausibility review & Supervisor disposition on IG 3.25% completeness note)* |
| Assessor | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Human Approver | Pending (`Rayan Ahmed; Cardiologist Adjudicator; Md. Mizanur Rahman`) |
| Assessment Date | `2026-11-28` |

## Mandatory Criteria Checklist (`STEP-038–040`)
| # | Criterion | Verified Evidence & Honest Caveats | Status |
|---|---|---|---|
| C1 | Train-only background (`N=256`) + additivity audit | [additivity_check.md](../../10_Explainability_XAI/XAI0001/additivity_check.md) (`TreeSHAP<=8.3e-7`, `2^4 Coalition<=4.44e-16`; 50-step IG `0.0325` flagged) | **EVIDENCED (IG Caveat Logged)** |
| C2 | Deletion/Insertion `AOPC` vs Random/Reverse controls & LOMO concordance | [faithfulness_stability_report.md](../../10_Explainability_XAI/XAI0001/faithfulness_stability_report.md) (`Del +0.0171 > -0.0005/-0.0007`; `LOMO rho=1.0`) | **EVIDENCED (Technical PASS)** |
| C3 | 5-Seed XAI stability & Lipschitz noise check | `Seed5 Spearman=0.9816`, `Kendall=0.9231`, `Lipschitz=0.8194` | **EVIDENCED (Technical PASS)** |
| C4 | Spurious-shortcut audit & Cardiologist `N=24` rubric sign-off | [shortcut_audit.md](../../10_Explainability_XAI/XAI0001/shortcut_audit.md) (`MC0015 CLEAN` vs `MC0004 DS0001 weight_kg_isnan #2`); Cardiologist sign-off pending | **PENDING HUMAN SIGN-OFF** |
