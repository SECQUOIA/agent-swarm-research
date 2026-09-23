"""Independent diagnostic of manuscript crossing against atan2.

Integer sign calculations determine manuscript k exactly. Floating-point angles
are only an independent finite diagnostic, never a proof or exact certificate.
"""
import math
from itertools import product
points = [(x, y) for x, y in product(range(-8, 9), repeat=2) if x or y]
count = 0
worst_error = 0.0
for start, end in product(points, repeat=2):
    d = start[0] * end[1] - start[1] * end[0]
    h = start[0] * end[0] + start[1] * end[1]
    if d == 0 and h < 0:
        continue
    k = 1 if start[1] < 0 <= end[1] and d > 0 else (-1 if end[1] < 0 <= start[1] and d < 0 else 0)
    alpha_start = math.atan2(start[1], start[0]) % math.tau
    alpha_end = math.atan2(end[1], end[0]) % math.tau
    delta = math.atan2(d, h)
    error = abs(delta - (alpha_end - alpha_start + math.tau * k))
    worst_error = max(worst_error, error)
    assert error < 4e-15, (start, end, k, error)
    count += 1
print(f'PASS {count} integer-coordinate phasor pairs; max angle identity residual {worst_error:.3g}')
print('Independent floating-point diagnostic only; signs are exact integers.')
