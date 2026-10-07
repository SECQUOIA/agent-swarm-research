"""Analyze logs/sweep.jsonl: leaves of the uniform bisection tree versus the
proved lower bounds of the note and the RLCT prediction.

For each instance: leaves, the Theorem 3.1 lower bound (full-dimensional, or
the edge face for 'bdry'), their ratio, and least-squares slopes of
log(leaves) and log(leaves / log(1/eps)^(theta-1)) against log(1/eps) over the
last three decades of eps.  Floating-point illustration only.
Usage: python3 analyze_sweep.py > logs/analyze_sweep.log
"""
import json
import math

import numpy as np

import instances
import integrals as it

PRED = {  # instance: (lower-bound integral, face dim d, lambda, theta, exponent)
    "xy2": (it.I_xy2, 2, 0.5, 2, 0.5),
    "sep24": (it.I_sep24, 2, 0.75, 1, 0.25),
    "cusp": (it.I_cusp, 2, 5 / 12, 1, 7 / 12),
    "xy2z4": (it.I_xy2z4, 3, 0.75, 2, 0.75),
    "bdry": (it.I_bdry_edge, 1, 0.25, 1, 0.25),
    "rrr1e-2": (lambda e: it.I_rrr(e, 1e-2), 2, 0.5, 1, 0.5),
    "rrr1e-3": (lambda e: it.I_rrr(e, 1e-3), 2, 0.5, 1, 0.5),
}


def slope(x, y):
    A = np.vstack([x, np.ones_like(x)]).T
    return float(np.linalg.lstsq(A, y, rcond=None)[0][0])


def main():
    rows = [json.loads(l) for l in open("logs/sweep.jsonl")]
    for name, (Ifun, d, lam, theta, ex) in PRED.items():
        rs = sorted([r for r in rows if r["instance"] == name], key=lambda r: -r["eps"])
        if not rs:
            continue
        alpha = instances.get(name)["alpha"]
        print(f"\n== {name}: face dim d = {d}, predicted RLCT ({lam:.4g}, {theta}), "
              f"exponent {ex:.4g}, log power {theta - 1}; alpha = {alpha:.4g}")
        print(f"{'eps':>10} {'nodes':>9} {'leaves':>9} {'lower bd':>10} {'leaves/LB':>9} {'undecided':>9}")
        E, Lv = [], []
        for r in rs:
            e = r["eps"]
            lb = (alpha * d / math.pi ** 2) ** (d / 2) * Ifun(e)
            print(f"{e:10.3e} {r['nodes']:9d} {r['leaves']:9d} {lb:10.4g} {r['leaves'] / lb:9.2f} {r['undecided']:9d}")
            E.append(e)
            Lv.append(r["leaves"])
        E, Lv = np.array(E), np.array(Lv, float)
        x = np.log(1 / E)
        sel = E <= E.min() * 1e3 * (1 + 1e-9)
        s1 = slope(x[sel], np.log(Lv[sel]))
        s2 = slope(x[sel], np.log(Lv[sel] / x[sel] ** (theta - 1)))
        print(f"slope of log(leaves) over eps in [{E[sel].min():.1e}, {E[sel].max():.1e}]: {s1:.3f}; "
              f"after dividing by log(1/eps)^{theta - 1}: {s2:.3f}; predicted exponent {ex:.4f}")
    # the noisy toy: leaves * sqrt(eps) keeps growing like log(1/eps) for delta = 0
    # (instance xy2 is (xy - 0)^2) and freezes for eps << delta^2
    print("\n== leaves * sqrt(eps) for m = (xy - delta)^2 (delta = 0 is instance xy2)")
    by = {}
    for r in rows:
        if r["instance"] in ("xy2", "rrr1e-3", "rrr1e-2"):
            by.setdefault(round(math.log10(r["eps"]) * 4), {})[r["instance"]] = r["leaves"] * math.sqrt(r["eps"])
    print(f"{'eps':>10} {'delta=0':>9} {'1e-3':>9} {'1e-2':>9}")
    for k in sorted(by, reverse=True):
        v = by[k]
        print(f"{10 ** (k / 4):10.3e} " + " ".join(f"{v.get(nm, float('nan')):9.1f}" for nm in ("xy2", "rrr1e-3", "rrr1e-2")))


if __name__ == "__main__":
    main()
