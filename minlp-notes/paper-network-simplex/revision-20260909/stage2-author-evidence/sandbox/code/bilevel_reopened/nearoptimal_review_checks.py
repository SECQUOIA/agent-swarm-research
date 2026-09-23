"""Independent exact algebra checks for near-optimal response compression.

Run: python code/bilevel_reopened/nearoptimal_review_checks.py
These checks support the accompanying proof review; they are not a QE solver.
"""

import unittest

import sympy as sp


class NearOptimalReviewChecks(unittest.TestCase):
    def test_measurement_fiber_preserves_nonstationary_adversary(self):
        # f=(z1^2+z2^2)/2, measurement z1+2*z2, delta=1.
        t, y = sp.symbols("t y", real=True)
        fiber_cost = ((t - 2 * y) ** 2 + y**2) / 2
        self.assertEqual(sp.solve(sp.diff(fiber_cost, y), y), [2 * t / 5])
        self.assertEqual(sp.simplify(fiber_cost.subs(y, 2 * t / 5)), t**2 / 10)
        z = sp.Matrix([sp.sqrt(10) / 5, 2 * sp.sqrt(10) / 5])
        self.assertEqual(sp.simplify((z.dot(z)) / 2), 1)
        self.assertEqual(sp.simplify(z[0] + 2 * z[1]), sp.sqrt(10))
        self.assertNotEqual(z, sp.zeros(2, 1))  # Not unconstrained-stationary.

    def test_nominal_value_must_exclude_nonglobal_stationary_points(self):
        y, t = sp.symbols("y t", real=True)
        f = (y**2 - 1) ** 2 + t**2
        self.assertEqual(set(sp.solve(sp.diff(f, y), y)), {-1, 0, 1})
        self.assertEqual(f.subs(y, 0) - f.subs(y, 1), 1)
        self.assertEqual(f.subs(y, -1), t**2)

    def test_empty_fibers_are_not_admissible(self):
        # A fixed positive leader in x*z=0 forces z=0; Tz=1 is empty.
        z = sp.symbols("z", real=True)
        self.assertEqual(sp.solve([z, z - 1], [z]), [])
        # At the rank-changing leader x=0, the same measurement is feasible.
        self.assertEqual(sp.solve([sp.Integer(0), z - 1], [z]), {z: 1})

    def test_zero_budget_convex_correspondence(self):
        # f=(z-x)^2 on [0,1], x in [0,1], delta=x^2.
        x = sp.symbols("x", nonnegative=True)
        self.assertEqual(sp.simplify((2 * x - x) ** 2 - x**2), 0)
        # Near-optimal interval [0,min(1,2x)] collapses continuously at zero.
        self.assertEqual(sp.limit(2 * x, x, 0, dir="+"), 0)

    def test_positive_budget_nonattainment_factorization(self):
        z = sp.symbols("z", real=True)
        delta = sp.Rational(1, 16)
        h = 3 * z**2 - 2 * z**3
        f0 = z**2 * (1 - z) ** 2 + delta * h
        factor = (z - 1) ** 2 * (16 * z**2 - 2 * z - 1) / 16
        self.assertEqual(sp.expand(f0 - delta - factor), 0)
        a = (1 + sp.sqrt(17)) / 16
        self.assertEqual(sp.simplify(f0.subs(z, a) - delta), 0)
        self.assertTrue(bool(a < sp.Rational(1, 3)))
        self.assertEqual(sp.diff(f0, z).subs(z, 1), 0)
        self.assertEqual(sp.diff(f0, z, 2).subs(z, 1), sp.Rational(13, 8))
        # Exact inequalities used in the proof for 0<z<=a<1/3:
        # f0'(z)/z >= 19/8 - (51/8)/3 = 1/4, strictly on this range.
        self.assertEqual(sp.expand(sp.diff(f0, z) / z),
                         4 * z**2 - sp.Rational(51, 8) * z + sp.Rational(19, 8))
        self.assertEqual(sp.Rational(19, 8) - sp.Rational(51, 8) / 3,
                         sp.Rational(1, 4))
        # h(z)<z since h/z=3z-2z^2<1 on (0,1/3).
        self.assertEqual(sp.expand(h / z), 3 * z - 2 * z**2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
