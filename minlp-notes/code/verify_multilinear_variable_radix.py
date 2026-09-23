"""Exact profile and graph checks for the variable-radix lower construction."""

from fractions import Fraction as F
from itertools import product

def add_edge(graph, first, second):
    graph.setdefault(first, set()).add(second)
    graph.setdefault(second, set()).add(first)


def remove_node(graph, node):
    for neighbor in graph[node]:
        graph[neighbor].remove(node)
    del graph[node]


def check_profiles(levels, radix):
    weights = [
        F(radix - 1, radix ** (j + 1)) for j in range(levels)
    ] + [F(1, radix**levels)]
    first = [0] + [radix**j for j in range(1, levels + 1)]
    second = [0, 0] + [radix ** (j - 1) for j in range(2, levels + 1)]
    mean_first = sum(w * count for w, count in zip(weights, first))
    mean_second = sum(w * count for w, count in zip(weights, second))
    theta = (1 - mean_second) / (mean_first - mean_second)
    assert 0 <= theta <= 1
    assert theta * mean_first + (1 - theta) * mean_second == 1
    values = []
    for counts in [first, second]:
        value = 0
        for active, (weight, count) in enumerate(zip(weights, counts)):
            payoff = sum(min(radix**j, count) for j in range(1, active + 1))
            majorant = count + sum(radix**j for j in range(1, active))
            assert payoff == majorant
            value += weight * payoff
        values.append(value)
    assert theta * values[0] + (1 - theta) * values[1] == 1 + F(
        levels - 1, radix
    )


def check_graph(levels, radix):
    graph = {}
    leaves = [("v", word) for word in product(range(radix), repeat=levels)]
    factors = {j: [] for j in range(1, levels + 1)}
    for level in factors:
        for prefix in product(range(radix), repeat=level):
            factor = ("e", level, prefix)
            factors[level].append(factor)
            add_edge(graph, factor, ("a", level))
    for leaf in leaves:
        for level in factors:
            add_edge(graph, leaf, ("e", level, leaf[1][:level]))
    original = {node: neighbors.copy() for node, neighbors in graph.items()}
    order = leaves + [
        factor
        for level in range(levels, 0, -1)
        for factor in factors[level]
    ] + [("a", level) for level in factors]
    width = 0
    for node in order:
        neighbors = list(graph[node])
        width = max(width, len(neighbors))
        if node[0] == "e":
            level, prefix = node[1:]
            allowed = {
                ("e", earlier, prefix[:earlier]) for earlier in range(1, level)
            } | {("a", deeper) for deeper in range(level, levels + 1)}
            assert set(neighbors) <= allowed
        for position, first in enumerate(neighbors):
            for second in neighbors[position + 1 :]:
                add_edge(graph, first, second)
        remove_node(graph, node)
    assert width == levels
    if levels >= 3:
        while original:
            node = min(original, key=lambda item: len(original[item]))
            assert len(original[node]) <= levels - 1
            remove_node(original, node)
    print(f"L={levels}, b={radix}: elimination width {width}; graph verified")


if __name__ == "__main__":
    for level_count in range(2, 9):
        for base in range(level_count, level_count + 4):
            check_profiles(level_count, base)
    print("Exact profile identities passed 28 parameter pairs.")
    for level_count, base in [(2, 2), (2, 3), (3, 3), (3, 4), (4, 4)]:
        check_graph(level_count, base)
