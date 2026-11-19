# CVD MULTIMODAL PROJECT EXECUTION BLUEPRINT

## Cover page

**Approved research title:** An Explainable Multimodal Framework for Early Cardiovascular Disease Risk Prediction Using Clinical, ECG, Laboratory, and Lifestyle Data.

| Field | Value |
|---|---|
| Document | CVD_MULTIMODAL_PROJECT_EXECUTION_BLUEPRINT.md |
| Version / date | v1.0.0 / 2026-11-20 |
| Type | Sequential Q1-grade research execution manual |
| Governing handbook | [CVD Multimodal Research Operating System](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md), v1.0.0 |
| Primary scientific authority | [FYDP Title Proposal](./fydp_title_proposal.pdf) (6-page scanned Proposal Approval Form and Detailed Proposal; SHA-256 verified in [OS Appendix F](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-f)) |
| Status | Complete planning document; execution NOT VERIFIED; all gates `G01–G17` NOT ASSESSED |
| Coverage | 17 stages (`S01–S17`); 50 focused step types (`STEP-001`–`STEP-050`), with repeatable literature, curation/adjudication, experiment/ablation, and writing sessions |
| Owners | Researchers Rayan Ahmed (`232-15-847`) and Mohammad Nafis Sadiq (`232-15-895`), Supervisor Md. Mizanur Rahman, hospital data custodian, IRB authority, and qualified cardiologist/clinical adjudicator; task ownership recorded at `STEP-001` |
| Intended system | Reproducible Transformer-based four-modality (Clinical, ECG, Laboratory, Lifestyle) early CVD risk-prediction framework with quantitatively validated SHAP explainability, FYDP thesis, Q1 journal manuscript (TRIPOD+AI compliant), and research decision-support prototype; NOT validated clinical deployment |

## Version history

| Version | Date | Change | Approval |
|---|---|---|---|
| v1.0.0 | 2026-11-20 | Initial proposal-grounded 17-stage, 50-step Q1 execution roadmap aligned 1:1 to `CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md` | Proposed; human adoption pending |

## How to use this blueprint

1. Read the [source facts (`RF01–RF18`) and unresolved decisions (`UD01–UD26`)](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-01). `PROPOSAL FACT`, `PLANNING RECOMMENDATION`, and `Unresolved / Human Decision Required` carry identical definitions in both documents. The five proposal gap bullets (`PG1–PG5`) are hypotheses to verify, not established facts.
2. Start at the earliest unfinished step whose prerequisite gates are `PASS`. All 50 steps begin **NOT STARTED**; unchecked checklist boxes represent future verification requirements, not completed work. All 17 gates (`G01–G17`) begin **NOT ASSESSED**.
3. The handbook defines scientific policy; this manual sequences its execution. All [folder contracts](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-02), [CSV registry schemas](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-b), [templates `T01–T32`](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-15), and the [Universal DoD](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a) apply automatically to every step.
4. For each active session, log the step ID plus a dated batch (`ADJB####`, search batch) or `RUN####` identifier in `01_Project_Management/diary/`. Time estimates are **provisional planning estimates**, excluding external IRB turnaround, hospital enrollment delays, cardiologist review turnaround, and GPU compute duration unless noted.
5. `Parallelizable` permits independent work only after all prerequisites are evidenced and never permits crossing a `FAIL`, `NOT ASSESSED`, or `STALE` gate or editing canonical registries concurrently. Assign IDs and merge canonical CSV registries serially.
6. Run planning/review prompts before implementation prompts. Prompts enforce zero fabrication and strict PHI protection—never paste patient data, clinical charts, or raw hospital ECGs into external unapproved AI prompts.
7. A gate `PASS` requires dated, hash-verified evidence for exact entity versions plus named human review ([OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14)). Technically valid negative or null experimental outcomes (e.g., modest multimodal gain) do **not** constitute gate failure.
8. Only the two planning documents are authored at this stage alongside the untouched `fydp_title_proposal.pdf`. All listed repository paths are intended execution outputs to be created starting at `STEP-001`–`STEP-003`.

## Source-specific execution constraints

- **Zero-bibliography proposal (`RF06`):** `fydp_title_proposal.pdf` contains zero citations or reference list. `STEP-004`–`STEP-009` must build an original-source-verified, PRISMA-aligned literature foundation from scratch and test `PG1–PG5` against direct and contradicting multimodal CVD literature.
- **Ethics before intake (`RF09`):** Primary dataset collection from hospitals or diagnostic centers MUST NOT start before written IRB/ethics approval, hospital administrative authorization, and informed consent/waiver (`STEP-011`, `UD05`).
- **Workflow Diagram leakage reconciliation (`RF13`):** The proposal's Workflow Diagram (p.5) depicts Preprocessing (Box 2) and Feature Extraction (Box 3) visually before Train/Val/Test Split (Box 4). This blueprint enforces Q1 leakage isolation: only deterministic record-local checks and fixed-parameter ECG parsing precede `STEP-020` (`G07`); all dataset-fitted imputation, scaling, encoding, and learned feature extraction happen exclusively on the training partition in `STEP-021` (`G08`).
- **Four approved modalities (`RF10`):** Clinical, ECG signals, Laboratory results, and Lifestyle information. Medical imaging (echo, CT, MRI, X-ray) mentioned in Background Study is contextual literature only and strictly outside primary input scope. Family History (listed under Lifestyle on p.4) must have an explicit, auditable schema mapping (`UD08`).
- **All six mandatory metrics (`RF12`):** Accuracy, Precision, Recall, F1-Score, ROC-AUC, and Confusion Matrix MUST be reported on the sealed held-out test set at frozen validation-selected thresholds, complemented by adopted Q1 clinical extensions (PR-AUC, Specificity/NPV, Brier/ECE/calibration slope, DCA, bootstrap 95% CIs, paired DeLong/McNemar tests with multiplicity correction).
- **Explainability beyond plots (`RF03`, `RF08`, `RF11`):** SHAP explanations must use training-only background distributions and pass quantitative faithfulness (deletion/insertion AOPC vs random baseline), multi-seed stability, spurious-shortcut auditing, and cardiologist plausibility review (`STEP-038`–`040`, `G14`)—never claiming unproven biological causality or proven clinician trust.
- **Clinical safety boundary (`RF15–RF16`):** The final framework is a bounded research decision-support prototype and academic/Q1 contribution, never validated clinical diagnosis or clinical deployment.

<a id="stage-map"></a>
## Stage-to-step map and contents

