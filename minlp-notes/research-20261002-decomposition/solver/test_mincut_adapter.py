"""Targeted model-binding, domain, proof replay and budget tests."""

from copy import deepcopy
from fractions import Fraction as F
from itertools import product
import json
import random
import unittest
from unittest.mock import patch

from certified_grid import BoxQP
import mincut_adapter as adapter


def instance(A, b, bounds=None, integers=(), constant=0):
    n = len(b)
    return BoxQP(A, b, bounds or [(0, 1)] * n, integers, [tuple(range(n))], [], constant)


class MincutAdapterTests(unittest.TestCase):
    def check_proof(self, result, problem):
        replay = json.loads(json.dumps(result))
        with patch.object(adapter._recourse, "_maxflow", side_effect=AssertionError("optimizer called")), \
                patch.object(adapter._recourse, "_minimize_core_faces", side_effect=AssertionError("faces called")):
            self.assertTrue(adapter.verify_mincut(replay, problem))
        return replay

    def test_signed_dense_integer_residual_uses_actual_endpoints(self):
        problem = instance([[-2, 3, -4], [3, -1, 2], [-4, 2, 0]], [1, -2, F(3, 5)],
                           [(-3, 2), (F(-5, 2), F(9, 2)), (F(1, 3), F(7, 3))], integers=(1,))
        result = adapter.solve_mincut(problem, F(1, 100))
        self.assertEqual(result["core"], [])
        self.assertEqual(result["status"], "exact")
        self.assertEqual(F(result["upper"]), min(problem.value(x) for x in product(*problem.bounds)))
        self.assertEqual(result["queries"], 1)
        self.check_proof(result, problem)

    def test_frustrated_cycle_discovery_and_integer_only_failure(self):
        problem = instance([[0, 1, 1], [1, 0, 1], [1, 1, 0]], [-1, -1, -1], integers=(0, 1))
        result = adapter.solve_mincut(problem, F(1, 10), max_core=1)
        self.assertEqual(result["core"], [2])
        self.assertEqual(result["status"], "exact")
        self.assertEqual(F(result["upper"]), F(-1))
        self.check_proof(result, problem)
        integer_problem = instance(problem.A, problem.b, integers=(0, 1, 2))
        unsupported = adapter.solve_mincut(integer_problem, F(1, 10), max_core=3)
        self.assertEqual(unsupported["status"], "unsupported")
        self.check_proof(unsupported, integer_problem)

    def test_permuted_core_arbitrary_boxes_and_fixed_variables(self):
        # Independent curved core has its exact dyadic optimum at (0, 2).
        problem = instance([[2, 0, 0, 0], [0, 8, 0, 2], [0, 0, 2, 0], [0, 2, 0, -2]],
                           [0, 1, -4, -3], [(-2, 2), (F(2, 3), F(2, 3)), (1, 5), (-2, 3)],
                           integers=(3,), constant=F(2, 7))
        result = adapter.solve_mincut(problem, F(1, 256), core=(2, 1, 0), max_core=2, max_levels=10)
        self.assertEqual(result["core"], [2, 0])
        self.assertLessEqual(F(result["gap"]), F(1, 256))
        self.assertEqual(tuple(map(F, result["point"]))[:3], (F(0), F(2, 3), F(2)))
        exact = min(problem.value((F(0), F(2, 3), F(2), z)) for z in problem.bounds[3])
        self.assertEqual(F(result["upper"]), exact)
        self.check_proof(result, problem)

    def test_exact_rational_output_is_separated_without_optimizer_replay(self):
        problem = instance([[2, 0], [0, -2]], [F(-2, 3), -1], constant=F(1, 9))
        result = adapter.solve_mincut(problem, 0, exact=True, max_levels=60, max_queries=1000)
        self.assertEqual(result["status"], "exact")
        self.assertEqual(result["point"], ["1/3", "1"])
        self.assertEqual(F(result["upper"]), -2)
        self.check_proof(result, problem)

    def test_query_limits_before_and_after_first_level(self):
        problem = instance([[2]], [-1])
        no_search = adapter.solve_mincut(problem, F(1, 100000), max_queries=1)
        self.assertEqual(no_search["status"], "resource_limit")
        self.assertEqual(no_search["queries"], 0)
        self.check_proof(no_search, problem)
        limited = adapter.solve_mincut(problem, F(1, 100000), max_queries=2)
        self.assertEqual(limited["status"], "resource_limit")
        self.assertEqual(limited["queries"], 2)
        self.assertEqual(limited["reason"], "query_limit")
        self.check_proof(limited, problem)
        level_limited = adapter.solve_mincut(problem, F(1, 100000), max_levels=0)
        self.assertEqual(level_limited["reason"], "level_limit")
        self.check_proof(level_limited, problem)

    def test_budget_callback_runs_during_oracle_queries_and_propagates(self):
        problem = instance([[2]], [-1])
        queries = []
        solve_recourse = adapter._recourse.solve_recourse

        def observe(*args, **kwargs):
            queries.append(1)
            return solve_recourse(*args, **kwargs)

        def check():
            if queries:
                raise TimeoutError("external cooperative budget")

        with patch.object(adapter._recourse, "solve_recourse", side_effect=observe):
            with self.assertRaises(TimeoutError):
                adapter.solve_mincut(problem, F(1, 100), check=check)
        self.assertEqual(len(queries), 1)

    def test_fixed_positive_integer_and_empty_active_model(self):
        problem = instance([[4, 2], [2, 2]], [-3, 4], [(2, 2), (F(1, 3), F(1, 3))], integers=(0,))
        result = adapter.solve_mincut(problem, 0, exact=True)
        self.assertEqual(result["status"], "exact")
        self.assertEqual(result["core"], [])
        self.assertEqual(result["point"], ["2", "1/3"])
        self.check_proof(result, problem)
        unsupported = instance([[2]], [-1], integers=(0,))
        result = adapter.solve_mincut(unsupported, F(1, 100))
        self.assertEqual(result["status"], "unsupported")
        self.assertEqual(result["reason"], "positive_diagonal_integer_residual")
        self.check_proof(result, unsupported)

    def test_discovery_and_normalization_against_exhaustive_endpoints(self):
        for seed in range(20):
            rng, n = random.Random(seed), 5
            A = [[F(0) for _ in range(n)] for _ in range(n)]
            for i in range(n):
                A[i][i] = -F(rng.randint(0, 5), 3)
                for j in range(i):
                    A[i][j] = A[j][i] = F(rng.randint(-3, 3), 2)
            b = [F(rng.randint(-5, 5), 7) for _ in range(n)]
            bounds = [(F(-rng.randint(1, 4), 3), F(rng.randint(1, 5), 2)) for _ in range(n)]
            problem = instance(A, b, bounds, integers=(1,), constant=F(seed, 11))
            result = adapter.solve_mincut(problem, F(1, 1000), max_core=3)
            self.assertEqual(result["status"], "exact")
            self.assertEqual(F(result["upper"]), min(problem.value(x) for x in product(*problem.bounds)))
            self.check_proof(result, problem)

    def test_model_flow_trace_and_output_corruption(self):
        problem = instance([[2, -1], [-1, -2]], [-1, -1])
        result = self.check_proof(adapter.solve_mincut(problem, F(1, 20)), problem)
        corrupt = deepcopy(result)
        corrupt["problem"]["constant"] = "1"
        self.assertFalse(adapter.verify_mincut(corrupt))
        self.assertFalse(adapter.verify_mincut(result, instance(problem.A, problem.b, constant=1)))
        corrupt = deepcopy(result)
        corrupt["proof"]["search"]["trace"][0]["lower"] = "999"
        self.assertFalse(adapter.verify_mincut(corrupt))
        corrupt = deepcopy(result)
        corrupt["proof"]["search"]["certificates"][0]["flow"].append([0, 1, "1"])
        self.assertFalse(adapter.verify_mincut(corrupt))
        corrupt = deepcopy(result)
        corrupt["point"][0] = "-1"
        self.assertFalse(adapter.verify_mincut(corrupt))
        corrupt = deepcopy(result)
        corrupt["flips"][0][1] *= -1
        self.assertFalse(adapter.verify_mincut(corrupt))


if __name__ == "__main__":
    unittest.main()
