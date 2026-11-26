# Whole-Cohort QA Audit, STARD Flow Reconciliation & Frozen `ADJ0001–ADJ0004` Release (`STEP-018`)

| Field | Value |
|---|---|
| TemplateID | T12-RELEASE (`adjudication_release_audit`) |
| template_version | v1.0.0 |
| entity_id | ADJ0001; ADJ0002; ADJ0003; ADJ0004 (`v1.0.0` Frozen Tier 2B) |
| owner | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |
| date | 2026-11-27 |
| status | Automated Audit Complete (`0` Violations) — Ready for `G06` Sign-Off (`DEC0006`) |
| source_inputs | `04_Outcome_Schema_QA/adjudications/ADJB0001..0004`, `14_Automation/freeze_adjudication_release.py`, `variables.csv` (`7b3165df...` pre / `cc4aed3d...` v1.0.1) |
| governing_section | OS §5.3, §11, §14.2 (`G06`), Appendix A; Blueprint `STEP-018` |
| phi_sensitivity | Tier 1 aggregate QA & STARD numbers; immutable release CSVs locked strictly in gitignored Tier 2B |
| reviewer | Md. Mizanur Rahman (`Supervisor`) + Mohammad Nafis Sadiq (`Data Lead`) |

---

## 1. Whole-Cohort STARD / CONSORT Flow Reconciliation (`FIG0001` Ground Truth)

Executed exhaustively via [freeze_adjudication_release.py](../../14_Automation/freeze_adjudication_release.py) across all `93,947` screened records (`0` invariant violations, `0` cross-fold leaks, `0` silent uncertain coercions):

| Release (`DS`) | Screened Rows (Patients) | Excluded / Quarantined Breakdown (`Zero Silent Coercion`) | Clean Eligible Retained (Unique Patients) | Final Class Balance (`CVD+` / `Neg`) |
|---|---|---|---|---|
| **`ADJ0001`** (`DS0001 PTB-XL`) | `21,837` (`18,885`) | **`639`**: `416` zero-SCP uncertain, `133` `<18y`, `89` missing age, `1` `ecg_id=12722` `V5` flatline | **`21,198`** (`18,434` pts; `0` cross-fold pts) | **`12,192`** (`57.51%`) / `9,006` |
| **`ADJ0002`** (`DS0002 CARDIO-ML-ED`) | `581` (`569`) | **`26`**: `12` `<18y`, `9` `.jpg` 6-lead/typo IDs (`RISK0012`), `4` missing age, `1` missing diag | **`555`** (`543` unique `Col1` pts; **`329` `C+E_png+L` [`323` pts]** + `226` `C+L`) | **`330`** (`59.46%` Initial Cardiac) / `225` |
| **`ADJ0003`** (`DS0003 CAIR-CVD-2025`) | `1,529` (`1,529`) | **`76`**: Physiologic anomalies (`65` `SBP<=DBP` $\cup$ `13` negative `Estimated LDL < 0`) | **`1,453`** (`1,453` unique adults) | **`695`** (`47.83%` HIGH) / `758` |
| **`ADJ0004`** (`DS0004 sulianova`) | `70,000` (`70,000`) | **`1,425`**: `1,367` BP/anthro extreme outliers, `34` discordant dup pairs (`17`), `24` redundant dups | **`68,575`** (`68,575` clean adults) | **`33,929`** (`49.48%` cardio) / `34,646` |
| **Total Multi-Cohort** | **`93,947`** | **`2,166`** | **`91,781` Clean Eligible** | **`47,146` (`51.37%`) / `44,635`** |

---

## 2. Eligibility, Temporal & Grouping Integrity Audit (`OS §5.3`)
- **Duplicate `RecordID` Count:** **`0`** across all 4 frozen releases (`0` cross-cohort patient collisions).
- **Patient-Level Grouping Invariant:** `ADJ0001` verified `0` patients spanning `>1` `strat_fold`; `ADJ0002` preserves repeated hospital IDs cleanly under `PatientGroupID` (`555` rows across `543` unique patients — e.g., Records `1560/1561` on `Col1=167233` verified acute `260/130 mmHg` ED hypertensive crisis, reflected in `variables.csv v1.0.1`).
- **Temporal Alignment ($t_0$) & Incorporation Bias:** `0` post-$t_0$ outcome/discharge columns inside eligible predictor schemas (`assert_no_leakage_predictors` enforced cleanly); `Troponin-I` segregated strictly as `TierB_TroponinI_ElevatedFlag` (`180` missing/`32.4%` inside `ADJ0002`).
- **Automated Whole-Cohort Range Check:** `0` invariant violations across all `91,781` eligible encounters (`Violations = 0`).

