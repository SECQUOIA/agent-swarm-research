"""Exact block-hull formulas versus an unmerged simplex-state feasibility LP.

The formula calculation uses Fraction throughout.  The independent LP retains
every simplex state for every block, including states the formulas aggregate.
It checks degenerate polygons, zero weights, repeated path observations, and
independent blocks with different observed-state sets.  It does not test graph
block extraction, which is a separate combinatorial preprocessing step.
"""

from fractions import Fraction as F
import random
import numpy as np
from scipy.optimize import linprog


def feasible_formula(base, weights, aggregate, observations):
    active = sorted(set(j for j, h, q in observations))
    states = [(j, weights[j]) for j in active]
    states.append((-1, 1 - sum(weights[j] for j in active)))
    lower_total = [F(0)] * 3
    upper_total = [F(0)] * 3
    for j, weight in states:
        low = [weight * a for a, b in base]
        high = [weight * b for a, b in base]
        for jj, h, q in observations:
            if jj == j:
                low[h] = max(low[h], q)
                high[h] = min(high[h], q)
        if any(a > b for a, b in zip(low, high)):
            return False
        if low[0] + low[1] > high[2] or low[2] > high[0] + high[1]:
            return False
        tight_low = [max(low[0], low[2] - high[1]),
                     max(low[1], low[2] - high[0]),
                     max(low[2], low[0] + low[1])]
        tight_high = [min(high[0], high[2] - low[1]),
                      min(high[1], high[2] - low[0]),
                      min(high[2], high[0] + high[1])]
        lower_total = [a + b for a, b in zip(lower_total, tight_low)]
        upper_total = [a + b for a, b in zip(upper_total, tight_high)]
    totals = [aggregate[0], aggregate[1], sum(aggregate)]
    return all(a <= x <= b for a, x, b in zip(lower_total, totals, upper_total))


def sample_point(rng, base):
    points = [(F(s, 3), F(t, 3)) for s in range(-9, 10) for t in range(-9, 10)
              if base[0][0] <= F(s, 3) <= base[0][1]
              and base[1][0] <= F(t, 3) <= base[1][1]
              and base[2][0] <= F(s + t, 3) <= base[2][1]]
    return rng.choice(points)


def decompose(base, weights, aggregate, observations):
    """Construct merged coordinates, refine them, and check original contracts."""
    active = sorted(set(j for j, h, q in observations))
    labels = active + [-1]
    state_weights = [weights[j] for j in active] + [1 - sum(weights[j] for j in active)]
    polygons, supports = [], []
    for j, weight in zip(labels, state_weights):
        low = [weight * a for a, b in base]
        high = [weight * b for a, b in base]
        for jj, h, q in observations:
            if jj == j:
                low[h], high[h] = max(low[h], q), min(high[h], q)
        polygons.append((low, high))
        supports.append(([max(low[0], low[2] - high[1]),
                          max(low[1], low[2] - high[0]),
                          max(low[2], sum(low[:2]))],
                         [min(high[0], high[2] - low[1]),
                          min(high[1], high[2] - low[0]),
                          min(high[2], sum(high[:2]))]))
    suffix_low = [sum(a[h] for a, b in supports) for h in range(3)]
    suffix_high = [sum(b[h] for a, b in supports) for h in range(3)]
    remaining = list(aggregate)
    merged = {}
    for j, (low, high), (a, b) in zip(labels, polygons, supports):
        suffix_low = [x - y for x, y in zip(suffix_low, a)]
        suffix_high = [x - y for x, y in zip(suffix_high, b)]
        rh = [remaining[0], remaining[1], sum(remaining)]
        il = [max(low[h], rh[h] - suffix_high[h]) for h in range(3)]
        iu = [min(high[h], rh[h] - suffix_low[h]) for h in range(3)]
        s = max(il[0], il[2] - iu[1])
        t = max(il[1], il[2] - s)
        assert all(il[h] <= value <= iu[h] for h, value in enumerate([s, t, s + t]))
        merged[j] = [s, t]
        remaining = [remaining[0] - s, remaining[1] - t]
    assert remaining == [0, 0]

    refined = []
    rest_weight = state_weights[-1]
    for j, weight in enumerate(weights):
        if j in merged:
            point = merged[j]
        elif rest_weight:
            point = [weight * v / rest_weight for v in merged[-1]]
        else:
            assert weight == 0
            point = [F(0), F(0)]
        refined.append(point)
        assert all(weight * low <= value <= weight * high
                   for (low, high), value in zip(base, [point[0], point[1], sum(point)]))
    assert [sum(point[h] for point in refined) for h in range(2)] == aggregate
    for j, h, q in observations:
        assert (refined[j][h] if h < 2 else sum(refined[j])) == q


