"""Exact arithmetic check of the correlation-face rounding inequalities.

Exhaust all equal-total marginal pairs on the quarter grid for m=1,2.
This supplements, and does not replace, the proof in the audit note.
"""

from collections import defaultdict
from fractions import Fraction as F
from itertools import product


def check(m, r_int, c_int):
    total_int = sum(r_int)
    if total_int == 0:
        return
    n = 2 * m
    r = [F(t, 4) for t in r_int]
    c = [F(t, 4) for t in c_int]
    total = F(total_int, 4)
    W = [[F(r_int[i] * c_int[j], 4 * total_int) for j in range(n)]
         for i in range(n)]
    D = 1 - sum(W[i][i] for i in range(n))
    B = sum(W[i][m + i] for i in range(m))
    g = m - total + (2 * m + 1) * B + (4 * m + 1) * D
    a = [int(t >= 2) for t in r_int]
    b = a.copy()
    for i in range(m):
        if a[i] + a[m + i] == 2:
            b[m + i] = 0
        elif a[i] + a[m + i] == 0:
            b[i] = 1
    u = sum(abs(r[i] - a[i]) for i in range(n))
    v = sum(abs(c[i] - a[i]) for i in range(n))
    h = sum(a[i] * a[m + i] for i in range(m))
    changes = sum(abs(a[i] - b[i]) for i in range(n))
    distance = sum(abs(W[i][j] - F(b[i] * b[j], m))
                   for i in range(n) for j in range(n))
    assert B + D <= g
    assert sum(abs(r[i] - c[i]) for i in range(n)) <= 2 * total * D
    assert u <= 6 * total * D
    assert v <= 8 * total * D
    assert h <= total * B + 8 * total * D
    assert changes <= 2 * total * B + 22 * total * D + abs(m - total)
    assert distance <= 4 * total * B + 58 * total * D + 5 * abs(m - total)
    assert distance <= (136 * m + 10) * g
    assert distance <= 28 * m * B + 156 * m * D + 5 * (m - total)


if __name__ == "__main__":
    for m in (1, 2):
        groups = defaultdict(list)
        for r in product(range(5), repeat=2 * m):
            groups[sum(r)].append(r)
        count = 0
        for vectors in groups.values():
            for r in vectors:
                for c in vectors:
                    check(m, r, c)
                    count += 1
        print(f"m={m}: all inequalities passed for {count} equal-total quarter-grid pairs")
