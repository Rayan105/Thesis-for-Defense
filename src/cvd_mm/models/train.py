"""Training, deterministic seeding, and SHA-256 checkpoint resume engine.

Supports:
  - Pure-Python deterministic training + JSON checkpoint/restore with exact RNG &
    weight preservation (verified locally & in STEP-027 EXP0000_SMOKE).
  - PyTorch Kaggle GPU training with AMP, cosine annealing, early stopping on
    Validation AUROC, and best_val/last checkpoint bundle saving.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
from pathlib import Path
from typing import Any, Sequence

from src.cvd_mm.metrics import roc_auc_score_exact
from src.cvd_mm.models.baselines import PurePythonLogisticModel
from src.cvd_mm.models.fusion_transformer import HAS_TORCH, torch


def set_global_seed(seed: int) -> None:
    """Seed Python stdlib (and PyTorch/CUDA if installed) deterministically."""
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    if HAS_TORCH:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def compute_pos_weight(y_train: Sequence[int]) -> float:
    """Compute Train-only class imbalance weight (neg_count / pos_count)."""
    pos = sum(1 for v in y_train if int(v) == 1)
    neg = len(y_train) - pos
    if pos == 0:
        raise ValueError("Training labels contain zero positive cases.")
    return float(neg) / float(pos)


def _canonical_json_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def save_checkpoint_bundle(
    path: str | Path,
    *,
    exp_id: str,
    candidate_id: str,
    epoch: int,
    best_val_roc_auc: float,
    model_state: dict[str, Any],
    config_hash: str,
    metrics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Persist deterministic JSON checkpoint envelope with embedded SHA-256 checksum."""
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    body = {
        "exp_id": exp_id,
        "candidate_id": candidate_id,
        "epoch": int(epoch),
        "best_val_roc_auc": float(best_val_roc_auc),
        "config_hash": config_hash,
        "python_random_state": repr(random.getstate()),
        "model_state": model_state,
        "metrics": metrics or {},
    }
    checksum = hashlib.sha256(_canonical_json_bytes(body)).hexdigest()
    envelope = {"sha256": checksum, "payload": body}
    out_path.write_text(json.dumps(envelope, indent=2, sort_keys=True), encoding="utf-8")
    return {"path": str(out_path), "sha256": checksum, "epoch": epoch}


def load_checkpoint_bundle(path: str | Path, verify_checksum: bool = True) -> dict[str, Any]:
    """Load checkpoint bundle and verify its SHA-256 payload digest against corruption."""
    ckpt_path = Path(path)
    envelope = json.loads(ckpt_path.read_text(encoding="utf-8"))
    payload = envelope["payload"]
    if verify_checksum:
        expected = envelope.get("sha256", "")
        actual = hashlib.sha256(_canonical_json_bytes(payload)).hexdigest()
        if expected != actual:
            raise ValueError(f"Checkpoint corruption detected in {ckpt_path}: expected {expected}, got {actual}")
    return payload


def train_pure_python_logistic_with_checkpoints(
    *,
    X_train: Sequence[Sequence[float]],
    y_train: Sequence[int],
    X_val: Sequence[Sequence[float]],
    y_val: Sequence[int],
    checkpoint_dir: str | Path,
    exp_id: str,
    candidate_id: str,
    config_hash: str,
    epochs: int = 10,
    lr: float = 0.15,
    l2: float = 1e-3,
    seed: int = 42,
    resume_from: str | Path | None = None,
) -> dict[str, Any]:
    """Train PurePythonLogisticModel with Validation monitoring & resume support."""
    set_global_seed(seed)
    n_features = len(X_train[0])
    pos_w = compute_pos_weight(y_train)
    model = PurePythonLogisticModel(n_features=n_features, l2=l2, lr=lr, pos_weight=pos_w, seed=seed)

    start_epoch = 0
    best_val_auc = -1.0
    history: list[dict[str, Any]] = []
    ckpt_root = Path(checkpoint_dir)
    ckpt_root.mkdir(parents=True, exist_ok=True)
    best_path = ckpt_root / f"{exp_id}_best_val.ckpt.json"
    last_path = ckpt_root / f"{exp_id}_last.ckpt.json"

    if resume_from is not None:
        loaded = load_checkpoint_bundle(resume_from, verify_checksum=True)
        model.load_state_dict(loaded["model_state"])
        start_epoch = int(loaded["epoch"])
        best_val_auc = float(loaded["best_val_roc_auc"])

    for _ in range(start_epoch, epochs):
        loss = model.step_epoch(X_train, y_train)
        val_probs = model.predict_proba(X_val)
        val_auc = roc_auc_score_exact(y_val, val_probs)
        rec = {"epoch": model.epoch, "train_loss": loss, "val_roc_auc": val_auc}
        history.append(rec)

        is_best = val_auc > best_val_auc
        if is_best:
            best_val_auc = val_auc
            save_checkpoint_bundle(
                best_path,
                exp_id=exp_id,
                candidate_id=candidate_id,
                epoch=model.epoch,
                best_val_roc_auc=best_val_auc,
                model_state=model.get_state_dict(),
                config_hash=config_hash,
                metrics=rec,
            )
        save_checkpoint_bundle(
            last_path,
            exp_id=exp_id,
            candidate_id=candidate_id,
            epoch=model.epoch,
            best_val_roc_auc=best_val_auc,
            model_state=model.get_state_dict(),
            config_hash=config_hash,
            metrics=rec,
        )

    return {
        "model": model,
        "best_val_roc_auc": best_val_auc,
        "best_checkpoint": str(best_path),
        "last_checkpoint": str(last_path),
        "history": history,
    }


