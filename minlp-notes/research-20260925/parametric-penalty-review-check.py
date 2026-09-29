"""Exact finite arithmetic audit; the Markdown review supplies the general proof."""
from fractions import Fraction as F

two_count = 0
one_count = 0
for n in range(1, 11):
    chain = [F(1, 4)]
    for _ in range(n - 1):
        chain.append(chain[-1] ** 2)
    delta = F(1, 1 << (1 << n))
    assert chain[-1] == delta

    threshold = 1 / delta
    assert threshold.numerator.bit_length() == (1 << n) + 1
    for rho in [F(0), threshold / 2, threshold, threshold + 1, 2 * threshold]:
        for lam in [
            F(0), rho / 2, -rho / 2, rho, -rho,
            rho + 1, -rho - 1, 2 * rho + 1,
        ]:
            candidates = []
            for q in [0, 1]:
                for b in [0, 1]:
                    lo = max(F(-1), delta - (1 - q) - 2 * (1 - b))
                    hi = min(F(1), -delta + (1 - q) + 2 * b)
                    ys = [lo, hi] + ([F(0)] if lo <= 0 <= hi else [])
                    candidates += [-q + lam * y + rho * abs(y) for y in ys]
            actual = min(candidates)
            t = rho - abs(lam)
            formula = min(F(0), -1 + delta * t) if t >= 0 else -1 + t
            assert actual == formula
            assert actual <= min(F(0), -1 + rho * delta)
            two_count += 1

    s = F(3, 8)
    assert s - s * s == F(15, 64)
    for q in [0, 1]:
        for b in [0, 1]:
            y = F(0) if q == 0 else F(2 * b - 1, 2)
            gaps = [
                s - F(1, 4), s, 1 - s, 1 - y, y + 1,
                y - (s - (1 - q) - 2 * (1 - b)),
                (-s + (1 - q) + 2 * b) - y,
            ]
            assert min(gaps) >= F(1, 8)

    threshold = 1 / (2 * delta)
    assert threshold.denominator == 1
    assert threshold.numerator.bit_length() == (1 << n)
    for rho in [F(0), threshold / 2, threshold, threshold + 1, 2 * threshold]:
        best = min(F(0), (2 * rho * delta - 1) / (1 + delta))
        opt = (1 + rho * (1 - delta)) / (1 + delta) if rho <= threshold else rho

        def evaluate(lam):
            points = [(0, F(-1)), (0, F(0)), (0, F(1)), (1, delta), (1, F(1))]
            return min(-q + lam * y + rho * abs(y) for q, y in points)

        assert evaluate(opt) == best
        for lam in [
            F(0), rho, -rho, opt, opt + 1, opt - 1,
            2 * rho + 1, -2 * rho - 1,
        ]:
            val = evaluate(lam)
            formula = min(
                F(0), rho - abs(lam),
                -1 + delta * (rho + lam), -1 + rho + lam,
            )
            assert val == formula and val <= best
            balanced = (
                delta * (rho - lam) + (-1 + delta * (rho + lam))
            ) / (1 + delta)
            assert balanced == (2 * rho * delta - 1) / (1 + delta)
            one_count += 1
        if rho > threshold:
            lam = threshold
            assert rho - abs(lam) > 0
            assert -1 + delta * (rho + lam) > 0

    for q in [0, 1]:
        y = F(0) if q == 0 else F(1, 2)
        assert min(
            s - F(1, 4), s, 1 - s, 1 - y, y + 1,
            y - (s - 2 * (1 - q)),
        ) >= F(1, 8)

print(
    f"PASS: {one_count} one-binary and {two_count} two-binary exact rational "
    "endpoint/multiplier checks, n=1..10; threshold bits, chain endpoints, "
    "Slater margins, balanced witnesses, and strict exactness checked."
)
