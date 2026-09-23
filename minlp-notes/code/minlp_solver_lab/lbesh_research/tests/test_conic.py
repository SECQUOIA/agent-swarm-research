"""Analytic and original-expression checks for the conic comparison baseline."""
import math
import unittest

import pyomo.environ as p
from pyomo.gdp import Disjunct, Disjunction

from lbesh_research.conic import UnsupportedConic, solve


def two_disjuncts():
    m = p.ConcreteModel()
    m.x = p.Var(bounds=(-5, 5))
    m.y = p.Var(bounds=(-5, 5))
    m.d = Disjunct([0, 1])
    m.dj = Disjunction(expr=[m.d[0], m.d[1]])
    return m


def check_witness(test, model, result, tolerance=2e-5):
    """Evaluate original expressions, independent of the conic translation."""
    for variable in model.component_data_objects(p.Var, descend_into=(p.Block, Disjunct)):
        value = result['witness'][variable.name]
        variable.set_value(value, skip_validation=True)
        if variable.lb is not None:
            test.assertGreaterEqual(value, p.value(variable.lb) - tolerance)
        if variable.ub is not None:
            test.assertLessEqual(value, p.value(variable.ub) + tolerance)
    rows = list(model.component_data_objects(p.Constraint, active=True, descend_into=(p.Block,)))
    for dj in model.component_data_objects(Disjunction, active=True):
        test.assertAlmostEqual(sum(p.value(d.binary_indicator_var) for d in dj.disjuncts), 1, delta=tolerance)
        for d in dj.disjuncts:
            test.assertAlmostEqual(p.value(d.binary_indicator_var), round(p.value(d.binary_indicator_var)), delta=tolerance)
            if p.value(d.binary_indicator_var) > .5:
                rows.extend(d.component_data_objects(p.Constraint, active=True))
    for constraint in rows:
        value = p.value(constraint.body)
        if constraint.has_lb():
            test.assertGreaterEqual(value, p.value(constraint.lower) - tolerance)
        if constraint.has_ub():
            test.assertLessEqual(value, p.value(constraint.upper) + tolerance)


