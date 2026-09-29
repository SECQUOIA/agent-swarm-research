"""Independent evaluation of Heuristic 3.8 on the Table 6.1 runs (dedup by (p, n, seed) as in fill_note.py)."""
import json, glob
from common import ridge_on
from verify_cg import author_instance
import numpy as np
D = '../../bb-complexity/sparse-regression/data/'
rows, seen = [], set()
for fn in [D + 'c1_p200_k8_t1.5.jsonl'] + sorted(glob.glob(D + 'c1_scaleP_*.jsonl')):
    for l in open(fn):
        r = json.loads(l); key = (r['p'], r['n'], r['seed'])
        if key in seen: continue
        seen.add(key); rows.append(r)
agree = tot = 0; wrong = []
for r in rows:
    X, y, lam, S = author_instance(r['n'], r['p'], r['k'], r['rule'], r['seed'])
    f, b, res = ridge_on(X, y, lam, S)
    a = np.abs(X.T @ res); nul = np.setdiff1d(np.arange(r['p']), S); m0 = lam * np.min(np.abs(b))
    pred = m0 ** 2 / lam - np.sum(np.maximum(a[nul] - m0, 0) ** 2) / r['n'] - np.max(a[nul]) ** 2 / (r['n'] + lam) > 0
    obs = r['c1'] is True or r['c1'] == 'capped'
    tot += 1; agree += (pred == obs)
    if pred != obs: wrong.append((r['p'], r['n'], r['seed'], 'pred C1' if pred else 'pred fail', 'obs', r['c1']))
print(f"Heuristic 3.8 agrees with observed C1 (capped counted as C1) in {agree} of {tot} runs")
print("disagreements: pred C1 but failed:", sum(w[3] == 'pred C1' for w in wrong), "; pred fail but C1:", sum(w[3] == 'pred fail' for w in wrong))
