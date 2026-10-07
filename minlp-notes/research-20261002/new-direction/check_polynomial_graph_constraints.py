"""Exact diagnostics for smoothed-polynomial-graph-constraints.md."""

from collections import Counter
from fractions import Fraction as Q
from itertools import product


def chain_objective(t, eta):
    targets = (Q(1, 2), Q(3, 4))
    regularization = Q(1, 4)
    free_noise = (Q(1), Q(-1), Q(1, 2))
    z = (t[0] * t[1], t[1] * t[2])
    return (sum((value - target) ** 2 for value, target in zip(z, targets))
            + regularization * sum(value * value for value in t)
            + sum(a * b for a, b in zip(free_noise, t))
            + sum(a * b for a, b in zip(eta, z)))


def graph_rounding():
    curvature = Q(9, 2)  # 4+2*lambda, with lambda=1/4.
    count = 0
    for eta in product([Q(-1), Q(0), Q(1)], repeat=2):
        for t in product([Q(k, 4) for k in range(5)], repeat=3):
            expected = Q(0)
            expected_auxiliary = Q(0)
            for corner in product([Q(0), Q(1)], repeat=3):
                probability = Q(1)
                for value, mean in zip(corner, t):
                    probability *= mean if value else 1 - mean
                expected += probability * chain_objective(corner, eta)
                expected_auxiliary += probability * (
                    eta[0] * corner[0] * corner[1] + eta[1] * corner[1] * corner[2]
                )
            variance = sum(value * (1 - value) for value in t)
            assert expected <= chain_objective(t, eta) + curvature * variance / 2
            assert expected_auxiliary == eta[0] * t[0] * t[1] + eta[1] * t[1] * t[2]
            diagonal = (Q(1, 2) + 2 * t[1] ** 2,
                        Q(1, 2) + 2 * t[0] ** 2 + 2 * t[2] ** 2,
                        Q(1, 2) + 2 * t[1] ** 2)
            assert max(diagonal) <= curvature
            count += 1
    return count


def check_decomposition():
    parents = {"z0": {"t0", "t1"}, "z1": {"t1", "t2"}, "z2": {"z0", "z1"}}
    bags = [{"t0", "t1", "z0"}, {"t1", "z0", "z1", "z2"}, {"t1", "t2", "z1"}]
    edges = [(0, 1), (1, 2)]
    ancestry = {f"t{i}": {f"t{i}"} for i in range(3)}
    for name, inputs in parents.items():
        ancestry[name] = set().union(*(ancestry[v] for v in inputs))
        assert any({name} | inputs <= bag for bag in bags)
    expanded = [set().union(*(ancestry[v] for v in bag)) for bag in bags]
    for collection in [bags, expanded]:
        for variable in set().union(*collection):
            occurrences = {i for i, bag in enumerate(collection) if variable in bag}
            reached = {min(occurrences)}
            while True:
                new = reached | {b for a, b in edges if a in reached and b in occurrences}
                new |= {a for a, b in edges if b in reached and a in occurrences}
                if new == reached:
                    break
                reached = new
            assert reached == occurrences
    assert max(map(len, expanded)) == 3
    assert ancestry["z2"] <= expanded[1]


def noise_and_curvature_obstructions():
    for size in [2, 4, 8]:
        law = [Q(-1) + Q(2 * k, size - 1) for k in range(size)]
        joint = Counter((a + b, a + 2 * b) for a, b in product(law, repeat=2))
        conditional = {c1: mass for (c1, c2), mass in joint.items() if c2 == 3}
        assert conditional == {Q(2): 1}
        assert Q(conditional[Q(2)], sum(conditional.values())) == 1 > Q(1, size)
        # Conditioning on an independent auxiliary coefficient preserves an anchor law.
        anchor_pairs = Counter((gamma, eta) for gamma, eta in product(law, repeat=2))
        for eta in law:
            assert [anchor_pairs[(gamma, eta)] for gamma in law] == [1] * size
    epsilon, cross = Q(1), Q(2) ** 100
    ambient_diagonal = 2 * epsilon
    pulled_diagonal = 2 * cross + 4 * epsilon
    assert pulled_diagonal > 2 ** 100 * ambient_diagonal


if __name__ == "__main__":
    count = graph_rounding()
    check_decomposition()
    noise_and_curvature_obstructions()
    print(f"PASS: {count} coupled quartic rounding and uniform-curvature cases")
    print("PASS: overlapping depth-two graph decomposition and ancestor bags")
    print("PASS: three finite noise laws, anchor escape, and curvature obstruction")
