"""Independent analytic and adversarial checks for finite graph separation."""

from copy import deepcopy
from fractions import Fraction as Q
from pathlib import Path
import sys
import unittest

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "solver"))
import separation as sep


class SeparationReview(unittest.TestCase):
    def setUp(self):
        self.x, self.y = sp.symbols("x y")

    def run_graph(self, features, box, query, **kwargs):
        symbols = (self.x, self.y)[:len(box)]
        result = sep.separate_graph(features, symbols, box, query, **kwargs)
        if result["status"] != "unresolved":
            self.assertTrue(sep.replay_separation(
                result, features, symbols, box, query,
                rows=kwargs.get("rows", ()), epsilon=kwargs.get("epsilon", Q(1, 100)),
                nonnegative=kwargs.get("nonnegative", ())))
        return result

    def test_quadratic_cut_matches_analytic_support(self):
        # min (x - 1/3)^2 = 0; no numerical optimizer supplies the expectation.
        feature = (self.x - sp.Rational(1, 3)) ** 2
        result = self.run_graph((feature,), [(0, 1)], [Q(-1, 7)],
                                epsilon=Q(1, 8), complete=True, proposal_rounds=0)
        self.assertEqual(result["status"], "cut")
        self.assertEqual(Q(result["cut"]["rhs"]), 0)
        self.assertEqual(Q(result["cut"]["coefficients"][0]), 1)

    def test_grid_finds_normal_missing_from_corners(self):
        # Exact L1 distance is 1/100. No c in {-1,0,1}^2 separates it.
        result = self.run_graph((self.x, self.x ** 2), [(0, 1)],
                                [Q(3, 10), Q(2, 25)], epsilon=Q(1, 4),
                                complete=True, proposal_rounds=0)
        self.assertEqual(result["status"], "cut")
        a, b = map(Q, result["cut"]["coefficients"])
        self.assertNotIn((a, b), [(Q(i), Q(j)) for i in (-1, 0, 1) for j in (-1, 0, 1)])
        candidates = [Q(0), a + b]
        if b > 0 and 0 <= -a / (2 * b) <= 1:
            candidates.append(-a * a / (4 * b))
        self.assertEqual(Q(result["cut"]["rhs"]), min(candidates))
        self.assertLessEqual(Q(result["cut"]["query_gap"]), Q(1, 100))
        self.assertGreater(result["stats"]["normal_grid_calls"], 3)
        # Recompute the true minimum for the actual exported binary64 row.
        export = result["cut"]["binary64"]
        self.assertTrue(export["available"])
        af, bf = map(Q, export["coefficients"])
        float_candidates = [Q(0), af + bf]
        if bf > 0 and 0 <= -af / (2 * bf) <= 1:
            float_candidates.append(-af * af / (4 * bf))
        self.assertLessEqual(Q(export["rhs"]), min(float_candidates))

    def test_export_with_negative_feature_range(self):
        result = self.run_graph((self.x, self.x ** 2), [(-2, -1)],
                                [Q(-3, 2), 2], epsilon=Q(1, 2), complete=True,
                                proposal_rounds=0)
        self.assertEqual(result["status"], "cut")
        export = result["cut"]["binary64"]
        self.assertTrue(export["available"])
        a, b = map(Q, export["coefficients"])
        candidates = [-2 * a + 4 * b, -a + b]
        if b > 0 and -2 <= -a / (2 * b) <= -1:
            candidates.append(-a * a / (4 * b))
        self.assertLessEqual(Q(export["rhs"]), min(candidates))
        self.assertTrue(export["separates"])

    def test_thin_affine_equality_has_exact_support(self):
        rows = [(1, 1, Q(1, 3)), (-1, -1, Q(-1, 3))]
        result = self.run_graph((self.x, self.y, self.x * self.y),
                                [(0, 1), (0, 1)], [Q(1, 6), Q(1, 6), Q(1, 24)],
                                rows=rows, epsilon=Q(1, 100), complete=True,
                                proposal_rounds=0)
        self.assertEqual(result["status"], "cut")
        self.assertEqual(tuple(map(Q, result["cut"]["coefficients"])), (-1, -1, -1))
        self.assertEqual(Q(result["cut"]["rhs"]), Q(-13, 36))
        self.assertEqual(Q(result["cut"]["query_gap"]), Q(1, 72))

    def test_nonquadratic_domain_net_lower_bound(self):
        feature = (self.x - sp.Rational(1, 3)) ** 4 + sp.Rational(1, 7)
        result = self.run_graph((feature,), [(0, 1)], [0],
                                epsilon=Q(1, 4), complete=True, proposal_rounds=0)
        self.assertEqual(result["status"], "cut")
        self.assertEqual(result["witness"]["kind"], "polynomial_net_support")
        # The exact minimum is 1/7. The certified lower bound may be weaker.
        self.assertGreater(Q(result["cut"]["rhs"]), 0)
        self.assertLessEqual(Q(result["cut"]["rhs"]), Q(1, 7))
        self.assertLessEqual(Q(result["witness"]["error"]), Q(1, 8))

    def test_complete_near_hull_grid_is_replayed(self):
        result = self.run_graph((self.x ** 4,), [(0, 1)], [Q(1, 2)],
                                epsilon=Q(1, 2), complete=True, proposal_rounds=0)
        self.assertEqual(result["status"], "within_tolerance")
        self.assertEqual(result["witness"]["kind"], "finite_normal_net")
        self.assertEqual(len(result["witness"]["points"]),
                         result["witness"]["intervals"] + 1)
        mutations = []
        omitted = deepcopy(result)
        omitted["witness"]["points"].pop()
        mutations.append(omitted)
        replaced = deepcopy(result)
        replaced["witness"]["points"] = [["0"] for _ in replaced["witness"]["points"]]
        mutations.append(replaced)
        outside = deepcopy(result)
        outside["witness"]["points"][0] = ["2"]
        mutations.append(outside)
        changed_error = deepcopy(result)
        changed_error["witness"]["support_error"] = "1"
        mutations.append(changed_error)
        for modified in mutations:
            self.assertFalse(sep.replay_separation(modified, (self.x ** 4,),
                             (self.x,), [(0, 1)], [Q(1, 2)], epsilon=Q(1, 2)))

    def test_primal_combination_is_actual_hull_evidence(self):
        result = self.run_graph((self.x, self.x ** 2), [(0, 1)],
                                [Q(1, 2), Q(1, 2)], epsilon=Q(1, 100), complete=True)
        self.assertEqual(result["status"], "within_tolerance")
        self.assertEqual(result["witness"]["kind"], "convex_combination")
        modified = deepcopy(result)
        modified["witness"]["weights"][0] = "-1"
        self.assertFalse(sep.replay_separation(modified, (self.x, self.x ** 2),
                         (self.x,), [(0, 1)], [Q(1, 2), Q(1, 2)], epsilon=Q(1, 100)))

    def test_constant_graph_zero_radius(self):
        result = self.run_graph((sp.Rational(2, 7),), [(0, 1)], [Q(2, 7)],
                                epsilon=Q(1, 100), complete=True, proposal_rounds=0)
        self.assertEqual(result["status"], "within_tolerance")

    def test_empty_domain_is_not_near_hull(self):
        result = self.run_graph((self.x,), [(0, 1)], [0],
                                rows=[(1, Q(-1, 100))], max_directions=0)
        self.assertEqual(result["status"], "empty_domain")

    def test_budget_exhaustion_is_not_a_certificate(self):
        for feature, kwargs in [(self.x ** 2, {"max_directions": 0}),
                                (self.x ** 4, {"max_samples": 0})]:
            result = self.run_graph((feature,), [(0, 1)], [Q(1, 2)],
                                    proposal_rounds=0, **kwargs)
            self.assertEqual(result["status"], "unresolved")
            self.assertFalse(sep.replay_separation(result, (feature,), (self.x,),
                             [(0, 1)], [Q(1, 2)]))

    def test_subnormal_exact_gap_need_not_export(self):
        tiny = Q(1, 2 ** 1100)
        result = self.run_graph((sp.Rational(tiny.numerator, tiny.denominator),),
                                [(0, 0)], [0], epsilon=tiny / 2,
                                complete=True, proposal_rounds=0)
        self.assertEqual(result["status"], "cut")
        self.assertEqual(Q(result["cut"]["rhs"]), tiny)
        self.assertTrue(result["cut"]["binary64"]["available"])
        self.assertFalse(result["cut"]["binary64"]["separates"])

    def test_binary64_overflow_preserves_rational_verdict(self):
        big = Q(2 ** 1100)
        result = self.run_graph((sp.Integer(big.numerator),), [(0, 0)], [0],
                                epsilon=big / 2, complete=True, proposal_rounds=0)
        self.assertEqual(result["status"], "cut")
        self.assertFalse(result["cut"]["binary64"]["available"])

    def test_high_precision_float_identity_is_preserved(self):
        value = sp.Float("0.10000000000000000000000000000000000000000000000000001", 100)
        exact = Q(sp.Rational(value))
        query = exact - Q(1, 2 ** 400)
        result = self.run_graph((value,), [(0, 0)], [query],
                                epsilon=Q(1, 2 ** 402), complete=True, proposal_rounds=0)
        self.assertEqual(result["status"], "cut")
        self.assertEqual(Q(result["cut"]["rhs"]), exact)

    def test_unevaluated_nonpolynomial_domain_is_rejected(self):
        expression = sp.Mul(self.x, sp.Pow(self.x, -1, evaluate=False), evaluate=False)
        with self.assertRaises(ValueError):
            sep.separate_graph((expression,), (self.x,), [(0, 0)], [1], complete=True)

    def test_expected_query_domain_epsilon_are_bound(self):
        result = self.run_graph((self.x ** 2,), [(0, 1)], [-1],
                                epsilon=Q(1, 4), complete=True)
        for box, query, epsilon in [([(0, 2)], [-1], Q(1, 4)),
                                    ([(0, 1)], [-2], Q(1, 4)),
                                    ([(0, 1)], [-1], Q(1, 3))]:
            self.assertFalse(sep.replay_separation(result, (self.x ** 2,),
                             (self.x,), box, query, epsilon=epsilon))
        modified = deepcopy(result)
        modified["cut"]["binary64"]["rhs"] = 1.0
        self.assertFalse(sep.replay_separation(modified, (self.x ** 2,),
                         (self.x,), [(0, 1)], [-1], epsilon=Q(1, 4)))

    def test_positive_coordinate_cone_has_one_sided_distance(self):
        result = self.run_graph((self.x, self.x ** 2), [(0, 1)],
                                [Q(1, 2), 10], nonnegative=(1,),
                                epsilon=Q(1, 100), complete=True)
        self.assertEqual(result["status"], "within_tolerance")
        self.assertEqual(Q(result["witness"]["distance"]), 0)
        self.assertFalse(sep.replay_separation(result, (self.x, self.x ** 2),
                         (self.x,), [(0, 1)], [Q(1, 2), 10], epsilon=Q(1, 100)))
        below = self.run_graph((self.x ** 2,), [(0, 1)], [-1],
                               nonnegative=(0,), epsilon=Q(1, 2), complete=True)
        self.assertEqual(below["status"], "cut")
        self.assertGreaterEqual(Q(below["cut"]["coefficients"][0]), 0)

    def test_positive_cone_finite_grid(self):
        result = self.run_graph((self.x, self.x ** 2), [(0, 1)],
                                [Q(1, 2), Q(1, 2)], nonnegative=(1,),
                                epsilon=Q(1, 2), complete=True, proposal_rounds=0)
        self.assertEqual(result["status"], "within_tolerance")
        self.assertEqual(result["witness"]["kind"], "finite_normal_net")

    def test_cone_replay_rejects_negative_normal(self):
        result = self.run_graph((self.x ** 2,), [(0, 1)], [2],
                                epsilon=Q(1, 2), complete=True)
        self.assertEqual(result["status"], "cut")
        self.assertLess(Q(result["cut"]["coefficients"][0]), 0)
        # Rebind the untrusted header as an attacker might; sign still must fail.
        result["problem"]["nonnegative"] = [0]
        self.assertFalse(sep.replay_separation(result, (self.x ** 2,), (self.x,),
                         [(0, 1)], [2], epsilon=Q(1, 2), nonnegative=(0,)))

    def test_malformed_top_level_certificate_is_rejected(self):
        for malformed in (None, [], "certificate", 1):
            self.assertFalse(sep.replay_separation(malformed, (self.x,),
                             (self.x,), [(0, 1)], [0]))

    def test_tiny_epsilon_respects_zero_direction_budget(self):
        result = self.run_graph((self.x,), [(0, 1)], [Q(1, 2)],
                                epsilon=Q(1, 2 ** 200), max_directions=0,
                                proposal_rounds=0)
        self.assertEqual(result["status"], "unresolved")
        self.assertEqual(result["stats"]["support_calls"], 0)
        self.assertGreater(result["stats"]["normal_grid_size"], 2 ** 100)

    def test_finite_enumerators_do_not_depend_on_python_stack_limit(self):
        # These are mathematical primitive contracts, independent of search order.
        self.assertEqual(list(sep._compositions(0, 1200)), [(0,) * 1200])
        compositions = list(sep._compositions(3, 5))
        self.assertEqual(len(compositions), 35)
        self.assertEqual(len(set(compositions)), 35)
        self.assertTrue(all(sum(p) == 3 and all(x >= 0 for x in p) for p in compositions))
        normal = next(sep._normal_net(1200, 1))
        self.assertEqual(len(normal), 1200)
        self.assertTrue(all(abs(x) == 1 for x in normal))
        net = list(sep._normal_net(2, 3, nonnegative=(1,)))
        expected = {(Q(i, 3), Q(j, 3)) for i in (-3, -1, 1, 3) for j in range(4)}
        self.assertEqual(set(net), expected)
        self.assertEqual(len(net), len(expected))


if __name__ == "__main__":
    unittest.main(verbosity=2)
