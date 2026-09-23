"""Exact regression for the Matsui preprint's small-p bound and its repair.

The general printed bound fails on the displayed counterexample. The retained
largest-fractional-index bound is tested on rational McCormick points; a
separate arithmetic check covers the large-parameter bracket used for hardness.
These finite checks supplement the manuscript's universal estimate.
"""
from fractions import Fraction as F
from random import Random


def gap(x, y, p):
    n = len(x)
    X = sum(p**(i + 1) * x[i] for i in range(n))
    Y = sum(p**(i + j + 2) * y[i][j] for i in range(n) for j in range(n))
    return Y - X * X


x = [F(1, 2)] * 5
y = [[F(1, 2) if i == j else F(0) for j in range(5)] for i in range(5)]
actual = gap(x, y, 2)
printed = 2**2 * F(1, 4) / 2 - 2 * 5**2
assert actual == -279 and printed == F(-99, 2) and actual < printed

rng = Random(317)
checked = 0
for _ in range(240):
    n = rng.randrange(2, 9)
    p = rng.randrange(1, 20)
    x = [F(rng.randrange(9), 8) for _ in range(n)]
    fractional = [i for i in range(n) if 0 < x[i] < 1]
    if not fractional:
        continue
    y = []
    for i in range(n):
        row = []
        for j in range(n):
            lo, hi = max(F(0), x[i] + x[j] - 1), min(x[i], x[j])
            value = x[i] if i == j else lo + F(rng.randrange(5), 4) * (hi - lo)
            assert 0 <= value <= 1
            if i != j:
                assert value <= x[i] and value <= x[j] and value >= x[i] + x[j] - 1
            row.append(value)
        y.append(row)
    k = max(fractional) + 1
    h = min(min(x[i], 1 - x[i]) for i in fractional)
    lower = p**(2*k - 1) * (p*h/2 - n*n)
    assert gap(x, y, p) >= lower
    checked += 1

for n in range(5, 13):
    # p=n^(n^4), h=n^(-3n^3), so p*h has this exact integer value.
    ph = n**(n**3 * (n - 3))
    assert ph >= n**3 and F(ph, 2) - n*n > 1

print(f"PASS: printed-bound counterexample, {checked} exact corrected-bound cases, and large-parameter brackets for n=5,...,12")
