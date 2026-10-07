"""Library for the ratio-bound stream (research-20261001/ratio-bound).

Bilinear set S = {(x, y, w) : w <= x y}, q(s) = w - x y ("side +" of the sfree note;
side "-" is the image under (x, y, w) -> (x, -y, -w)).  LP vertex sbar with q(sbar) > 0,
rays p_j (columns of P), costs c_j > 0 (called w in the sfree note; renamed here to
avoid the clash with the coordinate w).

  M(x, y, w; h) = [[w, x], [y, h]],   det M(s, 1) = q(s).
  Family (A): C_F = {s : sym(F^T M(s, 1)) >= 0}, det F > 0.
  Family (B): upward closure cl(C_F + R_+ e_w).

Normalized frame (the affine automorphism of S that sends sbar to (0, 0, 1)):
  x'' = t (x - xbar) / sqrt(qbar),  y'' = (y - ybar) / (t sqrt(qbar)),
  w'' = (w - ybar x - xbar y + xbar ybar) / qbar,
so that a ray p becomes (t p_x / sqrt(qbar), p_y / (t sqrt(qbar)), grad q(sbar)^T p / qbar).
In that frame M(sbar) = I and the orbit sets containing sbar in their interior are
C_X = {s : sym(X M(s)) >= 0} with sym(X) > 0.
"""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SFREE = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'research-20260928b', 'sfree', 'code'))
if SFREE not in sys.path:
    sys.path.insert(0, SFREE)
from core import corner_bound, bilinear_quadratic  # noqa: E402  (read-only reuse)
from bilinear import pencil_interval  # noqa: E402

Q, B, C0 = bilinear_quadratic('+')
E = np.array([[1.0, 0.0], [0.0, 0.0]])        # M(e_w; 0)
J2 = np.array([[0.0, 1.0], [-1.0, 0.0]])


def q(s):
    return float(s[2] - s[0] * s[1])


def grad(s):
    return np.array([-s[1], -s[0], 1.0])


def M(s, h=1.0):
    return np.array([[s[2], s[0]], [s[1], h]], dtype=float)


def sym(A):
    return 0.5 * (A + A.T)


def zK(sbar, P, c):
    """Exact corner bound (closed-form supports of size <= 2; Theorem 11 of the sfree note)."""
    return corner_bound(Q, B, C0, np.asarray(sbar, float), np.asarray(P, float), np.asarray(c, float),
                        max_support=2, return_point=True)


def scaled_rays(P, c, z):
    """p~_j = (z / c_j) p_j : the vertices sbar + p~_j of the simplex T_z."""
    return P * (z / np.asarray(c, float))[None, :]


def normalize(sbar, Pt, t=1.0):
    """Rays in the normalized frame (sbar -> (0,0,1)), hyperbolic parameter t."""
    qb = q(sbar)
    g = grad(sbar)
    rq = np.sqrt(qb)
    return np.vstack([t * Pt[0] / rq, Pt[1] / (t * rq), (g @ Pt) / qb])


def D_inv(sbar, Pt):
    """D = sqrt(max_j |p~_jx| * max_j |p~_jy| / q(sbar)); invariant under the automorphisms of S."""
    return float(np.sqrt(np.abs(Pt[0]).max() * np.abs(Pt[1]).max() / q(sbar)))


# --------------------------------------------------------------------------- parabolic cylinders
def cyl_steps(sbar, Pt, t):
    """Step lengths (in units of the columns of Pt) of the parabolic cylinder
    C_t = {s : q(s) >= (t (x - xbar) - (y - ybar)/t)^2 / 4}: alpha_j = 2 qbar / (sqrt(a^2 + qbar b^2) - a),
    a = grad q(sbar)^T p, b = t p_x + p_y / t."""
    qb = q(sbar)
    a = grad(sbar) @ Pt
    b = t * Pt[0] + Pt[1] / t
    den = np.sqrt(a * a + qb * b * b) - a
    with np.errstate(divide='ignore'):
        out = np.where(den > 0, 2.0 * qb / np.where(den > 0, den, 1.0), np.inf)
    return out