class ConicTests(unittest.TestCase):
    def test_standalone_boolean_survives_clone(self):
        m = p.ConcreteModel()
        m.x = p.Var(bounds=(0, 2))
        m.b = p.BooleanVar(initialize=False)
        m.logic = p.LogicalConstraint(expr=m.b)
        m.c = p.Constraint(expr=m.x >= 1)
        m.obj = p.Objective(expr=m.x)
        result = solve(m)
        self.assertEqual(result['boolean_witness'], {'b': True})
        self.assertAlmostEqual(result['obj'], 1, delta=1e-6)
        self.assertFalse(m.b.value)
        self.assertIsNone(m.b.get_associated_binary())

    def test_shifted_disks_and_unmodified_input(self):
        m = two_disjuncts()
        m.d[0].c = p.Constraint(expr=(m.x-1)**2 + m.y**2 <= 1)
        m.d[1].c = p.Constraint(expr=(m.x-4)**2 + m.y**2 <= 1)
        m.obj = p.Objective(expr=m.x)
        result = solve(m, mip_gap=1e-8)
        self.assertEqual(result['status'], 'optimal')
        self.assertAlmostEqual(result['obj'], 0, delta=1e-6)
        self.assertIsNone(m.x.value)
        check_witness(self, m, result)

    def test_fractional_perspective(self):
        m = two_disjuncts()
        m.x.setlb(0); m.x.setub(2); m.y.setlb(0); m.y.setub(4)
        m.d[0].c = p.Constraint(expr=m.x**2 <= m.y)
        m.d[1].cx = p.Constraint(expr=m.x == 0)
        m.d[1].cy = p.Constraint(expr=m.y == 0)
        m.half = p.Constraint(expr=m.d[0].binary_indicator_var == .5)
        m.demand = p.Constraint(expr=m.x >= 1)
        m.obj = p.Objective(expr=m.y)
        result = solve(m, relax_integrality=True)
        self.assertEqual(result['status'], 'optimal')
        self.assertAlmostEqual(result['obj'], 2, delta=1e-6)
        self.assertLessEqual(result['lb'], result['obj'] + 1e-7)
        self.assertIsNone(result['boolean_witness']['d[0].indicator_var'])
        self.assertIsNone(result['boolean_witness']['d[1].indicator_var'])

    def test_zero_weight_infeasible_disjunct(self):
        m = two_disjuncts()
        m.d[0].c = p.Constraint(expr=m.x**2 + 1 <= 0)
        m.d[1].c = p.Constraint(expr=m.x >= 3)
        m.obj = p.Objective(expr=m.x)
        result = solve(m)
        self.assertAlmostEqual(result['obj'], 3, delta=1e-6)
        self.assertAlmostEqual(result['witness']['d[0].binary_indicator_var'], 0, delta=1e-7)
        check_witness(self, m, result)

    def test_cross_terms_global_quadratic_objective(self):
        m = two_disjuncts()
        m.d[0].c = p.Constraint(expr=(m.x+m.y)**2 <= 1)
        m.d[1].c = p.Constraint(expr=m.x >= 4)
        m.global_c = p.Constraint(expr=m.x**2 + m.y**2 <= 4)
        m.obj = p.Objective(expr=(m.x-2)**2 + (m.y-2)**2)
        result = solve(m, mip_gap=1e-8)
        self.assertAlmostEqual(result['obj'], 4.5, delta=1e-5)
        check_witness(self, m, result)

    def test_norm_and_reciprocal(self):
        m = p.ConcreteModel()
        m.x = p.Var(bounds=(0, 5))
        m.y = p.Var(bounds=(0, 5))
        m.c = p.Constraint(expr=4/m.x <= m.y)
        m.obj = p.Objective(expr=p.sqrt(m.x**2+m.y**2))
        result = solve(m)
        self.assertAlmostEqual(result['obj'], math.sqrt(8), delta=1e-5)
        check_witness(self, m, result)

    def test_rank_deficient_decimal_square(self):
        m = two_disjuncts()
        m.fixed_y = p.Constraint(expr=m.y == 1)
        m.d[0].c = p.Constraint(expr=((m.x + .35*m.y)/7.3)**2 <= 1)
        m.d[1].c = p.Constraint(expr=m.x >= 4)
        m.obj = p.Objective(expr=m.x)
        result = solve(m)
        self.assertAlmostEqual(result['obj'], -5, delta=1e-6)
        check_witness(self, m, result)

    def test_maximum_bound_orientation(self):
        m = two_disjuncts()
        m.d[0].c = p.Constraint(expr=m.x**2 + m.y**2 <= 1)
        m.d[1].c = p.Constraint(expr=m.x <= 0)
        m.obj = p.Objective(expr=m.x, sense=p.maximize)
        result = solve(m)
        self.assertAlmostEqual(result['obj'], 1, delta=1e-5)
        self.assertGreaterEqual(result['lb'] + 1e-6, result['obj'])
        check_witness(self, m, result)

    def test_fixed_variable_and_inactive_disjunct(self):
        m = two_disjuncts()
        m.y.fix(2)
        m.d[0].c = p.Constraint(expr=(m.x-m.y)**2 <= 1)
        m.d[1].c = p.Constraint(expr=m.x >= 4)
        m.d[1].deactivate()
        m.obj = p.Objective(expr=m.x)
        result = solve(m)
        self.assertAlmostEqual(result['obj'], 1, delta=1e-5)
        check_witness(self, m, result)

    def test_rejects_nonconvex_and_nonquadratic_disjuncts(self):
        for expression in [lambda m: -m.x**2 <= -1, lambda m: p.exp(m.x) <= 2]:
            m = two_disjuncts()
            m.d[0].c = p.Constraint(expr=expression(m))
            m.d[1].c = p.Constraint(expr=m.x <= 0)
            m.obj = p.Objective(expr=m.x)
            with self.assertRaises(UnsupportedConic):
                solve(m)

    def test_rejects_missing_bounds_and_or(self):
        m = two_disjuncts()
        m.d[0].c = p.Constraint(expr=m.x <= 1)
        m.d[1].c = p.Constraint(expr=m.x >= 2)
        m.obj = p.Objective(expr=m.x)
        m.x.setub(None)
        with self.assertRaises(UnsupportedConic):
            solve(m)
        m.x.setub(5)
        m.dj.xor = False
        with self.assertRaises(UnsupportedConic):
            solve(m)


if __name__ == '__main__':
    unittest.main()
