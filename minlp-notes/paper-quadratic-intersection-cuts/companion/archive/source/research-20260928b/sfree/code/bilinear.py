"""Bilinear constraints: the det representation, the sliced orbit family (A) and its
maximal completion (B).

side '+': S = {w <= x y},  M(x,y,w;h) = [[w, x], [y, h]],  det M(s,1) = w - x y = q(s).
side '-': S = {w >= x y},  M(x,y,w;h) = [[x, w], [h, y]],  det M(s,1) = x y - w = q(s).

(A)  C_F = {s : sym(F^T M(s,1)) >= 0},  det F > 0      (all O(2,2)-images of Munoz-Serrano sets)
(B)  C_F^G = cl(C_F - sgn * R_+ e_w)                   (maximal completion; sgn = +1 for '+', -1 for '-')
     i.e. s in (B) iff exists tau >= 0 with s - sgn*tau*e_w in C_F.
"""
import numpy as np
from core import Mmat

J2 = np.array([[0.0, 1.0], [-1.0, 0.0]])
EW = np.array([0.0, 0.0, 1.0])


def sgn(side):
    return 1.0 if side == '+' else -1.0


def symm(X):
    return (X + X.T) / 2.0


def adj(A):
    return np.array([[A[1, 1], -A[0, 1]], [-A[1, 0], A[0, 0]]])


# ------------------------------------------------------------------ 2x2 pencils
def pencil_interval(A, B):
    """{t in R : A + t B >= 0} for symmetric 2x2 A, B, as (lo, hi) or None (exact up to fp)."""
    polys = [(B[0, 0], A[0, 0]), (B[1, 1], A[1, 1])]
    c2 = np.linalg.det(B); c0 = np.linalg.det(A)
    c1 = A[0, 0] * B[1, 1] + A[1, 1] * B[0, 0] - 2 * A[0, 1] * B[0, 1]
    pts = []
    for (s, c) in polys:
        if s != 0:
            pts.append(-c / s)
    if abs(c2) > 1e-300:
        disc = c1 * c1 - 4 * c2 * c0
        if disc >= 0:
            r = np.sqrt(disc)
            pts += [(-c1 - r) / (2 * c2), (-c1 + r) / (2 * c2)]
    elif c1 != 0:
        pts.append(-c0 / c1)
    pts = sorted(set(pts))
    cand = []
    if not pts:
        cand = [0.0]
    else:
        cand = [pts[0] - 1.0] + pts + [(pts[i] + pts[i + 1]) / 2 for i in range(len(pts) - 1)] + [pts[-1] + 1.0]

    def ok(t):
        X = A + t * B
        sc = 1e-11 * (1 + np.abs(A).max() + abs(t) * np.abs(B).max())
        return X[0, 0] >= -sc and X[1, 1] >= -sc and np.linalg.det(X) >= -sc * (1 + np.abs(X).max())
    good = [t for t in cand if ok(t)]
    if not good:
        return None
    lo, hi = min(good), max(good)
    # unbounded directions
    if ok(hi + 1e6 * (1 + abs(hi))):
        hi = np.inf
    if ok(lo - 1e6 * (1 + abs(lo))):
        lo = -np.inf
    return lo, hi


def exists_tau(A, B):
    """exists tau >= 0 with A + tau B >= 0 ?"""
    iv = pencil_interval(A, B)
    return iv is not None and iv[1] >= 0


# ------------------------------------------------------------------ families
def in_A(F, side, s, tol=1e-11):
    X = symm(F.T @ Mmat(side, s))
    return np.linalg.eigvalsh(X)[0] >= -tol * (1 + np.abs(X).max())


def in_B(F, side, s):
    A = symm(F.T @ Mmat(side, s))
    B = -sgn(side) * symm(F.T @ Mmat(side, EW, h=0.0))
    return exists_tau(A, B)


def step_A(F, side, sbar, p):
    A = symm(F.T @ Mmat(side, sbar)); B = symm(F.T @ Mmat(side, p, h=0.0))
    if np.linalg.eigvalsh(A)[0] <= 1e-9 * max(1.0, np.abs(A).max()):
        F = interior_shift(F, side, sbar)
        A = symm(F.T @ Mmat(side, sbar)); B = symm(F.T @ Mmat(side, p, h=0.0))
    L = np.linalg.cholesky(A); Li = np.linalg.inv(L)
    mn = np.linalg.eigvalsh(Li @ B @ Li.T)[0]
    return np.inf if mn >= 0 else -1.0 / mn


def interior_shift(F, side, sbar):
    """Return F + delta*M(sbar)^{-T} with sym(F^T M(sbar)) >= 1e-9 scale * I (the SDP
    solver may return sbar on the boundary of C_F); delta = 0 if already interior."""
    A = symm(F.T @ Mmat(side, sbar))
    lmin = np.linalg.eigvalsh(A)[0]; floor = 1e-9 * max(1.0, np.abs(A).max())
    if lmin <= floor:
        F = F + (floor - lmin) * np.linalg.inv(Mmat(side, sbar)).T
    return F


def step_B(F, side, sbar, p, amax=1e8, iters=80):
    F = interior_shift(F, side, sbar)
    if not in_B(F, side, sbar):
        return 0.0
    if in_B(F, side, sbar + amax * p):
        return np.inf
    lo, hi = 0.0, 1.0
    while in_B(F, side, sbar + hi * p):
        lo, hi = hi, 2 * hi
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if in_B(F, side, sbar + mid * p):
            lo = mid
        else:
            hi = mid
    return lo


def bound(F, side, sbar, P, w, fam='A'):
    st = step_A if fam == 'A' else step_B
    vals = []
    for j in range(P.shape[1]):
        a = st(F, side, sbar, P[:, j])
        if np.isfinite(a):
            vals.append(w[j] * a)
    return min(vals) if vals else np.inf


# ------------------------------------------------------------------ tangent-edge pencil
def kappa_pencil(side, t0, d):
    """F_kappa^T = G0 + kappa G1 (sign fixed so that sym(F^T M(t0)) is PSD)."""
    Md = Mmat(side, d, h=0.0); M0 = Mmat(side, t0)
    G0 = J2 @ adj(Md); G1 = J2 @ adj(M0)
    # Lemma 13: M0 = a0 b0^T and F^T a0 = c b0 with c > 0 (G1 a0 = 0, so c comes from G0)
    U, sv, Vt = np.linalg.svd(M0)
    a0 = U[:, 0] * sv[0]; b0 = Vt[0]
    c = (G0 @ a0) @ b0 / (b0 @ b0)
    s = 1.0 if c > 0 else -1.0
    return s * G0, s * G1


def kappa_set_A(G0, G1, side, v):
    """{kappa : sym((G0 + kappa G1) M(v)) >= 0}"""
    M = Mmat(side, v)
    return pencil_interval(symm(G0 @ M), symm(G1 @ M))


def kappa_ok_B(G0, G1, side, v, kap):
    F = (G0 + kap * G1).T
    return in_B(F, side, v)
