"""Exact endpoint recourse and adaptive continuous-core search.

The residual coordinates must be coordinatewise concave and become
attractive after the supplied endpoint flips. All arithmetic is rational.
This is a reference implementation, not a general continuous-submodular
solver. See note.md for the mathematical and complexity contracts.
"""

from collections import deque
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
from math import ceil, factorial, floor, prod


@dataclass(frozen=True)
class Quadratic:
    diagonal: tuple
    linear: tuple
    edges: tuple  # (i,j,coefficient), i<j, each pair once
    constant: Q = Q(0)

    def __post_init__(self):
        n = len(self.diagonal)
        if len(self.linear) != n:
            raise ValueError("coefficient dimension mismatch")
        coefficients = (*self.diagonal, *self.linear, self.constant,
                        *(coefficient for _, _, coefficient in self.edges))
        if any(not isinstance(value, (int, Q)) for value in coefficients):
            raise ValueError("coefficients must be integers or exact Fractions")
        seen = set()
        for i, j, _ in self.edges:
            if not 0 <= i < j < n or (i, j) in seen:
                raise ValueError("edges must be unique ordered pairs")
            seen.add((i, j))

    def value(self, x):
        return self.constant + sum(
            (a * t * t + b * t for a, b, t in
             zip(self.diagonal, self.linear, x)), Q(0)
        ) + sum((c * x[i] * x[j] for i, j, c in self.edges), Q(0))


@dataclass
class Certificate:
    point: tuple
    value: Q
    flow: dict  # antisymmetric net flow; missing entries are zero
    source_side: frozenset


def detect_flips(model, core):
    """Recognize concave, sign-switchable residual structure in linear graph time.

    The proposed core is supplied. Failure says only that this residual
    does not satisfy the sufficient class; it says nothing about hardness.
    """
    core = set(core)
    n = len(model.diagonal)
    if any(i < 0 or i >= n for i in core):
        raise ValueError("invalid core index")
    residual = [i for i in range(n) if i not in core]
    if any(model.diagonal[i] > 0 for i in residual):
        raise ValueError("residual diagonal must be nonpositive")
    adjacency = {i: [] for i in residual}
    for i, j, coefficient in model.edges:
        if i in adjacency and j in adjacency and coefficient:
            relation = -1 if coefficient > 0 else 1
            adjacency[i].append((j, relation))
            adjacency[j].append((i, relation))
    flips = {}
    for root in residual:
        if root in flips:
            continue
        flips[root] = 1
        queue = deque([root])
        while queue:
            i = queue.popleft()
            for j, relation in adjacency[i]:
                required = flips[i] * relation
                if j in flips:
                    if flips[j] != required:
                        raise ValueError("residual edge signs conflict on a cycle")
                else:
                    flips[j] = required
                    queue.append(j)
    return flips


def _network(model, core_values, bounds, flips, integer_indices=()):
    """Compile the endpoint energy; return graph and its exact offset."""
    n = len(model.diagonal)
    integer_indices = set(integer_indices)
    if len(bounds) != n or any(i < 0 or i >= n for i in core_values):
        raise ValueError("invalid dimensions or core indices")
    if any(i < 0 or i >= n for i in integer_indices):
        raise ValueError("invalid integer index")
    residual = [i for i in range(n) if i not in core_values]
    if (set(flips) != set(residual)
            or any(not isinstance(s, (int, Q)) or s not in (-1, 1) for s in flips.values())):
        raise ValueError("one endpoint flip is required for each residual coordinate")
    base, step = [Q(0)] * n, [Q(0)] * n
    for i, (lo, hi) in enumerate(bounds):
        lo, hi = Q(lo), Q(hi)
        if i in integer_indices:
            lo, hi = Q(ceil(lo)), Q(floor(hi))
        if lo > hi:
            raise ValueError("empty coordinate domain")
        if i in core_values:
            base[i] = Q(core_values[i])
            if not lo <= base[i] <= hi or (i in integer_indices and base[i].denominator != 1):
                raise ValueError("infeasible core assignment")
        else:
            if model.diagonal[i] > 0:
                raise ValueError("residual diagonal must be nonpositive")
            base[i] = lo if flips[i] == 1 else hi
            step[i] = (hi - lo) * flips[i]
    position = {v: j for j, v in enumerate(residual)}
    unary = [model.diagonal[i] * (2 * base[i] * step[i] + step[i] ** 2)
             + model.linear[i] * step[i] for i in residual]
    pair = []
    for i, j, c in model.edges:
        if i in position:
            unary[position[i]] += c * step[i] * base[j]
        if j in position:
            unary[position[j]] += c * step[j] * base[i]
        if i in position and j in position:
            # Check the class even when one requested interval is a singleton.
            if c * flips[i] * flips[j] > 0:
                raise ValueError("residual edge is not attractive after flips")
            coefficient = c * step[i] * step[j]
            pair.append((position[i], position[j], coefficient))
    count = len(residual)
    source, sink = count, count + 1
    capacities = {}

    def arc(i, j, capacity):
        if capacity:
            capacities[i, j] = capacities.get((i, j), Q(0)) + capacity

    for i, j, coefficient in pair:
        unary[i] += coefficient / 2
        unary[j] += coefficient / 2
        arc(i, j, -coefficient / 2)
        arc(j, i, -coefficient / 2)
    offset = model.value(base)
    for i, coefficient in enumerate(unary):
        if coefficient >= 0:
            arc(i, sink, coefficient)
        else:
            offset += coefficient
            arc(source, i, -coefficient)
    return residual, base, step, capacities, offset, source, sink


