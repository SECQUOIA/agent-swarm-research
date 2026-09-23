"""Exact rank and anisotropic Taylor check for a quartic graph example."""
import sympy as sp

z1, z2, w, r = x = sp.symbols('z1 z2 w r')
f = z1*w**3 + z2*(w+w**2) + w*r**2 + r**4
h = sp.hessian(f, x)
assert h[:2, :2] == sp.zeros(2)
assert h[:2, 3:] == sp.zeros(2, 1)
assert h.subs(dict.fromkeys(x, 1)).rank() == 3
assert sp.factor(h.det()) == 0

# Prefix coordinates in Z have zero bits, so their prefix equals zero.
a1, a2, aw, ar = a = sp.symbols('a1 a2 aw ar')
d1, d2, dw, dr = delta = sp.symbols('d1 d2 dw dr')
fa = f.subs(dict(zip(x, a)), simultaneous=True)
linear = fa + sum(sp.diff(f, xi).subs(dict(zip(x, a)), simultaneous=True)*di
                  for xi, di in zip(x, delta))
remainder = sp.expand(f.subs(dict(zip(x, [ai+di for ai, di in zip(a, delta)])), simultaneous=True)-linear)
poly = sp.Poly(remainder, *delta)
weights = [sp.Rational(0), sp.Rational(0), sp.Rational(1), sp.Rational(1, 2)]
for exponents, coefficient in poly.terms():
    assert coefficient != 0
    assert sum(e*weight for e, weight in zip(exponents, weights)) >= 1
assert len(poly.terms()) == 12
print('PASS: quartic Hessian rank3, forbidden blocks zero, all12 Taylor residual terms have precision weight>=1')
