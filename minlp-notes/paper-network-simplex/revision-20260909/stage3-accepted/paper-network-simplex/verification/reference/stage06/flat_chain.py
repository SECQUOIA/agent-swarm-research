"""Exact fixed-state oracle for a chain of two-arc gadgets and one bypass.

The circuit and profile-basis libraries are exponential in simplex dimension.
This implementation is intended for few-state problems; it is not a general
polynomial-time alternative to the disaggregated flow formulation.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from math import gcd, lcm

from .separator import Cut, SeparationResult, combine, variable


def _rref(matrix, columns):
    matrix = [[F(value) for value in row] for row in matrix]
    pivots = []
    for column in range(columns):
        index = next((i for i in range(len(pivots), len(matrix)) if matrix[i][column]), None)
        if index is None:
            continue
        row = len(pivots)
        matrix[row], matrix[index] = matrix[index], matrix[row]
        divisor = matrix[row][column]
        matrix[row] = [value / divisor for value in matrix[row]]
        for i in range(len(matrix)):
            if i != row and matrix[i][column]:
                multiplier = matrix[i][column]
                matrix[i] = [a - multiplier * b for a, b in zip(matrix[i], matrix[row])]
        pivots.append(column)
    return matrix, pivots


@lru_cache(maxsize=None)
def circuit_library(d):
    """Return all signed-subset normals and primitive positive circuits.

    Library construction uses exact rational elimination. For d=1,2,3 there
    are respectively 1,5,41 circuits. Costs grow exponentially with d.
    """
    if not isinstance(d, int) or d < 1:
        raise ValueError("d must be a positive integer")
    normals = tuple(tuple(sign * value for value in row)
                    for row in product((0, 1), repeat=d) if any(row)
                    for sign in (-1, 1))
    circuits = []
    for size in range(2, d + 2):
        for indices in combinations(range(len(normals)), size):
            matrix = [[normals[index][j] for index in indices] for j in range(d)]
            reduced, pivots = _rref(matrix, size)
            if len(pivots) != size - 1:
                continue
            free = next(j for j in range(size) if j not in pivots)
            ray = [F(0)] * size
            ray[free] = F(1)
            for row, pivot in enumerate(pivots):
                ray[pivot] = -reduced[row][free]
            if not all(value > 0 for value in ray):
                continue
            scale = lcm(*(value.denominator for value in ray))
            integers = [int(value * scale) for value in ray]
            divisor = gcd(*integers)
            circuits.append((indices, tuple(value // divisor for value in integers)))
    return normals, tuple(circuits)


@lru_cache(maxsize=None)
def _profile_bases(d):
    """Inverse bases for the always-present sum equality and d-1 subset rows."""
    normals, _ = circuit_library(d)
    full = (1,) * d
    indices = [i for i, row in enumerate(normals) if row not in (full, (-1,) * d)]
    found = []
    for selected in combinations(indices, d - 1):
        matrix = [full] + [normals[i] for i in selected]
        augmented = [list(row) + [int(i == j) for j in range(d)] for i, row in enumerate(matrix)]
        reduced, pivots = _rref(augmented, d)
        if len(pivots) == d:
            found.append((selected, tuple(tuple(row[d:]) for row in reduced)))
    return tuple(found)


@dataclass
class FlatChainDecomposition:
    """Weighted shared profile and arc-a state flows, with lazy graph output."""

    weights: tuple
    profile: tuple
    arc_a: tuple

    def positive_states(self):
        return (j for j, weight in enumerate(self.weights) if weight > 0)

    def flow(self, state):
        if not 0 <= state < len(self.weights) or self.weights[state] <= 0:
            raise ValueError("Only positive-weight states have decomposition flows")
        weight, branch = self.weights[state], self.profile[state]
        flow = []
        for gadget in self.arc_a:
            a = gadget[state]
            flow.extend((a / weight, (branch - a) / weight))
        flow.append((weight - branch) / weight)
        return tuple(flow)


class FlatChainSimplex:
    """Canonical unit-capacity, unit-flow flat series–parallel chain.

    Gadget l has arcs 2*l and 2*l+1, both l -> l+1. The bypass is arc
    2*gadgets, from node 0 to node gadgets. Explicit states range from 0 to
    simplex_size-1, and the residual simplex vertex has index simplex_size.
    """

    def __init__(self, gadgets, simplex_size, observations):
        if not isinstance(gadgets, int) or gadgets < 1:
            raise ValueError("gadgets must be a positive integer")
        if not isinstance(simplex_size, int) or simplex_size < 0:
            raise ValueError("simplex_size must be a nonnegative integer")
        self.gadgets, self.simplex_size = gadgets, simplex_size
        self.arcs = tuple((i, i+1, F(1)) for i in range(gadgets) for _ in range(2)) + ((0, gadgets, F(1)),)
        self.balances = (F(-1),) + (F(0),) * (gadgets - 1) + (F(1),)
        self.observations = tuple(sorted(set(observations)))
        for edge, state in self.observations:
            if not isinstance(edge, int) or not isinstance(state, int) or not (0 <= edge < len(self.arcs) and 0 <= state < simplex_size):
                raise ValueError("Observation indices must be integers in range")
        observation_set = set(self.observations)
        self.categories = []
        for gadget in range(gadgets):
            category = []
            for state in range(simplex_size + 1):
                a, b = (2*gadget, state) in observation_set, (2*gadget+1, state) in observation_set
                category.append("T" if a and b else "A" if a else "B" if b else "U")
            self.categories.append(tuple(category))
        self.normals, self.circuits = circuit_library(simplex_size + 1)

    def separate(self, point, decompose=True):
        """Return a globally valid exact cut, or membership and optional flows."""
        m, d, bypass = self.simplex_size, self.simplex_size + 1, 2*self.gadgets
        if len(point.x) != len(self.arcs) or len(point.y) != m:
            raise ValueError("Point dimensions do not match model")
        if set(point.z) != set(self.observations):
            raise ValueError("Point z keys must equal the model's observation set")

        def violated(expression, reason):
            expression.reason = reason
            assert expression.evaluate(point) > 0
            return SeparationResult(cut=expression)

        for edge, flow in enumerate(point.x):
            if flow < 0:
                return violated(-variable("x", edge), "flow bound")
            if flow > 1:
                return violated(variable("x", edge) - Cut({}, F(1)), "flow bound")
        for gadget in range(self.gadgets):
            expression = combine(variable("x", edge) for edge in (2*gadget, 2*gadget+1, bypass)) - Cut({}, F(1))
            value = expression.evaluate(point)
            if value:
                return violated(expression if value > 0 else -expression, "flat chain flow balance")
        for j, weight in enumerate(point.y):
            if weight < 0:
                return violated(-variable("y", j), "simplex nonnegativity")
        if sum(point.y) > 1:
            return violated(combine(variable("y", j) for j in range(m)) - Cut({}, F(1)), "simplex total weight")
        for (edge, state), value in point.z.items():
            if value < 0:
                return violated(-variable("z", edge, state), "product nonnegativity")

        weights = [variable("y", j) for j in range(m)]
        weights.append(Cut({}, F(1)) - combine(weights))
        grouped = {}

        def add(row, expression):
            row = tuple(row)
            value = expression.evaluate(point)
            if row not in grouped or value < grouped[row][0]:
                grouped[row] = (value, expression)

        def singleton(state, sign=1):
            return tuple(sign if j == state else 0 for j in range(d))

        full = (1,) * d
        total = Cut({}, F(1)) - variable("x", bypass)
        add(full, total)
        add((-1,) * d, -total)
        for state in range(d):
            add(singleton(state, -1), Cut({}))
            add(singleton(state), weights[state])
            if (bypass, state) in point.z:
                rhs = weights[state] - variable("z", bypass, state)
                add(singleton(state), rhs)
                add(singleton(state, -1), -rhs)
        for gadget, category in enumerate(self.categories):
            rhs_terms = [variable("x", 2*gadget)]
            for state, label in enumerate(category):
                if label in ("A", "T"):
                    u = variable("z", 2*gadget, state)
                    rhs_terms.append(-u)
                if label in ("B", "T"):
                    v = variable("z", 2*gadget+1, state)
                    if label == "B":
                        rhs_terms.append(v)
                if label == "A":
                    add(singleton(state, -1), -u)
                elif label == "B":
                    add(singleton(state, -1), -v)
                elif label == "T":
                    add(singleton(state), u + v)
                    add(singleton(state, -1), -(u + v))
            rhs = combine(rhs_terms)
            add(tuple(int(label == "B") for label in category), rhs)
            add(tuple(-int(label in ("B", "U")) for label in category), -rhs)

        zero = grouped.get((0,) * d)
        if zero is not None and zero[0] < 0:
            return violated(-zero[1], "flat profile zero row")
        present = {i: grouped[row] for i, row in enumerate(self.normals) if row in grouped}
        for indices, multipliers in self.circuits:
            if all(i in present for i in indices):
                value = sum(multiplier * present[i][0] for i, multiplier in zip(indices, multipliers))
                if value < 0:
                    expression = -combine(multiplier * present[i][1] for i, multiplier in zip(indices, multipliers))
                    return violated(expression, "flat profile positive circuit")
        if not decompose:
            return SeparationResult()

        total_value = 1 - point.x[bypass]
        profile = None
        for indices, inverse in _profile_bases(d):
            if not all(i in present for i in indices):
                continue
            rhs = [total_value] + [present[i][0] for i in indices]
            candidate = tuple(sum(a * b for a, b in zip(row, rhs)) for row in inverse)
            if all(sum(a * b for a, b in zip(self.normals[i], candidate)) <= value
                   for i, (value, _) in present.items()):
                profile = candidate
                break
        if profile is None:
            raise AssertionError("Circuit-feasible bounded profile has no enumerated vertex")
        arc_a = []
        for gadget, category in enumerate(self.categories):
            row = [F(0)] * d
            for state, label in enumerate(category):
                if label in ("A", "T"):
                    row[state] = point.z[2*gadget, state]
                elif label == "B":
                    row[state] = profile[state] - point.z[2*gadget+1, state]
            remaining = point.x[2*gadget] - sum(row)
            for state, label in enumerate(category):
                if label == "U":
                    row[state] = min(remaining, profile[state])
                    remaining -= row[state]
            assert remaining == 0 and all(0 <= row[j] <= profile[j] for j in range(d))
            arc_a.append(tuple(row))
        original_weights = point.y + (1 - sum(point.y),)
        return SeparationResult(decomposition=FlatChainDecomposition(original_weights, profile, tuple(arc_a)))
