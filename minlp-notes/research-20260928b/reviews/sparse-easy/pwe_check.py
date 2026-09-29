"""Remark 3.5: PWE root certificate max_{l notin S*}|a_l| <= m0 with the PWE ridge rho = lam = sqrt(n).
(1) per-entry noise sigma (PWE Sec. 3.1 model), fixed b/sigma = 2: replicate the note's 120-instance check.
(2) total-energy noise (per-entry sd gamma/sqrt n): exactness should switch on near n = 2(k + gamma^2/b^2) log p.
(3) noiseless model of Dong's experiments (k = ceil(sqrt p), n = alpha k log(p-k), rho = 2 sqrt n).
For p > 10^4 the null maximum is drawn from its exact conditional law: given (X_S, w) the null a_l/||r||
are iid N(0,1), so P(cert | X_S, w) = (1 - 2 Phibar(m0/||r||))^(p-k)."""
from common import ridge_on  # sets single-thread BLAS env before numpy loads
import numpy as np
from scipy.stats import norm

def one(n, p, k, lam, b, sd, seed, direct=True):
    rng = np.random.default_rng(seed)
    XS = rng.standard_normal((n, k)); w = rng.standard_normal(n)
    signs = rng.choice([-1.0, 1.0], k)
    y = XS @ (b * signs) + sd * w
    f, bS, r = ridge_on(XS, y, lam, np.arange(k))
    m0 = lam * np.min(np.abs(bS)); R = np.linalg.norm(r)
    if direct:
        Xn = rng.standard_normal((n, p - k))
        mx = np.max(np.abs(Xn.T @ r))
        return mx <= m0, mx / m0, (1 - 2 * norm.sf(m0 / R)) ** (p - k)
    return None, None, (1 - 2 * norm.sf(m0 / R)) ** (p - k)

def tau_lam2(n, k, lam, b, sd):
    bl = b * n / (n + lam); om2 = n * sd ** 2 + k * b ** 2 * lam ** 2 * n / (n + lam) ** 2
    return (lam * bl) ** 2 / om2

print("(1) per-entry noise, lam = sqrt n, b = 1, sigma = 0.5, k = 5, 20 seeds")
tot = 0; hits = 0
for p in (100, 1000, 10000):
    for alpha in (5, 20):
        k = 5; n = int(round(alpha * k * np.log(p))); lam = np.sqrt(n)
        res = [one(n, p, k, lam, 1.0, 0.5, 7000 + s) for s in range(20)]
        c = sum(r[0] for r in res); tot += 20; hits += c
        print(f"  p={p:6d} alpha={alpha:2d} n={n:5d}: cert {c}/20, median max|a|/m0 = {np.median([r[1] for r in res]):.2f}, "
              f"mean P(cert|X_S,w) = {np.mean([r[2] for r in res]):.2e}, tau_lam^2 = {tau_lam2(n, k, lam, 1, .5):.2f}, 2log p = {2*np.log(p):.2f}")
print(f"  total certificates: {hits}/{tot}")
print("  larger n at p = 1000 (alpha = 100, 400): the certificate stays off because tau_lam^2 <= b^2/sigma^2 = 4")
for alpha in (100, 400):
    k = 5; p = 1000; n = int(round(alpha * k * np.log(p))); lam = np.sqrt(n)
    res = [one(n, p, k, lam, 1.0, 0.5, 7100 + s, direct=False) for s in range(20)]
    print(f"    n={n}: mean P(cert|X_S,w) = {np.mean([r[2] for r in res]):.2e}, tau_lam^2={tau_lam2(n,k,lam,1,.5):.2f}")

print("\n(2) total-energy noise gamma = 1 (per-entry sd 1/sqrt n), lam = sqrt n, b = 1, k = 5; n = c * 2(k + gamma^2/b^2) log p")
for p in (1000, 10 ** 5, 10 ** 8):
    row = []
    for cfac in (0.5, 0.7, 0.85, 1.0, 1.2, 1.5):
        k = 5; n = int(round(cfac * 2 * (k + 1.0) * np.log(p))); lam = np.sqrt(n)
        res = [one(n, p, k, lam, 1.0, 1.0 / np.sqrt(n), 8000 + s, direct=False) for s in range(200)]
        row.append(f"c={cfac}: {np.mean([r[2] for r in res]):.2f}")
    print(f"  p={p:>9d}: P(root exact) " + ", ".join(row))

print("\n(3) noiseless, Dong's setup: k = ceil(sqrt p), n = alpha k log(p-k), rho = 2 sqrt n; 100 seeds")
for p in (64, 128, 256, 512):
    k = int(np.ceil(np.sqrt(p))); row = []
    for alpha in (1, 2, 3, 4, 5, 7):
        n = int(round(alpha * k * np.log(p - k))); lam = 2 * np.sqrt(n)
        res = [one(n, p, k, lam, 1.0, 0.0, 9000 + s, direct=True) for s in range(100)]
        row.append(f"a={alpha}: {np.mean([r[0] for r in res]):.2f}")
    print(f"  p={p:4d} k={k:2d}: " + ", ".join(row))
