"""Independent rational Taylor-SOS check using an actual PD Hessian Gram.

This checks the certificate transformation, not the tower's earlier theorem.
The author's two-gate checker separately covers the root-ideal identities.
"""

from fractions import Fraction

import sympy as sp


def split_positive_rational(weight):
    numerator, denominator = map(int, sp.fraction(weight))
    assert numerator > 0 and denominator > 0
    integer = numerator * denominator
    factors = []
    for bit in range(integer.bit_length()):
        if integer & (1 << bit):
            value = Fraction(1 << (bit // 2), denominator)
            factors += [sp.Rational(value.numerator, value.denominator)] * (1 + bit % 2)
    assert sum(a * a for a in factors) == weight
    return factors


x = sp.Matrix(sp.symbols("x0:3"))
y = sp.Matrix(sp.symbols("y0:3"))
v = sp.Matrix(sp.symbols("v0:3"))
u = x - y
T = sp.Matrix([[2, 1, 0], [1, 2, 0], [0, 0, 3]])
C = sp.Matrix([[2, 1, 0], [1, 3, 1], [0, 1, 2]])
F = sp.expand((x.T * T * x)[0] ** 2 + (x.T * C * x)[0])
vector_T = sp.Matrix(list(T))
Q = 8 * vector_T * vector_T.T + 4 * sp.kronecker_product(T, T)
M = sp.diag(2 * C, Q)
z = v.col_join(sp.kronecker_product(x, v))
assert sp.expand((z.T * M * z)[0] - (v.T * sp.hessian(F, x) * v)[0]) == 0
lower, diagonal = M.LDLdecomposition(hermitian=False)
assert lower * diagonal * lower.T == M
assert all(diagonal[i, i] > 0 for i in range(M.rows))

A = u.col_join(sp.kronecker_product(y, u))
B = sp.zeros(3, 1).col_join(sp.kronecker_product(u, u))
first = lower.T * (A + B / 3)
second = lower.T * B
square_factors = []
for i in range(M.rows):
    for coefficient in split_positive_rational(diagonal[i, i] / 2):
        square_factors.append(coefficient * first[i])
    for coefficient in split_positive_rational(diagonal[i, i] / 36):
        square_factors.append(coefficient * second[i])
sos = sp.expand(sum(q * q for q in square_factors))
FY = F.xreplace(dict(zip(x, y)))
gradient_Y = sp.Matrix([sp.diff(FY, yi) for yi in y])
assert sp.expand(sos - F + FY + (gradient_Y.T * u)[0]) == 0
assert all(sp.Poly(q, *x, *y).total_degree() <= 2 for q in square_factors)
assert all(coefficient.is_Rational for q in square_factors
           for coefficient in sp.Poly(q, *x, *y).coeffs())
print(f"PASS: actual 12-by-12 PD Hessian Gram; {len(square_factors)} rational Taylor squares; exact identity")
