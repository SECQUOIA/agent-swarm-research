"""Sanity checks of relax.py on tiny instances: validity (<= OPT by enumeration),
monotone ordering persp <= sdp1 <= sdp2 <= L2, sdp1 <= spart, sdp1 <= zb, and exactness at full fixings."""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import itertools, time
import numpy as np
from relax import instance, ridge, persp, sdp1, sdp2, L2, zb
tol = 1e-6
for seed in range(6):
    n, p, k = 6, 8, 2
    X, y, lam, S = instance(n, p, k, seed=100 + seed, tau0=1.0)
    OPT = min(ridge(X, y, lam, T)[0] for T in itertools.combinations(range(p), k))
    t = time.time()
    P = persp(X, y, lam, k)[0]; s1 = sdp1(X, y, lam, k); s2 = sdp2(X, y, lam, k); l2 = L2(X, y, lam, k)
    sp = sdp1(X, y, lam, k, spart=True); m2 = zb(X, y, lam, k)
    vals = dict(persp=P, sdp1=s1, sdp2=s2, L2=l2, spart=sp, zb=m2)
    ok = all(v <= OPT * (1 + tol) for v in vals.values())
    order = P <= s1 * (1 + tol) and s1 <= s2 * (1 + tol) and s2 <= l2 * (1 + tol) and s1 <= sp * (1 + tol) and s1 <= m2 * (1 + tol)
    # full fixing: every relaxation equals f(S) at S1 = S
    fS = ridge(X, y, lam, S)[0]
    full = [abs(f(X, y, lam, k, (), S) - fS) / fS for f in (sdp1, sdp2, L2, zb)]
    print(seed, 'OPT=%.5f' % OPT, ' '.join('%s=%.5f' % kv for kv in vals.items()),
          'valid' if ok else 'INVALID', 'ordered' if order else 'ORDER-VIOLATION',
          'fullfix_relerr=%.1e' % max(full), '%.1fs' % (time.time() - t), flush=True)
