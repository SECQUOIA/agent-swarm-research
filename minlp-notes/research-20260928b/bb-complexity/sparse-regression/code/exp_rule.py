"""Rule dependence below the C1 threshold (scaled lam, tau0 = 1.5, b = 1, sigma = 0.5).
usage: exp_rule.py OUT p k alphas seeds nproc cap
For each instance: best-first B&B with 'maxfrac' and with 'maxz' (node cap), then at the optimum S°:
number of failing removal nodes (bad0, i in S°) and forced-in nodes (bad1, j notin S°), each decided
by an exact node solve (primal value < OPT(1-1e-7) => not prunable)."""
import os, sys, json, time
os.environ["OMP_NUM_THREADS"] = "1"; os.environ["OPENBLAS_NUM_THREADS"] = "1"; os.environ["RAYON_NUM_THREADS"] = "1"; os.environ["MKL_NUM_THREADS"] = "1"
import numpy as np
from multiprocessing import Pool
from core import instance, ridge, solve_node
from bnb import bnb, forward_greedy
def job(args):
    p, k, alpha, seed, cap = args
    n = max(k + 2, int(round(alpha * k * np.log(p))))
    X, y, lam, S = instance(n, p, k, b=1.0, sigma=0.5, seed=seed, tau0=1.5)
    init = [S, forward_greedy(X, y, lam, k)]
    out = dict(p=p, k=k, n=n, alpha=alpha, seed=seed, lam=lam)
    best = None
    for br in ['maxz', 'maxfrac']:
        t = time.time(); r = bnb(X, y, lam, k, S_init=init, rule=br, max_nodes=cap)
        out[br] = dict(nodes=r['nodes'], done=r['done'], time=time.time() - t)
        if r['done']: best = r
    if best is not None:
        OPT = best['opt']; So = best['support']
        out.update(opt=OPT, rec=(So == tuple(S)))
        bad0 = sum(solve_node(X, y, lam, k, (i,), ())[1] < OPT * (1 - 1e-7) for i in So)
        bad1 = sum(solve_node(X, y, lam, k, (), (j,))[1] < OPT * (1 - 1e-7) for j in range(p) if j not in So)
        out.update(bad0=int(bad0), bad1=int(bad1))
    return out
if __name__ == '__main__':
    OUT, p, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    alphas = [float(v) for v in sys.argv[4].split(',')]; seeds = int(sys.argv[5]); nproc = int(sys.argv[6]); cap = int(sys.argv[7])
    jobs = [(p, k, a, 4000 + s, cap) for a in alphas for s in range(seeds)]
    with Pool(nproc) as pool, open(OUT, 'a') as f:
        for res in pool.imap_unordered(job, jobs):
            f.write(json.dumps(res) + '\n'); f.flush()
