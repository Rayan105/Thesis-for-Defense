# 16_Archive

| Metadata | Value |
|---|---|
| TemplateID | T01 (readme.md) |
| Purpose | Immutable project release snapshots (`ARCH####`), long-term deposition manifests, submission receipts, and clean restoration evidence |
| Owner | Release Custodians: Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Supervisor | Md. Mizanur Rahman |
| Inputs | Final thesis package, Q1 manuscript bundle, frozen code, model cards, aggregate evaluation tables |
| Outputs | `archive_manifest.csv`, `ARCH####.md`, restoration test logs |
| PHI Sensitivity | Tier 1 (Manifests & public research bundles); restricted clinical archives remain in Tier 4 offline storage. |
| Governing Sections | OS §11.2, §14; Blueprint Stage S17 (`STEP-049`–`STEP-050`) |

## Folder Contract
- Released archive snapshots are completely immutable; once tagged and hashed, no file in an archive bundle may be edited or replaced.
- Public archive bundles must contain zero PHI or unconsented health data.
- Full restoration drill (restoring and running synthetic inference from the archive snapshot) must be evidenced before declaring project completion (`G17`).
