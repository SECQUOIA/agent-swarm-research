"""Full graph-to-cut and exact reconstruction checks for the fixed-state oracle."""

import random
import unittest
from fractions import Fraction as F
from itertools import product
from unittest.mock import patch

from .flat_chain import FlatChainSimplex, circuit_library, reduced_library, _reduced_bases
from .separator import Point
from . import test_separator as baseline


class FlatChainTests(unittest.TestCase):
    def assert_exact_cut(self, model, candidate, cut):
        self.assertGreater(cut.evaluate(candidate), 0)
        # Exact maximization over all original path/simplex vertices.
        paths = [(F(0),)*(2*model.gadgets)+(F(1),)]
        paths += [tuple(F(e % 2 == choice[e//2]) for e in range(2*model.gadgets))+(F(0),)
                  for choice in product((0, 1), repeat=model.gadgets)]
        for path in paths:
            for state in range(model.simplex_size+1):
                y = tuple(F(j == state) for j in range(model.simplex_size))
                vertex = Point(path, y, {(e, j): path[e]*y[j] for e, j in model.observations})
                self.assertLessEqual(cut.evaluate(vertex), 0)

    def test_reduced_bases_are_not_anchored_to_total(self):
        normals, circuits = reduced_library(3)
        self.assertEqual(len(circuits), 16)
        bases = _reduced_bases(3)
        self.assertEqual(len(bases), 105)
        for indices, inverse in bases:
            self.assertTrue(all(sum(normals[indices[i]][k]*inverse[k][j] for k in range(3)) == (i == j)
                                for i in range(3) for j in range(3)))
        # All three explicit profile coordinates must be zero, while residual
        # branch flow is 1/4. Imposing a full-profile sum on these coordinates
        # (as the obsolete unreduced basis construction did) would fail.
        model = FlatChainSimplex(2, 3, [(4, j) for j in range(3)])
        point = Point([F(1, 8)]*4+[F(3, 4)], [F(1, 6)]*3,
                      {(4, j): F(1, 6) for j in range(3)})
        result = model.separate(point)
        self.assertTrue(result.feasible)
        self.assertEqual(result.decomposition.group_profile, (0, 0, 0, F(1, 4)))
        baseline.SeparatorTests.assert_decomposition(self, model, point, result.decomposition)

    def test_few_observed_labels_need_no_library_and_share_default(self):
        for labels in ((), (2,), (2, 17)):
            observations = [(0, j) for j in labels]
            with patch('network_simplex.flat_chain.reduced_library', side_effect=AssertionError('unexpected enumeration')), \
                 patch('network_simplex.flat_chain.circuit_library', side_effect=AssertionError('historical enumeration')):
                model = FlatChainSimplex(3, 20, observations)
                x = (F(1, 4),)*6+(F(1, 2),)
                y = (F(1, 40),)*20
                point = Point(x, y, {(e, j): x[e]*y[j] for e, j in observations})
                result = model.separate(point)
            self.assertTrue(result.feasible)
            dec = result.decomposition
            self.assertEqual(len(dec.group_profile), len(labels)+1)
            self.assertTrue(all(len(row) == len(labels)+1 for row in dec.group_arc_a))
            self.assertEqual(dec.flow(0), dec.flow(19))
            self.assertEqual(len(dec.profile), 21)
            self.assertEqual(len(dec.arc_a[0]), 21)
            baseline.SeparatorTests.assert_decomposition(self, model, point, dec)

    def test_both_three_label_bypass_coefficient_repairs(self):
        cases = [
            ([F(2, 5), F(1, 10)]*3+[F(1, 2)], [F(1, 3)]*3,
             {(2*i, i): F(0) for i in range(3)}, F(1, 5), 1),
            ([F(1, 20), F(9, 20)]*3+[F(1, 2)], [F(1, 4)]*3,
             {(2*i+1, j): F(1, 20) for i, pair in enumerate(((0, 1), (0, 2), (1, 2))) for j in pair}, F(1, 20), -1)]
        for x, y, z, violation, sign in cases:
            model = FlatChainSimplex(3, 3, z)
            point = Point(x, y, z)
            result = model.separate(point)
            self.assertFalse(result.feasible)
            self.assertEqual(result.cut.evaluate(point), violation)
            self.assertEqual(result.cut.coefficients['x', 6], F(sign))
            self.assertTrue(any(('x', 2*i+1) in result.cut.coefficients for i in range(3)))
            self.assertTrue(all(abs(v) <= 1 for key, v in result.cut.coefficients.items() if key[0] in ('x', 'z')))
            self.assert_exact_cut(model, point, result.cut)
            self.assertFalse(baseline.extended_feasible(model, point))

    def test_four_label_general_library_and_nonunit_obstruction(self):
        allowed = ({0, 1, 2}, {0, 3}, {1, 3}, {2, 3})
        observations = [(2*i, j) for i, row in enumerate(allowed) for j in range(4) if j not in row]
        model = FlatChainSimplex(4, 4, observations)
        x = []
        for row in allowed:
            value = len(row)*F(1, 8)+(4-len(row))*F(1, 32)
            x.extend((value, F(1, 2)-value))
        x.append(F(1, 2))
        z = {key: F(1, 32) for key in observations}
        center = Point(x, [F(1, 4)]*4, z)
        accepted = model.separate(center)
        self.assertTrue(accepted.feasible)
        baseline.SeparatorTests.assert_decomposition(self, model, center, accepted.decomposition)
        z[0, 3] -= F(1, 10000)
        outside = Point(x, center.y, z)
        result = model.separate(outside)
        self.assertFalse(result.feasible)
        self.assert_exact_cut(model, outside, result.cut)
        self.assertEqual(abs(result.cut.coefficients['z', 0, 3]/result.cut.coefficients['z', 2, 1]), 2)

    def test_malformed_observation_shapes(self):
        for observations in (None, [None], [1], [(0,)], [(0, 0, 0)], [(True, 0)], [(0, False)], [(9, 0)], [(0, 2)]):
            with self.assertRaises(ValueError):
                FlatChainSimplex(1, 2, observations)

    def test_exact_circuit_libraries(self):
        for d, expected in ((1, 1), (2, 5), (3, 41)):
            normals, circuits = circuit_library(d)
            self.assertEqual(len(circuits), expected)
            for indices, multipliers in circuits:
                self.assertTrue(all(value > 0 for value in multipliers))
                self.assertTrue(all(sum(weight * normals[i][j] for i, weight in zip(indices, multipliers)) == 0
                                    for j in range(d)))

    def test_arbitrary_observations_and_zero_weights_against_full_ef(self):
        rng = random.Random(9072026)
        for m in (0, 1, 2, 3):
            for length in (1, 2, 5, 10):
                for trial in range(10):
                    observations = [(edge, state) for edge in range(2*length+1) for state in range(m)
                                    if rng.random() < .6]
                    model = FlatChainSimplex(length, m, observations)
                    weights = [rng.randrange(4) for _ in range(m + 1)]
                    if not any(weights):
                        weights[-1] = 1
                    weights = tuple(F(w, sum(weights)) for w in weights)
                    flows = []
                    for state in range(m + 1):
                        branch = F(rng.randrange(8), 7)
                        flow = []
                        for gadget in range(length):
                            a = branch * F(rng.randrange(6), 5)
                            flow.extend((a, branch - a))
                        flows.append(tuple(flow) + (1 - branch,))
                    x = [sum(w * flow[e] for w, flow in zip(weights, flows)) for e in range(2*length+1)]
                    z = {(e, j): weights[j] * flows[j][e] for e, j in observations}
                    point = Point(x, weights[:-1], z)
                    for perturb in (False, True):
                        candidate = point
                        if perturb and z:
                            altered = dict(z)
                            for key in rng.sample(list(z), min(2, len(z))):
                                altered[key] += rng.choice((-1, 1)) * F(1, 13)
                            candidate = Point(x, weights[:-1], altered)
                        result = model.separate(candidate)
                        self.assertEqual(result.feasible, baseline.extended_feasible(model, candidate), (m, length, trial))
                        self.assertEqual(result.feasible, model.separate(candidate, decompose=False).feasible)
                        if result.feasible:
                            baseline.SeparatorTests.assert_decomposition(self, model, candidate, result.decomposition)
                        else:
                            self.assertGreater(result.cut.evaluate(candidate), 0)
                            self.assertLessEqual(baseline.maximize_cut(model, result.cut), 1e-8)
                            self.assertTrue(all(abs(c) <= 1 for key, c in result.cut.coefficients.items()
                                                if key[0] in ("x", "z")))

    def test_shared_profile_obstruction_passes_mccormick(self):
        # Independently feasible gadget states cannot share a total branch
        # profile: w0>=.3 and w1>=.3 conflict with w0+w1+w*=.5.
        model = FlatChainSimplex(2, 2, [(0, 0), (2, 1)])
        point = Point([F(3, 10), F(1, 5)]*2 + [F(1, 2)], [F(1, 2)]*2,
                      {(0, 0): F(3, 10), (2, 1): F(3, 10)})
        for (edge, state), value in point.z.items():
            self.assertLessEqual(value, min(point.x[edge], point.y[state]))
            self.assertGreaterEqual(value, max(0, point.x[edge] + point.y[state] - 1))
        result = model.separate(point)
        self.assertFalse(result.feasible)
        self.assertEqual(result.cut.reason, "flat profile positive circuit")
        self.assertEqual(result.cut.evaluate(point), F(1, 10))
        self.assertLessEqual(baseline.maximize_cut(model, result.cut), 1e-9)

    def test_zero_row_violation(self):
        model = FlatChainSimplex(1, 1, [(0, 0)])
        point = Point([F(1, 5), F(3, 10), F(1, 2)], [F(1, 2)], {(0, 0): F(3, 10)})
        result = model.separate(point)
        self.assertEqual(result.cut.reason, "flat profile zero row")
        self.assertGreater(result.cut.evaluate(point), 0)
        self.assertLessEqual(baseline.maximize_cut(model, result.cut), 1e-9)

    def test_fractional_observation_indices_are_rejected(self):
        for observation in ((0.5, 0), (0, 0.5)):
            with self.assertRaises(ValueError):
                FlatChainSimplex(1, 1, [observation])
            with self.assertRaises(ValueError):
                baseline.NetworkSimplex([(0, 1, 1)], [-1, 1], 1, [observation])


if __name__ == "__main__":
    unittest.main()
