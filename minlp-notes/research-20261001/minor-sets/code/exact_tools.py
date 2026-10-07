"""Exact rational tools for the minor-sets certificates (Python fractions only).

Points of R^4 are 4-tuples (a, b, c, d) <-> M = [[a, b], [c, d]], det = ad - bc.
Polar form of det: B(X, Y) = (1/2) tr(adj(X) Y), det(X) = B(X, X).
"""
import itertools
from fractions import Fraction as Fr

import numpy as np


def F(x):
    """Exact Fraction from int / str / Fraction (floats only if they are dyadic-exact)."""
    if isinstance(x, Fr):
        return x
    if isinstance(x, str):
        return Fr(x)
    if isinstance(x, int):
        return Fr(x)
    return Fr(x)        # exact binary value of the float


def vecF(v):
    return tuple(F(x) for x in v)


def det4(s):
    return s[0] * s[3] - s[1] * s[2]


def polar(s, t):
    """B(s, t) = (1/2)(a_s d_t + d_s a_t - b_s c_t - c_s b_t)."""
    return Fr(1, 2) * (s[0] * t[3] + s[3] * t[0] - s[1] * t[2] - s[2] * t[1])


def grad_det(s):
    """Gradient of det at s in coordinates (a, b, c, d): (d, -c, -b, a)."""
    return (s[3], -s[2], -s[1], s[0])


def dot(u, v):
    return sum(x * y for x, y in zip(u, v))


def add(u, v, cu=1, cv=1):
    return tuple(cu * x + cv * y for x, y in zip(u, v))


def m2(s):
    return [[s[0], s[1]], [s[2], s[3]]]


def mmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def mT(A):
    return [list(r) for r in zip(*A)]


def msym(A):
    return [[A[0][0], (A[0][1] + A[1][0]) / 2], [(A[0][1] + A[1][0]) / 2, A[1][1]]]


def madj(A):
    return [[A[1][1], -A[0][1]], [-A[1][0], A[0][0]]]


def mdet(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def madd(A, B, ca=1, cb=1):
    return [[ca * A[i][j] + cb * B[i][j] for j in range(2)] for i in range(2)]


def is_pd(Y):
    return Y[0][0] > 0 and mdet(Y) > 0


def is_psd(Y):
    return Y[0][0] >= 0 and Y[1][1] >= 0 and mdet(Y) >= 0


def solve_linear(A, b):
    """Unique solution of A x = b over Q (list of lists of Fractions), or None if singular."""
    n = len(A)
    M = [list(map(F, A[i])) + [F(b[i])] for i in range(n)]
    for col in range(n):
        piv = next((r for r in range(col, n) if M[r][col] != 0), None)
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [x / pv for x in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[col])]
    return [M[i][n] for i in range(n)]


def min_det_over_simplex(verts):
    """Exact minimum of det over conv(verts): enumerate faces, solve the face KKT system
    2 H_FF lam = mu 1, 1^T lam = 1 exactly.  Singular faces are skipped: on a singular face the
    stationary points form an affine set on which det is constant, so the face minimum is also
    attained on a lower-dimensional face (enumerated separately).  Also valid for the convex hull
    of more than five points: every point lies in a face of a sub-simplex (Caratheodory), those faces
    are among the enumerated subsets, and affinely dependent subsets give singular systems.
    Returns (min value, list of (face, lam, point) attaining it)."""
    n = len(verts)
    H = [[polar(verts[i], verts[j]) for j in range(n)] for i in range(n)]
    cands = []
    for r in range(1, n + 1):
        for face in itertools.combinations(range(n), r):
            if r == 1:
                lamF = [Fr(1)]
            else:
                A = [[2 * H[i][j] for j in face] + [Fr(-1)] for i in face] + [[Fr(1)] * r + [Fr(0)]]
                b = [Fr(0)] * r + [Fr(1)]
                sol = solve_linear(A, b)
                if sol is None:
                    continue
                lamF = sol[:r]
                if any(x <= 0 for x in lamF):
                    continue
            pt = tuple(sum(lamF[k] * verts[face[k]][c] for k in range(r)) for c in range(4))
            cands.append((det4(pt), face, tuple(lamF), pt))
    m = min(c[0] for c in cands)
    return m, [c for c in cands if c[0] == m]


def rationalize(x, den=10 ** 6):
    return Fr(x).limit_denominator(den)


def rat_matrix(A, den=10 ** 6):
    return [[rationalize(A[i][j], den) for j in range(len(A[0]))] for i in range(len(A))]


# ----------------------------------------------------------------------------- family brackets
def _solve(prob):
    """Clarabel, then SCS; True if a solution was returned (the certificates are checked exactly)."""
    for solver in ('CLARABEL', 'SCS'):
        try:
            prob.solve(solver=solver)
        except Exception:
            continue
        if prob.status in ('optimal', 'optimal_inaccurate'):
            return True
    return False


def family_constraint_ok(basis, coef, sbar, verts):
    """Exact check: F^T = sum coef_i basis_i has sym(F^T sbar) PD and sym(F^T v) PSD at all verts."""
    FT = [[sum(coef[i] * basis[i][r][c] for i in range(len(basis))) for c in range(2)] for r in range(2)]
    if not is_pd(msym(mmul(FT, m2(sbar)))):
        return False, FT
    return all(is_psd(msym(mmul(FT, m2(v)))) for v in verts), FT