| Stage | Steps / navigation | Governing handbook | Exit gate(s) |
|---|---|---|---|
| S01 Foundation and unresolved-decision charter | [001](#step-001) | §1, §12 | G01 |
| S02 Repository, PHI storage policy, templates and minimal tooling | [002](#step-002)–[003](#step-003) | §2, §11, §15, A–B | G02 |
| S03 Zero-seed systematic literature search, screening and extraction | [004](#step-004)–[007](#step-007) | §3 | Feeds G03 |
| S04 Proposal-gap verification (`PG1–PG5`) and Q1 RQ approval | [008](#step-008)–[009](#step-009) | §1, §3 | G03 |
| S05 Ethics/IRB, hospital acquisition, external cohort screening and intake | [010](#step-010)–[012](#step-012) | §4, §11 | IRB before intake; feeds G04 |
| S06 Four-modality quality, ECG signal integrity and cohort approval | [013](#step-013) | §4 | G04 |
| S07 Clinical endpoint ontology, 4-modality schema and QA protocol | [014](#step-014)–[015](#step-015) | §5 | G05 |
| S08 Pilot abstraction, clinical adjudication and cohort-label QA | [016](#step-016)–[018](#step-018) | §5 | G06 |
| S09 Leakage-safe splitting, modality preprocessing and prepared release | [019](#step-019)–[022](#step-022) | §4 | G07 (020), G08 (022) |
| S10 Framework/architecture selection, runtime lock and pipeline readiness | [023](#step-023)–[027](#step-027) | §6, §7, §8, §11 | G09 |
| S11 Controlled Q1 experiments, unimodal/fusion baselines and ablations | [028](#step-028)–[031](#step-031) | §6 | G10 per qualifying EXP |
| S12 Validation-only selection, calibration fit and final-test freeze | [032](#step-032)–[033](#step-033) | §7 | G11 (032) before test |
| S13 Final discrimination, calibration, statistical inference and DCA | [034](#step-034)–[036](#step-036) | §7 | G12 |
| S14 Subgroup fairness, missing-modality robustness, errors and PROBAST-AI | [037](#step-037) | §7 | G13 |
| S15 Multimodal XAI (SHAP), quantitative faithfulness, stability and clinical review | [038](#step-038)–[040](#step-040) | §8 | G14 |
| S16 Research prototype, optional defense demo and reproducibility audit | [041](#step-041)–[042](#step-042) | §9, §11 | G15 |
| S17 FYDP thesis, Q1 journal manuscript (TRIPOD+AI), archive and completion | [043](#step-043)–[050](#step-050) | §10, §11, §14 | G16 (thesis 046; paper 048), G17 (050) |

## Master dependency chain

```text
001/G01 → 002–003/G02 → 004–009/G03
→ 010–011(IRB) → 012–013/G04 → 014–015/G05 → 016–018/G06
→ 019(design) → 020/G07(split & seal) → 021(train-only fit) → 022/G08(REL)
→ 023–027/G09 → [028 → 029 → 030/G10] → 031(full Tier 1–4 + LOMO/progressive/multi-seed loop)
→ 032/G11(val-only selection, calibrator, threshold freeze) → 033(frozen test inference)
→ [034 metrics+calibration + 035 DeLong/bootstrap/DCA] → 036/G12
→ 037/G13(subgroups, missing-modality, error & PROBAST-AI)
→ 038(SHAP) → 039(faithfulness+stability) → 040/G14(shortcut+cardiologist review)
→ 041(prototype [+ optional UD22 demo]) → 042/G15(clean reproducibility audit)
→ 043–046/G16(thesis) → 047(thesis submission)
→ 048(Q1 manuscript + TRIPOD+AI + G16(paper) + submission/rebuttal OR approved disposition)
→ 049(tiered immutable archive & restore) → 050/G17(project completion)
```

## Universal session and artifact expectations

Every step inherits the [Universal DoD](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a). Record exact inputs, SHA-256 hashes, executed actions, outputs, verification checks, open blockers, and the next unblocked step in `01_Project_Management/diary/`. Git (Tier 1) holds PHI-free metadata, code, configs, safe registries, and aggregate metrics only; patient identities live exclusively in the encrypted Tier 2A linkage vault; de-identified clinical tables, ECG waveforms, and per-patient predictions/SHAP arrays stay strictly in restricted Tier 2B / Tier 3 storage with hash-verified backups.

For every planning/review prompt: read the cited OS sections and live registries, preserve the `PROPOSAL FACT` / `PLANNING RECOMMENDATION` / `Unresolved` boundary, surface blockers honestly, and never claim completed science without artifact evidence. For every implementation prompt: follow approved specs, keep raw clinical/ECG files immutable, fail loudly on missing settings or leakage, log exact versions/hashes, and produce verifiable test output.

---

<a id="step-001"></a>
## STEP-001 — Confirm FYDP proposal mandate, source facts, and unresolved decisions

**Objective:** Ratify the approved project scope, verify `RF01–RF18` against `fydp_title_proposal.pdf`, and assign named owners and blocking milestones to `UD01–UD26` without prematurely guessing unknown scientific details.

**Why this step exists:** The signed Proposal Approval Form endorses the title and direction, but leaves IRB/hospital permissions, clinical CVD endpoint criteria, ECG format, DL framework, split design, statistical plan, and Q1 target journal unresolved.

**Governing section references:** [OS §1](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §12](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-12); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** Both CVD multimodal planning documents and `fydp_title_proposal.pdf` present with verified SHA-256 (`BA7DD0EF21C8A2CA77B2E1BAFC2AC5A0E1FEC584E221C848085A971EAACEEFA8`); researchers and supervisor available for initial alignment.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours plus supervisor confirmation turnaround.

**Parallelizable:** No for scope ratification; individual `UD` briefing notes may be drafted in parallel.

**Inputs:** `fydp_title_proposal.pdf` (pp.1–6), `RF01–RF18`, `UD01–UD26`, any separate FYDP Title Phase Evaluation Report or departmental guidelines if they exist.

**Expected outputs:** Approved scope & exclusion charter (`scope.md`), role assignment between Rayan Ahmed and Mohammad Nafis Sadiq, initial `decisions.csv` with `DEC0001` (`UD01`), evaluation-report/feedback status record, and `G01` assessment.

**Repository/file changes:** Create `01_Project_Management/scope.md`, `decisions.csv`, `decision_log/DEC0001.md`, and `reviews/G01_assessment_<date>.md` (permitted prior to full skeleton in `STEP-002`).

**Execution procedure:**

1. Verify `fydp_title_proposal.pdf` hash and confirm verbatim title, member IDs, supervisor endorsement, and whether any Updated Title (§IV) or separate Title Phase Evaluation Report / examiner comments exist (`UD01`).
2. Assign operational role ownership between Rayan Ahmed and Mohammad Nafis Sadiq across literature, cohort/IRB coordination, ECG/tabular engineering, modeling, biostatistics/evaluation, XAI, and writing; identify target contacts for hospital custodian and qualified cardiologist.
3. Review all 26 `UD01–UD26` rows, assigning owners and blocking milestones while deliberately leaving unresolved scientific choices open until their evidence exists.
4. Obtain supervisor confirmation of scope boundaries (explicitly excluding medical imaging as primary input and distinguishing research decision-support from clinical deployment) and assess `G01`.

**Planning/review prompt:**

> Audit `CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md` §1 against `fydp_title_proposal.pdf` (pp.1–6). Produce a concise supervisor briefing confirming verbatim title, explicit scope exclusions, missing bibliography/workflow leakage constraints, and exact role/deadline assignments for `UD01–UD26` without pre-selecting datasets, endpoints, or models.

**Implementation prompt:**

> Documentation only: write `01_Project_Management/scope.md`, initial `decisions.csv`, `DEC0001.md`, and blank/evidenced `G01` audit form. Keep all unratified scientific parameters explicitly `Unresolved / Human Decision Required` and never pre-mark `G01` PASS without actual supervisor sign-off.

**Human-only actions and decisions:** Supervisor Md. Mizanur Rahman and researchers Rayan Ahmed & Mohammad Nafis Sadiq ratify scope, Q1 dual-deliverable intent, role assignments, and `UD01` feedback status.

**Version-control/artifact expectations:** Keep `fydp_title_proposal.pdf` untouched and immutable; preserve `STEP-001` files for initial Git commit in `STEP-002`. Zero patient data collection permitted here.

**Documentation updates:** Update `scope.md`, `decisions.csv`, and record actual adoption state in handbook cover/version log if ratified.

**Verification checklist:**

- [ ] Verbatim title and institutional details match `fydp_title_proposal.pdf` p.1.
- [ ] All 26 `UD01–UD26` items have named owners and blocking gates.
- [ ] Existence or absence of Title Phase Evaluation Report / examiner feedback explicitly documented (`UD01`).
- [ ] `G01` PASS backed by dated supervisor confirmation; zero research execution claimed.

**Common mistakes:** Treating the signed Proposal Approval Form as IRB or hospital data-collection approval; inventing an endpoint definition or dataset size during kickoff.

**Recovery procedure:** Log a superseding `DEC####` correcting any scope/title amendment, retain prior records, and re-audit `G01` before starting `STEP-002`.

**Definition of Done:** Approved scope charter, role assignments, and `UD01` decision evidenced; `G01` PASS. Universal DoD applies; this is a required future state.

**Next step:** [STEP-002](#step-002)

---

<a id="step-002"></a>
## STEP-002 — Create repository skeleton, PHI-safe storage policy, and minimal data-tool runtime

**Objective:** Instantiate all canonical domain folders, enforce four-tier PHI security before any hospital intake, and establish a tested minimal data/ECG inspection environment (`environment/data/`).

**Why this step exists:** Clinical tables and ECG waveforms contain sensitive health data; safe storage, `.gitignore` safeguards, and reproducible data-tooling locks must exist before touching a single patient file.

**Governing section references:** [OS §2](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-02); [OS §11](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-001` complete; `G01` PASS; `UD13` storage, PHI vault, and Git remote access decisions approved.

**Estimated difficulty and time (provisional):** Moderate; 4–6 hours including minimal runtime verification.

**Parallelizable:** Folder `README.md` drafting may be split between team members; Git initialization, `.gitignore`, and environment locking are serialized.

**Inputs:** OS §2 folder contracts, OS §11 four-tier storage rules, `STEP-001` outputs, and approved `UD13` storage/access decision.

**Expected outputs:** Full canonical directory tree, root governance files (`README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`), PHI-strict `.gitignore`/`.gitattributes`, storage/vault policy (`13_Documentation/pipeline.md`), and pinned tested `environment/data/` lock + `verification.md`.

**Repository/file changes:** Create `src/cvd_mm/`, `tests/`, `environment/data/`, and domain folders `01_Project_Management/` through `16_Archive/` (defer `prototype_ui/` unless/until `UD22` approves it); add `LICENSE` only after `UD25`.

**Execution procedure:**

1. Verify current workspace hashes (`fydp_title_proposal.pdf` and both planning docs) and initialize Git under the approved private/access-controlled workflow (`UD13`).
2. Create canonical directories and populate each folder's `README.md` (`T01`) defining purpose, owner, PHI sensitivity, and forbidden contents.
3. Configure `.gitignore` to strictly block `raw/`, `processed/`, `fitted_states/`, `adjudications/`, `*.edf`, `*.xml`, `*.dcm`, `*.mat`, `*.dat`, `*.hea`, `*.pt`, `*.pth`, `*.h5`, `*.ckpt`, `*.onnx`, `*.pkl`, credential files, and patient-level outputs; verify with synthetic dummy-path checks.
4. Establish separate encrypted Tier 2A (PHI linkage vault) and Tier 2B (restricted de-identified clinical/ECG storage) locations outside Git.
5. Build minimal `environment/data/` (Python, Pandas, NumPy, SciPy/WFDB-reader for ECG inspection, pytest, YAML/CSV schema validators), smoke-test on synthetic tabular + synthetic sine-wave ECG fixtures, and log exact versions in `environment/data/verification.md` and `13_Documentation/installation.md` (deferring PyTorch/TensorFlow selection to `STEP-023`–`024`).

**Planning/review prompt:**

> Translate OS §2 and §11 into an exact repository setup, PHI exclusion, and Tier 2A/2B storage verification checklist tailored to clinical tables and ECG signals. Confirm no deep-learning framework is prematurely locked here.

**Implementation prompt:**

> Materialize the approved repository skeleton, strict PHI `.gitignore`, folder READMEs, and minimal pinned `environment/data/` lock. Run automated ignore-rule tests and synthetic tabular/ECG smoke checks; record exact tool versions and output in `environment/data/verification.md`.

**Human-only actions and decisions:** Researchers and supervisor approve Git remote privacy, encrypted Tier 2A/2B storage custody, and backup destination (`UD13`).

**Version-control/artifact expectations:** Commit `STEP-001` records, skeleton, `.gitignore`, and `environment/data/` lock as `docs: initialize CVD multimodal repository and minimal data runtime`; never push to a public repository without explicit `UD13` clearance.

**Documentation updates:** Root `README.md`, `CHANGELOG.md`, `13_Documentation/installation.md`, `13_Documentation/pipeline.md` (storage/PHI policy).

**Verification checklist:**

- [ ] Directory layout matches OS §2.1 verbatim.
- [ ] Synthetic dummy PHI/ECG/checkpoint paths confirmed ignored by `git status`.
- [ ] Separate encrypted Tier 2A linkage vault path documented outside Git.
- [ ] `environment/data/` dependency lock installed and smoke-tested on synthetic fixtures.

**Common mistakes:** Pushing to a public GitHub repo by default; installing PyTorch/TensorFlow prematurely before `STEP-023`; assuming `.gitignore` retroactively scrubs already-committed files.

**Recovery procedure:** Immediately remove any accidentally staged sensitive/binary pattern, repair `.gitignore`, re-test dummy ignores, and re-verify environment lock before `STEP-003`.

**Definition of Done:** Safe canonical repository skeleton, PHI storage isolation, and tested `environment/data/` lock verified. Universal DoD applies.

**Next step:** [STEP-003](#step-003)

---

<a id="step-003"></a>
## STEP-003 — Install templates, canonical CSV registries, and automated integrity checks

**Objective:** Materialize all 32 blank templates (`T01–T32`) and all 22 Appendix B CSV registries, add lightweight schema/link validation, and pass `G02`.

**Why this step exists:** Q1 traceability collapses if literature extraction, cohort counts, ablations, evaluations, and SHAP audits drift into ad-hoc spreadsheets.

**Governing section references:** [OS §2](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-02); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS §15](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-15); [OS Appendix B](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-002` complete; PHI storage policy and `environment/data/` verification logged.

**Estimated difficulty and time (provisional):** Moderate; 3–5 hours.

**Parallelizable:** Template authoring (`T01–T32`) may be split across the two researchers; CSV header auditing and `G02` sign-off are serialized.

**Inputs:** OS §15 (`T01–T32`), OS Appendix B (22 registry schemas + 6 common columns), `STEP-001` actual decisions.

**Expected outputs:** Blank versioned `T01–T32` templates, header-verified CSV registries, lightweight registry/PHI validator in `14_Automation/`, `dashboard.md`, `timeline.md`, and `G02` assessment.

**Repository/file changes:** Populate `15_Templates_Prompts/`, initialize all 22 Appendix B CSV files across domain folders, create `01_Project_Management/dashboard.md`, `timeline.md`, `risk_register.csv` (initial risk themes from OS §13), `gates.csv`, `14_Automation/validate_repo.py`, and `reviews/G02_assessment_<date>.md`.

**Execution procedure:**

1. Materialize all 32 blank templates (`T01–T32`) in `15_Templates_Prompts/` with common headers and copy-ready skeletons (DEC, Gate Audit, `T32` multimodal YAML).
2. Create all 22 canonical CSV registries strictly matching Appendix B columns plus `Owner,Version,Status,Created,Updated,EvidencePath`; insert zero dummy scientific rows.
3. Initialize `gates.csv` with `G01` evidenced outcome and `G02–G17` explicitly `NOT ASSESSED`; populate initial domain risk themes in `risk_register.csv` without fabricated probabilities until reviewed.
4. Build and run `14_Automation/validate_repo.py` (verifying CSV headers, foreign-key rules, template presence, zero forbidden file extensions in Git-tracked paths) and assess `G02`.

**Planning/review prompt:**

> Audit every proposed template (`T01–T32`) and CSV registry header against OS §15 and Appendix B. Flag missing columns, competing ledgers, or any flag that falsely implies completed research.

**Implementation prompt:**

> Write the blank templates, canonical CSV headers, initial dashboard, and `14_Automation/validate_repo.py` tested via pytest on synthetic registry fixtures. Insert zero fake papers, patients, or experiments.

**Human-only actions and decisions:** Research lead reviews validator output and signs off `G02`.

**Version-control/artifact expectations:** Commit as `docs: install CVD multimodal templates, canonical registries and repo validator`.

**Documentation updates:** Template index (`15_Templates_Prompts/README.md`), registry index, `dashboard.md`, `G02` assessment.

**Verification checklist:**

- [ ] All 22 CSV registry headers match Appendix B exactly.
- [ ] All 32 templates (`T01–T32`) exist, are blank, and include required headers.
- [ ] `validate_repo.py` passes with zero dummy rows and zero pre-checked gates.
- [ ] `G02` PASS documented with hash/evidence paths.

**Common mistakes:** Creating duplicate experiment spreadsheets outside `experiment_registry.csv`; inserting example rows into production registries; marking `G02` PASS without testing `environment/data/`.

**Recovery procedure:** Consolidate duplicate ledgers into canonical Appendix B paths, purge any test/dummy rows, re-run `validate_repo.py`, and reassess `G02`.

**Definition of Done:** `G02` PASS; repository ready for systematic literature execution and ethical cohort planning. Universal DoD applies.

**Next step:** [STEP-004](#step-004)

---

<a id="step-004"></a>
## STEP-004 — Approve zero-seed systematic literature search and appraisal protocol

**Objective:** Design a PRISMA-aligned, falsification-oriented multi-database search and PROBAST-informed appraisal protocol from scratch (since `fydp_title_proposal.pdf` contains zero references).

**Why this step exists:** Q1 reviewers reject papers with selective, ad-hoc related work; searching specifically for strong 3–4 modality CVD frameworks and faithful XAI studies prevents blind-spot novelty claims.

**Governing section references:** [OS §1](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §3](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-003` complete; `G01–G02` PASS; candidate `O1–O4` and `PG1–PG5` recorded.

**Estimated difficulty and time (provisional):** Moderate; 3–4 hours.

**Parallelizable:** Database-specific syntax translation (PubMed MeSH, IEEE Xplore, Scopus, Web of Science, ACM DL) may be split after shared eligibility rules are approved.

**Inputs:** `RF05–RF07` (`PG1–PG5`), OS §3.1 seed Boolean queries A–C, institutional database subscriptions.

**Expected outputs:** Approved `02_Literature/searches/protocol.md`, exact per-database search strings, PRISMA screening inclusion/exclusion rules, relevance taxonomy, PROBAST-informed extraction checklist, and provisional `research_questions.md`.

**Repository/file changes:** Create `02_Literature/searches/protocol.md`, `02_Literature/research_questions.md` (marked provisional), and database search templates (`T04`).

**Execution procedure:**

1. Adapt seed Queries A (multimodal CVD ECG+tabular), B (Transformer multimodal fusion & missing modalities in cardiology), and C (SHAP/XAI faithfulness & calibration in CVD) to each accessible database's exact syntax.
2. Define explicit inclusion/exclusion rules, publication window (e.g., core modern DL/multimodal period plus seminal clinical risk-score benchmarks), language coverage, and deduplication hierarchy (DOI/PMID/title/preprint-to-journal).
3. Separate **Direct Comparators** (2+ modalities combining ECG and tabular clinical/lab/lifestyle for CVD risk prediction) from **Contextual Studies** (unimodal ECG/clinical models, cardiac imaging multimodal fusion, general clinical XAI faithfulness, clinical CVD risk scores).
4. Include PROBAST-aligned bias flags in the extraction form (leakage, endpoint horizon, calibration, external validation, XAI evaluation rigor) and obtain supervisor review of the protocol.

**Planning/review prompt:**

> Design a PRISMA-aligned zero-seed search protocol capable of rigorously testing and potentially refuting `PG1–PG5`. Ensure queries actively surface UK Biobank, MIMIC-IV-ECG, and recent Q1 multimodal Transformer CVD papers.

**Implementation prompt:**

> Documentation only: save approved database strings, eligibility rubric, and extraction schema in `02_Literature/searches/protocol.md`. Report zero invented retrieval counts or citations.

**Human-only actions and decisions:** Supervisor and researchers approve eligibility rules, database coverage, and access limitations.

**Version-control/artifact expectations:** Commit `lit: approve systematic literature search and screening protocol`.

**Documentation updates:** Search protocol, accessible vs inaccessible database log, provisional RQs.

**Verification checklist:**

- [ ] Verbatim database strings defined for Queries A, B, and C.
- [ ] Direct vs contextual study categories clearly separated.
- [ ] Screening exclusion reasons and deduplication rules locked prior to searching.
- [ ] PROBAST risk-of-bias & XAI faithfulness fields included in extraction rubric.

**Common mistakes:** Searching only for papers that use 1–2 modalities to confirm `PG1–PG2`; ignoring cardiology journals on PubMed; setting arbitrary paper quotas.

**Recovery procedure:** Amend overly narrow/noisy queries with logged rationale (`protocol_v1.1.0.md`) and re-execute affected database searches transparently.

**Definition of Done:** Approved reproducible search, screening, and extraction protocol ready for execution. Universal DoD applies.

**Next step:** [STEP-005](#step-005)

---

<a id="step-005"></a>
## STEP-005 — Execute multi-database searches and register deduplicated candidate papers

**Objective:** Run approved queries across accessible biomedical and engineering databases, log raw exports, deduplicate, and register candidate studies in `papers.csv`.

**Why this step exists:** Auditable PRISMA flow counts and verified DOI metadata are mandatory for Q1 literature reviews and eliminate hallucinated citations.

**Governing section references:** [OS §3](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS §11](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-004` protocol approved; database access available.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours per database batch, repeated to full protocol coverage.

**Parallelizable:** Searches across distinct databases can run in parallel; deduplication and `P####` ID assignment must be serialized.

**Inputs:** Approved database queries (`STEP-004`), lawful institutional/open-access retrieval routes.

**Expected outputs:** Per-database `T04` search logs, raw export snapshots/hashes, deduplicated `02_Literature/papers.csv`, initial `references.bib`, and lawful full-text pointers.

**Repository/file changes:** Populate `02_Literature/searches/SEARCH_<db>_<date>.md`, `papers.csv`, `references.bib`, and permitted `papers/P####.pdf` (or restricted institutional pointer for paywalled full texts).

**Execution procedure:**

1. Execute each database query verbatim, recording exact date, filters, retrieved record count, and raw export (RIS/BibTeX/CSV) SHA-256 hash.
2. Deduplicate across databases via DOI, PMID, and normalized title; explicitly link arXiv/medRxiv preprints to final peer-reviewed versions so no study is double-counted.
3. Assign sequential `P####` IDs in `papers.csv` with `MetadataVerified=no` until verified against original publisher records; perform backward/forward citation snowballing on seminal direct multimodal CVD studies and log snowball records transparently.
4. Retrieve lawful full texts where accessible; flag paywalled/inaccessible texts honestly without fabricating their content.

**Planning/review prompt:**

> Audit raw search exports and deduplication logs for completeness, preprint linkage, and retrieval bias. Do not summarize unread papers or invent missing DOIs/PMIDs.

**Implementation prompt:**

> Register deduplicated candidate records in `papers.csv` and search logs (`T04`). Store paywalled PDFs only under lawful institutional access rules outside public Git.

**Human-only actions and decisions:** Researchers use institutional access and decide on interlibrary/author requests for unavailable key full texts.

**Version-control/artifact expectations:** Commit search logs, `papers.csv`, and verified BibTeX metadata; exclude copyrighted bulk PDFs from public remotes.

**Documentation updates:** Search coverage summary, access limitations log, `papers.csv`.

**Verification checklist:**

- [ ] Every `P####` traces to a logged search or snowballing source.
- [ ] Preprints and published versions linked without double counting.
- [ ] Exact search dates and raw counts recorded per database.
- [ ] Zero invented DOIs, authors, or publication venues.

**Common mistakes:** Counting an arXiv preprint and its IEEE JBHI publication as two studies; pulling BibTeX blindly from Google Scholar with broken metadata.

**Recovery procedure:** Re-run any unlogged query, repair duplicate `P####` entries via `DuplicateOf` links, and verify metadata against CrossRef/PubMed before screening.

**Definition of Done:** Full planned search wave executed, deduplicated, and registered with auditable counts and access limits. Universal DoD applies.

**Next step:** [STEP-006](#step-006)

---

<a id="step-006"></a>
## STEP-006 — Screen candidate studies and document PRISMA eligibility flow

**Objective:** Apply two-stage title/abstract and full-text screening with explicit exclusion reasons to construct a defensible included literature corpus.

**Why this step exists:** Transparent screening prevents cherry-picking weak comparators and produces verifiable PRISMA counts for thesis and Q1 manuscript methods.

**Governing section references:** [OS §3](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-005` candidate batch registered; `STEP-004` eligibility criteria locked.

**Estimated difficulty and time (provisional):** Moderate; 3–5 hours per batch depending on retrieval volume.

**Parallelizable:** Both researchers should independently screen (dual screening recommended for Q1 rigor) and reconcile disagreements jointly.

**Inputs:** `papers.csv`, abstracts and lawful full texts, `STEP-004` screening protocol.

**Expected outputs:** Completed `02_Literature/screening.csv` with `SCR####` rows, reconciled PRISMA counts (`searches/screening_summary.md`), and tagged Direct vs Contextual included sets.

**Repository/file changes:** Update `02_Literature/screening.csv`, `papers.csv` (`ReadingStatus`), and create `02_Literature/searches/screening_summary.md`.

**Execution procedure:**

1. Perform Stage 1 (Title/Abstract) screening; retain any ambiguous study for full-text inspection.
2. Perform Stage 2 (Full-Text) screening against approved eligibility criteria, logging one primary exclusion code per excluded article (e.g., wrong modality/imaging-only, non-CVD outcome, review/editorial, inaccessible full text, duplicate cohort report).
3. Tag every included study as `Direct_Multimodal_CVD`, `Contextual_Unimodal_ECG_Tabular`, `Contextual_Clinical_Risk_Score`, or `Contextual_Medical_XAI_Methodology`.
4. Reconcile inter-screener disagreements, verify PRISMA count arithmetic (`Retrieved - Duplicates = Screened; Screened - TA_Excluded = FullText_Assessed; FullText_Assessed - FT_Excluded = Included`), and confirm contradicting strong studies are retained.

**Planning/review prompt:**

> Audit `screening.csv` for adherence to `protocol.md`. Flag any exclusion that unfairly removes strong 3–4 modality CVD papers or conflates cardiac imaging studies with ECG+tabular studies.

**Implementation prompt:**

> Save actual screening decisions and run a reconciliation script verifying PRISMA counts from `screening.csv`. Do not infer eligibility from abstracts alone for Stage 2.

**Human-only actions and decisions:** Both researchers reconcile screening disagreements; supervisor arbitrates borderline scope calls.

**Version-control/artifact expectations:** Commit `screening.csv` and `screening_summary.md`.

**Documentation updates:** PRISMA flow numbers, exclusion breakdown, updated `papers.csv`.

**Verification checklist:**

- [ ] Every candidate record has documented stage, decision, and reason.
- [ ] PRISMA counts reconcile with zero arithmetic errors.
- [ ] Strong competing 3–4 modality CVD papers retained honestly.
- [ ] Reviewer disagreements and resolutions logged.

**Common mistakes:** Excluding recent high-performing multimodal Transformer CVD papers because they weaken `PG2` or `PG5`; mixing chest X-ray/MRI studies into direct ECG+tabular tables.

**Recovery procedure:** Reopen misclassified `SCR####` rows, document corrected eligibility rationale, and regenerate PRISMA counts transparently.

**Definition of Done:** Current search corpus fully screened with reconciled PRISMA flow and dual-checked inclusion sets. Universal DoD applies.

**Next step:** [STEP-007](#step-007)

---

<a id="step-007"></a>
## STEP-007 — Read, extract, and verify included studies with PROBAST bias flags

**Objective:** Build original-source-verified structured extraction records (`P####.md`) capturing cohorts, modalities, ECG formats, leakage/PROBAST risks, fusion architectures, metrics, calibration, and XAI evaluation rigor.

**Why this step exists:** Comparing published ROC-AUCs across papers without extracting patient-split integrity, endpoint horizon, class prevalence, ECG representation, and calibration hides fatal comparability flaws.

**Governing section references:** [OS §3](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS §10](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-006` included corpus; lawful full texts and supplements available.

**Estimated difficulty and time (provisional):** Hard; 1.5–3 hours per full paper; repeat across included corpus.

**Parallelizable:** Yes across papers split between both researchers; cross-check numerical claims of key direct comparators.

**Inputs:** Included full texts & supplementary PDFs, `T05` (`paper_summary.md`), `papers.csv`.

**Expected outputs:** Structured `02_Literature/summaries/P####.md` summaries, verified `references.bib`, populated comparative columns in `papers.csv`, and locator-backed candidate `claims.csv` entries.

**Repository/file changes:** Create `02_Literature/summaries/P####.md`; update `papers.csv` (`MetadataVerified=yes`), `references.bib`, and `claims.csv`.

**Execution procedure:**

1. Read Methods, Results, Tables, Figures, and Supplements—never abstracts alone. Verify title, authors, journal, year, volume/pages, and DOI against the publisher PDF.
2. Extract cohort country/ethnicity (flagging South Asian / Bangladeshi representation), $N$ patients/events, CVD endpoint & time horizon, exact modalities (Clinical, ECG lead/waveform vs intervals, Lab, Lifestyle), and missing-modality handling.
3. Extract validation design and **PROBAST risk-of-bias flags**: patient-level vs record-level split, external/temporal validation, signs of pre-split SMOTE/scaling leakage, and incorporation bias.
4. Extract fusion architecture, baselines, discrimination + calibration + DCA metrics, and **XAI rigor** (did they merely print a SHAP plot, or did they evaluate faithfulness/stability/clinical review?), citing exact page/table locators and writing `not reported` for missing items.

**Planning/review prompt:**

> Extract `P####` strictly using `T05`. Attach page/table locators to every numerical result, classify PROBAST leakage/bias risks, and assess whether its XAI component was quantitatively evaluated or merely descriptive.

**Implementation prompt:**

> Save verified `P####.md`, update `papers.csv` and `references.bib` from publisher metadata only. Leave unreported items explicitly `not reported`—never infer unstated hyperparameters or split methods.

**Human-only actions and decisions:** Researchers cross-verify high-impact comparator extractions and PROBAST risk judgments.

**Version-control/artifact expectations:** Commit verified summaries, `papers.csv`, and `references.bib` cleanly.

**Documentation updates:** Extraction completeness tracker, comparative evidence matrix, `claims.csv`.

**Verification checklist:**

- [ ] 100% of extracted numerical metrics have exact page/table/figure locators.
- [ ] Cohort, endpoint horizon, modalities, ECG format, split level, and XAI evaluation rigor recorded or marked `not reported`.
- [ ] Publisher bibliographic metadata verified (`MetadataVerified=yes`) for every study cited in claims.
- [ ] Reviewer critique cleanly separated from author-stated limitations.

**Common mistakes:** Extracting from abstracts; equating high AUC on a leaked record-level split with genuine SOTA; assuming a study evaluated XAI faithfulness just because "SHAP" appears in the title.

**Recovery procedure:** Downgrade any unverified claim, inspect the original PDF/supplement, append corrected extraction with history, and recheck synthesis tables.

**Definition of Done:** Included direct and key contextual corpus extracted with full locators and publisher-verified citations. Universal DoD applies.

**Next step:** [STEP-008](#step-008)

---

<a id="step-008"></a>
## STEP-008 — Synthesize evidence and test proposal research gaps (`PG1–PG5`)

**Objective:** Evaluate each of the five proposal gap bullets (`PG1–PG5`, p.3) against verified supporting and contradicting studies to sharpen a reviewer-proof Q1 positioning.

**Why this step exists:** Broad FYDP gap statements (e.g., "few studies use >2 modalities" or "models don't use SHAP") often fail under Q1 peer review unless refined into precise, evidence-backed scientific gaps.

**Governing section references:** [OS §1](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §3](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-007` extractions complete across all themes needed to test `PG1–PG5`.

**Estimated difficulty and time (provisional):** Hard; 4–6 hours per synthesis iteration.

**Parallelizable:** Thematic matrices (multimodal fusion, ECG encoders, lifestyle incremental value, calibration/PROBAST biases, XAI faithfulness) can be drafted in parallel and merged jointly.

**Inputs:** `02_Literature/summaries/P####.md`, `papers.csv`, `RF07` (`PG1–PG5`), `T06` (`gap.md`).

**Expected outputs:** Evidence-backed `GAP####` records (`gaps.csv` + `gap_notes/GAP####.md`), comprehensive `02_Literature/synthesis.md`, and sharpened Q1 contribution options.

**Repository/file changes:** Populate `02_Literature/gaps.csv`, `02_Literature/gap_notes/GAP####.md`, `02_Literature/synthesis.md`, and update `claims.csv`.

**Execution procedure:**

1. Build structured synthesis tables comparing direct multimodal CVD studies by modality combination, population (highlighting under-representation of South Asian/Bangladesh 4-modality cohorts), split/leakage rigor, calibration/DCA reporting, missing-modality handling, and quantitative XAI validation.
2. Test each `PG1–PG5` explicitly against both supporting AND contradicting `P####` IDs, classifying status as `supported-within-search`, `narrowed`, `refuted`, or `unresolved`.
3. Where broad claims (e.g., `PG2` or `PG3`) are partially refuted by recent UK Biobank / MIMIC-IV / SHAP studies, articulate the **sharpened Q1 gap** (e.g., absence of leakage-free, missing-modality-tolerant 4-modality Transformer fusion with calibrated DCA and quantitatively verified SHAP faithfulness/shortcut auditing on an adjudicated South Asian primary clinical cohort).
4. Map refined gaps directly to candidate `O1–O4` and `RQ1–RQ4` without fabricating novelty.

**Planning/review prompt:**

> Challenge `PG1–PG5` rigorously using extracted `P####` evidence. Identify where broad proposal claims fail against recent Q1 literature and formulate sharp, defensible, falsifiable Q1 research gaps backed by concrete counterevidence.

**Implementation prompt:**

> Documentation only: write `gaps.csv`, `GAP####.md`, and `synthesis.md` referencing exact `P####` IDs and locators. Retain any refuted or narrowed proposal hypothesis transparently in the record.

**Human-only actions and decisions:** Supervisor evaluates sharpened Q1 contribution positioning and approves framing within the endorsed FYDP title.

**Version-control/artifact expectations:** Commit `lit: complete evidence synthesis and PG1-PG5 gap verification`.

**Documentation updates:** `gaps.csv`, `synthesis.md`, `claims.csv`, `research_questions.md` draft.

**Verification checklist:**

- [ ] Every `PG1–PG5` mapped to supporting AND contradicting `P####` IDs plus search coverage limits.
- [ ] Zero unsupported "first ever" or "no prior SHAP/multimodal study exists" wording.
- [ ] Methodological gaps in prior literature (leakage, missing calibration/DCA, unverified SHAP, lack of LOMO/lifestyle ablations) documented with locators.
- [ ] Sharpened Q1 contribution aligns cleanly with the approved title.

**Common mistakes:** Hiding contradicting 4-modality studies; confusing citation count with proof of a gap; attacking straw-man baselines from outdated papers.

**Recovery procedure:** Run targeted supplementary queries if a critical sub-domain (e.g., South Asian CVD risk or ECG-SHAP faithfulness) had thin coverage, extract new studies via `STEP-005`–`007`, and revise synthesis before `G03`.

**Definition of Done:** Evidence-grounded synthesis and sharpened Q1 gap analysis ready for RQ approval. Universal DoD applies.

**Next step:** [STEP-009](#step-009)

---

<a id="step-009"></a>
## STEP-009 — Lock Q1-aligned research questions and pass literature gate (`G03`)

**Objective:** Finalize permanent `RQ` identifiers mapped to `O1–O4`, `GAP####`, cohort/modality needs, baselines, and evaluation/XAI metrics, and pass `G03`.

**Why this step exists:** Hospital data design, CRF variables, Transformer fusion design, and statistical tests must directly answer explicit, supervisor-approved research questions.

**Governing section references:** [OS §1](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §3](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-008` synthesis & `GAP####` records complete; `STEP-004`–`007` PRISMA and verification logs intact; `G01–G02` current.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours plus supervisor review.

**Parallelizable:** No for scientific gate sign-off; ongoing living-review alerts may continue afterward.

**Inputs:** `O1–O4`, `GAP####`, `synthesis.md`, `papers.csv`, `screening_summary.md`, `claims.csv`.

**Expected outputs:** Locked `02_Literature/research_questions.md` (with full RQ-to-experiment-to-metric traceability table), literature search cutoff date, `DEC####` approving RQs, and `G03` assessment.

**Repository/file changes:** Finalize `02_Literature/research_questions.md`; update `decisions.csv`, `claims.csv`, `gates.csv`, and write `01_Project_Management/reviews/G03_assessment_<date>.md`.

**Execution procedure:**

1. Finalize primary and subordinate RQs (`RQ1–RQ4`) linking every question to `O1–O4`, verified `GAP####`, required 4-modality data fields, comparator tier, statistical test, XAI metric, and permitted claim boundary.
2. Verify that every citation supporting the RQs and gap narrative has `MetadataVerified=yes` and original-full-text provenance.
3. Confirm with supervisor that negative/null answers to any RQ (e.g., if lifestyle adds small marginal AUC or if GBDT rivals Transformer) remain publishable, rigorously analyzed outcomes.
4. Audit all `G03` mandatory criteria (logged searches, PRISMA counts, full-text verification, counterevidence, bounded novelty) and record `G03` outcome.

**Planning/review prompt:**

> Audit the full `02_Literature/` package against `G03` criteria. Verify that every RQ is falsifiable, maps cleanly to mandatory proposal metrics + Q1 extensions, and relies on zero unverified claims.

**Implementation prompt:**

> Documentation only: finalize `research_questions.md`, record the search cutoff date, link `CLAIM` IDs, and save the evidenced `G03` review. Keep downstream cohort/model choices linked to `UD02–UD26`.

**Human-only actions and decisions:** Supervisor Md. Mizanur Rahman approves final RQs, sharpened Q1 contribution boundaries, and signs `G03`.

**Version-control/artifact expectations:** Commit milestone `lit: lock approved Q1 research questions and pass G03`.

**Documentation updates:** `research_questions.md`, `dashboard.md`, `gates.csv`, literature cutoff log.

**Verification checklist:**

- [ ] Every RQ traces to `O1–O4`, verified `GAP####`, and measurable evaluation/XAI criteria.
- [ ] All citations backing RQs are publisher-verified full-text extractions.
- [ ] Contradictory literature and search limitations documented transparently.
- [ ] `G03` PASS signed and dated by supervisor.

**Common mistakes:** Requiring every `PG1–PG5` bullet to be confirmed; writing RQs that presume Transformer superiority; deferring citation verification until thesis week.

**Recovery procedure:** Return unsupported claims to `STEP-007`–`008`, revise RQs within approved scope, and re-audit `G03`.

**Definition of Done:** `G03` PASS; verified literature and approved Q1 RQs govern cohort design and modeling. Universal DoD applies.

**Next step:** [STEP-010](#step-010)

---

<a id="step-010"></a>
## STEP-010 — Assess sample-size feasibility, clinical sites, and optional external cohorts

**Objective:** Evaluate hospital/diagnostic-center collection feasibility, compute prospective sample-size/EPV power requirements (`UD04`), and screen optional external public CVD cohorts for Q1 generalizability (`UD06`).

**Why this step exists:** Multimodal Transformers overfit easily on tiny convenience samples, and spectrum bias across poorly matched recruitment sites destroys Q1 credibility before training begins.

**Governing section references:** [OS §4](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §13](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-009` complete; `G03` PASS; approved RQs and modality requirements known.

**Estimated difficulty and time (provisional):** Moderate to hard; 4–6 hours plus site liaison discussions.

**Parallelizable:** Primary Bangladesh hospital/diagnostic-center outreach and secondary public-cohort screening (e.g., credentialed PhysioNet/MIMIC-IV-ECG/PTB-XL/Framingham compatibility checks) may run concurrently.

**Inputs:** Approved RQs, literature cohort benchmarks (`STEP-007`), `RF09–RF10`, `UD04`, `UD06`, `UD26`.

**Expected outputs:** Prospective sample-size/EPV feasibility memo, candidate clinical site and external cohort register (`03_Datasets_Cohort/sites.csv`), spectrum-bias mitigation plan, and small-$N$ contingency criteria (`UD26`).

**Repository/file changes:** Populate `03_Datasets_Cohort/sites.csv`, `03_Datasets_Cohort/reports/feasibility_epv_study.md`, and draft `DEC####` options for `UD04`/`UD06`/`UD26`.

**Execution procedure:**

1. Compute prospective minimum sample size $N$ and CVD event count $E$ needed for stable risk-prediction development and calibration (e.g., Riley et al. criteria + EPV guidelines across anticipated predictor degrees of freedom), explicitly defining small-$N$ contingency thresholds (`UD26`).
2. Identify candidate hospitals and diagnostic centers in Bangladesh capable of supplying linked Clinical, ECG (verify digital vs paper availability early!), Laboratory, and Lifestyle records under consecutive or clinically matched recruitment to avoid extreme case-control spectrum bias.
3. Screen optional public/credentialed cohorts (`UD06`) strictly for modality overlap, clinical endpoint compatibility, licensing, and lawful external-validation or ECG-pretraining potential—never merging mirrors or assuming public downloads bypass data-use agreements.
4. Shortlist viable primary site(s) and optional external benchmark(s) for formal ethics and permission review in `STEP-011`.

**Planning/review prompt:**

> Perform a Q1-grade clinical feasibility and EPV analysis for four-modality CVD prediction. Flag spectrum-bias risks (e.g., inpatient CCU cases vs healthy student controls), ECG digitization pitfalls, and realistic external-validation candidates without inventing patient counts.

**Implementation prompt:**

> Save `sites.csv` and `feasibility_epv_study.md` grounded in documented site capabilities and published cohort metadata only. Execute zero patient data collection or restricted dataset downloads before `STEP-011`.

**Human-only actions and decisions:** Researchers and supervisor shortlist participating hospital(s)/diagnostic center(s), approve recruitment design (`UD04`), decide external-cohort adoption (`UD06`), and approve small-$N$ contingency thresholds (`UD26`).

**Version-control/artifact expectations:** Commit safe site metadata and EPV calculations; preserve rejected site/dataset rationales; zero patient records handled here.

**Documentation updates:** `sites.csv`, `feasibility_epv_study.md`, `risk_register.csv` (enrollment/IRB schedule risks), `decisions.csv`.

**Verification checklist:**

- [ ] Prospective sample-size/EPV calculation documented with explicit assumptions.
- [ ] Primary hospital/diagnostic recruitment strategy addresses spectrum bias.
- [ ] ECG acquisition format feasibility checked per candidate site.
- [ ] Optional external benchmark decision (`UD06`) and small-$N$ fallback (`UD26`) clearly framed; zero unapproved data acquired.

**Common mistakes:** Recruiting CVD cases from an ICU and controls from healthy university volunteers; choosing a hospital that only keeps unlinked paper ECGs without planning digitization validation; assuming public medical datasets need no credentialing or license check.

**Recovery procedure:** Expand multi-center site outreach, adopt a validated secondary public multimodal cohort under `UD06`, or activate compact-encoder / nested-CV contingency (`UD26`) with supervisor sign-off before IRB filing.

**Definition of Done:** Evidence-backed site shortlist, EPV feasibility analysis, and recruitment strategy ready for IRB/ethics submission. Universal DoD applies.

**Next step:** [STEP-011](#step-011)

---

<a id="step-011"></a>
## STEP-011 — Obtain IRB/ethics approval, hospital permissions, and data-use agreements

**Objective:** Secure lawful, documented ethical approval, hospital administrative authorization, informed consent (or IRB waiver), and credentialed access for any adopted external cohort before collecting or touching any patient data.

**Why this step exists:** `RF09` explicitly requires ethical approval prior to hospital collection; Q1 medical journals enforce immediate desk rejection without verifiable IRB protocol numbers, ethics committee names, and consent statements.

**Governing section references:** [OS §1](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §4](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §11](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS §12](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-12); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-010` shortlisted site(s) and recruitment plan; preliminary variable/modality scope (`RF10`); institutional IRB application forms available.

**Estimated difficulty and time (provisional):** Hard; 4–8 hours protocol drafting plus external IRB & hospital administration turnaround (unknown; start as early as feasible!).

**Parallelizable:** Institutional IRB preparation, hospital administrative MOU outreach, and credentialed external-cohort applications (e.g., CITI training / PhysioNet DUA if `UD06` adopted) can proceed in parallel; zero clinical intake may start until written approval lands.

**Inputs:** `STEP-010` feasibility/recruitment plan, PHI de-identification & Tier 2A/2B storage policy (`STEP-002`), draft informed consent / retrospective waiver justification, institutional/hospital ethics forms.

**Expected outputs:** Written IRB/ethics approval letter & protocol ID, hospital/diagnostic-center administrative permission, approved consent form or IRB waiver, signed DUAs for any external dataset, `SITE####` authorization records (`T08`), and resolved `UD05` `DEC####`.

**Repository/file changes:** Store signed/private IRB & hospital letters in restricted Tier 2A/2B storage; commit safe redacted metadata summaries (`03_Datasets_Cohort/irb_permissions/SITE####.md`), updated `sites.csv`, and `decisions.csv`.

**Execution procedure:**

1. Prepare the IRB/ethics protocol specifying study objectives, inclusion/exclusion criteria, 4-modality data elements, informed consent process (or retrospective de-identification waiver justification), Tier 2A/2B PHI safeguards, permitted compute environments, and retention/destruction schedule.
2. Obtain formal written approval from the appropriate institutional/hospital Ethics Committee / IRB and written data-access permission from each participating hospital or diagnostic center.
3. Explicitly verify rights for: (a) model training & validation, (b) publication of aggregate results and de-identified representative ECG/SHAP figures, (c) sharing trained weights or controlled-access data instructions per Q1 journal requirements, and (d) permitted compute destinations (blocking unapproved public cloud uploads of hospital PHI).
4. Complete any required CITI ethics training and DUA execution for optional external cohorts (`UD06`); keep pending or denied sites strictly blocked.

**Planning/review prompt:**

> Audit our IRB/ethics and hospital-permission package against Q1 biomedical journal ethics requirements (Declaration of Helsinki, IRB identifier, consent/waiver, PHI ECG-header scrubbing, compute-location restrictions). Flag any missing right without inventing legal or ethical approval.

**Implementation prompt:**

> Documentation only: record actual received IRB protocol IDs, approval dates, site restrictions, and retention terms in `03_Datasets_Cohort/irb_permissions/SITE####.md` and `decisions.csv` (`UD05`). Never draft fabricated approval signatures or assume verbal consent suffices.

**Human-only actions and decisions:** Institutional IRB / Ethics Committee grants written ethical approval; hospital authority signs collection permission; supervisor endorses ethics filing (`UD05`).

**Version-control/artifact expectations:** Signed original letters, consent sheets, and DUAs stay in restricted encrypted Tier 2A/2B storage; Git contains safe pointer summaries and IRB protocol metadata only—never signatures containing personal contact data or credentials.

**Documentation updates:** `sites.csv`, `irb_permissions/SITE####.md`, `decisions.csv` (`UD05`), `risk_register.csv`.

**Verification checklist:**

- [ ] Written IRB/ethics approval ID, committee name, and date obtained for every active primary site.
- [ ] Informed consent form (or written IRB waiver) explicitly documented.
- [ ] Permitted compute environments, publication-figure de-identification rights, and retention rules verified.
- [ ] Pending/unapproved sites remain strictly blocked from intake.

**Common mistakes:** Starting retrospective hospital chart/ECG collection based on informal verbal permission; forgetting to verify whether anonymized single-patient ECG/SHAP plots may be printed in a Q1 journal; uploading restricted clinical spreadsheets to unapproved cloud notebooks.

**Recovery procedure:** Halt any premature activity immediately, obtain formal written amendment or ethics clearance, or pivot to an authorized clinical site / lawful approved cohort via `STEP-010`, preserving denied records transparently.

**Definition of Done:** Written ethical, institutional, and custodial authorizations exist for every source scheduled for intake (`UD05` resolved). Universal DoD applies.

**Next step:** [STEP-012](#step-012)

---

<a id="step-012"></a>
## STEP-012 — Execute controlled PHI-de-identified intake and lock raw four-modality cohort

**Objective:** Acquire authorized primary (and any approved external) clinical, ECG, laboratory, and lifestyle records, strip all PHI into the isolated Tier 2A vault, assign pseudonymous `PAT########`/`ENC########` keys, and lock immutable raw SHA-256 manifests.

**Why this step exists:** Every downstream clinical label, split, model, and SHAP attribution must trace deterministically to immutable, de-identified raw source bytes with intact patient-level linkage.

**Governing section references:** [OS §4](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §11](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-011` written IRB & site approvals complete (`UD05`); Tier 2A linkage vault & Tier 2B encrypted storage operational (`G02` current); `environment/data/` tested.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours setup plus hospital collection/extraction duration (batch-repeatable across collection waves).

**Parallelizable:** Authorized collection/extraction across distinct `SITE####` facilities can run in parallel; pseudonymous `PAT########` deduplication across sites and `DS####` manifest locking are serialized.

**Inputs:** Authorized hospital/diagnostic-center exports & CRFs, raw digital ECG exports (or scanned strips if unavoidable under `UD07`), approved external cohort files (if `UD06` adopted), `STEP-011` IRB/de-identification rules.

**Expected outputs:** Locked immutable restricted `03_Datasets_Cohort/raw/DS####/`, SHA-256 file manifests, isolated encrypted Tier 2A PHI linkage table, `datasets.csv` entry, and intake reconciliation report.

**Repository/file changes:** Populate restricted Tier 2B `03_Datasets_Cohort/raw/DS####/` and `manifests/DS####_intake.csv`; update Git-safe `03_Datasets_Cohort/datasets.csv` and `reports/DS####_intake_summary.md`.

**Execution procedure:**

1. Acquire authorized clinical, ECG, lab, and lifestyle records from each approved `SITE####` in versioned intake batches, logging source export date, format, and original archive SHA-256.
2. Execute deterministic PHI scrubbing before moving files into analytical Tier 2B storage: replace real patient identifiers with `PAT########` and visits with `ENC########`, store the reverse mapping strictly in the encrypted Tier 2A vault, shift/offset exact dates relative to `IndexDate` ($t_0$), and strip patient names/MRNs from **ECG XML/DICOM/WFDB headers or burned-in image margins**.
3. Inventory every tabular record and ECG file (including corrupted, partial-modality, or unreadable files—never silently drop records!), computing per-file SHA-256 digests and checking cross-site/repeat-visit patient duplicates via the restricted vault before discarding PHI.
4. Set raw Tier 2B files read-only, verify encrypted backup restoration hash, and publish safe aggregate intake counts into `datasets.csv`.

**Planning/review prompt:**

> Design a zero-leakage PHI de-identification and four-modality intake checklist covering tabular EHR/CRF records AND raw ECG headers/waveforms. Specify exact count reconciliation checks and cross-visit patient deduplication rules.

**Implementation prompt:**

> Run read-only checksum, PHI-header scrubbing, and intake inventory scripts using `environment/data/`. Preserve unreadable/partial files with explicit status codes, lock raw bytes read-only in Tier 2B, and verify zero PHI enters Tier 1 Git.

**Human-only actions and decisions:** Hospital data custodian and authorized researchers execute on-site PHI de-identification and secure Tier 2A vault custody.

**Version-control/artifact expectations:** ZERO patient rows, MRNs, raw ECG files, or identifying filenames in Git. Commit aggregate `datasets.csv`, safe intake summary, and non-PHI manifest hashes only; back up Tier 2A and Tier 2B separately in encrypted storage.

**Documentation updates:** `datasets.csv`, `DS####_intake_summary.md`, `risk_register.csv` (enrollment actuals vs EPV target).

**Verification checklist:**

- [ ] Every acquired raw tabular/ECG file has recorded SHA-256 and read-only lock in Tier 2B.
- [ ] PHI scrubbed across clinical, lab, lifestyle, AND ECG file headers/metadata; linkage isolated in encrypted Tier 2A vault.
- [ ] Repeat visits of the same individual linked under one `PAT########`.
- [ ] Screened vs acquired vs unreadable counts reconcile completely; encrypted backup verified.

**Common mistakes:** Leaving patient name/DOB embedded inside ECG XML/PDF headers; assigning different IDs to repeat visits of the same patient (guaranteed future leakage!); overwriting raw hospital spreadsheets with manually edited Excel files.

**Recovery procedure:** Quarantine any intake batch containing residual PHI or broken hashes, scrub/re-acquire cleanly into a new `DS####` version, verify Tier 2A/2B isolation, and document remediation transparently.

**Definition of Done:** Immutable, PHI-de-identified, patient-linked four-modality raw `DS####` inventory locked and backed up; clinical usability assessed next. Universal DoD applies.

**Next step:** [STEP-013](#step-013)

---

<a id="step-013"></a>
## STEP-013 — Audit four-modality quality, ECG signal integrity, missingness, and pass `G04`

**Objective:** Inspect actual clinical, ECG, laboratory, and lifestyle data quality, missingness mechanisms (MNAR/MAR), modality alignment, and spectrum bias to approve cohort suitability and pass `G04`.

**Why this step exists:** Readable hospital exports routinely hide mixed lab units (`mg/dL` vs `mmol/L`), unusable/noisy ECG recordings, post-diagnosis timing conflicts, or extreme site/demographic confounding that destroy Q1 validity.

**Governing section references:** [OS §4](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-012` immutable `DS####` intake complete; `UD05` IRB permissions current; clinical/ECG reviewer available for sample quality review.

**Estimated difficulty and time (provisional):** Hard; 4–8 hours automated QC + clinical visual ECG/record spot-check.

**Parallelizable:** Automated tabular QC (Clinical/Lab/Lifestyle) and ECG signal-quality audits can run concurrently on `DS####`.

**Inputs:** Locked `DS####` raw inventory, `T09` (`cohort_card.md`), `STEP-010` EPV targets, `UD07`, `UD26`.

**Expected outputs:** Four-modality QC & missingness report (`DS####_quality.md`), ECG format/SNR/artifact audit, modality overlap Venn/matrix counts, reconciled exclusions/quarantine ledger, `DS####_card.md`, small-$N$ contingency trigger assessment (`UD26`), and `G04` audit.

**Repository/file changes:** Create `03_Datasets_Cohort/reports/DS####_quality.md`, `DS####_ecg_audit.md`, `DS####_card.md`, and `01_Project_Management/reviews/G04_assessment_<date>.md`; update `datasets.csv` and `gates.csv`.

**Execution procedure:**

1. Run read-only tabular profiling across Clinical, Laboratory, and Lifestyle fields: check missingness rates per variable and per site, unit heterogeneity (`mg/dL` vs `mmol/L`, `cm` vs `m`), physiological impossibilities (`SBP <= DBP`, negative values, extreme outliers), and temporal alignment relative to `IndexDate` ($t_0$).
2. Audit all ECG records (`UD07`): inspect actual file format, lead counts, sampling rates, duration, flatlines, clipping, baseline wander, 50 Hz powerline noise, SNR distributions, and conduct a stratified clinician visual check of raw ECG quality (and verify residual PHI is zero!).
3. Quantify four-modality availability (`All 4 complete`, `3 of 4`, `2 of 4`, per-modality availability by CVD status and site) to detect **informative missingness (MNAR)** and **spectrum/site imbalance** (e.g., whether age, sex, or site distributions diverge dramatically between CVD+ and CVD−).
4. Reconcile `Acquired = Retained + Excluded + Quarantined` using prospective quality rules only, evaluate whether observed $N$/$E$ triggers small-$N$ contingency (`UD26`), finalize `DS####_card.md`, and assess `G04`.

**Planning/review prompt:**

> Audit four-modality raw quality, ECG signal usability, lab unit consistency, MNAR missingness patterns, and site/demographic spectrum balance in `DS####`. Identify fatal confounders or EPV shortfalls honestly without peeking at model errors.

**Implementation prompt:**

> Run read-only profiling and ECG signal-integrity checks via `environment/data/` producing aggregate statistics and restricted visual QC sheets. Preserve raw bytes unchanged and log every exclusion criterion explicitly.

**Human-only actions and decisions:** Hospital custodian confirms de-identification/permissions; clinical/ECG reviewer validates ECG usability; supervisor and researchers approve cohort suitability, `UD07` format findings, `UD26` contingency status, and sign `G04`.

**Version-control/artifact expectations:** Commit safe aggregate QC reports, `DS####_card.md`, and `G04` review; keep per-patient QC plots and ECG strips strictly in restricted Tier 2B storage.

**Documentation updates:** `datasets.csv`, `DS####_card.md`, `DS####_quality.md`, `decisions.csv` (`UD04`/`UD06`/`UD07`/`UD26`), `gates.csv`.

**Verification checklist:**

- [ ] Patient/encounter/modality counts reconcile identically with zero raw byte mutation.
- [ ] Residual PHI audit passed across tabular fields and ECG headers/plots.
- [ ] ECG sampling rate, lead integrity, noise/artifact profile, and lab unit differences fully documented.
- [ ] Missingness/MNAR, spectrum-bias risks, and EPV sufficiency assessed; `G04` PASS evidenced with IRB/custodian/supervisor review.

**Common mistakes:** Dropping hard/noisy records selectively without pre-specified rules; ignoring lab unit discrepancies across two diagnostic centers; overlooking that missing lab/ECG tests correlate strongly with CVD status (MNAR).

**Recovery procedure:** Quarantine defective subsets under documented rules, remediate extraction bugs via a new `DS####` version, expand hospital recruitment or activate `UD06`/`UD26` if EPV is inadequate, and re-audit `G04`.

**Definition of Done:** `G04` PASS for an ethically authorized, PHI-verified, quality-audited four-modality cohort (`DS####`) with explicit metadata limitations. Universal DoD applies.

**Next step:** [STEP-014](#step-014)

---

<a id="step-014"></a>
## STEP-014 — Define CVD clinical endpoint charter and four-modality variable dictionary

**Objective:** Freeze the exact operational cardiovascular disease endpoint, prediction horizon, index time ($t_0$), alignment window ($\Delta t$), and complete four-modality variable dictionary/CRF (`UD02`, `UD03`, `UD08`).

**Why this step exists:** Proposal examples (`RF10`) are not a reproducible clinical schema; undefined CVD criteria, horizon ambiguity (longitudinal vs cross-sectional), or post-diagnosis variables inside "Medical History" cause fatal Q1 PROBAST bias.

**Governing section references:** [OS §1](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §5](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS Appendix B](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-013` complete; `G04` PASS; qualified cardiologist/clinical adjudicator engaged.

**Estimated difficulty and time (provisional):** Hard; 4–6 hours plus cardiologist consultation.

**Parallelizable:** Drafting Clinical, Lab, and Lifestyle variable rows can be split between researchers; endpoint charter, $t_0/\Delta t$ rules, and incorporation-bias checks require joint cardiologist review.

**Inputs:** `RF03`, `RF10`, `DS####_card.md` & quality findings, literature endpoint conventions (`STEP-007`), `T10` (`endpoint_charter.md`), `UD02–UD03`, `UD08`.

**Expected outputs:** Reviewed `04_Outcome_Schema_QA/endpoint_charter.md`, populated `04_Outcome_Schema_QA/variables.csv`, versioned CRF/abstraction manual, and incorporation-bias assessment.

**Repository/file changes:** Create `04_Outcome_Schema_QA/endpoint_charter.md`, `04_Outcome_Schema_QA/variables.csv`, `04_Outcome_Schema_QA/crf/crf_manual_v1.0.0.md`, and draft `DEC####` for `UD02`, `UD03`, `UD08`.

**Execution procedure:**

1. Define exact CVD target criteria (`UD02`): qualifying diagnoses/ICD-10 codes (e.g., CAD/IHD, MI/ACS, heart failure, stroke), confirmed non-CVD control definition, binary vs multi-class/ordinal formulation, and **honest study horizon classification** (prospective longitudinal follow-up with censoring rules vs cross-sectional early-stage diagnostic risk stratification).
2. Lock index time $t_0$ and maximum modality synchronization window $\Delta t$ (`UD03`), explicitly prohibiting any lab, ECG, or medication recorded *after* CVD diagnosis or treatment initiation from entering predictor sets.
3. Audit **incorporation bias** (PROBAST Domain 3): flag any predictor (e.g., diagnostic ECG changes or acute troponin) directly used to assign the outcome label and pre-register a sensitivity analysis excluding high-incorporation-bias variables where clinically warranted.
4. Populate `variables.csv` (`UD08`) for every Clinical, ECG, Laboratory, and Lifestyle feature—exact standardized units, physiological valid ranges, categorical codes (separating `refused/missing` from `0`), explicit documented placement of `Family History` (`RF10`), and exclusion list of leakage/treatment fields.

**Planning/review prompt:**

> Draft `endpoint_charter.md` and `variables.csv` from `DS####` reality and `RF10`. Audit every single predictor for temporal post-diagnosis leakage, medication leakage, unit ambiguity, and PROBAST incorporation bias, flagging unresolved clinical questions for the cardiologist.

**Implementation prompt:**

> Documentation & schema only: save `endpoint_charter.md`, `variables.csv`, and `crf_manual_v1.0.0.md` with explicit version headers. Leave unapproved clinical rules explicitly `Unresolved / Human Decision Required`.

**Human-only actions and decisions:** Qualified cardiologist and supervisor decide final CVD endpoint definition, horizon framing (`UD02`), $t_0/\Delta t$ window (`UD03`), and clinical variable inclusions/exclusions (`UD08`).

**Version-control/artifact expectations:** Commit PHI-free schema, endpoint charter, and CRF manual; keep any clinical example sheets strictly de-identified or restricted.

**Documentation updates:** `endpoint_charter.md`, `variables.csv`, `decisions.csv` (`UD02`, `UD03`, `UD08`).

**Verification checklist:**

- [ ] CVD positive, negative, and uncertain/borderline criteria operationally defined with standard codes.
- [ ] Prospective vs cross-sectional horizon explicitly locked with matching manuscript framing constraints.
- [ ] Index time $t_0$, $\Delta t$ window, and post-diagnosis/medication exclusion list specified.
- [ ] Every Clinical, Lab, and Lifestyle variable has exact unit, valid range, missingness code, and incorporation-bias rating; Family History grouping documented.

**Common mistakes:** Calling a cross-sectional hospital cohort "5-year prospective early risk prediction"; leaving post-diagnosis aspirin/statin/beta-blocker therapy or "previous MI" inside Medical History while predicting current CVD; conflating missing lifestyle answers with "healthy = 0."

**Recovery procedure:** Revise ambiguous clinical definitions with cardiologist sign-off, version `endpoint_charter_v1.1.0.md` / `variables.csv`, and re-verify before `STEP-015`.

**Definition of Done:** Complete, clinically reviewed CVD endpoint charter and four-modality variable dictionary ready for ECG & QA protocol freeze. Universal DoD applies.

**Next step:** [STEP-015](#step-015)

---

<a id="step-015"></a>
## STEP-015 — Approve ECG contract, clinical adjudication rules, QA thresholds, and pass `G05`

**Objective:** Freeze the ECG data/representation contract (`UD07`), outcome adjudication workflow, inter-rater QA thresholds (`UD09`), and pass `G05` before pilot curation/adjudication.

**Why this step exists:** Unpinned ECG formats, ad-hoc label editing, or post-hoc QA thresholds destroy ground-truth validity and Q1 reproducibility.

**Governing section references:** [OS §5](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS §15](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-15); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-014` reviewed endpoint charter & `variables.csv`; ECG format findings (`STEP-013`); named qualified cardiologist/clinical adjudicator confirmed.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours plus cardiologist & supervisor sign-off.

**Parallelizable:** ECG schema parser testing on synthetic waveforms can accompany QA protocol drafting; final `G05` approval is serialized.

**Inputs:** `endpoint_charter.md`, `variables.csv`, `DS####_ecg_audit.md`, `T11` (`crf_ecg_protocol.md`), `UD07`, `UD09`.

**Expected outputs:** Approved `04_Outcome_Schema_QA/ecg_contract.md`, frozen `endpoint_charter.md` & `variables.csv` (v1.0.0 hashes), prospective pilot/production QA thresholds (`qa_protocol.md`), verified synthetic schema parser test, and `G05` assessment.

**Repository/file changes:** Finalize `04_Outcome_Schema_QA/ecg_contract.md`, `qa_protocol.md`, `variables.csv`; add synthetic parser tests in `tests/test_schema_ecg.py`; write `01_Project_Management/reviews/G05_assessment_<date>.md`; update `decisions.csv` and `gates.csv`.

**Execution procedure:**

1. Finalize `ecg_contract.md` (`UD07`): lock authoritative ECG input format (e.g., 12-lead digital WFDB/XML/CSV at target Hz & length, and/or extracted standard intervals), lead order, amplitude units (mV), missing-lead handling, quality rejection criteria, and (if digitized paper ECGs are unavoidable) a mandatory digitization-accuracy validation protocol.
2. Specify the clinical adjudication & data-abstraction workflow (`UD09`): roles of abstractors vs qualified cardiologist adjudicator, blinding of adjudicator where feasible, handling of `uncertain / needs_adjudication` encounters, and immutable logging of label corrections.
3. Lock prospective pilot sample size, stratification (CVD+, CVD−, noisy ECG, multi-comorbidity), agreement metrics (Cohen's $\kappa$ for binary/categorical outcomes & lifestyle items; ICC & max numeric tolerance for continuous clinical/lab labs), and minimum PASS thresholds **prior to inspecting pilot agreement**.
4. Test schema validation and ECG parsing on synthetic fixtures, record SHA-256 hashes of frozen `endpoint_charter.md`, `variables.csv`, and `ecg_contract.md`, and obtain cardiologist + supervisor `G05` sign-off.

**Planning/review prompt:**

> Audit `endpoint_charter.md`, `variables.csv`, `ecg_contract.md`, and `qa_protocol.md` against `G05` criteria. Confirm zero ambiguity in ECG lead/unit schema, missing vs zero encoding, adjudication blinding, and prospective $\kappa$/ICC thresholds.

**Implementation prompt:**

> Freeze v1.0.0 schema files, compute SHA-256 hashes, and implement synthetic schema/ECG-parser unit tests in `tests/test_schema_ecg.py` using `environment/data/`. Record actual `UD07`/`UD09` decisions and `G05` evidence.

**Human-only actions and decisions:** Qualified cardiologist and supervisor ratify `UD07`, `UD09`, frozen clinical schemas, and sign `G05`.

**Version-control/artifact expectations:** Commit frozen v1.0.0 protocol files, hashes, and synthetic parser tests as `schema: freeze CVD endpoint, 4-modality dictionary, ECG contract and pass G05`.

**Documentation updates:** `variables.csv`, `ecg_contract.md`, `qa_protocol.md`, `decisions.csv`, `gates.csv`, `dashboard.md`.

**Verification checklist:**

- [ ] Endpoint charter, `variables.csv`, and `ecg_contract.md` frozen with SHA-256 hashes.
- [ ] ECG representation (leads, Hz, units, quality rules) unambiguously specified.
- [ ] Pilot sample size, dual-abstraction $\kappa$/ICC metrics, and minimum acceptance thresholds locked prospectively.
- [ ] Synthetic schema/ECG parser tests pass; `G05` PASS signed by cardiologist and supervisor.

**Common mistakes:** Leaving ECG format vague ("ECG signals") while abstracting data; picking $\kappa$ thresholds *after* seeing noisy abstraction; omitting rules for uncertain clinical outcomes.

**Recovery procedure:** Resolve schema gaps or parser failures, bump schema version (`v1.1.0`), re-test, and secure renewed cardiologist/supervisor `G05` approval prior to pilot start.

**Definition of Done:** `G05` PASS for versioned clinical endpoint, 4-modality schema, ECG contract, and prospective QA protocol. Universal DoD applies.

**Next step:** [STEP-016](#step-016)

---

<a id="step-016"></a>
## STEP-016 — Run pilot abstraction, clinical adjudication, and inter-rater QA

**Objective:** Empirically verify that abstractors and clinicians can curate all four modalities and adjudicate CVD outcomes consistently under the frozen `G05` protocol.

**Why this step exists:** Written CRFs and diagnostic rules frequently break on ambiguous real-world hospital charts, incomplete lab panels, and borderline ECGs; pilot calibration catches systemic errors before full cohort curation.

**Governing section references:** [OS §5](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-015` complete; `G04–G05` PASS; stratified pilot encounter sample drawn from `DS####`.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours setup/analysis plus independent dual abstraction and cardiologist adjudication.

**Parallelizable:** Two abstractors work completely independently on the pilot encounters before reconciliation; never copy labels across abstractors prior to agreement computation.

**Inputs:** Prospective pilot sample (`DS####`), frozen `endpoint_charter.md`, `variables.csv`, `ecg_contract.md`, `qa_protocol.md`.

**Expected outputs:** Independent dual pilot abstractions (preserved separately), inter-rater agreement report ($\kappa$, ICC, numeric discrepancy rates, ECG quality agreement), cardiologist adjudications, measured curation throughput, and pilot acceptance or protocol-revision plan.

**Repository/file changes:** Store restricted independent & adjudicated pilot files in Tier 2B `04_Outcome_Schema_QA/adjudications/pilot/`; commit safe aggregate `04_Outcome_Schema_QA/reviews/pilot_qa_review.md`.

**Execution procedure:**

1. Select the prospectively defined stratified pilot sample from `DS####` (covering CVD+, CVD−, noisy/abnormal ECGs, partial labs, and lifestyle questionnaires) and log selection seed/IDs.
2. Execute independent dual abstraction/entry and ECG quality grading under frozen v1.0.0 protocols, preserving both independent records immutably.
3. Compute Cohen's $\kappa$ (outcome, binary clinical/lifestyle fields), ICC and discrepancy rates (continuous labs/vitals), unit-conversion error rate, and ECG quality agreement using `environment/data/`.
4. Have the qualified cardiologist adjudicate every discrepancy and borderline case; evaluate against prospective `G05` thresholds—if thresholds fail or protocol rules change, revise protocols, re-pass `G05`, and repeat pilot verification.

**Planning/review prompt:**

> Evaluate the pilot curation and adjudication results strictly against `qa_protocol.md` thresholds. Distinguish clerical entry mistakes, unit mismatches, lifestyle coding ambiguity, and genuine clinical diagnostic uncertainty.

**Implementation prompt:**

> Compute inter-rater $\kappa$, ICC, exact mismatch counts, and ECG grading agreement from independent pilot records using `environment/data/`. Save aggregate `pilot_qa_review.md` in Git while keeping individual encounter files strictly in Tier 2B.

**Human-only actions and decisions:** Qualified cardiologist adjudicates all pilot disagreements and certifies pilot readiness; supervisor approves any protocol/scope adjustment.

**Version-control/artifact expectations:** Independent raw pilot files and adjudicated labels remain restricted in Tier 2B with SHA-256 backups; commit safe aggregate `pilot_qa_review.md` and any updated protocol version.

**Documentation updates:** `pilot_qa_review.md`, `timeline.md` (updated using measured curation throughput), `risk_register.csv`.

**Verification checklist:**

- [ ] Pilot sample follows prospective stratification and size rules.
- [ ] Both independent abstraction records preserved separately before reconciliation.
- [ ] $\kappa$, ICC, numeric mismatch rates, and ECG agreement reported honestly against prospective thresholds.
- [ ] All discrepancies adjudicated by cardiologist; changed protocol rules re-approved under `G05`.

**Common mistakes:** Letting abstractors discuss cases *before* measuring inter-rater agreement; lowering $\kappa$ acceptance criteria post hoc; ignoring systematic lab-unit transcription mistakes.

**Recovery procedure:** Clarify ambiguous CRF/endpoint rules, retrain abstractors, re-pass `G05` if rules changed, re-abstract a fresh pilot check, and retain failed pilot logs transparently.

**Definition of Done:** Pilot passes prospective `G05` QA thresholds with cardiologist sign-off, authorizing tracked production curation. Universal DoD applies.

**Next step:** [STEP-017](#step-017)

---

<a id="step-017"></a>
## STEP-017 — Execute tracked production curation and clinical adjudication batches

**Objective:** Curate, harmonize, link, and adjudicate the full authorized cohort across all four modalities in auditable, quality-monitored batches (`ADJB####`).

**Why this step exists:** Untracked bulk chart abstraction produces silent unit errors, unreviewed missing values, temporal alignment violations, and unrecoverable label drift.

**Governing section references:** [OS §5](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §11](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-016` accepted pilot; `G04–G05` current PASS; batch schedule and Tier 2B workspace prepared.

**Estimated difficulty and time (provisional):** Hard; 2–4 hours per curation/review session, repeated across batches (total duration driven by measured pilot throughput and hospital enrollment).

**Parallelizable:** Disjoint non-overlapping encounter batches (`ADJB####`) can be curated concurrently by both researchers; dual-QA sampling and clinical adjudication remain centralized.

**Inputs:** Frozen `G05` schemas/CRF/ECG contract, `DS####` raw intakes, batch assignments, `T12` (`adjudication_batch.md`).

**Expected outputs:** Verified tabular + ECG-linked batch outputs, explicit `missing` vs `0` codes, $t_0/\Delta t$ compliance flags, cardiologist adjudication logs, and per-batch `04_Outcome_Schema_QA/reviews/ADJB####.md` reports.

**Repository/file changes:** Store restricted batch tables & adjudication records in Tier 2B `04_Outcome_Schema_QA/adjudications/ADJB####/`; commit safe aggregate `reviews/ADJB####.md` logs.

**Execution procedure:**

1. Partition authorized encounters into disjoint `ADJB####` batches recording site, collector/abstractor, protocol/schema versions, and date range.
2. Harmonize clinical/laboratory units strictly per `variables.csv`, verify $t_0/\Delta t$ temporal alignment (quarantining any post-diagnosis/treatment-leaking modality record), link each encounter's raw ECG file, and encode lifestyle missing/refused states explicitly.
3. Queue every borderline/conflicting CVD diagnosis and poor-quality ECG to the qualified cardiologist adjudicator; never coerce uncertain cases silently into `0` or `1`.
4. Run ongoing dual-entry QA audits on the prospectively scheduled subsample per batch, resolve discrepancies, back up native and verified batch files with SHA-256 hashes, and close each batch only when QA checks pass.

**Planning/review prompt:**

> Prepare the batch assignment, $t_0/\Delta t$ temporal-alignment check, and ongoing dual-QA audit plan for `ADJB####`. Flag emerging missingness trends, site bottlenecks, or drift from pilot agreement rates.

**Implementation prompt:**

> Run deterministic schema/unit/range/ECG-link validation scripts from `environment/data/` on batch `ADJB####`. Quarantine out-of-window or invalid rows explicitly instead of silently imputing or coercing them.

**Human-only actions and decisions:** Qualified cardiologist adjudicates all queued clinical outcomes and ECG quality appeals; researchers verify dual-QA batch pass/fail.

**Version-control/artifact expectations:** Native and verified encounter-level batch datasets stay strictly in encrypted Tier 2B with verified backups; Git stores safe aggregate `ADJB####.md` QA metrics and hashes only.

**Documentation updates:** Per-batch `ADJB####.md`, cumulative enrollment/event tracker in `dashboard.md`, updated `risk_register.csv`.

**Verification checklist:**

- [ ] Every encounter in the batch has a recorded curation, temporal-alignment, and adjudication status.
- [ ] Standardized units, range checks, and explicit missingness codes verified across all 4 modalities.
- [ ] Scheduled dual-entry QA subsample passed thresholds with discrepancies resolved.
- [ ] All uncertain CVD outcomes adjudicated by cardiologist or explicitly quarantined under `endpoint_charter.md`.

**Common mistakes:** Silently filling blank lifestyle/smoking fields with `0`; skipping temporal alignment checks on lab tests taken *after* cardiac catheterization; closing batches before cardiologist adjudication finishes.

**Recovery procedure:** Reopen failed `ADJB####` batches, trace systemic coding/unit bugs back to the earliest affected batch, re-abstract/re-adjudicate affected encounters, preserve original files, and re-verify before release.

**Definition of Done:** All planned production batches curated, temporally audited, clinically adjudicated, and ready for whole-cohort QA freeze. Universal DoD applies.

**Next step:** [STEP-018](#step-018)

---

<a id="step-018"></a>
## STEP-018 — Audit whole-cohort clinical/structural QA and freeze `ADJ####` (`G06`)

**Objective:** Conduct comprehensive automated and stratified clinical quality assurance across the entire curated four-modality cohort, freeze immutable `ADJ####` hashes, and pass `G06`.

**Why this step exists:** Splitting and modeling on an unverified merged cohort hides cross-batch schema drift, orphaned ECG files, duplicate patients, or unresolved diagnostic labels.

**Governing section references:** [OS §5](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-017` all production batches closed; pilot and batch QA logs intact; `G04–G05` current.

**Estimated difficulty and time (provisional):** Hard; 4–6 hours automated whole-cohort audit + stratified cardiologist final review.

**Parallelizable:** Automated structural/temporal/ECG-linkage audits and stratified clinical spot-reviews may run concurrently; final `ADJ####` freeze waits for both.

**Inputs:** All closed `ADJB####` batch outputs, `DS####` raw manifest, frozen `endpoint_charter.md`, `variables.csv`, `ecg_contract.md`, `UD10`.

**Expected outputs:** Whole-cohort QA audit report (`adjudication_release_audit.md`), reconciled STARD/CONSORT cohort flow numbers, missingness & modality-availability matrix (`UD10`), frozen immutable `ADJ####` release hashes, `adjudication_registry.csv` entry, and `G06` assessment.

**Repository/file changes:** Lock restricted Tier 2B `04_Outcome_Schema_QA/adjudications/ADJ####/`; commit safe `04_Outcome_Schema_QA/adjudication_registry.csv`, `reviews/adjudication_release_audit.md`, `01_Project_Management/reviews/G06_assessment_<date>.md`, and update `gates.csv`.

**Execution procedure:**

1. Run whole-cohort integrity validation: unique `ENC########` keys, exact `PAT########` grouping integrity, zero schema/unit/range violations, 100% verified ECG file-path/hash correspondence, zero post-$t_0$ temporal-alignment violations, and full reconciliation of retained vs excluded vs uncertain encounters.
2. Perform a final stratified clinical spot-check (random fixed-seed sample across sites, CVD+/CVD−, and borderline/partial-modality cases) with the qualified cardiologist confirming adjudication closure and residual label uncertainty.
3. Finalize `UD10` missing-modality cohort policy (documenting exact count of complete 4-modality vs partial-modality patients retained for training/evaluation and missingness mechanism diagnostics).
4. Compute immutable SHA-256 hashes for the native and verified `ADJ####` artifacts, verify encrypted Tier 2B backup, update `adjudication_registry.csv`, and record `G06` outcome.

**Planning/review prompt:**

> Audit the merged four-modality cohort (`ADJ####`) against `G06` criteria. Verify full count reconciliation (suitable for `FIG0001` cohort flow), zero temporal/unit violations, and honest reporting of residual clinical adjudication uncertainty.

**Implementation prompt:**

> Execute whole-cohort automated structural, linkage, range, and ECG-integrity audits via `environment/data/`, generate immutable `ADJ####` SHA-256 manifests in Tier 2B, and output safe aggregate QA tables to `adjudication_release_audit.md`. Never silently auto-repair clinical values.

**Human-only actions and decisions:** Qualified cardiologist certifies clinical label integrity; data lead and supervisor approve `UD10` inclusion/missing-modality rules and sign `G06`.

**Version-control/artifact expectations:** Immutable `ADJ####` data stays in encrypted Tier 2B with verified backup; commit `adjudication_registry.csv`, safe QA report, cohort flow counts, and `G06` audit.

**Documentation updates:** `adjudication_registry.csv`, `adjudication_release_audit.md`, `decisions.csv` (`UD10`), `gates.csv`, `dashboard.md`.

**Verification checklist:**

- [ ] Zero unresolved schema, unit, range, orphan-ECG, or $t_0/\Delta t$ temporal violations.
- [ ] All batch dual-QA & final stratified cardiologist review metrics meet prospective `G05` thresholds.
- [ ] Cohort flow counts (Screened → Enrolled → Excluded/Uncertain → Final `ADJ####`) reconcile identically.
- [ ] `ADJ####` SHA-256 frozen and backed up; `G06` PASS signed by cardiologist and data lead.

**Common mistakes:** Assuming passing batch-level checks means cross-batch merged data has zero duplicate patients; hiding unresolved uncertain diagnoses inside the negative class.

**Recovery procedure:** Quarantine defective records/batches, remediate under cardiologist review, issue a new `ADJ####` version linked to its parent, and re-audit `G06`.

**Definition of Done:** `G06` PASS for a frozen, clinically adjudicated, four-modality `ADJ####` cohort ready for leakage-safe splitting. Universal DoD applies.

**Next step:** [STEP-019](#step-019)

---

<a id="step-019"></a>
## STEP-019 — Design leakage-free modality preprocessing, ECG filtering, and masking contracts

**Objective:** Architect the complete four-modality preprocessing specification, explicitly separating record-local deterministic operations from post-split training-only fitted transforms (`UD12`), resolving the proposal diagram leakage risk (`RF13`).

**Why this step exists:** Fitting imputers, scalers, encoders, or oversamplers before splitting invalidates Q1 claims, while overly aggressive ECG filtering can erase diagnostic ST-segment elevation/depression or T-wave inversions.

**Governing section references:** [OS §4](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §5](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-05); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-018` complete; `G06` PASS; frozen `ADJ####`, `variables.csv`, and `ecg_contract.md` available.

**Estimated difficulty and time (provisional):** Hard; 4–6 hours including ECG filter prototyping on synthetic/approved sample signals.

**Parallelizable:** Tabular preprocessing specs (Clinical/Lab/Lifestyle) and ECG signal-processing specs can be drafted in parallel; unified leakage-isolation review is joint.

**Inputs:** `ADJ####` QA & missingness reports, `variables.csv`, `ecg_contract.md`, `RF13`, `UD10`, `UD12`.

**Expected outputs:** Approved preprocessing design (`05_Preprocessing_Alignment/specs/pipeline.md`), explicit pre-split vs post-split operation boundary, ECG filter & morphology check criteria, missingness/modality mask contract, and unit tests in `tests/test_preprocessing_leakage.py`.

**Repository/file changes:** Create `05_Preprocessing_Alignment/specs/pipeline.md`, versioned config template in `05_Preprocessing_Alignment/configs/`, preprocessing modules in `src/cvd_mm/preprocessing.py` and `src/cvd_mm/ecg.py`, and synthetic leakage tests in `tests/`.

**Execution procedure:**

1. Partition every preprocessing operation into **Stage A (Record-local deterministic ONLY):** schema enforcement, unit harmonization, fixed-rate ECG resampling, fixed-parameter 50 Hz (or 60 Hz external) notch filter, and gentle baseline-wander filter ($\le 0.5\text{ Hz}$ zero-phase high-pass / wavelet filter designed to preserve ST-segment morphology) vs **Stage B (Training-partition-only fitted AFTER `STEP-020`):** numeric imputation (e.g., median/MICE/iterative), categorical encoding, continuous scaling (Standard/Robust/Quantile), optional skewed-lab log transforms, and any per-lead cohort normalization.
2. Specify explicit **feature-level missingness indicator columns** (capturing MNAR diagnostic ordering signal transparently) and **modality-level binary presence masks** (`[has_clinical, has_ecg, has_lab, has_lifestyle]`) so the Transformer fusion model handles missing modalities cleanly without fabricating synthetic ECG waveforms.
3. Prohibit pre-split SMOTE or synthetic oversampling of multimodal vectors; specify class-weighted loss / focal loss and validation-only probability calibration as default imbalance handling (`UD15`).
4. Implement synthetic unit tests proving that fitting Stage B transforms uses training indices exclusively and fails loudly if validation/test records are passed into `.fit()`.

**Planning/review prompt:**

> Design a leakage-proof four-modality preprocessing specification reconciling Proposal Diagram Boxes 2–3 with Box 4. Audit every ECG filter parameter for ST-T wave distortion risk and verify that missingness indicators and missing-modality masks are cleanly engineered.

**Implementation prompt:**

> Implement deterministic record-local ECG/tabular cleaners and `fit`/`transform` interfaces in `src/cvd_mm/preprocessing.py` and `src/cvd_mm/ecg.py` with pytest synthetic leakage guards. Do NOT fit any imputer or scaler on real `ADJ####` data until `STEP-020` locks the split.

**Human-only actions and decisions:** Clinical/ECG reviewer approves ECG filter parameters and morphology check criteria; researchers and supervisor approve `UD12` imputation, scaling, and missing-modality contracts.

**Version-control/artifact expectations:** Commit specs, code, and synthetic tests; keep any sample patient ECG inspection strips restricted in Tier 2B.

**Documentation updates:** `05_Preprocessing_Alignment/specs/pipeline.md`, `decisions.csv` (`UD12`), `13_Documentation/pipeline.md`.

**Verification checklist:**

- [ ] Strict operational wall separating record-local pre-split ops from post-split training-only fits.
- [ ] ECG notch/bandpass/baseline parameters explicitly chosen to protect ST-segment, T-wave, and Q-wave morphology.
- [ ] Feature missingness indicators and modality presence masks specified cleanly.
- [ ] Automated synthetic leakage tests pass; zero dataset statistics fitted before `STEP-020`.

**Common mistakes:** Running `StandardScaler().fit_transform(X_all)` or `KNNImputer().fit_transform(X_all)` before splitting; applying an aggressive 1–2 Hz high-pass ECG filter that distorts ST-segment elevation; silently imputing zeros for an entirely absent ECG modality.

**Recovery procedure:** Disable leaking or distorting transforms, patch `src/cvd_mm/`, update `pipeline.md` version, and re-run synthetic unit tests before splitting.

**Definition of Done:** Reviewed, leakage-tested preprocessing design and code ready; training-only fitting remains blocked until `G07` PASS. Universal DoD applies.

**Next step:** [STEP-020](#step-020)

---

<a id="step-020"></a>
## STEP-020 — Construct and approve patient/site-level leakage-safe split (`G07`)

**Objective:** Lock deterministic, patient-grouped, outcome-stratified data partitions (Train/Val/Test and/or nested CV + external/site holdout per `UD11`), seal final test access, and pass `G07`.

**Why this step exists:** Splitting multiple visits/ECGs of one patient across train and test, or peeking at test performance during development, causes catastrophic optimistic bias and immediate Q1 rejection.

**Governing section references:** [OS §4](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-019` preprocessing spec complete; `G04–G06` PASS; frozen `ADJ####` with verified `PAT########`, `SITE####`, and duplicate-linkage keys.

**Estimated difficulty and time (provisional):** Hard; 4–6 hours plus biostatistics & supervisor review.

**Parallelizable:** No competing splits selected by model accuracy; grouping/duplicate graph auditing precedes one deterministic split generation.

**Inputs:** Frozen `ADJ####` manifest, `PAT########`/`SITE####`/duplicate graph, measured $N$/$E$ prevalence, `T14` (`split.md`), `UD11`.

**Expected outputs:** Immutable `SPLIT####` manifest (`manifest.csv`), split configuration & fixed RNG seed, balance tables (outcome, site, sex, age, modality completeness across partitions), zero-overlap verification proof, test-custody seal policy, and `G07` assessment.

**Repository/file changes:** Store restricted encounter-level `03_Datasets_Cohort/splits/SPLIT####/manifest.csv` in Tier 2B; commit safe config, seed, aggregate balance tables (`report.md`), hash, `src/cvd_mm/splitting.py`, `tests/test_splitting.py`, and `01_Project_Management/reviews/G07_assessment_<date>.md`; update `gates.csv`.

**Execution procedure:**

1. Build connected grouping components linking every repeated encounter, follow-up ECG, and near-duplicate record of the same `PAT########` so no individual can ever span two partitions.
2. Select and approve the exact split geometry (`UD11`) based on measured $N$ and event count $E$: stratified patient-grouped Train/Validation/Test (e.g., 70/15/15 or 60/20/20) OR (recommended if $N$ is modest) stratified patient-grouped held-out Test + inner $K$-fold / nested CV, PLUS temporal or leave-one-site-out external holdout if multi-site/temporal span permits.
3. Run deterministic `src/cvd_mm/splitting.py` with fixed seed, asserting zero patient overlap, zero exact/near-duplicate leakage, reproducible identical outputs on re-run, and balanced CVD event prevalence, sex/age distribution, and 4-modality completeness across partitions (preserving patient groups even if exact ratios round slightly).
4. Seal the final test partition under documented access custody (`test_access_log.csv` initialized empty), verify `G07` criteria, and obtain supervisor + biostatistics sign-off.

**Planning/review prompt:**

> Design and audit `SPLIT####` for patient-level zero-leakage integrity, clinical stratification (CVD event, sex, site, modality availability), and appropriateness of Train/Val/Test vs nested CV given measured $N$ and $E$.

**Implementation prompt:**

> Implement deterministic grouped-stratified splitting in `src/cvd_mm/splitting.py` with zero-overlap assertions and pytest verification. Emit immutable `SPLIT####/manifest.csv` in Tier 2B and safe aggregate balance tables in `report.md`.

**Human-only actions and decisions:** Supervisor and biostatistics reviewer approve split design (`UD11`), accept minor rounding deviations from target percentages to preserve patient groups, and sign `G07`.

**Version-control/artifact expectations:** Never overwrite an existing `SPLIT####`; store encounter-level `manifest.csv` in Tier 2B and safe aggregate balance report + hashes + code in Tier 1 Git.

**Documentation updates:** `SPLIT####/report.md`, `decisions.csv` (`UD11`), `test_access_log.csv`, `gates.csv`, `dashboard.md`.

**Verification checklist:**

- [ ] Automated assertion proves zero `PAT########` or near-duplicate overlap across Train, Val, Test, and outer CV folds.
- [ ] Re-running script with recorded seed reproduces identical manifest SHA-256 bit-for-bit.
- [ ] Outcome prevalence, modality availability, sex, age, and site counts reported per partition.
- [ ] Final test partition formally sealed; `G07` PASS signed and dated.

**Common mistakes:** Using `sklearn.model_selection.train_test_split` randomly on encounters when patients have multiple hospital visits; retrying 20 random seeds to pick the "nicest" split; peeking at test distributions to adjust feature definitions.

**Recovery procedure:** Invalidate any leaked `SPLIT####` and all descendants, repair patient-grouping graph, generate a brand-new `SPLIT####`, re-audit `G07`, and disclose any prior test exposure transparently.

**Definition of Done:** `G07` PASS with reproducible, zero-overlap patient/site-level `SPLIT####` and sealed final test custody. Universal DoD applies.

**Next step:** [STEP-021](#step-021)

---

<a id="step-021"></a>
## STEP-021 — Fit training-only preprocessing states and verify ECG morphological fidelity

**Objective:** Execute record-local ECG/tabular cleaning, fit all imputation/scaling/encoding states strictly on the training partition (or inside each CV training fold), verify zero cross-partition leakage, and obtain cardiologist confirmation of ECG waveform fidelity.

**Why this step exists:** Even a clean split leaks silently if fitted preprocessing touches validation/test summaries, and unchecked digital filters can destroy the very ST/T/Q-wave signatures the ECG encoder must detect.

**Governing section references:** [OS §4](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-020` complete; `G07` PASS; approved `STEP-019` preprocessing config (`UD12`) and frozen `ADJ####`.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours plus cardiologist ECG waveform fidelity check.

**Parallelizable:** Deterministic Stage A per-record ECG filtering may execute concurrently per partition; Stage B fitting MUST run on training indices exclusively before transforming validation/test.

**Inputs:** Frozen `ADJ####`, locked `SPLIT####` manifest & hash, approved `PP####` config, `T13` (`preprocessing.md`).

**Expected outputs:** Serialized immutable training-only fitted state (`FitStateHash`), leakage verification log, cardiologist raw-vs-filtered ECG morphology audit report, and `PP####` verification report (`05_Preprocessing_Alignment/reports/PP####.md`).

**Repository/file changes:** Store restricted serialized fitted preprocessors in Tier 2B `05_Preprocessing_Alignment/fitted_states/PP####/`; commit safe config, hashes, leakage-audit output, and cardiologist sign-off summary in `05_Preprocessing_Alignment/reports/PP####.md` and `preprocessing_registry.csv`.

**Execution procedure:**

1. Verify input `ADJ####`, `variables.csv`, and `SPLIT####` SHA-256 hashes against locked registries; fail loudly on mismatch.
2. Apply Stage A record-local deterministic cleaning (unit harmonization, resampling, fixed 50 Hz notch & gentle baseline filter) and generate paired raw-vs-filtered ECG visual strips on a stratified clinical sample (normal sinus, ST-elevation/depression, T-inversion, arrhythmia, noisy baseline) for **cardiologist morphology verification**—confirming diagnostic waves are preserved undistorted!
3. Fit Stage B transforms (imputers, scalers, encoders, missingness indicator extractors, modality-mask generators) **strictly on Training data** (and separately inside every inner/outer CV training fold if CV is used), serialize fitted objects with `FitStateHash`, and transform Train, Validation, and Test deterministically using the frozen training state.
4. Run post-transform assertions: zero `NaN`/`Inf` in model-ready tensors, preserved patient/encounter ID alignment, unchanged raw `DS####`/`ADJ####` SHA-256 hashes, and exact round-trip inverse scaling verification on continuous features.

**Planning/review prompt:**

> Audit `PP####` execution logs to confirm zero validation/test statistics influenced imputation or scaling, missingness indicators accurately mirror pre-imputation missingness, and cardiologist ECG morphology sign-off covers ST-segment and T-wave preservation.

**Implementation prompt:**

> Run the versioned `PP####` pipeline into a new immutable artifact directory, serialize training-only fitted states with SHA-256 checksums, execute leakage and NaN/alignment assertions, and write `PP####.md` report.

**Human-only actions and decisions:** Qualified cardiologist/ECG reviewer signs off on raw-vs-filtered ECG morphological fidelity; implementer verifies leakage-free execution.

**Version-control/artifact expectations:** Fitted preprocessor binaries and sample patient ECG strips remain in restricted Tier 2B/3 storage with SHA-256 backups; commit safe config, hashes, `PP####.md`, and `preprocessing_registry.csv`.

**Documentation updates:** `preprocessing_registry.csv`, `05_Preprocessing_Alignment/reports/PP####.md`, `decisions.csv` (if filter tuned before locking).

**Verification checklist:**

- [ ] Stage B imputers/scalers/encoders fitted exclusively on training data (`FitStateHash` verified; per-fold if CV).
- [ ] Cardiologist signed off that filtered ECG waveforms preserve ST-segment, T-wave, Q-wave, and QRS morphology.
- [ ] Feature missingness indicators and 4-modality presence masks validated against raw `ADJ####`.
- [ ] Zero `NaN`/`Inf`, zero raw-file mutation, and exact encounter-to-label alignment verified.

**Common mistakes:** Fitting one global imputer outside the CV loop; forgetting to save the exact fitted preprocessor needed later by the prototype and SHAP pipeline; applying aggressive smoothing that flattens small pathological Q-waves or ST shifts.

**Recovery procedure:** Quarantine faulty `PP####`, adjust ECG filter or imputer config cleanly, issue a brand-new `PP####` ID, re-run cardiologist morphology check and leakage assertions without overwriting earlier artifacts.

**Definition of Done:** Leakage-free `PP####` fitted states and cardiologist-verified ECG transforms complete and ready for `REL####` binding. Universal DoD applies.

**Next step:** [STEP-022](#step-022)

---

<a id="step-022"></a>
## STEP-022 — Materialize immutable prepared multimodal release (`REL####`) and pass `G08`

**Objective:** Bind exact parent hashes (`DS####`, `ADJ####`, `variables.csv`, `SPLIT####`, `PP####`, `FitStateHash`) into an immutable model-ready multimodal release (`REL####`) and pass `G08`.

**Why this step exists:** Fair comparison across unimodal, simple-fusion, and Transformer models requires every single experiment to consume the exact same hash-verified multimodal release.

**Governing section references:** [OS §2](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-02); [OS §4](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-04); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix B](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-b).

**Prerequisites:** `STEP-021` complete; `G06–G07` current PASS; cardiologist ECG morphology audit passed.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours plus verification and backup.

**Parallelizable:** Partition serialization and checksum generation can run concurrently; `REL####` manifest locking and `G08` sign-off are serialized.

**Inputs:** `DS####`, `ADJ####`, `variables.csv` hash, `SPLIT####` manifest, `PP####` outputs & `FitStateHash`, code commit.

**Expected outputs:** Immutable prepared multimodal release `REL####` (aligned tabular tensors/Parquet + processed ECG arrays/WFDB + modality masks + labels per partition) in Tier 2B, full release manifest + SHA-256 checksums, `releases.csv` row, and `G08` assessment.

**Repository/file changes:** Write restricted Tier 2B `05_Preprocessing_Alignment/processed/REL####/`; commit Git-safe `03_Datasets_Cohort/releases.csv`, `03_Datasets_Cohort/reports/REL####_manifest_summary.md`, and `01_Project_Management/reviews/G08_assessment_<date>.md`; update `gates.csv`.

**Execution procedure:**

1. Export partition-segregated prepared datasets (`train/`, `val/`, `test/` sealed separately, plus fold indices if nested CV) aligning all four modalities (`Clinical`, `ECG`, `Laboratory`, `Lifestyle`), missingness indicators, modality masks, and adjudicated outcome targets by `ENC########`.
2. Reconcile exact patient/encounter/event/modality counts across `DS#### → ADJ#### → SPLIT#### → REL####` with zero dropped or duplicated records.
3. Lock `REL####` read-only in restricted Tier 2B, compute manifest SHA-256 digests, and verify encrypted backup restoration hash.
4. Register `REL####` in `03_Datasets_Cohort/releases.csv`, verify every `G08` criterion (raw untouched, ECG fidelity passed, train-only fit verified, zero leakage), and record `G08` outcome.

**Planning/review prompt:**

> Audit `REL####` full lineage (`DS → ADJ → SPLIT → PP → REL`) against `G08` criteria. Confirm exact count reconciliation, sealed test separation, and zero unresolved schema or hash mismatches.

**Implementation prompt:**

> Materialize immutable `REL####` in restricted Tier 2B, compute full SHA-256 digests, verify read-only permissions and backup integrity, and write safe summary records into `releases.csv` and `REL####_manifest_summary.md`.

**Human-only actions and decisions:** Clinical/ECG lead and implementer certify `G08` data/preprocessing readiness; supervisor notes readiness for modeling stage `S10`.

**Version-control/artifact expectations:** Prepared clinical/ECG data arrays remain strictly in encrypted Tier 2B with verified backup; commit `releases.csv`, safe manifest hashes, and `G08` audit to Git.

**Documentation updates:** `releases.csv`, `REL####_manifest_summary.md`, `gates.csv`, `dashboard.md`.

**Verification checklist:**

- [ ] Every parent ID and SHA-256 (`DS`, `ADJ`, `variables.csv`, `SPLIT`, `PP`, `FitStateHash`) recorded in `REL####`.
- [ ] Partition counts and outcome prevalence match `SPLIT####` identically.
- [ ] Test partition stored separately with enforced custody lock.
- [ ] Encrypted backup hash verified; `G08` PASS evidenced.

**Common mistakes:** Overwriting `REL0001` after tweaking an imputer instead of creating `REL0002`; storing `train+val+test` concatenated in one unguarded file where training scripts could accidentally index test rows.

**Recovery procedure:** Quarantine invalid `REL####`, return to earliest invalid parent (`STEP-019`–`021`), create new versioned `PP`/`REL`, and re-pass `G08`.

**Definition of Done:** `G08` PASS; an immutable, leakage-free four-modality `REL####` is ready for baseline and Transformer modeling. Universal DoD applies.

**Next step:** [STEP-023](#step-023)

---

<a id="step-023"></a>
## STEP-023 — Select DL framework, four-tier baselines, and Transformer fusion architecture

**Objective:** Resolve `PyTorch` vs `TensorFlow` (`UD13`), specify the four-tier Q1 comparator suite, and design the **Transformer-based Multimodal Fusion Network** (`UD14`) tailored to observed cohort size $N$/$E$ and ECG format (`UD07`, `UD26`).

**Why this step exists:** `fydp_title_proposal.pdf` lists both TensorFlow and PyTorch (`RF08`) without selecting one, and a Q1 paper requires principled architectural justification—especially matching Transformer complexity to actual sample size and handling missing modalities natively.

**Governing section references:** [OS §6](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §11](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-022` complete; `G03` and `G08` PASS; measured $N$/$E$, ECG format, missingness profile, and available GPU/CPU compute known.

**Estimated difficulty and time (provisional):** Hard; 4–8 hours architectural design & candidate review plus supervisor approval.

**Parallelizable:** Literature architectural comparison (ECG encoders, tabular tokenizers, cross-modal fusion blocks) can run in parallel between both researchers; final `UD13–UD14` decisions are unified.

**Inputs:** `REL####` schema & dimensions, literature extraction (`STEP-007`), `RF05`, `RF08`, `UD13`, `UD14`, `UD26`.

**Expected outputs:** Populated `06_Models_Fusion/candidates.csv`, approved `06_Models_Fusion/baseline_plan.md`, architectural blueprint `06_Models_Fusion/architectures/transformer_fusion_spec.md`, pretrained-weight provenance/license audit, and `DEC####` records for `UD13–UD14`.

**Repository/file changes:** Populate `06_Models_Fusion/candidates.csv`, create `baseline_plan.md`, `architectures/transformer_fusion_spec.md`, and `01_Project_Management/decision_log/DEC####.md` (`UD13`, `UD14`).

**Execution procedure:**

1. Compare **PyTorch vs TensorFlow** (`UD13`) against exact project needs: 1D-ECG ResNet/Transformer ecosystem, native `nn.MultiheadAttention`/key-padding-mask support for missing modalities, deterministic seeding, SHAP (`GradientSHAP`/`DeepSHAP`/Captum) compatibility, and available hardware/GPU drivers.
2. Specify all **Four Comparator Tiers (`UD14`)**:
   - *Tier 1 (Unimodal):* Clinical-only, Lab-only, Lifestyle-only (Logistic Regression, Random Forest, SVM, XGBoost/LightGBM/CatBoost, MLP/FT-Transformer) + ECG-only (1D-CNN/ResNet-1D, BiLSTM/CNN-LSTM, ECG Transformer).
   - *Tier 2 (Clinical Risk Score, optional):* Framingham / WHO South Asia CVD chart / ASCVD PCE **only** if endpoint and predictors are clinically compatible.
   - *Tier 3 (Simple Multimodal Fusion):* Early concatenation (tabular + extracted/learned ECG embeddings → XGBoost & MLP), Late probability ensemble/stacking, Gated/Attention fusion.
   - *Tier 4 (Proposed Transformer Multimodal Fusion):* Dedicated lightweight modality encoders (Clinical, Lab, Lifestyle tabular tokenizers/MLPs + 1D-CNN/Patch ECG encoder, optionally initialized from licensed pretrained ECG representations under `UD26` if $N$ is modest) → shared $d$-dim projection with modality-type embeddings → cross-modal Transformer encoder layers with **missing-modality key-padding masking / learnable `[MISSING]` tokens** → pooled risk head.
3. Audit parameter counts relative to observed EPV (`UD26`) to avoid massive overparameterization; check exact licenses and dataset-overlap risk of any pretrained ECG encoder weights.
4. Record chosen architecture, rejected alternatives, and verify whether any required ECG/tabular input shape requires returning to `STEP-019`–`022` for a new `REL####`.

**Planning/review prompt:**

> Compare PyTorch vs TensorFlow and design our four-tier Q1 baseline suite + Transformer-based Multimodal Fusion Network given exact `REL####` dimensions, ECG format, and observed sample size $N$/$E$. Justify parameter capacity, missing-modality attention masking, and fair comparison parity across classical ML and deep models.

**Implementation prompt:**

> Documentation & architecture specs only: populate `06_Models_Fusion/candidates.csv`, `baseline_plan.md`, and `architectures/transformer_fusion_spec.md` with exact tensor shapes, licenses, and rejected alternatives. Do not download unapproved weights or write ad-hoc training code yet.

**Human-only actions and decisions:** Supervisor and researchers approve framework (`UD13`), four-tier baseline hierarchy, clinical risk-score eligibility, and Transformer fusion specification (`UD14`).

**Version-control/artifact expectations:** Commit architecture specs, `candidates.csv`, and `DEC####`; any approved pretrained weights live in Tier 3 storage with SHA-256 and license proof.

**Documentation updates:** `candidates.csv`, `baseline_plan.md`, `transformer_fusion_spec.md`, `decisions.csv` (`UD13`, `UD14`).

**Verification checklist:**

- [ ] Single DL framework (PyTorch or TensorFlow) formally selected with documented rationale.
- [ ] All proposal model families (LR, RF, SVM, XGBoost, CNN, LSTM, Transformer) plus early/late fusion covered in Tiers 1–4.
- [ ] Transformer fusion specifies exact tensor shapes, parameter count vs EPV, and missing-modality masking mechanism.
- [ ] Pretrained weight origins/licenses audited (or training-from-scratch explicitly chosen); any data-shape change routed cleanly via `G08`.

**Common mistakes:** Building a 50-million-parameter Transformer for 500 hospital patients; forgetting simple Early-Concatenation + XGBoost and Late-Ensemble baselines (guaranteed Q1 reviewer objection!); omitting missing-modality masking.

**Recovery procedure:** Downsize Transformer depth/width or adopt vetted pretrained ECG encoders (`UD26`), record a superseding `DEC####`, and update `transformer_fusion_spec.md` before environment locking.

**Definition of Done:** Approved framework, four-tier Q1 baseline suite, and Transformer fusion architectural specification logged. Universal DoD applies.

**Next step:** [STEP-024](#step-024)

---

<a id="step-024"></a>
## STEP-024 — Pin and verify the modeling, statistics, and XAI runtime (`environment/model/`)

**Objective:** Build, pin, and smoke-test the deep learning, GBDT, statistical inference, calibration, and SHAP environment under `environment/model/` while preserving the earlier `environment/data/` lock untouched.

**Why this step exists:** Unpinned CUDA/cuDNN, PyTorch/TensorFlow, Scikit-learn, XGBoost, or SHAP versions break exact checkpoint restoration, alter numerical calibration, and fail clean reproducibility audits (`G15`).

**Governing section references:** [OS §6](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §9](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §11](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-023` framework & baseline selection (`UD13–UD14`); approved PHI-compliant compute hardware available; `environment/data/` preserved.

**Estimated difficulty and time (provisional):** Moderate to hard; 3–6 hours depending on GPU/CUDA compatibility.

**Parallelizable:** Documentation and PHI-compliance checks on the compute host may accompany dependency resolution; verification is sequential.

**Inputs:** Chosen framework (`UD13`), baseline/SHAP/stats dependencies (Scikit-learn, XGBoost/LightGBM/CatBoost, SHAP, SciPy, Statsmodels, PyTorch/TF), actual hardware specs, preserved `environment/data/` lock.

**Expected outputs:** Pinned `environment/model/` lock file (`requirements.lock` / `environment.yml`), `environment/model/versions.md` (OS, Python, GPU, driver, CUDA/cuDNN, library versions), import/GPU/SHAP smoke verification log, and updated `13_Documentation/installation.md`.

**Repository/file changes:** Populate `environment/model/` lock & `versions.md`; update `13_Documentation/installation.md`. Keep `environment/data/` unmodified.

**Execution procedure:**

1. Confirm compute hardware complies with `UD05` IRB/hospital data-location restrictions (never stage restricted hospital clinical/ECG data on an unapproved third-party server!).
2. Create a clean virtual/conda environment for `environment/model/` installing exact pinned versions of the chosen DL framework, Scikit-learn, XGBoost/GBDT, SciPy/Statsmodels, SHAP (plus optional LIME/Captum), Matplotlib/Seaborn, and pytest.
3. Run synthetic smoke tests verifying GPU/CPU tensor execution, deterministic seed behavior, GBDT training, calibration/DeLong/bootstrap math, and neural SHAP gradient hooks on dummy 4-modality inputs.
4. Export full pinned dependency freeze, verify clean re-installation instructions, and confirm whether any shared package differs from `environment/data/` (never silently altering `REL####` without re-verifying `G08`).

**Planning/review prompt:**

> Verify `environment/model/` dependency compatibility across the chosen DL framework, SHAP neural explainers, GPU drivers, and statistical libraries, confirming full compliance with IRB compute-location limits.

**Implementation prompt:**

> Construct and freeze `environment/model/`, execute synthetic GPU/CPU, GBDT, and SHAP smoke checks, and record exact observed OS, driver, CUDA, and package versions in `environment/model/versions.md`. Never fabricate GPU specs.

**Human-only actions and decisions:** Researchers approve final compute platform/budget and confirm IRB data-residency compliance (`UD13`).

**Version-control/artifact expectations:** Commit lock files, `versions.md`, and `installation.md`; exclude virtualenvs, caches, and credentials.

**Documentation updates:** `environment/model/versions.md`, `13_Documentation/installation.md`, `decisions.csv` (`UD13`).

**Verification checklist:**

- [ ] Observed OS, CPU/GPU, driver, CUDA/cuDNN, and exact package versions logged.
- [ ] Synthetic forward/backward pass, GBDT fit, and SHAP neural explainer verified.
- [ ] `environment/data/` preserved untouched; compute host confirmed IRB-compliant.
- [ ] Environment recreation steps tested or exact constraints documented.

**Common mistakes:** Relying on an ephemeral unpinned cloud notebook runtime; failing to test `shap.GradientExplainer`/`DeepExplainer` compatibility with the exact PyTorch/TF version before building the model.

**Recovery procedure:** Resolve version conflicts cleanly (especially SHAP vs DL framework compatibility), recreate lock, re-test synthetic smoke suite, and log changes transparently.

**Definition of Done:** Tested, pinned, IRB-compliant `environment/model/` runtime ready for pipeline implementation. Universal DoD applies.

**Next step:** [STEP-025](#step-025)

---

<a id="step-025"></a>
## STEP-025 — Approve prospective Q1 experiment, evaluation, calibration, stats, and XAI protocols

**Objective:** Preregister every controlled experiment/ablation row, multi-seed rule, validation-only calibration & threshold policy, statistical comparison plan, and quantitative SHAP faithfulness/stability/clinician-review protocol (`UD15–UD21`, `UD24`) before training.

**Why this step exists:** Deciding ablations, operating thresholds, calibrators, DeLong comparisons, or SHAP perturbation metrics *after* viewing results introduces post-hoc bias that Q1 peer reviewers immediately challenge.

**Governing section references:** [OS §6](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §7](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §8](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-08); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-023–024` complete; `G03` and `G08` current PASS; `REL####` size and runtime speed profile understood.

**Estimated difficulty and time (provisional):** Hard; 5–8 hours plus supervisor, biostatistics, and cardiologist review.

**Parallelizable:** Experiment matrix (`07_Experiments/`), statistical/calibration protocol (`09_Evaluation_Stats/`), and XAI faithfulness/plausibility protocol (`10_Explainability_XAI/`) can be drafted concurrently and reconciled together.

**Inputs:** Approved RQs (`STEP-009`), `baseline_plan.md`, `transformer_fusion_spec.md`, `REL####`, `UD15–UD21`, `UD24`.

**Expected outputs:** Approved `07_Experiments/experiment_plan.md` (Blocks A–F), `09_Evaluation_Stats/protocol.md`, `10_Explainability_XAI/xai_protocol.md`, expanded executable `T32` config schema, and `DEC####` records resolving `UD15–UD21` and `UD24`.

**Repository/file changes:** Create `07_Experiments/experiment_plan.md`, `09_Evaluation_Stats/protocol.md`, `10_Explainability_XAI/xai_protocol.md`, finalize `T32` YAML validator schema, and update `decisions.csv`.

**Execution procedure:**

1. Finalize **Controlled Experiment Matrix (`experiment_plan.md`, `UD15`)**: enumerate Blocks A–F (Tier 1 unimodals across all 4 modalities, Tier 2 clinical score if adopted, Tier 3 simple early/late/gated fusion, Tier 4 Transformer fusion, progressive modality addition, Leave-One-Modality-Out, architectural ablations, incorporation-bias sensitivity, and missing-modality stress tests), setting matched validation tuning budgets, fixed multi-seed count ($S \ge 3$–$5$), loss/imbalance rules, and early-stopping validation monitor.
2. Finalize **Evaluation, Calibration & Statistical Protocol (`09_Evaluation_Stats/protocol.md`, `UD16–UD18`, `UD24`)**: lock all 6 mandatory proposal metrics + adopted Q1 metrics (PR-AUC, Specificity, NPV, Balanced Accuracy/MCC, Brier, ECE, calibration slope/intercept), validation-only operating threshold rule ($\tau$) and post-hoc calibrator candidates, DCA clinical threshold range (confirmed with cardiologist), bootstrap repetitions ($B \ge 1{,}000$, patient-level stratified), paired DeLong / bootstrap / McNemar tests, Holm-Bonferroni/FDR multiplicity control, and subgroup strata (sex, age, site, modality tier).
3. Finalize **Multimodal XAI Protocol (`10_Explainability_XAI/xai_protocol.md`, `UD19–UD21`)**: pin exact SHAP algorithm(s) per model family, training-only stratified background size/seed, additivity tolerance, tabular + ECG + modality-share aggregation formulas, deletion/insertion AOPC perturbation baseline & random-control design, multi-seed rank-correlation metrics ($\rho$, Top-$k$ Jaccard), shortcut audit triggers, and cardiologist plausibility review rubric (`UD21`, explicitly confirming whether a separate IRB reader study is excluded).
4. Expand `T32` YAML config schema to cover every effective parameter of the selected framework and baselines so missing values fail validation before launch.

**Planning/review prompt:**

> Audit `experiment_plan.md`, `09_Evaluation_Stats/protocol.md`, and `10_Explainability_XAI/xai_protocol.md` as a hostile Q1 *IEEE JBHI* / *npj Digital Medicine* reviewer. Flag any unfair baseline budget, undefined threshold/calibration rule, unadjusted multiple comparisons, or non-quantitative SHAP design.

**Implementation prompt:**

> Save approved protocol documents, expand `T32` YAML schema, and record SHA-256 hashes of all three frozen planning protocols prior to any training execution. Record actual `UD15–UD21`/`UD24` decisions only.

**Human-only actions and decisions:** Supervisor, biostatistics reviewer, and cardiologist ratify `UD15–UD21` and `UD24` (DCA threshold range, clinical operating rule, cardiologist XAI rubric, multiplicity correction, and multi-seed budget).

**Version-control/artifact expectations:** Commit timestamped pre-training protocols (`exp: lock prospective Q1 experiment, evaluation, statistical and XAI protocols`); subsequent changes require explicit versioned amendments distinguishing prospective vs exploratory work.

**Documentation updates:** `experiment_plan.md`, `09_Evaluation_Stats/protocol.md`, `10_Explainability_XAI/xai_protocol.md`, `decisions.csv`.

**Verification checklist:**

- [ ] Every planned experiment block directly maps to approved RQs and uses matched fair budgets/seeds.
- [ ] All 6 mandatory metrics + Q1 calibration, DCA, bootstrap CIs, DeLong/McNemar, and multiplicity adjustments fully specified.
- [ ] Operating threshold and post-hoc calibration explicitly restricted to validation/OOF only.
- [ ] Quantitative XAI faithfulness (AOPC vs random control), stability, shortcut audit, and cardiologist rubric preregistered with training-only background rule.

**Common mistakes:** Leaving baseline tuning vague while extensively tuning the Transformer; omitting multiple-testing correction across 10+ baseline comparisons; designing SHAP without a training-only background set or deletion/insertion control.

**Recovery procedure:** Resolve any unspecified setting before `G09`; log any later unavoidable amendment transparently without falsely claiming preregistration.

**Definition of Done:** Complete, human-ratified Q1 experiment, evaluation, calibration, statistical, and XAI protocols ready for pipeline engineering. Universal DoD applies.

**Next step:** [STEP-026](#step-026)

---

<a id="step-026"></a>
## STEP-026 — Implement configuration-driven multimodal pipeline, evaluator, and XAI modules

**Objective:** Build clean, modular, configuration-driven code in `src/cvd_mm/` for 4-modality data loading, Tier 1–4 models, calibration, statistical evaluation, and SHAP faithfulness with rigorous synthetic unit tests.

**Why this step exists:** Ad-hoc notebooks hide hyperparameters, silently mix validation/test indices, compute buggy calibration/DeLong/AOPC formulas, and fail reproducibility audits.

**Governing section references:** [OS §2](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-02); [OS §6](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §7](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §8](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-08); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-025` approved protocols & expanded `T32` schema; `STEP-024` `environment/model/` verified; `G08` `REL####` available.

**Estimated difficulty and time (provisional):** Hard; 2–4 focused development days split across loaders, models, evaluator/stats, and XAI hooks.

**Parallelizable:** Tabular/ECG data loaders + Tier 1–4 model modules can be built in parallel with evaluation/calibration/DeLong/DCA and SHAP faithfulness modules against agreed tensor/prediction schemas.

**Inputs:** `transformer_fusion_spec.md`, `experiment_plan.md`, `09_Evaluation_Stats/protocol.md`, `10_Explainability_XAI/xai_protocol.md`, `T32` schema, `REL####` manifest contract.

**Expected outputs:** Tested `src/cvd_mm/` modules (`config.py`, `dataset.py`, `models/`, `train.py`, `calibrate.py`, `metrics.py`, `stats.py`, `xai.py`), thin CLI dispatchers in `14_Automation/`, comprehensive pytest suite on synthetic 4-modality fixtures, and updated `13_Documentation/pipeline.md`.

**Repository/file changes:** Populate `src/cvd_mm/`, `tests/test_config.py`, `test_models.py`, `test_metrics_stats.py`, `test_xai_faithfulness.py`, `14_Automation/` thin CLIs, and update `13_Documentation/pipeline.md`.

**Execution procedure:**

1. Build strict config & manifest validator (`config.py`, `dataset.py`) enforcing `REL`/`SPLIT`/`PP`/`variables.csv` SHA-256 checks, zero unresolved `null` values, active modality masking, and hard runtime failure if final-test indices are accessed outside frozen evaluation mode.
2. Implement Tier 1 unimodal wrappers (LR, RF, SVM, XGBoost/GBDT, MLP/1D-CNN/BiLSTM/ECG-Transformer), Tier 3 simple fusion models, and Tier 4 **Transformer-based Multimodal Fusion Network** with unit-tested missing-modality key-padding masking (verifying zero `NaN` outputs when any subset of 1–3 modalities is masked!).
3. Implement `calibrate.py`, `metrics.py`, and `stats.py` computing all 6 mandatory metrics, PR-AUC, Specificity/NPV, Brier/ECE/calibration slope & intercept, DCA net benefit, patient-level stratified bootstrap CIs, paired DeLong test, McNemar test, and Holm-Bonferroni/FDR adjustments—verifying every formula against exact analytical/known synthetic test cases!
4. Implement `xai.py` supporting training-only background sampling, TreeSHAP & neural Transformer SHAP, additivity-error check, modality-share aggregation, ECG segment/feature mapping, and deletion/insertion AOPC vs random-control curves—verified on a synthetic dataset with known ground-truth informative vs noise features!

**Planning/review prompt:**

> Review `src/cvd_mm/` interfaces and unit-test designs for subtle bugs: test-set guardrails, missing-modality Transformer masking (`NaN` safety), DeLong variance math, calibration-slope edge cases, and synthetic ground-truth verification of SHAP faithfulness (AOPC).

**Implementation prompt:**

> Implement the modular `src/cvd_mm/` package, thin `14_Automation/` CLIs, and pytest suite using synthetic 4-modality fixtures only. Keep all scientific settings in YAML configs and assert zero final-test data reads.

**Human-only actions and decisions:** Method and evaluation reviewers inspect known-case metric/DeLong/AOPC test outputs before approving readiness.

**Version-control/artifact expectations:** Commit clean code, synthetic fixtures, and passing pytest logs; zero real patient data or checkpoints in Git.

**Documentation updates:** `13_Documentation/pipeline.md` (CLI commands & schemas), test coverage summary.

**Verification checklist:**

- [ ] Config validator rejects `null` fields, hash mismatches, and unsealed test-set calls.
- [ ] Transformer fusion passes missing-modality masking tests (0, 1, 2, or 3 modalities missing without `NaN`).
- [ ] Known-case tests verify all 6 mandatory metrics, PR-AUC, Brier/ECE/slope, DCA, DeLong, and bootstrap CIs.
- [ ] Synthetic ground-truth feature test confirms SHAP assigns highest importance to true signal features and deletion AOPC beats random control.

**Common mistakes:** Softmaxing all-masked Transformer attention rows into `NaN`; using default `roc_auc_score` without checking binary vs multi-class probability shape; testing SHAP only visually without verifying additivity and synthetic ground-truth recovery.

**Recovery procedure:** Fix failing modules/tests, trace discrepancies against analytical synthetic expectations, and re-run full pytest suite before `STEP-027`.

**Definition of Done:** Modular, configuration-driven multimodal training, calibration, statistical evaluation, and SHAP faithfulness pipeline passes all synthetic unit tests. Universal DoD applies.

**Next step:** [STEP-027](#step-027)

---

<a id="step-027"></a>
## STEP-027 — Execute diagnostic smoke test, checkpoint recovery check, and pass `G09`

**Objective:** Prove end-to-end training, validation, checkpoint interruption/exact-resume recovery, backup retrieval, and SHAP hook execution on a tiny training/validation slice—and pass `G09`.

**Why this step exists:** Discovering broken ECG batching, silent GPU OOMs, missing optimizer state on resume, or corrupted artifact storage halfway through a multi-seed ablation wastes days and compromises comparability.

**Governing section references:** [OS §6](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §11](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-026` unit tests passing; `G08` current PASS; `environment/model/` locked; Tier 3 artifact storage ready.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours including smoke execution and simulated interruption/restore.

**Parallelizable:** `checkpoint_policy.md` drafting may accompany smoke runs; restore verification waits for generated checkpoint.

**Inputs:** Tiny training & validation slice of `REL####` (ZERO final-test access!), approved baseline & Transformer configs, `T18` (`checkpoint.md`).

**Expected outputs:** `08_Checkpoints/checkpoint_policy.md`, prospectively labeled diagnostic smoke `EXP` (`EXP0000_SMOKE` / clearly tagged diagnostic), verified checkpoint interruption/restore & backup SHA-256 proof, SHAP hook sanity check, and `G09` assessment.

**Repository/file changes:** Create `08_Checkpoints/checkpoint_policy.md`, diagnostic smoke bundle under `07_Experiments/`, smoke `CKPT` manifest under `08_Checkpoints/manifests/`, and `01_Project_Management/reviews/G09_assessment_<date>.md`; update `gates.csv`.

**Execution procedure:**

1. Write `08_Checkpoints/checkpoint_policy.md` specifying immutable `CKPT####` naming, state payload (weights, optimizer, scheduler, AMP scaler, epoch/step, RNG states), retention, and Tier 3 backup cadence.
2. Launch a prospectively labeled diagnostic smoke run of one tabular baseline (XGBoost) and the **Transformer Multimodal Fusion** model on a small Train/Val slice (confirming 4-modality loading, missing-modality masks, finite losses/gradients, validation metric logging, and zero final-test reads).
3. Deliberately interrupt the Transformer smoke run mid-epoch/between epochs, fetch the checkpoint from Tier 3 backup, verify its SHA-256, restore full state in the exact environment, resume training, and log exact continuity (documenting honestly if GPU nondeterminism limits bitwise resume).
4. Smoke-test calibration fitting and neural SHAP additivity on the tiny smoke checkpoint (diagnostic only—never reportable results!), confirm all `G09` criteria, and record supervisor + method reviewer sign-off.

**Planning/review prompt:**

> Audit `G09` readiness across runtime locks, prospective Q1 protocols, unit tests, diagnostic smoke execution, and checkpoint interruption/restore evidence. Flag any exact-resume limitation or unresolved config parameter.

**Implementation prompt:**

> Execute the labeled diagnostic smoke run and interruption/restore drill on Train/Val slice only, verify Tier 3 backup hash retrieval, confirm zero test-partition access, and record actual output in `G09` evidence files.

**Human-only actions and decisions:** Supervisor and method/evaluation reviewer verify all `G09` criteria (`UD13–UD21`, `UD24` resolved; runtime/recovery proven) and sign `G09` PASS.

**Version-control/artifact expectations:** Commit `checkpoint_policy.md`, safe diagnostic logs, and `G09` audit; keep smoke binaries in Tier 3 clearly tagged diagnostic.

**Documentation updates:** `checkpoint_policy.md`, `checkpoint_registry.csv`, `gates.csv`, `dashboard.md`.

**Verification checklist:**

- [ ] Diagnostic smoke runs succeed for classical baseline and 4-modality Transformer on Train/Val only.
- [ ] Deliberate interruption, backup SHA-256 retrieval, and state restoration verified with continuity log.
- [ ] Diagnostic SHAP additivity & calibrator pipeline execute cleanly without error.
- [ ] `G09` PASS signed; test-access log verified completely untouched.

**Common mistakes:** Calling a failed full experiment a "smoke test" after the fact; assuming `model.state_dict()` alone restores optimizer/scheduler/RNG state; touching final test data during smoke testing.

**Recovery procedure:** Preserve diagnostic failure logs (`T15`), fix loader/checkpoint/SHAP bugs, re-run synthetic & smoke drills cleanly, and re-audit `G09`.

**Definition of Done:** `G09` PASS; pipeline, checkpoint recovery, and prospective Q1 protocols verified ready for full controlled experimentation. Universal DoD applies.

**Next step:** [STEP-028](#step-028)

---

<a id="step-028"></a>
## STEP-028 — Register and validate an immutable experiment bundle (`EXP####`)

**Objective:** Create a fully resolved, hash-verified, immutable `EXP####` package tied to a specific row of the approved Q1 experiment matrix before launching compute.

**Why this step exists:** Fair comparison across unimodal, simple-fusion, Transformer, and ablation runs collapses unless every launched configuration is frozen and validated prior to execution.

**Governing section references:** [OS §6](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §11](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-027` complete; `G08–G09` current PASS; approved row in `07_Experiments/experiment_plan.md` (and `STEP-031` authorization for matrix iterations).

**Estimated difficulty and time (provisional):** Moderate; 0.5–1.5 hours per experiment bundle.

**Parallelizable:** Preparing multiple independent `EXP####` configs is parallelizable; sequential `EXP####` ID assignment in `experiment_registry.csv` is serialized.

**Inputs:** Approved `experiment_plan.md` row, `REL####`/`MC####` IDs, resolved `T32` YAML config, Git commit hash, Tier 3 destination.

**Expected outputs:** Immutable `07_Experiments/EXP####/config.yaml`, `README.md` (`T16`), `run_manifest.json`, validated config SHA-256, and registered `experiment_registry.csv` entry.

**Repository/file changes:** Create `07_Experiments/EXP####/config.yaml`, `README.md`, `run_manifest.json`; update `07_Experiments/experiment_registry.csv`.

**Execution procedure:**

1. Assign the next sequential `EXP####` ID linking its exact RQ, Comparison Block (`A–F`), Comparator Tier (`1–4`), parent baseline `EXP`, active modality mask (`Clinical`, `ECG`, `Lab`, `Lifestyle`), and fixed seed.
2. Populate `config.yaml` resolving 100% of effective fields—data hashes, encoder hyperparameters, fusion config, imbalance loss, tuning space/budget, early-stopping monitor, and runtime—leaving zero `null` executable fields.
3. Run `src/cvd_mm/config.py` validator verifying parent `REL`/`PP`/`SPLIT`/`variables.csv` SHA-256 matches, clean Git commit (or explicitly recorded diff), zero test-partition references, and adequate Tier 3 storage quota.
4. Commit the pre-launch `EXP####` metadata bundle and authorize launch.

**Planning/review prompt:**

> Audit `EXP####/config.yaml` against `experiment_plan.md` and fair-comparison invariants. Verify exact changed vs fixed factors, active modality flags, matched seed/budget, and zero test leakage.

**Implementation prompt:**

> Generate immutable `07_Experiments/EXP####/` metadata files, run automated config/hash validation, and register `Status=READY` in `experiment_registry.csv`. Never launch an experiment whose validator fails.

**Human-only actions and decisions:** Experiment lead authorizes launch of the approved matrix row; supervisor approves any planned deviation.

**Version-control/artifact expectations:** Commit pre-launch `EXP####` metadata before training; never edit `config.yaml` once launched (any change requires a brand-new `EXP####`).

**Documentation updates:** `07_Experiments/EXP####/README.md`, `experiment_registry.csv`, `dashboard.md`.

**Verification checklist:**

- [ ] Automated validator passed with zero unresolved fields and exact `REL`/`PP`/`SPLIT` hash matches.
- [ ] Active modality mask, comparator tier, parent baseline, and seed explicitly logged.
- [ ] `G08–G09` gates verified current (not `STALE`).
- [ ] Zero references to sealed final test data.

**Common mistakes:** Passing ad-hoc CLI overrides (`--lr 1e-4`) that contradict `config.yaml`; accidentally running a new Transformer on `REL0002` while comparing against an XGBoost baseline trained on `REL0001`.

**Recovery procedure:** Fix pre-launch bundle and re-validate; if already launched with a bug, preserve the flawed `EXP####` permanently and register a new `EXP####`.

**Definition of Done:** Validated, immutable `EXP####` bundle registered and authorized for training. Universal DoD applies.

**Next step:** [STEP-029](#step-029)

---

<a id="step-029"></a>
## STEP-029 — Train registered experiment on train/validation only and preserve every attempt

**Objective:** Execute the locked `EXP####` training/validation run (or inner CV loop) with continuous durable logging, checkpointing, and preservation of all outcomes including failures.

**Why this step exists:** Transparent Q1 methodology requires exact learning curves, stopping records, and complete visibility into failed, diverged, or overfit attempts.

**Governing section references:** [OS §6](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §11](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS §13](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-028` validated `EXP####` ready; `G08–G09` current PASS; IRB-compliant compute available.

**Estimated difficulty and time (provisional):** Hard; 1–2 hours monitoring per session plus actual GPU/CPU training duration (depends on cohort size & ECG architecture).

**Parallelizable:** Independent registered `EXP####` runs (e.g., distinct seeds or unimodal baselines) may execute in parallel if hardware permits; never share output folders or touch final test data.

**Inputs:** Frozen `EXP####/config.yaml`, `REL####` Train/Val partitions only, locked `environment/model/`, Tier 3 checkpoint destination.

**Expected outputs:** `RUN####` execution records, complete epoch/step train & validation curves (loss, ROC-AUC, PR-AUC, Brier), immutable `CKPT####` artifacts in Tier 3, validation predictions, and actual termination/failure state.

**Repository/file changes:** Populate `07_Experiments/EXP####/` logs, learning-curve CSVs, `run_manifest.json`, observations/failure reports (`T15`), and append `08_Checkpoints/checkpoint_registry.csv`; store checkpoint binaries strictly in Tier 3.

**Execution procedure:**

1. Re-verify `environment/model/` lock, code commit, `config.yaml` hash, and `REL####` hashes at runtime; dump complete effective library settings into `run_manifest.json`.
2. Execute training strictly on Training data (or inner-CV training folds) and evaluate exclusively on Validation data (or inner-CV validation folds), persisting learning curves, GPU/memory stats, and immutable `CKPT####` objects continuously to Tier 3 storage.
3. If interrupted (OOM, power/timeout), restore strictly from a hash-verified checkpoint under a linked `RUN####` (or launch a new `EXP####` if exact resume is unsupported or any setting changes).
4. Record exact stopping reason (`early_stopping_patience`, `max_epochs`, `converged`, `oom`, `nan_divergence`), verify SHA-256 digests of transferred Tier 3 checkpoints and validation OOF predictions before closing the compute session.

**Planning/review prompt:**

> Review the launch and interruption runbook for `EXP####`. Specify monitored overfitting/divergence alerts, Tier 3 persistence cadence, and required evidence before shutting down compute.

**Implementation prompt:**

> Launch `14_Automation/train.py --config 07_Experiments/EXP####/config.yaml` using `environment/model/`. Log effective settings, every epoch metric, warnings, and exact stopping reasons; never alter hyperparameters silently mid-run or access test indices.

**Human-only actions and decisions:** Experiment lead monitors anomalies and approves safety aborts; any hyperparameter/architecture adjustment requires a brand-new `EXP####` via `STEP-028`.

**Version-control/artifact expectations:** Checkpoint binaries and restricted per-patient validation predictions go to Tier 3/2B with SHA-256 backups; commit safe aggregate logs, curves, and `run_manifest.json` to Git.

**Documentation updates:** `EXP####/run_manifest.json`, `EXP####/README.md`, `checkpoint_registry.csv`, `failure_report.md` (if failed).

**Verification checklist:**

- [ ] Runtime effective settings match frozen `EXP####/config.yaml` exactly.
- [ ] Training and validation partitions only; zero final-test access logged.
- [ ] All epochs, stopping reason, and Tier 3 checkpoint SHA-256 hashes durably saved.
- [ ] Any failed/diverged/OOM attempt fully preserved rather than deleted.

**Common mistakes:** Leaving sole checkpoints in ephemeral cloud scratch disks; lowering batch size silently after an OOM without assigning a new `EXP####`; discarding low-AUC runs.

**Recovery procedure:** Log `T15` failure report, verify last uncorrupted backup checkpoint for exact resume if valid, or open a new `EXP####` with adjusted settings while retaining the failed record permanently.

**Definition of Done:** `EXP####` reaches a documented stop or failure with durable logs and hash-verified checkpoints ready for eligibility audit. Universal DoD applies.

**Next step:** [STEP-030](#step-030)

---

<a id="step-030"></a>
## STEP-030 — Audit run completion, register candidate model (`MODEL####`), and pass `G10`

**Objective:** Verify technical validity, checkpoint reload integrity, and full provenance of a completed `EXP####`, register its eligible validation-selected `MODEL####` card, and pass `G10`.

**Why this step exists:** A saved weight file without verified stopping compliance, config integrity, and reload equivalence cannot enter Q1 validation selection.

**Governing section references:** [OS §6](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-029` stopped with complete logs and Tier 3 checkpoints; original `EXP####` config and `REL####` hashes intact.

**Estimated difficulty and time (provisional):** Moderate; 1.5–3 hours per qualifying `EXP####`.

**Parallelizable:** Checkpoint hash/reload verification and `MODEL####` card drafting can proceed concurrently; `G10` sign-off requires both.

**Inputs:** `EXP####` logs & `run_manifest.json`, `CKPT####` manifests, validation metrics, `T17` (`model_card.md`).

**Expected outputs:** Audited `EXP####` conclusion (or preserved failure classification), verified reload proof, registered `MODEL####` & `06_Models_Fusion/cards/MODEL####.md` (if eligible), and per-EXP `G10` assessment.

**Repository/file changes:** Update `experiment_registry.csv`, `checkpoint_registry.csv`, `06_Models_Fusion/model_registry.csv`, write `06_Models_Fusion/cards/MODEL####.md`, `EXP####/README.md` conclusion, and `01_Project_Management/reviews/G10_EXP####_assessment_<date>.md`; update `gates.csv`.

**Execution procedure:**

1. Reconcile full training/validation logs, epoch counts, effective config hash, stopping criterion, and all `RUN####` attempts (confirming no silent alteration or missing epochs).
2. Reload the best validation checkpoint (`CKPT####`) from Tier 3 in read-only mode, verify its SHA-256 and deterministic reproduction of saved validation predictions within numeric tolerance, and verify backup availability.
3. For technically valid completed runs, register `MODEL####` with complete lineage (`EXP`, `RUN`, `CKPT`, `REL`, `PP`, `FitStateHash`, parameter count, modality requirements, intended research use) and author `06_Models_Fusion/cards/MODEL####.md`.
4. Assess `G10` strictly on execution validity (NOT on whether validation AUC beat another model!): mark valid completed runs `G10 PASS` and keep invalid/aborted runs documented as ineligible.

**Planning/review prompt:**

> Audit `EXP####` against `G10` mandatory criteria. Distinguish technically valid low-performing experiments (eligible for honest reporting) from invalid/incomplete executions (ineligible).

**Implementation prompt:**

> Run automated reload-parity and hash checks against Tier 3 `CKPT####`, populate `model_registry.csv` and `MODEL####.md`, and save evidenced `G10` review without altering historical metrics or configs.

**Human-only actions and decisions:** Experiment reviewer signs off `G10` eligibility for `EXP####`; researchers document observed validation tradeoffs honestly.

**Version-control/artifact expectations:** Commit safe registry updates, `MODEL####.md`, and `G10` review; keep checkpoint binaries immutable in Tier 3.

**Documentation updates:** `experiment_registry.csv`, `model_registry.csv`, `checkpoint_registry.csv`, `gates.csv`.

**Verification checklist:**

- [ ] Logs, config hash, and stopping criterion reconcile across every `RUN####`.
- [ ] `CKPT####` reload reproduces saved validation predictions and matches Tier 3 SHA-256.
- [ ] `MODEL####` card documents exact modality dependencies, parameter count, and clinical exclusions.
- [ ] `G10` PASS recorded per qualifying `EXP####`; failed attempts preserved honestly.

**Common mistakes:** Dropping a valid unimodal or Transformer run because validation AUC was lower than hoped; registering a checkpoint without verifying it reloads cleanly.

**Recovery procedure:** Restore missing checkpoint from verified Tier 3 backup; if genuinely unrecoverable, classify `EXP####` ineligible (`G10 FAIL`) and run a brand-new `EXP####` via `STEP-028` without fabricating continuity.

**Definition of Done:** `EXP####` fully accounted for; qualifying candidate holds `G10 PASS` and complete `MODEL####` provenance. Universal DoD applies.

**Next step:** [STEP-031](#step-031)

---

<a id="step-031"></a>
## STEP-031 — Execute complete controlled Q1 experiment, baseline, and ablation matrix

**Objective:** Run and audit all approved comparison blocks (`A–F` from `STEP-025`) across all four comparator tiers, progressive & Leave-One-Modality-Out ablations, architectural ablations, and multi-seed repeats via `STEP-028`–`030` on Train/Validation only.

**Why this step exists:** Q1 publication depends on rigorous, fair, multi-seed evidence comparing the Transformer Multimodal Fusion Network against strong unimodal models, simple early/late fusion baselines, clinical risk scores (if compatible), and controlled modality ablations.

**Governing section references:** [OS §6](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §7](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §13](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-13); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** First baseline `STEP-030` `G10 PASS`; approved `experiment_plan.md` Blocks A–F; `G08–G09` current PASS; compute budget tracked.

**Estimated difficulty and time (provisional):** Hard; repeatable cycles of 2–4 hours planning/auditing per comparison block plus measured compute time (typically 1–3 weeks depending on GPU availability and nested CV).

**Parallelizable:** Independent approved `EXP####` runs (e.g., Block A unimodals, Block C fusion baselines, Block D LOMO ablations, distinct seeds) may run concurrently; serialize `experiment_registry.csv` and `model_registry.csv` merges.

**Inputs:** `experiment_plan.md` Blocks A–F, `REL####`, baseline validation benchmarks, `UD14–UD15`.

**Expected outputs:** Completed `G10 PASS` records across all planned Blocks A–F (or prospectively approved dispositions), complete validation-only multi-seed comparison tables (mean ± SD ROC-AUC, PR-AUC, F1, Brier), ablation curves, and matrix-completion audit.

**Repository/file changes:** Repeat `STEP-028`–`030` creating sequential `EXP####` & `MODEL####` artifacts; write `07_Experiments/validation_matrix_summary.md` and update `experiment_plan.md`, `experiment_registry.csv`, `model_registry.csv`.

**Execution procedure:**

1. Execute **Block A (Unimodal Baselines):** Clinical-only, Lab-only, Lifestyle-only (LR, RF, SVM, XGBoost/GBDT, MLP/FT-Transformer) and ECG-only (1D-CNN/ResNet-1D, BiLSTM/CNN-LSTM, ECG Transformer) with fair validation-only hyperparameter tuning and multi-seed runs.
2. Execute **Block B (Clinical Risk Score, if adopted)** and **Block C (Multimodal Fusion Benchmarks):** Early concatenation (XGBoost & MLP), Late calibrated probability ensemble, Gated fusion, and Proposed **Transformer-based Multimodal Fusion Network** across all $S$ fixed seeds.
3. Execute **Block D (Modality Ablations — directly testing `PG1`, `PG2`, `PG4`):** Progressive addition (`Clinical → +Lab → +Lifestyle → +ECG` and `Clinical+ECG → +Lab → +Lifestyle`) and Leave-One-Modality-Out (4-modality minus each modality in turn).
4. Execute **Block E (Architectural Ablations)** (cross-modal attention vs simple concatenation, with vs without missing-modality masking, raw ECG encoder vs tabular ECG intervals if both exist) and **Block F (Sensitivity Runs)** (incorporation-bias exclusion check if flagged in `STEP-014`; validation missing-modality dropout check), then consolidate `validation_matrix_summary.md` retaining 100% of seeds, negative findings, and failed runs—strictly WITHOUT touching final test data!

**Planning/review prompt:**

> Audit our completed validation matrix (`Blocks A–F`) for comparison fairness, multi-seed completeness, confounded ablations, and evidence of validation overfitting. Confirm zero final-test data was accessed at any point.

**Implementation prompt:**

> Orchestrate approved matrix rows sequentially/in parallel via `STEP-028`–`030` with distinct `EXP####` IDs. Aggregate mean ± SD validation ROC-AUC, PR-AUC, F1, and Brier across ALL planned seeds into `validation_matrix_summary.md`.

**Human-only actions and decisions:** Supervisor and researchers approve any prospective matrix amendment (e.g., compute-constrained disposition of secondary ablations) and declare validation exploration closed prior to `STEP-032`.

**Version-control/artifact expectations:** Commit all `EXP####` metadata, `MODEL####` cards, `G10` audits, and `validation_matrix_summary.md`; retain all Tier 3 checkpoints cleanly indexed.

**Documentation updates:** `experiment_plan.md` status table, `validation_matrix_summary.md`, `dashboard.md`, `risk_register.csv` (compute actuals).

**Verification checklist:**

- [ ] Every Block A–F row has a `G10 PASS` outcome or documented prospective disposition.
- [ ] All planned seeds retained and aggregated honestly (mean ± SD; zero best-seed cherry-picking).
- [ ] Single-factor ablations hold non-target hyperparameters, splits, and seeds fixed.
- [ ] Final test partition remains 100% sealed (`test_access_log.csv` clean).

**Common mistakes:** Changing learning rate, dropout, AND fusion architecture simultaneously while claiming a fusion-layer ablation; tuning the Transformer across 100 trials while running XGBoost with default parameters; dropping an unfavorable random seed.

**Recovery procedure:** Reclassify any accidentally confounded run as exploratory, launch a clean single-factor `EXP####` if resources allow, or narrow claims honestly before `STEP-032`.

**Definition of Done:** Full controlled Q1 experiment and ablation program completed on validation with `G10 PASS` across all eligible candidates, ready for final selection and freeze. Universal DoD applies.

**Next step:** [STEP-032](#step-032)

---

<a id="step-032"></a>
## STEP-032 — Select champion, fit calibrator & threshold on validation, and freeze (`G11`)

**Objective:** Select the final champion model and prespecified final-test comparators **strictly on validation**, fit post-hoc probability calibrators and operating thresholds **strictly on validation/OOF**, freeze all hashes, and pass `G11` prior to opening test data.

**Why this step exists:** Selecting models, thresholds ($\tau$), or calibration curves using final-test scores destroys held-out validity and guarantees Q1 rejection for test-set leakage.

**Governing section references:** [OS §6](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-06); [OS §7](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §8](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-08); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-031` complete; `G10 PASS` for every candidate considered; `G07–G09` current PASS; `test_access_log.csv` verified clean.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours plus supervisor & evaluation-reviewer freeze audit.

**Parallelizable:** No for model selection and freeze; background thesis literature drafting may proceed independently.

**Inputs:** `validation_matrix_summary.md`, `MODEL####` cards, validation/OOF probability outputs, `09_Evaluation_Stats/protocol.md`, `10_Explainability_XAI/xai_protocol.md`, `UD16–UD20`.

**Expected outputs:** Immutable `09_Evaluation_Stats/freeze.md` naming exact champion + comparator `MODEL####` IDs, frozen validation-fitted calibrators (`CalibratorHash`), frozen operating threshold(s) ($\tau$), frozen SHAP background sample (`BackgroundHash`, drawn strictly from Train), locked protocol hashes, test-custody release authorization, and `G11` assessment.

**Repository/file changes:** Create `09_Evaluation_Stats/freeze.md`, store serialized frozen calibrator & training-only SHAP background reference in restricted Tier 3/2B, update `model_registry.csv`, `decisions.csv`, `gates.csv`, and write `01_Project_Management/reviews/G11_assessment_<date>.md`.

**Execution procedure:**

1. Apply the pre-declared validation selection criterion (`STEP-025`) to choose the champion multimodal model (and prespecified key comparators across Tiers 1–3 + ablations for paired final-test comparison) without any look at test data.
2. Fit and compare approved post-hoc calibration methods (`UD16`: temperature scaling, Platt scaling, isotonic regression, or raw uncalibrated if superior) strictly on validation/OOF predictions, freezing the winning calibrator with SHA-256 (`CalibratorHash`).
3. Lock the binary/multi-class operating threshold $\tau$ (`UD16`: e.g., Youden's $J$, F1-optimal, or cardiologist-specified sensitivity floor) strictly on calibrated validation probabilities, documenting the exact precision/recall/F1 tradeoff on validation.
4. Freeze the stratified **training-only** SHAP background dataset (`BackgroundHash`), final statistical/DCA/subgroup/XAI protocol hashes, audit `test_access_log.csv` for zero prior contamination, and obtain supervisor + evaluation reviewer `G11` sign-off authorizing test-set unlock.

**Planning/review prompt:**

> Audit `09_Evaluation_Stats/freeze.md` and `test_access_log.csv` against `G11`. Confirm that champion selection, calibrator fitting, operating threshold $\tau$, and SHAP background construction used ZERO final-test data, and flag any unfrozen setting.

**Implementation prompt:**

> Fit approved calibrator and threshold $\tau$ on validation/OOF predictions only, serialize frozen artifacts with SHA-256 checksums, freeze the training-only SHAP background sample, and write `freeze.md`. Enforce strict hash matching in final-test inference code.

**Human-only actions and decisions:** Supervisor and evaluation/biostatistics reviewer audit test custody, approve frozen champion, calibrator, threshold $\tau$, and sign `G11` authorizing final-test release.

**Version-control/artifact expectations:** Commit `freeze.md` and `G11` audit *before* final-test prediction timestamps (`eval: freeze champion, calibrator, threshold and pass G11`); store calibrator/background binaries in Tier 3/2B.

**Documentation updates:** `freeze.md`, `model_registry.csv` (`CalibratorHash`, `ThresholdVal`), `test_access_log.csv` (authorized unlock timestamp), `gates.csv`.

**Verification checklist:**

- [ ] Champion and final-test comparators selected strictly from `G10 PASS` validation results.
- [ ] Post-hoc calibrator and operating threshold $\tau$ fitted strictly on validation/OOF and frozen by SHA-256.
- [ ] Training-only SHAP background sample hashed and locked.
- [ ] `G11` PASS timestamp strictly precedes any final-test inference execution.

**Common mistakes:** Fitting Platt scaling or picking $\tau$ on the final test ROC curve; forgetting to lock comparators (allowing cherry-picking of weak baselines after seeing test AUC); drawing SHAP background samples from the test set.

**Recovery procedure:** Halt immediately on any detected test exposure, disclose contamination transparently, and redesign with a genuinely untouched approved external/new cohort or reclassify as exploratory—never erase exposure history.

**Definition of Done:** `G11` PASS with immutable hash-locked freeze bundle authorizing sealed final-test evaluation. Universal DoD applies.

**Next step:** [STEP-033](#step-033)

---

<a id="step-033"></a>
## STEP-033 — Generate and validate frozen final-test (and optional external) predictions

**Objective:** Run frozen inference across the champion and prespecified comparators on the sealed held-out test set (and external cohort if adopted under `UD06`), verifying 100% patient coverage, finite probabilities, and hash fidelity.

**Why this step exists:** Reliable clinical evaluation requires complete per-patient prediction coverage (zero silently dropped records) and strict equivalence to the frozen `G11` bundle.

**Governing section references:** [OS §7](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §9](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-032` complete; `G11` PASS; authorized sealed test partition (`REL####/test/`) and frozen bundle hashes available.

**Estimated difficulty and time (provisional):** Moderate; 2–4 hours plus inference compute.

**Parallelizable:** Deterministic inference across distinct frozen `MODEL####` comparators (and across test vs external cohort) may run concurrently; aggregate into unique `EVAL####` records serially.

**Inputs:** `09_Evaluation_Stats/freeze.md`, frozen `MODEL####`/`CKPT####`/`PP####`/`CalibratorHash`/`ThresholdVal`, sealed `REL####` test set (and external cohort if adopted).

**Expected outputs:** Unique `EVAL####` bundle(s), raw logits + uncalibrated & calibrated predicted risk probabilities + thresholded class calls for every scheduled test patient, 100% coverage & integrity report, and updated `evaluation_registry.csv`.

**Repository/file changes:** Store restricted per-patient predictions in Tier 2B/3 `09_Evaluation_Stats/EVAL####/predictions.parquet`; commit safe `EVAL####/coverage_audit.md`, prediction SHA-256 hashes, and updated `evaluation_registry.csv` & `test_access_log.csv`.

**Execution procedure:**

1. Log authorized test-set access in `test_access_log.csv` and verify runtime hashes of `MODEL`, `CKPT`, `PP`/`FitStateHash`, `variables.csv`, `CalibratorHash`, `ThresholdVal`, and `REL` against `freeze.md` (abort on any mismatch!).
2. Run deterministic inference across 100% of scheduled test patients (and external validation cohort if adopted) for the frozen champion, all prespecified Tier 1–3 baselines, and ablation models—applying zero test-side fitting, re-tuning, or threshold tweaking.
3. Emit per-patient prediction tables preserving `ENC########`, `PAT########`, ground-truth `ADJ####` label, modality availability vector, raw score, uncalibrated probability, calibrated probability, and frozen-threshold binary/class call—plus explicit status codes for any failed/unreadable input.
4. Validate 100% patient coverage (`N_predicted == N_test_scheduled`), finite probabilities in $[0, 1]$, zero duplicate encounter IDs, and hash-lock `predictions.parquet` in Tier 2B/3.

**Planning/review prompt:**

> Audit `EVAL####` inference execution against `freeze.md`. Confirm exact hash matching, 100% patient coverage, explicit missing-modality handling, and zero post-test parameter adjustments.

**Implementation prompt:**

> Execute `14_Automation/predict_frozen.py --freeze 09_Evaluation_Stats/freeze.md`, saving locked per-patient predictions in Tier 2B/3 and safe coverage/hash verification in `09_Evaluation_Stats/EVAL####/coverage_audit.md`. Fail loudly on any hash mismatch or missing patient.

**Human-only actions and decisions:** Evaluation lead verifies test-access log compliance and approves any pre-registered failure disposition if an unforeseen corrupt record appears.

**Version-control/artifact expectations:** Per-patient predictions stay restricted in Tier 2B/3 with SHA-256 backup; commit safe `coverage_audit.md`, hashes, and `evaluation_registry.csv` to Git.

**Documentation updates:** `evaluation_registry.csv`, `EVAL####/coverage_audit.md`, `test_access_log.csv`.

**Verification checklist:**

- [ ] Every frozen hash (`MODEL`, `PP`, `Calibrator`, `Threshold`, `REL`) matched at runtime.
- [ ] 100% of scheduled test (and external) patients accounted for with zero silent drops.
- [ ] All probabilities finite in $[0, 1]$ with zero `NaN`/`Inf` and exact ground-truth alignment.
- [ ] Zero tuning, threshold edits, or retraining after observing test outputs.

**Common mistakes:** Dropping partial-modality test patients silently to inflate multimodal accuracy; applying an unfitted scaler on test; forgetting to store both uncalibrated and calibrated probabilities.

**Recovery procedure:** If a verified software bug (not model weakness!) invalidates prediction generation, mark original `EVAL####` invalid (preserve it!), fix the deterministic bug, rerun under a brand-new `EVAL####` with full disclosure; any model edit triggers test-exposure rules (`OS §7.1`).

**Definition of Done:** Hash-verified, 100%-coverage frozen test predictions ready for metrics, calibration, statistical inference, and XAI. Universal DoD applies.

**Next step:** [STEP-034](#step-034)

---

<a id="step-034"></a>
## STEP-034 — Compute mandatory proposal metrics, Q1 discrimination, and probability calibration

**Objective:** Calculate all six mandatory proposal metrics (`RF12`) plus adopted Q1 imbalance-sensitive metrics and probability calibration measures (`UD17`) reproducibly from frozen `EVAL####` predictions.

**Why this step exists:** In clinical CVD risk prediction, reporting Accuracy or ROC-AUC without Confusion Matrix counts, PR-AUC, Brier score, ECE, and calibration slope hides miscalibrated risks and class-imbalance failure.

**Governing section references:** [OS §7](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-033` validated frozen predictions; `STEP-026` known-case metric/calibration tests passing; `G11` freeze current.

**Estimated difficulty and time (provisional):** Hard; 3–5 hours.

**Parallelizable:** Yes with `STEP-035` once `STEP-033` predictions are locked; shares identical frozen `EVAL####` source hashes.

**Inputs:** Frozen `EVAL####/predictions.parquet` (champion + comparators + ablations), ground-truth `ADJ####` labels, frozen `09_Evaluation_Stats/protocol.md`.

**Expected outputs:** Reproducible `metrics_summary.csv`, exact Confusion Matrices (`[TN, FP; FN, TP]`), ROC & PR curve coordinates, pre- vs post-calibration metrics (Brier, Brier Skill Score, ECE with exact bin rule, Calibration Slope & Intercept, reliability diagram data), and multi-seed variance tables.

**Repository/file changes:** Write safe aggregate `09_Evaluation_Stats/EVAL####/metrics_summary.csv`, `confusion_matrices.csv`, `calibration_metrics.csv`, and curve CSVs for `FIG0003`; update `evaluation_registry.csv`.

**Execution procedure:**

1. Compute all **6 mandatory proposal metrics** for the champion, Tier 1–3 baselines, and Block D/E ablations at their frozen validation thresholds $\tau$: **Accuracy**, **Precision (PPV)**, **Recall (Sensitivity)**, **F1-Score**, **ROC-AUC**, and exact integer **Confusion Matrix** (`TN, FP, FN, TP`), recording prevalence and handling any zero denominator as `N/A` with explicit denominator counts.
2. Compute adopted Q1 imbalance-sensitive metrics (`UD17`): **PR-AUC (AUPRC)** alongside positive prevalence baseline, **Specificity**, **Negative Predictive Value (NPV)**, **Balanced Accuracy**, and **Matthews Correlation Coefficient (MCC)**.
3. Compute comprehensive **probability calibration** (both pre- and post-validation-fitted calibration): **Brier Score**, **Brier Skill Score**, **ECE** (documenting exact bin count and equal-width/quantile scheme), **Calibration Slope** and **Calibration-in-the-Large (Intercept)**, and reliability-bin coordinates.
4. Report multi-seed mean ± SD across all $S$ seeds alongside the frozen ensemble/champion score; never hide weak modalities or inferior ablations.

**Planning/review prompt:**

> Audit `metrics_summary.csv` and `calibration_metrics.csv` against `RF12` and `09_Evaluation_Stats/protocol.md`. Verify exact confusion-matrix arithmetic, prevalence context for Accuracy/PR-AUC, pre- vs post-calibration transparency, and zero post-hoc threshold edits.

**Implementation prompt:**

> Run frozen `14_Automation/evaluate_metrics.py` against locked `EVAL####/predictions.parquet` saving full-precision CSV outputs and SHA-256 provenance. Never round intermediate calculations or alter $\tau$ on test outputs.

**Human-only actions and decisions:** Evaluation reviewer audits mathematical definitions, denominator conventions, and pre-/post-calibration behavior.

**Version-control/artifact expectations:** Commit safe aggregate metric/calibration CSVs and curve coordinates to Git; preserve full-precision provenance hashes.

**Documentation updates:** `EVAL####/metrics_summary.csv`, `calibration_metrics.csv`, `evaluation_registry.csv`.

**Verification checklist:**

- [ ] All 6 mandatory proposal metrics (`Accuracy`, `Precision`, `Recall`, `F1-Score`, `ROC-AUC`, `Confusion Matrix`) reported for champion and key comparators.
- [ ] Adopted Q1 metrics (`PR-AUC`, `Specificity`, `NPV`, `Brier`, `ECE`, `Calibration Slope/Intercept`) computed cleanly.
- [ ] Confusion-matrix counts reconcile identically with $N_{\text{test}}$, Precision, Recall, F1, and Accuracy.
- [ ] All multi-seed runs and negative/modest ablation outcomes retained honestly.

**Common mistakes:** Reporting Accuracy on an 85/15 imbalanced cohort without prevalence or PR-AUC; tuning $\tau$ on test to boost F1; skipping calibration slope/Brier for a "risk prediction" paper.

**Recovery procedure:** Invalidate defective metric scripts, preserve old output, repair verified math bugs under a new `EVAL####` with full disclosure, and re-verify against synthetic unit tests.

**Definition of Done:** Complete, traceable discrimination and probability calibration metrics generated from frozen predictions. Universal DoD applies.

**Next step:** [STEP-035](#step-035)

---

<a id="step-035"></a>
## STEP-035 — Run paired statistical inference (DeLong, bootstrap CIs, McNemar) and DCA

**Objective:** Quantify finite-sample uncertainty via patient-level stratified bootstrap 95% CIs, test superiority/non-inferiority via paired statistical tests with multiple-comparison correction, and evaluate clinical Net Benefit via Decision Curve Analysis (`UD17–UD18`).

**Why this step exists:** Point-estimate comparisons (e.g., "0.87 vs 0.85 AUC") without 95% CIs, paired DeLong $p$-values, multiplicity correction, and clinical utility (DCA) are routinely rejected by Q1 medical-AI reviewers.

**Governing section references:** [OS §7](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-033` locked predictions; `STEP-025` frozen statistical & DCA plan (`UD17–UD18`); `STEP-026` stats unit tests passing.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours plus bootstrap compute duration.

**Parallelizable:** Yes with `STEP-034` after `STEP-033`; uses exact same locked predictions and frozen bootstrap seed.

**Inputs:** Frozen `EVAL####/predictions.parquet`, `PAT########` grouping keys, `09_Evaluation_Stats/protocol.md` (`B` resamples, primary comparison pairs, DCA threshold grid, multiplicity method).

**Expected outputs:** `bootstrap_cis.csv` (95% CIs for all discrimination & calibration metrics), `paired_stat_tests.csv` (DeLong $\Delta$AUC + $p$ + adjusted $p$; paired bootstrap $\Delta$PR-AUC/$\Delta$F1/$\Delta$Brier; McNemar exact $p$), and `dca_net_benefit.csv` (Net Benefit across clinical threshold probabilities $p_t$ with bootstrap bands).

**Repository/file changes:** Write safe aggregate `09_Evaluation_Stats/EVAL####/bootstrap_cis.csv`, `paired_stat_tests.csv`, `dca_net_benefit.csv`, and `stats_dca_notes.md`; update `evaluation_registry.csv`.

**Execution procedure:**

1. Execute **patient-level stratified bootstrap** ($B \ge 1{,}000$–$2{,}000$, fixed seed, resampling whole `PAT########` clusters rather than individual encounters if repeat visits exist) to compute 95% confidence intervals (BCa or percentile per `UD18`) for all discrimination and calibration metrics across champion, Tier 1–3 comparators, and ablations.
2. Execute **paired statistical comparisons** between the frozen Transformer Multimodal Fusion champion and prespecified comparators (best Clinical-only, best ECG-only, best Lab-only, best Lifestyle-only, Early-Fusion XGBoost/MLP, Late-Fusion Ensemble, Clinical Risk Score if adopted, and LOMO ablations):
   - Two-sided **DeLong's test** for paired correlated ROC-AUCs;
   - **Paired patient-level bootstrap difference test** for $\Delta\text{PR-AUC}$, $\Delta\text{F1}$, $\Delta\text{Brier}$, and $\Delta\text{Net Benefit}$;
   - **McNemar's exact test** for paired thresholded classification discordance at frozen $\tau$.
3. Apply prespecified **multiple-comparison correction** (Holm-Bonferroni or Benjamini-Hochberg FDR per `UD18`) across primary comparison families, reporting raw $p$, adjusted $p$, effect size $\Delta$, and 95% CI of $\Delta$ honestly—never claiming "significant improvement" when adjusted $p \ge \alpha$ or 95% CI spans 0!
4. Execute **Decision Curve Analysis (DCA)** over the cardiologist-approved clinical threshold probability range $p_t$ comparing calibrated Transformer Multimodal Fusion vs best unimodal baseline vs "Treat/Screen All" vs "Treat/Screen None," recording exact Net Benefit curves and bootstrap uncertainty bands.

**Planning/review prompt:**

> Audit our paired statistical testing and DCA outputs for patient-level cluster resampling fidelity, correct multiple-testing adjustment across all prespecified comparisons, clinically sensible DCA threshold range, and honest interpretation of non-significant differences.

**Implementation prompt:**

> Run frozen `14_Automation/evaluate_stats_dca.py` with fixed bootstrap seed on locked `EVAL####` predictions, outputting `bootstrap_cis.csv`, `paired_stat_tests.csv`, and `dca_net_benefit.csv` with full SHA-256 provenance.

**Human-only actions and decisions:** Biostatistics reviewer verifies DeLong/bootstrap/multiplicity math; cardiologist confirms clinical interpretability of the DCA threshold probability range.

**Version-control/artifact expectations:** Commit safe aggregate statistical & DCA CSV tables and generator commit hash to Git.

**Documentation updates:** `EVAL####/stats_dca_notes.md`, `evaluation_registry.csv`, `claims.csv` draft entries.

**Verification checklist:**

- [ ] Bootstrap resamples at the `PAT########` level with documented fixed seed and $B \ge 1{,}000$.
- [ ] DeLong, paired bootstrap $\Delta$, and McNemar tests run on exact matched patient pairs with raw AND adjusted $p$-values plus effect sizes.
- [ ] DCA compares calibrated multimodal model against unimodal comparator, Treat-All, and Treat-None across the pre-declared $p_t$ range.
- [ ] Non-significant or null differences reported transparently without spin.

**Common mistakes:** Running unpaired independent $t$-tests across correlated models on the same test set; skipping multiplicity correction across 12 baseline tests; running DCA on uncalibrated logits instead of calibrated probabilities.

**Recovery procedure:** Fix verified statistical code bugs under a new versioned `EVAL####` with disclosure; never drop comparisons selectively to make adjusted $p$-values look smaller.

**Definition of Done:** Complete, multiplicity-adjusted statistical inference, 95% CIs, and clinical DCA utility evidence locked and verified. Universal DoD applies.

**Next step:** [STEP-036](#step-036)

---

<a id="step-036"></a>
## STEP-036 — Consolidate final quantitative evaluation report and pass `G12`

**Objective:** Assemble one unified, hash-traceable final quantitative evaluation report reconciling all discrimination, calibration, ablation, statistical, and DCA outputs—and pass `G12`.

**Why this step exists:** Q1 tables and abstracts must pull from one audited master evaluation report where every number, CI, $p$-value, and ablation reconciles identically.

**Governing section references:** [OS §7](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §10](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-034` and `STEP-035` complete; `G11` freeze traceability intact; all adopted protocol analyses executed (or deviations logged).

**Estimated difficulty and time (provisional):** Hard; 3–5 hours plus evaluation & biostatistics review.

**Parallelizable:** Report compilation and numerical cross-checking may be divided between the two researchers; `G12` approval waits for full reconciliation.

**Inputs:** `EVAL####` `coverage_audit.md`, `metrics_summary.csv`, `confusion_matrices.csv`, `calibration_metrics.csv`, `bootstrap_cis.csv`, `paired_stat_tests.csv`, `dca_net_benefit.csv`, `freeze.md`, `T19` (`evaluation.md`).

**Expected outputs:** Master `09_Evaluation_Stats/EVAL####/report.md`, finalized `evaluation_registry.csv`, verified empirical `claims.csv` updates, and `G12` assessment.

**Repository/file changes:** Write `09_Evaluation_Stats/EVAL####/report.md` and `01_Project_Management/reviews/G12_assessment_<date>.md`; update `evaluation_registry.csv`, `claims.csv`, and `gates.csv`.

**Execution procedure:**

1. Reconcile every single number in `EVAL####/report.md` back to full-precision CSV outputs, `freeze.md` hashes, and exact `MODEL`/`REL`/`PP` IDs (including external validation results separately from internal held-out test results if adopted under `UD06`).
2. Present unified Tier 1–4 comparison tables, Progressive Modality Addition & Leave-One-Modality-Out ablation tables, Confusion Matrices, Calibration parameters, DCA summaries, multi-seed variance, and multiplicity-adjusted statistical tests.
3. Explicitly distinguish validation-selection results (`STEP-031`) from sealed held-out final test results (`STEP-033–035`), preserving all negative/null findings and any documented protocol deviations.
4. Audit all `G12` mandatory criteria (validity, completeness, traceability—never requiring a pre-ordained AUC level!) and obtain evaluation & biostatistics reviewer sign-off.

**Planning/review prompt:**

> Audit `09_Evaluation_Stats/EVAL####/report.md` against `G12`. Check for any missing mandatory proposal metric, unadjusted $p$-value, omitted negative ablation, confusion-matrix mismatch, or conflation of internal vs external results.

**Implementation prompt:**

> Generate master markdown/CSV evaluation tables programmatically directly from `EVAL####/*.csv` preserving source hashes and consistent rounding rules; save verified `EVAL####/report.md` and `G12` review.

**Human-only actions and decisions:** Evaluation & biostatistics reviewer verifies complete quantitative validity and signs `G12`; supervisor notes any consequential deviations.

**Version-control/artifact expectations:** Commit `EVAL####/report.md`, `evaluation_registry.csv`, updated `claims.csv`, and `G12` review to Git.

**Documentation updates:** `EVAL####/report.md`, `evaluation_registry.csv`, `claims.csv`, `gates.csv`, `dashboard.md`.

**Verification checklist:**

- [ ] All 6 mandatory metrics + PR-AUC, calibration, DCA, 95% CIs, and adjusted paired $p$-values reconcile identically.
- [ ] All planned Tier 1–4 comparators, LOMO/progressive ablations, and seeds accounted for without selective omission.
- [ ] Validation numbers clearly separated from final held-out (and external) test numbers.
- [ ] `G12` PASS grounded strictly in methodological validity and signed by evaluation reviewer.

**Common mistakes:** Mixing best-seed accuracy from one run with AUC from another checkpoint; reporting uncalibrated validation scores beside calibrated test scores; omitting a strong early-fusion XGBoost baseline that nearly matched the Transformer.

**Recovery procedure:** Reconcile discrepancies directly from locked `EVAL####` CSVs, correct provenance/scripts under a versioned `EVAL####` if a calculation error occurred, and re-audit `G12`.

**Definition of Done:** `G12` PASS; single authoritative quantitative evidence package ready for fairness/error/XAI audits and Q1 writing. Universal DoD applies.

**Next step:** [STEP-037](#step-037)

---

<a id="step-037"></a>
## STEP-037 — Conduct subgroup fairness, missing-modality stress tests, error & PROBAST-AI audit (`G13`)

**Objective:** Evaluate demographic/site fairness, missing-modality inference robustness, systematic TP/FP/TN/FN clinical error patterns, and four-domain PROBAST-AI risk of bias—and pass `G13`.

**Why this step exists:** Top-tier Q1 medical-AI journals explicitly mandate subgroup equity checks, realistic missing-modality degradation tests, qualitative error inspection, and structured PROBAST-AI bias disclosure.

**Governing section references:** [OS §7](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-07); [OS §10](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-036` complete; `G12` PASS; frozen `EVAL####` predictions, subgroup metadata, and qualified cardiologist available.

**Estimated difficulty and time (provisional):** Hard; 5–8 hours analytical audit + cardiologist error review.

**Parallelizable:** Automated subgroup/missing-modality stress computations and qualitative TP/FP/TN/FN case packet assembly can proceed concurrently; PROBAST-AI synthesis follows both.

**Inputs:** Frozen champion `MODEL####` & `EVAL####` predictions, `REL####` demographic/site/ECG-quality metadata, `T20` (`error_probast.md`), PROBAST-AI 4-domain rubric.

**Expected outputs:** `subgroup_fairness.csv`, `missing_modality_robustness.csv`, systematic TP/FP/TN/FN clinical error review (`error_probast.md`), completed four-domain **PROBAST-AI Risk-of-Bias Self-Audit** (`12_Writing/checklists/PROBAST_AI.md`), bounded limitations charter, and `G13` assessment.

**Repository/file changes:** Create `09_Evaluation_Stats/EVAL####/subgroup_fairness.csv`, `missing_modality_robustness.csv`, `error_probast.md`, `12_Writing/checklists/PROBAST_AI.md`, and `01_Project_Management/reviews/G13_assessment_<date>.md`; update `evaluation_registry.csv`, `claims.csv`, and `gates.csv`.

**Execution procedure:**

1. **Subgroup fairness audit:** Stratify frozen test discrimination (ROC-AUC, PR-AUC, Recall, Specificity, F1) and calibration (Brier, ECE) by **Sex/Gender**, **Age strata**, **Hospital/Diagnostic site** (if multi-site), and **Modality-completeness tier**, reporting exact subgroup $n$/events and 95% CIs (flagging any disparity honestly!).
2. **Missing-modality inference stress test (`RQ2`):** Without retraining, systematically mask each non-clinical modality (Drop ECG, Drop Lab, Drop Lifestyle, Drop ECG+Lab, Drop ECG+Lifestyle, Drop Lab+Lifestyle) at test time on complete-case test patients to measure graceful degradation of the Transformer's missing-modality masking vs unimodal fallbacks.
3. **Systematic qualitative error review:** Draw a prospectively defined stratified sample of **TP, FP, TN, and FN** test encounters (including high-confidence errors and low-quality ECGs) for qualified cardiologist inspection—distinguishing genuine model failure from atypical clinical presentation, missing data, ECG noise, or residual label uncertainty.
4. **PROBAST-AI 4-domain self-audit & limitations:** Score Participants, Predictors, Outcome, and Analysis honestly (disclosing sample-size limits, cross-sectional vs longitudinal horizon, spectrum/site bias, incorporation bias, and lack of prospective clinical impact validation), and assess `G13`.

**Planning/review prompt:**

> Conduct an unsparing Q1 subgroup fairness, missing-modality degradation, clinical error, and PROBAST-AI audit on `EVAL####`. Surface every demographic disparity, incorporation-bias concern, or generalizability boundary before peer reviewers do.

**Implementation prompt:**

> Compute stratified subgroup metrics and missing-modality stress-test degradations strictly using the frozen `MODEL####`/`Calibrator`/`Threshold` (zero retraining or test-driven tuning!). Assemble de-identified TP/FP/TN/FN review packets in Tier 2B and commit safe aggregate tables and `PROBAST_AI.md`.

**Human-only actions and decisions:** Qualified cardiologist reviews TP/FP/TN/FN clinical error packets; supervisor approves PROBAST-AI risk-of-bias self-assessment, bounded limitations, and signs `G13`.

**Version-control/artifact expectations:** Per-patient error review packets stay strictly in restricted Tier 2B; commit safe aggregate fairness/robustness tables, `error_probast.md`, `PROBAST_AI.md`, and `G13` review to Git.

**Documentation updates:** `EVAL####/error_probast.md`, `PROBAST_AI.md`, `claims.csv`, `gates.csv`, `dashboard.md`.

**Verification checklist:**

- [ ] Sex, age, site (if multi-site), and modality-completeness subgroups reported with exact $n$/events and CIs.
- [ ] Missing-modality inference stress tests executed on frozen champion without retraining.
- [ ] Stratified TP/FP/TN/FN error review completed with qualified cardiologist input; zero cherry-picking.
- [ ] All four PROBAST-AI domains honestly audited; `G13` PASS signed by cardiologist and supervisor.

**Common mistakes:** Hiding poor sensitivity in female or older patients inside aggregate AUC; fixing test errors by editing the model retroactively; pretending PROBAST risk of bias is "Low" across all domains when primary $N$ is small or single-center.

**Recovery procedure:** Repair incomplete stratification or unbalanced case sampling, route any confirmed ground-truth error strictly through versioned `ADJ`/`REL`/`EVAL` disclosure (never silent re-tuning), and re-audit `G13`.

**Definition of Done:** `G13` PASS with comprehensive fairness, missing-modality robustness, clinical error, and PROBAST-AI limitations evidence. Universal DoD applies.

**Next step:** [STEP-038](#step-038)

---

<a id="step-038"></a>
## STEP-038 — Compute multimodal SHAP attributions (global, local, ECG & modality-share)

**Objective:** Generate reproducible multimodal SHAP attributions for the frozen champion (and key tree baseline comparator) using strictly **training-only** background data, verifying local additivity and decomposing importance across modalities, tabular variables, and ECG signals.

**Why this step exists:** Explainability is a headline pillar of the approved title (`RF01`, `RF08`, `RF11`); rigorous multimodal attribution across heterogeneous tabular features AND ECG signals requires exact background isolation and mathematical completeness checks.

**Governing section references:** [OS §8](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-08); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-036–037` complete; `G12–G13` PASS; frozen `MODEL####`, `EVAL####`, training-only `BackgroundHash` (`STEP-032`), and `10_Explainability_XAI/xai_protocol.md` locked.

**Estimated difficulty and time (provisional):** Hard; 4–8 hours plus SHAP computation time (especially for neural Transformer + ECG attributions).

**Parallelizable:** Champion Transformer SHAP, tree-baseline `TreeSHAP`, and optional LIME/Integrated Gradients cross-checks (`UD19`) may run in parallel against the identical frozen test set.

**Inputs:** Frozen champion `MODEL####` (all $S$ seeds for stability prep), frozen `BackgroundHash` (Train partition only!), locked `REL####` test inputs, `10_Explainability_XAI/xai_protocol.md`, `UD19`.

**Expected outputs:** Unique `XAI####` record, verified additivity-error report, global tabular SHAP summaries & non-linear dependence data, **modality-level SHAP share** (`Clinical %`, `ECG %`, `Laboratory %`, `Lifestyle %`) globally and per patient, ECG segment/lead/feature attributions, local explanation arrays (stored in Tier 3), and optional LIME/IG comparison.

**Repository/file changes:** Store full per-patient SHAP arrays & restricted local plots in Tier 3/2B `10_Explainability_XAI/XAI####/`; commit safe aggregate importance tables (`global_shap.csv`, `modality_shares.csv`, `additivity_check.md`), SHA-256 hashes, and updated `10_Explainability_XAI/xai_registry.csv`.

**Execution procedure:**

1. Verify hashes of frozen `MODEL####`, `PP`/`FitStateHash`, and the **training-only** SHAP background sample (`BackgroundHash`) before computing a single explanation—abort if any test record appears in the background set!
2. Execute the approved neural Shapley explainer (`UD19`: e.g., `GradientSHAP`/`DeepSHAP`/`PartitionSHAP` over semantic tabular + ECG patches/features) on 100% of test patients (and across all $S$ trained seeds to feed `STEP-039` stability) plus `TreeSHAP` on the top GBDT comparator and optional LIME/IG cross-check.
3. Verify **local additivity / completeness** ($\max_x |\sum_i \phi_i(x) + \phi_0 - f(x)|$ and median relative error) against the prospective tolerance in `xai_protocol.md`; diagnose and resolve any explainer convergence defect rather than plotting broken attributions.
4. Aggregate exact **modality-level SHAP contributions** (`Clinical`, `ECG`, `Laboratory`, `Lifestyle`), tabular global rankings & interaction/dependence curves, and clinically aligned ECG waveform/interval attributions; keep raw Transformer attention maps clearly segregated as architectural diagnostics, never labeled faithful feature attributions.

**Planning/review prompt:**

> Audit `XAI####` attribution generation against `xai_protocol.md` and `UD19`. Confirm training-only background isolation, verified local additivity convergence, mathematically valid modality-share aggregation across tabular + ECG inputs, and separation from raw attention weights.

**Implementation prompt:**

> Run `14_Automation/compute_xai.py --freeze 09_Evaluation_Stats/freeze.md`, storing full SHAP tensors in Tier 3 with SHA-256 checksums and safe aggregate global/modality CSVs and additivity diagnostics in `10_Explainability_XAI/XAI####/`.

**Human-only actions and decisions:** XAI lead verifies additivity convergence and inspects cross-method (SHAP vs TreeSHAP / LIME / IG) agreement.

**Version-control/artifact expectations:** Full per-patient SHAP arrays and local patient plots stay in Tier 3/2B; commit safe aggregate rankings, modality shares, additivity log, and `xai_registry.csv` to Git.

**Documentation updates:** `xai_registry.csv`, `XAI####/additivity_check.md`, `XAI####/global_shap.csv`, `XAI####/modality_shares.csv`.

**Verification checklist:**

- [ ] Background reference dataset strictly verified from Training partition (`BackgroundHash` match).
- [ ] Additivity / efficiency error verified within prospective tolerance across test cohort.
- [ ] Three explanation levels produced: modality-level share, tabular feature-level, and ECG signal/feature-level.
- [ ] Attributions computed across all $S$ seeds for objective stability analysis in `STEP-039`.

**Common mistakes:** Passing `X_test` as the SHAP background distribution; presenting raw Transformer attention weights as SHAP/faithful importance; summing raw signed vs absolute ECG time-step attributions carelessly so 5,000 ECG samples numerically swamp 10 tabular variables (always handle coalition/aggregation normalization cleanly per `UD19`!).

**Recovery procedure:** If additivity fails or high-dimensional ECG discretization distorts modality shares, revise the explainer coalition/normalization formula transparently under a new `XAI####` ID, verify on synthetic ground-truth data (`STEP-026`), and re-run without altering the frozen model.

**Definition of Done:** Verified, leakage-free, additivity-checked multimodal SHAP attributions produced across modalities, tabular features, ECG signals, and seeds. Universal DoD applies.

**Next step:** [STEP-039](#step-039)

---

<a id="step-039"></a>
## STEP-039 — Benchmark quantitative XAI faithfulness (AOPC) and multi-seed stability

**Objective:** Mathematically validate that the multimodal SHAP explanations genuinely reflect the frozen Transformer's decision mechanics via perturbation faithfulness (Deletion/Insertion AOPC vs random control), modality-ablation concordance, and multi-seed/perturbation stability (`UD20`).

**Why this step exists:** This single step separates Q1-publishable medical XAI papers from rejected "SHAP plot dump" submissions—proving objectively whether explanations are faithful and stable rather than arbitrary noise.

**Governing section references:** [OS §8](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-08); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-038` additivity-checked `XAI####` attributions across test patients and all $S$ seeds; `STEP-034–036` LOMO ablation results; frozen `xai_protocol.md` (`UD20`).

**Estimated difficulty and time (provisional):** Hard; 4–8 hours including perturbation inference compute.

**Parallelizable:** Deletion/Insertion perturbation curves, LOMO-vs-SHAP concordance, multi-seed rank stability, and local input-noise stability may execute concurrently on frozen `XAI####`.

**Inputs:** Frozen champion `MODEL####`, locked `XAI####` SHAP tensors (all $S$ seeds), `REL####` test inputs, training-distribution perturbation baselines, LOMO ablation metrics (`STEP-036`), `UD20`.

**Expected outputs:** `faithfulness_curves.csv` (Deletion & Insertion curves + AOPC / Comprehensiveness / Sufficiency vs random-masking & reverse-importance negative controls with 95% bootstrap CIs), `lomo_xai_concordance.csv`, `stability_metrics.csv` (multi-seed Spearman $\rho$, Kendall $\tau$, Top-$k$ Jaccard; local Lipschitz input-perturbation stability), and `faithfulness_stability_report.md`.

**Repository/file changes:** Write safe aggregate CSVs & `faithfulness_stability_report.md` inside `10_Explainability_XAI/XAI####/`; update `xai_registry.csv` (`DeletionAOPC`, `InsertionAOPC`, `RandomControlAOPC`, `LOMOConcordance`, `SeedStabilityRho`).

**Execution procedure:**

1. **Deletion & Insertion Faithfulness (`UD20`):** Progressively mask (deletion) or restore (insertion) the top-$k$ positively attributed tabular features and ECG segments using training-distribution baseline/conditional values, measuring predicted risk change across steps ($k = 1, \dots, K$). Compute **AOPC**, **Comprehensiveness**, and **Sufficiency** alongside **Random-Masking** and **Least-Important-First** negative controls (with paired patient-level bootstrap 95% CIs and significance tests!).
2. **Modality-Level SHAP vs Empirical LOMO Concordance:** Compare mean absolute modality-level SHAP shares (`Clinical`, `ECG`, `Laboratory`, `Lifestyle`) against empirical **Leave-One-Modality-Out** test performance drops ($\Delta\text{ROC-AUC}$ and $\Delta\text{Brier}$), quantifying rank agreement and interpreting correlated modality redundancy honestly.
3. **Multi-Seed Attribution Stability:** Across all $S$ independently trained champion seeds, compute pairwise Spearman $\rho$, Kendall $\tau$, and Top-$k$ ($k = 5, 10$) Jaccard overlap for both global feature rankings and per-patient local explanations.
4. **Local Input-Perturbation Stability:** Apply tiny clinically plausible perturbations within continuous assay/ECG noise bounds to verify that local SHAP explanations exhibit bounded Lipschitz stability rather than erratic rank flips; report poor faithfulness or instability honestly if observed!

**Planning/review prompt:**

> Audit `XAI####` faithfulness and stability benchmarks against Q1 XAI standards. Verify whether Deletion/Insertion AOPC outperforms random masking with statistical rigor, whether LOMO ablation agrees with modality SHAP shares, and whether multi-seed rankings remain stable.

**Implementation prompt:**

> Execute `14_Automation/evaluate_xai_faithfulness.py` on frozen `MODEL####` and `XAI####` arrays, computing Deletion/Insertion AOPC vs random controls, LOMO concordance, and multi-seed/perturbation stability with bootstrap 95% CIs, saving outputs to `10_Explainability_XAI/XAI####/`.

**Human-only actions and decisions:** XAI reviewer audits perturbation baselines (guarding against out-of-distribution masking artifacts) and verifies honest reporting of both strengths and instabilities.

**Version-control/artifact expectations:** Commit safe aggregate faithfulness/stability CSVs, curve data (for `FIG0006`), and `faithfulness_stability_report.md` to Git.

**Documentation updates:** `xai_registry.csv`, `XAI####/faithfulness_stability_report.md`, `claims.csv` drafts.

**Verification checklist:**

- [ ] Deletion and Insertion curves compared quantitatively against random-masking and reverse-order negative controls with 95% CIs.
- [ ] Modality-level SHAP shares cross-checked against empirical Leave-One-Modality-Out performance drops.
- [ ] Multi-seed Spearman $\rho$, Kendall $\tau$, and Top-$k$ Jaccard reported across ALL $S$ seeds.
- [ ] Local input-perturbation stability quantified; any instability or OOD perturbation caveat disclosed honestly.

**Common mistakes:** Omitting a random-masking negative control; zero-imputing masked features when `0` is a clinically meaningful value (e.g., 0 = non-smoker or scaled mean mismatch); claiming "stable XAI" after checking only one seed.

**Recovery procedure:** Fix invalid perturbation baselines (e.g., use training marginal/conditional replacement), re-run faithfully under a logged update, and never cherry-pick a subset of patients to inflate AOPC.

**Definition of Done:** Objective quantitative XAI faithfulness and stability evidence locked and ready for shortcut auditing and cardiologist review. Universal DoD applies.

**Next step:** [STEP-040](#step-040)

---

<a id="step-040"></a>
## STEP-040 — Perform spurious-shortcut audit, cardiologist XAI review, and pass `G14`

**Objective:** Audit top global and local SHAP drivers for non-clinical dataset shortcuts, conduct structured qualified cardiologist plausibility review across balanced TP/FP/TN/FN cases (`UD21`), bound XAI claims, and pass `G14`.

**Why this step exists:** High faithfulness proves explanations match the model—even if the model cheated via a hospital/missingness shortcut! Clinician review + shortcut auditing verify clinical sense and stop Q1 rejection for causal or trust overclaiming.

**Governing section references:** [OS §8](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-08); [OS §12](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-12); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-038–039` complete; `G13` current PASS; approved clinician review rubric (`UD21`) and qualified cardiologist engaged.

**Estimated difficulty and time (provisional):** Hard; 4–6 hours packet assembly & audit + qualified cardiologist review session.

**Parallelizable:** Automated shortcut screening and de-identified cardiologist packet preparation may proceed concurrently; `G14` final sign-off waits for clinical review.

**Inputs:** `XAI####` global/local/ECG/modality attributions, `faithfulness_stability_report.md`, `EVAL####` TP/FP/TN/FN stratified error sample, `T21` (`xai_audit.md`), `UD21`.

**Expected outputs:** Spurious-shortcut audit report, structured cardiologist plausibility review summary (global + stratified TP/FP/TN/FN local packets), master `10_Explainability_XAI/XAI####/report.md`, bounded XAI claim entries in `claims.csv`, and `G14` assessment.

**Repository/file changes:** Keep de-identified local clinician review packets in Tier 2B; commit safe `10_Explainability_XAI/XAI####/report.md`, `clinician_plausibility_summary.md`, `shortcut_audit.md`, `01_Project_Management/reviews/G14_assessment_<date>.md`, and update `xai_registry.csv`, `claims.csv`, `gates.csv`.

**Execution procedure:**

1. **Spurious-shortcut & confounder audit:** Inspect top global tabular, missingness-indicator, and ECG-segment SHAP attributions for red-flag shortcuts—specifically: (a) missingness indicator flags outranking core physiological risk factors, (b) recruitment-site proxies, (c) ECG baseline/50 Hz noise/padding edge artifacts, or (d) unexpected post-diagnosis treatment proxies. Log `CLEAN` or `SHORTCUT_DETECTED` honestly; any severe leakage shortcut triggers immediate disclosure/remediation before claiming Q1 validity!
2. **Balanced local packet selection (anti-cherry-picking):** Select a prospectively sampled set of de-identified test encounters spanning **TP, FP, TN, and FN** cases (including cases where ECG vs Lab vs Lifestyle drove divergent contributions), confirming zero PHI remains on any ECG strip or summary sheet.
3. **Structured cardiologist plausibility review (`UD21`):** Have the qualified cardiologist rate global rankings and local multimodal packets (calibrated risk + modality share + tabular waterfall + ECG attribution overlay) on: (a) concordance with cardiovascular pathophysiology, (b) interpretability/clarity of multimodal breakdown, and (c) clinically implausible or contradictory attributions (preserving negative clinical critiques verbatim!).
4. **Enforce strict XAI claim boundaries & assess `G14`:** Lock permitted claim phrasing in `claims.csv` (explicitly prohibiting biological causality from SHAP and prohibiting "increases clinician trust/speed" unless an IRB-approved clinician reader trial was conducted), finalize `XAI####/report.md`, and obtain XAI reviewer + cardiologist + supervisor `G14` sign-off.

**Planning/review prompt:**

> Audit `XAI####` shortcut screening, cardiologist plausibility ratings, and proposed manuscript XAI claims against `G14`. Flag any missingness/ECG-edge shortcut, cherry-picked patient example, causal verb ("proves", "causes"), or unproven clinician-trust assertion.

**Implementation prompt:**

> Generate balanced de-identified TP/FP/TN/FN clinical review packets (in Tier 2B) from locked `XAI####` arrays, compile aggregate rubric scores and shortcut-audit results into `10_Explainability_XAI/XAI####/report.md`, and record evidenced `G14` review.

**Human-only actions and decisions:** Qualified cardiologist completes structured clinical plausibility rubric; XAI reviewer and supervisor audit shortcut findings, enforce claim boundaries, and sign `G14`.

**Version-control/artifact expectations:** Individual clinical packets stay strictly in restricted Tier 2B (only IRB-cleared, fully de-identified illustrative examples approved for publication enter `11_Figures_Tables/`); commit safe `XAI####/report.md`, `xai_registry.csv`, and `G14` audit to Git.

**Documentation updates:** `XAI####/report.md`, `xai_registry.csv`, `claims.csv`, `gates.csv`, `dashboard.md`.

**Verification checklist:**

- [ ] Spurious-shortcut audit explicitly inspected missingness flags, site proxies, and ECG waveform artifacts.
- [ ] Qualified cardiologist reviewed global SHAP plus a balanced, non-cherry-picked TP/FP/TN/FN local sample.
- [ ] All XAI claims strictly distinguish model attribution from biological causality and omit unproven clinician-trust claims (unless a separate IRB trial occurred).
- [ ] `G14` PASS backed by `STEP-038–040` evidence and signed by XAI reviewer, cardiologist, and supervisor.

**Common mistakes:** Showing the cardiologist only 3 flattering True Positive examples; hiding that `missing_troponin_flag` was the #1 SHAP feature; writing "SHAP proves smoking/ECG caused CVD and boosts doctor confidence."

**Recovery procedure:** If a major leakage/site shortcut is discovered, do NOT hide it—document the finding transparently, remediate the earliest responsible step (`STEP-014`/`019`/`028`), disclose test exposure, and re-verify; if only claim wording overreached, narrow `claims.csv` and re-audit `G14`.

**Definition of Done:** `G14` PASS; multimodal XAI pillar is quantitatively faithful, stable, shortcut-audited, clinically reviewed, and honestly bounded for Q1 publication. Universal DoD applies.

**Next step:** [STEP-041](#step-041)

---

<a id="step-041"></a>
## STEP-041 — Package reproducible research prototype (and optional defense interface)

**Objective:** Package the frozen four-modality inference, probability calibration, and local SHAP explanation pipeline into a clean, hash-verified research decision-support prototype (plus optional defense interface if approved under `UD22`).

**Why this step exists:** `RF16` envisions a reliable decision-support research prototype; packaging the exact frozen scientific pipeline guarantees zero drift between evaluated models and showcased outputs.

**Governing section references:** [OS §2](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-02); [OS §9](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §11](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-036–040` complete; `G12–G14` current PASS; frozen `MODEL####`, `PP####`/`FitStateHash`, `CalibratorHash`, `ThresholdVal`, training-only SHAP background, and `UD22` decision recorded.

**Estimated difficulty and time (provisional):** Moderate; 6–12 hours for CLI prototype + tests (add 8–16 hours if optional local/hosted defense UI approved under `UD22`).

**Parallelizable:** Prototype documentation (`13_Documentation/prototype_guide.md`) and synthetic end-to-end sample fixtures may proceed alongside entry-point implementation.

**Inputs:** Frozen `G11` bundle, `src/cvd_mm/` inference/calibration/SHAP modules, permitted synthetic/disclosure-approved de-identified demo cases, `UD22` interface & disclaimer decision.

**Expected outputs:** Hash-verified `src/cvd_mm/prototype.py` + thin `14_Automation/predict_explain.py` CLI, synthetic end-to-end demo bundle (safe for public Q1 GitHub companion release!), functional error-contract tests, `13_Documentation/prototype_guide.md`, and (ONLY if `UD22` approved) `prototype_ui/` thin interface with parity report and offline fallback.

**Repository/file changes:** Finalize `src/cvd_mm/prototype.py`, `14_Automation/predict_explain.py`, `tests/test_prototype.py`, synthetic demo fixtures, `13_Documentation/prototype_guide.md`, and optional `prototype_ui/` if `UD22` selects one.

**Execution procedure:**

1. Build `src/cvd_mm/prototype.py` loading ONLY hash-verified frozen `PP####`/`FitStateHash`, `MODEL####`, `CalibratorHash`, `ThresholdVal`, and training-only `BackgroundHash` (refusing to execute on any SHA-256 mismatch!).
2. Emit structured JSON + optional local visualization containing: calibrated CVD risk score, frozen-threshold risk tier, explicit modality-presence flags (`Clinical/ECG/Lab/Lifestyle` present vs missing + uncertainty caveat), modality-level SHAP share, top tabular feature contributions, ECG attribution overlay, provenance hashes, and a persistent **research-only non-diagnostic disclaimer**.
3. Test all failure contracts using synthetic fixtures: complete 4-modality valid input, partial/missing-modality inputs (1–3 modalities missing), out-of-range units, corrupt ECG file, all-modalities-missing error, and model-hash mismatch error.
4. If (and ONLY if) `UD22` approves an interactive local dashboard or hosted defense interface: build a thin wrapper in `prototype_ui/` importing `src/cvd_mm/prototype.py` unchanged, verify numeric parity against CLI outputs within tolerance, enforce zero persistent PHI upload storage, use exclusively synthetic or IRB/disclosure-approved demo cases, and verify an offline local fallback.

**Planning/review prompt:**

> Review our research prototype contract (`UD22`) to ensure 100% behavioral parity with the `G11`-frozen, `G12`/`G14`-evaluated champion model, clean handling of missing modalities and corrupt inputs, zero PHI retention, and explicit non-diagnostic disclaimer wording.

**Implementation prompt:**

> Implement `src/cvd_mm/prototype.py`, thin CLI `14_Automation/predict_explain.py`, synthetic end-to-end demo inputs, and pytest error/parity tests. Never alter preprocessing, calibration, or thresholds to make demo outputs look prettier.

**Human-only actions and decisions:** Researchers and supervisor approve `UD22` interface choice; cardiologist approves explanation readability and research-only disclaimer; custodian approves any real de-identified demo profile (synthetic cases preferred).

**Version-control/artifact expectations:** Commit prototype code, synthetic demo inputs, tests, and guide to Git; keep real model weights in Tier 3 (loaded by pointer/hash) and never bundle patient PHI into any demo UI.

**Documentation updates:** `13_Documentation/prototype_guide.md`, `decisions.csv` (`UD22`), parity report (if UI built).

**Verification checklist:**

- [ ] Prototype verifies SHA-256 hashes of `PP`, `MODEL`, calibrator, and SHAP background at startup.
- [ ] Outputs include calibrated probability, modality-presence status, multimodal SHAP breakdown, provenance, and research-only disclaimer.
- [ ] All error-contract tests (missing modalities, corrupt ECG, invalid units, hash mismatch) pass on synthetic inputs.
- [ ] If optional `UD22` UI built: CLI parity verified, zero PHI stored, and offline defense fallback tested.

**Common mistakes:** Re-implementing scaling or lowering $\tau$ inside a dashboard to show more dramatic risk alerts; feeding real unconsented hospital patients into a live demo; claiming the prototype is a clinical diagnostic device.

**Recovery procedure:** Strip divergent UI logic, call `src/cvd_mm/prototype.py` verbatim, re-run parity & error tests, and update `prototype_guide.md`.

**Definition of Done:** Tested, hash-verified research prototype faithfully reproduces frozen calibrated predictions and SHAP explanations (with optional `UD22` parity/fallback if adopted). Universal DoD applies.

**Next step:** [STEP-042](#step-042)

---

<a id="step-042"></a>
## STEP-042 — Perform clean-environment reproducibility audit and pass `G15`

**Objective:** Verify from a genuinely fresh authorized environment—following written instructions alone—that frozen artifacts, metrics, calibration, statistical CIs, SHAP faithfulness curves, and representative figures reproduce within declared tolerances, and pass `G15`.

**Why this step exists:** Q1 reviewers and reproducibility chairs routinely audit code and artifact packages; catching missing dependencies, hidden local paths, or unrecorded state before writing prevents embarrassing post-submission retractions.

**Governing section references:** [OS §9](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §11](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-041` prototype & tests complete; `G12–G14` current PASS; locked `environment/data/` & `environment/model/` files and Tier 2B/3 artifact pointers intact.

**Estimated difficulty and time (provisional):** Hard; 4–8 hours active fresh-environment audit plus replay/retraining compute if Level B adopted.

**Parallelizable:** Artifact hash verification and clean environment build may proceed concurrently; replay comparisons follow installation.

**Inputs:** `13_Documentation/installation.md`, `pipeline.md`, `prototype_guide.md`, locked `environment/`, Tier 2B/3 manifests, frozen `EVAL####` & `XAI####` outputs, `T24` (`reproduce.md`).

**Expected outputs:** Verified `13_Documentation/reproduce.md`, `13_Documentation/data_access.md` (lawful controlled-access instructions for restricted primary hospital data + public synthetic pipeline replay), `13_Documentation/reproducibility_audit.md` (declaring exact verified Level A / Level B / Level C agreement and tolerances), and `G15` assessment.

**Repository/file changes:** Create `13_Documentation/reproduce.md`, `data_access.md`, `reproducibility_audit.md`, and `01_Project_Management/reviews/G15_assessment_<date>.md`; update `gates.csv`.

**Execution procedure:**

1. Provision a genuinely fresh environment (clean conda/venv or container) on an authorized IRB-compliant machine using **strictly** the commands written in `13_Documentation/installation.md` and `reproduce.md`—zero reliance on hidden shell variables, unlogged local files, or notebook memory!
2. Retrieve `REL####`, `PP`/`FitStateHash`, `MODEL####`, `CalibratorHash`, and `BackgroundHash` solely by manifest pointers, verifying 100% of SHA-256 checksums.
3. **Level A Replay (Mandatory):** Re-execute frozen test inference, all 6 mandatory metrics + PR-AUC/Brier/ECE/slope, DCA, DeLong/bootstrap CIs, SHAP values, Deletion/Insertion AOPC, and prototype smoke runs—comparing regenerated values against archived `EVAL####`/`XAI####` within pre-declared numeric tolerances.
4. **Level B Retraining (if feasible/adopted):** Re-run one full champion seed from `REL####` recording observed hardware nondeterminism vs archived run; ALSO verify that an external Q1 reviewer WITHOUT hospital data can run the complete pipeline end-to-end on the bundled synthetic 4-modality dataset; then audit and record `G15`.

**Planning/review prompt:**

> Audit `reproducibility_audit.md` and `data_access.md` against `G15` and Q1 journal Code/Data Availability policies. Clearly distinguish verified Level A replay, Level B retraining variance, public synthetic end-to-end replay, and IRB-restricted primary cohort access.

**Implementation prompt:**

> Execute the clean-environment reproduction checklist verbatim, logging exact shell commands, verified SHA-256 outputs, observed numeric deltas vs archived `EVAL####`/`XAI####`, and synthetic external-reviewer replay results in `reproducibility_audit.md`. Never silently patch archived numbers to force agreement.

**Human-only actions and decisions:** Reproduction reviewer (ideally the team member who did NOT author the given script, or supervisor/external lab peer) verifies clean replay evidence and signs `G15`.

**Version-control/artifact expectations:** Commit `reproduce.md`, `data_access.md`, `reproducibility_audit.md`, and `G15` audit to Git; keep restricted data strictly in Tier 2B.

**Documentation updates:** `13_Documentation/reproduce.md`, `data_access.md`, `reproducibility_audit.md`, `gates.csv`, `dashboard.md`.

**Verification checklist:**

- [ ] Clean environment built solely from documented installation lock files.
- [ ] All retrieved parent/model/calibrator/background SHA-256 checksums match archived manifests.
- [ ] Level A metrics, calibration, stats, DCA, and SHAP/AOPC reproduce within pre-declared tolerances (any Level B variance honestly reported).
- [ ] Public synthetic 4-modality replay succeeds end-to-end; `G15` PASS signed with explicit access limits.

**Common mistakes:** Testing reproducibility inside the original messy development environment; promising "100% public data release" when IRB prohibits publishing hospital patient records; conflating inference replay with bitwise GPU retraining determinism.

**Recovery procedure:** Identify missing dependency, hardcoded path, or unseeded operation, fix cleanly with versioned code/doc patches, re-verify affected `EVAL`/`XAI` if scientific output changed, and repeat `G15` audit.

**Definition of Done:** `G15` PASS with independently followable reproduction guide, verified Level A replay, synthetic external-reviewer pipeline proof, and lawful data-access statement. Universal DoD applies.

**Next step:** [STEP-043](#step-043)

---

<a id="step-043"></a>
## STEP-043 — Build writing evidence map, Q1 target-journal plan, and TRIPOD+AI matrix

**Objective:** Map every FYDP thesis chapter and Q1 journal manuscript section to verified evidence IDs, actual DIU CSE499 & Q1 journal author guidelines, authorship agreements (`UD23`), and every **TRIPOD+AI (2024)** checklist item.

**Why this step exists:** Writing directly from memory breeds mismatched numbers, missing TRIPOD+AI disclosures, wrong journal formatting, and unsupported clinical hype.

**Governing section references:** [OS §3](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS §10](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §15](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-15); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-042` complete; `G03`, `G12–G15` current PASS; complete verified literature, `EVAL####`, `XAI####`, and `PROBAST_AI.md` available.

**Estimated difficulty and time (provisional):** Moderate; 4–6 hours plus supervisor & author agreement.

**Parallelizable:** Retrieving DIU FYDP thesis format guidelines and auditing Q1 target journal instructions (word limits, figure specs, ethics/data/code templates) can proceed concurrently.

**Inputs:** Approved RQs, `claims.csv`, `EVAL####/report.md`, `error_probast.md`, `XAI####/report.md`, `reproducibility_audit.md`, actual DIU FYDP rules, target Q1 journal guidelines, `T27` (`tripod_ai_checklist.md`), `UD23`.

**Expected outputs:** Populated `12_Writing/writing_registry.csv`, `12_Writing/writing_plan.md`, Q1 target-journal shortlist & primary venue choice (`UD23`), initialized `12_Writing/checklists/TRIPOD_AI.csv` mapping every applicable item to manuscript sections and artifact IDs, and signed CRediT authorship agreement (`DEC####`).

**Repository/file changes:** Create `12_Writing/writing_plan.md`, `12_Writing/checklists/TRIPOD_AI.csv`, `12_Writing/thesis/requirements.md`, `12_Writing/paper_q1/venue_requirements.md`; populate `writing_registry.csv` and `decisions.csv` (`UD23`).

**Execution procedure:**

1. Collect actual DIU CSE499 FYDP thesis formatting instructions, required declarations, defense schedule, and page/citation conventions.
2. Shortlist 2–3 realistic **Q1 target journals** aligned to actual study scope & evidence strength (e.g., *IEEE Journal of Biomedical and Health Informatics*, *Computers in Biology and Medicine*, *Artificial Intelligence in Medicine*, *Journal of Biomedical Informatics*, *Information Fusion*, *npj Digital Medicine*), inspecting real journal aims/scope, word/figure limits, structured abstract format, open-access/APC policy, and mandatory reporting checklists (`UD23`).
3. Map every thesis chapter and Q1 paper section (`WR####`) to exact verified `CLAIM`, `P`, `DS`/`ADJ`, `EXP`, `EVAL`, `XAI`, `FIG`, and `TAB` IDs—plus map 100% of applicable **TRIPOD+AI (2024)** items in `12_Writing/checklists/TRIPOD_AI.csv` and PRISMA search flow numbers in `12_Writing/checklists/PRISMA.md`.
4. Finalize authorship order, CRediT roles (including collaborating cardiologist/clinical adjudicator and supervisor per ICMJE authorship criteria!), competing interests, funding/ethics declarations, and Q1 submission timeline/disposition (`UD23`).

**Planning/review prompt:**

> Build a unified evidence-first writing map for both the DIU FYDP thesis and our selected Q1 journal venue. Audit all 27 TRIPOD+AI (2024) items against our verified artifacts and surface any missing reporting detail before drafting begins.

**Implementation prompt:**

> Documentation only: populate `writing_registry.csv`, `writing_plan.md`, `TRIPOD_AI.csv`, and venue requirement summaries linking exact verified IDs. Never pre-fill draft prose or fabricate missing evidence.

**Human-only actions and decisions:** Supervisor Md. Mizanur Rahman, Rayan Ahmed, Mohammad Nafis Sadiq, and clinical collaborators finalize `UD23` (Q1 target journal, ICMJE authorship & CRediT roles, FYDP deadlines, and Q1 submission schedule).

**Version-control/artifact expectations:** Commit `writing: lock evidence map, Q1 venue plan, authorship and TRIPOD+AI matrix`.

**Documentation updates:** `writing_registry.csv`, `writing_plan.md`, `TRIPOD_AI.csv`, `decisions.csv` (`UD23`).

**Verification checklist:**

- [ ] Every planned thesis and Q1 manuscript claim links directly to verified `P`/`EVAL`/`XAI`/`FIG`/`TAB` IDs.
- [ ] Actual DIU FYDP thesis rules and selected Q1 journal author guidelines archived.
- [ ] Every applicable TRIPOD+AI (2024) item mapped to target section and evidence artifact.
- [ ] ICMJE authorship order, CRediT roles, and Q1 publication obligation explicitly approved (`UD23`).

**Common mistakes:** Picking a Q1 journal without checking APC fees or clinical-validation scope requirements; forgetting ICMJE authorship criteria for clinical adjudicators; maintaining separate conflicting bibliographies for thesis and paper.

**Recovery procedure:** Adjust venue choice or section map with supervisor approval, resolve any missing TRIPOD+AI disclosure from existing audited records, and update `writing_plan.md` prior to drafting.

**Definition of Done:** Approved unified writing plan, Q1 venue rules, ICMJE authorship, and TRIPOD+AI evidence matrix ready for drafting. Universal DoD applies.

**Next step:** [STEP-044](#step-044)

---

<a id="step-044"></a>
## STEP-044 — Draft FYDP thesis chapters from realized evidence

**Objective:** Author all complete DIU CSE499 FYDP thesis chapters strictly from verified evidence, documenting realized methods, complete results, quantitative XAI, limitations, and prototype architecture.

**Why this step exists:** The final thesis must transparently report what was actually executed and measured—never recycling future-tense proposal guesses or omitting negative comparisons.

**Governing section references:** [OS §10](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-043` approved writing map & DIU thesis format; `G03`, `G12–G15` current PASS.

**Estimated difficulty and time (provisional):** Hard; 3–6 hours per chapter session, repeated across full thesis (typically 1–2 weeks).

**Parallelizable:** Distinct chapters (Introduction/Background, Systematic Literature & Gap Verification, Cohort/Schema/Leakage-Safe Methodology, Modeling/Experiments, Evaluation/Calibration/Stats, Multimodal XAI Faithfulness, Prototype/Reproducibility, Discussion/Limitations/Conclusion) may be split between Rayan Ahmed and Mohammad Nafis Sadiq using one canonical glossary and `references.bib`, followed by unified editorial integration.

**Inputs:** `writing_plan.md`, `02_Literature/synthesis.md` & `references.bib`, `DS####_card.md`, `endpoint_charter.md`, `PP`/`SPLIT`/`REL` reports, `EVAL####/report.md`, `error_probast.md`, `XAI####/report.md`, `prototype_guide.md`, `reproducibility_audit.md`, `T26` (`writing_unit.md`).

**Expected outputs:** Complete chapter drafts in `12_Writing/thesis/`, evidence-backed Abstract & Conclusion, appendices (CRF/variable dictionary summary, config contract, ethics/reproducibility notes), and updated `writing_registry.csv`.

**Repository/file changes:** Create chapter files under `12_Writing/thesis/` (LaTeX/Overleaf-synced `.tex` or structured Markdown/DOCX source per DIU template); update `12_Writing/writing_registry.csv` and `claims.csv`.

**Execution procedure:**

1. Draft **Introduction & Literature Review** strictly from `STEP-004`–`009` verified extractions, presenting PRISMA flow, honest evaluation of `PG1–PG5` (including narrowed/refuted nuances), and approved RQs (`RQ1–RQ4`).
2. Draft **Cohort, Clinical Schema & Leakage-Safe Methodology** explicitly documenting IRB approval, $t_0/\Delta t$ alignment, 4-modality schema & ECG specs, resolution of the proposal Workflow Diagram leakage boundary (`RF13`), patient-level splitting, 4-tier comparator architecture, and preregistered calibration/statistical/XAI protocols.
3. Draft **Results & Explainability** faithfully pulling all 6 mandatory proposal metrics + PR-AUC, Brier/ECE/slope, DCA, bootstrap 95% CIs, multiplicity-adjusted DeLong/McNemar $p$-values, progressive & LOMO ablations, missing-modality stress tests, subgroup fairness, multimodal SHAP + Deletion/Insertion AOPC + multi-seed stability + shortcut audit + cardiologist review—preserving every negative/null finding.
4. Draft **Prototype, Reproducibility, Discussion, PROBAST-AI Limitations, Conclusion, and Abstract** ensuring strict clinical claim boundaries (supplementary research decision-support, zero causal SHAP claims, zero unproven clinician-trust claims).

**Planning/review prompt:**

> Draft chapter `WR####` strictly from linked verified evidence (`EVAL####`, `XAI####`, `P####`). Preserve exact past-tense realized methods, flag any unresolved detail as `Evidence pending`, separate observations from biological hypotheses, and enforce strict clinical/XAI claim boundaries.

**Implementation prompt:**

> Authoring task: save versioned thesis chapter source under `12_Writing/thesis/` linked to `02_Literature/references.bib` and update `writing_registry.csv`. Zero fabricated citations, smoothed metrics, or copy-pasted future-tense proposal claims.

**Human-only actions and decisions:** Rayan Ahmed and Mohammad Nafis Sadiq own scientific authorship and co-review every chapter for voice consistency; supervisor reviews milestone chapters.

**Version-control/artifact expectations:** Commit coherent chapter milestones (`writing: draft FYDP thesis chapters 1-N`); keep compiled binary PDFs out of Git until final versioned snapshots or store in Tier 3.

**Documentation updates:** `writing_registry.csv`, `claims.csv`, terminology/acronym consistency check against OS Appendices D–E.

**Verification checklist:**

- [ ] All DIU required chapters, front matter, references, and appendices drafted completely.
- [ ] Methods match actual frozen configs, counts, and leakage controls (past tense realized science).
- [ ] All 6 mandatory metrics, Q1 extensions, ablations, negative results, and quantitative XAI results accurately reported.
- [ ] Zero invented citations or overclaimed clinical/causal wording.

**Common mistakes:** Leaving future-tense text from `fydp_title_proposal.pdf` ("A primary dataset will be collected..."); claiming SHAP proves causality or increases doctor trust; omitting unfavorable unimodal/ablation comparisons.

**Recovery procedure:** Replace any ungrounded paragraph with verified artifact values or narrow the claim honestly, reconciling across Abstract, Results, and Conclusion.

**Definition of Done:** Complete, evidence-grounded FYDP thesis draft assembled and ready for Q1 visual generation and 100% claim/citation audit. Universal DoD applies.

**Next step:** [STEP-045](#step-045)

---

<a id="step-045"></a>
## STEP-045 — Generate Q1 publication figures/tables and audit 100% of citations & claims

**Objective:** Script-generate all publication-grade vector/high-DPI figures (`FIG####`) and formatted tables (`TAB####`) directly from locked data/EVAL/XAI CSVs, and perform a 100% line-by-line citation, numerical, and claim audit.

**Why this step exists:** Discrepant numbers between Abstract, Tables, and Figures—or low-resolution screenshots, unverified citations, or accidentally leaked ECG headers—trigger immediate negative reviews at Q1 journals.

**Governing section references:** [OS §3](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-03); [OS §10](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §15](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-15); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-044` complete thesis draft; locked `DS`/`ADJ`/`EVAL`/`XAI` CSV outputs; IRB/disclosure clearance for any illustrative de-identified ECG/SHAP patient figure.

**Estimated difficulty and time (provisional):** Hard; 6–10 hours across figure engineering, citation verification, and full numerical cross-check.

**Parallelizable:** Figure-generation scripting, LaTeX/Markdown table formatting, and line-by-line DOI/citation auditing can proceed concurrently; final issue reconciliation is unified.

**Inputs:** Thesis draft, `02_Literature/references.bib` & `papers.csv`, `claims.csv`, locked `EVAL####` & `XAI####` CSVs, `T23` (`figure_table.md`).

**Expected outputs:** Publication-grade figures (`FIG0001–FIG0006+`, vector PDF/SVG + 300–600 DPI PNG/TIFF, colorblind-safe), verified formatted tables (`TAB0001+`), populated `11_Figures_Tables/assets.csv`, 100% verified citation & numerical consistency audit report (`12_Writing/reviews/claim_citation_audit.md`), and zero-PHI visual clearance.

**Repository/file changes:** Populate `11_Figures_Tables/specs/`, `data/` (safe aggregated CSVs), `rendered/`, `assets.csv`, plotting scripts under `14_Automation/make_figures.py`; update `12_Writing/thesis/`, `claims.csv`, and `12_Writing/reviews/claim_citation_audit.md`.

**Execution procedure:**

1. Script-generate core Q1 visual assets directly from locked CSVs (`make_figures.py`):
   - `FIG0001`: STARD/CONSORT-style cohort recruitment, exclusion, 4-modality availability & patient-level split flow diagram;
   - `FIG0002`: Leakage-safe Transformer-based Multimodal Fusion & SHAP architecture schematic;
   - `FIG0003`: 4-panel held-out evaluation figure (ROC with 95% CIs, PR curves with prevalence baseline, Calibration Reliability Diagrams, Decision Curve Analysis Net Benefit);
   - `FIG0004`: Progressive Modality Addition, Leave-One-Modality-Out (LOMO), and Missing-Modality Degradation curves;
   - `FIG0005`: Multimodal XAI figure (Modality SHAP share, Global tabular beeswarm/dependence plots, and IRB-cleared de-identified TP/FP/FN local waterfall + ECG attribution overlay);
   - `FIG0006`: Quantitative XAI Faithfulness (Deletion & Insertion curves vs random control) and Multi-Seed Stability analysis.
2. Generate core Q1 tables (`TAB0001`: Baseline cohort characteristics by CVD status & missingness; `TAB0002`: Tier 1–4 main held-out comparison with all 6 mandatory metrics + PR-AUC + Brier/ECE + 95% CIs + adjusted DeLong $p$; `TAB0003`: Modality & architectural ablations; `TAB0004`: Subgroup fairness & missing-modality stress tests; `TAB0005`: Quantitative XAI faithfulness, stability & clinician plausibility summary; `TAB0006`: Contextual comparison vs verified prior literature explicitly noting non-comparability of distinct cohorts).
3. Inspect every rendered figure visually for legible fonts, units, confidence bands, colorblind safety, and **zero residual PHI** (especially inside any illustrative ECG waveform trace!).
4. Run a 100% audit verifying: every citation key resolves to a publisher-verified (`MetadataVerified=yes`) entry in `02_Literature/references.bib`; every empirical number in Abstract, Text, Tables, and Figures matches locked `EVAL`/`XAI` CSVs identically; zero `Evidence pending` placeholders remain.

**Planning/review prompt:**

> Audit every rendered figure (`FIG####`), table (`TAB####`), numerical claim, and bibliography entry in our thesis draft. Flag any rounding inconsistency across Abstract/Tables/Text, unreadable axis, unverified DOI, PHI risk in ECG figures, or unsupported clinical/XAI assertion.

**Implementation prompt:**

> Write reproducible `14_Automation/make_figures.py` reading strictly from locked safe CSVs to render vector/high-DPI `FIG####` assets and populate `11_Figures_Tables/assets.csv`. Run automated citation-key and numerical cross-check scripts outputting `claim_citation_audit.md`. Never hand-edit plotted coordinates.

**Human-only actions and decisions:** Both authors visually inspect every figure/table; cardiologist checks clinical accuracy and zero-PHI clearance of ECG/SHAP visual panels; supervisor verifies claim boundaries.

**Version-control/artifact expectations:** Commit `make_figures.py`, asset specs, safe plot CSVs, `assets.csv`, verified vector assets, and `claim_citation_audit.md` to Git.

**Documentation updates:** `assets.csv`, `claims.csv`, `writing_registry.csv`, `claim_citation_audit.md`.

**Verification checklist:**

- [ ] Every `FIG####` and `TAB####` generated programmatically with recorded command, source hash, units, and caption.
- [ ] All rendered visuals inspected for legibility, 300–600 DPI/vector quality, colorblind safety, and zero PHI.
- [ ] 100% of citations verified against publisher full texts (`MetadataVerified=yes`).
- [ ] Every number in Abstract, body prose, Tables, and Figures reconciles identically; zero `Evidence pending` markers survive.

**Common mistakes:** Screenshotting Jupyter notebook plots at 72 DPI; hand-typing table cells and creating discrepancies with Abstract; leaving patient timestamp/ID in the corner of an ECG figure; citing a paper from someone else's reference list without reading it.

**Recovery procedure:** Fix plotting/table scripts cleanly, regenerate assets with updated hashes, correct mismatched prose or unverified citations across all chapters, and re-run `claim_citation_audit.md`.

**Definition of Done:** All Q1-caliber visual assets, tables, citations, and numerical claims verified 100% consistent and PHI-safe. Universal DoD applies.

**Next step:** [STEP-046](#step-046)

---

<a id="step-046"></a>
## STEP-046 — Complete supervisor review and pass thesis submission readiness (`G16 / thesis`)

**Objective:** Incorporate actual supervisor feedback on the full FYDP thesis, verify DIU CSE499 institutional formatting and similarity/ethics declarations, compile the submission PDF, and pass document-scoped `G16 / thesis`.

**Why this step exists:** Thesis submission readiness requires real supervisor sign-off, clean rendering inspection, and institutional compliance—assessed independently so thesis deadlines are never stalled by Q1 journal submission scheduling.

**Governing section references:** [OS §10](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-045` asset/claim/citation audit passed; `G03`, `G12–G15` current PASS; actual DIU CSE499 format/submission checklist available.

**Estimated difficulty and time (provisional):** Hard; 4–8 hours per revision cycle plus supervisor review turnaround.

**Parallelizable:** Institutional formatting/reference polishing can run concurrently across both researchers; final `G16 / thesis` sign-off waits for supervisor approval.

**Inputs:** Verified thesis draft & assets (`STEP-045`), actual supervisor review comments, DIU CSE499 formatting/plagiarism/ethics guidelines, `T25` (`review_response.md`).

**Expected outputs:** Point-by-point supervisor review-response ledger, clean compiled final thesis PDF with verified SHA-256, institutional compliance check, and document-scoped `G16 / thesis` assessment.

**Repository/file changes:** Update `12_Writing/thesis/`, write `12_Writing/reviews/supervisor_thesis_responses.md`, `01_Project_Management/reviews/G16_thesis_assessment_<date>.md`; update `writing_registry.csv` and `gates.csv` (`DocumentOrEntityScope=thesis`).

**Execution procedure:**

1. Deliver the complete verified thesis draft to Supervisor Md. Mizanur Rahman and log every received comment verbatim in `supervisor_thesis_responses.md` (`T25`).
2. Address editorial/structural revisions directly; if any substantive methodological/experimental revision is requested, route it properly back through gated steps (`STEP-028`–`045`) with new IDs rather than ad-hoc edits.
3. Compile the final DIU-formatted thesis PDF and inspect every single page visually (cover/approval form attachment per `RF18`, TOC/LOF/LOT pagination, margins, figure resolution, equation rendering, references, appendices, IRB/ethics statement, similarity check if required).
4. Record compiled PDF SHA-256, verify all `G16 / thesis` mandatory criteria, and obtain formal supervisor + author sign-off (`G16 / thesis` PASS).

**Planning/review prompt:**

> Audit our revised FYDP thesis PDF and `supervisor_thesis_responses.md` against DIU CSE499 rules and `G16 / thesis` criteria. Distinguish resolved editorial changes from any item requiring new scientific evidence.

**Implementation prompt:**

> Apply approved revisions, compile final thesis PDF, compute its SHA-256 hash, inspect formatting/cross-references, and save evidenced `G16 / thesis` assessment (keeping `G16 / paper` completely separate for `STEP-048`).

**Human-only actions and decisions:** Supervisor Md. Mizanur Rahman reviews and formally authorizes thesis submission; both student authors verify declarations and signatures.

**Version-control/artifact expectations:** Commit final thesis sources, `supervisor_thesis_responses.md`, compiled PDF hash, and `G16 / thesis` audit to Git; store exact compiled PDF immutably in Tier 3/4.

**Documentation updates:** `writing_registry.csv`, `supervisor_thesis_responses.md`, `gates.csv` (`G16 / thesis`), `dashboard.md`.

**Verification checklist:**

- [ ] Every substantive supervisor comment resolved and logged with exact diff/evidence.
- [ ] All DIU CSE499 format, cover/approval attachment (`RF18`), ethics, and declaration items checked.
- [ ] Every page of compiled final PDF visually inspected with zero broken refs or clipped figures.
- [ ] `G16 / thesis` PASS recorded with distinct `AssessmentID` and dated supervisor approval.

**Common mistakes:** Submitting a PDF without checking broken LaTeX `??` citations or clipped tables; conflating `G16 / thesis` with `G16 / paper`; claiming approval before supervisor signs off.

**Recovery procedure:** Keep `G16 / thesis` FAIL until blocking comments or formatting errors are repaired, re-compile cleanly, update hash, and obtain actual supervisor authorization before `STEP-047`.

**Definition of Done:** `G16 / thesis` PASS and hash-verified final FYDP thesis ready for official institutional submission. Universal DoD applies.

**Next step:** [STEP-047](#step-047)

---

<a id="step-047"></a>
## STEP-047 — Submit FYDP thesis and preserve immutable submission snapshot & receipt

**Objective:** Complete official Daffodil International University CSE499 thesis submission and archive the exact submitted PDF hash, defense materials, and confirmation receipt.

**Why this step exists:** A finalized local PDF is not a confirmed institutional submission; preserving exact submitted hashes prevents later confusion during defense revisions or archiving.

**Governing section references:** [OS §10](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §11](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-046` complete; `G16 / thesis` PASS; DIU submission portal/office procedure and required attachments known.

**Estimated difficulty and time (provisional):** Moderate; 1–3 hours plus institutional submission/defense scheduling.

**Parallelizable:** No for the submission event itself; Q1 manuscript adaptation (`STEP-048`) may begin concurrently from the exact same frozen evidence base.

**Inputs:** `G16 / thesis`-approved final PDF + SHA-256, signed Proposal Approval Form attachment (`RF18`), institutional declarations, `T28` (`submission.md`).

**Expected outputs:** Confirmed thesis submission record (`12_Writing/thesis/submission.md`), exact submitted PDF SHA-256 matching `G16 / thesis`, institutional confirmation/receipt preserved immutably, and defense presentation/prototype rehearsal log (including offline fallback if `UD22` demo used).

**Repository/file changes:** Create `12_Writing/thesis/submission.md`; store immutable submitted PDF & receipt in Tier 3/4 pending `STEP-049` archive; update `writing_registry.csv` and `dashboard.md`.

**Execution procedure:**

1. Re-verify compiled thesis PDF SHA-256 against the `G16 / thesis` approved hash and confirm all required forms/attachments (including signed Proposal Approval Form from `fydp_title_proposal.pdf` p.1 if departmental policy requires it!).
2. Authorized researchers execute official DIU CSE499 submission through the designated departmental portal/office.
3. Save actual institutional receipt/confirmation (timestamp, portal confirmation ID, or signed office receipt) and log exact status in `12_Writing/thesis/submission.md` (`T28`).
4. Keep the submitted snapshot strictly read-only; route any post-defense examiner revisions to a clearly versioned `thesis_v1.1_final` snapshot with logged responses (`T25`).

**Planning/review prompt:**

> Verify the DIU CSE499 thesis submission checklist against approved file hashes and departmental requirements, strictly distinguishing `READY`, `UPLOADED`, and `CONFIRMED_SUBMITTED`.

**Implementation prompt:**

> Record exact submitted file hashes, submission timestamp, and real institutional receipt pointer in `12_Writing/thesis/submission.md` without fabricating receipts or performing automated external uploads.

**Human-only actions and decisions:** Rayan Ahmed and Mohammad Nafis Sadiq execute official university submission and defense presentation; supervisor endorses required departmental forms.

**Version-control/artifact expectations:** Commit safe `submission.md` metadata and SHA-256 to Git; store exact submitted PDF and receipt immutably in Tier 3/4; tag source commit (`thesis-submitted-v1.0.0`) only after verified confirmation.

**Documentation updates:** `12_Writing/thesis/submission.md`, `writing_registry.csv`, `dashboard.md`.

**Verification checklist:**

- [ ] Submitted PDF SHA-256 matches `G16 / thesis` approved build identically.
- [ ] Actual institutional submission receipt/confirmation archived.
- [ ] Submission date, destination, and exact files recorded in `submission.md`.
- [ ] Submitted snapshot locked read-only (post-defense edits create new versions).

**Common mistakes:** Marking thesis "submitted" when only compiled locally; editing the submitted file in place after defense comments without versioning.

**Recovery procedure:** Resolve any departmental portal/formatting rejection cleanly, resubmit only as authorized, retain both submission snapshots and receipts, and update `submission.md`.

**Definition of Done:** Official FYDP thesis submission confirmed with immutable artifact hash and receipt. Universal DoD applies.

**Next step:** [STEP-048](#step-048)

---

<a id="step-048"></a>
## STEP-048 — Author Q1 journal manuscript, TRIPOD+AI package, pass `G16 / paper`, and submit/rebut

**Objective:** Adapt the single frozen evidence base into a crisp, high-impact Q1 journal manuscript accompanied by complete **TRIPOD+AI (2024)** & **PROBAST-AI** supplements, pass document-scoped `G16 / paper`, and complete verified Q1 submission (plus peer-review rebuttal tracking) OR record an explicit approved deferral disposition (`UD23`).

**Why this step exists:** Turning an FYDP thesis into a Q1 journal acceptance requires tighter scientific framing, full TRIPOD+AI/PROBAST-AI transparency, polished cover letter/highlights/code-availability statements, and rigorous point-by-point handling of peer reviewer critiques.

**Governing section references:** [OS §10](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §11](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-045` verified assets/claims & `STEP-047` thesis milestone (or concurrent after `STEP-045` if timeline permits); `G03`, `G12–G15` current PASS; `UD23` Q1 target journal & authorship finalized.

**Estimated difficulty and time (provisional):** Hard; 2–4 weeks of focused Q1 manuscript refinement + external peer-review cycles (turnaround unknown).

**Parallelizable:** Tightening Methods/Results prose, compiling `TRIPOD_AI.csv` page locators, formatting venue-specific LaTeX/Word templates, and preparing public synthetic-replay GitHub supplement can proceed in parallel; final author sign-off and `G16 / paper` are serialized.

**Inputs:** Frozen thesis evidence base (`EVAL####`, `XAI####`, `FIG0001–FIG0006`, `TAB0001–TAB0006`), `02_Literature/references.bib` (refreshed via living-review check before submission!), `PROBAST_AI.md`, `TRIPOD_AI.csv`, `data_access.md`, target Q1 journal author guide (`UD23`), `T25`, `T27`, `T28`.

**Expected outputs:** Venue-formatted Q1 manuscript (`12_Writing/paper_q1/`), structured abstract, Graphical Abstract / Highlights (if required), completed **TRIPOD+AI (2024) checklist** with exact manuscript line/page locators, **PROBAST-AI supplement**, ethics/IRB/CRediT/COI/Data-and-Code-Availability statements, persuasive cover letter, document-scoped `G16 / paper` PASS + verified Q1 journal submission receipt (and rebuttal ledger when reviews arrive) OR explicit approved deferral disposition.

**Repository/file changes:** Populate `12_Writing/paper_q1/` (manuscript, supplement, cover letter, `submission.md`), finalize `12_Writing/checklists/TRIPOD_AI.csv`, `12_Writing/reviews/journal_rebuttal_r1.md` (when reviews arrive), `01_Project_Management/reviews/G16_paper_assessment_<date>.md`; update `writing_registry.csv` and `gates.csv` (`DocumentOrEntityScope=paper_q1`).

**Execution procedure:**

1. Run a quick living-literature update search (`OS §3.4`) right before final submission to verify no brand-new landmark 4-modality CVD Transformer paper was missed; integrate any verified new comparator honestly.
2. Condense the frozen evidence into the target Q1 journal's exact template, word limit, and figure/table cap—maximizing scientific density: sharpened Q1 gap, leakage-free methodology, complete Tier 1–4 + LOMO/progressive ablations, calibration + DCA + multiplicity-adjusted DeLong/bootstrap stats, subgroup/missing-modality robustness, quantitative SHAP faithfulness (AOPC) + stability + shortcut audit + cardiologist review, and candid PROBAST-AI limitations.
3. Complete 100% of applicable **TRIPOD+AI (2024)** items in `TRIPOD_AI.csv` with exact manuscript page/section locators; prepare clean supplementary tables, ethical/IRB statement, CRediT author roles, Data & Code Availability statement (linking reproducible code + synthetic end-to-end demo + lawful controlled-access route for hospital data), and a clear Q1 Cover Letter highlighting scientific rigor rather than hype.
4. Assess **`G16 / paper`** under a separate `AssessmentID` in `gates.csv` (checking 100% claim/citation/figure parity, TRIPOD+AI completeness, journal format compliance, zero PHI, and unanimous co-author + supervisor + cardiologist approval). **Block external journal submission until `G16 / paper` PASS.** After PASS, have the designated corresponding author submit via the journal portal, preserve the exact submitted PDF/LaTeX bundle hash and manuscript ID/receipt, and track all subsequent peer-review comments & revisions cleanly via `T25` (routing any reviewer-requested new experiments through `STEP-028–030` with new `EXP`/`EVAL` IDs!). If Q1 submission is formally deferred past FYDP closure, log an explicit supervisor-approved disposition rather than a fictitious `G16 / paper` PASS.

**Planning/review prompt:**

> Critique our complete Q1 manuscript, `TRIPOD_AI.csv`, `PROBAST_AI.md`, and Cover Letter as an Associate Editor and three strict reviewers at our target Q1 journal. Identify any desk-rejection risk (missing IRB/TRIPOD item, overclaimed novelty/causality/trust, missing calibration/CIs, unaddressed confounding) before `G16 / paper`.

**Implementation prompt:**

> Assemble venue-compliant manuscript, finalized `TRIPOD_AI.csv` with exact page locators, supplementary package, and verified citation/number audit. Save evidenced `G16 / paper` assessment and record actual journal manuscript ID/receipt (or approved deferral disposition) in `12_Writing/paper_q1/submission.md`. Never claim submission without receipt or acceptance before editorial decision.

**Human-only actions and decisions:** All ICMJE co-authors (Rayan Ahmed, Mohammad Nafis Sadiq, clinical collaborators, Supervisor Md. Mizanur Rahman) approve final manuscript, authorship, COI declarations, and `G16 / paper`; designated corresponding author executes journal portal submission and leads peer-review rebuttals.

**Version-control/artifact expectations:** Commit final Q1 manuscript sources, `TRIPOD_AI.csv`, `PROBAST_AI.md`, `submission.md` receipt metadata, and `G16 / paper` audit to Git; archive exact submitted PDF/bundle immutably per revision round (`v1_submitted`, `v2_R1_revised`, etc.).

**Documentation updates:** `writing_registry.csv`, `TRIPOD_AI.csv`, `12_Writing/paper_q1/submission.md`, `gates.csv` (`G16 / paper`), `dashboard.md`.

**Verification checklist:**

- [ ] Living-literature cutoff updated and every citation 100% publisher-verified.
- [ ] Every empirical number, CI, $p$-value, ablation, and SHAP AOPC value matches locked `EVAL`/`XAI` CSVs identically.
- [ ] 100% of applicable TRIPOD+AI (2024) items completed with exact locators; PROBAST-AI, IRB/consent, CRediT, and Data/Code Availability statements included.
- [ ] Separate `G16 / paper` PASS recorded with unanimous author/supervisor approval prior to submission (or explicit approved deferral disposition logged without false PASS); submission strictly distinguished from editorial acceptance.

**Common mistakes:** Submitting a raw thesis copy-paste exceeding journal word limits; omitting TRIPOD+AI checklist or IRB protocol number; making `G17` FYDP completion wait indefinitely on 6-month journal peer review; editing submitted files without versioning across R1/R2 revisions.

**Recovery procedure:** Keep `G16 / paper` FAIL until all journal format, TRIPOD+AI, or claim issues are fixed; if rejected/desk-rejected by target venue #1, archive decision letter transparently (`12_Writing/reviews/`), incorporate valid editorial critiques, update `venue_requirements.md` for target venue #2, re-verify `G16 / paper`, and resubmit cleanly.

**Definition of Done:** Approved Q1 publication obligation fulfilled via `G16 / paper` PASS + verified journal submission receipt (with active rebuttal workflow), OR explicit supervisor-approved deferral disposition without fictitious PASS. Universal DoD applies.

**Next step:** [STEP-049](#step-049)

---

<a id="step-049"></a>
## STEP-049 — Create tiered immutable release archives and verify restoration

**Objective:** Package immutable, hash-verified release archives across all storage tiers—strictly segregating IRB-restricted hospital clinical/ECG data from public-permitted Q1 companion code/synthetic-demo artifacts—and prove recoverability via actual restore tests.

**Why this step exists:** Finished theses and journal submissions rapidly become unrecoverable—or risk catastrophic PHI breaches—unless restricted data, trained checkpoints, fitted preprocessors, submissions, and public code releases are cleanly segregated, hashed, and restore-tested.

**Governing section references:** [OS §9](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-09); [OS §10](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §11](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-047` thesis receipt and `STEP-048` Q1 paper receipt or approved disposition; `UD25` licensing, public-subset clearance, retention, and custodian ownership decisions approved; `G01–G16` current.

**Estimated difficulty and time (provisional):** Hard; 4–8 hours plus encrypted transfer and restore verification.

**Parallelizable:** Tier 1 public-code/synthetic-demo audit and Tier 2B/3 restricted clinical/checkpoint inventory may run concurrently; consolidated `ARCH####` manifest and restore verification are unified.

**Inputs:** Complete Git history, locked `environment/`, `DS`/`ADJ`/`SPLIT`/`PP`/`REL` restricted manifests, `MODEL`/`CKPT`/`Calibrator`/`Background` binaries, `EVAL`/`XAI` reports, submitted thesis & Q1 paper snapshots + receipts, `T29` (`archive.md`), `UD25`.

**Expected outputs:** Immutable `ARCH####` release manifest (`16_Archive/archive_manifest.csv` & `ARCH####.md`), verified Git release tag, segregated public Q1 companion code + synthetic demo bundle (if IRB/license approved under `UD25`), encrypted restricted clinical/model retention archive with custodian schedule, and documented **executed restore-test proof**.

**Repository/file changes:** Populate `16_Archive/archive_manifest.csv`, `16_Archive/ARCH####.md`, `16_Archive/restore_verification_<date>.md`; add approved `LICENSE` (if `UD25` selects open-source code license); tag verified Git revision.

**Execution procedure:**

1. Inventory every final deliverable across Tiers 1–4 with exact version, SHA-256 hash, byte size, license, PHI classification (`PUBLIC_CODE`, `RESTRICTED_DEIDENTIFIED_CLINICAL`, `ENCRYPTED_PHI_VAULT`), and IRB retention/destruction date (`UD25`).
2. **Strict PHI segregation audit:** Verify with 100% certainty that any public Q1 journal code repository (`GitHub`/`Zenodo`) contains **ONLY** clean source code, pinned environment locks, blank templates, safe aggregate metrics/specs, and synthetic demo fixtures—ZERO real hospital records, ZERO raw/filtered patient ECGs, ZERO PHI linkage tables, ZERO secrets, and ZERO unlicensed weights!
3. Create immutable `ARCH####` snapshots across restricted encrypted storage (preserving raw `DS`, adjudicated `ADJ`, `SPLIT`, fitted `PP`, `REL`, `MODEL`/`CKPT`, `EVAL`/`XAI`, submitted thesis & Q1 PDFs + receipts) and tag the exact Git commit (`v1.0.0-archive`).
4. **Actual restore verification:** Restore a representative set (Git tag + `environment/` + one `REL` manifest + champion `MODEL`/`CKPT`/`Calibrator` + `EVAL`/`XAI` metrics + submitted PDFs) to a clean temporary verification location, verify 100% SHA-256 matches, record observed results in `restore_verification_<date>.md`, and document post-project Tier 2A/2B custodian ownership and IRB destruction/retention schedule.

**Planning/review prompt:**

> Audit our `ARCH####` release manifest and public-vs-restricted segregation plan against `UD05` (IRB rules), `UD25` (licenses/retention), and Q1 journal artifact-archiving guidelines. Verify zero PHI risk in public bundles and concrete restore-test coverage.

**Implementation prompt:**

> Generate immutable `ARCH####` manifests and SHA-256 inventories, audit public-subset files for zero PHI/secrets, execute the real restore verification drill, and record verified checksums in `16_Archive/archive_manifest.csv` and `restore_verification_<date>.md`. Never overwrite an earlier `ARCH####`.

**Human-only actions and decisions:** Hospital custodian, IRB compliance lead (where applicable), supervisor, and researchers approve `UD25` licensing, public-release subset, encrypted Tier 2A/2B custody handover, and retention/destruction dates.

**Version-control/artifact expectations:** Tag verified Git release; commit `archive_manifest.csv`, `ARCH####.md`, and `restore_verification_<date>.md` to Git; keep restricted clinical/model archives strictly in encrypted institutional/approved storage with independent backup.

**Documentation updates:** `16_Archive/archive_manifest.csv`, `ARCH####.md`, `restore_verification_<date>.md`, `decisions.csv` (`UD25`), `13_Documentation/data_access.md`.

**Verification checklist:**

- [ ] Every final deliverable and parent dependency inventoried with SHA-256, license, and PHI tier.
- [ ] Public companion code/synthetic bundle audited 100% free of PHI, real ECGs, secrets, and unlicensed binaries.
- [ ] Actual restore verification drill executed and passed with matching SHA-256 hashes.
- [ ] Custodian handover, retention period, and IRB destruction schedule formally recorded (`UD25`).

**Common mistakes:** Archiving only the final thesis PDF while losing fitted preprocessors, calibrators, and training-only SHAP background files; accidentally pushing a small sample CSV of real hospital patients into the public Q1 GitHub repo; relying on expiring cloud share links as the sole archive.

**Recovery procedure:** Pull down any misclassified public artifact immediately under `OS §11.4` incident rules, retrieve missing binaries from Tier 3 backups, replace temporary links with durable institutional/versioned storage, re-run restore verification, and log a superseding `ARCH####`.

**Definition of Done:** Lawful, PHI-segregated, immutable `ARCH####` release archive created and proven recoverable via executed restore tests. Universal DoD applies.

**Next step:** [STEP-050](#step-050)

---

<a id="step-050"></a>
## STEP-050 — Perform final project-completion audit and pass `G17`

**Objective:** Conduct the end-to-end audit verifying every approved scientific, ethical, Q1-writing, reproducibility, and archival deliverable across `G01–G16`, hand over post-project stewardship (including ongoing Q1 peer-review tracking), and pass `G17`.

**Why this step exists:** Planning completeness, model training, thesis submission, Q1 submission, and lawful archiving are distinct accomplishments; project closure requires evidence across every obligation without inventing unproven clinical outcomes or journal acceptance.

**Governing section references:** [OS §1](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-01); [OS §10](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-10); [OS §11](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-11); [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14); [OS Appendix A](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-a).

**Prerequisites:** `STEP-049` archive & restore proof verified; all applicable gates `G01–G16` current `PASS` (including `G10` for every qualifying reported experiment, `G16 / thesis`, and `G16 / paper` or approved disposition); thesis receipt and Q1 paper receipt/disposition archived.

**Estimated difficulty and time (provisional):** Moderate to hard; 3–5 hours plus supervisor final sign-off.

**Parallelizable:** Automated cross-registry foreign-key and deliverable checks can run independently; final `G17` completion sign-off is serialized.

**Inputs:** Complete `gates.csv`, all 22 canonical registries, `16_Archive/archive_manifest.csv`, `restore_verification_<date>.md`, `thesis/submission.md`, `paper_q1/submission.md`, `PROBAST_AI.md`, `TRIPOD_AI.csv`.

**Expected outputs:** Final `01_Project_Management/reviews/project_completion_audit.md`, finalized `dashboard.md`, post-project stewardship & Q1 peer-review handover record, and `G17` assessment bound to `ARCH####`.

**Repository/file changes:** Create `01_Project_Management/reviews/project_completion_audit.md` and `G17_assessment_<date>.md`; update `gates.csv`, `dashboard.md`, and append final completion pointer to `16_Archive/archive_manifest.csv`.

**Execution procedure:**

1. Run automated cross-registry integrity verification (`14_Automation/validate_repo.py`) confirming zero broken foreign keys across all 22 CSV registries (`DS → ADJ → SPLIT → PP → REL → EXP → CKPT/MODEL → EVAL → XAI → FIG/TAB → CLAIM → WR → ARCH`).
2. Audit every gate `G01–G16` confirming current `PASS` for the exact final entity versions (zero `STALE` or unassessed mandatory gates; `G10` verified per qualifying experiment; `G16 / thesis` + `G16 / paper` or approved deferral verified).
3. Verify every deliverable exists with recoverable evidence: IRB/ethics records, immutable 4-modality cohort & adjudication records, leakage-free release, complete Tier 1–4 + ablation experiments (including negative results), calibrated statistical/DCA evaluation, PROBAST-AI limitations, quantitatively faithful & clinician-reviewed SHAP audit, clean reproducibility audit, research prototype (plus `UD22` parity/fallback if adopted), FYDP thesis receipt, Q1 manuscript + TRIPOD+AI submission receipt or approved disposition, and verified `ARCH####` restore proof.
4. Record formal supervisor + researcher `G17` completion sign-off and clearly separate non-blocking future work (ongoing Q1 R1/R2 journal peer review, future prospective multi-center longitudinal clinical validation trial, or IRB-approved clinician reader/usability trial) without pretending those future studies are complete.

**Planning/review prompt:**

> Audit the entire CVD multimodal project against `CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md` §14 and all 17 gates (`G01–G17`). Report itemized PASS/FAIL evidence per deliverable strictly on scientific validity and obligation completion—never on hoped-for superiority or journal acceptance.

**Implementation prompt:**

> Run full automated registry foreign-key and deliverable hash verification, compile evidence-backed `project_completion_audit.md`, update `dashboard.md` strictly after actual `G17` sign-off, and bind final audit hashes to `16_Archive/`.

**Human-only actions and decisions:** Supervisor Md. Mizanur Rahman and researchers Rayan Ahmed & Mohammad Nafis Sadiq ratify `G17` project completion and post-project stewardship/Q1-rebuttal ownership.

**Version-control/artifact expectations:** Commit final completion audit, `gates.csv`, and `dashboard.md`; link cleanly to `ARCH####` without deleting any historical failed or negative run.

**Documentation updates:** `project_completion_audit.md`, `G17_assessment_<date>.md`, `gates.csv`, `dashboard.md`, `archive_manifest.csv`.

**Verification checklist:**

- [ ] All 22 CSV registries pass zero-broken-foreign-key validation.
- [ ] All applicable gates `G01–G16` are current `PASS` for exact final versions.
- [ ] Thesis receipt, Q1 paper receipt/disposition, TRIPOD+AI/PROBAST-AI compliance, and executed archive restore proof present.
- [ ] `G17` PASS signed by researchers and supervisor; zero invented clinical validation or journal acceptance claimed.

**Common mistakes:** Treating these planning documents as evidence that research is finished; hiding unresolved leakage or missing IRB receipts under "future work"; deleting failed experiments before final handover.

**Recovery procedure:** Keep `G17` FAIL, return to the earliest owning step with a missing/stale artifact, repair and re-verify affected gates, update `ARCH####`, and repeat `STEP-050`.

**Definition of Done:** `G17` PASS; all approved FYDP, Q1-grade scientific, ethical, reproducibility, and archival obligations evidenced and handed over cleanly. Universal DoD applies; this is a required future state.

**Next step:** None. Project closed within approved FYDP/Q1 scope; ongoing journal peer-review revisions follow `STEP-048` (`T25`) and any future prospective clinical validation trial requires a new IRB-approved research plan.

---

<a id="roadmap-self-review"></a>
# Final review — roadmap validation record

## Coverage and source fidelity

This execution blueprint implements the verbatim approved title (`RF01`) and all core elements of [fydp_title_proposal.pdf](./fydp_title_proposal.pdf) (6 scanned pages, SHA-256 `BA7DD0EF21C8A2CA77B2E1BAFC2AC5A0E1FEC584E221C848085A971EAACEEFA8`): primary hospital/diagnostic-center collection post-ethical approval (`RF09`), four approved modalities—Clinical, ECG signals, Laboratory results, and Lifestyle information (`RF10`)—separate modality feature extraction, Transformer-based multimodal fusion (`RF08`, `RF11`), all six mandatory performance metrics—Accuracy, Precision, Recall, F1-Score, ROC-AUC, and Confusion Matrix (`RF12`)—SHAP explainability (`RF08`, `RF11`), and decision-support research prototype framing (`RF16`).

Because the 6-page proposal contains zero formal citations (`RF06`), leaves critical parameters unspecified (`RF14`, `RF17`), and places Preprocessing/Feature Extraction visually before Train/Val/Test Split in its Workflow Diagram (`RF13`), this roadmap enforces systematic zero-seed literature review testing `PG1–PG5` (`STEP-004`–`009`), strict leakage-free post-split fitting (`STEP-019`–`022`), explicit resolution of all 26 blocking unknowns (`UD01–UD26`), and full Q1 biomedical-AI methodological rigor (four-tier comparators, progressive & LOMO ablations, missing-modality robustness, probability calibration, Decision Curve Analysis, multiplicity-adjusted DeLong/bootstrap statistics, subgroup fairness, PROBAST-AI self-audit, quantitative SHAP faithfulness/AOPC & stability, shortcut auditing, cardiologist plausibility review, and TRIPOD+AI compliance).

## Dependency, leakage, and recovery review

- **Bootstrap integrity:** `STEP-001` (`G01`) permits saving initial scope/UD records before `STEP-002`–`003` (`G02`) establish the repository, PHI vault tiers, blank templates, registries, and tested `environment/data/` lock—avoiding circular dependencies.
- **Ethics & clinical validity before modeling:** Written IRB/ethics approval and hospital permissions (`STEP-011`, `UD05`) strictly precede any clinical intake (`STEP-012`); four-modality & ECG quality auditing (`STEP-013`, `G04`) precedes endpoint & variable schema freezing (`STEP-014`–`015`, `G05`); pilot dual-abstraction $\kappa$/ICC QA and cardiologist adjudication (`STEP-016`–`018`, `G06`) precede splitting.
- **Leakage reconciliation (`RF13`):** Only deterministic record-local cleaning and fixed-parameter ECG parsing occur prior to patient/site-level grouped splitting (`STEP-020`, `G07`). All dataset-fitted imputers, scalers, encoders, and missingness transforms fit exclusively on training data (`STEP-021`) with mandatory cardiologist ST-T waveform morphology review prior to immutable `REL####` binding (`STEP-022`, `G08`).
- **Baseline parity & freeze discipline:** Framework/model runtime locking (`environment/model/`, `STEP-024`), preregistered Q1 experiment/calibration/statistical/XAI plans (`STEP-025`), unit tests (`STEP-026`), and checkpoint interruption/restore proof (`STEP-027`, `G09`) strictly precede full training (`STEP-028`–`031`, `G10` per EXP). Champion selection, post-hoc calibrator fitting, operating threshold $\tau$ selection, and training-only SHAP background freezing (`STEP-032`, `G11`) strictly precede opening the sealed test set (`STEP-033`).
- **Quantitative XAI & dual-track submission:** Quantitative faithfulness (Deletion/Insertion AOPC vs random baseline), multi-seed stability, shortcut audit, and cardiologist review (`STEP-038`–`040`, `G14`) precede XAI claims. Research prototype packaging and clean-environment reproducibility (`STEP-041`–`042`, `G15`) precede writing sign-off. Document-scoped `G16 / thesis` (`STEP-046` → `047`) never stalls on `G16 / paper` (`STEP-048`), and `G17` (`STEP-050`) verifies all applicable obligations and PHI-segregated archive restoration (`STEP-049`) without making completion depend on uncertain external journal acceptance.

## Canonical cross-reference checklist

| Item | Validation target for these planning documents |
|---|---|
| Exact approved title | Present verbatim in both documents (`RF01`) |
| Four approved modalities & scope exclusions | Clinical, ECG signals, Laboratory results, Lifestyle information; medical imaging excluded as primary input; supplementary research aid, NOT clinical deployment |
| Stages and steps | `S01–S17` aligned 1:1 to `STEP-001–050`; contiguous unique step IDs |
| Quality gates | `G01–G17` share identical names, owning steps, evidence requirements, and human reviewers with [OS §14](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-14) |
| Unresolved decisions | `UD01–UD26` canonical in [OS §1.6](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-01); steps resolve each at its blocking milestone |
| Registries | [OS Appendix B](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#appendix-b) (22 CSV schemas + 2 subordinate manifests) is the sole schema/path authority |
| Templates | `T01–T32` canonical in [OS §15](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md#os-15) and installed by `STEP-003` |
| Per-step operational completeness | Every step (`STEP-001` through `STEP-050`) contains all 20 labeled operational fields |
| Links and internal anchors | All relative links and `#anchor` references verified across both companion documents |
| Zero topic contamination | Completely native to Multimodal CVD Risk Prediction (Clinical/ECG/Lab/Lifestyle/Transformer/SHAP/TRIPOD+AI); zero carry-over from unrelated projects |
| Source cryptographic provenance | `fydp_title_proposal.pdf` preserved intact with verified SHA-256 (`BA7DD0EF21C8A2CA77B2E1BAFC2AC5A0E1FEC584E221C848085A971EAACEEFA8`) |

## Verification scope and initial execution state

The authoring verification validates **planning-document completeness, internal cross-reference consistency, source fidelity, zero topic contamination, and Q1 methodological architecture only**. It does **not** certify IRB approval, acquired hospital data, clinical adjudication, trained models, calibrated AUC/DCA metrics, faithful SHAP attributions, a submitted thesis, or a submitted/accepted Q1 paper. All 50 execution steps start **NOT STARTED**, all 26 `UD01–UD26` decisions start **Unresolved / Human Decision Required**, and all 17 gates (`G01–G17`) start **NOT ASSESSED** until actual human-reviewed evidence is produced.

**Start execution:** [STEP-001](#step-001). **Policy authority:** [CVD Multimodal Research Operating System](./CVD_MULTIMODAL_RESEARCH_OPERATING_SYSTEM.md).

*End of CVD Multimodal Project Execution Blueprint — v1.0.0; 50 focused step types across 17 research stages.*
