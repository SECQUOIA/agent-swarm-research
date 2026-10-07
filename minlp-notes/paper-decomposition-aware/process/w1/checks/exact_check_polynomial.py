"""Polynomial-factor checks.

(1) Interval curvature certificate: for random rational polynomials of degree
    <= 4 in <= 3 variables on random rational boxes, the bound
    Lhat_i = sum over monomials of the upper end of the exact monomial range of
    d^2/dx_i^2 dominates d_ii F at every point of a rational sample grid, and
    each monomial range is exact (attained at sample/vertex points).
(2) Native-integer lattice rule: every integer-point value lies in Q0^{-1} Z;
    if beta <= F* and U - beta < 1/Q0 for a feasible U, then U = F*.
(3) x^3 - 6x on [1,2]: d2 in [6,12] (interval bound 12), growth g = 3 holds on
    samples, the stationarity equation 3x^2 = 6 has no rational root.
(4) x^4 on [-1,1]: ratio x^4/x^2 -> 0, no positive quadratic growth.
"""
import random
from fractions import Fraction as Fr
from itertools import product
from math import lcm

random.seed(3)


def ipow(lo, hi, k):
    if k == 0:
        return Fr(1), Fr(1)
    a, b = lo ** k, hi ** k
    if k % 2 == 1 or lo >= 0:
        return min(a, b), max(a, b)
    if hi <= 0:
        return min(a, b), max(a, b)
    return Fr(0), max(a, b)


def imul(I1, I2):
    p = [I1[0] * I2[0], I1[0] * I2[1], I1[1] * I2[0], I1[1] * I2[1]]
    return min(p), max(p)


def mono_range(alpha, box):
    I = (Fr(1), Fr(1))
    for k, (lo, hi) in zip(alpha, box):
        I = imul(I, ipow(lo, hi, k))
    return I


def d2_terms(poly, i):
    out = []
    for c, alpha in poly:
        if alpha[i] >= 2:
            beta = list(alpha)
            beta[i] -= 2
            out.append((c * alpha[i] * (alpha[i] - 1), tuple(beta)))
    return out


def evalp(poly, x):
    total = Fr(0)
    for c, alpha in poly:
        t = c
        for v, k in zip(x, alpha):
            t *= v ** k
        total += t
    return total


def lhat(poly, i, box):
    tot = Fr(0)
    for c, beta in d2_terms(poly, i):
        lo, hi = mono_range(beta, box)
        tot += c * hi if c > 0 else c * lo
    return tot


def rand_poly(n, d):
    terms = {}
    for _ in range(random.randint(2, 7)):
        alpha = [0] * n
        deg = random.randint(0, d)
        for _ in range(deg):
            alpha[random.randrange(n)] += 1
        terms[tuple(alpha)] = terms.get(tuple(alpha), Fr(0)) + Fr(random.randint(-9, 9), random.choice([1, 2, 3, 5]))
    return [(c, a) for a, c in terms.items() if c != 0]


cnt = 0
for _ in range(300):
    n = random.randint(1, 3)
    poly = rand_poly(n, 4)
    box = []
    for _ in range(n):
        lo = Fr(random.randint(-6, 3), random.choice([1, 2, 3]))
        box.append((lo, lo + Fr(random.randint(1, 6), random.choice([1, 2]))))
    pts = [[lo + (hi - lo) * Fr(k, 4) for k in range(5)] for lo, hi in box]
    for i in range(n):
        L = lhat(poly, i, box)
        d2 = d2_terms(poly, i)
        for x in product(*pts):
            assert evalp(d2, x) <= L
            cnt += 1
        # exactness of each single-monomial range (attained on the sample grid,
        # which contains vertices and 0 when 0 is a quarter point is not
        # guaranteed, so check attainment at vertices or 0-crossings)
        for c, beta in d2:
            lo, hi = mono_range(beta, box)
            cand = [[lo_, hi_] + ([Fr(0)] if lo_ < 0 < hi_ else []) for lo_, hi_ in box]
            vals = [evalp([(Fr(1), beta)], x) for x in product(*cand)]
            assert min(vals) == lo and max(vals) == hi
print("curvature samples checked:", cnt)

# (2) native integer lattice rule
cnt2 = 0
for _ in range(200):
    n = random.randint(1, 3)
    poly = rand_poly(n, 4)
    box = [(random.randint(-3, 0), random.randint(1, 3)) for _ in range(n)]
    Q0 = lcm(*[c.denominator for c, _ in poly])
    vals = [evalp(poly, x) for x in product(*[range(l, u + 1) for l, u in box])]
    assert all((Q0 * v).denominator == 1 for v in vals)
    Fs = min(vals)
    for v in vals:
        for beta in (Fs, Fs - Fr(1, 2 * Q0), Fs - Fr(1, Q0) + Fr(1, 10 ** 6)):
            if v - beta < Fr(1, Q0):
                assert v == Fs
                cnt2 += 1
print("lattice-rule acceptances checked:", cnt2)

# (3) x^3 - 6x on [1,2]
p3 = [(Fr(1), (3,)), (Fr(-6), (1,))]
assert lhat(p3, 0, [(Fr(1), Fr(2))]) == 12
class Q2:
    """a + b sqrt2 with rational a, b."""
    def __init__(self, a, b=0):
        self.a, self.b = Fr(a), Fr(b)
    def __add__(self, o):
        o = o if isinstance(o, Q2) else Q2(o)
        return Q2(self.a + o.a, self.b + o.b)
    __radd__ = __add__
    def __sub__(self, o):
        o = o if isinstance(o, Q2) else Q2(o)
        return Q2(self.a - o.a, self.b - o.b)
    def __mul__(self, o):
        o = o if isinstance(o, Q2) else Q2(o)
        return Q2(self.a * o.a + 2 * self.b * o.b, self.a * o.b + self.b * o.a)
    __rmul__ = __mul__
    def __eq__(self, o):
        o = o if isinstance(o, Q2) else Q2(o)
        return self.a == o.a and self.b == o.b


r = Q2(0, 1)
Fstar = r * r * r - 6 * r          # = -4 sqrt2
assert Fstar == Q2(0, -4)
for k in range(0, 101):
    x = Q2(1 + Fr(k, 100))
    lhs = x * x * x - 6 * x - Fstar
    rhs = (x - r) * (x - r) * (x + 2 * r)
    assert lhs == rhs
print("x^3-6x: Lhat = 12, F* = -4 sqrt2, identity F-F* = (x-sqrt2)^2 (x+2 sqrt2) verified;"
      " so g = 1 + 2 sqrt2 >= 3 on [1,2]")
# no rational root of 3x^2 = 6: x^2 = 2 has no rational solution (classical)

# (4) x^4: ratio x^2 at x -> 0
print("x^4 growth ratios:", [float(Fr(1, 10 ** k) ** 2) for k in (1, 2, 3)])
