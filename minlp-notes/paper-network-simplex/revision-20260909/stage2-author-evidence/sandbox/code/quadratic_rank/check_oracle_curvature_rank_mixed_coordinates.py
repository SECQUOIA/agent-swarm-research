"""Independent exact rank-band checks with signed, nonconvex coordinates.

The ambient outputs are componentwise convex; a mixed basis makes individual
effective coordinate functions nonconvex. This tests subspace-preserving
rounding and a nontrivial inverse band matrix rather than ambient rounding.
"""

from fractions import Fraction as F
from itertools import product


def mv(matrix, vector):
    return tuple(sum(a * b for a, b in zip(row, vector)) for row in matrix)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def mix(a, b, t):
    return tuple((1 - t) * x + t * y for x, y in zip(a, b))


V = ((F(1), F(2)), (F(-1), F(1)), (F(0), F(3)), (F(3, 2), F(9, 2)))
B = ((F(1, 12), F(-1, 3)), (F(1, 12), F(1, 6)))
B_inverse = ((F(4), F(8)), (F(-2), F(2)))
r = 2
delta = F(1, 16 * r * 17)


def q(x):
    u, v = x*x - x, x**4 - x
    return ((u - 2*v) / 3, (u + v) / 3)


def gauge(coordinate):
    return r * max(map(abs, mv(B_inverse, coordinate)))


for signs in product((-1, 1), repeat=2):
    point = mv(B, tuple(F(s, r) for s in signs))
    assert max(map(abs, mv(V, point))) <= 1

polar_checks = 0
for raw in product(range(5), repeat=4):
    if sum(raw) > 4:
        continue
    lam = tuple(F(a, 4) for a in raw)
    # Basis polar weights are the first two ambient coordinate unit vectors.
    coefficients = (lam[0] + lam[2] + 2*lam[3],
                    lam[1] + lam[2] + lam[3]/2)
    assert max(map(abs, coefficients)) <= 3
    polar_checks += 1

band_checks = 0
errors = [tuple(sign * delta for sign in signs)
          for signs in product((-1, 1), repeat=2)]
for cell in range(16):
    left, right = F(cell, 16), F(cell + 1, 16)
    for numerator in range(9):
        t = F(numerator, 8)
        x = (1-t)*left + t*right
        exact = q(x)
        chord = mix(q(left), q(right), t)
        gap = tuple(a-b for a, b in zip(chord, exact))
        ambient_gap = mv(V, gap)
        assert all(value >= 0 for value in ambient_gap)
        scalar_gap = ambient_gap[0] + ambient_gap[1]
        assert scalar_gap <= F(13, 16 * 36 * r)
        assert gauge(gap) <= F(13, 64)
        for error_left, error_right in product(errors, repeat=2):
            error = mix(error_left, error_right, t)
            assert gauge(error) <= F(1, 16)
            center_error = add(gap, error)
            assert gauge(center_error) <= F(17, 64)
            for signs in product((-1, 1), repeat=2):
                band = mv(B, tuple(F(sign, 2*r) for sign in signs))
                full_error = add(center_error, band)
                assert gauge(full_error) <= F(49, 64)
                assert max(map(abs, mv(V, full_error))) <= 1
                band_checks += 1

print(f"PASS: {polar_checks} positive-polar representations and {band_checks} "
      "exact mixed-coordinate rounding/band errors; all remain in the rank-2 image.")
