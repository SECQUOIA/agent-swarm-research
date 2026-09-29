"""Exact maximum midpoint-conflict cliques over ALL k-subsets, for small p.

usage: exact_clique.py EXPERIMENT OUT [nproc]
  E1: the note's Table 6.4 instances (p = 10k = 30, k = 3, seeds 3000-3003, same
      instance generator and ridge rule lam = 0.75 sqrt(2 n log p)) -> compare
      the exact clique number with the author's greedy clique and node count.
  E2: own seeds 0-9; (p,k) in {(30,3), (20,4)}; alpha in {1,2,4}; pure noise
      (b=0) vs planted (b=1, sigma=0.5); lam = 0.75 sqrt(2 n log p). Also the
      removal half and the forced-in half of C1 at the optimal support S°,
      and the consistency check "removal half holds => omega <= k+1" (Lemma 1.3).
  E3: total-SNR scan (Theorem 4.4): p=30, k=3, alpha=4, sigma=1,
      beta*_i = +-sqrt(kappa_s/k), same X and w for every kappa_s, lam = sqrt(n),
      seeds 0-9.
Conflict: g(mid) < OPT (1 - 1e-10), OPT by full enumeration.
"""
import os, sys, json, time
os.environ["OMP_NUM_THREADS"] = "1"; os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np
from multiprocessing import Pool
from cliquelib import (instance_author, all_f, conflict_edges, max_clique, greedy_clique,
                       node_bound)

REL = 1e-10


def c1_halves(X, y, lam, k, Sopt, OPT):
    """Certified status of the removal half and the forced-in half at Sopt."""
    p = X.shape[1]
    status = {}
    for name, nodes in [('removal', [((i,), ()) for i in Sopt]),
                        ('forced', [((), (j,)) for j in range(p) if j not in Sopt])]:
        holds = True; undet = 0; nfail = 0
        for S0, S1 in nodes:
            LB, pv = node_bound(X, y, lam, k, S0, S1)
            if LB >= OPT * (1 - REL):
                continue
            if pv < OPT * (1 - REL):
                nfail += 1; holds = False
            else:
                undet += 1; holds = False
        status[name] = 'holds' if holds else ('fails' if nfail else 'undetermined')
        status[name + '_nfail'] = nfail
    return status


def run(X, y, lam, k, want_c1=False, author_greedy=False):
    sups, f = all_f(X, y, lam, k)
    OPT = float(f.min()); iopt = int(np.argmin(f))
    E, gmin = conflict_edges(X, y, lam, sups, OPT * (1 - REL))
    mc = max_clique(len(sups), E)
    out = dict(OPT=OPT, nsup=len(sups), edges=len(E), omega=len(mc),
               gmin_over_opt=float(gmin / OPT), Sopt=sups[iopt].tolist(),
               clique=[sups[v].tolist() for v in mc][:50])
    # members: how near-optimal are clique members? (rank of f among all supports)
    order = np.argsort(f); rank = np.empty(len(f), int); rank[order] = np.arange(len(f))
    out['clique_max_rank'] = int(max(rank[v] for v in mc)) if mc else None
    out['clique_max_rel_excess'] = float(max((f[v] - OPT) / OPT for v in mc)) if mc else None
    if author_greedy:
        # author-style: greedy clique on the 300 best supports only
        top = np.argsort(f)[:300]; tops = set(top.tolist())
        E300 = [(a, b) for a, b in E if a in tops and b in tops]
        remap = {v: i for i, v in enumerate(top.tolist())}
        out['greedy300'] = len(greedy_clique(300, [(remap[a], remap[b]) for a, b in E300]))
        out['omega300'] = len(max_clique(300, [(remap[a], remap[b]) for a, b in E300]))
    if want_c1:
        out.update(c1_halves(X, y, lam, k, tuple(sups[iopt].tolist()), OPT))
    return out


def job(args):
    exp, p, k, alpha, b, seed = args
    t = time.time()
    if exp in ('E1', 'E2'):
        n = max(k + 2, int(round(alpha * k * np.log(p))))
        lam = 0.75 * np.sqrt(2 * n * np.log(p))
        X, y, S = instance_author(n, p, k, b=b, sigma=0.5, seed=seed)
        out = run(X, y, lam, k, want_c1=(exp == 'E2'), author_greedy=(exp == 'E1'))
        out.update(exp=exp, p=p, k=k, n=n, alpha=alpha, b=b, seed=seed, lam=lam,
                   Sstar=list(S), rec=(out['Sopt'] == list(S)))
    else:  # E3
        kappa = b
        n = int(round(alpha * k * np.log(p)))
        rng = np.random.default_rng(10_000 + seed)
        X = rng.standard_normal((n, p)); w = rng.standard_normal(n)
        S = np.sort(rng.choice(p, k, replace=False)); signs = rng.choice([-1.0, 1.0], k)
        beta = np.zeros(p); beta[S] = signs * np.sqrt(kappa / k)
        y = X @ beta + w
        lam = np.sqrt(n)
        out = run(X, y, lam, k)
        x = 2 * float(np.sum(np.log(np.arange(p - k + 1, p + 1)) - np.log(np.arange(1, k + 1)))) / n
        out.update(exp=exp, p=p, k=k, n=n, alpha=alpha, kappa_s=kappa, seed=seed, lam=lam,
                   x=x, Sstar=S.tolist(), rec=(out['Sopt'] == S.tolist()),
                   disjoint_from_Sstar=all(not (set(c) & set(S.tolist())) for c in out['clique']))
    out['time'] = time.time() - t
    return out


if __name__ == '__main__':
    exp, OUT = sys.argv[1], sys.argv[2]
    nproc = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    if exp == 'E1':
        jobs = [('E1', 30, 3, a, b, 3000 + s) for a in (1, 2, 4) for b in (0.0, 1.0) for s in range(4)]
    elif exp == 'E2':
        jobs = [('E2', p, k, a, b, s) for (p, k) in ((30, 3), (20, 4)) for a in (1, 2, 4)
                for b in (0.0, 1.0) for s in range(10)]
    else:
        jobs = [('E3', 30, 3, 4, kap, s) for kap in (0.0, 0.05, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4)
                for s in range(10)]
    with Pool(nproc) as pool, open(OUT, 'w') as fh:
        for res in pool.imap_unordered(job, jobs):
            fh.write(json.dumps(res) + '\n'); fh.flush()
