"""Numerical closure of an orbit family at one corner, by cut generation.

    z_cl(w) = min{ w^T lam : lam >= 0, a(F)^T lam >= 1 for all F in the family }.

The LP over the cuts found so far gives lam^k; the pricing problem min_F a(F)^T lam^k is a
3-parameter nonconvex problem (F up to scale), solved by random sampling plus Nelder-Mead.
The output is numerical evidence (pricing is a heuristic global search); exact certificates are
produced separately (certify_closure_point.py).
"""
import numpy as np
from scipy.optimize import linprog, minimize
from orbit_lib import Corner, theta_to_Sc


def price(cn, lam, fam='A', nsample=4000, nstart=12, rng=None, extra_starts=()):
    """Approximately minimize a(F)^T lam over the family.  Returns (value, theta, a)."""
    rng = np.random.default_rng(0) if rng is None else rng

    def cutvec(th):
        if fam in ('A', 'P', 'BP'):
            S, c = theta_to_Sc(th)
            if S is None:
                return None
            if fam == 'P' or fam == 'BP':
                c = 0.0
            if fam in ('A', 'P'):
                return cn.cut_A(S, c)
            return cn.cut_B_fast(S, c)
        # fam == 'B': (S, c) free on the unit sphere of R^4
        v = np.asarray(th, float)
        nv = np.linalg.norm(v)
        if nv == 0:
            return None
        v = v / nv
        S = np.array([[v[0], v[1]], [v[1], v[2]]])
        return cn.cut_B_fast(S, v[3])

    def f(th):
        try:
            a = cutvec(th)
        except np.linalg.LinAlgError:
            return 1e6
        if a is None:
            return 1e6
        v = a @ lam
        return v if np.isfinite(v) else 1e6

    if fam == 'B':
        TH = rng.normal(size=(nsample, 4))
    else:
        TH = np.column_stack([rng.normal(scale=2.0, size=nsample), rng.normal(scale=2.0, size=nsample),
                              np.tan(np.pi * (rng.random(nsample) - 0.5)) * rng.choice([0.3, 1, 3, 10], nsample)])
    vals = np.array([f(t) for t in TH])
    order = np.argsort(vals)[:nstart]
    starts = [TH[i] for i in order] + [np.asarray(s, float) for s in extra_starts]
    best = (np.inf, None)
    for s in starts:
        r = minimize(f, s, method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-13, maxiter=4000, maxfev=8000))
        if r.fun < best[0]:
            best = (r.fun, r.x)
    a = cutvec(best[1])
    return best[0], best[1], a


def closure_value(cn, w, fam='A', maxit=200, tol=1e-9, verbose=False, rng=None, init_cuts=()):
    """Cut generation; returns (z_cl estimate, lam, cuts, history)."""
    rng = np.random.default_rng(1) if rng is None else rng
    cuts = [np.asarray(c, float) for c in init_cuts]
    thetas = []
    hist = []
    N = cn.N
    lam = np.full(N, 1e-3)
    for it in range(maxit):
        if cuts:
            A = -np.array(cuts)
            res = linprog(w, A_ub=A, b_ub=-np.ones(len(cuts)), bounds=[(0, None)] * N, method='highs')
            if res.status != 0:
                # unbounded LP (cuts do not bound w yet): use a large box
                res = linprog(w, A_ub=A, b_ub=-np.ones(len(cuts)), bounds=[(0, 1e6)] * N, method='highs')
            lam = res.x
        val, th, a = price(cn, lam, fam=fam, rng=rng, extra_starts=thetas[-3:])
        hist.append((it, float(w @ lam), float(val)))
        if verbose:
            print('it %3d  LP %.10f  pricing %.10f  lam %s' % (it, w @ lam, val, np.round(lam, 6)), flush=True)
        if val >= 1 - tol:
            break
        cuts.append(a)
        thetas.append(th)
    return float(w @ lam), lam, cuts, thetas, hist
