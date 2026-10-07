"""Core tools for quadratics on the cube [0,1]^3.

Notation
--------
A quadratic p is stored as a dict {exponent tuple: coefficient}.  The ten
quadratic exponents are QKEYS.  A quadratic moment point is a dict with the
same keys (value of the linear functional on each monomial), normalized by
y[(0,0,0)] = 1.

Cones and sets used here
------------------------
P3      quadratics nonnegative on [0,1]^3 (exact: six order simplices,
        COP_4 = PSD + NN).
P3plus  P3 with nonnegative square coefficients (dual of the positive-loop
        hull H3plus = K3 + diagonal slack).
R       the relaxation dual to  D3 (27 disjoint localizing matrices, no degree
        cutoff)  plus the 24 symmetry copies of the three-positive family
        q_{h,d,k} from research-20260925/three-positive-family-sdp.md.
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from fractions import Fraction
from itertools import permutations, product

import numpy as np

QKEYS = [
    (0, 0, 0),
    (1, 0, 0), (0, 1, 0), (0, 0, 1),
    (2, 0, 0), (0, 2, 0), (0, 0, 2),
    (1, 1, 0), (1, 0, 1), (0, 1, 1),
]
QINDEX = {k: i for i, k in enumerate(QKEYS)}
# The 20 monomials that occur in the disjoint localizing matrices.
MKEYS = [p for p in product(range(3), repeat=3) if p.count(2) <= 1]
MINDEX = {k: i for i, k in enumerate(MKEYS)}


def unit(i, n=3):
    return tuple(int(j == i) for j in range(n))


def padd(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) + v
    return {k: v for k, v in out.items() if v != 0}


def pscale(a, c):
    return {k: c * v for k, v in a.items() if c * v != 0}


def pmul(a, b):
    out = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            k = tuple(x + y for x, y in zip(ka, kb))
            out[k] = out.get(k, 0) + va * vb
    return {k: v for k, v in out.items() if v != 0}


def ppow(a, e):
    out = {(0, 0, 0): 1}
    for _ in range(e):
        out = pmul(out, a)
    return out


def var(i, one=1):
    return {unit(i): one}


def const(c):
    return {(0, 0, 0): c} if c != 0 else {}


def peval(p, x):
    total = 0
    for k, v in p.items():
        term = v
        for xi, e in zip(x, k):
            term = term * xi ** e
        total += term
    return total


# ---------------------------------------------------------------------------
# Symmetry group of the cube: g(x)_i = x_{perm[i]} or 1 - x_{perm[i]}.
# ---------------------------------------------------------------------------
GROUP = [(perm, flips) for perm in permutations(range(3))
         for flips in product((0, 1), repeat=3)]


def g_coordinates(g, one=1):
    """The affine polynomials g(x)_i."""
    perm, flips = g
    out = []
    for i in range(3):
        xi = var(perm[i], one)
        out.append(padd(const(one), pscale(xi, -1)) if flips[i] else xi)
    return out


def compose(p, g, one=1):
    """(p o g)(x) = p(g(x))."""
    coords = g_coordinates(g, one)
    out = {}
    for k, v in p.items():
        term = const(v)
        for i, e in enumerate(k):
            term = pmul(term, ppow(coords[i], e))
        out = padd(out, term)
    return out


def family_copy_reps():
    """24 representatives of GROUP modulo the x<->y swap of the family."""
    seen = set()
    reps = []
    for g in GROUP:
        perm, flips = g
        # (q o g) with q symmetric in its first two arguments: swapping the
        # first two output coordinates of g gives the same family.
        key = tuple(sorted([(perm[0], flips[0]), (perm[1], flips[1])])) + ((perm[2], flips[2]),)
        if key in seen:
            continue
        seen.add(key)
        reps.append(g)
    assert len(reps) == 24
    return reps


FAMILY_REPS = family_copy_reps()


# ---------------------------------------------------------------------------
# The family q_{h,d,k} and its 5x5 LMI.
# ---------------------------------------------------------------------------
def family_member(h, d1, d2, d3, k, one=1):
    x, y, z = var(0, one), var(1, one), var(2, one)
    L = padd(padd(padd(const(h), pscale(x, -d1)), pscale(y, -d2)), pscale(z, d3))
    D = d1 + d2 - h
    q = pmul(L, L)
    q = padd(q, pscale(pmul(z, padd(padd(const(one), pscale(x, -1)), pscale(y, -1))), 2 * d3 * k))
    q = padd(q, pscale(pmul(x, y), k * (2 * D + k)))
    return q


def moments_under(g, ymap):
    """Quadratic moments of g(x), given a function ymap(exponent)->moment.

    Returns dict on QKEYS.  Works with numbers or cvxpy expressions."""
    out = {}
    for key in QKEYS:
        mono = const(1)
        coords = g_coordinates(g)
        for i, e in enumerate(key):
            mono = pmul(mono, ppow(coords[i], e))
        out[key] = sum(v * ymap(k) for k, v in mono.items())
    return out


def family_b_B(m):
    """b and B of the family LMI from quadratic moments m (dict on QKEYS)."""
    mx, my, mz = m[(1, 0, 0)], m[(0, 1, 0)], m[(0, 0, 1)]
    Yxx, Yyy, Yzz = m[(2, 0, 0)], m[(0, 2, 0)], m[(0, 0, 2)]
    Yxy, Yxz, Yyz = m[(1, 1, 0)], m[(1, 0, 1)], m[(0, 1, 1)]
    b = [-mx, -my, mz, -Yxy]
    t = mz - Yxz - Yyz
    B = [[Yxx, Yxy, -Yxz, Yxy],
         [Yxy, Yyy, -Yyz, Yxy],
         [-Yxz, -Yyz, Yzz, t],
         [Yxy, Yxy, t, Yxy]]
    return b, B


# ---------------------------------------------------------------------------
# Disjoint localizing matrices.
# ---------------------------------------------------------------------------
STATUSES = list(product((-1, 0, 1), repeat=3))  # -1 free, 0 -> (1-x), 1 -> x


def weight(status, one=1):
    w = const(one)
    for i, s in enumerate(status):
        if s == 1:
            w = pmul(w, var(i, one))
        elif s == 0:
            w = pmul(w, padd(const(one), pscale(var(i, one), -1)))
    return w


def localizing_polys(status, one=1):
    free = [i for i, s in enumerate(status) if s == -1]
    basis = [const(one)] + [var(i, one) for i in free]
    w = weight(status, one)
    return [[pmul(w, pmul(a, b)) for b in basis] for a in basis]


# ---------------------------------------------------------------------------
# Order simplices of the cube (exact description of P3 / K3).
# ---------------------------------------------------------------------------
def simplex_vertex_matrix(perm):
    """4x4 matrix whose columns are (1, v_k) for the order simplex
    x_{perm0} >= x_{perm1} >= x_{perm2}."""
    V = np.zeros((4, 4))
    v = np.zeros(3)
    V[0, 0] = 1
    for k in range(3):
        v[perm[k]] = 1
        V[0, k + 1] = 1
        V[1:, k + 1] = v
    return V


SIMPLICES = [simplex_vertex_matrix(p) for p in permutations(range(3))]


def hom_matrix(p):
    """Symmetric 4x4 matrix P with (1,x)^T P (1,x) = p(x)."""
    P = np.zeros((4, 4))
    P[0, 0] = p.get((0, 0, 0), 0)
    for i in range(3):
        P[0, i + 1] = P[i + 1, 0] = p.get(unit(i), 0) / 2
        e = [0, 0, 0]
        e[i] = 2
        P[i + 1, i + 1] = p.get(tuple(e), 0)
    for i in range(3):
        for j in range(i + 1, 3):
            e = [0, 0, 0]
            e[i] = e[j] = 1
            P[i + 1, j + 1] = P[j + 1, i + 1] = p.get(tuple(e), 0) / 2
    return P


def quad_from_vector(v):
    return {k: float(v[i]) for i, k in enumerate(QKEYS) if v[i] != 0}


def vector_from_quad(p):
    return np.array([float(p.get(k, 0)) for k in QKEYS])


def uniform_moments():
    """Moments of the uniform distribution on the cube (interior of K3)."""
    m = {}
    for k in QKEYS:
        val = 1.0
        for e in k:
            val *= 1.0 / (e + 1)
        m[k] = val
    return m


# ---------------------------------------------------------------------------
# Zero structure of a numerical quadratic on the cube.
# ---------------------------------------------------------------------------
def face_minimizers(p, tol=1e-7):
    """Enumerate stationary points of p restricted to the relative interior
    of every face (nonsingular case) and the vertices.  Returns a list of
    (face status tuple, point, value)."""
    P = hom_matrix(p)
    Q = P[1:, 1:]
    c = 2 * P[0, 1:]
    out = []
    for status in STATUSES:
        free = [i for i, s in enumerate(status) if s == -1]
        fixed = [i for i, s in enumerate(status) if s != -1]
        x = np.array([0.0 if s == -1 else float(s) for s in status])
        if free:
            A = 2 * Q[np.ix_(free, free)]
            rhs = -c[free] - 2 * Q[np.ix_(free, fixed)] @ x[fixed]
            try:
                sol = np.linalg.solve(A, rhs)
            except np.linalg.LinAlgError:
                continue
            if np.any(sol <= tol) or np.any(sol >= 1 - tol):
                continue
            x[free] = sol
        val = x @ Q @ x + c @ x + P[0, 0]
        out.append((status, x, val))
    return out
