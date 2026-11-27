"""Tier 1-3 baselines & clinical heuristic scorers (MC0001-MC0005, MC0011, MC0013).

Provides both:
  1. Pure-Python stdlib L2-regularized Logistic Regression + WHO/Framingham
     contextual baseline + Late OOF Logit Stacker that execute deterministically on
     Windows Python 3.13 without extra libraries.
  2. Kaggle GPU/CPU SklearnBaselineSuite wrapping LogisticRegression, RandomForest,
     SVC+Platt, XGBoost, and LightGBM with strict Train-only pos_weight handling.
"""

from __future__ import annotations

import math
import random
from typing import Any, Sequence

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.svm import SVC

    HAS_SKLEARN = True
except ImportError:
    RandomForestClassifier = None
    LogisticRegression = None
    SVC = None
    HAS_SKLEARN = False

try:
    from xgboost import XGBClassifier

    HAS_XGBOOST = True
except ImportError:
    XGBClassifier = None
    HAS_XGBOOST = False

try:
    from lightgbm import LGBMClassifier

    HAS_LIGHTGBM = True
except ImportError:
    LGBMClassifier = None
    HAS_LIGHTGBM = False


def _sigmoid(z: float) -> float:
    if z >= 0.0:
        return 1.0 / (1.0 + math.exp(-min(z, 60.0)))
    ez = math.exp(max(z, -60.0))
    return ez / (1.0 + ez)


class PurePythonLogisticModel:
    """Stdlib L2-regularized binary logistic regression supporting Train pos_weight
    and exact deterministic state serialization for checkpoint recovery verification.
    """

    def __init__(
        self,
        n_features: int,
        l2: float = 1e-3,
        lr: float = 0.15,
        pos_weight: float = 1.0,
        seed: int = 42,
    ) -> None:
        if n_features <= 0:
            raise ValueError(f"n_features must be > 0, got {n_features}")
        self.n_features = n_features
        self.l2 = float(l2)
        self.lr = float(lr)
        self.pos_weight = float(pos_weight)
        self.seed = int(seed)
        self.weights = [0.0] * n_features
        self.bias = 0.0
        self.epoch = 0

    def predict_logits(self, X: Sequence[Sequence[float]]) -> list[float]:
        out: list[float] = []
        w = self.weights
        b = self.bias
        for row in X:
            z = b + sum(wi * float(xi) for wi, xi in zip(w, row))
            out.append(z)
        return out

    def predict_proba(self, X: Sequence[Sequence[float]]) -> list[float]:
        return [_sigmoid(z) for z in self.predict_logits(X)]

    def step_epoch(self, X: Sequence[Sequence[float]], y: Sequence[int]) -> float:
        """Run one deterministic shuffled batch gradient epoch; return weighted BCE loss."""
        n = len(X)
        if n == 0 or n != len(y):
            raise ValueError("X and y must be non-empty and have equal length.")
        order = list(range(n))
        rng = random.Random(self.seed + self.epoch)
        rng.shuffle(order)

        grad_w = [0.0] * self.n_features
        grad_b = 0.0
        loss_sum = 0.0
        weight_sum = 0.0

        for idx in order:
            row = X[idx]
            yi = 1.0 if int(y[idx]) == 1 else 0.0
            wi = self.pos_weight if yi == 1.0 else 1.0
            z = self.bias + sum(w * float(xv) for w, xv in zip(self.weights, row))
            p = _sigmoid(z)
            eps = 1e-12
            loss_sum += -wi * (yi * math.log(max(p, eps)) + (1.0 - yi) * math.log(max(1.0 - p, eps)))
            weight_sum += wi
            err = wi * (p - yi)
            grad_b += err
            for j in range(self.n_features):
                grad_w[j] += err * float(row[j])

        inv_w = 1.0 / max(weight_sum, 1.0)
        self.bias -= self.lr * (grad_b * inv_w)
        for j in range(self.n_features):
            reg = self.l2 * self.weights[j]
            self.weights[j] -= self.lr * (grad_w[j] * inv_w + reg)

        self.epoch += 1
        return loss_sum * inv_w + 0.5 * self.l2 * sum(w * w for w in self.weights)

    def fit(self, X: Sequence[Sequence[float]], y: Sequence[int], epochs: int = 50) -> list[float]:
        return [self.step_epoch(X, y) for _ in range(epochs)]

    def get_state_dict(self) -> dict[str, Any]:
        return {
            "n_features": self.n_features,
            "l2": self.l2,
            "lr": self.lr,
            "pos_weight": self.pos_weight,
            "seed": self.seed,
            "weights": list(self.weights),
            "bias": float(self.bias),
            "epoch": int(self.epoch),
        }

    def load_state_dict(self, state: dict[str, Any]) -> None:
        self.n_features = int(state["n_features"])
        self.l2 = float(state["l2"])
        self.lr = float(state["lr"])
        self.pos_weight = float(state["pos_weight"])
        self.seed = int(state["seed"])
        self.weights = [float(w) for w in state["weights"]]
        self.bias = float(state["bias"])
        self.epoch = int(state["epoch"])


