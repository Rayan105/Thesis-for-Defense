"""
Reproducible Sample-Size, Events-Per-Variable (EPV), and ROC-AUC Power Calculator (STEP-010).

Implements:
1. Riley et al. (BMJ 2020;368:m441 & Stat Med 2021) minimum sample size criteria for binary
   clinical prediction models (Shrinkage >= 0.90, Optimism <= 0.05, Prevalence CI +/-0.05).
2. Classical EPV benchmarks (EPV = 10, 15, 20).
3. Hanley & McNeil (Radiology 1982) test-set ROC-AUC standard error & 95% CI width.

Pure Python standard library implementation (no external numerical packages required).
"""

from __future__ import annotations

import math

SQRT2PI = math.sqrt(2.0 * math.pi)
SQRT2 = math.sqrt(2.0)


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / SQRT2))


def norm_ppf(p: float) -> float:
    lo, hi = -8.0, 8.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if norm_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def norm_pdf(x: float, mu: float = 0.0) -> float:
    z = x - mu
    return math.exp(-0.5 * z * z) / SQRT2PI


def cstat_to_r2_cs(auc: float, phi: float, n_steps: int = 8000) -> float:
    """Estimate Cox-Snell R^2 from anticipated C-statistic and event prevalence phi."""
    mu = SQRT2 * norm_ppf(auc)
    a, b = -8.0, 8.0 + mu
    dx = (b - a) / n_steps
    ll_model = 0.0
    for i in range(n_steps + 1):
        w = 0.5 if (i == 0 or i == n_steps) else 1.0
        x = a + i * dx
        f0 = norm_pdf(x, 0.0)
        f1 = norm_pdf(x, mu)
        mix = (1.0 - phi) * f0 + phi * f1
        if mix < 1e-300:
            continue
        p = min(max((phi * f1) / mix, 1e-12), 1.0 - 1e-12)
        ll_model += w * mix * (p * math.log(p) + (1.0 - p) * math.log(1.0 - p)) * dx
    ll_null = phi * math.log(phi) + (1.0 - phi) * math.log(1.0 - phi)
    lr_mean = max(0.0, 2.0 * (ll_model - ll_null))
    return 1.0 - math.exp(-lr_mean)


def riley_binary(P: int, phi: float, r2_cs: float, s_target: float = 0.90) -> dict[str, float | int]:
    """Compute Riley et al. (2020) three sample-size criteria and effective EPV."""
    max_r2_cs = 1.0 - math.exp(2.0 * (phi * math.log(phi) + (1.0 - phi) * math.log(1.0 - phi)))
    n1 = math.ceil(P / ((s_target - 1.0) * math.log(1.0 - r2_cs / s_target)))
    s2 = r2_cs / (r2_cs + 0.05 * max_r2_cs)
    n2 = math.ceil(P / ((s2 - 1.0) * math.log(1.0 - r2_cs / s2)))
    n3 = math.ceil((1.96 / 0.05) ** 2 * phi * (1.0 - phi))
    n_req = max(n1, n2, n3)
    e_req = math.ceil(n_req * phi)
    return {
        "n1_shrinkage": n1,
        "n2_optimism": n2,
        "n3_prevalence": n3,
        "n_dev": n_req,
        "e_dev": e_req,
        "epv_eff": e_req / P,
        "max_r2_cs": max_r2_cs,
    }


def hanley_mcneil_auc_ci(auc: float, n_test: int, phi: float) -> dict[str, float | int]:
    """Compute Hanley & McNeil (1982) ROC-AUC standard error and symmetric 95% half-width."""
    n1 = max(1, round(n_test * phi))
    n0 = max(1, n_test - n1)
    q1 = auc / (2.0 - auc)
    q2 = (2.0 * auc * auc) / (1.0 + auc)
    se = math.sqrt((auc * (1.0 - auc) + (n1 - 1) * (q1 - auc * auc) + (n0 - 1) * (q2 - auc * auc)) / (n1 * n0))
    hw = 1.96 * se
    return {"n_test": n_test, "e_test": n1, "none_test": n0, "se": se, "half_width": hw}


def main() -> None:
    print("=== Riley et al. (2020) Development Sample Size Grid ===")
    print("Prev | AUC  | R2_CS  | P  | n1   | n2   | n3  | N_dev | E_dev | EPV")
    for phi in [0.10, 0.15, 0.25, 0.35]:
        for auc in [0.75, 0.80, 0.85]:
            r2 = cstat_to_r2_cs(auc, phi)
            for P in [15, 25, 35, 45]:
                res = riley_binary(P, phi, r2)
                print(
                    f"{phi:.2f} | {auc:.2f} | {r2:.4f} | {P:2d} | "
                    f"{res['n1_shrinkage']:4d} | {res['n2_optimism']:4d} | {res['n3_prevalence']:3d} | "
                    f"{res['n_dev']:5d} | {res['e_dev']:5d} | {res['epv_eff']:4.2f}"
                )

    print("\n=== Hanley & McNeil (1982) Test-Set ROC-AUC 95% CI Precision (AUC=0.80) ===")
    for phi in [0.15, 0.25, 0.35]:
        for n_test in [150, 250, 400, 600, 1000]:
            hm = hanley_mcneil_auc_ci(0.80, n_test, phi)
            lo = max(0.0, 0.80 - hm["half_width"])
            hi = min(1.0, 0.80 + hm["half_width"])
            print(
                f"phi={phi:.2f} | N_test={hm['n_test']:4d} (E={hm['e_test']:3d}) | "
                f"SE={hm['se']:.4f} | 95% CI=[{lo:.3f}, {hi:.3f}] (+/-{hm['half_width']:.3f})"
            )


if __name__ == "__main__":
    main()
