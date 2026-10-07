"""Exact, scoped diagnostics for the all-scale count geometry.

These checks do not implement the general convex recourse algorithm or
quantifier elimination.  The fixtures have explicitly known conjugates.
"""

from fractions import Fraction as Q
from itertools import combinations, product


def clamp(x):
    return max(Q(0), min(Q(1), x))


def objective(x, curvature):
    return sum(
        a * t * t / 2 if a else t * t * (1 - t) ** 2
        for t, a in zip(x, curvature)
    )


def conjugate(c, curvature):
    total = Q(0)
    for t, a in zip(c, curvature):
        if not a:
            total += max(Q(0), t)
        elif t <= 0:
            continue
        elif t >= a:
            total += t - a / 2
        else:
            total += t * t / (2 * a)
    return total


def inverse_subgradient(y, curvature, upper):
    answer = []
    for t, a in zip(y, curvature):
        if not a:
            answer.append(upper * (t - clamp(t)))
        elif t <= 0:
            answer.append(upper * t)
        elif t >= 1 + a / upper:
            answer.append(upper * (t - 1))
        else:
            answer.append(a * upper * t / (a + upper))
    return tuple(answer)


def regularized(c, curvature, upper):
    return conjugate(c, curvature) + sum(t * t for t in c) / (2 * upper)


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    return sum(
        (-1) ** j
        * matrix[0][j]
        * determinant([row[:j] + row[j + 1 :] for row in matrix[1:]])
        for j in range(len(matrix))
    )


def max_simplex(points):
    dimension = len(points[0])
    best = Q(0)
    for vertices in combinations(points, dimension + 1):
        edges = [
            [vertices[j + 1][i] - vertices[0][i] for j in range(dimension)]
            for i in range(dimension)
        ]
        best = max(best, abs(determinant(edges)))
    return best


def run():
    upper = Q(2)
    witnesses = padding = node_bounds = 0
    # Zero entries mean a double-well quartic, whose convex envelope is zero.
    fixtures = [(Q(2),), (Q(0),), (Q(2), Q(0)), (Q(0), Q(0), Q(0))]
    for curvature in fixtures:
        k = len(curvature)
        coefficients = list(product((Q(-1, 2), Q(0), Q(1, 2)), repeat=k))
        for denominator in (2, 4):
            h = Q(1, denominator)
            epsilon = k * upper * h * h / 2
            grid = list(product((Q(j, denominator) for j in range(denominator + 1)), repeat=k))
            for c in coefficients:
                nodes = [
                    x for x in grid
                    if objective(x, curvature) - dot(c, x) + conjugate(c, curvature) <= epsilon
                ]
                assert nodes
                witnesses += len(nodes)
                for x in nodes:
                    for signs in product((-1, 1), repeat=k):
                        y = tuple(t + s / upper + sign * h / 4 for t, s, sign in zip(x, c, signs))
                        d = inverse_subgradient(y, curvature, upper)
                        h_star = dot(y, d) - regularized(d, curvature, upper)
                        residual = regularized(c, curvature, upper) + h_star - dot(c, y)
                        assert 0 <= residual <= k * upper * h * h
                        distance_squared = sum((a - b) ** 2 for a, b in zip(d, c))
                        assert distance_squared <= 2 * upper * residual
                        assert distance_squared < (4 * k * upper * h) ** 2
                        padding += 1
                # One- and two-dimensional actual simplex maxima, including
                # boundary-optimum and tie atoms.  Padding vertices suffice.
                if k <= 2 and denominator == 2:
                    points = sorted(set(
                        tuple(t + sign * h / 4 for t, sign in zip(x, signs))
                        for x in nodes
                        for signs in product((-1, 1), repeat=k)
                    ))
                    determinant_max = max_simplex(points)
                    assert len(nodes) * h**k <= 4**k * determinant_max
                    node_bounds += 1

    # A rational, nonsingular QR witness checks both determinant signs.
    orthogonal = [[Q(3, 5), Q(-4, 5)], [Q(4, 5), Q(3, 5)]]
    triangular = [[Q(2), Q(1, 3)], [Q(0), Q(7, 4)]]
    qr_checks = 0
    for sign in (-1, 1):
        qmat = [[sign * orthogonal[i][0], orthogonal[i][1]] for i in range(2)]
        for i in range(2):
            for j in range(2):
                assert sum(qmat[t][i] * qmat[t][j] for t in range(2)) == (i == j)
        matrix = [[sum(qmat[i][t] * triangular[t][j] for t in range(2)) for j in range(2)] for i in range(2)]
        assert abs(determinant(matrix)) == triangular[0][0] * triangular[1][1]
        qr_checks += 1

    # At zero noise for a double well, the inverse-gradient pushforward has
    # a whole unit interval as the preimage of a point: atom-safe coverings
    # really are needed, rather than only absolutely continuous measures.
    assert all(inverse_subgradient((Q(j, 8),), (Q(0),), upper) == (Q(0),) for j in range(9))
    print(f"PASS: {len(fixtures)} fixtures, {witnesses} near-optimal nodes, "
          f"{padding} padding/pushforward checks, {node_bounds} simplex node bounds, "
          f"{qr_checks} signed QR checks, 1 singular-measure fixture")


if __name__ == "__main__":
    run()
