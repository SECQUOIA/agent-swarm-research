"""Exact tools for convex hulls of graphs of ReLU layers over boxes.

Scratch code for the ml-surrogate-minlp scouting report (2026-09-28).

conv{(x, ReLU(Wx+b)) : x in box} is the convex hull of the graph points at
the vertices of the arrangement {w_j x + b_j = 0} restricted to the box.
Vertices are computed exactly with Fractions.  Facets are computed with
cddlib in floating point and then re-derived and verified exactly: every
reported facet is an exact rational inequality, valid for every exact
vertex, whose tight vertices have full affine rank.
"""
from fractions import Fraction as Fr
from itertools import combinations
import sys

sys.path.insert(0, "/tmp/pylibs")
import cdd  # noqa: E402


def solve_exact(A, rhs):
    """Solve square system A x = rhs exactly; return None if singular."""
    n = len(A)
    M = [[Fr(v) for v in row] + [Fr(r)] for row, r in zip(A, rhs)]
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None:
            return None
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [v / pv for v in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]


def arrangement_vertices(W, b, lo, hi):
    """Vertices of the arrangement of {W_j x + b_j = 0} inside the box [lo, hi]."""
    n = len(lo)
    hyps = []  # (a, rhs) meaning a.x = rhs
    for i in range(n):
        e = [0] * n
        e[i] = 1
        hyps.append((e, lo[i]))
        hyps.append((e, hi[i]))
    for wj, bj in zip(W, b):
        if any(v != 0 for v in wj):
            hyps.append((list(wj), -bj))
    verts = set()
    for S in combinations(range(len(hyps)), n):
        sol = solve_exact([hyps[s][0] for s in S], [hyps[s][1] for s in S])
        if sol is None:
            continue
        if all(Fr(lo[i]) <= sol[i] <= Fr(hi[i]) for i in range(n)):
            verts.add(tuple(sol))
    return sorted(verts)


def relu_layer(W, b, x):
    out = []
    for wj, bj in zip(W, b):
        t = sum(Fr(w) * xi for w, xi in zip(wj, x)) + Fr(bj)
        out.append(t if t > 0 else Fr(0))
    return out


def graph_points(W, b, lo, hi, extra=None):
    V = arrangement_vertices(W, b, lo, hi)
    pts = []
    for v in V:
        p = list(v) + relu_layer(W, b, v)
        pts.append(tuple(p))
    return sorted(set(pts))


def affine_rank(P):
    if not P:
        return -1
    base = P[0]
    rows = [[a - c for a, c in zip(p, base)] for p in P[1:]]
    return matrix_rank(rows)


def matrix_rank(rows):
    M = [list(map(Fr, r)) for r in rows]
    if not M:
        return 0
    ncol = len(M[0])
    rank = 0
    for c in range(ncol):
        piv = next((r for r in range(rank, len(M)) if M[r][c] != 0), None)
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        pv = M[rank][c]
        M[rank] = [v / pv for v in M[rank]]
        for r in range(len(M)):
            if r != rank and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f * bb for a, bb in zip(M[r], M[rank])]
        rank += 1
    return rank


def nullspace_vector(rows, ncol):
    """One nonzero vector in the right nullspace of rows (exact)."""
    M = [list(map(Fr, r)) for r in rows]
    pivcols = []
    rank = 0
    for c in range(ncol):
        piv = next((r for r in range(rank, len(M)) if M[r][c] != 0), None)
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        pv = M[rank][c]
        M[rank] = [v / pv for v in M[rank]]
        for r in range(len(M)):
            if r != rank and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f * bb for a, bb in zip(M[r], M[rank])]
        pivcols.append(c)
        rank += 1
    free = [c for c in range(ncol) if c not in pivcols]
    if not free:
        return None
    f = free[0]
    v = [Fr(0)] * ncol
    v[f] = Fr(1)
    for r, c in enumerate(pivcols):
        v[c] = -M[r][f]
    return v


def normalize_int(vec):
    from math import gcd
    den = 1
    for v in vec:
        den = den * v.denominator // gcd(den, v.denominator)
    iv = [int(v * den) for v in vec]
    g = 0
    for v in iv:
        g = gcd(g, abs(v))
    return [v // g for v in iv] if g else iv


def facets(points, tol=1e-7):
    """Exact facets of conv(points) (assumed full-dimensional).

    Returns list of (c0, c) with c0 + c.z >= 0 valid, as integer vectors.
    """
    D = len(points[0])
    assert affine_rank(points) == D, "hull not full-dimensional"
    mat = cdd.matrix_from_array([[1.0] + [float(v) for v in p] for p in points],
                                rep_type=cdd.RepType.GENERATOR)
    poly = cdd.polyhedron_from_matrix(mat)
    H = cdd.copy_inequalities(poly).array
    result = set()
    for row in H:
        c0, c = row[0], row[1:]
        tight = [p for p in points
                 if abs(c0 + sum(ci * float(pi) for ci, pi in zip(c, p))) < tol]
        # exact hyperplane through the tight points: solve [1 p] . (c0, c) = 0
        rows = [[1] + list(p) for p in tight]
        vec = nullspace_vector(rows, D + 1)
        assert vec is not None
        vec = normalize_int(vec)
        vals = [vec[0] + sum(ci * pi for ci, pi in zip(vec[1:], p)) for p in points]
        if all(v >= 0 for v in vals):
            pass
        elif all(v <= 0 for v in vals):
            vec = [-v for v in vec]
        else:
            raise AssertionError("exact hyperplane not valid")
        tight_exact = [p for p, v in zip(points, vals) if v == 0]
        assert affine_rank(tight_exact) == D - 1, "not a facet"
        result.add(tuple(vec))
    return sorted(result)


def fmt_ineq(vec, names):
    c0, c = vec[0], vec[1:]
    lhs = []
    for ci, nm in zip(c, names):
        if ci == 0:
            continue
        s = "+" if ci > 0 else "-"
        a = abs(ci)
        lhs.append(f"{s} {'' if a == 1 else a}{nm}")
    txt = " ".join(lhs).lstrip("+ ")
    return f"{txt} >= {-c0}"
