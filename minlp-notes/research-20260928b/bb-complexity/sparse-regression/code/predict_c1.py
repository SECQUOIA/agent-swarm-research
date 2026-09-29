"""Heuristic finite-size C1 predictor (primal balance at cap m0):
 pred = m0^2/lam - sum_l (|a_l| - m0)_+^2/n - max_l a_l^2/(n+lam) > 0.
Older version (witness-type, cap kappa<m0):, evaluated on the stored instances:
 pred = max_kappa [ (m0^2 - kappa^2)/lam - (p-k) ||r||^2 Psi(kappa/||r||)/n ],  Psi(t) = E(|Z|-t)_+^2.
Recomputes m0 and ||r|| from the instance (same seeds as exp_c1)."""
import json, sys, collections, numpy as np
from scipy.stats import norm
from core import instance, ridge
def Psi(t): return 2 * ((1 + t * t) * norm.sf(t) - t * norm.pdf(t))
d = collections.defaultdict(list)
for fn in sys.argv[1:]:
    for l in open(fn):
        r = json.loads(l)
        n, p, k, rule, seed = r['n'], r['p'], r['k'], r['rule'], r['seed']
        X, y, lam, S = (instance(n, p, k, seed=seed) if rule == 'sqrtn' else instance(n, p, k, seed=seed, tau0=float(rule)))
        f, b, res = ridge(X, y, lam, S); m0 = lam * np.abs(b).min(); R = np.linalg.norm(res)
        a = np.abs(X.T @ res); nul = [j for j in range(p) if j not in set(S)]
        gap = np.sum(np.maximum(a[nul] - m0, 0) ** 2) / n   # saturated gap at cap m0 (realized)
        pred = m0 ** 2 / lam - gap - np.max(a[nul]) ** 2 / (n + lam)
        d[(p, k, rule, n)].append((pred > 0, r['c1']))
print("p k rule n | N | predicted C1 | observed C1 (True/capped) | agree")
for key in sorted(d):
    v = d[key]
    print("%5d %3d %6s %4d | %d | %d | %d/%d | %d" % (*key, len(v), sum(a for a, _ in v), sum(c is True for _, c in v), sum(c == 'capped' for _, c in v),
          sum(a == (c is True or c == 'capped') for a, c in v)))

def agreement(rows):
    tot = agr = 0
    for r in rows:
        if True:
            n, p, k, rule, seed = r['n'], r['p'], r['k'], r['rule'], r['seed']
            X, y, lam, S = (instance(n, p, k, seed=seed) if rule == 'sqrtn' else instance(n, p, k, seed=seed, tau0=float(rule)))
            f, b, res = ridge(X, y, lam, S); m0 = lam * np.abs(b).min()
            a = np.abs(X.T @ res); nul = [j for j in range(p) if j not in set(S)]
            pred = m0 ** 2 / lam - np.sum(np.maximum(a[nul] - m0, 0) ** 2) / n - np.max(a[nul]) ** 2 / (n + lam)
            obs = r['c1'] is True or r['c1'] == 'capped'
            tot += 1; agr += ((pred > 0) == obs)
    return agr, tot
