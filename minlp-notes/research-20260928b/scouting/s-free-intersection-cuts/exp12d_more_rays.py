"""E12d: (i) 2-variable quadratics worst case with many restarts; (ii) bilinear corners with n = 10 rays."""
import numpy as np, json
import exp12_orbit as E
from sfree import ms_set, ic_bound, corner_bound
import test_sfree
from test_sfree import rand_inst
out = {}
for label, k, n_, case, N, rs in [('gen k=2 n=3', 2, 3, None, 20, 60), ('bilin k=3 n=10', 3, 10, 'bilinear', 12, 60)]:
    test_sfree.rng = np.random.default_rng(51); E.rng = np.random.default_rng(52)
    rows = []
    for t in range(N):
        Q, b, c, sbar, P, w = rand_inst(k, n_, case)
        zk = corner_bound(Q, b, c, sbar, P, w)
        if not np.isfinite(zk):
            continue
        G0, cs = ms_set(Q, b, c, sbar)
        z0 = ic_bound(G0, sbar, P, w)[0]
        zl, zo = E.orbit_bound(Q, b, c, sbar, P, w, restarts=rs)
        rows.append((min(z0, zk) / zk, min(max(zl, zo), zk) / zk, cs))
    R = np.array([r[:2] for r in rows])
    out[label] = dict(n=len(R), scip_mean=float(R[:, 0].mean()), scip_min=float(R[:, 0].min()),
                      orbit_mean=float(R[:, 1].mean()), orbit_min=float(R[:, 1].min()),
                      orbit_frac_ge_0p999=float(np.mean(R[:, 1] >= 0.999)),
                      worst=[(round(a, 4), round(b_, 4), c_) for a, b_, c_ in sorted(rows, key=lambda r: r[1])[:3]])
    print('SUMMARY', label, out[label], flush=True)
json.dump(out, open('exp12d_more_rays.json', 'w'), indent=1)
