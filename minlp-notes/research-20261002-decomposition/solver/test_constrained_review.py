"""Independent adversarial checks for the TU constrained solver.

Run only this module with: python -m unittest test_constrained_review -v
from this directory. Expected optima below follow by direct substitution.
"""
import copy
from fractions import Fraction as F
import random
import unittest

from constrained_grid import (ConstrainedQP, _recovery_data,
                              _stationary_candidate, solve)
from verify_constrained import CertificateError, verify


def model(H, b, *, bounds=None, labels=None, rows=(), rhs=(), senses=(),
          bags=None, edges=(), curvature=None, constant=0, tu="network"):
    n = len(b)
    return ConstrainedQP(H, b, bounds or [(0, 1)] * n, labels or {},
                         rows, rhs, senses, bags or [list(range(n))], edges,
                         {"kind": tu}, curvature=curvature, constant=constant)


class IndependentConstrainedReview(unittest.TestCase):
    def test_random_equality_fibers_against_scalar_formula(self):
        # Eliminate y=1-x analytically. This oracle does not use face search,
        # dynamic programming, interval pruning, or the solver's linear algebra.
        rng = random.Random(20491)
        for _ in range(40):
            a, c, d, e, f = [rng.randrange(-5, 6) for _ in range(5)]
            alpha = F(a - 2*c + d, 2)
            beta = c - d + e - f
            gamma = F(d, 2) + f
            candidates = [F(0), F(1)]
            if alpha > 0 and 0 < -F(beta)/(2*alpha) < 1:
                candidates.append(-F(beta)/(2*alpha))
            expected = min(alpha*x*x + beta*x + gamma for x in candidates)
            problem = model([[a, c], [c, d]], [e, f],
                            rows=[[1, 1], [-1, -1]], rhs=[1, -1],
                            senses=["==", "=="],
                            curvature={"L": str(max(F(0), alpha)),
                                       "mode": "equalities"})
            cert = solve(problem, exact=True, max_stages=80)
            self.assertEqual(cert["status"], "exact", (a, c, d, e, f, cert["reason"]))
            self.assertEqual(F(cert["upper"]), expected)
            self.assertTrue(verify(cert)["valid"])

    def test_correlated_rounding_and_equality_penalty_invariance(self):
        # On x=y, both objectives are 2*x*x-2*x, minimized at x=1/2.
        args = dict(rows=[[1, -1]], rhs=[0], senses=["=="],
                    curvature={"L": "2", "mode": "equalities"})
        original = model([[0, 2], [2, 0]], [-1, -1], **args)
        rho = 2**30
        penalized = model([[2*rho, 2-2*rho], [2-2*rho, 2*rho]],
                          [-1, -1], **args)
        first = solve(original, "1/256")
        second = solve(penalized, "1/256")
        self.assertEqual(first["stages"], second["stages"])
        self.assertEqual(F(first["upper"]), F(-1, 2))
        self.assertLessEqual(F(first["lower"]), F(-1, 2))
        self.assertTrue(verify(first)["valid"])
        self.assertTrue(verify(second)["valid"])
        with self.assertRaises(ValueError):
            model([[0, 2], [2, 0]], [-1, -1], rows=[[1, -1]],
                  rhs=[0], senses=["=="],
                  curvature={"L": "0", "mode": "equalities"})

    def test_large_integer_columns_and_nonconsecutive_labels(self):
        # x=3*z and z in {0,2}; the two feasible values are 0 and -24.
        problem = model([[2, 0], [0, 0]], [-10, 0],
                        bounds=[(0, 6), (0, 2)], labels={1: [0, 2]},
                        rows=[[1, -3]], rhs=[0], senses=["=="])
        cert = solve(problem, exact=True)
        self.assertEqual(cert["status"], "exact")
        self.assertEqual(tuple(map(F, cert["point"])), (F(6), F(2)))
        self.assertEqual(F(cert["lower"]), -24)
        self.assertTrue(verify(cert)["valid"])

    def test_non_dyadic_exact_coordinate_reconstruction_without_faces(self):
        # 3*x^2-2*x has its unique minimum -1/3 at x=1/3.
        problem = model([[6]], [-2])
        cert = solve(problem, exact=True, max_exact_faces=0,
                     max_recovery_pivots=0, max_stages=64)
        self.assertEqual(cert["status"], "exact")
        self.assertEqual(tuple(map(F, cert["point"])), (F(1, 3),))
        self.assertEqual(F(cert["lower"]), F(-1, 3))
        self.assertEqual(cert["statistics"]["exact_faces_attempted"], 0)
        self.assertTrue(verify(cert)["valid"])
        forged = copy.deepcopy(cert)
        forged["exact_proof"]["height"]["V"] = 1
        with self.assertRaises(CertificateError):
            verify(forged)

    def test_union_domains_and_stationary_recovery_for_disconnected_optima(self):
        # The optima are (0,1/3,1/3) and (1,1/3,1/3). Their x0 hull
        # contains an increasingly fine full interval; their union does not.
        problem = model([[-2, 0, 0], [0, 2, 0], [0, 0, 2]],
                        [1, F(-2, 3), F(-2, 3)], constant=F(2, 9),
                        rows=[[0, 1, -1]], rhs=[0], senses=["=="],
                        bags=[[0], [1, 2]], edges=[[0, 1]])
        cert = solve(problem, exact=True, retain_unions=True,
                     max_exact_faces=0, max_table_states=128, max_stages=64)
        self.assertEqual(cert["status"], "exact")
        self.assertEqual(F(cert["upper"]), 0)
        point = tuple(map(F, cert["point"]))
        self.assertIn(point[0], (F(0), F(1)))
        self.assertEqual(point[1:], (F(1, 3), F(1, 3)))
        self.assertGreater(cert["statistics"]["recovery_lp_calls"], 0)
        self.assertEqual(cert["statistics"]["exact_faces_attempted"], 0)
        split_stage = next(stage for stage in cert["stages"]
                           if len(stage["retained"][0]) == 2)
        self.assertTrue(verify(cert)["valid"])
        hull = solve(problem, exact=True, retain_unions=False,
                     max_exact_faces=0, max_table_states=128, max_stages=64)
        self.assertEqual(hull["status"], "limit")
        self.assertEqual(hull["reason"], "table-state limit")
        self.assertTrue(verify(hull)["valid"])
        forged = copy.deepcopy(cert)
        stage = forged["stages"][split_stage["level"]]
        pieces = stage["retained"][0]
        stage["retained"][0] = [[pieces[0][0], pieces[-1][1]]]
        with self.assertRaises(CertificateError):
            verify(forged)

    def test_stationary_recovery_on_an_optimal_continuum(self):
        # Every point of x+y=1/3 in the nonnegative box is optimal.
        # Exercise recovery alone: full fine grids across this continuum
        # have no favorable state bound, which is a documented limitation.
        problem = model([[2, 2], [2, 2]], [F(-2, 3), F(-2, 3)],
                        constant=F(1, 9))
        data = _recovery_data(problem)
        _, _, D, tau = data
        point = (F(1, 6), F(1, 6) + tau/(1000*D))
        self.assertTrue(problem.feasible(point))
        self.assertGreater(problem.value(point), 0)
        candidate, _, limited = _stationary_candidate(
            problem, point, data, set(), 1000, lambda: None)
        self.assertFalse(limited)
        self.assertIsNotNone(candidate)
        self.assertTrue(problem.feasible(candidate))
        self.assertEqual(sum(candidate), F(1, 3))
        self.assertEqual(problem.value(candidate), 0)

    def test_singular_ambient_hessian_and_fixed_coordinate(self):
        # The Hessian is singular, but the fixed second coordinate leaves
        # a strictly convex scalar problem with optimizer (1/3,0).
        problem = model([[6, 0], [0, 0]], [-2, 0],
                        bounds=[(0, 1), (0, 0)],
                        bags=[[0], [1]], edges=[[0, 1]])
        cert = solve(problem, exact=True, retain_unions=True, max_stages=64)
        self.assertEqual(cert["status"], "exact")
        self.assertEqual(tuple(map(F, cert["point"])), (F(1, 3), F(0)))
        self.assertEqual(F(cert["upper"]), F(-1, 3))
        self.assertTrue(verify(cert)["valid"])

    def test_branching_messages_with_infeasible_separator_states(self):
        # x0+x1=0 and x0=x2=x3 force all four nonnegative variables to zero.
        H = [[2 * int(i == j) for j in range(4)] for i in range(4)]
        problem = model(H, [0] * 4,
                        rows=[[1, 1, 0, 0], [1, 0, -1, 0], [1, 0, 0, -1]],
                        rhs=[0, 0, 0], senses=["=="] * 3,
                        bags=[[0, 1], [0, 2], [0, 3]],
                        edges=[[0, 1], [0, 2]], tu="all_minors")
        cert = solve(problem, "1/64")
        self.assertEqual(F(cert["upper"]), 0)
        self.assertTrue(any(row["value"] is None for stage in cert["stages"]
                            for msg in stage["messages"] for row in msg["rows"]))
        self.assertTrue(verify(cert)["valid"])
        forged = copy.deepcopy(cert)
        messages = forged["stages"][0]["messages"]
        target = next(row for msg in messages for row in msg["rows"]
                      if row["value"] is None)
        target["value"] = "0"
        with self.assertRaises(CertificateError):
            verify(forged)

    def test_empty_fiber_and_limits_are_distinct(self):
        empty = model([[2]], [0], rows=[[1]], rhs=[2], senses=["=="])
        cert = solve(empty, exact=True)
        self.assertEqual(cert["status"], "infeasible")
        self.assertTrue(verify(cert)["valid"])
        full = model([[6]], [-2])
        limited = solve(full, exact=True, max_stages=1, max_exact_faces=0)
        self.assertEqual(limited["status"], "limit")
        self.assertTrue(verify(limited)["valid"])
        forged = copy.deepcopy(limited)
        forged["status"] = "exact"
        with self.assertRaises(CertificateError):
            verify(forged)
        before_first_stage = solve(full, exact=True, max_table_states=1)
        self.assertEqual(before_first_stage["status"], "limit")
        self.assertEqual(before_first_stage["stages"], [])
        self.assertIsNone(before_first_stage["lower"])
        self.assertTrue(verify(before_first_stage)["valid"])

    def test_invalid_structure_alignment_and_curvature_are_rejected(self):
        with self.assertRaises(ValueError):
            model([[2]], [0], rows=[[1]], rhs=[F(1, 3)], senses=["=="])
        with self.assertRaises(ValueError):
            model([[2]], [0], bounds=[(0, F(1, 2))])
        with self.assertRaises(ValueError):
            model([[2, 0], [0, 2]], [0, 0],
                  rows=[[1, 1], [1, -1]], rhs=[1, 0], senses=["<=", "<="],
                  tu="all_minors")
        with self.assertRaises(ValueError):
            model([[2, 0], [0, 2]], [0, 0], rows=[[1, 1]], rhs=[1],
                  senses=["<="], curvature={"L": "0", "mode": "equalities"})
        with self.assertRaises(ValueError):
            model([[2, 0], [0, 2]], [0, 0], rows=[[1, 1]], rhs=[1],
                  senses=["<="], bags=[[0], [1]], edges=[[0, 1]])


if __name__ == "__main__":
    unittest.main()
