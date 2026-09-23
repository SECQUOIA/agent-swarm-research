"""Plot explicit trial checks; no numerical optimizer is implied."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import gamma


def main():
    data = json.loads(Path("results/risk-sensitive-design-checks.json").read_text())
    rows = data["trials"]
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False})
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 3.8), constrained_layout=True)
    colors = ["#277da8", "#7a5195", "#dd8452", "#34845d"]
    for q, color in zip([1.2, 1.6, 2, 3], colors):
        selected = [r for r in rows if r["order"] == q]
        budget = np.array([r["budget"] for r in selected])
        ratio = np.array([r["trial_to_uniform_ratio"] for r in selected])
        axes[0].loglog(budget, ratio, "o-", color=color, label=f"q = {q:g}")
    axes[0].set(xlabel="Mobility budget M", ylabel="Trial moment / uniform moment",
                title="A. Explicit graded designs")
    axes[0].axhline(1, color="0.6", lw=0.8, ls="--")
    axes[0].legend(frameon=False)
    axes[0].invert_xaxis()

    selected = [r for r in rows if r["order"] == 3]
    budget = np.array([r["budget"] for r in selected])
    trial = np.array([r["graded_trial_moment"] for r in selected])
    uniform = np.array([r["uniform_moment"] for r in selected])
    axes[1].loglog(budget, trial/trial[0], "o-", color=colors[3], label="Graded trial")
    axes[1].loglog(budget, uniform/uniform[0], "s-", color="0.4", label="Uniform")
    axes[1].loglog(budget, budget[0]/budget, "--", color=colors[3], label="M⁻¹ guide")
    axes[1].loglog(budget, (budget[0]/budget)**(7/6), ":", color="0.4", label="M⁻⁷⁄⁶ guide")
    axes[1].set(xlabel="Mobility budget M", ylabel="Third moment / value at M = 10⁻³",
                title="B. Different growth rates (q = 3)")
    axes[1].invert_xaxis()
    axes[1].legend(frameon=False)

    selected = [r for r in rows if r["order"] == 1.6]
    budget = np.array([r["budget"] for r in selected])
    scaled = np.array([r["scaled_trial_moment"] for r in selected])
    axes[2].semilogx(budget, scaled, "o-", color=colors[1])
    c0 = np.pi/2*gamma(0.25)/gamma(0.75)
    critical = (2*c0)**1.6/8*(4/7)**1.4
    axes[2].axhline(critical, color="0.4", ls="--", lw=1,
                    label=f"Proved limit: {critical:.3f}")
    axes[2].set(xlabel="Mobility budget M",
                ylabel="M²⁄⁵ E[J⁸⁄⁵] / [log(1/M)]⁷⁄⁵",
                title="C. Slow critical convergence")
    axes[2].invert_xaxis()
    axes[2].text(0.05, 0.25, "Explicit trial; slow convergence.\nNo finite-budget optimum is implied.",
                 transform=axes[2].transAxes, fontsize=9)
    axes[2].legend(frameon=False, loc="lower left")
    for ax in axes:
        ax.grid(alpha=0.15)
    fig.savefig("results/risk-sensitive-design.png", dpi=180)
    fig.savefig("results/risk-sensitive-design.pdf")


if __name__ == "__main__":
    main()
