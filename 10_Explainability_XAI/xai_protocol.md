# Preregistered Multimodal Explainability (XAI) & Faithfulness Protocol (`STEP-025` / `UD19–UD21`)

> [!IMPORTANT]
> **Execution Timing Notice:** This protocol is **preregistered NOW in `STEP-025`** before any training begins to eliminate post-hoc explanation cherry-picking. Actual SHAP / AOPC computation executes **ONLY AFTER frozen model testing in `Stage S15` (`STEP-038–040`)**.

| Field | Value |
|---|---|
| Document | `10_Explainability_XAI/xai_protocol.md` |
| Version | v1.0.0 (`Pre-Training Preregistered XAI Verification Contract`) |
| Step / Execution Stage | `STEP-025` Contract -> Executes Strictly in `Stage S15` (`STEP-038–040`) |
| Date | `2026-11-27` |
| XAI Lead | Rayan Ahmed (`232-15-847`) |
| Clinical Reviewer | Qualified Cardiologist (`TBD` at `G14`) + Md. Mizanur Rahman |
| Governing Section | OS §8.1–§8.3, §12.1 (`UD19–UD21`); Blueprint `STEP-025`, `STEP-038–040` |

---

## 1. Explainer-to-Architecture Contract & Leakage-Free Background (`UD19`)
1. **Tree Models (`MC0002 RF`, `MC0004 XGBoost`, `MC0005 LightGBM`):** Exact `shap.TreeExplainer` (interventional over Train background).
2. **`CVD-MM-Transformer` (`MC0015`) & Neural Baselines (`MC0006–MC0010, MC0014`):**
   - **`Captum GradientSHAP` + `IntegratedGradients`** (`m_steps = 50` Gauss-Legendre quadrature over logit output, complemented by `KernelSHAP`/`PartitionSHAP` over `4`-modality token coalitions `[C, E, L, S]`)!
   - **Mandatory Local Additivity Tolerance (`Efficiency Axiom`):** Verify $\left| f(x) - \left(\phi_0 + \sum_{i} \phi_i(x)\right) \right| \le 0.02 \cdot \max(1, |f(x)|)$ across audited test cases!
   - **Strict Attention-Weight Disclaimer:** Cross-modal attention weights (`alpha`) are logged purely for internal diagnostics and NEVER presented alone as faithful Shapley explanations (`OS §8.1`).
3. **Train-Only Stratified Background Distribution:** Sample **`N_bg = 256` encounters** stratified across `DS0001–04` and target outcome **exclusively from `REL0001 Train`** (`seed = 20261127`, saved with SHA-256 checksum). Zero `Val` or `Test` records may enter background expectations.

---

## 2. Three-Level Attribution Hierarchy
1. **Modality-Level Shares (`[C%, E%, L%, S%]`):** Sum absolute feature/token Shapley magnitudes per modality block ($\Phi_m(x) = \sum_{j \in m} |\phi_j(x)|$) normalized cleanly over active modalities (`ModalityMask_CELS == 1`).
2. **Tabular Clinical, Lab & Lifestyle Feature Level:** Global beeswarm/bar rankings, non-linear SHAP dependence plots (`Age x SBP`, `Glucose x BMI`, `Smoking x Cholesterol`), and individual waterfall charts separating physiological features from MNAR `_isnan` indicators.
3. **12-Lead ECG Attribution Level:** Maps `GradientSHAP` / `IntegratedGradients` back onto `500 Hz` 12-lead temporal segments (`P-QRS-ST-T`) for `PTB-XL` and spatial `256 x 768` waveform regions for `CARDIO-ML-ED` scans (`with smoothed saliency overlays excluding red-grid artifacts`).

---

## 3. Quantitative Faithfulness & Stability Benchmarks (`STEP-039` / `UD20`)
No interpretability claim is permitted unless all objective checks execute on Test cases (`Stage S15`):
1. **Perturbation Faithfulness — Deletion & Insertion `AOPC` Curves (`vs Negative Controls`):**
   - Rank active inputs/segments from `k = 1..K` by $|\phi_i(x)|$ (or signed risk-increasing $\phi_i > 0$).
   - **Deletion (`Comprehensiveness`):** Replace top-$k$ features/ECG windows sequentially with conditional Train median / neutral ECG baseline and compute **AOPC** ($\frac{1}{K}\sum_{k=1}^K [p(x) - p(x_{\text{del } k})]$). MUST significantly outperform **Random Feature Deletion** AND **Reverse-Order Deletion** (explicitly avoiding the failure caught in `P0029`!).
   - **Insertion (`Sufficiency`):** Start from Train baseline and insert top-$k$ features progressively, measuring predicted probability recovery AUC (`exceeding Random Insertion`).
2. **Modality-SHAP vs LOMO Empirical Concordance:** Correlate global modality SHAP shares (`[C%, E%, L%, S%]`) against Block D `Leave-One-Modality-Out` performance drops ($\Delta \text{ROC-AUC}$ & $\Delta \text{Brier}$).
3. **Multi-Seed Stability & Local Robustness:** Across the `5` canonical seeds (`STEP-031`), compute mean pairwise **Spearman rank correlation ($\rho$)**, Kendall's $\tau$, and **Top-5 feature Jaccard index**; also verify local Lipschitz stability under clinically negligible $\pm 0.05$ SD Gaussian perturbation.
4. **Spurious-Shortcut & MNAR Confounder Audit (`Mandatory for G14`):** Explicitly check whether missingness indicators (`{col}_isnan`), cohort site proxies, or residual ECG baseline/image border patterns rank among Top-3 SHAP drivers. Any non-physiological shortcut triggers audit investigation.

---

## 4. Cardiologist Plausibility Rubric & Strict Claim Boundaries (`STEP-040` / `UD21`)
- **Sampled Review Packet (`N = 24` stratified cases: `6 TP, 6 FP, 6 TN, 6 FN`):** Qualified cardiologist scores de-identified patient packets + global SHAP (`3`-point clinical pathophysiology concordance + intelligibility + implausibility flags).
- **IRB Scope & Claim Boundary (`UD21`):** No prospective hospital clinician-decision reader trial is conducted; therefore thesis and Q1 manuscript strictly avoid unsubstantiated *"improves physician trust/speed"* or causal biologic claims, stating strictly bounded faithfulness, stability, concordance, and clinician plausibility findings (`OS §8.3`).
