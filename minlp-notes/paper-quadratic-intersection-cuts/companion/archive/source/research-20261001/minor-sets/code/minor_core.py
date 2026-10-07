"""Core routines for the minor-sets stream (research-20261001/minor-sets/note.md).

Setting.  A 2x2 minor of the product matrix X whose row and column indices i1, i2, j1, j2 are four
distinct indices (so no entry of the minor is diagonal),
    M = [[X_{i1 j1}, X_{i1 j2}], [X_{i2 j1}, X_{i2 j2}]] = [[a, b], [c, d]],
must satisfy det M = ad - bc = 0.  Coordinates s = (a, b, c, d) in R^4.
S = {det = 0} (equivalently {det <= 0} when det(sbar) > 0, see the note, Lemma 2(3)).
The LP point sbar has det(sbar) > 0 (SCIP swaps the columns otherwise).

Families of S-free sets, all of the form C_F = {M : sym(F^T M) >= 0}:
  orbit : F^T in R^{2x2}, sym(F^T Mbar) > 0          (all automorphism images of SCIP's set)
  pr    : F^T Mbar symmetric positive definite        (point rule under every transformation)
  bcm   : F^T in span{I, J}                          (Bienstock-Chen-Munoz (14a), every lambda)
  scip  : F^T = U^T, Mbar = U P polar decomposition  (SCIP's sepa_interminor / Case 1 set)
Each family is {C_F : F^T in L} for a linear space L, so the best one-cut bound of the family is
found by bisection over z with 2x2 LMIs in the coordinates of L (quasiconvexity, note Prop. 4).

The corner bound z_K is computed with the exact support-<=2 closed forms of the sfree note
(research-20260928b/sfree/code/core.py, reused unchanged) plus its generic KKT formula for
supports 3 and 4 (by Prop. 5 of the note, support >= 3 is non-generic for det).
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SFREE = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'research-20260928b', 'sfree', 'code'))
if SFREE not in sys.path:
    sys.path.insert(0, SFREE)
from core import corner_bound as _corner_bound  # noqa: E402  (sfree note, Theorem 11 machinery)

Q4 = np.zeros((4, 4))
Q4[0, 3] = Q4[3, 0] = 0.5
Q4[1, 2] = Q4[2, 1] = -0.5
B4 = np.zeros(4)
J2 = np.array([[0.0, 1.0], [-1.0, 0.0]])
I2 = np.eye(2)


def mat(s):
    return np.array([[s[0], s[1]], [s[2], s[3]]], dtype=float)


def vec(M):
    return np.array([M[0, 0], M[0, 1], M[1, 0], M[1, 1]], dtype=float)


def det4(s):
    return s[0] * s[3] - s[1] * s[2]


def symm(X):
    return 0.5 * (X + X.T)


def adj(A):
    return np.array([[A[1, 1], -A[0, 1]], [-A[1, 0], A[0, 0]]])


# --------------------------------------------------------------------------- corner bound
def zK(sbar, P, w, return_point=False):
    """z_K(w) = min{w^T lam : lam >= 0, det(sbar + P lam) <= 0} (w > 0, det(sbar) > 0)."""
    assert det4(sbar) > 0
    return _corner_bound(Q4, B4, 0.0, np.asarray(sbar, float), np.asarray(P, float),
                         np.asarray(w, float), return_point=return_point)


# --------------------------------------------------------------------------- sets C_F
def step(FT, sbar, p):
    """alpha = sup{t >= 0 : sym(F^T (Mbar + t p)) >= 0}; requires sym(F^T Mbar) > 0."""
    A = symm(FT @ mat(sbar))
    Bm = symm(FT @ mat(p))
    L = np.linalg.cholesky(A)
    Li = np.linalg.inv(L)
    mn = np.linalg.eigvalsh(Li @ Bm @ Li.T)[0]
    return np.inf if mn >= 0 else -1.0 / mn


def bound_of(FT, sbar, P, w):
    """One-cut bound z_C(w) = min_j w_j alpha_j of C_F (inf if every alpha_j is inf)."""
    vals = []
    for j in range(P.shape[1]):
        a = step(FT, sbar, P[:, j])
        if np.isfinite(a):
            vals.append(w[j] * a)
    return min(vals) if vals else np.inf


def polar_rotation(Mbar):
    """U in SO(2) with Mbar = U P, P symmetric positive definite (det Mbar > 0)."""
    Wl, sv, Vt = np.linalg.svd(Mbar)
    U = Wl @ Vt
    assert np.linalg.det(U) > 0
    return U


def family_basis(fam, sbar):
    """Basis G_1..G_k of the linear space L of F^T matrices of the family."""
    Mbar = mat(sbar)
    if fam == 'orbit':
        return [np.array(E, float) for E in ([[1, 0], [0, 0]], [[0, 1], [0, 0]], [[0, 0], [1, 0]], [[0, 0], [0, 1]])]
    if fam == 'pr':
        Mi = np.linalg.inv(Mbar)
        return [np.array(E, float) @ Mi for E in ([[1, 0], [0, 0]], [[0, 0], [0, 1]], [[0, 1], [1, 0]])]
    if fam == 'bcm':
        return [I2.copy(), J2.copy()]
    if fam == 'scip':
        return [polar_rotation(Mbar).T]
    raise ValueError(fam)


# --------------------------------------------------------------------------- SCIP's formula, literally
EIGVEC = np.array([1.0, 1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 1.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0]).reshape(4, 4)
EIGVAL = np.array([0.5, 0.5, -0.5, -0.5])
EIGCOEF = 0.7071067811865475244008443621048490


def scip_interminor_step(sbar, p):
    """Step length of sepa_interminor.c (SCIP 10.0.3, usebounds = FALSE), transcribed from
    computeRestrictionToRay() and computeRoot(): vars = (xik, xjl, xil, xjk) = (a, d, b, c).
    Returns the smallest positive root of (A - D^2) t^2 + (B - 2DE) t + (C - E^2) (inf if
    sqrt(A) <= D), without SCIP's final safeguarding binary search."""
    z = np.array([sbar[0], sbar[3], sbar[1], sbar[2]])
    r = np.array([p[0], p[3], p[1], p[2]])
    a = b = c = d = e = 0.0
    for i in range(4):
        vdotray = EIGCOEF * EIGVEC[i] @ r
        vzlp = EIGCOEF * EIGVEC[i] @ z
        if EIGVAL[i] > 0:
            d += EIGVAL[i] * vzlp * vdotray
            e += EIGVAL[i] * vzlp ** 2
        else:
            a -= EIGVAL[i] * vdotray ** 2
            b -= 2.0 * EIGVAL[i] * vzlp * vdotray
            c -= EIGVAL[i] * vzlp ** 2
    e = np.sqrt(e)
    d /= e
    if np.sqrt(a) <= d:
        return np.inf
    A2, A1, A0 = a - d * d, b - 2 * d * e, c - e * e      # A0 < 0 since phi(0) < 0
    if abs(A2) < 1e-300:
        return -A0 / A1 if A1 > 0 else np.inf
    disc = A1 * A1 - 4 * A2 * A0
    if disc < 0:
        return np.inf
    roots = sorted([(-A1 - np.sqrt(disc)) / (2 * A2), (-A1 + np.sqrt(disc)) / (2 * A2)])
    pos = [t for t in roots if t > 0]
    return pos[0] if pos else np.inf


