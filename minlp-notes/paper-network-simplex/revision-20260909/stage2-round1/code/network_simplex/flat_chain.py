"""Exact sparse-label oracle for a chain of parallel pairs and one bypass.

Unobserved labels share one default state. Its profile coordinate is eliminated.
At most two observed labels need only interval tests; three use 16 circuits
and return unit flow/product coefficients after possible flow-balance repair.
Larger observed-label counts use exponential fixed libraries. Only Python's
standard library is used. Indices are zero based; the original residual state
has index simplex_size, and is never an independently observed product.
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
    """Historical unreduced bases; never used by the reduced production oracle."""
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


@lru_cache(maxsize=None)
def reduced_library(a):
    """Positive-subset, negative-singleton/full circuits in a dimensions.

Counts for a=1,2,3 are 1,5,16. Production bypasses this enumeration at a<=2.
"""
    if type(a) is not int or a < 1:
        raise ValueError("a must be a positive integer")
    positive = {tuple(row) for row in product((0, 1), repeat=a) if any(row)}
    normals = tuple(sorted(positive | {(-1,) * a} | {
        tuple(-int(j == k) for j in range(a)) for k in range(a)}))
    circuits = []
    for size in range(2, a + 2):
        for indices in combinations(range(len(normals)), size):
            reduced, pivots = _rref([[normals[i][j] for i in indices] for j in range(a)], size)
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
def _reduced_bases(a):
    """All full-dimensional inverse bases; there is no fixed profile sum."""
    normals, _ = reduced_library(a)
    found = []
    for indices in combinations(range(len(normals)), a):
        augmented = [list(normals[k]) + [int(i == j) for j in range(a)]
                     for i, k in enumerate(indices)]
        reduced, pivots = _rref(augmented, a)
        if len(pivots) == a:
            found.append((indices, tuple(tuple(row[a:]) for row in reduced)))
    return tuple(found)


@dataclass
class FlatChainDecomposition:
    """Compact grouped weighted flows; unused original labels share a default.

weights and flow(j) retain their original-state meaning. profile and arc_a
are compatibility properties that materialize the formerly dense arrays.
The stored grouped arrays have only len(labels)+1 state columns.
"""
    weights: tuple
    labels: tuple
    group_weights: tuple
    group_profile: tuple
    group_arc_a: tuple

    def __post_init__(self):
        self._slots = {j: i for i, j in enumerate(self.labels)}

    def positive_states(self):
        return (j for j, weight in enumerate(self.weights) if weight > 0)

    def _slot(self, state):
        return self._slots.get(state, len(self.labels))

    def _weighted(self, values, state):
        slot = self._slot(state)
        weight = self.group_weights[slot]
        return values[slot] * self.weights[state] / weight if weight else F(0)

    @property
    def profile(self):
        return tuple(self._weighted(self.group_profile, j) for j in range(len(self.weights)))

    @property
    def arc_a(self):
        return tuple(tuple(self._weighted(row, j) for j in range(len(self.weights)))
                     for row in self.group_arc_a)

    def flow(self, state):
        if type(state) is not int or not 0 <= state < len(self.weights) or self.weights[state] <= 0:
            raise ValueError("Only positive-weight states have decomposition flows")
        slot = self._slot(state)
        weight, branch = self.group_weights[slot], self.group_profile[slot]
        flow = []
        for gadget in self.group_arc_a:
            value = gadget[slot]
            flow.extend((value / weight, (branch - value) / weight))
        flow.append((weight - branch) / weight)
        return tuple(flow)


class FlatChainSimplex:
    """Canonical unit-capacity, unit-flow flat series--parallel chain.

