"""Exact identities for the native convex quadratic irrational singleton."""

import sympy as sp

x, y, r = sp.symbols("x y r")
minimal = sp.Poly(r**3 - 2, r)
q = [x**2 - y, y**2 - 2*x, (x - y)**2 - 2*x - y + 4]
weights = [2*r - 1, r**2 - 1, sp.Integer(1)]
point = {x: r, y: r**2}


def reduce_root(expression):
    return sp.Poly(sp.expand(expression), r).rem(minimal).as_expr()


assert all(reduce_root(f.subs(point)) == 0 for f in q)
matrix = sp.Matrix([[2*r, -1], [-1, r**2]])
displacement = sp.Matrix([x - r, y - r**2])
aggregate = sum(a*f for a, f in zip(weights, q))
assert reduce_root(aggregate - (displacement.T*matrix*displacement)[0]) == 0
assert reduce_root(matrix.det()) == 3
assert sp.Rational(5, 4)**3 < 2 < sp.Rational(4, 3)**3

# The three quadratic-part matrices are PSD, rank one, and independent.
hessians = [sp.hessian(f, (x, y))/2 for f in q]
assert all(h.is_positive_semidefinite and h.rank() == 1 for h in hessians)
assert sp.Matrix([[h[0, 0], h[0, 1], h[1, 1]] for h in hessians]).rank() == 3

ellipsoids = [3*f + sum(q) for f in q]
total_weight = sum(weights)
ellipse_weights = [(w - total_weight/6)/3 for w in weights]
assert sp.expand(sum(w*f for w, f in zip(ellipse_weights, ellipsoids)) - aggregate) == 0
expected_minima = [-sp.Rational(53, 36), -sp.Rational(101, 9), -sp.Rational(449, 36)]
for f, expected in zip(ellipsoids, expected_minima):
    h = sp.hessian(f, (x, y))/2
    assert h.is_positive_definite and h.det() == 9
    linear = sp.Matrix([sp.diff(f, v).subs({x: 0, y: 0}) for v in (x, y)])
    center = -h.inv()*linear/2
    assert sp.expand(f).subs({x: center[0], y: center[1]}) == expected

# Each ellipse-weight numerator is positive on [5/4,4/3].
numerators = [sp.expand(18*w) for w in ellipse_weights]
assert numerators == [10*r-r**2-5, 5*r**2-2*r-5, 7-2*r-r**2]
assert numerators[0].subs(r, sp.Rational(5, 4)) == sp.Rational(95, 16)
assert numerators[1].subs(r, sp.Rational(5, 4)) == sp.Rational(5, 16)
assert numerators[2].subs(r, sp.Rational(4, 3)) == sp.Rational(23, 9)
for polynomial, sign in zip(numerators, (1, 1, -1)):
    derivative = sp.diff(polynomial, r)
    assert sp.degree(derivative, r) <= 1
    assert all(sign*derivative.subs(r, endpoint) > 0
               for endpoint in (sp.Rational(5, 4), sp.Rational(4, 3)))

print("Exact singleton aggregate, Hessian span, and three ellipsoids verified.")
