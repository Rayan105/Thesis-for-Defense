# Case Report Form (CRF) & 12-Lead ECG Acquisition Contract

| Field | Value |
|---|---|
| TemplateID | T11 (crf_ecg_protocol.md) |
| template_version | v1.0.0 |
| entity_id | Unresolved / Human Decision Required |
| owner | Rayan Ahmed (232-15-847), Mohammad Nafis Sadiq (232-15-895) |
| date | 2026-11-20 |
| status | Template / Blank |
| source_inputs | not reported |
| governing_section | OS §5.2, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

# CRF & 12-Lead ECG Technical Protocol

## 1. Case Report Form (CRF) Items
- Clinical Variables: Age, Sex, Systolic BP, Diastolic BP, Heart Rate, BMI, Hypertension History, Diabetes History
- Laboratory Assays: Total Cholesterol, LDL-C, HDL-C, Triglycerides, Fasting Plasma Glucose, Serum Creatinine, Troponin
- Lifestyle Factors: Smoking status (pack-years), Physical activity level, Dietary risk score, Alcohol intake

## 2. 12-Lead ECG Standard Specifications
- Standard Lead Set: I, II, III, aVR, aVL, aVF, V1, V2, V3, V4, V5, V6
- Sampling Frequency: 500 Hz (minimum allowable 250 Hz)
- Recording Duration: Standard 10 seconds
- Voltage Calibration: 10 mm/mV (0.1 mV resolution)
- Raw File Format: [WFDB / XML / DICOM / CSV array]

## 3. Pre-Analysis Quality Thresholds
- High-frequency powerline interference ($50$ Hz) rejection
- Baseline wander removal ($< 0.5$ Hz) with ST-T complex geometry preservation
- Lead detachment / flatline detection
