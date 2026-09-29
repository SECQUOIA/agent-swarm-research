"""Light independent check of Tables 6.4/6.5 inputs for k = 3, 4: exact OPT by enumeration of all supports
(compared with the B&B 'opt' stored by the author), and a greedy clique of the midpoint-conflict graph
on the 300 best supports, with conflicts evaluated by my own g((1_S+1_T)/2) (closed form (F3)).
Instances follow the data specification of exp_hard.py (b = 0: no sign draw)."""
import json, itertools
from common import g_closed
import numpy as np

D = '../../bb-complexity/sparse-regression/data/'
recs = [json.loads(l) for l in open(D + 'hard_k3-8.jsonl')]
recs = [r for r in recs if r['k'] in (3, 4)]


def inst(n, p, k, b, seed, sigma=0.5):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, p))
    S = np.sort(rng.choice(p, k, replace=False))
    beta = np.zeros(p)
    if b > 0:
        beta[S] = b * rng.choice([-1.0, 1.0], k)
    y = X @ beta + sigma * rng.standard_normal(n)
    return X, y


def f_of(X, y, lam, T):
    XT = X[:, T]
    return float(y @ y - (XT.T @ y) @ np.linalg.solve(XT.T @ XT + lam * np.eye(len(T)), XT.T @ y))


worst = 0.0; bad_cl = []
for r in recs:
    n, p, k, b, seed, lam = r['n'], r['p'], r['k'], r['b'], r['seed'], r['lam']
    X, y = inst(n, p, k, b, seed)
    vals = {T: f_of(X, y, lam, list(T)) for T in itertools.combinations(range(p), k)}
    OPT = min(vals.values())
    worst = max(worst, abs(OPT - r['opt']) / OPT)
    best = sorted(vals, key=vals.get)[:300]
    m = len(best); adj = np.zeros((m, m), bool)
    for i in range(m):
        for j in range(i + 1, m):
            z = np.zeros(p); z[list(best[i])] += 0.5; z[list(best[j])] += 0.5
            if g_closed(X, y, lam, z)[0] < OPT * (1 - 1e-7):
                adj[i, j] = adj[j, i] = True
    cl_best = 0
    deg = adj.sum(1)
    for start in range(m):
        cl = [start]; cand = adj[start].copy()
        for j in np.argsort(-deg):
            if cand[j]:
                cl.append(j); cand &= adj[j]
        cl_best = max(cl_best, len(cl))
    if cl_best < r.get('clique', 0) or r.get('clique', 0) > (r['nodes'] + 1) // 2:
        bad_cl.append((k, r['alpha'], b, seed, r.get('clique'), cl_best, r['nodes']))
    print(f"k={k} alpha={r['alpha']} b={b} seed={seed}: OPT enum {OPT:.6f} vs B&B {r['opt']:.6f}; clique author {r.get('clique')}, mine (greedy, 300 best) {cl_best}; B&B nodes {r['nodes']}", flush=True)
print("max relative OPT discrepancy:", worst)
print("cases with my greedy clique < author's or author clique > leaves:", bad_cl)
