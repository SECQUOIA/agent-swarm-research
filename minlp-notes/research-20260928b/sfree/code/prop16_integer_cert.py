"""Exact checks for Proposition 16 added after the recheck: the integer certificate (from the recheck)
and the far-face near-contact min q = 31/2560 on the edge [sbar, v2]."""
import sympy as sp
R = sp.Rational
sb = sp.Matrix([-2, 3, 2]); v1 = sp.Matrix([0, 0, 0]); v2 = sp.Matrix([6, -2, R(1, 4)]); v3 = sp.Matrix([1, R(-5, 2), R(1, 2)])
q = lambda p: p[2] - p[0] * p[1]
s = sp.symbols('s')
e = sp.expand(q(sb + s * (v2 - sb)))
sc = sp.solve(sp.diff(e, s), s)[0]
print('edge [sbar, v2]: q minimized at s =', sc, ', value', e.subs(s, sc))
M = lambda p: sp.Matrix([[p[2], p[0]], [p[1], 1]])
Y = [sp.Matrix([[92, -75], [-75, 64]]), sp.Matrix([[726, 89], [89, 12]]), sp.Matrix([[96, -64], [-64, 45]]), sp.Matrix([[20, 16], [16, 16]])]
tot = sp.zeros(2, 2); ok = True
for name, p, Yv in zip(('sbar', 'v1', 'v2', 'v3'), (sb, v1, v2, v3), Y):
    prod = M(p) * Yv; tot += prod
    ok &= Yv[0, 0] > 0 and Yv.det() > 0
    print('%-4s M(v)Y_v = %s   Y11 = %s  det Y = %s' % (name, prod.tolist(), Yv[0, 0], Yv.det()))
print('sum =', tot.tolist())
print('ALL PASS' if ok and tot == sp.zeros(2, 2) and e.subs(s, sc) == R(31, 2560) else 'FAIL')
