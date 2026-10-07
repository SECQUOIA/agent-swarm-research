"""Dossier check (copy of the reviewer's certifier in /tmp): reproduce the tightest LP leaf of
eg_disc2_s part 1 and estimate how large a relative exp error the certificate tolerates."""
import glob, numpy as np
from fractions import Fraction as Fr
from scipy.optimize import linprog
import indep_cert as IC
th = Fr("5.642100574331458")
fs = sorted(glob.glob('../res/p1_c*.npz'))
L = [(np.load(f)['lo'], np.load(f)['hi'], np.load(f)['mg'], np.load(f)['how']) for f in fs]
lo = np.concatenate([a[0] for a in L]); hi = np.concatenate([a[1] for a in L])
mg = np.concatenate([a[2] for a in L]); how = np.concatenate([a[3] for a in L])
order = np.argsort(mg)[:5]
C = IC.Certifier('eg_disc2_s', "5.642100574331458")
M = C.M
print("sum|a| per row (objective rows max, e25..e28):", float(np.abs(M.A[:24]).sum(1).max()), np.abs(M.A[24:]).sum(1).round(1).tolist())
for j in order:
    l, h = lo[j:j+1], hi[j:j+1]
    c, r, beta, aL, aU = M.taylor(l, h)
    nlo, nhi = M.natural(l, h)
    ok = C._one(l[0], h[0], c[0], beta[0], aL[0], aU[0], nlo[0], nhi[0])
    # recompute the LP multipliers exactly as _one does
    rows, rhs, tags = [], [], []
    for k in range(24):
        if np.isfinite(aL[0, k]): rows.append(list(beta[0, k]) + [-1.0]); rhs.append(-(M.c[k] + aL[0, k])); tags.append(("obj", k))
    for jj in range(4):
        k = 24 + jj
        if M.qghi[jj] is not None and np.isfinite(aL[0, k]): rows.append(list(beta[0, k]) + [0.0]); rhs.append(M.ghi[jj] - aL[0, k]); tags.append(("up", k))
        if M.qglo[jj] is not None and np.isfinite(aU[0, k]): rows.append(list(-beta[0, k]) + [0.0]); rhs.append(aU[0, k] - M.glo[jj]); tags.append(("lo", k))
    dl = [Fr(a) - Fr(b) for a, b in zip(l[0], c[0])]; dh = [Fr(a) - Fr(b) for a, b in zip(h[0], c[0])]
    bounds = [(float(a), float(b)) for a, b in zip(dl, dh)] + [(None, None)]
    cost = np.zeros(M.d + 1); cost[-1] = 1
    res = linprog(cost, A_ub=np.array(rows), b_ub=np.array(rhs), bounds=bounds, method="highs")
    y = np.maximum(-np.asarray(res.ineqlin.marginals), 0.0)
    # sensitivity: weights times sum_m |w_km| at the centre (exp error enters through w)
    t = M.MU + M.S * c[0]
    E0 = (M.GA[:, None, :] * t * t).sum(-1)
    W = np.abs(M.A * np.exp(E0)).sum(-1)
    ys = sum(v for v, tg in zip(y, tags) if tg[0] == "obj")
    S = sum(v * W[tg[1]] for v, tg in zip(y, tags) if v > 0) / ys
    act = [(tg[0], tg[1] + 1, round(float(v / ys), 4)) for v, tg in zip(y, tags) if v > 1e-12]
    print(f"leaf {j}: recorded margin {mg[j]:.4e} how {how[j]}; reproduced ok={ok}; width {np.round(h[0]-l[0],8).tolist()}")
    print(f"   active multipliers (normalised by sum over objective rows): {act}")
    print(f"   sensitivity S = sum_k y_k sum_m|w_km| / sum_obj y = {S:.1f}; tolerated extra exp error ~ margin/S = {mg[j]/S:.2e}")