# --------------------------------------------------------------------------- best bound of a family
class FamilySolver:
    """Bisection on z for max{z : exists F^T in L, sym(F^T Mbar) >= I, sym(F^T V_j(z)) >= 0},
    V_j(z) = Mbar + (z / w_j) p_j.  Each step solves the always-feasible margin problem
        max t  s.t.  sym(F^T Mbar) >= I,  sym(F^T V_j(z)) >= t I,  t <= 1
    (parametrized cvxpy problem, DPP) and accepts z when t >= -1e-9; Clarabel, SCS as fallback.
    The returned lower bound is always the exact one-cut bound of an explicit F (certified up to
    floating point); the bisection upper value is numerical only."""

    def __init__(self, fam, sbar, P, w, solver='CLARABEL'):
        import cvxpy as cp
        self.cp = cp
        self.fam, self.sbar, self.P, self.w = fam, np.asarray(sbar, float), np.asarray(P, float), np.asarray(w, float)
        self.basis = family_basis(fam, self.sbar)
        self.solver = solver
        k = len(self.basis)
        N = self.P.shape[1]
        self.c = cp.Variable(k)
        self.t = cp.Variable()
        self.z = cp.Parameter(nonneg=True)
        Mbar = mat(self.sbar)

        def symexpr(M):
            X = sum(self.c[i] * (self.basis[i] @ M) for i in range(k))
            return 0.5 * (X + X.T)
        A0 = symexpr(Mbar)
        cons = [A0 >> np.eye(2), self.t <= 1]
        for j in range(N):
            Bj = symexpr(mat(self.P[:, j]))
            cons.append(A0 + (self.z / self.w[j]) * Bj >> self.t * np.eye(2))
        self.prob = cp.Problem(cp.Maximize(self.t), cons)

    def feasible(self, z):
        self.z.value = float(z)
        for solver in (self.solver, 'SCS'):
            try:
                self.prob.solve(solver=solver)
            except Exception:
                continue
            if self.prob.status in ('optimal', 'optimal_inaccurate') and self.t.value is not None:
                if self.t.value >= -1e-9:
                    return sum(self.c.value[i] * self.basis[i] for i in range(len(self.basis)))
                return None
        return None

    def best(self, zhi, iters=40):
        """Returns (certified lower bound from an explicit F, bisection upper value, F^T)."""
        if self.fam == 'scip':
            FT = self.basis[0]
            v = bound_of(FT, self.sbar, self.P, self.w)
            return v, v, FT
        # shortcut: most corners are attained; test z = (1 - 1e-6) zhi first
        FT = self.feasible((1 - 1e-6) * zhi)
        if FT is not None:
            try:
                return bound_of(FT, self.sbar, self.P, self.w), zhi, FT
            except np.linalg.LinAlgError:
                pass
        lo, hi = 0.0, 1.0 - 1e-6
        bestFT = self.feasible(0.0)
        bestv = -np.inf
        for _ in range(iters):
            mid = 0.5 * (lo + hi)
            FT = self.feasible(mid * zhi)
            if FT is not None:
                lo = mid
                try:
                    v = bound_of(FT, self.sbar, self.P, self.w)
                except np.linalg.LinAlgError:
                    v = -np.inf
                if v > bestv:
                    bestv, bestFT = v, FT
            else:
                hi = mid
        cert = max(bestv, 0.0)
        if bestFT is not None and not np.isfinite(bestv):
            try:
                cert = bound_of(bestFT, self.sbar, self.P, self.w)
            except np.linalg.LinAlgError:
                cert = 0.0
        return cert, hi * zhi, bestFT


