"""Focused exact checks; not a proof or implementation of the smooth theorem."""
from fractions import Fraction as F
from itertools import product
import sympy as sp

x, y, t, p, q, dx, dy = sp.symbols('x y t p q dx dy')
f = (x*x-y*y)/t
hessian = sp.hessian(f, (x, y, t))
assert sp.simplify(hessian.det()) == 0
assert sp.simplify(hessian[:2, :2].det()) == -4/t**2
assert all(sp.simplify(v) == 0 for v in hessian*sp.Matrix([x, y, t]))
ell = p*x+q*y-(p*p-q*q)*t/4
fiber = {x:p*t/2, y:-q*t/2}
assert sp.simplify((f-ell).subs(fiber, simultaneous=True)) == 0
assert all(sp.simplify(sp.diff(f-ell, v).subs(fiber, simultaneous=True)) == 0
           for v in (x, y, t))
assert sp.simplify((f-ell).subs({x:p*t/2+dx, y:-q*t/2+dy}, simultaneous=True)
                   -(dx*dx-dy*dy)/t) == 0

# The bound applies throughout tubes, including parameter values outside a
# selected parameter cell. Both transverse directions have opposite curvature.
tubes = 0
for tv, pv, qv, dv, ev in product(
        (F(1), F(3,2), F(2)), (F(-2), F(0), F(3)),
        (F(-1), F(2)), (F(-1,8), F(0), F(1,8)),
        (F(-1,8), F(0), F(1,8))):
    xv, yv = pv*tv/2+dv, -qv*tv/2+ev
    remainder = (xv*xv-yv*yv)/tv-(pv*xv+qv*yv-(pv*pv-qv*qv)*tv/4)
    assert remainder == (dv*dv-ev*ev)/tv
    assert abs(remainder) <= dv*dv+ev*ev
    tubes += 1

# For integral beta the four perspective-product inequalities leave exactly
# v=t*beta. Check their interval intersection with non-unit positive bounds.
products = 0
for lower, upper in ((F(1,7),F(9,5)), (F(3),F(3)), (F(1,2),F(7))):
    for k in range(33):
        tv = lower+(upper-lower)*F(k,32)
        for bit in (0,1):
            low = max(lower*bit, tv-upper*(1-bit))
            high = min(upper*bit, tv-lower*(1-bit))
            assert low == high == tv*bit
            products += 1

# Row homogenization is algebraically exact with an arbitrarily large
# continuous auxiliary; there is no bound-dependent continuous product gadget.
rows = 0
for tv, input_v, output_v, aux, bit in product(
        (F(1,7),F(3,2),F(9)), (F(-1),F(2,3)),
        (F(-5),F(11,9)), (F(-10**60),F(10**60)), (0,1)):
    original = 2*input_v-3*output_v+5*aux+7*bit-F(13,11)
    scaled = 2*(tv*input_v)-3*(tv*output_v)+5*(tv*aux)+7*(tv*bit)-tv*F(13,11)
    assert scaled == tv*original
    assert (scaled <= 0) == (original <= 0)
    rows += 1

print(f'PASS: symbolic indefinite rank-two affine-fiber identities, {tubes} exact tube points, '
      f'{products} perspective-product sections, {rows} homogenized rows')
