"""Targeted exact checks for the nonconvex Hessian-span proof audit.

These finite checks do not establish the generic incidence theorem or NP bound.
"""
from itertools import product
import sympy as sp

count = 0
for d in range(1, 5):
    u = sp.symbols(f'u0:{d}')
    for s in range(d + 1):
        multipliers = sp.symbols(f'l0:{s}')
        constraints = [u[i] ** 2 - 1 for i in range(s)]
        objective = sum(t * t for t in u) + sum(u[:s])
        lagrangian = objective + sum(multipliers[i] * constraints[i] for i in range(s))
        hessian = sp.hessian(lagrangian, u)
        gradient = sp.Matrix([[sp.diff(f, t) for t in u] for f in constraints]) if s else sp.zeros(0, d)
        bordered = hessian.row_join(gradient.T).col_join(gradient.row_join(sp.zeros(s, s)))
        for signs in product((-1, 1), repeat=s):
            assignment = {u[i]: signs[i] if i < s else 0 for i in range(d)}
            assignment.update({multipliers[i]: -1 - sp.Rational(1, 2 * signs[i]) for i in range(s)})
            assert all(sp.diff(lagrangian, t).subs(assignment) == 0 for t in u)
            assert all(f.subs(assignment) == 0 for f in constraints)
            m = hessian.subs(assignment)
            g = gradient.subs(assignment)
            b = bordered.subs(assignment)
            assert m.det() != 0 and b.det() != 0
            assert b.det() == m.det() * (-g * m.inv() * g.T).det()
            count += 1
print(f'PASS: {count} exact genericity-witness KKT points, including empty active sets.')

# LICQ plus invertible indefinite M alone does not imply reduced nonsingularity.
m = sp.diag(1, -1)
g = sp.Matrix([[1, 1]])
b = m.row_join(g.T).col_join(g.row_join(sp.zeros(1, 1)))
assert m.det() != 0 and g.rank() == 1
assert (g * m.inv() * g.T)[0, 0] == 0 and b.det() == 0
print('PASS: the bordered-KKT hypothesis is independently necessary for this proof route.')

# The inactive-row deletion obstruction uses the correct global endpoint minimum.
x = sp.symbols('x')
squared_norm = sp.expand(x*x + 4 - 4*(x - 2)**2)
assert squared_norm == -3*x*x + 16*x - 12
assert sp.diff(squared_norm, x, 2) == -6
assert squared_norm.subs(x, sp.Rational(5, 2)) == sp.Rational(37, 4)
assert squared_norm.subs(x, 3) == 9
assert squared_norm.subs(x, 1) == 1
print('PASS: ellipse cap minimum 9 versus retained-ellipse minimum 1.')
