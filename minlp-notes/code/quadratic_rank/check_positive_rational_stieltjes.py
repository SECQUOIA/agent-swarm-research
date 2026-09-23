"""Numerical checks of the proved positive rational Stieltjes construction.

Gaussian nodes are computed at high precision, not by certified root isolation.
The lemma supplies the uniform certificate; these samples are additional checks.
All rounded coefficients and the endpoint normalizer below are exact rationals.
"""

from fractions import Fraction

import mpmath as mp


def ceil_log2(n):
    return (n - 1).bit_length()


def rational_significand(value, bits=96):
    """Round a positive mp value to a rational with a binary significand."""
    mantissa, exponent = mp.frexp(value)
    numerator = int(mp.floor(mp.ldexp(mantissa, bits) + mp.mpf("0.5")))
    exponent -= bits
    if exponent >= 0:
        return Fraction(numerator << exponent)
    return Fraction(numerator, 1 << (-exponent))


def as_mp(value):
    return mp.mpf(value.numerator) / value.denominator


def run():
    mp.mp.dps = 100
    total_terms = total_samples = 0
    worst_ratio = mp.mpf(0)
    for degree, p in [(3, 8), (8, 8), (32, 4)]:
        epsilon = Fraction(1, 1 << p)
        lower = (degree * (p + ceil_log2(degree) + 8) + 1) // 2
        upper = 3 * (p + 8)
        panels = lower + upper
        order = (p + ceil_log2(256 * panels) + 1) // 2
        gamma = mp.mpf(2) / degree
        roots, weights = mp.gauss_quadrature(order, "legendre")
        pairs = []
        max_relative_rounding = mp.mpf(0)
        for j in range(-lower, upper):
            for root, weight in zip(roots, weights):
                node = (root + 3) / 2
                weight /= 2
                b = mp.ldexp(node, j)
                a = weight * mp.power(b, gamma) / node
                ar, br = rational_significand(a), rational_significand(b)
                assert ar > 0 and br > 0
                max_relative_rounding = max(
                    max_relative_rounding,
                    abs(as_mp(ar) / a - 1),
                    abs(as_mp(br) / b - 1),
                )
                pairs.append((ar, br))

        tau = as_mp(epsilon) / (128 * (degree + 4))
        assert max_relative_rounding < tau
        normalizer = sum((a / (1 + b) for a, b in pairs), Fraction(0))
        assert normalizer > 0
        assert sum((a / (1 + b) for a, b in pairs), Fraction(0)) / normalizer == 1
        assert sum((a * 0 / b for a, b in pairs), Fraction(0)) == 0
        numeric_pairs = [(as_mp(a), as_mp(b)) for a, b in pairs]
        numeric_normalizer = as_mp(normalizer)
        points = {mp.mpf(0), mp.mpf(1)}
        points.update(mp.mpf(i) / 16 for i in range(1, 16))
        points.update(mp.ldexp(mp.mpf(1), -k) for k in [1, p, lower // 2, lower, 2 * lower])
        maximum_error = mp.mpf(0)
        for t in sorted(points):
            value = mp.fsum(a * t / (t + b) for a, b in numeric_pairs) / numeric_normalizer
            expected = mp.power(t, gamma) if t else mp.mpf(0)
            error = abs(value - expected)
            assert error <= as_mp(epsilon)
            maximum_error = max(maximum_error, error)
        total_terms += len(pairs)
        total_samples += len(points)
        worst_ratio = max(worst_ratio, maximum_error / as_mp(epsilon))
        print(
            f"D={degree}, precision={p}, terms={len(pairs)}, "
            f"samples={len(points)}, max error={mp.nstr(maximum_error, 8)}",
            flush=True,
        )
    print(
        f"Passed {total_terms} positive rational terms and {total_samples} samples; "
        f"worst error/tolerance={mp.nstr(worst_ratio, 8)}. Exact endpoints passed."
    )


if __name__ == "__main__":
    run()
