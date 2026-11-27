"""
Multimodal SHAP Faithfulness, Stability & Shortcut Audit Hooks (STEP-026 / OS §8).

Governance Notice (`DEC0012` / `STEP-025`):
XAI computations execute strictly AFTER G11 evaluation freeze in Stage S15 (`STEP-038-040`).
This module verifies and exposes the exact mathematical contracts ahead of training:
- `sample_train_only_background`: strictly blocks Val/Test background leakage (`PermissionError`).
- `check_shap_additivity`: verifies local SHAP efficiency axiom within `tol <= 0.02`.
- `aggregate_modality_shares`: computes `[C%, E%, L%, S%]` normalized strictly over active modalities.
- `evaluate_aopc_faithfulness`: Deletion (comprehensiveness) & Insertion (sufficiency) AOPC curves
  compared explicitly against Random and Reverse-Importance negative controls (`P0029`/`OS §8.2`).
- `rank_stability_metrics`: Multi-seed Spearman rho & Top-k Jaccard similarity.
- `audit_mnar_shortcut_flags`: Detects whether `_isnan` missingness masks dominate physiological drivers.
"""

from __future__ import annotations

import math
import random
from typing import Any, Callable, Sequence


def sample_train_only_background(
    records: Sequence[Any],
    split_tags: Sequence[str],
    n_bg: int = 256,
    seed: int = 20261127,
) -> list[Any]:
    """Draw SHAP background distribution strictly from Train partition (OS §8.1)."""
    if len(records) != len(split_tags):
        raise ValueError("records and split_tags lengths must match.")
    forbidden = {str(t).strip().lower() for t in split_tags} - {"train"}
    if forbidden:
        raise PermissionError(
            f"XAI_BACKGROUND_LEAKAGE: Non-train split_tags {sorted(forbidden)} barred from SHAP background!"
        )
    rng = random.Random(seed)
    k = min(n_bg, len(records))
    return rng.sample(list(records), k)


def check_shap_additivity(
    phi_matrix: Sequence[Sequence[float]],
    base_value: float,
    predictions: Sequence[float],
    tol: float = 0.02,
) -> dict[str, Any]:
    """Verify Shapley efficiency axiom |f(x) - (phi_0 + sum phi_i)| <= tol * max(1, |f(x)|)."""
    max_abs_err = 0.0
    max_rel_err = 0.0
    violations = 0
    for phi, pred in zip(phi_matrix, predictions):
        recon = base_value + sum(phi)
        abs_e = abs(pred - recon)
        rel_e = abs_e / max(1.0, abs(pred))
        max_abs_err = max(max_abs_err, abs_e)
        max_rel_err = max(max_rel_err, rel_e)
        if rel_e > tol:
            violations += 1
    return {
        "max_abs_error": round(max_abs_err, 8),
        "max_rel_error": round(max_rel_err, 8),
        "violations": violations,
        "passed": violations == 0,
    }


def aggregate_modality_shares(
    abs_attributions: Sequence[float],
    modality_slices: dict[str, Sequence[int]],
    modality_mask: Sequence[int],
) -> dict[str, float]:
    """Normalize mean |SHAP| modality shares [C%, E%, L%, S%] across active modalities only."""
    order = ("clinical", "ecg", "laboratory", "lifestyle")
    raw = {}
    for m_idx, m_name in enumerate(order):
        if int(modality_mask[m_idx]) == 0:
            raw[m_name] = 0.0
        else:
            idxs = modality_slices.get(m_name, ())
            raw[m_name] = sum(abs(abs_attributions[i]) for i in idxs)
    tot = sum(raw.values())
    if tot <= 1e-12:
        return {k: 0.0 for k in order}
    return {k: round(raw[k] * 100.0 / tot, 4) for k in order}


