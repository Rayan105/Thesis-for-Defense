# 07_Experiments

| Metadata | Value |
|---|---|
| TemplateID | T01 (readme.md) |
| Purpose | Experiment execution plans, master experiment registry, and immutable per-experiment directories (`EXP####`) containing frozen configs and run manifests |
| Owner | Experiment Lead: Rayan Ahmed (`232-15-847`) |
| Inputs | Prepared release (`REL####`), candidate architectures (`MC####`), hyperparameter search spaces |
| Outputs | `experiment_plan.md`, `experiment_registry.csv`, `EXP####/config.yaml`, `EXP####/README.md`, `EXP####/run_manifest.json` |
| PHI Sensitivity | Tier 1 (Public / Git-safe configs & logs). Per-patient test predictions reside in Tier 2B/Tier 3. |
| Governing Sections | OS §6.2, §13; Blueprint Stage S11 (`STEP-028`–`STEP-031`) |

## Folder Contract
- Every experiment run must be pre-registered with fixed seeds, exact configuration YAML, and parent commit hash.
- Never edit an experiment configuration once training has launched.
- Failed, diverged, or negative runs must never be deleted; all attempts remain permanently cataloged.
