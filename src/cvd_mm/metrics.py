"""
Mandatory Proposal & Q1 Clinical Evaluation Metrics (STEP-026 / OS §7.2–§7.3).

Pure-Python stdlib analytical implementations verified against known edge cases:
- All 6 mandatory proposal metrics: Accuracy, Precision, Recall, F1, ROC-AUC, Confusion Matrix.
- Q1 discrimination & imbalance metrics: PR-AUC, Specificity, NPV, Balanced Accuracy, MCC.
- Probability calibration metrics: Brier Score, Brier Skill Score, ECE (quantile & uniform bins),
  and logistic recalibration Slope & Intercept (via damped Newton-Raphson MLE).
"""

from __future__ import annotations

import math
from typing import Any, Sequence


def _safe_logit(p: float, eps: float = 1e-7) -> float:
    pc = max(eps, min(1.0 - eps, p))
    return math.log(pc / (1.0 - pc))


def _sigmoid(z: float) -> float:
    if z >= 0:
        ez = math.exp(-z)
        return 1.0 / (1.0 + ez)
    ez = math.exp(z)
    return ez / (1.0 + ez)


def confusion_counts(
    y_true: Sequence[int],
    y_prob: Sequence[float],
    threshold: float = 0.5,
) -> dict[str, int]:
    """Compute exact integer TN, FP, FN, TP covering 100% of samples."""
    if len(y_true) != len(y_prob) or not y_true:
        raise ValueError("y_true and y_prob must have matching non-zero length.")
    tn = fp = fn = tp = 0
    for y, p in zip(y_true, y_prob):
        pred = 1 if p >= threshold else 0
        if y == 1 and pred == 1:
            tp += 1
        elif y == 0 and pred == 0:
            tn += 1
        elif y == 0 and pred == 1:
            fp += 1
        elif y == 1 and pred == 0:
            fn += 1
        else:
            raise ValueError(f"Binary labels must be 0/1, got {y}")
    return {"tn": tn, "fp": fp, "fn": fn, "tp": tp}


def roc_auc_score_exact(y_true: Sequence[int], y_prob: Sequence[float]) -> float:
    """Compute exact tie-aware Mann-Whitney / Wilcoxon ROC-AUC."""
    n = len(y_true)
    if n != len(y_prob) or n == 0:
        raise ValueError("Invalid y_true / y_prob inputs.")
    pos_scores = [p for y, p in zip(y_true, y_prob) if y == 1]
    neg_scores = [p for y, p in zip(y_true, y_prob) if y == 0]
    if not pos_scores or not neg_scores:
        return float("nan")

    # Sort combined pairs once for O(N log N) average-rank Mann-Whitney U
    paired = sorted(((float(p), int(y)) for y, p in zip(y_true, y_prob)), key=lambda x: x[0])
    rank_sum_pos = 0.0
    i = 0
    while i < n:
        j = i + 1
        while j < n and paired[j][0] == paired[i][0]:
            j += 1
        avg_rank = 0.5 * ((i + 1) + j)
        pos_in_tie = sum(paired[k][1] for k in range(i, j))
        rank_sum_pos += pos_in_tie * avg_rank
        i = j

    n_pos = len(pos_scores)
    n_neg = len(neg_scores)
    u = rank_sum_pos - (n_pos * (n_pos + 1)) / 2.0
    return u / (n_pos * n_neg)


def pr_auc_score_exact(y_true: Sequence[int], y_prob: Sequence[float]) -> float:
    """Compute average precision (area under step Precision-Recall curve, AP / PR-AUC)."""
    n_pos = sum(y_true)
    if n_pos == 0:
        return float("nan")
    paired = sorted(zip(y_prob, y_true), key=lambda x: x[0], reverse=True)
    tp = 0
    ap = 0.0
    i = 0
    n = len(paired)
    while i < n:
        # Process tied probabilities together
        j = i + 1
        while j < n and paired[j][0] == paired[i][0]:
            j += 1
        delta_tp = sum(paired[k][1] for k in range(i, j))
        tp += delta_tp
        if delta_tp > 0:
            precision_at_j = tp / j
            ap += precision_at_j * (delta_tp / n_pos)
        i = j
    return ap


def expected_calibration_error(
    y_true: Sequence[int],
    y_prob: Sequence[float],
    n_bins: int = 15,
    quantile: bool = True,
) -> float:
    """Compute ECE across quantile (primary) or equal-width probability bins."""
    n = len(y_true)
    if n == 0:
        return float("nan")
    order = sorted(zip(y_prob, y_true), key=lambda x: x[0])
    ece = 0.0
    if quantile:
        for b in range(n_bins):
            lo = (b * n) // n_bins
            hi = ((b + 1) * n) // n_bins
            if hi <= lo:
                continue
            chunk = order[lo:hi]
            avg_p = sum(p for p, _ in chunk) / len(chunk)
            avg_y = sum(y for _, y in chunk) / len(chunk)
            ece += (len(chunk) / n) * abs(avg_y - avg_p)
    else:
        for b in range(n_bins):
            lo_v, hi_v = b / n_bins, (b + 1) / n_bins
            chunk = [
                (p, y) for p, y in order if (lo_v <= p < hi_v) or (b == n_bins - 1 and p == 1.0)
            ]
            if not chunk:
                continue
            avg_p = sum(p for p, _ in chunk) / len(chunk)
            avg_y = sum(y for _, y in chunk) / len(chunk)
            ece += (len(chunk) / n) * abs(avg_y - avg_p)
    return ece


