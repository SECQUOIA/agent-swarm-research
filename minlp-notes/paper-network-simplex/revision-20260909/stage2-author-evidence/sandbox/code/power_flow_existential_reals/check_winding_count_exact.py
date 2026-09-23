"""Exact boundary checks for the real-angle ETR encoding; no solver needed.

Eight rational rays represent multiples of pi/4. Integer ray indices give
an independent lift/winding oracle without evaluating trigonometric functions.
Positive rational rescaling tests that unequal voltage magnitudes are harmless.
"""
from fractions import Fraction
from itertools import product

RAYS = ((1, 0), (1, 1), (0, 1), (-1, 1),
        (-1, 0), (-1, -1), (0, -1), (1, -1))
SCALES = (Fraction(1, 7), Fraction(1), Fraction(13))


def crossing(start, end):
    e_j, f_j = start
    e_i, f_i = end
    if e_i + e_j > 0:
        if f_j < 0 <= f_i:
            return 1
        if f_i < 0 <= f_j:
            return -1
    return 0


def short_step(a, b):
    return (b - a + 4) % 8 - 4


def main():
    pairs = cycles = nonzero = 0
    for a, b, scale_a, scale_b in product(range(8), range(8), SCALES, SCALES):
        start = tuple(scale_a * v for v in RAYS[a])
        end = tuple(scale_b * v for v in RAYS[b])
        step = short_step(a, b)
        dot = sum(x * y for x, y in zip(start, end))
        assert (dot >= 0) == (abs(step) <= 2)
        if abs(step) > 2:
            continue
        expected = (a + step) // 8 - a // 8
        assert crossing(start, end) == expected, (a, b, scale_a, scale_b)
        assert crossing(end, start) == -expected
        pairs += 1

    # Include repeated vertices, axis contacts, both traversal directions,
    # zero-winding cycles, and quarter-turn winding counterexamples.
    for length in (3, 4, 5):
        for vertices in product(range(8), repeat=length):
            edges = list(zip(vertices, vertices[1:] + vertices[:1]))
            steps = [short_step(a, b) for a, b in edges]
            if any(abs(step) > 2 for step in steps):
                continue
            total = sum(steps)
            assert total % 8 == 0
            winding = total // 8
            assert sum(crossing(RAYS[a], RAYS[b]) for a, b in edges) == winding
            cycles += 1
            nonzero += winding != 0
    assert crossing(RAYS[7], RAYS[0]) == 1
    assert crossing(RAYS[0], RAYS[7]) == -1
    assert sum(crossing(RAYS[a], RAYS[b]) for a, b in
               ((0, 2), (2, 4), (4, 6), (6, 0))) == 1
    print(f"PASS: {pairs} scaled pairs; {cycles} cycles; {nonzero} nonzero windings")


if __name__ == "__main__":
    main()
