"""Upper bounds on the zb root value at large p: zb of the instance restricted to the columns
C = S* u (top-N nulls by |a_l|).  Setting the other rows/columns of the moment matrix to zero is
feasible for the full zb, so zb(full) <= zb(restricted).  A restricted value below f(S*) certifies
(up to solver accuracy) that the full zb root is inexact.
usage: exp_zbr.py OUT n k pmax p Nlist seeds_csv nproc"""
import os, sys, json, time
for v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[v] = "1"
import numpy as np
from multiprocessing import Pool
from relax import ridge, zb
from exp_mech import make

def job(args):
    n, k, pmax, p, N, seed = args
    X, y, lam, S = make(n, k, pmax, p, seed)
    fS, bS, r = ridge(X, y, lam, S)
    a = np.abs(X.T @ r); a[list(S)] = -1.0
    m0 = lam * np.abs(bS).min()
    C = list(S) + [int(j) for j in np.argsort(-a)[:N]]
    t = time.time(); v = zb(X[:, C], y, lam, k, solver='SCS')
    return dict(n=n, k=k, p=p, N=N, seed=seed, fS=fS, zb_restr=v, nviol=int((a > m0).sum()),
                maxratio=float(a.max() / m0), time=time.time() - t)

if __name__ == '__main__':
    OUT, n, k, pmax, p = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    Ns = [int(v) for v in sys.argv[6].split(',')]; seeds = [int(s) for s in sys.argv[7].split(',')]; nproc = int(sys.argv[8])
    jobs = [(n, k, pmax, p, N, s) for N in Ns for s in seeds]
    with Pool(nproc) as pool, open(OUT, 'a') as f:
        for res in pool.imap_unordered(job, jobs):
            f.write(json.dumps(res) + '\n'); f.flush(); print(res, flush=True)
