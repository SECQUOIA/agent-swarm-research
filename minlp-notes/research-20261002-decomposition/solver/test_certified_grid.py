"""Targeted observable-behavior tests for exact sparse QP certificates."""

from copy import deepcopy
from fractions import Fraction as F
from itertools import product
import json
import random
import unittest

from certified_grid import (BoxQP, BudgetExceeded, coordinate_grid, grid_dp,
                            solve)
from verify_certificate import CertificateError, verify_certificate


def brute(problem, grids, penalties):
    lower = None
    marginals = [[None] * len(row) for row in grids]
    for indices in product(*(range(len(row)) for row in grids)):
        point = tuple(grids[i][k] for i, k in enumerate(indices))
        value = problem.value(point) - sum((penalties[i][k] for i, k in enumerate(indices)), F(0))
        lower = value if lower is None else min(lower, value)
        for i, k in enumerate(indices):
            if marginals[i][k] is None or value < marginals[i][k]:
                marginals[i][k] = value
    return lower, tuple(map(tuple, marginals))


def nonconvex():
    return BoxQP([[2, -3], [-3, 2]], [0, 0], [(0, 1), (0, 1)], [], [(0, 1)], [],
                 constant=F(2, 7), name="coupled_nonconvex")


class ExactGridTests(unittest.TestCase):
    def test_branching_dp_and_all_marginals_match_exhaustive_grid(self):
        bags = [(0, 1, 2), (0, 2, 3), (0, 2, 4), (0, 1, 5)]
        edges = [(0, 1), (0, 2), (0, 3)]
        for seed in range(5):
            rng = random.Random(seed)
            A = [[F(0) for _ in range(6)] for _ in range(6)]
            for bag in bags:
                for i in bag:
                    for j in bag:
                        if i <= j:
                            A[i][j] = A[j][i] = F(rng.randint(-4, 4), 3)
            b = [F(rng.randint(-3, 3), 5) for _ in range(6)]
            problem = BoxQP(A, b, [(-1, 1)] * 6, {1, 4}, bags, edges, constant=F(7, 3))
            grids = [(F(-1), F(0), F(1))] * 6
            penalties = [tuple(max(F(0), A[i][i]) / 8 if i not in {1, 4} else F(0)
                               for _ in grids[i]) for i in range(6)]
            result = grid_dp(problem, grids, penalties)
            expected, marginals = brute(problem, grids, penalties)
            self.assertEqual(result["lower"], expected)
            self.assertEqual(result["marginals"], marginals)
            self.assertEqual(problem.value(result["point"]) - sum(
                penalties[i][grids[i].index(x)] for i, x in enumerate(result["point"])), expected)

    def test_empty_separator_and_fixed_coordinate(self):
        problem = BoxQP([[2, 0], [0, -2]], [0, 1], [(F(1, 3), F(1, 3)), (-2, 2)],
                        [], [(0,), (1,)], [(0, 1)], constant=F(2, 5))
        result = solve(problem)
        self.assertEqual(F(result["lower"]), F(result["upper"]))
        self.assertTrue(verify_certificate(result)["valid"])

    def test_integer_unit_intervals_have_zero_correction(self):
        grid, radii = coordinate_grid(F(-2), F(3), F(0), F(1, 8), F(1, 4), True)
        self.assertEqual(grid, tuple(map(F, range(-2, 4))))
        self.assertEqual(radii, (F(0),) * 6)
        problem = BoxQP([[2]], [F(-5, 2)], [(F(-5, 2), F(7, 2))], [0], [(0,)], [])
        result = solve(problem, epsilon=0, max_stages=12, convex_presolve=False)
        self.assertEqual(F(result["lower"]), F(-3, 2))
        self.assertEqual(F(result["upper"]), F(-3, 2))
        self.assertEqual(result["point"], ["1"])
        self.assertTrue(verify_certificate(result)["valid"])

    def test_one_pass_integer_and_bound_iterables_preserve_the_domain(self):
        problem = BoxQP([[2]], [-1], ((0, 1) for _ in range(1)),
                        (i for i in [0]), [(0,)], [], constant=F(1, 4))
        result = solve(problem, epsilon=0)
        self.assertEqual(problem.integers, frozenset({0}))
        self.assertEqual(F(result["lower"]), F(1, 4))
        self.assertEqual(F(result["upper"]), F(1, 4))
        self.assertIn(result["point"], [["0"], ["1"]])
        self.assertTrue(verify_certificate(result)["valid"])

    def test_nonpositive_diagonal_uses_only_endpoints(self):
        problem = BoxQP([[0, 3, 0], [3, -2, -2], [0, -2, 0]], [1, -1, 2],
                        [(-2, 3)] * 3, [], [(0, 1), (1, 2)], [(0, 1)])
        result = solve(problem, epsilon=0, convex_presolve=False)
        exact = min(problem.value(x) for x in product(*(pair for pair in problem.bounds)))
        self.assertEqual(F(result["lower"]), exact)
        self.assertEqual(F(result["upper"]), exact)
        self.assertEqual(len(result["stages"]), 1)
        self.assertTrue(all(len(row) == 2 for row in result["stages"][0]["grids"]))
        self.assertTrue(verify_certificate(result)["valid"])

    def test_convex_psd_kkt_certificate_and_rational_point(self):
        problem = BoxQP([[2, -1], [-1, 2]], [F(-1, 3), F(-1, 5)], [(-1, 1)] * 2,
                        [], [(0, 1)], [])
        result = solve(problem, epsilon=0)
        self.assertEqual(result["status"], "certified")
        self.assertEqual(result["point"], ["13/45", "11/45"])
        self.assertIn("convex", result["initial"])
        self.assertFalse(result["stages"])
        self.assertTrue(verify_certificate(result)["valid"])
        corrupt = deepcopy(result)
        corrupt["initial"]["convex"]["D"][0] = "-1"
        with self.assertRaises(CertificateError):
            verify_certificate(corrupt)

    def test_singular_psd_boundary_and_fixed_coordinates(self):
        problem = BoxQP([[2, -2, 0], [-2, 2, 0], [0, 0, 0]], [0, 0, -1],
                        [(0, 1), (0, 1), (2, 2)], [], [(0, 1), (2,)], [(0, 1)])
        result = solve(problem, epsilon=0)
        self.assertEqual(F(result["lower"]), F(-2))
        self.assertTrue(verify_certificate(result)["valid"])

    def test_original_nonconvex_objective_certified_and_pruning_replays(self):
        problem = nonconvex()
        result = solve(problem, epsilon=F(1, 1000), max_stages=24, time_limit=5)
        exact = F(-5, 7)
        self.assertLessEqual(F(result["lower"]), exact)
        self.assertGreaterEqual(F(result["upper"]), exact)
        self.assertEqual(result["status"], "certified")
        self.assertTrue(any(stage["removed_intervals"] for stage in result["stages"]))
        self.assertTrue(verify_certificate(json.loads(json.dumps(result)))["valid"])

    def test_mixed_integer_continuous_objective(self):
        # (x-y)^2 + (y-1/3)^2, x integer. Minimum at (0,1/6), value 1/18.
        problem = BoxQP([[2, -2], [-2, 4]], [0, F(-2, 3)], [(-1, 1), (-1, 1)],
                        [0], [(0, 1)], [], constant=F(1, 9))
        result = solve(problem, epsilon=F(1, 500), max_stages=30, time_limit=5)
        self.assertEqual(result["status"], "certified")
        self.assertLessEqual(F(result["lower"]), F(1, 18))
        self.assertGreaterEqual(F(result["upper"]), F(1, 18))
        self.assertTrue(verify_certificate(result)["valid"])

    def test_limit_results_keep_original_box_certificate(self):
        for options, status in [({"time_limit": 0}, "time_limit"),
                                ({"max_stages": 0}, "stage_limit"),
                                ({"max_table_states": 1}, "table_limit")]:
            result = solve(nonconvex(), epsilon=0, **options)
            self.assertEqual(result["status"], status)
            self.assertTrue(verify_certificate(result)["valid"])
        result = solve(nonconvex(), epsilon=0, max_stages=3)
        self.assertEqual(result["status"], "stage_limit")
        self.assertEqual(len(result["stages"]), 3)
        self.assertTrue(verify_certificate(result)["valid"])

    def test_adaptive_uniform_and_no_filter_ablations(self):
        for options in [dict(pruning=False), dict(grid_mode="uniform", pruning=False),
                        dict(schedule="adaptive", slope_decay_period=1)]:
            result = solve(nonconvex(), epsilon=F(1, 20), max_stages=12,
                           max_table_states=10000, time_limit=5, **options)
            self.assertEqual(result["status"], "certified")
            self.assertTrue(verify_certificate(result)["valid"])

    def test_unknown_growth_trials_restart_and_certify_a_flat_optimal_set(self):
        # Disable exact convex presolve to exercise the outer schedule itself.
        # The optimum is the entire diagonal; fixed coarse slopes stall.
        problem = BoxQP([[2, -2], [-2, 2]], [0, 0], [(-1, 1)] * 2,
                        [], [(0, 1)], [])
        result = solve(problem, epsilon=F(1, 50), max_stages=30, time_limit=2,
                       max_table_states=10000, convex_presolve=False, polish_sweeps=0)
        self.assertEqual(result["status"], "certified")
        trials = {stage["trial"] for stage in result["stages"]}
        self.assertGreater(len(trials), 1)
        self.assertTrue(all(stage["restart"] == (stage["trial_stage"] == 0)
                            for stage in result["stages"]))
        self.assertLessEqual(F(result["lower"]), 0)
        self.assertEqual(F(result["upper"]), 0)
        self.assertTrue(verify_certificate(result)["valid"])

    def test_invalid_messages_filtering_upper_and_coverage_are_rejected(self):
        problem = BoxQP([[2, -3, 0], [-3, 2, -3], [0, -3, 2]], [0, 0, 0],
                        [(0, 1)] * 3, [], [(0, 1), (1, 2)], [(0, 1)])
        result = solve(problem, max_stages=3)
        mutations = [
            lambda c: c["stages"][0]["messages"][0]["rows"][0].update(value="1000"),
            lambda c: c["stages"][0]["min_marginals"][0].__setitem__(0, "1000"),
            lambda c: c["stages"][0]["next_bounds"][0].__setitem__(0, "1/2"),
            lambda c: c["stages"][0]["grids"][0].__setitem__(0, "1/2"),
            lambda c: c.__setitem__("upper", "-1000"),
            lambda c: c["stages"][0]["messages"].pop(),
        ]
        for mutate in mutations:
            corrupted = deepcopy(result)
            mutate(corrupted)
            with self.assertRaises(CertificateError):
                verify_certificate(corrupted)

    def test_invalid_models_and_float_inputs_are_rejected(self):
        base = dict(A=[[2, 1], [1, 2]], b=[0, 0], bounds=[(-1, 1)] * 2,
                    integers=[], bags=[(0, 1)], edges=[])
        for patch in [dict(A=[[2, 1], [0, 2]]), dict(b=[0.0, 0]),
                      dict(bags=[(0,), (1,)], edges=[(0, 1)]),
                      dict(bounds=[(1, 0), (0, 1)]),
                      dict(integers=[0], bounds=[(F(1, 4), F(3, 4)), (0, 1)]),
                      dict(bags=[(0, 1), (0,), (0, 1)], edges=[(0, 1), (1, 2)])]:
            with self.assertRaises(ValueError):
                BoxQP(**(base | patch))

    def test_automatic_decomposition_roundtrips_and_matches_supplied_model(self):
        problem = BoxQP([[2, -3, 0], [-3, 2, -3], [0, -3, 2]], [0, 0, 0],
                        [(0, 1)] * 3, [])
        certificate = solve(problem, max_stages=12)
        self.assertTrue(verify_certificate(certificate)["valid"])
        self.assertEqual(max(map(len, problem.bags)), 2)
        self.assertEqual(BoxQP.from_dict(problem.to_dict()).to_dict(), problem.to_dict())
        with self.assertRaises(ValueError):
            BoxQP([[2]], [0], [(0, 1)], [], bags=[(0,)])

    def test_resource_cap_precedes_dp_table_allocation(self):
        with self.assertRaises(BudgetExceeded):
            grid_dp(nonconvex(), [(F(0), F(1))] * 2, [(F(0), F(0))] * 2,
                    max_table_states=3)


if __name__ == "__main__":
    unittest.main()