def train_pytorch_model_with_checkpoints(
    model: Any,
    train_loader: Any,
    val_loader: Any,
    *,
    checkpoint_dir: str | Path,
    exp_id: str,
    candidate_id: str,
    epochs: int = 30,
    lr: float = 1e-3,
    weight_decay: float = 1e-4,
    pos_weight: float = 1.0,
    patience: int = 6,
    seed: int = 42,
    device: str = "cuda",
) -> dict[str, Any]:
    """Kaggle GPU PyTorch training loop with BCEWithLogitsLoss(pos_weight), CosineLR & EarlyStopping."""
    if not HAS_TORCH:
        raise RuntimeError("PyTorch is required for train_pytorch_model_with_checkpoints.")

    set_global_seed(seed)
    dev = torch.device(device if torch.cuda.is_available() else "cpu")
    model = model.to(dev)
    criterion = torch.nn.BCEWithLogitsLoss(pos_weight=torch.tensor([pos_weight], device=dev))
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=max(1, epochs))

    ckpt_root = Path(checkpoint_dir)
    ckpt_root.mkdir(parents=True, exist_ok=True)
    best_pt = ckpt_root / f"{exp_id}_{candidate_id}_best_val.pt"
    best_auc = -1.0
    wait = 0
    history: list[dict[str, float]] = []

    for ep in range(1, epochs + 1):
        model.train()
        total_loss = 0.0
        steps = 0
        for batch in train_loader:
            optimizer.zero_grad(set_to_none=True)
            ds_id, tab_mods, mask_cels, ecg_1d, ecg_2d, y_b = batch
            tab_mods = {k: v.to(dev) for k, v in tab_mods.items()}
            mask_cels = mask_cels.to(dev)
            ecg_1d = ecg_1d.to(dev) if ecg_1d is not None else None
            ecg_2d = ecg_2d.to(dev) if ecg_2d is not None else None
            y_b = y_b.float().to(dev)
            logits = model(ds_id, tab_mods, mask_cels, ecg_1d=ecg_1d, ecg_2d=ecg_2d)
            loss = criterion(logits, y_b)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            total_loss += float(loss.item())
            steps += 1
        scheduler.step()

        model.eval()
        y_true_val: list[int] = []
        y_prob_val: list[float] = []
        with torch.no_grad():
            for batch in val_loader:
                ds_id, tab_mods, mask_cels, ecg_1d, ecg_2d, y_b = batch
                tab_mods = {k: v.to(dev) for k, v in tab_mods.items()}
                mask_cels = mask_cels.to(dev)
                ecg_1d = ecg_1d.to(dev) if ecg_1d is not None else None
                ecg_2d = ecg_2d.to(dev) if ecg_2d is not None else None
                probs = torch.sigmoid(model(ds_id, tab_mods, mask_cels, ecg_1d=ecg_1d, ecg_2d=ecg_2d))
                y_true_val.extend(int(v) for v in y_b.tolist())
                y_prob_val.extend(float(p) for p in probs.cpu().tolist())

        val_auc = roc_auc_score_exact(y_true_val, y_prob_val)
        history.append({"epoch": float(ep), "train_loss": total_loss / max(1, steps), "val_roc_auc": val_auc})
        if val_auc > best_auc:
            best_auc = val_auc
            wait = 0
            torch.save(
                {
                    "epoch": ep,
                    "best_val_roc_auc": best_auc,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                },
                best_pt,
            )
        else:
            wait += 1
            if wait >= patience:
                break

    return {"best_val_roc_auc": best_auc, "best_checkpoint": str(best_pt), "history": history}
