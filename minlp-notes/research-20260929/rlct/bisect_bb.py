"""Uniform 2^n-ary dyadic bisection B&B with exact alphaBB node bounds.

Node relaxation on a box B = [l, u]:  f_B = m - alpha q_B,
q_B(y) = sum_i (y_i - l_i)(u_i - y_i).  This satisfies (G^pt_alpha) and
(U^q_alpha) with equality.  The incumbent is fixed at f* = 0 and a box is
pruned iff LB(B) = min_B f_B >= -eps.  The tree is the uniform refinement
T_bis of the note (children of every non-pruned cube are processed), so
|T_bis| = 1 + 2^n #(non-pruned cubes).

LB(B) is a convex problem (alpha >= alpha0).  It is solved in batch by
accelerated projected gradient.  Decisions use two valid bounds:
  upper:  min over iterates of f_B(x)            (>= LB)
  lower:  f_B(x) + sum_i min(g_i (l_i - x_i), g_i (u_i - x_i))   (<= LB),
the second by convexity (Frank-Wolfe gap).  A box is pruned when the lower
bound is >= -eps and kept when the upper bound is < -eps.  Boxes still
undecided after the iteration budget are counted separately and treated
as non-pruned.  Floating point; an illustration, not a certified count.

Usage: python3 bisect_bb.py INSTANCE EPS [ALPHA]
Prints one JSON line.
"""
import json
import sys
import time

import numpy as np

import instances


def node_bounds(fun, l, u, alpha, L, eps, max_iter=3000, chunk=25):
    """Return (decided_prune, decided_keep, undecided) boolean arrays."""
    N, n = l.shape
    x = 0.5 * (l + u)
    y = x.copy()
    tk = np.ones(N)
    best = np.full(N, np.inf)
    prune = np.zeros(N, bool)
    keep = np.zeros(N, bool)
    active = np.arange(N)
    it = 0
    while active.size and it < max_iter:
        la, ua = l[active], u[active]
        xa, ya, ta = x[active], y[active], tk[active]
        fprev = np.full(active.size, np.inf)
        for _ in range(chunk):
            _, g = fun(ya)
            g = g + alpha * (2 * ya - la - ua)
            xn = np.clip(ya - g / L, la, ua)
            v, _ = fun(xn)
            fv = v - alpha * np.sum((xn - la) * (ua - xn), axis=1)
            # function-value restart of the momentum
            restart = fv > fprev
            tn = 0.5 * (1 + np.sqrt(1 + 4 * ta * ta))
            mom = ((ta - 1) / tn)[:, None]
            ya = np.where(restart[:, None], xn, xn + mom * (xn - xa))
            ta = np.where(restart, 1.0, tn)
            xa = xn
            fprev = fv
        it += chunk
        v, g = fun(xa)
        g = g + alpha * (2 * xa - la - ua)
        fv = v - alpha * np.sum((xa - la) * (ua - xa), axis=1)
        lb = fv + np.sum(np.minimum(g * (la - xa), g * (ua - xa)), axis=1)
        b = np.minimum(best[active], fv)
        best[active] = b
        pr = lb >= -eps
        kp = (~pr) & (b < -eps)
        prune[active[pr]] = True
        keep[active[kp]] = True
        x[active], y[active], tk[active] = xa, ya, ta
        active = active[~(pr | kp)]
    und = np.zeros(N, bool)
    und[active] = True
    return prune, keep, und


def run(name, eps, alpha=None, max_level=60):
    d = instances.get(name, alpha)
    fun, n, lo, s0, alpha = d["fun"], d["n"], d["lo"], d["side"], d["alpha"]
    L = d["hmax"] + 2 * alpha
    corners = lo[None, :].copy()          # lower corners of level-j cubes
    offsets = np.array(np.meshgrid(*[[0, 1]] * n, indexing="ij")).reshape(n, -1).T
    nonpruned_per_level = []
    undecided_total = 0
    t0 = time.time()
    s = s0
    for j in range(max_level):
        if corners.shape[0] == 0:
            break
        l = corners
        u = corners + s
        keep_all = np.zeros(l.shape[0], bool)
        B = 200000
        for a in range(0, l.shape[0], B):
            pr, kp, und = node_bounds(fun, l[a:a + B], u[a:a + B], alpha, L, eps)
            keep_all[a:a + B] = kp | und
            undecided_total += int(und.sum())
        kept = l[keep_all]
        nonpruned_per_level.append(int(kept.shape[0]))
        s = s / 2
        corners = (kept[:, None, :] + s * offsets[None, :, :]).reshape(-1, n)
    nonpruned = sum(nonpruned_per_level)
    nodes = 1 + (2 ** n) * nonpruned
    leaves = nodes - nonpruned
    return dict(instance=name, eps=eps, alpha=alpha, n=n, nodes=nodes,
                leaves=leaves, nonpruned_per_level=nonpruned_per_level,
                undecided=undecided_total, seconds=round(time.time() - t0, 2))


if __name__ == "__main__":
    name = sys.argv[1]
    eps = float(sys.argv[2])
    alpha = float(sys.argv[3]) if len(sys.argv) > 3 else None
    print(json.dumps(run(name, eps, alpha)), flush=True)
