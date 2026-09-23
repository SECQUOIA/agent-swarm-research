"""Exact small checks of the shattering argument, not a probability proof."""

from fractions import Fraction
from itertools import product
from math import comb


def main():
    m = 3
    vertices = tuple(product((0, 1), repeat=m))
    grids = tuple(product((-4, 0, 4), repeat=m))
    coordinate_sets = tuple(
        tuple(i for i in range(m) if mask & (1 << i))
        for mask in range(1 << m)
    )
    cases = states = shattered_checks = moment_checks = 0
    for mask in range(1, 1 << len(vertices)):
        feasible = tuple(z for j, z in enumerate(vertices) if mask & (1 << j))
        for cost_type in range(3):
            costs = {
                z: (0 if cost_type == 0 else
                    (sum(z) - 1) ** 2 if cost_type == 1 else
                    3 * z[0] * z[1] - 2 * z[1] * z[2] + z[0])
                for z in feasible
            }
            for delta_units in (0, 1, 2):
                tail_counts = [0] * (m + 1)
                moment_sums = {p: 0 for p in (1, 2, 3)}
                for noise in grids:
                    objective = {
                        z: costs[z] + sum(x * b for x, b in zip(noise, z))
                        for z in feasible
                    }
                    optimum = min(objective.values())
                    near = tuple(z for z in feasible
                                 if objective[z] <= optimum + delta_units)
                    dimension = 0
                    for coords in coordinate_sets:
                        patterns = {tuple(z[i] for i in coords) for z in near}
                        if len(patterns) != 1 << len(coords):
                            continue
                        dimension = max(dimension, len(coords))
                        if not coords:
                            continue
                        class_cost = {}
                        for z in feasible:
                            pattern = tuple(z[i] for i in coords)
                            value = costs[z] + sum(
                                noise[j] * z[j] for j in range(m) if j not in coords
                            )
                            class_cost[pattern] = min(
                                class_cost.get(pattern, value), value
                            )
                        zero = (0,) * len(coords)
                        for position, coordinate in enumerate(coords):
                            unit = tuple(int(j == position) for j in range(len(coords)))
                            assert abs(class_cost[unit] + noise[coordinate]
                                       - class_cost[zero]) <= delta_units
                            shattered_checks += 1
                    assert len(near) <= sum(comb(m, j) for j in range(dimension + 1))
                    assert len(near) <= (m + 1) ** dimension
                    for k in range(1, dimension + 1):
                        tail_counts[k] += 1
                    for p in moment_sums:
                        moment_sums[p] += len(near) ** p
                    states += 1
                # Actual noise is {-1,0,1}; costs and tolerances above use quarters.
                alpha = Fraction(delta_units, 4) + Fraction(1, 3)
                for k in range(1, m + 1):
                    assert Fraction(tail_counts[k], len(grids)) <= comb(m, k) * alpha ** k
                for p, total in moment_sums.items():
                    bound = (1 + (m + 1) ** p * alpha) ** m
                    assert Fraction(total, len(grids)) <= bound
                    moment_checks += 1
                cases += 1
    print(f"PASS: {cases} exact distribution cases; {states} noise states; "
          f"{shattered_checks} conditional interval checks; "
          f"{moment_checks} moment inequalities.")


if __name__ == "__main__":
    main()
