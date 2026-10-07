"""Exact, scoped checks for simplex multiplier atoms and patch repair."""

from collections import Counter
from fractions import Fraction as Q
from itertools import product


def clip(value, lower, upper):
    return min(upper, max(lower, value))


def project_slab(vector, lower, upper, sum_lower, sum_upper):
    """Return the rational Euclidean projection and a sum multiplier."""
    clipped = tuple(clip(v, lo, hi) for v, lo, hi in zip(vector, lower, upper))
    if sum_lower <= sum(clipped) <= sum_upper:
        return clipped, Q(0)
    target = sum_lower if sum(clipped) < sum_lower else sum_upper
    breaks = sorted({v - bound for v, lo, hi in zip(vector, lower, upper)
                     for bound in (lo, hi)})
    probes = [breaks[0] - 1, *breaks, breaks[-1] + 1]
    for left, right in zip(probes, probes[1:]):
        middle = (left + right) / 2
        free = [i for i, v in enumerate(vector)
                if lower[i] < v - middle < upper[i]]
        fixed = sum(clip(v - middle, lo, hi)
                    for i, (v, lo, hi) in enumerate(zip(vector, lower, upper))
                    if i not in free)
        alpha = ((fixed + sum(vector[i] for i in free) - target) / len(free)
                 if free else left)
        if left <= alpha <= right:
            answer = tuple(clip(v - alpha, lo, hi)
                           for v, lo, hi in zip(vector, lower, upper))
            if sum(answer) == target:
                return answer, alpha
    raise AssertionError("No rational threshold found")


def verify_projection(vector, lower, upper, sum_lower, sum_upper, answer, alpha):
    assert all(lo <= y <= hi for y, lo, hi in zip(answer, lower, upper))
    assert sum_lower <= sum(answer) <= sum_upper
    if sum(answer) != sum_lower:
        assert alpha >= 0
    if sum(answer) != sum_upper:
        assert alpha <= 0
    for v, y, lo, hi in zip(vector, answer, lower, upper):
        residual = y - v + alpha
        if lo < y < hi:
            assert residual == 0
        elif y == lo:
            assert residual >= 0
        elif y == hi:
            assert residual <= 0


def multiplier_checks():
    draws = comparisons = zero_atoms = 0
    for dimension in (2, 3):
        lower, upper = (Q(0),) * dimension, (Q(1),) * dimension
        center = (Q(1, dimension),) * dimension
        for grid_size in (2, 4, 8):
            noise = tuple(-1 + Q(2 * i, grid_size - 1) for i in range(grid_size))
            counts = Counter()
            for gamma in product(noise, repeat=dimension):
                vector = tuple(a - g / 2 for a, g in zip(center, gamma))
                point, alpha = project_slab(vector, lower, upper, Q(0), Q(1))
                verify_projection(vector, lower, upper, Q(0), Q(1), point, alpha)
                support = tuple(i for i, x in enumerate(point) if x > 0)
                tight = sum(point) == 1
                gradient = tuple(2 * (x - a) + g
                                 for x, a, g in zip(point, center, gamma))
                budget_multiplier = -gradient[support[0]] if tight else Q(0)
                assert budget_multiplier >= 0
                active = []
                if tight:
                    active.append(("budget", budget_multiplier))
                for i in range(dimension):
                    multiplier = gradient[i] + budget_multiplier
                    if i in support:
                        assert multiplier == 0
                    else:
                        assert multiplier >= 0
                        active.append((i, multiplier))
                free_dimension = len(support) - int(tight)
                for facet, multiplier in active:
                    zero_atoms += multiplier == 0
                    for threshold in (Q(0), Q(1, 8), Q(1, 2)):
                        if multiplier <= threshold:
                            counts[(support, tight, free_dimension, facet, threshold)] += 1
                draws += 1
            for (_, _, free_dimension, _, threshold), count in counts.items():
                probability = Q(count, grid_size ** dimension)
                bound = 2 ** free_dimension * (threshold + Q(1, grid_size))
                assert probability <= bound
                comparisons += 1
    assert zero_atoms > 0
    return draws, comparisons, zero_atoms


def patch_checks():
    fixtures = [
        ((Q(0), Q(0), Q(0)), (Q(1), Q(1), Q(1)), Q(1), True),
        ((Q(1, 8), Q(1, 7)), (Q(3, 4), Q(5, 7)), Q(1), False),
        ((Q(1, 4), Q(1, 4), Q(1, 4)),
         (Q(1, 4) + Q(1, 2 ** 200),) * 3,
         Q(3, 4) + Q(3, 2 ** 201), True),
    ]
    projections = balls = 0
    for lower, upper, budget, equality in fixtures:
        width_sum = sum(hi - lo for lo, hi in zip(lower, upper))
        lam = ((budget - sum(lower)) / width_sum if equality
               else min(Q(1, 2), (budget - sum(lower)) / (2 * width_sum)))
        center = tuple(lo + lam * (hi - lo) for lo, hi in zip(lower, upper))
        assert all(lo < c < hi for lo, c, hi in zip(lower, center, upper))
        if equality:
            assert sum(center) == budget
            reduced_lower, reduced_upper = lower[:-1], upper[:-1]
            reduced_center = center[:-1]
            sum_lower, sum_upper = budget - upper[-1], budget - lower[-1]
        else:
            assert sum(center) < budget
            reduced_lower, reduced_upper, reduced_center = lower, upper, center
            sum_lower, sum_upper = sum(lower) - 1, budget
        dimension = len(reduced_center)
        slacks = [(c - lo, 1) for lo, c in zip(reduced_lower, reduced_center)]
        slacks += [(hi - c, 1) for hi, c in zip(reduced_upper, reduced_center)]
        slacks += [(sum(reduced_center) - sum_lower, dimension),
                   (sum_upper - sum(reduced_center), dimension)]
        radius = min(slack / (1 + row_norm) for slack, row_norm in slacks)
        assert radius > 0
        assert all(radius * row_norm < slack for slack, row_norm in slacks)
        balls += 1
        for displacement in product((Q(-2), Q(0), Q(2)), repeat=dimension):
            vector = tuple(c + delta for c, delta in zip(reduced_center, displacement))
            answer, alpha = project_slab(vector, reduced_lower, reduced_upper,
                                         sum_lower, sum_upper)
            verify_projection(vector, reduced_lower, reduced_upper,
                              sum_lower, sum_upper, answer, alpha)
            physical = (*answer, budget - sum(answer)) if equality else answer
            assert all(lo <= x <= hi for x, lo, hi in zip(physical, lower, upper))
            assert sum(physical) <= budget
            if equality:
                assert sum(physical) == budget
            projections += 1
    return balls, projections


if __name__ == "__main__":
    draws, comparisons, zero_atoms = multiplier_checks()
    balls, projections = patch_checks()
    print(f"PASS: {draws} finite-noise draws, {comparisons} face/multiplier bounds, "
          f"{zero_atoms} zero-multiplier incidences")
    print(f"PASS: {balls} rational relative-interior balls, {projections} exact "
          "projection/KKT checks, including 200-bit thin equality patch")
