"""Independent exact identities for the quadratic graph realization review."""

import sympy as sp


def tensor(x, y):
    return sp.Matrix([a * b for a in x for b in y])


def shift(center):
    n = len(center)
    return sp.eye(n).row_join(sp.zeros(n, n * n)).col_join(
        (-sp.kronecker_product(center, sp.eye(n))).row_join(sp.eye(n * n)))


def gram_at_center(polynomials, weights, variables, center):
    n = len(variables)
    c = sp.zeros(n)
    d = sp.zeros(n, n * n)
    q = sp.zeros(n * n)
    substitution = dict(zip(variables, center))
    for polynomial, weight in zip(polynomials, weights):
        h = sp.hessian(polynomial, variables) / 2
        b = sp.Matrix([sp.diff(polynomial, x) for x in variables]).subs(substitution)
        vector = sp.Matrix([h[i, j] for i in range(n) for j in range(n)])
        cross = sp.Matrix(n, n * n,
                          lambda i, kj: 2 * b[kj // n] * h[i, kj % n]
                          + 4 * b[i] * h[kj // n, kj % n])
        c += 2 * weight * b * b.T
        d += weight * cross
        q += weight * (8 * vector * vector.T + 4 * sp.kronecker_product(h, h))
    centered = c.row_join(d).col_join(d.T.row_join(q))
    return shift(center).T * centered * shift(center)


def lift_gradient(f, y, pairs, z):
    result = []
    for variable in y:
        lifted = 0
        for powers, coefficient in sp.Poly(sp.diff(f, variable), *y).terms():
            if sum(powers) == 3:
                indices = [i for i, power in enumerate(powers) for _ in range(power)]
                lifted += coefficient * z[pairs.index(tuple(indices[:2]))] * y[indices[2]]
            else:
                lifted += coefficient * sp.prod(x ** power for x, power in zip(y, powers))
        result.append(lifted)
    return result


for n in [1, 2]:
    y = sp.Matrix(sp.symbols(f"y0:{n}"))
    q = sp.Matrix(sp.symbols(f"q0:{n}"))
    p = sp.Matrix([sp.Rational(2, 3), -sp.Rational(1, 2)][:n])
    pairs = [(i, j) for i in range(n) for j in range(i, n)]
    z = sp.Matrix(sp.symbols(f"z0:{len(pairs)}"))
    h = sp.Matrix([[2]]) if n == 1 else sp.Matrix([[2, 1], [1, 3]])
    u = y - p
    exposing = (u.T * h * u)[0]
    f = sp.expand(exposing ** 2 + u.dot(u))
    eh = sp.Matrix([h[i, j] for i in range(n) for j in range(n)])
    ac = sp.diag(2 * sp.eye(n), 4 * sp.kronecker_product(h, h) + 8 * eh * eh.T)
    a = shift(p).T * ac * shift(p)
    direction = sp.Matrix(sp.symbols(f"b0:{n}"))
    basis = direction.col_join(tensor(y, direction))
    assert sp.expand((basis.T * a * basis)[0]
                     - (direction.T * sp.hessian(f, list(y)) * direction)[0]) == 0

    d = y - q
    s = sp.Matrix([z[k] - q[i] * y[j] - q[j] * y[i] + q[i] * q[j]
                   for k, (i, j) in enumerate(pairs)])
    duplicated = sp.Matrix([s[pairs.index(tuple(sorted((i, j))))]
                            for i in range(n) for j in range(n)])
    t = sp.Symbol("t")
    vector = d.col_join(tensor(q, d) + t * duplicated)
    integral = sp.integrate(sp.expand((1 - t) * (vector.T * a * vector)[0]), (t, 0, 1))
    substitutions = dict(zip(y, q))
    grad = sp.Matrix([sp.diff(f, variable) for variable in y]).subs(substitutions)
    g = sp.expand(f.subs(substitutions) + grad.dot(d) + integral)
    graph = dict(zip(z, [y[i] * y[j] for i, j in pairs]))
    assert sp.expand(g.subs(graph) - f) == 0
    w = list(y) + list(z)
    wp = list(p) + [p[i] * p[j] for i, j in pairs]
    at_zero_center = dict(zip(q, p)) | dict(zip(w, wp))
    assert g.subs(at_zero_center) == 0
    assert all(sp.diff(g, variable).subs(at_zero_center) == 0 for variable in w)

    residuals = lift_gradient(f, y, pairs, z) + [y[i] * y[j] - z[k]
                                               for k, (i, j) in enumerate(pairs)]
    jacobian = sp.Matrix(residuals).jacobian(w).subs(graph)
    assert sp.expand(jacobian.det() - (-1) ** len(pairs)
                     * sp.hessian(f, list(y)).det()) == 0
    print(f"PASS: n={n} Taylor graph identity, zero gradient, residual determinant")

    if n == 1:
        # Test formal-center recovery independently of the true-center identity.
        fixed_g = g.subs(dict(zip(q, p)))
        factors = [fixed_g] + residuals
        weights = [1] + [sp.Rational(1, 1000)] * len(residuals)
        bstar = sp.expand(sum(weight * polynomial ** 2
                             for weight, polynomial in zip(weights, factors)))
        formal = sp.Matrix(sp.symbols(f"v0:{len(w)}"))
        matrix = gram_at_center(factors, weights, w, formal)
        assert max(sp.Poly(entry, *formal).total_degree() for entry in matrix) <= 4
        exact = matrix.subs(dict(zip(formal, wp)))
        bd = sp.Matrix(sp.symbols(f"d0:{len(w)}"))
        full = bd.col_join(tensor(w, bd))
        hessian_biform = sp.expand((bd.T * sp.hessian(bstar, w) * bd)[0])
        assert sp.expand((full.T * exact * full)[0] - hessian_biform) == 0

        selectors = {}
        all_variables = w + list(bd)
        for i in range(len(full)):
            for j in range(len(full)):
                monomial = sp.Poly(full[i] * full[j], *all_variables).monoms()[0]
                selectors.setdefault(monomial, []).append((i, j))
        coefficients = sp.Poly(hessian_biform, *all_variables).as_dict()
        trial = matrix.subs(dict(zip(formal, [wp[0] + sp.Rational(1, 100), wp[1]])))
        projected = trial.copy()
        for monomial, indices in selectors.items():
            correction = (coefficients.get(monomial, 0)
                          - sum(trial[i, j] for i, j in indices)) / len(indices)
            for i, j in indices:
                projected[i, j] += correction
        assert sp.expand((full.T * projected * full)[0] - hessian_biform) == 0
        before = sum(entry ** 2 for entry in trial - exact)
        after = sum(entry ** 2 for entry in projected - exact)
        assert after <= before
        print("PASS: formal-center degree, true-center Gram, exact projection and contraction")
