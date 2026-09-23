"""Exact algebraic checks for the transformations audited in Stage 3.

These verify identities and a chart-degeneracy regression, not the
complexity theorems or their universal physical correspondence proofs.
Run with Python and SymPy; no numerical solver or tolerance is used.
"""
import sympy as s

q, C1, C2, B, b, z1, z2, v = s.symbols('q C1 C2 B b z1 z2 v')
g1, g2 = C1-q, C2-q
R = b*(B-q)
w1 = g1*(R-g2*(z1+z2))/(C1-C2)
quality_residual = g1*z1 + g2*z2 - R
assert s.factor((w1-g1*z1)*(C1-C2) + g1*quality_residual) == 0

# General vector-coordinate residual after projecting onto beta.
c1, c2, Bp, H1, H2, Hq, BH, w = s.symbols('c1 c2 Bp H1 H2 Hq BH w')
g1p, g2p, Rp = c1-q, c2-q, b*(Bp-q)
a = (H1-Hq)*g2p - (H2-Hq)*g1p
f = g1p*(b*(BH-Hq)*g2p-(H2-Hq)*Rp)
original = (H1-Hq)*w/g1p + (H2-Hq)*(Rp-w)/g2p - b*(BH-Hq)
assert s.factor(original*g1p*g2p - (a*w-f)) == 0
assert s.Poly(a, q, Hq).total_degree() <= 1
assert s.Poly(f, q, Hq).total_degree() <= 2

# Two-vector class masses, eliminating z0 from product mass balance.
z0, z_one = s.symbols('z0 z_one')
W0, W1 = -q*z0, (1-q)*z_one
two_quality = W0+W1-b*(B-q)
outlet_identity = W0-q*b*(B-1)-q*(1-q)*v
assert s.factor(outlet_identity.subs(v,b-z0-z_one)-q*two_quality) == 0

# A row discarded on an open parameter cell can be essential at a zero.
# On rho>0, x<=0 is redundant given rho*x<=0. Keeping only the latter
# and specializing rho=0 admits x=1/2, while the original system rejects it.
rho, x = s.symbols('rho x')
assert (rho*x).subs({rho:1,x:s.Rational(1,2)}) > 0
assert (rho*x).subs({rho:0,x:s.Rational(1,2)}) == 0
assert x.subs(x,s.Rational(1,2)) > 0

print('PASS: scalar outlet interval identity')
print('PASS: full-vector residual identity and affine/quadratic degrees')
print('PASS: two-class shared quadratic identity')
print('PASS: singleton row-selection regression')
