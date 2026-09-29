"""Targeted exact checks for disjunctive-review.md; no numerical solver."""

from itertools import combinations

import sympy as sp


R = sp.Rational


def moment_matrix(mean, second):
    return sp.BlockMatrix([[sp.ones(1, 1), mean.T], [mean, second]]).as_explicit()


def check_psd(matrix):
    # For a real symmetric matrix, all principal minors being nonnegative
    # is necessary and sufficient for positive semidefiniteness.
    assert matrix == matrix.T
    for size in range(1, matrix.rows + 1):
        for subset in combinations(range(matrix.rows), size):
            assert matrix.extract(subset, subset).det() >= 0


bag_a = [(R(1, 2), R(1, 4), 0), (R(1, 2), R(3, 4), 1)]
bag_b = [(R(1, 5), 0, 0), (R(4, 5), R(5, 8), 1)]
features = [lambda x, y: x, lambda x, y: x*x, lambda x, y: y,
            lambda x, y: y*y, lambda x, y: x*y]
assert [sum(w*f(x, y) for w, x, y in bag_a) for f in features] == [
    R(1, 2), R(5, 16), R(1, 2), R(1, 2), R(3, 8)]
assert [sum(w*f(x, y) for w, x, y in bag_b) for f in features] == [
    R(1, 2), R(5, 16), R(4, 5), R(4, 5), R(1, 2)]
assert R(1, 2)*R(4, 5) + R(1, 8)*R(1, 10)/R(1, 16) == R(3, 5)
print('Two-bag witness: exact moments and forced missing-edge moment verified.')

Q = sp.Matrix([[R(1, 4), -R(1, 2), 0, 0], [-R(1, 2), 1, -1, 0],
               [0, -1, 1, -R(1, 2)], [0, 0, -R(1, 2), R(1, 4)]])
c = sp.Matrix([R(1, 2), 1, 0, 0])

# Zhang--Wang, arXiv:2609.03617v1, Appendix A.
x = sp.Matrix([R(41, 200), R(26, 75), R(49, 75), R(159, 200)])
X = sp.Matrix([[R(19, 125), R(9, 50), R(41, 200), R(9, 50)],
               [R(9, 50), R(32, 125), R(26, 75), R(26, 75)],
               [R(41, 200), R(26, 75), R(563, 1000), R(377, 600)],
               [R(9, 50), R(26, 75), R(377, 600), R(371, 500)]])
check_psd(moment_matrix(x, X))
weights = [R(9, 50), R(1, 6), R(169, 600), R(1, 6), R(1, 40), R(9, 50)]
points = [sp.Matrix(z) for z in [(0, 0, 0, 0), (0, 0, 0, 1),
          (0, 0, 1, 1), (0, 1, 1, 1), (1, 0, 1, 0), (1, 1, 1, 1)]]
assert sum(weights) == 1 and all(w >= 0 for w in weights)
assert sum((w*z for w, z in zip(weights, points)), sp.zeros(4, 1)) == x
assert all(sum(w*z[i]*z[j] for w, z in zip(weights, points)) == X[i, j]
           for i in range(4) for j in range(i + 1, 4))
assert all(X[i, i] <= x[i] for i in range(4))
assert sp.trace(Q*X) + (c.T*x)[0] == -R(1, 100)
print('Appendix A: PSD, BQP representation, diagonal RLT, and exact gap verified.')

# Zhang--Wang, arXiv:2609.03617v1, Appendix B.
x = sp.Matrix([R(1, 6), R(1, 2), 1, R(9, 8)])
X = sp.Matrix([[R(7, 72), R(1, 8), R(1, 6), R(1, 8)],
               [R(1, 8), R(7, 24), R(1, 2), R(1, 2)],
               [R(1, 6), R(1, 2), 1, R(9, 8)],
               [R(1, 8), R(1, 2), R(9, 8), R(87, 64)]])
check_psd(moment_matrix(x, X))


def psi(z):
    return sp.Matrix([z[0], z[1], z[0]*z[2], z[0]*z[3], z[1]*z[2],
                      z[1]*z[3], z[0]**2, z[1]**2, z[0]*z[1]])


Psi = sp.Matrix([x[0], x[1], X[0, 2], X[0, 3], X[1, 2], X[1, 3],
                 X[0, 0], X[1, 1], X[0, 1]])
assert Psi == (R(15, 16)*psi([0, R(1, 3), 1, 1])
               + R(3, 16)*psi([R(2, 3), 1, 1, 1])
               + R(1, 8)*psi([R(1, 3), 0, 1, 0]))
eta = sp.symbols('eta')
gap = sp.trace(Q*X) + (c.T*x)[0] + eta*(X[3, 3] - x[3]) + eta/4
assert sp.expand(gap) == -R(25, 2304) + R(31, 64)*eta
assert gap.subs(eta, R(1, 100)) == -R(173, 28800) < -R(1, 200)
print('Appendix B: PSD, conic moment identity, and exact perturbed gap verified.')
