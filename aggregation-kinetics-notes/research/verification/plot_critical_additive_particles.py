"""Plot the saved fixed experiment. Requires matplotlib; does not rerun simulation."""
import csv
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

directory = Path(__file__).resolve().parent
with (directory / "critical_additive_particles.csv").open() as stream:
    rows = list(csv.DictReader(stream))

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
figure, axes = plt.subplots(2, 3, figsize=(12, 7.2), constrained_layout=True)
panels = [
    ("normalized_count", "Particle count / n"),
    ("M_half", "Fractional moment M(1/2)"),
    ("log_mean", "Number-weighted mean log size"),
    ("largest_mass_fraction", "Mass fraction in largest particle"),
    ("number_CDF_0.01", "Number fraction with size ≤ 0.01"),
    ("mass_CDF_100", "Mass fraction in sizes ≤ 100"),
]
colors = {1000: "#3b78b4", 10000: "#d28029", 100000: "#278568"}
for axis, (key, label) in zip(axes.flat, panels):
    for n, color in colors.items():
        for seed in (11, 29, 47):
            samples = [row for row in rows if int(row["n"]) == n and int(row["seed"]) == seed]
            axis.plot([float(row["time"]) for row in samples], [float(row[key]) for row in samples],
                      color=color, alpha=.7, linewidth=1.1, label=f"n={n:,}" if seed == 11 else None)
    axis.set(xlabel="Time (b=1)", title=label, xlim=(0, 10))
    axis.grid(alpha=.16)
axes[0, 0].axhline(1, color="black", linestyle="--", linewidth=1, label="Continuum count")
axes[0, 0].legend(fontsize=8)
times = [index / 20 for index in range(201)]
kappa = 3 - 2 * math.sqrt(2)
axes[0, 1].plot(times, [math.exp(-kappa * t) for t in times], color="black", linestyle="--", linewidth=1,
                label="Continuum upper bound")
axes[0, 1].set_yscale("log")
axes[0, 1].legend(fontsize=8)
lower = [-2 * math.log(2) * t for t in times]
upper = [low + (1 - math.exp(-2 * kappa * t)) / (2 * kappa) for low, t in zip(lower, times)]
axes[0, 2].fill_between(times, lower, upper, color="gray", alpha=.16, label="Continuum mean bounds")
axes[0, 2].legend(fontsize=8)
for axis in axes[1]:
    axis.set_ylim(-.025, 1.025)
figure.suptitle("Finite critical additive coagulation with equal fragmentation\nThree independent seeds per n; dashed bounds concern the continuum equation", fontsize=13)
figure.savefig(directory / "critical_additive_particles.png", dpi=180)
figure.savefig(directory / "critical_additive_particles.pdf")
