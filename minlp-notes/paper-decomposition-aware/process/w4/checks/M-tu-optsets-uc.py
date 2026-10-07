"""Exact run of UC (Algorithm alg:uc) on the instance of prop:twocenters.

F_M = x^2 - 2xz + Mz on [0,M]^2, S = {(0,0),(M,M)}, g_S = 1/20, L = 2, r = 2.
Checks per stage: S inside the retained union, beta_j <= OPT, U - beta_j <=
(1/2) n L h_j^2, and node counts <= K_S = 12 r (2 sqrt(n kappa_S) + 1).
Also a mixed-integer variant with z integer.
"""
from fractions import Fraction as Fr
import math

def uc(M, eps, integer_z=False):
    n, L = 2, Fr(2)
    Ls = [Fr(2), Fr(0)]
    lo, hi = [Fr(0), Fr(0)], [Fr(M), Fr(M)]
    s = Fr(M)
    F = lambda x, z: x * x - 2 * x * z + M * z
    J = 0
    while Fr(1, 2) * n * L * s * s / 4 ** J > eps:
        J += 1
    cells = [[(lo[0], hi[0])], [(lo[1], hi[1])]]
    U = F(lo[0], lo[1])
    kS = 40
    KS = 12 * 2 * (2 * math.sqrt(n * kS) + 1)
    maxnodes = 0
    for j in range(J + 1):
        h = s / 2 ** j
        stage = []
        for i in range(2):
            isint = integer_z and i == 1
            pts = []
            sc = []
            for (a, a2) in cells[i]:
                if isint:
                    k0 = 0
                    cuts = sorted({lo[i] + math.ceil(k * h) for k in range(0, int(s / h) + 2)})
                else:
                    cuts = [lo[i] + k * h for k in range(0, int(s / h) + 2)]
                inner = [p for p in cuts if a < p < a2]
                bps = [a] + inner + [a2]
                sc += list(zip(bps, bps[1:]))
            stage.append(sc)
        G, w = [], []
        for i in range(2):
            isint = integer_z and i == 1
            nodes = sorted({p for c in stage[i] for p in c})
            wi = {}
            for (a, a2) in stage[i]:
                ew = Fr(0) if (isint and a2 - a == 1) else a2 - a
                for p in (a, a2):
                    wi[p] = max(wi.get(p, Fr(0)), ew)
            G.append(nodes); w.append(wi)
        maxnodes = max(maxnodes, len(G[0]), len(G[1]))
        Q = {(x, z): F(x, z) - Ls[0] / 8 * w[0][x] ** 2 - Ls[1] / 8 * w[1][z] ** 2 for x in G[0] for z in G[1]}
        beta = min(Q.values())
        y = min(Q, key=Q.get)
        if F(*y) < U:
            U = F(*y)
        assert beta <= 0, "beta > OPT"
        assert U - beta <= Fr(1, 2) * n * L * h * h, "gap bound"
        m0 = {x: min(Q[(x, z)] for z in G[1]) for x in G[0]}
        m1 = {z: min(Q[(x, z)] for x in G[0]) for z in G[1]}
        mm = [m0, m1]
        for i in range(2):
            cells[i] = [(a, a2) for (a, a2) in stage[i] if min(mm[i][a], mm[i][a2]) <= U]
            for v in (Fr(0), Fr(M)):
                assert any(a <= v <= a2 for (a, a2) in cells[i]), "minimizer removed"
    assert maxnodes <= KS
    return J, maxnodes, U, beta, KS

for M in (8, 64, 1024):
    for q in (4, 10, 16):
        for iz in (False, True):
            J, mx, U, beta, KS = uc(M, Fr(1, 2 ** q), iz)
            print("M=%5d eps=2^-%2d int_z=%d: stages %2d, max nodes %3d (K_S=%.0f), U=%s, beta=%.3g"
                  % (M, q, iz, J + 1, mx, KS, U, float(beta)))
print("ALL PASS")
