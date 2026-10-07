"""Independent exact checks for Prop. lim:prop:setgrowth (verifier, W3).

F(x) = sum_{i<n} (x_i - x_{i+1})^2 on [0,1]^n, L = (2,4,...,4,2) (n>=3), (2,2) (n=2).
(a) m_j(v) <= -(L_j/8) w_j(v)^2 for every node of random grids of X (brute force).
(c) random two-stage path certificates with the largest valid beta:
    every stage-0 interval not contained in X^(1)_i has length <= 2 sqrt(eps),
    where eps = F(xhat) - beta and xhat is the best grid point seen.
    For k = 0: every stage-0 interval has length <= 2 sqrt(eps).
"""
import itertools
import random
from fractions import Fraction as Fr

random.seed(20261003)


def F(x):
    return sum((x[i] - x[i + 1]) ** 2 for i in range(len(x) - 1))


def Ls(n):
    return [Fr(2)] * 2 if n == 2 else [Fr(2)] + [Fr(4)] * (n - 2) + [Fr(2)]


def widths(g):
    w = {}
    for k, v in enumerate(g):
        cand = []
        if k > 0:
            cand.append(v - g[k - 1])
        if k + 1 < len(g):
            cand.append(g[k + 1] - v)
        w[v] = max(cand) if cand else Fr(0)
    return w


def tables(G, L):
    n = len(G)
    W = [widths(g) for g in G]
    m = [{v: None for v in g} for g in G]
    beta = None
    for y in itertools.product(*G):
        q = F(y) - sum(L[i] / 8 * W[i][y[i]] ** 2 for i in range(n))
        beta = q if beta is None else min(beta, q)
        for i in range(n):
            if m[i][y[i]] is None or q < m[i][y[i]]:
                m[i][y[i]] = q
    return W, m, beta


def rand_grid(lo, hi, k):
    pts = {lo, hi}
    while len(pts) < k:
        pts.add(lo + (hi - lo) * Fr(random.randint(1, 59), 60))
    return sorted(pts)


def check_a(trials=150):
    for _ in range(trials):
        n = random.choice([2, 3, 4])
        L = Ls(n)
        G = [rand_grid(Fr(0), Fr(1), random.randint(2, 5 if n < 4 else 4)) for _ in range(n)]
        W, m, beta = tables(G, L)
        for j in range(n):
            for v in G[j]:
                assert m[j][v] <= -L[j] / 8 * W[j][v] ** 2, (G, j, v)
            Wj = max(b - a for a, b in zip(G[j], G[j][1:]))
            assert beta <= -L[j] / 8 * Wj ** 2
    print(f"(a): {trials} random grids of X, n=2..4: m_j(v) <= -(L_j/8) w_j(v)^2 OK")


def check_c(trials=150):
    for _ in range(trials):
        n = random.choice([2, 3])
        L = Ls(n)
        G0 = [rand_grid(Fr(0), Fr(1), random.randint(2, 6)) for _ in range(n)]
        W0, m0, beta0 = tables(G0, L)
        best = min(F(y) for y in itertools.product(*G0))
        if random.random() < 0.25:
            # k = 0: beta = corrected minimum of G0
            beta = beta0
            eps = best - beta
            for i in range(n):
                for a, b in zip(G0[i], G0[i][1:]):
                    assert (b - a) ** 2 <= 4 * eps
            continue
        # stage 1: random subbox spanned by nodes of G0, random grid on it
        box = []
        for i in range(n):
            a, b = sorted(random.sample(G0[i], 2))
            box.append((a, b))
        G1 = [rand_grid(a, b, random.randint(2, 4)) for a, b in box]
        W1, m1, beta1 = tables(G1, L)
        best = min(best, min(F(y) for y in itertools.product(*G1)))
        removed = []
        cands = [beta1]
        for i in range(n):
            for a, b in zip(G0[i], G0[i][1:]):
                if not (box[i][0] <= a and b <= box[i][1]):
                    removed.append(b - a)
                    cands.append(min(m0[i][a], m0[i][b]))
        beta = min(cands)  # largest beta for which (C1),(C2) hold
        eps = best - beta
        for gam in removed:
            assert gam ** 2 <= 4 * eps, (gam, eps)
    print(f"(c): {trials} random certificates (k=0 or 1), n=2,3: removed stage-0 intervals <= 2 sqrt(eps) OK")


def check_example():
    n, L = 2, Ls(2)
    G0 = [[Fr(k, 5) for k in range(6)]] * 2
    W0, m0, beta0 = tables(G0, L)
    assert all(m0[i][v] == Fr(-1, 50) for i in range(2) for v in G0[i])
    G1 = [[Fr(0), Fr(1, 5)]] * 2
    _, _, beta1 = tables(G1, L)
    assert beta1 == Fr(-1, 50) and F((0, 0)) - Fr(-1, 50) == Fr(1, 50)
    print("example n=2, eps=1/50: stage-0 min-marginals -1/50, last grid 2 nodes, gap 1/50 OK")


def check_misc():
    import math
    # (1 + log2 k)^2 <= 4 k for k >= 1 (used in app:lbproduct)
    for t in [x / 100 for x in range(0, 4000)]:
        assert (1 + t) ** 2 <= 4 * 2 ** t
    # kappa_S <= 2 n (n-1) with L = max L_i and g_S = 2/(n(n-1))
    for n in range(2, 30):
        assert max(Ls(n)) / Fr(2, n * (n - 1)) <= 2 * n * (n - 1)
    print("misc: (1+log2 k)^2 <= 4k on [1, 2^40]; kappa_S <= 2n(n-1) OK")


if __name__ == "__main__":
    check_a()
    check_c()
    check_example()
    check_misc()
