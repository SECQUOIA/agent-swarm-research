import json, sys, numpy as np, warnings; warnings.filterwarnings('ignore')


class AR:
    @staticmethod
    def build(th):   # same parametrization as adversarial_ratio.build
        x0, y0, g, a, bb = th[:5]; s = th[5:8]; r = th[8:11]
        t0 = np.array([x0, y0, x0 * y0]); e = np.exp(g)
        d = np.array([1.0, -e, y0 - x0 * e])
        v1 = t0 + np.exp(a) * d; v2 = t0 - np.exp(bb) * d; sbar = t0 + s; v3 = t0 + r
        return sbar, np.stack([v1 - sbar, v2 - sbar, v3 - sbar], 1)
from core import bilinear_quadratic, corner_bound, best_orbit_bound, orbit_feasible, Mmat
from bilinear import kappa_pencil, kappa_set_A, step_A
from scout_sfree import corner_bound_scip
Q, b, c = bilinear_quadratic('+')
for line in open(sys.argv[1]):
    if not line.startswith('{'): continue
    r = json.loads(line); th = np.array(r['theta'])
    sbar, P = AR.build(th)
    zk, lam = corner_bound(Q, b, c, sbar, P, np.ones(3), return_point=True)
    zs = corner_bound_scip(Q, b, c, sbar, P, np.ones(3))
    t0 = sbar + P @ lam; V = [sbar + P[:, j] for j in range(3)]
    G0, G1 = kappa_pencil('+', t0, V[0] - V[1])
    ivs = [kappa_set_A(G0, G1, '+', v) for v in [sbar] + V]
    lo = max(iv[0] for iv in ivs if iv); hi = min(iv[1] for iv in ivs if iv)
    cert, hib, F = best_orbit_bound('+', sbar, P, np.ones(3), 1.0, iters=45)
    print('restart', r['restart'], 'reported', round(r['final'], 4), '| zK %.8f SCIP %.8f lam %s' % (zk, zs, lam.round(4)),
          '| kappa-intersection', 'EMPTY' if (any(iv is None for iv in ivs) or lo > hi) else (lo, hi),
          '| cert %.6f bisect %.6f' % (cert, hib), '| scale |P| %.1e' % np.abs(P).max(), flush=True)
