"""Exact checks of the two-positive-vertex SDP obstruction, no numerical SDP."""

from itertools import combinations
import sympy as s


u, a, b, v = s.symbols('u a b v')
q = a*a+b*b-u*a-2*a*b-b*v+s.Rational(3,4)*u+a+s.Rational(1,4)*v
endpoints = [
    ((0, 0), (a-b)**2+a),
    ((1, 0), (a-b)**2+s.Rational(3,4)),
    ((0, 1), (a-b+s.Rational(1,2))**2),
    ((1, 1), (a-b)**2+1-b),
]
for (eu, ev), expected in endpoints:
    assert s.expand(q.subs({u: eu, v: ev})-expected) == 0


def check_moments(integer_matrix, denominator, expected_value):
    M = s.Matrix(integer_matrix)/denominator
    mu, X = M[1:, 0], M[1:, 1:]
    assert M[0, 0] == 1
    for k in range(1, 6):
        for I in combinations(range(5), k):
            assert M.extract(I, I).det() >= 0
    for i in range(4):
        for j in range(i, 4):
            assert 0 <= X[i,j] <= min(mu[i], mu[j])
            assert X[i,j] >= mu[i]+mu[j]-1
    assert X[0,0] == mu[0] and X[3,3] == mu[3]
    value = X[1,1]+X[2,2]-X[0,1]-2*X[1,2]-X[2,3]
    value += s.Rational(3,4)*mu[0]+mu[1]+s.Rational(1,4)*mu[3]
    assert value == expected_value
    return M, mu, X


A = s.Matrix([
    [45,8,15,30,37],
    [8,8,8,8,6],
    [15,8,11,15,15],
    [30,8,15,26,30],
    [37,6,15,30,37],
])
assert [A[:k,:k].det() for k in range(1,6)] == [45,296,496,56,4]
_, _, X = check_moments(A,45,-s.Rational(1,60))
assert -s.Rational(1,60)+(X[1,1]+X[2,2])/100 == -s.Rational(19,2250)

B = s.Matrix([
    [400,152,165,235,248],
    [152,152,144,152,144],
    [165,144,144,165,165],
    [235,152,165,214,227],
    [248,144,165,227,248],
])
assert [B[:k,:k].det() for k in range(1,6)] == [400,37696,218664,124416,0]
M, mu, X = check_moments(B,400,-s.Rational(1,200))
atoms = [s.Matrix(z) for z in [(0,0,0,0),(0,0,0,1),(0,0,1,1),
                               (0,1,1,1),(1,0,1,0),(1,1,1,1)]]
weights = [s.Rational(k,400) for k in [144,21,62,21,8,144]]
assert sum(weights) == 1 and min(weights) > 0
assert sum((p*z for p,z in zip(weights,atoms)),s.zeros(4,1)) == mu
binary_X = sum((p*z*z.T for p,z in zip(weights,atoms)),s.zeros(4,4))
for i in range(4):
    for j in range(i+1,4):
        assert binary_X[i,j] == X[i,j]
assert -s.Rational(1,200)+(X[1,1]+X[2,2])/200 == -s.Rational(21,40000)
positive_block = s.Matrix([[s.Rational(201,200),-1],[-1,s.Rational(201,200)]])
assert set(positive_block.eigenvals()) == {s.Rational(1,200),s.Rational(401,200)}
print('PASS: four endpoint identities; both exact PSD/RLT witnesses; BQP mixture; two strict-curvature perturbations')
