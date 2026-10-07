#!/usr/bin/env python3
"""Exact finite checks for the product-face rounding certificate."""

from bisect import bisect_left
from fractions import Fraction as F
from itertools import product

from check_mixed_shell_certificate import grid as physical_grid
from check_mixed_shell_certificate import distribution as physical_rounding


def grid(delta, dimension):
    values = [F(0), delta / dimension]
    while values[-1] < 1:
        values.append(min(F(1), (1 + delta) * values[-1]))
    return values


def rounding(value, values):
    j = bisect_left(values, value)
    if values[j] == value:
        return [(value, F(1))]
    lower, upper = values[j - 1], values[j]
    return [(lower, (upper - value) / (upper - lower)),
            (upper, (value - lower) / (upper - lower))]


def objective(a, c, b, x, y):
    dimension = len(x)
    return (sum(a[i][j] * x[i] * x[j]
                for i in range(dimension) for j in range(dimension))
            + sum(c[i] * x[i] for i in range(dimension))
            + sum(b[i][j] * x[i] * y[j]
                  for i in range(dimension) for j in range(len(y))))


# Each fixture supplies a valid positive active-curvature upper bound.
# Free integer endpoints may be far apart; no interior labels are tabled.
fixtures = [
    ([[F(-1, 2)]], [F(2)], [[F(-1)]], [(F(0), F(1))], F(1)),
    ([[F(1), F(-1, 2)], [F(-1, 2), F(1)]],
     [F(1), F(1)],
     [[F(-1, 4), F(1, 10**6)], [F(1, 4), F(-1, 2 * 10**6)]],
     [(F(0), F(1)), (F(0), F(10**6))], F(2)),
    ([[F(0), F(-1)], [F(-1), F(0)]],
     [F(2), F(2)], [[F(1, 2)], [F(-1, 2)]],
     [(F(-1), F(1))], F(1)),
]

rounding_cases = 0
radial_cases = 0
table_entries = 0
certificates = 0
for a, c, b, bounds, curvature in fixtures:
    dimension = len(c)
    free_endpoints = list(product(*bounds))
    for i in range(dimension):
        slope_min = c[i] + sum(min(b[i][j] * lo, b[i][j] * hi)
                               for j, (lo, hi) in enumerate(bounds))
        assert slope_min >= 0
        assert 2 * a[i][i] <= curvature
    for delta in (F(1, 2), F(1, 4)):
        values = grid(delta, dimension)
        sigma = curvature * delta**2 / 8
        shell = [u for u in product(values, repeat=dimension) if max(u) == 1]
        minimum = min(objective(a, c, b, u, v)
                      - 2 * sigma * sum(t * t for t in u)
                      for u in shell for v in free_endpoints)
        bound = minimum - sigma / dimension
        assert bound > 0
        table_entries += len(shell) * len(free_endpoints)
        certificates += 1

        sample_x = ([ (F(1),) ] if dimension == 1 else
                    [(F(1), F(0)), (F(1), F(1)),
                     (F(1), F(7, 20)), (F(2, 5), F(1))])
        sample_y = free_endpoints + [tuple((lo + hi) / 2 for lo, hi in bounds)]
        for x, y in product(sample_x, sample_y):
            distributions = ([rounding(value, values) for value in x]
                             + [rounding(value, [lo, hi])
                                for value, (lo, hi) in zip(y, bounds)])
            expected_f = F(0)
            expected_norm = F(0)
            variance = [F(0)] * dimension
            mass = F(0)
            for atom in product(*distributions):
                probability = F(1)
                for _, weight in atom:
                    probability *= weight
                u = tuple(value for value, _ in atom[:dimension])
                v = tuple(value for value, _ in atom[dimension:])
                assert max(u) == 1
                mass += probability
                expected_f += probability * objective(a, c, b, u, v)
                expected_norm += probability * sum(t * t for t in u)
                for i in range(dimension):
                    variance[i] += probability * (u[i] - x[i]) ** 2
            original = objective(a, c, b, x, y)
            norm = sum(t * t for t in x)
            assert mass == 1
            assert expected_f - original == sum(a[i][i] * variance[i]
                                                for i in range(dimension))
            assert expected_norm == norm + sum(variance)
            assert 4 * sum(variance) <= delta**2 * expected_norm + delta**2 / dimension
            assert (expected_f - sigma * expected_norm
                    - original + sigma * norm
                    <= sigma * expected_norm + sigma / dimension)
            assert original >= sigma * norm + bound
            rounding_cases += 1
            for scale in (F(0), F(1, 7), F(2, 3), F(1)):
                scaled_x = tuple(scale * value for value in x)
                scaled_f = objective(a, c, b, scaled_x, y)
                assert scaled_f >= scale**2 * original
                assert scaled_f >= sigma * scale**2 * norm + bound * scale**2
                radial_cases += 1

