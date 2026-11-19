# Grounded Paper Extraction Summary (P####)

| Field | Value |
|---|---|
| TemplateID | T05 (paper_summary.md) |
| template_version | v1.0.0 |
| entity_id | Unresolved / Human Decision Required |
| owner | Rayan Ahmed (232-15-847), Mohammad Nafis Sadiq (232-15-895) |
| date | 2026-11-20 |
| status | Template / Blank |
| source_inputs | not reported |
| governing_section | OS §3.2, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

# P#### — [Paper Title]

## 1. Bibliographic Provenance
- Citation Key: [AuthorYear]
- DOI: [DOI link]
- PubMed ID (PMID): [PMID or None]
- Authors: [Author list]
- Venue & Year: [Journal/Conference, Year]
- Reading Status: Full-Text Verified

## 2. Study Design & Cohort Characteristics
- Setting & Country: [Setting]
- Sample Size ($N$): [Total patients, encounters]
- Event Count & Prevalence: [Event count, %]
- Endpoint Definition & Horizon: [e.g., 5-year CVD incidence, in-hospital mortality]

## 3. Modality & Technical Architecture
- Modalities Included: [Clinical, ECG, Lab, Lifestyle]
- ECG Format & Sampling: [e.g., 12-lead, 500 Hz, raw waveform vs intervals]
- Model Families: [LR, XGBoost, CNN, Transformer, etc.]
- Fusion Strategy: [Early, Late, Cross-Attention]

## 4. Quantitative Results & Evaluation Rigor
- Primary Discrimination: ROC-AUC = [Value] (95% CI: [Low-High])
- Secondary Metrics: PR-AUC = [Value], F1 = [Value], Brier Score = [Value]
- Calibration Evaluated: [Yes / No / ECE reported]
- Statistical Significance Testing: [DeLong test / Paired bootstrap]

## 5. Explainability & Bias Audit
- XAI Methods: [SHAP / LIME / Attention weights]
- XAI Faithfulness Benchmarked: [Yes / No / Not Reported]
- PROBAST Risk of Bias Rating: [Low / High / Unclear]
- Specific Limitations & Failure Modes: [Details with page locators]