def _maxflow(capacities, source, sink):
    """Edmonds--Karp, with an exact net-flow certificate."""
    adjacency = [set() for _ in range(sink + 1)]
    for i, j in capacities:
        adjacency[i].add(j)
        adjacency[j].add(i)
    adjacency = [sorted(row) for row in adjacency]
    flow = {}
    while True:
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            i = queue.popleft()
            for j in adjacency[i]:
                if j not in parent and capacities.get((i, j), Q(0)) - flow.get((i, j), Q(0)) > 0:
                    parent[j] = i
                    queue.append(j)
        if sink not in parent:
            return flow, frozenset(parent)
        path = []
        j = sink
        while j != source:
            i = parent[j]
            path.append((i, j))
            j = i
        amount = min(capacities.get(edge, Q(0)) - flow.get(edge, Q(0)) for edge in path)
        for i, j in path:
            flow[i, j] = flow.get((i, j), Q(0)) + amount
            flow[j, i] = flow.get((j, i), Q(0)) - amount


def solve_recourse(model, core_values, bounds, flips, integer_indices=()):
    residual, base, step, capacities, offset, source, sink = _network(
        model, core_values, bounds, flips, integer_indices
    )
    flow, source_side = _maxflow(capacities, source, sink)
    point = list(base)
    for j, i in enumerate(residual):
        point[i] += step[i] * (j in source_side)
    value = model.value(point)
    cut = sum((c for (i, j), c in capacities.items()
               if i in source_side and j not in source_side), Q(0))
    assert value == offset + cut
    return Certificate(tuple(point), value, flow, source_side)


def verify_recourse(model, core_values, bounds, flips, certificate, integer_indices=()):
    """Verify primal endpoint and dual flow evidence without running maxflow."""
    if (not isinstance(certificate.value, (int, Q))
            or any(not isinstance(value, (int, Q)) for value in certificate.point)
            or any(not isinstance(value, (int, Q)) for value in certificate.flow.values())
            or any(not isinstance(i, int) for i in certificate.source_side)
            or any(not isinstance(i, int) or not isinstance(j, int) for i, j in certificate.flow)):
        return False
    residual, base, step, capacities, offset, source, sink = _network(
        model, core_values, bounds, flips, integer_indices
    )
    side, flow = certificate.source_side, certificate.flow
    if not source in side or sink in side or any(i < 0 or i > sink for i in side):
        return False
    expected = list(base)
    for j, i in enumerate(residual):
        expected[i] += step[i] * (j in side)
    if tuple(expected) != certificate.point or model.value(expected) != certificate.value:
        return False
    edges = set(capacities) | set(flow) | {(j, i) for i, j in flow}
    balance = [Q(0)] * (sink + 1)
    for i, j in edges:
        if not (0 <= i <= sink and 0 <= j <= sink):
            return False
        amount = flow.get((i, j), Q(0))
        if amount != -flow.get((j, i), Q(0)) or amount > capacities.get((i, j), Q(0)):
            return False
        balance[i] += amount
    if any(balance[i] for i in range(source)) or balance[source] != -balance[sink]:
        return False
    cut = sum((c for (i, j), c in capacities.items() if i in side and j not in side), Q(0))
    return balance[source] == cut and offset + cut == certificate.value


