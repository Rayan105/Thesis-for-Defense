# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]
- Step 003: Blank templates T01–T32 and 22 canonical Appendix B CSV registries.
- Step 004–009: Systematic literature search, screening, and PRISMA extraction.

## [v0.2.0] - 2026-11-20
### Added
- **STEP-002 Execution:**
  - Instantiated full canonical 17-domain directory tree matching OS §2.1.
  - Root governance documents: `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `.gitattributes`.
  - Storage & Four-Tier PHI security policy in `13_Documentation/pipeline.md`.
  - Minimal data-tool runtime specifications in `environment/data/requirements.txt` and `environment/data/environment.yml`.
  - Installation manual in `13_Documentation/installation.md` and verification log in `environment/data/verification.md`.
  - Folder contract `README.md` files across all initialized domain folders (`01_Project_Management` through `16_Archive`).
  - Python package anchor `src/cvd_mm/__init__.py` and testing harness `tests/__init__.py`.
  - Synthetic data smoke test `tests/test_synthetic_smoke.py`.
  - STEP-002 session diary entry: `01_Project_Management/diary/2026-11-20_STEP-002_session.md`.

## [v0.1.0] - 2026-11-20
### Added
- **STEP-001 Execution:**
  - Foundational project scope & exclusion charter: `01_Project_Management/scope.md`.
  - Canonical decisions ledger `01_Project_Management/decisions.csv` initialized with `DEC0001`.
  - Decision record for UD01: `01_Project_Management/decision_log/DEC0001.md`.
  - Gate status registry `01_Project_Management/gates.csv` with gates `G01–G17` initialized to `NOT ASSESSED`.
  - Initial `G01` gate assessment document: `01_Project_Management/reviews/G01_assessment_2026-11-20.md`.
  - Session diary entry: `01_Project_Management/diary/2026-11-20_STEP-001_session.md`.
  - Strict PHI and planning document exclusion rules configured in `.gitignore`.
  - Initialized Git repository tracking `main` branch connected to remote `https://github.com/Rayan105/Thesis-for-Defense.git`.
