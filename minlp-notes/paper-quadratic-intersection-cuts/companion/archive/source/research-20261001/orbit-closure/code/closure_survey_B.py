"""Single-cut bound and closure bound of the completion family (B) and of SCIP's point-rule
completion family (BP) at w = (1, 1, 1), on the instances of closure_survey.py.

Usage: python3 closure_survey_B.py NAME [NAME ...]
Output: one JSON line per instance.  Numerical evidence only: the single-cut values are
heuristic lower bounds (sampling + Nelder-Mead over F), the closure values are cut-generation LP
values (valid lower bounds on the closure value, each cut being an exact (B) cut computed in
floating point) and LP value / min pricing (upper bounds if the pricing search is globally optimal).
"""
import sys, json, time
import numpy as np
from scipy.optimize import minimize
import orbit_lib
from orbit_lib import Corner, corner_bound, theta_to_Sc
from closure import closure_value, price
from closure_survey import INST


def cutvec(cn, th, fam):
    if fam == 'BP':
        S, c = theta_to_Sc(th)
        return None if S is None else cn.cut_B_fast(S, 0.0)
    v = np.asarray(th, float); v = v / np.linalg.norm(v)
    return cn.cut_B_fast(np.array([[v[0], v[1]], [v[1], v[2]]]), v[3])


def single_best(cn, w, fam, nsample=20000, nstart=30, seed=0):
    rng = np.random.default_rng(seed)

    def negval(th):
        try:
            a = cutvec(cn, th, fam)
        except np.linalg.LinAlgError:
            return 1e6
        if a is None:
            return 1e6
        with np.errstate(divide='ignore'):
            vals = np.where(a > 0, w / np.where(a > 0, a, 1), np.inf)
        z = vals.min()
        return -z if np.isfinite(z) else -1e6
    dim = 3 if fam == 'BP' else 4
    TH = rng.normal(size=(nsample, dim)) * (2.0 if fam == 'BP' else 1.0)
    vals = np.array([negval(t) for t in TH])
    best = (np.inf, None)
    for i in np.argsort(vals)[:nstart]:
        r = minimize(negval, TH[i], method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-13, maxiter=4000))
        if r.fun < best[0]:
            best = (r.fun, r.x)
    return -best[0]


def run(name):
    sb, P = INST[name]()
    w = np.ones(P.shape[1])
    cn = Corner(sb, P)
    zK, lamK = corner_bound(sb, P, w)
    out = dict(name=name, zK=float(zK))
    t = time.time()
    for fam in ('B', 'BP'):
        out['z1_' + fam] = single_best(cn, w, fam)
        z, lam, cuts, th, hist = closure_value(cn, w, fam=fam, maxit=60, tol=1e-7)
        pv = price(cn, lam, fam=fam, nsample=20000, nstart=30, rng=np.random.default_rng(7))[0]
        out.update({'zcl_' + fam: z, 'zcl_%s_up' % fam: z / min(pv, 1.0), 'lam_cl_' + fam: lam.tolist(),
                    'ncuts_' + fam: len(cuts), 'min_pricing_' + fam: pv})
    out['seconds'] = time.time() - t
    return out


if __name__ == '__main__':
    import warnings
    warnings.filterwarnings('ignore')
    for nm in sys.argv[1:]:
        print(json.dumps(run(nm)), flush=True)
