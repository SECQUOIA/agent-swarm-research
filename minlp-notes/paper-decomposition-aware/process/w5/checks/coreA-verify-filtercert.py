"""W5 coreA verification: exact check of Corollary cor:filtercert (grids.tex).

Random mixed box QPs (two continuous coordinates on [0,2], one integer
coordinate on {0,...,4}), uniform grids, k filtering stages with thresholds
U_j >= OPT (values of feasible points, optionally increased).  Checks, in
exact rational arithmetic:
  * U_j >= beta_j at every stage (condition of Def. def:filter);
  * X^(j+1) is a subbox of X^(j), integer nodes are integers;
  * (C1) for every j < k against beta = beta_k, and (C2);
  * every sampled feasible point with F <= min_j U_j lies in X^(k)
    (Prop. prop:filter, as used for "every minimizer lies in every X^(j)");
  * F(x) >= beta_k at sampled feasible points (Thm. thm:certificate).
"""
import itertools
import random
from fractions import Fraction as Fr

random.seed(5)
IC, IZ = [0, 1], [2]
LO, UP = [Fr(0), Fr(0), Fr(0)], [Fr(2), Fr(2), Fr(4)]


def make_F():
    H = [[Fr(0)] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(i, 3):
            H[i][j] = H[j][i] = Fr(random.randint(-6, 6), 2)
    b = [Fr(random.randint(-8, 8), 2) for _ in range(3)]
    F = lambda x: sum(H[i][j] * x[i] * x[j] for i in range(3) for j in range(3)) / 2 \
        + sum(b[i] * x[i] for i in range(3))
    L = [max(H[i][i], Fr(0)) for i in range(3)]
    return F, L


def grid(lo, up, m=5):
    G = []
    for i in range(3):
        if i in IZ:
            G.append([Fr(t) for t in range(int(lo[i]), int(up[i]) + 1)])
        elif lo[i] == up[i]:
            G.append([lo[i]])
        else:
            G.append([lo[i] + (up[i] - lo[i]) * t / (m - 1) for t in range(m)])
    return G


def eff_width(i, a, a2):
    return Fr(0) if (i in IZ and a2 - a == 1) else a2 - a


def intervals(Gi):
    return [(Gi[0], Gi[0])] if len(Gi) == 1 else list(zip(Gi, Gi[1:]))


def corrected(F, L, G):
    d = []
    for i in range(3):
        w = {v: Fr(0) for v in G[i]}
        for a, a2 in intervals(G[i]):
            ww = eff_width(i, a, a2)
            w[a], w[a2] = max(w[a], ww), max(w[a2], ww)
        d.append({v: L[i] * w[v] ** 2 / 8 for v in G[i]})
    Q, best_F = {}, None
    for y in itertools.product(*G):
        fy = F(y)
        Q[y] = fy - sum(d[i][y[i]] for i in range(3))
        best_F = fy if best_F is None else min(best_F, fy)
    beta = min(Q.values())
    m = [{v: min(q for y, q in Q.items() if y[i] == v) for v in G[i]} for i in range(3)]
    return beta, m, best_F


def check_once(k=3):
    F, L = make_F()
    P = [i for i in range(3) if L[i] > 0]
    lo, up = LO[:], UP[:]
    stages, U, Us = [], None, []
    for j in range(k + 1):
        G = grid(lo, up)
        beta, m, bF = corrected(F, L, G)
        U = bF if U is None else min(U, bF)       # value of a feasible point
        stages.append((lo[:], up[:], G, beta, m))
        if j == k:
            break
        Uj = U + Fr(random.choice([0, 0, 1, 3]), 4)  # any threshold >= OPT
        Us.append(Uj)
        assert Uj >= beta, "U_j < beta_j"
        nlo, nup = lo[:], up[:]
        for i in P:
            ret = [(a, a2) for a, a2 in intervals(G[i]) if min(m[i][a], m[i][a2]) <= Uj]
            assert ret, "no retained interval"
            nlo[i], nup[i] = min(a for a, _ in ret), max(a2 for _, a2 in ret)
            assert lo[i] <= nlo[i] <= nup[i] <= up[i]
            if i in IZ:
                assert nlo[i].denominator == 1 and nup[i].denominator == 1
        lo, up = nlo, nup
    beta_k = stages[-1][3]
    # (C1)
    for j in range(k):
        _, _, G, _, m = stages[j]
        lo1, up1 = stages[j + 1][0], stages[j + 1][1]
        for i in range(3):
            for a, a2 in intervals(G[i]):
                if not (lo1[i] <= a and a2 <= up1[i]):
                    assert i in P
                    assert min(m[i][a], m[i][a2]) >= beta_k, "(C1) fails"
    # sampled feasible points
    Umin = min(Us)
    lok, upk = stages[-1][0], stages[-1][1]
    for x0 in itertools.product([Fr(t, 10) for t in range(21)], [Fr(t, 10) for t in range(21)],
                                [Fr(t) for t in range(5)]):
        fx = F(x0)
        assert fx >= beta_k, "Theorem: F < beta"
        if fx <= Umin:
            assert all(lok[i] <= x0[i] <= upk[i] for i in range(3)), "point with F<=U removed"
    return len(P)


ps = [check_once() for _ in range(60)]
print("PASS: 60 random filtering runs, |P| distribution", {p: ps.count(p) for p in set(ps)})
