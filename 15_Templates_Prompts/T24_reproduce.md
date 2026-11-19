# Clean-Environment Reproducibility Audit

| Field | Value |
|---|---|
| TemplateID | T24 (reproduce.md) |
| template_version | v1.0.0 |
| entity_id | Unresolved / Human Decision Required |
| owner | Rayan Ahmed (232-15-847), Mohammad Nafis Sadiq (232-15-895) |
| date | 2026-11-20 |
| status | Template / Blank |
| source_inputs | not reported |
| governing_section | OS §9.2, §15.2 |
| phi_sensitivity | Tier 1 (Public / Git-safe) |
| reviewer | Md. Mizanur Rahman |

---

# Reproducibility Audit — Stage S16 Verification

## 1. Audit Setup
- Audit Date: YYYY-MM-DD
- Execution Host: Clean virtual environment / Fresh container
- Environment Lock Hash: [Checksum]
- Evaluator: [Evaluator Name]

## 2. Replay Commands & Execution
```bash
# Exact commands executed to reproduce study findings
git clone https://github.com/Rayan105/Thesis-for-Defense.git
cd Thesis-for-Defense
pip install -r environment/data/requirements.txt
python 14_Automation/reproduce_study.py --release REL0001
```

## 3. Numerical Tolerance Agreement
| Target Metric | Original Reported Value | Replayed Value | Absolute Difference | Within Tolerance ($< 10^{-4}$)? |
|---|---|---|---|---|
| Held-out ROC-AUC | [Value] | [Value] | [Diff] | PASS |
| Held-out PR-AUC | [Value] | [Value] | [Diff] | PASS |
| Brier Score | [Value] | [Value] | [Diff] | PASS |

## 4. Declared Reproducibility Level
- Level A (Deterministic Replay): Evidenced and Verified
- Controlled Data Access Statement: Lawful access protocol documented for external researchers
