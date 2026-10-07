"""Single-tree lower bound (Corollary 2.1) for the path family
F_n(x) = sum phi(x_i) + b sum x_i x_{i+1},  phi(t) = t^2 - kappa t^4,  X0 = [-1,1]^n,
with alphaBB weight |b|/2 on each bilinear factor (unary factors convex, exact).

Evaluates, in high precision,
  L_n(eps) = 2 (2n/pi)^{n/2} (prod alpha_j / det H)^{1/2} / Gamma(n/2) * J_n(R/sqrt(eps)),
  H = tridiag(b, 2, b),  R^2 = lambda_min(H)/2,  J_n(T) = int_0^T t^{n-1} (1+t^2)^{-n/2} dt,
and the closed-form bound 0.068 sqrt(n) (2e/pi)^{n/2} log(0.2/(n eps)) (b = 0.8).
Also checks, for n = 2 and 3, that the ellipsoid restriction is below the full
integral int_{X0} (F + eps)^{-n/2} (computed by quadrature / Monte Carlo).
"""
import sys
import mpmath as mp
import numpy as np

mp.mp.dps = 30


def detH(n, b):
    d0, d1 = mp.mpf(1), mp.mpf(2)
    for _ in range(2, n + 1):
        d0, d1 = d1, 2 * d1 - b * b * d0
    return d1


def Jn(n, T):
    f = lambda t: t ** (n - 1) * (1 + t * t) ** (-mp.mpf(n) / 2)
    pts = [0, 1]
    while pts[-1] * 10 < T:
        pts.append(pts[-1] * 10)
    pts.append(T)
    return mp.quad(f, pts)


def L(n, b, eps):
    b = mp.mpf(b)
    alphas = [abs(b)] * n
    alphas[0] = alphas[-1] = abs(b) / 2
    prod_a = mp.fprod(alphas)
    lam_min = 2 - 2 * abs(b) * mp.cos(mp.pi / (n + 1))
    R = mp.sqrt(lam_min / 2)
    T = R / mp.sqrt(eps)
    val = 2 * (2 * n / mp.pi) ** (mp.mpf(n) / 2) * mp.sqrt(prod_a / detH(n, b)) / mp.gamma(mp.mpf(n) / 2) * Jn(n, T)
    return val


def closed_form(n, eps):
    return 0.068 * mp.sqrt(n) * (2 * mp.e / mp.pi) ** (mp.mpf(n) / 2) * mp.log(0.2 / (n * eps))


def F(x, b, kappa):
    return np.sum(x ** 2 - kappa * x ** 4, axis=-1) + b * np.sum(x[..., :-1] * x[..., 1:], axis=-1)


def main():
    b, kappa = 0.8, 0.1
    print("# Corollary 2.1 on the path family, b=%.2f kappa=%.2f" % (b, kappa))
    print("# n  eps  L_n(eps)  closed_form  L_n/L_{n-1}")
    for eps in [1e-4, 1e-6, 1e-8]:
        prev = None
        for n in [2, 3, 4, 6, 8, 10, 12, 16, 20, 30, 40, 60, 80]:
            v = L(n, b, eps)
            cf = closed_form(n, eps) if 0.2 / (n * eps) > 1 else mp.nan
            ratio = (v / prev) ** (mp.mpf(1) / (n - pn)) if prev is not None else mp.nan
            print("%3d %.0e %12.5e %12.5e  per-var-growth %s" % (n, eps, float(v), float(cf), mp.nstr(ratio, 5)))
            prev, pn = v, n
    # asymptotic per-variable base and threshold on b
    print("# asymptotic per-variable base sqrt(4e/pi * |b|/(1+sqrt(1-b^2)))")
    for bb in [0.5, 0.535, 0.54, 0.6, 0.8, 0.9]:
        base = mp.sqrt(4 * mp.e / mp.pi * bb / (1 + mp.sqrt(1 - bb * bb)))
        print("b=%.3f base=%s" % (bb, mp.nstr(base, 6)))
    thr = mp.findroot(lambda bb: bb / (1 + mp.sqrt(1 - bb * bb)) - mp.pi / (4 * mp.e), 0.5)
    print("# threshold |b| for exponential growth: %s" % mp.nstr(thr, 6))
    # sanity: full integral >= ellipsoid lower bound (n = 2 by quadrature, n = 3 by Monte Carlo)
    eps = 1e-3
    n = 2
    full = mp.quad(lambda u, v: (F(np.array([float(u), float(v)]), b, kappa) + eps) ** (-1.0), [-1, 0, 1], [-1, 0, 1])
    alphas_prod = (b / 2) ** 2
    ell = (n / mp.pi ** 2) ** (n / 2) * mp.sqrt(alphas_prod) * full
    print("# n=2 eps=1e-3: full-integral bound %s >= ellipsoid bound %s" % (mp.nstr(ell, 6), mp.nstr(L(2, b, eps), 6)))
    rng = np.random.default_rng(0)
    n = 3
    N = 4_000_000
    x = rng.uniform(-1, 1, size=(N, n))
    vals = (F(x, b, kappa) + eps) ** (-n / 2)
    mc = 2 ** n * vals.mean()
    se = 2 ** n * vals.std() / np.sqrt(N)
    alphas_prod = (b / 2) ** 2 * b
    full = (n / np.pi ** 2) ** (n / 2) * np.sqrt(alphas_prod) * mc
    print("# n=3 eps=1e-3: full-integral bound (MC) %.4f +- %.4f >= ellipsoid bound %s" % (
        full, (n / np.pi ** 2) ** (n / 2) * np.sqrt(alphas_prod) * se, mp.nstr(L(3, b, eps), 6)))


if __name__ == "__main__":
    main()
