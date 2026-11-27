# SPLIT0001 — Patient-Grouped Leakage-Free Dataset Split Report (`STEP-020`)

| Field | Value |
|---|---|
| TemplateID | T14 (split.md) |
| template_version | v1.0.0 |
| entity_id | SPLIT0001 |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | 2026-11-27 |
| status | Locked & Verified (`0` Patient Overlap; Test Partition Sealed; Pending `G07` Sign-Off) |
| source_inputs | `ADJ0001–ADJ0004` (`91,781` Clean Eligible Encounters), `src/cvd_mm/splitting.py` |
| governing_section | OS §4.3–§4.4, §12.1 (`UD11`), §14.2 (`G07`); Blueprint `STEP-020` |
| phi_sensitivity | Tier 1 aggregate statistics & SHA-256 hashes (row-level `manifest.csv` isolated in `.gitignore` Tier 2B) |
| reviewer | Md. Mizanur Rahman (Supervisor) + Biostatistics Reviewer |

---

## 1. Split Specification & Cryptographic Proof
- **Split ID:** `SPLIT0001`
- **Fixed RNG Seed:** `20261127`
- **Grouping Key:** `(DS, PatientGroupID)` — strict patient-level isolation across all `4` cohorts
- **Manifest Location (`Tier 2B`, Gitignored):** `03_Datasets_Cohort/splits/SPLIT0001/manifest.csv`
- **Manifest SHA-256 (Deterministic):** `db74cfeb8fed769c6c370e4e3b664b3ca6edc0af1b1ad20fe64e1123892cd3e6`
- **Total Eligible Records / Unique Patient Groups:** `91,781` / `89,005`
- **Partition Scheme (`UD11 Option A`):**
  - **`DS0001 PTB-XL` (`ADJ0001`):** Official patient-grouped benchmark `strat_fold` (`1–8` Train, `9` Validation, `10` Test) + deterministic `5`-fold grouped CV inside `Train`.
  - **`DS0002 CARDIO-ML-ED`, `DS0003 CAIR-CVD-2025`, `DS0004 sulianova`:** Connected `PatientGroupID` stratified split targeting **`70%` Train / `15%` Validation / `15%` Test** + deterministic `5`-fold grouped CV inside `Train`.

---

## 2. Aggregate Balance & Demographics Per Cohort & Partition

### Combined All 4 Cohorts (`ADJ0001–ADJ0004`)
| Partition | Patients ($N$) | Encounters ($n$) | Multi-Visit Pts | CVD+ Events (%) | Male / Female (%) | Mean Age (y) | `[C, E, L, S]` Counts |
|---|---|---|---|---|---|---|---|
| **Train** | 64,076 | 66,338 | 1,637 | 34,216 (51.58%) | 39.5% / 60.5% | 54.85 | `[66,338, 17,160, 49,409, 49,019]` |
| **Val** | 12,490 | 12,724 | 187 | 6,467 (50.83%) | 38.1% / 61.9% | 54.28 | `[12,724, 2,185, 10,589, 10,505]` |
| **Test** | 12,439 | 12,719 | 217 | 6,463 (50.81%) | 38.0% / 62.0% | 54.60 | `[12,719, 2,182, 10,585, 10,504]` |

### Cohort 1 — `DS0001 PTB-XL` (`C_partial+E_wfdb`)
| Partition | Patients ($N$) | Encounters ($n$) | Multi-Visit Pts | CVD+ Events (%) | Male / Female (%) | Mean Age (y) | `[C, E, L, S]` Counts |
|---|---|---|---|---|---|---|---|
| **Train** | 14,677 | 16,929 | 1,627 | 9,747 (57.58%) | 52.1% / 47.9% | 59.82 | `[16,929, 16,929, 0, 0]` |
| **Val** | 1,902 | 2,135 | 186 | 1,224 (57.33%) | 52.2% / 47.8% | 60.30 | `[2,135, 2,135, 0, 0]` |
| **Test** | 1,855 | 2,134 | 216 | 1,221 (57.22%) | 51.9% / 48.1% | 60.93 | `[2,134, 2,134, 0, 0]` |