def adaptive_core(model, core, bounds, flips, tolerance, max_levels=24, integer_indices=()):
    """Return a certified additive enclosure, or a bounded unfinished run.

    Core domains are [0,1] and continuous. Residual domains may be integer.
    The returned trace records every generated cell and evaluated corner;
    oracle certificates are cached and can be checked independently.
    """
    core = tuple(core)
    integer_indices = tuple(integer_indices)
    if len(set(core)) != len(core) or any(bounds[i] != (0, 1) for i in core):
        raise ValueError("core indices must be distinct with unit intervals")
    if set(core) & set(integer_indices):
        raise ValueError("the adaptive search core must be continuous")
    if tolerance <= 0 or max_levels < 0:
        raise ValueError("positive tolerance and nonnegative level limit required")
    k = len(core)
    curvature = max([Q(0)] + [2 * model.diagonal[i] for i in core])
    candidates = {tuple(0 for _ in core)}
    cache, trace = {}, []
    incumbent = None
    lower = None
    offsets = list(product((0, 1), repeat=k))
    for level in range(max_levels + 1):
        denominator = 2 ** level
        cell_values = {}
        before = len(cache)
        for cell in sorted(candidates):
            corners = [tuple(Q(i + d, denominator) for i, d in zip(cell, bits)) for bits in offsets]
            for corner in corners:
                if corner not in cache:
                    cert = solve_recourse(model, dict(zip(core, corner)), bounds, flips, integer_indices)
                    cache[corner] = cert
                    if incumbent is None or cert.value < incumbent.value:
                        incumbent = cert
            cell_values[cell] = min(cache[v].value for v in corners)
        error = Q(k) * curvature / (8 * denominator ** 2)
        level_lower = min(cell_values.values()) - error
        lower = level_lower if lower is None else max(lower, level_lower)
        retained = {cell for cell, value in cell_values.items() if value - error <= incumbent.value}
        trace.append({"level": level, "generated": len(candidates), "retained": len(retained),
                      "new_queries": len(cache) - before, "error": error,
                      "lower": lower, "upper": incumbent.value,
                      "retained_cells": sorted(retained)})
        if incumbent.value - lower <= tolerance:
            return {"complete": True, "lower": lower, "upper": incumbent.value,
                    "incumbent": incumbent, "trace": trace, "certificates": cache}
        candidates = {tuple(2 * i + d for i, d in zip(cell, bits))
                      for cell in retained for bits in offsets}
    return {"complete": False, "lower": lower, "upper": incumbent.value,
            "incumbent": incumbent, "trace": trace, "certificates": cache}


def verify_search(model, core, bounds, flips, tolerance, result, integer_indices=()):
    """Check a complete search trace without solving any optimization problem."""
    core = tuple(core)
    integer_indices = tuple(integer_indices)
    if len(set(core)) != len(core) or any(bounds[i] != (0, 1) for i in core):
        return False
    if set(core) & set(integer_indices) or tolerance <= 0:
        return False
    cache = result["certificates"]
    for corner, cert in cache.items():
        if len(corner) != len(core) or not verify_recourse(
            model, dict(zip(core, corner)), bounds, flips, cert, integer_indices
        ):
            return False
    k = len(core)
    curvature = max([Q(0)] + [2 * model.diagonal[i] for i in core])
    offsets = list(product((0, 1), repeat=k))
    candidates, seen = {tuple(0 for _ in core)}, set()
    lower, upper = None, None
    for level, row in enumerate(result["trace"]):
        if row["level"] != level or row["generated"] != len(candidates):
            return False
        cell_values = {}
        before = len(seen)
        for cell in candidates:
            corners = [tuple(Q(i + d, 2 ** level) for i, d in zip(cell, bits)) for bits in offsets]
            if any(v not in cache for v in corners):
                return False
            seen.update(corners)
            value = min(cache[v].value for v in corners)
            upper = value if upper is None else min(upper, value)
            cell_values[cell] = value
        error = Q(k) * curvature / (8 * 2 ** (2 * level))
        candidate_lower = min(cell_values.values()) - error
        lower = candidate_lower if lower is None else max(lower, candidate_lower)
        retained = {cell for cell, value in cell_values.items() if value - error <= upper}
        if (row["error"] != error or row["lower"] != lower or row["upper"] != upper
                or row["new_queries"] != len(seen) - before
                or row["retained"] != len(retained) or row["retained_cells"] != sorted(retained)):
            return False
        candidates = {tuple(2 * i + d for i, d in zip(cell, bits))
                      for cell in retained for bits in offsets}
    if not result["trace"] or set(cache) != seen:
        return False
    if result["incumbent"] not in cache.values() or result["incumbent"].value != upper:
        return False
    if result["lower"] != lower or result["upper"] != upper:
        return False
    return result["complete"] == (upper - lower <= tolerance)


def optimum_denominator_bound(model, core, bounds):
    """Conservative uniform denominator bound for endpoint-label QP optima.

    Only the core has a unit-box requirement. The bound follows from a
    minimal-face stationary point and a determinant bound; see note.md.
    """
    core = tuple(core)
    if len(set(core)) != len(core) or any(bounds[i] != (0, 1) for i in core):
        raise ValueError("core indices must be distinct with unit intervals")
    coefficients = (*model.diagonal, *model.linear, model.constant,
                    *(value for _, _, value in model.edges),
                    *(endpoint for pair in bounds for endpoint in pair))
    scale = prod(Q(value).denominator for value in coefficients) ** 3
    core_set = set(core)
    entries = [2 * model.diagonal[i] for i in core]
    entries.extend(value for i, j, value in model.edges if i in core_set and j in core_set)
    height = max([1] + [abs(Q(value) * scale) for value in entries])
    assert Q(height).denominator == 1
    determinant_bound = factorial(len(core)) * int(height) ** len(core)
    return scale * determinant_bound ** 2


