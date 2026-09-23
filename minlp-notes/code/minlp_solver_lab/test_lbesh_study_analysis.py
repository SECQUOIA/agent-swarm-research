"""Targeted failure-boundary tests for the post-freeze analysis only."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import lbesh_study_analysis as a


def record(name="toy", method="lbesh-esh-hull-single", objective=10., bound=10., sense="minimize"):
    validation = dict(feasible=True, objective=objective, objective_sense=sense, issues=[])
    return dict(instance=name, method=method, outcome="completed", raw_status="optimal",
                validation=validation, witness={"variables":{"x":objective}}, dual_bound=bound,
                bound_valid=True, wall_time=2., wall_limit=150., solver_time_limit=120., threads=1)


def run(records):
    return dict(label="toy", schedule=dict(instances=sorted({r["instance"] for r in records}),
        methods=sorted({r["method"] for r in records}), wall_limit=150), records=records)


class AuditTests(unittest.TestCase):
    def test_other_feasible_witness_refutes_closed_bound_both_senses(self):
        for sense,best in (("minimize",8.),("maximize",12.)):
            bad=record(sense=sense)
            good=record(method="other",objective=best,bound=None,sense=sense)
            r=run([bad,good])
            with patch.object(a,"revalidate",side_effect=lambda r:r["validation"]):
                warnings=a.audit([r],[])
            self.assertFalse(bad["audit_assessment"]["solved"])
            self.assertTrue(warnings)
            self.assertEqual(bad["audit_issues"][0]["kind"],"bound_contradicts_feasible_witness")
            self.assertTrue(good["audit_assessment"]["feasible"])

    def test_revalidation_overrides_saved_feasible_and_score(self):
        r=record()
        with patch.object(a,"revalidate",return_value=dict(feasible=False,objective=10.,
                        objective_sense="minimize",issues=[dict(kind="constraint")])):
            warnings=a.audit([run([r])],[])
        self.assertFalse(r["audit_assessment"]["solved"])
        self.assertEqual(warnings[0]["kind"],"validation_disagreement")

    def test_par10_uses_failure_and_pair_uses_identical_common_instances(self):
        rs=[]
        for name, method, time, solved in [
            ("a","lbesh-esh-hull-single",2,True),("b","lbesh-esh-hull-single",4,False),
            ("a","lbesh-ecp-hull-single",8,True),("b","lbesh-ecp-hull-single",10,True)]:
            r=record(name,method,bound=10 if solved else 0)
            r["wall_time"]=time
            rs.append(r)
        r=run(rs)
        with patch.object(a,"revalidate",side_effect=lambda r:r["validation"]):
            a.audit([r],[])
        summaries,pairs,_,_=a.tables([r])
        esh=next(x for x in summaries if x["dimension"]=="all" and "esh-hull" in x["method"])
        pair=next(x for x in pairs if x["dimension"]=="all")
        self.assertEqual(esh["par10_mean"],751)
        self.assertEqual(pair["common_instances"],["a"])
        self.assertAlmostEqual(pair["esh_over_ecp_shifted_geomean"],.25)

    def test_no_witness_never_becomes_solved(self):
        r=record();r.pop("witness")
        a.audit([run([r])],[])
        self.assertFalse(r["audit_assessment"]["solved"])


class ScheduleTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/"input.jsonl"
        self.schedule=dict(instances=["toy"],methods=["m"],ordered_jobs=[["toy","m"]],
                           wall_limit=150,time_limit=120,threads=1,parallel=1,order_seed=1)
        self.plan=dict(primary_schedule=self.schedule,repetitions=dict(order_seeds=[],methods=[]),
                       wall_limit=150,solver_time_limit=120,threads=1,max_workers=6)
        self.manifest={}
        target=Path(str(self.path)+".runs");target.mkdir()
        (target/"schedule.json").write_text(json.dumps(self.schedule))

    def test_wholly_missing_method_is_rejected(self):
        self.path.write_text("")
        with patch.object(a,"check_metadata"):
            with self.assertRaisesRegex(ValueError,"Incomplete schedule"):
                a.load_run(self.path,self.manifest,self.plan)

    def test_duplicate_record_is_rejected(self):
        r=record(method="m");r["metadata"]={"source_sha256":{}}
        self.path.write_text((json.dumps(r)+"\n")*2)
        self.schedule["metadata"]={}
        Path(str(self.path)+".runs/schedule.json").write_text(json.dumps(self.schedule))
        with patch.object(a,"check_metadata"):
            with self.assertRaisesRegex(ValueError,"Duplicate or unscheduled"):
                a.load_run(self.path,self.manifest,self.plan)

    def test_missing_source_fingerprint_is_rejected(self):
        manifest={"files":{a.PREFIX+"gdp_instances.py":"frozen",a.PREFIX+"uv.lock":"lock"}}
        with self.assertRaisesRegex(ValueError,"source mismatch/missing"):
            a.check_metadata({"source_sha256":{},"uv_lock_sha256":"lock"},manifest)

    def test_timeout_without_worker_metadata_remains_failure(self):
        r=record(method="m");r.pop("witness");r.pop("validation")
        r.update(outcome="wall_timeout",bound_valid=False)
        self.path.write_text(json.dumps(r)+"\n")
        with patch.object(a,"check_metadata"):
            loaded=a.load_run(self.path,self.manifest,self.plan)
        a.audit([loaded],[])
        self.assertEqual(a.category(loaded["records"][0]),"wall_timeout")


class SupplementaryTests(unittest.TestCase):
    def test_declared_batch_coverage_and_order_validation(self):
        supplement=a.read_json(a.LAB/"results/lbesh_development/supplementary_plan_v1.json")
        runs=[]
        for job in supplement["jobs"]:
            if "instances" not in job:
                continue
            seed=int(job["command"][job["command"].index("--order-seed")+1])
            jobs=list(a.itertools.product(job["instances"],job["methods"]))
            a.random.Random(seed).shuffle(jobs)
            runs.append(dict(label=job["name"],schedule=dict(instances=job["instances"],
                methods=job["methods"],order_seed=seed,ordered_jobs=jobs)))
        coverage=a.supplementary_coverage(runs,supplement)
        self.assertTrue(all(r["supplied"] for r in coverage if r["kind"] == "benchmark"))
        self.assertFalse(next(r for r in a.supplementary_coverage(runs[:-1],supplement) if r["name"] == runs[-1]["label"])["supplied"])
        runs[-1]["schedule"]["ordered_jobs"].reverse()
        with self.assertRaisesRegex(ValueError,"shuffled order"):
            a.supplementary_coverage(runs,supplement)

    def test_required_diagnostic_fingerprints_cannot_be_omitted(self):
        with self.assertRaisesRegex(ValueError,"source mismatch/missing"):
            a.check_diagnostic_sources({"source_sha256":{}})
        data=a.read_json(a.LAB/"results/lbesh_development/oracle_diagnostic.json")
        a.check_diagnostic_sources(data)


class SensitivityProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/"sensitivity.jsonl"
        self.manifest=a.read_json(a.LAB/"results/lbesh_development/source_v1_manifest.json")
        self.plan=a.read_json(a.LAB/"results/lbesh_development/study_plan_v1.json")
        self.schedule=a.read_json(a.LAB/"results/lbesh_development/gurobi_trig_sensitivity_plan_v1.json")
        self.rows=[dict(instance=name,method=method,outcome="wall_timeout",bound_valid=False,
            metadata=copy.deepcopy(self.schedule["metadata"]),wall_time=150.,wall_limit=150.,
            solver_time_limit=120.,threads=1) for name,method in self.schedule["ordered_jobs"]]
        Path(str(self.path)+".runs").mkdir()

    def save(self):
        self.path.write_text("".join(json.dumps(r)+"\n" for r in self.rows))
        Path(str(self.path)+".runs/schedule.json").write_text(json.dumps(self.schedule))

    def test_wrapped_timeout_requires_worker_wrapper_and_adapter_hashes(self):
        self.save()
        loaded=a.load_run(self.path,self.manifest,self.plan)
        self.assertIsNotNone(loaded["wrapper_plan_sha256"])
        for field in ("supplementary_wrapper_sha256","copied_adapter_source_sha256"):
            original=self.rows[0]["metadata"].pop(field)
            self.save()
            with self.assertRaisesRegex(ValueError,"wrapper provenance mismatch/missing"):
                a.load_run(self.path,self.manifest,self.plan)
            self.rows[0]["metadata"][field]=original
        self.rows[0].pop("metadata")
        self.save()
        with self.assertRaisesRegex(ValueError,"wrapper provenance mismatch/missing"):
            a.load_run(self.path,self.manifest,self.plan)

    def test_sensitivity_schedule_requires_declared_current_wrapper_and_all_nine(self):
        for field in ("supplementary_wrapper_sha256","copied_adapter_source_sha256"):
            changed=copy.deepcopy(self.schedule)
            changed["metadata"][field]="incorrect"
            with self.assertRaisesRegex(ValueError,"source mismatch/missing"):
                a.check_sensitivity_schedule(changed,self.manifest)
        changed=copy.deepcopy(self.schedule);changed["instances"].pop()
        with self.assertRaisesRegex(ValueError,"Sensitivity schedule differs"):
            a.check_sensitivity_schedule(changed,self.manifest)


class LegacyExportAndWrapperTests(unittest.TestCase):
    def test_mixed_missing_and_present_lp_reason_keys_export(self):
        import csv
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"table.csv"
            a.write_csv(path,[dict(method="method",lp_end_reasons={None:4,"stalled":23})])
            with path.open() as f:
                row=next(csv.DictReader(f))
            self.assertEqual(json.loads(row["lp_end_reasons"]),{"null":4,"stalled":23})

    def test_initialization_routes_only_to_its_declared_eight_by_three_plan(self):
        manifest=a.read_json(a.LAB/"results/lbesh_development/source_v1_manifest.json")
        declaration=a.LAB/"results/lbesh_development/legacy_initialization_plan_v2.json"
        plan=a.read_json(declaration)
        self.assertEqual(a.check_sensitivity_schedule(plan,manifest),declaration)
        for field in ("initialization","unchanged","validator_tolerances"):
            changed=copy.deepcopy(plan);changed[field]="modified"
            with self.assertRaisesRegex(ValueError,"schedule differs"):
                a.check_sensitivity_schedule(changed,manifest)
        changed=copy.deepcopy(plan);changed["methods"].pop()
        with self.assertRaisesRegex(ValueError,"schedule differs"):
            a.check_sensitivity_schedule(changed,manifest)
        changed=copy.deepcopy(plan);changed["metadata"].pop("supplementary_wrapper_sha256")
        with self.assertRaisesRegex(ValueError,"source mismatch/missing"):
            a.check_sensitivity_schedule(changed,manifest)


if __name__ == "__main__":
    unittest.main()
