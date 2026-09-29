"""E8: explicit family S = {y^2 >= x^2 + 1}, xbar = (x0, 0), rays (-1,0), (0,1), w = (eps, 1).
SCIP default wedge vs horizontal strip vs corner bound."""
import numpy as np
from sfree import *
Q = np.diag([1.0, -1.0]); b = np.zeros(2); c = 1.0
P = np.array([[-1.0, 0.0], [0.0, 1.0]])
for x0, eps in [(10, 1e-3), (100, 1e-4), (1000, 1e-6), (2, 0.1)]:
    sbar = np.array([float(x0), 0.0]); w = np.array([eps, 1.0])
    G, cs = ms_set(Q, b, c, sbar)
    zms, al = ic_bound(G, sbar, P, w)
    Gs, _ = ms_set(Q, b, c, sbar, lam=np.array([0.0, 1.0]))   # strip |y| <= 1
    zst, als = ic_bound(Gs, sbar, P, w)
    zk = corner_bound(Q, b, c, sbar, P, w)
    pred_ms = min(eps * (x0 + 1 / x0), np.sqrt(x0 ** 2 + 1))
    print(f"x0={x0} eps={eps}: case={cs} z_MS={zms:.6g} (pred {pred_ms:.6g}), alphas={al}, z_strip={zst:.6g}, z_K={zk:.6g}, ratio MS/K={zms/zk:.3g}")
