"""Independent analytic fixtures for the small-block certificate interfaces.

Expected extrema and distances below are derived directly from the named
functions. They do not use the support producer as the expected-value oracle.
Run from the repository root with the environment documented in the review.
"""

from copy import deepcopy
from fractions import Fraction as Q
from math import factorial, inf, nextafter
from pathlib import Path
import sys
import unittest

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solver.certified import (
    certify_support, downward_float, elementary_interval, replay_support,
)
from solver.screening import (
    SampleCache, replay_screen, screen_convex_combination, upper_float,
)
from theory.quadratic_polygon import support_quadratic, replay_quadratic


X, Y = sp.symbols("x y", real=True)


class SupportAnalyticReview(unittest.TestCase):
    def test_exported_binary_coefficient_defines_the_cut(self):
        result = certify_support((X,), (X,), ((10, 10),), (Q(1, 10),))
        expected = 10 * Q.from_float(0.1)
        self.assertEqual(result.status, "complete")
        self.assertEqual(result.cut.coefficients, (0.1,))
        self.assertLessEqual(result.cut.rhs_exact, expected)
        self.assertGreater(Q(nextafter(result.cut.rhs, inf)), expected)

    def test_feature_float_is_exact_binary_input(self):
        result = certify_support((X + sp.Float(0.1),), (X,), ((0, 0),), (1,))
        self.assertEqual(result.cut.rhs_exact, Q.from_float(0.1))

    def test_downward_float_handles_sign_and_subnormal_values(self):
        for exact in (Q(1, 10), -Q(1, 10), Q(1, 2**1075), -Q(1, 2**1075)):
            rounded = downward_float(exact)
            self.assertLessEqual(Q(rounded), exact)
            self.assertGreater(Q(nextafter(rounded, inf)), exact)

    def test_bernstein_subdivision_recovers_known_quadratic_minimum(self):
        # x²-x has minimum -1/4 at x=1/2; the unsplit Bernstein bound is -1/2.
        result = certify_support((X**2 - X,), (X,), ((0, 1),), (1,), target=-Q(1, 4))
        self.assertEqual(result.status, "complete")
        self.assertEqual(result.cut.rhs_exact, -Q(1, 4))
        self.assertEqual(result.stats["cells"], 3)

    def test_two_variable_bernstein_covers_interior_minimum(self):
        # The sum of these squares is nonnegative and vanishes at (1/2,1/2).
        expr = (X + Y - 1)**2 + (X - Y)**2
        result = certify_support((expr,), (X, Y), ((0, 1), (0, 1)), (1,),
                                 target=-Q(1, 16), max_cells=1024,
                                 quadratic_fast_path=False)
        self.assertEqual(result.status, "complete")
        self.assertLessEqual(result.cut.rhs_exact, 0)
        self.assertGreaterEqual(result.cut.rhs_exact, -Q(1, 16))

    def test_exact_degenerate_interval(self):
        result = certify_support((X**3,), (X,), ((Q(1, 3), Q(1, 3)),), (1,))
        self.assertEqual(result.cut.rhs, downward_float(Q(1, 27)))

    def test_bernstein_translation_includes_negative_domain_bounds(self):
        result = certify_support(((X - 3)**2 + (Y + 4)**2,), (X, Y),
                                 ((2, 4), (-5, -3)), (1,), target=0,
                                 quadratic_fast_path=False)
        self.assertEqual(result.status, "complete")
        self.assertEqual(result.cut.rhs_exact, 0)

    def test_empty_domain_requires_strict_row_exclusion(self):
        rows = (((1,), Q(1, 3)), ((-1,), -Q(2, 3)))
        # An unattainable target forces refinement; without a target a valid
        # whole-box lower bound may return before emptiness is discovered.
        result = certify_support((X**3,), (X,), ((0, 1),), (1,), rows=rows, target=2)
        self.assertEqual(result.status, "empty")
        self.assertTrue(replay_support((X**3,), (X,), ((0, 1),), (1,), rows, result.witness))
        # At x=0, x<=0 is active and the domain is nonempty.
        point = certify_support((X**3,), (X,), ((0, 0),), (1,), rows=(((1,), 0),))
        self.assertEqual(point.status, "complete")
        self.assertEqual(point.cut.rhs_exact, 0)

    def test_uncertain_domain_does_not_return_a_cut(self):
        for expr, interval in ((sp.log(X), (0, 1)), (1 / X, (-1, 1)),
                               (sp.Pow(X, sp.Rational(1, 3), evaluate=False), (-1, 1))):
            result = certify_support((expr,), (X,), (interval,), (1,), max_cells=32, max_depth=5)
            self.assertEqual(result.status, "incomplete")
            self.assertIsNone(result.cut)

    def test_cancelled_and_zero_weight_features_still_need_domains(self):
        reciprocal = sp.Pow(X, -1, evaluate=False)
        cancelled_product = sp.Mul(X, reciprocal, evaluate=False)
        logarithm = sp.log(X)
        cancelled_sum = sp.Add(logarithm, -logarithm, evaluate=False)
        for features, coefficients in (((cancelled_product,), (1,)),
                                       ((cancelled_sum,), (1,)),
                                       ((X, logarithm), (1, 0))):
            result = certify_support(features, (X,), ((0, 1),), coefficients,
                                     max_cells=32, max_depth=5)
            self.assertEqual(result.status, "incomplete")
            self.assertIsNone(result.cut)

    def test_continuous_nonsmooth_domain_endpoints_are_included(self):
        for expr, box in ((sp.sqrt(X), ((0, 1),)), (sp.Abs(X), ((-1, 1),))):
            result = certify_support((expr,), (X,), box, (1,), target=0)
            self.assertEqual(result.status, "complete")
            self.assertEqual(result.cut.rhs_exact, 0)

    def test_combined_scalar_preserves_exact_cancellation(self):
        result = certify_support((sp.exp(X), sp.exp(X)), (X,), ((-100, 100),), (1, -1), target=0)
        self.assertEqual(result.status, "complete")
        self.assertEqual(result.cut.rhs_exact, 0)
        self.assertEqual(result.stats["cells"], 1)

    def test_chord_bound_uses_upper_second_derivative(self):
        # exp(x)-x has minimum 1 on [0,1]. Its independent feature bound is
        # zero, while min(endpoint values)-sup(g'')/8 = 1-e/8 > 0.6602.
        result = certify_support((sp.exp(X), X), (X,), ((0, 1),), (1, -1), max_cells=1)
        self.assertEqual(result.status, "complete")
        self.assertGreater(result.cut.rhs_exact, Q(6602, 10000))
        self.assertLess(result.cut.rhs_exact, Q(6603, 10000))
        self.assertLessEqual(result.cut.rhs_exact, 1)

    def test_concave_chord_needs_no_curvature_penalty(self):
        # log(1+x)-x is concave, decreasing, with minimum log(2)-1.
        # The endpoint bound is about -0.3068528; independent ranges give -1.
        result = certify_support((sp.log(1 + X), X), (X,), ((0, 1),), (1, -1), max_cells=1)
        self.assertEqual(result.status, "complete")
        self.assertGreater(result.cut.rhs_exact, -Q(307, 1000))
        self.assertLess(result.cut.rhs_exact, -Q(306, 1000))

    def test_nonsmooth_derivative_cannot_license_a_chord_bound(self):
        # This V-shaped function has minimum zero at 0, below both endpoints.
        result = certify_support((sp.Abs(X), X), (X,), ((-1, 1),), (1, -Q(1, 2)))
        self.assertEqual(result.status, "complete")
        self.assertLessEqual(result.cut.rhs_exact, 0)

    def test_transcendental_range_contains_known_interior_extrema(self):
        for expr, interval in ((sp.sin(X), (Q(0), Q(7))),
                               (sp.cos(X), (-Q(4), Q(4)))):
            lower, upper = elementary_interval(expr, X, interval)
            self.assertLessEqual(lower, -1)
            self.assertGreaterEqual(upper, 1)

    def test_exp_endpoint_against_independent_rational_series(self):
        # 0 < e - sum_{k=0}^N 1/k! < 1/(N*N!), by a geometric tail bound.
        n = 35
        partial = sum((Q(1, factorial(k)) for k in range(n + 1)), Q(0))
        remainder = Q(1, n * factorial(n))
        lower, upper = elementary_interval(sp.exp(X), X, (Q(1), Q(1)), precision=128)
        self.assertLessEqual(lower, partial + remainder)
        self.assertGreaterEqual(upper, partial)
        self.assertLess(upper - lower, Q(1, 10**35))

    def test_rational_endpoint_is_not_rounded_to_binary64(self):
        tiny = Q(1, 2**200)
        lower, upper = elementary_interval(sp.log(X), X, (1 + tiny, 1 + tiny), precision=256)
        # z/(1+z) <= log(1+z) <= z for z>=0, from the integral of 1/(1+t).
        self.assertLessEqual(lower, tiny)
        self.assertGreaterEqual(upper, tiny / (1 + tiny))
        self.assertGreater(lower, 0)

    def test_no_endpoint_sliver_can_be_replaced_by_endpoint_value(self):
        # An arbitrarily narrow interior peak is located at x=2^-300.
        # Negative support must include its value -1, however close to zero.
        peak = 1 / (1 + (2**300 * X - 1)**2)
        result = certify_support((peak,), (X,), ((0, 1),), (-1,))
        self.assertEqual(result.status, "complete")
        self.assertLessEqual(result.cut.rhs_exact, -1)

    def test_reciprocal_negative_interval_and_odd_power(self):
        self.assertEqual(elementary_interval(1 / X, X, (-Q(2), -Q(1))), (-Q(1), -Q(1, 2)))
        self.assertEqual(elementary_interval(X**3, X, (-Q(2), Q(1))), (-Q(8), Q(1)))

    def test_replay_rejects_model_and_proof_mutations(self):
        features, symbols, box, coefficients = (X**2 - X,), (X,), ((0, 1),), (1,)
        result = certify_support(features, symbols, box, coefficients, target=-Q(1, 4))
        witness = result.witness
        self.assertTrue(replay_support(features, symbols, box, coefficients, (), witness))
        self.assertFalse(replay_support(features, symbols, ((0, 2),), coefficients, (), witness))
        self.assertFalse(replay_support(features, symbols, box, (2,), (), witness))
        self.assertFalse(replay_support((X**2,), symbols, box, coefficients, (), witness))
        mutations = []
        changed = deepcopy(witness)
        changed["rhs"] = nextafter(result.cut.rhs, inf).hex()
        mutations.append(changed)
        changed = deepcopy(witness)
        changed["proof"]["children"].pop()
        mutations.append(changed)
        changed = deepcopy(witness)
        changed["proof"]["split"] = True
        mutations.append(changed)
        changed = deepcopy(witness)
        changed["proof"]["children"][0]["lower"] = "100"
        mutations.append(changed)
        for changed in mutations:
            self.assertFalse(replay_support(features, symbols, box, coefficients, (), changed))

    def test_replay_rejects_excluding_a_row_boundary(self):
        rows = (((1,), 0),)
        result = certify_support((X**3,), (X,), ((0, 1),), (1,), rows=rows)
        changed = deepcopy(result.witness)
        changed["status"] = "empty"
        changed.pop("lower_bound")
        changed.pop("rhs")
        changed["proof"] = {"excluded_by": 0}
        self.assertFalse(replay_support((X**3,), (X,), ((0, 1),), (1,), rows, changed))

    def test_producer_budgets_match_replay_limits(self):
        # Regression from review: depth 271 previously returned a complete
        # producer proof that replay rejected at its fixed depth-256 cap.
        with self.assertRaises(ValueError):
            certify_support((X,), (X,), ((0, 1),), (1,),
                            rows=(((-1,), -Q(1, 2**270)),),
                            target=Q(1, 2**271), max_depth=300, max_cells=1000)
        with self.assertRaises(ValueError):
            certify_support((X,), (X,), ((0, 1),), (1,), max_cells=1000001)
        rows = (((-1,), -Q(1, 2**255)),)
        result = certify_support((X,), (X,), ((0, 1),), (1,), rows=rows,
                                 target=Q(1, 2**256), max_depth=256, max_cells=1000)
        self.assertEqual(result.status, "complete")
        self.assertTrue(replay_support((X,), (X,), ((0, 1),), (1,), rows, result.witness))


