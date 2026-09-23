"""Fresh-review checks for the separate Gurobi sensitivity; no solver is run."""
from pathlib import Path
from types import SimpleNamespace
import hashlib
import json
import signal
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import contextlib
import io
import copy

import pyomo.environ as pe

import lbesh_gurobi_sensitivity as sensitivity
import lbesh_study_analysis as analysis
from lbesh_research import benchmark
from lbesh_research.instances import MANIFEST, build


class FakeGams:
    def __init__(self, status=7):
        self.native = {"MODELSTAT": status, "SOLVESTAT": 3, "OBJEST": 1.25, "OBJVAL": 2.0}
        self.arguments = None
        self.rows = None

    def available(self, **kwargs):
        return True

    def _parse_dat_results(self, *args):
        return {}, self.native

    def solve(self, model, **kwargs):
        self.arguments = kwargs
        Path(kwargs["logfile"]).write_text("GAMS 54.3.1\nGurobi Optimizer version 13.0.2\n  FeasibilityTol 1e-08\n")
        self.rows = [(row.name, str(row.expr)) for row in
                     model.component_data_objects(pe.Constraint, active=True)]
        self._parse_dat_results(None)
        return SimpleNamespace(
            solution=[],
            solver=SimpleNamespace(termination_condition="maxTimeLimit", status="ok", message="mock"),
            problem=SimpleNamespace(lower_bound=-999, upper_bound=999))


