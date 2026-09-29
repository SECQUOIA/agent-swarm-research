"""Targeted test of Conjecture 16 (support-1 minimizer => orbit (A) attains z_K) in the degenerate
subcase where the minimizer t* = v1 is the endpoint of an edge [v1, v2] of T* that is tangent to dS at t*
(zero multiplier on ray 2).  Construction (w = 1, z_K = 1): t* = (x0, y0, x0 y0);
v1 = t*;  v2 = t* + d with grad q(t*).d = 0, det M(d;0) = -dx dy > 0;  v3 = t* + r with grad q(t*).r > 0;
sbar = t* - p with grad q(t*).(sbar - t*) > 0 and q(sbar) > 0.  Accept if z_K = 1 (my_supp2 and SCIP)
and the minimizer is unique (support-2 values on edges {1,3} and {2,3} and single rays 2,3 exceed 1+1e-6)."""
import sys, numpy as np, warnings
warnings.filterwarnings('ignore')
import rv_zk_check as zc, rv_orbit_numeric as on
Q = np.zeros((3, 3)); Q[0, 1] = Q[1, 0] = -0.5; b = np.array([0, 0, 1.0]); c = 0.0
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 11)
n = 0; worst = 1.0
while n < int(sys.argv[2]) if len(sys.argv) > 2 else 25:
    x0, y0 = rng.normal(size=2) * 2
    t = np.array([x0, y0, x0 * y0]); gq = np.array([-y0, -x0, 1.0])
    dx = rng.normal(); dy = -abs(rng.normal()) * np.sign(dx) if dx != 0 else 1.0
    d = np.array([dx, dy, y0 * dx + x0 * dy]) * np.exp(rng.normal())      # grad q . d = 0, -dx dy > 0
    r = rng.normal(size=3) * 3
    if gq @ r <= 0.2 * np.linalg.norm(gq) * np.linalg.norm(r):
        continue
    p = rng.normal(size=3) * 2
    sbar = t - p
    if zc.qv(Q, b, c, sbar) <= 0.05 or gq @ (sbar - t) <= 0.1 * np.linalg.norm(gq) * np.linalg.norm(p):
        continue
    V = [t, t + d, t + r]
    P = np.stack([v - sbar for v in V], 1); w = np.ones(3)
    if abs(np.linalg.det(P)) < 1e-3:
        continue
    m2 = zc.my_supp2(Q, b, c, sbar, P, w)
    if abs(m2 - 1) > 1e-7:
        continue
    # uniqueness / support 1: other supports strictly worse
    others = [zc.my_supp2(Q, b, c, sbar, P[:, J], w[list(J)]) for J in ((1, 2), (0, 2))]
    if min(others[0], zc.first_hit(Q, b, c, sbar, P[:, 1]), zc.first_hit(Q, b, c, sbar, P[:, 2])) < 1 + 1e-6:
        continue
    try:
        sc, _ = zc.scip(Q, b, c, sbar, P, w, 1.0)
    except Exception:
        continue
    if abs(sc - 1) > 1e-5:
        continue
    lo, hi, Fb = 0.0, 1.0, None
    for _ in range(30):
        mid = (lo + hi) / 2
        F = on.feasible(sbar, V, mid)
        if F is not None:
            lo, Fb = mid, F
        else:
            hi = mid
    cert = on.exactA(Fb, sbar, [v - sbar for v in V])[0] if Fb is not None else 0.0
    n += 1; worst = min(worst, hi)
    print('inst %2d: z_K=1 (SCIP %.7f), orbit (A): bisection hi %.6f, certified %.6f' % (n, sc, hi, cert), flush=True)
    import json; open('rv_conj16_instances.jsonl', 'a').write(json.dumps(dict(n=n, sbar=sbar.tolist(), V=[v.tolist() for v in V], hi=hi, cert=cert, others=[float(o) for o in others])) + '\n')
print('worst orbit/z_K over %d degenerate support-1 corners: %.6f' % (n, worst))
