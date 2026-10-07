"""W5 verifier checks for the limits group (exact arithmetic where possible).

1. (1+log2 t)^2 <= 4t for t >= 1 (used for f(p,t) <= 4 c0 (c1 p)^p t^{p/2+2}).
2. (I+2)^5 <= 3^5 I^5 for I >= 1 (C = 5 in Proposition prop:lbproduct).
3. Remark lim:rem:dk: for c = 2^k, ell = ceil(log2(2c)) = k+1, 5 ell + 2 = 5k+7,
   D = 2^ell = 2c and 20 ell D^2 = 80 (k+1) 4^k.
4. Proposition lim:prop:setgrowth(a): on random small grids of [0,1]^n,
   every min-marginal of Q = F - D satisfies m_j(v) <= -L_j w_j(v)^2/8
   (exhaustive minimisation, exact fractions).
"""
from fractions import Fraction as Fr
import itertools
import math
import random

# 1. Minimum of 2*2^{t/2} - 1 - t over t >= 0 is positive (sqrt form).
t_star = 2 * math.log2(1 / math.log(2))
val = 2 * 2 ** (t_star / 2) - 1 - t_star
assert val > 0.8, val
for t in [x / 100 for x in range(0, 4000)]:
    assert (1 + t) ** 2 <= 4 * 2 ** t
print("1 ok: min of 2*2^(t/2)-1-t is", round(val, 4))

# 2.
for I in range(1, 2000):
    assert (I + 2) ** 5 <= 3 ** 5 * I ** 5
print("2 ok")

# 3.
for k in range(2, 60):
    c = 2 ** k
    ell = (2 * c - 1).bit_length()  # ceil(log2(2c)) for 2c a power of two
    assert 2 ** ell >= 2 * c and 2 ** (ell - 1) < 2 * c
    assert ell == k + 1 and 5 * ell + 2 == 5 * k + 7
    D = 2 ** ell
    assert D == 2 * c and 20 * ell * D * D == 80 * (k + 1) * 4 ** k
print("3 ok")


# 4.
def check_setgrowth(n, grids):
    L = [Fr(2) if i in (0, n - 1) else Fr(4) for i in range(n)]

    def w(i, v):
        g = grids[i]
        idx = g.index(v)
        left = v - g[idx - 1] if idx > 0 else Fr(0)
        right = g[idx + 1] - v if idx + 1 < len(g) else Fr(0)
        return max(left, right)

    best = {}
    for x in itertools.product(*grids):
        F = sum((x[i] - x[i + 1]) ** 2 for i in range(n - 1))
        D = sum(L[i] * w(i, x[i]) ** 2 / 8 for i in range(n))
        Q = F - D
        for j in range(n):
            key = (j, x[j])
            if key not in best or Q < best[key]:
                best[key] = Q
    for (j, v), m in best.items():
        assert m <= -L[j] * w(j, v) ** 2 / 8, (grids, j, v, m)


random.seed(1)
count = 0
for n in (2, 3, 4):
    for _ in range(150 if n < 4 else 40):
        grids = []
        for i in range(n):
            k = random.randint(0, 4 if n < 4 else 3)
            inner = sorted({Fr(random.randint(1, 23), 24) for _ in range(k)})
            grids.append([Fr(0)] + inner + [Fr(1)])
        check_setgrowth(n, grids)
        count += 1
print("4 ok:", count, "grids")
print("PASS")