def check(seed):
    rng = random.Random(seed)
    count = rng.randrange(2, 9)  # includes the original residual state
    raw = [rng.randrange(0, 6) for j in range(count)]
    raw[0] += 1
    weights = [F(v, sum(raw)) for v in raw]
    blocks = []
    for block in range(rng.randrange(1, 5)):
        base = [(F(-rng.randrange(0, 4)), F(rng.randrange(0, 4))) for h in range(3)]
        points = [sample_point(rng, base) for j in range(count)]
        aggregate = [sum(weights[j] * points[j][h] for j in range(count)) for h in range(2)]
        observations = []
        for j in range(count - 1):  # no direct observation at the residual vertex
            for h in range(3):
                if rng.random() < .35:
                    val = points[j][h] if h < 2 else sum(points[j])
                    observations.append((j, h, weights[j] * val))
                    if rng.random() < .15:
                        observations.append((j, h, weights[j] * val))
        if seed % 2 and observations:
            idx = rng.randrange(len(observations))
            j, h, val = observations[idx]
            observations[idx] = j, h, val + F(rng.choice([-1, 1]), 5)
        if seed % 3 == 1:
            aggregate[rng.randrange(2)] += F(1, 7)
        blocks.append((base, aggregate, observations))

    predicted = all(feasible_formula(base, weights, aggregate, obs)
                    for base, aggregate, obs in blocks)
    size = 2 * count * len(blocks)
    a_ub, b_ub, a_eq, b_eq = [], [], [], []
    for k, (base, aggregate, obs) in enumerate(blocks):
        for j, weight in enumerate(weights):
            for h, (low, high) in enumerate(base):
                row = np.zeros(size)
                for coord in ([h] if h < 2 else [0, 1]):
                    row[2 * (k * count + j) + coord] = 1
                a_ub += [row, -row]
                b_ub += [float(weight * high), float(-weight * low)]
        for h in range(2):
            row = np.zeros(size)
            for j in range(count):
                row[2 * (k * count + j) + h] = 1
            a_eq.append(row)
            b_eq.append(float(aggregate[h]))
        for j, h, q in obs:
            row = np.zeros(size)
            for coord in ([h] if h < 2 else [0, 1]):
                row[2 * (k * count + j) + coord] = 1
            a_eq.append(row)
            b_eq.append(float(q))
    result = linprog(np.zeros(size), A_ub=a_ub, b_ub=b_ub,
                     A_eq=a_eq, b_eq=b_eq, bounds=(None, None), method="highs")
    assert result.status in (0, 2), (seed, result.message)
    assert predicted == result.success, (seed, predicted, result.message)
    if predicted:
        for base, aggregate, observations in blocks:
            decompose(base, weights, aggregate, observations)
    return predicted


if __name__ == "__main__":
    accepted = sum(check(seed) for seed in range(400))
    print(f"Passed 400 exact-formula versus full unmerged LP classifications: "
          f"{accepted} feasible, {400 - accepted} infeasible.")
    print("All feasible cases passed exact rational constructive decomposition "
          "and refinement checks against the original unmerged contracts.")
