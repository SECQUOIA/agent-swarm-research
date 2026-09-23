"""Independent exact arrangement-vertex checks for the path reduction.

This enumerates the original continuous leader objective's arrangement
vertices, rather than checking only the subset-induced leader choices.
Small finite checks supplement, and do not replace, the general proof.
"""

from fractions import Fraction as F
from itertools import combinations, product


def solve(rows, dimension):
    matrix = [list(row) for row in rows]
    for col in range(dimension):
        pivot = next((i for i in range(col, dimension) if matrix[i][col]), None)
        if pivot is None:
            return None
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        scale = matrix[col][col]
        matrix[col] = [x / scale for x in matrix[col]]
        for i in range(dimension):
            if i != col and matrix[i][col]:
                factor = matrix[i][col]
                matrix[i] = [a - factor * b for a, b in zip(matrix[i], matrix[col])]
    return tuple(row[-1] for row in matrix)


def clip(value):
    return min(F(1), max(F(0), value))


def objective(point, weights, target):
    increments = [point[i + 1] - point[i] for i in range(len(weights))]
    direct = point[0] + abs(point[-1] - target) + sum(
        min(abs(t), abs(t - r)) for t, r in zip(increments, weights)
    )
    follower = 2 * point[0] - 2 * point[-1] + target + 2 * clip(point[-1] - target)
    follower += 2 * sum(
        clip(t) - clip(t - r / 2) + clip(t - r)
        for t, r in zip(increments, weights)
    )
    assert direct == follower
    return direct


instances = [([2, 3], 1), ([2, 3], 2), ([2, 4], 3),
             ([2, 3, 7], 6), ([2, 3, 7], 5), ([1, 4, 6], 8)]
vertex_count = 0
for integers, integer_target in instances:
    total = sum(integers)
    weights = [F(a, total) for a in integers]
    target = F(integer_target, total)
    dimension = len(integers) + 1
    hyperplanes = []
    for j in range(dimension):
        normal = [F(i == j) for i in range(dimension)]
        hyperplanes.extend([tuple(normal + [F(0)]), tuple(normal + [F(1)])])
    for j, weight in enumerate(weights):
        normal = [F(0)] * dimension
        normal[j], normal[j + 1] = F(-1), F(1)
        hyperplanes.extend(tuple(normal + [cut]) for cut in (F(0), weight / 2, weight))
    hyperplanes.append(tuple([F(0)] * (dimension - 1) + [F(1), target]))

    vertices = set()
    for rows in combinations(hyperplanes, dimension):
        point = solve(rows, dimension)
        if point is not None and all(0 <= x <= 1 for x in point):
            vertices.add(point)
    continuous_minimum = min(objective(point, weights, target) for point in vertices)
    subset_minimum = min(
        abs(sum(a * bit for a, bit in zip(integers, bits)) - integer_target)
        for bits in product((0, 1), repeat=len(integers))
    ) / F(total)
    assert continuous_minimum == subset_minimum
    vertex_count += len(vertices)

# Check every branch of the signed distance identity, including endpoints.
identity_count = 0
for r in (F(1, 7), F(1, 2), F(1)):
    for t in [F(k, 24) for k in range(-24, 25)] + [r / 2, r]:
        assert min(abs(t), abs(t - r)) == -t + 2 * clip(t) - 2 * clip(t - r / 2) + 2 * clip(t - r)
        identity_count += 1

print(f"PASS: {len(instances)} exact continuous arrangement minima, "
      f"{vertex_count} feasible vertices, {identity_count} distance identities.")
