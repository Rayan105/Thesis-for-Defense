# CVD Multimodal Project Execution Timeline

| Stage | Name | Target Steps | Target Gate | Estimated Duration | Status |
|---|---|---|---|---|---|
| **S01** | Foundation & Unresolved-Decision Charter | STEP-001 | G01 | Week 1 | **COMPLETED Docs** *(Awaiting local PDF root copy for `C2`)* |
| **S02** | Repository, PHI Storage & Tooling Setup | STEP-002–003 | G02 | Week 1–2 | **COMPLETED (`G02 PASS`)** |
| **S03** | Zero-Seed PRISMA Systematic Literature Review | STEP-004–007 | Feeds G03 | Week 2–3 | **COMPLETED (`42/42` verified)** |
| **S04** | Proposal Gap Testing (`PG1–PG5`) & Q1 RQs | STEP-008–009 | G03 | Week 3–4 | **COMPLETED (`G03 PASS`)** |
| **S05** | Ethics Exemption, Secondary Intake & Hash Lock | STEP-010–012 | Feeds G04 | Week 4–5 | **COMPLETED (`DS0001–04` + `ECGS/` hashed)** |
| **S06** | 4-Modality Quality, ECG Integrity & Cohort Approval | STEP-013 | G04 | Week 5 | **COMPLETED (`G04 PASS`)** |
| **S07** | Clinical Endpoint Ontology & 4-Modality Schema | STEP-014–015 | G05 | Week 6 | **COMPLETED (`G05 PASS` under `DEC0005 OptA`)** |
| **S08** | Pilot Abstraction & Clinical Adjudication QA | STEP-016–018 | G06 | Week 6–7 | **COMPLETED (`G06 PASS`, `91,781` Clean)** |
| **S09** | Leakage-Safe Split, Preprocessing & Release | STEP-019–022 | G07, G08 | Week 7–8 | **In Progress (`STEP-019` Done -> `STEP-020` Next)** |
| **S10** | Architecture Selection, Runtime Lock & Smoke Run | STEP-023–027 | G09 | Week 8–9 | Planned *(incl. Multi-DB lit update #1)* |
| **S11** | Controlled Experiments, Baselines & Ablations | STEP-028–031 | G10 | Week 9–11 | Planned |
| **S12** | Validation Selection, Calibrator Fit & Test Freeze | STEP-032–033 | G11 | Week 11–12 | Planned |
| **S13** | Held-Out Metrics, Calibration, Stats & DCA | STEP-034–036 | G12 | Week 12–13 | Planned |
| **S14** | Subgroup Fairness, Missing Robustness & PROBAST | STEP-037 | G13 | Week 13–14 | Planned |
| **S15** | Multimodal SHAP, Faithfulness (AOPC) & Clinician Review | STEP-038–040 | G14 | Week 14–15 | Planned |
| **S16** | Research Decision-Support Prototype & Audit | STEP-041–042 | G15 | Week 15–16 | Planned |
| **S17** | FYDP Thesis, Q1 Manuscript (TRIPOD+AI) & Archive | STEP-043–050 | G16, G17 | Week 16–18 | Planned *(incl. Multi-DB lit update #2)* |

---

> [!NOTE]
> Secondary-data pivot (`DEC0004 Option B`) accelerated Stage `S05–S08` curation based on measured `STEP-016` dual-stream QA throughput (`32.3 rec/s` across raw files). External clinical review milestones (`G08` ECG filter morphology & `G14` SHAP plausibility) remain gated on qualified clinical sign-off rather than deadlines.
