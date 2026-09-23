"""Opt-in tiny licensed-solver checks; five seconds and one thread per solve."""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import pyomo.environ as pe
from pyomo.gdp import Disjunct, Disjunction
from . import benchmark


@unittest.skipUnless(os.environ.get("LBESH_RUN_SOLVER_REVIEW") == "1", "set LBESH_RUN_SOLVER_REVIEW=1")
class IndependentRealAdapterTests(unittest.TestCase):
    def test_maximize_affine_gdp_across_three_adapters(self):
        environment = Path(__file__).resolve().parents[1] / "results/lbesh_development/environment.json"
        metadata = json.loads(environment.read_text())
        directories = [str(Path(metadata["executables"][name]).parent) for name in ("gams", "ipopt")]
        task_path = os.pathsep.join(directories + [os.environ["PATH"]])

        def build(_):
            m = pe.ConcreteModel()
            m.x = pe.Var(bounds=(0, 4), initialize=0)
            m.d = Disjunct([0, 1])
            m.d[0].c = pe.Constraint(expr=m.x <= 1)
            m.d[1].c = pe.Constraint(expr=m.x <= 3)
            m.dj = Disjunction(expr=[m.d[0], m.d[1]])
            m.obj = pe.Objective(expr=m.x, sense=pe.maximize)
            return m

        for method in ("lbesh-ecp-bigm-single-nonlp-nolp", "conic-hull-gurobi", "gams-shot-bigm"):
            with self.subTest(method=method), tempfile.TemporaryDirectory() as tmp, \
                 patch.object(benchmark, "_build", build), patch.dict(os.environ, {"PATH": task_path}), \
                 contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                record = benchmark.run_one("independent_max", method, 5, 1, Path(tmp))
            diagnostic = {k: v for k, v in record.items() if k != "metadata"}
            self.assertEqual(record["outcome"], "completed", diagnostic)
            self.assertTrue(record["assessment"]["solved"], diagnostic)
            self.assertLessEqual(abs(record["reported_objective"] - 3), 1e-6 + 1e-7 * 3)
            self.assertLessEqual(abs(record["dual_bound"] - 3), 1e-6 + 1e-7 * 3)

    def test_conic_standalone_boolean_witness_survives_clone(self):
        m = pe.ConcreteModel()
        m.x = pe.Var(bounds=(0, 2), initialize=1)
        m.b = pe.BooleanVar(initialize=False)
        m.logic = pe.LogicalConstraint(expr=m.b)
        m.obj = pe.Objective(expr=m.x)
        with tempfile.TemporaryDirectory() as tmp, patch.object(benchmark, "_build", return_value=m), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            record = benchmark.run_one("independent_boolean", "conic-hull-gurobi", 5, 1, Path(tmp))
        diagnostic = {k: v for k, v in record.items() if k != "metadata"}
        self.assertEqual(record["outcome"], "completed", diagnostic)
        self.assertTrue(record["assessment"]["solved"], diagnostic)
        self.assertIs(record["witness"]["booleans"]["b"], True)
        self.assertEqual(record["reported_objective"], 0)


if __name__ == "__main__":
    unittest.main()
