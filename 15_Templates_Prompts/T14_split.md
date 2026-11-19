# Patient-Grouped Split Report (SPLIT####)

| Field | Value |
|---|---|
| TemplateID | T14 (split.md) |
| template_version | v1.0.0 |
| entity_id | Unresolved / Human Decision Required |
| owner | Rayan Ahmed (232-15-847), Mohammad Nafis Sadiq (232-15-895) |
| date | 2026-11-20 |
| status | Template / Blank |
| source_inputs | not reported |
| governing_section | OS §4.3, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

# SPLIT#### — Leakage-Free Dataset Split Report

## 1. Split Specification
- Split ID: `SPLIT####`
- Source Dataset ID: `DS####`
- Grouping Key: `PatientID` (Strict patient-level isolation)
- Partitioning Scheme: [e.g., Train 70%, Validation 15%, Test 15% / 5-Fold Nested CV]
- Random Seed: [e.g., 42]
- Stratification Factors: Outcome CVD event status, Clinical Site, Sex

## 2. Partition Demographics & Event Prevalence
| Partition | Patient Count ($N$) | Encounter Count | CVD Events (%) | Male / Female (%) |
|---|---|---|---|---|
| Train | [N] | [Count] | [%] | [% / %] |
| Validation | [N] | [Count] | [%] | [% / %] |
| Test (Held-Out) | [N] | [Count] | [%] | [% / %] |

## 3. Verification of Zero Patient Overlap
- Overlap Check: `len(set(Train_Patients) & set(Val_Patients) & set(Test_Patients)) == 0`
- Assertion Result: PASS (Zero cross-partition patient overlap)
- Test Partition Sealed Custody: [Custody details]
