"""Constant checks for the second-round revision of theory-coupling/coupling.md.

(1) Proposition 1.1, convex-cost remark. Path family F_n of [D, Section 2.1]
    (b = 0.8, kappa = 0.1) plus g(y) = y^T G y / 2, y = A x (G PSD, A dense).
    Checks: 0 stays the unique minimizer with value 0 (sampled); the new
    quadratic upper bound H' = H + A^T G A holds (sampled); the determinant
    identity det(H')^{-1/2} = det(H)^{-1/2} det(I + H^{-1/2} A^T G A H^{-1/2})^{-1/2};
    the lower estimate (1 + ||A||^2 ||G|| / lambda_min(H))^{-k/2}; and the full
    [D, Corollary 2.1] bound with H' divided by the one with H (the J_n factor
    only grows, since lambda_min(H') >= lambda_min(H)).
(2) Theorem 4.5, Gamma_sigma. Random parameters; theta = largest power of 1/2
    below [2(1+Delta)(d+1) max(1, 64 sqrt(k) V)]^{-1}, V = nu_A (1 + M_F/c_g)^2,
    with the worst case rho ||A|| alpha_A / c_g = V. Checks (T4) and
    4/theta <= Gamma_sigma, and K/c_g <= kappa^2 (1 + M_F/c_g)^2.
(3) Proposition 5.2. alpha/lambda' and the alphaBB base at m = 4; the
    envelope extension: h'' <= -(beta - 12) on [-1, 1], chord gap >=
    ((beta-12)/2)(s-l)(u-s) on random boxes, and the bases
    sqrt(4 e alpha' / (pi lambda')) over 1 <= k <= m for m = 4, 8, 16, 32, 1024.

Usage: python3 r4_constants.py
"""
import math

import numpy as np
from scipy.special import gammaln
from scipy.integrate import quad

rng = np.random.default_rng(20260930)


def fn(x, b=0.8, kap=0.1):
    return np.sum(x ** 2 - kap * x ** 4) + b * np.sum(x[:-1] * x[1:])


def cor21(n, alphas, H, rin, eps):
    """[D, Corollary 2.1] bound, log10."""
    lmin = np.linalg.eigvalsh(H)[0]
    R = math.sqrt(lmin * rin ** 2 / 2)
    T = R / math.sqrt(eps)
    J = quad(lambda t: t ** (n - 1) * (1 + t * t) ** (-n / 2), 0, T, limit=200)[0]
    sign, logdet = np.linalg.slogdet(H)
    val = (math.log(2) + (n / 2) * math.log(2 * n / math.pi) + 0.5 * (np.sum(np.log(alphas)) - logdet)
           - gammaln(n / 2) + math.log(J))
    return val / math.log(10)


def part1():
    print("(1) Proposition 1.1 with a convex quadratic cost on k aggregates")
    b = 0.8
    for n, k in ((8, 1), (8, 3), (16, 2), (24, 4)):
        H = np.diag(np.full(n, 2.0)) + np.diag(np.full(n - 1, b), 1) + np.diag(np.full(n - 1, b), -1)
        A = rng.normal(size=(k, n))
        Q = rng.normal(size=(k, k))
        G = Q @ Q.T / k
        Hp = H + A.T @ G @ A
        # sampled checks on [-1,1]^n
        worst_up, worst_min = -np.inf, np.inf
        for _ in range(20000):
            x = rng.uniform(-1, 1, size=n) * rng.uniform(0, 1) ** 2
            val = fn(x) + 0.5 * (A @ x) @ G @ (A @ x)
            worst_up = max(worst_up, val - 0.5 * x @ Hp @ x)
            worst_min = min(worst_min, val)
        w, V = np.linalg.eigh(H)
        Hm12 = V @ np.diag(w ** -0.5) @ V.T
        M = np.eye(n) + Hm12 @ A.T @ G @ A @ Hm12
        fac = np.linalg.det(M) ** -0.5
        ident = abs(np.linalg.det(Hp) ** -0.5 - np.linalg.det(H) ** -0.5 * fac) / np.linalg.det(Hp) ** -0.5
        low = (1 + np.linalg.norm(A, 2) ** 2 * np.linalg.norm(G, 2) / w[0]) ** (-k / 2)
        alphas = np.full(n, b)
        alphas[0] = alphas[-1] = b / 2
        eps = 1e-6
        ratio = 10 ** (cor21(n, alphas, Hp, 1.0, eps) - cor21(n, alphas, H, 1.0, eps))
        print(f"  n={n:2d} k={k}: max(m - x^T H' x/2) = {worst_up:.2e} (<= 0), min value = {worst_min:.2e} (>= 0); "
              f"identity rel.err {ident:.1e}; det factor {fac:.4e} >= lower est. {low:.4e}: {fac >= low}; "
              f"Cor 2.1 ratio {ratio:.4e} >= det factor: {ratio >= fac * (1 - 1e-9)}")
    print("  one dense row of ones, g(y) = y^2/2: det factor versus n (is it a constant?)")
    for n in (10, 100, 1000):
        H = np.diag(np.full(n, 2.0)) + np.diag(np.full(n - 1, b), 1) + np.diag(np.full(n - 1, b), -1)
        a = np.ones(n)
        fac = (1 + a @ np.linalg.solve(H, a)) ** -0.5
        print(f"    n={n:5d}: factor {fac:.4f}; sqrt(n) * factor = {math.sqrt(n) * fac:.4f}")


