"""
Leakage-Free Multimodal Tabular Preprocessing Module (STEP-019).

Strictly decouples:
- Stage A (`StageARecordCleaner`): deterministic record-local cleaning and schema/leakage assertions.
- Stage B (`TrainOnlyTabularPreprocessor`): stateful imputation, MNAR missingness masks, robust scaling,
  and one-hot categorical encoding that REFUSES to fit on validation or test partitions (`OS §4.4`).
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Sequence

from src.cvd_mm.schema_ecg import assert_no_leakage_predictors


def build_modality_presence_mask(
    has_clinical: bool,
    has_ecg: bool,
    has_lab: bool,
    has_lifestyle: bool,
) -> list[int]:
    """Return canonical 4D modality mask [C, E, L, S] as binary ints."""
    return [int(bool(has_clinical)), int(bool(has_ecg)), int(bool(has_lab)), int(bool(has_lifestyle))]


class StageARecordCleaner:
    """Zero-parameter, record-local deterministic cleaner safe prior to splitting."""

    @staticmethod
    def validate_feature_schema(feature_names: Sequence[str], tier: str = "A") -> None:
        """Enforce OS §5.1 predictor leakage & Tier-A Troponin-I exclusions."""
        assert_no_leakage_predictors(feature_names, var_rows=None, tier=tier)

    @staticmethod
    def clean_record(raw_row: dict[str, Any], ds_id: str) -> dict[str, Any]:
        """Convert units and apply deterministic physiological range flags per single encounter."""
        out = dict(raw_row)
        # Age in years (handle sulianova age in days deterministically)
        if ds_id == "DS0004" and "age_days" in out and out["age_days"] not in (None, ""):
            out["age_years"] = round(float(out["age_days"]) / 365.25, 4)

        # Harmonize height (cm) and BMI if needed
        ht = out.get("height_cm")
        wt = out.get("weight_kg")
        if ht not in (None, ""):
            ht_val = float(ht)
            out["height_cm"] = ht_val if 100.0 <= ht_val <= 220.0 else None
        if wt not in (None, ""):
            wt_val = float(wt)
            out["weight_kg"] = wt_val if 30.0 <= wt_val <= 200.0 else None
        if out.get("height_cm") and out.get("weight_kg") and out.get("bmi_kgm2") in (None, ""):
            bmi_val = out["weight_kg"] / ((out["height_cm"] / 100.0) ** 2)
            out["bmi_kgm2"] = round(bmi_val, 3) if 10.0 <= bmi_val <= 70.0 else None

        # Check negative LDL artifact (DS0003)
        if "ldl_estimated_mgdl" in out and out["ldl_estimated_mgdl"] not in (None, ""):
            ldl = float(out["ldl_estimated_mgdl"])
            out["ldl_estimated_mgdl"] = ldl if ldl >= 0.0 else None

        return out


class TrainOnlyTabularPreprocessor:
    """
    Stateful Stage B preprocessor guaranteeing strict Train-only parameter fitting (`OS §4.4`).
    Emits binary MNAR missingness masks, Train-median imputed values scaled by Train Robust IQR,
    and Train-only one-hot encoded categories.
    """

    def __init__(
        self,
        numeric_cols: Sequence[str],
        categorical_cols: Sequence[str] = (),
        tier: str = "A",
    ) -> None:
        StageARecordCleaner.validate_feature_schema(list(numeric_cols) + list(categorical_cols), tier=tier)
        self.numeric_cols = list(numeric_cols)
        self.categorical_cols = list(categorical_cols)
        self.tier = tier
        self.fitted = False
        self.medians_: dict[str, float] = {}
        self.iqrs_: dict[str, float] = {}
        self.cat_vocab_: dict[str, list[str]] = {}
        self.fit_state_hash_: str = ""

    @staticmethod
    def _quantile(sorted_vals: list[float], q: float) -> float:
        n = len(sorted_vals)
        if n == 1:
            return sorted_vals[0]
        pos = q * (n - 1)
        lo = int(math.floor(pos))
        hi = int(math.ceil(pos))
        frac = pos - lo
        return sorted_vals[lo] * (1.0 - frac) + sorted_vals[hi] * frac

    def fit(
        self,
        records: Sequence[dict[str, Any]],
        split_tags: Sequence[str] | None = None,
    ) -> "TrainOnlyTabularPreprocessor":
        """
        Fit medians, IQRs, and categorical vocabularies EXCLUSIVELY on rows tagged 'train'.
        Raises PermissionError immediately if any non-'train' partition is supplied.
        """
        if not records:
            raise ValueError("Cannot fit TrainOnlyTabularPreprocessor on empty records.")
        if split_tags is None:
            raise ValueError("split_tags must be provided explicitly to prove Train-only isolation.")
        if len(split_tags) != len(records):
            raise ValueError("split_tags length must match records length.")

        forbidden = {str(t).strip().lower() for t in split_tags} - {"train"}
        if forbidden:
            raise PermissionError(
                f"LEAKAGE_VIOLATION: Stage B .fit() received non-train split tag(s): {sorted(forbidden)}"
            )

        self.medians_.clear()
        self.iqrs_.clear()
        for col in self.numeric_cols:
            vals = sorted(
                float(r[col])
                for r in records
                if r.get(col) not in (None, "") and not (isinstance(r.get(col), float) and math.isnan(r[col]))
            )
            if not vals:
                self.medians_[col] = 0.0
                self.iqrs_[col] = 1.0
            else:
                med = self._quantile(vals, 0.5)
                q25 = self._quantile(vals, 0.25)
                q75 = self._quantile(vals, 0.75)
                iqr = q75 - q25
                self.medians_[col] = med
                self.iqrs_[col] = iqr if iqr > 1e-9 else 1.0

        self.cat_vocab_.clear()
        for col in self.categorical_cols:
            cats = sorted({
                str(r[col]).strip()
                for r in records
                if r.get(col) not in (None, "") and str(r[col]).strip() != ""
            })
            self.cat_vocab_[col] = cats

        state_payload = json.dumps(
            {
                "numeric_cols": self.numeric_cols,
                "categorical_cols": self.categorical_cols,
                "medians": self.medians_,
                "iqrs": self.iqrs_,
                "cat_vocab": self.cat_vocab_,
            },
            sort_keys=True,
        ).encode("utf-8")
        self.fit_state_hash_ = hashlib.sha256(state_payload).hexdigest()
        self.fitted = True
        return self

    def feature_names(self) -> list[str]:
        names = []
        for col in self.numeric_cols:
            names.append(col)
            names.append(f"{col}_isnan")
        for col in self.categorical_cols:
            for val in self.cat_vocab_[col]:
                names.append(f"{col}__{val}")
            names.append(f"{col}__MISSING")
        return names

    def transform(self, records: Sequence[dict[str, Any]]) -> list[list[float]]:
        """Transform records into dense float vectors using frozen Train-only fit state."""
        if not self.fitted:
            raise RuntimeError("TrainOnlyTabularPreprocessor must be fitted on Train before transform().")

        out_matrix: list[list[float]] = []
        for r in records:
            vec: list[float] = []
            for col in self.numeric_cols:
                raw = r.get(col)
                is_miss = raw in (None, "") or (isinstance(raw, float) and math.isnan(raw))
                if is_miss:
                    val = self.medians_[col]
                    miss_flag = 1.0
                else:
                    val = float(raw)
                    miss_flag = 0.0
                scaled = (val - self.medians_[col]) / self.iqrs_[col]
                vec.append(scaled)
                vec.append(miss_flag)

            for col in self.categorical_cols:
                raw = str(r.get(col) or "").strip()
                vocab = self.cat_vocab_[col]
                is_miss = raw == ""
                for v in vocab:
                    vec.append(1.0 if (not is_miss and raw == v) else 0.0)
                vec.append(1.0 if (is_miss or raw not in vocab) else 0.0)
            out_matrix.append(vec)
        return out_matrix

    def inverse_scale_numeric(self, col: str, scaled_val: float) -> float:
        """Inverse-transform scaled numeric value back to native clinical units (STEP-021 round-trip)."""
        if not self.fitted:
            raise RuntimeError("TrainOnlyTabularPreprocessor must be fitted before inverse scaling.")
        return scaled_val * self.iqrs_[col] + self.medians_[col]
