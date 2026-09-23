"""Independent, solver-free review of the declared legacy initialization study."""
import hashlib
import copy
import csv
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import pyomo.environ as pe
from pyomo.gdp import Disjunct, Disjunction

import lbesh_legacy_initialization as followup
import lbesh_study_analysis as analysis


DESCEND = (pe.Block, Disjunct)


def fingerprint(model):
    return dict(
        variables=[(v.name, str(v.domain), v.bounds, v.fixed) for v in
                   model.component_data_objects(pe.Var, active=None, descend_into=DESCEND)],
        booleans=[(v.name, v.value, v.fixed) for v in
                  model.component_data_objects(pe.BooleanVar, active=None, descend_into=DESCEND)],
        expressions=[(c.name, str(c.expr), c.active) for kind in
                     (pe.Constraint, pe.Objective, pe.Expression, pe.LogicalConstraint) for c in
                     model.component_data_objects(kind, active=None, descend_into=DESCEND)],
        disjunctions=[(d.name, d.xor, d.active, tuple(c.name for c in d.disjuncts)) for d in
                      model.component_data_objects(Disjunction, active=None, descend_into=DESCEND)])


class IndependentLegacyInitializationTests(unittest.TestCase):
    def test_all_eight_only_declared_variable_values_change_and_bigm_is_identical(self):
        for name in followup.INSTANCES:
            with self.subTest(name=name):
                model = followup.primary._build(name)
                untouched = model.clone()
                before = fingerprint(model)
                old_values = {v.name: v.value for v in
                              model.component_data_objects(pe.Var, active=None, descend_into=DESCEND)}
                changes = followup.initialize_model(name, model)
                self.assertEqual(fingerprint(model), before)
                declared = {change["variable"] for change in changes}
                actual = {v.name for v in model.component_data_objects(pe.Var, active=None, descend_into=DESCEND)
                          if v.value != old_values[v.name]}
                self.assertEqual(actual, declared)
                for change in changes:
                    self.assertEqual(change["old_value"], old_values[change["variable"]])
                    var = model.find_component(change["variable"])
                    self.assertEqual(var.value, change["new_value"])
                    self.assertIn(var.value, var.domain)
                    self.assertGreaterEqual(var.value, var.lb)
                    self.assertLessEqual(var.value, var.ub)
                pe.TransformationFactory("gdp.bigm").apply_to(model)
                pe.TransformationFactory("gdp.bigm").apply_to(untouched)
                self.assertEqual(fingerprint(model), fingerprint(untouched))

    def test_unused_check_rejects_references_in_inactive_and_named_expressions(self):
        for kind in ("inactive_constraint", "inactive_disjunct", "expression", "objective", "logical"):
            with self.subTest(kind=kind):
                model = followup.primary._build("gdplib.batch_processing")
                var = model.storageTankSize_log[model.STAGES.last()]
                if kind == "inactive_constraint":
                    model.sentinel = pe.Constraint(expr=var >= var.lb)
                    model.sentinel.deactivate()
                elif kind == "inactive_disjunct":
                    model.sentinel = Disjunct()
                    model.sentinel.c = pe.Constraint(expr=var >= var.lb)
                    model.sentinel.deactivate()
                elif kind == "expression":
                    model.sentinel = pe.Expression(expr=var + 1)
                elif kind == "objective":
                    model.sentinel = pe.Objective(expr=var)
                    model.sentinel.deactivate()
                else:
                    model.sentinel = pe.LogicalConstraint(expr=var >= var.lb)
                with self.assertRaisesRegex(ValueError, "referenced by sentinel"):
                    followup.initialize_model("gdplib.batch_processing", model)
                self.assertIsNone(var.value)

    def test_all_24_workers_delegate_exact_arguments_to_frozen_adapter(self):
        for name in followup.INSTANCES:
            for method in followup.METHODS:
                with self.subTest(name=name, method=method), tempfile.TemporaryDirectory() as folder:
                    returned = dict(native_gams={"OBJVAL": None, "OBJEST": 123},
                                    has_solution=False, dual_bound=123, bound_valid=False,
                                    options={"sentinel": "preserved"})
                    with patch.object(followup.primary, "_gams", return_value=returned) as adapter:
                        record = followup.run_one(name, method, Path(folder))
                    self.assertEqual(record["outcome"], "completed")
                    self.assertEqual(adapter.call_count, 1)
                    self.assertEqual(adapter.call_args.args[1:],
                                     (method.split("-")[1], "bigm", 120.0, 1, Path(folder), 1))
                    self.assertEqual(adapter.call_args.kwargs, {})
                    self.assertEqual(record["dual_bound"], 123)
                    self.assertFalse(record["bound_valid"])
                    self.assertEqual(record["options"], {"sentinel": "preserved"})
                    self.assertIsNone(record["witness"])
                    self.assertIsNone(record["validation"])

    def test_erased_returned_unused_value_is_not_filled_after_solve(self):
        def fake(model, *args):
            model.storageTankSize_log[model.STAGES.last()].set_value(None)
            return dict(native_gams={"OBJVAL": None}, has_solution=True,
                        dual_bound=0, bound_valid=True)
        with tempfile.TemporaryDirectory() as folder, patch.object(followup.primary, "_gams", fake):
            record = followup.run_one("gdplib.batch_processing", followup.METHODS[0], Path(folder))
        self.assertEqual(record["outcome"], "completed")
        self.assertIsNone(record["witness"]["variables"]["storageTankSize_log[10]"])
        self.assertFalse(record["assessment"]["solved"])
        self.assertIn(("missing_or_nonfinite_variable", "storageTankSize_log[10]"),
                      {(r["kind"], r["name"]) for r in record["validation"]["issues"]})

    def test_metadata_complete_and_plan_matches_exact_eight_by_three(self):
        meta = followup.metadata()
        manifest = json.loads(followup.SOURCE_MANIFEST.read_text())
        analysis.check_metadata(meta, manifest, legacy=True)
        self.assertEqual(meta["source_manifest_sha256"],
                         hashlib.sha256(followup.SOURCE_MANIFEST.read_bytes()).hexdigest())
        plan = json.loads((followup.LAB / "results/lbesh_development/legacy_initialization_plan_v2.json").read_text())
        self.assertEqual(plan["metadata"]["supplementary_wrapper_sha256"],
                         hashlib.sha256(Path(followup.__file__).read_bytes()).hexdigest())
        self.assertEqual(set(map(tuple, plan["ordered_jobs"])),
                         {(name, method) for name in followup.INSTANCES for method in followup.METHODS})
        self.assertEqual(len(plan["ordered_jobs"]), 24)

    def test_analyzer_accepts_complete_initialized_schedule_and_rejects_policy_mixing(self):
        schedule = json.loads(json.dumps(followup.schedule(6, 20260927)))
        manifest = json.loads(followup.SOURCE_MANIFEST.read_text())
        study = analysis.read_json(followup.LAB / "results/lbesh_development/study_plan_v1.json")
        accepted = analysis.check_sensitivity_schedule(schedule, manifest)
        self.assertEqual(accepted.name, "legacy_initialization_plan_v2.json")
        changes = {"initialization": "Postsolve witness repair",
                   "unchanged": "Bounds and solver options may change",
                   "methods": schedule["methods"] + ["gams-gurobi-bigm-feas1e8"],
                   "ordered_jobs": list(reversed(schedule["ordered_jobs"]))}
        for field, value in changes.items():
            changed = copy.deepcopy(schedule)
            changed[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "differs from declaration"):
                analysis.check_sensitivity_schedule(changed, manifest)
        changed = copy.deepcopy(schedule)
        trig = analysis.read_json(followup.LAB / "results/lbesh_development/gurobi_trig_sensitivity_plan_v1.json")
        changed["metadata"]["supplementary_wrapper_sha256"] = trig["metadata"]["supplementary_wrapper_sha256"]
        with self.assertRaisesRegex(ValueError, "source mismatch/missing"):
            analysis.check_sensitivity_schedule(changed, manifest)
        records = [dict(instance=name, method=method, outcome="wall_timeout", bound_valid=False,
                        metadata=copy.deepcopy(schedule["metadata"]), wall_time=150, wall_limit=150,
                        solver_time_limit=120, threads=1) for name, method in schedule["ordered_jobs"]]
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "initialized.jsonl"
            artifact = Path(str(output) + ".runs")
            artifact.mkdir()
            (artifact / "schedule.json").write_text(json.dumps(schedule))
            output.write_text("".join(json.dumps(record) + "\n" for record in records))
            loaded = analysis.load_run(output, manifest, study)
            self.assertEqual(len(loaded["records"]), 24)
            self.assertEqual(Path(loaded["wrapper_plan_path"]).name, "legacy_initialization_plan_v2.json")
            records[10]["metadata"].pop("supplementary_wrapper_sha256")
            output.write_text("".join(json.dumps(record) + "\n" for record in records))
            with self.assertRaisesRegex(ValueError, "wrapper provenance mismatch/missing"):
                analysis.load_run(output, manifest, study)

    def test_csv_preserves_counts_with_missing_lp_reason_and_quoted_values(self):
        row = dict(method='a,"quoted" method', lp_end_reasons={None: 5, "stalled": 2},
                   values=[None, "a,b", 7])
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "output.csv"
            analysis.write_csv(output, [row])
            with output.open(newline="") as stream:
                loaded = list(csv.DictReader(stream))
        self.assertEqual(loaded[0]["method"], row["method"])
        self.assertEqual(json.loads(loaded[0]["lp_end_reasons"]), {"null": 5, "stalled": 2})
        self.assertEqual(json.loads(loaded[0]["values"]), row["values"])


if __name__ == "__main__":
    unittest.main()
