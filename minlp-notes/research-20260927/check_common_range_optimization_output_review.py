"""Exact boundary checks for the common-range optimal-output review.

These examples do not verify the general complexity or algebraic bounds.
"""

import sympy as sp


root = sp.sqrt(2)
cases = 0
for rank in range(1, 13):
    # Native cones force u=sqrt(2); remaining rows are affine:
    # v_j >= j*u, w >= 0, and -1 <= t <= 1.
    # Minimize sum(v_j**2) + w. The optimal face varies freely in t.
    n = rank + 3
    q_matrix = sp.diag(0, *([2] * rank), 0, 0)
    linear = sp.zeros(n, 1)
    linear[rank + 1] = 1
    theta = 2 * sum(j * j for j in range(1, rank + 1))
    gradient = None
    for t in (sp.Rational(-1), sp.Rational(0), sp.Rational(2, 3)):
        x = sp.Matrix([root, *[j * root for j in range(1, rank + 1)], 0, t])
        value = (x.T * q_matrix * x)[0] / 2 + (linear.T * x)[0]
        assert sp.simplify(value - theta) == 0
        current = q_matrix * x + linear
        if gradient is None:
            gradient = current
        assert current == gradient
        assert sp.simplify(2 - x[0] ** 2) == 0
        assert sp.simplify(2 * x[0] ** 2 - 4) == 0
        assert x[0].is_positive
        assert all(sp.simplify(x[j] - j * x[0]) == 0 for j in range(1, rank + 1))
        cases += 1

    b = gradient - linear
    x0 = q_matrix.pinv() * b
    assert q_matrix * x0 == b
    rhs = sp.simplify(theta - (x0.T * q_matrix * x0)[0] / 2)
    assert rhs == 0
    assert q_matrix.rank() == rank

    # The gradient equations alone admit this feasible, nonoptimal point.
    wrong = sp.Matrix([root, *[j * root for j in range(1, rank + 1)], 1, 0])
    assert q_matrix * wrong == b
    assert (linear.T * wrong)[0] != rhs
    assert sp.simplify((wrong.T * q_matrix * wrong)[0] / 2 + (linear.T * wrong)[0] - theta) == 1

    # One quadratic field suffices despite the increasing ambient rank.
    for entry in list(gradient) + list(x0):
        assert sp.Poly(sp.minpoly(entry)).degree() <= 2

print(f"PASS: {cases} exact optimal-face points, 12 scalar-equation counterexamples,")
print("and 12 arbitrary-rank families with a common quadratic field.")
