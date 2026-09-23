"""Exact graph-to-cut implementation of the parallel-path hull theorem.

All arithmetic uses fractions.Fraction. Node, arc, and explicit state indices
are zero based. Incidence is incoming minus outgoing. The implicit residual
simplex state has index ``simplex_size``. There are no numerical tolerances.
"""

from collections import deque
from dataclasses import dataclass
from fractions import Fraction as F


class UnsupportedGraph(ValueError):
    """A biconnected block is not a union of internally disjoint paths."""


class InfeasibleModel(ValueError):
    """The base flow polytope is empty."""


def rational(value):
    # Decimal text avoids surprising binary expansions for ordinary float input.
    return F(str(value)) if isinstance(value, float) else F(value)


@dataclass(frozen=True)
class Point:
    x: tuple
    y: tuple
    z: dict

    def __post_init__(self):
        object.__setattr__(self, "x", tuple(map(rational, self.x)))
        object.__setattr__(self, "y", tuple(map(rational, self.y)))
        object.__setattr__(self, "z", {k: rational(v) for k, v in self.z.items()})


@dataclass
class Cut:
    """A globally valid inequality ``constant + sum(coefficients * point) <= 0``.

    Keys are ("x", edge), ("y", state), or ("z", edge, state). Coefficients
    and constant are exact fractions. ``reason`` identifies the violated family.
    """

    coefficients: dict
    constant: F = F(0)
    reason: str = ""

    def evaluate(self, point):
        def value(key):
            if key[0] == "x":
                return point.x[key[1]]
            if key[0] == "y":
                return point.y[key[1]]
            return point.z[key[1:]]
        return self.constant + sum((c * value(k) for k, c in self.coefficients.items()), F(0))

    def __add__(self, other):
        return combine((self, other))

    def __sub__(self, other):
        return combine((self, -other))

    def __neg__(self):
        return self * -1

    def __mul__(self, scalar):
        scalar = rational(scalar)
        return Cut({k: v * scalar for k, v in self.coefficients.items() if v * scalar},
                   self.constant * scalar)

    __rmul__ = __mul__


def combine(expressions):
    coefficients = {}
    constant = F(0)
    for expression in expressions:
        constant += expression.constant
        for key, value in expression.coefficients.items():
            coefficients[key] = coefficients.get(key, F(0)) + value
    return Cut({k: v for k, v in coefficients.items() if v}, constant)


def variable(*key):
    return Cut({key: F(1)})


@dataclass
class _Active:
    value: F
    expression: Cut


def active_sum(values):
    values = list(values)
    return _Active(sum((v.value for v in values), F(0)),
                   combine(v.expression for v in values))


def active_neg(value):
    return _Active(-value.value, -value.expression)


@dataclass
class _Block:
    paths: list
    lower: tuple
    upper: tuple
    scalar: bool = False


@dataclass
class CompactDecomposition:
    """Normalized block vectors, with one default and observed-state exceptions.

    ``flow(j)`` materializes a feasible full flow for any positive-weight state.
    The shared representation avoids storing (m+1)*|E| flow entries.
    """

    model: object
    weights: tuple
    coordinates: list

    def flow(self, state):
        if not 0 <= state < len(self.weights) or self.weights[state] <= 0:
            raise ValueError("Only positive-weight states have decomposition flows")
        flow = list(self.model.reference)
        for block, (default, exceptions) in zip(self.model.blocks, self.coordinates):
            vector = exceptions.get(state, default)
            for path, deviation in zip(block.paths, vector):
                for edge, sign in path:
                    flow[edge] += sign * deviation
        return tuple(flow)

    def positive_states(self):
        return (j for j, weight in enumerate(self.weights) if weight > 0)


@dataclass
class SeparationResult:
    cut: Cut | None = None
    decomposition: CompactDecomposition | None = None

    @property
    def feasible(self):
        return self.cut is None


def _transport(row_sums, column_sums, capacities):
    """Edmonds–Karp with exact rational capacities; return matrix or violated rows."""
    rows, columns = len(row_sums), len(column_sums)
    source, sink = rows + columns, rows + columns + 1
    adjacency = [[] for _ in range(sink + 1)]

    def add(u, v, cap):
        forward = [v, len(adjacency[v]), cap]
        reverse = [u, len(adjacency[u]), F(0)]
        adjacency[u].append(forward)
        adjacency[v].append(reverse)
        return forward

    for i, supply in enumerate(row_sums):
        add(source, i, supply)
    cells = [[add(i, rows + j, capacities[i][j]) for j in range(columns)]
             for i in range(rows)]
    for j, demand in enumerate(column_sums):
        add(rows + j, sink, demand)
    total = sum(row_sums, F(0))
    value = F(0)
    while value < total:
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            u = queue.popleft()
            for index, (v, _, capacity) in enumerate(adjacency[u]):
                if capacity > 0 and v not in parent:
                    parent[v] = (u, index)
                    queue.append(v)
        if sink not in parent:
            return None, {i for i in range(rows) if i in parent}
        amount = total - value
        v = sink
        while v != source:
            u, index = parent[v]
            amount = min(amount, adjacency[u][index][2])
            v = u
        v = sink
        while v != source:
            u, index = parent[v]
            arc = adjacency[u][index]
            arc[2] -= amount
            adjacency[v][arc[1]][2] += amount
            v = u
        value += amount
    return [[capacities[i][j] - cells[i][j][2] for j in range(columns)]
            for i in range(rows)], None


