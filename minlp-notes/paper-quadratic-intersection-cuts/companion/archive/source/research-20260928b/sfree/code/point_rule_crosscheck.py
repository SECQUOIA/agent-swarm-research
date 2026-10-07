"""Cross-check of point_rule_check.py misses (the code that produced logs/point_rule_crosscheck.log,
run inline): z_K vs SCIP, full orbit (SOCP), point-rule family, SCIP's own set."""
import numpy as np, warnings; warnings.filterwarnings('ignore')
import point_rule_check as prc
from core import corner_bound
from scout_sfree import ms_set, ic_bound, corner_bound_scip
from orbit_n1 import best_orbit
rng = np.random.default_rng(0)
for i in range(40):
    Q, b, c, sbar, P, w = prc.case2_instance(rng)
    zk = corner_bound(Q, b, c, sbar, P, w)
    if not np.isfinite(zk):
        continue
    zp = prc.point_rule_best(Q, b, c, sbar, P, w)
    if zp >= zk * (1 - 1e-6):
        continue
    G, case = ms_set(Q, b, c, sbar); zms = ic_bound(G, sbar, P, w)[0]
    try:
        zo, sig = best_orbit(Q, b, c, sbar, P, w, zk)
    except Exception:
        zo = float('nan')
    zs = corner_bound_scip(Q, b, c, sbar, P, w)
    print('inst %2d %s N=%d: zK %.6f (SCIP %.6f)  full orbit/zK %.6f  point rule/zK %.6f  SCIP set/zK %.6f'
          % (i, case, P.shape[1], zk, zs, zo / zk, zp / zk, min(zms, zk) / zk), flush=True)
