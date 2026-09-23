"""Focused tests for the independent exact cone reference."""
import math
import unittest

import cvxpy as cp

from .conic_reference import _phi_cone, solve, enumerate_small, UnsupportedConicReference
from .instances import build
from .validation import validate_witness


class ClosedPerspectiveTests(unittest.TestCase):
    def test_trig_explicitly_unsupported(self):
        for solver in (solve, enumerate_small):
            with self.subTest(solver=solver.__name__):
                with self.assertRaisesRegex(UnsupportedConicReference, "family 'trig'"):
                    solver("lbesh.trig.small.s104729")

    def test_positive_scale_and_zero_closure(self):
        for law in ("exp", "log", "reciprocal", "quadratic"):
            for y, z in ((1., .3), (.2, .06), (0., 0.)):
                with self.subTest(law=law, y=y):
                    rows = []
                    q = _phi_cone(cp.Constant(z), cp.Constant(y), law, rows)
                    problem = cp.Problem(cp.Minimize(q), rows)
                    problem.solve(solver="CLARABEL", max_threads=1,
                                  tol_gap_abs=1e-10, tol_gap_rel=1e-10, tol_feas=1e-10)
                    a = .3
                    value = {"exp": math.expm1(3*a)/math.expm1(1.5),
                             "log": -math.log1p(-a)/math.log(2),
                             "reciprocal": 1/(1-a)-1,
                             "quadratic": 4*a*a}[law]
                    self.assertEqual(problem.status, "optimal")
                    self.assertAlmostEqual(problem.value, y*value, delta=3e-8)

    def test_singular_log_reciprocal_domain_rejected(self):
        for law in ("log", "reciprocal"):
            rows = []
            q = _phi_cone(cp.Constant(1.), cp.Constant(1.), law, rows)
            problem = cp.Problem(cp.Minimize(q), rows+[q <= 2])
            problem.solve(solver="CLARABEL", max_threads=1)
            self.assertEqual(problem.status, "infeasible")

    def test_independent_best_assignments(self):
        # Frozen values from independent expression-based CVXPY enumeration.
        refs = {"exp": ((0, 2, 2), 2.2988982512571163),
                "log": ((0, 2, 2), 2.623680887970512),
                "reciprocal": ((0, 2, 2), 2.3284312623657657),
                "quadratic": ((1, 2, 2), 1.9062495933553476),
                "logsumexp": ((1, 2, 0), .12390703718756486)}
        for law, (modes, expected) in refs.items():
            with self.subTest(law=law):
                name = f"lbesh.{law}.small.s104729"
                result = solve(name, modes=modes)
                self.assertEqual(result["status"], "optimal")
                self.assertAlmostEqual(result["obj"], expected, delta=2e-7)
                self.assertAlmostEqual(result["lb"], expected, delta=2e-7)
                report = validate_witness(build(name), {"variables": result["witness"]},
                                          reported_objective=result["obj"])
                self.assertTrue(report["feasible"], report["issues"])
                self.assertFalse(result["bound_certified"])


if __name__ == "__main__":
    unittest.main()
