#!/usr/bin/env python3
"""Reproduce Stage 2 numerical diagnostics; meshes are not feasibility proofs.

Run in the qipm environment. Thresholds use the unique hyperbolic stationary
point, avoiding minimization on a mesh. The manuscript proves contractivity.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq
from scipy.special import eval_chebyt


def threshold(r: int, rho: float) -> tuple[float, float]:
    n = 2 * r
    a = np.log((np.sqrt(rho) + 1) / (np.sqrt(rho) - 1))
    h = (rho - 1) / 2
    # Solve in the order-one offset s=n(t-a), rather than subtracting roots.
    def stationary(s: float) -> float:
        t = a + s / n
        difference = 2 * np.sinh((t + a) / 2) * np.sinh(s / (2 * n))
        return n * difference * np.tanh(n * t) - np.sinh(t)
    upper = 2.0
    while stationary(upper) < 0:
        upper *= 2
    s = brentq(stationary, 0, upper, xtol=1e-14)
    t = a + s / n
    difference = 2 * np.sinh((t + a) / 2) * np.sinh(s / (2 * n))
    return h * difference / np.cosh(n * t), s


def gate(x: np.ndarray, delta: float, r: int, rho: float, k: int):
    contacts = (rho + 1) / 2 + (rho - 1) / 2 * np.cos(np.pi * np.arange(r + 1) / r)
    theta = np.arcsin(x)
    log_leakage = np.zeros_like(x)
    for y in contacts:
        for sign in (-1, 1):
            u = theta - sign * np.arcsin(delta * y)
            kernel = np.sinc(k * u / np.pi) / np.sinc(u / np.pi)
            # Roundoff can overshoot the analytically proved |kernel|<=1.
            power = np.minimum(np.abs(kernel), 1.0) ** (2 * r + 4)
            with np.errstate(divide="ignore", invalid="ignore"):
                log_leakage += (r + 1) * np.log1p(-power)
    return -np.expm1(log_leakage), np.exp(log_leakage), contacts


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "figures" / "stage2-diagnostics")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    rho, leading = 2.0, 64.0
    radius = (np.sqrt(rho) + 1) / (np.sqrt(rho) - 1)
    rows = []
    for r in range(1, 33):
        value, offset = threshold(r, rho)
        asymptotic = np.sqrt(rho) / (np.e * r) * radius ** (-2 * r)
        rows.append(dict(r=r, G_r=value, asymptotic=asymptotic, ratio=value / asymptotic, stationary_offset=offset))
    write_csv(args.output / "thresholds.csv", rows)

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.7), constrained_layout=True)
    axes[0].plot([row["r"] for row in rows], [row["ratio"] for row in rows], marker=".")
    axes[0].axhline(1, color="black", lw=0.8, ls="--")
    axes[0].set(xlabel="Threshold index r", ylabel="Exact G_r / leading asymptotic", title="Threshold asymptotic, rho = 2")

    kernel_rows = []
    for r in (2, 3, 4):
        # k*delta is about .064 for every example. Large k is never expanded
        # into polynomial coefficients; the gate is evaluated near its pins.
        delta = 10.0 ** (-6 * r)
        k = int(np.ceil(leading * delta ** (-1 + 1 / (2 * r))))
        k += 1 - k % 2
        value, _ = threshold(r, rho)
        y = np.linspace(1, rho, 2001)
        W, leakage, contacts = gate(delta * y, delta, r, rho, k)
        e = value * eval_chebyt(2 * r, (y - (rho + 1) / 2) / ((rho - 1) / 2))
        # N has the manuscript's high-tail order with K=G_r and c=1/2.
        N = int(np.ceil(np.log(2 / (value * delta)) / -np.log(0.75)))
        coefficients = []
        coefficient, cumulative = 0.5, 0.0
        for j in range(1, N + 1):
            if j > 1:
                coefficient *= (j - 1.5) / j
            cumulative += coefficient
            coefficients.append(cumulative)
        x = delta * y
        u = x * x
        series = u * (1 - u) * np.polynomial.polynomial.polyval(1 - u, coefficients)
        # Evaluate the signed-error identity, avoiding subtraction of q~1.
        normalized_error = W * (e / value) + leakage * (1 - x - series) / (value * delta)
        slack = value - e
        noncontacts = slack > value * 1e-10
        max_ratio = np.max(leakage[noncontacts] / (delta * slack[noncontacts]))
        _, pin_leakage, _ = gate(delta * contacts, delta, r, rho, k)
        kernel_rows.append(dict(r=r, delta=delta, k=k, k_delta=k * delta, N=N,
                                max_sampled_abs_error_over_G_delta=float(np.max(np.abs(normalized_error))),
                                max_sampled_leakage_over_delta_slack=float(max_ratio),
                                max_pin_leakage=float(np.max(pin_leakage))))
        axes[1].plot(y, normalized_error, label=f"r={r}")
    write_csv(args.output / "pinned_kernels.csv", kernel_rows)
    axes[1].axhline(1, color="black", lw=0.8, ls="--")
    axes[1].axhline(-1, color="black", lw=0.8, ls="--")
    axes[1].set(xlabel="Scaled eigenvalue y", ylabel="Signed low error / (G_r delta)", title="Pinned threshold errors (diagnostic)")
    axes[1].legend()
    fig.savefig(args.output / "joint_diagnostics.pdf")
    fig.savefig(args.output / "joint_diagnostics.png", dpi=160)
    for row in kernel_rows:
        print(row)
    print(f"Saved CSV data and figures to {args.output}")


if __name__ == "__main__":
    main()
