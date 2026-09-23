"""Independent finite exact checks using arbitrary rational-radius integer points.
The oracle solves a segment/ray intersection; it does not call paper check code.
"""
from fractions import Fraction as F
from itertools import product

pts = [tuple(map(F, p)) for p in product(range(-4, 5), repeat=2) if p != (0, 0)]
count = axes = long_arcs = 0
for start, end in product(pts, repeat=2):
    dot = start[0]*end[0] + start[1]*end[1]
    det = start[0]*end[1] - start[1]*end[0]
    if det == 0 and dot < 0:
        continue
    formula = (1 if start[1] < 0 <= end[1] and det > 0 else
               -1 if end[1] < 0 <= start[1] and det < 0 else 0)
    oracle = 0
    if start[1] != end[1]:
        t = -start[1]/(end[1]-start[1])
        hit_x = start[0] + t*(end[0]-start[0])
        if hit_x > 0:
            if start[1] < 0 and 0 < t <= 1:
                oracle = 1
            elif end[1] < 0 and 0 <= t < 1:
                oracle = -1
    assert formula == oracle, (start, end, formula, oracle)
    count += 1
    axes += start[1] == 0 or end[1] == 0
    long_arcs += dot < 0
print(f'PASS: {count} exact ordered phasor pairs, {axes} real-axis cases, {long_arcs} arcs longer than pi/2.')
