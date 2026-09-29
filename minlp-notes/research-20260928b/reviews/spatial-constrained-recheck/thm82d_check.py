"""Independent recheck of Theorem 8.2(d) (first-order gap, Morse-Bott manifold).

1. Symbolic check of the constants in the lower and upper bounds.
2. Tube-volume bounds (1 -/+ R/tau)^p omega_{n-p} R^{n-p} H^p(M) on an ellipsoid (p = 2, n = 3),
   by Monte Carlo against Weyl's exact formula 2 R A + (8 pi/3) R^3.
3. Cell-counting step (steps 2-3 of the upper-bound proof): number of closed dyadic cells
   of side s_j meeting the closed r_j-tube of M, against
   (3/2)^p 2^(n-p) omega_(n-p) H^p(M) (Lambda_1/c_g)^((n-p)/2) s_j^(-(n+p)/2),
   for a circle in [0,1]^2 and a sphere in [0,1]^3, on the levels s_j <= s_*.
"""
import itertools
import math
import numpy as np
import sympy as sp

print("1. constants")
n, p, eps, Mf, alpha, H, om, tauM, Lam, cg, s = sp.symbols('n p eps M_f alpha H omega tau_M Lambda_1 c_g s', positive=True)
R = sp.sqrt(2 * eps / Mf)
lower_derived = 2**(-n) * 2**(-p) * om * R**(n - p) * H * (alpha / (4 * eps))**n
lower_stated = 2**(-n - p) * 2**((n - p) / 2) * 4**(-n) * om * H * alpha**n * Mf**(-(n - p) / 2) * eps**(-(n + p) / 2)
print("   lower: derived/stated =", sp.simplify(sp.powsimp(sp.expand_power_base(lower_derived / lower_stated, force=True), force=True)))
r_j = sp.sqrt(Lam * s / cg)
Nj_derived = sp.Rational(3, 2)**p * om * (2 * r_j)**(n - p) * H / s**n
Nj_stated = sp.Rational(3, 2)**p * 2**(n - p) * om * H * (Lam / cg)**((n - p) / 2) * s**(-(n + p) / 2)
print("   N_j: derived/stated =", sp.simplify(sp.powsimp(sp.expand_power_base(Nj_derived / Nj_stated, force=True), force=True)))
# final: 1 + 2^n 3^n * 2 (Lam/eps)^((n+p)/2) * const  vs stated 2^(n+1) 3^n (3/2)^p 2^(n-p) omega H (Lam/cg)^((n-p)/2) (Lam/eps)^((n+p)/2)
const = sp.Rational(3, 2)**p * 2**(n - p) * om * H * (Lam / cg)**((n - p) / 2)
up_derived = 2**n * 3**n * 2 * (Lam / eps)**((n + p) / 2) * const
up_stated = 2**(n + 1) * 3**n * sp.Rational(3, 2)**p * 2**(n - p) * om * H * (Lam / cg)**((n - p) / 2) * (Lam / eps)**((n + p) / 2)
print("   upper: derived/stated =", sp.simplify(up_derived / up_stated))
# level conditions
print("   sqrt(n) s <= r_j  <=>  s <= Lambda_1/(n c_g):",
      sp.solve(sp.Eq(n * s**2, Lam * s / cg), s))
print("   2 r_j <= tau_M/2  <=>  s <= c_g tau_M^2/(16 Lambda_1):",
      sp.solve(sp.Eq(Lam * s / cg, tauM**2 / 16), s))
# geometric sum: sum_{s_j > s_min} s_j^-a <= 2 s_min^-a needs a >= 1; here a = (n+p)/2 with p >= 1, n >= p+1
print("   (n+p)/2 >= 1.5 since p >= 1 and n >= p+1; sum_{k>=0} 2^(-a k) = 1/(1-2^-a) <= 2 for a >= 1")

print("\n2. tube volume, ellipsoid semi-axes (1, 0.8, 0.6); reach taken as c^2/a = 0.36")
rng = np.random.default_rng(1)
ax = np.array([1.0, 0.8, 0.6])


