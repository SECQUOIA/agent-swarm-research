"""Exact stress cases for degree drops and rational norm interpolation.

This checks algebra after exact minimal-polynomial recognition. It does not
implement KLL, verify precision bounds, or establish asymptotic complexity.
"""

import sympy as sp


S, T = sp.symbols("S T")


def check_case(name, alpha, beta, expected_norm, expected_coordinate):
    primitive = sp.Poly(sp.minimal_polynomial(alpha, T), T, domain=sp.QQ)
    p = primitive.monic()
    d = p.degree()
    samples, degrees = [], []
    for s in range(d+1):
        minimal = sp.Poly(sp.minimal_polynomial(alpha+s*beta, T), T, domain=sp.QQ)
        e = minimal.degree()
        assert d % e == 0
        degrees.append(e)
        samples.append((minimal.monic()**(d//e)).as_expr())

    norm = 0
    for s, sample in enumerate(samples):
        lagrange = 1
        for t in range(d+1):
            if t != s:
                lagrange *= (S-t)/sp.Integer(s-t)
        norm += sample*lagrange
    norm = sp.expand(norm)
    assert sp.expand(norm-expected_norm) == 0
    assert sp.expand(norm.subs(S, 0)-p.as_expr()) == 0
    inverse = sp.invert(p.diff(), p)
    derivative = sp.Poly(sp.diff(norm, S).subs(S, 0), T, domain=sp.QQ)
    recovered = (-derivative*inverse).rem(p)
    assert sp.expand(recovered.as_expr()-expected_coordinate) == 0
    assert sp.simplify(recovered.as_expr().subs(T, alpha)-beta) == 0
    print(f"PASS {name}: sample degrees {degrees}; coordinate {recovered.as_expr()}")
    return primitive, samples


def main():
    _, samples = check_case(
        "zero sample in quadratic field", sp.sqrt(2), -sp.sqrt(2),
        T**2-2*(1-S)**2, -T,
    )
    assert samples[1] == T**2

    t = sp.real_root(2, 3)
    check_case(
        "nonnormal cubic field", t, t**2,
        T**3-6*S*T-2-4*S**3, T**2,
    )
    primitive, _ = check_case(
        "nonmonic integer polynomial", t/2, t**2/3,
        T**3-S*T-sp.Rational(1, 4)-sp.Rational(4, 27)*S**3,
        sp.Rational(4, 3)*T**2,
    )
    assert primitive.as_expr() == 4*T**3-1


if __name__ == "__main__":
    main()