def rho_par(sbar, Pt, ngrid=4001):
    """max_t min_j alpha_j(t) for the z-scaled rays Pt (so the value is a ratio to z).
    Returns (value, t).  Any t gives a valid lower bound; the maximization is numerical."""
    ts = np.exp(np.linspace(-12, 12, ngrid))
    vals = np.array([cyl_steps(sbar, Pt, t).min() for t in ts])
    k = int(np.argmax(vals))
    lo, hi = np.log(ts[max(k - 1, 0)]), np.log(ts[min(k + 1, ngrid - 1)])
    f = lambda u: cyl_steps(sbar, Pt, np.exp(u)).min()
    gr = (np.sqrt(5) - 1) / 2
    for _ in range(100):
        m1, m2 = hi - gr * (hi - lo), lo + gr * (hi - lo)
        if f(m1) >= f(m2):
            hi = m2
        else:
            lo = m1
    u = 0.5 * (lo + hi)
    best, tb = (f(u), np.exp(u)) if f(u) >= vals[k] else (vals[k], ts[k])
    return float(best), float(tb)


def theoremA_bound(D):
    """Explicit bound of Theorem A: 1/(1 + 2 D^2) for D <= 1, 1/((1 + sqrt 2) D) for D >= 1."""
    return 1.0 / (1.0 + 2.0 * D * D) if D <= 1 else 1.0 / ((1.0 + np.sqrt(2.0)) * D)


# --------------------------------------------------------------------------- family (A) in the normalized frame
def steps_X(X, Pn):
    """Exact step lengths of C_X (normalized frame) along the columns of Pn."""
    S = sym(X)
    L = np.linalg.cholesky(S)
    Li = np.linalg.inv(L)
    out = []
    for j in range(Pn.shape[1]):
        Bj = sym(X @ M(Pn[:, j], h=0.0))
        mn = np.linalg.eigvalsh(Li @ Bj @ Li.T)[0]
        out.append(np.inf if mn >= 0 else -1.0 / mn)
    return np.array(out)


def feasible_X(Pn, r, solver='CLARABEL'):
    """X with sym(X) >= I and sym(X (I + r M_j)) >= 0 for all j, or None."""
    import cvxpy as cp
    X = cp.Variable((2, 2))
    cons = [(X + X.T) / 2 >> np.eye(2)]
    for j in range(Pn.shape[1]):
        A = X @ (np.eye(2) + r * M(Pn[:, j], h=0.0))
        cons.append((A + A.T) / 2 >> 0)
    prob = cp.Problem(cp.Minimize(cp.norm(X, 'fro')), cons)
    try:
        prob.solve(solver=solver)
    except Exception:
        return None
    if prob.status not in ('optimal', 'optimal_inaccurate'):
        return None
    return X.value


def zA_ratio(sbar, Pt, iters=40, hi0=1.0, solver='CLARABEL'):
    """Best family-(A) single-cut bound divided by z, for the z-scaled rays Pt.
    Returns (certified lower bound from an explicit X, bisection upper value, X)."""
    Pn = normalize(sbar, Pt)
    lo, hi = 0.0, hi0
    bestX = np.eye(2)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        X = feasible_X(Pn, mid, solver)
        if X is not None:
            lo, bestX = mid, X
        else:
            hi = mid
    try:
        cert = float(steps_X(bestX, Pn).min())
    except np.linalg.LinAlgError:
        cert = 0.0
    return cert, hi, bestX


# --------------------------------------------------------------------------- family (B) in the normalized frame
def in_B_X(X, s, tol=1e-12):
    """s (normalized frame) lies in cl(C_X + R_+ e_w) iff some tau in [0, q(s)] has
    sym(X (M(s) - tau E)) >= 0 (a lowered point with tau > q(s) is in int S).  The minimum
    eigenvalue of the pencil is concave in tau, so a golden-section search is exact up to tol."""
    qs = q(s)
    A = sym(X @ M(s))
    Z = sym(X @ E)
    scale = 1.0 + np.abs(A).max() + max(qs, 0.0) * np.abs(Z).max()
    lmin = lambda tau: np.linalg.eigvalsh(A - tau * Z)[0]
    if lmin(0.0) >= -tol * scale:
        return True
    if qs < -tol * scale:
        return False
    lo, hi = 0.0, max(qs, 0.0)
    gr = (np.sqrt(5) - 1) / 2
    for _ in range(120):
        m1, m2 = hi - gr * (hi - lo), lo + gr * (hi - lo)
        if lmin(m1) >= lmin(m2):
            hi = m2
        else:
            lo = m1
    return max(lmin(lo), lmin(hi), lmin(max(qs, 0.0))) >= -tol * scale


