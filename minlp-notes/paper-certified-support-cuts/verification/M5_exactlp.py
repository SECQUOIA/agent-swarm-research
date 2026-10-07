"""M5: small dense exact rational LP solver (two-phase simplex, Bland's rule).

Written because sympy 1.14's simplex returned a suboptimal point for a
problem with free variables and raised an 'oscillating system' error on a
degenerate one.  Bland's rule guarantees termination.  Callers must still
check primal and dual certificates; this module is only a proposal engine.
"""
from fractions import Fraction as F


def _simplex_std(A, b, c):
    """min c^T x, A x = b, x >= 0, b >= 0 assumed. Returns (status, x)."""
    m, n = len(A), len(c)
    # phase 1 with artificials n..n+m-1
    T = [list(map(F, A[i])) + [F(1) if j == i else F(0) for j in range(m)] + [F(b[i])] for i in range(m)]
    basis = [n + i for i in range(m)]

    def pivot(r, col):
        pv = T[r][col]
        T[r] = [v / pv for v in T[r]]
        for i in range(m):
            if i != r and T[i][col] != 0:
                f = T[i][col]
                T[i] = [a - f * bb for a, bb in zip(T[i], T[r])]
        basis[r] = col

    def run(cost, allowed):
        while True:
            # reduced costs
            red = []
            for j in allowed:
                if j in basis:
                    continue
                rc = cost[j] - sum(cost[basis[i]] * T[i][j] for i in range(m))
                if rc < 0:
                    red.append(j)
            if not red:
                return "optimal"
            col = min(red)  # Bland
            ratios = [(T[i][-1] / T[i][col], basis[i], i) for i in range(m) if T[i][col] > 0]
            if not ratios:
                return "unbounded"
            best = min(ratios)
            cands = [r for r in ratios if r[0] == best[0]]
            r = min(cands, key=lambda z: z[1])[2]  # Bland tie-break on leaving index
            pivot(r, col)

    cost1 = [F(0)] * n + [F(1)] * m
    run(cost1, list(range(n + m)))
    if sum(T[i][-1] for i in range(m) if basis[i] >= n) != 0:
        return "infeasible", None
    # drive artificials out of the basis where possible
    for i in range(m):
        if basis[i] >= n:
            for j in range(n):
                if T[i][j] != 0:
                    pivot(i, j)
                    break
    keep = [i for i in range(m) if basis[i] < n]
    T[:] = [T[i] for i in keep]
    basis[:] = [basis[i] for i in keep]
    m = len(T)
    cost2 = list(map(F, c)) + [F(0)] * len(A)
    status = run(cost2, list(range(n)))
    if status != "optimal":
        return status, None
    x = [F(0)] * n
    for i in range(m):
        x[basis[i]] = T[i][-1]
    return "optimal", x


def solve(c, A_ub=(), b_ub=(), A_eq=(), b_eq=(), bounds=None):
    """min c^T x s.t. A_ub x <= b_ub, A_eq x = b_eq, lo <= x <= hi.

    bounds: list of (lo, hi), None meaning infinite; default (0, None)."""
    n = len(c)
    bounds = bounds or [(0, None)] * n
    # x_j = lo_j + y_j (y_j >= 0) or x_j = y_j^+ - y_j^- when lo_j is None
    cols = []  # list of (orig index, sign, shift)
    for j, (lo, hi) in enumerate(bounds):
        if lo is None:
            cols.append((j, 1, F(0)))
            cols.append((j, -1, F(0)))
        else:
            cols.append((j, 1, F(lo)))
    N = len(cols)
    rows, rhs, kinds = [], [], []

    def expand(row):
        return [F(row[j]) * s for (j, s, _) in cols]

    def shift(row):
        return sum((F(row[j]) * F(bounds[j][0]) for j in range(n) if bounds[j][0] is not None), F(0))

    for row, bv in zip(A_ub, b_ub):
        rows.append(expand(row)); rhs.append(F(bv) - shift(row)); kinds.append("ub")
    for row, bv in zip(A_eq, b_eq):
        rows.append(expand(row)); rhs.append(F(bv) - shift(row)); kinds.append("eq")
    for j, (lo, hi) in enumerate(bounds):
        if hi is not None:
            row = [0] * n
            row[j] = 1
            rows.append(expand(row)); rhs.append(F(hi) - shift(row)); kinds.append("ub")
    nslack = kinds.count("ub")
    A, b = [], []
    si = 0
    for row, bv, kd in zip(rows, rhs, kinds):
        slack = [F(0)] * nslack
        if kd == "ub":
            slack[si] = F(1)
            si += 1
        full = row + slack
        if bv < 0:
            full = [-v for v in full]
            bv = -bv
        A.append(full); b.append(bv)
    cc = [F(c[j]) * s for (j, s, _) in cols] + [F(0)] * nslack
    if not A:
        A, b = [[F(0)] * len(cc)], [F(0)]
    status, y = _simplex_std(A, b, cc)
    if status != "optimal":
        return status, None, None
    x = [F(0)] * n
    for (j, s, sh), v in zip(cols, y[:N]):
        x[j] += s * v
    for j, (lo, hi) in enumerate(bounds):
        if lo is not None:
            x[j] += F(lo)
    val = sum((F(cj) * xj for cj, xj in zip(c, x)), F(0))
    return "optimal", val, x


if __name__ == "__main__":
    import random
    import numpy as np
    from scipy.optimize import linprog
    random.seed(1)
    for trial in range(200):
        n, m = random.randint(1, 5), random.randint(1, 5)
        c = [random.randint(-3, 3) for _ in range(n)]
        A = [[random.randint(-3, 3) for _ in range(n)] for _ in range(m)]
        b = [random.randint(-2, 4) for _ in range(m)]
        bounds = [random.choice([(0, None), (-1, 1), (None, None), (0, 2)]) for _ in range(n)]
        st, val, x = solve(c, A, b, bounds=bounds)
        ref = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")
        if ref.status == 0:
            assert st == "optimal" and abs(float(val) - ref.fun) < 1e-9, (trial, st, val, ref.fun)
            assert all(sum(F(a) * xi for a, xi in zip(row, x)) <= bv for row, bv in zip(A, b))
        else:  # HiGHS may report an unbounded model as infeasible; recheck feasibility
            feas = linprog([0] * n, A_ub=A, b_ub=b, bounds=bounds, method="highs")
            assert st == ("unbounded" if feas.status == 0 else "infeasible"), (trial, st)
    print("exact LP agrees with HiGHS on 200 random LPs")
