"""E5: search for instances where SCIP's constant-Gamma cut is much weaker than the best cut."""
import numpy as np
from sfree import *
rng = np.random.default_rng(7)
worst = []
for t in range(4000):
    k = 2; n = 2
    A = rng.normal(size=(k, k)); Q = (A + A.T) / 2
    th = np.linalg.eigvalsh(Q)
    if not (th.min() < -1e-3 and th.max() > 1e-3):
        continue
    b = rng.normal(size=k); c = rng.normal()
    sbar = rng.normal(size=k)
    if qval(Q, b, c, sbar) <= 0.01:
        continue
    P = rng.normal(size=(k, n)); w = rng.uniform(0.1, 1, n)
    zk = corner_bound(Q, b, c, sbar, P, w)
    if not np.isfinite(zk) or zk <= 0:
        continue
    G, cs = ms_set(Q, b, c, sbar)
    zms = ic_bound(G, sbar, P, w)[0]
    worst.append((min(zms, zk) / zk, cs, t))
worst.sort()
print(worst[:10])
import collections
print(collections.Counter(c for r, c, t in worst if r < 0.2), collections.Counter(c for r, c, t in worst))
