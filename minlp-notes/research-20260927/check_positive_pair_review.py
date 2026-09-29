"""Exact independent checks of the adjacent-positive-vertices counterexample."""

import sympy as sp


def objective(mu, X):
    return (
        X[1, 1] + X[2, 2] - X[0, 1] - 2 * X[1, 2] - X[2, 3]
        + sp.Rational(3, 4) * mu[0] + mu[1] + sp.Rational(1, 4) * mu[3]
    )


def check_rlt(mu, X):
    for i in range(4):
        for j in range(i, 4):
            slacks = (
                X[i, j], mu[i] - X[i, j], mu[j] - X[i, j],
                1 - mu[i] - mu[j] + X[i, j],
            )
            assert all(sp.simplify(v).is_nonnegative for v in slacks)


def main():
    u, s, t, v = sp.symbols("u s t v")
    q = (
        s**2 + t**2 - u*s - 2*s*t - t*v
        + sp.Rational(3, 4)*u + s + sp.Rational(1, 4)*v
    )
    endpoints = {
        (0, 0): (s-t)**2 + s,
        (1, 0): (s-t)**2 + sp.Rational(3, 4),
        (0, 1): (s-t+sp.Rational(1, 2))**2,
        (1, 1): (s-t)**2 + 1-t,
    }
    for (a, b), expected in endpoints.items():
        assert sp.expand(q.subs({u: a, v: b}) - expected) == 0
    assert q.subs({u: 0, s: 0, t: 0, v: 0}) == 0

    A = sp.Matrix([
        [45, 8, 15, 30, 37],
        [8, 8, 8, 8, 6],
        [15, 8, 11, 15, 15],
        [30, 8, 15, 26, 30],
        [37, 6, 15, 30, 37],
    ])
    assert [A[:k, :k].det() for k in range(1, 6)] == [45, 296, 496, 56, 4]
    M = A/45
    mu, X = M[1:, 0], M[1:, 1:]
    check_rlt(mu, X)
    assert objective(mu, X) == -sp.Rational(1, 60)

    # A strict-sign version also has a positive definite continuous block.
    tau = sp.Rational(1, 100)
    perturbed = q + u*(1-u) + v*(1-v) + tau*(s**2+t**2)
    Qcc = sp.hessian(perturbed, (s, t))/2
    assert set(Qcc.eigenvals()) == {sp.Rational(1, 100), sp.Rational(201, 100)}
    perturbed_value = (
        objective(mu, X) + mu[0]-X[0, 0] + mu[3]-X[3, 3]
        + tau*(X[1, 1]+X[2, 2])
    )
    assert perturbed_value == -sp.Rational(19, 2250)

    # A second witness survives every valid cut in means/off-diagonal moments.
    A_bqp = sp.Matrix([
        [400, 152, 165, 235, 248],
        [152, 152, 144, 152, 144],
        [165, 144, 144, 165, 165],
        [235, 152, 165, 214, 227],
        [248, 144, 165, 227, 248],
    ])
    assert [A_bqp[:k, :k].det() for k in range(1, 6)] == [
        400, 37696, 218664, 124416, 0,
    ]
    M_bqp = A_bqp/400
    P, B, C = M_bqp[:4, :4], M_bqp[:4, 4:], M_bqp[4:, 4:]
    assert C-B.T*P.inv()*B == sp.zeros(1)
    mu_bqp, X_bqp = M_bqp[1:, 0], M_bqp[1:, 1:]
    check_rlt(mu_bqp, X_bqp)
    atoms = ("0000", "0001", "0011", "0111", "1010", "1111")
    weights = (144, 21, 62, 21, 8, 144)
    assert sum(weights) == 400 and min(weights) > 0
    mean, second = sp.zeros(4, 1), sp.zeros(4)
    for atom, weight in zip(atoms, weights):
        binary = sp.Matrix([int(coordinate) for coordinate in atom])
        mean += sp.Rational(weight, 400)*binary
        second += sp.Rational(weight, 400)*binary*binary.T
    assert mean == mu_bqp
    assert all(
        second[i, j] == X_bqp[i, j]
        for i in range(4) for j in range(i+1, 4)
    )
    assert X_bqp[0, 0] == mu_bqp[0] and X_bqp[3, 3] == mu_bqp[3]
    assert objective(mu_bqp, X_bqp) == -sp.Rational(1, 200)
    strict_bqp_value = (
        objective(mu_bqp, X_bqp)
        + sp.Rational(1, 200)*(X_bqp[1, 1]+X_bqp[2, 2])
    )
    assert strict_bqp_value == -sp.Rational(21, 40000)

    # The source-derived irrational optimum has an independent exact check.
    g = 2-sp.sqrt(3)
    mu = sp.Matrix([2*g/3, sp.Rational(1, 3), sp.Rational(2, 3), 1-2*g/3])
    X = sp.Matrix([
        [2*g/3, 2*g/3, 2*g/3, 2*(1-3*g)/3],
        [2*g/3, (1-g)/3, sp.Rational(1, 3), sp.Rational(1, 3)],
        [2*g/3, sp.Rational(1, 3), (2-g)/3, sp.Rational(2, 3)],
        [2*(1-3*g)/3, sp.Rational(1, 3), sp.Rational(2, 3), 1-2*g/3],
    ])
    M = sp.Matrix.vstack(sp.Matrix.hstack(sp.ones(1), mu.T), sp.Matrix.hstack(mu, X))
    P, B, C = M[:3, :3], M[:3, 3:], M[3:, 3:]
    assert all(sp.simplify(P[:k, :k].det()).is_positive for k in range(1, 4))
    assert (C-B.T*P.inv()*B).applyfunc(sp.simplify) == sp.zeros(2)
    check_rlt(mu, X)
    optimum = sp.sqrt(3)-sp.Rational(7, 4)
    assert sp.simplify(objective(mu, X)-optimum) == 0
    ell1, ell2 = -g+u+(g-2)*s+t, s+(g-2)*t+v
    certificate = (
        (ell1**2+ell2**2)/4 + g*u*(1-s)/2 + u*(1-t)/2
        + g*s*(1-t) + s*(1-v)/2 + g*t*(1-v)/2
        + (u*(1-u)+v*(1-v))/4
    )
    assert sp.expand(q-optimum-certificate) == 0
    print("PASS: endpoint identities, rational PSD/RLT and BQP witnesses, strict perturbations, exact SDP optimum")


if __name__ == "__main__":
    main()
