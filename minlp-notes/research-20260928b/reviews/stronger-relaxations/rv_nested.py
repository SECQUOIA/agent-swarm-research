"""Check 4: spot checks on the nested n = 40 designs (note Sections 7.2-7.3), reviewer code only.
mode p100 SEED : perspective, SDP1, sdp_2 (and zb if ZB=1) at p = 100, OPT by enumeration, PWE ratio.
mode r3200 SEED: restricted instance S* u top-60 nulls at p = 3200 (persp, SDP1, sdp_2), and my own
                 certified upper bound on the FULL p = 3200 L_2 root from Lemma 4.1(ii):
                 F = S* u top-h violators, Z1 = [p] minus F, eps2 = min_sigma bracket, and
                 min over z in K with supp z in F of the inflated perspective (convex program; any
                 feasible (z, beta) gives a valid bound, recomputed in numpy).
usage: rv_nested.py MODE SEED"""
import os as _os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"]:
    _os.environ[_v] = "1"
import os, sys, json, time
import numpy as np
import cvxpy as cp
from rv_common import gen_nested, fval, persp, sdp1, sdp2, zb_vec as zb
from rv_enum import opt3

mode, seed = sys.argv[1], int(sys.argv[2])
out = dict(mode=mode, seed=seed)
t0 = time.time()
if mode == 'p100':
    X, y, lam, S = gen_nested(40, 3, 3200, 100, seed)
    fS, bS, r = fval(X, y, lam, S)
    a = np.abs(X.T @ r); a[list(S)] = 0
    out.update(fS=fS, ratio=float(a.max() / (lam * np.abs(bS).min())), nviol=int((a > lam * np.abs(bS).min()).sum()))
    out['OPT'], out['arg'] = opt3(X, y, lam)
    out['persp'] = persp(X, y, lam, 3)
    out['sdp1'] = sdp1(X, y, lam, 3)
    if os.environ.get('SDP2', '0') == '1':
        out['sdp2'] = sdp2(X, y, lam, 3)
    if os.environ.get('ZB', '0') == '1':
        zs = os.environ.get('ZBSOLVER', 'CLARABEL')
        out['zb'] = zb(X, y, lam, 3, solver=zs); out['zb_solver'] = zs
else:
    X, y, lam, S = gen_nested(40, 3, 3200, 3200, seed)
    p = X.shape[1]
    fS, bS, r = fval(X, y, lam, S)
    a = np.abs(X.T @ r); a[list(S)] = -1
    order = [int(j) for j in np.argsort(-a)]
    C = list(S) + order[:60]
    Xc = X[:, C]
    out.update(fS=fS, r_persp=persp(Xc, y, lam, 3), r_sdp1=sdp1(Xc, y, lam, 3))
    if os.environ.get('SDP2', '1') == '1':
        out['r_sdp2'] = sdp2(Xc, y, lam, 3)
    best = (np.inf, None)
    for h in (1, 2, 3, 5, 8, 12):
        F = list(S) + order[:h]
        Z1 = np.setdiff1d(np.arange(p), F)
        W = X[:, Z1] @ X[:, Z1].T
        Wi = np.linalg.inv(W)
        XF = X[:, F]
        theta = float(np.linalg.eigvalsh(XF.T @ Wi @ XF).max())
        qmax = float(np.max(np.einsum('im,im->m', X[:, Z1], Wi @ X[:, Z1])))
        sg = np.logspace(-4, 1, 2001)
        e2 = float(np.min(sg + (1 + sg) * theta * (1 + 1 / (sg * (1 - qmax)))))
        Hm = XF.T @ XF - lam * e2 * np.eye(len(F))
        if np.linalg.eigvalsh(Hm).min() <= 0:
            continue
        zc, bc, tc = cp.Variable(len(F)), cp.Variable(len(F)), cp.Variable(len(F))
        cons = [zc >= 0, zc <= 1, cp.sum(zc) <= 3, cp.SOC(zc + tc, cp.vstack([2 * bc, zc - tc]), axis=0)]
        obj = cp.quad_form(bc, cp.psd_wrap(Hm)) - 2 * (XF.T @ y) @ bc + lam * (1 + e2) * cp.sum(tc)
        cp.Problem(cp.Minimize(obj), cons).solve(solver=cp.CLARABEL)
        z = np.clip(zc.value, 0, 1); z = z * min(1.0, 3 / z.sum())
        bF = np.where(z > 1e-12, bc.value, 0.0)
        nz = z > 1e-12
        val = float(np.sum((y - XF @ bF) ** 2) + lam * bF @ bF + lam * (1 + e2) * np.sum(bF[nz] ** 2 * (1 / z[nz] - 1)))
        if val < best[0]:
            best = (val, dict(h=h, theta=theta, qmax=qmax, eps2=e2))
    out['L2_ub_full'] = best[0]; out['L2_ub_info'] = best[1]
    out['L2_ub_minus_fS'] = best[0] - fS
out['time'] = round(time.time() - t0, 1)
print(json.dumps(out, default=float), flush=True)