class QuadraticAnalyticReview(unittest.TestCase):
    def test_known_exact_minima_cover_all_candidate_classes(self):
        fixtures = (
            # Strictly convex, unique interior minimizer (1/3,2/5).
            (((0, 1), (0, 1)), (), (Q(1, 9) + Q(8, 25), -Q(2, 3), -Q(8, 5), 1, 0, 2), Q(0)),
            # x²+y² >= (x+y)²/2 >= 1/2; equality at (1/2,1/2).
            (((0, 1), (0, 1)), ((-1, -1, -1),), (0, 0, 0, 1, 0, 1), Q(1, 2)),
            # Indefinite objective: x²-y² >= -1, attained at (0,+/-1).
            (((-1, 1), (-1, 1)), (), (0, 0, 0, 1, 0, -1), -Q(1)),
            # Singular positive semidefinite Hessian, line of minimizers.
            (((0, 1), (0, 1)), (), (1, -2, -2, 1, 2, 1), Q(0)),
            # Linear objective on the clipped triangle.
            (((0, 1), (0, 1)), ((-1, -1, -1),), (0, 1, 2, 0, 0, 0), Q(1)),
            # Segment y=x: 2x²-2x has minimum -1/2.
            (((0, 1), (0, 1)), ((1, -1, 0), (-1, 1, 0)), (0, -1, -1, 1, 0, 1), -Q(1, 2)),
            # Singleton: x*y=2/15.
            (((Q(1, 3), Q(1, 3)), (Q(2, 5), Q(2, 5))), (), (0, 0, 0, 0, 1, 0), Q(2, 15)),
        )
        for bounds, rows, coefficients, expected in fixtures:
            with self.subTest(coefficients=coefficients, rows=rows):
                result = support_quadratic(bounds, rows, coefficients)
                self.assertEqual(result["status"], "complete")
                self.assertEqual(Q(result["bound"]), expected)

    def test_empty_domain_and_imported_oracle_binding(self):
        bounds, rows, coefficients = ((0, 1), (0, 1)), ((1, 1, -1),), (0, 0, 0, 1, 0, 1)
        result = support_quadratic(bounds, rows, coefficients)
        self.assertEqual(result["status"], "empty")
        self.assertTrue(replay_quadratic(bounds, rows, coefficients, result))
        self.assertFalse(replay_quadratic(bounds, (), coefficients, result))
        support = certify_support((X**2 + Y**2,), (X, Y), bounds, (1,),
                                  rows=(((-1, -1), -1),))
        self.assertEqual(support.cut.rhs_exact, Q(1, 2))
        self.assertTrue(replay_support((X**2 + Y**2,), (X, Y), bounds, (1,),
                                       (((-1, -1), -1),), support.witness))
        changed = deepcopy(support.witness)
        changed["proof"]["quadratic"]["bound"] = "1"
        self.assertFalse(replay_support((X**2 + Y**2,), (X, Y), bounds, (1,),
                                        (((-1, -1), -1),), changed))
        self.assertFalse(replay_support((X**2 + Y**2,), (X, Y), bounds, (1,), (), support.witness))

    def test_imported_star_support_and_mutation_binding(self):
        z = sp.Symbol("z", real=True)
        # Both squares are nonnegative and vanish at x=y=z=0.
        features, symbols = ((X - Y)**2, (X - z)**2), (X, Y, z)
        box = ((-1, 1),) * 3
        result = certify_support(features, symbols, box, (1, 1))
        self.assertEqual(result.status, "complete")
        self.assertEqual(result.stats["method"], "quadratic_star")
        self.assertEqual(result.cut.rhs_exact, 0)
        self.assertTrue(replay_support(features, symbols, box, (1, 1), (), result.witness))
        self.assertFalse(replay_support(features, symbols, box, (1, 2), (), result.witness))
        changed = deepcopy(result.witness)
        changed["proof"]["star"]["bound"] = "1"
        self.assertFalse(replay_support(features, symbols, box, (1, 1), (), changed))


