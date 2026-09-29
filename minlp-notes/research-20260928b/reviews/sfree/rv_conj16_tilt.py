"""Tilt the tangent edge of instance 13 outward: v2 = t* + d + eps*|d|*g/|g|^2... (grad q(t*).(v2 - t*) > 0),
so every edge of T* at t* is transversal (strict complementarity) while t* stays the unique support-1
minimizer (checked by support-enumeration scan and SCIP).  Report z_A (Clarabel bisection + exact bound)."""
import json, numpy as np, warnings
warnings.filterwarnings('ignore')
import rv_zk_check as zc, rv_orbit_numeric as on
Q = np.zeros((3, 3)); Q[0, 1] = Q[1, 0] = -0.5; b = np.array([0, 0, 1.0]); c = 0.0
recs = {json.loads(l)['n']: json.loads(l) for l in open('rv_conj16_instances.jsonl')}
for n in (13, 14):
    d = recs[n]; sbar = np.array(d['sbar']); V0 = [np.array(v) for v in d['V']]
    t = V0[0]; dv = V0[1] - t; gq = np.array([-t[1], -t[0], 1.0])
    for eps in (0.0, 1e-3, 1e-2, 3e-2, 1e-1):
        v2 = t + dv + eps * np.linalg.norm(dv) * gq / np.linalg.norm(gq)
        V = [t, v2, V0[2]]; P = np.stack([v - sbar for v in V], 1); w = np.ones(3)
        m2 = zc.my_supp2(Q, b, c, sbar, P, w)
        try:
            sc, lam = zc.scip(Q, b, c, sbar, P, w, 1.0)
        except Exception:
            sc, lam = np.nan, None
        lo, hi, Fb = 0.0, 1.0, None
        for _ in range(30):
            mid = (lo + hi) / 2
            F = on.feasible(sbar, V, mid)
            if F is not None:
                lo, Fb = mid, F
            else:
                hi = mid
        cert = on.exactA(Fb, sbar, [v - sbar for v in V])[0]
        cosang = gq @ (v2 - t) / np.linalg.norm(gq) / np.linalg.norm(v2 - t)
        print('inst %d eps=%.0e: cos(grad q, edge)=%.4f  z_K: scan %.7f SCIP %.7f  z_A: certified %.6f (infeasible at %.6f)' % (n, eps, cosang, m2, sc, cert, hi), flush=True)
