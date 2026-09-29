"""Symbolic checks of determinant elimination and a degenerate limiting family.

Requires SymPy. These finite examples do not validate effective quantifier
elimination, coefficient-height bounds, or the general penalty theorem.
"""
import sympy as sp


def scalar(matrix):
    assert matrix.shape == (1, 1)
    return matrix[0]


def zero(expression):
    assert sp.cancel(expression) == 0, expression


eps, l1, l2, w = sp.symbols('eps l1 l2 w')
variables = (eps, l1, l2, w)
q_matrices = [sp.diag(2, 0), sp.Matrix([[2, 2], [2, 2]]), 2*sp.eye(2)]
a_vectors = [sp.Matrix([1, -2]), sp.Matrix([-1, 3]), sp.zeros(2, 1)]
constants = [sp.Rational(1, 3), sp.Rational(-2, 5), -10]
M = q_matrices[0] + 2*eps*sp.eye(2) + l1*q_matrices[1] + l2*q_matrices[2]
a = a_vectors[0] + l1*a_vectors[1] + l2*a_vectors[2]
Delta = sp.expand(M.det())
p = -M.adjugate()*a
u = p/Delta
for entry in M*p + Delta*a:
    zero(entry)
assert sp.Poly(Delta, *variables).total_degree() <= 2
assert all(sp.Poly(entry, *variables).total_degree() <= 2 for entry in p)
constraints = []
for i in (1, 2):
    Qi, ai, ci = q_matrices[i], a_vectors[i], constants[i]
    Gi = (scalar(p.T*Qi*p)/2 + Delta*scalar(ai.T*p)
          + (ci-eps)*Delta**2)
    qi = scalar(u.T*Qi*u)/2 + scalar(ai.T*u) + ci
    zero(Gi-Delta**2*(qi-eps))
    assert sp.Poly(Gi, *variables).total_degree() <= 5
    assert sp.Poly((l1 if i == 1 else l2)*Gi, *variables).total_degree() <= 6
    constraints.append(Gi)
G0 = (scalar(p.T*q_matrices[0]*p)/2 + Delta*scalar(a_vectors[0].T*p)
      + (constants[0]-w)*Delta**2 + eps*scalar(p.T*p))
q0 = scalar(u.T*q_matrices[0]*u)/2 + scalar(a_vectors[0].T*u) + constants[0]
zero(G0-Delta**2*(q0+eps*scalar(u.T*u)-w))
assert sp.Poly(G0, *variables).total_degree() <= 5

# Original problem: min c+x+y^2 subject to x^2<=0 and x^2+y^2<=4.
# It has no Slater point; Q0 is singular. The relaxed regularized optimum
# for eps=t^2, 0<t<=1/2, is (x,y)=(-t,0), with divergent multiplier
# lambda_1=1/(2t)-t^2 and lambda_ball=0. Only rational arithmetic is used.
t, c = sp.symbols('t c', positive=True)
x, y = sp.symbols('x y')
primal = sp.Matrix([-t, 0])
substitution = {x: primal[0], y: primal[1], eps: t**2}
lam = 1/(2*t)-t**2
regularized_objective = c+x+y**2+eps*(x**2+y**2)
relaxed_constraints = [x**2-eps, x**2+y**2-4-eps]
singular_multipliers = [lam, sp.Integer(0)]
lagrangian = regularized_objective + sum(
    multiplier*constraint
    for multiplier, constraint in zip(singular_multipliers, relaxed_constraints))
singular_M = sp.hessian(lagrangian, (x, y)).subs(substitution)
for coordinate in (x, y):
    zero(sp.diff(lagrangian, coordinate).subs(substitution))
value = sp.expand(regularized_objective.subs(substitution))
zero(value-(c-t+t**4))
assert sp.limit(value, t, 0, dir='+') == c
assert sp.limit(lam, t, 0, dir='+') == sp.oo
for denom in [2, 3, 4, 8, 16, 32]:
    tt = sp.Rational(1, denom)
    # Sylvester's criterion and exact KKT conditions certify the minimum.
    assert singular_M[0, 0].subs(t, tt) > 0
    assert singular_M.det().subs(t, tt) > 0
    for multiplier, constraint in zip(singular_multipliers, relaxed_constraints):
        constraint_value = constraint.subs(substitution).subs(t, tt)
        multiplier_value = multiplier.subs(t, tt)
        assert constraint_value <= 0
        assert multiplier_value >= 0
        assert multiplier_value*constraint_value == 0
    assert value.subs({t: tt, c: sp.Rational(2, 3)}) < sp.Rational(2, 3)

# Reciprocal graph on a slice with two residual coordinates. Enumerate
# valid and invalid t values, including saturation of the smaller coordinate,
# to test both directions of the inequalities-plus-saturation characterization.
reciprocal_cases = 0
for xx in [sp.Rational(0), sp.Rational(1, 3), sp.Rational(1, 2), sp.Rational(1)]:
    residual = [xx+sp.Rational(1, 4), 2*xx-1]
    expected = 1/max(abs(r) for r in residual)
    candidates = {sp.Integer(0), sp.Integer(-1), expected, -expected,
                  expected/2, 2*expected, expected+1}
    for r in residual:
        if r:
            candidates.update({1/r, -1/r})
    for reciprocal in candidates:
        graph_holds = (reciprocal >= 0
                       and all(-1 <= reciprocal*r <= 1 for r in residual)
                       and any(reciprocal*r in (-1, 1) for r in residual))
        assert bool(graph_holds) == (reciprocal == expected)
        reciprocal_cases += 1

print('PASS: two-dimensional adjugate stationarity and all constraint/objective')
print('      numerator identities, determinant/numerator/complementarity degree bounds;')
print('      singular no-Slater family with divergent multipliers at six rational scales;')
print(f'      exact value limit and {reciprocal_cases} two-coordinate reciprocal-graph candidates.')
print('Not checked: general QE or algebraic height/radius bounds; these use cited theorems.')
