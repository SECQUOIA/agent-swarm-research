"""How much does restricting the clique search to the 300 best supports (as in the note's
Section 6 method) lose, relative to the exact clique number over all supports? Pure-noise E2 cells."""
import os; os.environ["OMP_NUM_THREADS"] = "1"
import json, numpy as np
from multiprocessing import Pool
from cliquelib import instance_author, all_f, conflict_edges, max_clique

def job(r):
    X, y, S = instance_author(r['n'], r['p'], r['k'], b=r['b'], sigma=0.5, seed=r['seed'])
    sups, f = all_f(X, y, r['lam'], r['k']); OPT = f.min()
    top = np.argsort(f)[:300]
    E, _ = conflict_edges(X, y, r['lam'], sups, OPT * (1 - 1e-10), cand=top)
    remap = {v: i for i, v in enumerate(top.tolist())}
    return (r['p'], r['k'], r['alpha'], r['seed'], r['omega'], len(max_clique(300, [(remap[a], remap[b]) for a, b in E])))

rows = [json.loads(l) for l in open('e2.jsonl') if json.loads(l)['b'] == 0.0]
with Pool(5) as P:
    res = sorted(P.map(job, rows))
lost = [(a, b) for (_, _, _, _, a, b) in res if b < a]
print("pure-noise E2 instances: %d; omega_top300 < omega_all in %d" % (len(res), len(lost)))
for t in res:
    if t[5] < t[4]: print("  p=%d k=%d alpha=%s seed=%d omega_all=%d omega_top300=%d" % t)
