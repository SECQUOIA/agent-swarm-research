"""Independent high-precision physical equations for the added-edge gadget.

The unknown objective flow is scaled by D to avoid numerical loss from its
small magnitude. These checks supplement, rather than prove, the gap bounds.
"""

from fractions import Fraction
from itertools import product
from random import Random

import mpmath as mp


mp.mp.dps = 70
rng = Random(9137)
scenario_count = 0
maximum_residual = mp.mpf(0)

for n in range(1, 7):
    for _ in range(3):
        items = [rng.randrange(1, 30) for _ in range(n)]
        target = rng.randrange(1, sum(items) + 1)
        gap_rational = Fraction(6, (31 * target + 18 * sum(items))**2)
        exact_ratio = Fraction(10000) / gap_rational
        D_integer = -(-exact_ratio.numerator // exact_ratio.denominator)
        D = mp.mpf(D_integer)
        gap = mp.mpf(gap_rational.numerator) / gap_rational.denominator
        H = 1 - gap / 2
        for choices in product((0, 1), repeat=n):
            selected = sum(a * z for a, z in zip(items, choices))
            tau = mp.mpf(1) / 2 + mp.mpf(selected) / (2 * target)
            coefficient = 12 * tau + 1
            q0 = 46 / (mp.sqrt(100 + 92 * coefficient) + 10)
            old_drop = 1 - (q0 - 1)**2 / 6

            def physical_equations(a, q, scaled_flow):
                t = scaled_flow / D
                b = a + 3 - q
                c = 4 + t - a
                d = 1 + t - a + q
                path_drop = a**2 / 2 + b**2 / 6
                return (
                    path_drop - c**2 / 6 - d**2 / 2,
                    c**2 / 6 - a**2 / 2 - tau * q**2,
                    3 * (1 - t)**2 - path_drop - H * scaled_flow**2,
                )

            a, q, scaled_flow = mp.findroot(
                physical_equations,
                ((q0 + 1) / 2, q0, mp.sqrt(old_drop / H)),
                tol=mp.mpf("1e-58"),
            )
            residual = max(abs(v) for v in physical_equations(a, q, scaled_flow))
            maximum_residual = max(maximum_residual, residual)
            assert residual < mp.mpf("1e-50")
            t = scaled_flow / D
            assert min(a, q, a + 3 - q, 4 + t - a, 1 + t - a + q, 1 - t) > 0
            assert 0 < scaled_flow <= 2
            new_drop = H * scaled_flow**2
            assert -mp.mpf("1e-50") <= old_drop - new_drop <= 528 / D
            assert abs(scaled_flow - 1) >= 3 * gap / 32
            assert (scaled_flow > 1) == (selected == target)
            assert Fraction(6 * n * target * (31 * target + 18 * sum(items))**2) * (
                (1 - gap_rational / 2) * D_integer**2
            ) == 6 * n * target * ((31 * target + 18 * sum(items))**2 - 3) * D_integer**2
            scenario_count += 1

print(
    f"PASS: {scenario_count} physical scenarios across 18 instances; "
    f"maximum equation residual {mp.nstr(maximum_residual, 5)}; "
    "pressure loss, strict flow threshold, gap, integer scaling"
)
