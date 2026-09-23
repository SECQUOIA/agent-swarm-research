"""Independent dense-matrix checks of identities in the lower-bound proofs.

These finite examples detect algebra/index mistakes; they are not proofs.
Run with the qipm Python interpreter from any directory.
"""
import numpy as np
from numpy.polynomial import Polynomial as P
from numpy.polynomial import Chebyshev as T


def second_kind(n):
    if n == 0:
        return P([1.0])
    prev, curr = P([1.0]), P([0.0, 2.0])
    for _ in range(1, n):
        prev, curr = curr, P([0.0, 2.0]) * curr - prev
    return curr


def check_witness(kappa, degree):
    a = 1 / kappa
    m, h = (1 + a) / 2, (1 - a) / 2
    A, C = 4 * (m / h) ** 2 - 3, 4 * a * m / h**2
    omega = np.sqrt(A * A - 1)
    delta = 1 / (A + omega)
    poly_t = T.basis(degree).convert(kind=P)
    poly_u = second_kind(degree - 1)
    poly_r = P([-1, A]) * poly_u + omega * poly_t
    roots = poly_r.roots()
    assert np.max(np.abs(roots.imag)) < 1e-10
    nodes_t = np.r_[-1, np.sort(roots.real), 1]
    poly_l = P([-1, 0, 1]) * poly_r
    derivatives = poly_l.deriv()(nodes_t)
    masses = 1 / np.abs(derivatives)
    masses /= masses.sum()
    signs = np.sign(derivatives)
    qvals = C / (A - nodes_t)
    error = C * delta**degree / omega**2
    diagonal = C * A / omega**2
    np.testing.assert_allclose(masses @ qvals, diagonal, rtol=2e-7)
    np.testing.assert_allclose((masses * signs) @ qvals, error, rtol=2e-6, atol=1e-12)

    x = np.sqrt((nodes_t + 3) / 4)
    B = 1 / (2 * np.sum(masses / x**2))
    nodes = np.r_[-x, 0, x]
    weights = np.r_[B * masses / (2 * x**2), 0.5, B * masses / (2 * x**2)]
    # Lanczos in the diagonal spectral representation, with reorthogonalization.
    basis = [np.sqrt(weights)]
    offdiag = []
    for j in range(len(nodes) - 1):
        w = nodes * basis[j]
        for _ in range(2):
            for vector in basis:
                w -= np.dot(vector, w) * vector
        beta = np.linalg.norm(w)
        offdiag.append(beta)
        basis.append(w / beta)
    jacobi = np.diag(offdiag, 1) + np.diag(offdiag, -1)
    inverse = a * np.linalg.inv(m * np.eye(len(nodes)) + h * jacobi)
    np.testing.assert_allclose(inverse[1, 1], diagonal, rtol=3e-7)
    np.testing.assert_allclose(inverse[-2, -2], diagonal, rtol=3e-7)
    np.testing.assert_allclose(inverse[1, -2], error, rtol=3e-6, atol=1e-12)


def check_path(kappa, n):
    a = 1 / kappa
    m, h = (1 + a) / 2, (1 - a) / 2
    jacobi = np.diag(np.full(n - 1, .5), 1) + np.diag(np.full(n - 1, .5), -1)
    inverse = a * np.linalg.inv(m * np.eye(n) + h * jacobi)
    theta = np.log((np.sqrt(kappa) + 1) / (np.sqrt(kappa) - 1))
    un = np.sinh((n + 1) * theta) / np.sinh(theta)
    un1 = np.sinh(n * theta) / np.sinh(theta)
    np.testing.assert_allclose(abs(inverse[0, -1]), 2 * a / (h * un), rtol=1e-10)
    np.testing.assert_allclose(inverse[0, 0], 2 * a * un1 / (h * un), rtol=1e-10)


for kappa in [4, 16, 128, 1024, 10000]:
    for degree in [1, 2, 3, 6, 8]:
        check_witness(kappa, degree)
    for n in [3, 6, 12, 30, 60]:
        check_path(kappa, n)
print('PASS: 25 witness Jacobi realizations and 25 constant paths.')
