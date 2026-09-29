"""E12c: re-optimize the orbit bound on the worst E12b-style instances with many restarts
(distinguishes optimizer failure from genuine insufficiency of the O(n,m)-orbit family)."""
import numpy as np, json
import exp12_orbit as E
from sfree import ms_set, ic_bound, corner_bound
import test_sfree
from test_sfree import rand_inst
test_sfree.rng = np.random.default_rng(41); E.rng = np.random.default_rng(42)
inst = []
for t in range(25):
    Q, b, c, sbar, P, w = rand_inst(3, 6, 'bilinear')
    zk = corner_bound(Q, b, c, sbar, P, w)
    if not np.isfinite(zk):
        continue
    zl, zo = E.orbit_bound(Q, b, c, sbar, P, w, restarts=16)
    inst.append((max(zl, zo) / zk, (Q, b, c, sbar, P, w, zk)))
inst.sort(key=lambda r: r[0])
res = []
for r0, (Q, b, c, sbar, P, w, zk) in inst[:3]:
    E.rng = np.random.default_rng(7)
    zl, zo = E.orbit_bound(Q, b, c, sbar, P, w, restarts=150)
    res.append((round(r0, 4), round(max(zl, zo) / zk, 4)))
    print('before', round(r0, 4), 'after 150 restarts', round(max(zl, zo) / zk, 4), flush=True)
json.dump(res, open('exp12c_worst_retry.json', 'w'))
