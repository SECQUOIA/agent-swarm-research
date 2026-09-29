"""Check 5: zb on pure-noise instances of PT Table 6.4 (note Table 7.3), reviewer code only.
Instances regenerated with the documented generator (b = 0, sigma = 0.5) from the stored (n, p, k, seed, lam);
OPT recomputed by enumeration; zb solved with Clarabel (tolerance 1e-10) using my own formulation.
usage: rv_noise.py k alpha seed"""
import os as _os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"]:
    _os.environ[_v] = "1"
import os, sys, json, time
import numpy as np
from rv_common import gen_core, zb, sdp1
from rv_enum import optk

HERE = os.path.dirname(os.path.abspath(__file__))
k, alpha, seed = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
row = None
for l in open(os.path.join(HERE, '..', '..', 'bb-complexity', 'sparse-regression', 'data', 'hard_k3-8.jsonl')):
    r = json.loads(l)
    if r['b'] == 0.0 and r['k'] == k and float(r['alpha']) == alpha and r['seed'] == seed:
        row = r
X, y, _, _ = gen_core(row['n'], row['p'], k, b=0.0, sigma=0.5, seed=seed, lam=row['lam'])
lam = row['lam']
t0 = time.time()
OPT, arg = optk(X, y, lam, k)
v = zb(X, y, lam, k)
s1 = sdp1(X, y, lam, k)
print(json.dumps(dict(k=k, alpha=alpha, seed=seed, n=row['n'], p=row['p'], OPT_mine=OPT, OPT_stored=row['opt'],
                      zb=v, zb_relgap=(OPT - v) / OPT if v is not None else None, sdp1=s1,
                      sdp1_relgap=(OPT - s1) / OPT if s1 is not None else None,
                      persp_relgap_stored=(row['opt'] - row['root']) / row['opt'], time=round(time.time() - t0, 1))), flush=True)