def stepB_X(X, p, amax=1e6, iters=60):
    """Step length of cl(C_X + R_+ e_w) from (0,0,1) along p (normalized frame); inf if > amax.
    (Steps beyond 1e6 z-units never matter for the ratios, and the PSD test loses accuracy there.)"""
    o = np.array([0.0, 0.0, 1.0])
    lo, hi = 0.0, 1.0
    while in_B_X(X, o + hi * p):
        lo, hi = hi, 2 * hi
        if hi > amax:
            return np.inf
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if in_B_X(X, o + mid * p):
            lo = mid
        else:
            hi = mid
    return lo


def _dform(P, Qm):
    """Polarized determinant on symmetric 2x2 matrices: det(P) = _dform(P, P)."""
    return 0.5 * (P[0, 0] * Qm[1, 1] + P[1, 1] * Qm[0, 0]) - P[0, 1] * Qm[0, 1]


def _first_neg(m, cands, amax):
    """First s > 0 where the continuous function m (m(0) > 0) becomes negative, given
    candidate breakpoints; bisection refines the crossing."""
    prev = 0.0
    for c in sorted(x for x in cands if 0 < x < amax) + [amax]:
        for probe in (0.5 * (prev + c), c):
            if m(probe) < 0:
                lo, hi = prev, probe
                for _ in range(200):
                    mm = 0.5 * (lo + hi)
                    if m(mm) >= 0:
                        lo = mm
                    else:
                        hi = mm
                return lo
        prev = c
    return np.inf


def stepB_closed(X, p, amax=1e6):
    """Closed-form step of cl(C_X + R_+ e_w) from (0,0,1) along p (normalized frame).
    The pairs (s, tau) with A0 + s A1 - tau Z >= 0 form a convex set (A0 = sym X, A1 = sym(X M_p),
    Z = sym(X E)); det Z <= 0, so d(s, tau) = det(A0 + s A1 - tau Z) is concave in tau and the
    step is the first s > 0 at which max_{tau >= 0} d(s, tau) < 0 (for each s the tau-interval
    with d >= 0 is PSD throughout or NSD throughout, and it is PSD at s = 0).  Falls back to
    bisection when det Z is (nearly) zero."""
    A0 = sym(X)
    A1 = sym(X @ M(p, h=0.0))
    Z = sym(X @ E)
    f = _dform(Z, Z)
    nz = np.abs(Z).max()
    if f > -1e-10 * nz * nz:
        return stepB_X(X, p, amax)
    d00, d01, d11 = _dform(A0, A0), _dform(A0, A1), _dform(A1, A1)
    e0, e1 = _dform(A0, Z), _dform(A1, Z)

    def m(s):
        ts = (e0 + e1 * s) / f
        v = d00 + 2 * d01 * s + d11 * s * s
        return v + (e0 + e1 * s) ** 2 / (-f) if ts > 0 else v
    cands = []
    for (a2, a1, a0) in ((d11, 2 * d01, d00),
                         (d11 + e1 * e1 / (-f), 2 * d01 + 2 * e0 * e1 / (-f), d00 + e0 * e0 / (-f))):
        if abs(a2) < 1e-300:
            if a1 != 0:
                cands.append(-a0 / a1)
            continue
        disc = a1 * a1 - 4 * a2 * a0
        if disc >= 0:
            r = np.sqrt(disc)
            cands += [(-a1 - r) / (2 * a2), (-a1 + r) / (2 * a2)]
    if e1 != 0:
        cands.append(-e0 / e1)
    return _first_neg(m, cands, amax)


def boundB_X(X, Pn):
    return min(stepB_closed(X, Pn[:, j]) for j in range(Pn.shape[1]))


def X_from(u):
    """Parametrization of the family-(B) sets whose upward closure contains (0,0,1) in its interior:
    X = Y diag(1/(1 - tau0), 1) with Y = [[1, b + a], [b - a, c]], c = b^2 + exp(e) (sym(Y) > 0),
    tau0 = 1/(1 + exp(-g)) in (0, 1) if len(u) == 4, else tau0 = 0 (then sym(X) > 0, family (A)
    normalization).  (0,0,1) - tau0 e_w lies in int C_X."""
    a, b, e = u[:3]
    Y = np.array([[1.0, b + a], [b - a, b * b + np.exp(e)]])
    if len(u) == 3:
        return Y
    tau0 = 1.0 / (1.0 + np.exp(-u[3]))
    return Y @ np.diag([1.0 / (1.0 - tau0), 1.0])