def part2():
    print("\n(2) Theorem 4.5: Gamma_sigma from (T4)")
    bad = 0
    maxratio = 0.0
    for _ in range(200000):
        Delta = int(rng.integers(0, 6))
        d = int(rng.integers(0, 60))
        k = int(rng.integers(1, 40))
        V = 10 ** rng.uniform(-4, 4)
        X = 2 * (1 + Delta) * (d + 1) * max(1.0, 64 * math.sqrt(k) * V)
        mu = math.ceil(math.log2(X))
        theta = 2.0 ** (-mu)
        while theta * 2 <= 1 / X:  # guard against rounding
            theta *= 2
        while theta > 1 / X:
            theta /= 2
        t4a = theta * ((1 + Delta) * d + Delta) <= 0.5
        # worst case rho ||A|| alpha_A = V c_g, so condition 2 reads
        t4b = 128 * V * math.sqrt(k) * (1 + Delta) * (d + 1) * theta <= 1 + 1e-12
        gam = 16 * (1 + Delta) * (d + 1) * max(1.0, 64 * math.sqrt(k) * V)
        ok = t4a and t4b and (4 / theta <= gam * (1 + 1e-12)) and theta <= 1
        bad += not ok
        maxratio = max(maxratio, (4 / theta) / gam)
    print(f"  200000 random (Delta, d, k, V): failures {bad}; max (4/theta)/Gamma_sigma = {maxratio:.4f} (<= 1)")
    worst = 0.0
    for m in np.concatenate([np.linspace(0, 10, 1001), 10 ** np.linspace(-6, 6, 1001)]):
        lhs = m * m / 2 + m / 2 + 0.5  # K / (c_g kappa^2) with m = M_F/c_g
        worst = max(worst, lhs / (1 + m) ** 2)
    print(f"  max over m = M_F/c_g of (K/c_g)/(kappa^2 (1+m)^2) = {worst:.4f} (<= 1)")
    for Delta, d in ((1, 10), (2, 4)):
        print(f"  paths/trees example Delta={Delta}, d={d}: 16(1+Delta)(d+1) = {16 * (1 + Delta) * (d + 1)}")


def part3():
    print("\n(3) Proposition 5.2")
    for m in (4, 8, 16):
        lam1 = 0.8 * m + 0.5  # k = 1, largest lambda'
        a = 1.6 * m
        print(f"  alphaBB m={m}: alpha/lambda' (k=1) = {a / lam1:.5f}, base sqrt(4e a/(pi l')) = "
              f"{math.sqrt(4 * math.e * a / (math.pi * lam1)):.4f}")
    for m in (4, 8, 16, 32):
        beta = 3.2 * m
        s = np.linspace(-1, 1, 20001)
        hpp = -beta + 12 * s ** 2
        worst_gap = np.inf
        for _ in range(3000):
            l, u = np.sort(rng.uniform(-1, 1, 2))
            if u - l < 1e-6:
                continue
            ss = np.linspace(l, u, 401)
            h = -beta * ss ** 2 / 2 + ss ** 4
            hl, hu = -beta * l ** 2 / 2 + l ** 4, -beta * u ** 2 / 2 + u ** 4
            chordv = hl + (hu - hl) * (ss - l) / (u - l)
            q = (ss - l) * (u - ss)
            inner = q > 1e-12
            if inner.any():
                worst_gap = min(worst_gap, np.min((h - chordv)[inner] / q[inner]))
        ap = (beta - 12) / 2
        bases = [math.sqrt(max(0.0, 4 * math.e * ap / (math.pi * (0.8 * m + 1 / (2 * k * k)))))
                 for k in range(1, m + 1)]
        print(f"  m={m:3d}: max h'' on [-1,1] = {hpp.max():.2f} = -(beta-12) = {-(beta - 12):.2f}; "
              f"min (h - chord)/q over boxes = {worst_gap:.4f} >= alpha' = {ap:.4f}; "
              f"envelope base range {min(bases):.4f}-{max(bases):.4f}")
    m = 1024
    ap = (3.2 * m - 12) / 2
    print(f"  m=1024: base (k=1) {math.sqrt(4 * math.e * ap / (math.pi * (0.8 * m + 0.5))):.4f}; "
          f"limit sqrt(8e/pi) = {math.sqrt(8 * math.e / math.pi):.4f}")


if __name__ == "__main__":
    part1()
    part2()
    part3()
