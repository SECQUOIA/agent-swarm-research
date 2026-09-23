"""Numerical support for the certified positive-curvature integration proof.

Branch intervals use exact rational polynomial root isolation. Gaussian nodes
and square-root values use high-precision arithmetic here, not the certified
interval implementation described by the theorem.
"""

from fractions import Fraction as F

import mpmath as mp
import sympy as sp


def ceil_log2(value):
    k = max(0, value.numerator.bit_length() - value.denominator.bit_length())
    while F(1 << k) < value:
        k += 1
    return k


def rational(value):
    return F(int(value.p), int(value.q))


def numeric(value):
    return mp.mpf(value.numerator) / value.denominator


def run():
    mp.mp.dps = 90
    symbol = sp.Symbol("x")
    tolerance = F(1, 1024)
    queries = [F(1, 4), F(1, 2), F(3, 4), F(1)]
    panel_count = checks = 0
    worst_ratio = mp.mpf(0)
    for coefficients in [[F(16)], [F(0), F(0), F(256, 9)],
                         [F(1), F(10), F(0), F(100)]]:
        degree = len(coefficients) - 1
        upper = max(F(1), sum(coefficients))
        depth = max(1, ceil_log2(16 * upper / tolerance))
        cutoff = F(1, 1 << depth)
        subdivisions = 16 * max(1, degree)
        order = (ceil_log2(128 * upper / tolerance) + 1) // 2
        polynomial = sum(sp.Rational(c.numerator, c.denominator) * symbol**i
                         for i, c in enumerate(coefficients))
        crossing = sp.Poly((1 - symbol)**2 * polynomial - 1, symbol)
        width = tolerance / (16 * upper * (degree + 3))
        root_intervals = crossing.intervals(
            eps=sp.Rational(width.numerator, width.denominator))
        boxes = []
        for (left, right), _ in root_intervals:
            left, right = max(cutoff, rational(left)), min(F(1), rational(right))
            if left <= right:
                boxes.append((left, right))
        cuts = {cutoff, F(1), *queries}
        for j in range(depth):
            left = F(1, 1 << (j + 1))
            cuts.update(left + left * F(k, subdivisions)
                        for k in range(subdivisions + 1))
        for left, right in boxes:
            cuts.update([left, right])
        cuts = sorted(cuts)
        nodes, weights = mp.gauss_quadrature(order, "legendre")
        numeric_coefficients = list(map(numeric, coefficients))

        def h(x):
            return sum(c * x**i for i, c in enumerate(numeric_coefficients))

        def density(x):
            value = h(x)
            return min(mp.sqrt(value), (1 - x) * value)

        cumulative = mp.mpf(0)
        approximations = {}
        for left, right in zip(cuts, cuts[1:]):
            midpoint = (left + right) / 2
            if not any(a <= midpoint <= b for a, b in boxes):
                h_mid = sum(c * midpoint**i for i, c in enumerate(coefficients))
                if (1 - midpoint)**2 * h_mid < 1:
                    exact = sum((c * ((right**(i+1) - left**(i+1)) / (i+1)
                                    - (right**(i+2) - left**(i+2)) / (i+2))
                                 for i, c in enumerate(coefficients)), F(0))
                    cumulative += numeric(exact)
                else:
                    half = numeric((right - left) / 2)
                    center = numeric(midpoint)
                    cumulative += half * mp.fsum(
                        w * mp.sqrt(h(center + half * node))
                        for node, w in zip(nodes, weights))
                panel_count += 1
            if right in queries:
                approximations[right] = cumulative

        precise_roots = []
        for (left, right), _ in crossing.intervals(eps=sp.Rational(1, 2**220)):
            midpoint = (rational(left) + rational(right)) / 2
            if 0 < midpoint < 1:
                precise_roots.append(numeric(midpoint))
        for endpoint in queries:
            x = numeric(endpoint)
            points = [mp.mpf(0)] + [root for root in precise_roots if root < x] + [x]
            reference = mp.quad(density, points)
            if coefficients == [F(16)]:
                exact = 4*x if x <= mp.mpf(".75") else 16*x - 8*x*x - mp.mpf("4.5")
                assert abs(reference - exact) < mp.mpf("1e-60")
            error = abs(approximations[endpoint] - reference)
            assert error < numeric(tolerance)
            worst_ratio = max(worst_ratio, error / numeric(tolerance))
            checks += 1
    print(f"Passed {checks} cumulative-integral comparisons over {panel_count} panels; "
          f"worst error/tolerance={mp.nstr(worst_ratio, 8)}.")


if __name__ == "__main__":
    run()
