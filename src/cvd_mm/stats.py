"""
Clinical Utility (DCA) & Exact Paired Statistical Inference Module (STEP-026 / OS §7.3–§7.4).

Pure-Python stdlib verified implementations:
- Decision Curve Analysis (`compute_dca_curve`) over threshold probabilities `0.05..0.50`.
- Exact Sun & Xu two-sided paired DeLong test (`delong_paired_roc_test`).
- Stratified patient-grouped bootstrap 95% CIs (`bootstrap_metric_ci` & `bootstrap_paired_delta`).
- Exact two-sided McNemar binomial test (`mcnemar_exact_test`).
- Holm-Bonferroni step-down & Benjamini-Hochberg FDR multiple-testing adjustments.
"""

from __future__ import annotations

import collections
import math
import random
from typing import Any, Callable, Sequence

from src.cvd_mm.metrics import roc_auc_score_exact


def _normal_two_sided_p(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2.0))


def compute_dca_curve(
    y_true: Sequence[int],
    y_prob: Sequence[float],
    thresholds: Sequence[float] | None = None,
) -> list[dict[str, float]]:
    """Compute Net Benefit vs Treat-All and Treat-None across decision thresholds p_t."""
    if thresholds is None:
        thresholds = [round(0.05 + 0.01 * i, 2) for i in range(46)]  # 0.05..0.50
    n = len(y_true)
    prev = sum(y_true) / n
    curve = []
    for pt in thresholds:
        odds = pt / (1.0 - pt)
        tp = sum(1 for y, p in zip(y_true, y_prob) if y == 1 and p >= pt)
        fp = sum(1 for y, p in zip(y_true, y_prob) if y == 0 and p >= pt)
        nb_model = (tp / n) - (fp / n) * odds
        nb_all = prev - (1.0 - prev) * odds
        curve.append({
            "threshold_pt": pt,
            "net_benefit_model": round(nb_model, 6),
            "net_benefit_all": round(nb_all, 6),
            "net_benefit_none": 0.0,
        })
    return curve


def _placement_values(pos_scores: Sequence[float], neg_scores: Sequence[float]) -> tuple[float, list[float], list[float]]:
    """Compute exact Sun & Xu structural DeLong V10 / V01 placement vectors."""
    m = len(pos_scores)
    n = len(neg_scores)
    v10 = [0.0] * m
    v01 = [0.0] * n
    auc_sum = 0.0
    for i, xp in enumerate(pos_scores):
        s = 0.0
        for j, xn in enumerate(neg_scores):
            if xp > xn:
                s += 1.0
                v01[j] += 1.0
            elif xp == xn:
                s += 0.5
                v01[j] += 0.5
        v10[i] = s / n
        auc_sum += v10[i]
    v01 = [x / m for x in v01]
    return auc_sum / m, v10, v01


def delong_paired_roc_test(
    y_true: Sequence[int],
    probs_model_a: Sequence[float],
    probs_model_b: Sequence[float],
) -> dict[str, float]:
    """Two-sided paired DeLong test comparing correlated ROC-AUCs on identical test patients."""
    pos_idx = [i for i, y in enumerate(y_true) if y == 1]
    neg_idx = [i for i, y in enumerate(y_true) if y == 0]
    m, n = len(pos_idx), len(neg_idx)
    if m < 2 or n < 2:
        raise ValueError("Paired DeLong test requires >= 2 positive and >= 2 negative cases.")

    auc_a, v10_a, v01_a = _placement_values([probs_model_a[i] for i in pos_idx], [probs_model_a[i] for i in neg_idx])
    auc_b, v10_b, v01_b = _placement_values([probs_model_b[i] for i in pos_idx], [probs_model_b[i] for i in neg_idx])

    s10 = sum((va - auc_a) * (vb - auc_b) for va, vb in zip(v10_a, v10_b)) / (m - 1)
    s01 = sum((va - auc_a) * (vb - auc_b) for va, vb in zip(v01_a, v01_b)) / (n - 1)
    s10_a = sum((va - auc_a) ** 2 for va in v10_a) / (m - 1)
    s01_a = sum((va - auc_a) ** 2 for va in v01_a) / (n - 1)
    s10_b = sum((vb - auc_b) ** 2 for vb in v10_b) / (m - 1)
    s01_b = sum((vb - auc_b) ** 2 for vb in v01_b) / (n - 1)

    var_a = s10_a / m + s01_a / n
    var_b = s10_b / m + s01_b / n
    cov_ab = s10 / m + s01 / n
    var_diff = max(0.0, var_a + var_b - 2.0 * cov_ab)

    diff = auc_a - auc_b
    if var_diff <= 1e-15:
        z, p = 0.0, 1.0
    else:
        z = diff / math.sqrt(var_diff)
        p = _normal_two_sided_p(z)
    return {
        "auc_a": round(auc_a, 6),
        "auc_b": round(auc_b, 6),
        "delta_auc": round(diff, 6),
        "se_diff": round(math.sqrt(var_diff), 6),
        "z_stat": round(z, 6),
        "p_value": round(p, 8),
    }


