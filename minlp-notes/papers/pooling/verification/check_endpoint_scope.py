"""Exact checks of the upper-only endpoint formulation and its scope boundary."""

from fractions import Fraction as F
from itertools import product


def main():
    grid = [F(i, 4) for i in range(5)]
    checked = 0
    for clean, dirty, strict_delivery in product(grid, repeat=3):
        total = clean + dirty
        if total > 1 or strict_delivery > total:
            continue
        lax_delivery = total - strict_delivery
        quality = dirty / total if total else F(0)
        original_upper_constraints = (quality*strict_delivery <= 0
                                      and quality*lax_delivery <= lax_delivery)
        support_disjunction = dirty == 0 or strict_delivery == 0
        assert original_upper_constraints == support_disjunction
        checked += 1

    # An exact-quality-one product has upper bound one but also a lower bound.
    # The upper-only formulation cannot represent the lower bound.
    clean, dirty, delivery = F(1), F(0), F(1)
    d, s = dirty, F(0)  # No outlet has upper bound zero.
    assert d == 0 or s == 0
    quality_mass = dirty*delivery/(clean+dirty)
    assert not (delivery <= quality_mass <= delivery)
    print(f'PASS: {checked} exact physical/disjunctive comparisons; '
          'the missing-lower-bound counterexample is reproduced.')


if __name__ == '__main__':
    main()
