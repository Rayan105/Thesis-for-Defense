"""Multimodal deep fusion and ECG encoders (MC0006-MC0017, UD14/DEC0010).

Implements the exact compact CVD-MM-Transformer specification (<250K params,
d_model=64, 2 Pre-LN Transformer layers, 4 heads, ModalityMask_CELS token masking
with [CLS] anchor so 0..4 missing modalities never yield NaN), alongside compact
1D/2D ECG encoders and a pure-Python stdlib masked-attention mirror so unit tests
verify missing-modality safety deterministically even without PyTorch installed.
"""

from __future__ import annotations

import math
import random
from typing import Any, Sequence

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    HAS_TORCH = True
except ImportError:
    torch = None  # type: ignore[assignment]
    nn = None  # type: ignore[assignment]
    F = None  # type: ignore[assignment]
    HAS_TORCH = False

MODALITY_ORDER_CELS: tuple[str, ...] = ("clinical", "ecg", "laboratory", "lifestyle")


def build_cels_key_padding_mask(modality_mask_cels: Sequence[int | float | bool]) -> list[bool]:
    """Convert 4-bit CELS availability mask [C, E, L, S] (1=present, 0=missing)
    into a 5-token Transformer padding mask [CLS, C, E, L, S] where True=IGNORED.

    Keeping [CLS] unconditionally unmasked (False) guarantees softmax stability
    even if all 4 modalities are masked in extreme stress cases.
    """
    if len(modality_mask_cels) != 4:
        raise ValueError(f"Expected 4-element ModalityMask_CELS, got {len(modality_mask_cels)}")
    return [False] + [not bool(float(v) > 0.0) for v in modality_mask_cels]


def _sigmoid(z: float) -> float:
    if z >= 0.0:
        return 1.0 / (1.0 + math.exp(-min(z, 60.0)))
    ez = math.exp(max(z, -60.0))
    return ez / (1.0 + ez)


def _dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


