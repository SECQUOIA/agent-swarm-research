"""Closed-form ratio for the complete k-uniform hypergraph K_n^(k) (all coefficients 1) and its n -> oo limit.

For phi(x) = sum_{|t|=k} prod_{j in t} x_j, phi(v) = C(|v|, k) depends only on |v|, C(s,k) is convex in s,
and {x in [0,1]^n : m <= sum x <= m+1} is an integral polytope, hence

    vex_H[phi](x) = Clin(sum_j x_j),   Clin = piecewise-linear interpolation of s -> C(s,k) at integers.

So no LP is needed and n can be large.  The n -> oo limit with coordinate profile mu (a probability
distribution on [0,1]) is

    ratio(mu) = [E min(X_1..X_k) - E max(0, X_1+..+X_k-k+1)] / [E min(X_1..X_k) - (E X)^k],  X_i iid ~ mu.

Usage: python complete_hypergraph.py
"""
from __future__ import annotations

import itertools
import math

import numpy as np
from scipy.optimize import minimize


def clin(s, k):
    m = math.floor(s)
    f = s - m
    return (1 - f) * math.comb(m, k) + f * math.comb(m + 1, k)


def ratio_complete(x, k):
    x = np.asarray(x, float)
    xs = np.sort(x)
    n = len(x)
    cav = 0.0
    tbt = 0.0
    for t in itertools.combinations(range(n), k):
        v = xs[list(t)]
        cav += v.min()
        tbt += max(0.0, v.sum() - k + 1)
    vex = clin(xs.sum(), k)
    return (cav - tbt) / (cav - vex) if cav - vex > 1e-12 else 1.0


def ratio_two_valued(n, k, p, u, w):
    """x has n1 = round(p n) coordinates equal to u and the rest equal to w; exact combinatorial sums."""
    n1 = int(round(p * n));  n2 = n - n1
    cav = tbt = 0.0
    for i in range(0, k + 1):  # i coordinates from the u-block
        cnt = math.comb(n1, i) * math.comb(n2, k - i)
        if cnt == 0:
            continue
        mn = min(u, w) if 0 < i < k else (u if i == k else w)
        cav += cnt * mn
        tbt += cnt * max(0.0, i * u + (k - i) * w - k + 1)
    vex = clin(n1 * u + n2 * w, k)
    return (cav - tbt) / (cav - vex) if cav - vex > 1e-12 else 1.0


def limit_ratio(weights, values, k, samples=None):
    """n -> oo ratio for discrete profile mu = sum w_i delta_{v_i}, computed exactly by enumeration."""
    w = np.asarray(weights, float);  w = w / w.sum()
    v = np.asarray(values, float)
    emin = emax = 0.0
    for idx in itertools.product(range(len(v)), repeat=k):
        pr = np.prod(w[list(idx)])
        vals = v[list(idx)]
        emin += pr * vals.min()
        emax += pr * max(0.0, vals.sum() - k + 1)
    ex = float(w @ v)
    return (emin - emax) / (emin - ex ** k)


def main():
    from envelopes import Multilinear
    from families import complete

    rng = np.random.default_rng(1)
    # check closed form against the LP
    for n, k in [(5, 3), (6, 3), (6, 4), (7, 2)]:
        f = complete(n, k)
        for _ in range(5):
            x = rng.random(n)
            assert abs(f.vex(x) - clin(x.sum(), k)) < 1e-9, (n, k)
            assert abs(f.ratio(x) - ratio_complete(x, k)) < 1e-9
    print("closed form agrees with LP on random points (K_5^3, K_6^3, K_6^4, K_7)")

    print("\nuniform x = c*1, best c, as n grows (k=3):")
    for n in [6, 8, 10, 12, 16, 24, 32, 48, 64]:
        best = max(((ratio_two_valued(n, 3, 1.0, c, c), c) for c in np.linspace(0.05, 0.95, 901)))
        print(f"  n={n:3d}: max_c ratio = {best[0]:.6f} at c = {best[1]:.4f}")

    print("\ntwo-valued x (p, u, w), multistart Nelder-Mead, k=3:")
    for n in [8, 12, 16, 24, 32]:
        best = (0, None)
        for _ in range(30):
            z0 = rng.random(3)

            def obj(z):
                p, u, w = np.clip(z, 0, 1)
                return -ratio_two_valued(n, 3, p, u, w)

            res = minimize(obj, z0, method="Nelder-Mead", options={"xatol": 1e-8, "fatol": 1e-12})
            if -res.fun > best[0]:
                best = (-res.fun, np.clip(res.x, 0, 1))
        p, u, w = best[1]
        print(f"  n={n:3d}: max ratio = {best[0]:.6f}  (n1={int(round(p*n))} coords at {u:.4f}, rest at {w:.4f})")

    print("\nfull multistart over x in [0,1]^n (Nelder-Mead), k=3:")
    for n in [8, 10, 12]:
        best = (0, None)
        for _ in range(20):
            x0 = rng.random(n)
            res = minimize(lambda z: -ratio_complete(np.clip(z, 0, 1), 3), x0, method="Nelder-Mead",
                           options={"maxfev": 4000 * n, "xatol": 1e-7, "fatol": 1e-11})
            if -res.fun > best[0]:
                best = (-res.fun, np.clip(res.x, 0, 1))
        print(f"  n={n:3d}: max ratio = {best[0]:.6f}  x = {np.round(np.sort(best[1]), 4)}")

    print("\nn -> oo limit, discrete profiles with up to 3 atoms, k = 2,3,4,5:")
    for k in [2, 3, 4, 5]:
        best = (0, None)
        for _ in range(80):
            z0 = rng.random(5)

            def obj(z):
                w = np.abs(z[:3]) + 1e-9
                v = np.clip(z[3:], 0, 1)
                return -limit_ratio(w, np.append(v, v[0]), k)  # third atom duplicates the first (2 free atoms)

            res = minimize(obj, z0, method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-12})
            if -res.fun > best[0]:
                best = (-res.fun, res.x)
        c = (k - 1) / k
        print(f"  k={k}: best 2-atom profile ratio = {best[0]:.6f};  uniform c=(k-1)/k gives 1/(1-c^(k-1)) = {1/(1-c**(k-1)):.6f}")


if __name__ == "__main__":
    main()
