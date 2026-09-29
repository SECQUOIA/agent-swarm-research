"""Sanity check: subset sum -> split-inequality separation reduction.

Builds the rational PSD matrix Y (Y_00 = 1) from a subset-sum instance and
brute-forces v in a box, comparing "exists v with v^T Y v + v^T Y e0 < 0"
with subset-sum solvability. Exact rational arithmetic. A box search is only
a sanity check; the reduction's correctness rests on the written argument.
"""
from fractions import Fraction as F
from itertools import product, combinations


def build(a, s, M=3, gamma=F(2)):
    n = len(a)
    m = n + 2  # coordinates: sum, n parity, extra
    cols = []
    for i in range(n):
        v = [F(0)] * m
        v[0] = F(M * a[i]); v[1 + i] = F(2)
        cols.append(v)
    g = [F(M * s)] + [F(1)] * n + [gamma]
    cols.append(g)
    tprime = [F(0)] * (n + 1) + [-gamma]          # t - g
    h = gamma                                      # 8 h^2 >= ||t'||^2
    b0 = [2 * x for x in tprime] + [2 * h]
    B = [b0] + [c + [F(0)] for c in cols]
    nrm = sum(x * x for x in b0)
    Y = [[sum(x * y for x, y in zip(B[i], B[j])) / nrm for j in range(len(B))]
         for i in range(len(B))]
    return Y


def violated(Y, R=3):
    N = len(Y)
    best = None
    for v in product(range(-R, R + 1), repeat=N):
        q = sum(v[i] * Y[i][j] * v[j] for i in range(N) for j in range(N))
        q += sum(v[i] * Y[i][0] for i in range(N))
        if best is None or q < best[0]:
            best = (q, v)
    return best


def subset_sum(a, s):
    return any(sum(c) == s for r in range(len(a) + 1) for c in combinations(a, r))


if __name__ == "__main__":
    a = [3, 5, 7]
    for s in [4, 8, 9, 10, 11, 13, 15, 16]:
        Y = build(a, s)
        assert Y[0][0] == 1
        q, v = violated(Y, R=2)
        print(f"s={s:2d} subset_sum={subset_sum(a, s)!s:5} min_q={float(q):+.4f} "
              f"violated={q < 0} v={v}")
