"""Exact quadratic-multiplier certificate for the ternary counterexample.

For F from check_ternary_rational_sos_convex_counterexample.py and
S = 1+x^2+y^2+z^2, verify 8*S*F = b.T*N*b with integer N and N-8*I > 0.
The entries of b form the rational degree-at-most-three vanishing space at
(a^-1,a,a^-3), where a^5=2. Positive rational LDL pivots are sums of four
rational squares, so this is a rational SOS certificate for S*F.

Multiplying that SOS identity by S gives F as a sum of rational-function
squares with common denominator S, which is positive everywhere. No
nonconstant rational affine common denominator can repair a non-Q-SOS
polynomial: each numerator vanishes on its real hyperplane and is divisible
by it, so the denominator cancels. Thus denominator degree two is minimal.

Discovery used a numerical SDP, followed by integer rounding of free Gram
entries and exact coefficient projection. This checker uses only exact
SymPy arithmetic; it requires no numerical solver or discovery files.
"""

from itertools import product

import sympy as s


x, y, z = variables = s.symbols("x y z")
a = s.symbols("a")
residuals = [
    2-2*x*y,
    2*x*x-2*y*z,
    2*y*y-4*z,
    2*z*z-x,
    2*x*z-y,
]
exposing = sum(c*q for c, q in zip([4, 5, 3, 9], residuals))
F = s.expand(exposing**2 + sum(q*q for q in residuals[:4])
             - residuals[4]**2)
S = 1+x*x+y*y+z*z
basis = s.Matrix([
    z**2-x/2,
    y**2-2*z,
    x*z-y/2,
    x*y-1,
    x**2-y*z,
    z**3-y/4,
    y*z**2-s.Rational(1, 2),
    y**2*z-x,
    y**3-2*y*z,
    x*z**2-y*z/2,
    x*y*z-z,
    x*y**2-y,
    x**2*z-s.Rational(1, 2),
    x**2*y-x,
    x**3-z,
])
N = s.Matrix([
    [4240, 527, 792, -124, 992, -1728, 696, -1112, 216, -312, 1212, -384, -1200, 76, -8],
    [527, 556, 376, -194, 361, -16, 136, -92, 0, 280, -340, -232, 44, 168, -128],
    [792, 376, 3176, -175, 568, -1000, 584, -232, 256, -1272, 432, -912, -1112, 990, -384],
    [-124, -194, -175, 980, -72, 432, -1080, 552, -200, 104, -408, 488, -320, -624, 136],
    [992, 361, 568, -72, 1960, -216, 480, 400, -80, -912, 184, -400, -576, 440, -720],
    [-1728, -16, -1000, 432, -216, 2624, -1440, 700, -24, 0, -912, 8, 1052, -256, -40],
    [696, 136, 584, -1080, 480, -1440, 3784, -1896, 440, -240, 728, -680, -1344, 1232, -352],
    [-1112, -92, -232, 552, 400, 700, -1896, 2000, -480, -96, -832, 400, 560, -816, 240],
    [216, 0, 256, -200, -80, -24, 440, -480, 320, -24, 240, -384, 56, 264, -80],
    [-312, 280, -1272, 104, -912, 0, -240, -96, -24, 3368, -672, 264, 40, -488, 460],
    [1212, -340, 432, -408, 184, -912, 728, -832, 240, -672, 2800, -552, -952, 376, -304],
    [-384, -232, -912, 488, -400, 8, -680, 400, -384, 264, -552, 1296, 24, -944, 244],
    [-1200, 44, -1112, -320, -576, 1052, -1344, 560, 56, 40, -952, 24, 2760, -528, 0],
    [76, 168, 990, -624, 440, -256, 1232, -816, 264, -488, 376, -944, -528, 1848, -640],
    [-8, -128, -384, 136, -720, -40, -352, 240, -80, 460, -304, 244, 0, -640, 832],
])
assert N == N.T
assert s.Poly(s.expand((basis.T*N*basis)[0]-8*S*F), variables).is_zero
print("PASS: exact identity 8*(1+x^2+y^2+z^2)*F = b.T*N*b")

L, D = (N-8*s.eye(15)).LDLdecomposition(hermitian=False)
assert L*D*L.T == N-8*s.eye(15)
assert all(D[i, i] > 0 for i in range(15))
print("PASS: exact rational LDL proves N-8*I positive definite")

point = {x: a**4/2, y: a, z: a**2/2}


def at_point(q):
    return s.rem(s.expand(q.subs(point)), a**5-2, a, domain=s.QQ)


monomials = [s.prod(v**e for v, e in zip(variables, exponents))
             for exponents in product(range(4), repeat=3)
             if sum(exponents) <= 3]
evaluation = s.Matrix([
    [s.Poly(at_point(m), a).coeff_monomial(a**i) for m in monomials]
    for i in range(5)
])
coefficients = s.Matrix([
    [s.Poly(q, variables).coeff_monomial(m) for q in basis]
    for m in monomials
])
assert len(monomials) == 20 and evaluation.rank() == 5
assert coefficients.rank() == 15
assert evaluation*coefficients == s.zeros(5, 15)
assert all(at_point(q) == 0 for q in basis)
print("PASS: b is a basis of the 15-dimensional rational cubic vanishing space")
print("Consequence: S*F is Q-SOS; F has rational-function SOS denominator S")
