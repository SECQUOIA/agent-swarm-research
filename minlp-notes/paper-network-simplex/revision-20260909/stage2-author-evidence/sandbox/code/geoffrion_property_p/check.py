"""Exact arithmetic spot checks; the continuum proof is in the result note."""
from fractions import Fraction as Q


def feasible(x):
    r, a, b, t = x
    return (0 <= a <= 1 and 0 <= b <= 1 and r >= 0 and t >= 0
            and r * r <= a and r * r <= b and (a + b) * t >= 1)


def coupling(x, y):
    _, a, b, _ = x
    return Q(1, 2) - (1 - y) * a - y * b


for u in map(Q, [0, Q(1, 4), Q(1, 2), 1, 2, 10, 100]):
    q = Q(1) if u <= Q(1, 2) else 1 / (2 * u)
    x = (q, q * q, q * q, 1 / (2 * q * q))
    assert feasible(x)
    expected = 1 - u / 2 if u <= Q(1, 2) else u / 2 + 1 / (4 * u)
    for y in [0, 1]:
        assert x[0] + u * coupling(x, y) == expected
    # Verify exact scalar domination on a rational grid, including endpoints.
    for k in range(101):
        r = Q(k, 100)
        assert u / 2 + r - u * r * r <= expected
    if u > Q(1, 2):
        assert Q(1, 2) - coupling(x, 0) == 1 / (4 * u * u)
        assert x[3] == 2 * u * u

for y, x in [(0, (Q(0), Q(0), Q(1), Q(1))),
             (1, (Q(0), Q(1), Q(0), Q(1)))]:
    assert feasible(x)
    assert coupling(x, y) == Q(1, 2)

strict = (Q(1, 4), Q(1, 4), Q(1, 4), Q(3))
assert feasible(strict)
assert all(coupling(strict, y) > 0 for y in [0, 1])
assert strict[0] ** 2 < strict[1] and strict[0] ** 2 < strict[2]
assert (strict[1] + strict[2]) * strict[3] > 1
print("Exact checks passed: common scalar optima, individual feasibility maxima, Slater, and escape rate.")
