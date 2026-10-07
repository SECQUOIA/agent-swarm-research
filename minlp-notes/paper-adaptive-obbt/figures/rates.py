#!/usr/bin/env python3
"""Plot proved analytic OBBT factors; no solver or experimental data are used.

Run from any directory: python3 /path/to/paper-adaptive-obbt/figures/rates.py
Requires NumPy and Matplotlib. Outputs rates.pdf and rates.svg beside this file.
Sources: sections/local-rates.tex, prop:quadratic-growth,
prop:two-variable-rate, and ex:many-term.
"""

from fractions import Fraction
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def rho(a):
    """Exact centered-cube Jacobi factor for two variables, 0 < a < 2."""
    return (np.sqrt(2 * a**2 + 4 * a) - a) / 2


def scalar_q(a):
    """Quadratic-growth bound with mu=1-a^2/4 and tau=a/4."""
    return np.sqrt(a / (1 - a**2 / 4))


def t_n(a, n):
    """Untruncated complete-graph cube factor; this formula requires n >= 3."""
    if n < 3:
        raise ValueError("The complete-graph formula requires n >= 3.")
    return (np.sqrt(a**2 * (n - 1) ** 2 + 2 * a * n * (n - 1))
            - a * (n - 1)) / 2


def main():
    a_q = 2 * np.sqrt(2) - 2
    q_max = 1.6
    # Invert q(a)=q_max; the stable expression avoids subtracting close roots.
    q_end = 2 * q_max**2 / (np.sqrt(1 + q_max**4) + 1)
    thresholds = {3: Fraction(1), 4: Fraction(1, 3), 6: Fraction(1, 10)}

    # These checks evaluate the source formulas, not an OBBT experiment.
    np.testing.assert_allclose([rho(0), rho(2), scalar_q(a_q)], [0, 1, 1])
    np.testing.assert_allclose(scalar_q(q_end), q_max)
    assert np.all(rho(np.linspace(0.001, 1.999, 1000)) < 1)
    for n, threshold in thresholds.items():
        assert threshold * (n - 1) * (n - 2) == 2
        np.testing.assert_allclose(t_n(float(threshold), n), 1)
        assert t_n(0.99 * float(threshold), n) < 1
        assert t_n(1.01 * float(threshold), n) > 1

    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["DejaVu Serif"],
        "font.size": 10,
        "mathtext.fontset": "cm",
        "axes.labelsize": 10,
        "axes.titlesize": 10,
        "axes.linewidth": 0.7,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "pdf.fonttype": 42,
        "svg.hashsalt": "analytic-obbt-rates",
        "savefig.facecolor": "white",
    })
    fig, (left, right) = plt.subplots(1, 2, figsize=(6.4, 2.7))
    fig.subplots_adjust(left=0.085, right=0.985, bottom=0.19,
                        top=0.87, wspace=0.34)

    for ax in (left, right):
        ax.set_xlim(0, 2)
        ax.set_xticks([0, 0.5, 1, 1.5, 2], ["0", "0.5", "1", "1.5", "2"])
        ax.set_xlabel(r"$a$", labelpad=2)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(direction="out", length=3, width=0.7, pad=3)
        ax.axhline(1, color="0.78", linewidth=0.7, zorder=0)

    # Squared grids resolve the square-root behavior at a=0. Endpoints show
    # continuous limits; all scientific claims concern the open interval (0,2).
    a = np.linspace(0, np.sqrt(2), 900) ** 2
    q_a = np.unique(np.r_[np.linspace(0, np.sqrt(q_end), 650) ** 2, a_q])
    left.plot(a, rho(a), color="0.12", linewidth=1.6, label=r"Exact $\rho(a)$")
    left.plot(q_a, scalar_q(q_a), color="0.40", linewidth=1.5,
              linestyle=(0, (5, 3)), label=r"Scalar $q(a)$")
    left.plot([a_q, a_q], [0, 1], color="0.65", linewidth=0.7,
              linestyle=(0, (2, 3)), zorder=0)
    left.plot(a_q, 1, marker="o", markersize=4.5, markerfacecolor="white",
              markeredgecolor="0.40", markeredgewidth=1, zorder=4)
    left.text(a_q - 0.035, 1.06, r"$2\sqrt{2}-2$", ha="right", va="bottom")
    left.set_ylim(0, 1.65)
    left.set_yticks([0, 0.5, 1, 1.5], ["0", "0.5", "1", "1.5"])
    left.set_ylabel(r"$\rho(a),\ q(a)$", labelpad=4)
    left.set_title("(a) Two variables", loc="left", pad=6)
    left.legend(loc="lower right", frameon=False, handlelength=2.2,
                borderaxespad=0.35, labelspacing=0.35)

    styles = {3: ("0.12", "-", "o"),
              4: ("0.36", (0, (5, 3)), "s"),
              6: ("0.55", (0, (1, 2)), "^")}
    lines = {}
    # Draw the solid n=3 curve last so the common plateau remains legible.
    for n in (6, 4, 3):
        threshold = float(thresholds[n])
        n_a = np.unique(np.r_[a, threshold])
        color, linestyle, marker = styles[n]
        lines[n], = right.plot(
            n_a, np.minimum(1, t_n(n_a, n)), color=color, linewidth=1.5,
            linestyle=linestyle, marker=marker, markersize=4.5,
            markevery=[int(np.flatnonzero(n_a == threshold)[0])],
            markerfacecolor="white", markeredgewidth=1, label=rf"$n={n}$")
    # Redraw threshold markers above the overlapping plateau segments.
    for n, label in ((6, r"$\frac{1}{10}$"), (4, r"$\frac{1}{3}$"), (3, r"$1$")):
        color, _, marker = styles[n]
        threshold = float(thresholds[n])
        right.plot(threshold, 1, marker=marker, markersize=4.5,
                   markerfacecolor="white", markeredgecolor=color,
                   markeredgewidth=1, zorder=5)
        right.text(threshold, 1.045, label, ha="center", va="bottom")
    right.set_ylim(0, 1.2)
    right.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
    right.set_ylabel(r"$\min\{1,t_n(a)\}$", labelpad=4)
    right.set_title("(b) Complete-graph family", loc="left", pad=6)
    right.legend(handles=[lines[n] for n in (3, 4, 6)], loc="lower right",
                 frameon=False, handlelength=2.2, borderaxespad=0.35,
                 labelspacing=0.25)

    output = Path(__file__).resolve().parent
    metadata = {"Title": "Analytic OBBT contraction factors",
                "Creator": "Matplotlib; figures/rates.py"}
    fig.savefig(output / "rates.pdf", metadata={**metadata, "Author": "",
                "CreationDate": None, "ModDate": None})
    fig.savefig(output / "rates.svg", metadata={**metadata, "Date": None})
    plt.close(fig)
    print("Wrote rates.pdf and rates.svg; analytic identities passed.")


if __name__ == "__main__":
    main()
