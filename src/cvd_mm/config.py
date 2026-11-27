"""
Configuration & Lineage Integrity Validator (STEP-026).

Parses expanded T32 YAML experiment configs (using PyYAML when available or a built-in
strict YAML subset parser so zero third-party dependencies are required locally), enforces
exp_t32_schema_v1 rules (zero nulls/missing fields), verifies parent SHA-256 digests, and
prohibits unsealed Test partition access before Gate G11 freeze.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from typing import Any, Mapping

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PREREG_HASHES_PATH = os.path.join(REPO_ROOT, "07_Experiments", "preregistration_hashes.json")
T32_SCHEMA_PATH = os.path.join(REPO_ROOT, "07_Experiments", "configs", "exp_t32_schema_v1.json")

ALLOWED_BLOCKS = {"Block_A", "Block_B", "Block_C", "Block_D", "Block_E", "Block_F", "SMOKE"}
ALLOWED_RQS = {"RQ0", "RQ1", "RQ2", "RQ3", "RQ4"}
ALLOWED_TIERS = {"unimodal", "clinical_score", "simple_fusion", "transformer_fusion", "ablation"}
ALLOWED_SCOPES = {"ALL_COHORTS", "DS0001", "DS0002", "DS0003", "DS0004"}


def _parse_scalar(val: str) -> Any:
    s = val.strip()
    if s in ("null", "Null", "NULL", "~", ""):
        return None
    if s in ("true", "True", "TRUE"):
        return True
    if s in ("false", "False", "FALSE"):
        return False
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(part) for part in inner.split(",")]
    try:
        if "." in s or "e" in s.lower():
            f = float(s)
            if not s.isdigit():
                return f
        return int(s)
    except ValueError:
        return s


def parse_yaml_config(text: str) -> dict[str, Any]:
    """Parse nested YAML config via PyYAML if installed, or pure-stdlib indentation parser."""
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(text)
        if not isinstance(loaded, dict):
            raise ValueError("Top-level experiment config must be a mapping.")
        return loaded
    except ImportError:
        pass

    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    for raw_line in text.splitlines():
        # Strip full-line or inline comments outside quotes
        in_sq = in_dq = False
        cleaned_chars = []
        for ch in raw_line:
            if ch == "'" and not in_dq:
                in_sq = not in_sq
            elif ch == '"' and not in_sq:
                in_dq = not in_dq
            elif ch == "#" and not in_sq and not in_dq:
                break
            cleaned_chars.append(ch)
        line = "".join(cleaned_chars).rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if ":" not in stripped:
            raise ValueError(f"Malformed YAML line: {raw_line}")
        key, rest = stripped.split(":", 1)
        key = key.strip()
        rest = rest.strip()
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if rest == "":
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = _parse_scalar(rest)
    return root


def load_config_file(path: str) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    if path.lower().endswith(".json"):
        obj = json.loads(txt)
        if not isinstance(obj, dict):
            raise ValueError("Top-level JSON config must be an object.")
        return obj
    return parse_yaml_config(txt)


def _assert_no_nulls(obj: Any, prefix: str = "", allow_optional_paths: set[str] | None = None) -> None:
    optional = allow_optional_paths or set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            full = f"{prefix}.{k}" if prefix else k
            if v is None and full not in optional:
                raise ValueError(f"CONFIG_NULL_VIOLATION: Required field '{full}' cannot be null.")
            _assert_no_nulls(v, full, optional)
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            _assert_no_nulls(item, f"{prefix}[{idx}]", optional)


def validate_experiment_config(
    cfg: Mapping[str, Any],
    *,
    allow_frozen_test_eval: bool = False,
    verify_prereg_files: bool = True,
) -> dict[str, Any]:
    """
    Strictly validate T32 config values, preregistered hashes, and Test-partition custody rules.
    Raises ValueError or PermissionError immediately on any violation.
    """
    required_top = [
        "experiment_id", "comparison_block", "research_question_id", "comparator_tier",
        "candidate_id", "approval_record", "source_commit", "data", "model", "training",
        "evaluation_and_calibration", "xai_hooks", "runtime",
    ]
    for k in required_top:
        if k not in cfg:
            raise ValueError(f"CONFIG_MISSING_SECTION: Missing top-level key '{k}'.")

    # Tree/linear baselines do not use Transformer integer fields d_model/nhead/dim_feedforward/dropout
    fw = str(cfg["model"].get("framework") or "").lower()
    optional_nulls = set()
    if fw in ("sklearn", "xgboost", "lightgbm", "custom_score"):
        optional_nulls.update({
            "model.d_model", "model.num_layers", "model.nhead", "model.dim_feedforward",
            "model.dropout", "model.max_trainable_params_budget", "model.pretrained_weights_sha256",
            "training.learning_rate", "training.weight_decay", "training.early_stopping_patience",
        })
    elif str(cfg["model"].get("pretrained_weights_sha256") or "") == "none_from_scratch":
        pass

    _assert_no_nulls(cfg, allow_optional_paths=optional_nulls)

    if not re.match(r"^EXP[0-9]{4}(_SMOKE)?$", str(cfg["experiment_id"])):
        raise ValueError(f"Invalid experiment_id '{cfg['experiment_id']}' (expected EXP#### or EXP####_SMOKE).")
    if cfg["comparison_block"] not in ALLOWED_BLOCKS:
        raise ValueError(f"Invalid comparison_block '{cfg['comparison_block']}'.")
    if cfg["research_question_id"] not in ALLOWED_RQS:
        raise ValueError(f"Invalid research_question_id '{cfg['research_question_id']}'.")
    if cfg["comparator_tier"] not in ALLOWED_TIERS:
        raise ValueError(f"Invalid comparator_tier '{cfg['comparator_tier']}'.")
    if not re.match(r"^MC[0-9]{4}$", str(cfg["candidate_id"])):
        raise ValueError(f"Invalid candidate_id '{cfg['candidate_id']}'.")

    data_cfg = cfg["data"]
    if not re.match(r"^REL[0-9]{4}$", str(data_cfg["release_id"])):
        raise ValueError(f"Invalid release_id '{data_cfg['release_id']}'.")
    if data_cfg["dataset_scope"] not in ALLOWED_SCOPES:
        raise ValueError(f"Invalid dataset_scope '{data_cfg['dataset_scope']}'.")
    if data_cfg.get("allow_troponin_tier_b") not in (False, True):
        raise ValueError("data.allow_troponin_tier_b must be boolean.")

    tr_cfg = cfg["training"]
    if tr_cfg.get("deterministic_mode") is not True:
        raise ValueError("training.deterministic_mode MUST be true.")
    loss_policy = str(tr_cfg.get("loss_and_imbalance_policy", "")).lower()
    if "smote" in loss_policy and "no_smote" not in loss_policy:
        raise PermissionError("LEAKAGE_POLICY_VIOLATION: Pre-split SMOTE is strictly prohibited.")

    ev_cfg = cfg["evaluation_and_calibration"]
    if ev_cfg.get("validation_only_tuning") is not True:
        raise PermissionError("TEST_LEAKAGE_VIOLATION: validation_only_tuning MUST be true.")
    if ev_cfg.get("test_partition_access") != "SEALED_UNTIL_G11" and not allow_frozen_test_eval:
        raise PermissionError(
            "TEST_CUSTODY_VIOLATION: test_partition_access must stay SEALED_UNTIL_G11 during training/tuning."
        )
    if int(ev_cfg.get("bootstrap_resamples", 0)) < 1000:
        raise ValueError("evaluation_and_calibration.bootstrap_resamples must be >= 1000.")

    xai_cfg = cfg["xai_hooks"]
    if xai_cfg.get("background_partition") != "train":
        raise PermissionError("XAI_LEAKAGE_VIOLATION: xai_hooks.background_partition MUST be 'train'.")

    if verify_prereg_files and os.path.isfile(PREREG_HASHES_PATH):
        with open(PREREG_HASHES_PATH, encoding="utf-8") as pf:
            prereg = json.load(pf)["files"]
        exp_h = ev_cfg.get("experiment_plan_sha256")
        eval_h = ev_cfg.get("eval_protocol_sha256")
        xai_h = ev_cfg.get("xai_protocol_sha256")
        if exp_h != prereg["07_Experiments/experiment_plan.md"]:
            raise ValueError("Preregistered experiment_plan_sha256 mismatch!")
        if eval_h != prereg["09_Evaluation_Stats/protocol.md"]:
            raise ValueError("Preregistered eval_protocol_sha256 mismatch!")
        if xai_h != prereg["10_Explainability_XAI/xai_protocol.md"]:
            raise ValueError("Preregistered xai_protocol_sha256 mismatch!")

    return dict(cfg)
