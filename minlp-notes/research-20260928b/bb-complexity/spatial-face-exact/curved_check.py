"""Proposition 3.14 (curved, non-transversal optimal surface; counterexample to Conjecture 7.1' found by
the face-exact recheck).  Own code; verifies the counterexample numerically.

psi(s) = -s - s^2/2, c0 = 3/4, D = x1 - x2 - c0, on [0,1]^3:
   f = max_{s in [-1,2]} (D - psi(s)) (y - s)  =  G(D, y) + D y,
   G(D, y) = max_s [-s D - psi(s) y + psi(s) s]   (convex: max of affine functions of (D, y)),
   phi = D y = x1 y - x2 y - c0 y (bilinear, path x1 - y - x2), termwise McCormick.
Checks:
 [1] closed-form maximisation over s (cubic in s: endpoints and critical points) versus a fine grid;
 [2] f >= 0, f = 0 on Sigma = {D = psi(y)}, and f >= (D - psi(y))^2 / 12;
 [3] convexity of G by midpoint tests;
 [4] the row-slice inequality Gamma_C(p) >= ell * d_y at the midpoint p of a row slice, for random boxes
     (exact McCormick gaps, Lemma 2.1(a));
 [5] A = area of Sigma in (t, y) coordinates, and the lower bound A / (2 eps (1 + ln(1/(2 eps))));
 [6] the Theorem 3.6 (p = 2) upper bound 4 (12 eta)^(1/4) / (9 (eps + eta)) maximised over eta.
"""
import math
import numpy as np
from scipy import integrate

rng = np.random.default_rng(11)
C0 = 0.75
psi = lambda s: -s - s * s / 2


def f_closed(D, y):
    cands = [-1.0, 2.0]
    # h(s) = (D - psi(s)) (y - s); h'(s) = -(3/2) s^2 + (y - 2) s + (y - D)
    disc = (y - 2) ** 2 + 6 * (y - D)
    if disc >= 0:
        for sgn in (1, -1):
            s = ((y - 2) + sgn * math.sqrt(disc)) / 3
            if -1 <= s <= 2:
                cands.append(s)
    return max((D - psi(s)) * (y - s) for s in cands)


def f_grid(D, y, n=20001):
    s = np.linspace(-1, 2, n)
    return float(np.max((D - psi(s)) * (y - s)))


def G(D, y):
    return f_closed(D, y) - D * y


def gap_bilinear(c, xi, xj, li, ui, lj, uj):
    dm_i, dp_i, dm_j, dp_j = xi - li, ui - xi, xj - lj, uj - xj
    return c * min(dm_i * dm_j, dp_i * dp_j) if c > 0 else -c * min(dm_i * dp_j, dp_i * dm_j)


def main():
    worst = 0.0
    for _ in range(3000):
        x1, x2, y = rng.uniform(0, 1, 3)
        D = x1 - x2 - C0
        worst = max(worst, abs(f_closed(D, y) - f_grid(D, y)))
    print(f"[1] closed-form max over s versus grid (20001 points), 3000 points: max diff = {worst:.2e}")

    fmin, onS, ratio = math.inf, 0.0, math.inf
    for _ in range(20000):
        x1, x2, y = rng.uniform(0, 1, 3)
        D = x1 - x2 - C0
        v = f_closed(D, y)
        fmin = min(fmin, v)
        dlt = D - psi(y)
        if abs(dlt) > 1e-6:
            ratio = min(ratio, v / dlt ** 2)
    for _ in range(5000):
        y, t = rng.uniform(0, 1, 2)
        x2 = t; x1 = t + psi(y) + C0
        if 0 <= x1 <= 1:
            onS = max(onS, abs(f_closed(x1 - x2 - C0, y)))
    print(f"[2] min f = {fmin:.2e} (>= 0);  max |f| on Sigma = {onS:.2e};  min f/(D-psi(y))^2 = {ratio:.4f} (>= 1/12 = 0.0833)")

    viol = 0
    for _ in range(20000):
        p, q = rng.uniform(-1.75, 0.25, 2), rng.uniform(0, 1, 2)
        Dm, ym = 0.5 * (p[0] + p[1]), 0.5 * (q[0] + q[1])
        if G(Dm, ym) > 0.5 * (G(p[0], q[0]) + G(p[1], q[1])) + 1e-12:
            viol += 1
    print(f"[3] convexity of G: midpoint violations in 20000 tests = {viol}")

    worst, nchk = math.inf, 0
    for _ in range(40000):
        l = rng.uniform(0, 1, 3); u = l + rng.uniform(0.001, 1, 3); u = np.minimum(u, 1)
        y = rng.uniform(l[2], u[2])
        off = psi(y) + C0   # x1 = t + off, x2 = t
        t_lo = max(l[1], l[0] - off); t_hi = min(u[1], u[0] - off)
        if t_hi <= t_lo:
            continue
        ell = t_hi - t_lo; t = 0.5 * (t_lo + t_hi)
        x1, x2 = t + off, t
        gam = gap_bilinear(1.0, x1, y, l[0], u[0], l[2], u[2]) + gap_bilinear(-1.0, x2, y, l[1], u[1], l[2], u[2])
        dy = min(y - l[2], u[2] - y)
        if ell * dy > 1e-12:
            worst = min(worst, gam / (ell * dy)); nchk += 1
    print(f"[4] row-slice inequality Gamma(p) >= ell*d_y on {nchk} random boxes: min ratio = {worst:.4f} (>= 1)")

    A = integrate.quad(lambda y: 1 - abs(psi(y) + C0), 0, 1, points=[-1 + math.sqrt(2.5)])[0]
    print(f"[5] A = {A:.4f};  lower bound A/(2 eps (1 + ln(1/(2 eps)))):")
    for e in (1e-2, 1e-4, 1e-6, 1e-10, 1e-16):
        lb = A / (2 * e * (1 + math.log(1 / (2 * e))))
        ub = max(4 * (12 * eta) ** 0.25 / (9 * (e + eta)) for eta in np.geomspace(e * 1e-3, 1.0, 4000))
        print(f"    eps={e:.0e}: N_cov >= {lb:.3e};  Thm 3.6 (p=2) bound <= {ub:.3e} = {ub * e ** 0.75:.3f} eps^-3/4;  ratio {lb / ub:.2f}")


if __name__ == "__main__":
    main()
