"""Second round of exact checks for claims summarized in intro/conclusion.

1. Conclusion, open problem (2): ceil(log2(n+2))^p <= 2 p^p (n+2) for all
   n >= 1, p >= 1 (the form of eq:logabsorb with n in place of n_P).
   Checked exactly for p <= 14 and all n with ceil(log2(n+2)) <= 60, using
   that the left side depends on n only through b = ceil(log2(n+2)) and the
   right side is smallest at the least n with that b, n = 2^(b-1) - 1.
2. Intro, certificate paragraph (Prop. prop:cellwise(b)): the minimum over a
   product grid of F - sum_i L_i w_i(v)^2/8 equals the minimum over all cells
   of the vertex bound min_vert F - sum_i L_i w(J_i)^2/8, with effective
   width 0 for integer unit intervals. Random small mixed instances, exact
   rationals.
3. Intro, snapping sentence (Thm. thm:transfer, Rem. rem:setgrowth):
   log2(1/eps_S) <= log2(max{64 n^2 R^2, 2 Omega^2}) + max{0, log2(1/g_S)},
   so k = poly(I) + max{0, log2(1/g_S)} suffices; checked on a grid of values.
"""
from fractions import Fraction as Fr
import itertools, math, random

# 1
for p in range(1, 15):
    for b in range(2, 61):           # n >= 1 gives b = ceil(log2(n+2)) >= 2
        n_min = 2 ** (b - 1) - 1     # least n with ceil(log2(n+2)) = b
        if n_min < 1:
            n_min = 1
        assert (n_min + 1).bit_length() == b, (b, n_min)  # = ceil(log2(n_min+2))
        assert b ** p <= 2 * p ** p * (n_min + 2), (p, b)
print("1 ok: ceil(log2(n+2))^p <= 2 p^p (n+2)")

# 2
random.seed(7)

def quad(H, c, x):
    n = len(x)
    return sum(Fr(1, 2) * H[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) \
        + sum(c[i] * x[i] for i in range(n))

def eff_w(a, b, integer):
    return Fr(0) if (integer and b - a == 1) else b - a

trials = 0
for _ in range(300):
    n = random.choice([2, 3])
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = Fr(random.randint(-4, 4))
        for j in range(i + 1, n):
            H[i][j] = H[j][i] = Fr(random.randint(-4, 4))
    c = [Fr(random.randint(-5, 5)) for _ in range(n)]
    L = [max(H[i][i], Fr(0)) for i in range(n)]
    integer = [random.random() < 0.3 for _ in range(n)]
    grids = []
    for i in range(n):
        if integer[i]:
            pts = sorted(set([0, 4] + random.sample(range(1, 4), random.randint(0, 3))))
            grids.append([Fr(v) for v in pts])
        else:
            pts = sorted(set([Fr(0), Fr(1)] + [Fr(random.randint(1, 15), 16)
                                               for _ in range(random.randint(0, 3))]))
            grids.append(pts)
    ivs = [list(zip(g, g[1:])) for g in grids]
    wv = []
    for i in range(n):
        d = {}
        for a, b in ivs[i]:
            w = eff_w(a, b, integer[i])
            d[a] = max(d.get(a, Fr(0)), w)
            d[b] = max(d.get(b, Fr(0)), w)
        wv.append(d)
    beta = min(quad(H, c, y) - sum(L[i] * wv[i][y[i]] ** 2 / 8 for i in range(n))
               for y in itertools.product(*grids))
    cellmin = None
    for cell in itertools.product(*ivs):
        vb = min(quad(H, c, v) for v in itertools.product(*cell))
        bc = vb - sum(L[i] * eff_w(cell[i][0], cell[i][1], integer[i]) ** 2 / 8
                      for i in range(n))
        cellmin = bc if cellmin is None else min(cellmin, bc)
    assert beta == cellmin, (beta, cellmin)
    trials += 1
print(f"2 ok: corrected grid minimum = best cell vertex bound ({trials} instances)")

# 3
for n in [1, 3, 10]:
    for R in [Fr(1), Fr(7), Fr(10 ** 6)]:
        for Om in [Fr(1), Fr(5), Fr(10 ** 9)]:
            for gS in [Fr(1, 10 ** 12), Fr(1, 3), Fr(1), Fr(10 ** 8)]:
                epsS = min(gS / (64 * n * n * R * R), 1 / (2 * Om * Om))
                lhs = math.log2(1 / epsS)
                rhs = math.log2(max(64 * n * n * R * R, 2 * Om * Om)) \
                    + max(0.0, math.log2(1 / gS))
                assert lhs <= rhs + 1e-9, (n, R, Om, gS)
print("3 ok: log2(1/eps_S) <= log2 max{64n^2R^2, 2Omega^2} + max{0, log2(1/g_S)}")
