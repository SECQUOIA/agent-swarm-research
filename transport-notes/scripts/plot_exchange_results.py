"""Create standalone scientific figures from the recorded checks."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.special import gammaln


def main():
    root = Path("results")
    data = json.loads((root/"surface-exchange-checks.json").read_text())
    trans = json.loads((root/"exchange-transient-checks.json").read_text())
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False, "savefig.dpi": 200})
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.7), constrained_layout=True)
    x = np.logspace(-3, 3, 300)
    c = np.pi/2*np.exp(gammaln((x+1)/4)-gammaln((x+3)/4))
    ax = axes[0]
    ax.loglog(x, c, color="#126e82", label="Local crossover")
    ax.loglog(x, np.pi/np.sqrt(x), "--", color="#d68c45", label="Immobile wall limit")
    ax.axhline(data["quadratic_zero_constant"], color="0.65", ls=":")
    rows = [r for r in data["wall_crossover"] if r["surface_diffusivity"] == 1e-6 and r["scaled_floor"] > 0]
    ax.scatter([r["scaled_floor"] for r in rows], [r["scaled_integral"] for r in rows],
               color="black", s=22, zorder=3, label="Periodic wall solve")
    ax.set(xlabel=r"Rate floor $\delta/\sqrt{aD_s}$", ylabel=r"Scaled surface resolvent $\mathcal{C}$",
           title="A. Rate floor versus surface diffusion")
    ax.legend(frameon=False, fontsize=8)
    ax = axes[1]
    for n, marker in [(512, "o"), (1024, "s"), (2048, "^")]:
        rows = [r for r in data["finite_bulk_checks"] if r["n"] == n]
        ax.semilogx([r["surface_diffusivity"] for r in rows],
                    [r["bulk_remainder"] for r in rows], marker+"-", label=f"Wall grid {n}")
    ax.axhline(data["predicted_limiting_bulk_remainder"], ls="--", color="black", label=r"Predicted $R_0$")
    ax.set(xlabel=r"Surface diffusivity $D_s$ (dimensionless)",
           ylabel=r"Bulk correction $D_{\rm flow}-BJ$", title="B. Finite bulk diffusion")
    ax.legend(frameon=False, fontsize=8)
    ax = axes[2]
    rows = trans["checks"]
    ax.semilogx([r["time"] for r in rows], [r["stationary_to_injected_variance_ratio"] for r in rows],
                "o-", color="#126e82")
    ax.axhline(2, ls="--", color="black")
    ax.set(xlabel="Time (dimensionless)", ylabel="Stationary / injected variance",
           title="C. Known renewal initialization effect")
    fig.savefig(root/"surface-exchange-verification.png")
    fig.savefig(root/"surface-exchange-verification.pdf")
    plt.close(fig)
    print("Created results/surface-exchange-verification.png and .pdf")


if __name__ == "__main__":
    main()
