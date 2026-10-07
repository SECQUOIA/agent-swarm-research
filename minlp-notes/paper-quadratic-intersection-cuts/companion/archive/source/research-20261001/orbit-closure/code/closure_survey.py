"""Single-cut bound versus closure bound of the orbit family (A) and of the point-rule
subfamily (P, SCIP's rule lambda = x(T sbar)/|x(T sbar)| under all transformations, i.e. c = 0)
on the corners of the sfree note, at w = (1, 1, 1).

Usage: python3 closure_survey.py NAME [NAME ...]    (names below; 'all' for every instance)
Output: one JSON line per instance (numerical evidence; pricing is a heuristic global search).
  zK       exact corner bound (support enumeration)
  z1_A     best single orbit cut (LMI bisection, certified lower value)
  zcl_A    closure LP value after cut generation (a valid lower bound on the closure value, given
           that each generated cut is an exact orbit cut) and zcl_A_up = LP value / min pricing
           (an upper bound if the pricing search is globally optimal)
  z1_P, zcl_P   the same for the point-rule subfamily
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[7])

import sys, json, time
import numpy as np
import orbit_lib
from orbit_lib import Corner, corner_bound
from closure import closure_value, price
import core

SF = (_PUBLIC_REPO + '/research-20260928b/sfree/code')
sys.path.insert(0, SF)


def adv(theta):
    from adversarial_ratio import build
    return build(np.array(theta))


def verts(sb, vs):
    sb = np.array(sb, float)
    return sb, np.column_stack([np.array(v, float) - sb for v in vs])


ADV = {}
try:
    for line in open((_PUBLIC_REPO + '/research-20260928b/sfree/logs/adversarial_ratio_8_margin.log')):
        if line.startswith('{'):
            d = json.loads(line)
            ADV['adv8_%d' % d['restart']] = d['theta']
except FileNotFoundError:
    pass

INST = {
    'thm14': lambda: verts([-4.5, 0, 1.5], [[-1, -6, 18], [-5, 6, -18], [0, 2.5, 2.5]]),
    'bigA': lambda: verts([-0.5, 0.5, 1], [[0.5, -4, -0.5], [-10, 3, 24], [4.5, 0.5, 7.5]]),
    'prop16': lambda: verts([-2, 3, 2], [[0, 0, 0], [6, -2, 0.25], [1, -2.5, 0.5]]),
    'prop16_v2_1': lambda: verts([-2, 3, 2], [[0, 0, 0], [6, -2, 1], [1, -2.5, 0.5]]),
    'prop16_v8': lambda: verts([-2, 3, 2], [[0, 0, 0], [8, -3, 0.25], [1, -2.5, 0.5]]),
    'supp1_1074': lambda: verts([0.0, -4.5, 3.0], [[-1.0, -2.0, 2.0], [2.05, -2.98, -2.98], [-1.0, 1.0, 4.0]]),
    'supp1_3437': lambda: verts([-3.5, 1.5, 4.0], [[-2.0, -1.0, 2.0], [0.05, -6.9, 12.05], [1.0, -1.5, 0.5]]),
    'supp1_4580': lambda: verts([0.5, 0.5, 0.5], [[-1.0, 0.0, 0.0], [2.0, -8.91, 9.09], [-4.0, 2.5, 0.5]]),
    'supp1_5512': lambda: verts([-1.5, 0.5, 0.5], [[0.0, 0.0, 0.0], [1.0, -2.0, 0.02], [2.0, 0.0, 1.0]]),
}
for k, th in ADV.items():
    INST[k] = (lambda th=th: adv(th))


def best_single_P(cn, w, zhi, iters=40):
    """Best single cut of the point-rule subfamily by bisection (LMI in S with c = 0)."""
    import cvxpy as cp
    lo, hi = 0.0, 1.0
    bestS = None
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        S = cp.Variable((2, 2), symmetric=True)
        cons = [S >> np.eye(2) * 1e-6]
        for j in range(cn.N):
            Aj = S @ cn.Nj[j]
            cons.append(S + (mid * zhi / w[j]) * (Aj + Aj.T) / 2 >> 0)
        pr = cp.Problem(cp.Minimize(cp.trace(S)), cons + [cp.trace(S) <= 1e6, cp.trace(S) >= 1])
        try:
            pr.solve(solver='CLARABEL')
        except Exception:
            pr = None
        if pr is not None and pr.status in ('optimal', 'optimal_inaccurate'):
            lo, bestS = mid, S.value
        else:
            hi = mid
    cert = 0.0
    if bestS is not None:
        Sn = bestS / np.trace(bestS)
        try:
            a = cn.cut_A(Sn + 1e-12 * np.eye(2), 0.0)
            cert = min(w[j] / a[j] for j in range(cn.N) if a[j] > 0)
        except np.linalg.LinAlgError:
            pass
    return cert, hi * zhi


def run(name):
    sb, P = INST[name]()
    w = np.ones(P.shape[1])
    cn = Corner(sb, P)
    zK, lamK = corner_bound(sb, P, w)
    out = dict(name=name, sbar=sb.tolist(), P=P.tolist(), zK=float(zK), lamK=lamK.tolist())
    t = time.time()
    c1, h1, F = core.best_orbit_bound('+', sb, P, w, zK, iters=40)
    out.update(z1_A=float(c1), z1_A_hi=float(h1))
    z, lam, cuts, th, hist = closure_value(cn, w, fam='A', maxit=60, tol=1e-7)
    pv = price(cn, lam, fam='A', nsample=20000, nstart=30, rng=np.random.default_rng(7))[0]
    out.update(zcl_A=z, zcl_A_up=z / min(pv, 1.0), lam_cl_A=lam.tolist(), ncuts_A=len(cuts), min_pricing_A=pv)
    p1, ph = best_single_P(cn, w, zK)
    out.update(z1_P=float(p1), z1_P_hi=float(ph))
    z, lam, cuts, th, hist = closure_value(cn, w, fam='P', maxit=60, tol=1e-7)
    pv = price(cn, lam, fam='P', nsample=20000, nstart=30, rng=np.random.default_rng(7))[0]
    out.update(zcl_P=z, zcl_P_up=z / min(pv, 1.0), lam_cl_P=lam.tolist(), ncuts_P=len(cuts), min_pricing_P=pv)
    out['seconds'] = time.time() - t
    return out


if __name__ == '__main__':
    import warnings
    warnings.filterwarnings('ignore')
    names = sys.argv[1:]
    if names == ['all']:
        names = list(INST)
    for nm in names:
        print(json.dumps(run(nm)), flush=True)
