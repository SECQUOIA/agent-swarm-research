"""R4: exact check that a valid path certificate (Definition def:cert) for the
set-growth example F = sum (x_i - x_{i+1})^2 can have a two-node last-stage
grid, contradicting the literal claim of Proposition lim:prop:setgrowth
("every corrected-grid certificate of accuracy eps ... has a last-stage grid
with at least 1 + 1/(2 sqrt(eps)) nodes in every coordinate").

Stage 0: uniform grid of spacing w on [0,1]^n.  Stage 1: box [0,delta]^n with
grid {0,delta}.  Curvatures L_i = max(0, H_ii).  We check (C1), (C2), the gap,
and compare the last-stage node count with the claimed lower bound.
"""
from fractions import Fraction as Fr
from itertools import product
import math


def curvatures(n):
    if n == 2:
        return [2, 2]
    return [2] + [4] * (n - 2) + [2]


def F(y):
    return sum((y[i] - y[i + 1]) ** 2 for i in range(len(y) - 1))


def corrections(grid, L):
    # d_i(v) = L/8 * (largest adjacent interval width)^2 for a continuous coordinate
    d = {}
    for k, v in enumerate(grid):
        widths = []
        if k > 0:
            widths.append(v - grid[k - 1])
        if k + 1 < len(grid):
            widths.append(grid[k + 1] - v)
        d[v] = Fr(L, 8) * max(widths) ** 2
    return d


def min_marginals(grids, L):
    n = len(grids)
    ds = [corrections(grids[i], L[i]) for i in range(n)]
    m = [dict() for _ in range(n)]
    beta = None
    for y in product(*grids):
        q = F(y) - sum(ds[i][y[i]] for i in range(n))
        beta = q if beta is None else min(beta, q)
        for i in range(n):
            if y[i] not in m[i] or q < m[i][y[i]]:
                m[i][y[i]] = q
    return beta, m


def run(n, K):
    L = curvatures(n)
    w = Fr(1, K)
    delta = w
    g0 = [[Fr(k, K) for k in range(K + 1)]] * n
    g1 = [[Fr(0), delta]] * n
    beta0, m0 = min_marginals(g0, L)
    beta1, _ = min_marginals(g1, L)
    beta = beta1  # certificate bound = corrected minimum of the last grid (C2 holds with equality)
    # (C1): every stage-0 interval not contained in [0, delta] has min endpoint marginal >= beta
    ok_c1 = True
    for i in range(n):
        gi = g0[i]
        for a, b in zip(gi, gi[1:]):
            if not (a >= 0 and b <= delta):
                if min(m0[i][a], m0[i][b]) < beta:
                    ok_c1 = False
    xhat = (Fr(0),) * n
    gap = F(xhat) - beta
    eps = gap
    claimed = 1 + 1 / (2 * math.sqrt(eps))
    print(f"n={n} K={K}: beta0={beta0} beta={beta} (C1) ok={ok_c1} gap=eps={eps} "
          f"last-stage nodes=2, claimed lower bound={claimed:.3f}, "
          f"stage-0 nodes={K+1}")
    assert ok_c1 and 2 < claimed


if __name__ == "__main__":
    run(2, 5)
    run(2, 10)
    run(3, 5)
    run(4, 4)
