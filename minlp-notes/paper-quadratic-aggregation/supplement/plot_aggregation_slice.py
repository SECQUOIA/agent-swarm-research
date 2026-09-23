"""Reproduce the finite-aggregation figure using explicit radial formulas.

Requires Python 3, NumPy, and Matplotlib. Run from any directory. The
output PDF is an illustration, not a computation of the full-dimensional
Hausdorff error. No optimization solver or external data is used.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


def exact_squared_radius(phi):
    # With x=rho*cos(phi), y=rho*sin(phi), the boundary equation is
    # a*rho^4-rho^2+3/4=0. Rationalization selects its smaller root
    # without cancellation, including a=0 on a coordinate axis.
    a = np.cos(phi) ** 2 * np.sin(phi) ** 2
    return 1.5 / (1 + np.sqrt(1 - 3 * a))


def mesh_squared_radius(phi, n):
    # The theta cut on this plane is
    # cos(theta)^2*x^2 + sin(theta)^2*y^2 <= 1-sin(theta)*cos(theta).
    theta = np.linspace(0, np.pi / 2, n)[:, None]
    denominator = (
        np.cos(theta) ** 2 * np.cos(phi)[None, :] ** 2
        + np.sin(theta) ** 2 * np.sin(phi)[None, :] ** 2
    )
    numerator = 1 - np.sin(theta) * np.cos(theta)
    radii = np.full_like(denominator, np.inf)
    np.divide(numerator, denominator, out=radii, where=denominator > 0)
    return np.min(radii, axis=0)


def main():
    phi = np.linspace(0, 2 * np.pi, 8001)
    exact = np.sqrt(exact_squared_radius(phi))
    curves = {n: np.sqrt(mesh_squared_radius(phi, n)) for n in (3, 5, 9)}
    # Finite numerical checks detect plotting/parametrization mistakes;
    # they do not verify the approximation theorem.
    x, y = exact * np.cos(phi), exact * np.sin(phi)
    assert np.max(np.abs((1 - x*x) * (1 - y*y) - 0.25)) < 2e-15
    assert np.max(np.abs(x)) < 1 and np.max(np.abs(y)) < 1
    for n, radius in curves.items():
        assert np.min(radius - exact) > -2e-15
        px, py = radius * np.cos(phi), radius * np.sin(phi)
        theta = np.linspace(0, np.pi / 2, n)[:, None]
        residual = (
            np.cos(theta)**2 * px[None, :]**2
            + np.sin(theta)**2 * py[None, :]**2
            - 1 + np.sin(theta)*np.cos(theta)
        )
        assert np.max(np.abs(np.max(residual, axis=0))) < 2e-15
    assert np.max(curves[9] - curves[5]) < 2e-15
    assert np.max(curves[5] - curves[3]) < 2e-15

    plt.rcParams.update({
        "font.family": "serif", "font.size": 10,
        "axes.labelsize": 11, "axes.titlesize": 11,
        "pdf.fonttype": 42, "ps.fonttype": 42,
    })
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 3.35), layout="constrained")
    styles = {
        3: ("#c44e00", (0, (5, 2))),
        5: ("#087e8b", (0, (3, 1, 1, 1))),
        9: ("#8153a4", (0, (1, 1))),
    }
    for ax in axes:
        ax.fill(x, y, facecolor="#e8edf0", edgecolor="none", zorder=0)
        for n, radius in curves.items():
            color, linestyle = styles[n]
            ax.plot(radius*np.cos(phi), radius*np.sin(phi), color=color,
                    linestyle=linestyle, linewidth=1.45, label=rf"$N={n}$")
        ax.plot(x, y, color="#111111", linewidth=1.5, label="Exact hull")
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$y$", rotation=0, labelpad=8)
        ax.grid(color="#d9d9d9", linewidth=0.5, alpha=0.65)
        ax.set_axisbelow(True)
    axes[0].set(xlim=(-1.06, 1.06), ylim=(-1.06, 1.06), title="Full planar section")
    axes[0].set_xticks((-1, -0.5, 0, 0.5, 1))
    axes[0].set_yticks((-1, -0.5, 0, 0.5, 1))
    axes[0].add_patch(Rectangle((0.72, 0.12), 0.24, 0.54, fill=False,
                               edgecolor="#777777", linewidth=0.8))
    axes[1].set(xlim=(0.72, 0.96), ylim=(0.12, 0.66), title="Enlarged boundary")
    axes[1].set_xticks((0.75, 0.85, 0.95))
    axes[1].set_yticks((0.2, 0.4, 0.6))
    handles, labels = axes[0].get_legend_handles_labels()
    # Keep the exact hull first in the shared legend.
    fig.legend(handles[-1:] + handles[:-1], labels[-1:] + labels[:-1],
               loc="outside lower center", ncol=4, frameon=False)
    out = Path(__file__).resolve().parents[1] / "figures"
    out.mkdir(exist_ok=True)
    fig.savefig(out / "finite-aggregation-slice.pdf", metadata={
        "Title": "Finite good-aggregation approximations of a quartic slice",
        "Author": "", "CreationDate": None, "ModDate": None,
    })
    fig.savefig(out / "finite-aggregation-slice.png", dpi=200)
    plt.close(fig)
    print("PASS: radial boundary checks at 8001 directions; figure generated")


if __name__ == "__main__":
    main()
