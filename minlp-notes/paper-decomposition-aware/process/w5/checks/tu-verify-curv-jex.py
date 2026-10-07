"""W5 verifier checks for group tu (constraints.tex, appendix-tu.tex).

1. rem:tu-curv(i): for random polynomials in continuous x and discrete z,
   b_{ii'} (monomial ranges on [l,u] x prod [min Z_k, max Z_k]) bounds
   |d_{ii'}F| exactly at random rational points, and max_i sum_i' b_{ii'}
   bounds the largest eigenvalue of the x-Hessian (numerically, with margin).
2. rem:tu-curv(ii): projector row-sum bound >= max Rayleigh quotient on ker C.
3. thm:tu-exact(c): the first level j with E_j <= min{g_S tau^2/(4 n_c),
   1/(2 Omega^2)} is at most J_ex (exact rationals; sqrt handled by squaring).
4. thm:tu-states(b): an interval of length 2a+2h contains at most
   floor(4a/h)+5 points of (h/2)Z.
"""
import itertools
import math
import random
from fractions import Fraction as Fr

import numpy as np

random.seed(20261003)


def mono_range(alpha, box):
    lo, hi = Fr(1), Fr(1)
    for a, (l, u) in zip(alpha, box):
        if a == 0:
            continue
        vals = [l**a, u**a]
        if a % 2 == 0 and l < 0 < u:
            vals.append(Fr(0))
        rlo, rhi = min(vals), max(vals)
        prods = [lo * rlo, lo * rhi, hi * rlo, hi * rhi]
        lo, hi = min(prods), max(prods)
    return lo, hi


def deriv(poly, k):
    out = {}
    for alpha, c in poly.items():
        if alpha[k] == 0:
            continue
        beta = list(alpha)
        beta[k] -= 1
        out[tuple(beta)] = out.get(tuple(beta), 0) + c * alpha[k]
    return out


def evalp(poly, v):
    s = Fr(0)
    for alpha, c in poly.items():
        t = Fr(c)
        for a, x in zip(alpha, v):
            t *= x**a
        s += t
    return s


def rand_fr(lo, hi):
    return lo + (hi - lo) * Fr(random.randint(0, 1000), 1000)


fails = 0
# 1. polynomial curvature certificate
for trial in range(80):
    nc, nd = random.randint(1, 3), random.randint(0, 2)
    n = nc + nd
    deg = random.randint(2, 4)
    poly = {}
    for _ in range(random.randint(2, 7)):
        alpha = [0] * n
        for _ in range(random.randint(0, deg)):
            alpha[random.randrange(n)] += 1
        poly[tuple(alpha)] = Fr(random.randint(-9, 9), random.randint(1, 4))
    box = []
    for i in range(nc):
        l = Fr(random.randint(-4, 2), random.randint(1, 3))
        box.append((l, l + Fr(random.randint(1, 6), random.randint(1, 3))))
    Z = [sorted(random.sample(range(-3, 4), random.randint(1, 3))) for _ in range(nd)]
    for zk in Z:
        box.append((Fr(min(zk)), Fr(max(zk))))
    hess = [[deriv(deriv(poly, i), ip) for ip in range(nc)] for i in range(nc)]
    b = [[sum(abs(c) * max(abs(x) for x in mono_range(a, box)) for a, c in hess[i][ip].items())
          for ip in range(nc)] for i in range(nc)]
    Lbar = max(sum(row) for row in b)
    for _ in range(30):
        x = [rand_fr(*box[i]) for i in range(nc)]
        z = [Fr(random.choice(zk)) for zk in Z]
        v = x + z
        Hv = [[evalp(hess[i][ip], v) for ip in range(nc)] for i in range(nc)]
        if any(abs(Hv[i][ip]) > b[i][ip] for i in range(nc) for ip in range(nc)):
            fails += 1
            print("FAIL entry bound", trial)
        lam = max(np.linalg.eigvalsh(np.array([[float(e) for e in r] for r in Hv])))
        if lam > float(Lbar) + 1e-9:
            fails += 1
            print("FAIL eigen bound", trial, lam, float(Lbar))
    # quadratic case: b equals |H|
    if deg == 2 and all(sum(alpha) <= 2 for alpha in poly):
        for i, ip in itertools.product(range(nc), range(nc)):
            const = hess[i][ip].get(tuple([0] * n), Fr(0))
            if b[i][ip] != abs(const):
                fails += 1
                print("FAIL quadratic b != |H|", trial)