def precondition(sbar, P):
    """Automorphism M -> Mbar^{-1} M: maps sbar to I and rays to Mbar^{-1} p_j.  The orbit and the
    point-rule families are equivariant (note, Prop. 3), so their bounds are unchanged."""
    Mi = np.linalg.inv(mat(sbar))
    return vec(np.eye(2)), np.stack([vec(Mi @ mat(P[:, j])) for j in range(P.shape[1])], 1)


def bcm_best(sbar, P, w, ngrid=7200):
    """Best one-cut bound over the BCM family C_R, R = rotation by phi (F^T = cos I + sin J):
    grid over phi plus golden-section refinement.  Returns (bound of an explicit set, phi)."""
    Mbar = mat(sbar)

    def val(phi):
        FT = np.cos(phi) * I2 + np.sin(phi) * J2
        A = symm(FT @ Mbar)
        if np.linalg.eigvalsh(A)[0] <= 1e-12 * np.abs(A).max():
            return -np.inf
        return bound_of(FT, sbar, P, w)
    grid = np.linspace(0, 2 * np.pi, ngrid, endpoint=False)
    vals = np.array([val(t) for t in grid])
    best_v, best_t = -np.inf, None
    for kk in np.argsort(-vals)[:5]:
        if not np.isfinite(vals[kk]):
            continue
        lo, hi = grid[kk] - 2 * np.pi / ngrid, grid[kk] + 2 * np.pi / ngrid
        gr = (np.sqrt(5) - 1) / 2
        for _ in range(60):
            m1 = hi - gr * (hi - lo); m2 = lo + gr * (hi - lo)
            if val(m1) >= val(m2):
                hi = m2
            else:
                lo = m1
        for t in (grid[kk], 0.5 * (lo + hi)):
            v = val(t)
            if v > best_v:
                best_v, best_t = v, t
    return best_v, best_t


