"""Reviewer r1: independent exact checks of Lemma A, Lemma B, Prop. C(c) and
Prop. D of note.md section 4 (no stream code imported).
Usage: python3 reviews/r1-code/r1_props.py"""
import itertools
import math
import random
from fractions import Fraction as F

random.seed(20261003)


def q(Y, v):
    N = len(v)
    return sum(v[i] * Y[i][j] * v[j] for i in range(N) for j in range(N)) + sum(v[i] * Y[i][0] for i in range(N))


def rand_psd(N, r):
    B = [[F(random.randint(-4, 4), random.randint(1, 3)) for _ in range(N)] for _ in range(r)]
    Y = [[sum(B[k][i] * B[k][j] for k in range(r)) for j in range(N)] for i in range(N)]
    if Y[0][0] == 0:
        return None
    return [[e / Y[0][0] for e in row] for row in Y]


def frac(t):
    return t - math.floor(t)


# Lemma A: max over v0 of -q equals phi(t) - w^T S w, with the argmax v0 = -ceil(t) (u = {t}-1) if t not integer
badA = 0; nA = 0
for _ in range(400):
    N = random.randint(2, 5); Y = rand_psd(N, random.randint(1, N))
    if Y is None:
        continue
    w = [random.randint(-3, 3) for _ in range(N - 1)]
    x = [Y[0][i] for i in range(1, N)]
    t = sum(a * b for a, b in zip(w, x))
    S = [[Y[i][j] - Y[0][i] * Y[0][j] for j in range(1, N)] for i in range(1, N)]
    wSw = sum(w[i] * S[i][j] * w[j] for i in range(N - 1) for j in range(N - 1))
    best = max(-q(Y, [v0] + w) for v0 in range(-40, 41))
    pred = frac(t) * (1 - frac(t)) - wSw
    nA += 1; badA += best != pred
    if t != math.floor(t):
        badA += -q(Y, [-math.ceil(t)] + w) != pred
print(f"Lemma A: {nA} cases, {badA} failures")

# Lemma B identity and nonnegativity, on random symmetric Y with Y00 = 1
badB = 0
for _ in range(500):
    N = random.randint(2, 5)
    Y = [[F(0)] * N for _ in range(N)]
    for i in range(N):
        for j in range(i, N):
            Y[i][j] = Y[j][i] = F(random.randint(-9, 9), random.randint(1, 7))
    Y[0][0] = F(1)
    wp = [random.randint(-3, 3) for _ in range(N - 1)]
    k = random.randint(2, 6); s = random.randint(-25, 25)
    t = math.floor(F(2 * s + 1 - k, 2 * k))
    b = F((2 * s + 1) * k - (2 * t + 1) * k * k, 2); a = k * k - b
    c = (k * (t + 1) - s) * (k * (t + 1) - s - 1)
    lhs = q(Y, [-s - 1] + [k * e for e in wp])
    rhs = a * q(Y, [-t - 1] + wp) + b * q(Y, [-t - 2] + wp) + c
    badB += lhs != rhs or a < 0 or b < 0 or c < 0
print(f"Lemma B: 500 cases, {badB} failures")

# Prop C(c): x1 = 1 - 1/D; is w = a e1 (a = floor(D/2)) non-primitive?  max violation
for D in range(2, 9):
    a = D // 2
    x = F(D - 1, D)
    Y = [[F(1), x], [x, x * x]]
    viol_a = -q(Y, [-a, a]); viol_el = -q(Y, [-1, 1])
    mx = max(-q(Y, [v0, w]) for v0 in range(-20, 21) for w in range(-20, 21))
    print(f"Prop C(c) D={D}: a={a} ({'non-primitive' if a >= 2 else 'PRIMITIVE'}), viol(a e1)={viol_a}, "
          f"floor(D^2/4)/D^2={F(D * D // 4, D * D)}, max over box={mx}, elementary={viol_el}, "
          f"normalized a e1={viol_a / (a * a)} vs elementary {viol_el}")

# Prop D: exhaustive for small subset-sum instances, family {0,1}^{n+2}; also signed family {-1,0,1}^{n+2}
badD = 0; badDs = 0; cnt = 0
for n in range(1, 5):
    for aa in itertools.product(range(1, 5), repeat=n):
        for T in range(1, sum(aa) + 2):
            x = [F(-12 * ai, 5) for ai in aa] + [F(12 * T - 2, 5)]
            Y = [[F(1)] + x] + [[xi] + [xi * xj for xj in x] for xi in x]
            solv = any(sum(c) == T for k in range(n + 1) for c in itertools.combinations(aa, k))
            viol = any(q(Y, v) < 0 for v in itertools.product((0, 1), repeat=n + 2))
            cnt += 1; badD += viol != solv
            if n <= 3:
                signed = any(sum(e * ai for e, ai in zip(eps, aa)) == T for eps in itertools.product((-1, 0, 1), repeat=n))
                viols = any(q(Y, v) < 0 for v in itertools.product((-1, 0, 1), repeat=n + 2))
                badDs += viols != signed
print(f"Prop D: {cnt} instances, {badD} mismatches for {{0,1}}; signed box {{-1,0,1}} vs signed subset sum (n<=3): {badDs} mismatches")
