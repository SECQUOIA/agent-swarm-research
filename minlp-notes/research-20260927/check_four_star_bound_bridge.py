"""Exact algebra checks for the four-star book-bridge obstruction."""

import sympy as sp


def main():
    t, y, z, w = sp.symbols("t y z w")
    half = sp.Rational(1, 2)
    q = (y - 2 * t + half) ** 2 + (t - sp.Rational(3, 16)) * z
    q += (sp.Rational(13, 16) - t) * w
    certificate = (y - 2 * t + half - z / 4 + w / 4) ** 2
    certificate += y * z / 2 + (1 - y) * w / 2
    certificate += (z * (1 - z) + w * (1 - w)) / 16 + z * w / 8
    assert sp.expand(q - certificate) == 0
    assert sp.expand(q.subs({y: 2 * t - half, z: 0, w: 0})) == 0

    variables = (t, y, z, w)
    for point in (
        (half, half, 0, 0),
        (sp.Rational(1, 8), 0, 1, 0),
        (sp.Rational(7, 8), 1, 0, 1),
    ):
        assert q.subs(dict(zip(variables, point))) == 0
    for point in ((0, -half, 1, 0), (1, sp.Rational(3, 2), 0, 1)):
        assert q.subs(dict(zip(variables, point))) == -sp.Rational(3, 16)

    # A general pair of leaves has no cross coefficient precisely when
    # alpha - beta - gamma + delta = 0. Its remaining polynomial is affine.
    u, v, alpha, beta, gamma, delta = sp.symbols(
        "u v alpha beta gamma delta"
    )
    pair = alpha * u * v + beta * u * (1 - v)
    pair += gamma * (1 - u) * v + delta * (1 - u) * (1 - v)
    affine = delta + (beta - delta) * u + (gamma - delta) * v
    assert sp.expand(pair.subs(alpha, beta + gamma - delta) - affine) == 0
    print("PASS: identity, zero segment, three minimizers, two extension witnesses")
    print("PASS: cancellation of a leaf-pair cross coefficient gives an affine sum")
    print("Unchecked: analytic sign/orientation argument and novelty")


if __name__ == "__main__":
    main()
