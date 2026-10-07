"""Diagnostics for check_dump.py findings: list rays where SCIP's step length differs from the bisection reference
(relative difference > TOL), with the case data, and recompute z_K for corners with z_C > z_K.
Usage: python3 diag_dump.py DUMP [MAXCORNERS] [TOL]
"""
import sys, json, gzip
import numpy as np
from check_dump import Corner, reduced, rho, corner_bound

path = sys.argv[1]; maxc = int(sys.argv[2]) if len(sys.argv) > 2 else 60
TOL = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-6
lines = [json.loads(l.replace('-nan', 'NaN').replace('nan', 'NaN')) for l in gzip.open(path, 'rt') if l.strip()]
k = 0; nc = 0
while k < len(lines) and nc < maxc:
    d = lines[k]; fin = lines[k + 1] if k + 1 < len(lines) and lines[k + 1]['type'] == 'final' else None
    k += 2 if fin is not None else 1
    if d['type'] != 'corner':
        continue
    nc += 1
    c = Corner(d)
    lam0 = np.array(d['lam0']); lam = np.array(d['lam'])
    N = c.P.shape[1]
    for name, al, l in (('alpha0', d['alpha0'], lam0), ('alpha', d['alpha'], lam if d['changed'] else lam0)):
        for j in range(N):
            a = np.inf if al[j] < 0 else al[j]
            b = c.step(l, c.P[:, j])
            if np.isinf(a) and np.isinf(b):
                continue
            if np.isinf(a) != np.isinf(b):
                if max(a if np.isfinite(a) else 0, b if np.isfinite(b) else 0) > 1e9:
                    continue
            rel = abs(a - b) / max(1.0, abs(b)) if np.isfinite(a) and np.isfinite(b) else 1.0
            if rel > TOL:
                # check the gauge at the C step length and q along the ray
                g_at = c.G(l, c.sbar + a * c.P[:, j]) if np.isfinite(a) else None
                q_mid = c.q(c.sbar + 0.5 * (a + b) * c.P[:, j]) if np.isfinite(a) and np.isfinite(b) else None
                print(json.dumps(dict(corner=nc, which=name, ray=j, case4=c.iscase4, kappa=c.kappa, dim=d['dim'],
                                      C=a, ref=b, rel=rel, G_at_C=g_at, q_between=q_mid, qbar=c.q(c.sbar),
                                      changed=d['changed'])))
    # z_K violation check
    wt = np.maximum(c.w, 1e-6 * max(c.w.max(), 1e-9))
    ref0 = np.array([c.step(lam0, c.P[:, j]) for j in range(N)])
    zC0 = min([wt[j] * ref0[j] for j in range(N) if np.isfinite(ref0[j])], default=np.inf)
    rh = rho(c)
    if rh <= 4 and N <= 40:
        Qr, br, cr, tbar, Pr = reduced(c)
        zk = corner_bound(Qr, br, cr, tbar, Pr, wt, max_support=min(rh, np.linalg.matrix_rank(Pr)))
        if np.isfinite(zk) and zC0 > zk + 1e-6 * max(1.0, abs(zk)):
            jmin = int(np.argmin([wt[j] * ref0[j] if np.isfinite(ref0[j]) else np.inf for j in range(N)]))
            # direct search for a feasible corner point below zC0: sample lambda on the simplex face of 1-2 rays
            best = np.inf
            rng = np.random.default_rng(0)
            for _ in range(20000):
                J = rng.choice(N, size=min(2, N), replace=False)
                lamv = np.zeros(N); lamv[J] = rng.exponential(size=len(J)) 
                lamv *= zC0 / (wt @ lamv)          # on the level set w^T lam = zC0
                for t in (0.5, 0.8, 0.95, 0.99, 1.0):
                    if c.q(c.sbar + c.P @ (t * lamv)) <= 0:
                        best = min(best, t * zC0); break
            print(json.dumps(dict(corner=nc, ZK_CHECK=True, zC0=zC0, zK=zk, rho=rh, rankP=int(np.linalg.matrix_rank(Pr)),
                                  sampled_feasible_below=best, N=N, case4=c.iscase4, kappa=c.kappa)))
