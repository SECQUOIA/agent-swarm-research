"""Independent physical-shell composition fixtures using exact fractions."""

from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "new-direction"))
from check_mixed_shell_certificate import grid, distribution, ceil_q


def value(point, matrix, linear):
    return sum(c*x for c, x in zip(linear, point)) + sum(
        matrix[i][j]*point[i]*point[j] for i in range(len(point)) for j in range(len(point)))


def minimum_dp(states, matrix, linear, sigma, radius, bags, parents):
    n = len(states)
    owners = {i: next(t for t, bag in enumerate(bags) if i in bag) for i in range(n)}
    separators = [()] + [tuple(i for i in bags[t] if i in bags[parents[t]]) for t in range(1, len(bags))]
    children = [[j for j in range(t+1, len(bags)) if parents[j] == t] for t in range(len(bags))]
    terms = [[] for _ in bags]
    for i in range(n):
        terms[owners[i]].append((i, i))
        for j in range(i+1, n):
            if matrix[i][j]:
                t = next(t for t, bag in enumerate(bags) if i in bag and j in bag)
                terms[t].append((i, j))
    messages = {}
    for t in reversed(range(len(bags))):
        message = {}
        for assignment in product(*(states[i] for i in bags[t])):
            point = dict(zip(bags[t], assignment))
            local = sum(linear[i]*point[i] + (matrix[i][i]-2*sigma)*point[i]**2
                        if i == j else 2*matrix[i][j]*point[i]*point[j] for i, j in terms[t])
            flag = int(any(abs(point[i]) >= radius for i in bags[t] if owners[i] == t))
            costs = {flag: local}
            for child in children[t]:
                separator = tuple(point[i] for i in separators[child])
                combined = {}
                for flag, cost in costs.items():
                    for other in (0, 1):
                        child_cost = messages[child].get((separator, other))
                        if child_cost is not None:
                            key, candidate = flag | other, cost + child_cost
                            combined[key] = min(combined.get(key, candidate), candidate)
                costs = combined
            separator = tuple(point[i] for i in separators[t])
            for flag, cost in costs.items():
                key = separator, flag
                message[key] = min(message.get(key, cost), cost)
        messages[t] = message
    result = messages[0].get(((), 1))
    points = [x for x in product(*states) if max(map(abs, x)) >= radius]
    direct = min((value(x, matrix, linear)-2*sigma*sum(v*v for v in x) for x in points), default=None)
    assert result == direct
    return result


def signed_states(widths, meshes, radius, n):
    states = []
    for (negative, positive), mesh in zip(widths, meshes):
        lower = grid(negative, radius, Q(1, 2), n, mesh) if negative else [Q(0)]
        upper = grid(positive, radius, Q(1, 2), n, mesh) if positive else [Q(0)]
        states.append(sorted(set([-x for x in lower] + upper)))
    return states


def main():
    shell_checks = 0
    # Aspect ratio 2^40 affects the number of shells, not trial resolution.
    sigma = Q(1, 16)
    largest_grid = 0
    for j in range(41):
        radius = Q(2) ** (j-40)
        states = signed_states([(Q(1, 2**40), Q(1))], [None], radius, 1)
        minimum = minimum_dp(states, [[Q(1)]], [Q(0)], sigma, radius, [(0,)], [-1])
        assert minimum >= sigma * radius**2
        largest_grid = max(largest_grid, len(states[0]))
        shell_checks += 1
    assert largest_grid < 30

    # Huge linear and off-diagonal coefficients must not inflate L=2.
    for height in (Q(1), Q(2**200)):
        matrix = [[Q(1), -height], [-height, Q(1)]]
        for radius in (Q(1, 2), Q(1)):
            states = signed_states([(Q(0), Q(1))]*2, [Q(1), None], radius, 2)
            minimum = minimum_dp(states, matrix, [height, height], sigma, radius, [(0, 1)], [-1])
            assert minimum >= sigma * radius**2 / 2
            shell_checks += 1

    # Integer candidate is interior in its integer interval; continuous
    # coordinates have both signs. The owner-flag star DP matches enumeration.
    matrix = [[Q(2), Q(-1, 2), Q(-1, 2)], [Q(-1, 2), Q(2), Q(0)],
              [Q(-1, 2), Q(0), Q(2)]]
    for radius in (Q(1, 2), Q(1)):
        states = signed_states([(Q(1), Q(1))]*3, [Q(1), None, None], radius, 3)
        minimum = minimum_dp(states, matrix, [Q(0)]*3, Q(1, 8), radius,
                             [(0, 1), (0, 2)], [-1, 0])
        assert minimum >= Q(1, 8) * radius**2 / 3
        shell_checks += 1

    # The exact ceil(S/h) threshold is essential for preserving the shell.
    threshold_checks = 0
    for mesh in (Q(1), Q(3, 7)):
        radius = Q(17)
        nodes = grid(2*radius, radius, Q(1, 2), 2, mesh)
        threshold = mesh * ceil_q(radius / mesh)
        assert all(x >= radius for x, mass in distribution(nodes, threshold) if mass)
        omitted = [x for x in nodes if x != threshold]
        assert any(x < radius for x, mass in distribution(omitted, threshold) if mass)
        threshold_checks += 1

    # Endpoint-only proof for L=0, checked independently of shell routines.
    endpoint_checks = 0
    for matrix, linear, widths in (
        ([[Q(0), Q(-1, 2)], [Q(-1, 2), Q(0)]], [Q(1), Q(1)], [Q(1), Q(1)]),
        ([[Q(-1), Q(0)], [Q(0), Q(-1)]], [Q(2), Q(3)], [Q(1), Q(1)]),
    ):
        endpoints = list(product(*[(Q(0), w) for w in widths]))
        gap = min(value(x, matrix, linear) for x in endpoints if any(x))
        margin = gap / sum(w*w for w in widths)
        assert margin > 0
        for target in product(*(tuple(Q(j, 8)*w for j in range(9)) for w in widths)):
            assert value(target, matrix, linear) >= margin * sum(x*x for x in target)
            endpoint_checks += 1
    print(f"{shell_checks} full shell DPs matched direct enumeration; largest aspect fixture grid {largest_grid}")
    print(f"{threshold_checks} necessary lattice-threshold insertion checks; {endpoint_checks} zero-curvature growth checks")


if __name__ == '__main__':
    main()
