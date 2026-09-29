"""Remark after Lemma 2: with the first block scaled by M, the admissible window is
n < gamma^2 <= n + min(8, M^2). Checked at the upper end and just above it."""
import random
import sys
from fractions import Fraction as F

from tools import normalize, violators_fp, zero_one_solutions, predicted

random.seed(19)


def G_scaled(a, s, M, g2, h2):
    n = len(a)
    N = n + 2
    G = [[F(0)] * N for _ in range(N)]
    G[0][0] = 4 * g2 + 4 * h2
    G[0][N - 1] = G[N - 1][0] = -2 * g2
    for i in range(n):
        for j in range(n):
            G[1 + i][1 + j] = F(M * M * a[i] * a[j] + 4 * (i == j))
        G[1 + i][N - 1] = G[N - 1][1 + i] = F(M * M * a[i] * s + 2)
    G[N - 1][N - 1] = F(M * M * s * s + n) + g2
    return G


inst = []
for _ in range(300):
    n = random.randint(1, 3)
    a = [random.randint(-3, 5) for _ in range(n)]
    s = random.randint(-3, 8)
    inst.append((a, s))

fails = 0
for M in (1, 2, 3, 4):
    top = min(8, M * M)
    for label, g2f, expect_ok in (("top", lambda n: F(n + top), True),
                                  ("above", lambda n: F(n + top) + F(1, 100), False)):
        bad = 0
        for a, s in inst:
            n = len(a)
            g2 = g2f(n)
            X = normalize(G_scaled(a, s, M, g2, g2))
            bad += violators_fp(X, zero_first=True) != predicted(zero_one_solutions([a], [s]))
        good = (bad == 0) if expect_ok else (bad > 0)
        fails += not good
        print(f"[M={M}, gamma^2 = n+{top}{' + 1/100' if not expect_ok else ''}] {len(inst)} instances: "
              f"{bad} mismatches ({'expected 0' if expect_ok else 'expected > 0'}) -> {'OK' if good else 'UNEXPECTED'}")
print("ALL OK" if fails == 0 else f"FAILURES: {fails}")
sys.exit(1 if fails else 0)
