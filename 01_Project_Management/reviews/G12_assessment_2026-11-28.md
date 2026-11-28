# G12 Assessment — Held-Out Quantitative Metrics, Calibration, Stats & DCA (`Pending Human Sign-Off`)

| Field | Value |
|---|---|
| TemplateID | T22 (gate_audit.md) |
| AssessmentID | `G12-20261128-01` |
| GateID | `G12` |
| DocumentOrEntityScope | `EVAL0001` (`metrics_summary.csv`, `confusion_matrices.csv`, `calibration_metrics.csv`, `bootstrap_cis.csv`, `paired_stat_tests.csv`, `dca_net_benefit.csv`, `report.md`) |
| EntityVersions | `EVAL0001 v1.0.0`, `REL0001 v1.0.0`, `MODEL0015` + `EXP0015_ENS5` (`N=12,719`) |
| Outcome | **`NOT ASSESSED`** *(Package verified complete & pushed for Mohammad Nafis Sadiq & Supervisor Md. Mizanur Rahman sign-off)* |
| Assessor | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |
| Human Approver | Pending (`Mohammad Nafis Sadiq; Md. Mizanur Rahman`) |
| Assessment Date | `2026-11-28` |

## Mandatory Criteria Checklist (`STEP-033–036`)
| # | Criterion | Verified Evidence | Status |
|---|---|---|---|
| C1 | Frozen custody & 100% Test coverage (`12,719/12,719`, `0` NaNs) | [coverage_audit.md](../../09_Evaluation_Stats/EVAL0001/coverage_audit.md) (`NPZ SHA256=92748e44f175774a...`) | **EVIDENCED (Technical PASS)** |
| C2 | All 6 mandatory + Q1 discrimination/calibration metrics + 5-seed variance | [report.md](../../09_Evaluation_Stats/EVAL0001/report.md) (`AUC=0.8131`, `ENS5=0.8162`, `ECE=0.0186`) | **EVIDENCED (Technical PASS)** |
| C3 | `B=2,000` cluster bootstrap, paired DeLong, exact McNemar, Holm & DCA | [stats_dca_notes.md](../../09_Evaluation_Stats/EVAL0001/stats_dca_notes.md) (`EXP0012 > EXP0015` pooled AUC honestly disclosed) | **EVIDENCED (Technical PASS)** |
| C4 | Evaluation & Biostatistics Lead + Supervisor formal sign-off | Pending human confirmation | **PENDING HUMAN SIGN-OFF** |
