"""Exact checks of the approximate-oracle partition certificate.

This checker exhausts small support sets to supply deliberately unfavorable
valid approximate answers. It checks correctness of the partition and the
failure-implies-many-near-optima implication. It is not a runtime experiment
or a verification of the probability theorem.
"""

from fractions import Fraction as F
from itertools import product
from random import Random


def matches(z, pattern):
    return all(value is None or z[i] == value for i, value in enumerate(pattern))


def run_stage(cost, epsilon, budget):
    n = len(next(iter(cost)))
    optimum = min(cost.values())
    queried = 0
    cells = []
    extracted = set()
    incumbent = None

    def add_cell(pattern):
        nonlocal queried, incumbent
        queried += 1
        members = [z for z in cost if matches(z, pattern)]
        if not members:
            return
        best = min(cost[z] for z in members)
        # The worst allowed candidate challenges the error certificate.
        candidate = max(
            (z for z in members if cost[z] <= best + epsilon),
            key=lambda z: (cost[z], z),
        )
        value = cost[candidate]
        lower = value - epsilon
        assert lower <= best <= value <= best + epsilon
        cells.append((lower, pattern, candidate))
        incumbent = value if incumbent is None else min(incumbent, value)

    add_cell((None,) * n)
    for step in range(budget + 1):
        covered = []
        for _, pattern, _ in cells:
            covered.extend(z for z in cost if matches(z, pattern))
        assert len(covered) == len(set(covered))
        assert set(covered) == set(cost) - extracted
        if not cells or min(cell[0] for cell in cells) >= incumbent:
            assert incumbent == optimum
            return True, len(extracted), queried
        if step == budget:
            assert len(extracted) == budget
            assert all(cost[z] <= optimum + epsilon for z in extracted)
            assert queried <= 1 + budget * n
            return False, len(extracted), queried

        index = min(range(len(cells)), key=lambda j: cells[j][0])
        lower, pattern, candidate = cells.pop(index)
        assert candidate not in extracted
        assert lower <= optimum
        assert cost[candidate] <= optimum + epsilon
        extracted.add(candidate)
        prefix = list(pattern)
        for i, value in enumerate(pattern):
            if value is not None:
                continue
            child = prefix.copy()
            child[i] = 1 - candidate[i]
            add_cell(tuple(child))
            prefix[i] = candidate[i]
    raise AssertionError("unreachable")


def main():
    rng = Random(20260922)
    stages = certificates = failures = calls = 0
    for n in range(1, 7):
        cube = list(product((0, 1), repeat=n))
        for case in range(12):
            supports = [z for z in cube if rng.randrange(4) != 0] or [cube[0]]
            noise = [F(rng.randrange(-3, 4), 7) for _ in range(n)]
            # Nonlinear, nonintegral deterministic support offsets.
            cost = {
                z: F(rng.randrange(-12, 13), 11)
                + sum(noise[i] * z[i] for i in range(n))
                for z in supports
            }
            if case == 0:
                cost = {z: F(0) for z in supports}  # Persistent ties.
            for epsilon in (F(0), F(1, 100), F(1, 3), F(2), F(10)):
                for budget in (1, 3, 5):
                    certified, _, queried = run_stage(cost, epsilon, budget)
                    stages += 1
                    certificates += certified
                    failures += not certified
                    calls += queried
    print(
        f"PASS: {stages} exact stages; {certificates} optimality certificates; "
        f"{failures} higher-gap failure witnesses; {calls} oracle calls."
    )
    print("Checked disjoint coverage, exact lower bounds, distinct extraction, "
          "and failure implying budget-many epsilon-near-optimal supports.")
    print("Not checked: continuous probability, asymptotic runtime, "
          "or the indicator grid-DP implementation.")


if __name__ == "__main__":
    main()
