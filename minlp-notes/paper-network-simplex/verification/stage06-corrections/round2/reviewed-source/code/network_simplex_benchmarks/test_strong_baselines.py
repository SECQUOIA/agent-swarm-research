"""Independent legacy-EF comparisons for stronger numerical baseline builders."""
from fractions import Fraction as F
import unittest
from unittest.mock import patch

import numpy as np
from scipy.optimize import OptimizeResult, linprog

from .baselines import Instance, incidence, full_ef, full_ef_membership
from .strong_baselines import optimize_ef, membership_ef, optimize_independent_states


class StrongBaselineTests(unittest.TestCase):
    def instance(self, seed, m=5):
        rng = np.random.default_rng(seed)
        # Arbitrary orientations, parallel arcs, loops, and an isolated vertex.
        arcs = [(int(rng.integers(4)), int(rng.integers(4)), int(rng.integers(1, 5))) for _ in range(7)]
        reference = np.asarray([cap/2 for _, _, cap in arcs])
        obs = [(e, j) for e in range(7) for j in range(m) if rng.random() < .3 and j % 2 == 0]
        instance = Instance(arcs, np.zeros(5), m, obs, reference)
        instance.balances = incidence(instance)@reference
        return instance, rng

    def test_optimization_preserves_all_original_y_objectives(self):
        for seed in range(20):
            instance, rng = self.instance(seed, seed % 6)
            E, m = instance.edge_count, instance.simplex_size
            objective = rng.normal(size=E+m+len(instance.observations))
            for fixed in (None, [F(1, m+2)]*m):
                legacy = full_ef(instance, objective, y_fixed=fixed)
                self.assertEqual(legacy.status, 0)
                if fixed is not None:
                    factored = optimize_independent_states(instance, objective, fixed)
                    self.assertAlmostEqual(factored.fun, legacy.fun, places=7)
                for merge in (False, True):
                    result = optimize_ef(instance, objective, y_fixed=fixed, merge=merge)
                    self.assertEqual(result.status, 0)
                    self.assertAlmostEqual(result.fun, legacy.fun, places=7)
                    self.assertAlmostEqual(float(objective@result.original_point), result.fun, places=7)
                    self.assertEqual(len(result.original_point), E+m+len(instance.observations))
                    if fixed is not None:
                        np.testing.assert_allclose(result.original_point[E:E+m], np.asarray(fixed, float), atol=1e-9)

    def test_coupled_original_rows_map_to_both_formulations(self):
        from network_simplex_compressed import CompressedNetworkSimplex
        for seed in range(8):
            instance, rng = self.instance(seed)
            E, m = instance.edge_count, instance.simplex_size
            objective = rng.normal(size=E+m+len(instance.observations))
            resource = np.r_[np.ones(E), np.zeros(m+len(instance.observations))]
            rhs = sum(instance.reference)
            results = [optimize_ef(instance, objective, [F(1, 10)]*m, merge=merge,
                                   extra_rows=[(resource, rhs)]) for merge in (False, True)]
            model = CompressedNetworkSimplex(instance.arcs, -instance.balances, m, instance.observations)
            model.ub.append(({i: F(1) for i in range(E)}, F(str(rhs))))
            independent = model.optimize(objective, y_fixed=[F(1, 10)]*m)
            self.assertTrue(independent.success)
            for result in results:
                self.assertTrue(result.success)
                self.assertAlmostEqual(result.fun, independent.fun, places=7)
                self.assertLessEqual(resource@result.original_point, rhs+1e-8)

    def test_membership_zero_states_and_two_state_reduction(self):
        for seed in range(24):
            instance, rng = self.instance(seed)
            m = instance.simplex_size
            for weights in ((F(1, 2), F(1, 2), 0, 0, 0),
                            (F(1, 3), F(1, 3), 0, 0, 0),
                            (0, 0, F(1), 0, 0), (0,)*m):
                x = [F(str(v)) for v in instance.reference]
                z = [x[e]*weights[j] for e, j in instance.observations]
                for perturb in (False, True):
                    changed = list(z)
                    if perturb and changed: changed[seed % len(changed)] += F(1, 7)
                    old = full_ef_membership(instance, np.asarray(x, float), np.asarray(weights, float), np.asarray(changed, float))
                    self.assertIn(old.status, (0, 2))
                    for merge in (False, True):
                        for reduce in (False, True):
                            new = membership_ef(instance, x, weights, changed, merge=merge, two_state=reduce)
                            self.assertEqual(new.status, old.status, (seed, weights, perturb, merge, reduce))

    def test_fixed_weight_joint_lp_against_original_hull_vertices(self):
        # Four network vertices, including an independent loop; original hull
        # vertices are enumerated directly without a state-flow formulation.
        flows = np.asarray([[a, 1-a, loop] for a in (0, 1) for loop in (0, 1)])
        obs = [(0, 0), (1, 0), (2, 2), (0, 4)]
        m, E = 5, 3
        instance = Instance([(0, 1, 1), (0, 1, 1), (0, 0, 1)],
                            np.array([1., -1.]), m, obs, np.full(E, .5))
        vertices = []
        for state in range(m+1):
            y = np.eye(m+1)[state, :m]
            for flow in flows:
                vertices.append(np.r_[flow, y, [flow[e]*y[j] for e, j in obs]])
        vertices = np.asarray(vertices).T
        for seed in range(12):
            rng = np.random.default_rng(seed)
            objective = rng.normal(size=E+m+len(obs))
            for weights in ((F(1, 4), F(1, 4), 0, F(1, 4), 0),
                            (F(1, 2), 0, F(1, 2), 0, 0),
                            (0, 0, 0, 1, 0), (0,)*m):
                y = np.asarray(weights, float)
                witness = np.r_[instance.reference, y, [instance.reference[e]*y[j] for e, j in obs]]
                # Dense original x/y/z rows, including costs of unobserved labels.
                rows = rng.normal(size=(3, len(objective)))
                rhs = rows@witness + np.array([0., .05, .1])
                vertex_lp = linprog(objective@vertices,
                    A_eq=np.vstack((np.ones(vertices.shape[1]), vertices[E:E+m])),
                    b_eq=np.r_[1., y], A_ub=rows@vertices, b_ub=rhs,
                    bounds=(0., None), method='highs')
                self.assertEqual(vertex_lp.status, 0)
                for merge in (False, True):
                    result = optimize_ef(instance, objective, weights, merge=merge,
                                         extra_rows=list(zip(rows, rhs)))
                    self.assertEqual(result.status, vertex_lp.status)
                    self.assertAlmostEqual(result.fun, vertex_lp.fun, places=7)
                    p = result.original_point
                    self.assertAlmostEqual(objective@p, result.fun, places=7)
                    np.testing.assert_allclose(p[E:E+m], y, atol=1e-10)
                    self.assertTrue(np.all(rows@p <= rhs+1e-8))
                    self.assertTrue(np.all(p[:E] >= -1e-9) and np.all(p[:E] <= 1+1e-9))
                    np.testing.assert_allclose(incidence(instance)@p[:E], instance.balances, atol=1e-9)
                    self.assertEqual(full_ef_membership(instance, p[:E], p[E:E+m], p[E+m:]).status, 0)
                    labels = sorted({j for _, j in obs}) if merge else list(range(m))
                    positive = [weights[j] for j in labels]+[1-sum(weights[j] for j in labels)]
                    positive = [float(w) for w in positive if w > 0]
                    self.assertEqual(result.model_stats['variables'], E*len(positive))
                    recovered = result.x.reshape(len(positive), E)
                    self.assertTrue(np.all(recovered >= -1e-9))
                    self.assertTrue(np.all(recovered <= np.asarray(positive)[:, None]+1e-9))
                    for f, w in zip(recovered, positive):
                        np.testing.assert_allclose(incidence(instance)@f, w*instance.balances, atol=1e-9)
        # A y-only extra row must not disappear when y is substituted.
        row = np.zeros(E+m+len(obs)); row[E+3] = 1
        for merge in (False, True):
            result = optimize_ef(instance, np.zeros(len(row)), (0, 0, 0, 1, 0),
                                 merge=merge, extra_rows=[(row, F(1, 2))])
            self.assertEqual(result.status, 2)
            self.assertFalse(hasattr(result, 'original_point'))

    def test_two_state_conflicting_observations_are_infeasible(self):
        a = Instance([(0, 1, 1)], np.array([1., -1.]), 2, [(0, 0), (0, 1)], np.ones(1))
        result = membership_ef(a, [1], [F(1, 2)]*2, [F(2, 5)]*2)
        self.assertEqual(result.status, 2)
        self.assertEqual(result.model_stats['variables'], 0)

    def test_solver_failures_are_never_called_infeasible(self):
        a, _ = self.instance(1)
        with patch('network_simplex_benchmarks.strong_baselines.linprog', return_value=OptimizeResult(status=4, success=False, message='injected failure')):
            with self.assertRaises(RuntimeError):
                optimize_ef(a, np.zeros(a.edge_count+a.simplex_size+len(a.observations)))
            for merge in (False, True):
                with self.assertRaises(RuntimeError):
                    optimize_ef(a, np.zeros(a.edge_count+a.simplex_size+len(a.observations)),
                                 [F(1, 8)]*a.simplex_size, merge=merge)
            x = [F(str(v)) for v in a.reference]
            y = [F(1, 8)]*a.simplex_size
            z = [x[e]*y[j] for e, j in a.observations]
            with self.assertRaises(RuntimeError):
                membership_ef(a, x, y, z)


if __name__ == '__main__':
    unittest.main()
