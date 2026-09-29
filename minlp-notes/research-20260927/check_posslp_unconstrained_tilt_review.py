"""Independent exact checks for the cubic tilt in the PosSLP reduction.

This checks the Hessian Gram identity, scalar no-case margin, and the
rational Taylor identities used for the positive-branch SOS consequence.
It does not check the signed-root realization or the full circuit reduction.
"""

import sympy as sp


def check_hessian_gram():
    xa, xb, ya, yb, kappa = sp.symbols("xa xb ya yb kappa")
    variables = sp.Matrix([xa, xb])
    direction = sp.Matrix([ya, yb])
    cubic = -(xa - kappa) ** 2 * (xb - kappa)
    basis = sp.Matrix([ya, yb, xa * ya, xa * yb, xb * ya, xb * yb])
    gram = sp.zeros(6)
    gram[0, 0] = 2 * kappa
    gram[0, 1] = gram[1, 0] = 2 * kappa
    gram[0, 4] = gram[4, 0] = -1
    gram[1, 2] = gram[2, 1] = -2
    expected = (direction.T * sp.hessian(cubic, variables) * direction)[0]
    actual = (basis.T * gram * basis)[0]
    assert sp.expand(actual - expected) == 0

    up, vp = sp.symbols("up vp")
    gradient_at_p = sp.Matrix([sp.diff(cubic, x) for x in variables]).subs(
        {xa: up + kappa, xb: vp + kappa}
    )
    assert gradient_at_p == sp.Matrix([-2 * up * vp, -up**2])
    assert sp.expand(gradient_at_p.dot(gradient_at_p) - (4 * up**2 * vp**2 + up**4)) == 0


def check_no_case_margin():
    q, a = sp.symbols("q a")
    bound = q * a - (4 * q * a**2 + q**2) / 2
    # If q <= a/2 and a <= 1/8, both summands on the right are nonnegative.
    residual = q * (a * (sp.Rational(1, 4) - 2 * a) + (a / 2 - q) / 2)
    assert sp.expand(bound - q * a / 2 - residual) == 0
    assert bound.subs({q: sp.Rational(1, 16), a: sp.Rational(1, 8)}) == sp.Rational(1, 256)


def check_rational_taylor_identity():
    t, u, v, d, g, value = sp.symbols("t u v d g value")
    integral = sp.integrate((1 - t) * (u + t * v) ** 2, (t, 0, 1))
    claimed = (u + v / 3) ** 2 / 2 + (v / 6) ** 2
    assert sp.expand(integral - claimed) == 0
    completed = (d + g) ** 2 / 2 + value - g**2 / 2
    assert sp.expand(completed - (value + g * d + d**2 / 2)) == 0


if __name__ == "__main__":
    check_hessian_gram()
    check_no_case_margin()
    check_rational_taylor_identity()
    print("PASS: exact cubic Hessian Gram, gradient norm, no-case margin, and Taylor identities")
