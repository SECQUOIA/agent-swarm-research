"""Exact examples for the strict Farkas oracle and rational ellipsoid tests.

These checks do not verify the general radius, gap, or lattice algorithm.
"""
import sympy as sp

u, v, epsilon = sp.symbols('u v epsilon', real=True)

# Two opposite linear rows project to u**4 <= 0 before relaxation.
# The strict relaxed phase-I LP has sigma*=epsilon-u**4/2.
rows = [v + u**4 - epsilon, -v - epsilon]
lam = [sp.Rational(1, 2), sp.Rational(1, 2)]
F = sp.expand(sum(a * b for a, b in zip(lam, rows)))
assert F == u**4 / 2 - epsilon
v_star = -u**4 / 2
sigma_star = epsilon - u**4 / 2
assert all(sp.expand(row.subs(v, v_star) + sigma_star) == 0 for row in rows)
assert F.subs({u: 0, epsilon: sp.Rational(1, 32)}) < 0
assert F.subs({u: sp.Rational(1, 2), epsilon: sp.Rational(1, 32)}) == 0
assert F.subs({u: 1, epsilon: sp.Rational(1, 32)}) > 0
assert sp.diff(F, u, 2) == 6 * u**2

# Strict-family membership differs from the unrelaxed weak family at
# noninteger query points, even when the integer solutions coincide.
assert sp.Rational(1, 2)**2 > 0
assert sp.Rational(1, 2)**2 - 1 < 0

# Dyadic factor-two square-root bounds and 2m exact rational test points.
checked_points = 0
for m in range(1, 7):
    L = sp.eye(m)
    for i in range(m):
        for j in range(i):
            L[i, j] = (i + 2 * j + 1) % 5 - 2
    ds = [sp.Rational(2 * i + 3, i + 2) for i in range(m)]
    A = L * sp.diag(*ds) * L.T
    A_inv = A.inv()
    center = sp.Matrix([sp.Rational(i + 1, i + 2) for i in range(m)])
    ts = []
    for di in ds:
        ti = sp.Rational(1)
        while 4 * ti**2 < di:
            ti *= 2
        while ti**2 > di:
            ti /= 2
        assert ti**2 <= di <= 4 * ti**2
        ts.append(ti)
    for i, ti in enumerate(ts):
        ei = sp.eye(m)[:, i]
        offset = L * ei * ti / (m + 1)
        ellipsoidal_norm_squared = (offset.T * A_inv * offset)[0]
        assert ellipsoidal_norm_squared == ti**2 / (ds[i] * (m + 1)**2)
        assert ellipsoidal_norm_squared <= sp.Rational(1, (m + 1)**2)
        assert ellipsoidal_norm_squared >= sp.Rational(1, 4 * (m + 1)**2)
        for sign in (-1, 1):
            point = center + sign * offset
            assert all(coordinate.is_Rational for coordinate in point)
            checked_points += 1
    beta = 2 * m * (m + 1)
    assert beta**2 >= 4 * m * (m + 1)**2

# A unimodular lattice section must normalize the ROW normal, not merely
# place it in a column. This checks the substantive recursion correction.
w, t = sp.symbols('w t')
normal = sp.Matrix([[2, 3]])
U = sp.Matrix([[3, -1], [-2, 1]])
assert U.det() == 1
assert normal * U == sp.Matrix([[0, 1]])
section = U * sp.Matrix([w, t])
assert sp.expand((normal * section)[0]) == t
wrong_column_completion = sp.Matrix([[1, 2], [1, 3]])
assert wrong_column_completion.det() == 1
assert wrong_column_completion[:, 1] == normal.T
assert normal * wrong_column_completion != sp.Matrix([[0, 1]])

print(f'Passed: strict quartic projection/boundary identities, {checked_points} rational ellipsoid test points, and the unimodular lattice-section correction.')
