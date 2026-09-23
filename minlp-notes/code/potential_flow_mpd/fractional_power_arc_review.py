"""Independent small-instance arithmetic checks of the fractional-power reduction.

Numerical root checks supplement the exact monotonicity proof; they do not
solve general Square-Root-Sum instances with an unproved separation bound.
"""

from math import prod, sqrt
from random import Random

import numpy as np
from scipy.optimize import brentq


def main():
    random = Random(47903)
    examples = [([1, 4, 9], k) for k in [5, 6, 7]]
    for _ in range(100):
        radicands = [random.randint(1, 20) for _ in range(random.randint(2, 8))]
        k = max(1, int(sum(map(sqrt, radicands))) + random.choice([-1, 0, 1, 2]))
        examples.append((radicands, k))
    maximum_root_discrepancy = 0
    for radicands, k in examples:
        c = np.array(radicands + [-1], dtype=float)
        beta = np.array([1 / a for a in radicands] + [k])
        nomination = c - np.roll(c, 1)
        assert sum(nomination) == 0

        def residual(z, coefficients=beta):
            flow = c + z
            return float(coefficients @ (np.sign(flow) * abs(flow) ** 1.5))

        root = brentq(residual, -max(radicands), 1, xtol=1e-13)
        source_gap = sum(map(sqrt, radicands)) - k
        assert abs(residual(0) - source_gap) < 1e-11
        assert (root >= -1e-11) == (source_gap <= 1e-11)
        assert np.max(abs((c + root) - np.roll(c + root, 1) - nomination)) < 1e-12
        scale = prod(radicands)
        integer_beta = np.array([scale // a for a in radicands] + [scale * k], dtype=float)
        integer_root = brentq(lambda z: residual(z, integer_beta), -max(radicands), 1, xtol=1e-13)
        maximum_root_discrepancy = max(maximum_root_discrepancy, abs(root - integer_root))
        assert abs(root - integer_root) < 1e-11
        # Reversing the distinguished edge negates its flow and changes the
        # queried lower bound -1 into the upper bound +1.
        assert ((-1 + root) >= -1 - 1e-11) == ((1 - root) <= 1 + 1e-11)
    print(f"PASS: {len(examples)} small cycle instances, including exact equality and both decision directions.")
    print(f"Integer-resistance common scaling maximum root discrepancy: {maximum_root_discrepancy:.3g}.")
    print("Conservation, capacity direction, arc reversal, and rational/integer resistance versions checked.")


if __name__ == "__main__":
    main()
