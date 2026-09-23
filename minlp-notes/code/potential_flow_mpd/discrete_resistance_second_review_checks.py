"""Independent symbolic and high-precision checks of the discrete theta gadget."""

from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import product
from random import Random

import sympy as sp


q, tau_symbol = sp.symbols("q tau", real=True)
short_flow, long_flow = (q + 1) / 2, (7 - q) / 2
assert sp.expand(short_flow + long_flow - 4) == 0
assert sp.expand(long_flow + q - short_flow - 3) == 0
cycle_polynomial = (12 * tau_symbol + 1) * q**2 + 10 * q - 23
assert sp.expand(
    long_flow**2 / 6 - short_flow**2 / 2 - tau_symbol * q**2
    + cycle_polynomial / 12
) == 0
assert sp.expand(short_flow**2 / 2 + long_flow**2 / 6 - 2 - (q - 1)**2 / 6) == 0

rng = Random(931)
scenario_count = 0
with localcontext() as context:
    context.prec = 70
    for n in range(1, 9):
        for _ in range(5):
            weights = [rng.randrange(1, 35) for _ in range(n)]
            total_weight = sum(weights)
            target = rng.randrange(1, total_weight + 1)
            gap = Decimal(6) / Decimal(31 * target + 18 * total_weight)**2
            feasible_subset = False
            best_value = Decimal("-Infinity")
            for choices in product((0, 1), repeat=n):
                selected_sum = sum(a * z for a, z in zip(weights, choices))
                tau = Fraction(1, 2) + Fraction(selected_sum, 2 * target)
                edge_resistances = [
                    Fraction(1, 2 * n) + Fraction(a * z, 2 * target)
                    for a, z in zip(weights, choices)
                ]
                assert sum(edge_resistances, Fraction(0)) == tau
                coefficient = 12 * Decimal(tau.numerator) / Decimal(tau.denominator) + 1
                flow = Decimal(46) / ((100 + 92 * coefficient).sqrt() + 10)
                assert 0 < flow < 2
                value = 1 - (flow - 1)**2 / 6
                best_value = max(best_value, value)
                if selected_sum == target:
                    feasible_subset = True
                    assert abs(value - 1) < Decimal("1e-65")
                else:
                    assert 1 - value >= gap - Decimal("1e-65")
                for resistance, a, z in zip(edge_resistances, weights, choices):
                    assert 6 * n * target * resistance == 3 * target + 3 * n * a * z
                scenario_count += 1
            assert (abs(best_value - 1) < Decimal("1e-65")) == feasible_subset

print(
    f"PASS: 4 symbolic identities; {scenario_count} scenarios across 40 instances; "
    "series aggregation, root sign, gap, integer scaling, threshold equivalence"
)
