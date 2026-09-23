"""Illustrative plug-flow titration model; no parameters are fitted to a catalyst.

Run: python research/calculations/titration_front.py
Requires numpy, scipy, matplotlib. Outputs are written beside this script.

Question: when a titrant is fed to a packed bed during reaction, does the
rate-versus-cumulative-uptake curve reveal that only a fraction of the
titratable sites are catalytically active?

Model (dimensionless). Bed coordinate z in [0, 1]; time t in units of the
residence time tau. Two titratable site classes: A (active, per-site rate 1)
and S (spectator, rate 0). Site densities per unit bed length: nA = 1 - fS,
nS = fS (total titratable inventory 1). Titrant enters at c = 1 and is
consumed by adsorption only; gas-phase accumulation is neglected (quasi-steady
gas balance), which is the usual case because site inventory per bed volume
far exceeds gas-phase titrant inventory.

    dc/dz     = -DaA * nA * c * (1 - thA) - DaS * nS * c * (1 - thS)
    dthA/dt   =  DaA * c * (1 - thA) - RA * thA
    dthS/dt   =  DaS * c * (1 - thS) - RS * thS

DaA, DaS: adsorption rate constants times residence time (large = adsorption
much faster than convection, giving a sharp front). RA, RS: desorption rate
constants times residence time (0 = irreversible). The titrant feed rate per
titratable site per residence time is epsilon = eps; uptake U(t) is the
integral of nA*thA + nS*thS over the bed, and the observed reaction rate is
the integral of nA*(1 - thA) over the bed (differential conversion of the
reactant, which does not perturb the titrant).

Every rate is normalized to the fresh rate and every uptake to the total
titratable inventory, so the ideal front limit predicts the line
rate = 1 - U for every fS.
"""

from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp


OUT = Path(__file__).resolve().parent
NZ = 400


def simulate(fS, DaA, DaS, RA=0.0, RS=0.0, eps=0.02, t_end=None, n_out=400):
    """Return (U, rate) arrays normalized as described in the module docstring."""
    nA, nS = 1.0 - fS, fS
    z = (np.arange(NZ) + 0.5) / NZ
    dz = 1.0 / NZ

    def gas_profile(thA, thS):
        # Quasi-steady titrant profile: integrate dc/dz = -k(z) c along the bed.
        k = DaA * nA * (1.0 - thA) + DaS * nS * (1.0 - thS)
        # Exact solution on each cell for piecewise-constant k.
        c_in = np.empty(NZ)
        c_mean = np.empty(NZ)
        c = 1.0
        for i in range(NZ):
            c_in[i] = c
            ki = k[i]
            if ki * dz < 1e-12:
                c_mean[i] = c
            else:
                c_mean[i] = c * (1.0 - np.exp(-ki * dz)) / (ki * dz)
                c = c * np.exp(-ki * dz)
        return c_mean

    def rhs(_t, y):
        thA = y[:NZ]
        thS = y[NZ:]
        c = gas_profile(thA, thS)
        # eps scales the titrant feed so that the ideal front needs 1/eps
        # residence times to titrate the whole inventory.
        dA = eps * (DaA * c * (1.0 - thA)) - RA * thA
        dS = eps * (DaS * c * (1.0 - thS)) - RS * thS
        return np.concatenate([dA, dS])

    if t_end is None:
        t_end = 1.6 / eps
    t_eval = np.linspace(0.0, t_end, n_out)
    sol = solve_ivp(rhs, (0.0, t_end), np.zeros(2 * NZ), t_eval=t_eval,
                    method="LSODA", rtol=1e-7, atol=1e-10)
    thA = sol.y[:NZ].T
    thS = sol.y[NZ:].T
    U = (nA * thA + nS * thS).mean(axis=1)
    rate = (nA * (1.0 - thA)).mean(axis=1) / nA
    return U, rate


def intercept_and_slope(U, rate, upper=0.5):
    """Linear fit of the early part (rate above `upper` of fresh) as an
    experimentalist would extrapolate to the uptake at zero rate."""
    mask = rate >= upper
    p = np.polyfit(U[mask], rate[mask], 1)
    slope, offset = p
    return -offset / slope, slope


