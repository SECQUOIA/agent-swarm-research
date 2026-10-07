"""Reviewer's recomputation of the Theorem C.3 constants (chiral chain, b,g,ev = 0.6,0.3,0.05).

1. gamma_k(theta) on cores K_theta = [-theta,theta]^k for P_2 (and P_1), k = 7, with cg.py (independent).
2. Lambda_j exact maxima by dense grids; analytic per-variable base exp(gamma/(2 Lambda (k+1))).
3. Computed bound: Phi(mu) <= max{ e^{-mu gamma(1)}, ((1+theta_{i+1})/2) e^{-mu gamma(theta_i)}, Psi(mu) },
   Psi from the separable bound f_k(p) <= sum c_j p_j^2 (rechecked on a grid), evaluated by the reviewer's
   own code; optimize mu; also the best k-independent analytic base (k -> infinity limit).
4. Leftover windows: Phi_r(mu) <= 1 for windows of length r < k at the reported mu (needed when
   n+1 is not a multiple of k+1).
5. The ceiling box reported in chiral_bounds_P2.log (k = 7): recompute V(B) and mu0.
"""
import json, sys
import numpy as np
from cg import *

b, g, ev = 0.6, 0.3, 0.05; a = b + ev
ginf = (g - ev) ** 2 / (4 * g); q = (g - ev) / (2 * g)
d = int(sys.argv[1]) if len(sys.argv) > 1 else 2
k = int(sys.argv[2]) if len(sys.argv) > 2 else 7
thetas = np.round(np.arange(0.2, 1.0001, 0.05), 4)
gam = []
for th in thetas:
    cb = ClassBound(chiral_chain(k, b, g, ev), poly_tests(d), K=7)
    lo, up, it = cb.bound(np.full(k, -th), np.full(k, th), None, maxit=300, tol=1e-10)
    gam.append(-up)
gam = np.array(gam)
print(json.dumps(dict(cls=f"P{d}", k=k, gamma_theta={float(t): round(float(v), 5) for t, v in zip(thetas, gam)})), flush=True)

# 2. Lambda
G = np.linspace(-1, 1, 2001); X, Y = np.meshgrid(G, G, indexing="ij")
dxW = a * X + b * Y + g / 2 * (Y**2 - 2 * X * Y)
dyW = a * Y + b * X + g / 2 * (2 * X * Y - X**2)
Lam = np.abs(dxW).max() + np.abs(dyW).max()
print("Lambda interior (grid):", Lam, " formula bound 2a+2b+3g =", 2 * a + 2 * b + 3 * g)
an = np.exp(gam[-1] / (2 * Lam * (k + 1)))
print(f"analytic transport base per variable with LP gap: {an:.5f}; with proved gap (k-1)g_inf - a q = {(k-1)*ginf - a*q:.5f}:"
      f" {np.exp(max((k-1)*ginf - a*q, 0) / (2 * Lam * (k + 1))):.5f} (Lambda=2.8), {np.exp(max((k-1)*ginf - a*q, 0) / (2 * 3.4 * (k + 1))):.5f} (Lambda=3.4)")
for kk in (7, 10, 20, 50, 200, 10**6):
    print(f"   proved analytic base, k={kk}: {np.exp(max((kk-1)*ginf - a*q, 0) / (2 * 2.8 * (kk + 1))):.5f} per variable (Lambda=2.8)")

# separable bound check on a grid: W(x,y) <= ((b+g)/2)(x^2+y^2) + (a/2)(x^2+y^2)
Wv = a / 2 * (X**2 + Y**2) + b * X * Y + g / 2 * (X * Y**2 - X**2 * Y)
print("separable bound slack min (should be >= 0):", float(((a + b + g) / 2 * (X**2 + Y**2) - Wv).min()))

# 3. computed bound
c = np.array([a + (b + g) / 2] + [a + b + g] * (k - 2) + [a + (b + g) / 2])
dd = np.linspace(0, 1, 20001)[1:]


def corner(mu, cj):
    return float(np.max((1 - dd) / 2 * np.exp(mu * cj * dd**2)))


