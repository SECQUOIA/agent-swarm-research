"""Exact checks of numeric claims summarized in intro/conclusion (front-verify).

1. f(p,k) = c0 (c1 p sqrt k)^p k (1+log2 k)^2 is increasing in k >= 1, so
   f(p, kbar) <= f(p, ceil(kbar))  (intro, "Parameterized form").
2. mu* = max{2, ceil(log4(8 kbar))} gives 2^mu* <= 6 sqrt(kbar), hence the
   cap K_mu = 10 * 2^mu * ceil(log2(n+2)) <= 60 sqrt(kbar) ceil(log2(n+2))
   for every trial mu <= mu* (Theorem 1.1(b): O(sqrt(kbar) log(n+2)) nodes).
3. Prop lbwidth constants: g = 1/(2n), L = 1/n, weighted constant 1/2 give
   kbar <= kappa <= 2 (Theorem 1.2(b)).
4. Point growth implies weighted growth with kbar <= kappa: for L > 0,
   gamma = g/L gives max{1,1/gamma} = max{1,L/g}.
5. Prop lim:prop:unique: kappa <= 4/g with g = lambda/(m(1+2(m-1)|a|^2)),
   lambda = 1/(m 2^(m+1)); check kappa <= 2^(m+3) m^2 (1+2m|a|^2) exactly.
"""
from fractions import Fraction as Fr
import math, itertools

def f(p, k, c0=1.0, c1=1.0):
    return c0 * (c1 * p * math.sqrt(k)) ** p * k * (1 + math.log2(k)) ** 2

# 1
for p in range(1, 8):
    ks = [1 + i / 50 for i in range(2000)]
    vals = [f(p, k) for k in ks]
    assert all(a < b for a, b in zip(vals, vals[1:])), p
print("1 ok: f increasing in kappa on [1,41)")

# 2 (exact: compare squares)
def mu_star(kb):
    mu = 2
    while Fr(4) ** mu < 8 * kb:   # ceil(log4(8 kb)) as least mu with 4^mu >= 8kb
        mu += 1
    return max(2, mu)
for num in range(1, 4000):
    kb = Fr(num, 7)
    if kb < 1:
        continue
    m = mu_star(kb)
    assert 8 * kb * Fr(1, 4 ** m) <= 1
    assert Fr(4) ** m <= 36 * kb, (kb, m)   # (2^mu)^2 <= 36 kbar
print("2 ok: 8 kbar theta^2 <= 1 and 2^mu* <= 6 sqrt(kbar)")

# 3
for n in range(1, 30):
    g = Fr(1, 2 * n); L = Fr(1, n)
    kappa = max(Fr(1), L / g); kbar = max(Fr(1), 1 / Fr(1, 2))
    assert kbar <= kappa <= 2
print("3 ok: lbwidth kbar <= kappa <= 2")

# 4
for L in [Fr(1, 3), Fr(2), Fr(7, 5)]:
    for g in [Fr(1, 9), Fr(1), Fr(5)]:
        gamma = g / L
        assert max(Fr(1), 1 / gamma) == max(Fr(1), L / g)
print("4 ok: kbar = kappa for gamma = g/L")

# 5
for m in range(2, 9):
    for a2 in [1, 2, 5, 100, 10**6]:
        lam = Fr(1, m * 2 ** (m + 1))
        g = lam / (m * (1 + 2 * (m - 1) * a2))
        kappa = max(Fr(1), 4 / g)
        assert kappa <= 2 ** (m + 3) * m * m * (1 + 2 * m * a2)
print("5 ok: unique-minimizer kappa bound")
