"""Reviewer's independent implementation (review round 1).

Does not import any code of the stream.  Polynomials are dicts
{exponent tuple: coefficient}.  Quadratic coefficient vectors use the order
QK = [1, x, y, z, x^2, y^2, z^2, xy, xz, yz].

Objects:
  R_D : moment functionals l on V (20 monomials, at most one exponent 2),
        l(1) = 1, all 27 localizing matrices l(w_{A,B} v v^T) PSD.
  R   : R_D plus the family LMI [[1, b^T], [b, B - N]] >= 0, N >= 0, diag N = 0
        for each of the 24 copies (family note, research-20260925).
  P3+ : exact description by the six order simplices, COP_4 = PSD + NN.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
from itertools import permutations, product

import cvxpy as cp
import numpy as np

QK = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (2, 0, 0), (0, 2, 0), (0, 0, 2),
      (1, 1, 0), (1, 0, 1), (0, 1, 1)]
VK = [a for a in product(range(3), repeat=3) if sum(1 for t in a if t == 2) <= 1]
assert len(VK) == 20
OPTS = dict(solver="CLARABEL", tol_gap_abs=1e-9, tol_gap_rel=1e-9, tol_feas=1e-9, max_iter=400)


def e(i):
    return tuple(1 if j == i else 0 for j in range(3))


def mul(p, q):
    out = {}
    for a, u in p.items():
        for b, v in q.items():
            k = tuple(s + t for s, t in zip(a, b))
            out[k] = out.get(k, 0) + u * v
    return {k: v for k, v in out.items() if v != 0}


def add(p, q, c=1):
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, 0) + c * v
    return {k: v for k, v in out.items() if v != 0}


ONE = {(0, 0, 0): 1}


def X(i):
    return {e(i): 1}


def OMX(i):
    return {(0, 0, 0): 1, e(i): -1}


def weight(A, B):
    w = ONE
    for i in A:
        w = mul(w, X(i))
    for j in B:
        w = mul(w, OMX(j))
    return w


def statuses():
    """All 27 (A, B, free) splits of {0,1,2}."""
    out = []
    for s in product(range(3), repeat=3):  # 0 free, 1 in A, 2 in B
        A = [i for i in range(3) if s[i] == 1]
        B = [i for i in range(3) if s[i] == 2]
        F = [i for i in range(3) if s[i] == 0]
        out.append((A, B, F))
    return out


def quad_poly(c):
    return {k: v for k, v in zip(QK, c) if v != 0}


def moment_relaxation(family=True):
    """Return (l, cons): l is a cvxpy vector indexed by VK."""
    l = cp.Variable(len(VK))
    idx = {k: i for i, k in enumerate(VK)}

    def L(poly):
        return sum(v * l[idx[k]] for k, v in poly.items())
    cons = [l[idx[(0, 0, 0)]] == 1]
    for A, B, F in statuses():
        w = weight(A, B)
        basis = [ONE] + [X(f) for f in F]
        n = len(basis)
        M = cp.bmat([[L(mul(w, mul(basis[a], basis[b]))) for b in range(n)] for a in range(n)])
        cons.append(M >> 0)
    if family:
        for g in family_copies():
            u = [g_coord(g, i) for i in range(3)]   # u_i as affine polys in x
            m = [L(u[i]) for i in range(3)]
            Y = [[L(mul(u[i], u[j])) for j in range(3)] for i in range(3)]
            b = [-m[0], -m[1], m[2], -Y[0][1]]
            Bm = [[Y[0][0], Y[0][1], -Y[0][2], Y[0][1]],
                  [Y[0][1], Y[1][1], -Y[1][2], Y[0][1]],
                  [-Y[0][2], -Y[1][2], Y[2][2], m[2] - Y[0][2] - Y[1][2]],
                  [Y[0][1], Y[0][1], m[2] - Y[0][2] - Y[1][2], Y[0][1]]]
            N = cp.Variable((4, 4), symmetric=True)
            cons += [N >= 0, cp.diag(N) == 0]
            top = [[1.0 + 0 * l[0]] + b]
            rows = top + [[b[i]] + [Bm[i][j] - N[i, j] for j in range(4)] for i in range(4)]
            cons.append(cp.bmat([[cp.reshape(t, (1, 1), order='F') if not isinstance(t, float) else t
                                  for t in r] for r in rows]) >> 0)
    return l, idx, cons


def g_coord(g, i):
    """g = (perm, comp): u_i = x_{perm[i]} or 1 - x_{perm[i]}."""
    perm, comp = g
    return OMX(perm[i]) if comp[i] else X(perm[i])


def family_copies():
    """24 copies: q(u(x)) with u_i = x_perm[i] or 1 - x_perm[i]; the swap of
    u_0, u_1 gives the same copy, so keep perm[0] < perm[1]."""
    out = []
    for perm in permutations(range(3)):
        if perm[0] > perm[1]:
            continue
        for comp in product((0, 1), repeat=3):
            out.append((perm, comp))
    assert len(out) == 24
    return out


class MinOver:
    def __init__(self, family):
        self.l, self.idx, cons = moment_relaxation(family)
        self.c = cp.Parameter(10)
        obj = sum(self.c[i] * self.l[self.idx[k]] for i, k in enumerate(QK))
        self.prob = cp.Problem(cp.Minimize(obj), cons)

    def __call__(self, c):
        self.c.value = np.asarray(c, float)
        v = self.prob.solve(**OPTS)
        return v, self.prob.status

    def quad_moments(self):
        return np.array([self.l.value[self.idx[k]] for k in QK])


def hom(c):
    """4x4 matrix Qh with p(x) = (1,x)^T Qh (1,x)."""
    c0, cx, cy, cz, cxx, cyy, czz, cxy, cxz, cyz = c
    return [[c0, cx / 2, cy / 2, cz / 2], [cx / 2, cxx, cxy / 2, cxz / 2],
            [cy / 2, cxy / 2, cyy, cyz / 2], [cz / 2, cxz / 2, cyz / 2, czz]]


def simplex_vertex_mats():
    mats = []
    for perm in permutations(range(3)):
        verts = [np.zeros(3)]
        v = np.zeros(3)
        for i in perm:
            v = v.copy(); v[i] = 1; verts.append(v)
        V = np.array([[1.0] + list(vv) for vv in verts]).T  # columns (1, v_j)
        mats.append(V)
    return mats


UNIFORM = np.array([1, .5, .5, .5, 1 / 3, 1 / 3, 1 / 3, .25, .25, .25])


class SepP3plus:
    """min <q, y> over q in P3+ (optionally with sign constraints on the cross
    coefficients), normalized by <q, uniform moments> = 1."""

    def __init__(self, cross_sign=None, diag_nonneg=True):
        self.q = cp.Variable(10)
        self.y = cp.Parameter(10)
        cons = [self.q @ UNIFORM == 1]
        if diag_nonneg:
            cons += [self.q[4] >= 0, self.q[5] >= 0, self.q[6] >= 0]
        if cross_sign == 'sub':
            cons += [self.q[7] <= 0, self.q[8] <= 0, self.q[9] <= 0]
        if cross_sign == 'sup':
            cons += [self.q[7] >= 0, self.q[8] >= 0, self.q[9] >= 0]
        Qh = cp.bmat(hom([self.q[i] for i in range(10)]))
        for V in simplex_vertex_mats():
            N = cp.Variable((4, 4), symmetric=True)
            cons += [N >= 0, V.T @ Qh @ V - N >> 0]
        self.prob = cp.Problem(cp.Minimize(self.q @ self.y), cons)

    def __call__(self, y):
        self.y.value = np.asarray(y, float)
        v = self.prob.solve(**OPTS)
        return v, self.prob.status, self.q.value


def eval_quad(c, x):
    x0, x1, x2 = x
    return float(np.dot(c, [1, x0, x1, x2, x0 * x0, x1 * x1, x2 * x2, x0 * x1, x0 * x2, x1 * x2]))


def cube_min(c):
    """Minimum of a quadratic over [0,1]^3 by enumerating the 27 faces: on each
    face solve grad = 0 in the free coordinates when the restricted Hessian is
    nonsingular.  (When it is singular and the minimum is attained in the
    relative interior, a line of minimizers reaches a lower face, so lower
    faces cover that case.)"""
    Qh = np.array(hom(c), float)
    H = 2 * Qh[1:, 1:]
    g0 = 2 * Qh[1:, 0]
    best = np.inf
    for s in product((0, 1, None), repeat=3):
        F = [i for i in range(3) if s[i] is None]
        x = np.array([0.0 if t is None else float(t) for t in s])
        if F:
            HF = H[np.ix_(F, F)]
            if abs(np.linalg.det(HF)) < 1e-13:
                continue
            rhs = -(g0[F] + H[np.ix_(F, [i for i in range(3) if i not in F])] @ x[[i for i in range(3) if i not in F]]) \
                if len(F) < 3 else -g0
            xf = np.linalg.solve(HF, rhs)
            if np.any(xf < -1e-12) or np.any(xf > 1 + 1e-12):
                continue
            x[F] = np.clip(xf, 0, 1)
        best = min(best, eval_quad(c, x))
    return best
