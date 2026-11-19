# Checkpoint Manifest Record (CKPT####)

| Field | Value |
|---|---|
| TemplateID | T18 (checkpoint.md) |
| template_version | v1.0.0 |
| entity_id | Unresolved / Human Decision Required |
| owner | Rayan Ahmed (232-15-847), Mohammad Nafis Sadiq (232-15-895) |
| date | 2026-11-20 |
| status | Template / Blank |
| source_inputs | not reported |
| governing_section | OS §11.2, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

# CKPT#### — Model Checkpoint Manifest

## 1. Checkpoint Provenance
- Checkpoint ID: `CKPT####`
- Experiment ID: `EXP####`
- Run Attempt: `RUN####`
- Epoch / Step: [Epoch #]
- Trigger Reason: Best Validation ROC-AUC

## 2. Stored State Components
- [x] Model weights (state_dict)
- [x] Optimizer state
- [x] Learning rate scheduler state
- [x] Random Number Generator (RNG) seeds (Python, NumPy, Framework)

## 3. Storage & Integrity Audit
- File Format: [e.g., .pt / .ckpt]
- File Size: [Bytes]
- Cryptographic SHA-256 Checksum: [Checksum]
- Tier 3 Storage Path: `E:/FYDP_SECURE_VAULT/Tier3/checkpoints/CKPT####.pt`
- Restore Verification Test: PASS (Exact inference reproduction verified)
