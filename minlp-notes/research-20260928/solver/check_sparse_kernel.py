"""Targeted exact-arithmetic checks for sparse-kernel-rounding.md.

This does not prove the infinite family, interval positivity, or SDP duality.
It checks the explicit kernel arithmetic, damping bounds, and unequal local
separator measures whose smoothed densities agree exactly.
"""

from fractions import Fraction as F
from math import comb


def kernel_coefficients(m):
    b = {j: m - abs(j) for j in range(-m + 1, m)}
    a = [sum(b[j] * b.get(j - k, 0) for j in b) for k in range(2 * m - 1)]
    return a, [F(v, a[0]) for v in a]


def chebyshev(k, x):
    a, b = F(1), x
    if k == 0:
        return a
    for _ in range(1, k):
        a, b = b, 2 * x * b - a
    return b


def matched_measures(order):
    # The (order+1)st finite difference annihilates degree <= order.
    n = order + 1
    plus, minus = [], []
    for j in range(n + 1):
        atom = (F(-1) + F(2 * j, n), F(comb(n, j), 2 ** (n - 1)))
        (plus if j % 2 == 0 else minus).append(atom)
    return plus, minus


def moment(measure, degree):
    return sum(weight * chebyshev(degree, x) for x, weight in measure)


def kernel_value(g, x, y):
    return 1 + 2 * sum(g[k] * chebyshev(k, x) * chebyshev(k, y)
                       for k in range(1, len(g)))


kernel_tests = 0
for m in range(2, 25):
    a, g = kernel_coefficients(m)
    assert a[0] == F(2 * m**3 + m, 3)
    assert a[0] - a[1] == m
    for k in range(8 * m):
        damping = g[k] if k < len(g) else F(0)
        assert 0 <= damping <= 1
        assert 1 - damping <= F(3 * k * k, 2 * m * m + 1)
        kernel_tests += 1
    for x in (F(-1), F(-3, 4), F(0), F(1, 3), F(1)):
        for y in (F(-1), F(-2, 3), F(0), F(2, 5), F(1)):
            assert kernel_value(g, x, y) >= 0
            kernel_tests += 1

separator_tests = 0
for r in range(2, 9):
    m = r // 2 + 1  # width two
    _, g = kernel_coefficients(m)
    plus, minus = matched_measures(2 * r)
    assert sum(p for _, p in plus) == sum(p for _, p in minus) == 1
    assert moment(plus, 2 * r + 1) != moment(minus, 2 * r + 1)
    for k in range(2 * r + 1):
        assert moment(plus, k) == moment(minus, k)
        separator_tests += 1
    # Separator density Chebyshev coefficients from both bags are identical.
    left = [moment(plus, 0)] + [2 * g[k] * moment(plus, k)
                                        for k in range(1, len(g))]
    right = [moment(minus, 0)] + [2 * g[k] * moment(minus, k)
                                          for k in range(1, len(g))]
    assert left == right
    # Bags have local records (leaf,separator)=(y²,y) and (y,-y).
    # Exact positivity at test points is a check of complete bag densities.
    for u in (F(-1), F(0), F(1, 2), F(1)):
        for v in (F(-1), F(-1, 3), F(0), F(1)):
            h_left = sum(p * kernel_value(g, y*y, u) * kernel_value(g, y, v)
                         for y, p in plus)
            h_right = sum(p * kernel_value(g, y, u) * kernel_value(g, -y, v)
                          for y, p in minus)
            assert h_left >= 0 and h_right >= 0
            separator_tests += 1

# An explicit degree-parity warning: PSD M has eigenvalues 0,3/2,3/2,
# local box generators have expectation zero, but (1-x)(1-y) is negative.
M = [[F(1), F(1, 2), F(1, 2)],
     [F(1, 2), F(1), F(-1, 2)],
     [F(1, 2), F(-1, 2), F(1)]]
assert all(M[i][i] >= 0 for i in range(3))
assert all(M[i][i] * M[j][j] - M[i][j]**2 >= 0
           for i in range(3) for j in range(i))
det = sum(M[0][j] * (M[1][(j+1)%3] * M[2][(j+2)%3]
                     - M[1][(j+2)%3] * M[2][(j+1)%3]) for j in range(3))
assert det == 0
assert 1 - M[0][1] - M[0][2] + M[1][2] == F(-1, 2)

print(f"PASS: {kernel_tests} rational kernel checks; "
      f"{separator_tests} separator/density checks; parity counterexample.")
