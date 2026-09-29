"""Spot-check of two adversarial instances (restarts 1 and 4 of adversarial_ratio_8_margin.log).
Decoding of theta re-implemented from the docstring of adversarial_ratio.py; everything else is the
reviewer's code: z_K by my_supp2 (dense scan) and SCIP, z_A by SDP bisection + exact bound,
(B) by Nelder-Mead over F with the reviewer's (B) membership (rv_orbit_numeric.boundB)."""
import json, sys, numpy as np, warnings
warnings.filterwarnings('ignore')
from scipy.optimize import minimize
import rv_zk_check as zc
import rv_orbit_numeric as on

Q = np.zeros((3, 3)); Q[0, 1] = Q[1, 0] = -0.5; b = np.array([0, 0, 1.0]); c = 0.0
recs = [json.loads(l) for l in open('../../sfree/logs/adversarial_ratio_8_margin.log') if l.startswith('{')]
for idx in (int(a) for a in sys.argv[1:]):
    th = np.array(recs[idx]['theta'])
    x0, y0, g, a, bb = th[:5]; s = th[5:8]; r = th[8:11]
    t0 = np.array([x0, y0, x0 * y0]); e = np.exp(g); d = np.array([1.0, -e, y0 - x0 * e])
    v1 = t0 + np.exp(a) * d; v2 = t0 - np.exp(bb) * d; sbar = t0 + s; v3 = t0 + r
    P = np.stack([v1 - sbar, v2 - sbar, v3 - sbar], 1); w = np.ones(3)
    qs = zc.qv(Q, b, c, sbar)
    m2 = zc.my_supp2(Q, b, c, sbar, P, w); sc, lam = zc.scip(Q, b, c, sbar, P, w, m2)
    # relative discriminants of rays (grazing margin)
    rd = []
    for j in range(3):
        p = P[:, j]; A_ = p @ Q @ p; B_ = 2 * p @ (Q @ sbar + b / 2)
        rd.append((B_ * B_ - 4 * A_ * qs) / (B_ * B_ + abs(4 * A_ * qs)))
    print('restart %d: q(sbar)=%.3e  q/max|P|^2=%.2e  rel.disc=%s  z_K: my_supp2=%.7f SCIP=%.7f' % (idx, qs, qs / np.abs(P).max() ** 2, np.round(rd, 4), m2, sc))
    on.INST['adv'] = (sbar, [v1, v2, v3])
    Pl = [v1 - sbar, v2 - sbar, v3 - sbar]
    lo, hi, Fb = 0.0, 1.0, None
    for _ in range(36):
        mid = (lo + hi) / 2
        F = on.feasible(sbar, [v1, v2, v3], mid)
        if F is not None:
            lo, Fb = mid, F
        else:
            hi = mid
    cert, al = on.exactA(Fb, sbar, Pl)
    print('   (A): bisection [%.6f, %.6f], exact bound of F = %.6f' % (lo, hi, cert))
    rng = np.random.default_rng(3)
    best = on.boundB(Fb, sbar, Pl, tmax=3.0)
    starts = [Fb.ravel() / np.linalg.norm(Fb)] + [rng.standard_normal(4) for _ in range(16)]
    for x0_ in starts:
        res = minimize(lambda x: -on.boundB(x.reshape(2, 2) / max(1e-12, np.linalg.norm(x)), sbar, Pl, 3.0), x0_,
                       method='Nelder-Mead', options=dict(maxiter=600, xatol=1e-7, fatol=1e-8))
        best = max(best, -res.fun)
    print('   (B): best found over %d starts = %.6f' % (len(starts), best), flush=True)
