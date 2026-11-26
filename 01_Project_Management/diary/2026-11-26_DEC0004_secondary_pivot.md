# Secondary Data Scope Pivot Log — `DEC0004` (`Kaggle / Mendeley / PhysioNet`)

| Field | Value |
|---|---|
| TemplateID | T03 (session.md) |
| template_version | v1.0.0 |
| session_id | SESS-20261126-010B |
| step_id | Scope Amendment (`DEC0004` bridging `STEP-010` $\rightarrow$ `STEP-011`) |
| stage_id | S05 (Secondary Cohort Licensing, Provenance & Ethics Exemption Audit) |
| date | 2026-11-26 |
| local_time | 11:12:00+06:00 |
| researchers | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| supervisor | Md. Mizanur Rahman (Senior Lecturer, Dept. of CSE, DIU) |
| status | Prepared (Awaiting Dataset Architecture Choice & Supervisor Approval) |
| governing_section | OS §1.1, §1.2 (`RF09`), §4.1; Blueprint `STEP-010`–`STEP-011` |
| phi_sensitivity | Tier 1 (Public / Git-safe) |

---

## 1. Change Summary
Per user directive (*working with secondary Kaggle/open benchmark data rather than primary Bangladesh hospital collection*), executed systematic governance sync without breaking verbatim title (`RF01`), Q1 statistical/XAI rigor, or anti-leakage rules:
1. Drafted `01_Project_Management/decision_log/DEC0004.md` establishing strict anti-stitching rules (`never concatenate unrelated patients from separate Kaggle CSVs`), rejecting scalar-only tabular substitutes lacking ECG signals, and framing Options A (`PhysioNet MIMIC-IV-ECG/MDS-ED + PTB-XL + CAIR-CVD-2025`), B (`Open Kaggle/Mendeley CARDIO-ML-ED + PTB-XL + CAIR-CVD-2025`), and C (`Custom Kaggle candidates post-audit`).
2. Amended `scope.md` (`v1.1.0`), `research_questions.md` (`v1.1.0`, adapting `RQ4` to secondary multi-cohort generalizability with prospective primary BD hospital work bounded to Future Work), and `gaps.csv` (`GAP0005`), re-hashing `G03_assessment_2026-11-26.md` accurately.
3. Added `SITE0009` (`CARDIO-ML-ED`) and `SITE0010` (`MIMIC-IV-Ext-MDS-ED`) to `03_Datasets_Cohort/sites.csv`, updated `SITE0007` (`CAIR-CVD-2025` as Missing-ECG branch candidate), and added `RISK0010` to `risk_register.csv`.
4. Adapted `STEP_TRACKER.md` and `dashboard.md` so `STEP-011` covers secondary-data license/CITI/DUA/provenance verification & institutional ethics-exemption clearance.
