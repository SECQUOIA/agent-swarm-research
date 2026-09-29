"""Exact checks of the elementary lemmas behind the R-DDM Hessian criterion.

L0: for integers d_i, d_j and a_k = sgn(d_k) floor(|d_k|/2), b_k = d_k - a_k,
    (a_i + s a_j)(b_i + s b_j) >= 0 for s = +1, -1.
L1: mu(p, q) = p + a and mu(q, p) = p + b with a, b as above (Tamura-Tsurumi
    directed midpoints).
L2: for random rational DD+ matrices H and all d in {-3..3}^n, a^T H b >= 0.
L3: DD+ is preserved by one-step Gaussian elimination (Schur complement),
    exact rational arithmetic, random instances.
"""
import itertools
import random
from fractions import Fraction as Fr
from dcheck import mu


def ab(d):
    a = tuple((1 if x > 0 else -1) * (abs(x) // 2) for x in d)
    return a, tuple(x - y for x, y in zip(d, a))


# L0
R = 60
for di in range(-R, R + 1):
    for dj in range(-R, R + 1):
        (ai, aj), (bi, bj) = ab((di, dj))
        for s in (1, -1):
            assert (ai + s * aj) * (bi + s * bj) >= 0, (di, dj, s)
print("L0 ok for |d| <=", R)

# L1
for n in (1, 2, 3):
    for p in itertools.product(range(-3, 4), repeat=n):
        for q in itertools.product(range(-3, 4), repeat=n):
            d = tuple(y - x for x, y in zip(p, q))
            a, b = ab(d)
            assert mu(p, q) == tuple(x + y for x, y in zip(p, a))
            assert mu(q, p) == tuple(x + y for x, y in zip(p, b))
print("L1 ok")


def rand_dd(n):
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            H[i][j] = H[j][i] = Fr(random.randint(-9, 9), random.randint(1, 5))
    for i in range(n):
        H[i][i] = sum(abs(H[i][j]) for j in range(n) if j != i) + Fr(random.randint(0, 3), random.randint(1, 3))
    return H


def is_dd(H):
    n = len(H)
    return all(H[i][i] >= sum(abs(H[i][j]) for j in range(n) if j != i) for i in range(n))


random.seed(1)
for n in (2, 3, 4):
    for _ in range(200):
        H = rand_dd(n)
        for d in itertools.product(range(-3, 4), repeat=n):
            a, b = ab(d)
            val = sum(a[i] * H[i][j] * b[j] for i in range(n) for j in range(n))
            assert val >= 0
print("L2 ok")

for n in (2, 3, 4, 5, 6):
    for _ in range(500):
        H = rand_dd(n)
        k = random.randrange(n)
        if H[k][k] == 0:
            continue
        idx = [i for i in range(n) if i != k]
        S = [[H[i][j] - H[i][k] * H[k][j] / H[k][k] for j in idx] for i in idx]
        assert is_dd(S)
print("L3 ok")
