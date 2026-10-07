"""W3 limits: exact checks for the revised Proposition lim:prop:setgrowth.

F(x) = sum_{i<n} (x_i - x_{i+1})^2 on [0,1]^n, L_1 = L_n = 2, L_i = 4 inside
(L = 2 for n = 2).

(a) For every grid of [0,1]^n and every node v of G_j:
    m_j(v) <= -(L_j/8) w_j(v)^2.  Checked on random rational grids, n = 2..4.
(b) Filtering with U >= OPT = 0 removes nothing (every interval has an
    endpoint min-marginal <= 0).
(c) The reviewer's two-stage certificate (n = 2, eps = 1/50) is valid, has a
    two-node last grid, and its removed stage-0 intervals have length
    <= 2 sqrt(eps), as part (c) requires.
"""
from fractions import Fraction as Fr
from itertools import product
import random


def curv(n):
    return [2, 2] if n == 2 else [2] + [4] * (n - 2) + [2]


def F(y):
    return sum((y[i] - y[i + 1]) ** 2 for i in range(len(y) - 1))


def widths(g):
    w = {}
    for k, v in enumerate(g):
        c = []
        if k > 0:
            c.append(v - g[k - 1])
        if k + 1 < len(g):
            c.append(g[k + 1] - v)
        w[v] = max(c)
    return w


def marginals(grids, L):
    n = len(grids)
    ws = [widths(g) for g in grids]
    m = [dict() for _ in range(n)]
    beta = None
    for y in product(*grids):
        q = F(y) - sum(Fr(L[i], 8) * ws[i][y[i]] ** 2 for i in range(n))
        beta = q if beta is None else min(beta, q)
        for i in range(n):
            if y[i] not in m[i] or q < m[i][y[i]]:
                m[i][y[i]] = q
    return beta, m, ws


def rand_grid(rng, maxnodes):
    k = rng.randint(0, maxnodes - 2)
    inner = sorted({Fr(rng.randint(1, 59), 60) for _ in range(k)})
    return [Fr(0)] + inner + [Fr(1)]


def check_a_b(trials=400, seed=1):
    rng = random.Random(seed)
    for _ in range(trials):
        n = rng.randint(2, 4)
        L = curv(n)
        grids = [rand_grid(rng, 6 if n < 4 else 4) for _ in range(n)]
        beta, m, ws = marginals(grids, L)
        for j in range(n):
            for v in grids[j]:
                assert m[j][v] <= -Fr(L[j], 8) * ws[j][v] ** 2, (grids, j, v)
            # (b): every grid interval is retained with U = 0
            for a, a2 in zip(grids[j], grids[j][1:]):
                assert min(m[j][a], m[j][a2]) <= 0
            W = max(b - a for a, b in zip(grids[j], grids[j][1:]))
            assert beta <= -Fr(L[j], 8) * W ** 2
    print(f"(a),(b): {trials} random grids, n=2..4: all min-marginal bounds hold")


def check_c():
    n, L = 2, curv(2)
    g0 = [[Fr(k, 5) for k in range(6)]] * n
    g1 = [[Fr(0), Fr(1, 5)]] * n
    beta0, m0, _ = marginals(g0, L)
    beta1, _, _ = marginals(g1, L)
    beta = beta1
    xhat = (Fr(0), Fr(0))
    eps = F(xhat) - beta
    assert eps == Fr(1, 50)
    removed = []
    for i in range(n):
        for a, b in zip(g0[i], g0[i][1:]):
            if not (b <= Fr(1, 5)):
                assert min(m0[i][a], m0[i][b]) >= beta  # (C1)
                removed.append(b - a)
    assert beta1 >= beta  # (C2)
    # part (c): removed stage-0 intervals have length <= 2 sqrt(eps)
    assert all(w * w <= 4 * eps for w in removed)
    print(f"(c): n=2, eps={eps}: certificate valid, last grid 2 nodes, "
          f"stage-0 beta={beta0}, removed interval lengths {sorted(set(removed))} "
          f"<= 2 sqrt(eps) = {2 * (1/50) ** 0.5:.4f}; filtering-run bound "
          f"1+1/(2 sqrt eps) = {1 + 1 / (2 * (1/50) ** 0.5):.3f}")


if __name__ == "__main__":
    check_a_b()
    check_c()
