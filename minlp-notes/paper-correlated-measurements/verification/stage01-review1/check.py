"""Independent exact arithmetic checks for the Stage 1 review."""
from itertools import combinations
import sympy as s


def psd(A):
    return all(A.extract(k, k).det() >= 0
               for size in range(1, A.rows + 1)
               for k in combinations(range(A.rows), size))


B = s.Matrix([[1, 2], [-1, 1], [0, 3], [2, -1]]) / 3
R = s.eye(4) + B * B.T
F = s.Matrix([[1, 0, 2], [0, 1, -1], [2, 1, 0], [1, -1, 1]])
M = 1 + s.trace(B * B.T)
alpha = (M + 1) ** 2 / (4 * M)
checked = 0
for J0 in (s.zeros(3), s.diag(1, 0, 0), s.eye(3)):
    for size in range(5):
        for idx in combinations(range(4), size):
            comp = tuple(i for i in range(4) if i not in idx)
            if idx:
                Fs = F.extract(idx, range(3))
                A = R.extract(idx, idx)
                J = J0 + Fs.T * A.inv() * Fs
                G = J0 + Fs.T * R.inv().extract(idx, idx) * Fs
            else:
                J = G = J0
            assert psd(G - J) and psd(alpha * J - G)
            assert J.nullspace() == G.nullspace()
            cross_rank = R.extract(idx, comp).rank()
            assert (G - J).rank() <= cross_rank
            if idx and comp:
                cross = R.extract(idx, comp)
                C = R.extract(comp, comp)
                H = cross.T * A.inv() * Fs
                assert G - J == H.T * (C - cross.T * A.inv() * cross).inv() * H
                assert (G == J) == (H == s.zeros(len(comp), 3))
            checked += 1

h = s.symbols('h', positive=True)
kinetic_F = s.Matrix([
    [s.Rational(1, 2)**j - s.Rational(1, 4)**j,
     2*(s.Rational(1, 2)**j - s.Rational(1, 4)**j) - j*h*s.Rational(1, 2)**j,
     -(s.Rational(1, 2)**j - s.Rational(1, 4)**j) + j*h*s.Rational(1, 4)**j]
    for j in (1, 2, 3)])
assert s.factor(kinetic_F.det()) == -h**2 / 2048
print(f'PASS: {checked} exact subset/prior checks; kinetic sensitivity determinant = -log(2)^2/2048.')
