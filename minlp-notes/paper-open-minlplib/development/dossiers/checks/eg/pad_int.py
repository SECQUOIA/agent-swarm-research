"""Dossier check: size of the a-posteriori padding (G - aL) of the reviewer's certifier for rows
e12 and e26 on small boxes around the eg_int_s point, combined with the LP multiplier 22.27."""
import numpy as np
import indep_cert as IC
M = IC.Model('eg_int_s')
sol = dict(l.split() for l in open('../eg_int_s.retry.sol'))
x = np.array([float(sol[v]) for v in M.vars])
for hw in [1e-6, 1e-7, 1e-9]:
    lo = x.copy(); hi = x.copy()
    for i in range(4):
        lo[i] = max(x[i] - hw, M.lb[i]); hi[i] = min(x[i] + hw, M.ub[i])
    c, r, beta, aL, aU = M.taylor(lo[None], hi[None])
    t = M.MU + M.S * c[0]; E0 = (M.GA[:, None, :] * t * t).sum(-1)
    G = (M.A * np.exp(E0)).sum(-1) + M.LIN @ c[0]
    pad = G - aL[0]
    print(f"half-width {hw:g}: G-aL e12 {pad[11]:.3e}, e26 {pad[25]:.3e}; combined e12 + 22.27*e26 = {pad[11] + 22.27*pad[25]:.3e}")
