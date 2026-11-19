# 14_Automation

| Metadata | Value |
|---|---|
| TemplateID | T01 (readme.md) |
| Purpose | Thin command-line automation scripts, registry validation tools, PHI-leakage scanners, and reproduction runners |
| Owner | Automation Lead: Mohammad Nafis Sadiq (`232-15-895`) |
| Inputs | Live repository registries, Git status diffs, environment locks |
| Outputs | `validate_repo.py`, `check_phi_leakage.py`, automated audit logs |
| PHI Sensitivity | Tier 1 (Public / Git-safe). |
| Governing Sections | OS §2.2, §14, §15; Blueprint Stages S02, S16 |

## Folder Contract
- Automation scripts must remain lightweight, modular, and callable via standard CLI interfaces.
- Repository validator (`validate_repo.py`) enforces Appendix B CSV column schemas, foreign-key relationships, and `.gitignore` integrity.
- Never write scripts that bypass access controls, alter immutable release hashes, or write into sealed test partitions.
