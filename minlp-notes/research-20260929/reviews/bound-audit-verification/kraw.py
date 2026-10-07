"""Own Krawczyk existence test for a square subsystem of an OSIL model.

Setting. x0 is a point (Fractions). A set S of equality rows and a set B of
basic continuous variables with |S| = |B| are chosen; every other variable is
fixed exactly at its value in x0 (after optional snapping to bounds and
rounding of integers). F(x_B) = rows_S(x_B, x_N) - rhs_S.

Center c is a float vector (so X = [c - r, c + r] has exact endpoints).
Krawczyk: K(X) = c - R F(c) + (I - R J(X)) (X - c). If
  |R F(c)| + |I - R J(X)| r < r  (componentwise, rigorously bounded)
then X contains a zero of F (and exactly one), by Krawczyk's theorem.
J(X) is the interval Jacobian from forward-mode AD in outward-rounded
rational interval arithmetic (ivl). Floating-point matrix products use the
a-priori bound |fl(AB) - AB| <= gamma_k |A||B| (valid for any summation order,
with or without FMA), with a safety factor 2 and underflow terms.

After the test, every row not in S and every bound/integrality condition is
checked over X (rows by interval evaluation, exact for fixed values), and the
objective is enclosed over X.
"""
import math
import time
from fractions import Fraction as F

import numpy as np
import scipy.linalg as sla

import ad
import ivl
import osil

U = 2.0 ** -53
ETA = 2.0 ** -1074


def gamma(k):
    return k * U / (1 - k * U)


def fup(q):
    """Float >= Fraction q."""
    f = float(q)
    if F(f) < q:
        f = math.nextafter(f, math.inf)
    return f


def fdn(q):
    f = float(q)
    if F(f) > q:
        f = math.nextafter(f, -math.inf)
    return f


def mm(A, B):
    """Return (P, E): exact A@B lies in P +- E (entrywise)."""
    k = A.shape[1]
    P = A @ B
    S = np.abs(A) @ np.abs(B)
    g = gamma(k)
    E = 2 * g * (S + k * ETA) + 2 * k * ETA
    return P, E


def mm_nonneg_up(A, B):
    """Upper bound of exact A@B for A, B >= 0."""
    P, E = mm(A, B)
    return P + E


def rhs_of(M, i):
    lb, ub = M.clb[i], M.cub[i]
    assert lb is not None and ub is not None and lb == ub, f"row {M.cname[i]} not an equality"
    return lb


class System:
    def __init__(self, M, xN, S, B, sides=None):
        """sides: optional {row: 'lb'|'ub'} for inequality rows held active."""
        self.M, self.S, self.B = M, list(S), list(B)
        self.xN = list(xN)  # full vector; entries in B are overwritten
        self.Bset = set(B)
        self.col = {j: k for k, j in enumerate(B)}
        sides = sides or {}
        self.rhs = [(M.clb[i] if sides[i] == "lb" else M.cub[i]) if i in sides else rhs_of(M, i) for i in S]

    def full(self, xB):
        x = list(self.xN)
        for k, j in enumerate(self.B):
            x[j] = xB[k]
        return x

    def F_float(self, cB):
        x = self.full([float(v) for v in cB])
        x = [float(v) for v in x]
        n = len(self.S)
        Fv = np.zeros(n)
        J = np.zeros((n, n))
        for k, i in enumerate(self.S):
            v, g = ad.row(self.M, i, x, ad.FloatT, self.Bset)
            Fv[k] = v - float(self.rhs[k])
            for j, d in g.items():
                J[k, self.col[j]] += d
        return Fv, J

    def F_encl(self, cB):
        """Enclosure of F at the float point cB: returns (Fm, Fr) floats."""
        x = self.full([F(float(v)) for v in cB])
        n = len(self.S)
        Fm, Fr = np.zeros(n), np.zeros(n)
        for k, i in enumerate(self.S):
            if osil.is_algebraic(self.M.nl[i]):
                v = osil.row_exact(self.M, i, x) - self.rhs[k]
                lo = hi = v
            else:
                iv = osil.row_iv(self.M, i, x)
                lo, hi = iv.lo - self.rhs[k], iv.hi - self.rhs[k]
            m = float((lo + hi) / 2)
            Fm[k] = m
            Fr[k] = fup(max(hi - F(m), F(m) - lo))
        return Fm, Fr

    def J_encl(self, X):
        """Interval Jacobian over box X (list of ivl.I for basic vars)."""
        x = self.full(X)
        n = len(self.S)
        Jm, Jr = np.zeros((n, n)), np.zeros((n, n))
        for k, i in enumerate(self.S):
            _, g = ad.row(self.M, i, x, ad.IvT, self.Bset)
            for j, d in g.items():
                c = self.col[j]
                m = float((d.lo + d.hi) / 2)
                Jm[k, c] = m
                Jr[k, c] = fup(max(d.hi - F(m), F(m) - d.lo))
        return Jm, Jr


