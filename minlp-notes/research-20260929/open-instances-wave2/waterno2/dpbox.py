"""Lagrangian relaxation plus dynamic programming over boxes of the tank levels
at the period boundaries.

For every boundary t (between periods t and t+1) the level space is split into
boxes (a product grid of per-tank intervals).  The problem restricted to one
box per boundary is relaxed by giving each period its own copy of the
boundary levels (both copies constrained to the box) and dualizing the copy
equalities with the fixed multipliers u = (lam, mu).  For a box sequence
(k_0, ..., k_{T-2}) this gives the bound mu*c + sum_t phi_t(u; k_{t-1}, k_t);
the minimum over all sequences (a shortest path) is a lower bound on the
optimum because the boxes cover the level space.

mode 'scip': phi values are SCIP estimates (not certified; exploration only).
mode 'rbb' : phi values are certified lower bounds from rbb.solve.

usage: python3 dpbox.py T mult.json splits mode out.json [workers] [node_limit] [time_limit]
  splits: per-tank breakpoints, e.g. "3.5;;4" (tank 1 split at 3.5, tank 2 unsplit,
          tank 3 split at 4); the same grid is used at every boundary.
"""
import os
import sys
import json
import time
import itertools
import multiprocessing as mp

import numpy as np

import period
import rbb
import bundle

_D = None


def _init(T):
    global _D
    _D = period.setup(T, os.environ.get("WATERNO2_IMPLIED"))


def level_bounds(D, v):
    M = D["M"]
    lo, hi = float(M["lb"][v]), float(M["ub"][v])
    if v in D["extra"]:
        lo, hi = max(lo, D["extra"][v][0]), min(hi, D["extra"][v][1])
    return lo, hi


def boxes_for_boundary(D, t, splits):
    """List of boxes; each box is a list of 3 intervals (tank 1..3)."""
    S = D["S"]
    per_tank = []
    for k, (i, a, b) in enumerate(S["link"][t]):
        la, ha = level_bounds(D, a)
        lb_, hb = level_bounds(D, b)
        lo, hi = max(la, lb_), min(ha, hb)
        pts = [lo] + [p for p in splits[k] if lo < p < hi] + [hi]
        per_tank.append([(pts[j], pts[j + 1]) for j in range(len(pts) - 1)])
    return [list(bx) for bx in itertools.product(*per_tank)]


def period_box(D, t, bin_, bout):
    S = D["S"]
    box = {}
    if t > 0 and bin_ is not None:
        for k, (i, a, b) in enumerate(S["link"][t - 1]):
            box[b] = bin_[k]
    if t < D["T"] - 1 and bout is not None:
        for k, (i, a, b) in enumerate(S["link"][t]):
            box[a] = bout[k]
    return box


def _task(args):
    t, i, j, bin_, bout, lam, mu, mode, node_limit, time_limit, target = args
    D = _D
    box = period_box(D, t, bin_, bout)
    tic = time.time()
    if mode == "scip":
        try:
            r = period.solve_window(D, t, t + 1, lam, mu, 120, {} if os.environ.get("WATERNO2_SCIP") == "default" else bundle.NOPROP, box)
        except ValueError:
            return (t, i, j, np.inf, np.inf, "empty", 0.0)
        val = r["dual"] if r["status"] != "infeasible" else np.inf
        pr = r["primal"]
        return (t, i, j, val, pr, r["status"], time.time() - tic)
    W = rbb.Window(D, t, t + 1, box)
    if np.any(W.lo0 > W.hi0):
        return (t, i, j, np.inf, np.inf, "empty", 0.0)
    c = W.objective(lam, mu)
    obbt_vars = sorted({a for kind, args_ in W.auxdef for a in args_ if not W.isbin[a]})
    res = rbb.solve(W, c, target, node_limit=node_limit, time_limit=time_limit, obbt_vars=obbt_vars)
    return (t, i, j, res["bound"], target, res["status"], time.time() - tic)


def dp(T, boxes, phi, mu_c):
    """Shortest path; returns (value, path)."""
    f = {j: phi[(0, None, j)] for j in range(len(boxes[0]))}
    back = []
    for t in range(1, T - 1):
        g, bk = {}, {}
        for j in range(len(boxes[t])):
            best, arg = np.inf, None
            for i in range(len(boxes[t - 1])):
                v = f[i] + phi[(t, i, j)]
                if v < best:
                    best, arg = v, i
            g[j], bk[j] = best, arg
        f = g
        back.append(bk)
    best, arg = np.inf, None
    for i in range(len(boxes[T - 2])):
        v = f[i] + phi[(T - 1, i, None)]
        if v < best:
            best, arg = v, i
    path = [arg]
    for bk in reversed(back):
        path.append(bk[path[-1]])
    return mu_c + best, list(reversed(path))


def main():
    T = int(sys.argv[1])
    mult = json.load(open(sys.argv[2]))
    lam, mu = mult["lam"], mult["mu"]
    splits = [[float(p) for p in s.split(",") if p] for s in sys.argv[3].split(";")]
    mode = sys.argv[4]
    out = sys.argv[5]
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else 6
    node_limit = int(sys.argv[7]) if len(sys.argv) > 7 else 100000
    time_limit = float(sys.argv[8]) if len(sys.argv) > 8 else 1800.0
    targets = json.load(open(sys.argv[9])) if len(sys.argv) > 9 else None
    D = period.setup(T, os.environ.get("WATERNO2_IMPLIED"))
    boxes = [boxes_for_boundary(D, t, splits) for t in range(T - 1)]
    tasks = []
    for t in range(T):
        ins = [None] if t == 0 else list(range(len(boxes[t - 1])))
        outs = [None] if t == T - 1 else list(range(len(boxes[t])))
        for i in ins:
            for j in outs:
                key = f"{t},{i},{j}"
                tg = targets[key] if targets and key in targets else None
                tasks.append((t, i, j, None if i is None else boxes[t - 1][i],
                              None if j is None else boxes[t][j], lam, mu, mode, node_limit, time_limit, tg))
    tic = time.time()
    pool = mp.Pool(workers, initializer=_init, initargs=(T,))
    res = pool.map(_task, tasks, chunksize=1)
    pool.close()
    phi = {(r[0], r[1], r[2]): r[3] for r in res}
    mu_c = mu * float(D["hor_rhs"])
    val, path = dp(T, boxes, phi, mu_c)
    print(f"boxes per boundary: {[len(b) for b in boxes]}; subproblems {len(tasks)}; wall {time.time()-tic:.0f}s")
    print(f"DP bound ({mode}): {val:.6f}; path {path}")
    for t in range(T):
        i = None if t == 0 else path[t - 1]
        j = None if t == T - 1 else path[t]
        print(f"  period {t}: in {None if i is None else boxes[t-1][i]} out {None if j is None else boxes[t][j]} "
              f"phi {phi[(t, i, j)]:.6f}")
    json.dump(dict(T=T, splits=splits, mode=mode, boxes=boxes, bound=val, path=path,
                   results=[dict(t=r[0], i=r[1], j=r[2], value=r[3], primal_or_target=r[4], status=r[5],
                                 time=r[6]) for r in res],
                   lam=[[repr(v) for v in l] for l in lam], mu=repr(mu)), open(out, "w"), indent=0)


if __name__ == "__main__":
    main()