class SensitivityIndependentReview(unittest.TestCase):
    def test_all_nine_schedule_and_frozen_adapter_hash(self):
        expected = sorted(name for name, row in MANIFEST.items() if row["family"] == "trig")
        plan = sensitivity.schedule(6, 20260926)
        self.assertEqual(len(expected), 9)
        self.assertEqual(plan["instances"], expected)
        self.assertEqual(set(map(tuple, plan["ordered_jobs"])),
                         {(name, sensitivity.METHOD) for name in expected})
        self.assertEqual(plan["time_limit"], 120)
        self.assertEqual(plan["wall_limit"], 150)
        self.assertEqual(plan["threads"], 1)
        self.assertEqual(plan["validator_tolerances"],
                         {"absolute": 1e-6, "relative": 1e-7, "integrality": 1e-6})
        self.assertEqual(plan["metadata"]["supplementary_wrapper_sha256"],
                         hashlib.sha256(Path(sensitivity.__file__).read_bytes()).hexdigest())
        manifest = json.loads(Path("results/lbesh_development/source_v1_manifest.json").read_text())
        self.assertEqual(sensitivity.COPIED_ADAPTER_SHA256,
                         manifest["files"]["code/minlp_solver_lab/lbesh_research/benchmark.py"])

    def test_native_adapter_diff_is_exactly_tolerance_optfile(self):
        name = "lbesh.trig.small.s104729"
        original, changed = FakeGams(), FakeGams()
        with tempfile.TemporaryDirectory() as folder:
            primary_dir, sensitivity_dir = Path(folder) / "primary", Path(folder) / "sensitivity"
            primary_dir.mkdir()
            sensitivity_dir.mkdir()
            with patch.object(pe, "SolverFactory", return_value=original):
                first = benchmark._gams(build(name), "gurobi", "bigm", 120.0, 1, primary_dir, 1)
            with patch.object(pe, "SolverFactory", return_value=changed):
                second = sensitivity.solve_gams(build(name), sensitivity_dir, 1)
            self.assertEqual(original.rows, changed.rows)
            old, new = dict(original.arguments), dict(changed.arguments)
            for key in ("logfile", "tmpdir"):
                old.pop(key)
                new.pop(key)
            self.assertEqual(new.pop("add_options"), old.pop("add_options") + ["GAMS_MODEL.optfile=1;"])
            self.assertEqual(old, new)
            self.assertEqual((sensitivity_dir / "gams/gurobi.opt").read_text(), "feasibilitytol 1e-8\n")
            for key in ("native_gams", "dual_bound", "bound_valid", "has_solution", "raw_lower_bound",
                        "raw_upper_bound", "bound_source", "raw_status", "raw_solver_status"):
                self.assertEqual(first[key], second[key], key)
            self.assertEqual(second["dual_bound"], 1.25)  # Native OBJEST, not generic -999.

    def test_local_status_does_not_supply_global_bound(self):
        for status in (2, 4, 5, 6, 10, 13):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as folder, \
                 patch.object(pe, "SolverFactory", return_value=FakeGams(status)):
                result = sensitivity.solve_gams(build(sensitivity.INSTANCES[0]), Path(folder), 1)
                self.assertFalse(result["bound_valid"])
                self.assertFalse(result["has_solution"])

    def test_original_model_validation_catches_bad_numeric_witness(self):
        def fake_solve(model, workdir, sense):
            var = next(v for v in model.component_data_objects(pe.Var) if not v.is_binary())
            var.set_value(float(pe.value(var.ub)) + 100, skip_validation=True)
            objective = next(model.component_data_objects(pe.Objective, active=True))
            return dict(has_solution=True, native_gams={"OBJVAL": float(pe.value(objective))},
                        dual_bound=-1e5, bound_valid=True)
        with tempfile.TemporaryDirectory() as folder, patch.object(sensitivity, "solve_gams", fake_solve):
            record = sensitivity.run_one(sensitivity.INSTANCES[0], Path(folder))
        self.assertEqual(record["outcome"], "completed")
        self.assertFalse(record["validation"]["feasible"])
        self.assertFalse(record["assessment"]["solved"])
        self.assertIn("upper_bound", {issue["kind"] for issue in record["validation"]["issues"]})

    def test_missing_or_wrong_effective_tolerance_is_rejected(self):
        for log in ("No effective parameter reported\n", " FeasibilityTol 1e-06\n"):
            class WrongLog(FakeGams):
                def solve(self, model, **kwargs):
                    result = super().solve(model, **kwargs)
                    Path(kwargs["logfile"]).write_text(log)
                    return result
            with self.subTest(log=log), tempfile.TemporaryDirectory() as folder, \
                 patch.object(pe, "SolverFactory", return_value=WrongLog()):
                with self.assertRaisesRegex(RuntimeError, "does not confirm"):
                    sensitivity.solve_gams(build(sensitivity.INSTANCES[0]), Path(folder), 1)

    def test_cli_rejects_overwrite_and_excess_parallelism_before_launch(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "retained.jsonl"
            output.write_text("retain original data\n")
            for extra in ([], ["--parallel", "7"], ["--worker", sensitivity.INSTANCES[0]]):
                with self.subTest(extra=extra), \
                     patch.object(sensitivity.sys, "argv", ["sensitivity", "--out", str(output)] + extra), \
                     patch.object(sensitivity, "execute") as execute, \
                     patch.object(sensitivity, "run_one") as worker, \
                     contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as raised:
                        sensitivity.main()
                    self.assertEqual(raised.exception.code, 2)
                    execute.assert_not_called()
                    worker.assert_not_called()
                    self.assertEqual(output.read_text(), "retain original data\n")

    def test_timeout_kills_process_group_ignores_partial_result(self):
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder)
            class Process:
                pid = 543210
                waited = False
                def wait(self, timeout=None):
                    if timeout is not None:
                        raise subprocess.TimeoutExpired("mock", timeout)
                    return -9
            calls = []
            def popen(command, **kwargs):
                calls.append((command, kwargs))
                Path(command[-1]).write_text(json.dumps({"outcome": "completed", "assessment": {"solved": True}}))
                return Process()
            with patch.object(sensitivity.subprocess, "Popen", popen), \
                 patch.object(sensitivity.os, "killpg", side_effect=ProcessLookupError) as kill:
                result = sensitivity.execute(sensitivity.INSTANCES[0], directory)
            kill.assert_called_once_with(Process.pid, signal.SIGKILL)
            self.assertEqual(result["outcome"], "wall_timeout")
            self.assertFalse(result["bound_valid"])
            self.assertNotIn("assessment", result)
            self.assertTrue(calls[0][1]["start_new_session"])
            for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
                self.assertEqual(calls[0][1]["env"][key], "1")
            final = json.loads((Path(result["artifacts"]) / "final.json").read_text())
            self.assertEqual(final, result)


