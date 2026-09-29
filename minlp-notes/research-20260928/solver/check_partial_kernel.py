"""Exact finite checks for partial-kernel-rounding.md; not a proof of its theorem."""

from itertools import combinations

import sympy as sp

u, v = sp.symbols("u v", real=True)


def kernel(m):
    b = {j: m - abs(j) for j in range(-m + 1, m)}
    a = {k: sum(bj * b.get(j - k, 0) for j, bj in b.items())
         for k in range(2 * m - 1)}
    g = {k: sp.Rational(a[k], a[0]) for k in a}
    polynomial = 1 + 2 * sum(g[k] * sp.chebyshevt(k, u) * sp.chebyshevt(k, v)
                             for k in range(1, 2 * m - 1))
    return sp.expand(polynomial), g


def psd(matrix):
    for size in range(1, matrix.rows + 1):
        for indices in combinations(range(matrix.rows), size):
            assert matrix.extract(indices, indices).det() >= 0


def arcsine_integral(polynomial):
    polynomial = sp.Poly(sp.expand(polynomial), v)
    return sum(coefficient * (0 if exponent[0] % 2 else
                               sp.binomial(exponent[0], exponent[0] // 2)
                               / 2 ** exponent[0])
               for exponent, coefficient in polynomial.terms())


def cheb_coefficients(polynomial):
    polynomial = sp.Poly(sp.expand(polynomial), u)
    out = {}
    while not polynomial.is_zero:
        degree = polynomial.degree()
        coefficient = polynomial.LC() / sp.Poly(sp.chebyshevt(degree, u), u).LC()
        out[degree] = coefficient
        polynomial = sp.Poly(sp.expand(polynomial.as_expr()
                                      - coefficient * sp.chebyshevt(degree, u)), u)
    return out


# Four supported shared coordinates. Each private matrix is PSD, has diagonal
# at most one, and has a mean in the triangle y >= 0, y1 + y2 <= 1.
# These need not represent a joint measure supported on that triangle.
shared_points = [sp.Rational(-1), sp.Rational(-1, 2), sp.Rational(1, 3), sp.Rational(1)]
weights = [sp.Rational(1, 10), sp.Rational(1, 5), sp.Rational(3, 10), sp.Rational(2, 5)]
means = [[sp.Rational(1, 2), sp.Rational(1, 2)], [0, sp.Rational(1, 2)],
         [sp.Rational(1, 4), sp.Rational(1, 4)], [sp.Rational(3, 4), 0]]
source_matrices = [sp.Matrix([[1, a, b], [a, 1, 0], [b, 0, 1]]) for a, b in means]
for matrix in source_matrices:
    psd(matrix)
# At the first source state, E(y1^2)=1 > E(y1)=1/2, impossible on this P.
assert source_matrices[0][1, 1] > source_matrices[0][0, 1]

H = sp.Matrix([[u**3, (u**2-u)/2, -u/2],
               [(u**2-u)/2, 1+u**2, u], [-u/2, u, 1]])
# The private quadratic block has determinant one, everywhere on the real line.
assert sp.expand(H[1:, 1:].det()) == 1
pseudo_objective = sum(weight * sp.trace(H.subs(u, point) * matrix)
                       for weight, point, matrix in zip(weights, shared_points, source_matrices))
coefficient_budget = sum(abs(coefficient) * degree**2 for entry in H
                         for degree, coefficient in cheb_coefficients(entry).items())

counts = {"conditional_matrix_checks": 0, "objective_identity_checks": 0,
          "zero_density_checks": 0, "counterexample_checks": 0}
for m in [2, 3, 4]:
    K, g = kernel(m)
    M = sum((weight * K.subs(u, point) * matrix
             for weight, point, matrix in zip(weights, shared_points, source_matrices)),
            sp.zeros(3))
    M = M.applyfunc(sp.expand)
    h = M[0, 0]
    assert arcsine_integral(h) == 1
    smoothed_objective = arcsine_integral(sp.trace(H.subs(u, v) * M))
    spectral_objective = 0
    for i in range(3):
        for j in range(3):
            for degree, coefficient in cheb_coefficients(H[i, j]).items():
                mixed_moment = sum(weight * sp.chebyshevt(degree, point) * matrix[i, j]
                                   for weight, point, matrix in zip(weights, shared_points, source_matrices))
                assert abs(mixed_moment) <= 1
                spectral_objective += coefficient * g.get(degree, 0) * mixed_moment
    assert sp.simplify(smoothed_objective - spectral_objective) == 0
    assert abs(smoothed_objective - pseudo_objective) <= 3 * coefficient_budget / (2*m*m+1)
    counts["objective_identity_checks"] += 1
    for target in [sp.Rational(j, 8) for j in range(-8, 9)]:
        conditional = M.subs(v, target)
        psd(conditional)
        density = conditional[0, 0]
        assert density > 0
        private_mean = conditional[0, 1:].T / density
        assert all(entry >= 0 for entry in private_mean)
        assert sum(private_mean) <= 1
        assert all(conditional[i, i] <= density for i in [1, 2])
        zz = sp.Matrix([1, *private_mean])
        rounded_cost_mass = density * (zz.T * H.subs(u, target) * zz)[0]
        assert rounded_cost_mass <= sp.trace(H.subs(u, target) * conditional)
        counts["conditional_matrix_checks"] += 1

# Exact zero-density kernel section: a source at u=1, target v=-1, even m.
for m in [2, 4]:
    K, _ = kernel(m)
    assert K.subs({u: 1, v: -1}) == 0
    assert K.subs({u: 1, v: -1}) * source_matrices[0] == sp.zeros(3)
    counts["zero_density_checks"] += 1

# Affine localizers without the private quadratic bound leave L(y^2) unbounded.
for variance in [2, 10, 100]:
    psd(sp.diag(1, variance))
    assert variance > 1  # Both affine bounds still have pseudoexpectation one.
    counts["counterexample_checks"] += 1

# Without convexity, even the r-independent relaxation value can be wrong:
# P is the nonnegative triangle, objective -(y1+y2)^2 has true min -1.
# L(1)=1, L(y_i)=1/2, L(y_i y_j)=1 satisfies (7)--(9), yet objective is -4.
nonconvex_M = sp.Matrix([[1, sp.Rational(1, 2), sp.Rational(1, 2)],
                        [sp.Rational(1, 2), 1, 1], [sp.Rational(1, 2), 1, 1]])
psd(nonconvex_M)
assert nonconvex_M[0, 1] >= 0 and nonconvex_M[0, 2] >= 0
assert 1 - nonconvex_M[0, 1] - nonconvex_M[0, 2] == 0
assert all(nonconvex_M[i, i] <= 1 for i in [1, 2])
assert -sum(nonconvex_M[i, j] for i in [1, 2] for j in [1, 2]) == -4
counts["counterexample_checks"] += 1

print("PASS:", counts)
