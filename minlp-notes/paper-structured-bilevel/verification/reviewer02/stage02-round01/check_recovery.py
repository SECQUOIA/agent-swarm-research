"""Small independent exact check; not an implementation of general QE."""
from itertools import product, combinations
import sympy as s

a = s.sqrt(2)
locals_ = [[s.Matrix(v) for v in [(0, 0), (1, 0), (0, 1)]],
           [s.Matrix([v]) for v in [0, 1]],
           [s.Matrix([s.Rational(1, 2), s.Rational(1, 3)])]]
maps = [s.diag(a, 1), s.Matrix([1, a]), s.diag(1, a)]
tuples = list(product(*locals_))
images = [sum((w*y for w, y in zip(maps, ys)), s.zeros(2, 1)) for ys in tuples]

def recover(points, target):
    rhs = target.col_join(s.ones(1, 1))
    for count in range(1, 4):
        for subset in combinations(range(len(points)), count):
            mat = s.Matrix.hstack(*(points[j].col_join(s.ones(1, 1)) for j in subset))
            if mat.rank() != count or mat.row_join(rhs).rank() != count:
                continue
            weights = mat.gauss_jordan_solve(rhs)[0].applyfunc(s.simplify)
            if all(v >= 0 for v in weights):
                assert mat*weights == rhs or (mat*weights-rhs).applyfunc(s.simplify).is_zero_matrix
                return subset, weights
    raise AssertionError('No three-point convex representation')

selected = set()
for p, q in product(range(-5, 6), repeat=2):
    direction = s.Matrix([p, q])
    indices = []
    for vertices, w in zip(locals_, maps):
        scores = [(direction.T*w*y)[0] for y in vertices]
        best = 0
        for j in range(1, len(scores)):
            if s.simplify(scores[j]-scores[best]) > 0:
                best = j
        indices.append(best)
    ys = tuple(locals_[i][j] for i, j in enumerate(indices))
    selected.add(next(j for j, t in enumerate(tuples) if t == ys))
selected = sorted(selected)
points = [images[j] for j in selected]
for target in images:
    recover(points, target)
target = sum(images, s.zeros(2, 1))/len(images)
subset, weights = recover(points, target)
recovered = [sum((weights[j]*tuples[selected[idx]][b] for j, idx in enumerate(subset)),
                 s.zeros(len(locals_[b][0]), 1)).applyfunc(s.simplify) for b in range(3)]
assert recovered[0][0] >= 0 and recovered[0][1] >= 0
assert s.simplify(sum(recovered[0])) <= 1
assert 0 <= recovered[1][0] <= 1
assert recovered[2] == locals_[2][0]
assert (sum((w*y for w, y in zip(maps, recovered)), s.zeros(2, 1))-target).applyfunc(s.simplify).is_zero_matrix
for value in list(weights) + [v for y in recovered for v in y]:
    s.QQ.algebraic_field(a).from_sympy(value)
print('Full tuples:', len(tuples), 'support tuples:', len(selected), 'recovery support:', len(subset))
print('All full-product images belong to the selected support hull; recovered tuple is feasible in Q(sqrt(2)).')

x = s.symbols('x')
matrix = s.Matrix([[2, x], [x, 0]])
assert s.expand(matrix.det()) == -x**2
assert matrix.inv()*s.Matrix([2, 0]) == s.Matrix([0, 2/x])
assert s.solve(2*x-2, x) == [1]
z = s.symbols('z')
f = z**2*(1-z)**2
assert s.diff(f, z).subs(z, s.Rational(1, 2)) == 0
assert f.subs(z, s.Rational(1, 2)) == s.Rational(1, 16)
assert f.subs(z, 0) == f.subs(z, 1) == 0
print('Moving-normal determinant and nonglobal stationary midpoint checks passed.')
