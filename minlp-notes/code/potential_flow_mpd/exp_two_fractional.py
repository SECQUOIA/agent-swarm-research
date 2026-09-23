"""Experiment 1: drop across a cycle when load moves between two nodes on
opposite a-c paths.

Setting.  Cycle with nodes 0..k-1, a = 0, c = h (h = k//2).  P1 = nodes
1..h-1 (one side), P2 = nodes h+1..k-1 (other side).  Loads: b_a = t > 0
(through-flow entering at a), fixed loads at all other nodes, except a
fractional pair p in P1, q in P2 with b_p = s, b_q = S - s; c absorbs the
remainder.  g(s) = pi_a - pi_c.

By the KKT analysis in the note, every node on P1 above p is at its upper
bound (injection >= 0) and below p at its lower bound (withdrawal <= 0),
same on P2 w.r.t. q.  We sample such sign patterns ("kkt" mode) and also
completely random fixed loads ("random" mode), and count interior local
maxima of g on a fine grid.
"""

from __future__ import annotations

import sys
import numpy as np
from pbflow import cycle_graph, solve_flow


def drop_function(k, h, p, q, fixed, t, S, r, betas=None, ngrid=401, smin=None, smax=None):
    G = cycle_graph(k, betas)
    if smin is None:
        smin, smax = min(0.0, S), max(0.0, S)
    ss = np.linspace(smin, smax, ngrid)
    g = np.empty(ngrid)
    for i, s in enumerate(ss):
        b = fixed.copy()
        b[0] = t
        b[p] = s
        b[q] = S - s
        b[h] = -(b.sum() - b[h])
        x, pi = solve_flow(G, b, r)
        g[i] = pi[0] - pi[h]
    return ss, g


def interior_local_maxima(g, tol=1e-12):
    idx = []
    for i in range(1, len(g) - 1):
        if g[i] > g[i - 1] + tol and g[i] > g[i + 1] + tol:
            idx.append(i)
    return idx


def main(mode="kkt", trials=2000, r=2.0, seed=0):
    rng = np.random.default_rng(seed)
    n_interior = 0
    n_nonmono_deriv = 0
    worst = None
    for tr in range(trials):
        k = int(rng.integers(4, 9))
        h = k // 2
        P1 = list(range(1, h))
        P2 = list(range(h + 1, k))
        if not P1 or not P2:
            continue
        p = int(rng.choice(P1))
        q = int(rng.choice(P2))
        fixed = np.zeros(k)
        scale = 1.0
        if mode == "kkt":
            for v in P1:
                fixed[v] = rng.uniform(0, scale) if v < p else -rng.uniform(0, scale)
            for v in P2:
                # on P2 nodes closer to a have larger index
                fixed[v] = rng.uniform(0, scale) if v > q else -rng.uniform(0, scale)
        else:
            for v in P1 + P2:
                fixed[v] = rng.uniform(-scale, scale)
        t = rng.uniform(0, 2 * scale)
        S = rng.uniform(-2 * scale, 2 * scale)
        betas = rng.uniform(0.2, 3.0, size=k)
        ss, g = drop_function(k, h, p, q, fixed, t, S, r, betas)
        lm = interior_local_maxima(g)
        if lm:
            n_interior += 1
            if worst is None or len(lm) > worst[0]:
                worst = (len(lm), k, h, p, q, fixed.copy(), t, S, betas.copy(), ss[lm], g[lm], g[0], g[-1])
        d = np.diff(g)
        # count sign changes of derivative (quasi-convex => at most one, - to +)
        signs = np.sign(d[np.abs(d) > 1e-12])
        changes = int(np.sum(signs[1:] != signs[:-1]))
        if changes > 1 or (changes == 1 and signs[0] > 0):
            n_nonmono_deriv += 1
    print(f"mode={mode} r={r} trials={trials}: instances with interior local max = {n_interior}, "
          f"instances not quasi-convex (derivative pattern) = {n_nonmono_deriv}")
    if worst is not None:
        print("example:", worst)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "kkt"
    r = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    trials = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
    main(mode, trials, r)
