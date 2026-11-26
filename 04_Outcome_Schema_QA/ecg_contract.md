# 12-Lead ECG Acquisition & Multi-Representation Technical Contract (`STEP-015`)

| Field | Value |
|---|---|
| TemplateID | T11 (crf_ecg_protocol.md) |
| template_version | v1.0.0 |
| entity_id | ECG-CONTRACT-v1.0.0 (`UD07`) |
| owner | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| date | 2026-11-27 |
| status | Approved (`DEC0005 Option A` — `2026-11-27`) |
| source_inputs | `03_Datasets_Cohort/reports/four_modality_qc_and_ecg_audit.md`, `04_Outcome_Schema_QA/endpoint_charter.md`, `04_Outcome_Schema_QA/variables.csv`, `src/cvd_mm/schema_ecg.py` |
| governing_section | OS §4.3, §4.5, §5.2 (`UD07`), §14.2 (`G05`), §15.2 (`T11`); Blueprint `STEP-015` |
| phi_sensitivity | Tier 1 (Public / Git-safe technical specification) |
| reviewer | Md. Mizanur Rahman + Qualified Cardiologist (`TBD` per `scope.md §8.2`) |

---

## 1. Governing Architecture Decision (`UD07`)
Under `DEC0004 Option B`, two heterogeneous raw ECG representations exist in our dataset portfolio (`DS0001 PTB-XL` digital WFDB waveforms and `DS0002 CARDIO-ML-ED` digitized paper-scan PNG strips), while `DS0003` and `DS0004` carry `[MISSING_ECG]` status. **Contract Invariant:** Raw digital waveforms (`DS0001`) and 2D scanned paper strips (`DS0002`) MUST be handled via **separate modality-appropriate encoders and quality pipelines** — never stitched row-by-row or treated identically.

---

## 2. Track 1 — Raw Digital 12-Lead WFDB Contract (`DS0001 PTB-XL`)
- **Authoritative Format:** PhysioNet WFDB paired `.hea` + `.dat` (`int16` little-endian binary).
- **Canonical 12-Lead Order (`exact sequence`):** `['I', 'II', 'III', 'AVR', 'AVL', 'AVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']`.
- **Sampling Frequency & Duration:**
  - Primary high-res tier: **`500 Hz`**, `10.0s` (`12 × 5,000` samples; `120,000` bytes).
  - Compact secondary tier: **`100 Hz`**, `10.0s` (`12 × 1,000` samples; `24,000` bytes).
- **Amplitude Units:** Millivolts (`mV`), decoded using per-channel `.hea` gain (`1000.0/mV` nominal) and baseline (`0`).
- **Automated Rejection / Quarantine Thresholds (`enforced by src/cvd_mm/schema_ecg.py`):**
  1. Malformed `.hea`, `num_leads != 12`, unsupported `Hz`, or mismatched canonical lead names.
  2. Any `.hea` comment line starting with `#` (PHI guard — verified `0/43,674` on intake).
  3. Any lead with zero dynamic range (`min == max` flatline — isolates & excludes **`ecg_id=12722`**, lead `V5=0`).
  4. Any `int16` saturation clipping (`<= -32768` or `>= 32767`) across any lead.
- **Stage `S09` Filtering Spec (`STEP-021` / `G08`):** Record-local `0.5 Hz` high-pass / median baseline wander suppression + `50 Hz` European powerline notch (`PTB-XL` Berlin origin), subject to clinical ST-T morphology fidelity inspection before `G08`.

---

## 3. Track 2 — Digitized 12-Lead Paper-Scan Image Contract (`DS0002 CARDIO-ML-ED`)
- **Authoritative Image Subset:** **`400` cropped 12-row `.png` scans** (`814–5100 × 2757–7020` px RGB; excluding pediatric `age < 18y` and missing-age rows -> `<= 327` adult same-patient `C + E_img + L` candidates).
- **Mandatory Quarantine List (`RISK0012`):**
  1. **Exclude `8` Uncropped `.jpg` 6-Lead Paper Strips:** `126035-1.jpg`, `126035-2.jpg`, `127578-1.jpg`, `127660.jpg`, `142560-1.jpg`, `163401.jpg`, `26.jpg`, `35.jpg` contain uncropped vendor margins (`PAB`, `ordered by TST`, `5mm/mV`) and 6-lead splits -> **excluded from 12-row PNG encoder** to prevent format shortcut leakage (`G14`).
  2. **Quarantine ID Discrepancies:** Isolate the `2` numeric filename/label mismatch pairs (`140354/1403354`, `148679/148676`) and `13` clinical-unlinked base-IDs until resolved/excluded at `STEP-017/018`.
  3. **Filename Normalization:** Strip trailing whitespace (`'150753 '`) and normalize `(2)` suffix (`'136883(2)'` -> `'136883-2'`) deterministically via `normalize_cardiomled_image_stem()`.
- **Image Standardization & Digitization Validation Protocol (`OS §5.2`):**
  - Correct `90°` portrait rotation deterministically so time axis runs left-to-right across all 12 rows.
  - Because `.png` scans retain red millimeter paper grids (`STEP-013` visual audit), Stage `S09` applies record-local color/luminance red-grid suppression followed by aspect-ratio-preserving letterbox resize before 2D CNN/ViT encoding.
  - **Clinical Readability QA (`STEP-016`):** Stratified visual check by Qualified Cardiologist confirming trace visibility, unclipped R-peaks, and ST-segment preservation before/after red-grid normalization.

---

## 4. Track 3 — Missing-ECG Indicator Contract (`DS0003` & `DS0004`)
- `DS0003` (`CAIR-CVD-2025`, `1,529` BD pts) and `DS0004` (`sulianova`, `70,000` pts) carry zero raw ECG traces. Represented natively via `has_ecg_mask = 0` and learnable `[MISSING_ECG]` token inside multimodal Transformer architectures (`zero synthetic ECG generation`).

---

## 5. Ratification (`UD07 / G05`)
- **Status:** `Approved Option A (Supervisor Ratified 2026-11-27; External Clinician Required at G08 ST-T Check)`
- **Reviewers:** Md. Mizanur Rahman (`Supervisor`, approved `2026-11-27`) + External Clinical Reviewer (`TBD` prior to `G08`)
