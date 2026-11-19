# Cohort & Dataset Quality Card (DS####)

| Field | Value |
|---|---|
| TemplateID | T09 (cohort_card.md) |
| template_version | v1.0.0 |
| entity_id | Unresolved / Human Decision Required |
| owner | Rayan Ahmed (232-15-847), Mohammad Nafis Sadiq (232-15-895) |
| date | 2026-11-20 |
| status | Template / Blank |
| source_inputs | not reported |
| governing_section | OS §4.2, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

# DS#### — [Cohort Dataset Name]

## 1. Provenance & Administration
- Dataset ID: `DS####`
- Clinical Sites (`SITE####`): [Site IDs]
- IRB Protocol Reference: [IRB ID]
- Recruitment Window: YYYY-MM-DD to YYYY-MM-DD
- Target Population: [Description of screening population]

## 2. Quantitative Summary
- Total Patient Count: [N]
- Total Clinical Encounters: [N]
- Cardiovascular Events (CVD+): [Count, %]
- Controls (CVD-): [Count, %]
- Complete 4-Modality Cases: [Count, %]

## 3. Modality Availability & Missingness
| Modality | Available Encounters | Missing Rate (%) | Primary Acquisition Device / Instrument |
|---|---|---|---|
| Clinical Records | [Count] | [%] | Hospital EHR / Case Report Form |
| 12-Lead ECG | [Count] | [%] | Digital ECG Machine (XML/DICOM/WFDB) |
| Laboratory Assays | [Count] | [%] | Serum Biochemistry Analyzer |
| Lifestyle Profiles | [Count] | [%] | Structured Patient Questionnaire |

## 4. Signal Integrity & Quality Checks
- ECG Quality Pass Rate: [% passing SNR and baseline wander checks]
- Raw File Manifest Hash (SHA-256): [Checksum]
- Tier 2B Storage Location: `E:/FYDP_SECURE_VAULT/Tier2B/DS####/`
