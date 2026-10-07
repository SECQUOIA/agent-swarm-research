"""Reproduce SCIP's inconsistent 'optimal' claims on period subproblems of
waterno2_06 (Lagrangian objective at fixed multipliers, logs/scip_repro_mult.json).

For each period t in {0, 4, 5} SCIP is run with several parameter settings.
All runs report status 'optimal', but the optimal values differ by up to 2.4.
The best point found by any run is re-evaluated in double precision on the
period rows (max row and bound violation).  A point with value v and small
violation shows that a run claiming an optimum > v (by more than the
tolerance effect) returned an invalid dual bound.
"""
import json
import subprocess
import sys

import period
import bundle

SETTINGS = {
    "default": {},
    "noprop": dict(bundle.NOPROP),
    "noobbt": {"propagating/obbt/freq": -1},
    "seed7": {"randomization/randomseedshift": 7},
    "feastol1e-8": {"numerics/feastol": 1e-8},
}


def viol(D, t, x):
    M, S = D["M"], D["S"]
    worst = 0.0
    for i in S["per_rows"][t]:
        r = M["rows"][i]
        s = 0.0
        for mono, a in r["poly"].items():
            v = float(a)
            for j in mono:
                v *= x[j]
            s += v
        if r["lb"].upper() != "-INF":
            worst = max(worst, float(r["lb"]) - s)
        if r["ub"].upper() not in ("INF", "+INF"):
            worst = max(worst, s - float(r["ub"]))
    for j in S["per_vars"][t]:
        if M["lb"][j].upper() != "-INF":
            worst = max(worst, float(M["lb"][j]) - x[j])
        if M["ub"][j].upper() not in ("INF", "+INF"):
            worst = max(worst, x[j] - float(M["ub"][j]))
    return worst


def main():
    D = period.setup(6)
    k = json.load(open("logs/scip_repro_mult.json"))
    lam = [[float(v) for v in l] for l in k["lam"]]
    mu = float(k["mu"])
    M, S = D["M"], D["S"]
    for t in (0, 4, 5):
        best = None
        for name, prm in SETTINGS.items():
            r = period.solve_window(D, t, t + 1, lam, mu, 300, prm)
            conf = [int(round(r["x"][v])) for v in S["per_vars"][t] if M["vt"][v] == "B"]
            print(f"period {t} {name:12s} status {r['status']:8s} claimed optimum {r['dual']:.6f} "
                  f"incumbent {r['primal']:.6f} viol {viol(D, t, r['x']):.1e} pumps {conf} "
                  f"nodes {r['nodes']} time {r['time']:.1f}s", flush=True)
            if best is None or r["primal"] < best[0]:
                best = (r["primal"], name)
        print(f"period {t}: lowest incumbent {best[0]:.6f} (setting {best[1]})", flush=True)


if __name__ == "__main__":
    main()
