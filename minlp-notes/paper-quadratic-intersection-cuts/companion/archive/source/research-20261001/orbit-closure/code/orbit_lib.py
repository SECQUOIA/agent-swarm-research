"""Shared routines for the orbit-closure stream (research-20261001/orbit-closure).

Setting (side '+'):  S = {(x, y, w) : w <= x y},  q(s) = w - x y,  M(s) = [[w, x], [y, 1]],
det M(s) = q(s).  LP vertex sbar with q(sbar) > 0, projected rays p_1..p_N (columns of P),
lambda-space corner set X = {lam >= 0 : q(sbar + P lam) <= 0}.

Family (A) (sliced orbit sets):  C_F = {s : sym(F^T M(s)) >= 0}, det F > 0.
Parametrization used here (sbar in int C_F):  F^T = (S + c J) M(sbar)^{-1} with S symmetric
positive definite and c real; then sym(F^T M(sbar)) = S.  Scaling F does not change C_F, so
S is normalized to trace 1.  The point-rule (SCIP) subfamily is c = 0 (F^T M(sbar) symmetric).

Cut vector of a set C with sbar in int C:  a_j = 1/alpha_j(C) (0 if the ray stays in C).
For (A):  a_j = max(0, lambda_max(-A_j, S)) with A_j = sym((S + cJ) N_j), N_j = M(sbar)^{-1} M0(p_j),
M0(p) = [[p_w, p_x], [p_y, 0]] (linear part of M).

Family (B) (maximal completions):  B_F = cl(C_F + R_+ e_w).  sbar + mu p in B_F iff there is
tau >= 0 with sym(F^T M(sbar + mu p)) - tau sym(F^T E) >= 0, E = [[1, 0], [0, 0]].
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[7])

import sys
import numpy as np

SFREE = (_PUBLIC_REPO + '/research-20260928b/sfree/code')
if SFREE not in sys.path:
    sys.path.insert(0, SFREE)

J2 = np.array([[0.0, 1.0], [-1.0, 0.0]])
E2 = np.array([[1.0, 0.0], [0.0, 0.0]])


def M(s, h=1.0):
    x, y, w = s
    return np.array([[w, x], [y, h]], dtype=float)


def M0(p):
    return M(p, h=0.0)


def sym(X):
    return 0.5 * (X + X.T)


def qval(s):
    return s[2] - s[0] * s[1]


class Corner:
    """Corner (sbar, P) for S = {w <= xy}."""

    def __init__(self, sbar, P):
        self.sbar = np.asarray(sbar, dtype=float)
        self.P = np.asarray(P, dtype=float)
        assert qval(self.sbar) > 0
        self.N = self.P.shape[1]
        self.Ms = M(self.sbar)
        self.Msi = np.linalg.inv(self.Ms)
        self.Nj = [self.Msi @ M0(self.P[:, j]) for j in range(self.N)]
        self.NE = self.Msi @ E2

    # ---------------------------------------------------------------- F <-> (S, c)
    def FT(self, S, c):
        return (S + c * J2) @ self.Msi

    def Sc_of_F(self, F):
        X = F.T @ self.Ms
        return sym(X), 0.5 * (X[0, 1] - X[1, 0])

    # ---------------------------------------------------------------- family (A)
    def cut_A(self, S, c):
        """Cut vector a (a_j = 1/alpha_j) of C_F with F^T = (S + cJ) M(sbar)^{-1}, S > 0."""
        L = np.linalg.cholesky(S)
        Li = np.linalg.inv(L)
        G = S + c * J2
        a = np.empty(self.N)
        for j in range(self.N):
            Aj = sym(G @ self.Nj[j])
            ev = np.linalg.eigvalsh(Li @ (-Aj) @ Li.T)[-1]
            a[j] = max(0.0, ev)
        return a

    # ---------------------------------------------------------------- family (B)
    def cut_B(self, S, c, iters=60):
        """Cut vector of B_F (F^T = (S + cJ) M(sbar)^{-1}, S symmetric, not necessarily PD).
        Returns None if sbar is not in int B_F."""
        G = S + c * J2
        Z = sym(G @ self.NE)
        # sbar in int B_F  iff  exists tau0 >= 0 with S - tau0 Z > 0
        if not _exists_tau_pd(S, -Z):
            return None
        a = np.empty(self.N)
        for j in range(self.N):
            Aj = sym(G @ self.Nj[j])
            # alpha = sup{mu : exists tau >= 0, S + mu Aj - tau Z >= 0}
            def feas(mu):
                return _exists_tau_psd(S + mu * Aj, -Z)
            hi = 1.0
            if feas(1e9):
                a[j] = 0.0
                continue
            lo = 0.0
            while feas(hi):
                lo, hi = hi, 2.0 * hi
            for _ in range(iters):
                mid = 0.5 * (lo + hi)
                if feas(mid):
                    lo = mid
                else:
                    hi = mid
            a[j] = 1.0 / lo if lo > 0 else np.inf
        return a


def _pencil_roots(A, B):
    """Real t with det(A + tB) = 0 plus the zeros of the diagonal entries."""
    c2 = B[0, 0] * B[1, 1] - B[0, 1] ** 2
    c1 = A[0, 0] * B[1, 1] + A[1, 1] * B[0, 0] - 2 * A[0, 1] * B[0, 1]
    c0 = A[0, 0] * A[1, 1] - A[0, 1] ** 2
    pts = []
    if abs(c2) > 1e-300:
        disc = c1 * c1 - 4 * c2 * c0
        if disc >= 0:
            r = np.sqrt(disc)
            pts += [(-c1 - r) / (2 * c2), (-c1 + r) / (2 * c2)]
    elif c1 != 0:
        pts.append(-c0 / c1)
    for k in range(2):
        if B[k, k] != 0:
            pts.append(-A[k, k] / B[k, k])
    return pts


def _exists_tau_psd(A, B, tol=1e-12):
    """exists tau >= 0 with A + tau B PSD (2x2)."""
    pts = [0.0] + [t for t in _pencil_roots(A, B) if t > 0]
    pts = sorted(set(pts))
    cand = list(pts) + [0.5 * (pts[i] + pts[i + 1]) for i in range(len(pts) - 1)] + [pts[-1] + 1.0, 2 * pts[-1] + 1e6]
    sc = tol * (1 + np.abs(A).max() + np.abs(B).max())
    for t in cand:
        X = A + t * B
        if X[0, 0] >= -sc * (1 + t) and X[1, 1] >= -sc * (1 + t) and \
                X[0, 0] * X[1, 1] - X[0, 1] ** 2 >= -sc * (1 + t) * (1 + np.abs(X).max()):
            return True
    return False


def _exists_tau_pd(A, B):
    pts = [0.0] + [t for t in _pencil_roots(A, B) if t > 0]
    pts = sorted(set(pts))
    cand = [0.5 * (pts[i] + pts[i + 1]) for i in range(len(pts) - 1)] + [pts[-1] + 1.0, 2 * pts[-1] + 1e6, 0.0]
    for t in cand:
        X = A + t * B
        if X[0, 0] > 0 and X[0, 0] * X[1, 1] - X[0, 1] ** 2 > 0:
            return True
    return False


# -------------------------------------------------------------------- parametrization
def S_of(u):
    """Map u = (u1, u2) in the open unit disk to S > 0 with trace 1:
    S = [[1/2 + r cos/2, r sin/2], [., 1/2 - r cos/2]] with r < 1."""
    r = np.hypot(u[0], u[1])
    if r >= 1:
        return None
    return np.array([[0.5 + 0.5 * u[0], 0.5 * u[1]], [0.5 * u[1], 0.5 - 0.5 * u[0]]])


def theta_to_Sc(th):
    """Unconstrained 3-vector -> (S, c): disk coordinates via tanh squashing."""
    v = np.array(th[:2])
    n = np.hypot(*v)
    r = min(np.tanh(n), 1 - 1e-12)
    u = v * (r / n) if n > 0 else v
    return S_of(u), th[2]


def corner_bound(sbar, P, w):
    """Exact corner bound z_K(w) (support enumeration, sfree core.py)."""
    import core
    Q, b, c = core.bilinear_quadratic('+')
    return core.corner_bound(Q, b, c, np.asarray(sbar, float), np.asarray(P, float), np.asarray(w, float),
                             return_point=True)


# -------------------------------------------------------------------- family (B), closed form
def _isotropic(Z, tol=1e-14):
    """Unit vectors v with v^T Z v = 0 (Z symmetric 2x2): 0, 1, 2 directions or None if Z = 0."""
    a, b, c = Z[0, 0], Z[0, 1], Z[1, 1]
    sc = max(abs(a), abs(b), abs(c))
    if sc == 0:
        return None
    a, b, c = a / sc, b / sc, c / sc
    out = []
    # v = (cos t, sin t): a cos^2 + 2 b cos sin + c sin^2 = 0
    if abs(a) < tol:
        out.append(np.array([1.0, 0.0]))
        if abs(c) > tol:
            # 2b cos + c sin = 0 with sin != 0
            v = np.array([c, -2 * b]); out.append(v / np.linalg.norm(v))
        return out
    disc = b * b - a * c
    if disc < -tol:
        return []
    disc = max(disc, 0.0)
    for sgn in (1, -1):
        # v = (x, 1): a x^2 + 2 b x + c = 0
        x = (-b + sgn * np.sqrt(disc)) / a
        v = np.array([x, 1.0]); out.append(v / np.linalg.norm(v))
    return out


def stepB_closed(S, A, Z):
    """alpha = sup{mu >= 0 : exists tau >= 0 with S + mu A - tau Z >= 0}, assuming sbar in int B_F
    (S - tau0 Z > 0 for some tau0 >= 0).  Uses the kept-inequality description
    B_F = {s : v^T A(s) v >= 0 for all v with v^T Z v >= 0}: alpha is the infimum of
    v^T S v / (-v^T A v) over kept v with v^T A v < 0, attained at an isotropic direction of Z or at a
    generalized eigenvector of (S, A) that is kept."""
    cands = []
    iso = _isotropic(Z)
    if iso is not None:
        cands += iso
    # generalized eigenvectors: (S + r A) v = 0  <=>  det(S + r A) = 0
    c2 = A[0, 0] * A[1, 1] - A[0, 1] ** 2
    c1 = S[0, 0] * A[1, 1] + S[1, 1] * A[0, 0] - 2 * S[0, 1] * A[0, 1]
    c0 = S[0, 0] * S[1, 1] - S[0, 1] ** 2
    rs = []
    if abs(c2) > 1e-300:
        disc = c1 * c1 - 4 * c2 * c0
        if disc >= 0:
            rs += [(-c1 - np.sqrt(disc)) / (2 * c2), (-c1 + np.sqrt(disc)) / (2 * c2)]
    elif c1 != 0:
        rs.append(-c0 / c1)
    for r in rs:
        G = S + r * A
        # kernel vector of the (near-)singular 2x2 G
        if abs(G[0, 0]) + abs(G[0, 1]) >= abs(G[1, 1]) + abs(G[0, 1]):
            v = np.array([-G[0, 1], G[0, 0]])
        else:
            v = np.array([G[1, 1], -G[0, 1]])
        nv = np.linalg.norm(v)
        if nv > 0:
            cands.append(v / nv)
    best = np.inf
    zs = 1e-12 * max(1.0, np.abs(Z).max())
    for v in cands:
        if iso is not None and v @ Z @ v < -zs:
            continue                      # not kept
        av = v @ A @ v
        if av < 0:
            best = min(best, (v @ S @ v) / (-av))
    if iso is None or len(iso) == 0:
        # Z definite (or zero): if Z > 0 every v is kept, the generalized-eigenvector candidates cover it;
        # if Z < 0 no v is kept and B_F is everything (cannot happen for sbar outside S); return as is
        pass
    return best


def sbar_in_int_B(S, Z):
    return _exists_tau_pd(S, -Z)


def cut_B_fast(cn, S, c, require_det=True):
    """Cut vector of B_F with F^T = (S + cJ) M(sbar)^{-1}; None if sbar not in int B_F or
    (require_det) det F <= 0, i.e. det S + c^2 <= 0 (F outside the orbit)."""
    if require_det and S[0, 0] * S[1, 1] - S[0, 1] ** 2 + c * c <= 0:
        return None
    G = S + c * J2
    Z = sym(G @ cn.NE)
    if not sbar_in_int_B(S, Z):
        return None
    a = np.empty(cn.N)
    for j in range(cn.N):
        Aj = sym(G @ cn.Nj[j])
        al = stepB_closed(S, Aj, Z)
        a[j] = 0.0 if not np.isfinite(al) else (1.0 / al if al > 0 else np.inf)
    return a


Corner.cut_B_fast = cut_B_fast
