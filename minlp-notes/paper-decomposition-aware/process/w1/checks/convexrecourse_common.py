"""Exact rational helpers for the convex-recourse checks.

Everything uses fractions.Fraction.  The routines are meant for very small
instances (dimension <= 4); they are diagnostics, not efficient solvers.
"""
from fractions import Fraction as Fr
from itertools import product


def mat(rows):
    return [[Fr(x) for x in r] for r in rows]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))]
            for i in range(len(A))]


def transpose(A):
    return [list(r) for r in zip(*A)]


def matvec(A, x):
    return [sum(a * b for a, b in zip(row, x)) for row in A]


def solve(A, b):
    """Solve a nonsingular square system exactly (Gauss-Jordan)."""
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            raise ZeroDivisionError("singular")
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        M[c] = [x / piv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]


def inverse(A):
    n = len(A)
    cols = [solve(A, [Fr(int(i == j)) for i in range(n)]) for j in range(n)]
    return transpose(cols)


def is_psd(A):
    """Exact PSD test by symmetric elimination allowing zero pivots."""
    A = [list(r) for r in A]
    n = len(A)
    idx = list(range(n))
    while idx:
        i = idx[0]
        if A[i][i] < 0:
            return False
        if A[i][i] == 0:
            if any(A[i][j] != 0 for j in idx):
                return False
            idx = idx[1:]
            continue
        piv = A[i][i]
        rest = idx[1:]
        for j in rest:
            for k in rest:
                A[j][k] -= A[j][i] * A[i][k] / piv
        idx = rest
    return True


# ---------------------------------------------------------------- box QP

def box_qp_pd(C, g, l, u):
    """min 1/2 y'Cy + g'y over l<=y<=u, C positive definite, by enumerating
    lower/free/upper patterns and testing KKT exactly.  Returns (value, y,
    pattern)."""
    r = len(C)
    for pat in product("LFU", repeat=r):
        y = [None] * r
        for i, s in enumerate(pat):
            if s == "L":
                y[i] = l[i]
            elif s == "U":
                y[i] = u[i]
        F = [i for i in range(r) if pat[i] == "F"]
        if F:
            A = [[C[i][j] for j in F] for i in F]
            rhs = [-(g[i] + sum(C[i][j] * y[j] for j in range(r) if pat[j] != "F"))
                   for i in F]
            yF = solve(A, rhs)
            for k, i in enumerate(F):
                y[i] = yF[k]
        if any(y[i] < l[i] or y[i] > u[i] for i in range(r)):
            continue
        grad = [sum(C[i][j] * y[j] for j in range(r)) + g[i] for i in range(r)]
        ok = True
        for i, s in enumerate(pat):
            if s == "L" and grad[i] < 0:
                ok = False
            if s == "U" and grad[i] > 0:
                ok = False
            if s == "F" and grad[i] != 0:
                ok = False
        if ok:
            val = sum(Fr(1, 2) * y[i] * C[i][j] * y[j] for i in range(r) for j in range(r)) \
                + sum(g[i] * y[i] for i in range(r))
            return val, y, pat
    raise RuntimeError("no KKT pattern found")


# ------------------------------------------------- Fourier-Motzkin LP feasibility

