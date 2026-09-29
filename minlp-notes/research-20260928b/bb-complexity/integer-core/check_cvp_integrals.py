"""High-precision check of the pair-count integral in Theorem 3.4.

Units: lengths in GH units, so vol(B_r) = r^n.  With r0 <= 1 (r0^2 = lower
bound on (OPT - eps)/GH^2), R^2 = rho r0^2, s1^2 = 4 (R^2 - r0^2):

  J / V' = int_{|v| < s1} vol(B_R cap (B_R + v)) dv / vol(B_R)
         = n (2R)^n int_0^{y1} y^{n-1} I_{1-y^2}((n+1)/2, 1/2) dy,
  y1 = s1/(2R) = sqrt((rho-1)/rho),

where I is the regularized incomplete beta function (lens of two radius-R
balls at distance 2Ry, as a fraction of vol(B_R)).  The proof of Theorem 3.4
uses the bound J/V' <= n (4 (rho-1) r0^2 / rho)^{n/2}.  This script
(1) evaluates J/V' by quadrature (mpmath, 30 digits) and checks the bound,
(2) checks the lens-fraction formula against Monte Carlo in small dimension,
(3) reports the exponential rate (1/n) log2(J/V') to locate the threshold rho = 4/3.
"""
import mpmath as mp
import numpy as np

mp.mp.dps = 30


def lens_fraction(n, y):
    # two balls of radius 1 with centres at distance 2y (0 <= y <= 1)
    return mp.betainc((n + 1) / mp.mpf(2), mp.mpf(1) / 2, 0, 1 - y * y, regularized=True)


def J_over_V(n, rho, r0=1):
    R = mp.sqrt(rho) * r0
    y1 = mp.sqrt((rho - 1) / rho)
    integ = mp.quad(lambda y: y ** (n - 1) * lens_fraction(n, y), [0, y1])
    return n * (2 * R) ** n * integ


def bound(n, rho, r0=1):
    return n * (4 * (rho - 1) * r0 ** 2 / rho) ** (mp.mpf(n) / 2)


def mc_lens(n, y, samples=400000, seed=0):
    rng = np.random.default_rng(seed)
    g = rng.standard_normal((samples, n))
    g /= np.linalg.norm(g, axis=1)[:, None]
    r = rng.random(samples) ** (1.0 / n)
    x = g * r[:, None]
    c = np.zeros(n)
    c[0] = 2 * y
    return float(np.mean(np.linalg.norm(x - c, axis=1) < 1))


if __name__ == "__main__":
    print("== lens fraction: formula vs Monte Carlo ==")
    for n, y in [(3, 0.3), (5, 0.5), (8, 0.2), (12, 0.4)]:
        print(f"n={n} y={y}: formula={float(lens_fraction(n, mp.mpf(y))):.5f}  MC={mc_lens(n, y):.5f}")
    print("== J/V' exact vs bound n(4(rho-1)/rho)^{n/2} (r0 = 1) ==")
    worst = 0.0
    for rho in [mp.mpf("1.1"), mp.mpf("1.2"), mp.mpf("1.3"), mp.mpf(4) / 3 - mp.mpf("0.01")]:
        for n in [10, 20, 40, 80, 160, 320]:
            J = J_over_V(n, rho)
            b = bound(n, rho)
            worst = max(worst, float(J / b))
            print(f"rho={float(rho):.4f} n={n:4d}: J/V'={mp.nstr(J, 6):>12}  bound={mp.nstr(b, 6):>12}  ratio={float(J / b):.3e}")
    print(f"max ratio exact/bound = {worst:.3e} (must be <= 1)")
    print("== rate (1/n) log2(J/V') at n = 400, and log2 of bound base ==")
    for rho in [1.25, 1.3, 1.32, 4 / 3, 1.34, 1.36, 1.4]:
        rho = mp.mpf(rho)
        n = 400
        J = J_over_V(n, rho)
        print(f"rho={float(rho):.4f}: rate={float(mp.log(J, 2) / n):+.5f}   0.5*log2(4(rho-1)/rho)={float(0.5 * mp.log(4 * (rho - 1) / rho, 2)):+.5f}")
    print("== clique exponent 0.5*log2(rho) at rho=4/3:", float(0.5 * mp.log(mp.mpf(4) / 3, 2)))
    print("== class exponent 0.5*log2(3/2):", float(0.5 * mp.log(mp.mpf(3) / 2, 2)))
    print("== old shell exponent 0.5*log2(5/4):", float(0.5 * mp.log(mp.mpf(5) / 4, 2)))