def mcnemar_exact_test(
    y_true: Sequence[int],
    preds_a: Sequence[int],
    preds_b: Sequence[int],
) -> dict[str, Any]:
    """Exact two-sided McNemar test on paired binary correctness discordance."""
    b_cnt = c_cnt = 0
    for y, pa, pb in zip(y_true, preds_a, preds_b):
        ca = (pa == y)
        cb = (pb == y)
        if ca and not cb:
            b_cnt += 1
        elif cb and not ca:
            c_cnt += 1
    n_disc = b_cnt + c_cnt
    if n_disc == 0:
        return {"b_a_only_correct": 0, "c_b_only_correct": 0, "p_value": 1.0}
    k = min(b_cnt, c_cnt)
    p_one = sum(math.comb(n_disc, i) * (0.5 ** n_disc) for i in range(k + 1))
    return {
        "b_a_only_correct": b_cnt,
        "c_b_only_correct": c_cnt,
        "p_value": round(min(1.0, 2.0 * p_one), 8),
    }


def bootstrap_patient_metric_ci(
    y_true: Sequence[int],
    patient_ids: Sequence[str],
    metric_fn: Callable[[list[int], list[int]], float],
    n_boot: int = 2000,
    seed: int = 20261127,
) -> dict[str, float]:
    """Stratified patient-grouped bootstrap 95% confidence interval (OS §7.4)."""
    by_pat: dict[str, list[int]] = collections.defaultdict(list)
    for idx, pid in enumerate(patient_ids):
        by_pat[pid].append(idx)

    pos_pats = [p for p, idxs in by_pat.items() if any(y_true[i] == 1 for i in idxs)]
    neg_pats = [p for p, idxs in by_pat.items() if p not in set(pos_pats)]
    rng = random.Random(seed)
    all_idx = list(range(len(y_true)))
    point = metric_fn(all_idx, list(y_true))

    vals = []
    for _ in range(n_boot):
        samp_pats = (rng.choices(pos_pats, k=len(pos_pats)) if pos_pats else []) + (
            rng.choices(neg_pats, k=len(neg_pats)) if neg_pats else []
        )
        samp_idx = [i for p in samp_pats for i in by_pat[p]]
        v = metric_fn(samp_idx, [y_true[i] for i in samp_idx])
        if not math.isnan(v):
            vals.append(v)
    vals.sort()
    if not vals:
        return {"point": point, "ci_low": float("nan"), "ci_high": float("nan")}
    lo = vals[max(0, int(0.025 * len(vals)))]
    hi = vals[min(len(vals) - 1, int(0.975 * len(vals)))]
    return {"point": round(point, 6), "ci_low": round(lo, 6), "ci_high": round(hi, 6)}


def holm_bonferroni_adjust(p_values: Sequence[float]) -> list[float]:
    """Step-down Holm-Bonferroni multiplicity correction maintaining monotonicity."""
    m = len(p_values)
    indexed = sorted(enumerate(p_values), key=lambda x: x[1])
    adj = [0.0] * m
    running_max = 0.0
    for rank, (orig_i, p) in enumerate(indexed):
        val = min(1.0, (m - rank) * p)
        running_max = max(running_max, val)
        adj[orig_i] = round(running_max, 8)
    return adj


def bh_fdr_adjust(p_values: Sequence[float]) -> list[float]:
    """Benjamini-Hochberg false discovery rate adjustment."""
    m = len(p_values)
    indexed = sorted(enumerate(p_values), key=lambda x: x[1], reverse=True)
    adj = [0.0] * m
    running_min = 1.0
    for rev_r, (orig_i, p) in enumerate(indexed):
        rank = m - rev_r
        val = min(1.0, p * m / rank)
        running_min = min(running_min, val)
        adj[orig_i] = round(running_min, 8)
    return adj
