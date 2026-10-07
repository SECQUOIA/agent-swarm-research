"""Localized exact acceptance (a proposed post-processing test, not part of the solver).

Given a stage of a replayed corrected-grid certificate, the test proves that a
rational feasible point xhat is globally optimal by combining
  (1) the filtering history: every point outside the retained box B has
      objective above a recorded incumbent value U' >= U >= F(xhat);
  (2) node exclusion: a node v with min-marginal m_i(v) > U excludes the whole
      slice x_i = v; for integer coordinates this narrows B to the hull of the
      surviving labels; for coordinatewise concave coordinates (endpoint grid)
      it fixes x_i at the surviving endpoint, by endpoint replacement;
  (3) a first/second-order minorant on the narrowed box B':
      F(x) - F(xhat) >= d_W'(H_WW + 2 diag(mu))d_W/2 for every x in B' cap X,
      where mu_i = |l_i|/w_i at a box endpoint with inward gradient, mu_i = 0
      at an interior point with zero gradient, mu_i = -|l_i| for an integer
      coordinate otherwise. An exact LDL' test checks positive semidefiniteness.
All arithmetic is exact. This is Proposition prop:local of the paper. Two
candidates are provided: the stationary point of the face of the stage
incumbent (``candidate``, used for the S1 counts) and the face candidate of
Definition def:facecand (``face_candidate``), which Corollary cor:local covers.
"""
from fractions import Fraction as F


def is_psd(matrix):
    m = [list(r) for r in matrix]
    n = len(m)
    for k in range(n):
        p = m[k][k]
        if p < 0:
            return False
        if p == 0:
            if any(m[i][k] for i in range(k + 1, n)):
                return False
            continue
        for i in range(k + 1, n):
            if m[i][k]:
                f = m[i][k] / p
                for j in range(k + 1, i + 1):
                    m[i][j] -= f * m[j][k]
                    m[j][i] = m[i][j]
    return True


def _solve_linear(M, r):
    n = len(M)
    rows = [list(M[i]) + [r[i]] for i in range(n)]
    for c in range(n):
        piv = next((k for k in range(c, n) if rows[k][c]), None)
        if piv is None:
            return None
        rows[c], rows[piv] = rows[piv], rows[c]
        p = rows[c][c]
        rows[c] = [v / p for v in rows[c]]
        for k in range(n):
            if k != c and rows[k][c]:
                f = rows[k][c]
                rows[k] = [a - f * b for a, b in zip(rows[k], rows[c])]
    return [rows[i][n] for i in range(n)]


def candidate(problem, point):
    """Untrusted proposal: stationary point of the face of `point` (original bounds)."""
    n = len(point)
    H, b = problem.A, problem.b
    fixed = [i for i in range(n) if point[i] in problem.bounds[i] or i in problem.integers]
    free = [i for i in range(n) if i not in fixed]
    x = list(point)
    if free:
        sol = _solve_linear([[H[i][j] for j in free] for i in free],
                            [-b[i] - sum(H[i][j] * x[j] for j in fixed) for i in free])
        if sol is None:
            return None
        for i, v in zip(free, sol):
            x[i] = v
    return tuple(x) if problem.feasible(x) else None


def narrowed_box(problem, stage):
    """Retained hull of one certificate stage, narrowed by node exclusion."""
    upper = F(stage['upper'])
    box = []
    for i, (lo, hi) in enumerate(stage['next_bounds']):
        lo, hi = F(lo), F(hi)
        grid = [F(v) for v in stage['grids'][i]]
        marg = [F(v) for v in stage['min_marginals'][i]]
        if problem.A[i][i] <= 0 and len(grid) == 2:
            (a, b), (ma, mb) = grid, marg
            if ma > upper >= mb:
                lo = hi = b
            elif mb > upper >= ma:
                lo = hi = a
        elif i in problem.integers:
            keep = [v for v, m in zip(grid, marg) if lo <= v <= hi and m <= upper]
            for k in range(len(grid) - 1):
                a, b = grid[k], grid[k + 1]
                if b - a >= 2 and lo <= a and b <= hi and min(marg[k], marg[k + 1]) <= upper:
                    keep.extend([a + 1, b - 1])
            if keep:
                lo, hi = min(keep), max(keep)
        box.append((lo, hi))
    return tuple(box)


def local_accept(problem, xhat, box, upper):
    if xhat is None or not all(lo <= v <= hi for v, (lo, hi) in zip(xhat, box)):
        return False
    if problem.value(xhat) > upper:
        return False
    n = len(xhat)
    H, b = problem.A, problem.b
    grad = [b[i] + sum(H[i][j] * xhat[j] for j in range(n)) for i in range(n)]
    W = [i for i in range(n) if box[i][0] < box[i][1]]
    mu = {}
    for i in W:
        lo, hi = box[i]
        if xhat[i] == lo and grad[i] >= 0:
            mu[i] = grad[i] / (hi - lo)
        elif xhat[i] == hi and grad[i] <= 0:
            mu[i] = -grad[i] / (hi - lo)
        elif lo < xhat[i] < hi and grad[i] == 0:
            mu[i] = F(0)
        elif i in problem.integers:
            mu[i] = -abs(grad[i])
        else:
            return False
    return is_psd([[H[i][j] + (2 * mu[i] if i == j else 0) for j in W] for i in W])


def face_candidate(problem, y, box):
    """Face candidate of Definition def:facecand at a stage with corrected
    minimizer y and narrowed box B': integer coordinates and coordinates with a
    single-point B'_i copy y; a continuous coordinate with B'_i of positive
    length is fixed at l_i if l_i is in B'_i, else at u_i if u_i is in B'_i,
    and is free otherwise; the free part solves the stationarity equations.
    Returns None if the free Hessian block is singular."""
    n = len(y)
    H, b = problem.A, problem.b
    x = list(y)
    free = []
    for i in range(n):
        lo, hi = box[i]
        if i in problem.integers or lo == hi:
            continue
        l0, u0 = problem.bounds[i]
        if lo <= l0 <= hi:
            x[i] = F(l0)
        elif lo <= u0 <= hi:
            x[i] = F(u0)
        else:
            free.append(i)
    if free:
        fixed = [i for i in range(n) if i not in free]
        sol = _solve_linear([[H[i][j] for j in free] for i in free],
                            [-b[i] - sum(H[i][j] * x[j] for j in fixed) for i in free])
        if sol is None:
            return None
        for i, v in zip(free, sol):
            x[i] = v
    return tuple(x)


def first_face_acceptance(problem, certificate):
    """First stage at which the face candidate passes Proposition prop:local."""
    for st in certificate['stages']:
        box = narrowed_box(problem, st)
        y = tuple(F(v) for v in st['grid_point'])
        xhat = face_candidate(problem, y, box)
        if xhat is not None and local_accept(problem, xhat, box, F(st['upper'])):
            return st['stage'], xhat
    return None, None


def first_acceptance(problem, certificate):
    """First stage whose retained box admits the localized proof, with its point."""
    for st in certificate['stages']:
        box = narrowed_box(problem, st)
        xhat = candidate(problem, tuple(F(v) for v in st['incumbent']))
        if local_accept(problem, xhat, box, F(st['upper'])):
            return st['stage'], xhat, local_accept(problem, xhat, tuple(problem.bounds), F(st['upper']))
    return None, None, None
