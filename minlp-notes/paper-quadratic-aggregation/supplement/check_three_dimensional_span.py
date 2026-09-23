"""Exact identities and witnesses for the three-dimensional-span appendix.

The symbolic coefficient checks use only integer arithmetic. Rational
examples additionally check all signs, including the two added rows.
These checks do not prove HHC, the facet theorem, universal hull equalities,
or literature priority; those arguments are in the manuscript.
"""

from fractions import Fraction as F
from itertools import permutations


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for monomial, value in polynomial.items():
            result[monomial] = result.get(monomial, 0) + value
    return {m: v for m, v in result.items() if v}


def scale(polynomial, coefficient):
    return {m: coefficient * v for m, v in polynomial.items()
            if coefficient * v}


def multiply(left, right):
    result = {}
    for ml, vl in left.items():
        for mr, vr in right.items():
            monomial = tuple(a + b for a, b in zip(ml, mr))
            result[monomial] = result.get(monomial, 0) + vl * vr
    return {m: v for m, v in result.items() if v}


def subtract(left, right):
    return add(left, scale(right, -1))


one = {(0, 0, 0): 1}
a = {(1, 0, 0): 1}
b = {(0, 1, 0): 1}
c = {(0, 0, 1): 1}

# Universal three-variable Vandermonde coefficient identity.
rows = [[v, subtract(one, multiply(v, v)), scale(one, -1)]
        for v in (a, b, c)]
determinant = {}
for permutation in permutations(range(3)):
    inversions = sum(permutation[i] > permutation[j]
                     for i in range(3) for j in range(i + 1, 3))
    term = one
    for i, j in enumerate(permutation):
        term = multiply(term, rows[i][j])
    determinant = add(determinant, scale(term, (-1) ** inversions))
vandermonde = multiply(multiply(subtract(b, a), subtract(c, a)),
                       subtract(c, b))
assert determinant == vandermonde

# Numerator of f_b(p_a), after multiplication by 1+a^2.
numerator = add(scale(multiply(a, b), 2),
                subtract(one, multiply(b, b)),
                scale(add(one, multiply(a, a)), -1))
assert numerator == scale(multiply(subtract(b, a), subtract(b, a)), -1)

# Universal coordinate identity Q(a)+a(-E1)+(1-a^2)(-E2)=-E3.
assert add(rows[0][0], scale(a, -1)) == {}
assert add(rows[0][1], scale(subtract(one, multiply(a, a)), -1)) == {}
assert rows[0][2] == scale(one, -1)

# Distinct rational instances validate signs and augmented constraints.
pair_count = 0
for m in range(3, 16):
    parameters = [F(i, m + 1) for i in range(1, m + 1)]
    for ai in parameters:
        x_squared = 2 * ai / (1 + ai * ai)
        rho = 1 / (1 + ai * ai)
        assert x_squared > 0 and rho > 0
        assert -x_squared < 0 and -rho < 0
        for aj in parameters:
            slack = aj * x_squared + (1 - aj * aj) * rho - 1
            expected = -(aj - ai) ** 2 / (1 + ai * ai)
            assert slack == expected
            assert (slack == 0) == (ai == aj)
            assert slack <= 0
            pair_count += 1

print("PASS: exact Vandermonde, witness-numerator, and negative-cone")
print(f"coefficient identities; {pair_count} rational witness evaluations.")