class WHOFraminghamContextScorer:
    """MC0011 Domain Clinical Baseline approximating Framingham/WHO directional risk
    on robustly scaled clinical/laboratory/lifestyle covariates without external APIs.
    """

    def __init__(self, weights: dict[str, float] | None = None, bias: float = -0.35) -> None:
        self.weights = weights or {
            "age_z": 0.65,
            "sbp_z": 0.45,
            "chol_z": 0.30,
            "gluc_z": 0.28,
            "bmi_z": 0.20,
            "smoke": 0.35,
            "male": 0.22,
        }
        self.bias = bias

    def predict_proba(self, records: Sequence[dict[str, float]]) -> list[float]:
        probs: list[float] = []
        for rec in records:
            score = self.bias
            for k, w in self.weights.items():
                score += w * float(rec.get(k, 0.0))
            probs.append(_sigmoid(score))
        return probs


class LateOOFStacker:
    """MC0013 Level-1 Late Stacking over OOF modality risk logits + CELS mask."""

    def __init__(self, n_modalities: int = 4, l2: float = 1e-2, seed: int = 42) -> None:
        self.model = PurePythonLogisticModel(n_features=n_modalities * 2, l2=l2, lr=0.1, seed=seed)

    @staticmethod
    def _build_features(oof_probs: Sequence[Sequence[float]], masks_cels: Sequence[Sequence[int]]) -> list[list[float]]:
        rows: list[list[float]] = []
        for ps, ms in zip(oof_probs, masks_cels):
            logits = []
            for p, m in zip(ps, ms):
                if m:
                    pc = min(max(float(p), 1e-6), 1.0 - 1e-6)
                    logits.append(math.log(pc / (1.0 - pc)))
                else:
                    logits.append(0.0)
            rows.append(logits + [float(m) for m in ms])
        return rows

    def fit(self, oof_probs: Sequence[Sequence[float]], masks_cels: Sequence[Sequence[int]], y: Sequence[int]) -> list[float]:
        feats = self._build_features(oof_probs, masks_cels)
        return self.model.fit(feats, y, epochs=80)

    def predict_proba(self, oof_probs: Sequence[Sequence[float]], masks_cels: Sequence[Sequence[int]]) -> list[float]:
        feats = self._build_features(oof_probs, masks_cels)
        return self.model.predict_proba(feats)


class SklearnBaselineSuite:
    """Factory creating MC0001-MC0005 tabular models on Kaggle."""

    @staticmethod
    def build(candidate_id: str, seed: int = 42, scale_pos_weight: float = 1.0) -> Any:
        if candidate_id == "MC0001":
            if not HAS_SKLEARN:
                raise RuntimeError("scikit-learn required for MC0001 on Kaggle.")
            return LogisticRegression(C=1.0, max_iter=1000, class_weight="balanced", random_state=seed)
        if candidate_id == "MC0002":
            if not HAS_SKLEARN:
                raise RuntimeError("scikit-learn required for MC0002 on Kaggle.")
            return RandomForestClassifier(
                n_estimators=300, max_depth=12, class_weight="balanced", n_jobs=-1, random_state=seed
            )
        if candidate_id == "MC0003":
            if not HAS_SKLEARN:
                raise RuntimeError("scikit-learn required for MC0003 on Kaggle.")
            return SVC(C=1.0, kernel="rbf", probability=True, class_weight="balanced", random_state=seed)
        if candidate_id == "MC0004":
            if not HAS_XGBOOST:
                raise RuntimeError("xgboost required for MC0004 on Kaggle.")
            return XGBClassifier(
                n_estimators=400,
                max_depth=6,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                scale_pos_weight=scale_pos_weight,
                eval_metric="auc",
                random_state=seed,
                n_jobs=-1,
            )
        if candidate_id == "MC0005":
            if not HAS_LIGHTGBM:
                raise RuntimeError("lightgbm required for MC0005 on Kaggle.")
            return LGBMClassifier(
                n_estimators=400,
                max_depth=-1,
                num_leaves=31,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                scale_pos_weight=scale_pos_weight,
                random_state=seed,
                n_jobs=-1,
                verbose=-1,
            )
        raise ValueError(f"Unsupported tabular baseline candidate_id: {candidate_id}")
