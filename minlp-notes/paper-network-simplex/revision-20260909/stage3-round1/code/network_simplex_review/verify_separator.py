"""Independent audit of graph-to-cut separator (no baseline/code internals).

Run: python code/network_simplex_review/verify_separator.py
Requires numpy/scipy for an independently assembled full disaggregation LP.
LP checks are numerical; returned decomposition identities are checked exactly.
"""

import random
import sys
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from network_simplex import InfeasibleModel, NetworkSimplex, Point, UnsupportedGraph


def incidence(arcs, n):
    a = np.zeros((n, len(arcs)))
    for e, (tail, head, _) in enumerate(arcs):
        a[tail, e] -= 1
        a[head, e] += 1
    return a


def lp_membership(model, point):
    """State-flow variables only; equations assembled directly from definition."""
    edges, states = len(model.arcs), model.simplex_size + 1
    a = incidence(model.arcs, len(model.balances))
    weights = point.y + (1 - sum(point.y),)
    eq, rhs = [], []
    for state, weight in enumerate(weights):
        for node, balance in enumerate(model.balances):
            row = np.zeros(edges * states)
            row[state * edges:(state + 1) * edges] = a[node]
            eq.append(row)
            rhs.append(float(weight * balance))
    for edge, value in enumerate(point.x):
        row = np.zeros(edges * states)
        row[edge::edges] = 1
        eq.append(row)
        rhs.append(float(value))
    for (edge, state), value in point.z.items():
        row = np.zeros(edges * states)
        row[state * edges + edge] = 1
        eq.append(row)
        rhs.append(float(value))
    bounds = [(0, float(weight * u)) for weight in weights for _, _, u in model.arcs]
    result = linprog(np.zeros(edges * states), A_eq=np.array(eq), b_eq=rhs,
                     bounds=bounds, method="highs")
    assert result.status in (0, 2), result.message
    return result.success


def verify_global_cut(model, cut):
    """Maximize the cut over each simplex vertex and its entire flow polytope."""
    a = incidence(model.arcs, len(model.balances))
    for state in range(model.simplex_size + 1):
        objective = np.zeros(len(model.arcs))
        constant = cut.constant
        for key, value in cut.coefficients.items():
            if key[0] == "x":
                objective[key[1]] += float(value)
            elif key[0] == "y" and key[1] == state:
                constant += value
            elif key[0] == "z" and key[2] == state:
                objective[key[1]] += float(value)
        result = linprog(-objective, A_eq=a, b_eq=np.array(model.balances, float),
                         bounds=[(0, float(u)) for _, _, u in model.arcs], method="highs")
        assert result.success
        assert float(constant) - result.fun <= 1e-7, (cut, state, result.x)
    assert all(abs(v) <= 1 for k, v in cut.coefficients.items() if k[0] in ("x", "z")), cut


def verify_decomposition(model, point, decomposition):
    flows = {j: decomposition.flow(j) for j in decomposition.positive_states()}
    for j, flow in flows.items():
        balance = [F(0)] * len(model.balances)
        for value, (tail, head, capacity) in zip(flow, model.arcs):
            assert 0 <= value <= capacity
            balance[tail] -= value
            balance[head] += value
        assert tuple(balance) == model.balances
    for edge, value in enumerate(point.x):
        assert sum(decomposition.weights[j] * flow[edge] for j, flow in flows.items()) == value
    for (edge, state), value in point.z.items():
        assert decomposition.weights[state] * flows[state][edge] == value if state in flows else value == 0


def random_model(rng):
    """Articulated/disconnected unions of paths, bridges and loops, random directions."""
    arcs, nodes = [], 1
    for _ in range(rng.randint(1, 5)):
        if rng.random() < .15:
            nodes += 1  # New disconnected component, possibly an isolated vertex.
        start = nodes - 1
        end = nodes
        nodes += 1
        for _ in range(rng.randint(1, 7)):
            previous = start
            length = rng.randint(1, 4)
            for pos in range(length):
                target = end if pos == length - 1 else nodes
                if target == nodes:
                    nodes += 1
                tail, head = (previous, target) if rng.randrange(2) else (target, previous)
                arcs.append((tail, head, F(rng.randint(0, 12), rng.randint(1, 4))))
                previous = target
        if rng.random() < .5:
            arcs.append((end, end, F(rng.randint(0, 10))))
    flow = [u * F(rng.randint(0, 5), 5) for _, _, u in arcs]
    balance = [F(0)] * nodes
    for value, (tail, head, _) in zip(flow, arcs):
        balance[tail] -= value
        balance[head] += value
    m = rng.randint(0, 7)
    observations = [(e, j) for e in range(len(arcs)) for j in range(m) if rng.random() < .17]
    return NetworkSimplex(arcs, balance, m, observations), flow


