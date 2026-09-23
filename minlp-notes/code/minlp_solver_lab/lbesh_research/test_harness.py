"""Focused witness and scoring regressions; no commercial solver required."""
import unittest
import pyomo.environ as pe
from pyomo.gdp import Disjunct, Disjunction
from .validation import capture_witness, validate_witness
from .summarize import assessed, summarize


def model():
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(0,5),initialize=1)
    m.z = pe.Var(domain=pe.Integers,bounds=(0,3),initialize=1)
    m.f = pe.Var(initialize=2)
    m.f.fix(2)
    m.d = Disjunct([0,1])
    m.d[0].c = pe.Constraint(expr=m.x >= 1)
    m.d[1].c = pe.Constraint(expr=m.x >= 3)
    m.dj = Disjunction(expr=[m.d[0],m.d[1]])
    m.d[0].indicator_var.set_value(True)
    m.d[1].indicator_var.set_value(False)
    m.logic = pe.LogicalConstraint(expr=m.d[0].indicator_var.implies(m.z >= 0))
    m.obj = pe.Objective(expr=m.x + m.z + m.f)
    return m


class WitnessTests(unittest.TestCase):
    def test_selected_rows_and_original_objective(self):
        m = model()
        result = validate_witness(m,capture_witness(m),reported_objective=4)
        self.assertTrue(result["feasible"],result)
        self.assertEqual(result["rows_checked"],1)
        self.assertEqual(result["objective"],4)

    def test_bad_fixed_integrality_and_objective(self):
        for variable,value,expected in (("x",0,"constraint"),("x",7,"upper_bound"),
                ("z",1.25,"integrality"),("f",3,"fixed_value")):
            with self.subTest(variable=variable,value=value):
                m = model(); witness = capture_witness(m)
                witness["variables"][variable] = value
                result = validate_witness(m,witness)
                self.assertFalse(result["feasible"])
                self.assertIn(expected,[r["kind"] for r in result["issues"]])
        m = model()
        self.assertFalse(validate_witness(m,capture_witness(m),reported_objective=3)["feasible"])

    def test_logic_and_disjunction(self):
        m = model(); m.logic.set_value(m.d[1].indicator_var)
        result = validate_witness(m,capture_witness(m))
        self.assertIn("logical_constraint",[r["kind"] for r in result["issues"]])
        m = model(); witness = capture_witness(m)
        witness["variables"]["d[1].binary_indicator_var"] = 1
        witness["booleans"]["d[1].indicator_var"] = True
        result = validate_witness(m,witness)
        self.assertIn("disjunction",[r["kind"] for r in result["issues"]])

    def test_missing_and_nonfinite_rejected(self):
        for value in (None,float("nan"),float("inf")):
            m = model(); witness = capture_witness(m)
            witness["variables"]["x"] = value
            self.assertFalse(validate_witness(m,witness)["feasible"])

    def test_boolean_truth_does_not_round_numeric_witness(self):
        m = model()
        m.obj.set_value(1e9*m.d[0].binary_indicator_var)
        witness = capture_witness(m)
        witness["variables"]["d[0].binary_indicator_var"] = 0.9999995
        result = validate_witness(m,witness,reported_objective=999999500)
        self.assertTrue(result["feasible"],result)
        self.assertEqual(result["objective"],999999500)


def record(instance="a",method="one",objective=10,bound=10,wall_time=2):
    return dict(instance=instance,method=method,wall_limit=10,wall_time=wall_time,
                outcome="completed",bound_valid=True,dual_bound=bound,
                validation=dict(feasible=True,objective=objective,objective_sense="minimize"))


class SummaryTests(unittest.TestCase):
    def test_two_sided_reference_and_bound(self):
        self.assertFalse(assessed(record(objective=9,bound=10))["solved"])
        ref = dict(verified=True,objective=10,evidence="analytic proof")
        self.assertFalse(assessed(record(objective=9,bound=9),reference=ref)["solved"])
        r = record(); r["bound_valid"] = False
        self.assertFalse(assessed(r)["solved"])
        r = record(); r["validation"]["objective_sense"] = "maximize"; r["dual_bound"] = 9
        self.assertTrue(assessed(r)["inconsistent_bound"])

    def test_common_set_and_penalty(self):
        records = [record("a","one",wall_time=1),record("a","two",wall_time=2),
                   record("b","one",wall_time=4),record("b","two",bound=0)]
        result = summarize(records)
        self.assertEqual(result["pairs"]["one / two"]["instances"],["a"])
        self.assertEqual(result["methods"]["two"]["par_mean"],51)
        self.assertEqual(result["methods"]["one"]["common_all_shifted_geomean"],1)

    def test_duplicate_and_unverified_reference_rejected(self):
        with self.assertRaises(ValueError):
            summarize([record(),record()])
        with self.assertRaises(ValueError):
            assessed(record(),reference=dict(objective=10))

    def test_schedule_retains_entire_missing_instance_and_method(self):
        result = summarize([record()],schedule=dict(instances=["a","b"],
            methods=["one","missing"],wall_limit=10))
        self.assertEqual(result["methods"]["one"]["scheduled"],2)
        self.assertEqual(result["methods"]["missing"]["par_mean"],100)


if __name__ == "__main__":
    unittest.main()
