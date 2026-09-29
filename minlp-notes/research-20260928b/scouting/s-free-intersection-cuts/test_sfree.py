import numpy as np
from sfree import *
rng = np.random.default_rng(0)

def rand_inst(k, n, case=None):
    while True:
        A = rng.normal(size=(k, k)); Q = (A + A.T) / 2
        if case == 'bilinear':  # q = s0*s1 - s2  (w >= xy side) or reversed
            Q = np.zeros((k, k)); Q[0, 1] = Q[1, 0] = 0.5
            b = np.zeros(k); b[2] = -1.0; c = 0.0
            if rng.random() < 0.5:
                Q, b = -Q, -b
        else:
            b = rng.normal(size=k); c = rng.normal()
        th = np.linalg.eigvalsh(Q)
        if not (th.min() < -1e-6 and (th.max() > 1e-6 or case == 'bilinear')):
            continue
        sbar = rng.normal(size=k)
        if qval(Q, b, c, sbar) <= 0.05:
            continue
        P = rng.normal(size=(k, n))
        w = rng.uniform(0.1, 1.0, size=n)
        return Q, b, c, sbar, P, w

# check S-freeness of ms_set by sampling
bad = 0
for trial in range(300):
    k = rng.integers(2, 5)
    Q, b, c, sbar, P, w = rand_inst(k, k + 2, case='bilinear' if (trial % 3 == 0 and k >= 3) else None)
    G, case = ms_set(Q, b, c, sbar)
    assert G(sbar) < 0, (case, G(sbar))
    # sample points in C near boundary and deep
    for _ in range(400):
        d = rng.normal(size=k); d /= np.linalg.norm(d)
        a = step_length(G, sbar, d)
        if not np.isfinite(a):
            a = 50.0
        for t in rng.uniform(0, 1, 5) * a * 0.999:
            s = sbar + t * d
            if qval(Q, b, c, s) < -1e-7 * (1 + np.abs(s).max() ** 2):
                bad += 1
print('S-free violations:', bad)

# compare corner_bound to SCIP
mx = 0
for trial in range(40):
    k = rng.integers(2, 4)
    Q, b, c, sbar, P, w = rand_inst(k, k + 3, case='bilinear' if (trial % 2 == 0 and k >= 3) else None)
    z1 = corner_bound(Q, b, c, sbar, P, w)
    z2 = corner_bound_scip(Q, b, c, sbar, P, w)
    mx = max(mx, abs(z1 - z2) / (1 + abs(z2)) if np.isfinite(z1) and np.isfinite(z2) else (0 if z1 == z2 else 1))
    if abs(z1 - z2) > 1e-4 * (1 + abs(z2)):
        print('mismatch', k, z1, z2)
print('max rel diff exact vs SCIP', mx)