class PurePythonMaskedFusionModel:
    """Stdlib deterministic masked cross-modality attention mirror for CVD-MM-Transformer.

    Mirrors the exact [CLS, Clinical, ECG, Laboratory, Lifestyle] token sequence,
    per-cohort linear projections into d_model, modality-type embeddings,
    key-padding mask over ~ModalityMask_CELS, scaled dot-product attention, and
    binary risk readout. Used for fast CPU structural/leakage/masking verification.
    """

    def __init__(
        self,
        cohort_modality_dims: dict[str, dict[str, int]],
        d_model: int = 16,
        ecg_dim: int = 16,
        seed: int = 42,
    ) -> None:
        self.cohort_modality_dims = cohort_modality_dims
        self.d_model = d_model
        self.ecg_dim = ecg_dim
        self.seed = seed

        rng = random.Random(seed)
        scale = 1.0 / math.sqrt(max(1, d_model))

        def _mat(rows: int, cols: int) -> list[list[float]]:
            return [[rng.gauss(0.0, scale) for _ in range(cols)] for _ in range(rows)]

        def _vec(n: int) -> list[float]:
            return [rng.gauss(0.0, scale) for _ in range(n)]

        self.cls_token = _vec(d_model)
        self.type_emb = {m: _vec(d_model) for m in ("cls",) + MODALITY_ORDER_CELS}

        self.proj: dict[tuple[str, str], list[list[float]]] = {}
        for ds_id, mod_map in sorted(cohort_modality_dims.items()):
            for mod, in_dim in sorted(mod_map.items()):
                if in_dim > 0:
                    self.proj[(ds_id, mod)] = _mat(d_model, in_dim)
        self.ecg_proj = _mat(d_model, ecg_dim)

        self.w_q = _mat(d_model, d_model)
        self.w_k = _mat(d_model, d_model)
        self.w_v = _mat(d_model, d_model)
        self.head_w = _vec(d_model)
        self.head_b = 0.0

    @staticmethod
    def _matvec(mat: list[list[float]], vec: Sequence[float]) -> list[float]:
        return [sum(w * x for w, x in zip(row, vec)) for row in mat]

    @staticmethod
    def _layernorm(vec: Sequence[float], eps: float = 1e-5) -> list[float]:
        n = len(vec)
        mean = sum(vec) / n
        var = sum((x - mean) ** 2 for x in vec) / n
        inv = 1.0 / math.sqrt(var + eps)
        return [(x - mean) * inv for x in vec]

    def _encode_token(
        self,
        ds_id: str,
        mod: str,
        values: Sequence[float] | None,
        is_present: bool,
    ) -> list[float]:
        if not is_present or values is None:
            return list(self.type_emb[mod])
        if mod == "ecg":
            padded = list(values[: self.ecg_dim]) + [0.0] * max(0, self.ecg_dim - len(values))
            base = self._matvec(self.ecg_proj, padded)
        else:
            key = (ds_id, mod)
            if key not in self.proj:
                return list(self.type_emb[mod])
            w = self.proj[key]
            clean = [0.0 if (math.isnan(v) or math.isinf(v)) else float(v) for v in values]
            base = self._matvec(w, clean)
        return [math.tanh(b + te) for b, te in zip(base, self.type_emb[mod])]

    def forward(
        self,
        ds_id: str,
        modality_vectors: dict[str, Sequence[float]],
        modality_mask_cels: Sequence[int | float | bool],
    ) -> dict[str, Any]:
        """Run masked self-attention from [CLS] over [CLS, C, E, L, S].

        Returns logit, prob, cls_repr, attention_weights (5 weights summing to 1.0),
        and key_padding_mask so tests can inspect zero-weight masking directly.
        """
        pad_mask = build_cels_key_padding_mask(modality_mask_cels)
        tokens: list[list[float]] = [
            [c + te for c, te in zip(self.cls_token, self.type_emb["cls"])]
        ]
        for idx, mod in enumerate(MODALITY_ORDER_CELS):
            present = not pad_mask[idx + 1]
            tokens.append(self._encode_token(ds_id, mod, modality_vectors.get(mod), present))

        q_cls = self._matvec(self.w_q, self._layernorm(tokens[0]))
        keys = [self._matvec(self.w_k, self._layernorm(tok)) for tok in tokens]
        vals = [self._matvec(self.w_v, self._layernorm(tok)) for tok in tokens]

        inv_sqrt_d = 1.0 / math.sqrt(self.d_model)
        scores = [
            float("-inf") if pad_mask[j] else _dot(q_cls, keys[j]) * inv_sqrt_d
            for j in range(len(tokens))
        ]
        max_s = max(s for s in scores if not math.isinf(s))
        exps = [0.0 if pad_mask[j] else math.exp(scores[j] - max_s) for j in range(len(tokens))]
        denom = sum(exps)
        attn_weights = [e / denom for e in exps]

        ctx = [0.0] * self.d_model
        for w, v in zip(attn_weights, vals):
            if w > 0.0:
                for k in range(self.d_model):
                    ctx[k] += w * v[k]

        cls_out = self._layernorm([a + b for a, b in zip(tokens[0], ctx)])
        logit = _dot(self.head_w, cls_out) + self.head_b
        return {
            "logit": logit,
            "prob": _sigmoid(logit),
            "cls_repr": cls_out,
            "attention_weights": attn_weights,
            "key_padding_mask": pad_mask,
        }


