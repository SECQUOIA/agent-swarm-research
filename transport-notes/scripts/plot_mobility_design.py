"""Plot verified design laws and the random-offset sensitivity result."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from check_placement_phases import candidate, ONSET, MERGER


def main():
    root = Path("results")
    placement = json.loads((root/"optimal-placement-checks.json").read_text())
    disorder = json.loads((root/"coalescing-zero-checks.json").read_text())
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False, "savefig.dpi": 200})
    fig, axes = plt.subplots(2, 2, figsize=(10, 7), constrained_layout=True)
    ax = axes[0, 0]
    x = np.linspace(-1.3, 1.3, 700)
    y = abs(x)
    d = np.where(y < 1, y*(1-y)**2*(1+2*y)/8, 0)
    ax.plot(x, d, color="#126e82")
    ax.axvline(0, color="0.65", ls=":")
    ax.set(xlabel=r"Distance from kinetic zero $s/R$",
           ylabel=r"Optimal mobility $D_*/(aR^4)$",
           title="A. Exact placement at a fixed budget")
    ax.annotate("Kinetic zero", (0, 0), (0.15, 0.017),
                arrowprops={"arrowstyle": "->", "color": "0.4"}, fontsize=8)
    ax = axes[0, 1]
    rows = placement["periodic_design_comparison"]
    ax.semilogx([r["budget"] for r in rows], [r["localized_to_uniform_ratio"] for r in rows],
                 "o-", color="#126e82")
    ax.set(xlabel=r"Total mobility budget $M$ (dimensionless)",
           ylabel="Localized / uniform surface contribution",
           title="B. Same budget, different placement")
    ax = axes[1, 0]
    etas = np.linspace(ONSET, 4.5, 250)
    profiles = [candidate(e)[0] for e in etas]
    left = np.array([r["left"] for r in profiles])
    right = np.array([r["right"] for r in profiles])
    ax.fill_between(etas, left, right, color="#126e82", alpha=0.7)
    ax.fill_between(etas, -right, -left, color="#126e82", alpha=0.7)
    ax.axvline(ONSET, color="0.3", ls="--")
    ax.axvline(MERGER, color="0.3", ls=":")
    ax.set(xlim=(1, 4.5), xlabel=r"Flow parameter $\eta=|V|\sqrt{a}/\delta^{3/2}$",
           ylabel=r"Position $s\sqrt{a/\delta}$",
           title="C. Support of the optimal mobility")
    ax.text(1.02, 2.25, "No mobility", fontsize=8)
    ax.text(1.61, 2.25, "Two flanks", fontsize=8)
    ax.text(2.52, 2.25, "Central region", fontsize=8)
    ax = axes[1, 1]
    rows = disorder["random_offset_moments"]
    dx = np.logspace(-9, -3, 160)
    variance_constant = disorder["pair_moment_integrals"][1]["candidate_ensemble_moment_coefficient"]
    mean_constant = rows[0]["candidate_scaled_mean"]
    ax.loglog(dx, variance_constant/mean_constant**2*dx**(-1/6), "--", color="#d68c45",
              label=r"Leading $D_s^{-1/6}$ law")
    ax.loglog([r["diffusivity"] for r in rows],
              [r["coefficient_of_variation_squared"] for r in rows],
              "o-", color="#126e82", label="Periodic ensemble calculation")
    ax.set(xlabel=r"Surface diffusivity $D_s$ (dimensionless)",
           ylabel="Squared coefficient of variation",
           title="D. Sensitivity to a random rate offset")
    ax.legend(frameon=False, fontsize=8)
    fig.savefig(root/"mobility-design-and-disorder.png")
    fig.savefig(root/"mobility-design-and-disorder.pdf")
    plt.close(fig)
    print("Created results/mobility-design-and-disorder.png and .pdf")


if __name__ == "__main__":
    main()
