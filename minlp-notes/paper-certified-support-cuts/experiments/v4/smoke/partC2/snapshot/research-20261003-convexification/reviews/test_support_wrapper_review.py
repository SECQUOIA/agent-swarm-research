"""Independent v2 wrapper checks beyond the primitive polytope audit."""
import copy
from fractions import Fraction as Q
import math
from pathlib import Path
import sys
import unittest

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solver.support import certify_support, replay_support


class SupportWrapperReview(unittest.TestCase):
    def test_equality_simplex_exact_minimum_and_float_intercept(self):
        x, y, z = sp.symbols("x y z", real=True)
        symbols = (x, y, z)
        features = (x*x + y*y + z*z,)
        rows = [((1, 1, 1), 1), ((-1, -1, -1), -1)]
        result = certify_support(features, symbols, [(0, 1)]*3, [1.0], rows=rows)
        self.assertEqual(result.status, "complete")
        self.assertEqual(Q(result.stats["exact_support"]), Q(1, 3))
        self.assertLessEqual(Q(result.cut.rhs), Q(1, 3))
        self.assertGreater(Q(math.nextafter(result.cut.rhs, math.inf)), Q(1, 3))
        self.assertTrue(replay_support(features, symbols, [(0, 1)]*3, [1.0], rows, result.witness))
        changed = copy.deepcopy(result.witness)
        changed["rhs"] = math.nextafter(result.cut.rhs, math.inf).hex()
        self.assertFalse(replay_support(features, symbols, [(0, 1)]*3, [1.0], rows, changed))
        self.assertFalse(replay_support(features, symbols, [(0, 1)]*3, [1.0], [], result.witness))

    def test_actual_binary64_coefficient_with_rational_source(self):
        x, y, z = sp.symbols("x y z", real=True)
        features = (sp.Rational(1, 7) + (x-sp.Rational(1, 3))**2
                    + (y-sp.Rational(1, 5))**2 + (z-sp.Rational(2, 7))**2,)
        result = certify_support(features, (x, y, z), [(0, 1)]*3, [Q(1, 10)])
        self.assertEqual(result.status, "complete")
        exact = Q(float(Q(1, 10))) / 7
        self.assertEqual(Q(result.stats["exact_support"]), exact)
        self.assertLessEqual(Q(result.cut.rhs), exact)
        self.assertTrue(replay_support(features, (x, y, z), [(0, 1)]*3,
                                       [0.1], [], result.witness))

    def test_zero_weight_feature_cannot_hide_a_pole(self):
        x, y, z = sp.symbols("x y z", real=True)
        # Keep the reciprocal syntax even though its coefficient is zero.
        features = (x*x+y*y+z*z, sp.Pow(x, -1, evaluate=False))
        result = certify_support(features, (x, y, z), [(-1, 1)]*3, [1, 0])
        self.assertNotEqual(result.status, "complete")


if __name__ == "__main__":
    unittest.main()
