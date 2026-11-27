# Model Checkpoint, Hashing & Recovery Policy (`STEP-027` / `OS §11.2, §15.2`)

| Field | Value |
|---|---|
| Document | `08_Checkpoints/checkpoint_policy.md` |
| Version | `v1.0.0` |
| Step / Gate | `STEP-027` (`Stage S10` -> Feeds Gate `G09`) |
| Authors | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Reviewer | Md. Mizanur Rahman (Supervisor) |
| Tiered Storage Boundary | Binaries (`.pt`, `.ckpt.json`, `.pkl`) strictly stay in **Tier 3 (`08_Checkpoints/binaries/` + Kaggle/External Backup)**, gitignored cleanly; only text manifests (`08_Checkpoints/manifests/`) and `checkpoint_registry.csv` enter Git Tier 1. |

---

## 1. Immutable Naming & Provenance Rules
- **Canonical Checkpoint ID:** `CKPT####` (`e.g., CKPT0001` for `EXP0000_SMOKE`, sequential monotonic assignment in `08_Checkpoints/checkpoint_registry.csv`).
- **Diagnostic Tagging:** Every diagnostic/smoke checkpoint MUST carry `Role = diagnostic_smoke` and reside under `08_Checkpoints/binaries/EXP0000_SMOKE/`, strictly separated from reportable `EXP####` runs (`Block_A..Block_F`).
- **Two Canonical Artifacts per Run:**
  1. `best_val`: Saved ONLY when strict `Validation ROC-AUC` improves (`val_roc_auc > best_val_roc_auc`). This artifact alone feeds Gate `G11` Validation-only selection and post-hoc calibration.
  2. `last`: Overwritten cleanly at epoch boundaries for fault-tolerant interruption recovery.

## 2. Mandatory State Payload Contract
No checkpoint may rely on `model.state_dict()` alone. Every `CKPT####` envelope MUST embed or co-save:
1. `model_state_dict` (trainable model weights + BatchNorm buffers)
2. `optimizer_state_dict` (AdamW momentum/variance buffers)
3. `scheduler_state_dict` (CosineAnnealingLR / warmup step count)
4. `amp_scaler_state_dict` (if FP16 GradScaler is active on Kaggle GPU)
5. `epoch` & `global_step` + `best_val_roc_auc`
6. `rng_states` (`python`, `numpy`, `torch`, `torch.cuda` where applicable)
7. `config_sha256` + `release_id` (`REL0001`) + `fit_state_hash` (`d9ccfbf40b2b1cbb500bb4b9d0f5857611c71058f6c98532f288d03e62c0b536`)

## 3. Cryptographic Integrity & Resume Audit
- **SHA-256 Digest:** Computed immediately after atomic write and stored inside `08_Checkpoints/manifests/CKPT####.md` (`T18`) and `checkpoint_registry.csv`.
- **Pre-Load Verification:** `load_checkpoint_bundle()` re-computes SHA-256 prior to tensor/state restoration and refuses corrupted files immediately.
- **Honest Nondeterminism Disclosure:** Bitwise-exact resume is verified on CPU stdlib/PyTorch deterministic runs (`STEP-027`); when cuDNN atomic CUDA operations on Kaggle GPU introduce floating-point ULP drift across resume boundaries, exact weight/step/optimizer continuity and `val_roc_auc` tolerance must be explicitly logged in `G09` / run logs.

## 4. Retention & Tier 3 Backup Cadence
- All `best_val` checkpoints for registered `EXP####` runs are mirrored to external Tier 3 storage (`Kaggle Output Dataset Snapshot / Local Encrypted Backup`) with SHA-256 parity verified before deleting transient `last` scratch weights.
- Smoke/failed checkpoints stay marked diagnostic and are never promoted into `06_Models_Fusion/model_registry.csv`.