def dist_ellipsoid(X):
    a2 = ax**2
    lo = np.full(len(X), -a2.min() + 1e-15)
    hi = np.full(len(X), 10.0)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        F = np.sum((ax * X / (a2 + mid[:, None]))**2, axis=1) - 1
        lo = np.where(F > 0, mid, lo)
        hi = np.where(F > 0, hi, mid)
    t = 0.5 * (lo + hi)
    P = a2 * X / (a2 + t[:, None])
    return np.linalg.norm(X - P, axis=1)


# surface area
from scipy.integrate import dblquad
def area_integrand(v, u):
    x_u = np.array([-ax[0]*np.sin(u)*np.sin(v), ax[1]*np.cos(u)*np.sin(v), 0])
    x_v = np.array([ax[0]*np.cos(u)*np.cos(v), ax[1]*np.sin(u)*np.cos(v), -ax[2]*np.sin(v)])
    return np.linalg.norm(np.cross(x_u, x_v))
A = dblquad(area_integrand, 0, 2*np.pi, 0, np.pi)[0]
tau = ax[2]**2 / ax[0]
print(f"   area A = {A:.6f}")
for Rt in [0.05, 0.1, 0.18]:
    box = ax + Rt
    Nmc = 4_000_000
    hits = 0
    for _ in range(4):
        X = rng.uniform(-box, box, size=(Nmc // 4, 3))
        hits += np.count_nonzero(dist_ellipsoid(X) < Rt)
    vol = hits / Nmc * np.prod(2 * box)
    se = math.sqrt(hits * (1 - hits / Nmc)) / Nmc * np.prod(2 * box)
    weyl = 2 * Rt * A + 8 * math.pi / 3 * Rt**3
    lo_b = (1 - Rt / tau)**2 * 2 * Rt * A
    hi_b = (1 + Rt / tau)**2 * 2 * Rt * A
    print(f"   R={Rt}: MC vol = {vol:.5f} +- {se:.5f}; Weyl = {weyl:.5f}; bounds [{lo_b:.5f}, {hi_b:.5f}]; "
          f"R <= tau/2: {Rt <= tau/2}; inside bounds: {lo_b <= vol <= hi_b}")

print("\n3. cell counts vs the Theorem 8.2(d) per-level bound")


def count_cells_shell(center, R0, r, s, dim):
    """closed dyadic cells of side s in [0,1]^dim meeting {x : | |x-c| - R0 | <= r}."""
    k = int(round(1 / s))
    idx = np.arange(k)
    grids = np.meshgrid(*([idx] * dim), indexing='ij')
    lo = [g.astype(float) * s for g in grids]
    dmin2 = sum(np.maximum(0, np.maximum(l - c, c - (l + s)))**2 for l, c in zip(lo, center))
    dmax2 = sum(np.maximum(np.abs(l - c), np.abs(l + s - c))**2 for l, c in zip(lo, center))
    meet = (np.sqrt(dmin2) <= R0 + r) & (np.sqrt(dmax2) >= R0 - r)
    return int(np.count_nonzero(meet))


for dim, R0, center, lam, jr in [(2, 0.3, (0.513, 0.493), 1.0, range(8, 14)),
                                 (2, 0.3, (0.513, 0.493), 0.05, range(4, 14)),
                                 (3, 0.3, (0.513, 0.493, 0.507), 1.0, range(8, 10)),
                                 (3, 0.3, (0.513, 0.493, 0.507), 0.05, range(4, 9))]:
    pdim = dim - 1
    Hp = 2 * math.pi * R0 if pdim == 1 else 4 * math.pi * R0**2
    om = 2.0  # omega_1
    s_star = min(lam / dim, R0**2 / (16 * lam))  # Lambda_1/c_g = lam, tau_M = R0
    print(f"   {'circle in R^2' if dim == 2 else 'sphere in R^3'}, Lambda_1/c_g = {lam}, s_* = {s_star:.4g}")
    for j in jr:
        sj = 2.0**-j
        if sj > s_star:
            continue
        rj = math.sqrt(lam * sj)
        cnt = count_cells_shell(center, R0, rj, sj, dim)
        bound = 1.5**pdim * 2**(dim - pdim) * om * Hp * lam**((dim - pdim) / 2) * sj**(-(dim + pdim) / 2)
        print(f"      j={j:2d}: cells meeting tube = {cnt:8d}; bound = {bound:10.1f}; ratio = {cnt/bound:.3f}")
