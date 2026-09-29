"""50% points (logistic fit in tau_hat^2 = (m0/||r||)^2) of exact C1, witness and PWE root certificate,
per (p, lam), from c1_lam.jsonl; compared with 2 log(p lam/n), 2 log p and the second-order heuristic
t = 2 log(p lam/n) + 0.93 - 5 log t (balance of Heuristic 3.8 with Psi(t) ~ 4 phi(t)/t^3)."""
import json, collections, numpy as np
from scipy.optimize import minimize, brentq

rows = [json.loads(l) for l in open('c1_lam.jsonl')]
d = collections.defaultdict(list)
for r in rows:
    d[(r['p'], r['lam'])].append(r)


def fit50(x, yv):
    x = np.asarray(x); yv = np.asarray(yv, float)
    if yv.min() == yv.max():
        return float('nan'), float('nan')
    nll = lambda w: np.sum(np.logaddexp(0, -(2 * yv - 1) * (w[0] + w[1] * (x - 7)))) + 0.05 * w[1] ** 2
    w = minimize(nll, [0.0, 1.0], method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-9, maxiter=4000)).x
    x50 = 7 - w[0] / w[1]
    # crude bootstrap standard error
    rng = np.random.default_rng(0); bs = []
    for _ in range(200):
        i = rng.integers(0, len(x), len(x))
        if yv[i].min() == yv[i].max(): continue
        ww = minimize(lambda w: np.sum(np.logaddexp(0, -(2 * yv[i] - 1) * (w[0] + w[1] * (x[i] - 7)))) + 0.05 * w[1] ** 2, w,
                      method='Nelder-Mead').x
        if ww[1] > 0: bs.append(7 - ww[0] / ww[1])
    return x50, float(np.std(bs))


print("p     lam   n/lam | 50% tau_hat^2: exact C1 (se) | witness (se) | root cert (se) || 2log(p lam/n)  heuristic-2nd  2log p | undecided")
for key in sorted(d):
    p, lam = key; v = d[key]; n = v[0]['n']
    x = [r['tau2'] for r in v]
    c1 = fit50(x, [r['status'] == 'C1' for r in v])
    wi = fit50(x, [r['wit'] for r in v]); rt = fit50(x, [r['pwe'] for r in v])
    L2 = 2 * np.log(p * lam / n)
    h2 = brentq(lambda t: t - (L2 + 0.93 - 5 * np.log(t)), 0.5, 60)
    und = sum(r['status'] not in ('C1', 'fail') for r in v)
    print(f"{p:5d} {lam:5.0f} {n/lam:6.1f} |   {c1[0]:5.2f} ({c1[1]:.2f})          | {wi[0]:5.2f} ({wi[1]:.2f}) | {rt[0]:5.2f} ({rt[1]:.2f})   || {L2:6.2f}        {h2:6.2f}      {2*np.log(p):6.2f} | {und}")
