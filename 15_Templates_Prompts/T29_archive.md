# Immutable Release Archive Record (ARCH####)

| Field | Value |
|---|---|
| TemplateID | T29 (archive.md) |
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

# ARCH#### — Immutable Research Release Archive

## 1. Archive Manifest
- Archive ID: `ARCH####`
- Release Tag: `v1.0.0`
- Timestamp: YYYY-MM-DDTHH:MM:SS+06:00
- Custodian: Academic Department / Lead Researchers

## 2. Preserved Artifacts & Cryptographic Checksums
| Component | Storage Path | Format | SHA-256 Checksum | PHI Sensitivity Tier |
|---|---|---|---|---|
| Complete Git Repository | `16_Archive/ARCH####/repo_snapshot.bundle` | Git Bundle | [Checksum] | Tier 1 |
| Final Thesis & Supplements | `16_Archive/ARCH####/thesis_final.pdf` | PDF | [Checksum] | Tier 1 |
| Q1 Manuscript & Checklist | `16_Archive/ARCH####/manuscript_q1.pdf` | PDF | [Checksum] | Tier 1 |
| Frozen Trained Weights | `Tier3/ARCH####/checkpoints/` | PyTorch Binary | [Checksum] | Tier 3 |
| De-Identified Test Cohort | `Tier2B/ARCH####/cohort/` | Encrypted CSV/WFDB | [Checksum] | Tier 2B |

## 3. Restoration Test Evidence
- Clean Restore Test Date: YYYY-MM-DD
- Replay Status: PASS (100% hash and output reproduction confirmed)
