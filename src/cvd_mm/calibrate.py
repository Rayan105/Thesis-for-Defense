"""
Validation-Only Post-Hoc Probability Calibration & Threshold Selection (STEP-026 / UD16).

Enforces strict OS §7.1 custody: fitting any calibrator (`Temperature`, `Platt`, or `Isotonic PAVA`)
or operating threshold (`Youden J`, `Sensitivity >= 0.85`) raises PermissionError if `test` rows
appear inside `split_tags`.
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Sequence


def _assert_val_only_fit_tags(split_tags: Sequence[str] | None, n: int) -> None:
    if split_tags is None or len(split_tags) != n:
        raise ValueError("split_tags matching length n is mandatory to enforce Validation-only calibration.")
    forbidden = {str(t).strip().lower() for t in split_tags} - {"val", "train_oof"}
    if forbidden:
        raise PermissionError(
            f"CALIBRATION_LEAKAGE_VIOLATION: Calibrator/threshold fit received forbidden split tags: {sorted(forbidden)}"
        )


def _sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)


def _logit(p: float, eps: float = 1e-7) -> float:
    pc = max(eps, min(1.0 - eps, p))
    return math.log(pc / (1.0 - pc))


class TemperatureScalingCalibrator:
    """Single-parameter Temperature scaling (`logit_cal = logit / T`) minimizing NLL on Validation."""

    def __init__(self) -> None:
        self.temperature_: float = 1.0
        self.fitted: bool = False
        self.calibrator_hash_: str = ""

    def fit(self, y_val: Sequence[int], logits_val: Sequence[float], split_tags: Sequence[str] | None = None) -> "TemperatureScalingCalibrator":
        _assert_val_only_fit_tags(split_tags, len(y_val))
        best_t, best_nll = 1.0, float("inf")
        # Coarse-to-fine 1D NLL search (deterministic, convex in log-T!)
        for step in range(1, 200):
            t = 0.05 * step
            nll = 0.0
            for y, z in zip(y_val, logits_val):
                p = max(1e-9, min(1.0 - 1e-9, _sigmoid(z / t)))
                nll -= (y * math.log(p) + (1 - y) * math.log(1.0 - p))
            if nll < best_nll:
                best_nll, best_t = nll, t
        self.temperature_ = round(best_t, 6)
        self.fitted = True
        self.calibrator_hash_ = hashlib.sha256(
            json.dumps({"method": "temperature", "T": self.temperature_}, sort_keys=True).encode()
        ).hexdigest()
        return self

    def transform(self, logits: Sequence[float]) -> list[float]:
        if not self.fitted:
            raise RuntimeError("TemperatureScalingCalibrator must be fitted on Validation first.")
        return [_sigmoid(z / self.temperature_) for z in logits]


class PlattLogisticCalibrator:
    """Two-parameter Platt scaling (`p_cal = sigmoid(a * logit + b)`) fitted strictly on Validation."""

    def __init__(self) -> None:
        self.coef_: float = 1.0
        self.intercept_: float = 0.0
        self.fitted: bool = False
        self.calibrator_hash_: str = ""

    def fit(self, y_val: Sequence[int], logits_or_probs: Sequence[float], *, is_prob: bool = False, split_tags: Sequence[str] | None = None) -> "PlattLogisticCalibrator":
        _assert_val_only_fit_tags(split_tags, len(y_val))
        xs = [_logit(v) if is_prob else float(v) for v in logits_or_probs]
        ys = [float(y) for y in y_val]
        a, b = 1.0, 0.0
        for _ in range(50):
            gb = ga = hbb = hba = haa = 0.0
            for x, y in zip(xs, ys):
                p = _sigmoid(a * x + b)
                w = max(1e-8, p * (1.0 - p))
                diff = p - y
                gb += diff
                ga += diff * x
                hbb += w
                hba += w * x
                haa += w * x * x
            hbb += 1e-4
            haa += 1e-4
            det = hbb * haa - hba * hba
            if abs(det) < 1e-12:
                break
            db = (haa * gb - hba * ga) / det
            da = (-hba * gb + hbb * ga) / det
            b -= db
            a -= da
            if abs(da) < 1e-8 and abs(db) < 1e-8:
                break
        self.coef_, self.intercept_ = a, b
        self.fitted = True
        self.calibrator_hash_ = hashlib.sha256(
            json.dumps({"method": "platt", "a": self.coef_, "b": self.intercept_}, sort_keys=True).encode()
        ).hexdigest()
        return self

    def transform(self, logits_or_probs: Sequence[float], *, is_prob: bool = False) -> list[float]:
        if not self.fitted:
            raise RuntimeError("PlattLogisticCalibrator must be fitted on Validation first.")
        return [_sigmoid(self.coef_ * (_logit(v) if is_prob else float(v)) + self.intercept_) for v in logits_or_probs]


class IsotonicCalibrator:
    """Non-parametric Pool-Adjacent-Violators (PAVA) isotonic calibrator fitted on Validation."""

    def __init__(self) -> None:
        self.blocks_: list[tuple[float, float, float]] = []  # (min_x, max_x, y_val)
        self.fitted: bool = False
        self.calibrator_hash_: str = ""

    def fit(self, y_val: Sequence[int], probs_val: Sequence[float], split_tags: Sequence[str] | None = None) -> "IsotonicCalibrator":
        _assert_val_only_fit_tags(split_tags, len(y_val))
        pts = sorted(zip(probs_val, y_val), key=lambda t: t[0])
        # PAVA pooling: each block is [x_lo, x_hi, sum_y, weight]
        blocks: list[list[float]] = []
        for x, y in pts:
            blocks.append([float(x), float(x), float(y), 1.0])
            while len(blocks) >= 2 and (blocks[-2][2] / blocks[-2][3]) > (blocks[-1][2] / blocks[-1][3]):
                b2 = blocks.pop()
                b1 = blocks[-1]
                b1[1] = max(b1[1], b2[1])
                b1[2] += b2[2]
                b1[3] += b2[3]
        self.blocks_ = [(b[0], b[1], b[2] / b[3]) for b in blocks]
        self.fitted = True
        self.calibrator_hash_ = hashlib.sha256(
            json.dumps({"method": "isotonic", "blocks": self.blocks_}, sort_keys=True).encode()
        ).hexdigest()
        return self

    def transform(self, probs: Sequence[float]) -> list[float]:
        if not self.fitted:
            raise RuntimeError("IsotonicCalibrator must be fitted on Validation first.")
        out = []
        for p in probs:
            val = self.blocks_[0][2]
            for x_lo, _, y_b in self.blocks_:
                if p >= x_lo:
                    val = y_b
                else:
                    break
            out.append(val)
        return out


def select_validation_thresholds(
    y_val: Sequence[int],
    probs_val: Sequence[float],
    split_tags: Sequence[str] | None = None,
    min_sensitivity: float = 0.85,
) -> dict[str, float]:
    """Select frozen operating thresholds (`tau_youden` & `tau_sens_target`) strictly on Validation."""
    _assert_val_only_fit_tags(split_tags, len(y_val))
    n_pos = sum(y_val)
    n_neg = len(y_val) - n_pos
    if n_pos == 0 or n_neg == 0:
        return {"tau_youden": 0.5, "tau_sens_target": 0.5}

    cands = sorted(set(float(p) for p in probs_val))
    best_j, best_tau_j = -1.0, 0.5
    best_tau_s, best_spec_s = cands[0], -1.0

    for tau in cands:
        tp = sum(1 for y, p in zip(y_val, probs_val) if y == 1 and p >= tau)
        tn = sum(1 for y, p in zip(y_val, probs_val) if y == 0 and p < tau)
        sens = tp / n_pos
        spec = tn / n_neg
        j = sens + spec - 1.0
        if j > best_j:
            best_j, best_tau_j = j, tau
        if sens >= min_sensitivity and spec > best_spec_s:
            best_spec_s, best_tau_s = spec, tau

    return {
        "tau_youden": round(best_tau_j, 6),
        "tau_sens_target": round(best_tau_s, 6),
    }
