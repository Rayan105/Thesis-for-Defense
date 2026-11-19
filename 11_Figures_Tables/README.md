# 11_Figures_Tables

| Metadata | Value |
|---|---|
| TemplateID | T01 (readme.md) |
| Purpose | Publication-grade figure and table specifications, generation scripts, high-resolution vector/raster outputs, and asset registry |
| Owner | Visual & Asset Lead: Rayan Ahmed (`232-15-847`) |
| Inputs | Quantitative evaluation data (`EVAL####`), XAI audit data (`XAI####`), cohort statistics |
| Outputs | `assets.csv`, `specs/FIG####.md`, `specs/TAB####.md`, `scripts/*.py`, rendered vector/raster assets |
| PHI Sensitivity | Tier 1 (Public / Git-safe). All plotted data must be strictly de-identified aggregate statistics or IRB-cleared exemplars. |
| Governing Sections | OS §10.3; Blueprint Stages S11–S17 |

## Folder Contract
- All figures must be generated programmatically from reproducible scripts; manual modification of plotted values is strictly prohibited.
- Vector formats (PDF, SVG) or high-resolution raster files (300–600 DPI) must be used.
- Palette choices must be colorblind-friendly and conform to standard biomedical journal publication standards.
