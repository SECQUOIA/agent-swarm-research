"""Independent exact checks of original-row elimination and float conversion."""
from fractions import Fraction as Q
import itertools
import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solver.row_certificate import AffineSide, certify_row_combination


class RowRoundingReview(unittest.TestCase):
    def verify_sharp_box_correction(self, kwargs):
        result = certify_row_combination(**kwargs)
        names = kwargs["variables"]
        # The expected elimination is derived directly, independently of
        # producer serialization or its replay routine.
        source = {name: Q(0) for name in names}
        terms = kwargs["linear_terms"]
        terms = terms.items() if hasattr(terms, "items") else terms
        for name, value in terms:
            source[name] += Q(value)
        rhs = Q(kwargs["support_rhs"])
        for multiplier, side in zip(kwargs["multipliers"], kwargs["sides"]):
            multiplier = Q(multiplier)
            rhs -= multiplier * Q(side.rhs)
            for name, value in side.affine_terms:
                source[name] -= multiplier * Q(value)
        errors = {name: Q(value) - source[name]
                  for name, value in zip(names, result.coefficients)}
        endpoints = [[Q(x) for x in kwargs["bounds"][name]] for name in names]
        corrections = [sum((errors[name] * value for name, value in zip(names, point)), Q(0))
                       for point in itertools.product(*endpoints)]
        threshold = rhs + min(corrections)
        self.assertLessEqual(Q(result.rhs), threshold)
        self.assertGreater(Q(math.nextafter(result.rhs, math.inf)), threshold)
        for point in itertools.product(*endpoints):
            exact_activity = sum((source[name] * value for name, value in zip(names, point)), Q(0))
            exported_activity = sum((Q(value) * x for value, x in zip(result.coefficients, point)), Q(0))
            self.assertGreaterEqual(exported_activity - Q(result.rhs),
                                    exact_activity - rhs)
        return result

    def test_both_rounding_signs_and_negative_endpoints(self):
        for sign in (1, -1):
            with self.subTest(sign=sign):
                self.verify_sharp_box_correction({
                    "variables": ["x", "y"],
                    "bounds": {"x": (-13, -2), "y": (3, 17)},
                    "linear_terms": [("x", 0.3), ("y", -0.7)],
                    "multipliers": [0.1, 0.9],
                    "support_rhs": Q(1, 3),
                    "sides": [AffineSide("one", [("x", sign * Q(1, 10)),
                                                    ("y", -sign * Q(2, 7))], Q(1, 11)),
                              AffineSide("two", [("x", Q(3, 17)),
                                                    ("y", Q(1, 10))], -Q(4, 3))],
                    "support_id": "independent-review",
                })

    def test_duplicate_terms_cancel_exactly_before_rounding(self):
        result = self.verify_sharp_box_correction({
            "variables": ["x"], "bounds": {"x": (-1, 1)},
            "linear_terms": [("x", 1.0)], "multipliers": [1.0],
            "support_rhs": 0,
            "sides": [AffineSide("cancellation", [("x", 10**30), ("x", 1),
                                                      ("x", -10**30)], 0)],
        })
        self.assertEqual(tuple(result.coefficients), (0.0,))
        self.assertEqual(result.rhs, 0.0)

    def test_exact_epigraph_coefficient_needs_no_finite_bound(self):
        result = certify_row_combination(
            variables=["x", "objective_aux"],
            bounds={"x": (-1, 1), "objective_aux": (-math.inf, math.inf)},
            linear_terms={"x": 1}, multipliers=[0.1], support_rhs=0,
            sides=[AffineSide("objective", [("objective_aux", -1)], 0)])
        self.assertEqual(tuple(result.coefficients), (1.0, 0.1))
        self.assertEqual(result.rhs, 0.0)

    def test_unbounded_coordinate_cannot_hide_rounding_error(self):
        for bounds in ((-math.inf, math.inf), (0, math.inf), (-math.inf, 1)):
            with self.subTest(bounds=bounds), self.assertRaises(ValueError):
                certify_row_combination(
                    variables=["x"], bounds={"x": bounds}, linear_terms={},
                    multipliers=[0.1], support_rhs=0,
                    sides=[AffineSide("row", [("x", Q(1, 10))], 0)])

    def test_wrong_multiplier_sign_rejected(self):
        with self.assertRaises(ValueError):
            certify_row_combination(
                variables=["x"], bounds={"x": (0, 1)}, linear_terms={},
                multipliers=[-1], support_rhs=0,
                sides=[AffineSide("row", [("x", 1)], 0)])


if __name__ == "__main__":
    unittest.main()
