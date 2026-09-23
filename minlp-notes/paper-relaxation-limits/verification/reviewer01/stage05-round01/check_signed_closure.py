"""Exact finite stress test of width closure, signs, and character Gram entries.

This does not establish the random-instance or universal width theorem.
"""
from itertools import product
from collections import defaultdict
import json

supports = [0b000111, 0b011001, 0b101010, 0b110100]

def closure(signs, width):
    derived = {(0, 1), *zip(supports, signs)}
    while True:
        new = {(a ^ b, s * t) for a, s in derived for b, t in derived
               if (a ^ b).bit_count() <= width}
        if new <= derived:
            return derived
        derived |= new

counts = defaultdict(int)
for signs in product((-1, 1), repeat=4):
    sat = [x for x in range(64) if all(
        (-1) ** ((x & a).bit_count()) == s for a, s in zip(supports, signs))]
    for width in (3, 4, 5):
        derived = closure(signs, width)
        contradiction = (0, -1) in derived
        assert not contradiction or not sat
        if width >= 4:
            assert contradiction == (not sat)
        if contradiction:
            counts['contradictions'] += 1
            continue
        counts['consistent_closures'] += 1
        y = dict(derived)
        assert len(y) == len(derived) and y[0] == 1
        assert all(y[a] == s for a, s in zip(supports, signs))
        indices = [a for a in range(64) if a.bit_count() <= width // 2]
        classes = {}
        for a in indices:
            if a not in classes:
                for b in indices:
                    if a ^ b in y:
                        assert b not in classes
                        classes[b] = (a, y[a ^ b])
        for a in indices:
            for b in indices:
                ca, sa = classes[a]
                cb, sb = classes[b]
                assert y.get(a ^ b, 0) == (sa * sb if ca == cb else 0)
                counts['exact_gram_entries'] += 1
        # Several dense polynomials use all six variables jointly.
        for shift in range(7):
            coeff = {a: ((a * 17 + shift * 11) % 13) - 6 for a in indices}
            value = sum(coeff[a] * coeff[b] * y.get(a ^ b, 0)
                        for a in indices for b in indices)
            grouped = defaultdict(int)
            for a in indices:
                ca, sa = classes[a]
                grouped[ca] += coeff[a] * sa
            assert value == sum(v * v for v in grouped.values()) >= 0
            counts['dense_square_checks'] += 1
        if width == 3:
            assert all(y.get(a, 0) == 0 for a in range(1, 64)
                       if a.bit_count() <= 2)
            counts['odd_width_signed_cubic_cases'] += 1

assert 384 * 3 ** 24 < 2 ** 64
print(json.dumps({'arithmetic': 'exact integer', 'counts': dict(counts),
                  'limit': 'Finite stress test only; no asymptotic inference.'}, indent=2))
