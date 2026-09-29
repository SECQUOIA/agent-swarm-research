"""Exact checks for the secular-sum decision benchmark, not an FPT proof."""

from fractions import Fraction

import sympy as sp


lam, value = sp.symbols("lam value")
d = (sp.Integer(1), sp.Integer(2))
b = (sp.Integer(1), sp.Integer(1))
denominator = sp.prod(lam + di for di in d) ** 2
secular = sp.factor(
    denominator * (1 - sum(bi**2 / (lam + di) ** 2 for di, bi in zip(d, b)))
)
expected = lam**4 + 6 * lam**3 + 11 * lam**2 + 6 * lam - 1
assert sp.expand(secular - expected) == 0
assert sp.Poly(secular, lam).is_irreducible

x = [bi / (lam + di) for di, bi in zip(d, b)]
norm_error = sp.factor(sum(xj**2 for xj in x) - 1)
assert sp.cancel(norm_error + secular / denominator) == 0
objective = sum(di * xj**2 / 2 - bi * xj for di, bi, xj in zip(d, b, x))
formula = -(lam + sum(bi**2 / (lam + di) for di, bi in zip(d, b))) / 2
identity_error = sp.factor(objective - formula)
assert sp.cancel(identity_error - lam * secular / (2 * denominator)) == 0

# The objective value has a quartic annihilator in this small example.
value_equation = sp.together(value - formula).as_numer_denom()[0]
value_resultant = sp.factor(sp.resultant(secular, value_equation, lam))
value_polynomial = sp.Poly(value_resultant, value).primitive()[1]
assert value_polynomial.degree() == 4
assert value_polynomial.is_irreducible

# Two ball Hessians and the budget Hessian are independent when one block
# has unequal diagonal entries. All three are positive semidefinite.
ball_one = sp.diag(2, 2, 0, 0)
ball_two = sp.diag(0, 0, 2, 2)
budget = sp.diag(1, 2, 1, 2)
columns = [sp.Matrix(matrix).reshape(16, 1) for matrix in (ball_one, ball_two, budget)]
assert sp.Matrix.hstack(*columns).rank() == 3
assert all(matrix.is_positive_semidefinite for matrix in (ball_one, ball_two, budget))
assert budget.is_positive_definite

for h in range(1, 13):
    point = [Fraction(1, 2 ** (2**i)) for i in range(h + 1)]
    assert point[0] == Fraction(1, 2)
    assert all(point[i - 1] ** 2 == point[i] for i in range(1, h + 1))
    residuals = [point[i - 1] ** 2 - point[i] for i in range(1, h + 1)] + [point[h]]
    assert max(Fraction(0), *residuals) == Fraction(1, 2 ** (2**h))
    assert point[h] > 0

print("Passed: secular and value identities, quartic irreducibility, Hessian span, 12 exact squaring chains.")
