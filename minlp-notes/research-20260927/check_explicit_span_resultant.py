"""Exact small adversarial checks of the two-parameter elimination lemma.

Run directly with Python and SymPy.  These finite examples do not prove the
general elimination lemma or its degree and coefficient bounds.
"""

from itertools import product

import sympy as sp


x, y, epsilon, delta, w, zeta = sp.symbols("x y epsilon delta w zeta")


def characteristic_determinant(equations, variables, degree, denominator, numerator):
    """Return det(w A - B - zeta I) in the stipulated monomial basis."""
    exponent_bound = degree + 1
    deformed = [
        equation + delta * variable**exponent_bound
        for equation, variable in zip(equations, variables)
    ]
    basis = list(product(range(exponent_bound), repeat=len(variables)))
    index = {exponent: j for j, exponent in enumerate(basis)}
    groebner = sp.groebner(
        deformed,
        *variables,
        order="grlex",
        domain=sp.QQ.frac_field(delta, epsilon),
    )

    def multiplication(polynomial):
        matrix = sp.zeros(len(basis))
        for column, exponent in enumerate(basis):
            monomial = sp.prod(v**p for v, p in zip(variables, exponent))
            remainder = groebner.reduce(sp.expand(polynomial * monomial))[1]
            for powers, coefficient in sp.Poly(remainder, *variables).terms():
                assert powers in index
                matrix[index[powers], column] = coefficient
        return matrix

    a = multiplication(denominator**2)
    b = multiplication(numerator)
    return sp.factor((-1) ** len(basis) * (w * a - b).charpoly(zeta).as_expr())


def extract(determinant):
    """Clear delta denominators, then take lowest zeta and delta terms."""
    polynomial, denominator = sp.cancel(determinant).as_numer_denom()
    assert not denominator.has(w, zeta, epsilon)
    assert sp.Poly(denominator, delta).is_monomial
    zeta_polynomial = sp.Poly(polynomial, zeta)
    zeta_order = min(exponent[0] for exponent, _ in zeta_polynomial.terms())
    zeta_coefficient = zeta_polynomial.coeff_monomial(zeta**zeta_order)
    delta_polynomial = sp.Poly(zeta_coefficient, delta)
    delta_order = min(exponent[0] for exponent, _ in delta_polynomial.terms())
    relation = sp.factor(delta_polynomial.coeff_monomial(delta**delta_order))
    return zeta_order, delta_order, relation


# A persistent base point kills the naive determinant for every delta and w.
one_variable = characteristic_determinant([x * (x - 1)], (x,), 2, x, x)
assert one_variable.subs(zeta, 0) == 0
order, _, relation = extract(one_variable)
assert order == 1
assert sp.expand(relation + w * (w - 1)) == 0
assert relation.subs(w, 1) == 0

# The original system has the entire line x=0 and the isolated nonsingular
# point (1,epsilon).  The deformed base point (0,0) has algebraic length three.
equations = [x * (x - 1), x * (y - epsilon)]
jacobian = sp.Matrix(equations).jacobian((x, y))
assert jacobian.subs({x: 1, y: epsilon}).det() == 1
two_variables = characteristic_determinant(equations, (x, y), 2, x, x + y)
assert two_variables.subs(zeta, 0) == 0
order, _, relation = extract(two_variables)
assert order == 3
assert sp.expand(relation + w**3 * (w - 1 - epsilon)) == 0
assert relation.subs(w, 1 + epsilon) == 0

# Independently construct the same polynomial by iterated resultants.
deformed_x = equations[0] + delta * x**3
deformed_y = equations[1] + delta * y**3
iterated = sp.resultant(
    deformed_x,
    sp.resultant(deformed_y, w * x**2 - x - y - zeta, y),
    x,
)
assert sp.cancel(iterated / two_variables) == delta**9
assert extract(iterated)[2] == relation

# Specializing the external parameter before elimination gives a relation
# vanishing at the same target, including the collision epsilon=-1, w=0.
for value in (-2, -1, 0, 1, 2):
    specialized_relation = extract(two_variables.subs(epsilon, value))[2]
    assert specialized_relation.subs(w, 1 + value) == 0

# Specialization can increase the persistent base multiplicity and make the
# globally extracted relation identically zero.  The lemma must allow this.
specializing_base = characteristic_determinant(
    [x * (x - 1) * (x - epsilon)], (x,), 3, x, x
)
order, _, relation = extract(specializing_base)
assert order == 1
assert sp.expand(relation + epsilon * w * (w - 1) * (epsilon * w - 1)) == 0
assert relation.subs(epsilon, 0) == 0
epsilon_polynomial = sp.Poly(relation, epsilon)
epsilon_order = min(powers[0] for powers, _ in epsilon_polynomial.terms())
assert epsilon_order == 1
assert epsilon_polynomial.coeff_monomial(epsilon).subs(w, 1) == 0
specialized_order, _, specialized_relation = extract(
    specializing_base.subs(epsilon, 0)
)
assert specialized_order == 2
assert sp.expand(specialized_relation - w * (w - 1)) == 0

# Outside the hypothesis, positive-dimensional components are not recovered:
# x=0, arbitrary y solves G=(x,x), but the extracted relation misses y=1.
singular = characteristic_determinant([x, x], (x, y), 1, sp.Integer(1), y)
order, _, relation = extract(singular)
assert order == 0
assert sp.expand(relation + w**2) == 0
assert relation.subs(w, 1) != 0

print("PASS: persistent base locus, positive-dimensional component, parameter")
print("specializations, increased base multiplicity, independent resultants,")
print("and singular-root limitation")
