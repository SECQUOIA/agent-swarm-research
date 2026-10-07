"""Hard-side experiment: B&B node counts and certified midpoint-conflict cliques.
usage: exp_hard.py OUT ks alphas bs seeds nproc cap [pratio]
p = pratio*k; lam = 0.75*sqrt(2 n log p) (same rule as tau0=1.5, sigma/b=0.5); sigma = 0.5.
Clique: pool = B&B candidate supports + all one-swap neighbours of the 20 best; conflicts checked
exactly (g(mid) < OPT(1-1e-7)) on the 300 best pool supports; greedy clique (60 starts)."""
import os, sys, json, time
os.environ["OMP_NUM_THREADS"] = "1"; os.environ["OPENBLAS_NUM_THREADS"] = "1"; os.environ["RAYON_NUM_THREADS"] = "1"; os.environ["MKL_NUM_THREADS"] = "1"
import numpy as np
from multiprocessing import Pool
from core import instance, ridge
from bnb import bnb, forward_greedy
from hard import g_mid

def clique(X, y, lam, k, pool, OPT, ncand=300):
    items = sorted(pool.items(), key=lambda t: t[1])[:ncand]
    C = [t[0] for t in items]; m = len(C)
    adj = np.zeros((m, m), bool)
    for i in range(m):
        for j in range(i + 1, m):
            if g_mid(X, y, lam, C[i], C[j]) < OPT * (1 - 1e-7):
                adj[i, j] = adj[j, i] = True
    best = []
    order = np.argsort(-adj.sum(1))
    for start in list(range(min(30, m))) + list(order[:30]):
        cl = [start]; cand = adj[start].copy()
        for j in np.argsort(-adj.sum(1)):
            if cand[j]:
                cl.append(j); cand &= adj[j]
        if len(cl) > len(best): best = cl
    return len(best), int(adj.sum() // 2), m

def job(args):
    p, k, alpha, b, seed, cap = args
    n = max(k + 2, int(round(alpha * k * np.log(p))))
    lam = 0.75 * np.sqrt(2 * n * np.log(p))
    X, y, _, S = instance(n, p, k, b=b, sigma=0.5, seed=seed, lam=lam)
    init = [forward_greedy(X, y, lam, k)] + ([S] if b > 0 else [])
    pool = {}
    t = time.time()
    r = bnb(X, y, lam, k, S_init=init, rule='maxfrac', max_nodes=cap, pool=pool)
    out = dict(p=p, k=k, n=n, alpha=alpha, b=b, seed=seed, lam=lam, nodes=r['nodes'], done=r['done'],
               opt=r['opt'], root=r['root'], rec=(b > 0 and r['support'] == tuple(S)), t_bnb=time.time() - t)
    if r['done']:
        OPT = r['opt']
        best = sorted(pool.items(), key=lambda t: t[1])[:20]
        for Sx, _ in best:
            for i in Sx:
                for j in range(p):
                    if j in Sx: continue
                    T = tuple(sorted((set(Sx) - {i}) | {j}))
                    if T not in pool: pool[T] = ridge(X, y, lam, T)[0]
        cl, ne, m = clique(X, y, lam, k, pool, OPT)
        out.update(clique=cl, edges=ne, ncand=m)
    out['time'] = time.time() - t
    return out

if __name__ == '__main__':
    OUT = sys.argv[1]; ks = [int(v) for v in sys.argv[2].split(',')]; alphas = [float(v) for v in sys.argv[3].split(',')]
    bs = [float(v) for v in sys.argv[4].split(',')]; seeds = int(sys.argv[5]); nproc = int(sys.argv[6]); cap = int(sys.argv[7])
    pr = int(sys.argv[8]) if len(sys.argv) > 8 else 10
    jobs = [(pr * k, k, a, b, 3000 + s, cap) for k in ks for a in alphas for b in bs for s in range(seeds)]
    jobs.sort(key=lambda j: (j[1], j[2]))
    with Pool(nproc) as pool, open(OUT, 'a') as f:
        for res in pool.imap_unordered(job, jobs):
            f.write(json.dumps(res) + '\n'); f.flush()