def newton(sysm, c0, iters=30, exact_iters=3, log=print):
    c = np.array([float(v) for v in c0])
    for it in range(iters):
        Fv, J = sysm.F_float(c)
        dx = np.linalg.solve(J, Fv)
        c = c - dx
        rel = np.max(np.abs(dx) / np.maximum(np.abs(c), 1e-300))
        if rel < 1e-15:
            break
    for it in range(exact_iters):
        Fm, Fr = sysm.F_encl(c)
        _, J = sysm.F_float(c)
        dx = np.linalg.solve(J, Fm)
        c = c - dx
        log(f"  exact-residual Newton {it}: max|F|={np.max(np.abs(Fm)):.3e} max|dx|/|c|={np.max(np.abs(dx)/np.maximum(np.abs(c),1e-300)):.3e}")
    return c


def krawczyk(sysm, c, r, log=print):
    """Return (ok, X, info). c, r float arrays."""
    n = len(c)
    X = [ivl.I(F(float(c[k])) - F(float(r[k])), F(float(c[k])) + F(float(r[k]))) for k in range(n)]
    t0 = time.time()
    Fm, Fr = sysm.F_encl(c)
    Jm, Jr = sysm.J_encl(X)
    t1 = time.time()
    R = np.linalg.inv(Jm)
    aR = np.abs(R)
    P1, E1 = mm(R, Fm[:, None])
    t1v = np.abs(P1[:, 0]) + E1[:, 0]
    t2v = mm_nonneg_up(aR, Fr[:, None])[:, 0]
    P3, E3 = mm(R, Jm)
    C = np.eye(n) - P3
    Cabs = np.abs(C) * (1 + 4 * U) + E3
    t3v = mm_nonneg_up(Cabs, r[:, None])[:, 0]
    v = mm_nonneg_up(Jr, r[:, None])
    t4v = mm_nonneg_up(aR, v)[:, 0]
    T = (t1v + t2v + t3v + t4v) * (1 + 1e-12)
    ratio = T / r
    info = dict(max_ratio=float(np.max(ratio)), resid_term=float(np.max(t1v / r)),
                contraction=float(np.max((t3v + t4v) / r)), time_encl=t1 - t0)
    ok = bool(np.all(T < r))
    return ok, X, info


def box_check(M, sysm, X, check_rows=None):
    """Check every row not in S, all bounds and integrality over X.

    Returns (ok, failures, objective enclosure)."""
    x = sysm.full(X)
    fails = []
    inS = set(sysm.S)
    rows = range(M.m) if check_rows is None else check_rows
    for i in rows:
        if i in inS:
            continue
        vs = osil.row_vars(M, i)
        if not (vs & sysm.Bset) and osil.is_algebraic(M.nl[i]):
            v = osil.row_exact(M, i, x)
            lo = hi = v
        else:
            iv = osil.row_iv(M, i, x)
            lo, hi = iv.lo, iv.hi
        if M.clb[i] is not None and lo < M.clb[i]:
            fails.append(("row lb", M.cname[i], float(M.clb[i] - lo)))
        if M.cub[i] is not None and hi > M.cub[i]:
            fails.append(("row ub", M.cname[i], float(hi - M.cub[i])))
    for j in range(M.n):
        v = x[j]
        lo, hi = (v.lo, v.hi) if isinstance(v, ivl.I) else (v, v)
        if M.lb[j] is not None and lo < M.lb[j]:
            fails.append(("var lb", M.vname[j], float(M.lb[j] - lo)))
        if M.ub[j] is not None and hi > M.ub[j]:
            fails.append(("var ub", M.vname[j], float(hi - M.ub[j])))
        if M.vtype[j] in ("B", "I"):
            if isinstance(v, ivl.I) or v.denominator != 1:
                fails.append(("int", M.vname[j], 0.0))
    ob = osil.obj_iv(M, x)
    return (not fails), fails, ob


def choose_basis(M, S, cand, x0, log=print):
    """QR with column pivoting on the row-equilibrated Jacobian."""
    xf = [float(v) for v in x0]
    cand = list(cand)
    cs = set(cand)
    col = {j: k for k, j in enumerate(cand)}
    J = np.zeros((len(S), len(cand)))
    for k, i in enumerate(S):
        _, g = ad.row(M, i, xf, ad.FloatT, cs)
        for j, d in g.items():
            J[k, col[j]] += d
    rs = np.max(np.abs(J), axis=1)
    assert np.all(rs > 0), "row without candidate variables"
    J = J / rs[:, None]
    Q, Rq, piv = sla.qr(J, mode="economic", pivoting=True)
    d = np.abs(np.diag(Rq))
    log(f"  basis: {len(S)} rows, {len(cand)} candidates, |R_kk| range [{d.min():.3e}, {d.max():.3e}]")
    return [cand[p] for p in piv[:len(S)]], d
