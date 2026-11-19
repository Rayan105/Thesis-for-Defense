# 09_Evaluation_Stats

| Metadata | Value |
|---|---|
| TemplateID | T01 (readme.md) |
| Purpose | Evaluation protocol, test-set freeze records, quantitative metrics, probability calibration, Decision Curve Analysis (DCA), statistical inference (DeLong, bootstrap CIs), and subgroup fairness audits |
| Owner | Evaluation & Biostatistics Lead: Mohammad Nafis Sadiq (`232-15-895`) |
| Supervisor | Md. Mizanur Rahman |
| Inputs | Frozen test partition, trained candidate checkpoints (`CKPT####`), validation-fitted calibrators |
| Outputs | `protocol.md`, `freeze.md`, `evaluation_registry.csv`, `EVAL####/report.md`, `EVAL####/error_probast.md` |
| PHI Sensitivity | Tier 1 (Safe aggregate metrics and summary tables). Individual patient predictions stay in Tier 2B/Tier 3. |
| Governing Sections | OS §7; Blueprint Stages S12–S14 (`STEP-032`–`STEP-037`) |

## Folder Contract
- Model selection and probability calibrator fitting must occur strictly on the validation partition; the test partition remains sealed until `G11` freeze.
- Mandatory 6 proposal metrics (Accuracy, Precision, Recall, F1, ROC-AUC, Confusion Matrix) must be evaluated alongside Q1 extensions (PR-AUC, Specificity, NPV, Brier score, ECE, DCA).
- Statistical comparisons must report 95% bootstrap confidence intervals and paired test $p$-values with multiple-testing correction.
