"""Audit frozen LB-ESH study files and export descriptive numerical results.

No solver is invoked. Complete schedules and frozen executable provenance are
required. Every supplied witness is evaluated on a fresh original GDP model.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import importlib.metadata
import itertools
import json
import math
from pathlib import Path
import platform
import random
import statistics
import sys

from lbesh_research.instances import MANIFEST, build
from lbesh_research.summarize import assessed, shifted_geomean
from lbesh_research.validation import finite, validate_witness

LAB = Path(__file__).resolve().parent
REPO = LAB.parents[1]
PREFIX = "code/minlp_solver_lab/"
METRICS = ("cuts", "lp_iters", "milp_iters", "nlp_solves", "interior_nlps",
           "lazy_calls", "user_cuts", "nodes", "time_master", "time_nlp",
           "time_interior", "time_cuts", "time_setup", "time_total", "lp_bound",
           "last_lp_max_perspective_violation")
MEANING = "Numerically validated primal and solver-reported global bound; no exact certificate."


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text())


def read_records(path):
    text = Path(path).read_text()
    try:
        data = json.loads(text)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        return [json.loads(line) for line in text.splitlines() if line.strip()]


def tolerance(value):
    return 1e-6 + 1e-4 * max(1, abs(value))


def original(name):
    if name in MANIFEST:
        return build(name)
    from gdp_instances import INSTANCES
    return INSTANCES[name]()


def core_files(manifest):
    """Frozen executable files recorded by every generated worker."""
    return {path.removeprefix(PREFIX): sha for path, sha in manifest["files"].items()
            if path.startswith(PREFIX) and (
                path in (PREFIX+"gdp_instances.py", PREFIX+"pyproject.toml") or
                (Path(path).parent.as_posix() in
                 (PREFIX+"lbesh", PREFIX+"lbesh_research") and
                 path.endswith(".py") and not Path(path).name.startswith("test_")))}


def check_metadata(metadata, manifest, *, legacy=False):
    if not metadata:
        raise ValueError("Missing schedule/worker source metadata")
    expected = core_files(manifest)
    if legacy:
        expected.update({p.removeprefix(PREFIX): sha for p, sha in manifest["files"].items()
                         if p.startswith(PREFIX+"instances/")})
    actual = metadata.get("source_sha256", {})
    failures = [p for p, sha in expected.items() if actual.get(p) != sha]
    if failures:
        raise ValueError(f"Frozen source mismatch/missing: {failures}")
    lock = manifest["files"][PREFIX+"uv.lock"]
    if metadata.get("uv_lock_sha256") != lock:
        raise ValueError("Worker environment lock differs from frozen lock")


def check_sensitivity_schedule(schedule, manifest):
    """Check either explicitly declared post-freeze supplementary wrapper."""
    metadata = schedule.get("metadata") or {}
    keys = ("supplementary_wrapper_sha256", "copied_adapter_source_sha256")
    initialized = {f"gams-{solver}-bigm-initialized" for solver in ("shot", "gurobi", "scip")}
    known_methods = initialized | {"gams-gurobi-bigm-feas1e8"}
    if not (set(schedule["methods"]) & known_methods or any(key in metadata for key in keys)):
        return None
    if set(schedule["methods"]) & initialized:
        plan_name = "legacy_initialization_plan_v2.json"
        wrapper_name = "lbesh_legacy_initialization.py"
        policy_fields = ("initialization", "unchanged")
    else:
        plan_name = "gurobi_trig_sensitivity_plan_v1.json"
        wrapper_name = "lbesh_gurobi_sensitivity.py"
        policy_fields = ("solver_options", "primary_results_unchanged")
    path = LAB/"results/lbesh_development"/plan_name
    declared = read_json(path)
    for key in ("instances", "methods", "time_limit", "wall_limit", "threads", "order_seed",
                "ordered_jobs", "validator_tolerances") + policy_fields:
        if schedule.get(key) != declared[key]:
            raise ValueError(f"Sensitivity schedule differs from declaration: {key}")
    expected = dict(supplementary_wrapper_sha256=digest(LAB/wrapper_name),
                    copied_adapter_source_sha256=manifest["files"][PREFIX+"lbesh_research/benchmark.py"])
    for key, sha in expected.items():
        if metadata.get(key) != sha or declared["metadata"].get(key) != sha:
            raise ValueError(f"Sensitivity wrapper source mismatch/missing: {key}")
    return path


def load_run(path, manifest, plan, *, primary=False):
    path = Path(path).resolve()
    schedule_path = Path(str(path)+".runs/schedule.json")
    schedule = read_json(schedule_path)
    instances, methods = schedule["instances"], schedule["methods"]
    if not instances or not methods:
        raise ValueError(f"Empty schedule: {path}")
    if len(set(instances)) != len(instances) or len(set(methods)) != len(methods):
        raise ValueError(f"Duplicate schedule entries: {path}")
    expected = set(itertools.product(instances, methods))
    ordered = [tuple(x) for x in schedule["ordered_jobs"]]
    if len(ordered) != len(expected) or set(ordered) != expected:
        raise ValueError(f"Schedule job list does not equal full Cartesian schedule: {path}")
    if primary:
        for k, v in plan["primary_schedule"].items():
            if schedule.get(k) != v:
                raise ValueError(f"Primary schedule disagrees with frozen plan: {k}")
    if schedule.get("order_seed") in plan["repetitions"]["order_seeds"]:
        wanted = {i for i in plan["primary_schedule"]["instances"]
                  if MANIFEST[i]["split"] == "held_out"}
        if set(instances) != wanted or set(methods) != set(plan["repetitions"]["methods"]):
            raise ValueError(f"Repetition schedule disagrees with frozen plan: {path}")
    for key, plan_key in (("time_limit", "solver_time_limit"), ("wall_limit", "wall_limit"),
                          ("threads", "threads")):
        if schedule[key] != plan[plan_key]:
            raise ValueError(f"Scheduled {key} differs from protocol: {path}")
    if schedule["parallel"] > plan["max_workers"]:
        raise ValueError(f"Scheduled concurrency exceeds protocol: {path}")
    check_metadata(schedule.get("metadata"), manifest,
                   legacy=any(i not in MANIFEST for i in instances))
    wrapper_plan = check_sensitivity_schedule(schedule,manifest)
    records = read_records(path)
    by = {}
    for record in records:
        key = (record["instance"], record["method"])
        if key in by or key not in expected:
            raise ValueError(f"Duplicate or unscheduled record {key}: {path}")
        by[key] = record
        for rk, sk in (("solver_time_limit", "time_limit"), ("wall_limit", "wall_limit"),
                       ("threads", "threads")):
            if record.get(rk) != schedule[sk]:
                raise ValueError(f"Record setting mismatch {key}: {rk}")
        if finite(record.get("wall_time")) is None or record["wall_time"] < 0:
            raise ValueError(f"Missing/invalid wall time: {key}")
        for field in ("supplementary_wrapper_sha256", "copied_adapter_source_sha256"):
            worker_value = (record.get("metadata") or {}).get(field)
            scheduled_value = (schedule.get("metadata") or {}).get(field)
            if worker_value != scheduled_value or (wrapper_plan and worker_value is None):
                raise ValueError(f"Worker wrapper provenance mismatch/missing: {key}, {field}")
        if record.get("metadata"):
            check_metadata(record["metadata"], manifest, legacy=key[0] not in MANIFEST)
            for k in ("python", "platform", "packages"):
                if record["metadata"].get(k) != schedule["metadata"].get(k):
                    raise ValueError(f"Worker environment differs from schedule: {key}, {k}")
        elif record.get("outcome") not in ("wall_timeout", "crash"):
            raise ValueError(f"Worker missing provenance: {key}")
        # A killed worker has no result metadata; it remains a scheduled failure.
    missing = expected - set(by)
    if missing:
        raise ValueError(f"Incomplete schedule {path}: {len(by)}/{len(expected)} present; "
                         f"missing examples {sorted(missing)[:5]}")
    return dict(label=path.stem, path=str(path), schedule_path=str(schedule_path),
                sha256=digest(path), schedule_sha256=digest(schedule_path),
                schedule=schedule, records=records,
                wrapper_plan_path=str(wrapper_plan) if wrapper_plan else None,
                wrapper_plan_sha256=digest(wrapper_plan) if wrapper_plan else None)


def revalidate(record):
    witness = record.get("witness")
    if not witness:
        return dict(feasible=False, objective=None, objective_sense=None,
                    issues=[dict(kind="no_witness")])
    return validate_witness(original(record["instance"]), witness,
                            reported_objective=record.get("reported_objective"))


def load_references(paths, manifest):
    roots, witnesses, provenance = [], [], []
    for path in paths:
        provenance.append(dict(path=str(Path(path).resolve()), sha256=digest(path)))
        for record in read_records(path):
            rows = record.get("rows", [record])
            for row in rows:
                for name in ("instances.py", "conic_reference.py"):
                    key = PREFIX+"lbesh_research/"+name
                    if row.get("source_sha256", {}).get(name) != manifest["files"][key]:
                        raise ValueError(f"Reference source mismatch: {path}, {name}")
                key = PREFIX+"lbesh_research/conic_reference_env/uv.lock"
                if row.get("environment_lock_sha256") != manifest["files"][key]:
                    raise ValueError(f"Reference environment lock mismatch: {path}")
                if row.get("relax_integrality") is True:
                    roots.append(row)
                elif row.get("witness"):
                    checked = validate_witness(original(row["name"]),
                               {"variables": row["witness"], "booleans": {}},
                               reported_objective=row.get("obj"))
                    witnesses.append(dict(instance=row["name"], method=row["method"],
                                          source=str(path), validation=checked))
    return roots, witnesses, provenance


def audit(runs, reference_witnesses):
    """Recheck all witnesses, then compare every bound to every feasible candidate."""
    candidates = defaultdict(list)
    warnings = []
    for ref in reference_witnesses:
        if ref["validation"]["feasible"]:
            candidates[ref["instance"]].append(ref)
        else:
            warnings.append(dict(kind="invalid_reference_witness", **ref))
    for run in runs:
        for record in run["records"]:
            validation = revalidate(record)
            old = record.get("validation") or {}
            if bool(old.get("feasible")) != validation["feasible"]:
                warnings.append(dict(kind="validation_disagreement", run=run["label"],
                                     instance=record["instance"], method=record["method"],
                                     recorded=old, recomputed=validation))
            record["validation"] = validation
            record["audit_assessment"] = assessed(record)
            record["audit_issues"] = []
            if validation["feasible"]:
                candidates[record["instance"]].append(dict(source=run["label"],
                    method=record["method"], validation=validation))
    for run in runs:
        for r in run["records"]:
            for witness in candidates[r["instance"]]:
                val = witness["validation"]
                direction = 1 if val["objective_sense"] == "minimize" else -1
                obj = val["objective"]
                bound = finite(r.get("dual_bound"))
                if bound is not None and direction*(bound-obj) > tolerance(obj):
                    r["audit_issues"].append(dict(kind="bound_contradicts_feasible_witness",
                        bound=bound, witness_objective=obj, witness_source=witness.get("source"),
                        witness_method=witness["method"]))
                if "infeasible" in str(r.get("raw_status", "")).lower():
                    r["audit_issues"].append(dict(kind="infeasible_status_with_feasible_witness",
                        witness_objective=obj, witness_source=witness.get("source")))
            if r["audit_issues"]:
                r["audit_assessment"]["solved"] = False
                warnings.append(dict(run=run["label"], instance=r["instance"],
                                     method=r["method"], issues=r["audit_issues"]))
    return warnings


def group_info(name):
    return {k: MANIFEST.get(name, {}).get(k, "legacy") for k in ("family", "size", "split")}


def groups(instances):
    yield "all", "all", list(instances)
    for dim in ("family", "size", "split"):
        for value in sorted({group_info(i)[dim] for i in instances}):
            yield dim, value, [i for i in instances if group_info(i)[dim] == value]
    for values in sorted({tuple(group_info(i)[d] for d in ("family", "size", "split"))
                          for i in instances}):
        yield "family/size/split", "/".join(values), [i for i in instances if
            tuple(group_info(i)[d] for d in ("family", "size", "split")) == values]


def category(r):
    if r["audit_issues"]:
        return "contradiction"
    if r["audit_assessment"]["solved"]:
        return "numerical_solve"
    if r.get("outcome") != "completed":
        return r.get("outcome", "unknown")
    if r["audit_assessment"]["feasible"]:
        return "feasible_open_gap"
    if "infeasible" in str(r.get("raw_status", "")).lower():
        return "reported_infeasible"
    return "invalid_witness" if r.get("witness") else "no_witness"


def tables(runs):
    summaries, pairs, metrics, detailed = [], [], [], []
    for run in runs:
        s = run["schedule"]
        by = {(r["instance"], r["method"]): r for r in run["records"]}
        cap = s["wall_limit"]
        def wall(r):
            return min(cap, r["wall_time"])
        for r in run["records"]:
            detailed.append(dict(run=run["label"], instance=r["instance"], method=r["method"],
                **group_info(r["instance"]), outcome=r.get("outcome"), raw_status=r.get("raw_status"),
                category=category(r), **r["audit_assessment"], wall_time=r["wall_time"],
                objective=r["validation"].get("objective"), dual_bound=r.get("dual_bound"),
                max_normalized_violation=r["validation"].get("max_normalized_violation"),
                invalid_witness=bool(r.get("witness")) and not r["validation"]["feasible"],
                validation_issues=r["validation"]["issues"], contradictions=r["audit_issues"],
                lp_end_reason=r.get("solver_metrics", {}).get("lp_end_reason"),
                **{m: finite(r.get("solver_metrics", {}).get(m)) for m in METRICS}))
        for dimension, value, names in groups(s["instances"]):
            base = dict(run=run["label"], dimension=dimension, group=value)
            for method in s["methods"]:
                rs = [by[i, method] for i in names]
                solved = [r for r in rs if r["audit_assessment"]["solved"]]
                times = [wall(r) if r["audit_assessment"]["solved"] else 10*cap for r in rs]
                summaries.append(dict(**base, method=method, scheduled=len(rs), present=len(rs),
                    numerical_solved=len(solved), validated_feasible=sum(r["validation"]["feasible"] for r in rs),
                    invalid_witnesses=sum(bool(r.get("witness")) and not r["validation"]["feasible"] for r in rs),
                    contradictory_runs=sum(bool(r["audit_issues"]) for r in rs),
                    par10_mean=statistics.mean(times), par10_shifted_geomean=shifted_geomean(times),
                    solved_only_shifted_geomean=shifted_geomean([wall(r) for r in solved]),
                    categories=dict(Counter(category(r) for r in rs)),
                    raw_statuses=dict(Counter(str(r.get("raw_status")) for r in rs)),
                    lp_end_reasons=dict(Counter(r.get("solver_metrics", {}).get("lp_end_reason") for r in rs))))
                for metric in METRICS:
                    vals = [finite(r.get("solver_metrics", {}).get(metric)) for r in rs]
                    vals = [v for v in vals if v is not None]
                    if vals:
                        metrics.append(dict(**base, method=method, metric=metric,
                            available=len(vals), scheduled=len(rs), mean=statistics.mean(vals),
                            median=statistics.median(vals), minimum=min(vals), maximum=max(vals)))
            for a in s["methods"]:
                if not a.startswith("lbesh-esh-"):
                    continue
                b = a.replace("lbesh-esh-", "lbesh-ecp-", 1)
                if b not in s["methods"]:
                    continue
                pieces = a.split("-")
                form, tree = pieces[2:4]
                variant = "-".join(pieces[4:]) or "default"
                common = [i for i in names if all(by[i,m]["audit_assessment"]["solved"] for m in (a,b))]
                ta, tb = [[wall(by[i,m]) for i in common] for m in (a,b)]
                ga, gb = shifted_geomean(ta), shifted_geomean(tb)
                pairs.append(dict(**base, formulation=form, tree=tree, variant=variant, scheduled=len(names),
                    common_solved=len(common), common_instances=common,
                    esh_solved=sum(by[i,a]["audit_assessment"]["solved"] for i in names),
                    ecp_solved=sum(by[i,b]["audit_assessment"]["solved"] for i in names),
                    esh_shifted_geomean=ga, ecp_shifted_geomean=gb,
                    esh_over_ecp_shifted_geomean=ga/gb if gb else None,
                    esh_faster=sum(x<y for x,y in zip(ta,tb)), ecp_faster=sum(y<x for x,y in zip(ta,tb)),
                    esh_par10_mean=statistics.mean([wall(by[i,a]) if by[i,a]["audit_assessment"]["solved"] else 10*cap for i in names]),
                    ecp_par10_mean=statistics.mean([wall(by[i,b]) if by[i,b]["audit_assessment"]["solved"] else 10*cap for i in names])))
    return summaries, pairs, metrics, detailed


def repetition_table(runs, plan):
    chosen = [r for r in runs if (
        r["schedule"]["order_seed"] in plan["repetitions"]["order_seeds"] or
        (r["schedule"]["order_seed"] == plan["primary_schedule"]["order_seed"] and
         set(r["schedule"]["instances"]) == set(plan["primary_schedule"]["instances"]) and
         set(r["schedule"]["methods"]) == set(plan["primary_schedule"]["methods"])))]
    if len({r["schedule"]["order_seed"] for r in chosen}) != len(chosen):
        raise ValueError("Duplicate planned repetition order seed")
    rows = []
    for i in plan["primary_schedule"]["instances"]:
        if MANIFEST[i]["split"] != "held_out":
            continue
        for method in plan["repetitions"]["methods"]:
            records = [(run["label"], r) for run in chosen for r in run["records"]
                       if r["instance"] == i and r["method"] == method]
            if not records:
                continue
            times = [r["wall_time"] for _,r in records]
            objectives = [r["validation"]["objective"] for _,r in records if r["validation"]["feasible"]]
            rows.append(dict(instance=i, method=method, repetitions_available=len(records),
                repetitions_planned=3, all_planned_available=len(records)==3,
                numerical_solves=sum(r["audit_assessment"]["solved"] for _,r in records),
                categories={label:category(r) for label,r in records},
                wall_times={label:r["wall_time"] for label,r in records},
                wall_min=min(times), wall_median=statistics.median(times), wall_max=max(times),
                wall_max_over_min=max(times)/min(times) if min(times)>0 else None,
                feasible_objective_spread=max(objectives)-min(objectives) if objectives else None))
    return rows


def cone_table(runs, roots):
    rows = []
    for run in runs:
        for r in run["records"]:
            lp = finite(r.get("solver_metrics", {}).get("lp_bound"))
            if lp is None or "-hull-" not in r["method"]:
                continue
            for ref in roots:
                if ref["name"] != r["instance"]:
                    continue
                obj, lb = finite(ref.get("obj")), finite(ref.get("lb"))
                rows.append(dict(run=run["label"], instance=r["instance"], method=r["method"],
                    lp_bound=lp, lp_end_reason=r["solver_metrics"].get("lp_end_reason"),
                    cone_status=ref.get("status"), cone_primal_objective=obj,
                    cone_dual_estimate=lb, cone_primal_residual=ref.get("primal_residual"),
                    cone_dual_residual=ref.get("dual_residual"),
                    cone_dual_minus_lp=lb-lp if lb is not None else None,
                    cone_primal_minus_lp=obj-lp if obj is not None else None,
                    bound_certified=False))
    return rows


def write_csv(path, rows):
    if not rows:
        path.write_text("")
        return
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows({k: json.dumps(v) if isinstance(v,(dict,list)) else v
                         for k,v in row.items()} for row in rows)


def plot(output, summaries, pairs, primary_label, *, is_primary=True):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 9, "svg.fonttype": "none", "pdf.fonttype": 42})
    rows = [r for r in summaries if r["run"] == primary_label and r["dimension"] == "all"]
    fig, axes = plt.subplots(1,2,figsize=(10,5), layout="constrained")
    labels = [r["method"] for r in rows]
    axes[0].barh(labels, [r["numerical_solved"] for r in rows])
    axes[0].set_xlabel(f"Numerical solves / {rows[0]['scheduled']}")
    axes[1].barh(labels, [r["par10_mean"] for r in rows])
    axes[1].set_xlabel("PAR10 mean wall time (s); failure = 1500 s")
    for ax in axes:
        ax.invert_yaxis()
    axes[1].tick_params(labelleft=False)
    fig.suptitle(("Primary" if is_primary else "Supplied") + " scheduled set: descriptive numerical results")
    for suffix in ("pdf", "svg", "png"):
        fig.savefig(output/f"primary_outcomes.{suffix}", dpi=200)
    plt.close(fig)
    rows = [r for r in pairs if r["run"] == primary_label and r["dimension"] == "family" and r["variant"] == "default"]
    if rows:
        families = sorted({r["group"] for r in rows})
        fig, ax = plt.subplots(figsize=(8,4), layout="constrained")
        combinations = sorted({(r["formulation"], r["tree"]) for r in rows})
        for offset,(form,tree) in enumerate(combinations):
            rs = [next(r for r in rows if r["group"]==family and r["formulation"]==form and r["tree"]==tree)
                  for family in families]
            xs = [i+(offset-(len(combinations)-1)/2)*.18 for i in range(len(families))]
            ys = [r["esh_over_ecp_shifted_geomean"] for r in rs]
            present = [(x,y,r) for x,y,r in zip(xs,ys,rs) if y is not None]
            ax.scatter([x for x,_,_ in present], [y for _,y,_ in present], label=f"{form}, {tree}")
            for x,y,r in present:
                ax.annotate(str(r["common_solved"]), (x,y), xytext=(0,5), textcoords="offset points", ha="center", fontsize=7)
        ax.axhline(1,color="black",lw=.8)
        ax.set_yscale("log")
        ax.set_xticks(range(len(families)),families)
        ax.set_ylabel("ESH / ECP shifted geometric mean wall time")
        ax.set_title("Common numerical solves; labels give paired counts")
        ax.legend(ncol=2,fontsize=8)
        for suffix in ("pdf","svg","png"):
            fig.savefig(output/f"paired_family_times.{suffix}",dpi=200)
        plt.close(fig)


def plot_oracle(output, data):
    """Fixed diagnostic design, all sampled geometries; ranges are not intervals."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    scales = [None]+data["design"]["scales"]
    scalar = {(r["scale"], r["policy"]):r for r in data["scalar"]}
    expected = set(itertools.product(scales, ("esh", "ecp")))
    if set(scalar) != expected or len(scalar) != len(data["scalar"]):
        raise ValueError("Diagnostic scalar design is incomplete or duplicated")
    paired = defaultdict(dict)
    for row in data["quadratic"]:
        key = (row["scale"], row["shape"], row["radius"], row["angle_radians"])
        if row["policy"] in paired[key]:
            raise ValueError("Duplicate quadratic diagnostic")
        paired[key][row["policy"]] = row
    if data["design"]["quadratic_angles"] != "2*pi*k/16, k=0,...,15":
        raise ValueError("Quadratic diagnostic design has an unknown angle rule")
    declared = set(itertools.product(scales, ("disk", "ellipsoid"),
        data["design"]["quadratic_radii"], (2*math.pi*k/16 for k in range(16))))
    if set(paired) != declared:
        raise ValueError("Quadratic diagnostic design is incomplete or contains extra geometries")
    ratios = defaultdict(list)
    for key, rows in paired.items():
        if set(rows) != {"esh", "ecp"}:
            raise ValueError("Unpaired quadratic diagnostic")
        ratios[key[0]].append(rows["ecp"]["cut_depth"]/rows["esh"]["cut_depth"])
    stats = [dict(scale=scale, pairs=len(ratios[scale]),
                  median=statistics.median(ratios[scale]), minimum=min(ratios[scale]),
                  maximum=max(ratios[scale])) for scale in scales]
    fig, axes = plt.subplots(1,3,figsize=(11,3.6),layout="constrained")
    xs = list(range(len(scales)))
    for policy,marker in (("esh","o"),("ecp","s")):
        for ax,metric in zip(axes[:2],("cuts","function_calls")):
            ax.plot(xs,[scalar[scale,policy][metric] for scale in scales],marker=marker,label=policy.upper())
    axes[0].set_ylabel("Cuts to scalar geometric tolerance")
    axes[1].set_ylabel("Scalar function evaluations")
    axes[0].legend()
    axes[2].plot(xs,[r["median"] for r in stats],marker="s",label="Median")
    axes[2].fill_between(xs,[r["minimum"] for r in stats],[r["maximum"] for r in stats],alpha=.2,label="Full sampled range")
    axes[2].set_ylabel("ECP / ESH normalized cut depth")
    axes[2].legend(fontsize=8)
    for ax in axes:
        ax.set_xticks(xs,["base"]+[str(s) for s in scales[1:]])
        ax.set_xlabel("Increasing transformation parameter")
    fig.suptitle("Fixed-geometry oracle diagnostic; no GDP performance inference")
    for suffix in ("pdf", "svg", "png"):
        fig.savefig(output/f"oracle_mechanism.{suffix}",dpi=200)
    plt.close(fig)
    (output/"oracle_plot_stats.json").write_text(json.dumps(dict(
        quadratic_depth_ratios=stats, scalar=data["scalar"],
        meaning="All diagnostic samples; min/max are descriptive ranges, not confidence intervals."),
        indent=2,allow_nan=False)+"\n")


