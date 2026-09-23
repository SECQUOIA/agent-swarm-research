"""Graph-to-cut contracts against independent original-state flow LPs.

Run: PYTHONPATH=code python -m unittest network_simplex.test_separator -v
SciPy is used only for the independent test oracle, never by the separator.
"""

import random
import unittest
from fractions import Fraction as F

import numpy as np
from scipy.optimize import linprog

from .separator import InfeasibleModel, NetworkSimplex, Point, UnsupportedGraph


def extended_feasible(model, point):
    """Keep every arc and every original simplex state; no block coordinates."""
    edges, states = len(model.arcs), model.simplex_size + 1
    weights = point.y + (1 - sum(point.y),)
    rows, rhs = [], []
    for edge in range(edges):
        row = np.zeros(edges * states)
        row[edge::edges] = 1
        rows.append(row)
        rhs.append(float(point.x[edge]))
    for state in range(states):
        for node, balance in enumerate(model.balances):
            row = np.zeros(edges * states)
            for edge, (a, b, _) in enumerate(model.arcs):
                row[state * edges + edge] = (b == node) - (a == node)
            rows.append(row)
            rhs.append(float(weights[state] * balance))
    bounds = [(0, float(weights[state] * cap)) for state in range(states)
              for _, _, cap in model.arcs]
    for (edge, state), z in point.z.items():
        bounds[state * edges + edge] = (float(z), float(z))
    # Observation bounds must also retain the original scaled capacities.
    if any(z < 0 or z > weights[j] * model.arcs[e][2] for (e, j), z in point.z.items()):
        return False
    answer = linprog(np.zeros(edges * states), A_eq=np.array(rows), b_eq=rhs,
                     bounds=bounds, method="highs")
    if answer.status not in (0, 2):
        raise AssertionError(answer.message)
    return answer.success


def maximize_cut(model, cut):
    """Maximize over each simplex vertex and the full original flow polytope."""
    incidence = np.zeros((len(model.balances), len(model.arcs)))
    for edge, (a, b, _) in enumerate(model.arcs):
        incidence[a, edge] -= 1
        incidence[b, edge] += 1
    maximum = -float("inf")
    for state in range(model.simplex_size + 1):
        objective = np.zeros(len(model.arcs))
        constant = float(cut.constant)
        for key, value in cut.coefficients.items():
            if key[0] == "x":
                objective[key[1]] += float(value)
            elif key[0] == "y" and key[1] == state:
                constant += float(value)
            elif key[0] == "z" and key[2] == state:
                objective[key[1]] += float(value)
        answer = linprog(-objective, A_eq=incidence, b_eq=list(map(float, model.balances)),
                         bounds=[(0, float(u)) for _, _, u in model.arcs], method="highs")
        if not answer.success:
            raise AssertionError(answer.message)
        maximum = max(maximum, constant - answer.fun)
    return maximum


def generated_case(rng, k, states=4):
    """A large path block, a cycle, a bridge, a loop, and an isolated node."""
    arcs, base, blocks = [], [], []
    next_node = 1
    anchor = 0
    for path_count in (k, 2):
        target = next_node
        next_node += 1
        paths = []
        for _ in range(path_count):
            internal = list(range(next_node, next_node + rng.randrange(3)))
            next_node += len(internal)
            nodes = [anchor] + internal + [target]
            path = []
            for a, b in zip(nodes, nodes[1:]):
                sign = rng.choice((-1, 1))
                if sign < 0:
                    a, b = b, a
                flow = rng.randrange(2, 5)
                path.append((len(arcs), sign))
                arcs.append((a, b, flow + 4))
                base.append(F(flow))
            paths.append(path)
        blocks.append(paths)
        anchor = target
    arcs.append((anchor, next_node, 3))
    base.append(F(2))
    next_node += 1
    loop = len(arcs)
    arcs.append((0, 0, 5))
    base.append(F(2))
    balances = [F(0)] * (next_node + 1)
    for (a, b, _), flow in zip(arcs, base):
        balances[a] -= flow
        balances[b] += flow
    weights = [rng.randrange(4) for _ in range(states + 1)]
    if not sum(weights):
        weights[-1] = 1
    weights = [F(w, sum(weights)) for w in weights]
    flows = []
    for _ in weights:
        flow = list(base)
        for paths in blocks:
            deviations = [0] * len(paths)
            first, second = rng.sample(range(len(paths)), 2)
            deviations[first], deviations[second] = 1, -1
            for path, deviation in zip(paths, deviations):
                for edge, sign in path:
                    flow[edge] += sign * deviation
        flow[loop] += rng.choice((-1, 0, 1))
        flows.append(flow)
    observations = [(e, j) for e in range(len(arcs)) for j in range(states)
                    if rng.random() < .4]
    model = NetworkSimplex(arcs, balances, states, observations)
    point = Point([sum(w * f[e] for w, f in zip(weights, flows)) for e in range(len(arcs))],
                  weights[:-1], {(e, j): weights[j] * flows[j][e] for e, j in observations})
    return model, point


