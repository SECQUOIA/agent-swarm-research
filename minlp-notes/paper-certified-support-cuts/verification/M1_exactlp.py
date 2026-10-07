"""Lane M1: a small exact two-phase simplex (Bland's rule) over Fractions.

Used by M1_closure_random.py and M1_rounding.py.  sympy's simplex raised
"Oscillating system" on feasible phase-1 problems and returned without
error for infeasible problems with a constant objective, so it is not used.
"""
from fractions import Fraction as Fr


def _simplex_std(c, A, b):
    """min c.x  s.t.  A x = b, x >= 0  (b >= 0 required).

    Returns ("optimal", value, x) / ("unbounded", None, None) /
    ("infeasible", None, None)."""
    m, n = len(A), len(c)
    # phase 1 tableau with artificials n..n+m-1
    T = [list(map(Fr, A[i])) + [Fr(int(i == k)) for k in range(m)] + [Fr(b[i])] for i in range(m)]
    basis = [n + i for i in range(m)]

    def pivot(r, col):
        pv = T[r][col]
        T[r] = [v / pv for v in T[r]]
        for i in range(len(T)):
            if i != r and T[i][col] != 0:
                f = T[i][col]
                T[i] = [vi - f * vr for vi, vr in zip(T[i], T[r])]
        basis[r] = col

    def run(cost, allowed):
        while True:
            # reduced costs
            red = []
            for j in allowed:
                if j in basis:
                    continue
                rc = cost[j] - sum(cost[basis[i]] * T[i][j] for i in range(len(T)))
                if rc < 0:
                    red.append(j)
            if not red:
                return "optimal"
            col = min(red)                      # Bland: smallest index enters
            best = None
            for i in range(len(T)):
                if T[i][col] > 0:
                    ratio = T[i][-1] / T[i][col]
                    key = (ratio, basis[i])
                    if best is None or key < best[0]:
                        best = (key, i)
            if best is None:
                return "unbounded"
            pivot(best[1], col)

    cost1 = [Fr(0)] * n + [Fr(1)] * m
    run(cost1, list(range(n + m)))
    if sum(T[i][-1] for i in range(m) if basis[i] >= n) != 0:
        return ("infeasible", None, None)
    # drive artificials out of the basis
    r = 0
    while r < len(T):
        if basis[r] >= n:
            col = next((j for j in range(n) if T[r][j] != 0), None)
            if col is None:
                del T[r]
                del basis[r]
                continue
            pivot(r, col)
        r += 1
    cost2 = [Fr(v) for v in c] + [Fr(0)] * m
    status = run(cost2, list(range(n)))
    if status == "unbounded":
        return ("unbounded", None, None)
    x = [Fr(0)] * n
    for i, j in enumerate(basis):
        x[j] = T[i][-1]
    return ("optimal", sum(Fr(c[j]) * x[j] for j in range(n)), x)


def solve_lp(c, A_ub=(), b_ub=(), A_eq=(), b_eq=(), bounds=None):
    """min c.x s.t. A_ub x <= b_ub, A_eq x = b_eq, lo <= x <= hi.

    bounds: list of (lo, hi), each Fraction or None (= infinite).
    Returns (status, value, x)."""
    nv = len(c)
    bounds = bounds or [(Fr(0), None)] * nv
    # column map: x_j = off_j + sum_k coef * y_k
    cols, off = [], []
    extra_ub, extra_b = [], []
    ny = 0
    for j, (lo, hi) in enumerate(bounds):
        if lo is not None:
            cols.append([(ny, Fr(1))]); off.append(Fr(lo)); ny += 1
            if hi is not None:
                extra_ub.append((ny - 1, Fr(hi) - Fr(lo)))
        elif hi is not None:
            cols.append([(ny, Fr(-1))]); off.append(Fr(hi)); ny += 1
        else:
            cols.append([(ny, Fr(1)), (ny + 1, Fr(-1))]); off.append(Fr(0)); ny += 2

    def tr(row):
        out = [Fr(0)] * ny
        shift = Fr(0)
        for j, a in enumerate(row):
            a = Fr(a)
            shift += a * off[j]
            for k, s in cols[j]:
                out[k] += a * s
        return out, shift

    rows, rhs, nslack = [], [], len(A_ub) + len(extra_ub)
    k = 0
    for row, bb in zip(A_ub, b_ub):
        r, sh = tr(row)
        rows.append(r + [Fr(int(i == k)) for i in range(nslack)]); rhs.append(Fr(bb) - sh); k += 1
    for y, ub in extra_ub:
        r = [Fr(0)] * ny
        r[y] = Fr(1)
        rows.append(r + [Fr(int(i == k)) for i in range(nslack)]); rhs.append(ub); k += 1
    for row, bb in zip(A_eq, b_eq):
        r, sh = tr(row)
        rows.append(r + [Fr(0)] * nslack); rhs.append(Fr(bb) - sh)
    for i in range(len(rows)):
        if rhs[i] < 0:
            rows[i] = [-v for v in rows[i]]; rhs[i] = -rhs[i]
    cc, csh = tr(c)
    cc = cc + [Fr(0)] * nslack
    status, val, y = _simplex_std(cc, rows, rhs)
    if status != "optimal":
        return status, None, None
    x = [off[j] + sum(s * y[k] for k, s in cols[j]) for j in range(nv)]
    return "optimal", val + csh, x


if __name__ == "__main__":
    # tiny self-test
    st, v, x = solve_lp([1, 1], A_ub=[[-1, -1]], b_ub=[-1], bounds=[(Fr(0), None), (Fr(0), Fr(2))])
    assert st == "optimal" and v == 1
    st, v, x = solve_lp([1], A_eq=[[1]], b_eq=[Fr(-3)], bounds=[(None, None)])
    assert st == "optimal" and v == -3
    st, _, _ = solve_lp([0], A_ub=[[1], [-1]], b_ub=[0, -1], bounds=[(None, None)])
    assert st == "infeasible"
    st, _, _ = solve_lp([-1], bounds=[(Fr(0), None)])
    assert st == "unbounded"
    print("M1_exactlp self-test passed")
