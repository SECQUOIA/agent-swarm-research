"""Independent finite checks of stage 2 proof boundaries; not a QE solver."""
from itertools import combinations, product
from pathlib import Path
import json
import sympy as s


def nonnegative(value):
    result = s.simplify(value).is_nonnegative
    assert result is not None, value
    return result


# Redundant equalities and inequalities, with a lower-dimensional local block.
E = s.Matrix([[1, 1], [2, 2]])
e = s.Matrix([1, 2])
G = s.Matrix([[-1, 0], [0, -1], [1, 0], [0, 1], [-2, 0]])
h = s.Matrix([0, 0, 1, 1, 0])
local_cases = 0
for q1, q2 in product(range(-3, 4), repeat=2):
    q = s.Matrix([q1, q2])
    first = min(s.Integer(1), max(s.Integer(0), s.Rational(1 + q2 - q1, 2)))
    expected = s.Matrix([first, 1 - first])
    valid = []
    for J in [()] + [(i,) for i in range(G.rows)]:
        V = E[:1, :].col_join(G[list(J), :]) if J else E[:1, :]
        if V.rank() != V.rows:
            continue
        rhs = e[:1, :].col_join(h[list(J), :]) if J else e[:1, :]
        M = s.eye(2).row_join(V.T).col_join(V.row_join(s.zeros(V.rows)))
        sol = M.inv() * (-q).col_join(rhs)
        y = sol[:2, :]
        if E * y != e or not all(nonnegative(v) for v in h - G * y):
            continue
        if not all(nonnegative(sol[3 + j]) for j in range(len(J))):
            continue
        assert y == expected
        valid.append(y)
    assert valid
    local_cases += 1

# Algebraic core x=sqrt(2), rational input boxes, and three scalar blocks.
# The second interval endpoint is x inside a fixed [0,2] box.
alpha = s.sqrt(2)
lengths = [s.Integer(1), alpha, s.Integer(2)]
columns = [s.Matrix([1, 0]), s.Matrix([0, 1]), s.Matrix([1, -1])]
all_tuples = list(product(*[(s.Integer(0), bound) for bound in lengths]))
directions = [s.Matrix(v) for v in product(range(-2, 3), repeat=2)]
selected = set()
for direction in directions:
    # First maximizer chooses zero on a tied endpoint score.
    selected.add(tuple(lengths[i] if (direction.dot(columns[i]) > 0) else s.Integer(0)
                       for i in range(3)))
tuples = sorted(selected, key=str)
aggregate = lambda z: sum((columns[i] * z[i] for i in range(3)), s.zeros(2, 1))
images = [aggregate(z) for z in tuples]


def recover(target):
    for count in range(1, 4):
        for subset in combinations(range(len(images)), count):
            lifted = s.Matrix.hstack(*[images[j].col_join(s.ones(1, 1)) for j in subset])
            if lifted.rank() != count:
                continue
            try:
                weights, params = lifted.gauss_jordan_solve(target.col_join(s.ones(1, 1)))
            except ValueError:
                continue
            assert params.rows == 0
            if not all(nonnegative(v) for v in weights):
                continue
            z = [s.simplify(sum(weights[t] * tuples[j][b] for t, j in enumerate(subset)))
                 for b in range(3)]
            assert all(nonnegative(z[b]) and nonnegative(lengths[b] - z[b]) for b in range(3))
            assert all(s.simplify(v) == 0 for v in aggregate(z) - target)
            assert s.simplify(sum(weights) - 1) == 0
            # Membership in the existing field, rather than unrelated radicals.
            for value in [*weights, *z]:
                s.to_number_field(value, alpha)
            return subset, weights, z
    raise AssertionError(target)


# Checking all original vertex sums proves hull coverage for this finite example.
for z in all_tuples:
    recover(aggregate(z))
target = aggregate([s.Rational(1, 3), alpha / 2, s.Rational(4, 3)])
subset, weights, z = recover(target)

# Moving-rank and global-versus-stationary checks from the examples.
x, y = s.symbols('x y')
M = s.Matrix([[1, x], [x, 0]])
assert M.det() == -x**2
assert M.subs(x, 0).det() == 0
assert M.subs(x, 1).inv() * s.Matrix([1, 0]) == s.Matrix([0, 1])
f = y**2 * (1-y)**2
stationary = s.solve(s.diff(f, y), y)
assert stationary == [0, s.Rational(1, 2), 1]
assert [f.subs(y, v) for v in stationary] == [0, s.Rational(1, 16), 0]

result = {
    'redundant_local_block_cases': local_cases,
    'support_tuples': len(tuples),
    'original_vertex_sums_checked': len(all_tuples),
    'algebraic_target': [str(v) for v in target],
    'support_subset': list(subset),
    'weights': [str(s.simplify(v)) for v in weights],
    'recovered_blocks': [str(v) for v in z],
    'common_field': 'Q(sqrt(2))',
    'moving_rank': 'passed',
    'nonglobal_stationary_exclusion': 'passed',
}
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
