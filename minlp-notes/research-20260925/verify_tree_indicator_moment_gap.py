"""Exact algebra checks for the three-vertex indicator moment-gap review."""

from itertools import product

import sympy as sp


Q = sp.Matrix([[3, 1, 1], [1, 1, 0], [1, 0, 1]])
x = sp.Matrix([0, 1, 0])
half = sp.Rational(1, 2)
third = sp.Rational(1, 3)
a = sp.sqrt(3) / 3
p = sp.symbols("p", real=True)
p_star = sp.sqrt(3) - sp.Rational(3, 2)
u = sp.Matrix([1, 1 + a, 0])


def embedded_inverse(pattern):
    support = [j for j, selected in enumerate(pattern) if selected]
    result = sp.zeros(3)
    if support:
        inverse = Q.extract(support, support).inv()
        for j, row in enumerate(support):
            for k, column in enumerate(support):
                result[row, column] = inverse[j, k]
    return result


def scalar_equal(left, right):
    assert sp.simplify(left - right) == 0, (left, right)


assert [Q[:j, :j].det() for j in range(1, 4)] == [3, 2, 1]

# Check the claimed affine inequality on every support, including z0 = 0.
for pattern in product([0, 1], repeat=3):
    H = embedded_inverse(pattern)
    conjugate = (u.T * H * u)[0]
    z0, z1, z2 = pattern
    majorant = sp.Rational(1, 6) * (1 + z0 + z2)
    majorant += (sp.Rational(7, 6) + 2 * a) * z1
    difference = sp.simplify(majorant - conjugate)
    assert difference.is_nonnegative, (pattern, difference)
    if z0 == 1:
        assert difference == 0

patterns = [(1, 0, 0), (1, 1, 0), (1, 0, 1), (1, 1, 1)]
weights = [p, half - p, half - p, p]
W = sp.zeros(3)
for pattern, weight in zip(patterns, weights):
    W += weight * embedded_inverse(pattern)
claimed_W = sp.Matrix(
    [
        [p / 3 + half, -p / 2 - sp.Rational(1, 4), -p / 2 - sp.Rational(1, 4)],
        [-p / 2 - sp.Rational(1, 4), p / 2 + sp.Rational(3, 4), p],
        [-p / 2 - sp.Rational(1, 4), p, p / 2 + sp.Rational(3, 4)],
    ]
)
assert sp.simplify(W - claimed_W) == sp.zeros(3)
f = (x.T * W.inv() * x)[0]
claimed_f = (4 * p**2 - 12 * p - 15) / (3 * (2 * p - 3) * (2 * p + 1))
scalar_equal(f, claimed_f)
scalar_equal(W.det(), -(2 * p - 3) * (2 * p + 1) / 16)
scalar_equal(
    sp.diff(f, p),
    8 * (4 * p**2 + 12 * p - 3) / (3 * (2 * p - 3) ** 2 * (2 * p + 1) ** 2),
)
scalar_equal(f.subs(p, p_star), 1 + a)
scalar_equal(f.subs(p, 0), sp.Rational(5, 3))
scalar_equal(f.subs(p, half), sp.Rational(5, 3))

# Independently verify a four-point original-set convex combination.
mean_x = sp.zeros(3, 1)
mean_z = sp.zeros(3, 1)
mean_cost = sp.Integer(0)
for pattern, weight in zip(patterns, weights):
    probability = weight.subs(p, p_star)
    assert probability.is_positive
    point = (embedded_inverse(pattern) * u).applyfunc(sp.simplify)
    for j, selected in enumerate(pattern):
        if not selected:
            assert point[j] == 0
    mean_x += probability * point
    mean_z += probability * sp.Matrix(pattern)
    mean_cost += probability * (point.T * Q * point)[0]
assert sp.simplify(mean_x - x) == sp.zeros(3, 1)
assert sp.simplify(mean_z - sp.Matrix([1, half, half])) == sp.zeros(3, 1)
scalar_equal(mean_cost, 1 + a)

# Check the relaxation's attained value and a global nonnegative identity.
r = sp.Rational(1, 4)
M = sp.diag(1, r)
M1 = sp.Matrix([[half, -sp.Rational(1, 4)], [-sp.Rational(1, 4), sp.Rational(1, 8)]])
M2 = sp.diag(half, r)
for matrix in [M1, M2, M - M1, M - M2]:
    assert matrix[0, 0] >= 0 and matrix[1, 1] >= 0 and matrix.det() >= 0
relaxation_cost = 3 * r
for xi, matrix in zip([1, 0], [M1, M2]):
    relaxation_cost += (xi + matrix[0, 1]) ** 2 / half - matrix[1, 1]
scalar_equal(relaxation_cost, sp.Rational(3, 2))
r, s1, s2, r1, r2 = sp.symbols("r s1 s2 r1 r2", real=True)
objective = 3 * r + 2 * (1 + s1) ** 2 + 2 * s2**2 - r1 - r2
certificate = (
    (r - 2 * s1**2 - r1)
    + (r - 2 * s2**2 - r2)
    + (r - 4 * s1**2)
    + 8 * (s1 + sp.Rational(1, 4)) ** 2
    + 4 * s2**2
)
scalar_equal(objective - sp.Rational(3, 2), certificate)
print("PASS: exact support cut, W(p), hull witness, PSD witness, and relaxation certificate")
