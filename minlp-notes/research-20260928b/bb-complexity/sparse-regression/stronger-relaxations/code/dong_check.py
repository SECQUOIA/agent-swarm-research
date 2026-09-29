"""Exact root-exactness decision for SDP1 (optimal perspective) by Dong's Theorem 2 (arXiv 1603.04572),
evaluated at the optimal support T (exact OPT support from opt_check.py).

SDP1 is exact at T iff there is lt > 0 with
    f(lt) = lambda_max( D(lt) - X'X/lam - I ) <= 0,
    D_ii = lt / a_i^2 (i in T),   D_ii = a_i^2 / lt (i not in T),   a = X' r_T  (a_i = lam beta^T_i on T).
f is convex in lt (Dong, Section 3.1); we minimize it over log(lt) on Dong's initial interval
[max_{i not in T} a_i^2/(|x_i|^2/lam + 1), min_{i in T} a_i^2 (|x_i|^2/lam + 1)] (empty interval => not exact).
Output: min f, relative to the scale ||X'X/lam + I|| (exact if <= 1e-10).
usage: dong_check.py OUT mech FILE OPTFILE   |   dong_check.py OUT cmp FILE OPTFILE"""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import sys, json
import numpy as np
from scipy.optimize import minimize_scalar
from relax import ridge, instance
from exp_mech import make


def dong_min(X, y, lam, T):
    p = X.shape[1]
    T = list(T)
    fT, bT, r = ridge(X, y, lam, T)
    a2 = (X.T @ r) ** 2
    inT = np.zeros(p, bool); inT[T] = True
    if np.any(a2[inT] == 0):
        return np.inf
    M = X.T @ X / lam + np.eye(p)
    diagM = np.diag(M)
    lo = np.max(a2[~inT] / diagM[~inT]); hi = np.min(a2[inT] * diagM[inT])
    scale = np.linalg.eigvalsh(M).max()
    if lo > hi:
        return float('inf')

    def f(u):
        lt = np.exp(u)
        d = np.where(inT, lt / a2, a2 / lt)
        return np.linalg.eigvalsh(np.diag(d) - M).max() / scale

    us = np.linspace(np.log(lo), np.log(hi), 41) if hi > lo else np.array([np.log(lo)])
    vals = [f(u) for u in us]
    b = int(np.argmin(vals))
    if len(us) > 1:
        a_, c_ = us[max(b - 1, 0)], us[min(b + 1, len(us) - 1)]
        res = minimize_scalar(f, bounds=(a_, c_), method='bounded', options=dict(xatol=1e-12))
        return float(min(res.fun, vals[b]))
    return float(vals[b])


if __name__ == '__main__':
    OUT, kind, fn, optfn = sys.argv[1:5]
    opt = {}
    for l in open(optfn):
        o = json.loads(l); opt[(o['p'], o['seed'], o['n'])] = o
    with open(OUT, 'w') as f:
        for l in open(fn):
            r = json.loads(l)
            if r.get('sdp1') is None:
                continue
            o = opt.get((r['p'], r['seed'], r['n']))
            if o is None or 'OPT_support' not in o:
                continue
            if kind == 'mech':
                X, y, lam, S = make(r['n'], r['k'], 2560 if r['n'] == 20 else 3200, r['p'], r['seed'])
            else:
                X, y, lam, S = instance(r['n'], r['p'], r['k'], seed=r['seed'], tau0=1.5)
            m = dong_min(X, y, lam, o['OPT_support'])
            OPT = o['OPT']
            out = dict(n=r['n'], p=r['p'], seed=r['seed'], alpha=r.get('alpha'), dong_minf=m, dong_exact=bool(m <= 1e-10),
                       solver_exact=bool((OPT - r['sdp1']) <= 1e-6 * OPT), solver_gap=(OPT - r['sdp1']) / OPT)
            f.write(json.dumps(out) + '\n'); f.flush()
            print(out, flush=True)