class ScreeningAnalyticReview(unittest.TestCase):
    @staticmethod
    def graph(point):
        x, = point
        return x, x*x

    def test_two_norms_and_strict_threshold_semantics(self):
        samples = SampleCache(bounds=((0, 1),), evaluate=self.graph).bind(((0,), (1,)))
        # Mixture=(1/2,1/2), query=(3/2,5/2), scales=(2,4).
        # Scaled residual=(1/2,1/2): infinity bound=1/2, L1 bound=1.
        query, scales = (Q(3, 2), Q(5, 2)), (2, 4)
        a = screen_convex_combination(query, samples, (1, 1), scales=scales, threshold=Q(1, 2))
        b = screen_convex_combination(query, samples, (1, 1), scales=scales, threshold=1, norm="1")
        self.assertEqual(a.upper_bound, Q(1, 2))
        self.assertEqual(b.upper_bound, 1)
        self.assertTrue(a.can_skip)
        self.assertTrue(b.can_skip)
        # L1 uses max(s_j*|normal_j|)<=1. Here equality is attained.
        normal = (Q(1, 2), Q(1, 4))
        self.assertEqual(sum(c * (q - Q(1, 2)) for c, q in zip(normal, query)), b.threshold)
        # This is why the API excludes only violations strictly greater than threshold.

    def test_interval_samples_use_worst_endpoint_not_midpoint(self):
        def enclosed_graph(point):
            x, = point
            return (x - Q(1, 10), x + Q(1, 5)), x*x
        samples = SampleCache(bounds=((0, 1),), evaluate=enclosed_graph).bind(((0,), (1,)))
        certificate = screen_convex_combination((Q(1, 2), Q(1, 2)), samples, (1, 1))
        self.assertEqual(certificate.upper_bound, Q(1, 5))
        self.assertFalse(certificate.can_skip)

    def test_exact_row_feasibility_rejects_nearby_infeasible_samples(self):
        cache = SampleCache(bounds=((0, 1),), rows=((1, Q(1, 3)),), evaluate=self.graph)
        with self.assertRaises(ValueError):
            cache.bind(((Q(1, 3) + Q(1, 2**100),),))
        samples = cache.bind(((Q(1, 3),),))
        self.assertEqual(samples.points, ((Q(1, 3),),))

    def test_original_evaluator_and_query_are_bound_on_replay(self):
        samples = SampleCache(bounds=((0, 1),), evaluate=self.graph).bind(((0,), (1,)))
        query = (Q(1, 2), Q(1, 2))
        certificate = screen_convex_combination(query, samples, (1, 1)).to_dict()
        self.assertTrue(replay_screen(query, certificate, bounds=((0, 1),), evaluate=self.graph))
        self.assertFalse(replay_screen((Q(1, 2), 0), certificate,
                                       bounds=((0, 1),), evaluate=self.graph))
        self.assertFalse(replay_screen(query, certificate, bounds=((0, 1),),
                                       evaluate=lambda p: (p[0], p[0]**2 + 1)))
        changed = deepcopy(certificate)
        changed["samples"][0]["values"][0] = ["100", "100"]
        self.assertFalse(replay_screen(query, changed, bounds=((0, 1),), evaluate=self.graph))

    def test_weights_repair_preserves_convexity_and_upper_rounding(self):
        samples = SampleCache(bounds=((0, 1),), evaluate=self.graph).bind(((0,), (1,)))
        certificate = screen_convex_combination((1, 1), samples, (-Q(1, 2**100), 2))
        self.assertEqual(certificate.weights, (0, 1))
        self.assertEqual(certificate.upper_bound, 0)
        for exact in (Q(1, 10), Q(1, 2**1075)):
            rounded = upper_float(exact)
            self.assertGreaterEqual(Q(rounded), exact)
            self.assertLess(Q(nextafter(rounded, -inf)), exact)


if __name__ == "__main__":
    unittest.main(verbosity=2)
