# 06_Models_Fusion

| Metadata | Value |
|---|---|
| TemplateID | T01 (readme.md) |
| Purpose | Model candidates, unimodal/fusion architecture specifications, comparator baseline plans, and bounded model cards |
| Owner | Modeling Lead: Rayan Ahmed (`232-15-847`) |
| Supervisor | Md. Mizanur Rahman |
| Inputs | Candidate model families (LR, RF, SVM, XGBoost, 1D-CNN, LSTM, Multimodal Transformer), pretrained encoder weights |
| Outputs | `candidates.csv`, `model_registry.csv`, `baseline_plan.md`, `architectures/*`, `cards/MODEL####.md` |
| PHI Sensitivity | Tier 1 (Public / Git-safe). Weight binaries live in Tier 3. |
| Governing Sections | OS §6; Blueprint Stage S10 (`STEP-023`–`STEP-027`) |

## Folder Contract
- Model architectures must implement standardized interfaces across unimodal baselines and multimodal Transformer fusion.
- All candidate models must be registered in `candidates.csv` with explicit architectural documentation, parameter counts, and licenses.
- Model cards (`MODEL####.md`) must explicitly state intended research use and safety limitations.
