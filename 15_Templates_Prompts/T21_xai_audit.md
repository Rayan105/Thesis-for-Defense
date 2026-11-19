# Multimodal Explainability Audit (XAI####)

| Field | Value |
|---|---|
| TemplateID | T21 (xai_audit.md) |
| template_version | v1.0.0 |
| entity_id | Unresolved / Human Decision Required |
| owner | Rayan Ahmed (232-15-847), Mohammad Nafis Sadiq (232-15-895) |
| date | 2026-11-20 |
| status | Template / Blank |
| source_inputs | not reported |
| governing_section | OS §8.1, §8.2, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

# XAI#### — Multimodal SHAP & Faithfulness Audit

## 1. Explainer Setup & Additivity
- Explainer Type: [TreeSHAP / GradientSHAP / KernelSHAP]
- Background Distribution: Training partition stratified sample ($N = 200$)
- Local Additivity Error: PASS ($\sum \phi_i + \phi_0 - f(x) < 10^{-4}$)

## 2. Multimodal Modality-Share Contributions
- Clinical Modality Share: [%]
- 12-Lead ECG Modality Share: [%]
- Laboratory Modality Share: [%]
- Lifestyle Modality Share: [%]
- Modality-Ablation Concordance: Correlates with empirical Leave-One-Modality-Out drops

## 3. Quantitative Faithfulness Benchmarks
- Deletion AOPC (Comprehensiveness): [Value] (Significantly degrades faster than random masking, $p < 0.001$)
- Insertion AOPC (Sufficiency): [Value] (Recovers prediction faster than random insertion)
- Multi-Seed Ranking Stability: Spearman $ho = [Value]$ across independent random seeds

## 4. Spurious-Shortcut & Clinical Plausibility Audit
- Shortcut Detection: Negative (Site IDs, powerline noise, missingness flags show negligible attribution)
- Cardiologist Rubric: Pathophysiological plausibility confirmed for top clinical risk drivers
