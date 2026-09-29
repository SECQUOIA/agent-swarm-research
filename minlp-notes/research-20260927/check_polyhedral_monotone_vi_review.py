"""Exact checks of a nonpotential cubic VI and its affine restriction.

These finite symbolic checks do not implement PosSLP, prove the general
existence theorem, or test the asymptotic gap and LP operation bounds.
"""

import sympy as sp


x = sp.Matrix(sp.symbols("x0:3"))
v = sp.Matrix(sp.symbols("v0:3"))
skew = sp.Matrix([[0, -2, 1], [2, 0, -3], [-1, 3, 0]])
normal = sp.Matrix([1, 2, 1])
p = -normal / 6
base = (1 + x.dot(x)) * x + skew * x
offset = base.subs(dict(zip(x, p))) - normal
mapping = base - offset
jacobian = mapping.jacobian(x)

assert skew + skew.T == sp.zeros(3)
assert mapping.subs(dict(zip(x, p))) == normal
assert sp.expand(
    (v.T * jacobian * v)[0]
    - (1 + x.dot(x)) * v.dot(v)
    - 2 * x.dot(v) ** 2
) == 0
assert jacobian - jacobian.T == 2 * skew
print("PASS globally strongly monotone cubic with nonzero skew Jacobian")

# The polyhedron is x0 + 2*x1 + x2 = -1, x0 <= 0, with redundancy.
rows = [normal.T, -normal.T, 2 * normal.T,
        sp.Matrix([[1, 0, 0]]), sp.zeros(1, 3), sp.zeros(1, 3)]
rhs = [sp.Integer(-1), sp.Integer(1), sp.Integer(-2),
       sp.Integer(0), sp.Integer(0), sp.Integer(1)]
slacks = [b - (a * p)[0] for a, b in zip(rows, rhs)]
active = [i for i, slack in enumerate(slacks) if slack == 0]
assert active == [0, 1, 2, 4]
assert all(slack >= 0 for slack in slacks)

y = sp.Matrix(sp.symbols("y0:2"))
translation = sp.Matrix([-1, 0, 0])
chart = sp.Matrix([[-2, -1], [1, 0], [0, 1]])
chart_point = translation + chart * y
assert chart.T * chart - sp.eye(2) == sp.Matrix([[4, 2], [2, 1]])
assert normal.T * chart == sp.zeros(1, 2)
assert normal.dot(translation) == -1
restricted = sp.simplify(chart.T * mapping.subs(dict(zip(x, chart_point))))
root = sp.Matrix([p[1], p[2]])
assert restricted.subs(dict(zip(y, root))) == sp.zeros(2, 1)
restricted_jacobian = restricted.jacobian(y)
assert restricted_jacobian - restricted_jacobian.T == 2 * chart.T * skew * chart
assert restricted_jacobian - restricted_jacobian.T != sp.zeros(2)
w = sp.Matrix(sp.symbols("w0:2"))
assert sp.expand(
    (w.T * restricted_jacobian * w)[0]
    - (1 + chart_point.dot(chart_point)) * (chart * w).dot(chart * w)
    - 2 * chart_point.dot(chart * w) ** 2
) == 0
print("PASS two-dimensional affine restriction preserves monotonicity and nonpotentiality")

# Both signs of the equality normal are active. All tangent directions
# annihilate it, so T(p) pairs to zero with every feasible displacement.
assert mapping.subs(dict(zip(x, p))).T * chart == sp.zeros(1, 2)
assert all(slacks[i] > 0 for i in range(len(rows)) if i not in active)
print("PASS full active mask and exact constrained VI certificate")

# A distinct feasible boundary point is rejected by a rational tangent
# direction. This checks the sign orientation independently.
q = p + chart[:, 0] / 20
q_slacks = [b - (a * q)[0] for a, b in zip(rows, rhs)]
q_active = [i for i, slack in enumerate(q_slacks) if slack == 0]
assert all(slack >= 0 for slack in q_slacks)
assert q_active == active
direction = p - q
assert max(abs(t) for t in direction) <= 1
assert all((rows[i] * direction)[0] <= 0 for i in q_active)
pairing = mapping.subs(dict(zip(x, q))).dot(direction)
assert pairing < 0
assert pairing <= -direction.dot(direction)
print(f"PASS incorrect point rejected by tangent direction: pairing {pairing}")
