"""Exact boundary checks for convex-quartic-minimal-sos-length.md.

These checks verify examples and an illustrative flat-direction reduction.
They do not verify the universal theorem or its topological degree step.
"""

import sympy as sp


for n in range(1, 6):
    x = sp.symbols(f"x0:{n}")
    vector = sp.Matrix(x)
    radius_squared = sum(t**2 for t in x)
    sharp = radius_squared**2 + radius_squared
    expected = 8 * vector * vector.T + (4 * radius_squared + 2) * sp.eye(n)
    assert sp.hessian(sharp, x) == expected
    positive_minimum = (1 + radius_squared) ** 2
    assert sp.hessian(positive_minimum, x) == (
        8 * vector * vector.T + 4 * (1 + radius_squared) * sp.eye(n)
    )
    assert sharp.subs(dict.fromkeys(x, 0)) == 0
    assert positive_minimum.subs(dict.fromkeys(x, 0)) == 1
print("Sharp and positive-minimum example Hessians: n=1,...,5 passed.")

x, y = sp.symbols("x y", real=True)
nonconvex = x**2 + (y - x**2) ** 2
hessian = sp.hessian(nonconvex, (x, y))
assert hessian.subs({x: 0, y: 0}) == 2 * sp.eye(2)
assert hessian[0, 0].subs({x: 0, y: 1}) == -2
print("Unique regular zero without convexity: exact Hessian check passed.")

# A square map whose leading quadratic part has a flat input direction.
# Removing that direction leaves a proper scalar quadratic with two roots.
# The two regular zeros have opposite Jacobian signs, as degree parity predicts.
w, v = sp.symbols("w v", real=True)
q = sp.Matrix([w**2 + w, 2 * v + 3 * w + 1])
v0 = -(3 * w + 1) / 2
reduced = w**2 + w
assert sp.expand(q.dot(q) - 4 * (v - v0) ** 2 - reduced**2) == 0
assert sp.simplify(q[1].subs(v, v0)) == 0
jacobian = q.jacobian((w, v))
zero1, zero2 = {w: 0, v: -sp.Rational(1, 2)}, {w: -1, v: 1}
assert q.subs(zero1) == sp.zeros(2, 1)
assert q.subs(zero2) == sp.zeros(2, 1)
assert jacobian.det().subs(zero1) == 2
assert jacobian.det().subs(zero2) == -2
assert sp.diff(reduced**2, w, 2).subs(w, -sp.Rational(1, 2)) == -1
print("Flat-direction completion and opposite regular-zero signs passed.")
