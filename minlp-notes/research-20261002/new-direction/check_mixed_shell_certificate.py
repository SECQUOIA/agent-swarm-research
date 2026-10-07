"""Targeted exact checks for mixed-shell-certificate.md; no external packages."""

from bisect import bisect_left
from fractions import Fraction as Q
from itertools import product


def ceil_q(value):
    return -(-value.numerator // value.denominator)


def grid(upper, radius, delta, dimension, mesh=None):
    """One unsigned side, already translated to the proposed point."""
    upper = min(upper, 2 * radius)
    if mesh is not None:
        upper = (upper // mesh) * mesh
    if not upper:
        return [Q(0)]
    initial = delta * radius / (2 * dimension)
    if mesh is not None:
        initial = mesh * ceil_q(initial / mesh)
    nodes = {Q(0)}
    node = min(upper, initial)
    while True:
        nodes.add(node)
        if node == upper:
            break
        if mesh is None:
            node = min(upper, node * (1 + delta))
        else:
            node = min(upper, node + mesh * max(1, (delta * node) // mesh))
    threshold = radius if mesh is None else mesh * ceil_q(radius / mesh)
    if threshold <= upper:
        nodes.add(threshold)
    return sorted(nodes)


def distribution(nodes, target):
    index = bisect_left(nodes, target)
    if nodes[index] == target:
        return [(target, Q(1))]
    low, high = nodes[index - 1], nodes[index]
    return [(low, (high - target) / (high - low)),
            (high, (target - low) / (high - low))]


def scalar_checks():
    count = 0
    for delta, dimension, radius, mesh in product(
        [Q(1, 2), Q(1, 4)], [1, 3],
        [Q(1, 8), Q(1, 2), Q(3, 2), Q(4), Q(10)],
        [None, Q(1), Q(1, 3), Q(3, 2)],
    ):
        upper = Q(7) if mesh is None else 7 * mesh
        nodes = grid(upper, radius, delta, dimension, mesh)
        if mesh is None:
            targets = set(nodes)
            for low, high in zip(nodes, nodes[1:]):
                targets.update(low + Q(k, 4) * (high - low) for k in range(1, 4))
        else:
            targets = [k * mesh for k in range(int(nodes[-1] / mesh) + 1)]
        for target in targets:
            rounded = distribution(nodes, target)
            assert sum(value * prob for value, prob in rounded) == target
            second = sum(value * value * prob for value, prob in rounded)
            variance = second - target * target
            assert 4 * variance <= delta * delta * (
                second + radius * radius / (dimension * dimension)
            )
            if target >= radius:
                assert all(value >= radius for value, prob in rounded if prob)
            if mesh is not None:
                assert all(value / mesh == int(value / mesh) for value, _ in rounded)
            # Reflection supplies exactly the same variance and absolute-value flag.
            assert sum(-value * prob for value, prob in rounded) == -target
            count += 1
    return count


def mixed_shell_checks():
    # A coupled mixed example: z is integer, u continuous, candidate (0,0).
    def objective(point):
        z, u = point
        return z * z - z / 2 + u * u - z * u

    delta, curvature, dimension = Q(1, 2), Q(2), 2
    sigma = curvature * delta * delta / 8
    count = 0
    shell_minima = {}
    for radius in [Q(1, 2), Q(1), Q(2), Q(4)]:
        grids = [grid(Q(4), radius, delta, dimension, Q(1)),
                 grid(Q(1), radius, delta, dimension)]
        candidates = [point for point in product(*grids) if max(point) >= radius]
        minimum = min(objective(point) - 2 * sigma * sum(v * v for v in point)
                      for point in candidates)
        assert minimum >= sigma * radius * radius / dimension
        shell_minima[radius] = minimum
        for z, u in product(range(5), [Q(k, 16) for k in range(17)]):
            target = (Q(z), u)
            if not radius <= max(target) <= 2 * radius:
                continue
            rounded = [distribution(nodes, value) for nodes, value in zip(grids, target)]
            expected_corrected = Q(0)
            expected_r = Q(0)
            for (a, pa), (b, pb) in product(*rounded):
                norm2 = a * a + b * b
                expected_corrected += pa * pb * (objective((a, b)) - 2 * sigma * norm2)
                expected_r += pa * pb * (objective((a, b)) - sigma * norm2)
                assert max(a, b) >= radius
            target_r = objective(target) - sigma * sum(v * v for v in target)
            variances = [sum(p * (value - x) ** 2 for value, p in dist)
                         for dist, x in zip(rounded, target)]
            assert expected_r - target_r == (1 - sigma) * sum(variances)
            assert target_r >= expected_corrected - sigma * radius * radius / dimension
            assert target_r >= minimum - sigma * radius * radius / dimension
            count += 1
    # In the bottom region z=0; this checks the radial extension against
    # nonzero continuous linear terms as well as homogeneous growth.
    for slope, curvature, displacement in product(
        [Q(0), Q(1), Q(5)], [Q(-1), Q(0), Q(2)],
        [Q(1, 32), Q(1, 8), Q(3, 8)],
    ):
        radius = Q(1, 2)
        scale = displacement / radius
        inner = slope * displacement + curvature * displacement * displacement
        outer = slope * radius + curvature * radius * radius
        assert inner >= scale * scale * outer
        count += 1
    return count, shell_minima


def obstructions():
    q = lambda z: z * z - z / 2
    assert q(Q(1, 4)) == Q(-1, 16)
    assert q(Q(1)) < Q(1, 4) * q(Q(2))
    binary = lambda z, w: z * z + 4 * w * w - Q(9, 2) * z * w
    assert min(binary(Q(z), Q(w)) / (z * z + w * w)
               for z, w in product(range(2), repeat=2) if z or w) == Q(1, 4)
    assert binary(Q(1), Q(9, 16)) == Q(-17, 64)
    integer = lambda z, w: z * z + w * w - Q(9, 8) * z * w - Q(3, 4) * z
    assert min(integer(Q(z), Q(w)) / (z * z + w * w)
               for z, w in product(range(51), repeat=2) if z or w) == Q(1, 16)
    assert Q(1, 4) + Q(9, 16) ** 2 - Q(9, 8) * Q(9, 16) == Q(-17, 256)


def endpoint_checks():
    # Both coordinate diagonals are negative; all other corners have gap 1.
    objective = lambda x, y: 2 * x + 2 * y - x * x - y * y - x * y
    endpoint_gap = min(objective(Q(x), Q(y))
                       for x, y in product(range(2), repeat=2) if x or y)
    assert endpoint_gap == 1
    count = 0
    for x, y in product([Q(k, 16) for k in range(17)], repeat=2):
        expected = x + y - x * y
        probability_different = 1 - (1 - x) * (1 - y)
        assert objective(x, y) - expected == x * (1 - x) + y * (1 - y)
        assert expected >= endpoint_gap * probability_different
        assert probability_different >= max(x, y) >= (x * x + y * y) / 2
        assert objective(x, y) >= endpoint_gap * (x * x + y * y) / 2
        # Off-diagonal/linear scale can grow while diagonal curvature stays fixed.
        inflated_example = 100 * (x + y - 2 * x * y) + x * x + y * y
        assert inflated_example >= x * x + y * y
        count += 1
    return count


if __name__ == "__main__":
    scalar_count = scalar_checks()
    mixed_count, minima = mixed_shell_checks()
    obstructions()
    endpoint_count = endpoint_checks()
    print(f"PASS: {scalar_count} exact scalar rounding cases")
    print(f"PASS: {mixed_count} mixed-shell and inner radial cases")
    print("PASS: three exact obstruction families")
    print(f"PASS: {endpoint_count} endpoint-certificate and scale-inflation cases")
    print("Verified mixed shell minima:", {str(s): str(m) for s, m in minima.items()})
