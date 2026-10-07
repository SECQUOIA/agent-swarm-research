#!/usr/bin/env python3
"""Draw the five edge zeros used in the three-variable quadratic example.

This is a fixed affine projection of exact coordinates. It performs no
optimization, sampling, or numerical verification of the polynomial.
"""

from itertools import product
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def project(point):
    """Project the coordinate axes to three fixed directions in the plane."""
    x, y, z = point
    return np.array([1.20 * x - 0.85 * y, -0.28 * x - 0.43 * y + 1.30 * z])


def main():
    output = Path(__file__).resolve().parent
    previews = output.parent / "verification" / "previews"
    previews.mkdir(parents=True, exist_ok=True)
    matplotlib.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["DejaVu Serif"],
            "font.size": 10,
            "mathtext.fontset": "cm",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )
    fig, ax = plt.subplots(figsize=(4.5, 3.6))
    vertices = list(product((0, 1), repeat=3))
    origin = (0, 0, 0)
    zero_edges = {
        frozenset((origin, (1, 0, 0))),
        frozenset((origin, (0, 1, 0))),
        frozenset(((1, 0, 0), (1, 0, 1))),
        frozenset(((0, 1, 0), (0, 1, 1))),
        frozenset(((1, 1, 0), (1, 1, 1))),
    }

    for first in vertices:
        for second in vertices:
            if first >= second or sum(a != b for a, b in zip(first, second)) != 1:
                continue
            edge = frozenset((first, second))
            projected = np.stack([project(first), project(second)])
            # The three edges incident to the rear vertex are dashed.
            hidden = origin in edge
            emphasized = edge in zero_edges
            ax.plot(
                projected[:, 0],
                projected[:, 1],
                color="0.38" if emphasized else "0.64",
                linewidth=1.1 if emphasized else 0.8,
                linestyle=(0, (3, 3)) if hidden else "solid",
                solid_capstyle="round",
                zorder=1 if hidden else 2,
            )

    contacts = {
        "a": ((0.5, 0, 0), (0, 11), "center"),
        "b": ((0, 0.5, 0), (-8, 10), "right"),
        "c": ((1, 0, 1 / 6), (10, 0), "left"),
        "d": ((0, 1, 1 / 6), (-10, 0), "right"),
        "e": ((1, 1, 5 / 6), (10, 0), "left"),
    }
    for label, (point, offset, alignment) in contacts.items():
        planar = project(point)
        ax.plot(*planar, "o", markersize=4.4, color="black", zorder=5)
        ax.annotate(
            rf"${label}$",
            planar,
            xytext=offset,
            textcoords="offset points",
            ha=alignment,
            va="center",
            fontsize=12,
            zorder=6,
        )

    coordinate_labels = [
        ((0, 0, 0), r"$(0,0,0)$", (-7, 10), "right"),
        ((1, 0, 0), r"$(1,0,0)$", (6, -12), "left"),
        ((0, 1, 0), r"$(0,1,0)$", (-5, -12), "right"),
        ((0, 0, 1), r"$(0,0,1)$", (-6, 10), "right"),
    ]
    for point, label, offset, alignment in coordinate_labels:
        ax.annotate(
            label,
            project(point),
            xytext=offset,
            textcoords="offset points",
            ha=alignment,
            va="center",
            fontsize=9,
            color="0.25",
        )

    ax.set_aspect("equal")
    ax.set_xlim(-1.40, 1.74)
    ax.set_ylim(-0.93, 1.61)
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.savefig(
        output / "five-edge-zeros.pdf",
        bbox_inches="tight",
        pad_inches=0.02,
        metadata={"CreationDate": None, "ModDate": None},
    )
    fig.savefig(previews / "five-edge-zeros.png", dpi=220, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


if __name__ == "__main__":
    main()