def check_diagnostic_sources(diagnostic):
    required = ("lbesh_oracle_diagnostic.py", "lbesh/solver.py", "lbesh/structure.py")
    actual = diagnostic.get("source_sha256", {})
    for name in required:
        if actual.get(name) != digest(LAB/name):
            raise ValueError(f"Diagnostic source mismatch/missing: {name}")


def check_reference_collection(roots, enumerations):
    supported = {name for name,info in MANIFEST.items() if info["family"] != "trig"}
    small = {name for name in supported if MANIFEST[name]["size"] == "small"}
    if len(roots) != len(supported) or {r["name"] for r in roots} != supported:
        raise ValueError("Reference root collection is incomplete or duplicated")
    if any(r.get("method") != "clarabel_exact_cone_root" or r.get("modes") is not None
           or r.get("relax_integrality") is not True for r in roots):
        raise ValueError("Reference root collection includes a wrong solve mode")
    if len(enumerations) != len(small) or {r["name"] for r in enumerations} != small:
        raise ValueError("Reference enumeration collection is incomplete or duplicated")
    for record in enumerations:
        if record.get("method") != "clarabel_exhaustive_cone_enumeration":
            raise ValueError("Reference enumeration collection includes a wrong solve mode")
        wanted = set(itertools.product(range(3),repeat=MANIFEST[record["name"]]["units"]))
        rows = record.get("rows", [])
        if (len(rows) != len(wanted) or {tuple(r.get("modes") or []) for r in rows} != wanted
                or any(r.get("name") != record["name"] or
                       r.get("method") != "clarabel_fixed_assignment" or
                       r.get("relax_integrality") is not False for r in rows)):
            raise ValueError(f"Reference enumeration assignments incomplete/duplicated: {record['name']}")
        unresolved = sum(r.get("status") not in ("optimal","infeasible") for r in rows)
        if record.get("assignments") != len(rows) or record.get("unresolved_assignments") != unresolved:
            raise ValueError(f"Reference enumeration counts disagree with rows: {record['name']}")
    return dict(root_count=len(roots), root_statuses=dict(Counter(r.get("status") for r in roots)),
                enumeration_count=len(enumerations),
                fixed_assignment_count=sum(len(r["rows"]) for r in enumerations),
                enumerations=[{k:r.get(k) for k in ("name","status","assignments","unresolved_assignments")}
                              for r in enumerations],
                meaning="Complete scheduled numerical evaluations; completeness does not certify optimality.")


