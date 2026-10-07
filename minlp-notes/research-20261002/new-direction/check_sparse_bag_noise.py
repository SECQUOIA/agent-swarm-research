"""Exact diagnostic for the conditional bag-count inequality; not a proof."""

from fractions import Fraction as Q
from itertools import product


BOUNDS = ((Q(0), Q(1)), (Q(-1, 4), Q(2, 3)))
SIGMA, N, L, AMBIENT_N = Q(4), 8, Q(2), 3
NOISE = tuple(-SIGMA + 2 * SIGMA * k / (N - 1) for k in range(N))


def grid(lo, hi, h):
    nodes = []
    value = lo
    while value < hi:
        nodes.append(value)
        value += h
    return tuple(nodes + [hi])


def value(v, private_noise):
    x, y = v
    # Minimize x^2+y^2-z^2+(2x-3y+1/3+private_noise)z over z in [0,1].
    return x * x + y * y + min(Q(0), 2 * x - 3 * y - Q(2, 3) + private_noise)


def minimum(noise, private_noise):
    costs = []
    for z in (0, 1):
        coeffs = (noise[0] + 2 * z, noise[1] - 3 * z)
        points = [max(lo, min(hi, -a / 2)) for a, (lo, hi) in zip(coeffs, BOUNDS)]
        costs.append(sum(t * t + a * t for t, a in zip(points, coeffs))
                     + z * (private_noise - Q(2, 3)))
    return min(costs)


cases = checked_tuples = negative_intervals = 0
for private_noise in NOISE[3:5]:
    optima = {noise: minimum(noise, private_noise) for noise in product(NOISE, repeat=2)}
    for level in range(4):
        h = Q(1, 2 ** level)
        epsilon = AMBIENT_N * L * h * h / 4
        grids = tuple(grid(lo, hi, h) for lo, hi in BOUNDS)
        regular = tuple({t for t in nodes if t - h in nodes and t + h in nodes}
                        for nodes in grids)
        assert all(len(nodes) - len(interior) <= 3 for nodes, interior in zip(grids, regular))
        total_near = 0
        for v in product(*grids):
            checked_tuples += 1
            base = value(v, private_noise)
            intervals = []
            probability_bound = Q(1)
            for i in range(2):
                if v[i] not in regular[i]:
                    intervals.append(None)
                    continue
                plus, minus = list(v), list(v)
                plus[i] += h
                minus[i] -= h
                lower = (base - value(plus, private_noise) - epsilon) / h
                upper = (value(minus, private_noise) - base + epsilon) / h
                width = upper - lower
                assert width <= L * h + 2 * epsilon / h
                negative_intervals += width < 0
                intervals.append((lower, upper))
                probability_bound *= max(Q(0), min(Q(1), width / (2 * SIGMA) + Q(1, N))) if width >= 0 else Q(0)
            near = rectangle = 0
            for noise, optimum in optima.items():
                in_rectangle = all(interval is None or interval[0] <= noise[i] <= interval[1]
                                   for i, interval in enumerate(intervals))
                is_near = base + sum(a * t for a, t in zip(noise, v)) <= optimum + epsilon
                assert not is_near or in_rectangle
                near += is_near
                rectangle += in_rectangle
            assert Q(rectangle, N * N) <= probability_bound
            total_near += near
        factors = [3 + (1 + Q(AMBIENT_N, 2)) * L * (hi - lo) / (2 * SIGMA)
                   + (hi - lo) / (N * h) for lo, hi in BOUNDS]
        cap_factors = [4 + (1 + Q(AMBIENT_N, 2)) * L * (hi - lo) / (2 * SIGMA)
                       for lo, hi in BOUNDS]
        expected = Q(total_near, N * N)
        bound = factors[0] * factors[1]
        assert expected <= bound <= cap_factors[0] * cap_factors[1]
        print(f"outside={private_noise}, level={level}: E[count]={expected}, bound={bound}")
        cases += 1

assert negative_intervals > 0
print(f"PASS: {cases} clipped-grid cases, {checked_tuples} tuples; "
      f"{negative_intervals} empty comparison intervals.")