def verify_hypersimplex(rng, reasons, repetitions=240):
    """Mixed state flows; globally check cuts exactly over all binary vertices."""
    for iteration in range(repetitions):
        k = 2 + iteration % 7
        total = rng.randint(1, k - 1)
        m = rng.randint(1, 6)
        vertices = [tuple(F(i in selected) for i in range(k))
                    for selected in combinations(range(k), total)]
        state_flows = [tuple((a + b) / 2 for a, b in zip(rng.choice(vertices), rng.choice(vertices)))
                       for _ in range(m + 1)]
        raw = [rng.randint(0, 5) for _ in range(m + 1)]
        if not sum(raw):
            raw[-1] = 1
        weights = [F(v, sum(raw)) for v in raw]
        x = tuple(sum(weight * flow[i] for weight, flow in zip(weights, state_flows)) for i in range(k))
        obs = [(i, j) for i in range(k) for j in range(m) if rng.random() < .30]
        model = NetworkSimplex([(0, 1, 1)] * k, [-total, total], m, obs)
        z = {(i, j): weights[j] * state_flows[j][i] for i, j in obs}
        variants = [Point(x, weights[:-1], z)]
        # Each alternative state observation is itself consistent with a feasible
        # state flow. Incompatibility can arise only in their aggregate coupling.
        alternate = [rng.choice(state_flows) for _ in range(m)]
        variants.append(Point(x, weights[:-1], {(i, j): weights[j] * alternate[j][i] for i, j in obs}))
        for candidate in variants:
            result = model.separate(candidate)
            assert result.feasible == lp_membership(model, candidate)
            if result.feasible:
                verify_decomposition(model, candidate, result.decomposition)
                reasons["hypersimplex feasible decomposition"] += 1
            else:
                cut = result.cut
                assert cut.evaluate(candidate) > 0
                assert all(abs(v) <= 1 for key, v in cut.coefficients.items() if key[0] in ("x", "z"))
                for state in range(m + 1):
                    for vertex in vertices:
                        graph_point = Point(vertex, tuple(F(j == state) for j in range(m)),
                                            {(i, j): vertex[i] * F(j == state) for i, j in obs})
                        assert cut.evaluate(graph_point) <= 0, cut
                reasons["hypersimplex " + cut.reason] += 1


def run(seed=972451, repetitions=120):
    rng = random.Random(seed)
    reasons = Counter()
    for _ in range(repetitions):
        model, flow = random_model(rng)
        raw = [rng.randint(0, 5) for _ in range(model.simplex_size + 1)]
        if not sum(raw):
            raw[-1] = 1
        y = tuple(F(v, sum(raw)) for v in raw[:-1])
        point = Point(tuple(flow), y, {(e, j): flow[e] * y[j] for e, j in model.observations})
        variants = [point]
        # Perturb individual products and all products. Includes zero-weight states.
        if model.observations:
            for _ in range(3):
                z = dict(point.z)
                for key in rng.sample(list(z), min(len(z), rng.randint(1, 6))):
                    z[key] += F(rng.choice([-2, -1, 1, 2]), rng.randint(1, 9))
                variants.append(Point(point.x, point.y, z))
        for candidate in variants:
            result = model.separate(candidate)
            assert result.feasible == lp_membership(model, candidate)
            assert result.feasible == model.separate(candidate, decompose=False).feasible
            if result.feasible:
                verify_decomposition(model, candidate, result.decomposition)
                reasons["feasible decomposition"] += 1
            else:
                assert result.cut.evaluate(candidate) > 0
                verify_global_cut(model, result.cut)
                reasons[result.cut.reason] += 1
        # Domain violations are tested separately: no EF with negative capacities.
        domain = [Point((-1,) + point.x[1:], y, point.z)]
        if y:
            domain.extend([Point(point.x, (-1,) + y[1:], point.z),
                           Point(point.x, (2,) + y[1:], point.z)])
        for candidate in domain:
            result = model.separate(candidate)
            assert not result.feasible and result.cut.evaluate(candidate) > 0
            verify_global_cut(model, result.cut)
            reasons[result.cut.reason] += 1
    # Forbidden biconnected block: K4. Capacity feasibility must not imply support.
    try:
        NetworkSimplex([(i, j, 1) for i in range(4) for j in range(i + 1, 4)], [0] * 4, 1, [])
    except UnsupportedGraph:
        pass
    else:
        raise AssertionError("K4 accepted")
    # A series-parallel block with nested parallel branches is also unsupported.
    nested = [(0, 1, 1), (0, 1, 1), (1, 2, 1), (1, 2, 1), (0, 2, 1)]
    try:
        NetworkSimplex(nested, [0] * 3, 1, [])
    except UnsupportedGraph:
        pass
    else:
        raise AssertionError("General series-parallel block accepted")
    for arcs, balances in [([], [1]), ([(0, 1, 1)], [-2, 2]), ([(0, 0, -1)], [0])]:
        try:
            NetworkSimplex(arcs, balances, 0, [])
        except InfeasibleModel:
            pass
        else:
            raise AssertionError("Infeasible base model accepted")
    empty = NetworkSimplex([], [0, 0], 2, [])
    result = empty.separate(Point((), (F(1, 3), F(2, 3)), {}))
    verify_decomposition(empty, Point((), (F(1, 3), F(2, 3)), {}), result.decomposition)
    bridge = NetworkSimplex([(0, 1, 2)], [-1, 1], 0, [])
    bad_balance = bridge.separate(Point((F(1, 2),), (), {}))
    assert bad_balance.cut.reason == "flow balance"
    verify_global_cut(bridge, bad_balance.cut)
    verify_hypersimplex(rng, reasons)
    print(dict(sorted(reasons.items())))
    print(f"PASS: {repetitions} random multigraphs + 240 hypersimplex models; independent EF, global cut LPs, exact vertex/decomposition checks; seed={seed}")


if __name__ == "__main__":
    run()
