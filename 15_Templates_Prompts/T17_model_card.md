# Bounded Model Card (MODEL####)

| Field | Value |
|---|---|
| TemplateID | T17 (model_card.md) |
| template_version | v1.0.0 |
| entity_id | Unresolved / Human Decision Required |
| owner | Rayan Ahmed (232-15-847), Mohammad Nafis Sadiq (232-15-895) |
| date | 2026-11-20 |
| status | Template / Blank |
| source_inputs | not reported |
| governing_section | OS §6.3, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

# MODEL#### — Bounded Model Card

## 1. Model Overview
- Model ID: `MODEL####`
- Architecture Family: [e.g., Cross-Modal Transformer Fusion Network]
- Framework: [PyTorch / TensorFlow]
- Parameter Count: [Total parameters]
- Training Experiment: `EXP####`
- Best Checkpoint: `CKPT####`

## 2. Intended Use & Boundaries
- Intended Domain: Research clinical decision-support for early CVD risk prediction
- Primary Users: Medical researchers and clinical AI evaluators
- Out-of-Scope Use: Autonomous diagnostic decisions, emergency triage without doctor review

## 3. Inputs & Modalities Handled
- Modality Encoders:
  - Clinical: Multi-layer Perceptron (MLP)
  - ECG: 1D-ResNet / Convolutional Transformer
  - Laboratory: Tabular embedding layer
  - Lifestyle: Tabular embedding layer
- Missing-Modality Behavior: Masked cross-attention token imputation

## 4. Performance & Calibration Summary
- Held-Out ROC-AUC: [Value] (95% CI: [Low-High])
- Operating Decision Threshold ($	au$): [Threshold Value]
- Post-Hoc Calibrator: [Platt Scaling / Isotonic Regression]
