"""B&B of ann_tm restricted to a sub-box around the incumbent: min f over R intersected with
{u : |u - u*| <= rho * (box width)} (per coordinate).  Shows how the optimum's neighbourhood closes.

    python3 local_close.py rho tlim [tol_rel]
"""
import sys
import numpy as np
import ann_tm as at

rho = float(sys.argv[1]); tlim = float(sys.argv[2]); tol_rel = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-6
M = at.SepModel(); M.full_mu = False; M.old_min_relw = 1.0 / 16; M.grad_small = True
UB, u = at.incumbent(M)
M.lag, _ = at.kkt_lag(M, u)
sc = M.hi0 - M.lo0
lo = np.maximum(u - rho * sc, M.lo0)[None]; hi = np.minimum(u + rho * sc, M.hi0)[None]
r = at.bnb(M, UB, u, tol_rel * abs(UB), tlim, batch=512, init=(lo, hi, np.array([-np.inf])), log_every=10,
           log=lambda s: print(s, flush=True))
print(f"sub-box rho={rho}: done={r['done']} processed {r['processed']} open {r['open']} time {r['time']:.0f}s; "
      f"min f over R in sub-box >= {r['LB']!r} (UB {r['UB']!r}, gap {r['UB'] - r['LB']:.3g}, tol {tol_rel * abs(UB):.3g})")