class SeparatorTests(unittest.TestCase):
    def assert_decomposition(self, model, point, decomposition):
        combined = [F(0)] * len(model.arcs)
        for state in decomposition.positive_states():
            weight, flow = decomposition.weights[state], decomposition.flow(state)
            balance = [F(0)] * len(model.balances)
            for edge, ((a, b, capacity), value) in enumerate(zip(model.arcs, flow)):
                self.assertGreaterEqual(value, 0)
                self.assertLessEqual(value, capacity)
                balance[a] -= value
                balance[b] += value
                combined[edge] += weight * value
                if (edge, state) in point.z:
                    self.assertEqual(weight * value, point.z[edge, state])
            self.assertEqual(tuple(balance), model.balances)
        self.assertEqual(tuple(combined), point.x)

    def test_joint_state_cut(self):
        model = NetworkSimplex([(0, 1, 1)] * 3, [-1, 1], 2,
                               [(e, j) for e in range(2) for j in range(2)])
        point = Point([F(1, 3)] * 3, [F(1, 3)] * 2, {o: 0 for o in model.observations})
        result = model.separate(point)
        self.assertFalse(result.feasible)
        self.assertEqual(result.cut.evaluate(point), F(1, 3))
        self.assertLessEqual(maximize_cut(model, result.cut), 1e-9)

    def test_graph_cases_against_full_extended_hull(self):
        rng = random.Random(83117)
        accepted, rejected, reasons = 0, 0, set()
        for k in (2, 3, 4, 6):
            for trial in range(20):
                model, point = generated_case(rng, k)
                for original in (True, False):
                    candidate = point
                    if not original and point.z:
                        z = dict(point.z)
                        for key in rng.sample(list(z), min(4, len(z))):
                            z[key] += rng.choice((-1, 1)) * F(1, 7)
                        candidate = Point(point.x, point.y, z)
                    result = model.separate(candidate)
                    self.assertEqual(result.feasible, extended_feasible(model, candidate), (k, trial))
                    self.assertEqual(result.feasible, model.separate(candidate, decompose=False).feasible)
                    if result.feasible:
                        accepted += 1
                        self.assert_decomposition(model, candidate, result.decomposition)
                    else:
                        rejected += 1
                        reasons.add(result.cut.reason)
                        self.assertGreater(result.cut.evaluate(candidate), 0)
                        self.assertLessEqual(maximize_cut(model, result.cut), 1e-8, result.cut)
                        self.assertTrue(all(abs(c) <= 1 for key, c in result.cut.coefficients.items()
                                            if key[0] in ("x", "z")))
        self.assertGreaterEqual(accepted, 80)
        self.assertGreater(rejected, 30)

    def test_transportation_subset_obstruction(self):
        # Four paths force the general max-flow branch; two states cannot both
        # occupy paths 2/3 because their aggregate capacity is insufficient.
        model = NetworkSimplex([(0, 1, 1)] * 4, [-1, 1], 2,
                               [(e, j) for e in (0, 1) for j in (0, 1)])
        point = Point([F(1, 4)] * 4, [F(1, 3)] * 2, {o: 0 for o in model.observations})
        result = model.separate(point)
        self.assertFalse(result.feasible)
        self.assertEqual(result.cut.reason, "transportation subset")
        self.assertLessEqual(maximize_cut(model, result.cut), 1e-9)

    def test_zero_weights_fixed_arcs_and_no_observations(self):
        model = NetworkSimplex([(0, 1, 0), (0, 1, 1), (1, 1, 0)], [-1, 1], 2,
                               [(0, 0), (1, 0), (1, 1)])
        point = Point([0, 1, 0], [0, 1], {(0, 0): 0, (1, 0): 0, (1, 1): 1})
        result = model.separate(point)
        self.assertTrue(result.feasible)
        self.assert_decomposition(model, point, result.decomposition)
        empty = NetworkSimplex([], [0, 0], 0, [])
        self.assertTrue(empty.separate(Point([], [], {})).feasible)
        model = NetworkSimplex([(0, 1, 2)] * 5, [-1, 1], 2, [])
        point = Point([F(1, 5)] * 5, [F(1, 3), F(1, 4)], {})
        result = model.separate(point)
        self.assert_decomposition(model, point, result.decomposition)

    def test_bad_models_and_original_constraints(self):
        with self.assertRaises(InfeasibleModel):
            NetworkSimplex([(0, 1, 1)], [-2, 2], 0, [])
        with self.assertRaises(InfeasibleModel):
            NetworkSimplex([], [1, -1], 0, [])
        with self.assertRaises(UnsupportedGraph):
            NetworkSimplex([(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 0, 1),
                            (0, 2, 1), (1, 3, 1)], [0] * 4, 0, [])
        model = NetworkSimplex([(0, 1, 2)], [-1, 1], 1, [(0, 0)])
        for point, reason in [(Point([3], [0], {(0, 0): 0}), "flow bound"),
                              (Point([0], [0], {(0, 0): 0}), "flow balance"),
                              (Point([1], [-1], {(0, 0): 0}), "simplex nonnegativity"),
                              (Point([1], [2], {(0, 0): 0}), "simplex total weight"),
                              (Point([1], [F(1, 2)], {(0, 0): 0}), "bridge observation")]:
            result = model.separate(point)
            self.assertEqual(result.cut.reason, reason)
            self.assertGreater(result.cut.evaluate(point), 0)
            self.assertLessEqual(maximize_cut(model, result.cut), 1e-9)

    def test_deep_graph_preprocessing_is_iterative(self):
        n = 1500
        model = NetworkSimplex([(i, i + 1, 1) for i in range(n)], [-1] + [0] * (n - 1) + [1], 0, [])
        self.assertTrue(model.separate(Point([1] * n, [], {})).feasible)


if __name__ == "__main__":
    unittest.main()
