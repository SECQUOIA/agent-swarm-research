"""E2: does optimizing the constant Gamma (lambda) close the gap to z_K?
Grid search over unit lambda (d = 2: 720 angles; d = 3: 1500 random + NM refine)."""
import numpy as np, json
from scipy.optimize import minimize
from sfree import *
import test_sfree
from test_sfree import rand_inst
rng = np.random.default_rng(2)
test_sfree.rng = rng


def lam_dim(Q, b, c, sbar):
    G, cs = ms_set(Q, b, c, sbar)
    th = np.linalg.eigvalsh(Q)
    npos = int(np.sum(th > 1e-9))
    return cs, (npos if cs in ('case1', 'case3') else npos + 1)


def zlam(Q, b, c, sbar, P, w, L):
    G, _ = ms_set(Q, b, c, sbar, lam=L)
    if G(sbar) >= -1e-12:
        return 0.0
    return min(ic_bound(G, sbar, P, w)[0], 1e9)


def best_lambda_bound(Q, b, c, sbar, P, w):
    cs, d = lam_dim(Q, b, c, sbar)
    if d == 1:
        return zlam(Q, b, c, sbar, P, w, np.array([1.0])), cs
    if d == 2:
        best = 0
        for th in np.linspace(0, 2 * np.pi, 721)[:-1]:
            best = max(best, zlam(Q, b, c, sbar, P, w, np.array([np.cos(th), np.sin(th)])))
        return best, cs
    V = rng.normal(size=(1500, d)); V /= np.linalg.norm(V, axis=1)[:, None]
    vals = [zlam(Q, b, c, sbar, P, w, v) for v in V]
    best = max(vals)
    for i in np.argsort(vals)[-3:]:
        f = lambda v: -zlam(Q, b, c, sbar, P, w, v / max(np.linalg.norm(v), 1e-12))
        r = minimize(f, V[i], method='Nelder-Mead', options=dict(maxiter=200))
        best = max(best, -r.fun)
    return best, cs


if __name__ == '__main__':
    out = {}
    for label, k, n, case in [('gen k=2 n=2', 2, 2, None), ('gen k=2 n=5', 2, 5, None),
                              ('bilin k=3 n=3', 3, 3, 'bilinear'), ('bilin k=3 n=6', 3, 6, 'bilinear'),
                              ('gen k=3 n=4', 3, 4, None)]:
        r0, r1, cases = [], [], {}
        for t in range(40):
            Q, b, c, sbar, P, w = rand_inst(k, n, case)
            zk = corner_bound(Q, b, c, sbar, P, w)
            if not np.isfinite(zk):
                continue
            G, cs = ms_set(Q, b, c, sbar)
            z0 = ic_bound(G, sbar, P, w)[0]
            z1, cs = best_lambda_bound(Q, b, c, sbar, P, w)
            z1 = max(z1, min(z0, 1e9))
            r0.append(min(z0, zk) / zk); r1.append(min(z1, zk) / zk)
            cases[cs] = cases.get(cs, 0) + 1
        r0, r1 = np.array(r0), np.array(r1)
        out[label] = dict(n=len(r0), default_mean=float(r0.mean()), bestlam_mean=float(r1.mean()),
                          default_q10=float(np.quantile(r0, .1)), bestlam_q10=float(np.quantile(r1, .1)),
                          default_min=float(r0.min()), bestlam_min=float(r1.min()),
                          bestlam_frac_opt=float(np.mean(r1 > 1 - 1e-3)), cases=cases)
        print(label, out[label], flush=True)
    json.dump(out, open('exp2_bestlambda.json', 'w'), indent=1)
