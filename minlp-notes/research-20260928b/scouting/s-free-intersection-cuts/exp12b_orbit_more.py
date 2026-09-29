"""E12b: orbit selection on bilinear corners with more rays (n = 6) and random k = 3 quadratics."""
import numpy as np, json
import exp12_orbit as E
from sfree import ms_set, ic_bound, corner_bound
import test_sfree
from test_sfree import rand_inst
test_sfree.rng = np.random.default_rng(41); E.rng = np.random.default_rng(42)
out = {}
for label, k, n_, case, N in [('bilin k=3 n=6', 3, 6, 'bilinear', 25), ('gen k=3 n=4', 3, 4, None, 25)]:
    rows = []
    for t in range(N):
        Q, b, c, sbar, P, w = rand_inst(k, n_, case)
        zk = corner_bound(Q, b, c, sbar, P, w)
        if not np.isfinite(zk):
            continue
        G0, cs = ms_set(Q, b, c, sbar)
        z0 = ic_bound(G0, sbar, P, w)[0]
        zl, zo = E.orbit_bound(Q, b, c, sbar, P, w, restarts=16)
        rows.append((min(z0, zk) / zk, min(zl, zk) / zk, min(max(zo, zl), zk) / zk))
    R = np.array(rows)
    out[label] = dict(n=len(R), scip_mean=float(R[:, 0].mean()), lam_mean=float(R[:, 1].mean()), orbit_mean=float(R[:, 2].mean()),
                      scip_min=float(R[:, 0].min()), lam_min=float(R[:, 1].min()), orbit_min=float(R[:, 2].min()),
                      orbit_frac_ge_0p99=float(np.mean(R[:, 2] >= 0.99)))
    print('SUMMARY', label, out[label], flush=True)
json.dump(out, open('exp12b_orbit_more.json', 'w'), indent=1)
