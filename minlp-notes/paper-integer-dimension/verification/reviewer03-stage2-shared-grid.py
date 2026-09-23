"""Independent exact checks of the rational shared residual construction."""
from fractions import Fraction as F
from itertools import product
from math import log2
import random
import sympy as sp

n = 3
v = sp.Matrix([1, 2, 2])
U = sp.eye(n) - 2 * v * v.T / (v.dot(v))
assert U.T * U == sp.eye(n)
H = [sp.Matrix([[2, -3, 1], [-3, 0, 2], [1, 2, -4]]),
     sp.Matrix([[0, 2, -1], [2, 3, 0], [-1, 0, 1]])]
H.append(H[0] + 2 * H[1])
a = [sp.Matrix([1, -2, 3]), sp.Matrix([2, 0, -1]), sp.Matrix([-1, 1, 2])]
b = [sp.Rational(1, 3), sp.Rational(-2, 5), sp.Rational(3, 7)]
lam = [sp.Rational(1, 4), sp.Rational(1, 16), sp.Rational(1, 64)]
width = [sum(abs(U[k, i]) for k in range(n)) for i in range(n)]
lower = sp.Matrix([sum(min(0, U[k, i]) for k in range(n)) for i in range(n)])
c = U * lower
G = [U.T * h * U for h in H]
P = U * sp.diag(*lam) * U.T
energy = [sp.trace(h * P * h * P) for h in H]
C = sp.Matrix([[1, 2, -1], [2, -1, 3]])
W = C.T * C
group_energy = sum(W[j, k] * sp.trace(H[j] * P * H[k] * P)
                   for j in range(3) for k in range(3))
L = []
for i in range(n):
    depth = 0
    while n * width[i] ** 2 > lam[i] * 4 ** depth:
        depth += 1
    L.append(depth)
h = [width[i] / 2 ** L[i] for i in range(n)]
assert sum(L) <= -.5 * log2(float(P.det())) + n * log2(n) + n
rng = random.Random(30302)
points = list(product([0, 1], repeat=n))
points += [tuple(sp.Rational(rng.randrange(17), 16) for _ in range(n)) for _ in range(12)]
pairs = [(i, k) for i in range(n) for k in range(i, n)]
checks = 0
for point in points:
    x = sp.Matrix(point)
    y = U.T * x - lower
    assert x == c + U * y
    idx = [min(int(sp.floor(y[i] / h[i])), 2 ** L[i] - 1) for i in range(n)]
    A = [idx[i] * h[i] for i in range(n)]
    rho = [y[i] - A[i] for i in range(n)]
    assert all(0 <= rho[i] <= h[i] for i in range(n))
    # Verify every exact binary product satisfies its four linear inequalities.
    for i in range(n):
        bits = [(idx[i] >> (L[i] - ell)) & 1 for ell in range(1, L[i] + 1)]
        assert A[i] == width[i] * sum(sp.Rational(bit, 2 ** ell) for ell, bit in enumerate(bits, 1))
        for bit in bits:
            for k in range(n):
                for u, bound in [(y[k], width[k]), (rho[k], h[k])]:
                    z = bit * u
                    assert 0 <= z <= bound * bit and z <= u and z >= u - bound * (1-bit)
    endpoints = []
    for i, k in pairs:
        low = max(0, h[k]*rho[i] + h[i]*rho[k] - h[i]*h[k])
        high = min(h[k]*rho[i], h[i]*rho[k])
        assert low <= rho[i]*rho[k] <= high
        endpoints.append((low, high))
    truth = sp.Matrix([(x.T * H[j] * x)[0]/2 + a[j].dot(x) + b[j] for j in range(3)])
    affine = [((c.T*H[j]*c)[0]/2 + a[j].dot(c) + b[j]
               + (U.T*(H[j]*c+a[j])).dot(y)) for j in range(3)]
    for qs in product(*endpoints):
        monomial = sp.zeros(n)
        for (i, k), q in zip(pairs, qs):
            monomial[i, k] = monomial[k, i] = A[i]*y[k] + rho[i]*A[k] + q
            assert abs(monomial[i, k] - y[i]*y[k]) <= h[i]*h[k]/4
        output = sp.Matrix([affine[j] + sp.trace(G[j]*monomial)/2 for j in range(3)])
        error = output - truth
        assert all(error[j]**2 <= energy[j]/64 for j in range(3))
        assert (error.T*W*error)[0] <= group_energy/64
        assert error[2] - error[0] - 2*error[1] == 0
        checks += 1
    exact_monomial = y*y.T
    assert sp.Matrix([affine[j] + sp.trace(G[j]*exact_monomial)/2 for j in range(3)]) == truth
print(f'PASS: {checks} exact residual-extreme output checks at {len(points)} original-domain points; depths {L}; coordinate reconstruction, binary-product rows, graph witnesses, grouped budgets, and cancellation verified.')
