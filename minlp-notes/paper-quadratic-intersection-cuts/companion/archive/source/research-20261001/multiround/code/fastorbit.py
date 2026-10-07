"""Fast best-orbit bisection for bilinear terms (family (A) of the sfree note).

Same mathematics as research-20260928b/sfree/code/core.py:best_orbit_bound, which builds
each bisection step with cvxpy:  minimize ||F||_F  s.t.  sym(F^T M(sbar)) >= I  and
sym(F^T M(v_j)) >= 0 at the vertices v_j = sbar + (z/w_j) p_j.  Here the 2x2 LMIs are
written as 3-dimensional second-order cones and passed to Clarabel directly, which
removes the cvxpy overhead (about 50x faster).  The minimum-norm F is unique (strictly
convex objective), so both implementations return the same F up to solver tolerance;
code/check_fastorbit.py compares them.

Also provides a weighted variant: any positive weight vector u can replace w ("which
corner bound is maximized"), which is how the perturbed and geometric rules are built.
"""
import os
import sys
import numpy as np
import scipy.sparse as sp
import clarabel

SFREE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..',
                     'research-20260928b', 'sfree', 'code')
sys.path.insert(0, os.path.abspath(SFREE))
from core import Mmat  # noqa: E402
from core import orbit_feasible as _core_orbit_feasible  # noqa: E402

FALLBACK = [0]   # number of bisection steps solved by the cvxpy fallback

_SET = clarabel.DefaultSettings()
_SET.verbose = False


def _lin_sym(side, s, h=1.0):
    """Linear map f=(F11,F12,F21,F22) -> (a, b, c) with sym(F^T M(s,h)) = [[a,b],[b,c]]."""
    M = Mmat(side, s, h)
    L = np.zeros((3, 4))
    # (F^T M)_{ab} = sum_c F_{c a} M_{c b};  F_{ca} -> index 2c+a
    def coef(a, b):
        row = np.zeros(4)
        for c in range(2):
            row[2 * c + a] += M[c, b]
        return row
    L[0] = coef(0, 0)
    L[1] = 0.5 * (coef(0, 1) + coef(1, 0))
    L[2] = coef(1, 1)
    return L


def _soc_rows(L, shift):
    """Rows of u = T L f - shift_vec, with u in SOC3 meaning [[a-sh,b],[b,c-sh]] >= 0."""
    T = np.array([[1.0, 0.0, 1.0], [1.0, 0.0, -1.0], [0.0, 2.0, 0.0]])
    return T @ L, np.array([2.0 * shift, 0.0, 0.0])


def orbit_feasible(side, sbar, pts):
    """min ||F||_F s.t. sym(F^T M(sbar)) >= I, sym(F^T M(t)) >= 0 (t in pts).
    Returns F (2x2) or None.  Variables x = (f1..f4, t)."""
    blocks_A, blocks_b, cones = [], [], []
    # epigraph t >= ||f||: s = (t, f) in SOC5 ;  s = b - A x  ->  A = -[I], b = 0
    A0 = np.zeros((5, 5)); A0[0, 4] = -1.0; A0[1:, :4] = -np.eye(4)
    blocks_A.append(A0); blocks_b.append(np.zeros(5)); cones.append(clarabel.SecondOrderConeT(5))
    for t, sh in [(sbar, 1.0)] + [(p, 0.0) for p in pts]:
        TL, c = _soc_rows(_lin_sym(side, t), sh)
        A = np.zeros((3, 5)); A[:, :4] = -TL
        blocks_A.append(A); blocks_b.append(-c); cones.append(clarabel.SecondOrderConeT(3))
    A = sp.csc_matrix(np.vstack(blocks_A)); b = np.concatenate(blocks_b)
    q = np.zeros(5); q[4] = 1.0
    P = sp.csc_matrix((5, 5))
    sol = clarabel.DefaultSolver(P, q, A, b, cones, _SET).solve()
    st = str(sol.status)
    if st in ('Solved', 'AlmostSolved'):
        return np.array(sol.x[:4]).reshape(2, 2)
    if st in ('PrimalInfeasible', 'AlmostPrimalInfeasible'):
        return None
    # NumericalError, InsufficientProgress, ...: fall back to the cvxpy formulation of
    # the sfree note (core.orbit_feasible)
    FALLBACK[0] += 1
    return _core_orbit_feasible(side, [sbar], list(pts))


def interior_shift(F, side, sbar):
    A = F.T @ Mmat(side, sbar); A = (A + A.T) / 2
    lmin = np.linalg.eigvalsh(A)[0]; floor = 1e-9 * max(1.0, np.abs(A).max())
    if lmin <= floor:
        F = F + (floor - lmin) * np.linalg.inv(Mmat(side, sbar)).T
    return F


def steps_A(F, side, sbar, P):
    """alpha_j = sup{a : sym(F^T M(sbar + a p_j)) >= 0} for all columns of P."""
    F = interior_shift(F, side, sbar)
    A = F.T @ Mmat(side, sbar); A = (A + A.T) / 2
    L = np.linalg.cholesky(A); Li = np.linalg.inv(L)
    out = np.empty(P.shape[1])
    for j in range(P.shape[1]):
        B = F.T @ Mmat(side, P[:, j], h=0.0); B = (B + B.T) / 2
        mn = np.linalg.eigvalsh(Li @ B @ Li.T)[0]
        out[j] = np.inf if mn >= 0 else -1.0 / mn
    return out


def best_orbit(side, sbar, P, u, zhi, iters=25):
    """Bisection on z/zhi for max_F min_j u_j alpha_j(F) (u > 0), as in core.best_orbit_bound.
    Returns (certified value, upper value, F)."""
    lo, hi = 0.0, 1.0
    bestF = orbit_feasible(side, sbar, [])
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        pts = [sbar + (mid * zhi / u[j]) * P[:, j] for j in range(P.shape[1])]
        F = orbit_feasible(side, sbar, pts)
        if F is not None:
            lo, bestF = mid, F
        else:
            hi = mid
    if bestF is None:
        return 0.0, hi * zhi, None
    try:
        al = steps_A(bestF, side, sbar, P)
    except np.linalg.LinAlgError:
        return 0.0, hi * zhi, bestF
    v = [u[j] * al[j] for j in range(len(u)) if np.isfinite(al[j])]
    return (min(v) if v else np.inf), hi * zhi, bestF


def best_orbit_lex(side, sbar, P, w, nr, zk_w, zk_nr, eta=0.1, iters=25):
    """Lexicographic rule: among orbit sets whose corner bound for w is at least
    (1 - eta) times the best orbit bound, maximize the smallest Euclidean step
    min_j alpha_j ||r_j|| (nr = ray norms).  Two bisections.  Returns F (or None)."""
    z1, _, F1 = best_orbit(side, sbar, P, w, min(zk_w, 1e6), iters=iters)
    if F1 is None or not np.isfinite(z1) or z1 <= 0:
        return F1
    base = (1.0 - eta) * z1 / w
    lo, hi, bestF = 0.0, 1.0, F1
    thi = min(zk_nr, 1e6)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        pts = [sbar + max(base[j], mid * thi / nr[j]) * P[:, j] for j in range(P.shape[1])]
        F = orbit_feasible(side, sbar, pts)
        if F is not None:
            lo, bestF = mid, F
        else:
            hi = mid
    return bestF
