"""E6: are scaled M-natural-convex functions integrally convex?

f = infimal convolution of univariate convex functions along generators
g in {e_i, -e_i, e_i - e_j}; f is M-natural-convex (M-natural convexity is
closed under convolution).  The scaled function f_2(y) = f(2y) is in general
not M-natural (Murota-Shioura scaling example).  E4 suggested that
restrictions of continuous M-natural functions to Z^n are integrally convex;
this is the discrete special case.  We test IC of f_2 and f_3 on their whole
(finite) effective domains, n = 3, 4.
"""
import itertools
import sys
import numpy as np
from dcheck import ic_violations, mnat_violations, ddm_violations, INF

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 3)


def rand_gens(n, m):
    gens = []
    for _ in range(m):
        t = rng.integers(3)
        i, j = rng.choice(n, size=2, replace=False)
        g = [0] * n
        if t == 0:
            g[i] = 1
        elif t == 1:
            g[i] = -1
        else:
            g[i] = 1; g[j] = -1
        gens.append(tuple(g))
    return gens


def mnat_function(n, gens, U, sets_only):
    f = {tuple([0] * n): 0.0}
    for g in gens:
        u = int(rng.integers(1, U + 1))
        if sets_only:
            phi = [0.0] * (u + 1)
        else:
            a, c = rng.uniform(0.1, 2), rng.uniform(-2, 2)
            phi = [a * k * k + c * k for k in range(u + 1)]
        new = {}
        for x, v in f.items():
            for k in range(u + 1):
                y = tuple(xi + k * gi for xi, gi in zip(x, g))
                w = v + phi[k]
                if w < new.get(y, INF):
                    new[y] = w
        f = new
    return f


def scaled(f, alpha, n):
    g = {}
    for x, v in f.items():
        if all(xi % alpha == 0 for xi in x):
            g[tuple(xi // alpha for xi in x)] = v
    return g


def complete(g, n):
    """Tabulate g on its bounding box with +inf outside the domain."""
    lo = [min(p[i] for p in g) for i in range(n)]
    hi = [max(p[i] for p in g) for i in range(n)]
    return {p: g.get(p, INF) for p in itertools.product(*[range(lo[i], hi[i] + 1) for i in range(n)])}


for n, m, U, trials in ((3, 6, 2, 150), (4, 7, 2, 80)):
    for sets_only in (True, False):
        st = dict(inst=0, base_mnat_viol=0, scaled_mnat_viol=0, scaled_ddm_viol=0, scaled_ic_viol=0)
        example = None
        for _ in range(trials):
            gens = rand_gens(n, m)
            f = mnat_function(n, gens, U, sets_only)
            st["inst"] += 1
            if n == 3 and st["inst"] <= 20:
                st["base_mnat_viol"] += bool(mnat_violations(complete(f, n)))
            for alpha in (2, 3):
                g = scaled(f, alpha, n)
                if len(g) < 2:
                    continue
                G = complete(g, n)
                iv = ic_violations(G)
                st["scaled_ic_viol"] += bool(iv)
                st["scaled_mnat_viol"] += bool(mnat_violations(G))
                st["scaled_ddm_viol"] += bool(ddm_violations(G))
                if iv and example is None:
                    example = (gens, alpha, iv[0])
        print(f"n={n} sets_only={sets_only}: {st} example={example}", flush=True)