def Phi(mu, start):
    th, gm = thetas[start:], gam[start:]
    terms = [np.exp(-mu * gm[-1])]
    terms += [(1 + th[i + 1]) / 2 * np.exp(-mu * max(gm[i], 0)) for i in range(len(th) - 1)]
    H = [max(1.0, corner(mu, cj)) for cj in c]
    Hp = [max((1 + th[0]) / 2, corner(mu, cj)) for cj in c]
    psi = max(Hp[j] * np.prod([H[i] for i in range(k) if i != j]) for j in range(k))
    terms.append(psi)
    return max(terms), terms


best = (np.inf, None)
for mu in np.linspace(1.0, 3.5, 251):
    for start in range(0, len(thetas) - 1):
        v, _ = Phi(mu, start)
        if v < best[0]:
            best = (v, (round(mu, 4), float(thetas[start])))
mu, th1 = best[1]
v, terms = Phi(mu, list(thetas).index(th1))
print(f"computed: Phi = {best[0]:.5f} at mu={mu}, theta1={th1}: per window {1/best[0]:.4f}, per variable {best[0]**(-1/(k+1)):.5f}")
print("   terms sorted:", sorted([round(float(t), 4) for t in terms], reverse=True)[:6], " Psi =", round(float(terms[-1]), 4))
v2, _ = Phi(2.112, 0)
print(f"   at the note's mu = 2.112 (theta1 = 0.2): Phi = {v2:.5f}")

# 4. leftover windows of length r < k at mu: transport bound needs 2 mu Lambda <= 1, which fails; use the corner/core bound
for r in range(1, k):
    gr = []
    for th in thetas:
        if r >= 2:
            cb = ClassBound(chiral_chain(r, b, g, ev), poly_tests(d), K=5)
            lo, up, it = cb.bound(np.full(r, -th), np.full(r, th), None, maxit=200, tol=1e-9)
            gr.append(-up)
        else:
            gr.append(0.0)
    gr = np.array(gr)
    cr = np.array([a] if r == 1 else [a + (b + g) / 2] + [a + b + g] * (r - 2) + [a + (b + g) / 2])
    H = [max(1.0, corner(mu, cj)) for cj in cr]
    Hp = [max((1 + thetas[0]) / 2, corner(mu, cj)) for cj in cr]
    psi = max(Hp[j] * np.prod([H[i] for i in range(r) if i != j]) for j in range(r))
    terms = [np.exp(-mu * gr[-1])] + [(1 + thetas[i + 1]) / 2 * np.exp(-mu * max(gr[i], 0)) for i in range(len(thetas) - 1)] + [psi]
    print(f"   leftover window r={r}: Phi_r({mu}) <= {max(terms):.4f}; max corner sup = {max(corner(mu, cj) for cj in cr):.4f}")

# 5. ceiling box of the note (k = 7, P2)
if k == 7:
    l = np.array([0.696, 0.838, 0.523, 0.455, 0.872, 0.264, 0.927]); u = np.ones(7)
    cb = ClassBound(chiral_chain(7, b, g, ev), poly_tests(d), K=5)
    lo, up, it = cb.bound(l, u, None, maxit=200, tol=1e-10)
    logvol = np.sum(np.log((u - l) / 2))
    print(f"ceiling box: V in [{lo:.5f}, {up:.5f}], mu0 = {-logvol/lo:.4f} -> ceiling per variable exp(mu0 gamma/(k+1)) = {np.exp(-logvol/lo*gam[-1]/(k+1)):.5f}")
    # local search for a smaller mu0 (lower ceiling); coordinate perturbation of the corner box, all-positive corner
    rng = np.random.default_rng(3)
    bestmu = -logvol / lo; bestl = l.copy()
    for it in range(150):
        cand = np.clip(bestl + rng.normal(scale=0.05, size=7), 0.05, 0.98)
        lo2, up2, _ = cb.bound(cand, u, None, maxit=80, tol=1e-8)
        if lo2 > 0:
            m2 = -np.sum(np.log((u - cand) / 2)) / lo2
            if m2 < bestmu:
                bestmu, bestl = m2, cand
    print(f"   local search: mu0 = {bestmu:.4f} at l = {np.round(bestl, 3).tolist()} -> ceiling per variable {np.exp(bestmu*gam[-1]/(k+1)):.5f}")
