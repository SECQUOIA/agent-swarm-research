"""Exact maximum clique of the midpoint-conflict graph on the 600 best supports for the one instance where
the author's greedy clique (8) exceeded mine (k=4, alpha=1, pure noise, seed 3002)."""
import os
os.environ['OMP_NUM_THREADS'] = '1'
import itertools, json, numpy as np
from common import g_closed

def inst(n, p, k, b, seed, sigma=0.5):
    rng = np.random.default_rng(seed); X = rng.standard_normal((n, p)); S = np.sort(rng.choice(p, k, replace=False))
    beta = np.zeros(p)
    if b > 0: beta[S] = b * rng.choice([-1.0, 1.0], k)
    return X, X @ beta + sigma * rng.standard_normal(n)

r = [json.loads(l) for l in open('../../bb-complexity/sparse-regression/data/hard_k3-8.jsonl')]
r = [x for x in r if x['k'] == 4 and x['alpha'] == 1.0 and x['b'] == 0.0 and x['seed'] == 3002][0]
n, p, k, lam = r['n'], r['p'], r['k'], r['lam']; X, y = inst(n, p, k, 0.0, 3002)
def f_of(T):
    XT = X[:, T]; return float(y @ y - (XT.T @ y) @ np.linalg.solve(XT.T @ XT + lam * np.eye(len(T)), XT.T @ y))
vals = {T: f_of(list(T)) for T in itertools.combinations(range(p), k)}; OPT = min(vals.values())
best = sorted(vals, key=vals.get)[:600]; m = len(best)
nb = [0] * m
for i in range(m):
    for j in range(i + 1, m):
        z = np.zeros(p); z[list(best[i])] += 0.5; z[list(best[j])] += 0.5
        if g_closed(X, y, lam, z)[0] < OPT * (1 - 1e-7):
            nb[i] |= 1 << j; nb[j] |= 1 << i
bestc = [0]
def expand(R, P):
    if P == 0:
        bestc[0] = max(bestc[0], R); return
    if R + bin(P).count('1') <= bestc[0]:
        return
    while P:
        if R + bin(P).count('1') <= bestc[0]: return
        v = P.bit_length() - 1
        expand(R + 1, P & nb[v]); P &= ~(1 << v)
expand(0, (1 << m) - 1)
print('exact max clique among 600 best supports:', bestc[0], '| author reported', r['clique'], '| leaves', (r['nodes'] + 1) // 2)
