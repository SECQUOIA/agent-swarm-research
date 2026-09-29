"""Conjecture 7.1': a curved variant of Proposition 4.7 on which the listed lower bounds are
O(eps^-3/4) while N_cov = Omega(1/(eps log(1/eps))).

Instance (box-constrained, phi bilinear, g convex semialgebraic):
    psi(s) = -s - s^2/2 (strictly decreasing and concave on [-1, 2]),  c0 = 3/4,
    D = x1 - x2 - c0,
    G(D, y) = max_{s in [-1,2]} [ -s D - psi(s) y + psi(s) s ]   (a max of affine maps: convex),
    f = G(D, y) + D*y  on [0,1]^3,   phi = D*y = x1*y - x2*y - c0*y  (termwise McCormick).
Then m = f = max_s (D - psi(s)) (y - s) >= 0 (take s = y), and m = 0 on the ruled surface
Sigma = {D = psi(y)}.  Sigma contains the direction (1,1,0) (so it is not transversal) and is curved.

Checks (floating point; the proof is in the recheck report):
[1] m >= 0 and m = 0 on Sigma; kappa0 = min m / (D - psi(y))^2 on a grid (proof needs >= 1/12);
[2] convexity of G (random midpoint tests);
[3] A_Sigma = (t, y)-area of Sigma in the box;
[4] the slice inequality Gamma_C(midpoint) >= ell * d_y on random boxes (Lemma 2.1(c));
[5] the proved lower bound on N_cov against upper bounds for every tool listed in L(eps).
"""
import math
import random

C0 = 0.75
S_LO, S_HI = -1.0, 2.0


def psi(s):
    return -s - 0.5 * s * s


def m_val(D, y):
    """max over s in [-1, 2] of (D - psi(s)) (y - s); stationary points of the cubic + endpoints."""
    cands = [S_LO, S_HI, y]
    # d/ds: -(D - psi(s)) + psi'(s)(y - s) ... expanded: -1.5 s^2 + (y - 2) s + (y - D) = 0
    A, B, Cc = -1.5, y - 2.0, y - D
    disc = B * B - 4 * A * Cc
    if disc >= 0:
        for r in ((-B + math.sqrt(disc)) / (2 * A), (-B - math.sqrt(disc)) / (2 * A)):
            if S_LO <= r <= S_HI:
                cands.append(r)
    return max((D - psi(s)) * (y - s) for s in cands)


def G_val(D, y):
    return m_val(D, y) - D * y


print("[1] m >= 0, m = 0 on Sigma, quadratic growth constant")
mn, kap, zero_err = math.inf, math.inf, 0.0
N = 400
for i in range(N + 1):
    y = i / N
    zero_err = max(zero_err, abs(m_val(psi(y), y)))
    for j in range(N + 1):
        D = -1.75 + 2.0 * j / N          # D = x1 - x2 - 3/4 ranges over [-1.75, 0.25]
        mv = m_val(D, y)
        mn = min(mn, mv)
        dl = D - psi(y)
        if abs(dl) > 1e-9:
            kap = min(kap, mv / (dl * dl))
print(f"    min m on grid = {mn:.3e};  max |m| on Sigma = {zero_err:.3e};  "
      f"min m/(D-psi(y))^2 = {kap:.4f}  (>= 1/12 = {1 / 12:.4f}: {kap >= 1 / 12})")

print("[2] convexity of G (midpoint test on random pairs)")
rng = random.Random(1)
worst = -math.inf
for _ in range(20000):
    p = (rng.uniform(-1.75, 0.25), rng.uniform(0, 1)); q = (rng.uniform(-1.75, 0.25), rng.uniform(0, 1))
    mid = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    worst = max(worst, G_val(*mid) - (G_val(*p) + G_val(*q)) / 2)
print(f"    max [G(mid) - average] = {worst:.2e}  (<= 0 up to rounding means convex)")

print("[3] A_Sigma = int_0^1 (1 - |psi(y) + c0|) dy")
M = 200000
A_sig = sum(max(0.0, 1 - abs(psi((k + 0.5) / M) + C0)) for k in range(M)) / M
print(f"    A_Sigma = {A_sig:.5f}")


def mc_gap(c, xi, xj, li, ui, lj, uj):
    dim, dip, djm, djp = xi - li, ui - xi, xj - lj, uj - xj
    return c * min(dim * djm, dip * djp) if c > 0 else -c * min(dim * djp, dip * djm)


print("[4] slice inequality: at the midpoint of the row-y slice of Sigma ∩ C, Gamma >= ell * d_y")
bad, used, minr = 0, 0, math.inf
for _ in range(50000):
    l1, u1 = sorted((rng.random(), rng.random())); l2, u2 = sorted((rng.random(), rng.random()))
    ly, uy = sorted((rng.random(), rng.random()))
    y = rng.uniform(ly, uy)
    off = psi(y) + C0                     # on Sigma: x1 = t + off, x2 = t
    tl, tu = max(l2, l1 - off), min(u2, u1 - off)
    if tl >= tu:
        continue
    ell = tu - tl
    t = (tl + tu) / 2
    x1, x2 = t + off, t
    gap = mc_gap(1.0, x1, y, l1, u1, ly, uy) + mc_gap(-1.0, x2, y, l2, u2, ly, uy)
    dy = min(y - ly, uy - y)
    used += 1
    if ell * dy > 0:
        minr = min(minr, gap / (ell * dy))
    bad += gap < ell * dy * (1 - 1e-12)
print(f"    {used} boxes: violations {bad}, min Gamma/(ell d_y) = {minr:.4f}")

print("[5] proved lower bound on N_cov vs upper bounds on every tool listed in L(eps)")
k0 = 1 / 12


def thm36_p2(eps):
    # max over eta of min(1, 4 (eta/k0)^(1/4)) / (9 (eps + eta))
    best = 0.0
    for i in range(-4000, 1):
        eta = eps * 10 ** (i / 200)
        if eta > 10:
            break
        best = max(best, min(1.0, 4 * (eta / k0) ** 0.25) / (9 * (eps + eta)))
    for i in range(0, 4000):
        eta = eps * 10 ** (i / 200)
        if eta > 10:
            break
        best = max(best, min(1.0, 4 * (eta / k0) ** 0.25) / (9 * (eps + eta)))
    return best


print("    eps      N_cov >=      Thm3.6(p=2)<=  Thm3.6(p=1)<=  Thm3.8<=    Thm3.4<=   Prop3.10<=  ratio")
for k in range(4, 17, 2):
    eps = 10.0 ** -k
    lb = A_sig / (2 * eps * (1 + math.log(1 / (2 * eps))))
    t36 = thm36_p2(eps)
    t36p1 = 1 / (2 * math.sqrt(eps))
    t38 = 1 / (4 * math.sqrt(eps)) + 0.5
    t34 = 1 / (math.pi * math.sqrt(eps))
    p310 = (1 / math.sqrt(k0)) ** 3
    L = max(t36, t36p1, t38, t34, p310)
    print(f"    1e-{k:02d}  {lb:12.4g}  {t36:12.4g}  {t36p1:12.4g}  {t38:10.4g}  {t34:10.4g}  {p310:8.3g}"
          f"  {lb / L:8.2f}")
print("    ratio = N_cov lower bound / max of the tool upper bounds; it grows like eps^(-1/4)/log(1/eps)")
