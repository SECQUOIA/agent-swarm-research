"""quick test of the ANN third-order bound: fathoming near the optimum and soundness on samples."""
import time
import numpy as np
from fractions import Fraction as Fr
import ann_h3 as ah
M = ah.H3Model(); N = M.D['names']
M.lag = [(N.index('x647'), Fr(58.509053436320386), Fr(-1), 1), (N.index('x772'), Fr(20891.433722402617), Fr('0.999'), 1)]
u = np.array([370.9280572920674, 0.7863373968889928, 1.620252679906157, 0.9494678019619749, 0.734065236105183])
fstar = -3379.982394046125
rng = np.random.default_rng(0)
scale = (M.hi0 - M.lo0)
for rho in [0.02, 0.005, 0.001]:
    e = rng.standard_normal((256, 5)); e /= np.linalg.norm(e, axis=1)[:, None]
    c = np.clip(u + rho * scale * e, M.lo_in, M.hi_in); r = 0.25 * rho * scale / np.sqrt(5)
    lo = np.maximum(c - r, M.lo0); hi = np.minimum(c + r, M.hi0)
    t = time.time(); R3 = M.fbound3(lo, hi); dt = time.time() - t
    R1 = M.fbound(lo, hi)
    ok = np.isfinite(R1['lb'])
    print(f"rho={rho}: fathomed first-order {np.mean(R1['lb'][ok] >= fstar):.2f}, third-order {np.mean(R3['lb'][ok] >= fstar):.2f}; "
          f"infeasible {np.mean(~ok):.2f}; {dt / 256 * 1e3:.1f} ms/box", flush=True)
viol = 0; tot = 0
for rho in [0.05, 0.01, 0.002]:
    c = np.clip(u + rho * scale * rng.standard_normal((60, 5)), M.lo_in, M.hi_in)
    lo = np.maximum(c - rho * scale / 2, M.lo0); hi = np.minimum(c + rho * scale / 2, M.hi0)
    R3 = M.fbound3(lo, hi)
    for k in range(60):
        for p in lo[k] + (hi[k] - lo[k]) * rng.random((15, 5)):
            okp, fv = M.point_value(np.clip(p, M.lo_in, M.hi_in))
            tot += 1
            if okp and fv < R3['lb'][k] - 1e-9:
                viol += 1
print('soundness violations', viol, 'of', tot, flush=True)
