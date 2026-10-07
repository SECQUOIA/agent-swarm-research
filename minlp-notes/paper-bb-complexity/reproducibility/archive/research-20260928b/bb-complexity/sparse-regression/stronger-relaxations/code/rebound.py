"""Recompute the certified L_1/L_2 root bounds of stored exp_mech rows with the current cbound.py
(the SDP values are kept).  usage: rebound.py FILE [PMAX]   (rows with p > PMAX are left unchanged)"""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import sys, json
import numpy as np
from relax import ridge
from cbound import best_small_F_bound, delta_opt_persp
from exp_mech import make
rows = [json.loads(l) for l in open(sys.argv[1])]
pmax = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
for r in rows:
    if r['p'] > pmax:
        continue
    X, y, lam, S = make(r['n'], r['k'], 2560 if r['n'] == 20 else 3200, r['p'], r['seed'])
    fS, bS, res = ridge(X, y, lam, S)
    a = np.abs(X.T @ res); a[list(S)] = -1.0
    cand = [int(j) for j in np.argsort(-a)[:20]]
    L1, L2, info = best_small_F_bound(X, y, lam, r['k'], S, cand, hs=(1, 2, 3, 5, 8, 12, 20), delta=delta_opt_persp(X, lam))
    r.update(L1_ub=L1, L2_ub=L2, ub_info=info)
    for m, ub in (('sdp1', 'L1_ub'), ('sdp2', 'L2_ub'), ('zb', None)):
        if ub and r.get(m) is not None and r[m] > r[ub] * (1 + 1e-6):
            print('INCONSISTENT', r['p'], r['seed'], m, r[m], ub, r[ub])
with open(sys.argv[1], 'w') as f:
    for r in rows:
        f.write(json.dumps(r, default=float) + '\n')
print('rebounded', len(rows))
