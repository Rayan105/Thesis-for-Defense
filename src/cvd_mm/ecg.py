"""
Record-Local 12-Lead ECG Signal Processing & Paper-Scan Grid Cleaning (STEP-019).

Pure-Python DSP & RGB image-cleaning helpers verifying zero phase/ST-T distortion:
1. Zero-phase biquad 50 Hz / 60 Hz powerline notch filter (when fs > 2.2 * notch_hz).
2. Zero-phase 2nd-order <=0.5 Hz Butterworth high-pass baseline wander removal.
3. Red millimeter grid suppression on CARDIO-ML-ED cropped PNG paper scans.
"""

from __future__ import annotations

import math
from typing import Sequence


def _biquad_direct_form_ii(
    x: Sequence[float],
    b0: float,
    b1: float,
    b2: float,
    a1: float,
    a2: float,
) -> list[float]:
    """Apply normalized (a0 = 1) second-order IIR difference equation causally."""
    y = [0.0] * len(x)
    x1 = x2 = y1 = y2 = 0.0
    for i, xi in enumerate(x):
        yi = b0 * xi + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
        y[i] = yi
        x2, x1 = x1, xi
        y2, y1 = y1, yi
    return y


def _zero_phase_biquad(
    signal: Sequence[float],
    b0: float,
    b1: float,
    b2: float,
    a1: float,
    a2: float,
    padlen: int = 32,
) -> list[float]:
    """Forward-backward reflection-padded zero-phase filter preserving waveform phase & QRS peaks."""
    n = len(signal)
    if n == 0:
        return []
    pad = min(padlen, n - 1) if n > 1 else 0
    if pad > 0:
        left = [2.0 * signal[0] - signal[i] for i in range(pad, 0, -1)]
        right = [2.0 * signal[-1] - signal[n - 2 - i] for i in range(pad)]
        padded = left + list(signal) + right
    else:
        padded = list(signal)

    fwd = _biquad_direct_form_ii(padded, b0, b1, b2, a1, a2)
    rev = _biquad_direct_form_ii(list(reversed(fwd)), b0, b1, b2, a1, a2)
    restored = list(reversed(rev))
    return restored[pad : pad + n] if pad > 0 else restored


def apply_powerline_notch_zero_phase(
    signal: Sequence[float],
    fs_hz: float = 500.0,
    notch_hz: float = 50.0,
    q: float = 30.0,
) -> list[float]:
    """
    Apply zero-phase 2nd-order RBJ biquad notch filter at notch_hz (e.g. 50 Hz).
    Safely bypasses when fs_hz <= 2.2 * notch_hz (e.g. 100 Hz recordings where Nyquist = 50 Hz).
    """
    if fs_hz <= 2.2 * notch_hz or len(signal) < 8:
        return list(signal)

    w0 = 2.0 * math.pi * notch_hz / fs_hz
    alpha = math.sin(w0) / (2.0 * q)
    a0 = 1.0 + alpha
    b0 = 1.0 / a0
    b1 = (-2.0 * math.cos(w0)) / a0
    b2 = 1.0 / a0
    a1 = (-2.0 * math.cos(w0)) / a0
    a2 = (1.0 - alpha) / a0
    return _zero_phase_biquad(signal, b0, b1, b2, a1, a2)


def apply_baseline_highpass_zero_phase(
    signal: Sequence[float],
    fs_hz: float = 500.0,
    cutoff_hz: float = 0.5,
) -> list[float]:
    """
    Apply zero-phase 2nd-order Butterworth high-pass filter (strictly <= 0.5 Hz cutoff)
    removing slow respiratory baseline wander while preserving ST-T complexes.
    """
    if cutoff_hz > 0.5:
        raise ValueError(f"High-pass cutoff {cutoff_hz} Hz exceeds ST-T safety limit of 0.5 Hz.")
    if len(signal) < 8:
        return list(signal)

    w0 = 2.0 * math.pi * cutoff_hz / fs_hz
    alpha = math.sin(w0) / math.sqrt(2.0)  # Q = 1/sqrt(2) Butterworth
    cos_w0 = math.cos(w0)
    a0 = 1.0 + alpha
    b0 = ((1.0 + cos_w0) / 2.0) / a0
    b1 = (-(1.0 + cos_w0)) / a0
    b2 = ((1.0 + cos_w0) / 2.0) / a0
    a1 = (-2.0 * cos_w0) / a0
    a2 = (1.0 - alpha) / a0
    return _zero_phase_biquad(signal, b0, b1, b2, a1, a2)


def suppress_red_ecg_grid_rgb(r: int, g: int, b: int) -> int:
    """
    Deterministic record-local pixel transform mapping RGB scanned ECG paper pixels
    to clean 8-bit grayscale [0=black ink, 255=white background], suppressing red/pink grids.
    Pink/red grid pixels exhibit high red excess (r - min(g, b)) and relatively high green/blue vs dark ink.
    """
    # Red/pink grid has high R and high luminance compared to dark neutral ECG ink (where R,G,B are all low)
    chroma_max = max(r, g, b)
    red_excess = max(0, r - max(g, b))
    # Suppress red hue saturation & recover white paper luminance cleanly while keeping neutral dark ink
    gray_paper_boost = min(255, int(round(0.299 * r + 0.587 * g + 0.114 * b + 0.75 * red_excess)))
    # Crisp soft stretch so faint background grid turns white (>=240) while black trace (<80) stays sharp
    if gray_paper_boost >= 155 and chroma_max >= 165:
        return 255
    return gray_paper_boost


def pearson_correlation(a: Sequence[float], b: Sequence[float]) -> float:
    """Compute Pearson correlation coefficient for morphology fidelity checks (G08 prep)."""
    n = len(a)
    if n != len(b) or n < 2:
        raise ValueError("Signals must have matching length >= 2.")
    ma = sum(a) / n
    mb = sum(b) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    da = math.sqrt(sum((x - ma) ** 2 for x in a))
    db = math.sqrt(sum((y - mb) ** 2 for y in b))
    return (num / (da * db)) if (da > 0 and db > 0) else 0.0
