"""Exact certificates for the two-variable degree-four convex QCQP example."""

import sympy as sp


lam, value = sp.symbols("lam value")
x = 2 / (1 + 2 * lam)
y = 2 / (1 + 4 * lam)
constraint_numerator = sp.together(x**2 + 2 * y**2 - 1).as_numer_denom()[0]
multiplier_polynomial = (
    64 * lam**4 + 96 * lam**3 - 44 * lam**2 - 52 * lam - 11
)
assert sp.expand(constraint_numerator + multiplier_polynomial) == 0

objective = (x**2 + y**2) / 2 - 2 * x - 2 * y
value_relation = sp.together(value - objective).as_numer_denom()[0]
value_polynomial = (
    64 * value**4 + 160 * value**3 + 1588 * value**2 - 3036 * value - 12599
)
resultant = sp.resultant(constraint_numerator, value_relation, lam)
assert sp.expand(resultant - 2**24 * value_polynomial) == 0

# Degree-four irreducibility criterion over F_3: all roots lie in F_81,
# while none lies in the only proper maximal subfield F_9.
p = sp.Poly(value_polynomial, value, modulus=3)
assert p.as_expr() == value**4 + value**3 + value**2 + 1
assert sp.rem(sp.Poly(value**81 - value, value, modulus=3), p).is_zero
assert sp.gcd(p, sp.Poly(value**9 - value, value, modulus=3)).degree() == 0

print("PASS: exact KKT elimination and degree-four irreducibility certificate")
