"""Independent adversarial checks for the post-freeze study analyzer.

No optimization is invoked. Synthetic outcomes exercise the analysis rules;
one saved real witness exercises original-model revalidation.
"""
import copy
import itertools
import json
import math
from pathlib import Path
import random
import tempfile
import unittest
from unittest.mock import patch

import lbesh_study_analysis as a


def row(name="toy", method="lbesh-esh-hull-single", sense="minimize", obj=10., bound=10., time=3.):
    return dict(instance=name, method=method, outcome="completed", raw_status="optimal",
                validation=dict(feasible=True, objective=obj, objective_sense=sense, issues=[]),
                witness={"variables": {"x": obj}}, dual_bound=bound, bound_valid=True,
                wall_time=time, wall_limit=150., solver_time_limit=120., threads=1)


def run(rows, seed=7):
    return dict(label=f"run{seed}", schedule=dict(
        instances=sorted({r["instance"] for r in rows}),
        methods=sorted({r["method"] for r in rows}), wall_limit=150., order_seed=seed), records=rows)


def audited(rows):
    runs=[run(rows)]
    with patch.object(a, "revalidate", side_effect=lambda r: copy.deepcopy(r.get("validation", {}))):
        warnings=a.audit(runs, [])
    return runs, warnings


class IndependentAnalysisTests(unittest.TestCase):
    def test_bound_unusable_and_worker_timeout_cannot_solve(self):
        for changes in ({"bound_valid": False}, {"outcome": "wall_timeout"},
                        {"dual_bound": None}, {"dual_bound": math.nan}):
            r=row(); r.update(changes)
            runs,_=audited([r])
            self.assertFalse(r["audit_assessment"]["solved"])
            summary=next(s for s in a.tables(runs)[0] if s["dimension"]=="all")
            self.assertEqual(summary["par10_mean"],1500.)

    def test_maximize_closed_and_open_gaps_have_correct_sign(self):
        good=row(sense="maximize",bound=10.00001)
        open_gap=row(method="second",sense="maximize",bound=11.)
        _,warnings=audited([good,open_gap])
        self.assertEqual(warnings,[])
        self.assertTrue(good["audit_assessment"]["solved"])
        self.assertAlmostEqual(open_gap["audit_assessment"]["absolute_gap"],1.)
        self.assertFalse(open_gap["audit_assessment"]["solved"])

    def test_cross_repetition_witness_disqualifies_wrong_bound(self):
        bad=row(obj=10.,bound=10.)
        better=row(obj=8.,bound=None)
        runs=[run([bad],7),run([better],8)]
        with patch.object(a,"revalidate",side_effect=lambda r:copy.deepcopy(r["validation"])):
            warnings=a.audit(runs,[])
        self.assertTrue(warnings)
        self.assertFalse(bad["audit_assessment"]["solved"])
        self.assertEqual(a.category(bad),"contradiction")

    def test_invalid_witness_is_not_used_to_refute_another_bound(self):
        good=row()
        invalid=row(method="invalid",obj=-100.,bound=None)
        invalid["validation"]["feasible"]=False
        _,warnings=audited([good,invalid])
        self.assertEqual(warnings,[])
        self.assertTrue(good["audit_assessment"]["solved"])
        self.assertEqual(a.category(invalid),"invalid_witness")

    def test_reported_infeasibility_refuted_by_validated_reference(self):
        r=row();r.update(raw_status="infeasible",witness=None,validation={})
        ref=dict(instance="toy",method="reference",source="ref.json",
                 validation=dict(feasible=True,objective=10.,objective_sense="minimize"))
        warnings=a.audit([run([r])],[ref])
        self.assertTrue(warnings)
        self.assertEqual(a.category(r),"contradiction")

    def test_empty_common_set_is_explicit_and_full_par10_retained(self):
        rs=[row("a",bound=None),row("b"),
            row("a","lbesh-ecp-hull-single"),row("b","lbesh-ecp-hull-single",bound=None)]
        runs,_=audited(rs)
        pair=next(p for p in a.tables(runs)[1] if p["dimension"]=="all")
        self.assertEqual(pair["scheduled"],2)
        self.assertEqual(pair["common_instances"],[])
        self.assertIsNone(pair["esh_over_ecp_shifted_geomean"])
        self.assertEqual(pair["esh_par10_mean"],751.5)

    def test_saved_real_witness_is_rechecked_and_corruption_detected(self):
        path=a.LAB/"results/lbesh_development/main_generated_v1.jsonl"
        record=next(r for r in a.read_records(path) if r.get("validation",{}).get("feasible"))
        self.assertTrue(a.revalidate(record)["feasible"])
        corrupted=copy.deepcopy(record)
        corrupted["witness"]["variables"]={}
        self.assertFalse(a.revalidate(corrupted)["feasible"])

    def test_all_repeats_retained_without_best_time_selection(self):
        name=next(n for n,v in a.MANIFEST.items() if v["split"]=="held_out")
        method="lbesh-esh-hull-single"
        runs=[]
        for seed,time in ((7,100.),(8,3.),(9,40.)):
            r=row(name,method,time=time)
            audited([r]); runs.append(run([r],seed))
        plan=dict(primary_schedule=runs[0]["schedule"],repetitions=dict(order_seeds=[8,9],methods=[method]))
        result=a.repetition_table(runs,plan)[0]
        self.assertEqual(result["repetitions_available"],3)
        self.assertEqual(result["wall_median"],40.)
        self.assertEqual(list(result["wall_times"].values()),[100.,3.,40.])
        self.assertTrue(result["all_planned_available"])

    def test_omitted_repeat_is_visible(self):
        name=next(n for n,v in a.MANIFEST.items() if v["split"]=="held_out")
        r=row(name); runs,_=audited([r])
        plan=dict(primary_schedule=runs[0]["schedule"],repetitions=dict(order_seeds=[8,9],methods=[r["method"]]))
        result=a.repetition_table(runs,plan)[0]
        self.assertEqual(result["repetitions_available"],1)
        self.assertFalse(result["all_planned_available"])

    def test_external_and_ablation_pairs_remain_separate(self):
        name=next(iter(a.MANIFEST))
        primary=run([row(name),row(name,"lbesh-ecp-hull-single",time=9.)],7)
        external=run([row("pyomo.small_lit.basic_step",time=15.),
                      row("pyomo.small_lit.basic_step","lbesh-ecp-hull-single",time=5.)],8)
        ablation=run([row(name,"lbesh-esh-hull-single-nonlp",time=20.),
                      row(name,"lbesh-ecp-hull-single-nonlp",time=4.)],9)
        runs=[primary,external,ablation]
        with patch.object(a,"revalidate",side_effect=lambda r:copy.deepcopy(r["validation"])):
            a.audit(runs,[])
        summaries,pairs,_,_=a.tables(runs)
        all_pairs=[p for p in pairs if p["dimension"]=="all"]
        self.assertEqual({p["run"] for p in all_pairs},{"run7","run8","run9"})
        by_run={p["run"]:p for p in all_pairs}
        self.assertAlmostEqual(by_run["run7"]["esh_over_ecp_shifted_geomean"],1/3)
        self.assertEqual(by_run["run8"]["common_instances"],["pyomo.small_lit.basic_step"])
        self.assertEqual(by_run["run9"]["variant"],"nonlp")
        self.assertAlmostEqual(by_run["run9"]["esh_over_ecp_shifted_geomean"],5.)
        self.assertTrue(all(s["group"]=="legacy" for s in summaries
                            if s["run"]=="run8" and s["dimension"]=="family"))


class IndependentScheduleTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/"input.jsonl"
        self.schedule=dict(instances=["toy"],methods=["m"],ordered_jobs=[["toy","m"]],
                           time_limit=120,wall_limit=150,threads=1,parallel=1,order_seed=7,
                           metadata={"python":"p","platform":"os","packages":{}})
        self.plan=dict(primary_schedule=copy.deepcopy(self.schedule),repetitions=dict(order_seeds=[]),
                       solver_time_limit=120,wall_limit=150,threads=1,max_workers=6)
        self.r=row(method="m");self.r["metadata"]=copy.deepcopy(self.schedule["metadata"])

    def load(self):
        folder=Path(str(self.path)+".runs");folder.mkdir(exist_ok=True)
        (folder/"schedule.json").write_text(json.dumps(self.schedule))
        self.path.write_text(json.dumps(self.r)+"\n")
        with patch.object(a,"check_metadata"):
            return a.load_run(self.path,{},self.plan)

    def test_omitted_cartesian_job_rejected_before_records(self):
        self.schedule["methods"].append("missing")
        with self.assertRaisesRegex(ValueError,"Cartesian"):
            self.load()

    def test_unscheduled_record_rejected(self):
        self.r["method"]="other"
        with self.assertRaisesRegex(ValueError,"unscheduled"):
            self.load()

    def test_worker_package_mismatch_rejected(self):
        self.r["metadata"]["packages"]={"pyomo":"different"}
        with self.assertRaisesRegex(ValueError,"environment differs"):
            self.load()

    def test_completed_worker_missing_provenance_rejected(self):
        self.r.pop("metadata")
        with self.assertRaisesRegex(ValueError,"missing provenance"):
            self.load()

    def test_frozen_actual_schedule_metadata_accepted_and_mutation_rejected(self):
        manifest=a.read_json(a.LAB/"results/lbesh_development/source_v1_manifest.json")
        schedule=a.read_json(a.LAB/"results/lbesh_development/main_generated_v1.jsonl.runs/schedule.json")
        a.check_metadata(schedule["metadata"],manifest)
        bad=copy.deepcopy(schedule["metadata"])
        bad["source_sha256"]["lbesh/solver.py"]="changed"
        with self.assertRaisesRegex(ValueError,"source mismatch"):
            a.check_metadata(bad,manifest)


