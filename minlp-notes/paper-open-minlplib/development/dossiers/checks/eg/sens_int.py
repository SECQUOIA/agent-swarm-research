"""Dossier check: LP certificate sensitivity near the eg_int_s optimum (boxes around the saved
point, integers fixed), with the reviewer's certifier copied to /tmp."""
import numpy as np
from fractions import Fraction as Fr
from scipy.optimize import linprog
import indep_cert as IC
C = IC.Certifier('eg_int_s', "6.4531031529331155"); M = C.M
sol = dict(l.split() for l in open('../eg_int_s.retry.sol'))
x = np.array([float(sol[v]) for v in M.vars])
for hw in [1e-4, 1e-5, 1e-6, 1e-7]:
    lo = x.copy(); hi = x.copy()
    for i in range(4):
        lo[i] = max(x[i] - hw, M.lb[i]); hi[i] = min(x[i] + hw, M.ub[i])
    l, h = lo[None], hi[None]
    c, r, beta, aL, aU = M.taylor(l, h); nlo, nhi = M.natural(l, h)
    rows, rhs, tags = [], [], []
    for k in range(24):
        rows.append(list(beta[0, k]) + [-1.0]); rhs.append(-(M.c[k] + aL[0, k])); tags.append(("obj", k))
    for jj in range(4):
        k = 24 + jj
        if M.qghi[jj] is not None: rows.append(list(beta[0, k]) + [0.0]); rhs.append(M.ghi[jj] - aL[0, k]); tags.append(("up", k))
        if M.qglo[jj] is not None: rows.append(list(-beta[0, k]) + [0.0]); rhs.append(aU[0, k] - M.glo[jj]); tags.append(("lo", k))
    dl = [Fr(a) - Fr(b) for a, b in zip(l[0], c[0])]; dh = [Fr(a) - Fr(b) for a, b in zip(h[0], c[0])]
    bounds = [(float(a), float(b)) for a, b in zip(dl, dh)] + [(None, None)]
    cost = np.zeros(M.d + 1); cost[-1] = 1
    res = linprog(cost, A_ub=np.array(rows), b_ub=np.array(rhs), bounds=bounds, method="highs")
    y = np.maximum(-np.asarray(res.ineqlin.marginals), 0.0)
    v = C._dual_value(y, tags, [[Fr(float(b)) for b in beta[0, k]] for k in range(28)], aL[0], aU[0], dl, dh)
    t = M.MU + M.S * c[0]; E0 = (M.GA[:, None, :] * t * t).sum(-1); W = np.abs(M.A * np.exp(E0)).sum(-1)
    ys = sum(vv for vv, tg in zip(y, tags) if tg[0] == "obj")
    S = sum(vv * W[tg[1]] for vv, tg in zip(y, tags) if vv > 0) / ys
    act = [(tg[0], tg[1] + 1, round(float(vv / ys), 3)) for vv, tg in zip(y, tags) if vv > 1e-12]
    # size of the padding in the combined bound: sum_k y_k (G_k - aL_k - |beta.d| terms) is not separated here;
    print(f"half-width {hw:g}: LP bound - theta* = {float(v - C.theta):.3e}; multipliers {act}; S = {S:.0f}; margin/S = {float(v - C.theta)/S:.2e}")
