# Quantitative Evaluation Report (EVAL####)

| Field | Value |
|---|---|
| TemplateID | T19 (evaluation.md) |
| template_version | v1.0.0 |
| entity_id | Unresolved / Human Decision Required |
| owner | Rayan Ahmed (232-15-847), Mohammad Nafis Sadiq (232-15-895) |
| date | 2026-11-20 |
| status | Template / Blank |
| source_inputs | not reported |
| governing_section | OS §7.1, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

# EVAL#### — Quantitative Held-Out Evaluation Report

## 1. Evaluation Protocol & Freeze
- Evaluation ID: `EVAL####`
- Evaluated Model: `MODEL####`
- Test Partition Release: `REL####` (Sealed Test Set)
- Test Freeze Protocol Hash: [Checksum]
- Operating Threshold ($	au$): [Threshold] (Frozen on validation)

## 2. Primary Discrimination & Classification Metrics
| Metric | Value | 95% Bootstrap CI | Proposal Mandatory |
|---|---|---|---|
| ROC-AUC | [Value] | [[Low] - [High]] | Yes |
| Precision-Recall AUC (PR-AUC) | [Value] | [[Low] - [High]] | Q1 Adopted |
| Accuracy | [Value] | [[Low] - [High]] | Yes |
| Sensitivity (Recall) | [Value] | [[Low] - [High]] | Yes |
| Specificity | [Value] | [[Low] - [High]] | Q1 Adopted |
| Positive Predictive Value (Precision) | [Value] | [[Low] - [High]] | Yes |
| Negative Predictive Value (NPV) | [Value] | [[Low] - [High]] | Q1 Adopted |
| F1-Score | [Value] | [[Low] - [High]] | Yes |

## 3. 2x2 Confusion Matrix
```text
                 Observed CVD-    Observed CVD+
Predicted Low:       [TN]             [FN]
Predicted High:      [FP]             [TP]
```

## 4. Probability Calibration & Clinical Utility
- Brier Score: [Value] (Lower is better)
- Expected Calibration Error (ECE): [Value]
- Calibration Slope: [Value] (Target = 1.0)
- Calibration Intercept: [Value] (Target = 0.0)
- Decision Curve Analysis (DCA): Superior Net Benefit across risk thresholds [Range]
