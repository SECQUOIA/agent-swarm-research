"""Single-tree B&B on a path with the class bounds of robust_bb.Relax and two branching rules.

Rules (both split at the midpoint of the chosen coordinate):
  bisect : widest side, lowest index on ties (as in robust_bb.bb);
  spread : the coordinate with the largest weighted spread (variance) of its marginals in the last
           primal family of the node (the fooling family returned by the column generation), summed
           over the factors that contain it; ties and zero spread fall back to the widest side.
A box is pruned when the column-generation LOWER bound reaches f* - eps (as in robust_bb).
Floating-point illustration, not a certified count.
"""
import sys
import time
import json
import numpy as np
sys.path.insert(0, "..")
from robust_bb import Relax  # noqa: E402


def spread_scores(rel, n):
    pts, w = rel.last_primal
    score = np.zeros(n)
    col = 0
    for e in range(n - 1):
        P_e = pts[e]; m = len(P_e)
        we = np.maximum(w[col:col + m], 0.0); col += m
        s = we.sum()
        if s <= 0:
            continue
        for j, k in ((0, e), (1, e + 1)):
            mu = np.dot(we, P_e[:, j]) / s
            score[k] += np.dot(we, (P_e[:, j] - mu) ** 2) / s
    return score


def bb(fam, cls, eps, fstar, rule="bisect", base="balanced", maxnodes=400_000, K=5, timelimit=7200):
    n = fam.n
    rel = Relax(fam, cls, base, K)
    target = fstar - eps
    stack = [(np.full(n, -1.0), np.full(n, 1.0))]
    leaves = nodes = ambiguous = 0
    t0 = time.time()
    while stack:
        l, u = stack.pop()
        nodes += 1
        lo, up, _ = rel.bound(l, u, target)
        if lo >= target:
            leaves += 1
            continue
        if up >= target:
            ambiguous += 1
        width = u - l
        if rule == "spread" and hasattr(rel, "last_primal"):
            sc = spread_scores(rel, n) * (width > 1e-9)
            j = int(np.argmax(sc)) if sc.max() > 1e-14 else int(np.argmax(width))
        else:
            j = int(np.argmax(width))
        m = 0.5 * (l[j] + u[j])
        u1 = u.copy(); u1[j] = m
        l2 = l.copy(); l2[j] = m
        stack.append((l, u1)); stack.append((l2, u))
        if nodes > maxnodes or time.time() - t0 > timelimit:
            return dict(leaves=None, nodes=nodes, aborted=True, time=round(time.time() - t0, 1))
    return dict(leaves=leaves, nodes=nodes, ambiguous=ambiguous, lpfail=rel.failures, time=round(time.time() - t0, 1))
