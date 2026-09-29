"""Like-for-like comparison on restricted instances: columns C = S* u (top-N nulls by |a_l|) of the nested
n = 40 design at p = 3200.  Solves the perspective relaxation, SDP1 and sdp2 (Clarabel) and zb (SCS) on the
restricted instance (each value is an upper bound on the value of the same relaxation for the full instance).
usage: exp_restr_cmp.py OUT N seeds_csv"""
import os, sys, json, time
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import numpy as np
from relax import ridge, persp, sdp1, sdp2, zb
from exp_mech import make

OUT, N = sys.argv[1], int(sys.argv[2]); seeds = [int(s) for s in sys.argv[3].split(',')]
with open(OUT, 'a') as f:
    for seed in seeds:
        X, y, lam, S = make(40, 3, 3200, 3200, seed)
        fS, bS, r = ridge(X, y, lam, S)
        a = np.abs(X.T @ r); a[list(S)] = -1.0
        C = list(S) + [int(j) for j in np.argsort(-a)[:N]]
        Xc = X[:, C]; t = time.time()
        out = dict(n=40, p=3200, N=N, seed=seed, fS=fS, persp=persp(Xc, y, lam, 3)[0], sdp1=sdp1(Xc, y, lam, 3),
                   sdp2=sdp2(Xc, y, lam, 3), zb=zb(Xc, y, lam, 3, solver='SCS'))
        out['time'] = time.time() - t
        f.write(json.dumps(out) + '\n'); f.flush()
        print({k: (round(v - fS, 6) if k in ('persp', 'sdp1', 'sdp2', 'zb') else v) for k, v in out.items()}, flush=True)