def get_pytorch_model_classes() -> dict[str, Any]:
    """Return PyTorch nn.Module classes for Kaggle GPU training (MC0006-MC0017).

    Raises RuntimeError with actionable guidance if PyTorch is absent locally.
    """
    if not HAS_TORCH:
        raise RuntimeError(
            "PyTorch is not installed in this local environment. "
            "Use PurePythonMaskedFusionModel/PurePythonLogisticModel locally or run "
            "on Kaggle GPU with environment/model/requirements.txt."
        )

    class _SEBlock1D(nn.Module):
        def __init__(self, channels: int, reduction: int = 4) -> None:
            super().__init__()
            hidden = max(4, channels // reduction)
            self.fc = nn.Sequential(
                nn.Linear(channels, hidden),
                nn.SiLU(),
                nn.Linear(hidden, channels),
                nn.Sigmoid(),
            )

        def forward(self, x: Any) -> Any:
            scale = x.mean(dim=-1)
            scale = self.fc(scale).unsqueeze(-1)
            return x * scale

    class _ResBlock1D(nn.Module):
        def __init__(self, in_ch: int, out_ch: int, stride: int = 1, dropout: float = 0.1) -> None:
            super().__init__()
            self.conv1 = nn.Conv1d(in_ch, out_ch, kernel_size=5, stride=stride, padding=2, bias=False)
            self.bn1 = nn.BatchNorm1d(out_ch)
            self.conv2 = nn.Conv1d(out_ch, out_ch, kernel_size=5, stride=1, padding=2, bias=False)
            self.bn2 = nn.BatchNorm1d(out_ch)
            self.se = _SEBlock1D(out_ch)
            self.drop = nn.Dropout(dropout)
            self.shortcut = (
                nn.Sequential(
                    nn.Conv1d(in_ch, out_ch, kernel_size=1, stride=stride, bias=False),
                    nn.BatchNorm1d(out_ch),
                )
                if (stride != 1 or in_ch != out_ch)
                else nn.Identity()
            )

        def forward(self, x: Any) -> Any:
            out = F.gelu(self.bn1(self.conv1(x)))
            out = self.drop(out)
            out = self.bn2(self.conv2(out))
            out = self.se(out)
            return F.gelu(out + self.shortcut(x))

    class CompactResNet1D(nn.Module):
        """MC0006/MC0009 12-lead ECG SE-ResNet-1D encoder projecting to embed_dim."""

        def __init__(self, in_leads: int = 12, embed_dim: int = 64, dropout: float = 0.1) -> None:
            super().__init__()
            self.stem = nn.Sequential(
                nn.Conv1d(in_leads, 32, kernel_size=7, stride=2, padding=3, bias=False),
                nn.BatchNorm1d(32),
                nn.GELU(),
            )
            self.blocks = nn.Sequential(
                _ResBlock1D(32, 32, stride=2, dropout=dropout),
                _ResBlock1D(32, 64, stride=2, dropout=dropout),
                _ResBlock1D(64, embed_dim, stride=2, dropout=dropout),
            )
            self.head = nn.Linear(embed_dim, 1)

        def encode(self, x: Any) -> Any:
            h = self.blocks(self.stem(x))
            return h.mean(dim=-1)

        def forward(self, x: Any) -> Any:
            return self.head(self.encode(x)).squeeze(-1)

    class Conv1DBiLSTMEncoder(nn.Module):
        """MC0007 Conv1D + Bidirectional LSTM encoder for 12-lead ECG morphology/rhythm."""

        def __init__(self, in_leads: int = 12, embed_dim: int = 64, dropout: float = 0.1) -> None:
            super().__init__()
            self.conv = nn.Sequential(
                nn.Conv1d(in_leads, 32, kernel_size=7, stride=2, padding=3, bias=False),
                nn.BatchNorm1d(32),
                nn.GELU(),
                nn.MaxPool1d(2),
                nn.Conv1d(32, 48, kernel_size=5, stride=2, padding=2, bias=False),
                nn.BatchNorm1d(48),
                nn.GELU(),
                nn.Dropout(dropout),
            )
            self.lstm = nn.LSTM(
                input_size=48,
                hidden_size=embed_dim // 2,
                num_layers=1,
                batch_first=True,
                bidirectional=True,
            )
            self.head = nn.Linear(embed_dim, 1)

        def encode(self, x: Any) -> Any:
            seq = self.conv(x).transpose(1, 2)
            out, _ = self.lstm(seq)
            return out.mean(dim=1)

        def forward(self, x: Any) -> Any:
            return self.head(self.encode(x)).squeeze(-1)

    class CompactCNN2DPNG(nn.Module):
        """MC0008 Compact 2D-CNN for DS0005 CARDIO-ML-ED red-grid-removed ECG PNG images."""

        def __init__(self, in_channels: int = 1, embed_dim: int = 64, dropout: float = 0.15) -> None:
            super().__init__()
            self.features = nn.Sequential(
                nn.Conv2d(in_channels, 16, kernel_size=3, stride=2, padding=1, bias=False),
                nn.BatchNorm2d(16),
                nn.GELU(),
                nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1, bias=False),
                nn.BatchNorm2d(32),
                nn.GELU(),
                nn.Conv2d(32, embed_dim, kernel_size=3, stride=2, padding=1, bias=False),
                nn.BatchNorm2d(embed_dim),
                nn.GELU(),
                nn.AdaptiveAvgPool2d(1),
                nn.Flatten(),
                nn.Dropout(dropout),
            )
            self.head = nn.Linear(embed_dim, 1)

        def encode(self, img: Any) -> Any:
            return self.features(img)

        def forward(self, img: Any) -> Any:
            return self.head(self.encode(img)).squeeze(-1)

    class ECGPatchTransformer(nn.Module):
        """MC0010 Patch-tokenized temporal Transformer for 12-lead ECG signals."""

        def __init__(
            self,
            in_leads: int = 12,
            patch_len: int = 50,
            d_model: int = 64,
            n_heads: int = 4,
            n_layers: int = 2,
            dropout: float = 0.1,
        ) -> None:
            super().__init__()
            self.patch_proj = nn.Conv1d(in_leads, d_model, kernel_size=patch_len, stride=patch_len)
            self.cls_token = nn.Parameter(torch.zeros(1, 1, d_model))
            enc_layer = nn.TransformerEncoderLayer(
                d_model=d_model,
                nhead=n_heads,
                dim_feedforward=d_model * 2,
                dropout=dropout,
                activation="gelu",
                batch_first=True,
                norm_first=True,
            )
            self.encoder = nn.TransformerEncoder(enc_layer, num_layers=n_layers)
            self.norm = nn.LayerNorm(d_model)
            self.head = nn.Linear(d_model, 1)

        def encode(self, x: Any) -> Any:
            patches = self.patch_proj(x).transpose(1, 2)
            b = patches.size(0)
            cls = self.cls_token.expand(b, -1, -1)
            seq = torch.cat([cls, patches], dim=1)
            out = self.norm(self.encoder(seq))
            return out[:, 0]

        def forward(self, x: Any) -> Any:
            return self.head(self.encode(x)).squeeze(-1)

    class TabularModalityMLP(nn.Module):
        """Compact Pre-LN Residual MLP projecting variable-width tabular slice -> d_model."""

        def __init__(self, in_dim: int, d_model: int = 64, dropout: float = 0.15) -> None:
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(in_dim, d_model),
                nn.LayerNorm(d_model),
                nn.GELU(),
                nn.Dropout(dropout),
                nn.Linear(d_model, d_model),
            )

        def forward(self, x: Any) -> Any:
            return self.net(x)

    class GatedAttentionFusionNet(nn.Module):
        """MC0014 Compact Gated Attention multimodal fusion baseline (C, E, L, S)."""

        def __init__(self, mod_dims: dict[str, int], d_model: int = 64, dropout: float = 0.15) -> None:
            super().__init__()
            self.proj = nn.ModuleDict(
                {m: TabularModalityMLP(dim, d_model, dropout) for m, dim in mod_dims.items() if dim > 0}
            )
            self.gate = nn.Sequential(nn.Linear(d_model, d_model // 2), nn.Tanh(), nn.Linear(d_model // 2, 1))
            self.head = nn.Sequential(nn.LayerNorm(d_model), nn.Dropout(dropout), nn.Linear(d_model, 1))

        def forward(self, modality_inputs: dict[str, Any], modality_mask_cels: Any) -> Any:
            embeds = []
            for mod in MODALITY_ORDER_CELS:
                if mod in modality_inputs and mod in self.proj:
                    embeds.append(self.proj[mod](modality_inputs[mod]))
                else:
                    b = modality_mask_cels.size(0)
                    device = modality_mask_cels.device
                    embeds.append(torch.zeros(b, next(iter(self.proj.values())).net[0].out_features, device=device))
            stacked = torch.stack(embeds, dim=1)  # (B, 4, d_model)
            scores = self.gate(stacked).squeeze(-1)
            scores = scores.masked_fill(~modality_mask_cels.bool(), -1e9)
            weights = F.softmax(scores, dim=-1).unsqueeze(-1)
            fused = (stacked * weights).sum(dim=1)
            return self.head(fused).squeeze(-1)

    class CVDMMTransformer(nn.Module):
        """MC0015 Proposed CVD-MM-Transformer (UD14 / DEC0010).

        Per-cohort tabular modality adapters + ECG encoders project into shared d_model=64,
        concatenated behind a learnable [CLS] anchor token. Passes through 2 Pre-LN
        TransformerEncoder layers (4 heads, dim_feedforward=128) with src_key_padding_mask
        derived from ~ModalityMask_CELS so missing modalities are strictly zeroed out without
        producing NaNs, plus training-time ModalityDropout (p=0.15) preserving >=1 modality.
        """

        def __init__(
            self,
            cohort_modality_dims: dict[str, dict[str, int]],
            d_model: int = 64,
            n_heads: int = 4,
            n_layers: int = 2,
            dim_feedforward: int = 128,
            dropout: float = 0.1,
            modality_dropout_p: float = 0.15,
        ) -> None:
            super().__init__()
            self.d_model = d_model
            self.modality_dropout_p = modality_dropout_p

            adapters: dict[str, nn.Module] = {}
            for ds_id, mods in sorted(cohort_modality_dims.items()):
                for mod, in_dim in sorted(mods.items()):
                    if mod != "ecg" and in_dim > 0:
                        adapters[f"{ds_id}__{mod}"] = TabularModalityMLP(in_dim, d_model, dropout)
            self.tab_adapters = nn.ModuleDict(adapters)
            self.ecg_1d_encoder = CompactResNet1D(in_leads=12, embed_dim=d_model, dropout=dropout)
            self.ecg_2d_encoder = CompactCNN2DPNG(in_channels=1, embed_dim=d_model, dropout=dropout)

            self.cls_token = nn.Parameter(torch.zeros(1, 1, d_model))
            self.mod_type_emb = nn.Parameter(torch.randn(1, 4, d_model) * 0.02)
            enc_layer = nn.TransformerEncoderLayer(
                d_model=d_model,
                nhead=n_heads,
                dim_feedforward=dim_feedforward,
                dropout=dropout,
                activation="gelu",
                batch_first=True,
                norm_first=True,
            )
            self.encoder = nn.TransformerEncoder(enc_layer, num_layers=n_layers)
            self.norm = nn.LayerNorm(d_model)
            self.classifier = nn.Sequential(
                nn.Linear(d_model, d_model // 2),
                nn.GELU(),
                nn.Dropout(dropout),
                nn.Linear(d_model // 2, 1),
            )

        def _apply_modality_dropout(self, mask_cels: Any) -> Any:
            if not self.training or self.modality_dropout_p <= 0.0:
                return mask_cels
            drop = torch.rand_like(mask_cels.float()) < self.modality_dropout_p
            new_mask = mask_cels.bool() & (~drop)
            # Never drop all present modalities for a sample during training
            all_dropped = new_mask.sum(dim=1) == 0
            if all_dropped.any():
                new_mask[all_dropped] = mask_cels.bool()[all_dropped]
            return new_mask

        def forward(
            self,
            ds_id: str,
            tabular_modalities: dict[str, Any],
            modality_mask_cels: Any,
            ecg_1d: Any | None = None,
            ecg_2d: Any | None = None,
        ) -> Any:
            b = modality_mask_cels.size(0)
            device = modality_mask_cels.device
            eff_mask = self._apply_modality_dropout(modality_mask_cels.bool())

            toks = []
            for idx, mod in enumerate(MODALITY_ORDER_CELS):
                if mod == "ecg":
                    if ecg_1d is not None:
                        emb = self.ecg_1d_encoder.encode(ecg_1d)
                    elif ecg_2d is not None:
                        emb = self.ecg_2d_encoder.encode(ecg_2d)
                    else:
                        emb = torch.zeros(b, self.d_model, device=device)
                else:
                    key = f"{ds_id}__{mod}"
                    if key in self.tab_adapters and mod in tabular_modalities:
                        emb = self.tab_adapters[key](tabular_modalities[mod])
                    else:
                        emb = torch.zeros(b, self.d_model, device=device)
                toks.append(emb + self.mod_type_emb[:, idx, :])

            mod_seq = torch.stack(toks, dim=1)  # (B, 4, d_model)
            cls = self.cls_token.expand(b, -1, -1)
            full_seq = torch.cat([cls, mod_seq], dim=1)  # (B, 5, d_model)

            cls_valid = torch.zeros(b, 1, dtype=torch.bool, device=device)
            src_key_padding_mask = torch.cat([cls_valid, ~eff_mask], dim=1)  # True = IGNORED
            encoded = self.norm(self.encoder(full_seq, src_key_padding_mask=src_key_padding_mask))
            return self.classifier(encoded[:, 0]).squeeze(-1)

    return {
        "CompactResNet1D": CompactResNet1D,
        "Conv1DBiLSTMEncoder": Conv1DBiLSTMEncoder,
        "CompactCNN2DPNG": CompactCNN2DPNG,
        "ECGPatchTransformer": ECGPatchTransformer,
        "TabularModalityMLP": TabularModalityMLP,
        "GatedAttentionFusionNet": GatedAttentionFusionNet,
        "CVDMMTransformer": CVDMMTransformer,
    }
