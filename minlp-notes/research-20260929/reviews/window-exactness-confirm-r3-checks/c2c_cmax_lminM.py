"""Round-3 confirmation, item 3 probe: inf and max |lambda_min(M) - 2 eps| for cmax on A and A0 over the log
segment (4000 geometric points from 1e-8 to 0.049), P' from the lam = log(s) dense output, three lam steps."""
import sys, numpy as np
sys.path.insert(0, '.')
from c2_aniso import *
for ex in ("A", "A0"):
    p = EX[ex]; eps = 0.02
    Pf, _ = continuous_family(p, eps, delta1=None)
    th = find_switch(p)[0]; lay = th + 0.05
    segs_cl = [c.cell_contents for c in Pf.__closure__ if isinstance(c.cell_contents, list)][0]
    sol2 = [f for lo, hi, f in segs_cl if abs(lo - th) < 1e-9 and abs(hi - lay) < 1e-12][0].__defaults__[0]
    Q = lambda lam: np.asarray(sol2(lam)).reshape(2, 2)
    ss = np.geomspace(1e-8, 0.049, 4000)
    for hl in (1e-2, 3e-3, 1e-3):
        dev = []
        for s in ss:
            lam = np.log(s); P = Q(lam); dP = five(Q, lam, hl) / s
            M = dP + A.T @ P + P @ A + p.Hxx; M = (M + M.T) / 2
            dev.append(np.linalg.eigvalsh(M)[0] - 2 * eps)
        dev = np.array(dev); i, j = dev.argmin(), np.abs(dev).argmax()
        print(ex, f"hl={hl:g}: min dev {dev[i]:+.2e} at s={ss[i]:.2e}; max |dev| {abs(dev[j]):.2e} at s={ss[j]:.2e}; "
              f"max |dev| for s>=1e-6: {np.abs(dev[ss >= 1e-6]).max():.2e}")
