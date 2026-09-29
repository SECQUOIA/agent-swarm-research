"""Exact stress cases for ordered coefficient extraction; not a proof checker."""

import sympy as sp


eps, delta, beta, zeta, w, lam, u = sp.symbols(
    "eps delta beta zeta w lam u"
)


def lowest_coefficient(poly, parameter):
    expanded = sp.Poly(sp.expand(poly), parameter)
    powers = [monomial[0] for monomial, coefficient in expanded.terms() if coefficient]
    assert powers
    return sp.expand(expanded.nth(min(powers)))


# The two ordered limits cannot be replaced by an arbitrary diagonal path.
relation = (eps + delta) * w - eps
inner_relation = lowest_coefficient(relation, delta)
outer_relation = lowest_coefficient(inner_relation, eps)
assert sp.expand(outer_relation - (w - 1)) == 0
ratio = eps / (eps + delta)
assert sp.limit(sp.limit(ratio, delta, 0), eps, 0) == 1
assert sp.limit(sp.limit(ratio, eps, 0), delta, 0) == 0
assert sp.simplify(ratio.subs(delta, eps)) == sp.Rational(1, 2)

# Lowest coefficients can vanish identically at a fixed outer parameter.
exceptional_relation = (eps - 1) * (w - eps) + delta * (w - 2)
exceptional_inner = lowest_coefficient(exceptional_relation, delta)
assert exceptional_inner.subs(eps, 1) == 0
assert sp.solve(exceptional_relation.subs(eps, 1), w) == [2]
assert lowest_coefficient(exceptional_inner, eps) == -w

# A permanent undefined-value root forces the auxiliary zeta extraction.
# G=lambda(lambda-c), A=lambda, B=lambda^2; deform G by beta lambda^3.
c = 1 + eps + delta
mul_lam = sp.Matrix([[0, 0, 0], [1, 0, c / beta], [0, 1, -1 / beta]])
mul_a = mul_lam
mul_b = mul_lam**2
scaled = beta**2 * (w * mul_a - mul_b - zeta * sp.eye(3))
determinant = sp.expand(scaled.det())
assert determinant.subs(zeta, 0) == 0
after_zeta = lowest_coefficient(determinant, zeta)
after_beta = lowest_coefficient(after_zeta, beta)
assert sp.expand(after_beta.subs(w, c)) == 0
after_delta = lowest_coefficient(after_beta, delta)
after_eps = lowest_coefficient(after_delta, eps)
assert after_eps != 0
assert after_eps.subs(w, 1) == 0

# A rational affine chart must retain the original-coordinate squared norm.
original_norm = (1 + u) ** 2 + (2 * u) ** 2
canonical_parameter = sp.solve(sp.diff(original_norm, u), u)
assert canonical_parameter == [-sp.Rational(1, 5)]
assert tuple(expression.subs(u, canonical_parameter[0]) for expression in (1 + u, 2 * u)) == (
    sp.Rational(4, 5),
    -sp.Rational(2, 5),
)
assert sp.solve(sp.diff(u**2, u), u) == [0]

print("PASS: ordered limits, exceptional specialization, undefined-value factor, original norm")
