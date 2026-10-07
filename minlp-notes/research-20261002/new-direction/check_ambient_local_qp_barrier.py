"""Targeted exact-rational checks for the ambient local-count construction."""

from fractions import Fraction as Q
from random import Random


CROSS = Q(3, 4)
WIDTH = Q(4)


def clip(value, lower, upper):
    return max(lower, min(upper, value))


def inner(alpha, epsilon, residual_slope, noise_z, auxiliary):
    """Minimize the strictly convex reduced recourse QP on its rectangle."""
    linear_y = residual_slope - alpha * auxiliary
    denominator = alpha * (1 - CROSS**2)
    free_y = (-linear_y + CROSS * noise_z) / denominator
    free_z = (-noise_z + CROSS * linear_y) / denominator
    candidates = []
    if abs(free_y) <= WIDTH and abs(free_z) <= epsilon:
        candidates.append((free_y, free_z))
    for y in (-WIDTH, WIDTH):
        z = clip(-CROSS * y - noise_z / alpha, -epsilon, epsilon)
        candidates.append((y, z))
    for z in (-epsilon, epsilon):
        y = clip(auxiliary - residual_slope / alpha - CROSS * z, -WIDTH, WIDTH)
        candidates.append((y, z))

    def value(pair):
        y, z = pair
        return (
            alpha * (CROSS * y * z + z * z / 2)
            + residual_slope * y
            + noise_z * z
            + alpha * (auxiliary - y) ** 2 / 2
        )

    best = min(candidates, key=value)
    return value(best), best


def original_minimum(alpha, epsilon, slope, noise_z):
    # For every fixed z, the original reduced objective is affine in y.
    values = []
    for y in (-WIDTH, WIDTH):
        z = clip(-CROSS * y - noise_z / alpha, -epsilon, epsilon)
        values.append(alpha * (CROSS * y * z + z * z / 2) + slope * y + noise_z * z)
    return min(values)


def level_step(domain_width, lower):
    step = domain_width
    while step > 2 * lower:
        step /= 2
    assert lower <= step <= 2 * lower
    return step


def near_step(domain_width, alpha, m):
    step = domain_width
    while alpha * m * step * step > 256:
        step /= 2
    assert 64 <= alpha * m * step * step <= 256
    return step


def grid_nodes(step):
    count = int(1 / step)
    # The full symmetric dyadic auxiliary grid contains zero.
    return [index * step for index in sorted({-count, -1, 0, 1, count}) if abs(index * step) <= 1]


rng = Random(20261002)
draw_checks = local_checks = global_checks = derivative_checks = 0
z_states = set()
for m in (64, 128, 256):
    n = m * m
    denominator = 2**24 - 1
    plus_size = n // 2 - 2
    minus_size = n // 2
    # Ambient endpoint-grid draws are kept as integer numerators until reduction.
    for trial in range(12):
        plus = [2 * rng.randrange(denominator + 1) - denominator for _ in range(plus_size)]
        minus = [2 * rng.randrange(denominator + 1) - denominator for _ in range(minus_size)]
        extra = [2 * rng.randrange(denominator + 1) - denominator for _ in range(2)]
        if trial % 3 == 0:
            extra[1] = extra[0]  # Exercise an interior z optimum at a suitable a.
        d = Q(sum(plus) - sum(minus) + sum(extra), m * denominator)
        gamma_plus = Q(min(plus), denominator)
        gamma_minus = Q(min(minus), denominator)
        slope = Q(m, 2) * (gamma_plus - gamma_minus)
        noise_z = Q(extra[0] - extra[1], 2 * denominator)
        residual_plus = gamma_plus - d / m
        residual_minus = gamma_minus + d / m
        residual_slope = Q(m, 2) * (residual_plus - residual_minus)
        assert residual_slope == slope - d
        if not (gamma_plus <= -1 + Q(4, n) and gamma_minus <= -1 + Q(4, n) and abs(d) <= 2):
            continue
        draw_checks += 1
        epsilon = Q(1, m**3)
        for alpha in (Q(1), Q(m)):
            domain_width = 2 * WIDTH + Q(2 * m) / alpha
            step = level_step(domain_width, Q(16, 1) / (alpha * m))
            for auxiliary in grid_nodes(step) + [residual_slope / alpha]:
                value, (y, z) = inner(alpha, epsilon, residual_slope, noise_z, auxiliary)
                assert abs(y) < WIDTH
                derivative = alpha * (auxiliary - y) + d
                assert derivative == slope + alpha * CROSS * z
                derivative_checks += 1
                z_states.add(-1 if z == -epsilon else 1 if z == epsilon else 0)
                if abs(auxiliary) > 1:
                    continue
                current = value + d * auxiliary
                for direction in (-1, 1):
                    neighbor = auxiliary + direction * step
                    neighbor_value, _ = inner(alpha, epsilon, residual_slope, noise_z, neighbor)
                    assert current <= neighbor_value + d * neighbor + alpha * step * step / 4
                    local_checks += 1

            coarse = near_step(domain_width, alpha, m)
            optimum = original_minimum(alpha, epsilon, slope, noise_z) - d * d / (2 * alpha)
            for auxiliary in grid_nodes(coarse):
                value, _ = inner(alpha, epsilon, residual_slope, noise_z, auxiliary)
                gap = value + d * auxiliary - optimum
                assert 0 <= gap < Q(15, m)
                assert gap <= alpha * coarse * coarse / 4
                global_checks += 1

assert draw_checks > 0
assert z_states == {-1, 0, 1}
assert 2 * (1 - CROSS**2) > 0
print(
    f"PASS: {draw_checks} ambient-noise fixtures satisfying E; "
    f"{derivative_checks} exact derivative identities; "
    f"{local_checks} local comparisons; {global_checks} global-gap checks; "
    "all three z active states."
)
