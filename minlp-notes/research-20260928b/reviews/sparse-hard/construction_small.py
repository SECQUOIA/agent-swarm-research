"""The Theorem 4.3 construction at small sizes, with the EXACT OPT (full enumeration).

Pure noise (y independent of X), lam = sqrt(n). For each instance:
  - exact OPT/||y||^2, the rigorous Lemma 4.1(a) bound (1-rho*) with delta = 0.05,
    and the asymptotic value e^{-x}, x = 2 log C(p,k)/n;
  - W = top M = R k features by |x_j'y|; all k-subsets of W; exact midpoint values
    for all pairs; exact max clique of the conflict graph restricted to subsets of W
    (a valid lower bound on the full clique number);
  - the fraction of pairs with |S \\ T| >= m that conflict, and the Lemma 4.2 bound.
usage: construction_small.py OUT [nproc]
"""
import os, sys, json, itertools
os.environ["OMP_NUM_THREADS"] = "1"; os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np
from multiprocessing import Pool
from scipy.optimize import brentq
from scipy.special import gammaln
from cliquelib import midpoints_for_pairs, max_clique


def logbinom(a, b):
    return float(gammaln(a + 1) - gammaln(b + 1) - gammaln(a - b + 1))


def opt_enum(X, y, lam, k, chunk=400000):
    p = X.shape[1]; G = X.T @ X; bv = X.T @ y; yy = float(y @ y)
    best = np.inf
    it = itertools.combinations(range(p), k)
    while True:
        blk = np.array(list(itertools.islice(it, chunk)), dtype=np.int64)
        if len(blk) == 0:
            break
        A = G[blk[:, :, None], blk[:, None, :]] + lam * np.eye(k)
        v = bv[blk]
        f = yy - np.einsum('ij,ij->i', v, np.linalg.solve(A, v[:, :, None])[:, :, 0])
        best = min(best, float(f.min()))
    return best


def rho_star(n, p, k, delta=0.05):
    q = k / n
    d = lambda r: q * np.log(q / r) + (1 - q) * np.log((1 - q) / (1 - r))
    target = 2 * (logbinom(p, k) + np.log(1 / delta)) / n
    return brentq(lambda r: d(r) - target, q * (1 + 1e-12), 1 - 1e-15)


def job(args):
    p, k, alpha, R, seed = args
    rng = np.random.default_rng(777 + seed)
    n = int(round(alpha * k * np.log(p)))
    X = rng.standard_normal((n, p)); y = rng.standard_normal(n)
    lam = np.sqrt(n); yy = float(y @ y)
    OPT = opt_enum(X, y, lam, k)
    x = 2 * logbinom(p, k) / n
    c = X.T @ (y / np.sqrt(yy))
    W = np.argsort(-np.abs(c))[:R * k]
    subs = np.array(list(itertools.combinations(sorted(W.tolist()), k)), dtype=np.int64)
    N = len(subs); iu = np.triu_indices(N, 1)
    G = X.T @ X; bv = X.T @ y
    gm = midpoints_for_pairs(G, bv, yy, lam, subs, iu[0], iu[1])
    inter = np.array([len(set(subs[i]) & set(subs[j])) for i, j in zip(*iu)])
    E = [(int(i), int(j)) for i, j, g in zip(iu[0], iu[1], gm) if g < OPT * (1 - 1e-10)]
    omegaW = len(max_clique(N, E))
    out = dict(p=p, k=k, n=n, alpha=alpha, R=R, seed=seed, x=x, lam=lam,
               opt_frac=OPT / yy, rigorous_lb_frac=1 - rho_star(n, p, k), asym_lb_frac=float(np.exp(-x)),
               min_mid_frac=float(gm.min() / yy), omegaW=omegaW, nsubW=N, edgesW=len(E))
    for dmin in range(1, k + 1):
        sel = (k - inter) >= dmin
        out['conflict_frac_d%d' % dmin] = float(np.mean(gm[sel] < OPT * (1 - 1e-10))) if sel.any() else None
    return out


if __name__ == '__main__':
    OUT = sys.argv[1]; nproc = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    jobs = [(p, k, a, R, s) for (p, k) in ((60, 3), (200, 3), (60, 4)) for a in (2, 4, 8)
            for R in (3,) for s in range(6)]
    with Pool(nproc) as pool, open(OUT, 'w') as fh:
        for r in pool.imap_unordered(job, jobs):
            fh.write(json.dumps(r) + '\n'); fh.flush()
