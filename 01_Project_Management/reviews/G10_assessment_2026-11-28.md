# G10 Assessment — Stage S11 Completion, Checkpoint Integrity & Model Cards (`PASS Pending Supervisor Ratification`)

| Field | Value |
|---|---|
| TemplateID | T22 (gate_audit.md) |
| template_version | v1.0.0 |
| AssessmentID | `G10-20261128-01` |
| GateID | `G10` |
| DocumentOrEntityScope | `EXP0001–EXP0020` (`Blocks A–F`), `CKPT0002–CKPT0016`, `MODEL0001–MODEL0015`, `07_Experiments/validation_matrix_summary.md` |
| EntityVersions | `REL0001 v1.0.0`; `S11` v1.0.0 (`91` Val rows, `15` checkpoints) |
| Outcome | **`PASS (Technical Verified — Pending Supervisor Ratification)`** |
| Assessor | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Human Approver | Md. Mizanur Rahman (`Supervisor Sign-Off Requested`) |
| Assessment Date | `2026-11-28` |
| PHI Sensitivity | Tier 1 (Public / Git-safe) |

---

## Mandatory Criteria Audit (`STEP-030` / `STEP-031`)

| # | Criterion | Verified Evidence & Honest Notes | Status |
|---|---|---|---|
| **C1** | **Config, Seed & Stopping Reconciliation (`EXP0001–EXP0020`):** Immutable `config.yaml` hashes match, all 20 experiments (`91` rows) complete, negative & null results (`EXP0009` 2D-CNN `0.5486`, `DS0003` RF > Transformer) retained honestly. | [experiment_registry.csv](../../07_Experiments/experiment_registry.csv), [validation_matrix_summary.md](../../07_Experiments/validation_matrix_summary.md) | **PASS** *(266.6K param delta disclosed)* |
| **C2** | **Tier 3 Checkpoint SHA-256 & Val Prediction Parity (`CKPT0002–CKPT0016`):** All `15` saved checkpoints verified 100% byte & SHA-256 match post-extraction; all `91` `.npz` validation predictions finite and bounded `[0, 1]`. | [s11_checkpoint_manifest.json](../../08_Checkpoints/s11_checkpoint_manifest.json), [checkpoint_registry.csv](../../08_Checkpoints/checkpoint_registry.csv) | **PASS** |
| **C3** | **Model Registry & Bounded Model Cards (`MODEL0001–MODEL0015`):** All 15 evaluated architectures documented with modalities, limitations, calibration scalars, and boundaries. | [model_registry.csv](../../06_Models_Fusion/model_registry.csv), `06_Models_Fusion/cards/MODEL0001–0015.md` | **PASS** |
| **C4** | **Zero Test Partition Exposure:** All `91` CSV rows & `results.zip` built exclusively from `REL0001` `train`/`val`; `test_access_log.csv` remains `TACC0001 SEALED`. | [test_access_log.csv](../../03_Datasets_Cohort/splits/test_access_log.csv) | **PASS** |
| **C5** | **Supervisor Ratification:** Md. Mizanur Rahman reviews `validation_matrix_summary.md` & disclosed deviations (`266.6K` params, epoch cap `30/25`, deterministic tabular refit at `STEP-033`). | Pending Human Confirmation | **PENDING** |
