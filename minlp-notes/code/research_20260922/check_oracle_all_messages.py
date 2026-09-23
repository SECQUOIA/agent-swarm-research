"""Exact adversarial checks for the approximate enumeration/net construction.

This is a finite mathematical checker, not an implementation of the proposed
treewidth algorithm or a verification of its probabilistic runtime.
"""

from fractions import Fraction as F
from itertools import product
from random import Random


def enumerate_near(costs, epsilon, delta):
    dimension = len(next(iter(costs)))
    calls = 0
    extracted = []

    def query(cell):
        nonlocal calls
        calls += 1
        members = [z for z in costs if all(z[i] == v for i, v in cell.items())]
        if not members:
            return None
        best = min(costs[z] for z in members)
        # Deliberately return the worst allowed approximate candidate.
        z = max((z for z in members if costs[z] <= best + epsilon),
                key=lambda z: (costs[z], z))
        return (costs[z] - epsilon, z, cell)

    cells = [query({})]
    initial = costs[cells[0][1]]

    def check_partition():
        members = []
        for _, _, cell in cells:
            members.extend(z for z in costs
                           if all(z[i] == v for i, v in cell.items()))
        assert len(members) == len(set(members))
        assert set(members) == set(costs) - set(extracted)

    while cells:
        check_partition()
        index = min(range(len(cells)), key=lambda i: cells[i][0])
        bound, z, cell = cells[index]
        if bound > initial + delta:
            break
        cells.pop(index)
        assert z not in extracted
        extracted.append(z)
        prefix = dict(cell)
        for i in range(dimension):
            if i in cell:
                continue
            child = dict(prefix)
            child[i] = 1 - z[i]
            result = query(child)
            if result is not None:
                cells.append(result)
            prefix[i] = z[i]
    check_partition()
    optimum = min(costs.values())
    assert {z for z in costs if costs[z] <= optimum + delta} <= set(extracted)
    assert all(costs[z] <= optimum + delta + 2 * epsilon for z in extracted)
    assert calls <= 1 + dimension * len(extracted)
    return set(extracted), calls


def active_affine_supports(branches):
    """Test activity on [-1,1] by exact intersections of linear inequalities."""
    result = set()
    for z, (a, b) in branches.items():
        lo, hi = F(-1), F(1)
        feasible = True
        for c, d in branches.values():
            slope, rhs = a - c, d - b
            if slope > 0:
                hi = min(hi, rhs / slope)
            elif slope < 0:
                lo = max(lo, rhs / slope)
            elif rhs < 0:
                feasible = False
        if feasible and lo <= hi:
            result.add(z)
    return result


def main():
    random = Random(20260922)
    net_cases = net_points = active = 0
    for dimension in range(1, 5):
        cube = list(product((0, 1), repeat=dimension))
        for repeat in range(20):
            branches = {z: (F(random.randint(-4, 4)),
                            F(random.randint(-6, 6), 2)) for z in cube}
            # A branch that is optimal only at one tie is included explicitly.
            if dimension == 2 and repeat == 0:
                branches = {(0, 0): (F(1), F(0)),
                            (0, 1): (F(-1), F(0)),
                            (1, 0): (F(0), F(0)),
                            (1, 1): (F(0), F(2))}
            epsilon = F(1, 2)
            lipschitz = max(abs(a) for a, _ in branches.values())
            subdivisions = max(1, int(2 * lipschitz / epsilon))
            dictionary = set()
            for j in range(subdivisions):
                t = -1 + F(2 * j + 1, subdivisions)
                costs = {z: a * t + b for z, (a, b) in branches.items()}
                found, _ = enumerate_near(costs, epsilon, epsilon)
                dictionary.update(found)
            actual_active = active_affine_supports(branches)
            assert actual_active <= dictionary
            active += len(actual_active)
            net_points += subdivisions
            net_cases += 1
    print(f"Passed {net_cases} exact affine-net instances: {net_points} "
          f"net points, {active} active supports, including a tie-only support.")


if __name__ == "__main__":
    main()
