"""Monte Carlo check of Step 4 of Theorem 2: for a Haar-random unimodular
lattice L and t uniform on R^n/L, N = |L ∩ B(t, r)| has E N = Var N = vol B_r.

Haar-random lattices are approximated by Goldstein-Mayer (Hecke) lattices
    L = p^{-1/n} {x in Z^n : x_1 = a_2 x_2 + ... + a_n x_n (mod p)},
p prime, a uniform in (Z/p)^{n-1}; these equidistribute to Haar as p -> infinity.
A fundamental domain of the unscaled lattice is [0,p) x [0,1)^{n-1}.
We also report Var_t N for a few *fixed* lattices, to show that the identity
Var N = V' needs the average over L (for fixed L it can be far from V').
"""
import math, sys
import numpy as np


def count_points(p, a, T, R):
    n = len(T)
    rng_axes = [np.arange(math.ceil(T[i] - R), math.floor(T[i] + R) + 1) for i in range(1, n)]
    grids = np.meshgrid(*rng_axes, indexing='ij')
    X = np.stack([g.ravel() for g in grids], axis=1)  # candidates for x_2..x_n
    d2 = ((X - T[1:]) ** 2).sum(axis=1)
    ok = d2 <= R * R
    X = X[ok]; d2 = d2[ok]
    R1 = np.sqrt(R * R - d2)
    c = (X @ a) % p
    lo = np.ceil((T[0] - R1 - c) / p); hi = np.floor((T[0] + R1 - c) / p)
    return int(np.maximum(hi - lo + 1, 0).sum())


def unit_ball_vol(n):
    return math.pi ** (n / 2) / math.gamma(n / 2 + 1)


def run(n, Vp, samples, p, rng):
    GH = unit_ball_vol(n) ** (-1.0 / n)
    r = GH * Vp ** (1.0 / n)
    R = r * p ** (1.0 / n)
    Ns = np.empty(samples)
    for s in range(samples):
        a = rng.integers(0, p, n - 1)
        T = np.concatenate([[rng.uniform(0, p)], rng.uniform(0, 1, n - 1)])
        Ns[s] = count_points(p, a, T, R)
    m = Ns.mean(); v = Ns.var(ddof=1)
    # standard error of the variance estimate (normal approx using 4th moment)
    se_v = math.sqrt(max(((Ns - m) ** 4).mean() - v * v, 0) / samples)
    print("n=%d V'=%5.1f p=%d samples=%d: mean N=%.3f (se %.3f), Var N=%.3f (se %.3f), Var/V'=%.3f, P(N<V'/2)=%.4f, Chebyshev 4/V'=%.3f"
          % (n, Vp, p, samples, m, Ns.std() / math.sqrt(samples), v, se_v, v / Vp, (Ns < Vp / 2).mean(), 4 / Vp))
    sys.stdout.flush()


def fixed_lattice(n, Vp, samples, p, rng, a):
    GH = unit_ball_vol(n) ** (-1.0 / n)
    R = GH * Vp ** (1.0 / n) * p ** (1.0 / n)
    Ns = np.array([count_points(p, a, np.concatenate([[rng.uniform(0, p)], rng.uniform(0, 1, n - 1)]), R)
                   for _ in range(samples)])
    return Ns.mean(), Ns.var(ddof=1)


if __name__ == '__main__':
    rng = np.random.default_rng(12345)
    p = 100003
    for n, Vps, samples in ((2, (2.0, 8.0, 20.0), 40000), (3, (2.0, 8.0, 20.0), 40000), (4, (2.0, 8.0, 20.0), 20000)):
        for Vp in Vps:
            run(n, Vp, samples, p, rng)
    print("fixed lattices (n=3, V'=8, 4000 targets each): mean, Var_t N")
    for _ in range(6):
        a = rng.integers(0, p, 2)
        m, v = fixed_lattice(3, 8.0, 4000, p, rng, a)
        print("   a=%s: mean=%.3f Var_t=%.3f" % (a, m, v))
