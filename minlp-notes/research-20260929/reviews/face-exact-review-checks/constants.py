"""Referee recomputation of the constants in theory-face-exact/face-exact-exponential.md.
Independent of bounds.py. Floating point.
Usage: python3 constants.py
"""
import math
import numpy as np
from scipy import optimize, integrate

D, b, eps, r = 2.0, 0.8, 1e-4, 1.0

# ---- Theorem 1 constants and Lemma 3.1 ----
F = lambda S: (1 + S) / (2 * S * S) - math.log(1 + 1 / S)
Smax = optimize.brentq(F, 1.01, 3.0, xtol=1e-15)
print(f"S_max={Smax:.6f} rho_max={Smax**2-1:.6f}  sign F on (S_max,3.56): {F(2.0):.3e} {F(3.5):.3e} {F(50):.3e}")
rho = D / (2 * b); S = math.sqrt(1 + rho); th = S / (1 + S); lam = (1 + S) / (2 * S * S)
print(f"rho={rho} S={S} theta={th} lambda={lam} 1/theta={1/th}")
for n in (4, 10, 16, 20):
    print(f"  T1 closed n={n}: {th**-n * math.exp(-lam*(1+eps/(b*r*r))):.3f}")
print(f"  factor at eps<=1e-4, r>=1/2: {math.exp(-lam*(1+1e-4/(b*0.25))):.4f};  r=sqrt(eps/b): {math.exp(-2*lam):.4f}")

# Lemma 3.1 exact check: max_s k(s) - k(s0) with a fine grid near 1 as well (log-spaced)
def k(s, rho):
    S = math.sqrt(1 + rho); lam = (1 + S) / (2 * S * S)
    return np.log1p(-s) + lam * (rho * s * s + 2 * s)
worst = -1
s = np.concatenate([np.linspace(0, 1, 400001)[:-1], 1 - np.logspace(-12, -1, 2000)])
for rh in np.linspace(1e-4, Smax**2 - 1, 800):
    S_ = math.sqrt(1 + rh); th_ = S_ / (1 + S_); lam_ = (1 + S_) / (2 * S_ * S_)
    worst = max(worst, np.max(k(s, rh)) - (math.log(th_) + lam_))
print(f"Lemma 3.1: max_s k(s) - k(s0) over rho in (0, rho_max]: {worst:.2e}")

# Theorem 1(b) Lagrangian optimum (base unchanged; constant)
def Psi_mc(mu, rho):
    res = optimize.minimize_scalar(lambda s: -(math.log1p(-s) + mu * (rho * s * s + 2 * s - 1)),
                                   bounds=(0, 1 - 1e-12), method="bounded", options={"xatol": 1e-14})
    grid = np.linspace(0, 1, 200001)[:-1]
    return max(-res.fun, np.max(np.log1p(-grid) + mu * (rho * grid**2 + 2 * grid - 1)))
for n in (4, 10, 20):
    best = min((n * Psi_mc(mu, rho) + mu * (1 + eps / (b * r * r)), mu) for mu in np.linspace(0.05, 2, 391))
    print(f"  T1(b) Lagrangian n={n}: {math.exp(-best[0]):.3f} (mu={best[1]:.3f})")
print(f"  T1(b) generic rho form n=10: {math.exp((10-1-eps/(b*r*r))/(rho+2)):.3f}")

# ---- Theorem 2 base: sup over (sigma, mu) of -Psi_J ----
def PsiJ(sig, mu):
    phi = lambda s: 2*b*sig*s + (b*(1-sig) + D/2)*s*s + (D*sig*sig/2)*(1-s)**2
    h = lambda s: math.log1p(-s) + mu * (phi(s) - b * sig)
    grid = np.linspace(0, 1, 100001)[:-1]
    vals = np.log1p(-grid) + mu * (2*b*sig*grid + (b*(1-sig)+D/2)*grid**2 + (D*sig*sig/2)*(1-grid)**2 - b*sig)
    i = int(np.argmax(vals))
    lo, hi = grid[max(i-1, 0)], grid[min(i+1, len(grid)-1)]
    res = optimize.minimize_scalar(lambda t: -h(t), bounds=(lo, hi), method="bounded", options={"xatol": 1e-14})
    return max(vals[i], -res.fun)
