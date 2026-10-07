"""Automatic boundary-face discovery, exact implicit output, and replay."""

import copy
from fractions import Fraction as F
import unittest

from certified_grid import BudgetExceeded
from polynomial_grid import PolynomialBox, PolynomialFactor, solve
from polynomial_boundary import certify_boundary, discover_boundary
from verify_polynomial_boundary import BoundaryCertificateError, verify_certificate


def square_shift(coordinate=0):
    return PolynomialFactor((coordinate,), [(1, (2,)), (-F(1, 2), (1,)), (F(1, 16), (0,))])


def quartic(coordinate=0):
    return PolynomialFactor((coordinate,), [(1, (4,)), (-1, (2,)), (F(1, 4), (0,))])


class BoundaryTests(unittest.TestCase):
    def test_negative_full_hessian_weak_derivative_reduction(self):
        problem = PolynomialBox([(0, 1), (0, F(1, 2))], [square_shift(),
                                PolynomialFactor((1,), [(1, (1,)), (-1, (2,))])])
        result = discover_boundary(problem)
        self.assertEqual(result["status"], "certified")
        cert = result["certificate"]
        self.assertEqual(cert["kind"], "strongly_convex_patch")
        self.assertEqual(cert["reductions"][0]["derivative_lower"], "0")
        checked = verify_certificate(cert, problem)
        self.assertEqual(checked["free"], (0,))
        self.assertEqual(checked["face_bounds"][1], (0, 0))
        self.assertEqual(problem.hessian([F(1, 4), 0])[1][1], -2)

    def test_irrational_optimizer_requires_actual_global_refinement(self):
        problem = PolynomialBox([(0, 1)] * 2, [quartic(),
                                PolynomialFactor((0, 1), [(1, (0, 1)), (1, (1, 2))])])
        result = discover_boundary(problem)
        self.assertEqual(result["status"], "certified")
        self.assertGreater(len(result["attempts"]), 1)
        checked = verify_certificate(result["certificate"], problem)
        lo, hi = checked["face_bounds"][0]
        self.assertLess(lo * lo, F(1, 2))
        self.assertGreater(hi * hi, F(1, 2))
        self.assertEqual(checked["face_bounds"][1], (0, 0))
        self.assertNotIn("point", checked)
        self.assertNotIn("value", checked)

    def test_sequential_reduction_and_zero_active_gradient(self):
        # y²+z(1-y) has derivative in y of ambiguous sign until z is fixed.
        problem = PolynomialBox([(0, 1)] * 3, [square_shift(),
                                PolynomialFactor((1, 2), [(1, (2, 0)), (1, (0, 1)), (-1, (1, 1))])])
        result = discover_boundary(problem)
        self.assertEqual(result["status"], "certified")
        cert = result["certificate"]
        self.assertEqual([row["coordinate"] for row in cert["reductions"]], [2, 1])
        self.assertEqual(verify_certificate(cert)["free"], (0,))
        self.assertEqual(problem.gradient([F(1, 4), 0, 0])[1], 0)

    def test_upper_boundary_and_permuted_scope(self):
        problem = PolynomialBox([(0, 1)] * 2, [square_shift(1),
                                PolynomialFactor((0,), [(1, (0,)), (-1, (1,))])],
                                bags=[(1,), (0,)], edges=[(0, 1)])
        cert = discover_boundary(problem)["certificate"]
        self.assertEqual(cert["reductions"][0]["endpoint"], "1")
        self.assertEqual(verify_certificate(cert)["face_bounds"][0], (1, 1))

    def test_native_integer_labels_are_fixed_by_global_filtering(self):
        problem = PolynomialBox([(0, 1), (0, 3)], [quartic(),
                                PolynomialFactor((1,), [(1, (2,)), (-2, (1,)), (1, (0,))])], integers=[1])
        result = discover_boundary(problem, time_limit=20)
        self.assertEqual(result["status"], "certified")
        checked = verify_certificate(result["certificate"])
        self.assertEqual(checked["face_bounds"][1], (1, 1))
        self.assertEqual(checked["free"], (0,))

    def test_exact_grid_point_does_not_need_optimal_set_isolation(self):
        problem = PolynomialBox([(0, 1), (0, 10000)], [], integers=[1])
        result = discover_boundary(problem)
        self.assertEqual(result["certificate"]["kind"], "grid_point")
        checked = verify_certificate(result["certificate"], problem)
        self.assertEqual(checked["value"], 0)
        self.assertTrue(problem.feasible(checked["point"]))

    def test_weak_reductions_preserve_one_optimizer_not_all(self):
        # x²−x/2+1/16 has a flat y direction. The weak sign safely chooses y=0.
        problem = PolynomialBox([(0, 1)] * 2, [square_shift()])
        cert = discover_boundary(problem)["certificate"]
        checked = verify_certificate(cert)
        self.assertEqual(checked["face_bounds"][1], (0, 0))
        self.assertEqual(problem.value([F(1, 4), 1]), 0)

    def test_original_binding_and_derivative_curvature_trace_corruption(self):
        problem = PolynomialBox([(0, 1), (0, F(1, 2))], [square_shift(),
                                PolynomialFactor((1,), [(1, (1,)), (-1, (2,))])])
        cert = discover_boundary(problem)["certificate"]
        mutations = [lambda c: c["reductions"][0].update(endpoint="1/2"),
                     lambda c: c["reductions"][0].update(derivative_lower="1"),
                     lambda c: c["hessian"][0].__setitem__(0, "3"),
                     lambda c: c.update(hessian_error="-1"),
                     lambda c: c.update(free=[1]),
                     lambda c: c["face_bounds"][0].__setitem__(1, "1/4"),
                     lambda c: c["grid_certificate"]["retained_bounds"][0].__setitem__(1, "1/4"),
                     lambda c: c["midpoint"].__setitem__(0, 0.5)]
        for mutate in mutations:
            bad = copy.deepcopy(cert)
            mutate(bad)
            with self.assertRaises(BoundaryCertificateError):
                verify_certificate(bad)
        different = PolynomialBox(problem.bounds, [square_shift()])
        with self.assertRaises(BoundaryCertificateError):
            verify_certificate(cert, different)

    def test_unresolved_multimodal_box_and_resource_limits(self):
        problem = PolynomialBox([(-1, 1)], [quartic()])
        result = discover_boundary(problem, max_rounds=2)
        self.assertEqual(result["status"], "inconclusive")
        self.assertEqual(result["reason"], "round_limit")
        self.assertNotIn("certificate", result)
        self.assertEqual(discover_boundary(problem, time_limit=0)["reason"], "time_limit")
        grid = solve(problem, epsilon=1)
        self.assertEqual(certify_boundary(problem, grid, time_limit=0)["reason"], "time_limit")

    def test_replay_interrupt_propagates(self):
        problem = PolynomialBox([(0, 1)] * 2, [square_shift()])
        cert = discover_boundary(problem)["certificate"]
        def stop():
            raise BudgetExceeded("test")
        with self.assertRaises(BudgetExceeded):
            verify_certificate(cert, check=stop)


if __name__ == "__main__":
    unittest.main()
