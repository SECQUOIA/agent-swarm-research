"""Independent SymPy audit of the star certificate; read only literal data."""

import ast
from itertools import combinations
from pathlib import Path

import sympy as sp


source = Path(__file__).with_name('check_star_counterexample.py')
tree = ast.parse(source.read_text())
data = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1:
        target = node.targets[0]
        if isinstance(target, ast.Name) and target.id in {'A', 'R'}:
            data[target.id] = sp.Matrix(ast.literal_eval(node.value))
A, R = data['A'], data['R']
Y = R / 10**6
assert A == A.T and Y == Y.T and Y[0, 0] == 1
principal_minors = [
    R.extract(indices, indices).det()
    for size in range(1, 7)
    for indices in combinations(range(6), size)
]
assert len(principal_minors) == 63 and all(v > 0 for v in principal_minors)
slacks = []
for i in range(1, 6):
    assert 0 < Y[0, i] < 4
    for j in range(i, 6):
        slacks.extend([Y[i, j], 4*Y[0, i] - Y[i, j],
                       4*Y[0, j] - Y[i, j],
                       Y[i, j] - 4*(Y[0, i]+Y[0, j]) + 16])
assert min(slacks) == sp.Rational(1, 250000)
assert sp.trace(A*Y) == -sp.Rational(9337, 250000)

t, a, b, c, d = sp.symbols('t a b c d')
z = sp.Matrix([1, t, a, b, c, d])
q = sp.expand((z.T*A*z)[0])
leaves = [a, b, c, d]
zero_leaves = {v: 0 for v in leaves}
linear = [sp.diff(q, v).subs(zero_leaves) for v in leaves]
assert [sp.diff(q, v, 2) for v in leaves] == [1250]*4
breaks = sorted([sp.S(0), sp.S(4)] + [sp.solve(term, t)[0] for term in linear])
assert breaks == [0, sp.Rational(7, 25), sp.Rational(527, 600),
                  sp.Rational(600, 527), sp.Rational(25, 7), 4]
for term in linear:
    unconstrained = -term/1250
    assert max(unconstrained.subs(t, 0), unconstrained.subs(t, 4)) < 4
reduced = []
minima = []
for lo, hi in zip(breaks, breaks[1:]):
    mid = (lo + hi)/2
    minimizers = {v: -term/1250 if term.subs(t, mid) < 0 else 0
                  for v, term in zip(leaves, linear)}
    piece = sp.factor(q.subs(minimizers))
    # Each linear leaf derivative can change sign only at a listed breakpoint.
    for v, term in zip(leaves, linear):
        if minimizers[v] == 0:
            assert term.subs(t, lo) >= 0 and term.subs(t, hi) >= 0
        else:
            assert term.subs(t, lo) <= 0 and term.subs(t, hi) <= 0
    candidates = [lo, hi] + [r for r in sp.solve(sp.diff(piece, t), t)
                             if r.is_real and lo <= r <= hi]
    minimum = min(piece.subs(t, point) for point in candidates)
    assert minimum >= 0
    reduced.append(piece)
    minima.append(minimum)
assert q.subs({t: sp.Rational(48, 25), a: 1, b: 0, c: 0, d: 0}) == 0

u = sp.symbols('u0:5')
substitution = {t: 4*u[0], a: 4*u[1], b: 4*(1-u[2]),
                c: 4*(1-u[3]), d: 4*u[4]}
p = sp.expand(q.subs(substitution))
expected = (14425 + 10000*sum(v*v for v in u) + 32064*u[0] + 4216*u[1]
            - 15200*u[2] - 18600*u[3] + 5000*u[4]
            - 19200*u[0]*u[1] - 16864*u[0]*u[2]
            - 20000*u[0]*u[3] - 5600*u[0]*u[4])
assert sp.expand(p-expected) == 0
# The center/leaf Schur complement proves exactly one negative eigenvalue.
Q = A[1:, 1:]
assert Q[1:, 1:] == 625*sp.eye(4)
schur = Q[0, 0] - (Q[0, 1:]*Q[1:, 0])[0]/625
assert schur == -sp.Rational(668354, 625)
print('All 63 principal minors: positive; all full RLT slacks: positive.')
print('Exact objective:', sp.trace(A*Y))
print('Independently derived reduced pieces:', reduced)
print('Exact piece minima:', minima)
print('Unit-box polynomial verified; Hessian inertia: four positive, one negative.')
