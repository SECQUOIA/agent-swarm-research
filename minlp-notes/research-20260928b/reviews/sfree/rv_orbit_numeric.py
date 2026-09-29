"""Numerical best-orbit bounds for the two rational instances (reviewer's own implementation).

(A) sliced orbit sets C_F cap H: bisection on z with an SDP feasibility problem (CVXPY/Clarabel),
    then the *exact* bound of the returned F via 2x2 generalized eigenvalues (certified lower bound).
(B) maximal completions cl((C_F cap H) + R_+ e_w): membership of a point s is
    max_{tau >= 0} lambda_min(sym(F^T M(s)) - tau sym(F^T E)) >= 0 (concave in tau); step lengths by
    bisection along each ray; the bound is maximized over F (normalized) by Nelder-Mead from the
    (A) optimum and random starts.
Usage: python3 rv_orbit_numeric.py [n_random_starts]
"""
import sys
import numpy as np
import cvxpy as cp
from scipy.optimize import minimize

INST = {
    'thm14': (np.array([-4.5, 0, 1.5]), [np.array([-1., -6, 18]), np.array([-5., 6, -18]), np.array([0, 2.5, 2.5])]),
    'second': (np.array([-.5, .5, 1]), [np.array([.5, -4, -.5]), np.array([-10., 3, 24]), np.array([4.5, .5, 7.5])]),
}


def M(s, h=1.0):
    return np.array([[s[2], s[0]], [s[1], h]])


E = np.array([[1.0, 0.0], [0.0, 0.0]])


def sym(X):
    return 0.5 * (X + X.T)


def lmin(X):
    a, b, c = X[0, 0], X[0, 1], X[1, 1]
    return 0.5 * (a + c) - np.hypot(0.5 * (a - c), b)


def feasible(sbar, V, z):
    F = cp.Variable((2, 2))
    cons = [sym(F.T @ M(sbar)) >> np.eye(2)]
    for v in V:
        pt = sbar + z * (v - sbar)
        cons.append(sym(F.T @ M(pt)) >> 0)
    pr = cp.Problem(cp.Minimize(cp.norm(F, 'fro')), cons)
    try:
        pr.solve(solver='CLARABEL')
    except Exception:
        return None
    return F.value if pr.status == 'optimal' else None


def exactA(F, sbar, P):
    A = sym(F.T @ M(sbar))
    Lc = np.linalg.cholesky(A)
    Li = np.linalg.inv(Lc)
    al = []
    for p in P:
        B = sym(F.T @ M(p, 0.0))
        mn = np.linalg.eigvalsh(Li @ B @ Li.T)[0]
        al.append(np.inf if mn >= 0 else -1.0 / mn)
    return min(al), al


def inB(F, s):
    A = sym(F.T @ M(s)); Z = sym(F.T @ E)
    qs = s[2] - s[0] * s[1]
    if qs < 0:
        return False
    f = lambda t: lmin(A - t * Z)
    lo, hi = 0.0, qs
    if f(lo) >= 0:
        return True
    gr = (np.sqrt(5) - 1) / 2
    for _ in range(60):
        m1 = hi - gr * (hi - lo); m2 = lo + gr * (hi - lo)
        if f(m1) >= f(m2):
            hi = m2
        else:
            lo = m1
    return f(0.5 * (lo + hi)) >= -1e-12 or f(qs) >= 0


def boundB(F, sbar, P, tmax=3.0):
    if lmin(sym(F.T @ M(sbar))) <= 0:
        return 0.0
    al = []
    for p in P:
        lo, hi = 0.0, tmax
        if inB(F, sbar + hi * p):
            al.append(hi); continue
        for _ in range(45):
            mid = 0.5 * (lo + hi)
            if inB(F, sbar + mid * p):
                lo = mid
            else:
                hi = mid
        al.append(lo)
    return min(al)


def run(name, nstarts):
    sbar, V = INST[name]
    P = [v - sbar for v in V]
    lo, hi, Fbest = 0.0, 1.0, None
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        F = feasible(sbar, V, mid)
        if F is not None:
            lo, Fbest = mid, F
        else:
            hi = mid
    cert, al = exactA(Fbest, sbar, P)
    print('%s: (A) bisection interval [%.8f, %.8f]; exact bound of returned F = %.8f; alphas %s' % (name, lo, hi, cert, np.round(al, 6)))
    print('   F =', np.round(Fbest / np.linalg.norm(Fbest), 6).tolist())
    zB0 = boundB(Fbest, sbar, P)
    print('   (B) bound of the same F = %.6f' % zB0)
    rng = np.random.default_rng(12345)
    best = (zB0, Fbest)
    starts = [Fbest.ravel() / np.linalg.norm(Fbest)] + [rng.standard_normal(4) for _ in range(nstarts)]
    for x0 in starts:
        obj = lambda x: -boundB(x.reshape(2, 2) / max(1e-12, np.linalg.norm(x)), sbar, P)
        res = minimize(obj, x0, method='Nelder-Mead', options=dict(maxiter=800, xatol=1e-7, fatol=1e-8))
        val = -res.fun
        if val > best[0] + 1e-9:
            best = (val, res.x.reshape(2, 2) / np.linalg.norm(res.x))
    print('   best (B) bound found over %d starts: %.6f  F = %s' % (len(starts), best[0], np.round(best[1], 6).tolist()))


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    for nm in INST:
        run(nm, n)