class NetworkSimplex:
    """Preprocessed bounded flow/simplex block model.

    ``arcs`` contains (tail, head, capacity); ``balances`` supplies one incoming
    minus outgoing balance per node. Parallel arcs, loops, isolated nodes, and
    disconnected components are supported. A base-infeasible model raises
    InfeasibleModel; an unsupported block raises UnsupportedGraph.
    """

    def __init__(self, arcs, balances, simplex_size, observations):
        self.balances = tuple(map(rational, balances))
        self.arcs = tuple((a, b, rational(u)) for a, b, u in arcs)
        self.simplex_size = simplex_size
        if not isinstance(simplex_size, int) or simplex_size < 0:
            raise ValueError("simplex_size must be a nonnegative integer")
        nodes = len(self.balances)
        for a, b, capacity in self.arcs:
            if not isinstance(a, int) or not isinstance(b, int) or not (0 <= a < nodes and 0 <= b < nodes):
                raise ValueError("Arc endpoints must index balances")
            if capacity < 0:
                raise InfeasibleModel("Negative capacity")
        self.observations = tuple(sorted(set(observations)))
        for edge, state in self.observations:
            if not isinstance(edge, int) or not isinstance(state, int) or not (0 <= edge < len(self.arcs) and 0 <= state < simplex_size):
                raise ValueError("Observation indices must be integers in range")
        self._preprocess()
        self.grouped = [{} for _ in self.blocks]
        self.bridge_observations = []
        for edge, state in self.observations:
            if edge not in self.location:
                self.bridge_observations.append((edge, state))
            else:
                block, path, sign = self.location[edge]
                self.grouped[block].setdefault(state, []).append((edge, path, sign))
        self.block_states = [tuple(sorted(group)) for group in self.grouped]

    def _preprocess(self):
        """Iterative edge-stack Tarjan, preserving distinct parallel arc IDs."""
        n = len(self.balances)
        adjacency = [[] for _ in range(n)]
        loops = []
        for edge, (a, b, _) in enumerate(self.arcs):
            if a == b:
                loops.append(edge)
            else:
                adjacency[a].append((b, edge))
                adjacency[b].append((a, edge))
        discovery = [-1] * n
        low = [0] * n
        subtree = list(self.balances)
        reference = [F(0)] * len(self.arcs)
        edge_stack, components = [], []
        clock = 0
        for root in range(n):
            if discovery[root] >= 0:
                continue
            discovery[root] = low[root] = clock
            clock += 1
            stack = [[root, -1, -1, 0]]
            while stack:
                node, parent, parent_edge, cursor = stack[-1]
                if cursor < len(adjacency[node]):
                    neighbor, edge = adjacency[node][cursor]
                    stack[-1][3] += 1
                    if edge == parent_edge:
                        continue
                    if discovery[neighbor] < 0:
                        edge_stack.append(edge)
                        discovery[neighbor] = low[neighbor] = clock
                        clock += 1
                        stack.append([neighbor, node, edge, 0])
                    elif discovery[neighbor] < discovery[node]:
                        low[node] = min(low[node], discovery[neighbor])
                        edge_stack.append(edge)
                else:
                    stack.pop()
                    if parent >= 0:
                        subtree[parent] += subtree[node]
                        a, b, _ = self.arcs[parent_edge]
                        reference[parent_edge] = subtree[node] if b == node else -subtree[node]
                        low[parent] = min(low[parent], low[node])
                        if low[node] >= discovery[parent]:
                            component = []
                            while True:
                                edge = edge_stack.pop()
                                component.append(edge)
                                if edge == parent_edge:
                                    break
                            components.append(component)
                    elif subtree[node] != 0:
                        raise InfeasibleModel("Nonzero total balance in a connected component")
        self.reference = tuple(reference)
        self.blocks, self.bridges, self.location = [], [], {}
        for component in components:
            if len(component) == 1:
                edge = component[0]
                if not 0 <= reference[edge] <= self.arcs[edge][2]:
                    raise InfeasibleModel("A forced bridge flow violates its bounds")
                self.bridges.append(edge)
                continue
            local = {}
            for edge in component:
                a, b, _ = self.arcs[edge]
                local.setdefault(a, []).append((b, edge))
                local.setdefault(b, []).append((a, edge))
            terminals = [node for node in local if len(local[node]) != 2]
            if not terminals:  # Split a cycle at the ends of any one arc.
                start, end, _ = self.arcs[component[0]]
            elif len(terminals) == 2 and len(local[terminals[0]]) == len(local[terminals[1]]):
                start, end = terminals
            else:
                raise UnsupportedGraph(f"Block with arcs {sorted(component)} is not parallel-path")
            paths, used = [], set()
            for neighbor, first_edge in local[start]:
                path, node, previous, edge = [], neighbor, start, first_edge
                while True:
                    if edge in used:
                        raise UnsupportedGraph("Parallel-path extraction revisited an arc")
                    used.add(edge)
                    a, b, _ = self.arcs[edge]
                    path.append((edge, 1 if a == previous and b == node else -1))
                    if node == end:
                        break
                    choices = [(v, e) for v, e in local[node] if e != edge]
                    if len(choices) != 1:
                        raise UnsupportedGraph("Parallel path has an internal branch")
                    previous, (node, edge) = node, choices[0]
                paths.append(path)
            if len(used) != len(component):
                raise UnsupportedGraph("Parallel paths do not cover the block")
            self._add_block(paths)
        for edge in loops:
            self._add_block([[(edge, 1)]], scalar=True)

    def _add_block(self, paths, scalar=False):
        lower, upper = [], []
        for path in paths:
            bounds = []
            for edge, sign in path:
                v, u = self.reference[edge], self.arcs[edge][2]
                bounds.append((-v, u-v) if sign == 1 else (v-u, v))
            lower.append(max(a for a, _ in bounds))
            upper.append(min(b for _, b in bounds))
        if any(a > b for a, b in zip(lower, upper)) or (not scalar and not sum(lower) <= 0 <= sum(upper)):
            raise InfeasibleModel("A block has no capacity-feasible circulation coordinates")
        index = len(self.blocks)
        self.blocks.append(_Block(paths, tuple(lower), tuple(upper), scalar))
        for p, path in enumerate(paths):
            for edge, sign in path:
                self.location[edge] = (index, p, sign)

    def separate(self, point, decompose=True):
        """Return an exact violated original-coordinate cut or hull membership.

        Two/three-path blocks use constant support families and linear-time
        construction. Larger blocks use exact capacitated max flow.
        """
        if len(point.x) != len(self.arcs) or len(point.y) != self.simplex_size:
            raise ValueError("Point dimensions do not match model")
        if set(point.z) != set(self.observations):
            raise ValueError("Point z keys must equal the model's observation set")

        def violation(expression, reason):
            if expression.evaluate(point) > 0:
                expression.reason = reason
                return SeparationResult(cut=expression)
            return None

        def equality(expression, reason):
            value = expression.evaluate(point)
            return violation(expression if value > 0 else -expression, reason) if value else None

        for edge, (_, _, capacity) in enumerate(self.arcs):
            for expression in (-variable("x", edge), variable("x", edge) - Cut({}, capacity)):
                result = violation(expression, "flow bound")
                if result:
                    return result
        balance_expressions = [Cut({}, -b) for b in self.balances]
        # In-place accumulation keeps high-degree node processing linear.
        for edge, (a, b, _) in enumerate(self.arcs):
            if a != b:
                balance_expressions[a].coefficients[("x", edge)] = F(-1)
                balance_expressions[b].coefficients[("x", edge)] = F(1)
        for expression in balance_expressions:
            result = equality(expression, "flow balance")
            if result:
                return result
        for j in range(self.simplex_size):
            result = violation(-variable("y", j), "simplex nonnegativity")
            if result:
                return result
        result = violation(combine(variable("y", j) for j in range(self.simplex_size)) - Cut({}, F(1)),
                           "simplex total weight")
        if result:
            return result
        for edge, j in self.bridge_observations:
            result = equality(variable("z", edge, j) - self.reference[edge] * variable("y", j),
                              "bridge observation")
            if result:
                return result
        coordinates = []
        for index, block in enumerate(self.blocks):
            states = self.block_states[index]
            weights = [variable("y", j) for j in states]
            weights.append(Cut({}, F(1)) - combine(weights))
            weight_values = [w.evaluate(point) for w in weights]
            k, count = len(block.paths), len(weights)
            lower = [[_Active(weight_values[j] * block.lower[i], weights[j] * block.lower[i])
                      for j in range(count)] for i in range(k)]
            upper = [[_Active(weight_values[j] * block.upper[i], weights[j] * block.upper[i])
                      for j in range(count)] for i in range(k)]
            for column, state in enumerate(states):
                for edge, path, sign in self.grouped[index][state]:
                    expression = sign * (variable("z", edge, state) - self.reference[edge] * variable("y", state))
                    active = _Active(expression.evaluate(point), expression)
                    if active.value > lower[path][column].value:
                        lower[path][column] = active
                    if active.value < upper[path][column].value:
                        upper[path][column] = active
            aggregate = []
            for path in block.paths:
                edge, sign = path[0]
                expression = sign * (variable("x", edge) - Cut({}, self.reference[edge]))
                aggregate.append(_Active(expression.evaluate(point), expression))
            for j in range(count):
                for i in range(k):
                    if lower[i][j].value > upper[i][j].value:
                        return violation(lower[i][j].expression - upper[i][j].expression, "state interval")
                if not block.scalar:
                    lo = active_sum(lower[i][j] for i in range(k))
                    hi = active_sum(upper[i][j] for i in range(k))
                    if lo.value > 0:
                        return violation(lo.expression, "state lower sum")
                    if hi.value < 0:
                        return violation(-hi.expression, "state upper sum")

            if block.scalar or k <= 3:
                tight_lower, tight_upper = lower, upper
                if not block.scalar:
                    tight_lower = [[max((lower[i][j], active_neg(active_sum(upper[h][j] for h in range(k) if h != i))),
                                         key=lambda a: a.value) for j in range(count)] for i in range(k)]
                    tight_upper = [[min((upper[i][j], active_neg(active_sum(lower[h][j] for h in range(k) if h != i))),
                                         key=lambda a: a.value) for j in range(count)] for i in range(k)]
                for i in range(k):
                    lo, hi = active_sum(tight_lower[i]), active_sum(tight_upper[i])
                    if aggregate[i].value < lo.value:
                        return violation(lo.expression - aggregate[i].expression, "aggregate lower support")
                    if aggregate[i].value > hi.value:
                        return violation(aggregate[i].expression - hi.expression, "aggregate upper support")
                if not decompose:
                    continue
                suffix_lo = [[F(0)] * (count + 1) for _ in range(k)]
                suffix_hi = [[F(0)] * (count + 1) for _ in range(k)]
                for i in range(k):
                    for j in range(count - 1, -1, -1):
                        suffix_lo[i][j] = suffix_lo[i][j+1] + tight_lower[i][j].value
                        suffix_hi[i][j] = suffix_hi[i][j+1] + tight_upper[i][j].value
                remaining = [a.value for a in aggregate]
                matrix = [[F(0)] * count for _ in range(k)]
                for j in range(count):
                    lo = [max(lower[i][j].value, remaining[i] - suffix_hi[i][j+1]) for i in range(k)]
                    hi = [min(upper[i][j].value, remaining[i] - suffix_lo[i][j+1]) for i in range(k)]
                    vector = list(lo)
                    if not block.scalar:
                        left = -sum(vector)
                        for i in range(k):
                            amount = min(left, hi[i] - lo[i])
                            vector[i] += amount
                            left -= amount
                        assert left == 0
                    for i in range(k):
                        assert lo[i] <= vector[i] <= hi[i]
                        matrix[i][j] = vector[i]
                        remaining[i] -= vector[i]
                assert not any(remaining)
            else:
                row_lower = [active_sum(lower[i]) for i in range(k)]
                rows = [aggregate[i].value - row_lower[i].value for i in range(k)]
                for i, amount in enumerate(rows):
                    if amount < 0:
                        return violation(row_lower[i].expression - aggregate[i].expression, "aggregate row lower bound")
                columns = [-sum(lower[i][j].value for i in range(k)) for j in range(count)]
                capacities = [[upper[i][j].value - lower[i][j].value for j in range(count)] for i in range(k)]
                transport, subset = _transport(rows, columns, capacities)
                if subset is not None:
                    rhs = []
                    for j in range(count):
                        upper_part = active_sum(upper[i][j] for i in subset)
                        lower_part = active_neg(active_sum(lower[i][j] for i in range(k) if i not in subset))
                        rhs.append(min((upper_part, lower_part), key=lambda a: a.value))
                    cut = active_sum(aggregate[i] for i in subset).expression - active_sum(rhs).expression
                    result = violation(cut, "transportation subset")
                    assert result is not None
                    return result
                if not decompose:
                    continue
                matrix = [[transport[i][j] + lower[i][j].value for j in range(count)] for i in range(k)]
            if decompose:
                default = tuple(matrix[i][-1] / weight_values[-1] for i in range(k)) if weight_values[-1] else tuple(a.value for a in aggregate)
                exceptions = {state: tuple(matrix[i][j] / weight_values[j] for i in range(k))
                              for j, state in enumerate(states) if weight_values[j] > 0}
                coordinates.append((default, exceptions))
        decomposition = None
        if decompose:
            weights = point.y + (F(1) - sum(point.y),)
            decomposition = CompactDecomposition(self, weights, coordinates)
        return SeparationResult(decomposition=decomposition)