def logistic_calibration_slope_intercept(
    y_true: Sequence[int],
    y_prob: Sequence[float],
    max_iter: int = 40,
) -> tuple[float, float]:
    """Fit Cox logistic recalibration logit(P(y=1)) = intercept + slope * logit(p_hat)."""
    xs = [_safe_logit(p) for p in y_prob]
    ys = [float(y) for y in y_true]
    alpha, beta = 0.0, 1.0
    for _ in range(max_iter):
        g0 = g1 = h00 = h01 = h11 = 0.0
        for x, y in zip(xs, ys):
            p = _sigmoid(alpha + beta * x)
            w = max(1e-8, p * (1.0 - p))
            diff = p - y
            g0 += diff
            g1 += diff * x
            h00 += w
            h01 += w * x
            h11 += w * x * x
        # Slight ridge stabilizes degenerate separable synthetic cases
        h00 += 1e-6
        h11 += 1e-6
        det = h00 * h11 - h01 * h01
        if abs(det) < 1e-12:
            break
        da = (h11 * g0 - h01 * g1) / det
        db = (-h01 * g0 + h00 * g1) / det
        alpha -= da
        beta -= db
        if abs(da) < 1e-8 and abs(db) < 1e-8:
            break
    return beta, alpha


def compute_all_metrics(
    y_true: Sequence[int],
    y_prob: Sequence[float],
    threshold: float = 0.5,
) -> dict[str, Any]:
    """Return full dictionary covering all 6 mandatory proposal metrics + Q1 extensions."""
    cm = confusion_counts(y_true, y_prob, threshold=threshold)
    tn, fp, fn, tp = cm["tn"], cm["fp"], cm["fn"], cm["tp"]
    n = tn + fp + fn + tp
    prev = (tp + fn) / n

    acc = (tp + tn) / n
    prec = (tp / (tp + fp)) if (tp + fp) > 0 else None
    rec = (tp / (tp + fn)) if (tp + fn) > 0 else None
    spec = (tn / (tn + fp)) if (tn + fp) > 0 else None
    npv = (tn / (tn + fn)) if (tn + fn) > 0 else None
    f1 = (2.0 * prec * rec / (prec + rec)) if (prec is not None and rec is not None and (prec + rec) > 0) else 0.0
    bal_acc = (0.5 * ((rec or 0.0) + (spec or 0.0)))
    mcc_den = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    mcc = ((tp * tn - fp * fn) / mcc_den) if mcc_den > 0 else 0.0

    roc_auc = roc_auc_score_exact(y_true, y_prob)
    pr_auc = pr_auc_score_exact(y_true, y_prob)
    brier = sum((p - y) ** 2 for y, p in zip(y_true, y_prob)) / n
    brier_ref = prev * (1.0 - prev)
    bss = (1.0 - brier / brier_ref) if brier_ref > 1e-9 else 0.0
    ece_q = expected_calibration_error(y_true, y_prob, n_bins=15, quantile=True)
    ece_u = expected_calibration_error(y_true, y_prob, n_bins=15, quantile=False)
    slope, intercept = logistic_calibration_slope_intercept(y_true, y_prob)

    return {
        "n_eval": n,
        "prevalence": round(prev, 6),
        "threshold": threshold,
        "accuracy": round(acc, 6),
        "precision": round(prec, 6) if prec is not None else None,
        "recall": round(rec, 6) if rec is not None else None,
        "f1": round(f1, 6),
        "roc_auc": round(roc_auc, 6) if not math.isnan(roc_auc) else None,
        "confusion_matrix": [[tn, fp], [fn, tp]],
        "pr_auc": round(pr_auc, 6) if not math.isnan(pr_auc) else None,
        "specificity": round(spec, 6) if spec is not None else None,
        "npv": round(npv, 6) if npv is not None else None,
        "balanced_accuracy": round(bal_acc, 6),
        "mcc": round(mcc, 6),
        "brier_score": round(brier, 6),
        "brier_skill_score": round(bss, 6),
        "ece_quantile_15": round(ece_q, 6),
        "ece_uniform_15": round(ece_u, 6),
        "calibration_slope": round(slope, 6),
        "calibration_intercept": round(intercept, 6),
    }
