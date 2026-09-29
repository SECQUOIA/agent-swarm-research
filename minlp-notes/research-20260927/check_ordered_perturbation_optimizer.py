"""Exact stress test for the ordered-limit elimination lemma.

The selected multiplier diverges and the two iterated limits differ.
This checks one example, not the general optimizer theorem.
"""

import sympy as sp


def lowest_coefficient(expression, variable):
    polynomial = sp.Poly(expression, variable)
    exponent = min(power[0] for power, value in polynomial.terms() if value)
    return sp.expand(polynomial.coeff_monomial(variable**exponent))


epsilon, delta, beta, w, zeta = sp.symbols("epsilon delta beta w zeta")

# G = delta * lambda - 1 and its deformation beta * lambda**2 + G.
# Columns are coordinates in the ordered quotient basis (1, lambda).
multiply_lambda = sp.Matrix([[0, 1 / beta], [1, -delta / beta]])
identity = sp.eye(2)
assert sp.simplify(
    beta * multiply_lambda**2 + delta * multiply_lambda - identity
) == sp.zeros(2)

multiply_a = identity + epsilon * multiply_lambda
multiply_b = epsilon * multiply_lambda
determinant = sp.factor(
    (beta**2 * (w * multiply_a - multiply_b - zeta * identity)).det()
)
expected = beta**3 * (
    beta * (w - zeta) ** 2
    - delta * epsilon * (w - 1) * (w - zeta)
    - epsilon**2 * (w - 1) ** 2
)
assert sp.expand(determinant - expected) == 0

relation = lowest_coefficient(lowest_coefficient(determinant, zeta), beta)
selected_ratio = epsilon / (epsilon + delta)
assert sp.simplify(relation.subs(w, selected_ratio)) == 0
inner_relation = lowest_coefficient(relation, delta)
final_relation = lowest_coefficient(inner_relation, epsilon)
assert sp.expand(final_relation + (w - 1) ** 2) == 0
assert final_relation.subs(w, 1) == 0
assert final_relation.subs(w, 0) != 0

prescribed_limit = sp.limit(
    sp.limit(selected_ratio, delta, 0, dir="+"), epsilon, 0, dir="+"
)
reversed_limit = sp.limit(
    sp.limit(selected_ratio, epsilon, 0, dir="+"), delta, 0, dir="+"
)
assert prescribed_limit == 1
assert reversed_limit == 0
assert sp.limit(1 / delta, delta, 0, dir="+") == sp.oo

print(
    "PASS: quotient identity, exact multiplication determinant, selected-root "
    "relation, ordered coefficients, divergent multiplier, unequal iterated limits"
)
