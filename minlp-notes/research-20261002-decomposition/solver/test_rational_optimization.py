"""Observable exact-oracle contracts and degenerate regression cases."""
from dataclasses import replace
from fractions import Fraction as F
import random
import unittest
from unittest.mock import patch

from rational_optimization import (LPResult, QPResult, solve_lp, verify_lp_result,
                                   solve_convex_box_qp, verify_convex_box_qp_result,
                                   is_psd, solve_nonsingular)


class LPTests(unittest.TestCase):
    def check_lp(self, c, status="optimal", **kwargs):
        result = solve_lp(c, **kwargs)
        self.assertEqual(result.status, status, result)
        self.assertTrue(verify_lp_result(c, result, **kwargs))
        return result

    def test_free_variables_rational_negative_rhs(self):
        r = self.check_lp([1, -2], A_ub=[[1, 1], [-2, 1]], b_ub=[F(1, 3), -1],
                          bounds=[(-2, 2), (-2, 2)])
        self.assertEqual(r.x, (F(4, 9), F(-1, 9)))
        self.assertEqual(r.value, F(2, 3))

    def test_redundant_equalities_and_singular_stationarity(self):
        r = self.check_lp([0, 0], A_eq=[[1, 1], [2, 2], [0, 0]], b_eq=[1, 2, 0],
                          bounds=[(0, 1)] * 2)
        self.assertEqual(sum(r.x), 1)

    def test_infeasible_equality_and_bounds_have_farkas_witness(self):
        for kwargs in ({"A_eq": [[1], [2]], "b_eq": [1, 3]},
                       {"bounds": [(2, 1)]},
                       {"A_ub": [[0]], "b_ub": [-1]}):
            self.check_lp([0], status="infeasible", **kwargs)

    def test_unbounded_has_feasible_origin_and_improving_ray(self):
        r = self.check_lp([-1, 0], status="unbounded", A_eq=[[1, -1]], b_eq=[F(1, 7)])
        self.assertEqual(r.certificate["ray"][0], r.certificate["ray"][1])
        self.assertGreater(r.certificate["ray"][0], 0)

    def test_blands_rule_terminates_classical_cycling_example(self):
        r = self.check_lp([-10, 57, 9, 24],
                          A_ub=[[F(1, 2), F(-11, 2), F(-5, 2), 9],
                                [F(1, 2), F(-3, 2), F(-1, 2), 1], [1, 0, 0, 0]],
                          b_ub=[0, 0, 1], bounds=[(0, None)] * 4)
        self.assertEqual(r.value, -1)
        self.assertLess(r.pivots, 100)

    def test_empty_dimension_and_no_constraints(self):
        self.assertEqual(self.check_lp([]).value, 0)
        self.check_lp([], A_eq=[[]], b_eq=[1], status="infeasible")
        self.check_lp([0])
        self.check_lp([1], status="unbounded")

    def test_resource_limits_and_callback_do_not_claim_infeasibility(self):
        r = solve_lp([1], bounds=[(1, 2)], max_pivots=0)
        self.assertEqual((r.status, r.reason, r.pivots), ("limit", "max_pivots", 0))
        self.assertFalse(verify_lp_result([1], r, bounds=[(1, 2)]))
        def stop():
            raise TimeoutError("shared budget")
        with self.assertRaises(TimeoutError):
            solve_lp([1], bounds=[(1, 2)], check=stop)

    def test_tampered_and_malformed_certificates_rejected_without_optimizer(self):
        r = self.check_lp([1], bounds=[(1, 2)])
        with patch("rational_optimization.solve_lp", side_effect=AssertionError("optimizer called")):
            self.assertTrue(verify_lp_result([1], r, bounds=[(1, 2)]))
            self.assertFalse(verify_lp_result([1], replace(r, value=F(2)), bounds=[(1, 2)]))
            self.assertFalse(verify_lp_result([1], replace(r, certificate={}), bounds=[(1, 2)]))
            cert = dict(r.certificate, inequality_multipliers=(-1, 0))
            self.assertFalse(verify_lp_result([1], replace(r, certificate=cert), bounds=[(1, 2)]))
        u = solve_lp([-1])
        self.assertFalse(verify_lp_result([-1], replace(u, certificate={"ray": [0]})))
        self.assertFalse(verify_lp_result([1], LPResult("infeasible", certificate={"ray": [1]})))

    def test_exact_input_contract(self):
        with self.assertRaises(ValueError):
            solve_lp([0.1])
        with self.assertRaises(ValueError):
            solve_lp([1], A_eq=[[1, 2]], b_eq=[1])
        with self.assertRaises(ValueError):
            solve_lp([1], max_pivots=True)


class LinearAlgebraTests(unittest.TestCase):
    def test_exact_square_solve_and_singularity_contract(self):
        self.assertEqual(solve_nonsingular([[0, 2], [3, 1]], [1, 2]), (F(1, 2), F(1, 2)))
        self.assertIsNone(solve_nonsingular([[1, 1], [2, 2]], [1, 2]))
        self.assertIsNone(solve_nonsingular([[1, 1], [2, 2]], [1, 3]))
        self.assertEqual(solve_nonsingular([], []), ())
        with self.assertRaises(ValueError):
            solve_nonsingular([[1, 2]], [1])
        with self.assertRaises(ValueError):
            solve_nonsingular([[1.0]], [1])