class IndependentPlotSelectionTests(unittest.TestCase):
    def test_missing_complete_geometry_pair_rejected(self):
        data=a.read_json(a.LAB/"results/lbesh_development/oracle_diagnostic.json")
        victim=data["quadratic"][0]
        keys=("scale","shape","radius","angle_radians")
        data["quadratic"]=[r for r in data["quadratic"]
                           if tuple(r[k] for k in keys)!=tuple(victim[k] for k in keys)]
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError,"[Qq]uadratic.*(design|complete|missing)"):
                a.plot_oracle(Path(tmp),data)

    def test_extra_complete_geometry_pair_rejected(self):
        data=a.read_json(a.LAB/"results/lbesh_development/oracle_diagnostic.json")
        extras=copy.deepcopy(data["quadratic"][:2])
        for r in extras:
            r["radius"]=2.5
        data["quadratic"].extend(extras)
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError,"[Qq]uadratic.*(design|complete|extra)"):
                a.plot_oracle(Path(tmp),data)

    def test_required_diagnostic_fingerprints_cannot_be_omitted(self):
        data=a.read_json(a.LAB/"results/lbesh_development/oracle_diagnostic.json")
        a.check_diagnostic_sources(data)
        for key in list(data["source_sha256"]):
            bad=copy.deepcopy(data);bad["source_sha256"].pop(key)
            with self.assertRaisesRegex(ValueError,"source mismatch/missing"):
                a.check_diagnostic_sources(bad)


class IndependentSupplementaryTests(unittest.TestCase):
    def test_wholly_absent_batch_visible_and_wrong_order_rejected(self):
        job=dict(name="declared",instances=["a","b"],methods=["m","n"],count=4,
                 command=["benchmark","--order-seed","42"])
        supplement=dict(jobs=[job])
        self.assertEqual(a.supplementary_coverage([],supplement),
                         [dict(name="declared",kind="benchmark",scheduled=4,supplied=False)])
        ordered=list(itertools.product(job["instances"],job["methods"]))
        random.Random(42).shuffle(ordered)
        supplied=dict(label="declared",schedule=dict(instances=job["instances"],
                      methods=job["methods"],order_seed=42,ordered_jobs=ordered))
        self.assertTrue(a.supplementary_coverage([supplied],supplement)[0]["supplied"])
        supplied["schedule"]["ordered_jobs"]=ordered[::-1]
        with self.assertRaisesRegex(ValueError,"shuffled order differs"):
            a.supplementary_coverage([supplied],supplement)

    def reference_fixture(self):
        roots=[];enumerations=[]
        for name,info in a.MANIFEST.items():
            if info["family"]=="trig":
                continue
            roots.append(dict(name=name,method="clarabel_exact_cone_root",modes=None,
                              relax_integrality=True,status="optimal"))
            if info["size"]!="small":
                continue
            rows=[dict(name=name,method="clarabel_fixed_assignment",modes=list(modes),
                       relax_integrality=False,status="optimal")
                  for modes in itertools.product(range(3),repeat=info["units"])]
            enumerations.append(dict(name=name,method="clarabel_exhaustive_cone_enumeration",
                                     rows=rows,assignments=len(rows),unresolved_assignments=0,
                                     status="optimal"))
        return roots,enumerations

    def test_missing_root_and_assignment_are_rejected(self):
        roots,enums=self.reference_fixture()
        result=a.check_reference_collection(roots,enums)
        self.assertEqual((result["root_count"],result["enumeration_count"],
                          result["fixed_assignment_count"]),(42,14,378))
        with self.assertRaisesRegex(ValueError,"root collection is incomplete"):
            a.check_reference_collection(roots[:-1],enums)
        enums[0]["rows"].pop()
        with self.assertRaisesRegex(ValueError,"assignments incomplete"):
            a.check_reference_collection(roots,enums)

    def test_unresolved_references_remain_explicit(self):
        roots,enums=self.reference_fixture()
        enums[0]["rows"][0]["status"]="optimal_inaccurate"
        with self.assertRaisesRegex(ValueError,"counts disagree"):
            a.check_reference_collection(roots,enums)
        enums[0].update(status="unresolved",unresolved_assignments=1)
        result=a.check_reference_collection(roots,enums)
        self.assertEqual(result["enumerations"][0]["unresolved_assignments"],1)
        self.assertEqual(result["enumerations"][0]["status"],"unresolved")


if __name__=="__main__":
    unittest.main()