class SensitivityAnalysisIndependentReview(unittest.TestCase):
    def setUp(self):
        self.manifest = analysis.read_json(analysis.LAB / "results/lbesh_development/source_v1_manifest.json")
        self.plan = analysis.read_json(analysis.LAB / "results/lbesh_development/study_plan_v1.json")
        self.schedule = json.loads(json.dumps(sensitivity.schedule(6, 20260926)))

    def test_schedule_mutations_and_changed_current_wrapper_fail_closed(self):
        mutations = {
            "order_seed": 20260927,
            "solver_options": {"feasibilitytol": 1e-6},
            "validator_tolerances": {"absolute": .1, "relative": .1, "integrality": .1},
            "primary_results_unchanged": False,
            "ordered_jobs": list(reversed(self.schedule["ordered_jobs"])),
        }
        for field, value in mutations.items():
            changed = copy.deepcopy(self.schedule)
            changed[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "differs from declaration"):
                analysis.check_sensitivity_schedule(changed, self.manifest)
        digest = analysis.digest
        def changed_hash(path):
            return "0" * 64 if Path(path).name == "lbesh_gurobi_sensitivity.py" else digest(path)
        with patch.object(analysis, "digest", changed_hash), \
             self.assertRaisesRegex(ValueError, "source mismatch/missing"):
            analysis.check_sensitivity_schedule(self.schedule, self.manifest)

    def test_each_worker_outcome_requires_same_hashes(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "sensitivity.jsonl"
            artifact = Path(str(output) + ".runs")
            artifact.mkdir()
            (artifact / "schedule.json").write_text(json.dumps(self.schedule))
            records = [dict(instance=name, method=method, outcome="wall_timeout",
                            metadata=copy.deepcopy(self.schedule["metadata"]),
                            wall_time=150, wall_limit=150, solver_time_limit=120, threads=1)
                       for name, method in self.schedule["ordered_jobs"]]
            output.write_text("".join(json.dumps(record) + "\n" for record in records))
            loaded = analysis.load_run(output, self.manifest, self.plan)
            self.assertEqual(len(loaded["records"]), 9)
            self.assertTrue(loaded["wrapper_plan_sha256"])
            for outcome in ("completed", "error", "unavailable", "crash", "wall_timeout"):
                for field in ("supplementary_wrapper_sha256", "copied_adapter_source_sha256"):
                    changed = copy.deepcopy(records)
                    changed[4]["outcome"] = outcome
                    changed[4]["metadata"][field] = "different"
                    output.write_text("".join(json.dumps(record) + "\n" for record in changed))
                    with self.subTest(outcome=outcome, field=field), \
                         self.assertRaisesRegex(ValueError, "wrapper provenance mismatch/missing"):
                        analysis.load_run(output, self.manifest, self.plan)

    def test_ordinary_primary_worker_timeout_metadata_exemption_is_preserved(self):
        name = sensitivity.INSTANCES[0]
        method = "gams-gurobi-bigm"
        schedule = dict(instances=[name], methods=[method], time_limit=120, wall_limit=150,
                        threads=1, parallel=1, order_seed=42, ordered_jobs=[[name, method]],
                        metadata=benchmark._metadata())
        record = dict(instance=name, method=method, outcome="wall_timeout", wall_time=150,
                      wall_limit=150, solver_time_limit=120, threads=1)
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "ordinary.jsonl"
            artifact = Path(str(output) + ".runs")
            artifact.mkdir()
            (artifact / "schedule.json").write_text(json.dumps(schedule))
            output.write_text(json.dumps(record) + "\n")
            result = analysis.load_run(output, self.manifest, self.plan)
        self.assertIsNone(result["wrapper_plan_sha256"])
        self.assertEqual(result["records"][0]["outcome"], "wall_timeout")


if __name__ == "__main__":
    unittest.main()
