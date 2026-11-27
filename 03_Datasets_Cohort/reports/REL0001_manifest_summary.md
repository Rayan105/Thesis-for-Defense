# REL0001 — Immutable Prepared Multimodal Release Summary (`STEP-022`)

| Field | Value |
|---|---|
| Release ID | `REL0001` (`v1.0.0`) |
| Source Cohorts / Adjudications | `DS0001–DS0004` (`ADJ0001–ADJ0004`) |
| Variables SHA-256 | `cc4aed3d66c5eb7b2e54154da9ba40984a8a8924f97e859fb72212239cc8219b` |
| Split ID / Manifest SHA-256 | `SPLIT0001` / `db74cfeb8fed769c6c370e4e3b664b3ca6edc0af1b1ad20fe64e1123892cd3e6` |
| Preprocessing ID / `FitStateHash` | `PP0001` / `d9ccfbf40b2b1cbb500bb4b9d0f5857611c71058f6c98532f288d03e62c0b536` |
| **`REL0001` `ManifestHash`** | `7be9fa07a6275fbdb99619b6704e38c0bb18a6aeaef3f214749a2344bfa76866` |
| Tier-2B Custody (`Gitignored`) | `05_Preprocessing_Alignment/processed/REL0001/` (`Read-Only Locked` + Checksum Drill PASS) |

---

## 1. End-to-End Count Reconciliation (`DS -> ADJ -> SPLIT -> PP -> REL`)

| Stage | Cohorts / Partitions | Records / Encounters | Unique Patient Groups | Positive Events | Discrepancy |
|---|---|---|---|---|---|
| **Raw Intake (`DS0001–04`)** | 4 cohorts | `93,947` (`21,837 + 581 + 1,529 + 70,000`) | `~91,000` | `48,359` | Base intake |
| **Quarantined (`STEP-017/18`)** | Excluded anomalies / <18y / JPG / dups | `-2,166` (`639 + 26 + 76 + 1,425`) | - | `-1,213` | `UNCERTAIN_EXCLUDED` isolated |
| **Frozen Clean (`ADJ0001–04`)** | `ADJ0001..ADJ0004` | **`91,781`** | **`89,005`** | **`47,146`** (`51.37%`) | `0` (`Violations=0`) |
| **`SPLIT0001` + `PP0001` -> `REL0001` Train** | `train` (`CVFolds 0..4`) | `66,338` | `64,076` | `34,216` | `0` (`0` overlap) |
| **`SPLIT0001` + `PP0001` -> `REL0001` Val** | `val` (`CVFold = -1`) | `12,724` | `12,490` | `6,467` | `0` (`0` overlap) |
| **`SPLIT0001` + `PP0001` -> `REL0001` Test (SEALED)** | `test` (`CVFold = -1`) | `12,719` | `12,439` | `6,463` | `0` (`TACC0001` Sealed) |

---

## 2. How the 4 Modalities Are Structured & Combined Without Cross-Cohort Stitching (`DEC0004` / `DEC0006`)

| Cohort (`DS`) | Encounters (`REL0001`) | `ModalityMask [C, E, L, S]` | `TabularFeatures` Block (`X`) | `ECGReference` Asset Binding |
|---|---|---|---|---|
| **`DS0001` (`PTB-XL`)** | `21,198` | `[1, 1, 0, 0]` | `11` dims (`age, height, weight, bmi` + `_isnan` + `sex` OHE) | `500 Hz` & `100 Hz` WFDB `.dat`/`.hea` paths (`0` missing) |
| **`DS0002` (`CARDIO-ML-ED`, Paired PNG)** | `329` | `[1, 1, 1, 0]` | `15` dims (`age, sbp, dbp, pr, creatinine, wbc` + `_isnan` + `sex`) | Cropped `12`-row `.png` scan path (`0` missing, `100%` verified) |
| **`DS0002` (`CARDIO-ML-ED`, No ECG)** | `226` | `[1, 0, 1, 0]` | `15` dims (Clinical vitals + ED labs + `_isnan`) | `null` (`ECG` encoder gated off by `mask[1]=0`) |
| **`DS0003` (`CAIR-CVD-2025`)** | `1,453` | `[1, 0, 1, 1]` | `31` dims (Clinical + `mg/dL` lipids/glucose + smoking/famHx/activity) | `null` (`ECG` masked cleanly by `mask[1]=0`) |
| **`DS0004` (`Kaggle sulianova`)** | `68,575` | `[1, 0, 1, 1]` | `25` dims (Clinical + ordinal lipid/glucose `1-3` + smoke/alco/active) | `null` (`ECG` masked cleanly by `mask[1]=0`) |

---

## 3. Partition SHA-256 Manifest & Integrity Verification
- **Train (`rel0001_train.jsonl`):** SHA-256 `6f150398599c8f42a1b81c2ba4399b84ddc67f60c5ce6c0bfc151fd6a0923bae` (`35,991,558` bytes)
- **Val (`rel0001_val.jsonl`):** SHA-256 `b0f5975e0b5d32dc0399b208e143b90dbc02c7a92dd4254c372876a3bfc78083` (`6,542,121` bytes)
- **Test (`rel0001_test.jsonl`, Sealed Custody):** SHA-256 `a01d9338fe4c768758ecd8a0df8a0aa28a845b9331ebd287bfbb9cb97a321e3d` (`6,553,859` bytes)
- **Read-Only Permission Lock & Restore Checksum Drill:** **PASS** (100% checksum match post-lock)
