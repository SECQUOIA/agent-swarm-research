"""Illustrative identifiability calculation; no parameters are fitted to a catalyst.

Run: python research/calculations/aging_schedule.py
Requires numpy, scipy, matplotlib. Outputs are written beside this script.
"""

from pathlib import Path
import csv
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp


OUT = Path(__file__).resolve().parent
WET_TIME = 10.0  # Arbitrary time units, not minutes or hours.
DRY_TIME = 10.0
PULSES = (1, 2, 5, 10, 20, 50, 100)
# kh: hydrolysis, kr: recovery, kd: irreversible loss of Al equivalents.
# dD/dt = kd*R**2; kd includes the stoichiometric factor for a pair event.
REGIMES = {
    "finite_relaxation": {"wet": (1.0, 0.1, 1.0), "dry": (0.0, 1.0, 0.0)},
    "fast_equilibration": {"wet": (10000.0, 1000.0, 1.0), "dry": (0.0, 1.0, 0.0)},
    "dry_inert": {"wet": (1.0, 0.1, 1.0), "dry": (0.0, 0.0, 0.0)},
    "dry_also_damages": {"wet": (1.0, 0.1, 1.0), "dry": (0.0, 1.0, 2.0)},
}


def evolve(state, duration, rates, rtol=1e-8):
    kh, kr, kd = rates

    def rhs(_time, y):
        f, r, _d = y
        exchange = kh*f - kr*r
        loss = kd*r*r
        return (-exchange, exchange-loss, loss)

    sol = solve_ivp(rhs, (0, duration), state, method="Radau", rtol=rtol, atol=rtol*0.01)
    if not sol.success:
        raise RuntimeError(sol.message)
    y = sol.y[:, -1]
    if abs(y.sum()-1) > 1e-7 or y.min() < -1e-9:
        raise RuntimeError(f"Unphysical Al balance: {y}")
    return y


def schedule(regime, n, rtol=1e-8):
    y = np.array([1.0, 0.0, 0.0])
    for _ in range(n):
        y = evolve(y, WET_TIME/n, regime["wet"], rtol)
        y = evolve(y, DRY_TIME/n, regime["dry"], rtol)
    # Ideal terminal assay: recover all R without damage. This is an explicit
    # observation-model assumption, not a claim about an actual NH3 assay.
    return y, y[0]+y[1]


def main():
    rows = []
    for name, regime in REGIMES.items():
        for n in PULSES:
            y, surviving = schedule(regime, n)
            rows.append({"regime": name, "pulses": n, "wet_bout": WET_TIME/n,
                         "F_before_assay": y[0], "R_before_assay": y[1],
                         "D": y[2], "recoverable_after_ideal_assay": surviving})
    with (OUT/"aging_schedule.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    # A stricter numerical solve verifies the representative pulse extremes.
    max_difference = 0.0
    for name, regime in REGIMES.items():
        for n in (1, 100):
            normal = schedule(regime, n)[1]
            tighter = schedule(regime, n, rtol=1e-10)[1]
            max_difference = max(max_difference, abs(normal-tighter))
    # Separable direct-loss null: dF/dt = -k(t)*F**2, integral k dt = 10.
    direct_null = 1/(1+WET_TIME)
    # A heterogeneous independent-site null also depends only on exposure.
    heterogeneous_null = 0.5*np.exp(-0.1*WET_TIME)+0.5*np.exp(-WET_TIME)
    summary = {"interpretation": "Illustration only; arbitrary unfitted time/rate units",
               "wet_time": WET_TIME, "dry_time": DRY_TIME, "rates": REGIMES,
               "max_absolute_tolerance_check_difference": max_difference,
               "direct_second_order_null_survival": direct_null,
               "heterogeneous_first_order_null_survival": heterogeneous_null,
               "nonseparable_scalar_null": {
                   "equations": "wet: dF/dt=-F**2; dry: dF/dt=-F; each duration 1",
                   "wet_then_dry": 0.5*np.exp(-1),
                   "dry_then_wet": np.exp(-1)/(1+np.exp(-1)),
                   "meaning": "Order dependence without a hidden recoverable population"},
               "endpoint_summary": [r for r in rows if r["pulses"] in (1, 100)]}
    (OUT/"aging_schedule_summary.json").write_text(json.dumps(summary, indent=2)+"\n")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for name in REGIMES:
        selected = [r for r in rows if r["regime"] == name]
        ax.semilogx([r["wet_bout"] for r in selected],
                    [r["recoverable_after_ideal_assay"] for r in selected],
                    "o-", label=name.replace("_", " "))
    ax.axhline(direct_null, color="black", linestyle="--", label="separable direct-loss null")
    ax.set(xlabel="Wet-bout duration (arbitrary time units)",
           ylabel="Surviving F + R fraction",
           title="Illustrative models: equal total wet and dry exposure")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(OUT/"aging_schedule.png", dpi=180)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
