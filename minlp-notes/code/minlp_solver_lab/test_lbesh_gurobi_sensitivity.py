"""Solver-free contract checks for the separate numerical sensitivity adapter."""
import json
from pathlib import Path
from types import SimpleNamespace
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch
import pyomo.environ as pe
import lbesh_gurobi_sensitivity as sensitivity


class SensitivityContracts(unittest.TestCase):
    def test_schedule_has_all_nine_cases_and_fixed_protocol(self):
        plan = sensitivity.schedule(2, 20260926)
        expected = {f"lbesh.trig.{size}.s{seed}" for size in ("small", "medium", "large")
                    for seed in (104729, 130363, 155921)}
        self.assertEqual(set(plan["instances"]), expected)
        self.assertEqual({tuple(job) for job in plan["ordered_jobs"]},
                         {(name, sensitivity.METHOD) for name in expected})
        self.assertEqual((plan["time_limit"], plan["wall_limit"], plan["threads"]), (120, 150, 1))
        self.assertEqual(plan["solver_options"], {"feasibilitytol": 1e-8})
        self.assertEqual(len(plan["metadata"]["supplementary_wrapper_sha256"]), 64)

    def test_gams_adapter_options_native_bounds_and_solution_gate(self):
        for status, nsolutions, expected_load, expected_bound in (
                (1, 1, True, True), (8, 1, True, True), (2, 1, True, False),
                (8, 0, False, True), (4, 1, False, False)):
            with self.subTest(status=status, nsolutions=nsolutions), tempfile.TemporaryDirectory() as tmp:
                model = pe.ConcreteModel()
                model.x = pe.Var(initialize=1)
                model.obj = pe.Objective(expr=model.x)
                native = {"MODELSTAT": status, "SOLVESTAT": 1, "OBJEST": .5, "OBJVAL": 1.}
                result = SimpleNamespace(solver=SimpleNamespace(termination_condition="optimal", status="ok", message=None),
                                         problem=SimpleNamespace(lower_bound=-99, upper_bound=1), solution=[{}] * nsolutions)
                opt = Mock()
                opt.available.return_value = True
                opt._parse_dat_results.return_value = ({}, native)
                def fake_solve(*args, **kwargs):
                    opt._parse_dat_results("fake.dat")
                    Path(kwargs["logfile"]).write_text("GAMS 54.3.1\nGurobi Optimizer version 13.0.2\n    FeasibilityTol  1e-08\n")
                    return result
                opt.solve.side_effect = fake_solve
                with patch.object(pe, "SolverFactory", return_value=opt), patch.object(model.solutions, "load_from") as load:
                    rec = sensitivity.solve_gams(model, Path(tmp), 1)
                self.assertEqual(rec["native_gams"], native)
                self.assertEqual(rec["dual_bound"], .5)
                self.assertEqual(rec["bound_valid"], expected_bound)
                self.assertEqual(load.called, expected_load)
                self.assertEqual(rec["has_solution"], expected_load)
                self.assertEqual((Path(tmp) / "gams/gurobi.opt").read_text(), "feasibilitytol 1e-8\n")
                kwargs = opt.solve.call_args.kwargs
                self.assertFalse(kwargs["load_solutions"])
                self.assertEqual(kwargs["io_options"], {"put_results_format": "dat"})
                self.assertEqual(kwargs["add_options"], ["option reslim=120.0;", "option threads=1;",
                                 "option optcr=0.0001;", "option optca=0.000001;", "GAMS_MODEL.optfile=1;"])
                self.assertEqual(rec["native_versions"], {"gams": "54.3.1", "gurobi": "13.0.2"})

    def test_original_witness_is_checked_and_invalid_witness_cannot_solve(self):
        def fake_solve(model, directory, sense):
            model.t[0].set_value(-.1, skip_validation=True)
            obj = pe.value(model.objective)
            return {"native_gams": {"OBJVAL": obj}, "has_solution": True, "dual_bound": obj, "bound_valid": True}
        with tempfile.TemporaryDirectory() as tmp, patch.object(sensitivity, "solve_gams", side_effect=fake_solve):
            rec = sensitivity.run_one("lbesh.trig.small.s104729", Path(tmp))
        self.assertEqual(rec["outcome"], "completed")
        self.assertFalse(rec["validation"]["feasible"])
        self.assertFalse(rec["assessment"]["solved"])
        self.assertEqual(rec["witness"]["variables"]["t[0]"], -.1)

    def test_no_incumbent_does_not_export_initialized_witness(self):
        fake = {"native_gams": {"OBJVAL": None}, "has_solution": False, "dual_bound": 0, "bound_valid": True}
        with tempfile.TemporaryDirectory() as tmp, patch.object(sensitivity, "solve_gams", return_value=fake):
            rec = sensitivity.run_one("lbesh.trig.small.s104729", Path(tmp))
        self.assertIsNone(rec["witness"])
        self.assertIsNone(rec["validation"])
        self.assertFalse(rec["assessment"]["solved"])

    def test_timeout_kills_process_group_and_ignores_partial_result(self):
        process = Mock(pid=12345)
        process.wait.side_effect = [subprocess.TimeoutExpired("worker", 150), -9]
        with tempfile.TemporaryDirectory() as tmp:
            def launch(command, **kwargs):
                Path(command[-1]).write_text(json.dumps({"outcome": "completed"}))
                return process
            with patch.object(sensitivity.subprocess, "Popen", side_effect=launch) as spawn, \
                 patch.object(sensitivity.os, "killpg", side_effect=ProcessLookupError) as kill:
                rec = sensitivity.execute("lbesh.trig.small.s104729", Path(tmp))
            self.assertEqual(rec["outcome"], "wall_timeout")
            self.assertFalse(rec["bound_valid"])
            kill.assert_called_once_with(12345, sensitivity.signal.SIGKILL)
            self.assertTrue(spawn.call_args.kwargs["start_new_session"])
            self.assertEqual(spawn.call_args.kwargs["env"]["OMP_NUM_THREADS"], "1")
            self.assertIn("lbesh_gurobi_sensitivity.py", spawn.call_args.args[0][1])
            self.assertEqual(json.loads((Path(rec["artifacts"]) / "final.json").read_text())["outcome"], "wall_timeout")


if __name__ == "__main__":
    unittest.main()
