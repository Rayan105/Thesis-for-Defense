"""
cvd_mm: Reproducible Multimodal Framework for Cardiovascular Disease Risk Prediction.

Modules:
    - intake: Cohort intake, de-identification audits, and manifest generation.
    - ecg: 12-lead ECG waveform parsing, filtering, and quality control.
    - tabular: Clinical, laboratory, and lifestyle schema validation and processing.
    - split: Leakage-safe, patient-grouped dataset partitioning.
    - preprocess: Pre-split record cleaning and train-only fitted transformations.
    - models: Baseline classifiers and Transformer-based multimodal fusion architectures.
    - eval: Discrimination, calibration, decision curve analysis, and statistical tests.
    - xai: Multimodal SHAP attribution, faithfulness benchmarks, and stability audits.
    - prototype: Research inference and clinical decision-support entrypoint.
"""

__version__ = "0.2.0"
__author__ = "Rayan Ahmed, Mohammad Nafis Sadiq"
