"""Exact finite-law budgets and an unavoidable exceptional atom.

This does not rerun the author's nonlinear sparse-DP fixture or implement
real-algebraic fallback. All arithmetic here is rational/integer.
"""

from fractions import Fraction as Q


def power_two_ceiling(x):
    result = 1
    while result < x:
        result *= 2
    return result


def budget(n, widths, sigma, curvature, gradient_bound, third_bound,
           fallback, section_count, face_count):
    total_width = sum(widths)
    s = power_two_ceiling(max(Q(1), *widths))
    rho = Q(1, 4 * fallback)
    growth = rho * sigma / (2 * total_width)
    margin = rho * sigma / (2 * face_count)
    radius_factor = 2 + n * curvature / growth
    cutoff = min(Q(1) / (4 * radius_factor),
                 margin / (4 * gradient_bound * radius_factor),
                 growth / (4 * third_bound * radius_factor))
    depth, mesh = 0, Q(s)
    while mesh > cutoff:
        depth += 1
        mesh /= 2
    grid_size = power_two_ceiling(max(Q(2), Q(2**depth),
                                     4 * n * section_count / rho,
                                     2 * face_count / rho))
    growth_failure = total_width * growth / sigma + Q(2 * n * section_count, grid_size)
    gradient_failure = face_count * (margin / sigma + Q(1, grid_size))
    assert growth_failure <= rho and gradient_failure <= rho
    assert fallback * (growth_failure + gradient_failure) <= Q(1, 2)
    assert radius_factor * mesh <= Q(1, 4)
    assert 2 * gradient_bound * radius_factor * mesh <= margin / 2
    assert growth - 2 * third_bound * radius_factor * mesh >= growth / 2
    assert grid_size >= 2**depth
    # Every level's extra atomic term in the bag count is at most one.
    for level in (0, depth // 2, depth):
        level_mesh = Q(s, 2**level)
        assert all(width / (grid_size * level_mesh) <= 1 for width in widths)
    return depth, grid_size.bit_length() - 1


def check_flat_atom(grid_size):
    # F_gamma(x)=(gamma-1)x on [0,1], gamma uniform on [-1,1].
    # gamma=1 is an actual endpoint atom with an entire optimal interval.
    noise = [-Q(1) + Q(2 * k, grid_size - 1) for k in range(grid_size)]
    growths = [1 - gamma for gamma in noise]
    assert sum(g == 0 for g in growths) == 1
    for threshold in (Q(1, 10000), Q(1, 8), Q(1, 2), Q(3)):
        probability = Q(sum(g < threshold for g in growths), grid_size)
        assert probability <= threshold + Q(2, grid_size)
        active_event = Q(sum(0 < g <= threshold for g in growths), grid_size)
        assert active_event <= threshold + Q(1, grid_size)
    # Off the exceptional atom, the optimizer is the upper bound and the
    # derivative sign proves it. At the atom, neither a strict sign nor a
    # positive Hessian certificate exists; exact fallback must handle ties.
    assert all(gamma < 1 for gamma in noise[:-1])
    assert noise[-1] == 1


def check_weak_optimization_cleanup(width):
    # f=x^2 on [1,1+width]. A valid weak optimizer may lie outside both
    # the box and the epigraph; rational projection must repair it.
    lower, upper = Q(1), 1 + width
    value_bound = 1 + upper**2
    inner_radius = min(width / 2, Q(1, 2))
    gradient_bound = 2 * upper
    cost = 1 + (2 * value_bound + 1) / inner_radius
    total = cost + gradient_bound + 1
    target = Q(1, 2**30)
    tolerance = min(inner_radius / 2, target / total)
    query_x, query_t = lower - tolerance / 2, Q(1) - tolerance / 2
    # (1,1) is a feasible epigraph point within the promised tolerance.
    assert (query_x - 1)**2 + (query_t - 1)**2 <= tolerance**2
    # t below the true optimum certainly satisfies the eroded-body upper
    # comparison. It does not imply that the returned point is feasible.
    assert query_t < 1 and query_x < lower
    feasible_x = min(upper, max(lower, query_x))
    upper_value = feasible_x**2
    lower_value = query_t - cost * tolerance
    assert lower_value <= 1 <= upper_value
    assert upper_value - lower_value <= total * tolerance <= target


if __name__ == "__main__":
    fixtures = [
        (1, [Q(1)], Q(1), Q(1), Q(1), Q(1), 8, 16, 3),
        (3, [Q(1, 8), Q(7), Q(2)], Q(1, 16), Q(8), Q(64), Q(128), 2**40, 2**90, 2**20),
        (2, [Q(2**200), Q(1, 2**150)], Q(1, 2**80), Q(2**100), Q(2**120), Q(2**140), 2**500, 2**900, 2**300),
        (4, [Q(1)] * 4, Q(2**60), Q(1, 2**60), Q(2**1000), Q(2**1200), 2**1000, 2**3000, 2**600),
    ]
    results = [budget(*fixture) for fixture in fixtures]
    for grid_size in (8, 16, 64):
        check_flat_atom(grid_size)
    for width in (Q(1), Q(1, 2**60), Q(1, 2**200)):
        check_weak_optimization_cleanup(width)
    print(f"PASS: 4 exact base-only budgets (depth,noise bits)={results}; "
          "3 finite laws with a genuine tied endpoint atom; "
          "growth/gradient tails, closure inequalities, and expected fallback allocations; "
          "3 near-feasible epigraph cleanup cases including 200-bit thin boxes.")