### Cohort 2 — `DS0002 CARDIO-ML-ED` (`C+E_png+L` & `C+L_[MISSING_ECG]`)
| Partition | Patients ($N$) | Encounters ($n$) | Multi-Visit Pts | CVD+ Events (%) | Male / Female (%) | Mean Age (y) | `[C, E, L, S]` Counts |
|---|---|---|---|---|---|---|---|
| **Train** | 380 | 390 | 10 | 233 (59.74%) | 40.0% / 60.0% | 52.15 | `[390, 231, 390, 0]` |
| **Val** | 83 | 84 | 1 | 49 (58.33%) | 40.5% / 59.5% | 50.64 | `[84, 50, 84, 0]` |
| **Test** | 80 | 81 | 1 | 48 (59.26%) | 40.7% / 59.3% | 54.52 | `[81, 48, 81, 0]` |

### Cohort 3 — `DS0003 CAIR-CVD-2025` (`C+L+S_[MISSING_ECG]`)
| Partition | Patients ($N$) | Encounters ($n$) | Multi-Visit Pts | CVD+ Events (%) | Male / Female (%) | Mean Age (y) | `[C, E, L, S]` Counts |
|---|---|---|---|---|---|---|---|
| **Train** | 1,018 | 1,018 | 0 | 487 (47.84%) | 49.5% / 50.5% | 47.18 | `[1,018, 0, 1,018, 1,018]` |
| **Val** | 218 | 218 | 0 | 104 (47.71%) | 49.5% / 50.5% | 46.53 | `[218, 0, 218, 218]` |
| **Test** | 217 | 217 | 0 | 104 (47.93%) | 49.3% / 50.7% | 46.38 | `[217, 0, 217, 217]` |

### Cohort 4 — `DS0004 Kaggle sulianova` (`C+L_ord+S_[MISSING_ECG]`)
| Partition | Patients ($N$) | Encounters ($n$) | Multi-Visit Pts | CVD+ Events (%) | Male / Female (%) | Mean Age (y) | `[C, E, L, S]` Counts |
|---|---|---|---|---|---|---|---|
| **Train** | 48,001 | 48,001 | 0 | 23,749 (49.48%) | 34.9% / 65.1% | 53.27 | `[48,001, 0, 48,001, 48,001]` |
| **Val** | 10,287 | 10,287 | 0 | 5,090 (49.48%) | 34.9% / 65.1% | 53.22 | `[10,287, 0, 10,287, 10,287]` |
| **Test** | 10,287 | 10,287 | 0 | 5,090 (49.48%) | 34.9% / 65.1% | 53.44 | `[10,287, 0, 10,287, 10,287]` |

### `DS0002 CARDIO-ML-ED` Sub-Modality Stratification Check
- **Train:** `{'C+E_png+L': 231, 'C+L_[MISSING_ECG]': 159}`
- **Validation:** `{'C+E_png+L': 50, 'C+L_[MISSING_ECG]': 34}`
- **Test:** `{'C+E_png+L': 48, 'C+L_[MISSING_ECG]': 33}`

---

## 3. Zero-Overlap Verification & Sealed Test Custody (`OS §4.4`)
- **`train & val` Patient Overlap:** `0` (**PASS**)
- **`train & test` Patient Overlap:** `0` (**PASS**)
- **`val & test` Patient Overlap:** `0` (**PASS**)
- **Internal Train `5`-Fold CV Patient Overlap:** `0` (**PASS**)
- **Bit-for-Bit Deterministic Seed Re-Run Check:** **PASS** (identical `ManifestSHA256` on double generation)
- **Test Partition Custody:** Formally sealed in `03_Datasets_Cohort/splits/test_access_log.csv` (`TACC0001: SEALED`); zero reads permitted until Gate `G11` validation champion selection.