def fm_feasible_point(cons, d):
    """cons: list of (coeffs, rhs) meaning coeffs . x <= rhs, with d variables.
    Returns an exact feasible point or None.  Exponential; tiny d only."""
    levels = []
    cur = [(list(map(Fr, a)), Fr(b)) for a, b in cons]
    for k in range(d):
        levels.append(cur)
        pos = [c for c in cur if c[0][k] > 0]
        neg = [c for c in cur if c[0][k] < 0]
        zer = [c for c in cur if c[0][k] == 0]
        new = list(zer)
        seen = set()
        for (ap, bp) in pos:
            for (an, bn) in neg:
                fp, fn = ap[k], -an[k]
                a = [ap[j] / fp + an[j] / fn for j in range(d)]
                b = bp / fp + bn / fn
                a[k] = Fr(0)
                key = (tuple(a), b)
                if key not in seen:
                    seen.add(key)
                    new.append((a, b))
        # drop trivially true rows, detect trivially false rows
        cur = []
        for a, b in new:
            if all(x == 0 for x in a):
                if b < 0:
                    return None
                continue
            cur.append((a, b))
    if any(b < 0 for a, b in cur):
        return None
    x = [Fr(0)] * d
    for k in reversed(range(d)):
        lo, hi = None, None
        for a, b in levels[k]:
            rest = b - sum(a[j] * x[j] for j in range(d) if j != k)
            if a[k] > 0:
                v = rest / a[k]
                hi = v if hi is None or v < hi else hi
            elif a[k] < 0:
                v = rest / a[k]
                lo = v if lo is None or v > lo else lo
            else:
                if rest < 0:
                    return None
        if lo is not None and hi is not None:
            if lo > hi:
                return None
            x[k] = (lo + hi) / 2
        elif lo is not None:
            x[k] = lo
        elif hi is not None:
            x[k] = hi
        else:
            x[k] = Fr(0)
    for a, b in cons:
        assert sum(Fr(p) * q for p, q in zip(a, x)) <= Fr(b)
    return x


def eq(a, b):
    """Equality a.x = b as two inequalities."""
    return [(a, b), ([-x for x in a], -b)]


def lp_feasible(eqs, ineqs, d):
    """Exact feasibility of {x: a.x = b for (a,b) in eqs; a.x <= b for (a,b)
    in ineqs}.  Equalities are eliminated by exact row reduction, then the
    inequalities in the remaining parameters go to Fourier-Motzkin.
    Returns a feasible point or None."""
    rows = [list(map(Fr, a)) + [Fr(b)] for a, b in eqs]
    piv_cols = []
    rr = 0
    for col in range(d):
        p = next((i for i in range(rr, len(rows)) if rows[i][col] != 0), None)
        if p is None:
            continue
        rows[rr], rows[p] = rows[p], rows[rr]
        pv = rows[rr][col]
        rows[rr] = [x / pv for x in rows[rr]]
        for i in range(len(rows)):
            if i != rr and rows[i][col] != 0:
                f = rows[i][col]
                rows[i] = [x - f * y for x, y in zip(rows[i], rows[rr])]
        piv_cols.append(col)
        rr += 1
    for i in range(rr, len(rows)):
        if rows[i][d] != 0:
            return None
    free = [c for c in range(d) if c not in piv_cols]
    # x = x_p + N t, t indexed by free columns
    def param(t):
        x = [Fr(0)] * d
        for k, c in enumerate(free):
            x[c] = t[k]
        for i, c in enumerate(piv_cols):
            x[c] = rows[i][d] - sum(rows[i][f] * x[f] for f in free)
        return x
    base = param([Fr(0)] * len(free))
    cols = []
    for k in range(len(free)):
        e = [Fr(int(j == k)) for j in range(len(free))]
        xk = param(e)
        cols.append([xk[j] - base[j] for j in range(d)])
    red = []
    for a, b in ineqs:
        a = list(map(Fr, a))
        coef = [sum(a[j] * cols[k][j] for j in range(d)) for k in range(len(free))]
        rhs = Fr(b) - sum(a[j] * base[j] for j in range(d))
        red.append((coef, rhs))
    if not free:
        return base if all(rhs >= 0 for _, rhs in red) else None
    t = fm_feasible_point(red, len(free))
    if t is None:
        return None
    x = param(t)
    for a, b in eqs:
        assert sum(Fr(p) * q for p, q in zip(a, x)) == Fr(b)
    for a, b in ineqs:
        assert sum(Fr(p) * q for p, q in zip(a, x)) <= Fr(b)
    return x
