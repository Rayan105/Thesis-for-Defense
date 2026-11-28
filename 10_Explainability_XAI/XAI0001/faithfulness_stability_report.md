# Quantitative XAI Faithfulness, LOMO Concordance & Multi-Seed Stability (`XAI0001` / `STEP-039`)

## 1. Deletion & Insertion Perturbation Faithfulness (`N=80` Test Records across `DS0001–04`)
| Top-k Step | Deletion Top-k `AOPC` | Deletion Random Ctrl | Deletion Reverse Ctrl | Insertion Top-k Prob | Insertion Random Ctrl |
|---:|---:|---:|---:|---:|---:|
| `1` | **0.030864** | -0.002595 | 0.0 | **0.493642** | 0.450788 |
| `2` | **0.024203** | 0.000263 | 0.0 | **0.486473** | 0.450607 |
| `3` | **0.011453** | -0.0004 | 4.1e-05 | **0.476555** | 0.449962 |
| `4` | **0.01349** | 0.000913 | -0.000672 | **0.475594** | 0.457913 |
| `5` | **0.014517** | -0.002902 | -0.001886 | **0.471738** | 0.458302 |
| `6` | **0.00799** | 0.00146 | -0.001959 | **0.469196** | 0.470367 |
- **Mean Deletion Top-k `AOPC`:** **`0.017086`** vs Random Control **`-0.000544`** and Reverse Control **`-0.000746`** — strictly outperforms BOTH negative controls at every step `k = 1..6` (overcoming the deletion-control failure observed in `P0029`).
- **Mean Insertion Prob:** **`0.478866`** vs Random Control **`0.456323`** (`+0.0225` higher recovery).

## 2. Modality-SHAP vs Empirical LOMO Concordance & 5-Seed Stability
- **Exact Modality Shares `[C, E, L, S]` (`%`):** **`[44.8, 27.19, 14.69, 13.31]`** vs Empirical LOMO ΔAUC Drops `[0.12986, 0.03234, 0.00702, 0.0024]` -> **Spearman `rho = 1.0`**, **Pearson `r = 0.9761`**!
- **5-Seed Feature-Ranking Stability (`CKPT0011, 0013–16` on `DS0004`):** Pairwise **Spearman `rho = 0.9816`**, **Kendall `tau = 0.9231`**, **Top-5 Jaccard = `0.5298`**.
- **Local Lipschitz Robustness (`±0.05 SD` Gaussian perturbation):** Mean feature-attribution Spearman **`rho = 0.8194`**.