def _solve_nonsingular(matrix, rhs):
    count = len(rhs)
    rows = [[Q(value) for value in row] + [Q(value)] for row, value in zip(matrix, rhs)]
    for j in range(count):
        pivot = next((i for i in range(j, count) if rows[i][j]), None)
        if pivot is None:
            return None
        rows[j], rows[pivot] = rows[pivot], rows[j]
        multiplier = rows[j][j]
        rows[j] = [value / multiplier for value in rows[j]]
        for i in range(count):
            if i != j and rows[i][j]:
                multiplier = rows[i][j]
                rows[i] = [left - multiplier * right for left, right in zip(rows[i], rows[j])]
    return tuple(row[-1] for row in rows)


def _minimize_core_faces(model, core, residual_point):
    """Enumerate 3^k core faces; residual endpoint label stays fixed."""
    k = len(core)
    positions = {i: j for j, i in enumerate(core)}
    hessian = [[Q(0)] * k for _ in range(k)]
    slope = [model.linear[i] for i in core]
    for j, i in enumerate(core):
        hessian[j][j] = 2 * model.diagonal[i]
    for left, right, coefficient in model.edges:
        if left in positions and right in positions:
            i, j = positions[left], positions[right]
            hessian[i][j] = hessian[j][i] = coefficient
        elif left in positions:
            slope[positions[left]] += coefficient * residual_point[right]
        elif right in positions:
            slope[positions[right]] += coefficient * residual_point[left]
    best_point, best_value = None, None
    for status in product((0, 1, 2), repeat=k):  # lower, free, upper
        free = [i for i, code in enumerate(status) if code == 1]
        core_point = [Q(code == 2) for code in status]
        matrix = [[hessian[i][j] for j in free] for i in free]
        rhs = [-slope[i] - sum((hessian[i][j] * core_point[j] for j in range(k) if j not in free), Q(0))
               for i in free]
        solution = _solve_nonsingular(matrix, rhs)
        if solution is None or any(value < 0 or value > 1 for value in solution):
            continue
        for i, value in zip(free, solution):
            core_point[i] = value
        point = list(residual_point)
        for i, value in zip(core, core_point):
            point[i] = value
        value = model.value(point)
        if best_value is None or value < best_value:
            best_point, best_value = tuple(point), value
    assert best_point is not None
    return best_point, best_value


def exact_core(model, core, bounds, flips, max_levels=32, integer_indices=()):
    """Bounded exact-output mode using rational value separation.

    Completion is mathematically exact; an insufficient level budget
    returns the certified unfinished additive search. Conservative value
    heights may require far more than the default level budget.
    """
    core, integer_indices = tuple(core), tuple(integer_indices)
    denominator = optimum_denominator_bound(model, core, bounds)
    tolerance = Q(1, 2 * denominator ** 2)
    search = adaptive_core(model, core, bounds, flips, tolerance,
                           max_levels=max_levels, integer_indices=integer_indices)
    result = {"complete": False, "denominator_bound": denominator, "search": search}
    if not search["complete"]:
        return result
    point, value = _minimize_core_faces(model, core, search["incumbent"].point)
    assert value <= search["upper"] and value.denominator <= denominator
    result.update(complete=True, point=point, value=value)
    return result


def verify_exact(model, core, bounds, flips, result, integer_indices=()):
    """Verify a completed exact output without face enumeration or maxflow."""
    core, integer_indices = tuple(core), tuple(integer_indices)
    if not result["complete"]:
        return False
    denominator = optimum_denominator_bound(model, core, bounds)
    if result["denominator_bound"] != denominator:
        return False
    tolerance = Q(1, 2 * denominator ** 2)
    if not verify_search(model, core, bounds, flips, tolerance, result["search"], integer_indices):
        return False
    if not result["search"]["complete"]:
        return False
    point, value = result["point"], result["value"]
    if (len(point) != len(bounds) or not isinstance(value, (int, Q))
            or any(not isinstance(t, (int, Q)) for t in point)
            or any(not lo <= t <= hi for t, (lo, hi) in zip(point, bounds))
            or any(Q(point[i]).denominator != 1 for i in integer_indices)):
        return False
    if model.value(point) != value or Q(value).denominator > denominator:
        return False
    lower, upper = result["search"]["lower"], result["search"]["upper"]
    return lower <= value <= upper and upper - lower < Q(1, denominator ** 2)