def evaluate_aopc_faithfulness(
    predict_fn: Callable[[list[list[float]]], list[float]],
    X_eval: Sequence[Sequence[float]],
    phi_eval: Sequence[Sequence[float]],
    baseline_vec: Sequence[float],
    max_k: int | None = None,
    seed: int = 20261127,
) -> dict[str, Any]:
    """
    Compute Deletion AOPC (Comprehensiveness) & Insertion AOPC (Sufficiency)
    versus Random and Reverse-Importance negative controls (`UD20`).
    """
    n_rows = len(X_eval)
    d = len(baseline_vec)
    k_lim = min(d, max_k) if max_k is not None else d
    rng = random.Random(seed)

    base_preds = predict_fn([list(r) for r in X_eval])
    zero_base_preds = predict_fn([list(baseline_vec) for _ in X_eval])

    del_top_drops: list[float] = [0.0] * k_lim
    del_rand_drops: list[float] = [0.0] * k_lim
    del_rev_drops: list[float] = [0.0] * k_lim
    ins_top_gains: list[float] = [0.0] * k_lim
    ins_rand_gains: list[float] = [0.0] * k_lim

    top_orders = [sorted(range(d), key=lambda i: abs(phi[i]), reverse=True) for phi in phi_eval]
    rev_orders = [list(reversed(ord_i)) for ord_i in top_orders]
    rand_orders = []
    for _ in range(n_rows):
        ro = list(range(d))
        rng.shuffle(ro)
        rand_orders.append(ro)

    for k in range(1, k_lim + 1):
        # 1. Deletion batches
        b_top, b_rand, b_rev = [], [], []
        # 2. Insertion batches
        i_top, i_rand = [], []
        for r_idx, row in enumerate(X_eval):
            t_del = list(row)
            r_del = list(row)
            v_del = list(row)
            t_ins = list(baseline_vec)
            r_ins = list(baseline_vec)
            for j in top_orders[r_idx][:k]:
                t_del[j] = baseline_vec[j]
                t_ins[j] = row[j]
            for j in rand_orders[r_idx][:k]:
                r_del[j] = baseline_vec[j]
                r_ins[j] = row[j]
            for j in rev_orders[r_idx][:k]:
                v_del[j] = baseline_vec[j]
            b_top.append(t_del)
            b_rand.append(r_del)
            b_rev.append(v_del)
            i_top.append(t_ins)
            i_rand.append(r_ins)

        p_del_top = predict_fn(b_top)
        p_del_rand = predict_fn(b_rand)
        p_del_rev = predict_fn(b_rev)
        p_ins_top = predict_fn(i_top)
        p_ins_rand = predict_fn(i_rand)

        # Measure absolute/signed probability perturbation magnitude relative to unperturbed score
        del_top_drops[k - 1] = sum(abs(p0 - pk) for p0, pk in zip(base_preds, p_del_top)) / n_rows
        del_rand_drops[k - 1] = sum(abs(p0 - pk) for p0, pk in zip(base_preds, p_del_rand)) / n_rows
        del_rev_drops[k - 1] = sum(abs(p0 - pk) for p0, pk in zip(base_preds, p_del_rev)) / n_rows
        ins_top_gains[k - 1] = sum(1.0 - abs(p0 - pk) for p0, pk in zip(base_preds, p_ins_top)) / n_rows
        ins_rand_gains[k - 1] = sum(1.0 - abs(p0 - pk) for p0, pk in zip(base_preds, p_ins_rand)) / n_rows

    aopc_del_top = sum(del_top_drops) / k_lim
    aopc_del_rand = sum(del_rand_drops) / k_lim
    aopc_del_rev = sum(del_rev_drops) / k_lim
    aopc_ins_top = sum(ins_top_gains) / k_lim
    aopc_ins_rand = sum(ins_rand_gains) / k_lim

    return {
        "aopc_deletion_top": round(aopc_del_top, 6),
        "aopc_deletion_random": round(aopc_del_rand, 6),
        "aopc_deletion_reverse": round(aopc_del_rev, 6),
        "aopc_insertion_top": round(aopc_ins_top, 6),
        "aopc_insertion_random": round(aopc_ins_rand, 6),
        "deletion_beats_random": aopc_del_top > aopc_del_rand,
        "deletion_beats_reverse": aopc_del_top > aopc_del_rev,
        "insertion_beats_random": aopc_ins_top > aopc_ins_rand,
        "baseline_score": round(sum(zero_base_preds) / n_rows, 6),
    }


def rank_stability_metrics(
    importance_seed_a: Sequence[float],
    importance_seed_b: Sequence[float],
    top_k: int = 5,
) -> dict[str, float]:
    """Compute Spearman rank correlation rho and Top-k Jaccard across seeds."""
    d = len(importance_seed_a)
    if d != len(importance_seed_b) or d < 2:
        raise ValueError("Feature importance vectors must match in length >= 2.")

    def _ranks(vals: Sequence[float]) -> list[float]:
        ordered = sorted(enumerate(vals), key=lambda x: x[1], reverse=True)
        r = [0.0] * d
        for rank, (idx, _) in enumerate(ordered, 1):
            r[idx] = float(rank)
        return r

    ra, rb = _ranks(importance_seed_a), _ranks(importance_seed_b)
    ma, mb = sum(ra) / d, sum(rb) / d
    num = sum((a - ma) * (b - mb) for a, b in zip(ra, rb))
    den = math.sqrt(sum((a - ma) ** 2 for a in ra) * sum((b - mb) ** 2 for b in rb))
    rho = (num / den) if den > 0 else 0.0

    top_a = set(sorted(range(d), key=lambda i: importance_seed_a[i], reverse=True)[:top_k])
    top_b = set(sorted(range(d), key=lambda i: importance_seed_b[i], reverse=True)[:top_k])
    jacc = len(top_a & top_b) / max(1, len(top_a | top_b))
    return {"spearman_rho": round(rho, 6), "top_k_jaccard": round(jacc, 6)}


def audit_mnar_shortcut_flags(
    feature_names: Sequence[str],
    global_mean_abs_shap: Sequence[float],
    top_k: int = 3,
) -> dict[str, Any]:
    """Flag whether `_isnan` MNAR missingness masks or site proxies dominate Top-k global SHAP."""
    ordered = sorted(zip(feature_names, global_mean_abs_shap), key=lambda x: x[1], reverse=True)
    top_feats = [name for name, _ in ordered[:top_k]]
    shortcut_hits = [n for n in top_feats if n.endswith("_isnan") or "MISSING" in n]
    return {
        "top_features": top_feats,
        "shortcut_hits_in_top_k": shortcut_hits,
        "shortcut_free": len(shortcut_hits) == 0,
    }
