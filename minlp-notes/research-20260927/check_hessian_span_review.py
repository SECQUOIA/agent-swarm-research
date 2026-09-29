"""Exact adversarial examples for the Hessian-span value bound.

These checks verify explicit algebraic examples, not the general theorem,
quantifier elimination, or the bit complexity of the ellipsoid method.
"""

from itertools import combinations

import sympy as sp


def check_irrational_singleton():
    x, y, t = sp.symbols("x y t")
    modulus = sp.Poly(t**3 - 2, t)

    def reduce_t(expr):
        return sp.rem(sp.Poly(sp.expand(expr), t), modulus).as_expr()

    rows = [x**2 - y, y**2 - 2*x, (x-y)**2 - y - 2*x + 4]
    weights = [t**2-t/2, 1-t/2, t/2]
    aggregate = sp.expand(sum(a*q for a, q in zip(weights, rows)))
    for q in rows:
        assert reduce_t(q.subs({x: t, y: t**2})) == 0
    for derivative in (sp.diff(aggregate, x), sp.diff(aggregate, y)):
        assert reduce_t(derivative.subs({x: t, y: t**2})) == 0
    hessians = [sp.hessian(q, (x, y)) for q in rows]
    assert all(q.rank() == 1 for q in hessians)
    assert all(q[0, 0] >= 0 and q[1, 1] >= 0 and q.det() == 0
               for q in hessians)
    assert sp.Matrix.hstack(*(q.reshape(4, 1) for q in hessians)).rank() == 3
    hessian = sp.hessian(aggregate, (x, y))
    assert hessian == sp.Matrix([[2*t**2, -t], [-t, 2]])
    assert sp.expand(hessian.det()) == 3*t**2
    # The real root t of t^3=2 lies in (1,2), so all weights and
    # the leading principal minors of the aggregate are positive.
    print("irrational singleton: exact vanishing, stationarity, PSD rows, span 3")


def check_many_extreme_rays():
    t, s = sp.symbols("t s")
    matrix = sp.Matrix([[1, t], [t, t**2 + 1]])
    assert matrix.det() == 1
    exposing_value = matrix[1, 1] - 2*s*matrix[0, 1] + (s**2-1)*matrix[0, 0]
    assert sp.expand(exposing_value - (t-s)**2) == 0
    sampled = [matrix.subs(t, j) for j in range(1, 8)]
    assert sp.Matrix.hstack(*(q.reshape(4, 1) for q in sampled)).rank() == 3
    print("many extreme rays: seven PD matrices, span 3, exact exposing identity")


def check_active_multiplier_compression():
    u, v, w = sp.symbols("u v w")
    parameters = list(range(1, 8))
    coefficients = [sp.Matrix([1, j, j*j]) for j in parameters]
    weights = sp.Matrix([1, 2, 3, 4, 5, 6, 7])
    coefficient_matrix = sp.Matrix.hstack(*coefficients)
    aggregate = coefficient_matrix * weights
    compressed = None
    for support in combinations(range(len(parameters)), 3):
        candidate = coefficient_matrix[:, support].inv() * aggregate
        if all(value >= 0 for value in candidate):
            compressed = support, candidate
            break
    assert compressed is not None
    support, candidate = compressed
    basis = sp.Matrix([u*u + u + sp.Rational(1, 2), v*v, w*w])
    rows = [(c.T*basis)[0] for c in coefficients]
    old = sum(weight*q for weight, q in zip(weights, rows))
    new = sum(weight*rows[index] for index, weight in zip(support, candidate))
    assert sp.expand(old-new) == 0
    assert all(q.subs({u: 0, v: 0, w: 0}) == sp.Rational(1, 2) for q in rows)
    print(f"active multiplier compression: 7 rows to {len(support)}; identity exact")


if __name__ == "__main__":
    check_irrational_singleton()
    check_many_extreme_rays()
    check_active_multiplier_compression()
