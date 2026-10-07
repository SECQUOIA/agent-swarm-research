"""Exact checks of point-grid DP with min-marginal interval pruning.

The two-pass junction-tree DP is the tested algorithm. Independent checks
use exhaustive finite grids and the small active-face oracle; neither is
part of the proposed optimization algorithm.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
import json

from check_core_box_bb import face_oracle, value


@dataclass
class Case:
    name: str
    a: list
    b: list
    bounds: list
    integers: set
    bags: list
    edges: list
    optimizer: tuple
    growth: F
    stages: int = 8
    curvature: F = None
    theta: F = F(1, 8)


def coordinate_grid(lo, hi, center, h, theta, integer):
    assert lo <= center <= hi
    nodes = {lo, hi, center}
    for endpoint, sign in ((lo, -1), (hi, 1)):
        point = center
        while point != endpoint:
            step = h + theta * abs(point - center)
            if integer:
                step = F(max(1, step.numerator // step.denominator))
            point += sign * min(step, abs(endpoint - point))
            nodes.add(point)
    nodes = tuple(sorted(nodes))
    lengths = [b - a for a, b in zip(nodes, nodes[1:])]
    ell = []
    for k, node in enumerate(nodes):
        adjacent = lengths[max(0, k - 1):min(k + 1, len(lengths))]
        if integer:
            adjacent = [length for length in adjacent if length > 1]
            assert node.denominator == 1
        radius = max(adjacent, default=F(0))
        assert radius <= h + theta * abs(node - center)
        ell.append(radius)
    return nodes, tuple(ell)


def check_decomposition(n, bags, edges):
    neighbors = [[] for _ in bags]
    for u, v in edges:
        neighbors[u].append(v)
        neighbors[v].append(u)
    assert len(edges) == len(bags) - 1
    seen = {0}
    order = [0]
    parents = {0: None}
    for u in order:
        for v in neighbors[u]:
            if v not in seen:
                seen.add(v)
                parents[v] = u
                order.append(v)
    assert len(seen) == len(bags)
    for i in range(n):
        containing = {t for t, bag in enumerate(bags) if i in bag}
        assert containing
        reached = {next(iter(containing))}
        pending = list(reached)
        for u in pending:
            for v in neighbors[u]:
                if v in containing and v not in reached:
                    reached.add(v)
                    pending.append(v)
        assert reached == containing
    return neighbors, parents, order


def point_grid_dp(a, b, bags, edges, grids, penalties, trace=None):
    """Return the corrected optimum, witness, and every unary min-marginal."""
    n = len(b)
    bags = [tuple(bag) for bag in bags]
    neighbors, parents, order = check_decomposition(n, bags, edges)
    home = [next(t for t, bag in enumerate(bags) if i in bag)
            for i in range(n)]
    unaries = [[] for _ in bags]
    interactions = [[] for _ in bags]
    for i, t in enumerate(home):
        unaries[t].append(i)
    for i in range(n):
        for j in range(i + 1, n):
            if a[i][j]:
                t = next(t for t, bag in enumerate(bags)
                         if i in bag and j in bag)
                interactions[t].append((i, j))

    positions = [{i: k for k, i in enumerate(bag)} for bag in bags]
    separators = {}
    projections = {}
    for u, adjacent in enumerate(neighbors):
        for v in adjacent:
            separator = tuple(sorted(set(bags[u]) & set(bags[v])))
            separators[u, v] = separator
            projections[u, v] = tuple(positions[u][i] for i in separator)

    def key(state, u, v):
        return tuple(state[k] for k in projections[u, v])

    tables = []
    for t, bag in enumerate(bags):
        local = {}
        for state in product(*(range(len(grids[i])) for i in bag)):
            x = {i: grids[i][state[k]] for k, i in enumerate(bag)}
            cost = sum((a[i][i] * x[i] ** 2 / 2 + b[i] * x[i]
                        - penalties[i][state[positions[t][i]]]
                        for i in unaries[t]), F(0))
            cost += sum((a[i][j] * x[i] * x[j]
                         for i, j in interactions[t]), F(0))
            local[state] = cost
        tables.append(local)

    messages = {}
    witnesses = {}

    def send(u, v, costs):
        message, witness = {}, {}
        for state, cost in costs.items():
            sep_state = key(state, u, v)
            if sep_state not in message or cost < message[sep_state]:
                message[sep_state] = cost
                witness[sep_state] = state
        messages[u, v] = message
        witnesses[u, v] = witness

    # Upward messages eliminate each child subtree.
    for u in reversed(order[1:]):
        parent = parents[u]
        costs = {}
        for state, local in tables[u].items():
            costs[state] = local + sum(
                (messages[v, u][key(state, u, v)]
                 for v in neighbors[u] if v != parent), F(0))
        send(u, parent, costs)

    # Downward messages supply the rest of the tree. Each full bag belief
    # then has the global min-marginal for every assignment to that bag.
    beliefs = {}
    for u in order:
        belief = {}
        for state, local in tables[u].items():
            belief[state] = local + sum(
                (messages[v, u][key(state, u, v)]
                 for v in neighbors[u]), F(0))
        beliefs[u] = belief
        for v in neighbors[u]:
            if parents.get(v) == u:
                costs = {state: cost - messages[v, u][key(state, u, v)]
                         for state, cost in belief.items()}
                send(u, v, costs)

    root_state = min(beliefs[0], key=beliefs[0].get)
    lower = beliefs[0][root_state]
    assert all(min(belief.values()) == lower for belief in beliefs.values())
    selected = {0: root_state}
    global_state = {}
    for u in order:
        state = selected[u]
        for i, index in zip(bags[u], state):
            assert i not in global_state or global_state[i] == index
            global_state[i] = index
        for v in neighbors[u]:
            if parents.get(v) == u:
                selected[v] = witnesses[v, u][key(state, u, v)]
    point = tuple(grids[i][global_state[i]] for i in range(n))
    correction = sum((penalties[i][global_state[i]] for i in range(n)), F(0))
    assert value(a, b, point) - correction == lower

    marginals = []
    for i, t in enumerate(home):
        marginal = [None] * len(grids[i])
        position = positions[t][i]
        for state, cost in beliefs[t].items():
            index = state[position]
            if marginal[index] is None or cost < marginal[index]:
                marginal[index] = cost
        assert min(marginal) == lower
        marginals.append(tuple(marginal))
    if trace is not None:
        trace.update({
            "bags": [list(bag) for bag in bags],
            "grids": [[str(x) for x in grid] for grid in grids],
            "penalties": [[str(d) for d in row] for row in penalties],
            "local_tables": [
                [{"indices": list(state), "cost": str(cost)}
                 for state, cost in table.items()] for table in tables],
            "messages": [
                {"from": u, "to": v, "separator": list(separators[u, v]),
                 "rows": [{"indices": list(state), "value": str(cost)}
                          for state, cost in message.items()]}
                for (u, v), message in sorted(messages.items())],
            "lower": str(lower),
            "minimizer": [str(x) for x in point],
            "coordinate_min_marginals": [[str(cost) for cost in row]
                                         for row in marginals],
        })
    return lower, point, tuple(marginals), sum(map(len, tables))


def brute_grid(a, b, grids, penalties):
    optimum = None
    marginals = [[None] * len(grid) for grid in grids]
    count = 0
    for state in product(*(range(len(grid)) for grid in grids)):
        count += 1
        point = tuple(grids[i][k] for i, k in enumerate(state))
        corrected = value(a, b, point) - sum(
            (penalties[i][k] for i, k in enumerate(state)), F(0))
        optimum = corrected if optimum is None else min(optimum, corrected)
        for i, k in enumerate(state):
            if marginals[i][k] is None or corrected < marginals[i][k]:
                marginals[i][k] = corrected
    return optimum, tuple(map(tuple, marginals)), count


def exact_mixed_oracle(case):
    integers = sorted(case.integers)
    best = None
    for assignment in product(*(range(int(case.bounds[i][0]),
                                      int(case.bounds[i][1]) + 1)
                                for i in integers)):
        candidate = face_oracle(case.a, case.b, case.bounds,
                                zip(integers, assignment))
        if best is None or candidate[0] < best[0]:
            best = candidate
    return best


def refine(case):
    n = len(case.b)
    s = max(hi - lo for lo, hi in case.bounds)
    curvature = case.curvature or max(F(0), max(case.a[i][i] for i in range(n)))
    theta = case.theta
    assert curvature > 0
    assert theta ** 2 <= min(F(1, 4), case.growth / (8 * curvature))
    optimum = value(case.a, case.b, case.optimizer)
    if n <= 5:
        exact, point = exact_mixed_oracle(case)
        assert exact == optimum and point == case.optimizer

    bounds = list(case.bounds)
    center = tuple(lo for lo, hi in bounds)
    upper = value(case.a, case.b, center)
    incumbent = center
    trace = []
    table_states = pruned_intervals = unit_intervals = strict_incumbent_stages = 0
    contraction_constant = max(F(1), 4 * curvature / (11 * case.growth))
    for stage in range(case.stages):
        h = s / 2 ** stage
        grids, radii = zip(*(coordinate_grid(lo, hi, center[i], h, theta,
                                             i in case.integers)
                            for i, (lo, hi) in enumerate(bounds)))
        penalties = tuple(tuple(curvature * ell ** 2 / 8 for ell in row)
                          for row in radii)
        lower, point, marginals, work = point_grid_dp(
            case.a, case.b, case.bags, case.edges, grids, penalties)
        table_states += work
        feasible_value = value(case.a, case.b, point)
        if feasible_value < upper:
            upper, incumbent = feasible_value, point
        if feasible_value > upper:
            strict_incumbent_stages += 1
        assert lower <= optimum <= upper
        correction = feasible_value - lower
        old_error = sum((a - b) ** 2 for a, b in zip(center, case.optimizer))
        error = sum((a - b) ** 2 for a, b in zip(point, case.optimizer))
        assert error <= 4 * curvature * n * h ** 2 / (15 * case.growth) + old_error / 15
        assert error <= contraction_constant * n * h ** 2
        assert correction <= 7 * curvature * n * h ** 2 / 8

        next_bounds = []
        removed_this_stage = 0
        for i, grid in enumerate(grids):
            if len(grid) == 1:
                assert marginals[i][0] <= upper
                retained = [(grid[0], grid[0])]
            else:
                retained = []
                for k, (left, right) in enumerate(zip(grid, grid[1:])):
                    if i in case.integers and right - left == 1:
                        unit_intervals += 1
                    keep = min(marginals[i][k:k + 2]) <= upper
                    if left <= case.optimizer[i] <= right:
                        assert keep
                    if keep:
                        retained.append((left, right))
                    else:
                        removed_this_stage += 1
            assert retained
            lo, hi = retained[0][0], retained[-1][1]
            assert bounds[i][0] <= lo <= case.optimizer[i] <= hi <= bounds[i][1]
            assert lo <= point[i] <= hi
            assert lo <= incumbent[i] <= hi
            if i in case.integers:
                assert lo.denominator == hi.denominator == 1
            next_bounds.append((lo, hi))

        pruned_intervals += removed_this_stage
        trace.append({
            "stage": stage,
            "h": str(h),
            "lower": str(lower),
            "upper": str(upper),
            "gap": str(upper - lower),
            "center": [str(x) for x in point],
            "center_value_above_incumbent": feasible_value > upper,
            "max_grid_nodes": max(map(len, grids)),
            "bag_table_states": work,
            "removed_intervals": removed_this_stage,
            "bounds": [[str(lo), str(hi)] for lo, hi in next_bounds],
        })
        center, bounds = point, next_bounds
        if upper == lower:
            break
    return {"case": case.name, "stages": len(trace),
            "table_states": table_states, "pruned_intervals": pruned_intervals,
            "unit_integer_intervals": unit_intervals,
            "strict_incumbent_stages": strict_incumbent_stages, "trace": trace}


def family(name, n, graph, bounds, integers, target, concave=(), stages=8):
    """Construct a known-growth family by diagonal dominance and boundary tilt."""
    a = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        a[i][i] = F(-1 if i in concave else 2)
    if graph == "fan":
        for i in range(1, n):
            a[0][i] = a[i][0] = F(1, 8 * n)
        for i in range(1, n - 1):
            a[i][i + 1] = a[i + 1][i] = F(1, 8)
        bags = [(0, i, i + 1) for i in range(1, n - 1)]
        edges = [(i, i + 1) for i in range(len(bags) - 1)]
    elif graph == "star":
        for i in range(1, n):
            a[0][i] = a[i][0] = F((-1) ** i, 8 * n)
        bags = [(0, i) for i in range(1, n)]
        edges = [(0, i) for i in range(1, len(bags))]
    else:
        for i in range(n - 1):
            a[i][i + 1] = a[i + 1][i] = F((-1) ** i, 8)
        bags = [(i, i + 1) for i in range(n - 1)]
        edges = [(i, i + 1) for i in range(len(bags) - 1)]
    gradient = [F(0)] * n
    for i in concave:
        assert bounds[i] == (F(0), F(1)) and target[i] == 0
        gradient[i] = F(2)
    b = [gradient[i] - sum(a[i][j] * target[j] for j in range(n))
         for i in range(n)]
    # Positive diagonal terms contribute d_i^2. Concave tilted terms
    # contribute 2d_i-d_i^2/2 >= 3d_i^2/2 on [0,1].
    growth = min(F(3, 2) if i in concave else F(1)
                 for i in range(n))
    growth -= max(sum(abs(a[i][j]) for j in range(n) if j != i)
                  for i in range(n)) / 2
    assert growth > 0
    return Case(name, a, b, bounds, integers, bags, edges,
                tuple(target), growth, stages)


def cases():
    unit = [(F(-1), F(1))] * 4
    yield family("continuous_path_interior", 4, "path", unit, set(),
                 (F(1, 3), F(-1, 4), F(2, 5), F(0)))
    yield family("continuous_fan_nonconvex_boundary", 4, "fan",
                 [(F(-1), F(1))] * 3 + [(F(0), F(1))], set(),
                 (F(1, 3), F(-1, 4), F(2, 5), F(0)), concave=(3,))
    yield family("mixed_path_integer_unit_cells", 4, "path",
                 [(F(-3), F(4)), (F(-1), F(1)),
                  (F(-2), F(3)), (F(0), F(1))], {0, 2},
                 (F(1), F(1, 3), F(-1), F(0)), concave=(3,), stages=10)
    yield family("all_integer_path", 3, "path",
                 [(F(-4), F(5)), (F(-3), F(3)), (F(-2), F(4))],
                 {0, 1, 2}, (F(2), F(-1), F(0)), stages=10)
    yield family("aspect_ratio_1024", 3, "path",
                 [(F(0), F(1)), (F(0), F(1, 1024)), (F(-1, 2), F(1, 2))],
                 set(), (F(1, 3), F(1, 3072), F(-1, 5)), stages=10)
    yield family("high_occurrence_nonconvex_fan", 9, "fan",
                 [(F(-1), F(1))] * 8 + [(F(0), F(1))], set(),
                 tuple([F(1, 3), F(-1, 4), F(2, 5), F(0)] * 2 + [F(0)]),
                 concave=(8,), stages=7)
    yield family("branching_high_occurrence_star", 10, "star",
                 [(F(-1), F(1))] * 10, set(),
                 tuple(F((-1) ** i, 3) for i in range(10)), stages=7)
    yield Case("empty_separator_and_singleton", [[F(2), F(0), F(0)],
               [F(0), F(2), F(0)], [F(0), F(0), F(2)]],
               [F(-2, 3), F(-1, 1536), F(-10)],
               [(F(0), F(1)), (F(0), F(1, 1024)), (F(5), F(5))],
               set(), [(0,), (1, 2)], [(0, 1)],
               (F(1, 3), F(1, 3072), F(5)), F(1), stages=10)
    # A valid loose curvature bound makes the corrected minimizer worse
    # than the saved incumbent; the next center must nevertheless survive.
    yield Case("center_worse_than_incumbent", [[F(2)]], [F(0)],
               [(F(0), F(1))], set(), [(0,)], [], (F(0),), F(1),
               stages=6, curvature=F(128), theta=F(1, 32))


def main():
    examples = list(cases())
    tiny_assignments = 0
    # Independent brute finite grids verify every min-marginal, including
    # both repeated-hub path decompositions and a branching decomposition.
    for case in examples:
        grids = []
        radii = []
        for i, (lo, hi) in enumerate(case.bounds):
            center = (lo if len(case.b) > 9 else
                      F((lo + hi) // 2) if i in case.integers else (lo + hi) / 2)
            grid, ell = coordinate_grid(lo, hi, center, hi - lo, F(1, 8),
                                        i in case.integers)
            grids.append(grid)
            radii.append(ell)
        curvature = case.curvature or max(case.a[i][i] for i in range(len(case.b)))
        penalties = [tuple(curvature * radius ** 2 / 8 for radius in ell)
                     for ell in radii]
        lower, point, marginals, _ = point_grid_dp(
            case.a, case.b, case.bags, case.edges, grids, penalties)
        brute_lower, brute_marginals, count = brute_grid(
            case.a, case.b, grids, penalties)
        assert lower == brute_lower and marginals == brute_marginals
        tiny_assignments += count

    # A complete readable table trace: two bags, one separator, and an
    # integer unit interval whose correction is zero.
    trace_a = [[F(2), F(1, 2), F(0)],
               [F(1, 2), F(2), F(-1, 4)],
               [F(0), F(-1, 4), F(-1)]]
    trace_b = [F(-2, 3), F(1, 2), F(2)]
    trace_grids = [(F(-1), F(0), F(1)), (F(-1), F(0), F(1)), (F(0), F(1))]
    trace_penalties = [(F(1, 4),) * 3, (F(1, 4),) * 3, (F(0),) * 2]
    small_trace = {"integer_coordinates": [2],
                   "hessian": [[str(x) for x in row] for row in trace_a],
                   "linear": [str(x) for x in trace_b]}
    trace_lower, _, trace_marginals, _ = point_grid_dp(
        trace_a, trace_b, [(0, 1), (1, 2)], [(0, 1)],
        trace_grids, trace_penalties, trace=small_trace)
    brute_lower, brute_marginals, count = brute_grid(
        trace_a, trace_b, trace_grids, trace_penalties)
    assert trace_lower == brute_lower and trace_marginals == brute_marginals
    tiny_assignments += count

    results = [refine(case) for case in examples]
    assert sum(result["pruned_intervals"] > 0 for result in results) >= 8
    assert any(result["unit_integer_intervals"] > 0 for result in results)
    special = next(result for result in results
                   if result["case"] == "center_worse_than_incumbent")
    assert special["trace"][2]["center"] == ["1/4"]
    assert special["trace"][2]["lower"] == "-1025/1024"
    assert special["trace"][2]["upper"] == "0"
    assert special["trace"][2]["center_value_above_incumbent"]
    print(json.dumps({
        "status": "PASS",
        "instances": len(results),
        "stages": sum(result["stages"] for result in results),
        "bag_table_states": sum(result["table_states"] for result in results),
        "pruned_intervals": sum(result["pruned_intervals"] for result in results),
        "strict_incumbent_stages": sum(result["strict_incumbent_stages"]
                                       for result in results),
        "independent_finite_grid_assignments": tiny_assignments,
        "checks": ["two-pass DP and all min-marginals vs brute finite grid",
                   "active-face mixed global oracle on all cases with n <= 5",
                   "every stage lower <= optimum <= incumbent",
                   "optimizer, saved incumbent, and next center retained in hulls",
                   "known-growth contraction and objective-gap bounds",
                   "integer unit intervals and actual interval pruning",
                   "branching, empty separators, singleton grids",
                   "corrected center worse than saved incumbent regression"],
        "small_dp_trace": small_trace,
        "results": results,
    }, indent=2))


if __name__ == "__main__":
    main()
