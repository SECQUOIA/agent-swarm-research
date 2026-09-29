"""T9: sanity check of the layered SAT embedding of Prop. 12 (revised: staggered heights).

CNF with N variables and m clauses -> GCS in R^{N+1}.  Let L0 = sqrt(N)/tan(theta),
eta = 0.1*L0/3 and L = L0 + 3*eta = 1.1*L0.  X_s = [0,1]^N x {0}, X_t = [0,1]^N x {(m+1)L};
literal j (j = 1..3) of clause i has set {x in [0,1]^N : x_k = a} x {iL + j*eta}, so all sets
are pairwise disjoint; consecutive layers are fully connected; Euclidean lengths.
Vertical displacements are >= L - 3 eta = L0, so every aperture is <= theta.
Satisfiable:   OPT = (m+1)L.
Unsatisfiable: OPT >= (m+1)L + 1/(2mL+1), ratio >= 1 + 1/(3(m+1)^2 L^2) >= 1 + tan^2/(4N(m+1)^2).
Usage: python3 t9_hardness.py
"""
import itertools
import numpy as np
from gcslib import *


def embed(clauses, N, theta):
    L0 = np.sqrt(N) / np.tan(theta)
    eta = 0.1 * L0 / 3
    L = L0 + 3 * eta
    m = len(clauses)
    sets = {"s": box(np.r_[np.zeros(N), 0.0], np.r_[np.ones(N), 0.0]),
            "t": box(np.r_[np.zeros(N), (m + 1) * L], np.r_[np.ones(N), (m + 1) * L])}
    layers = []
    for i, cl in enumerate(clauses, start=1):
        lay = []
        for j, (k, a) in enumerate(cl, start=1):
            h = i * L + j * eta
            lo, hi = np.r_[np.zeros(N), h], np.r_[np.ones(N), h]
            lo[k] = hi[k] = a
            sets[(i, j)] = box(lo, hi)
            lay.append((i, j))
        layers.append(lay)
    E = [("s", v) for v in layers[0]] + [(v, "t") for v in layers[-1]]
    for A, B in zip(layers, layers[1:]):
        E += [(u, v) for u in A for v in B]
    return GCS(sets, E, "s", "t", L2), L


def disjoint(S1, S2):
    return np.any(S1.hi < S2.lo - 1e-12) or np.any(S2.hi < S1.lo - 1e-12)


N = 2
unsat = [[(0, 1), (1, 1)], [(0, 1), (1, 0)], [(0, 0), (1, 1)], [(0, 0), (1, 0)]]
sat = unsat[:3]
for theta_deg in [30, 10, 3]:
    th = np.radians(theta_deg)
    for name, cls in [("sat", sat), ("unsat", unsat)]:
        g, L = embed(cls, N, th)
        m = len(cls)
        alldisj = all(disjoint(g.sets[a], g.sets[b]) for a, b in itertools.combinations(g.V, 2))
        km = max(kappa_l2(g.sets[u], g.sets[v]) for u, v in g.edges)
        o = opt(g)
        rh = relax(g, hull=True)
        lb = (m + 1) * L + 1 / (2 * m * L + 1)
        print(f"theta<={theta_deg:2d}deg {name:5s}: m={m} L={L:.4f} pairwise disjoint={alldisj} kappa_max={km:.5f} "
              f"(sec={1/np.cos(th):.5f}) OPT={o:.6f} (m+1)L={(m+1)*L:.6f} UNSAT-lower-bound={lb:.6f} REL_H={rh:.6f} "
              f"OPT/((m+1)L)-1={o/((m+1)*L)-1:.3e} tan^2/(4N(m+1)^2)={np.tan(th)**2/(4*N*(m+1)**2):.3e}")