Gadget l has arcs 2*l and 2*l+1, both l -> l+1. The bypass is 2*gadgets.
Only labels occurring in observations enter profile/circuit construction.
"""

    def __init__(self, gadgets, simplex_size, observations):
        if type(gadgets) is not int or gadgets < 1:
            raise ValueError("gadgets must be a positive integer")
        if type(simplex_size) is not int or simplex_size < 0:
            raise ValueError("simplex_size must be a nonnegative integer")
        self.gadgets, self.simplex_size = gadgets, simplex_size
        self.arcs = tuple((i, i+1, F(1)) for i in range(gadgets) for _ in range(2)) + ((0, gadgets, F(1)),)
        self.balances = (F(-1),) + (F(0),) * (gadgets - 1) + (F(1),)
        valid = []
        try:
            for observation in observations:
                edge, state = observation
                if type(edge) is not int or type(state) is not int or not (0 <= edge < len(self.arcs) and 0 <= state < simplex_size):
                    raise ValueError("Observation indices must be integers in range")
                valid.append((edge, state))
        except (TypeError, ValueError) as error:
            raise ValueError("Observations must be pairs of integer indices in range") from error
        self.observations = tuple(sorted(set(valid)))
        self.labels = tuple(sorted({j for _, j in self.observations}))
        a = len(self.labels)
        slots = {j: i for i, j in enumerate(self.labels)}
        categories = [["U"] * (a+1) for _ in range(gadgets)]
        for edge, state in self.observations:
            if edge == 2*gadgets:
                continue
            row, slot = categories[edge//2], slots[state]
            row[slot] = "T" if row[slot] != "U" else "A" if edge % 2 == 0 else "B"
        self.categories = tuple(map(tuple, categories))
        self.singletons = tuple(tuple(int(k == j) for k in range(a)) for j in range(a))
        if a == 0:
            self.normals, self.circuits = (), ()
        elif a == 1:
            self.normals, self.circuits = ((1,), (-1,)), (((0, 1), (1, 1)),)
        elif a == 2:
            self.normals = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1))
            self.circuits = (((0, 1), (1, 1)), ((2, 3), (1, 1)), ((4, 5), (1, 1)),
                             ((0, 2, 5), (1, 1, 1)), ((1, 3, 4), (1, 1, 1)))
        else:
            self.normals, self.circuits = reduced_library(a)

    def separate(self, point, decompose=True):
        """Return an exact globally valid cut, or membership and optional flows."""
        m, a, bypass = self.simplex_size, len(self.labels), 2*self.gadgets
        if len(point.x) != len(self.arcs) or len(point.y) != m:
            raise ValueError("Point dimensions do not match model")
        if set(point.z) != set(self.observations):
            raise ValueError("Point z keys must equal the model's observation set")

        def violated(expression, reason):
            expression.reason = reason
            assert expression.evaluate(point) > 0
            return SeparationResult(cut=expression)

        def balance(gadget):
            return combine(variable("x", edge) for edge in (2*gadget, 2*gadget+1, bypass)) - Cut({}, F(1))

        for edge, flow in enumerate(point.x):
            if flow < 0:
                return violated(-variable("x", edge), "flow bound")
            if flow > 1:
                return violated(variable("x", edge) - Cut({}, F(1)), "flow bound")
        for gadget in range(self.gadgets):
            value = point.x[2*gadget] + point.x[2*gadget+1] + point.x[bypass] - 1
            if value:
                expression = balance(gadget)
                return violated(expression if value > 0 else -expression, "flat chain flow balance")
        for j, weight in enumerate(point.y):
            if weight < 0:
                return violated(-variable("y", j), "simplex nonnegativity")
        weight_sum = sum(point.y, F(0))
        if weight_sum > 1:
            return violated(combine(variable("y", j) for j in range(m)) - Cut({}, F(1)), "simplex total weight")
        for (edge, state), value in point.z.items():
            if value < 0:
                return violated(-variable("z", edge, state), "product nonnegativity")
        original_weights = point.y + (1-weight_sum,)
        total_value = 1-point.x[bypass]
        if not a:
            dec = FlatChainDecomposition(original_weights, (), (F(1),), (total_value,),
                                         tuple((point.x[2*i],) for i in range(self.gadgets))) if decompose else None
            return SeparationResult(decomposition=dec)

        weights = [variable("y", j) for j in self.labels]
        weights.append(Cut({}, F(1)) - combine(weights))
        grouped = {}

        def add(row, expression):
            value = expression.evaluate(point)
            if row not in grouped or value < grouped[row][0]:
                grouped[row] = (value, expression)

        total = Cut({}, F(1)) - variable("x", bypass)
        add((1,)*a, total)
        add((-1,)*a, weights[-1]-total)
        for slot, state in enumerate(self.labels):
            singleton = self.singletons[slot]
            negative = tuple(-v for v in singleton)
            add(negative, Cut({})); add(singleton, weights[slot])
            if (bypass, state) in point.z:
                rhs = weights[slot]-variable("z", bypass, state)
                add(singleton, rhs); add(negative, -rhs)
        for gadget, category in enumerate(self.categories):
            rhs_terms = [variable("x", 2*gadget)]
            for slot, label in enumerate(category[:-1]):
                state = self.labels[slot]
                singleton = self.singletons[slot]
                negative = tuple(-v for v in singleton)
                if label in ("A", "T"):
                    u = variable("z", 2*gadget, state); rhs_terms.append(-u)
                if label in ("B", "T"):
                    v = variable("z", 2*gadget+1, state)
                    if label == "B": rhs_terms.append(v)
                if label == "A": add(negative, -u)
                elif label == "B": add(negative, -v)
                elif label == "T":
                    add(singleton, u+v); add(negative, -(u+v))
            rhs = combine(rhs_terms)
            add(tuple(int(label == "B") for label in category[:-1]), rhs)
            add(tuple(int(label in ("A", "T")) for label in category[:-1]), total-rhs)

        zero = grouped.get((0,)*a)
        if zero is not None and zero[0] < 0:
            return violated(-zero[1], "flat profile zero row")
        present = {i: grouped[row] for i, row in enumerate(self.normals) if row in grouped}
        for indices, multipliers in self.circuits:
            if not all(i in present for i in indices):
                continue
            value = sum(multiplier*present[i][0] for i, multiplier in zip(indices, multipliers))
            if value < 0:
                expression = -combine(multiplier*present[i][1] for i, multiplier in zip(indices, multipliers))
                if a == 3 and abs(expression.coefficients.get(("x", bypass), 0)) == 2:
                    sign = expression.coefficients["x", bypass]/2
                    gadget = next(i for i in range(self.gadgets) if expression.coefficients.get(("x", 2*i), 0) == sign)
                    expression = expression-sign*balance(gadget)
                if a <= 3:
                    assert all(abs(v) <= 1 for key, v in expression.coefficients.items() if key[0] in ("x", "z"))
                return violated(expression, "flat profile positive circuit")
        if not decompose:
            return SeparationResult()

        if a == 1:
            candidate = (-grouped[(-1,)][0],)
        elif a == 2:
            l1, l2, ls = (-grouped[(-1, 0)][0], -grouped[(0, -1)][0], -grouped[(-1, -1)][0])
            u1, u2 = grouped[(1, 0)][0], grouped[(0, 1)][0]
            chosen_sum = max(ls, l1+l2)
            first = max(l1, chosen_sum-u2)
            candidate = (first, chosen_sum-first)
        else:
            candidate = None
            for indices, inverse in _reduced_bases(a):
                if not all(i in present for i in indices): continue
                rhs = [present[i][0] for i in indices]
                trial = tuple(sum(v*b for v, b in zip(row, rhs)) for row in inverse)
                if all(sum(v*b for v, b in zip(row, trial)) <= value
                       for row, (value, _) in grouped.items()):
                    candidate = trial
                    break
            if candidate is None:
                raise AssertionError("Circuit-feasible bounded reduced profile has no enumerated vertex")
        profile = candidate + (total_value-sum(candidate),)
        group_weights = tuple(point.y[j] for j in self.labels) + (1-sum(point.y[j] for j in self.labels),)
        assert all(0 <= value <= weight for value, weight in zip(profile, group_weights))
        arc_a = []
        for gadget, category in enumerate(self.categories):
            row = [F(0)]*(a+1)
            for slot, label in enumerate(category[:-1]):
                state = self.labels[slot]
                if label in ("A", "T"): row[slot] = point.z[2*gadget, state]
                elif label == "B": row[slot] = profile[slot]-point.z[2*gadget+1, state]
            remaining = point.x[2*gadget]-sum(row)
            for slot, label in enumerate(category):
                if label == "U":
                    row[slot] = min(remaining, profile[slot]); remaining -= row[slot]
            assert remaining == 0 and all(0 <= row[j] <= profile[j] for j in range(a+1))
            arc_a.append(tuple(row))
        return SeparationResult(decomposition=FlatChainDecomposition(
            original_weights, self.labels, group_weights, profile, tuple(arc_a)))

