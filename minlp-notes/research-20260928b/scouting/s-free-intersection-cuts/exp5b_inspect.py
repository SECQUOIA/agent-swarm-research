import numpy as np
from sfree import *
rng = np.random.default_rng(7)
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
    if t in (940, 933):
        zk, lam = corner_bound(Q, b, c, sbar, P, w, return_point=True)
        G, cs = ms_set(Q, b, c, sbar)
        zms, al = ic_bound(G, sbar, P, w)
        tau = []
        for j in range(n):
            ts = [s for s in np.linspace(1e-4, 1e3, 2000001) if False]
        print('t', t, 'Q', Q.round(3).tolist(), 'b', b.round(3).tolist(), 'c', round(c, 3), 'sbar', sbar.round(3).tolist())
        print('  P', P.round(3).tolist(), 'w', w.round(3).tolist())
        print('  zK', zk, 'argmin lam', lam, ' zMS', zms, 'alphas MS', al)
        # first hits of S along rays
        for j in range(n):
            M = P[:, j] @ Q @ P[:, j]; m = P[:, j] @ (Q @ sbar + b / 2); mu0 = qval(Q, b, c, sbar)
            disc = m * m - M * mu0
            roots = [] if disc < 0 else sorted([r for r in ((-m - np.sqrt(disc)) / M, (-m + np.sqrt(disc)) / M) if r > 0])
            print('  ray', j, 'S-hits t =', roots)
