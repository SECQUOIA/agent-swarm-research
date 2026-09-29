"""Exact first-step check of the recursive rational radial separator.

Checks the base degree-two separator, the extension to degree three,
and the explicit sufficient N=1 scaling threshold. The general induction
is proved in rational-radial-quantitative-separation.md.
"""

from itertools import product
from math import comb, isqrt

import sympy as s


x, y, z = variables = s.symbols("x y z")
residuals = [
    2 - 2*x*y,
    2*x*x - 2*y*z,
    2*y*y - 4*z,
    2*z*z - x,
    2*x*z - y,
]
exposing = sum(c*q for c, q in zip((4, 5, 3, 9), residuals))
F = s.Poly(exposing**2 + sum(q*q for q in residuals[:4])
           - residuals[4]**2, variables, domain=s.QQ)
radial = s.Poly(x*x + y*y + z*z, variables, domain=s.QQ)
representatives = ((0, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1), (1, 0, 0))
K = 28450
a0 = s.Rational(85351, K)


def monomials(degree):
    return sorted(
        (e for e in product(range(degree + 1), repeat=3) if sum(e) <= degree),
        key=lambda e: (sum(e), e),
    )


def grid_moment(exponents, degree):
    return s.prod(sum(k**power for k in range(degree + 1))
                  for power in exponents)


def basis(degree):
    result = []
    for exponents in monomials(degree):
        if exponents in representatives:
            continue
        i, j, k = exponents
        exponent = 4*i + j + 2*k
        residue = exponent % 5
        shift = exponent // 5 - i - k + int(residue >= 2)
        coefficient = s.Rational(2)**shift
        leading = s.prod(v**n for v, n in zip(variables, exponents))
        remainder = s.prod(v**n for v, n in
                           zip(variables, representatives[residue]))
        result.append(s.Poly(leading - coefficient*remainder,
                             variables, domain=s.QQ))
    assert len(result) == comb(degree + 3, 3) - 5
    return result


weights = {e: s.Rational(grid_moment(e, 2), K) for e in monomials(4)}
weights[(0, 0, 1)] += 2
weights[(0, 2, 0)] += 4


def apply_functional(poly):
    return sum(coefficient*weights.get(e, 0) for e, coefficient in poly.terms())


def gram(polynomials):
    return s.Matrix(len(polynomials), len(polynomials),
                    lambda i, j: apply_functional(polynomials[i]*polynomials[j]))


evaluation_sum = sum(F.eval(dict(zip(variables, point)))
                     for point in product(range(3), repeat=3))
assert evaluation_sum == 28449
assert apply_functional(F) == -a0
old_basis = basis(2)
old_gram = gram(old_basis)
assert all(old_gram[:k, :k].det() > 0 for k in range(1, 6))
print("PASS: E(F)=28449; lambda_2(F)=-85351/28450; base Gram positive definite")

degree = 3
new_basis = basis(degree)
old_size = len(old_basis)
assert new_basis[:old_size] == old_basis
assert all(poly.total_degree() == degree for poly in new_basis[old_size:])
unextended = gram(new_basis)
A = unextended[:old_size, :old_size]
B = unextended[:old_size, old_size:]
C = unextended[old_size:, old_size:]
assert A == old_gram
new_monomials = [e for e in monomials(degree) if sum(e) == degree]
assert len(new_monomials) == len(new_basis) - old_size
D = s.Matrix(len(new_monomials), len(new_monomials), lambda i, j:
             grid_moment(tuple(a + b for a, b in
                               zip(new_monomials[i], new_monomials[j])), degree))
assert all(D[:k, :k].det() > 0 for k in range(1, D.rows + 1))
schur = C - B.T*A.inv()*B
row_bound = max(sum(abs(schur[i, j]) for j in range(schur.cols))
                for i in range(schur.rows))
determinant = D.det()
trace = s.trace(D)
beta = determinant / trace**(D.rows - 1)
T = s.ceiling((row_bound + 1) / beta)
assert T == 85434602576348679
assert T*beta - row_bound >= 1
for exponents in monomials(2*degree):
    if sum(exponents) == 2*degree:
        weights[exponents] = T*grid_moment(exponents, degree)
updated = gram(new_basis)
assert updated[:old_size, :old_size] == A
assert updated[:old_size, old_size:] == B
assert updated[old_size:, old_size:] == C + T*D
assert all(updated[:k, :k].det() > 0 for k in range(1, updated.rows + 1))
assert apply_functional(F) == -a0
print("D_3 determinant:", determinant)
print("D_3 trace:", trace)
print("m_3:", row_bound)
print("beta_3:", beta)
print("T_3:", T)
print("PASS: exact block identity and all 15 positive leading principal minors")

A1 = abs(apply_functional(F*radial))
threshold_square = max(s.Integer(1), 2*(A1 + 1)/a0)
numerator, denominator = map(int, s.fraction(threshold_square))
threshold = isqrt(numerator // denominator)
if threshold*threshold*denominator < numerator:
    threshold += 1
assert threshold == 711859414639
assert threshold*threshold >= threshold_square
perturbed = F*(s.Poly(1, variables, domain=s.QQ)
               + radial.mul_ground(s.Rational(1, threshold*threshold)))
assert apply_functional(perturbed) < -a0/2
print("A_1:", A1)
print("Sufficient integer threshold for N=1:", threshold)
print("PASS: the perturbed polynomial has strictly negative separator value")
