# Final Test-Evaluation Freeze Charter (`STEP-032` / Gate `G11` Prep)

| Field | Value |
|---|---|
| Document | `09_Evaluation_Stats/freeze.md` |
| Version | v1.0.0 (`Validation-Locked Pre-Unseal Bundle — Awaiting Supervisor G11 Sign-Off`) |
| Step / Gate | `STEP-032` / `Gate G11` |
| Date | `2026-11-28` |
| Leads | Mohammad Nafis Sadiq (`232-15-895`), Rayan Ahmed (`232-15-847`) |
| Approver Required | Md. Mizanur Rahman (`Supervisor`) + Evaluation Reviewer (`STEP-032`) |
| Test Partition Custody | **`SEALED` (`TACC0001`, `0` Test Reads Performed Prior to Sign-Off)** |

---

## 1. Frozen Champion & Prespecified Final-Test Comparators (Selected Strictly on `REL0001 Validation`)

1. **Primary Proposed Champion Model:** **`MODEL0015`** (`MC0015 CVD_MM_Transformer`, `EXP0015` seed `20261127` primary checkpoint `CKPT0011` SHA-256 `5e0686c33f471ea45acd5461e19504ae0dafdfa1a01ba0182e7f0caabec4c8ff` + `5`-seed ensemble `CKPT0013–CKPT0016`; `266,587` params; `ALL_COHORTS Val ROC-AUC = 0.8225 ± 0.0048`, Macro AUC `0.8169`, `ECE = 0.0169`, `DS0002 = 0.7353`, `DS0001 = 0.9333`).
2. **Prespecified Final-Test Comparators (Locked Before Unsealing `Test`):**
   - **Tier 1 Tabular Baselines:** `MODEL0001` (`LR`, best tabular on `DS0002 = 0.7248`), `MODEL0002` (`RF`, winner on `DS0003 = 0.8523`), `MODEL0004` (`XGBoost` `CKPT0002–CKPT0005`), `MODEL0005` (`LightGBM`, top tree on `DS0004 = 0.8025`).
   - **Tier 1 Unimodal ECG Encoders:** `MODEL0007` (`ResNet1D` `CKPT0006` `0.9346`), `MODEL0008` (`Conv1D-BiLSTM` `CKPT0007` `0.9374`), `MODEL0009` (`CNN2D_PNG` `CKPT0008` `0.5486`), `MODEL0010` (`ECGPatchTransformer` `CKPT0009` `0.9232`).
   - **Tier 2 Clinical Context:** `MODEL0011` (`WHO/FRS Clinical Score` on `DS0003`/`DS0004`).
   - **Tier 3 Simple Fusion:** `MODEL0012` (`EarlyConcat XGB` `0.8303`), `MODEL0013` (`Late OOF Stacker` `0.8274`), `MODEL0014` (`GatedAttention` `CKPT0010` `0.8264`).
   - **Block E Masking Ablation:** `EXP0018` (`MC0015 zero_fill`, `CKPT0012` `0.8256` pooled / `0.6939` `DS0002`).

---

## 2. Cryptographically Frozen Hashes & Custody Locks

| Artifact / Lock | Locked Identifier / SHA-256 Digest |
|---|---|
| **`REL0001` Release & Preprocessing** | `REL0001` (`7be9fa07a6275fbdb99619b6704e38c0bb18a6aeaef3f214749a2344bfa76866`), `PP0001` (`d9ccfbf40b2b1cbb500bb4b9d0f5857611c71058f6c98532f288d03e62c0b536`) |
| **Variables Schema & Split Manifest** | `variables.csv` (`cc4aed3d66c5eb7b2e54154da9ba40984a8a8924f97e859fb72212239cc8219b`), `SPLIT0001` (`db74cfeb8fed769c6c370e4e3b664b3ca6edc0af1b1ad20fe64e1123892cd3e6`) |
| **Eval & XAI Protocols** | `protocol.md` (`5e042d94047781bad0828dbecf465d30862c0f08eac4688c91dea0b1b98fb897`), `xai_protocol.md` (`7f8cd082a80611f59563bbf5a1ff9f44486550e4a4fc703ea0f54ea50fe2fced`) |
| **Frozen Validation Calibrator & $\tau$ Bundle** | [frozen_validation_calibration.json](./frozen_validation_calibration.json) (`CalibratorHash = ea5e5d969eeb72fcecd19e9b55812baac0c4b35ec12b9457e42999903a993e65`) |
| **Train-Only SHAP Background (`N=256`)** | [shap_background_ids.json](./shap_background_ids.json) (`BackgroundHash = fd797cf5dc180548a64b0243e35a1e7851354177b8202246ea536b4917a6eabe`) |
| **Primary Champion Checkpoint (`CKPT0011`)** | `08_Checkpoints/binaries/S11/s11_outputs/checkpoints/EXP0015_MC0015_seed20261127_best_val.pt` (`5e0686c33f471ea45acd5461e19504ae0dafdfa1a01ba0182e7f0caabec4c8ff`) |
| **Bootstrap / Stat Plan (`protocol.md`)** | Stratified Patient-Group Bootstrap `B = 2,000` (`seed=20261127`), Paired Two-Sided DeLong, Exact McNemar, Holm-Bonferroni $\alpha=0.05$, DCA $p_t \in [0.05, 0.50]$ |

---

## 3. Gate `G11` Unseal Authorization Status
- **Validation Parity Rule at `STEP-033`:** Before running Test predictions, all frozen `.pt`/`.pkl` checkpoints and any deterministic `sklearn`/`LGBM` refits MUST reproduce logged `REL0001 Validation` AUROCs identically (`<= 1e-4` tolerance).
- **Zero Test Leakage Verified:** [test_access_log.csv](../03_Datasets_Cohort/splits/test_access_log.csv) contains strictly `TACC0001 SEALED` (`0` reads of `rel0001_test.jsonl`).
- **Action Required to Unseal:** Supervisor Md. Mizanur Rahman confirmation of Gate `G10` + Gate `G11` before executing `STEP-033`.