best = max((-PsiJ(sg, mu), sg, mu) for sg in np.linspace(0.05, 1, 96) for mu in np.linspace(0.1, 4, 157))
res = optimize.minimize(lambda p: PsiJ(min(max(p[0], 0), 1), max(p[1], 1e-6)), [best[1], best[2]], method="Nelder-Mead",
                        options={"xatol": 1e-8, "fatol": 1e-12})
print(f"Theorem 2 base: grid {math.exp(best[0]):.5f} at sigma={best[1]:.3f} mu={best[2]:.3f}; "
      f"refined {math.exp(-res.fun):.5f} at sigma={res.x[0]:.4f} mu={res.x[1]:.4f}")
sg, mu = res.x
for n in (4, 10, 20):
    print(f"  T2 n={n}: {math.exp(-n*PsiJ(sg, mu) - mu*(b*sg + eps/r**2)):.3f}")

# ---- Section 6: alphaBB constants and bases ----
af = lambda h2: (math.sqrt(h2 * h2 + 4 * b * b) - h2) / 4
print(f"alpha_f(h''=2)={af(2):.4f}  alpha_f(h''=0.8)={af(0.8):.4f}")
K = D / 2 + b
def Psi_abb(mu, a):
    grid = np.linspace(0, 1, 200001)[:-1]
    return np.max(np.log1p(-grid) + mu * (K * grid**2 - a * (1 - grid)**2))
for a1 in (af(2), af(0.8)):
    a = 2 * a1
    bestb = min((Psi_abb(mu, a), mu) for mu in np.linspace(0.01, 5, 500))
    lg = (D + math.sqrt(D * D - 4 * b * b)) / 2   # geometric mean of spectrum of D I + b A
    print(f"  alpha_f={a1:.4f}: center-volume base {math.exp(-bestb[0]):.4f} (mu={bestb[1]:.3f}); "
          f"Thm 3.1 base sqrt(4e a/(pi lam_geo)) = {math.sqrt(4*math.e*a/(math.pi*lg)):.4f} (lam_geo={lg:.4f}); "
          f"threshold pi/(4e)={math.pi/(4*math.e):.4f}")
# lam_geo by direct eigenvalues for n=400
A = np.diag(np.ones(399), 1); A = A + A.T
print(f"  lam_geo(2I+0.8A), n=400, direct: {math.exp(np.mean(np.log(np.linalg.eigvalsh(2*np.eye(400)+0.8*A)))):.4f}")

# ---- Proposition 5.3 base ----
lgM = (D - b) + math.sqrt((D - b)**2 - b * b)
Ak = np.diag(np.ones(399), 1); Ak = Ak + Ak.T
print(f"Prop 5.3: lam_geo(M) closed {lgM:.4f}, direct {math.exp(np.mean(np.log(np.linalg.eigvalsh(2*(D-b)*np.eye(400)-b*Ak)))):.4f}; "
      f"base per variable {(4*math.e*b/(math.pi*lgM))**0.25:.4f}")
# Prop 5.3 value at n=4 (k=2) by direct 2-D quadrature over the full square (not just the ellipsoid)
def slice_full(n, eps):
    k = n // 2
    M = 2*(D-b)*np.eye(k) - b*(np.diag(np.ones(k-1), 1) + np.diag(np.ones(k-1), -1))
    if k == 1:
        val = integrate.quad(lambda t: (M[0,0]*t*t/2 + eps)**(-0.5), -r, r, points=[0], limit=200)[0]
    elif k == 2:
        val = integrate.dblquad(lambda t2, t1: ((np.array([t1, t2]) @ M @ np.array([t1, t2]))/2 + eps)**(-1.0),
                                -r, r, -r, r, epsabs=1e-10, epsrel=1e-8)[0]
    return (k*b/math.pi**2)**(k/2) * val
print(f"  Prop 5.3 full-cube quadrature: n=2 eps=1e-4 {slice_full(2,1e-4):.3f}; n=4 eps=1e-4 {slice_full(4,1e-4):.3f}; n=2 eps=1e-2 {slice_full(2,1e-2):.3f}")

# ---- Proposition 5.5 per-variable factor ----
for kap in (0.0, 0.1):
    mu0 = 1 - kap - b
    print(f"Prop 5.5 per-variable factor kappa={kap}: {2*math.sqrt(2*math.pi*math.e)*(1+math.sqrt(b/(4*mu0))):.2f}")
