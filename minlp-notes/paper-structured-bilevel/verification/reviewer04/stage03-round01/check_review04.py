"""Independent exact checks of stage 3; no manuscript/author code imports."""
import itertools
import json
from pathlib import Path
import random
import sympy as s


def qp(Q, a):
    n = Q.rows
    solutions = []
    for status in itertools.product(range(3), repeat=n):
        free = [i for i in range(n) if status[i] == 1]
        z = s.Matrix([int(v == 2) for v in status])
        if free:
            solved = Q.extract(free, free).inv() * (-(a + Q*z).extract(free, [0]))
            for i, value in zip(free, solved):
                z[i] = value
        g = Q*z + a
        if not all(0 <= v <= 1 for v in z):
            continue
        if not all((status[i] == 0 and g[i] >= 0) or
                   (status[i] == 2 and g[i] <= 0) or
                   (status[i] == 1 and g[i] == 0) for i in range(n)):
            continue
        solutions.append(z)
    assert solutions and all(z == solutions[0] for z in solutions)
    return solutions[0]


rng = random.Random(30404)
cases = 24
direction_checks = 0
for case in range(cases):
    B = s.Matrix(3, 3, [s.Rational(rng.randrange(-3, 4), 5) for _ in range(9)])
    Q = s.eye(3) + B.T*B
    H = s.diag(*[s.Rational(rng.randrange(3, 11), 5) for _ in range(3)])
    a = s.Matrix([s.Rational(rng.randrange(-10, 11), 5) for _ in range(3)])
    z, y = qp(Q, a), qp(H, a)
    e, p = z-y, (Q-H)*y
    assert (e.T*Q*e + p.T*e)[0] <= 0
    directions = [s.eye(3)[:, i] for i in range(3)] + [Q[:, i] for i in range(3)]
    directions += [s.Matrix([1, -2, 3])]
    for b in directions:
        left = (b.T*e + b.T*Q.inv()*p/2)[0]
        radius_squared = (b.T*Q.inv()*b)[0]*(p.T*Q.inv()*p)[0]/4
        assert left**2 <= radius_squared
        direction_checks += 1

# Nonstationary threshold-fiber witness: minimizing half the squared norm on
# [0,1]^2, budget 1/4, maximizing z1. The exact adverse point is irrational.
adverse = s.Matrix([1/s.sqrt(2), 0])
assert (adverse.T*adverse)[0]/2 == s.Rational(1, 4)
assert adverse[0] != 0  # original follower stationarity fails in coordinate 1
assert s.simplify(adverse[0] - s.sqrt(2)/2) == 0

# Positive-budget nonattainment identities.
z, c = s.symbols('z c')
rho = s.Rational(1, 16)
h = 3*z**2 - 2*z**3
f = z**2*(1-z)**2 + c*h
assert s.expand(f.subs(c, rho)-rho-(z-1)**2*(z**2-z/8-s.Rational(1,16))) == 0
assert s.expand(s.diff(f, z)-2*z*(1-z)*(1-2*z+3*c)) == 0
endpoint = (1+s.sqrt(17))/16
assert s.simplify(f.subs({c:rho,z:endpoint})-rho) == 0

# A genuine two-dimensional cell: no transitions, explicit overlapping
# vertex-simplex cover, and an indefinite dense perturbation in the radius.
vertices = [s.Matrix(v) for v in itertools.product([0, 1], repeat=2)]
triangles = list(itertools.combinations(range(4), 3))
grid = [s.Matrix(v) for v in itertools.product([s.Rational(i,4) for i in range(5)], repeat=2)]
for point in grid:
    covered = False
    for tri in triangles:
        matrix = s.Matrix.hstack(*[vertices[i].col_join(s.ones(1,1)) for i in tri])
        weights = matrix.inv()*point.col_join(s.ones(1,1))
        if all(w >= 0 for w in weights):
            covered = True
            break
    assert covered

C = -s.Matrix([[s.Rational(1,2),0],[0,s.Rational(1,2)],
               [s.Rational(1,4),s.Rational(1,4)]])
c0 = -s.ones(3,1)/4
H = s.eye(3)
E = s.Matrix([[0,s.Rational(1,256),-s.Rational(1,512)],
              [s.Rational(1,256),0,s.Rational(1,512)],
              [-s.Rational(1,512),s.Rational(1,512),0]])
Q = H+E
sigma, m0, L0, R = s.Rational(1,4), s.Integer(1), s.Integer(1), s.Integer(2)
radius = min(m0/2, sigma/(4*R*max(1/m0,1+L0/m0)))
residual = max(sum(abs(E[i,j]) for j in range(3)) for i in range(3))
assert radius == s.Rational(1,64) and residual <= radius
assert all(Q[:j,:j].det() > 0 for j in range(1,4))
for point in vertices:
    a = c0+C*point
    nominal = -a
    true = -Q.inv()*a
    assert all(sigma <= value <= 1-sigma for value in nominal)
    assert all(sigma/2 <= value <= 1-sigma/2 for value in true)
    assert Q*true+a == s.zeros(3,1)

# A zero residual closed cell has strict interior response only in relative
# interior; F remains valid at its zero-gradient endpoints.
assert qp(s.eye(1),s.Matrix([0])) == s.zeros(1,1)
assert qp(s.eye(1),s.Matrix([-1])) == s.ones(1,1)

result = {'independent_dense_qp_pairs':cases,'exact_directional_checks':direction_checks,
          'irrational_nonstationary_adverse_witness':'sqrt(2)/2, 0',
          'positive_budget_factorization_and_derivative':'passed',
          'leader_dimension':2,'overlapping_triangles':len(triangles),
          'simplex_cover_grid_points':len(grid),'transition_multiplicity':0,
          'neighborhood_radius':str(radius),'dense_residual_infinity_norm':str(residual),
          'all_free_whole_square_vertex_certificate':'passed',
          'zero_gradient_bound_endpoints':'passed'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
