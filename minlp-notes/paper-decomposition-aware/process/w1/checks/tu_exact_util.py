"""Small exact-rational helpers for the TU-cluster checks.

Everything uses fractions.Fraction. Sizes are tiny; nothing here is efficient.
"""
from fractions import Fraction as Fr
from itertools import combinations, product


def det(M):
    """Determinant by fraction Gaussian elimination."""
    n = len(M)
    if n == 0:
        return Fr(1)
    A = [[Fr(v) for v in row] for row in M]
    d = Fr(1)
    for c in range(n):
        piv = next((r for r in range(c, n) if A[r][c] != 0), None)
        if piv is None:
            return Fr(0)
        if piv != c:
            A[c], A[piv] = A[piv], A[c]
            d = -d
        d *= A[c][c]
        for r in range(c + 1, n):
            f = A[r][c] / A[c][c]
            if f:
                for k in range(c, n):
                    A[r][k] -= f * A[c][k]
    return d


def solve(M, b):
    """Solve square nonsingular system; return None if singular."""
    n = len(M)
    A = [[Fr(v) for v in row] + [Fr(bb)] for row, bb in zip(M, b)]
    for c in range(n):
        piv = next((r for r in range(c, n) if A[r][c] != 0), None)
        if piv is None:
            return None
        A[c], A[piv] = A[piv], A[c]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]
                for k in range(c, n + 1):
                    A[r][k] -= f * A[c][k]
    return [A[i][n] / A[i][i] for i in range(n)]


def rank(M):
    if not M:
        return 0
    A = [[Fr(v) for v in row] for row in M]
    m, n = len(A), len(A[0])
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if A[i][c] != 0), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        for i in range(m):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]
                for k in range(c, n):
                    A[i][k] -= f * A[r][k]
        r += 1
        if r == m:
            break
    return r


def nullspace(M, n):
    """Basis of {v in Q^n : M v = 0} (list of vectors)."""
    if not M:
        return [[Fr(int(i == j)) for i in range(n)] for j in range(n)]
    A = [[Fr(v) for v in row] for row in M]
    m = len(A)
    pivcols = []
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if A[i][c] != 0), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        pv = A[r][c]
        A[r] = [v / pv for v in A[r]]
        for i in range(m):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        pivcols.append(c)
        r += 1
        if r == m:
            break
    free = [c for c in range(n) if c not in pivcols]
    basis = []
    for f in free:
        v = [Fr(0)] * n
        v[f] = Fr(1)
        for i, pc in enumerate(pivcols):
            v[pc] = -A[i][f]
        basis.append(v)
    return basis


def dot(a, b):
    return sum(Fr(x) * Fr(y) for x, y in zip(a, b))


def matvec(M, v):
    return [dot(row, v) for row in M]


def vertices(Aineq, bineq, Aeq=(), beq=()):
    """All vertices of {x : Aineq x <= bineq, Aeq x = beq} (bounded, small)."""
    Aineq = [list(map(Fr, r)) for r in Aineq]
    bineq = list(map(Fr, bineq))
    Aeq = [list(map(Fr, r)) for r in Aeq]
    beq = list(map(Fr, beq))
    n = len(Aineq[0]) if Aineq else len(Aeq[0])
    req = rank(Aeq) if Aeq else 0
    need = n - req
    out = set()
    for S in combinations(range(len(Aineq)), need):
        rows = Aeq + [Aineq[i] for i in S]
        rhs = beq + [bineq[i] for i in S]
        if rank(rows) < n:
            continue
        # pick n independent rows
        sel, selr = [], []
        for r_, b_ in zip(rows, rhs):
            if rank(sel + [r_]) > len(sel):
                sel.append(r_)
                selr.append(b_)
            if len(sel) == n:
                break
        x = solve(sel, selr)
        if x is None:
            continue
        if all(dot(r_, x) == b_ for r_, b_ in zip(rows, rhs)) and \
           all(dot(r_, x) <= b_ for r_, b_ in zip(Aineq, bineq)) and \
           all(dot(r_, x) == b_ for r_, b_ in zip(Aeq, beq)):
            out.add(tuple(x))
    return [list(v) for v in out]


def caratheodory(t, Aineq, bineq, Aeq=(), beq=()):
    """Write the feasible point t as a convex combination of vertices of the
    bounded polytope {Aineq x <= bineq, Aeq x = beq}. Returns list of
    (weight, vertex). Exact constructive Caratheodory."""
    Aineq = [list(map(Fr, r)) for r in Aineq]
    bineq = list(map(Fr, bineq))
    Aeq = [list(map(Fr, r)) for r in Aeq]
    n = len(t)

    def tight(x):
        return [i for i, (r, b) in enumerate(zip(Aineq, bineq)) if dot(r, x) == b]

    def to_vertex(x):
        x = list(x)
        while True:
            T = Aeq + [Aineq[i] for i in tight(x)]
            ns = nullspace(T, n)
            if not ns:
                return x
            d = ns[0]
            # move along d until a new inequality becomes tight
            best = None
            for r, b in zip(Aineq, bineq):
                rd = dot(r, d)
                if rd > 0:
                    s = (b - dot(r, x)) / rd
                    if best is None or s < best:
                        best = s
            if best is None:  # try -d
                d = [-v for v in d]
                for r, b in zip(Aineq, bineq):
                    rd = dot(r, d)
                    if rd > 0:
                        s = (b - dot(r, x)) / rd
                        if best is None or s < best:
                            best = s
            x = [xi + best * di for xi, di in zip(x, d)]

    comb = []
    x = [Fr(v) for v in t]
    weight = Fr(1)
    for _ in range(n + 2):
        v = to_vertex(x)
        if v == x:
            comb.append((weight, v))
            break
        d = [xi - vi for xi, vi in zip(x, v)]
        # x' = x + mu d, maximal mu keeping feasibility
        mu = None
        for r, b in zip(Aineq, bineq):
            rd = dot(r, d)
            if rd > 0:
                s = (b - dot(r, x)) / rd
                if mu is None or s < mu:
                    mu = s
        assert mu is not None and mu >= 0
        xp = [xi + mu * di for xi, di in zip(x, d)]
        # x = lam v + (1-lam) xp, with x - v = d, xp - x = mu d -> lam = mu/(1+mu)
        lam = mu / (1 + mu)
        comb.append((weight * lam, v))
        weight *= (1 - lam)
        x = xp
    else:
        raise RuntimeError("Caratheodory did not terminate")
    tot = sum(w for w, _ in comb)
    assert tot == 1, tot
    mean = [sum(w * v[i] for w, v in comb) for i in range(n)]
    assert mean == [Fr(v) for v in t]
    return comb


def simplest_rational(lo, hi):
    """Rational with least denominator in the closed interval [lo, hi]."""
    lo, hi = Fr(lo), Fr(hi)
    assert lo <= hi
    import math
    fl = math.floor(lo)
    if fl == lo:
        return Fr(fl)
    if fl + 1 <= hi:
        return Fr(fl + 1)
    # both in (fl, fl+1)
    r = simplest_rational(1 / (hi - fl), 1 / (lo - fl))
    return fl + 1 / r