---

## 3. Eligible Missingness & `UD10` Modality Availability Matrix
Per `DEC0006` (`UD10`), partial-modality cohorts and intra-cohort missingness remain **un-imputed inside frozen `ADJ####`** (handled post-split in Train folds inside Stage `S09`):
- **`ADJ0001` (`PTB-XL`):** `height_cm`: `14,414 (68.0%)`, `weight_kg`: `12,012 (56.7%)`, `bmi_kgm2`: `14,627 (69.0%)`; `[MISSING_LAB]`, `[MISSING_LIFESTYLE]`.
- **`ADJ0002` (`CARDIO-ML-ED`):** `sbp_mmhg`: `14 (2.5%)`, `dbp_mmhg`: `17 (3.1%)`, `pr_bpm`: `25 (4.5%)`, `creatinine_mgdl`: `113 (20.4%)`, `wbc_ul`: `95 (17.1%)`, `TierB_TroponinI`: `180 (32.4%)`; `226/555 (40.7%)` `[MISSING_ECG]`, `100%` `[MISSING_LIFESTYLE]`.
- **`ADJ0003` (`CAIR-CVD-2025`):** `age_years`: `73 (5.0%)` (all observed `25–79y`), `height_cm`: `68 (4.7%)`, `weight_kg`: `76 (5.2%)`, `bmi_kgm2`: `61 (4.2%)`, `sbp_mmhg`: `71 (4.9%)`, `dbp_mmhg`: `82 (5.6%)`, `TC`: `70 (4.8%)`, `HDL`: `78 (5.4%)`, `LDL`: `67 (4.6%)`, `FBS`: `60 (4.1%)`; `100%` `[MISSING_ECG]`.
- **`ADJ0004` (`sulianova`):** `0` missing tabular values (`0.0%`); `100%` `[MISSING_ECG]`.

---

## 4. Immutable Frozen Release Checksums (`SHA-256` — Stored in Tier 2B `adjudications/ADJ####/`)
- **`endpoint_charter.md`:** `b35549c213b37f472fa8d5a27483d04f745a445394b24325e26121c4b9124b69` | **`variables.csv` (`v1.0.1`):** `cc4aed3d66c5eb7b2e54154da9ba40984a8a8924f97e859fb72212239cc8219b` | **`ecg_contract.md`:** `bf6672739c1ac1197547efd120e498c0bc6103c33337b941a2eceb0edf153928`

| Release ID | `NativeHash` (`native_snapshot.csv`) | `FullReleaseHash` (`verified_curated.csv`) | `EligibleOnlyHash` (`verified_eligible_only.csv`) |
|---|---|---|---|
| **`ADJ0001`** | `a23f2b90e2b82f648119e49c88a7d70d9c5888171107a206e04c016d7892c19f` | `01bbe8524dad7e533c6ff75038c8e6130a7ac758414eb2ec9f6c61774d57b197` | `f26f3d27364687fdd0671bfd342252aeacc92e3774ae3e94ed25dcf4987b0ab6` |
| **`ADJ0002`** | `025209fc5e27d3389401e720a5d3ff350bc6b50564735bff17e1a1b0d0c6d5de` | `677fe4cfb4ef0697634e1ce2255d7201cd2cf057d38a56b1da1c7ed8daa00fac` | `8e219a145268461c84c8b222d9f875d6f80073d47976179ae1a43914ac40fc4e` |
| **`ADJ0003`** | `e75456f4d48c1b7ce415579756dde4cc3999a3ea2a9e21cd55a3acbb2475b9a5` | `bcdcd00879568238be5b88bd7405b2ac4bf1d12deaec7b1f84b04f4dc2efdeb6` | `0a72fba7917c023ff19c53a9802a303ff40486d8cd2c59f3c1cad81d4c1f7f05` |
| **`ADJ0004`** | `2423cc5534fdc70887471778fc92b673ebb53d0d5188537b9029643b8a10e275` | `9f82fbd44f094eaf93ec3dd4d8f0fad6bda4604286d2ba9f727c6e97e748647c` | `3be5e89a5e8ccc3114bd96aabee0331023b17a03ebb7014e5688a7196554fae0` |
