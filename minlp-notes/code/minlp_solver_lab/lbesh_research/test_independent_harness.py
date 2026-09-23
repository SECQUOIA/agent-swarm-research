"""Independent adversarial checks of research witness and reporting contracts."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import pyomo.environ as pe
from pyomo.gdp import Disjunct, Disjunction

from . import benchmark
from .summarize import assessed, summarize
from .validation import capture_witness, validate_witness


def fixture():
    m = pe.ConcreteModel()
    m.x = pe.Var(bounds=(0, 4), initialize=1)
    m.b = pe.BooleanVar(initialize=True)
    m.d = Disjunct([0, 1])
    m.d[0].c = pe.Constraint(expr=m.x >= 1)
    m.d[1].c = pe.Constraint(expr=m.x >= 3)
    m.dj = Disjunction(expr=[m.d[0], m.d[1]])
    m.d[0].indicator_var.set_value(True)
    m.d[1].indicator_var.set_value(False)
    m.logic = pe.LogicalConstraint(expr=m.b)
    m.obj = pe.Objective(expr=m.x)
    return m


def run_record(instance="a", method="one", objective=1, bound=1, sense="minimize"):
    return dict(instance=instance, method=method, outcome="completed", bound_valid=True,
                dual_bound=bound, wall_time=2, wall_limit=10,
                validation=dict(feasible=True, objective=objective, objective_sense=sense))


class IndependentWitnessTests(unittest.TestCase):
    def test_boolean_loading_preserves_raw_numeric_witness_for_rows(self):
        m = fixture()
        m.scaled = pe.Constraint(expr=1e9 * m.d[0].binary_indicator_var >= 1e9)
        witness = capture_witness(m)
        witness["variables"]["d[0].binary_indicator_var"] = .9999995
        result = validate_witness(m, witness)
        self.assertFalse(result["feasible"], result)
        self.assertEqual(m.d[0].binary_indicator_var.value, .9999995)
        self.assertTrue(any(i["kind"] == "constraint" and i["name"] == "scaled"
                            for i in result["issues"]), result)

    def test_transformed_standalone_boolean_uses_solver_binary(self):
        m = pe.ConcreteModel()
        m.x = pe.Var(bounds=(0, 2), initialize=1)
        m.b = pe.BooleanVar(initialize=False)
        m.logic = pe.LogicalConstraint(expr=m.b)
        m.obj = pe.Objective(expr=m.x)
        original = m.clone()
        pe.TransformationFactory("core.logical_to_linear").apply_to(m)
        m.b.get_associated_binary().set_value(1)
        self.assertFalse(m.b.value, "fixture must retain stale Boolean initialization")
        full, wanted = capture_witness(m), capture_witness(original)
        witness = {kind: {key: full[kind].get(key) for key in wanted[kind]} for kind in wanted}
        self.assertTrue(witness["booleans"]["b"])
        self.assertTrue(validate_witness(original, witness)["feasible"])

    def test_stale_explicit_boolean_is_rejected(self):
        m = fixture()
        witness = capture_witness(m)
        witness["booleans"]["d[0].indicator_var"] = False
        result = validate_witness(m, witness)
        self.assertFalse(result["feasible"])
        self.assertIn("boolean_binary_mismatch", {i["kind"] for i in result["issues"]})

    def test_fixed_boolean_cannot_be_overwritten_by_binary_loading(self):
        m = fixture()
        m.d[0].indicator_var.fix(True)
        witness = capture_witness(m)
        witness["variables"]["d[0].binary_indicator_var"] = 0
        witness["booleans"]["d[0].indicator_var"] = False
        witness["variables"]["d[1].binary_indicator_var"] = 1
        witness["booleans"]["d[1].indicator_var"] = True
        witness["variables"]["x"] = 3
        result = validate_witness(m, witness)
        self.assertFalse(result["feasible"])
        self.assertIn("fixed_boolean", {i["kind"] for i in result["issues"]})

    def test_missing_standalone_boolean_and_indicator_rejected(self):
        for section, name in (("booleans", "b"), ("variables", "d[0].binary_indicator_var")):
            with self.subTest(name=name):
                m = fixture()
                witness = capture_witness(m)
                del witness[section][name]
                self.assertFalse(validate_witness(m, witness)["feasible"])

    def test_inactive_disjunct_rows_do_not_invalidate_witness(self):
        m = fixture()
        self.assertTrue(validate_witness(m, capture_witness(m))["feasible"])

    def test_discrete_noninteger_domain_and_bad_objective(self):
        m = fixture()
        m.allowed = pe.Set(initialize=[0, 2])
        m.z = pe.Var(domain=m.allowed, initialize=0)
        witness = capture_witness(m)
        witness["variables"]["z"] = 1
        self.assertFalse(validate_witness(m, witness)["feasible"])
        m = fixture()
        self.assertFalse(validate_witness(m, capture_witness(m), reported_objective=2)["feasible"])


class IndependentSummaryTests(unittest.TestCase):
    def test_historical_summary_makes_no_validated_solved_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "legacy.jsonl"
            path.write_text(json.dumps(dict(instance="a", method="old", status="optimal",
                                            obj=-100, lb=0, time=1)) + "\n")
            script = Path(__file__).resolve().parents[1] / "summarize_gdp_final.py"
            output = subprocess.check_output([sys.executable, str(script), str(path)], text=True)
        self.assertIn("HISTORICAL, UNVALIDATED", output)
        self.assertIn("no solved or certified counts", output)
        self.assertIn("obj_present", output)

    def test_both_objective_senses_and_invalid_bounds(self):
        for sense, bound in (("minimize", 2), ("maximize", 0)):
            result = assessed(run_record(bound=bound, sense=sense))
            self.assertTrue(result["inconsistent_bound"])
            self.assertFalse(result["solved"])
        for sense in ("minimize", "maximize"):
            self.assertTrue(assessed(run_record(sense=sense))["solved"])

    def test_status_does_not_replace_bound_or_feasibility(self):
        for update in (dict(bound_valid=False), dict(dual_bound=None), dict(outcome="wall_timeout"),
                       dict(validation=dict(feasible=False, objective=1, objective_sense="minimize"))):
            record = run_record()
            record.update(update, raw_status="optimal")
            self.assertFalse(assessed(record)["solved"])

    def test_missing_sense_must_not_certify(self):
        record = run_record()
        del record["validation"]["objective_sense"]
        self.assertFalse(assessed(record)["solved"])

    def test_missing_runs_are_penalized_and_pairs_share_instances(self):
        records = [run_record("a", "one"), run_record("a", "two"), run_record("b", "one")]
        records[0]["wall_time"] = 1
        records[2]["wall_time"] = 8
        result = summarize(records)
        self.assertEqual(result["methods"]["two"]["scheduled"], 2)
        self.assertEqual(result["methods"]["two"]["par_mean"], 51)
        self.assertEqual(result["pairs"]["one / two"]["instances"], ["a"])
        self.assertEqual(result["pairs"]["one / two"]["first_shifted_geomean"], 1)

    def test_explicit_schedule_preserves_wholly_missing_methods_and_instances(self):
        schedule = dict(instances=["a", "b"], methods=["one", "two"], wall_limit=10)
        result = summarize([run_record()], schedule=schedule)
        self.assertEqual(result["instances"], ["a", "b"])
        self.assertEqual(result["methods"]["two"]["present"], 0)
        self.assertEqual(result["methods"]["two"]["par_mean"], 100)
        self.assertEqual(result["methods"]["one"]["par_mean"], 51)
        empty = summarize([], schedule=schedule)
        self.assertEqual(empty["methods"]["one"]["par_mean"], 100)
        with self.assertRaises(ValueError):
            summarize([run_record(instance="unscheduled")], schedule=schedule)


class IndependentAdapterTests(unittest.TestCase):
    def test_shuffled_schedule_is_complete_and_reproducible(self):
        names, methods = ["a", "b", "c"], ["one", "two", "three"]
        jobs = benchmark.ordered_jobs(names, methods, 17)
        self.assertEqual(len(jobs), 9)
        self.assertEqual(set(jobs), {(i, m) for i in names for m in methods})
        self.assertEqual(jobs, benchmark.ordered_jobs(names, methods, 17))
        self.assertNotEqual(jobs, benchmark.ordered_jobs(names, methods, 18))

    def test_exit_between_timeout_and_kill_does_not_abort_schedule(self):
        process = Mock(pid=123456)
        process.wait.side_effect = [subprocess.TimeoutExpired("worker", .1), 0]
        with tempfile.TemporaryDirectory() as tmp, \
             patch.object(benchmark.subprocess, "Popen", return_value=process), \
             patch.object(benchmark.os, "killpg", side_effect=ProcessLookupError):
            record = benchmark.execute("fixture", "fake", time_limit=.1, wall_limit=.1,
                                       threads=1, directory=Path(tmp))
        self.assertEqual(record["outcome"], "wall_timeout")
        self.assertFalse(record["bound_valid"])

    def test_lbesh_maximize_uses_original_sense_obj_and_bound(self):
        m = pe.ConcreteModel()
        m.x = pe.Var(bounds=(0, 4), initialize=3)
        m.obj = pe.Objective(expr=m.x, sense=pe.maximize)
        class FakeLBESH:
            def __init__(self, model, **options):
                self.incumbent = {id(model.x): 3}
            def solve(self, **kwargs):
                values = dict(obj=3., bound=4., lb=3., ub=4., status="time_limit")
                return SimpleNamespace(**values, as_dict=lambda: values)
        with tempfile.TemporaryDirectory() as tmp, patch.object(benchmark, "_build", return_value=m), \
             patch("lbesh.solver.LBESH", FakeLBESH), patch.object(pe, "SolverFactory") as factory:
            factory.return_value.available.return_value = True
            result = benchmark.run_one("fixture", "lbesh-ecp-bigm-single", 5, 1, Path(tmp))
        self.assertEqual(result["outcome"], "completed", result)
        self.assertEqual(result["reported_objective"], 3.)
        self.assertEqual(result["dual_bound"], 4.)
        self.assertTrue(result["validation"]["feasible"], result)
        self.assertFalse(result["assessment"]["solved"])

    def test_native_gams_status_and_objest_override_generic_bound(self):
        from pyomo.opt.results import SolverResults
        for modelstat, valid in ((1, True), (2, False), (7, True), (8, True), (4, False)):
            with self.subTest(modelstat=modelstat), tempfile.TemporaryDirectory() as tmp:
                m = pe.ConcreteModel()
                m.x = pe.Var(bounds=(0, 4), initialize=1)
                m.obj = pe.Objective(expr=m.x)
                result = SolverResults()
                result.problem.lower_bound = 123
                result.problem.upper_bound = 456
                opt = SimpleNamespace(available=lambda **kw: True)
                opt._parse_dat_results = lambda *a: ({}, {"MODELSTAT": modelstat, "SOLVESTAT": 1, "OBJEST": .5, "OBJVAL": 1})
                def solve(*args, **kwargs):
                    opt._parse_dat_results(None)
                    return result
                opt.solve = solve
                with patch.object(pe, "SolverFactory", return_value=opt):
                    record = benchmark._gams(m, "shot", "bigm", 5, 1, Path(tmp), 1)
                self.assertEqual(record["dual_bound"], .5)
                self.assertEqual(record["bound_valid"], valid)
                self.assertEqual(record["native_gams"]["MODELSTAT"], modelstat)

    @unittest.skipUnless(sys.platform.startswith("linux"), "process group regression uses /proc")
    def test_wall_timeout_kills_worker_and_child_with_file_logs(self):
        real_popen = subprocess.Popen
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            child_pid = root / "child.pid"
            code = ("import subprocess,sys,time; from pathlib import Path; "
                    "p=subprocess.Popen([sys.executable,'-c','import time; time.sleep(20)']); "
                    f"Path({str(child_pid)!r}).write_text(str(p.pid)); "
                    "print('x'*200000,flush=True); time.sleep(20)")
            def spawn(_cmd, **kwargs):
                return real_popen([sys.executable, "-c", code], **kwargs)
            with patch.object(benchmark.subprocess, "Popen", side_effect=spawn):
                result = benchmark.execute("fixture", "fake", time_limit=.5, wall_limit=.5,
                                           threads=1, directory=root)
            self.assertEqual(result["outcome"], "wall_timeout")
            self.assertLess(result["wall_time"], 3)
            self.assertEqual(result["exit_code"], -signal.SIGKILL)
            self.assertTrue(child_pid.exists(), "child did not start")
            pid = int(child_pid.read_text())
            for _ in range(20):
                stat = Path(f"/proc/{pid}/stat")
                if not stat.exists() or stat.read_text().split()[2] == "Z":
                    break
                time.sleep(.05)
            else:
                os.kill(pid, signal.SIGKILL)
                self.fail("child process survived process-group timeout")
            self.assertGreater((Path(result["artifacts"]) / "stdout.log").stat().st_size, 100000)
            self.assertEqual(json.loads((Path(result["artifacts"]) / "final.json").read_text())["outcome"], "wall_timeout")


if __name__ == "__main__":
    unittest.main()