class ConvexQPTests(unittest.TestCase):
    def check_qp(self, h, c, bounds, **kwargs):
        r = solve_convex_box_qp(h, c, bounds, **kwargs)
        self.assertEqual(r.status, "optimal", r)
        self.assertTrue(verify_convex_box_qp_result(h, c, bounds, r,
                                                constant=kwargs.get("constant", 0)))
        return r

    def test_iterable_inputs_are_normalized_once(self):
        r = solve_convex_box_qp((iter(row) for row in [[2]]), iter([-1]), iter([(0, 1)]))
        self.assertEqual((r.status, r.x, r.value), ("optimal", (F(1, 2),), F(-1, 4)))
        self.assertTrue(verify_convex_box_qp_result([[2]], [-1], [(0, 1)], r))

    def test_singular_continuum_and_fixed_coordinates(self):
        r = self.check_qp([[2, 2], [2, 2]], [-2, -2], [(0, 1)] * 2)
        self.assertEqual(sum(r.x), 1)
        self.assertEqual(r.value, -1)
        r = self.check_qp([[0, 0], [0, 0]], [5, -7], [(2, 2), (3, 3)])
        self.assertEqual(r.x, (F(2), F(3)))
        self.assertEqual(r.value, -11)

    def test_boundary_kkt_and_exact_interior(self):
        r = self.check_qp([[2, 1], [1, 2]], [-5, 1], [(0, 1)] * 2)
        self.assertEqual(r.x, (F(1), F(0)))
        self.assertEqual(r.value, -4)
        r = self.check_qp([[6, 0], [0, 14]], [-1, -1], [(0, 1)] * 2, constant=F(3, 11))
        self.assertEqual(r.x, (F(1, 6), F(1, 14)))

    def test_seeded_psd_instances_with_known_kkt_values(self):
        rng = random.Random(28304)
        for _ in range(32):
            n = rng.randint(1, 5)
            rank = rng.randint(0, n)
            gram = [[F(rng.randint(-3, 3)) for _ in range(n)] for _ in range(rank)]
            h = [[sum((row[i] * row[j] for row in gram), F(0))
                  for j in range(n)] for i in range(n)]
            x = [rng.choice([F(0), F(1), F(1, 3)]) for _ in range(n)]
            grad = [F(rng.randint(1, 3)) if v == 0 else F(-rng.randint(1, 3)) if v == 1
                    else F(0) for v in x]
            c = [grad[i] - sum((h[i][j] * x[j] for j in range(n)), F(0)) for i in range(n)]
            r = self.check_qp(h, c, [(0, 1)] * n)
            expected = sum((c[i] * x[i] + sum((h[i][j] * x[j] * x[i]
                                                               for j in range(n)), F(0)) / 2
                            for i in range(n)), F(0))
            self.assertEqual(r.value, expected)

    def test_exhaustive_fallback_without_numerical_proposals(self):
        with patch("rational_optimization._proposed_faces", return_value=iter(())):
            r = self.check_qp([[2, 1], [1, 2]], [-5, 1], [(0, 1)] * 2)
        self.assertGreater(r.faces, 1)
        self.assertEqual(r.x, (F(1), F(0)))

    def test_nonconvex_and_capped_search_are_not_certified_optima(self):
        self.assertFalse(is_psd([[0, 1], [1, 0]]))
        self.assertFalse(is_psd([[1, 0], [1, 1]]))
        self.assertTrue(is_psd([[1, 1], [1, 1]]))
        r = solve_convex_box_qp([[-1]], [0], [(0, 1)])
        self.assertEqual(r.status, "not_convex")
        r = solve_convex_box_qp([[2]], [-1], [(0, 1)], max_faces=0)
        self.assertEqual((r.status, r.reason), ("limit", "max_faces"))
        r = solve_convex_box_qp([[2, 2], [2, 2]], [-2, -2], [(0, 1)] * 2, max_pivots=0)
        self.assertEqual((r.status, r.reason), ("limit", "max_pivots"))

    def test_empty_dimension_and_tampered_kkt(self):
        self.assertEqual(self.check_qp([], [], [], constant=7).value, 7)
        r = self.check_qp([[2]], [-3], [(0, 1)])
        with patch("rational_optimization.solve_convex_box_qp", side_effect=AssertionError("optimizer called")):
            self.assertTrue(verify_convex_box_qp_result([[2]], [-3], [(0, 1)], r))
            self.assertFalse(verify_convex_box_qp_result([[2]], [-3], [(0, 1)], replace(r, x=(F(0),))))
            self.assertFalse(verify_convex_box_qp_result([[2]], [-3], [(0, 1)], replace(r, certificate={})))
            self.assertFalse(verify_convex_box_qp_result([[2]], [-3], [(0, 1)], replace(r, value=F(0))))


if __name__ == "__main__":
    unittest.main()
