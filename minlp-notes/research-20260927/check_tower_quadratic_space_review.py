"""Independent finite checks for the tower's rational quadratic space.

Sparse power residues check all degree-two collisions for k=1,...,12.
Exact modular ranks check global pair-products for k=1,2,3; the all-k
statement still requires the block-degree proof in the review.
"""

from itertools import combinations_with_replacement

import sympy as sp


def homogeneous_monomials(variable_count, degree):
    for indices in combinations_with_replacement(range(variable_count), degree):
        exponent = [0] * variable_count
        for index in indices:
            exponent[index] += 1
        yield tuple(exponent)


def rank_mod(columns, prime=1009):
    pivots = {}
    for column in columns:
        vector = {m: int(c) % prime for m, c in column.items() if int(c) % prime}
        while vector:
            pivot = max(vector)
            value = vector[pivot]
            if pivot not in pivots:
                inverse = pow(value, -1, prime)
                pivots[pivot] = {m: c * inverse % prime for m, c in vector.items()}
                break
            for monomial, coefficient in pivots[pivot].items():
                updated = (vector.get(monomial, 0) - value * coefficient) % prime
                if updated:
                    vector[monomial] = updated
                else:
                    vector.pop(monomial, None)
    return len(pivots)


for k in range(1, 13):
    degree = 5**k
    weights = [power * 5 ** (k - i - 1) for i in range(k) for power in (1, 2, 3)]
    classes = {}
    total = 0
    for order in range(3):
        for exponent in homogeneous_monomials(3 * k, order):
            raw = sum(e * w for e, w in zip(exponent, weights))
            quotient, residue = divmod(raw, degree)
            assert quotient <= 1
            classes.setdefault(residue, []).append((exponent, 2**quotient))
            total += 1
    assert total - len(classes) == 5 * k

for k in (1, 2, 3):
    variables = sp.symbols(f"x0:{3*k}")
    quadrics = []
    for i in range(k):
        x, y, z = variables[3 * i:3 * i + 3]
        parent = 2 if i == 0 else variables[3 * (i - 1)]
        quadrics.extend([x*x-y, x*y-z, y*y-x*z, y*z-parent, z*z-parent*x])
    products = [sp.Poly(quadrics[i] * quadrics[j], *variables).as_dict()
                for i in range(5*k) for j in range(i, 5*k)]
    assert rank_mod(products) == (5*k)*(5*k+1)//2

x, y, z = sp.symbols("x y z")
leading = [x*x, x*y, y*y-x*z, y*z, z*z]
monomials = list(homogeneous_monomials(3, 4))
columns = [sp.Poly(leading[i]*leading[j], x, y, z)
           for i in range(5) for j in range(i, 5)]
matrix = sp.Matrix([[column.coeff_monomial(m) for column in columns] for m in monomials])
assert abs(matrix.det()) == 1
print("PASS: residue collision dimensions k=1..12; exact modular product ranks k=1..3; local determinant +/-1")
