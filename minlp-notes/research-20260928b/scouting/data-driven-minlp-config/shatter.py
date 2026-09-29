# Greedy search for a set of clean-model instances (x*, rho=2, eps) shattered by the
# one-parameter class alpha -> tree size, restricted to alpha in [LO, HI] on a fine grid.
import numpy as np, subprocess, itertools, sys, os
LO, HI, N = 0.40, 0.60, 4_000_001
xs_pool = [0.3141592653589793, 0.2718281828459045, 0.4142135623730951, 0.6180339887498949, 0.5772156649015329, 0.7071067811865476]
eps_pool = [10**(-k/2) for k in range(3, 21)]   # 10^-1.5 ... 10^-10
cache = {}
def dual(xs, eps):
    key = (xs, eps)
    if key not in cache:
        out = subprocess.run(['./quadmodel_bin', repr(xs), '2.0', repr(eps), repr(LO), repr(HI), str(N)], capture_output=True).stdout
        cache[key] = np.frombuffer(out, dtype=np.int32)
    return cache[key]
codes = np.zeros(N, dtype=np.int64)
chosen = []
for eps in eps_pool:
    for xs in xs_pool:
        v = dual(xs, eps)
        k = len(chosen)
        found = False
        for r in np.unique(v)[1:]:
            b = (v >= r).astype(np.int64)
            new = codes | (b << k)
            if len(np.unique(new)) == 2**(k+1):
                codes, found = new, True
                chosen.append((xs, eps, int(r)))
                print('added', k+1, 'instances: x*=%.4f eps=%.1e threshold=%d; patterns realized %d' % (xs, eps, r, 2**(k+1)), flush=True)
                break
        if found: break
print('shattered set size (lower bound on pdim restricted to alpha in [%.2f,%.2f]):' % (LO, HI), len(chosen))