def supplementary_coverage(runs, supplementary, reference_paths=()):
    """Verify declared batches and make wholly absent study batches explicit."""
    by_label = {run["label"]:run for run in runs}
    coverage = []
    for job in supplementary["jobs"]:
        if "instances" not in job or "methods" not in job:
            if job["name"] != "conic_references_frozen_v1":
                raise ValueError(f"Unknown supplementary collection: {job['name']}")
            command = job["command"]
            wanted_paths = [LAB/command[command.index(flag)+1]
                            for flag in ("--roots-out", "--enumeration-out")]
            supplied = {Path(path).resolve() for path in reference_paths}
            present = [path.resolve() in supplied for path in wanted_paths]
            entry = dict(name=job["name"], kind="references", scheduled=job["count"],
                         supplied=all(present), files_supplied=present)
            if all(present):
                entry.update(check_reference_collection(*[read_records(path) for path in wanted_paths]))
                if entry["root_count"]+entry["fixed_assignment_count"] != job["count"]:
                    raise ValueError("Reference evaluation count differs from supplementary declaration")
            coverage.append(entry)
            continue
        run = by_label.get(job["name"])
        coverage.append(dict(name=job["name"], kind="benchmark", scheduled=job["count"], supplied=run is not None))
        if run is None:
            continue
        schedule = run["schedule"]
        for key in ("instances", "methods"):
            if schedule[key] != job[key]:
                raise ValueError(f"Supplementary schedule differs from declaration: {job['name']}, {key}")
        if len(job["instances"])*len(job["methods"]) != job["count"]:
            raise ValueError(f"Inconsistent declared supplementary count: {job['name']}")
        command = job["command"]
        seed = int(command[command.index("--order-seed")+1])
        wanted = list(itertools.product(job["instances"],job["methods"]))
        random.Random(seed).shuffle(wanted)
        if schedule["order_seed"] != seed or [tuple(x) for x in schedule["ordered_jobs"]] != wanted:
            raise ValueError(f"Supplementary shuffled order differs from declaration: {job['name']}")
    return coverage


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("results", nargs="+", type=Path)
    p.add_argument("--primary", type=Path, help="Must be among results; enforce frozen primary schedule")
    p.add_argument("--references", nargs="*", default=[], type=Path)
    p.add_argument("--manifest", type=Path, default=LAB/"results/lbesh_development/source_v1_manifest.json")
    p.add_argument("--plan", type=Path, default=LAB/"results/lbesh_development/study_plan_v1.json")
    p.add_argument("--supplementary-plan", type=Path,
                   default=LAB/"results/lbesh_development/supplementary_plan_v1.json")
    p.add_argument("--require-complete-study", action="store_true",
                   help="Require --primary and every declared supplementary batch")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--plots", action="store_true")
    p.add_argument("--oracle-diagnostic", type=Path, help="Optional actual-oracle diagnostic JSON")
    args = p.parse_args()
    manifest, plan = read_json(args.manifest), read_json(args.plan)
    if len({x.resolve() for x in args.results}) != len(args.results):
        p.error("Duplicate input file")
    if args.primary and args.primary.resolve() not in {x.resolve() for x in args.results}:
        p.error("--primary must be among positional result files")
    if args.out.exists():
        p.error("Output already exists; use a new directory to preserve previous analyses")
    # Model/validation imports must match the snapshot used by the workers.
    for name, sha in core_files(manifest).items():
        if digest(LAB/name) != sha:
            raise ValueError(f"Current executable source differs from frozen source: {name}")
    if digest(LAB/"uv.lock") != manifest["files"][PREFIX+"uv.lock"]:
        raise ValueError("Current environment lock differs from frozen source")
    runs = [load_run(path,manifest,plan,primary=bool(args.primary and path.resolve()==args.primary.resolve()))
            for path in args.results]
    if len({r["label"] for r in runs}) != len(runs):
        raise ValueError("Input filename stems must be unique")
    supplementary = read_json(args.supplementary_plan)
    coverage = supplementary_coverage(runs,supplementary,args.references)
    if args.require_complete_study and (not args.primary or not all(r["supplied"] for r in coverage)):
        raise ValueError("Complete study requires the primary and every declared supplementary batch")
    if any(i not in MANIFEST for r in runs for i in r["schedule"]["instances"]):
        for name, sha in manifest["files"].items():
            if name.startswith(PREFIX+"instances/") and digest(REPO/name) != sha:
                raise ValueError(f"Current legacy source differs from frozen source: {name}")
    roots, witnesses, refs_provenance = load_references(args.references,manifest)
    diagnostic = read_json(args.oracle_diagnostic) if args.oracle_diagnostic else None
    if diagnostic is not None:
        check_diagnostic_sources(diagnostic)
    warnings = audit(runs,witnesses)
    summaries,pairs,metrics,details = tables(runs)
    output = dict(schema_version=1, meaning=MEANING, command=sys.argv,
        provenance=dict(analysis_source_sha256=digest(__file__), manifest_sha256=digest(args.manifest),
            plan_sha256=digest(args.plan), supplementary_plan_sha256=digest(args.supplementary_plan),
            python=sys.version, platform=platform.platform(),
            packages={n:importlib.metadata.version(n) for n in
                      (("pyomo", "matplotlib") if args.plots else ("pyomo",))},
            solver_environments={r["label"]:{k:r["schedule"]["metadata"].get(k)
                for k in ("python", "platform", "packages", "uv_lock_sha256",
                          "supplementary_wrapper_sha256", "copied_adapter_source_sha256")} for r in runs},
            input_files=[{k:r[k] for k in ("path","sha256","schedule_path","schedule_sha256",
                                             "wrapper_plan_path","wrapper_plan_sha256")} for r in runs],
            reference_files=refs_provenance,
            oracle_diagnostic=dict(path=str(args.oracle_diagnostic.resolve()),
                                   sha256=digest(args.oracle_diagnostic)) if diagnostic else None),
        summary=summaries, esh_ecp_pairs=pairs, metrics=metrics, records=details,
        supplementary_coverage=coverage,
        all_planned_benchmark_batches_supplied=bool(args.primary and all(r["supplied"] for r in coverage if r["kind"] == "benchmark")),
        all_planned_study_batches_supplied=bool(args.primary and all(r["supplied"] for r in coverage)),
        repetitions=repetition_table(runs,plan), cone_roots=cone_table(runs,roots), warnings=warnings,
        notes=["All scheduled outcomes retained; failures pay 10 times the 150-second wall cap.",
               "Common-solved timing is conditional; PAR10 includes every scheduled instance.",
               "One-second shifted geometric means. Every input repetition remains separate.",
               "Generated families/seeds/sizes are dependent controls; no significance claims.",
               "Matched ECP shares interior initialization with ESH; these comparisons do not measure an optimized standalone ECP algorithm.",
               "Single-tree time_master includes callback work; component times overlap and must not be summed.",
               "Fresh-model revalidation reuses the independently reviewed harness checker; it is not a second checker implementation.",
               "Cone dual estimates are numerical, uncertified, and never promoted to exact optimum references."])
    args.out.mkdir(parents=True)
    (args.out/"analysis.json").write_text(json.dumps(output,indent=2,allow_nan=False)+"\n")
    for name in ("summary","esh_ecp_pairs","metrics","records","repetitions","cone_roots"):
        write_csv(args.out/f"{name}.csv",output[name])
    if args.plots:
        primary_label = args.primary.stem if args.primary else runs[0]["label"]
        plot(args.out,summaries,pairs,primary_label,is_primary=bool(args.primary))
        if diagnostic:
            plot_oracle(args.out,diagnostic)
    print(json.dumps(dict(output=str(args.out),files=len(runs),records=len(details),warnings=len(warnings))))
    return 2 if warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
