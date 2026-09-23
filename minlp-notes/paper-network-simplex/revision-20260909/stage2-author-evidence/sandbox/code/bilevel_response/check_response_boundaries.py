"""Exact checks of two fragile compressed-response boundary cases.

The theorem proof is symbolic; these examples specifically exercise rank
changes in selected constraint normals and nonglobal follower KKT points.
"""
import sympy as sp

x, z = sp.symbols('x z', real=True)

# Moving equality x*z=0, box [0,1], positive local quadratic z^2/2-z.
# The equality-active KKT branch is valid only when its determinant != 0.
M = sp.Matrix([[1, x], [x, 0]])
rhs = sp.Matrix([1, 0])
delta = sp.factor(M.det())
denominator = sp.factor(delta**2)
numerators = sp.simplify(delta * M.adjugate() * rhs)
assert delta == -x**2
assert denominator == x**4
assert numerators == sp.Matrix([0, x**3])
assert sp.simplify(M * numerators - denominator * rhs) == sp.zeros(2, 1)
for leader in [sp.Rational(1, 100), sp.Rational(1, 2), sp.Integer(1)]:
    assert denominator.subs(x, leader) > 0
    assert (numerators[0] / denominator).subs(x, leader) == 0
assert denominator.subs(x, 0) == 0  # This branch must be rejected here.
# The empty equality subset supplies z=1, valid for all original rows at x=0.
empty_branch = sp.Integer(1)
assert (x * empty_branch).subs(x, 0) == 0
assert (empty_branch**2 / 2 - empty_branch) < 0

# At x=0 the quartic follower has three KKT points, but only two global optima.
f = z**2 * (1-z)**2 + x*z
stationary = sp.solve(sp.diff(f, z).subs(x, 0), z)
assert stationary == [0, sp.Rational(1, 2), 1]
values = {point: sp.factor(f.subs({x: 0, z: point})) for point in stationary}
assert values == {0: 0, sp.Rational(1, 2): sp.Rational(1, 16), 1: 0}
a = sp.Integer(1)
phi = z**2*(1-z)**2-z**2/2+x*z
assert sp.expand(a*z**2/2+phi-f) == 0
# At positive x, nonnegativity of both terms makes z=0 uniquely optimal.
for leader in [sp.Rational(1, 100), sp.Rational(1, 2), sp.Integer(1)]:
    assert f.subs({x: leader, z: 0}) == 0
    assert f.subs({x: leader, z: 1}) == leader
print('PASS: guarded moving-normal branches and nonglobal KKT exclusion.')
