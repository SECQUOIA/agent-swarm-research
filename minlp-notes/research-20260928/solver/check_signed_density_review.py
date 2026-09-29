"""Exact finite checks for the signed-density transfer; not a theorem proof."""

from fractions import Fraction as F
from math import ceil, comb, log2

import sympy as sp


def check_product_identity():
    delta = sp.symbols("delta")
    residuals = sp.symbols("r0:6")
    for j in range(1, 7):
        lhs = delta ** (2 * j) - sp.prod(r**2 for r in residuals[:j])
        rhs = sum(
            delta ** (2 * (j - i - 1))
            * (delta**2 - residuals[i] ** 2)
            * sp.prod(r**2 for r in residuals[:i])
            for i in range(j)
        )
        assert sp.expand(lhs - rhs) == 0
    for v in range(1, 9):
        for j in range(v + 1):
            # Degrees are expressed in units of the even source degree D.
            assert v - j + 2 * j <= 2 * v
            assert F(v - j, 2) + j <= v


def check_common_shift():
    u, s, v, correction = sp.symbols("u s v correction")
    # These two densities are signed but have mass one and identical
    # separator marginals under the product-arcsine reference measure.
    h_a = 1 + 3 * s + u * s
    h_b = 1 + 3 * s + v * s
    # Terms odd in the eliminated coordinate integrate to zero.
    marginal_a = ((h_a + correction) / (1 + correction)).subs(u, 0)
    marginal_b = ((h_b + correction) / (1 + correction)).subs(v, 0)
    assert sp.simplify(marginal_a - marginal_b) == 0
    # Different valid shifts need not preserve consistency.
    assert sp.simplify(marginal_a.subs(correction, 3)
                       - marginal_b.subs(correction, 4)) != 0
    original, reference = sp.symbols("original reference")
    corrected = (original + correction * reference) / (1 + correction)
    assert sp.simplify(corrected - original
                       - correction * (reference - corrected)) == 0


def check_positive_factor_obstruction():
    # An exact order-two ordinary-module pseudomoment functional.
    # Basis: 1, x, y, x^2, xy, y^2. Odd coordinate moments vanish.
    basis = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]
    even = {(0, 0): sp.Integer(1), (2, 0): sp.Rational(3, 4),
            (0, 2): sp.Rational(3, 4), (4, 0): sp.Rational(3, 4),
            (0, 4): sp.Rational(3, 4), (2, 2): sp.Rational(3, 8)}

    def moment(alpha):
        return even.get(alpha, sp.Integer(0))

    def pair(alpha, beta):
        return tuple(a + b for a, b in zip(alpha, beta))

    matrix = sp.Matrix([[moment(pair(a, b)) for b in basis] for a in basis])
    assert matrix.is_positive_semidefinite
    for generator in [(2, 0), (0, 2)]:
        local = sp.Matrix([
            [moment(pair(a, b)) - moment(pair(pair(a, b), generator))
             for b in basis[:3]] for a in basis[:3]
        ])
        assert local.is_positive_semidefinite
    residual_product = (moment((0, 0)) - moment((2, 0))
                        - moment((0, 2)) + moment((2, 2)))
    assert residual_product == -sp.Rational(1, 8)


def check_rate_bounds():
    cases = 0
    for s in range(2, 34):
        for w in range(1, 9):
            n = 2 * ceil(max(F(3, 2), F(w + 1, 4)) * log2(s))
            delta = F(1, 2 ** (n + 1))
            c_s = F(2 * s * s + 1, 3 * s)
            b = F(s * s * (n + 1), 1) / c_s
            delta_w = sum((comb(w, j) * delta**j * b ** (w - j)
                           for j in range(2, w + 1)), F(0))
            assert b >= 1
            assert delta <= F(1, 2 * s**3)
            if w >= 2:
                assert delta**2 <= F(1, 4 * s ** max(6, w + 1))
                assert delta_w <= comb(w, 2) * delta**2 * (b + delta) ** (w - 2)
            else:
                assert delta_w == 0
            previous = sum((comb(w - 1, j) * delta**j * b ** (w - 1 - j)
                            for j in range(2, w)), F(0))
            assert previous <= delta_w
            cases += 1
    return cases


if __name__ == "__main__":
    check_product_identity()
    check_common_shift()
    check_positive_factor_obstruction()
    count = check_rate_bounds()
    print("PASS: six exact residual-product identities and finite degree ledgers.")
    print("PASS: common-shift consistency and signed-objective identities.")
    print("PASS: exact feasible pseudomoment obstruction to product positivity.")
    print(f"PASS: {count} exact finite correction/rate-bound cases.")
    print("These checks do not prove the theorem for arbitrary degrees or pseudomoments.")
