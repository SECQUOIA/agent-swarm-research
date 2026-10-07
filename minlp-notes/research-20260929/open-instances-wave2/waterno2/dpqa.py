"""Lagrangian relaxation of the level links plus an exact treatment of the
horizon row  sum_t h_t >= c  (h_t = station-A outflow of period t) by
dynamic programming over bins of h_t.

For every period t and bin [a_k, b_k] of h_t, phi_t(u; k) is the period
Lagrangian value with h_t restricted to the bin (the mu-term of the horizon
row may be kept; mu = 0 is allowed).  Any feasible point has h_t in some bin
k_t for each t, and then sum_t b_{k_t} >= sum_t h_t >= c.  Hence
    opt >= mu*c + min { sum_t phi_t(u; k_t) : sum_t b_{k_t} >= c }.
The bin ends lie on a grid of step g, so the DP state (sum of upper ends,
capped at c) is exact.

mode 'scip': SCIP estimates (exploration).  mode 'rbb': certified values.

usage: python3 dpqa.py T mult.json binspec mode out.json [workers] [node_limit] [time_limit] [targets.json]
  binspec: comma-separated bin edges, e.g. "0,0,0.2,0.3,0.4,...,2.4"; a repeated
           edge "0,0" gives the degenerate bin [0,0].
"""
import os
import sys
import json
import time
import multiprocessing as mp
from fractions import Fraction

import numpy as np

import period
import rbb
import bundle

_D = None


def _init(T):
    global _D
    _D = period.setup(T, os.environ.get("WATERNO2_IMPLIED"))


def hvar(D, t):
    vs = [v for v in D["hor"] if D["per_of"][v] == t]
    assert len(vs) == 1
    return vs[0]


def _task(args):
    t, k, a, b, lam, mu, mode, node_limit, time_limit, target = args
    D = _D
    box = {hvar(D, t): (a, b)}
    tic = time.time()
    if mode == "scip":
        try:
            r = period.solve_window(D, t, t + 1, lam, mu, 120, {}, box)
        except ValueError:
            return (t, k, np.inf, np.inf, "empty", 0.0)
        val = r["dual"] if r["status"] != "infeasible" else np.inf
        return (t, k, val, r["primal"], r["status"], time.time() - tic)
    W = rbb.Window(D, t, t + 1, box)
    if np.any(W.lo0 > W.hi0):
        return (t, k, np.inf, np.inf, "empty", 0.0)
    c = W.objective(lam, mu)
    obbt_vars = sorted({x for kind, args_ in W.auxdef for x in args_ if not W.isbin[x]})
    res = rbb.solve(W, c, target, node_limit=node_limit, time_limit=time_limit, obbt_vars=obbt_vars)
    return (t, k, res["bound"], target, res["status"], time.time() - tic)


def dp(T, bins, phi, c_hor, mu_c):
    """min sum phi[t][k] s.t. sum of upper bin ends >= c_hor (exact rationals)."""
    cap = Fraction(c_hor)
    states = {Fraction(0): (0.0, [])}
    for t in range(T):
        new = {}
        for s, (v, path) in states.items():
            for k, (a, b) in enumerate(bins):
                val = phi[(t, k)]
                if not np.isfinite(val):
                    continue
                s2 = min(cap, s + Fraction(str(b)))
                v2 = v + val
                if s2 not in new or v2 < new[s2][0]:
                    new[s2] = (v2, path + [k])
        states = new
    if cap not in states:
        return np.inf, None
    v, path = states[cap]
    return mu_c + v, path


def main():
    T = int(sys.argv[1])
    mult = json.load(open(sys.argv[2]))
    lam, mu = mult["lam"], mult["mu"]
    edges = [float(e) for e in sys.argv[3].split(",")]
    bins = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]
    mode = sys.argv[4]
    out = sys.argv[5]
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else 4
    node_limit = int(sys.argv[7]) if len(sys.argv) > 7 else 100000
    time_limit = float(sys.argv[8]) if len(sys.argv) > 8 else 1800.0
    targets = json.load(open(sys.argv[9])) if len(sys.argv) > 9 else {}
    D = period.setup(T, os.environ.get("WATERNO2_IMPLIED"))
    tasks = [(t, k, a, b, lam, mu, mode, node_limit, time_limit, targets.get(f"{t},{k}"))
             for t in range(T) for k, (a, b) in enumerate(bins)]
    tic = time.time()
    pool = mp.Pool(workers, initializer=_init, initargs=(T,))
    res = pool.map(_task, tasks, chunksize=1)
    pool.close()
    phi = {(r[0], r[1]): r[2] for r in res}
    val, path = dp(T, bins, phi, D["hor_rhs"], mu * float(D["hor_rhs"]))
    print(f"bins {len(bins)}; subproblems {len(tasks)}; wall {time.time()-tic:.0f}s")
    print(f"DP bound ({mode}): {val:.6f}; path {path}")
    if path:
        for t, k in enumerate(path):
            print(f"  period {t}: h in {bins[k]}  phi {phi[(t, k)]:.6f}")
    json.dump(dict(T=T, bins=bins, mode=mode, bound=val, path=path,
                   results=[dict(t=r[0], k=r[1], value=r[2], primal_or_target=r[3], status=r[4], time=r[5])
                            for r in res],
                   lam=[[repr(v) for v in l] for l in lam], mu=repr(mu)), open(out, "w"), indent=0)


if __name__ == "__main__":
    main()