def u_from(X):
    X = X / X[0, 0]
    S = sym(X)
    a = 0.5 * (X[0, 1] - X[1, 0])
    b = S[0, 1]
    return np.array([a, b, np.log(max(S[1, 1] - b * b, 1e-300))])


def zB_heur(sbar, Pt, X0s=(), restarts=20, seed=0, maxiter=800):
    """Heuristic lower bound on the best family-(B) bound / z: Nelder-Mead over X, first with
    sym(X) > 0 (3 parameters), then over the 4-parameter family where only the upward closure
    contains sbar.  Every reported value is the exact bound of an explicit X (a valid lower bound)."""
    from scipy.optimize import minimize
    Pn = normalize(sbar, Pt)
    rng = np.random.default_rng(seed)
    best, bX = -1.0, None

    def safe_bound(u):
        # guard added in the second session: parameters can overflow (tau0 -> 1 or exp(e) -> inf), and the
        # step routines then return inf for a matrix with inf/nan entries; such X are rejected
        with np.errstate(all='ignore'):
            X = X_from(u)
        if not np.all(np.isfinite(X)) or np.abs(X).max() > 1e12 or np.linalg.det(X) <= 0:
            return 0.0
        return min(boundB_X(X, Pn), 1e6)

    def run(u0):
        nonlocal best, bX
        f = lambda u: -safe_bound(u)
        v0 = -f(u0)
        if v0 > best:
            best, bX = v0, X_from(u0)
        res = minimize(f, u0, method='Nelder-Mead', options=dict(maxiter=maxiter, xatol=1e-10, fatol=1e-12))
        if -res.fun > best:
            best, bX = -res.fun, X_from(res.x)
        return res.x
    starts = [u_from(X) for X in X0s] + [np.zeros(3)]
    starts += [rng.normal(size=3) * np.array([2.0, 2.0, 3.0]) for _ in range(restarts)]
    ends = [run(u0) for u0 in starts]
    ends.sort(key=lambda u: -safe_bound(u))
    for u in ends[:3]:
        for g in (-6.0, -2.0, 0.0, 2.0):
            run(np.append(u, g))
    for _ in range(restarts // 2):
        run(np.append(rng.normal(size=3) * np.array([2.0, 2.0, 3.0]), rng.normal() * 3))
    return float(best), bX


# --------------------------------------------------------------------------- SCIP's rule (Case 4 of Chmiela et al.)
def scip_F(sbar):
    """F with C_F = SCIP's (Munoz-Serrano, constant lambda) set before completion:
    F^T = R_theta, tan theta = (xbar - ybar)/(wbar + 1), in the original coordinates."""
    xh = np.array([(sbar[0] - sbar[1]) / 2.0, (sbar[2] + 1.0) / 2.0])
    lam = xh / np.linalg.norm(xh)
    s, c = lam                        # lambda = (sin theta, cos theta)
    R = np.array([[c, -s], [s, c]])
    return R.T


def to_normalized_X(F, sbar, t=1.0):
    """Express C_F (original coordinates) as C_X in the normalized frame of sbar (parameter t).
    M(s) = U D1 M(s'') D2 L with U = [[1, xbar], [0, 1]], L = [[1, 0], [ybar, 1]],
    D1 = diag(sqrt(qbar)/t, 1), D2 = diag(t sqrt(qbar), 1).  With K = D2 L,
    v^T F^T M(s) v = u^T K^{-T} F^T U D1 M(s'') u for u = K v, so X = K^{-T} F^T U D1."""
    rq = np.sqrt(q(sbar))
    U = np.array([[1.0, sbar[0]], [0.0, 1.0]])
    Lm = np.array([[1.0, 0.0], [sbar[1], 1.0]])
    D1 = np.diag([rq / t, 1.0])
    K = np.diag([rq * t, 1.0]) @ Lm
    return np.linalg.inv(K).T @ F.T @ U @ D1


def scip_ratio(sbar, Pt, fam='B'):
    """Single-cut bound of SCIP's set (A: uncompleted cone C_{R_theta}; B: its upward closure,
    which is the Case-4 set), divided by z, for z-scaled rays Pt."""
    X = to_normalized_X(scip_F(sbar), sbar)
    Pn = normalize(sbar, Pt)
    if fam == 'A':
        return float(steps_X(X, Pn).min())
    return float(boundB_X(X, Pn))
