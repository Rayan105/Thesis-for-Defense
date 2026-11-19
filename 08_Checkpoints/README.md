# 08_Checkpoints

| Metadata | Value |
|---|---|
| TemplateID | T01 (readme.md) |
| Purpose | Checkpoint policy, master checkpoint registry, SHA-256 manifests, and restore evidence |
| Owner | Experiment Lead: Rayan Ahmed (`232-15-847`) |
| Inputs | PyTorch/TensorFlow state dicts, optimizer states, epoch logs during training |
| Outputs | `checkpoint_policy.md`, `checkpoint_registry.csv`, `manifests/CKPT####.md` |
| PHI Sensitivity | Tier 1 (Metadata & SHA-256 manifests only). Checkpoint binary files (`*.pt`, `*.ckpt`) reside in Tier 3 artifact storage outside Git. |
| Governing Sections | OS §11.2; Blueprint Stage S11 (`STEP-030`) |

## Folder Contract
- Model weight binaries must never be committed to Git.
- Every saved checkpoint must register full state components (model weights, optimizer, RNG seeds, epoch/step) and SHA-256 checksums in `checkpoint_registry.csv`.
- Resumability and restore verification must be tested before declaring a checkpoint valid.
