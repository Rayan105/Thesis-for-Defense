# Experiment Execution Report (EXP####)

| Field | Value |
|---|---|
| TemplateID | T16 (experiment.md) |
| template_version | v1.0.0 |
| entity_id | Unresolved / Human Decision Required |
| owner | Rayan Ahmed (232-15-847), Mohammad Nafis Sadiq (232-15-895) |
| date | 2026-11-20 |
| status | Template / Blank |
| source_inputs | not reported |
| governing_section | OS §6.2, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

# EXP#### — [Experiment Title]

## 1. Scientific Objective
- Experiment ID: `EXP####`
- Research Question: [RQ#]
- Comparator Tier: [Tier 1 Unimodal / Tier 2 Clinical Score / Tier 3 Early Fusion / Tier 4 Transformer Fusion / Ablation]
- Primary Hypothesis: [Falsifiable performance hypothesis]

## 2. Data & Model Setup
- Prepared Release: `REL####`
- Split ID: `SPLIT####`
- Model Candidate: `MC####`
- Config Path: `07_Experiments/EXP####/config.yaml`
- Configuration Hash (SHA-256): [Checksum]
- Source Code Git Commit: [Commit Hash]

## 3. Training & Validation Execution
- Random Seed: [Seed]
- Optimization / Budget: [Optimizer, Learning Rate, Epochs, Batch Size]
- Early Stopping Criterion: Validation ROC-AUC (patience = 10)
- Validation Discrimination: ROC-AUC = [Value], PR-AUC = [Value]
- Validation Calibration: Brier Score = [Value]

## 4. Checkpoints & Artifact Pointers
- Best Checkpoint: `CKPT####`
- Artifact Storage Location: `E:/FYDP_SECURE_VAULT/Tier3/EXP####/`
- Outcome / Conclusion: [Summary of observed experimental findings]
