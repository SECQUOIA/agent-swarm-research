"""E1: one-cut bound of SCIP's constant-Gamma maximal quadratic-free set
versus the best possible intersection-cut bound (corner bound z_K)."""
import numpy as np, json
from sfree import *
from test_sfree import rand_inst
import test_sfree
rng = np.random.default_rng(1)
test_sfree.rng = rng
out = {}
for label, k, n, case in [('gen k=2 n=2', 2, 2, None), ('gen k=2 n=6', 2, 6, None),
                          ('gen k=3 n=3', 3, 3, None), ('gen k=3 n=8', 3, 8, None),
                          ('gen k=4 n=4', 4, 4, None), ('gen k=4 n=8', 4, 8, None),
                          ('bilin k=3 n=3', 3, 3, 'bilinear'), ('bilin k=3 n=8', 3, 8, 'bilinear')]:
    rs = []
    viol = 0
    for t in range(300):
        Q, b, c, sbar, P, w = rand_inst(k, n, case)
        G, cs = ms_set(Q, b, c, sbar)
        zms, al = ic_bound(G, sbar, P, w)
        zk = corner_bound(Q, b, c, sbar, P, w)
        if not np.isfinite(zk):
            continue  # K cap S empty: every a >= 0 valid; skip
        if zms > zk * (1 + 1e-6) + 1e-9:
            viol += 1
        rs.append(min(zms, zk) / zk if np.isfinite(zms) else 0.0)
    rs = np.array(rs)
    out[label] = dict(n=len(rs), mean=float(rs.mean()), median=float(np.median(rs)),
                      q10=float(np.quantile(rs, 0.1)), frac_opt=float(np.mean(rs > 1 - 1e-6)),
                      frac_below_half=float(np.mean(rs < 0.5)), validity_violations=viol)
    print(label, out[label])
json.dump(out, open('exp1_ratio.json', 'w'), indent=1)
