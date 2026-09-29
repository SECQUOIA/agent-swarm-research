"""Prop 12 check: layered 3SAT/2SAT embedding with a time axis, Euclidean lengths.
Unsatisfiable 2-CNF on N=2 variables, m=4 clauses; satisfiable subformula (first 3 clauses).
Reports OPT vs (m+1)L, the note's bounds, the max edge aperture, whether same-layer sets
intersect (the note says 'pairwise-disjoint polytopes'), and REL / REL_H."""
import itertools
import numpy as np
import cvxpy as cp
from rgcs import *


def literal_set(N, k, a, h):
    lo = np.r_[np.zeros(N), h]; hi = np.r_[np.ones(N), h]
    lo[k] = a; hi[k] = a
    return Box(lo, hi)


def build(clauses, N, L):
    m = len(clauses)
    sets = {"s": Box(np.r_[np.zeros(N), 0.0], np.r_[np.ones(N), 0.0]),
            "t": Box(np.r_[np.zeros(N), (m + 1) * L], np.r_[np.ones(N), (m + 1) * L])}
    layers = [["s"]]
    for i, cl in enumerate(clauses, start=1):
        Ls = []
        for j, (k, a) in enumerate(cl):
            name = f"c{i}_{j}"
            sets[name] = literal_set(N, k, a, i * L)
            Ls.append(name)
        layers.append(Ls)
    layers.append(["t"])
    E = [(u, v) for A, B in zip(layers[:-1], layers[1:]) for u in A for v in B]
    return G(sets, E, "s", "t", L2), layers


def max_sec(g):
    worst = 1.0
    for (u, v) in g.E:
        D = np.array([b - a for a in g.sets[u].V for b in g.sets[v].V])
        U = D / np.linalg.norm(D, axis=1, keepdims=True)
        a = cp.Variable(D.shape[1]); t = cp.Variable()
        cp.Problem(cp.Maximize(t), [U @ a >= t, cp.norm(a, 2) <= 1]).solve(solver="CLARABEL")
        worst = max(worst, 1 / t.value)
    return worst


unsat = [[(0, 1), (1, 1)], [(0, 1), (1, 0)], [(0, 0), (1, 1)], [(0, 0), (1, 0)]]
N = 2
for th_deg in [30, 10, 3]:
    th = np.radians(th_deg)
    L = np.sqrt(N) / np.tan(th)
    for name, cls in [("unsat m=4", unsat), ("sat m=3", unsat[:3])]:
        m = len(cls)
        g, layers = build(cls, N, L)
        o = opt(g)
        base = (m + 1) * L
        lb_note = base + 1 / (2 * m * L + 1)
        ratio_lb = 1 + np.tan(th) ** 2 / (3 * N * (m + 1) ** 2)
        rl, rh = relax(g), relax(g, hull=True)
        print(f"theta={th_deg:2d} {name}: OPT={o:.8f} (m+1)L={base:.8f} OPT-(m+1)L={o-base:.3e} "
              f"note LB (unsat)={lb_note-base:.3e}  OPT/((m+1)L)={o/base:.8f} ratio LB={ratio_lb:.8f} "
              f"REL={rl:.8f} REL_H={rh:.8f} sec(theta_max)={max_sec(g):.6f} (sec th={1/np.cos(th):.6f})")
# same-layer intersection check
g, layers = build(unsat, N, 1.0)
A, B = g.sets["c1_0"], g.sets["c1_1"]
lo = np.maximum(A.V.min(0), B.V.min(0)); hi = np.minimum(A.V.max(0), B.V.max(0))
print("layer-1 literal sets (x1=1) and (x2=1) intersect:", bool(np.all(lo <= hi)), "intersection box:", lo, hi)