# Exact unary reductions for two-label free integer coordinates,
# including large labels and coefficients. Rectangle cross terms stay
# unchanged because the reduction alters only y_i^2.
binary_reductions = 0
for lower in (-7, 0, 2**80):
    upper = lower + 1
    for coefficient in (F(-13, 7), F(1, 3), F(10**20)):
        for value in (lower, upper):
            assert coefficient * value**2 == coefficient * (
                (lower + upper) * value - lower * upper)
            binary_reductions += 1

print(f"PASS: {certificates} finite certificates from {table_entries} endpoint-grid entries")
print(f"PASS: {rounding_cases} exact rounding identities and {radial_cases} scaled growth checks")
print(f"PASS: {binary_reductions} two-label reductions, including 81-bit endpoints")


# Native mixed-fiber extension: z is active integer, u active continuous;
# w is free continuous and b is free integer with over a million labels.
# Free labels must never enter the active-radius flag or its correction.
def fiber_objective(active, free):
    z, u = active
    w, b = free
    return z*z - z/2 + u*u - z*u + w*z/4 + b*u/F(2**21)


fiber_cases = 0
fiber_table_entries = 0
free_vertices = list(product((F(0), F(1)), (F(0), F(2**20))))
free_samples = list(product((F(0), F(1, 2), F(1)),
                            (F(0), F(37), F(2**20))))
delta, sigma = F(1, 2), F(1, 16)
for radius in (F(1, 2), F(1), F(2), F(4)):
    active_grids = [physical_grid(F(4), radius, delta, 2, F(1)),
                   physical_grid(F(1), radius, delta, 2)]
    shell_points = [u for u in product(*active_grids) if max(u) >= radius]
    assert (F(0), F(0)) not in shell_points
    minimum = min(fiber_objective(u, y) - 2*sigma*sum(t*t for t in u)
                  for u in shell_points for y in free_vertices)
    assert minimum >= sigma * radius**2 / 2
    fiber_table_entries += len(shell_points) * len(free_vertices)
    for z, u in product(range(5), (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))):
        active = (F(z), u)
        if not radius <= max(active) <= 2*radius:
            continue
        for free in free_samples:
            dists = [physical_rounding(nodes, target)
                     for nodes, target in zip(active_grids, active)]
            dists += [physical_rounding([F(0), F(1)], free[0]),
                      physical_rounding([F(0), F(2**20)], free[1])]
            expected = F(0)
            expected_norm = F(0)
            variance = [F(0), F(0)]
            for atom in product(*dists):
                weight = F(1)
                for _, probability in atom:
                    weight *= probability
                rounded_active = tuple(value for value, _ in atom[:2])
                rounded_free = tuple(value for value, _ in atom[2:])
                assert max(rounded_active) >= radius
                expected += weight * fiber_objective(rounded_active, rounded_free)
                expected_norm += weight * sum(t*t for t in rounded_active)
                for i in range(2):
                    variance[i] += weight * (rounded_active[i] - active[i])**2
            value = fiber_objective(active, free)
            assert expected - value == sum(variance)
            residual = value - sigma * sum(t*t for t in active)
            assert residual >= minimum - sigma * radius**2 / 2
            assert value >= sigma * sum(t*t for t in active)
            fiber_cases += 1

# Below the bottom radius the active integer is fixed, and the uniform
# continuous KKT slope is b/2^21 >= 0 for every free assignment.
for free in free_samples:
    for displacement in (F(1, 32), F(1, 8), F(3, 8)):
        scale = 2 * displacement
        assert fiber_objective((F(0), displacement), free) >= scale**2 * (
            fiber_objective((F(0), F(1, 2)), free))
        fiber_cases += 1

print(f"PASS: {fiber_cases} native mixed-fiber and inner-region cases "
      f"from {fiber_table_entries} endpoint-shell entries")
