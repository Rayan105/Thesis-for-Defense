"""CVD Multimodal model registry exports (Tier 1-4 baselines and fusion models)."""

from __future__ import annotations

from src.cvd_mm.models.baselines import (
    HAS_LIGHTGBM,
    HAS_SKLEARN,
    HAS_XGBOOST,
    LateOOFStacker,
    PurePythonLogisticModel,
    SklearnBaselineSuite,
    WHOFraminghamContextScorer,
)
from src.cvd_mm.models.fusion_transformer import (
    HAS_TORCH,
    MODALITY_ORDER_CELS,
    PurePythonMaskedFusionModel,
    build_cels_key_padding_mask,
    get_pytorch_model_classes,
)
from src.cvd_mm.models.train import (
    compute_pos_weight,
    load_checkpoint_bundle,
    save_checkpoint_bundle,
    set_global_seed,
    train_pure_python_logistic_with_checkpoints,
    train_pytorch_model_with_checkpoints,
)

__all__ = [
    "HAS_LIGHTGBM",
    "HAS_SKLEARN",
    "HAS_TORCH",
    "HAS_XGBOOST",
    "MODALITY_ORDER_CELS",
    "LateOOFStacker",
    "PurePythonLogisticModel",
    "PurePythonMaskedFusionModel",
    "SklearnBaselineSuite",
    "WHOFraminghamContextScorer",
    "build_cels_key_padding_mask",
    "compute_pos_weight",
    "get_pytorch_model_classes",
    "load_checkpoint_bundle",
    "save_checkpoint_bundle",
    "set_global_seed",
    "train_pure_python_logistic_with_checkpoints",
    "train_pytorch_model_with_checkpoints",
]
