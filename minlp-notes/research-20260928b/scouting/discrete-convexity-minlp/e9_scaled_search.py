"""E9: random search for M-natural sets whose alpha-scaling is not IC,
by dimension n and scale alpha (sets only; generators e_i, -e_i, e_i - e_j
with multiplicities 1..U).  Reports the smallest (n, alpha) with a violation."""
import itertools
import sys
import numpy as np
from dcheck import ic_violations, INF

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 9)


def gens_rand(n, m):
    out = []
    for _ in range(m):
        t = rng.integers(3)
        i, j = rng.choice(n, size=2, replace=False)
        g = [0] * n
        if t == 0:
            g[i] = 1
        elif t == 1:
            g[i] = -1
        else:
            g[i], g[j] = 1, -1
        out.append((tuple(g), int(rng.integers(1, 4))))
    return out


def mset(n, gens):
    S = {tuple([0] * n)}
    for g, u in gens:
        S = {tuple(x + k * gi for x, gi in zip(s, g)) for s in S for k in range(u + 1)}
    return S


def ic_set(T, n):
    lo = [min(p[i] for p in T) for i in range(n)]
    hi = [max(p[i] for p in T) for i in range(n)]
    f = {p: (0.0 if p in T else INF) for p in itertools.product(*[range(lo[i], hi[i] + 1) for i in range(n)])}
    return ic_violations(f)


for n, m, trials in ((3, 7, 3000), (4, 7, 1500)):
    for alpha in (2, 3):
        found = 0
        ex = None
        for _ in range(trials):
            G = gens_rand(n, m)
            S = mset(n, G)
            T = {tuple(x // alpha for x in s) for s in S if all(x % alpha == 0 for x in s)}
            if len(T) < 2:
                continue
            v = ic_set(T, n)
            if v:
                found += 1
                if ex is None:
                    ex = (G, sorted(T)[:6], v[0])
        print(f"n={n} alpha={alpha}: trials={trials} non-IC scaled sets={found} example={ex}", flush=True)
