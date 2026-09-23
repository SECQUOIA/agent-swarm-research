"""Exact finite checks of the PARTITION-to-envelope reduction.

YES cases use a complementary-pair primal certificate. NO cases use an explicit
affine lower certificate checked on every binary vertex. Fractions are exact;
no floating-point envelope solver or unverified rounding is used.
"""

from fractions import Fraction as Q
from math import prod
import random


def check_instance(original, scale):
    a = [2 * value for value in original]  # Preserve PARTITION; force even total.
    total = sum(a)
    eps = Q(1, 16 * scale * total**3)
    baseline = 1 + eps * total / 2 + eps**2 * (Q(total**2, 8) - Q(sum(v*v for v in a), 4))
    threshold = baseline + eps**2 / 4
    values, sums = [], []
    partition = None
    for mask in range(1 << len(a)):
        bits = [int(bool(mask & (1 << i))) for i in range(len(a))]
        subtotal = sum(value * bit for value, bit in zip(a, bits))
        value = prod(1 + eps * weight * bit for weight, bit in zip(a, bits))
        quadratic = 1 + eps * subtotal + eps**2 / 2 * (
            subtotal**2 - sum(weight**2 * bit for weight, bit in zip(a, bits)))
        remainder = value - quadratic
        assert 0 <= remainder <= eps**2 / (8 * scale)
        values.append(value)
        sums.append(subtotal)
        if subtotal == total // 2:
            partition = mask
    slopes = [eps * weight + eps**2 / 2 * (total * weight - weight**2) for weight in a]
    tilted_values = [value - sum(slopes[i] for i in range(len(a)) if mask & (1 << i))
                     for mask, value in enumerate(values)]
    tilted_base = 1 - eps**2 * Q(total**2, 8)
    accuracy = eps**2 / 32
    tilted_threshold = tilted_base + eps**2 / 4
    if partition is not None:
        complement = ((1 << len(a)) - 1) ^ partition
        primal = (values[partition] + values[complement]) / 2
        assert primal <= baseline + eps**2 / 8 < threshold
        assert min(tilted_values) <= tilted_base + eps**2 / 8
        assert min(tilted_values) + accuracy < tilted_threshold
        return True, len(values)

    # A globally valid affine lower bound follows from the binary variance gap.
    constant = 1 - eps**2 * Q(total**2, 8) + eps**2 / 2
    for mask, value in enumerate(values):
        affine = constant + sum(slopes[i] for i in range(len(a)) if mask & (1 << i))
        assert value >= affine
        assert (sums[mask] - total // 2)**2 >= 1
    midpoint_lower = constant + sum(slopes) / 2
    assert midpoint_lower == baseline + eps**2 / 2 > threshold
    assert min(tilted_values) >= tilted_base + eps**2 / 2
    assert min(tilted_values) - accuracy > tilted_threshold
    return False, len(values)


def main():
    rng = random.Random(2026090431)
    yes = no = vertices = 0
    for _ in range(120):
        original = [rng.randrange(1, 14) for _ in range(rng.randrange(1, 10))]
        is_yes, checked = check_instance(original, rng.choice([1, 2, 7, 31]))
        yes += is_yes
        no += not is_yes
        vertices += checked
    print(f"Passed 120 exact reduction checks: {yes} YES and {no} NO instances.")
    print(f"Checked remainder bounds on {vertices} binary vertices.")
    print("YES primal mixtures and NO affine lower certificates strictly straddle the threshold.")
    print("Direct tilted-MIN values remain separated under additive error epsilon^2/32.")


if __name__ == "__main__":
    main()
