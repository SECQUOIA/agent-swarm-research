"""Exact/symbolic checks for the two boundary-output limitation examples.

(1) Weakly complementary example on [1/2,1] x [0,1]^2:
    F = u^2 + w1^2 + w2^2 + 3 w1 w2 + u (w1 - w2),  u = x^2 - 1/2.
    Identity F = 1/2(u^2+w1^2+w2^2) + 1/2(u+w1-w2)^2 + 4 w1 w2, coordinate curvature
    bound L = 12, Hessian at the optimizer indefinite, sign changes of dF/dw_i.
(2) Margin example on [0,1/2]^{n+1} x [0,1/2]:
    G = sum r_i^2 + y^2 + 3 y h,  r_0 = x_0 - 1/4, r_i = x_i - x_{i-1}^2/4,
    h = x_n - x_{n-1}^2/8.  Identity
    G = 1/4(F+y^2) + 3/4(F - r_n^2) + 3/4(r_n+y)^2 + 3/2 y x_n,
    optimizer a_i = 2^{-(4*2^i-2)}, inward derivative 3 a_n/2, curvature bounds,
    growth F >= 9/16 |x-a|^2 on rational samples, and the rectangle sign bound.
Run: python3 -B check_boundary.py
"""
import random
from fractions import Fraction as Fr

import sympy as sp

random.seed(3)

# ---------- (1) weak complementarity ----------
x, w1, w2 = sp.symbols("x w1 w2")
u = x**2 - sp.Rational(1, 2)
F = u**2 + w1**2 + w2**2 + 3 * w1 * w2 + u * (w1 - w2)
ident = sp.Rational(1, 2) * (u**2 + w1**2 + w2**2) + sp.Rational(1, 2) * (u + w1 - w2) ** 2 + 4 * w1 * w2
assert sp.expand(F - ident) == 0
# coordinate curvature on [1/2,1] x [0,1]^2
fxx = sp.expand(sp.diff(F, x, 2))
assert sp.expand(fxx - (12 * x**2 - 2 + 2 * (w1 - w2))) == 0
assert sp.diff(F, w1, 2) == 2 and sp.diff(F, w2, 2) == 2
a = {x: 1 / sp.sqrt(2), w1: 0, w2: 0}
Hs = sp.hessian(F, (x, w1, w2)).subs(a)
v = sp.Matrix([0, 1, -1])
assert (v.T * Hs * v)[0] == -2
assert sp.diff(F, w1).subs({w1: 0, w2: 0}) == u and sp.diff(F, w2).subs({w1: 0, w2: 0}) == -u
# growth: F >= 1/2 ((x-r)^2 + w^2) since (x+r)^2 >= 1 on [1/2,1]
r = 1 / sp.sqrt(2)
assert sp.simplify((sp.Rational(1, 2) + r) ** 2 - 1) > 0
for _ in range(2000):
    xv = Fr(random.randint(0, 600), 1200) + Fr(1, 2)
    a1 = Fr(random.randint(0, 100), 100)
    a2 = Fr(random.randint(0, 100), 100)
    uv = xv * xv - Fr(1, 2)
    Fv = uv**2 + a1**2 + a2**2 + 3 * a1 * a2 + uv * (a1 - a2)
    assert Fv >= (uv**2 + a1**2 + a2**2) / 2

# ---------- (2) margin example ----------
for n in (1, 2, 3, 4):
    X = sp.symbols(f"x0:{n + 1}")
    y = sp.Symbol("y")
    rr = [X[0] - sp.Rational(1, 4)] + [X[i] - X[i - 1] ** 2 / 4 for i in range(1, n + 1)]
    Fn = sum(t**2 for t in rr)
    h = X[n] - X[n - 1] ** 2 / 8
    G = Fn + y**2 + 3 * y * h
    rhs = sp.Rational(1, 4) * (Fn + y**2) + sp.Rational(3, 4) * (Fn - rr[n] ** 2) + sp.Rational(3, 4) * (rr[n] + y) ** 2 + sp.Rational(3, 2) * y * X[n]
    assert sp.expand(G - rhs) == 0
    av = [sp.Rational(1, 4)]
    for i in range(1, n + 1):
        av.append(av[-1] ** 2 / 4)
    for i in range(n + 1):
        assert av[i] == sp.Rational(1, 2 ** (4 * 2**i - 2))
    sub = {X[i]: av[i] for i in range(n + 1)}
    sub[y] = 0
    assert G.subs(sub) == 0
    assert sp.diff(G, y).subs(sub) == sp.Rational(3, 2) * av[n]
    # second derivatives: d2/dx_i^2 G = 2 + 3/4 x_i^2 - x_{i+1} (i<n-1), with -3y/4 extra at i = n-1
    for i in range(n + 1):
        d2 = sp.expand(sp.diff(G, X[i], 2))
        if i < n - 1:
            assert sp.expand(d2 - (2 + sp.Rational(3, 4) * X[i] ** 2 - X[i + 1])) == 0
        elif i == n - 1:
            assert sp.expand(d2 - (2 + sp.Rational(3, 4) * X[i] ** 2 - X[i + 1] - sp.Rational(3, 4) * y)) == 0
        else:
            assert d2 == 2
    assert sp.diff(G, y, 2) == 2
    # Hessian minor in (x_n, y) at the optimizer is indefinite
    Hm = sp.hessian(G, (X[n], y)).subs(sub)
    assert Hm.det() == 4 - 9
    # growth of F_n on rational samples (exact)
    fn = sp.lambdify(X, Fn, modules=[{"Rational": Fr}])
    for _ in range(300):
        pt = [Fr(random.randint(0, 64), 128) for _ in range(n + 1)]
        val = sum(((pt[0] - Fr(1, 4)) ** 2,)) + sum((pt[i] - pt[i - 1] ** 2 / 4) ** 2 for i in range(1, n + 1))
        d2 = sum((pt[i] - Fr(av[i].p, av[i].q)) ** 2 for i in range(n + 1))
        assert val >= Fr(9, 16) * d2
    # rectangle sign bound: min over box of dG/dy = 3(l_n - u_{n-1}^2/8) at y=0
    # any box containing a with that minimum >= 0 has a_n/2 <= l_n <= a_n
    an = Fr(av[n].p, av[n].q)
    anm1 = Fr(av[n - 1].p, av[n - 1].q)
    assert anm1 * anm1 / 8 == an / 2
print("boundary limitation examples checked (symbolic identities, curvature, growth samples, minors)")