print("1. polynomial curvature certificate: done")

# 2. projector row-sum test on ker C
for trial in range(200):
    nc = random.randint(2, 5)
    M = np.random.default_rng(trial).integers(-5, 6, size=(nc, nc)).astype(float)
    H = M + M.T
    rows = random.randint(1, nc - 1)
    C = np.random.default_rng(1000 + trial).integers(-1, 2, size=(rows, nc)).astype(float)
    if np.linalg.matrix_rank(C) < rows:
        continue
    P = np.eye(nc) - C.T @ np.linalg.solve(C @ C.T, C)
    bound = max(np.abs(P @ H @ P).sum(axis=1))
    # orthonormal basis of ker C
    _, s, Vt = np.linalg.svd(C)
    Xi = Vt[rows:].T
    lam = max(np.linalg.eigvalsh(Xi.T @ H @ Xi))
    if lam > bound + 1e-9:
        fails += 1
        print("FAIL projector bound", trial)
print("2. projector row-sum bound: done")


def ceil_log2(q):
    """Smallest integer k with 2^k >= q, for a positive rational q."""
    k = 0
    while Fr(2)**k < q:
        k += 1
    while k > -200 and Fr(2)**(k - 1) >= q:
        k -= 1
    return k


# 3. J_ex in thm:tu-exact(c); kappa_c chosen as a rational square so that
#    sqrt is exact, and L/g_S <= kappa_c.
for trial in range(400):
    eta = Fr(random.randint(1, 8), random.randint(1, 8))
    nc = random.randint(1, 30)
    Lbar = Fr(random.randint(1, 50), random.randint(1, 9))
    if trial % 4 == 0:
        # kappa_c = 1 with g_S > Lbar
        gS = Lbar * Fr(random.randint(10, 30), 10)
    else:
        sk = Fr(random.randint(4, 40), 4)
        gS = Lbar / (sk * sk)
    kappa = max(Fr(1), Lbar / gS)
    assert kappa == 1 or (kappa.numerator**0.5).is_integer()
    tau = Fr(1, random.randint(4, 4000))
    Omega = random.randint(1, 10**4)
    target = min(gS * tau**2 / (4 * nc), Fr(1, 2 * Omega**2))
    j = 0
    while nc * Lbar * (eta / 2**j)**2 / 8 > target:
        j += 1
    # J_ex terms: ceil(log2(eta nc sqrt(kappa)/tau)), ceil(log2(eta Omega sqrt(nc Lbar)))
    # 2^k >= sqrt(q) iff 4^k >= q
    q1 = (eta * nc / tau)**2 * kappa
    q2 = (eta * Omega)**2 * nc * Lbar
    k1 = 0
    while Fr(4)**k1 < q1:
        k1 += 1
    k2 = 0
    while Fr(4)**k2 < q2:
        k2 += 1
    Jex = max(0, k1, k2)
    if j > Jex:
        fails += 1
        print("FAIL J_ex", trial, j, Jex)
print("3. J_ex bound: done")

# 4. counting in thm:tu-states(b)
for trial in range(2000):
    h = Fr(1, 2**random.randint(0, 6))
    a = Fr(random.randint(0, 400), random.randint(1, 40))
    c = Fr(random.randint(-500, 500), random.randint(1, 50))
    lo, hi = c - a - h, c + a + h
    step = h / 2
    k_lo = math.ceil(lo / step)
    k_hi = math.floor(hi / step)
    cnt = max(0, k_hi - k_lo + 1)
    if cnt > math.floor(4 * a / h) + 5:
        fails += 1
        print("FAIL count", trial)
print("4. node count: done")

print("ALL PASS" if fails == 0 else f"FAILURES: {fails}")
