# Frozen Test Coverage & Cryptographic Custody Audit (`EVAL0001` / `STEP-033`)

| Field | Value |
|---|---|
| EvaluationID | `EVAL0001` |
| ReleaseID | `REL0001` (`REL0001_kaggle_final_test_bundle.zip`) |
| Authorization | `G11-20261128-02 PASS` / `TACC0002` (`UNSEAL_AUTHORIZED` prior to Test read) |
| Execution Custody | `TACC0003` (`EXECUTED_FROZEN_EVAL` on Kaggle `GPU T4 x1`, `2026-11-28`) |
| Backup Archive SHA-256 | `718714b5fa13cf29085fe30662f0e26430b5d767b332c01ad3a572be6318113c` (`08_Checkpoints/binaries/S12_S15/results_kaggle_backup.zip`) |
| Prediction NPZ SHA-256 | `92748e44f175774ac07f7dc3fa4e6ce5311de7cf8c9d9af1283cdda78fec090d` (`08_Checkpoints/binaries/S12_S15/s12_s15_outputs/frozen_test_predictions_bundle.npz`) |
| Freeze Digests Verified | `CalibratorHash=ea5e5d969eeb72fcecd19e9b55812baac0c4b35ec12b9457e42999903a993e65` / `BackgroundHash=fd797cf5dc180548a64b0243e35a1e7851354177b8202246ea536b4917a6eabe` / `REL0001=7be9fa07a6275fbdb99619b6704e38c0bb18a6aeaef3f214749a2344bfa76866` / `PP0001=d9ccfbf40b2b1cbb500bb4b9d0f5857611c71058f6c98532f288d03e62c0b536` |

## 1. Pre-Test Integrity & Validation Parity Gate
- All `15/15` serialized Stage `S11` checkpoints (`CKPT0002–CKPT0016`) verified identically by byte count and SHA-256 digest before touching Test data.
- Pre-Test `REL0001 Validation` parity check passed strictly (`|AUC_reloaded - AUC_S11_ref| <= 1e-4`) across serialized tree (`EXP0004`), unimodal ECG (`EXP0007–0010`), gated (`EXP0014`), champion (`EXP0015`), and unmasked ablation (`EXP0018`) checkpoints.
- Binary probability archive verification: **`62` prediction arrays + `62` ground-truth label arrays** checked independently; `0` NaN/Inf values, all probabilities strictly bounded in `[0.0, 1.0]`.

## 2. Scheduled Test Encounter Coverage (`100.0%` Zero Silent Drops)
| Cohort | Description | Scheduled `REL0001/test` | Evaluated `EVAL0001` | CVD+ Events (`%`) | Unimodal / Fusion Coverage |
|---|---|---|---|---|---|
| `DS0001` | PTB-XL 12-Lead WFDB + Clinical | `2,134` | `2,134` (`100.0%`) | `1,221` (`57.22%`) | `2,134/2,134` WFDB signals cached |
| `DS0002` | CARDIO-ML-ED Scanned ECG + Clinical + Lab | `81` | `81` (`100.0%`) | `48` (`59.26%`) | `48/48` PNG scans (`C+E_png+L`), `33/33` `C+L` missing-ECG |
| `DS0003` | CAIR-CVD-2025 Bangladeshi Clinical+Lab+Life | `217` | `217` (`100.0%`) | `104` (`47.93%`) | `217/217` tabular rows |
| `DS0004` | Sulianova CVD Clinical+Lab+Lifestyle | `10,287` | `10,287` (`100.0%`) | `5,090` (`49.48%`) | `10,287/10,287` tabular rows |
| **`ALL_COHORTS`** | **Pooled Held-Out Test** | **`12,719`** | **`12,719` (`100.0%`)** | **`6,463` (`50.81%`)** | **Zero patient overlap with Train/Val** |
