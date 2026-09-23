"""Independent analytic regressions for the quadratic GDP conic baseline."""
import unittest
import pyomo.environ as p
from pyomo.gdp import Disjunct, Disjunction
from lbesh_research.conic import UnsupportedConic, solve


def model():
    m = p.ConcreteModel()
    m.x = p.Var(bounds=(-4, 4))
    m.d = Disjunct([0, 1])
    m.dj = Disjunction(expr=[m.d[0], m.d[1]])
    return m


class IndependentConicTests(unittest.TestCase):
    def solve(self, m, **kwargs):
        return solve(m, time_limit=15, threads=1, mip_gap=1e-8, **kwargs)

    def test_shifted_square_fractional_hull(self):
        # At weights (1/4,3/4), intervals [1,3] and [-3,-1]
        # have weighted lower endpoint 1/4 - 9/4 = -2.
        m = model()
        m.d[0].c = p.Constraint(expr=(m.x - 2)**2 <= 1)
        m.d[1].c = p.Constraint(expr=(m.x + 2)**2 <= 1)
        m.half = p.Constraint(expr=m.d[0].binary_indicator_var == .25)
        m.o = p.Objective(expr=m.x)
        r = self.solve(m, relax_integrality=True)
        self.assertEqual(r['status'], 'optimal')
        self.assertAlmostEqual(r['obj'], -2, delta=2e-6)
        self.assertLessEqual(r['lb'], r['obj'] + 2e-6)

    def test_disjunct_indicator_reference_is_refused(self):
        # Without fixing branch copies, this incorrectly gives 0, not 1.5.
        m = model()
        m.x.setlb(0)
        m.d[0].c = p.Constraint(expr=m.x >= m.d[0].binary_indicator_var)
        m.d[1].c = p.Constraint(expr=m.x >= 2*m.d[1].binary_indicator_var)
        m.half = p.Constraint(expr=m.d[0].binary_indicator_var == .5)
        m.o = p.Objective(expr=m.x)
        with self.assertRaises(UnsupportedConic):
            self.solve(m, relax_integrality=True)

    def test_sos_constraints_are_not_silently_dropped(self):
        m = p.ConcreteModel()
        m.x = p.Var([0, 1], bounds=(0, 1))
        m.sos = p.SOSConstraint(var=m.x, sos=1)
        m.o = p.Objective(expr=sum(m.x.values()), sense=p.maximize)
        with self.assertRaises(UnsupportedConic):
            self.solve(m)

    def test_conditional_objective_is_not_silently_dropped(self):
        m = model()
        m.o = p.Objective(expr=m.x)
        m.d[0].conditional_objective = p.Objective(expr=-m.x)
        with self.assertRaises(UnsupportedConic):
            self.solve(m)

    def test_empty_quadratic_branch_at_zero_weight(self):
        m = model()
        m.d[0].c = p.Constraint(expr=(m.x + .3)**2 <= -1)
        m.d[1].c = p.Constraint(expr=m.x >= 2)
        m.o = p.Objective(expr=m.x)
        r = self.solve(m, relax_integrality=True)
        self.assertAlmostEqual(r['obj'], 2, delta=2e-6)
        self.assertAlmostEqual(r['witness']['d[0].binary_indicator_var'], 0, delta=2e-6)

    def test_tiny_indefiniteness_is_refused(self):
        m = model()
        m.z = p.Var(bounds=(-2, 2))
        m.d[0].c = p.Constraint(expr=m.x**2 + 2.000000000001*m.x*m.z + m.z**2 <= 1)
        m.d[1].c = p.Constraint(expr=m.x >= 2)
        m.o = p.Objective(expr=m.x)
        with self.assertRaises(UnsupportedConic):
            self.solve(m)

    def test_expanded_psd_matches_original_witness(self):
        m = model()
        m.z = p.Var(bounds=(-2, 2))
        m.fixed_z = p.Constraint(expr=m.z == 1)
        m.d[0].c = p.Constraint(expr=m.x**2 + 2*m.x*m.z + m.z**2 <= 1)
        m.d[1].c = p.Constraint(expr=m.x >= 2)
        m.o = p.Objective(expr=m.x)
        r = self.solve(m)
        self.assertAlmostEqual(r['obj'], -2, delta=2e-6)
        for v in m.component_data_objects(p.Var, descend_into=(p.Block, Disjunct)):
            v.set_value(r['witness'][v.name], skip_validation=True)
        self.assertLessEqual(p.value(m.d[0].c.body), p.value(m.d[0].c.upper) + 2e-6)
        self.assertAlmostEqual(p.value(m.d[0].binary_indicator_var), 1, delta=2e-6)

    def test_global_norm_reciprocal_maximum(self):
        m = p.ConcreteModel()
        m.x = p.Var(bounds=(0, 4))
        m.c = p.Constraint(expr=p.sqrt((m.x - 1)**2 + 1) <= 2)
        m.reciprocal = p.Constraint(expr=1/(m.x + 1) <= 1)
        m.o = p.Objective(expr=m.x, sense=p.maximize)
        r = self.solve(m)
        xstar = 1 + 3**.5
        self.assertAlmostEqual(r['witness']['x'], xstar, delta=2e-5)
        self.assertAlmostEqual(r['obj'], xstar, delta=2e-6)
        self.assertGreaterEqual(r['lb'], r['obj'] - 2e-6)

    def test_reciprocal_wrong_domain_refused(self):
        m = p.ConcreteModel()
        m.x = p.Var(bounds=(-1, 2))
        m.o = p.Objective(expr=1/m.x)
        with self.assertRaises(UnsupportedConic):
            self.solve(m)

    def test_lower_convex_bound_refused(self):
        m = model()
        m.d[0].c = p.Constraint(expr=m.x**2 >= 1)
        m.d[1].c = p.Constraint(expr=m.x >= 2)
        m.o = p.Objective(expr=m.x)
        with self.assertRaises(UnsupportedConic):
            self.solve(m)

    def test_infeasible_status_has_no_witness(self):
        m = p.ConcreteModel()
        m.x = p.Var(bounds=(0, 1))
        m.c = p.Constraint(expr=m.x >= 2)
        m.o = p.Objective(expr=m.x)
        r = self.solve(m)
        self.assertEqual(r['status'], 'infeasible')
        self.assertIsNone(r['obj'])
        self.assertEqual(r['witness'], {})


if __name__ == '__main__':
    unittest.main()
