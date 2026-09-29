"""Validity of the zb relaxation (and of sdp2) against exact OPT on random small instances:
zb <= OPT must hold (a violation would indicate an invalid constraint).  Also records how often
zb, sdp2 and SDP1 are exact.  Includes pure-noise instances (b = 0), where relaxations are weakest."""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import itertools
import numpy as np
from relax import instance, ridge, sdp1, sdp2, zb, persp
viol = 0; ex = dict(persp=0, sdp1=0, sdp2=0, zb=0); tot = 0
for seed in range(40):
    rng = np.random.default_rng(seed)
    n = int(rng.integers(5, 13)); p = int(rng.integers(12, 22)); k = int(rng.integers(2, 4)); b = [0.0, 0.5, 1.0][seed % 3]
    X, y, lam, S = instance(n, p, k, b=b if b > 0 else 1.0, seed=900 + seed, tau0=1.0)
    if b == 0:
        y = np.random.default_rng(5000 + seed).standard_normal(n)
    elif b == 0.5:
        y = y * 0 + X[:, list(S)] @ (0.5 * np.ones(k)) + 0.5 * np.random.default_rng(6000 + seed).standard_normal(n)
    OPT = min(ridge(X, y, lam, T)[0] for T in itertools.combinations(range(p), k))
    vals = dict(persp=persp(X, y, lam, k)[0], sdp1=sdp1(X, y, lam, k), sdp2=sdp2(X, y, lam, k), zb=zb(X, y, lam, k))
    tot += 1
    for m, v in vals.items():
        if v is None:
            continue
        if v > OPT * (1 + 1e-6) + 1e-8:
            viol += 1; print('VIOLATION', seed, m, v, OPT)
        if v >= OPT * (1 - 1e-6):
            ex[m] += 1
    print(seed, 'n=%d p=%d k=%d b=%.1f OPT=%.5f' % (n, p, k, b, OPT), ' '.join('%s=%.5f' % kv for kv in vals.items()), flush=True)
print('instances', tot, 'violations', viol, 'exact counts', ex)
