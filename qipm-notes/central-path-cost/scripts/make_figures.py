#!/usr/bin/env python3
"""Reproduce the paper's vector figures and numerical data.

Formulas are exact; sampled values and adaptive quadrature are floating-point
illustrations, not proof certificates. All output paths are relative to this
script's enclosing paper directory. No repository data or network is needed.
"""
import csv
from fractions import Fraction
from math import isqrt
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parents[1]


def velocity(s):
    log_hypot = 0.5 * np.logaddexp(0.0, 2 * np.asarray(s))
    return np.sqrt(-np.expm1(-log_hypot))


def metric_profile(s):
    # 2 atanh(v) = log(sqrt(1+exp(2s))) + 2 log(1+v).
    # This form does not round q(exp(s)) to the boundary when s is large.
    log_hypot = 0.5 * np.logaddexp(0.0, 2 * np.asarray(s))
    v = np.sqrt(-np.expm1(-log_hypot))
    return log_hypot + 2*np.log1p(v) - np.sqrt(2)*np.arctanh(v/np.sqrt(2))


def exact_exponents(rank):
    total = Fraction(0)
    result = []
    for j in range(1, rank+1):
        result.append((4*rank*total).__floor__())
        ceil_sqrt = isqrt(j-1)+1
        total += Fraction(1, j*ceil_sqrt)
    return np.array(result, dtype=np.int64)


def check_profile():
    for s in np.linspace(-12, 25, 75):
        value, error = quad(lambda t: float(velocity(t)), -40, s,
                            epsabs=2e-12, epsrel=2e-12)
        np.testing.assert_allclose(metric_profile(s), value,
                                   rtol=2e-10, atol=2e-12)
    # The derivative check is independent of numerical integration.
    for s in np.linspace(-10, 30, 45):
        step = 1e-4
        derivative = (metric_profile(s+step)-metric_profile(s-step))/(2*step)
        np.testing.assert_allclose(derivative, velocity(s), rtol=2e-8)


def flattened_figure():
    s = np.linspace(-18, 8, 1200)
    y = metric_profile(s[:, None]-np.array([0.0, 6.0]))
    y = np.vstack(([0.0, 0.0], y))
    fig, ax = plt.subplots(figsize=(6.3, 2.65), layout="constrained")
    ax.plot(y[:, 0], y[:, 1], color="#245d8f", lw=2, label="Central arc")
    ax.plot([0, y[-1, 0]], [0, y[-1, 1]], color="#be5a32", lw=1.8,
            linestyle="--", label="Shortest route to the same endpoint")
    ax.scatter([0, y[-1, 0]], [0, y[-1, 1]], color="#303030", s=20, zorder=5)
    for label in [0, 4, 6]:
        point = metric_profile(label-np.array([0.0, 6.0]))
        ax.plot(*point, marker="o", color="#245d8f", ms=4)
        ax.annotate(f"s = {label}", point, xytext=(3, 18 if label == 0 else 9), textcoords="offset points",
                    fontsize=8)
    ax.set(xlabel=r"$y_1=\rho(x_1)$", ylabel=r"$y_2=\rho(x_2)$")
    ax.set_aspect("equal", adjustable="box")
    ax.legend(loc="upper left", fontsize=8, frameon=False)
    ax.grid(alpha=.2)
    fig.savefig(ROOT / "figures/flattened-path.pdf", metadata={"CreationDate": None})
    plt.close(fig)


def dyadic_figure():
    rows = []
    for rank in [8, 16, 32, 64, 128, 256, 512, 1024]:
        exponents = exact_exponents(rank)
        a = exponents * np.log(2.0)
        terminal = a[-1]
        displacement = metric_profile(terminal-a)-metric_profile(-a)
        distance = np.linalg.norm(displacement)
        # Integrate each distinct activation interval separately. Splitting
        # removes sensitivity to unresolved sharp changes in the speed.
        value = error = 0.0
        boundaries = np.unique(np.r_[0.0, a, terminal])
        for left, right in zip(boundaries[:-1], boundaries[1:]):
            val, err = quad(lambda s: float(np.linalg.norm(velocity(s-a))),
                            left, right, epsabs=1e-9, epsrel=2e-11, limit=150)
            value += val
            error += err
        full_length = np.sqrt(2*rank)*terminal
        assert distance <= value + 10*error <= full_length + 10*error
        rows.append((rank, int(exponents[-1]), terminal, distance, value,
                     full_length, error))
    columns = ["rank", "A_r", "T", "primal_endpoint_distance", "primal_central_length",
               "full_central_length", "primal_quadrature_error_estimate"]
    with (ROOT / "data/dyadic-lengths.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(columns)
        writer.writerows(rows)
    array = np.asarray(rows)
    fig, ax = plt.subplots(figsize=(6.3, 3.6), layout="constrained")
    for column, color, marker, label in [
            (3, "#be5a32", "o", "Primal endpoint distance"),
            (4, "#245d8f", "s", "Primal central length"),
            (5, "#447750", "^", "Full primal–dual central length")]:
        ax.loglog(array[:, 0], array[:, column], color=color, marker=marker,
                  ms=4, lw=1.5, label=label)
    ax.set(xlabel=r"Rank $r$", ylabel="Metric distance or length")
    ax.set_xticks(array[:, 0], [str(int(r)) for r in array[:, 0]])
    ax.legend(frameon=False, fontsize=9)
    ax.grid(which="major", alpha=.2)
    fig.savefig(ROOT / "figures/dyadic-lengths.pdf", metadata={"CreationDate": None})
    plt.close(fig)
    print(f"Generated both figures and {len(rows)} dyadic data rows.")
    print("Largest relative quadrature error estimate:",
          max(row[-1]/row[4] for row in rows))


def main():
    (ROOT / "figures").mkdir(exist_ok=True)
    (ROOT / "data").mkdir(exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 10,
                         "pdf.fonttype": 42, "ps.fonttype": 42})
    check_profile()
    flattened_figure()
    dyadic_figure()


if __name__ == "__main__":
    main()
