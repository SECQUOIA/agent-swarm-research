"""Verifier check (W3, optsets) for Algorithm UC, Lemma lem:cells and
Theorem thm:cells on small instances, including an integer coordinate.

UC as in optsets.tex: meshes h_j = s 2^-j, mesh points ell_i + k h_j (continuous)
or ell_i + ceil(k h_j) (integer), stage cells = retained cells split at mesh
points, G_i = endpoints, w_i(v) = largest effective width of a stage cell with
endpoint v (integer cells of length 1 have width 0), Q = F - D, beta_j, y^(j),
min-marginals m_i by enumeration, filter: keep stage cells with
min{m_i(a), m_i(a')} <= U, no hulls.

Checked at every stage: beta_j <= OPT; every optimizer stays in X_j; every
retained cell has an endpoint within sqrt(n kappa_S) h_j of S_i (the step of
the count in the proof of thm:cells); node counts <= K_S; the final gap
U - beta_J <= eps.

Instances:
  A. F_M of prop:twocenters, M = 8, X = [0,8]^2 continuous; g_S = 1/20, L = 2.
  B. F = (x-z)^2 + (z-1)(z-2), x in [0,4] continuous, z in {0,...,3} integer;
     S = {(1,1),(2,2)}; L = (2,4); g_S = 3/5 (exact minimum of F/dist^2 over
     the four integer slices, attained at (4,3)).
Run: python3 -B optsets-verify-uc.py
"""
from fractions import Fraction as Fr
from math import ceil, sqrt, floor
import itertools

def run_uc(F, Ls, lo, hi, isint, S, gS, eps):
    n = len(lo); L = max(Ls); s = max(hi[i] - lo[i] for i in range(n))
    OPT = min(F(x) for x in S)
    kS = max(1, L / gS)
    r = max(len({x[i] for x in S}) for i in range(n))
    KS = 12 * r * (2 * sqrt(n * kS) + 1)
    J = 0
    while Fr(1, 2) * n * L * s * s / 4 ** J > eps:
        J += 1
    cells = [[(lo[i], hi[i])] for i in range(n)]
    U = F(tuple(lo)); ok = True; maxnodes = 0
    for j in range(J + 1):
        h = s / 2 ** j
        stage = []
        for i in range(n):
            pts = set()
            k = 0
            while True:
                v = lo[i] + (ceil(k * h) if isint[i] else k * h)
                if v >= hi[i]:
                    break
                pts.add(Fr(v)); k += 1
            sc = []
            for (a, b) in cells[i]:
                cut = sorted([a] + [v for v in pts if a < v < b] + [b])
                sc += [(cut[t], cut[t + 1]) for t in range(len(cut) - 1)]
            stage.append(sc)
        # optimizers stay in the domain X_j
        for x in S:
            ok &= all(any(a <= x[i] <= b for (a, b) in stage[i]) for i in range(n))
        G = [sorted({e for c in stage[i] for e in c}) for i in range(n)]
        maxnodes = max(maxnodes, max(len(g) for g in G))
        ok &= max(len(g) for g in G) <= KS
        d = []
        for i in range(n):
            di = {}
            for v in G[i]:
                w = 0
                for (a, b) in stage[i]:
                    if v in (a, b):
                        ew = 0 if (isint[i] and b - a == 1) else b - a
                        w = max(w, ew)
                di[v] = Ls[i] * w * w / 8
            d.append(di)
        Q = {y: F(y) - sum(d[i][y[i]] for i in range(n)) for y in itertools.product(*G)}
        beta = min(Q.values())
        ok &= beta <= OPT
        y = min(Q, key=Q.get)
        if F(y) < U:
            U = F(y)
        ok &= U - beta <= Fr(1, 2) * n * L * h * h
        m = [{v: min(q for yy, q in Q.items() if yy[i] == v) for v in G[i]} for i in range(n)]
        rad = sqrt(n * kS) * h
        new = []
        for i in range(n):
            keep = [(a, b) for (a, b) in stage[i] if min(m[i][a], m[i][b]) <= U]
            for (a, b) in keep:  # count step: some endpoint near S_i
                near = any(m[i][v] <= U and min(abs(float(v - x[i])) for x in S) <= rad + 1e-12 for v in (a, b))
                ok &= near
            new.append(keep)
        cells = new
    ok &= U - beta <= eps
    return ok, J, maxnodes, KS

okall = True
M = Fr(8)
FA = lambda v: v[0] ** 2 - 2 * v[0] * v[1] + M * v[1]
res = run_uc(FA, [Fr(2), Fr(0)], [Fr(0)] * 2, [M] * 2, [False, False], [(Fr(0), Fr(0)), (M, M)], Fr(1, 20), Fr(1, 2 ** 10))
print("A. F_8:", "ok" if res[0] else "FAIL", "stages", res[1] + 1, "max nodes", res[2], "K_S", round(res[3], 1))
okall &= res[0]
FB = lambda v: (v[0] - v[1]) ** 2 + (v[1] - 1) * (v[1] - 2)
# g_S = 3/5: exact check of F/dist^2 >= 3/5 on a fine grid of each slice
SB = [(Fr(1), Fr(1)), (Fr(2), Fr(2))]
for z in range(4):
    for a in range(0, 4 * 64 + 1):
        x = Fr(a, 64); pt = (x, Fr(z))
        dd = min((x - s0) ** 2 + (z - s1) ** 2 for (s0, s1) in SB)
        if dd > 0:
            okall &= FB(pt) / dd >= Fr(3, 5)
okall &= FB((Fr(4), Fr(3))) / min((4 - s0) ** 2 + (3 - s1) ** 2 for (s0, s1) in SB) == Fr(3, 5)
res = run_uc(FB, [Fr(2), Fr(4)], [Fr(0)] * 2, [Fr(4), Fr(3)], [False, True], SB, Fr(3, 5), Fr(1, 2 ** 10))
print("B. mixed:", "ok" if res[0] else "FAIL", "stages", res[1] + 1, "max nodes", res[2], "K_S", round(res[3], 1))
okall &= res[0]
print("ALL PASS" if okall else "FAIL")
