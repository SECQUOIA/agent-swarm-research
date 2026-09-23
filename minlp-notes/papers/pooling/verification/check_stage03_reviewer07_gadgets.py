"""Exact local arithmetic checks used in stage 03, round 01, review 07."""
from fractions import Fraction as F

vals = [F(k, 4) for k in range(9)]
count = 0
for x in vals:
    for beta in [F(1), F(3), F(33)]:
        u = [x, 2 - x]
        v = u
        middle = [4 - 2 * x, 2 * x]
        assert sum(middle) == 4 and sum(u) == 2
        for a, b, m in zip(u, v, middle):
            assert a + b + m == 4 and beta * b + beta * m / 2 == 2 * beta
        count += 1
    u = [x, 2 - x]
    v = [x / 2, 1 - x / 2]
    middle = [3 - 3 * x / 2, 3 * x / 2]
    assert sum(middle) == 3
    for a, b, m in zip(u, v, middle):
        assert a + b + m == 3 and 3 * b + m == 3
    assert x + 2 * (1 - x / 2) == 2
    count += 1
for u in vals:
    for w in vals:
        v = (u + w) / 2
        full = [v, v, 2 - u, 2 - w]
        half = [v, 1 - u / 2, 1 - w / 2]
        assert sum(full) == 4 and sum(half) == 2
        residuals = [c - f for c, f in zip([2, 1, 1], half)]
        assert min(residuals) >= 0 and sum(residuals) == 2
        count += 1
for u in vals:
    for v in vals:
        if u + v <= 2:
            flows = [u, v, 2 - u - v]
            mates = [2 - f for f in flows]
            assert sum(flows) == 2 and sum(mates) == 4
            assert sum(2 - f for f in mates) == 2
            count += 1
print('PASS:', count, 'exact rational gadget/averaging/splitting cases; endpoints included.')
