"""Exact local and coupled checks for the rational auxiliary certificate.

The test polynomial need not be convex: the symbolic identities are universal.
PSD of the Taylor Gram follows separately from the retained Hessian certificate.
"""

from fractions import Fraction

import sympy as sp


def rational_squares(a, b):
    """Return a deterministic rational square decomposition of positive a/b."""
    assert a > 0 and b > 0
    n = a * b
    terms = []
    for exponent in range(n.bit_length()):
        if (n >> exponent) & 1:
            base = Fraction(2 ** (exponent // 2), b)
            terms.extend([base] * (1 if exponent % 2 == 0 else 2))
    assert sum(v * v for v in terms) == Fraction(a, b)
    assert len(terms) <= 2 * n.bit_length()
    return terms


Y = sp.symbols("y0:6")
X = sp.symbols("x0:6")
u = sp.Matrix([x - y for x, y in zip(X, Y)])
residuals = []
relations = []
local_exposers = []
affine_coefficients = []
for i in range(2):
    x, y, z = Y[3 * i:3 * i + 3]
    b = sp.Integer(2) if i == 0 else Y[0]
    r1, r2, r3 = x**2 - y, x * y - z, y * z - b
    R, S = y**2 - x * z, z**2 - b * x
    assert sp.expand(R + y * r1 - x * r2) == 0
    assert sp.expand(S + z * r2 - x * r3) == 0
    # Deliberately different rational coefficients in the two coupled gates.
    c1, c2, c3, cR, cS = map(sp.Rational, (2 + i, -3, -1 - i, 1 - 2 * i, 1))
    g = c1 * r1 + c2 * r2 + c3 * r3 + cR * R + cS * S
    coeff = [c1 - cR * y, c2 + cR * x - cS * z, c3 + cS * x]
    assert sp.expand(g - sum(a * r for a, r in zip(coeff, (r1, r2, r3)))) == 0
    local_exposers.append(g)
    affine_coefficients.extend([sp.Rational(1, 2**i) * a for a in coeff])
    residuals.extend((r1, r2, r3))
    relations.append(R)

G = local_exposers[0] + local_exposers[1] / 2
assert sp.expand(G - sum(a * r for a, r in zip(affine_coefficients, residuals))) == 0
R = relations[-1]
q = [G, *residuals, R]
weights = [sp.Rational(7, 3), *([sp.Rational(5, 2)] * 6), sp.Integer(-1)]
F = sp.expand(sum(w * f**2 for w, f in zip(weights, q)))
FX = F.xreplace(dict(zip(Y, X)))
grad = sp.Matrix([sp.diff(F, y) for y in Y])
H = [sp.expand(w * (f + 2 * sum(sp.diff(f, y) * ui for y, ui in zip(Y, u))))
     for w, f in zip(weights, q)]
remainder = sp.expand(sum(h * f for h, f in zip(H, q)))
assert sp.expand(remainder - F - (grad.T * u)[0]) == 0
assert all(sp.Poly(h, *X, *Y).total_degree() <= 2 for h in H)

# Avoid symbolic quadrature of the full expanded polynomial: moments of powers
# of tau are exact, and the Hessian along a line has tau-degree at most two.
tau = sp.symbols("tau")
hess = sp.hessian(F, Y).subs(dict(zip(Y, [y + tau * ui for y, ui in zip(Y, u)])), simultaneous=True)
line = sp.Poly(sp.expand((u.T * hess * u)[0]), tau)
integral = sp.expand(sum(c / ((power[0] + 1) * (power[0] + 2))
                         for power, c in line.terms()))
assert sp.expand(FX - remainder - integral) == 0
assert sp.Poly(integral, *X, *Y).total_degree() <= 4

# Eliminate G and R from the ideal representation, retaining six root equations.
Rcoeff = [0, 0, 0, -Y[4], Y[3], 0]
reduced_H = [sp.expand(H[j + 1] + H[0] * affine_coefficients[j] + H[-1] * Rcoeff[j])
             for j in range(6)]
assert sp.expand(remainder - sum(h * r for h, r in zip(reduced_H, residuals))) == 0
assert all(sp.Poly(h, *X, *Y).total_degree() <= 3 for h in reduced_H)

# Exact integration Gram for A+tau B.
K = sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 6)],
               [sp.Rational(1, 6), sp.Rational(1, 12)]])
assert K.det() == sp.Rational(1, 72)
assert K[0, 0] > 0 and K.det() > 0
a, b = sp.symbols("a b")
assert sp.expand((sp.Matrix([a, b]).T * K * sp.Matrix([a, b]))[0]
                 - (a + b / 3)**2 / 2 - b**2 / 36) == 0

for numerator, denominator in [(1, 2), (7, 3), (41, 1009), (2**127 + 31, 2**83 + 9)]:
    rational_squares(numerator, denominator)

print("PASS: two-gate ideal, gradient, Taylor, Gram-moment, degree, and rational-square checks")