def lower_certificate(basis, sbar, P, w, z, den=10 ** 8, margin=1e-7):
    """Find a rational F^T in span(basis) whose set contains T_z (exactly checked).
    Numerical SDP with margin, then rounding.  Returns (ok, FT)."""
    import cvxpy as cp
    k = len(basis)
    Bn = [np.array([[float(x) for x in r] for r in G]) for G in basis]
    sbn = np.array([float(x) for x in sbar])
    verts = [tuple(sbar[c] + z / w[j] * P[j][c] for c in range(4)) for j in range(len(P))]
    vn = [np.array([float(x) for x in v]) for v in verts]
    M = lambda s: np.array([[s[0], s[1]], [s[2], s[3]]])
    c = cp.Variable(k)
    t = cp.Variable()

    def se(s):
        X = sum(c[i] * (Bn[i] @ M(s)) for i in range(k))
        return 0.5 * (X + X.T)
    cons = [se(sbn) >> np.eye(2)] + [se(v) >> t * np.eye(2) for v in vn] + [t <= 1]
    prob = cp.Problem(cp.Maximize(t), cons)
    if not _solve(prob):
        return False, None
    if c.value is None:
        return False, None
    coef = [rationalize(x, den) for x in c.value]
    ok, FT = family_constraint_ok(basis, coef, sbar, verts)
    return ok, FT


def upper_certificate(basis, sbar, P, w, z, den=10 ** 8):
    """Rational positive definite Y_v (v over the vertices of T_z, including sbar) with
    sum_v tr(G_i V Y_v) = 0 for every basis element G_i (exactly).  If it exists, no nonzero
    F^T in span(basis) has sym(F^T V) PSD at all vertices.  Returns (ok, Ys)."""
    import cvxpy as cp
    verts = [tuple(sbar)] + [tuple(sbar[c] + z / w[j] * P[j][c] for c in range(4)) for j in range(len(P))]
    nv = len(verts)
    Bn = [np.array([[float(x) for x in r] for r in G]) for G in basis]
    Vn = [np.array([[float(v[0]), float(v[1])], [float(v[2]), float(v[3])]]) for v in verts]
    Ys = [cp.Variable((2, 2), symmetric=True) for _ in range(nv)]
    t = cp.Variable()
    cons = [Y >> t * np.eye(2) for Y in Ys] + [sum(cp.trace(Y) for Y in Ys) == 1]
    for G in Bn:
        cons.append(sum(cp.trace(G @ Vn[v] @ Ys[v]) for v in range(nv)) == 0)
    prob = cp.Problem(cp.Maximize(t), cons)
    if not _solve(prob):
        return False, None
    if Ys[0].value is None or t.value is None or t.value <= 0:
        return False, None
    # round coarsely, then restore the linear equations exactly by solving for k pivot unknowns
    Vq = [m2(v) for v in verts]
    rows = []
    for G in basis:
        row = []
        for v in range(nv):
            GV = mmul(G, Vq[v])
            # tr(GV Y) = GV00 y00 + (GV01 + GV10) y01 + GV11 y11
            row += [GV[0][0], GV[0][1] + GV[1][0], GV[1][1]]
        rows.append(row)
    k = len(rows)
    scale = max(abs(Y.value).max() for Y in Ys)
    for dd in (10 ** 2, 10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, den):
        x = []
        for Y in Ys:
            x += [Fr(int(round(Y.value[0, 0] / scale * dd)), dd), Fr(int(round(Y.value[0, 1] / scale * dd)), dd),
                  Fr(int(round(Y.value[1, 1] / scale * dd)), dd)]
        r = [dot(row, x) for row in rows]
        # pivot columns: greedy, so that the k x k submatrix is nonsingular
        Af = np.array([[float(v) for v in row] for row in rows])
        piv = []
        for col in range(len(x)):
            if np.linalg.matrix_rank(Af[:, piv + [col]], tol=1e-9) == len(piv) + 1:
                piv.append(col)
            if len(piv) == k:
                break
        if len(piv) < k:
            return False, None
        sub = [[rows[i][c] for c in piv] for i in range(k)]
        delta = solve_linear(sub, [-ri for ri in r])
        if delta is None:
            continue
        for c, dl in zip(piv, delta):
            x[c] += dl
        assert all(dot(row, x) == 0 for row in rows)
        Yq = [[[x[3 * v], x[3 * v + 1]], [x[3 * v + 1], x[3 * v + 2]]] for v in range(nv)]
        if all(is_pd(Y) for Y in Yq):
            return True, Yq
    return False, None


ORBIT_BASIS = [[[Fr(1), Fr(0)], [Fr(0), Fr(0)]], [[Fr(0), Fr(1)], [Fr(0), Fr(0)]],
               [[Fr(0), Fr(0)], [Fr(1), Fr(0)]], [[Fr(0), Fr(0)], [Fr(0), Fr(1)]]]
BCM_BASIS = [[[Fr(1), Fr(0)], [Fr(0), Fr(1)]], [[Fr(0), Fr(1)], [Fr(-1), Fr(0)]]]


def pr_basis(sbar):
    Mi = madj(m2(sbar))
    dt = det4(sbar)
    Mi = [[x / dt for x in r] for r in Mi]
    return [mmul(E, Mi) for E in ([[Fr(1), Fr(0)], [Fr(0), Fr(0)]], [[Fr(0), Fr(0)], [Fr(0), Fr(1)]],
                                  [[Fr(0), Fr(1)], [Fr(1), Fr(0)]])]
