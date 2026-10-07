"""Verifier check (W3, optsets) for constants used in Section 9.3 / App. app:proximal
and in Proposition prop:twocenters.

1. Lemma lem:proximal(i): for PROX(khat) the graded grid of a box of radius
   varrho*h on each side of the center (the worst case; clipping only removes
   nodes) has at most K_theta = 8 theta^{-1} ceil(log2(n+2)) nodes, for
   khat in {1, 1.5, 2, 3, ..., 2^20} and n in a wide range. The node count per
   side is the least k with t_k >= R, t_k = h((1+theta)^k-1)/theta (exact
   recursion in fractions for small cases, closed form in floats otherwise).
2. The intermediate bound |G_i| <= 7 theta^{-1} ceil(log2(n+2)) of the proof.
3. eq:logabsorb with n in place of n_P: ceil(log2(n+2))^p <= 2 p^p (n+2).
4. K_theta^p <= 2(48 p sqrt(khat))^p (n+2) and 48 sqrt(2) < 68.
5. prop:twocenters arithmetic and stage-0 inequality.
Run: python3 -B optsets-verify-caps.py
"""
from fractions import Fraction as Fr
from math import ceil, log2, log, sqrt, isqrt

ok = True

def mu_of(khat):
    mu = 2
    while Fr(khat) / 4 ** mu > Fr(1, 8):
        mu += 1
    return mu

def ceil_sqrt(q):  # ceil(sqrt(q)) for a Fraction q >= 0
    r = isqrt(q.numerator // q.denominator) + 2
    while r > 0 and Fr((r - 1) ** 2) >= q:
        r -= 1
    return r

def side_nodes_exact(theta, rho):
    # nodes strictly on one side of the center for radius R = rho*h, mesh h = 1
    t, k = Fr(0), 0
    while t < rho:
        t = min(t + 1 + theta * t, Fr(rho)); k += 1
    return k

def side_nodes_float(theta, rho):
    # least k with ((1+theta)^k - 1)/theta >= rho
    k = ceil(log(1 + theta * rho) / log(1 + theta) - 1e-12)
    while ((1 + theta) ** k - 1) / theta < rho:
        k += 1
    while k > 0 and ((1 + theta) ** (k - 1) - 1) / theta >= rho:
        k -= 1
    return k

khats = [Fr(1), Fr(3, 2), Fr(2), Fr(3)] + [Fr(2) ** e for e in range(2, 21)] + [Fr(2) ** e - 1 for e in range(3, 21)]
ns = list(range(1, 65)) + [100, 127, 128, 255, 256, 1000, 1023, 1024, 4095, 10 ** 4, 10 ** 5, 10 ** 6]
worst = 0.0
for kh in khats:
    mu = mu_of(kh); theta = Fr(1, 2 ** mu)
    ok &= theta <= Fr(1, 4) and 8 * kh * theta ** 2 <= 1 and Fr(2 ** mu) ** 2 <= 36 * kh
    for n in ns:
        rho = 2 * ceil_sqrt(kh * n)
        if n <= 64 and kh <= 64:
            side = side_nodes_exact(theta, rho)
        else:
            side = side_nodes_float(float(theta), rho)
        nodes = 1 + 2 * side
        cl = ceil(log2(n + 2))
        Kth = 8 * 2 ** mu * cl
        ok &= nodes <= 7 * 2 ** mu * cl and nodes <= Kth
        worst = max(worst, nodes / Kth)
print("1-2. PROX node caps: max nodes/K_theta =", round(worst, 4), "(must be <= 7/8)")
ok &= worst <= 7 / 8

for p in range(1, 41):
    for n in list(range(1, 300)) + [10 ** k for k in range(3, 10)]:
        ok &= ceil(log2(n + 2)) ** p <= 2 * p ** p * (n + 2)
print("3. logabsorb with n: checked p<=40")
for kh in khats[:12]:
    mu = mu_of(kh)
    for p in (1, 2, 3, 5, 8):
        for n in (1, 2, 10, 1000, 10 ** 6):
            Kth = 8 * 2 ** mu * ceil(log2(n + 2))
            ok &= Kth ** p <= 2 * (48 * p * sqrt(float(kh))) ** p * (n + 2) * (1 + 1e-12)
ok &= 48 * sqrt(2) < 68
print("4. table bound and 48 sqrt2 < 68:", 48 * sqrt(2))

# 5. prop:twocenters arithmetic
ok &= Fr(23, 100) ** 2 / 20 > Fr(1, 379)
ok &= (Fr(1, 2) - Fr(9, 4) * Fr(1, 16)) * Fr(16, 25) == Fr(23, 100)
ok &= sqrt(20) + sqrt(379) < 24
# stage 0: M <= h < 2M gives h^2/20 < M^2/5 < M^2/4 and theta^2/379 < 1/4
ok &= Fr(4, 20) < Fr(1, 4) and Fr(1, 16) / 379 < Fr(1, 4)
# k = 1 case: M^2/16 >= theta^2 M^2/379 (theta<=1/4) and >= h^2/20 (h<=M)
ok &= Fr(1, 16) >= Fr(1, 16) / 379 and Fr(1, 16) >= Fr(1, 20)
# M/16 >= theta M/4 >= 0.23 theta M for theta <= 1/4
ok &= Fr(1, 4) * Fr(1, 4) <= Fr(1, 16) and Fr(1, 4) >= Fr(23, 100)
print("ALL PASS" if ok else "FAIL")
