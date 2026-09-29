"""Exact rational tools for the integer-core recheck (written from scratch).

phi(x) = ||A x - y||^2 with rational A (full column rank) and y.
All minima are exact Fractions.
"""
import itertools
from fractions import Fraction as Fr


def F(v):
    return v if isinstance(v, Fr) else Fr(v)


def matvec(A, x):
    return [sum(a * b for a, b in zip(row, x)) for row in A]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def phi(A, y, x):
    r = [ri - yi for ri, yi in zip(matvec(A, x), y)]
    return dot(r, r)


def solve(M, b):
    """Exact Gaussian elimination; returns None if M is singular."""
    n = len(M)
    aug = [list(map(F, row)) + [F(bi)] for row, bi in zip(M, b)]
    for c in range(n):
        piv = next((r for r in range(c, n) if aug[r][c] != 0), None)
        if piv is None:
            return None
        aug[c], aug[piv] = aug[piv], aug[c]
        pv = aug[c][c]
        aug[c] = [v / pv for v in aug[c]]
        for r in range(n):
            if r != c and aug[r][c] != 0:
                f = aug[r][c]
                aug[r] = [a - f * b2 for a, b2 in zip(aug[r], aug[c])]
    return [aug[r][n] for r in range(n)]


def affine_min(A, y, p0, dirs):
    """min of phi over p0 + span(dirs); returns (mu, x) or None if dirs are dependent."""
    if not dirs:
        return [], list(p0)
    Ad = [matvec(A, d) for d in dirs]
    r0 = [a - b for a, b in zip(matvec(A, p0), y)]
    G = [[dot(u, v) for v in Ad] for u in Ad]
    h = [-dot(u, r0) for u in Ad]
    mu = solve(G, h)
    if mu is None:
        return None
    x = [p0[i] + sum(m * d[i] for m, d in zip(mu, dirs)) for i in range(len(p0))]
    return mu, x


def simplex_candidate(A, y, pts):
    """If pts are affinely independent and the minimizer of phi over aff(pts) lies in
    conv(pts), return (value, x); otherwise None."""
    p0 = pts[0]
    dirs = [[a - b for a, b in zip(p, p0)] for p in pts[1:]]
    res = affine_min(A, y, p0, dirs)
    if res is None:
        return None
    mu, x = res
    if any(m < 0 for m in mu) or sum(mu) > 1:
        return None
    return phi(A, y, x), x


def hull_min(A, y, pts):
    """Exact min of phi over conv(pts) (Caratheodory: the minimizer is in the relative
    interior of a simplex spanned by an affinely independent subset, where it is also
    the minimizer over that subset's affine hull)."""
    d = len(pts[0])
    best = None
    for k in range(1, min(len(pts), d + 1) + 1):
        for T in itertools.combinations(pts, k):
            c = simplex_candidate(A, y, list(T))
            if c is not None and (best is None or c[0] < best[0]):
                best = c
    return best


def bad_masks(A, y, P, tau):
    """All affinely independent subsets T of P (|T| <= d+1) whose simplex contains a
    point with phi < tau.  A set I is tau-admissible iff it contains no such T."""
    d = len(P[0])
    bad = []
    for k in range(1, min(len(P), d + 1) + 1):
        for T in itertools.combinations(range(len(P)), k):
            c = simplex_candidate(A, y, [P[i] for i in T])
            if c is not None and c[0] < tau:
                bad.append(sum(1 << i for i in T))
    return bad


def admissible_table(nP, bad):
    badset = set(bad)
    ok = [True] * (1 << nP)
    ok[0] = True
    for m in range(1, 1 << nP):
        if m in badset:
            ok[m] = False
            continue
        mm = m
        good = True
        while mm:
            b = mm & -mm
            mm ^= b
            if m ^ b and not ok[m ^ b]:
                good = False
                break
        ok[m] = good
    return ok


def min_cover(nP, ok):
    """f[mask] = least number of admissible sets partitioning mask."""
    INF = 10 ** 9
    f = [INF] * (1 << nP)
    f[0] = 0
    for rem in range(1, 1 << nP):
        low = rem & -rem
        sub = rem
        best = INF
        while sub:
            if sub & low and ok[sub]:
                v = f[rem ^ sub] + 1
                if v < best:
                    best = v
            sub = (sub - 1) & rem
        f[rem] = best
    return f


def all_min_partitions(nP, ok, f, limit=10 ** 6):
    """Enumerate minimum partitions (canonical: each part contains the lowest remaining
    point)."""
    out = []

    def rec(rem, acc):
        if len(out) >= limit:
            return
        if rem == 0:
            out.append(list(acc))
            return
        low = rem & -rem
        sub = rem
        while sub:
            if sub & low and ok[sub] and f[rem ^ sub] + 1 == f[rem]:
                acc.append(sub)
                rec(rem ^ sub, acc)
                acc.pop()
            sub = (sub - 1) & rem
    rec((1 << nP) - 1, [])
    return out


def box_min(A, y, lo, hi):
    """Exact min of phi over the box [lo, hi] (face enumeration)."""
    n = len(lo)
    if any(l > h for l, h in zip(lo, hi)):
        return None
    free = [i for i in range(n) if lo[i] < hi[i]]
    best = None
    for states in itertools.product((0, 1, 2), repeat=len(free)):
        x0 = list(map(F, lo))
        fr = []
        for i, s in zip(free, states):
            if s == 0:
                x0[i] = F(lo[i])
            elif s == 1:
                x0[i] = F(hi[i])
            else:
                x0[i] = F(0)
                fr.append(i)
        dirs = []
        for i in fr:
            e = [F(0)] * n
            e[i] = F(1)
            dirs.append(e)
        res = affine_min(A, y, x0, dirs)
        if res is None:
            continue
        _, x = res
        if all(F(lo[i]) <= x[i] <= F(hi[i]) for i in range(n)):
            v = phi(A, y, x)
            if best is None or v < best:
                best = v
    return best


def halfspace_min(A, y, g, c):
    """Exact min of phi over {x : g.x >= c} (A square invertible, g != 0)."""
    n = len(g)
    xs = solve(A, y)  # unconstrained minimizer, phi = 0
    if dot(g, xs) >= c:
        return F(0)
    # min over the hyperplane g.x = c: (c - g.xs)^2 / (g^T H^{-1} g), H = A^T A
    H = [[sum(A[k][i] * A[k][j] for k in range(len(A))) for j in range(n)] for i in range(n)]
    w = solve(H, g)
    return (c - dot(g, xs)) ** 2 / dot(g, w)


def grad(A, y, x):
    r = [a - b for a, b in zip(matvec(A, x), y)]
    n = len(x)
    return [2 * sum(A[k][j] * r[k] for k in range(len(A))) for j in range(n)]
