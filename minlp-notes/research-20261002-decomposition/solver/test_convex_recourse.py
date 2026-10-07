"""Behavior and proof-integrity tests for conditional convex value factors."""

from copy import deepcopy
from fractions import Fraction as F
import json
import unittest
from unittest.mock import patch

from certified_grid import BoxQP
from convex_recourse import (ConvexRecourseError, solve_convex_recourse,
                              verify_convex_recourse)


def clipped():
    # V(z)=3z²-3z + min_[0,1] (y²+(1-4z)y), z in [0,1].
    # Conditional response is 0, 2z-1/2, 1 on three nonempty regions.
    # Its global minimum is at z=1,y=1 with value -2.
    return BoxQP([[6, -4], [-4, 2]], [-3, 1], [(0, 1)] * 2, [], [(0, 1)], [])


class ConvexRecourseTests(unittest.TestCase):
    def checked(self, problem, blocks, **options):
        proof = solve_convex_recourse(problem, blocks, **options)
        proof = json.loads(json.dumps(proof))
        with patch("convex_recourse.solve_convex_box_qp", side_effect=AssertionError("optimizer called")), \
             patch("rational_optimization.solve_lp", side_effect=AssertionError("optimizer called")):
            self.assertTrue(verify_convex_recourse(proof, problem))
        return proof

    def test_changing_active_set_and_uniform_ablation(self):
        p = clipped()
        for mode in ("geometric", "uniform"):
            proof = self.checked(p, [[1]], epsilon=F(1, 1000), max_levels=40, grid_mode=mode)
            self.assertIn(proof["status"], ("certified", "exact"))
            self.assertLessEqual(F(proof["lower"]), -2)
            self.assertGreaterEqual(F(proof["upper"]), -2)
            self.assertLessEqual(F(proof["gap"]), F(1, 1000))
            responses = [F(q["point"][0]) for q in proof["queries"]]
            self.assertIn(F(0), responses)
            self.assertIn(F(1), responses)
            self.assertTrue(any(0 < v < 1 for v in responses))

    def test_exact_interior_original_value(self):
        # (z-1/3)^2 + (y-z)^2; unique rational original optimizer.
        p = BoxQP([[4, -2], [-2, 2]], [F(-2, 3), 0], [(0, 1)] * 2,
                  [], [(0, 1)], [], F(1, 9))
        proof = self.checked(p, [[1]], exact=True, max_levels=100, time_limit=20)
        self.assertEqual(proof["status"], "exact")
        self.assertEqual(tuple(map(F, proof["point"])), (F(1, 3), F(1, 3)))
        self.assertEqual(F(proof["upper"]), 0)

    def test_native_integer_and_singular_block(self):
        # min (y1+y2-z)^2 - z² on z integer [-2,3], y in [0,1]^2.
        p = BoxQP([[0, -2, -2], [-2, 2, 2], [-2, 2, 2]], [0] * 3,
                  [(-2, 3), (0, 1), (0, 1)], [0], [(0, 1, 2)], [])
        proof = self.checked(p, [[1, 2]], epsilon=0)
        self.assertEqual(proof["status"], "exact")
        self.assertEqual(F(proof["upper"]), -8)
        self.assertEqual(F(proof["point"][0]), 3)

    def test_no_retained_variables_and_fixed_private(self):
        p = BoxQP([[2, 2], [2, 2]], [-2, -2], [(0, 1), (F(1, 4), F(1, 4))],
                  [], [(0, 1)], [])
        proof = self.checked(p, [[0, 1]], epsilon=0)
        self.assertEqual(proof["status"], "exact")
        self.assertEqual(F(proof["upper"]), -1)
        self.assertEqual(proof["stats"]["retained_variables"], 0)

    def test_multiple_scopes_and_user_decomposition(self):
        # Private y2 attaches to both z0,z1; y3 only to z1.
        p = BoxQP([[2, -1, -2, 0], [-1, 0, -1, 2], [-2, -1, 2, 0], [0, 2, 0, 0]],
                  [0, 0, 0, -1], [(0, 1)] * 4, [], [(0, 1, 2, 3)], [])
        proof = self.checked(p, [[2], [3]], epsilon=F(1, 100), max_levels=60,
                             residual_bags=[(0, 1)], residual_edges=[])
        self.assertLessEqual(F(proof["gap"]), F(1, 100))
        with self.assertRaises(ConvexRecourseError):
            solve_convex_recourse(p, [[2], [3]], residual_bags=[(0,), (1,)], residual_edges=[(0, 1)])

    def test_scalar_partition_removes_stiffness_and_rejects_tampering(self):
        # M(y1+y2-z)^2 + (y1-2z+1/2)^2 - z².
        # Its convex response changes face; no one affine map spans Z.
        for M in (1, 100):
            p = BoxQP([[2 * M + 6, -2 * M - 4, -2 * M],
                       [-2 * M - 4, 2 * M + 2, 2 * M],
                       [-2 * M, 2 * M, 2 * M]],
                      [-2, 1, 0], [(0, F(3, 4)), (0, 1), (0, 1)],
                      [], [(0, 1, 2)], [], F(1, 4))
            proof = self.checked(p, [[1, 2]], epsilon=F(1, 1000), max_levels=60)
            optimum = F(-(8 * M + 9), 16 * (M + 1))
            self.assertLessEqual(F(proof["lower"]), optimum)
            self.assertGreaterEqual(F(proof["upper"]), optimum)
            self.assertLessEqual(F(proof["gap"]), F(1, 1000))
            self.assertEqual(len(proof["curvature_proofs"]), 1)
            pieces = proof["curvature_proofs"][0]["pieces"]
            self.assertEqual(p.A[0][0] + max(2 * F(piece["value"][2]) for piece in pieces), 6)
            bad = deepcopy(proof)
            bad["curvature_proofs"][0]["pieces"].pop()
            with self.assertRaises(ConvexRecourseError):
                verify_convex_recourse(bad, p)
            bad = deepcopy(proof)
            bad["curvature_proofs"].append(deepcopy(bad["curvature_proofs"][0]))
            with self.assertRaises(ConvexRecourseError):
                verify_convex_recourse(bad, p)
            untightened = self.checked(p, [[1, 2]], epsilon=F(1, 1000), max_levels=2,
                                      scalar_curvature=False)
            self.assertFalse(untightened["curvature_proofs"])

    def test_resource_limits_keep_original_bounds(self):
        p = clipped()
        cases = (({"max_levels": 0}, "level_limit"),
                 ({"max_table_states": 1}, "table_limit"),
                 ({"max_faces": 0}, "oracle_limit"),
                 ({"time_limit": 0}, "time_limit"))
        for kwargs, status in cases:
            proof = self.checked(p, [[1]], **kwargs)
            self.assertEqual(proof["status"], status)
            self.assertLessEqual(F(proof["lower"]), -2)
            self.assertGreaterEqual(F(proof["upper"]), -2)

    def test_missing_or_altered_proofs_rejected(self):
        p = clipped()
        good = self.checked(p, [[1]], epsilon=F(1, 100))
        variants = []
        bad = deepcopy(good); bad["queries"][0]["value"] = "-100"; variants.append(bad)
        bad = deepcopy(good); bad["queries"][0]["lower_multipliers"][0] = "-1"; variants.append(bad)
        bad = deepcopy(good); bad["queries"].pop(0); variants.append(bad)
        bad = deepcopy(good); bad["stages"][0]["grid_minimum"] = "-100"; variants.append(bad)
        bad = deepcopy(good); bad["lower"] = "100"; variants.append(bad)
        bad = deepcopy(good); bad["retained"] = [1]; variants.append(bad)
        for bad in variants:
            with self.assertRaises(ConvexRecourseError):
                verify_convex_recourse(bad, p)
        other = BoxQP(p.A, [0, 0], p.bounds, p.integers, p.bags, p.edges)
        with self.assertRaises(ConvexRecourseError):
            verify_convex_recourse(good, other)

    def test_invalid_block_structure(self):
        p = clipped()
        for blocks in ([[0, 1]], [[1], [1]], [[5]], [[]]):
            with self.assertRaises(ConvexRecourseError):
                solve_convex_recourse(p, blocks)
        p = BoxQP([[2, 1], [1, 2]], [0, 0], [(0, 1)] * 2, [], [(0, 1)], [])
        with self.assertRaises(ConvexRecourseError):
            solve_convex_recourse(p, [[0], [1]])


if __name__ == "__main__":
    unittest.main()
