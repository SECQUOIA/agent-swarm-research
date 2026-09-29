"""Independent exact stress checks of the level-scaled multiplier proof.

The supplied membership degrees are 2 and 3. They are deliberately
nonminimal: high-degree Koszul syzygies exercise the full parent hierarchy.
"""

import sympy as sp


def monomial_exponents(degree):
    return [(i, j) for total in range(degree + 1) for i in range(total + 1)
            for j in [total - i]]


def symmetric_product(left, right):
    return (left * right.T + right * left.T) / 2


def check(degree):
    x, y = sp.symbols("x y")
    variables = (x, y)
    H = sp.Matrix([[2, 1], [1, 3]])
    G = 2*x*x + 2*x*y + 3*y*y + x - 2*y - 3
    factors = [G, x - 1, y]
    targets = [x*y + y + x - 1, (x - 1)**2 + 2*y*y - 3*x*y + y]
    coefficients = [[0, 1 + y, 2], [0, x - 1 - 3*y, 2*y - 2]]
    # Add zero syzygies with coefficient degree exactly the requested degree.
    for a in range(2):
        multiplier = variables[a] ** (degree - 2)
        coefficients[a][0] += multiplier * factors[a + 1]
        coefficients[a][a + 1] -= multiplier * G
        assert sp.expand(sum(u*q for u, q in zip(coefficients[a], factors)) - targets[a]) == 0
        assert max(sp.Poly(u, x, y).total_degree() for u in coefficients[a]) == degree

    monomials = monomial_exponents(degree)
    parents = monomial_exponents(degree - 1)
    w_index = {(alpha, i): j*3 + i for j, alpha in enumerate(monomials) for i in range(3)}
    entries = [x**alpha[0] * y**alpha[1] * q for alpha in monomials for q in factors]
    levels = [0] * len(entries)
    blocks = {}
    for a in range(2):
        for alpha in parents:
            blocks[a, alpha] = len(entries)
            entries.extend(x**alpha[0] * y**alpha[1] * v * targets[a] for v in variables)
            levels.extend([sum(alpha) + 1] * 2)
    size = len(entries)

    def unit(index):
        result = sp.zeros(size, 1)
        result[index] = 1
        return result

    initial_targets = []
    for a in range(2):
        vector = sp.zeros(size, 1)
        for i in range(3):
            polynomial = sp.Poly(coefficients[a][i], x, y)
            for alpha, coefficient in polynomial.terms():
                vector[w_index[alpha, i]] = coefficient
        initial_targets.append(vector)

    def target_coordinate(a, alpha):
        if sum(alpha) == 0:
            return initial_targets[a]
        j = next(index for index in range(2) if alpha[index])
        parent = list(alpha)
        parent[j] -= 1
        return unit(blocks[a, tuple(parent)] + j)

    kappas = {alpha: sp.factorial(degree) / (sp.factorial(degree - sum(alpha)) *
              sp.factorial(alpha[0]) * sp.factorial(alpha[1])) for alpha in monomials}
    initial = sp.zeros(size)
    for (alpha, i), index in w_index.items():
        initial[index, index] = kappas[alpha]
    identities = []
    errors = []
    for a in range(2):
        target = sp.Poly(targets[a], x, y)
        T = sp.Matrix([[target.coeff_monomial(x*x), target.coeff_monomial(x*y)/2],
                       [target.coeff_monomial(x*y)/2, target.coeff_monomial(y*y)]])
        r = [target.coeff_monomial(x), target.coeff_monomial(y)]
        constant = target.coeff_monomial(1)
        for alpha in parents:
            p = target_coordinate(a, alpha)
            g = unit(w_index[alpha, 0])
            z = [unit(blocks[a, alpha] + j) for j in range(2)]
            V = []
            for j in range(2):
                shifted = list(alpha)
                shifted[j] += 1
                V.append(unit(w_index[tuple(shifted), 0]))
            positive = sum((H[j, ell] * z[j]*z[ell].T
                            for j in range(2) for ell in range(2)), sp.zeros(size))
            Z = positive - 3 * p*p.T - constant * symmetric_product(g, p)
            for j in range(2):
                Z += [1, -2][j] * symmetric_product(p, z[j])
                Z -= r[j] * symmetric_product(g, z[j])
                for ell in range(2):
                    Z -= T[j, ell] * symmetric_product(V[j], z[ell])
            assert Z == Z.T
            polynomial = sum(Z[i, j] * entries[i] * entries[j]
                             for i in range(size) for j in range(size) if Z[i, j])
            assert sp.expand(polynomial) == 0
            identities.append((sum(alpha), Z))
            errors.append((sum(alpha), Z - positive))

    eta = min(sp.Integer(1), H.det()/sp.trace(H))
    K = sum(abs(value) for _, error in errors for value in error)
    rho = eta / (2 * (1 + K))
    Q = initial + sum((rho**(2*(level + 1)) * Z for level, Z in identities), sp.zeros(size))
    scaling = sp.diag(*(rho**(-level) for level in levels))
    transformed = scaling * Q * scaling
    positive = initial.copy()
    for start in blocks.values():
        positive[start:start + 2, start:start + 2] = H
    correction = transformed - positive
    assert sum(abs(value) for value in correction) <= K * rho < eta/2
    # A distinct exact PSD check: rational LDL of the assembled Gram.
    _, diagonal = Q.LDLdecomposition(hermitian=False)
    assert all(diagonal[j, j] > 0 for j in range(size))

    J = sp.Matrix([[1, 2], [2, -3]])
    target_gram = sp.zeros(size)
    for alpha in monomials:
        V = sp.Matrix.vstack(*(target_coordinate(a, alpha).T for a in range(2)))
        target_gram += kappas[alpha] * V.T * J * V
    bound = max(sum(abs(target_gram[i, j]) for j in range(size)) for i in range(size))
    threshold = sp.ceiling(2 * (bound + 1) / (eta * rho**(2*degree)))
    final = threshold * Q - target_gram
    _, diagonal = final.LDLdecomposition(hermitian=False)
    assert all(diagonal[j, j] > 0 for j in range(size))
    h = 1 + x*x + y*y
    expected = h**degree * (threshold * sum(q*q for q in factors) -
                            (sp.Matrix(targets).T * J * sp.Matrix(targets))[0])
    represented = sum(final[i, j] * entries[i] * entries[j]
                      for i in range(size) for j in range(size) if final[i, j])
    assert sp.expand(represented - expected) == 0
    assert all(sp.expand(q).subs({x: 1, y: 0}) == 0 for q in factors + targets)
    print(f"PASS: d={degree}, dimension={size}, all zero identities, level bound, two exact LDL checks, final polynomial identity")


if __name__ == "__main__":
    check(2)
    check(3)
