"""Targeted correctness, endpoint-domain, cap, and certificate tests."""
from copy import deepcopy
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import random
import unittest
from unittest.mock import patch

from certified_grid import BoxQP, BudgetExceeded
import submodular_recourse as backend
from verify_submodular_recourse import verify_submodular


def instance(A, b, bounds=None, integers=(), constant=0):
    return BoxQP(A, b, bounds or [(0, 1)] * len(b), integers,
                 [list(range(len(b)))], [], constant)


def fixture():
    return instance([[-2, F(-3, 2), F(-1, 2)], [F(-3, 2), -2, F(-1, 2)],
                     [F(-1, 2), F(-1, 2), 2]], [2, 2, F(-1, 2)], constant=F(1, 16))


def independent_minimum(problem):
    path = Path(__file__).resolve().parents[1] / "conditional-messages/check_mixed_submodular.py"
    spec = importlib.util.spec_from_file_location("mixed_diagnostic", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.full_face_minimum(problem.A, problem.b, problem.bounds, problem.constant)


class SubmodularRecourseTests(unittest.TestCase):
    def check(self, result, problem):
        encoded = json.loads(json.dumps(result))
        with patch.object(backend, "solve_lp", side_effect=AssertionError("LP called")), \
                patch.object(backend, "solve_convex_box_qp", side_effect=AssertionError("QP called")), \
                patch("rational_optimization.solve_lp", side_effect=AssertionError("LP called")), \
                patch("rational_optimization.solve_convex_box_qp", side_effect=AssertionError("QP called")):
            self.assertTrue(verify_submodular(encoded, problem))
        return encoded

    def test_mixture_is_constructed_without_label_enumeration(self):
        problem = fixture()
        result = backend.solve_submodular(problem, exact=True)
        self.assertEqual(result["status"], "exact")
        self.assertEqual(F(result["upper"]), 0)
        self.assertEqual(result["stats"]["queries"], 4)
        self.assertEqual(result["stats"]["cuts"], 2)
        self.assertEqual(sorted(entry["weight"] for entry in result["proof"]["mixture"]), ["1/2", "1/2"])
        self.check(result, problem)

    def test_signed_coupled_convex_block_with_permuted_concave_coordinates(self):
        # Convex block indices 0,2, with a supplied non-natural endpoint order.
        problem = instance([[4, 1, 1, -2], [1, -2, -2, 3], [1, -2, 3, 1], [-2, 3, 1, -1]],
                           [F(-2, 3), 2, -1, 1], [(-2, 3), (-1, 2), (F(1, 3), 2), (-2, 1)])
        result = backend.solve_submodular(problem, concave=(3, 1), exact=True)
        self.assertEqual(result["status"], "exact")
        self.assertEqual(result["proof"]["concave"], [3, 1])
        self.assertEqual(F(result["upper"]), independent_minimum(problem))
        self.check(result, problem)

    def test_singular_convex_block_and_fixed_positive_integer(self):
        problem = instance([[-2, -1, -1, 2], [-1, 1, -1, 3], [-1, -1, 1, -2], [2, 3, -2, 5]],
                           [1, 0, 0, -1], [(0, 1), (-1, 2), (-1, 2), (2, 2)], integers=(3,))
        result = backend.solve_submodular(problem, exact=True)
        self.assertEqual(result["status"], "exact")
        self.assertEqual(result["point"][3], "2")
        self.assertEqual(F(result["upper"]), independent_minimum(problem))
        self.check(result, problem)

    def test_native_integer_endpoints_and_arbitrary_boxes(self):
        problem = instance([[-2, 2, -1], [2, -1, 3], [-1, 3, 4]], [2, -1, F(-4, 3)],
                           [(F(-5, 2), F(7, 2)), (F(-4, 3), F(8, 3)), (-1, 2)], integers=(0, 1))
        result = backend.solve_submodular(problem, exact=True)
        self.assertEqual(result["status"], "exact")
        self.assertEqual(F(result["upper"]), independent_minimum(problem))
        for query in result["proof"]["queries"]:
            self.assertIn(F(query["point"][0]), problem.bounds[0])
            self.assertIn(F(query["point"][1]), problem.bounds[1])
        self.check(result, problem)

    def test_empty_endpoint_or_convex_block_and_fixed_model(self):
        for problem in (instance([[2, -1], [-1, 2]], [-1, -1]),
                        instance([[-2, -1], [-1, 0]], [2, -1]),
                        instance([[2, 3], [3, -1]], [5, 2], [(2, 2), (3, 3)], integers=(0,))):
            result = backend.solve_submodular(problem, exact=True)
            self.assertEqual(result["status"], "exact")
            self.assertEqual(F(result["upper"]), independent_minimum(problem))
            self.check(result, problem)

    def test_random_signed_dense_comparisons(self):
        for seed in range(18):
            rng, n = random.Random(840 + seed), 5
            signs = [rng.choice((-1, 1)) for _ in range(n)]
            A = [[F(0) for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(i):
                    A[i][j] = A[j][i] = -signs[i] * signs[j] * F(rng.randint(0, 3), 2)
            for i in range(3):
                A[i][i] = -F(rng.randint(0, 3), 2)
            for i in range(3, 5):
                A[i][i] = abs(A[3][4]) + 1
            b = [F(rng.randint(-5, 5), 3) for _ in range(n)]
            bounds = [(F(-rng.randint(0, 3), 2), F(rng.randint(1, 4), 2)) for _ in range(n)]
            problem = instance(A, b, bounds, constant=F(seed, 7))
            result = backend.solve_submodular(problem, exact=True)
            self.assertEqual(result["status"], "exact", seed)
            self.assertEqual(F(result["upper"]), independent_minimum(problem), seed)
            self.check(result, problem)

    def test_caps_keep_completed_bounds(self):
        problem = fixture()
        cases = (({"max_cuts": 0}, "cut_limit"), ({"max_cuts": 1}, "cut_limit"),
                 ({"max_queries": 0}, "query_limit"), ({"max_queries": 2}, "query_limit"),
                 ({"max_queries": 3}, "query_limit"), ({"max_faces": 0}, "qp_max_faces"),
                 ({"max_pivots": 0}, "lp_pivot_limit"), ({"time_limit": 0}, "time_limit"))
        for options, reason in cases:
            result = backend.solve_submodular(problem, exact=True, **options)
            self.assertEqual(result["status"], "resource_limit", options)
            self.assertEqual(result["reason"], reason, options)
            self.assertLessEqual(F(result["lower"]), 0)
            self.assertGreaterEqual(F(result["upper"]), 0)
            self.check(result, problem)

    def test_cooperative_interruption_after_successful_queries(self):
        problem = fixture()
        original = backend.solve_convex_box_qp
        completed = []

        def record(*args, **kwargs):
            result = original(*args, **kwargs)
            completed.append(1)
            return result

        def check():
            if len(completed) >= 2:
                raise BudgetExceeded("external_test_budget")

        with patch.object(backend, "solve_convex_box_qp", side_effect=record):
            result = backend.solve_submodular(problem, exact=True, check=check)
        self.assertEqual(result["reason"], "external_test_budget")
        self.assertEqual(len(result["proof"]["queries"]), 2)
        self.check(result, problem)

    def test_epsilon_stop_is_distinct_from_exact(self):
        problem = fixture()
        approximate = backend.solve_submodular(problem, epsilon=1, max_cuts=1)
        self.assertEqual(approximate["status"], "epsilon_optimal")
        self.assertGreater(F(approximate["gap"]), 0)
        self.check(approximate, problem)
        exact = backend.solve_submodular(problem, epsilon=1, exact=True, max_cuts=1)
        self.assertEqual(exact["status"], "resource_limit")
        self.check(exact, problem)

    def test_unsupported_models_and_invalid_options(self):
        for problem in (instance([[1, -2], [-2, 1]], [1, 1]),
                        instance([[2, -1], [-1, 2]], [-1, 1], integers=(0,)),
                        instance([[-1, 1, 1], [1, -1, 1], [1, 1, -1]], [0, 0, 0])):
            result = backend.solve_submodular(problem, exact=True)
            self.assertEqual(result["status"], "unsupported")
            self.check(result, problem)
        for options in ({"max_cuts": -1}, {"max_queries": True}, {"epsilon": -1},
                        {"time_limit": float("nan")}, {"concave": [0, 0]},
                        {"flips": {0: 1}}, {"exact": 1}):
            with self.assertRaises(ValueError, msg=str(options)):
                backend.solve_submodular(fixture(), **options)

    def test_certificate_corruptions_and_expected_model_binding(self):
        problem = fixture()
        certificate = self.check(backend.solve_submodular(problem, exact=True), problem)
        alterations = []
        item = deepcopy(certificate); item["proof"]["mixture"][0]["weight"] = "1/3"; alterations.append(item)
        item = deepcopy(certificate); item["proof"]["queries"][0]["point"][2] = "1/3"; alterations.append(item)
        item = deepcopy(certificate); item["proof"]["queries"][0]["value"] = "1"; alterations.append(item)
        item = deepcopy(certificate); item["proof"]["queries"].pop(); alterations.append(item)
        item = deepcopy(certificate); item["proof"]["flips"][0][1] = -1; alterations.append(item)
        item = deepcopy(certificate); item["proof"]["concave"].append(2); alterations.append(item)
        item = deepcopy(certificate); item["proof"]["mixture"][0]["permutation"] = [0, 0]; alterations.append(item)
        item = deepcopy(certificate); item["lower"] = "1"; alterations.append(item)
        item = deepcopy(certificate); item["problem"]["constant"] = "1"; alterations.append(item)
        for item in alterations:
            self.assertFalse(verify_submodular(item))
        changed = instance(problem.A, problem.b, constant=1)
        self.assertFalse(verify_submodular(certificate, changed))
        capped = backend.solve_submodular(problem, max_cuts=1)
        capped["status"] = "exact"
        self.assertFalse(verify_submodular(capped))


if __name__ == "__main__":
    unittest.main()