def family_bounds(sbar, P, w, zk, fams=('scip', 'bcm', 'pr', 'orbit'), iters=40):
    """Certified lower bounds (bound of an explicit set, min with zk), divided by zk.  For the LMI
    families also the bisection upper value ('upper', numerical)."""
    out = {}
    sbI, PI = precondition(sbar, P)
    for fam in fams:
        if fam == 'scip':
            v = bound_of(polar_rotation(mat(sbar)).T, sbar, P, w)
            out[fam] = dict(ratio=float(min(v, zk) / zk), upper=float(min(v, zk) / zk))
        elif fam == 'bcm':
            v, _ = bcm_best(sbar, P, w)
            out[fam] = dict(ratio=float(min(max(v, 0.0), zk) / zk), upper=None)
        else:
            cert, hi, FT = FamilySolver(fam, sbI, PI, w).best(zk, iters=iters)
            out[fam] = dict(ratio=float(min(cert, zk) / zk), upper=float(min(hi, zk) / zk))
    return out


# --------------------------------------------------------------------------- tangent-edge pencil
def kappa_pencil(t0, D):
    """Homogeneous tangent-edge pencil (note, Lemma 6): F_kappa^T = G0 + kappa G1 with
    G0 = s J adj(D), G1 = s J adj(M0), s = sign(c0), G0 a0 = c0 b0 where M0 = a0 b0^T."""
    M0 = mat(t0)
    Dm = mat(D)
    G0 = J2 @ adj(Dm)
    G1 = J2 @ adj(M0)
    U, sv, Vt = np.linalg.svd(M0)
    a0 = U[:, 0] * sv[0]
    b0 = Vt[0]
    c0 = (G0 @ a0) @ b0 / (b0 @ b0)
    s = 1.0 if c0 > 0 else -1.0
    return s * G0, s * G1


def nearest_orbit(sbar, P, w, z, target_FT):
    """Among orbit sets with C_F containing T_z (z <= best orbit bound), the one whose F^T is nearest
    (Frobenius) to c * target_FT, c chosen so that sym(c target^T Mbar) >= I.  Used to break ties among
    the many sets that attain the corner bound (note, Section 7.2).  Returns F^T or None."""
    import cvxpy as cp
    Mbar = mat(sbar)
    A0t = symm(target_FT @ Mbar)
    c = 1.0 / np.linalg.eigvalsh(A0t)[0]
    G = cp.Variable((2, 2))

    def se(M):
        X = G @ M
        return 0.5 * (X + X.T)
    cons = [se(Mbar) >> np.eye(2)] + [se(Mbar + (z / w[j]) * mat(P[:, j])) >> 0 for j in range(P.shape[1])]
    prob = cp.Problem(cp.Minimize(cp.norm(G - c * target_FT, 'fro')), cons)
    for solver in ('CLARABEL', 'SCS'):
        try:
            prob.solve(solver=solver)
        except Exception:
            continue
        if prob.status in ('optimal', 'optimal_inaccurate') and G.value is not None:
            return G.value
    return None
