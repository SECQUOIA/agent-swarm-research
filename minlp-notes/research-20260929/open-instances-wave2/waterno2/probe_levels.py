"""Lagrangian probing on the boundary tank levels (exploratory, SCIP estimates).

For boundary t (between periods t and t+1), tank k and a piece I of the level
range, the Lagrangian bound of the problem restricted to z_{t,k} in I is
    L(u) - phi_t - phi_{t+1} + phi_t(end_k in I) + phi_{t+1}(start_k in I).
If it exceeds the cutoff UB, no point with objective <= UB has z_{t,k} in I.
The surviving pieces give reduced level domains; a bound B computed on the
reduced problem certifies  opt >= min(UB, B).

usage: python3 probe_levels.py T mult.json UB pieces out.json [workers]
"""
import os
import sys
import json
import multiprocessing as mp

import numpy as np

import period
import dpbox

_D = None


def _init(T):
    global _D
    _D = period.setup(T, os.environ.get("WATERNO2_IMPLIED"))


def _task(args):
    t, box, lam, mu = args
    try:
        r = period.solve_window(_D, t, t + 1, lam, mu, 120, {}, box)
    except ValueError:
        return np.inf
    return r["dual"] if r["status"] != "infeasible" else np.inf


def main():
    T = int(sys.argv[1])
    mult = json.load(open(sys.argv[2]))
    lam, mu = mult["lam"], mult["mu"]
    UB = float(sys.argv[3])
    pieces = int(sys.argv[4])
    out = sys.argv[5]
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else 5
    D = period.setup(T, os.environ.get("WATERNO2_IMPLIED"))
    S, M = D["S"], D["M"]
    pool = mp.Pool(workers, initializer=_init, initargs=(T,))
    base = pool.map(_task, [(t, {}, lam, mu) for t in range(T)])
    L = mu * float(D["hor_rhs"]) + sum(base)
    print(f"L(u) (SCIP) = {L:.4f}; UB = {UB}; gap = {UB - L:.4f}", flush=True)
    tasks, meta = [], []
    for t in range(T - 1):
        for k, (i, a, b) in enumerate(S["link"][t]):
            la, ha = dpbox.level_bounds(D, a)
            lb_, hb = dpbox.level_bounds(D, b)
            lo, hi = max(la, lb_), min(ha, hb)
            edges = np.linspace(lo, hi, pieces + 1)
            for p in range(pieces):
                I = (float(edges[p]), float(edges[p + 1]))
                tasks.append((t, {a: I}, lam, mu))
                tasks.append((t + 1, {b: I}, lam, mu))
                meta.append((t, k, a, b, I))
    vals = pool.map(_task, tasks, chunksize=2)
    pool.close()
    bounds = {}
    for n, (t, k, a, b, I) in enumerate(meta):
        v = L - base[t] - base[t + 1] + vals[2 * n] + vals[2 * n + 1]
        key = (t, k)
        bounds.setdefault(key, []).append((I, v))
    newb = {}
    for (t, k), lst in sorted(bounds.items()):
        keep = [I for I, v in lst if v <= UB]
        i, a, b = S["link"][t][k]
        if keep:
            lo, hi = min(I[0] for I in keep), max(I[1] for I in keep)
        else:
            lo, hi = None, None
        print(f"boundary {t} tank {k + 1}: " + " ".join(f"[{I[0]:.2f},{I[1]:.2f}]:{v:.1f}" for I, v in lst)
              + f"  -> keep [{lo}, {hi}]", flush=True)
        if keep:
            newb[M["names"][a]] = (lo, hi)
            newb[M["names"][b]] = (lo, hi)
    json.dump(dict(T=T, UB=UB, L=L, bounds=newb), open(out, "w"), indent=0)


if __name__ == "__main__":
    main()