def main():
    cases = {}
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), sharey=True)

    # Panel 1: sharp-front regime, both classes adsorb fast.
    ax = axes[0]
    for fS in (0.0, 0.3, 0.6):
        U, r = simulate(fS, DaA=400.0, DaS=400.0)
        ax.plot(U, r, label=f"spectator fraction {fS:.1f}")
        icpt, slope = intercept_and_slope(U, r)
        cases[f"front_fS{fS}"] = {"extrapolated_intercept": float(icpt),
                                  "initial_slope": float(slope)}
    ax.plot([0, 1], [1, 0], "k:", lw=0.8, label="ideal front line")
    ax.set_title("Fast adsorption on both classes\n(sharp front, Da = 400)")
    ax.set_xlabel("uptake / titratable total")
    ax.set_ylabel("rate / fresh rate")
    ax.legend(fontsize=7)

    # Panel 2: slow adsorption everywhere (titrant nearly uniform along bed),
    # affinity of active sites 10x that of spectators.
    ax = axes[1]
    for fS in (0.0, 0.3, 0.6):
        U, r = simulate(fS, DaA=0.5, DaS=0.05, eps=0.4, t_end=60.0)
        ax.plot(U, r, label=f"spectator fraction {fS:.1f}")
        icpt, slope = intercept_and_slope(U, r)
        cases[f"uniform_affinity10_fS{fS}"] = {"extrapolated_intercept": float(icpt),
                                               "initial_slope": float(slope)}
    ax.plot([0, 1], [1, 0], "k:", lw=0.8)
    ax.set_title("Slow adsorption (Da = 0.5 / 0.05),\nactive sites bind 10x faster")
    ax.set_xlabel("uptake / titratable total")

    # Panel 3: sharp front for active sites, slow adsorption on spectators.
    ax = axes[2]
    for fS in (0.0, 0.3, 0.6):
        U, r = simulate(fS, DaA=400.0, DaS=0.5, eps=0.02, t_end=200.0)
        ax.plot(U, r, label=f"spectator fraction {fS:.1f}")
        icpt, slope = intercept_and_slope(U, r)
        cases[f"front_active_slow_spectator_fS{fS}"] = {
            "extrapolated_intercept": float(icpt), "initial_slope": float(slope)}
    ax.plot([0, 1], [1, 0], "k:", lw=0.8)
    ax.set_title("Sharp front on active sites (Da = 400),\nslow spectator uptake (Da = 0.5)")
    ax.set_xlabel("uptake / titratable total")

    for ax in axes:
        ax.set_xlim(0, 1.05)
        ax.set_ylim(0, 1.05)
    fig.tight_layout()
    fig.savefig(OUT / "titration_front.png", dpi=150)

    # Sensitivity: how sharp must the front be for the line to hide a 30 %
    # spectator fraction? Scan equal Da for both classes.
    scan = {}
    for Da in (1.0, 3.0, 10.0, 30.0, 100.0, 400.0):
        U, r = simulate(0.3, DaA=Da, DaS=Da, eps=0.02, t_end=120.0)
        icpt, slope = intercept_and_slope(U, r)
        # Maximum deviation from the ideal line over the range rate > 0.1.
        mask = r > 0.1
        dev = float(np.max(np.abs(r[mask] - (1.0 - U[mask]))))
        scan[f"Da{Da:g}"] = {"extrapolated_intercept": float(icpt),
                             "max_deviation_from_line": dev}

    # Reversible titrant with equal Da: desorption lets the titrant
    # redistribute; with equal affinity nothing changes, with unequal affinity
    # the active sites are titrated preferentially.
    rev = {}
    for label, (RA, RS) in {"equal_affinity": (0.05, 0.05),
                            "active_binds_stronger": (0.005, 0.05)}.items():
        U, r = simulate(0.3, DaA=400.0, DaS=400.0, RA=RA, RS=RS, eps=0.02,
                        t_end=150.0)
        icpt, slope = intercept_and_slope(U, r)
        rev[label] = {"extrapolated_intercept": float(icpt),
                      "initial_slope": float(slope),
                      "final_uptake": float(U[-1]), "final_rate": float(r[-1])}

    summary = {"panels": cases, "front_sharpness_scan_fS0.3": scan,
               "reversible_fS0.3": rev,
               "note": "Dimensionless illustration; intercepts and slopes are "
                       "normalized to the titratable total and the fresh rate."}
    (OUT / "titration_front_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
