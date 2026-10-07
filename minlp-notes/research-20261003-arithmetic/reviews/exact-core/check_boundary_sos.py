"""Fresh exact checks of the boundary-SOS example used by the core audit.

This reconstructs the Hessian Gram directly from the displayed quadratics.
It does not import any previous checker. The field and complexity arguments
are mathematical arguments in review.md, not claims established by this file.
"""

import sympy as sp


def main():
    x = sp.symbols("x0:3")
    v = sp.Matrix(sp.symbols("v0:3"))
    center = sp.Matrix([sp.Rational(3, 4), 1, sp.Rational(1, 2)])
    substitution = dict(zip(x, center))
    r = [
        2 - 2 * x[0] * x[1],
        2 * x[0] ** 2 - 2 * x[1] * x[2],
        2 * x[1] ** 2 - 4 * x[2],
        2 * x[2] ** 2 - x[0],
        2 * x[0] * x[2] - x[1],
    ]
    a = sum(c * q for c, q in zip([4, 5, 3, 9], r))
    factors = [a, *r]
    weights = [1, 1, 1, 1, 1, -1]
    f = sp.expand(sum(w * q**2 for w, q in zip(weights, factors)))

    def gram(q):
        t = sp.hessian(q, x) / 2
        b = sp.Matrix([sp.diff(q, xi).subs(substitution) for xi in x])
        d = q.subs(substitution)
        c = 2 * b * b.T + 4 * d * t
        cross = sp.Matrix(3, 9, lambda i, kj:
                          2 * b[kj // 3] * t[i, kj % 3]
                          + 4 * b[i] * t[kj // 3, kj % 3])
        flat = sp.Matrix(list(t))
        lower = 8 * flat * flat.T + 4 * sp.kronecker_product(t, t)
        return c.row_join(cross).col_join(cross.T.row_join(lower))

    m = sum((w * gram(q) for w, q in zip(weights, factors)), sp.zeros(12))
    u = sp.Matrix(x) - center
    basis = v.col_join(sp.kronecker_product(u, v))
    assert sp.expand((basis.T * m * basis)[0] - (v.T * sp.hessian(f, x) * v)[0]) == 0
    minors = [(2 * (m - sp.eye(12)))[:k, :k].det() for k in range(1, 13)]
    assert all(d > 0 for d in minors)

    def functional(poly):
        poly = sp.Poly(poly, *x)
        return 2 * poly.coeff_monomial(x[2]) + 4 * poly.coeff_monomial(x[1] ** 2)

    assert functional(f) == -4
    for i in range(5):
        for j in range(5):
            assert functional(r[i] * r[j]) == (4 if i == j == 4 else 0)

    # Work in Q[t]/(t^5-2), without a floating point root.
    t = sp.Symbol("t")
    at_zero = dict(zip(x, [t**4 / 2, t, t**2 / 2]))
    assert all(sp.rem(sp.Poly(q.subs(at_zero), t), sp.Poly(t**5 - 2, t)).is_zero for q in r)
    evaluation_basis = [1, x[1], x[2], x[1] * x[2], x[0]]
    evaluation = sp.Matrix(5, 5, lambda i, j: sp.Poly(sp.sympify(evaluation_basis[j]).subs(at_zero), t).nth(i))
    assert evaluation.det() != 0
    assert len(sp.Poly(f, *x).terms()) == 31
    assert max(abs(c) for c in sp.Poly(f, *x).coeffs()) == 448
    print("PASS: exact Hessian identity and 12 positive principal minors")
    print("PASS: zero relations, rank-five evaluation, 25 separating identities")
    print("PASS: 31 monomials; maximum absolute coefficient 448")


if __name__ == "__main__":
    main()
