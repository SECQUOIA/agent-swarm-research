"""Regression tests for automatic affine recognition and proof composition."""

from copy import deepcopy
from fractions import Fraction as F
import json
import unittest
from unittest.mock import patch

from certified_grid import BoxQP
from recourse import recognize_affine, solve_with_recourse, transform, lift
from verify_recourse import verify_pipeline, verify_selector, RecourseCertificateError


def qp(A, b, bounds, integers=(), constant=0):
    n = len(b)
    return BoxQP(A, b, bounds, integers, [list(range(n))], [], constant)


def singular_example():
    # (y1+y2-z)^2 - z^2/8, z in [0,2], y in [0,1]^2.
    return qp([[F(7, 4), -2, -2], [-2, 2, 2], [-2, 2, 2]],
              [0, 0, 0], [(0, 2), (0, 1), (0, 1)])


def two_blocks():
    # -z^2/4 + 20(y1-z/2)^2 + 30(y2-(z+1)/2)^2.
    return qp([[F(49, 2), -20, -30], [-20, 40, 0], [-30, 0, 60]],
              [15, 0, -30], [(0, 1)] * 3, constant=F(15, 2))


class RecourseTests(unittest.TestCase):
    def test_singular_selector_and_rejection_of_arbitrary_central_vertex(self):
        p = singular_example()
        r = recognize_affine(p, [1, 2])
        self.assertEqual(r["status"], "affine")
        self.assertTrue(verify_selector(p, r["proof"]))
        reduced, _ = transform(p, r["proof"])
        for z in (F(0), F(1, 3), F(1), F(2)):
            x = lift(p, r["proof"], [z])
            self.assertTrue(p.feasible(x))
            self.assertEqual(p.value(x), -z * z / 8)
            self.assertEqual(p.value(x), reduced.value([z]))
        bad = deepcopy(r["proof"])
        bad["a"], bad["B"] = ["0", "1"], [["0"], ["0"]]
        with self.assertRaises(RecourseCertificateError):
            verify_selector(p, bad)

    def test_clipped_response_rejected(self):
        p = qp([[2, -2], [-2, 2]], [0, 0], [(-1, 2), (0, 1)])
        self.assertEqual(recognize_affine(p, [1])["status"], "no_affine_selector")

    def test_bound_active_response(self):
        p = qp([[-1, 1], [1, 2]], [0, 2], [(0, 1), (0, 1)])
        r = recognize_affine(p, [1])
        self.assertEqual(r["status"], "affine")
        self.assertEqual(r["proof"]["a"], ["0"])
        self.assertTrue(verify_selector(p, r["proof"]))

    def test_multiple_blocks_automatic_and_permuted(self):
        p = two_blocks()
        for order in ((0, 1, 2), (2, 0, 1), (1, 2, 0)):
            permuted = qp([[p.A[i][j] for j in order] for i in order],
                          [p.b[i] for i in order], [p.bounds[i] for i in order], constant=p.constant)
            cert = solve_with_recourse(permuted, epsilon=F(1, 100), backend="grid", max_stages=5)
            self.assertEqual(F(cert["upper"]), F(-1, 4))
            self.assertEqual(F(cert["gap"]), 0)
            self.assertGreaterEqual(cert["stats"]["removed_coordinates"], 2)
            self.assertTrue(verify_pipeline(json.loads(json.dumps(cert)), permuted)["valid"])

    def test_singular_block_automatic(self):
        p = singular_example()
        cert = solve_with_recourse(p, backend="grid", max_stages=8)
        self.assertEqual(F(cert["upper"]), F(-1, 2))
        self.assertTrue(verify_pipeline(cert, p)["valid"])
        self.assertGreaterEqual(cert["stats"]["removed_coordinates"], 2)

    def test_fixed_integer_and_continuous_elimination(self):
        p = qp([[2, 3, 4], [3, -1, 0], [4, 0, 2]], [1, 2, -2],
               [(2, 2), (0, 1), (F(1, 2), F(1, 2))], integers=[0])
        cert = solve_with_recourse(p, backend="grid")
        self.assertTrue(verify_pipeline(cert, p)["valid"])
        self.assertEqual(cert["steps"][0]["kind"], "fixed")
        all_fixed = qp([[2]], [3], [(F(1, 3), F(1, 3))])
        terminal = solve_with_recourse(all_fixed)
        self.assertEqual(terminal["status"], "exact")
        self.assertTrue(verify_pipeline(terminal, all_fixed)["valid"])

    def test_original_binding_and_tampering(self):
        p = singular_example()
        cert = solve_with_recourse(p, backend="grid")
        variants = []
        bad = deepcopy(cert); bad["point"][0] = "0"; variants.append(bad)
        bad = deepcopy(cert); bad["steps"][0]["B"][0][0] = "7"; variants.append(bad)
        bad = deepcopy(cert); bad["lower"] = "-1/4"; variants.append(bad)
        bad = deepcopy(cert); bad["exact_requested"] = True; variants.append(bad)
        bad = deepcopy(cert); bad["exact_requested"] = "false"; variants.append(bad)
        for bad in variants:
            with self.assertRaises(RecourseCertificateError):
                verify_pipeline(bad, p)
        changed = qp(p.A, [1, 0, 0], p.bounds)
        with self.assertRaises(RecourseCertificateError):
            verify_pipeline(cert, changed)

    def test_zero_time_returns_original_certified_bounds(self):
        p = singular_example()
        cert = solve_with_recourse(p, time_limit=0)
        self.assertEqual(cert["status"], "time_limit")
        self.assertTrue(verify_pipeline(cert, p)["valid"])
        for bad_time in (float("nan"), float("inf"), -1, True, "10"):
            with self.assertRaises(ValueError):
                solve_with_recourse(p, time_limit=bad_time)

    def test_exact_mode_composes_both_reduced_proof_types(self):
        p = singular_example()
        for backend in ("grid", "auto"):
            cert = solve_with_recourse(p, backend=backend, exact=True, time_limit=5)
            self.assertEqual(cert["status"], "exact")
            self.assertEqual(cert["gap"], "0")
            self.assertTrue(verify_pipeline(cert, p)["valid"])
        for exact in (False, True):
            cert = solve_with_recourse(p, backend="grid", exact=exact, warm_start=(2, 1, 1))
            self.assertTrue(verify_pipeline(cert, p)["valid"])
        rational_optimum = qp([[2]], [F(-2, 3)], [(0, 1)])
        cert = solve_with_recourse(rational_optimum, discover=False, backend="grid", exact=True)
        self.assertEqual(cert["point"], ["1/3"])
        self.assertTrue(verify_pipeline(cert, rational_optimum)["valid"])

    def test_clipped_convex_backend_original_model_exact_output(self):
        p = qp([[6, -4], [-4, 2]], [0, 0], [(0, 1)] * 2)
        cert = solve_with_recourse(p, backend="convex", blocks=[[1]], exact=True,
                                   max_stages=24, time_limit=5)
        self.assertEqual(cert["status"], "exact")
        self.assertEqual(cert["point"], ["2/3", "1"])
        self.assertEqual(F(cert["upper"]), F(-1, 3))
        self.assertEqual(cert["method"], "convex")
        self.assertTrue(verify_pipeline(cert, p)["valid"])
        with self.assertRaises(RecourseCertificateError):
            verify_pipeline(cert, p, max_table_states=1)
        changed = deepcopy(cert)
        changed["inner"]["problem"]["b"][0] = "1"
        with self.assertRaises(RecourseCertificateError):
            verify_pipeline(changed, p)

    def test_mixed_submodular_backend_and_auto_dispatch(self):
        p = qp([[2, -2], [-2, F(-1, 2)]], [0, 1], [(0, 1), (0, 2)], integers=[1])
        for backend in ("submodular", "auto"):
            cert = solve_with_recourse(p, discover=False, backend=backend, exact=True)
            self.assertEqual(cert["method"], "submodular")
            self.assertEqual(cert["status"], "exact")
            self.assertEqual(cert["point"], ["1", "2"])
            self.assertEqual(F(cert["upper"]), -2)
            self.assertTrue(verify_pipeline(cert, p)["valid"])
            changed = deepcopy(cert)
            changed["inner"]["exact_requested"] = False
            with self.assertRaises(RecourseCertificateError):
                verify_pipeline(changed, p)

    def test_forced_affine_map_skips_lp_and_leaf_discovery_stays_small(self):
        clipped = qp([[2, -2], [-2, 2]], [0, 0], [(-1, 2), (0, 1)])
        # The private optimizer is bound-active at the center, but this
        # constant response fails the KKT sign at other parameters.
        active_center = qp([[-1, -1], [-1, 2]], [0, 0], [(-4, 1), (0, 1)])
        with patch("rational_optimization.solve_lp", side_effect=AssertionError("unnecessary LP")):
            self.assertEqual(recognize_affine(clipped, [1])["status"], "no_affine_selector")
            self.assertEqual(recognize_affine(active_center, [1])["status"], "no_affine_selector")
        n, core = 17, 8
        A = [[F(0)] * n for _ in range(n)]
        A[core][core] = 2 * (n - 2)
        for i in range(n):
            if i != core:
                A[i][i] = 2
                A[core][i] = A[i][core] = -2
        p = qp(A, [0] * n, [(0, 1)] * n)
        cert = solve_with_recourse(p, backend="grid", max_candidates=32, time_limit=5)
        self.assertGreaterEqual(cert["stats"]["removed_coordinates"], 16)
        self.assertEqual(F(cert["upper"]), -1)
        self.assertEqual(F(cert["gap"]), 0)
        self.assertTrue(verify_pipeline(cert, p)["valid"])


if __name__ == "__main__":
    unittest.main()
