"""Plot the saved fixed experiment. Requires matplotlib; does not rerun simulation.

By default the archived CSV next to this script is plotted and the PDF/PNG are written
beside it. Pass --data-dir to plot a rerun written elsewhere; the figures go there too.
"""
import argparse
import csv
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--data-dir", type=Path, default=Path(__file__).resolve().parent,
                    help="directory containing critical_additive_particles.csv (default: next to this script)")
directory = parser.parse_args().data_dir.resolve()
with (directory / "critical_additive_particles.csv").open() as stream:
    rows = list(csv.DictReader(stream))

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
figure, axes = plt.subplots(3, 2, figsize=(7.1, 8.8), constrained_layout=True)
panels = [
    ("normalized_count", "Particle count / n"),
    ("M_half", "Fractional moment M(1/2)"),
    ("log_mean", "Number mean log size"),
    ("largest_mass_fraction", "Largest mass fraction"),
    ("number_CDF_0.01", "Number fraction, size ≤ 0.01"),
    ("mass_CDF_100", "Mass fraction, size ≤ 100"),
]
colors = {1000: "#3b78b4", 10000: "#d28029", 100000: "#278568"}
flat = list(axes.flat)
for panel_index, (axis, (key, label)) in enumerate(zip(flat, panels)):
    for n, color in colors.items():
        for seed in (11, 29, 47):
            samples = [row for row in rows if int(row["n"]) == n and int(row["seed"]) == seed]
            axis.plot([float(row["time"]) for row in samples], [float(row[key]) for row in samples],
                      color=color, alpha=.7, linewidth=1.1, label=f"n={n:,}" if seed == 11 else None)
    axis.set(xlabel="Time (b=1)", title=f"({chr(97 + panel_index)}) {label}", xlim=(0, 10))
    axis.grid(alpha=.16)
flat[0].axhline(1, color="black", linestyle="--", linewidth=1, label="Continuum count")
flat[0].legend(fontsize=8)
times = [index / 20 for index in range(201)]
kappa = 3 - 2 * math.sqrt(2)
flat[1].plot(times, [math.exp(-kappa * t) for t in times], color="black", linestyle="--", linewidth=1,
                label="Continuum upper bound")
flat[1].set_yscale("log")
flat[1].legend(fontsize=8)
lower = [-2 * math.log(2) * t for t in times]
upper = [low + (1 - math.exp(-2 * kappa * t)) / (2 * kappa) for low, t in zip(lower, times)]
flat[2].fill_between(times, lower, upper, color="gray", alpha=.16, label="Continuum mean bounds")
flat[2].legend(fontsize=8)
for axis in flat[3:]:
    axis.set_ylim(-.025, 1.025)
figure.savefig(directory / "critical_additive_particles.png", dpi=180)
figure.savefig(directory / "critical_additive_particles.pdf")
