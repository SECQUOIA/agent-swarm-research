"""Exactly mean-consistent version of the n = 4 pair-box family of the WALL chain (balanced split, P_1):
  factor 1: delta(-1, s);  factor 2: al delta(-1, c) + (1-al) delta(c, -1);  factor 3: be delta(-1, -1) + (1-be) delta(s, -1),
with c the exact root of u'(c) = 2b in (-1,1) (sympy CRootOf), s rational in (-1, c); al, be from the mean equations.
Value compared with f(x^1) = f(x^3) at 40 digits.  The general-n pair boxes are local copies of this one."""
import sympy as sp
t = sp.symbols("t")
U = [0, sp.Rational(1022, 1000), sp.Rational(189, 1000), sp.Rational(1774, 1000), sp.Rational(1086, 1000)]
Bq = sp.Rational(962, 1000)
u = lambda z: sum(U[k] * z**k for k in range(5))
dpoly = sp.Poly(sp.diff(u(t), t) - 2 * Bq, t)
roots = [r for r in dpoly.real_roots() if -1 < r.evalf(50) < 1]
assert len(roots) == 1
c = roots[0]
s = sp.Rational(233524, 10**6)
al = (c - s) / (1 + c)                     # x2: s = -al + (1-al) c
m3 = al * c - (1 - al)                     # x3 mean in factor 2
be = (s - m3) / (1 + s)                    # factor 3: -be + (1-be) s = m3
F1 = lambda a, b_: u(a) + u(b_) / 2 + Bq * a * b_
F2 = lambda a, b_: u(a) / 2 + u(b_) / 2 + Bq * a * b_
F3 = lambda a, b_: u(a) / 2 + u(b_) + Bq * a * b_
val = F1(-1, s) + al * F2(-1, c) + (1 - al) * F2(c, -1) + be * F3(-1, -1) + (1 - be) * F3(s, -1)
f1 = u(-1) + u(-1) + u(c) + u(-1) + Bq * (1 - c - c)
print("c =", sp.N(c, 20), " al =", sp.N(al, 12), " be =", sp.N(be, 12), " (weights in [0,1]:", bool(0 <= sp.N(al, 30) <= 1 and 0 <= sp.N(be, 30) <= 1), ")")
print("s inside [-1, c]:", bool(-1 < s < sp.N(c, 30)))
print("value - f(x^1) =", sp.N(val - f1, 30))
