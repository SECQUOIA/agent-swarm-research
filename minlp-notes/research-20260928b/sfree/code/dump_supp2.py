"""Re-generate the support-2 instances of explore_supp2.py (seed 0, N=3) and
cross-check z_K for the non-exact ones with SCIP; save them to ../logs/supp2_instances.json."""
import json, numpy as np, warnings; warnings.filterwarnings('ignore')
from core import bilinear_quadratic, corner_bound, qval
from scout_sfree import corner_bound_scip
rng = np.random.default_rng(0); N = 3; got = 0; out = []
while got < 25:
    side = '+' if rng.random() < 0.5 else '-'
    Q, b, c = bilinear_quadratic(side)
    while True:
        sbar = rng.normal(size=3)
        if qval(Q, b, c, sbar) > 0.05: break
    P = rng.normal(size=(3, N)); w = rng.uniform(0.1, 1.0, N)
    zk, lam = corner_bound(Q, b, c, sbar, P, w, return_point=True)
    if not np.isfinite(zk) or np.sum(lam > 1e-9) != 2: continue
    got += 1
    if got in (1, 12, 25):
        zs = corner_bound_scip(Q, b, c, sbar, P, w)
        print('instance', got, 'zK', zk, 'SCIP', zs, 'lam', lam)
        out.append(dict(id=got, side=side, sbar=sbar.tolist(), P=P.tolist(), w=w.tolist(), zK=zk, lam=lam.tolist()))
json.dump(out, open('../logs/supp2_instances.json', 'w'), indent=1)
