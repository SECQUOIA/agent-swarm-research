"""Exact rational helpers for the exact-output checks (cluster `exact`).

Quadratics are F(x) = 1/2 x^T H x + b^T x + c with H the Hessian.
All arithmetic uses fractions.Fraction. Dimensions are tiny; brute force is
intended.
"""
from fractions import Fraction as Fr
from itertools import product, combinations
from math import lcm, prod


def value(H, b, c, x):
    n = len(x)
    return (sum(H[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) / 2
            + sum(b[i] * x[i] for i in range(n)) + c)


def grad(H, b, x):
    n = len(x)
    return [sum(H[i][j] * x[j] for j in range(n)) + b[i] for i in range(n)]


def det(M):
    M = [row[:] for row in M]
    n = len(M)
    d = Fr(1)
    for col in range(n):
        piv = next((r for r in range(col, n) if M[r][col] != 0), None)
        if piv is None:
            return Fr(0)
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
            d = -d
        d *= M[col][col]
        for r in range(col + 1, n):
            f = M[r][col] / M[col][col]
            if f:
                M[r] = [a - f * b_ for a, b_ in zip(M[r], M[col])]
    return d


def rank(M):
    M = [row[:] for row in M]
    if not M:
        return 0
    rows, cols = len(M), len(M[0])
    r = 0
    for col in range(cols):
        piv = next((i for i in range(r, rows) if M[i][col] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(rows):
            if i != r and M[i][col] != 0:
                f = M[i][col] / M[r][col]
                M[i] = [a - f * b_ for a, b_ in zip(M[i], M[r])]
        r += 1
        if r == rows:
            break
    return r


def solve_unique(A, rhs):
    """Solve A x = rhs (A has full column rank, possibly more rows).

    Returns the unique solution, or None if inconsistent or rank deficient.
    """
    rows = len(A)
    cols = len(A[0]) if rows else 0
    if cols == 0:
        return [] if all(v == 0 for v in rhs) else None
    M = [list(A[i]) + [rhs[i]] for i in range(rows)]
    r = 0
    pivcols = []
    for col in range(cols):
        piv = next((i for i in range(r, rows) if M[i][col] != 0), None)
        if piv is None:
            return None  # rank deficient
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][col]
        M[r] = [a / pv for a in M[r]]
        for i in range(rows):
            if i != r and M[i][col] != 0:
                f = M[i][col]
                M[i] = [a - f * b_ for a, b_ in zip(M[i], M[r])]
        pivcols.append(col)
        r += 1
    for i in range(r, rows):
        if M[i][-1] != 0:
            return None
    return [M[i][-1] for i in range(cols)]


def is_pd(M):
    """Positive definite via leading principal minors (Sylvester)."""
    n = len(M)
    return all(det([row[:k] for row in M[:k]]) > 0 for k in range(1, n + 1))


def is_psd(M):
    """Positive semidefinite via all principal minors >= 0."""
    n = len(M)
    for k in range(1, n + 1):
        for S in combinations(range(n), k):
            if det([[M[i][j] for j in S] for i in S]) < 0:
                return False
    return True


def common_den(xs):
    return lcm(*[Fr(v).denominator for v in xs]) if xs else 1


def monomial_denominator(H, b, c, bounds):
    """D clearing monomial coefficients (H_ii/2, H_ij for i<j), b, c, endpoints."""
    n = len(b)
    dens = [Fr(c).denominator] + [Fr(v).denominator for v in b]
    dens += [Fr(H[i][i] / 2).denominator for i in range(n)]
    dens += [Fr(H[i][j]).denominator for i in range(n) for j in range(i + 1, n)]
    dens += [Fr(v).denominator for lu in bounds for v in lu]
    return lcm(*dens)


def heights(H, b, c, bounds, integers):
    """Three coordinate-height bounds: Hadamard-diagonal (new), code row-norm,
    and report (2 n C_H)^n with the factor-two normalization."""
    n = len(b)
    D = monomial_denominator(H, b, c, bounds)
    cont = [i for i in range(n) if i not in integers and bounds[i][0] < bounds[i][1]]
    P = [[D * H[i][j] for j in range(n)] for i in range(n)]
    assert all(P[i][j].denominator == 1 for i in range(n) for j in range(n))
    R_had = D * prod(int(P[i][i]) for i in cont if P[i][i] > 0)
    # factor-two normalization (report/code): D2 clears H/2 entries
    dens2 = [Fr(c).denominator] + [Fr(v).denominator for v in b]
    dens2 += [Fr(H[i][j] / 2).denominator for i in range(n) for j in range(n)]
    dens2 += [Fr(v).denominator for lu in bounds for v in lu]
    D2 = lcm(*dens2)
    row = 1
    for i in cont:
        rn = sum(abs(D2 * H[i][j]) for j in cont)
        row *= max(1, int(rn))
    R_code = D2 * row
    CH = max([1] + [abs(int(D2 * H[i][j] / 2)) for i in range(n) for j in range(n)])
    R_rep = D2 * (2 * n * CH) ** n
    return dict(D=D, P=P, cont=cont, R_had=R_had, V_had=D * R_had ** 2,
                D2=D2, R_code=R_code, R_rep=R_rep)


def face_candidates(H, b, c, bounds, integers):
    """All stationary points of nonsingular free systems on all faces of all
    integer slices (continuous coords: lower / upper / free)."""
    n = len(b)
    ranges = []
    for i in range(n):
        l, u = bounds[i]
        if i in integers:
            ranges.append([('fix', Fr(k)) for k in range(int(l), int(u) + 1)])
        elif l == u:
            ranges.append([('fix', Fr(l))])
        else:
            ranges.append([('fix', Fr(l)), ('fix', Fr(u)), ('free', None)])
    out = []
    for choice in product(*ranges):
        free = [i for i in range(n) if choice[i][0] == 'free']
        fixed = {i: choice[i][1] for i in range(n) if choice[i][0] == 'fix'}
        if free:
            A = [[H[i][j] for j in free] for i in free]
            rhs = [-b[i] - sum(H[i][j] * fixed[j] for j in fixed) for i in free]
            if det(A) == 0:
                continue
            sol = solve_unique(A, rhs)
            if sol is None:
                continue
            x = [None] * n
            for i, v in fixed.items():
                x[i] = v
            for i, v in zip(free, sol):
                x[i] = v
        else:
            x = [fixed[i] for i in range(n)]
        if all(bounds[i][0] <= x[i] <= bounds[i][1] for i in range(n)):
            out.append((tuple(x), tuple(free)))
    return out


def corrected_grid_lower_bound(H, b, c, bounds, integers, m):
    """beta = min over a uniform grid of F - sum_i L_i w_i^2/8 (valid lower bound)."""
    n = len(b)
    grids = []
    for i in range(n):
        l, u = Fr(bounds[i][0]), Fr(bounds[i][1])
        if i in integers:
            grids.append([Fr(k) for k in range(int(l), int(u) + 1)])
        elif l == u:
            grids.append([l])
        else:
            grids.append([l + (u - l) * k / m for k in range(m + 1)])
    corr = []
    for i in range(n):
        Li = max(H[i][i], Fr(0))
        if i in integers or len(grids[i]) == 1:
            corr.append(Fr(0))
        else:
            w = grids[i][1] - grids[i][0]
            corr.append(Li * w * w / 8)
    best = None
    for y in product(*grids):
        q = value(H, b, c, list(y)) - sum(corr)
        best = q if best is None or q < best else best
    return best


def lp_feasible_point(A, rhs, box):
    """Find a vertex of {x in box : A x = rhs} by enumerating bound patterns.

    Tiny dimensions only. Returns a point or None.
    """
    m = len(box)
    idx = list(range(m))
    for k in range(m + 1):
        for K in combinations(idx, k):
            T = [i for i in idx if i not in K]
            for pattern in product((0, 1), repeat=k):
                xK = {i: box[i][p] for i, p in zip(K, pattern)}
                AT = [[A[r][i] for i in T] for r in range(len(A))]
                r2 = [rhs[r] - sum(A[r][i] * xK[i] for i in K) for r in range(len(A))]
                if T:
                    if rank(AT) < len(T):
                        continue
                    sol = solve_unique(AT, r2)
                    if sol is None:
                        continue
                else:
                    if any(v != 0 for v in r2):
                        continue
                    sol = []
                x = [None] * m
                for i, v in xK.items():
                    x[i] = v
                for i, v in zip(T, sol):
                    x[i] = v
                if all(box[i][0] <= x[i] <= box[i][1] for i in idx):
                    return x
    return None
