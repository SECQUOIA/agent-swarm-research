"""Independent retained-artifact audit of the two supplementary GAMS studies.

No solver runs. Original witnesses are re-evaluated and native DAT/log/options
are compared with each result and its unchanged primary counterpart.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re

from lbesh_results_independent_audit import artifact_directory, verify_source_archive
from lbesh_research import benchmark
from lbesh_research.validation import validate_witness

LAB = Path(__file__).resolve().parent
DATA = LAB / "results/lbesh_development"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rows(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def classify(record):
    if not record.get("witness"):
        return dict(feasible=False, solved=False, objective=None, issues=[{"kind": "no_witness"}])
    checked = validate_witness(benchmark._build(record["instance"]), record["witness"],
                               reported_objective=record.get("reported_objective"))
    primal, bound = checked["objective"], record.get("dual_bound")
    solved = False
    if checked["feasible"] and record.get("bound_valid") and bound is not None:
        gap = (primal - bound) * (1 if checked["objective_sense"] == "minimize" else -1)
        tol = 1e-6 + 1e-4 * max(1, abs(primal))
        solved = -tol <= gap <= tol
    return dict(feasible=checked["feasible"], solved=solved, objective=primal,
                max_violation=checked["max_violation"],
                max_normalized_violation=checked["max_normalized_violation"], issues=checked["issues"])


def audit(kind):
    if kind == "trig":
        filename, primary_file, plan_file, wrapper = (
            "gurobi_trig_sensitivity_v1.jsonl", "main_generated_v1.jsonl",
            "gurobi_trig_sensitivity_plan_v1.json", "lbesh_gurobi_sensitivity.py")
    else:
        filename, primary_file, plan_file, wrapper = (
            "legacy_initialization_v1.jsonl", "legacy_external_v1.jsonl",
            "legacy_initialization_plan_v2.json", "lbesh_legacy_initialization.py")
    path = DATA / filename
    records = rows(path)
    primary_records = rows(DATA / primary_file)
    primary = {(row["instance"], row["method"]): row for row in primary_records}
    plan = json.loads((DATA / plan_file).read_text())
    schedule = json.loads(Path(str(path) + ".runs/schedule.json").read_text())
    expected = {(name, method) for name in plan["instances"] for method in plan["methods"]}
    assert len(records) == len(expected), (len(records), len(expected))
    assert {(r["instance"], r["method"]) for r in records} == expected
    assert len(set(map(tuple, schedule["ordered_jobs"]))) == len(expected)
    assert schedule["ordered_jobs"] == plan["ordered_jobs"]
    assert schedule["instances"] == plan["instances"] and schedule["methods"] == plan["methods"]
    assert 1 <= schedule["parallel"] <= 6
    wrapper_hash = digest(LAB / wrapper)
    assert schedule["metadata"]["supplementary_wrapper_sha256"] == wrapper_hash
    assert plan["metadata"]["supplementary_wrapper_sha256"] == wrapper_hash
    source_manifest = json.loads((DATA / "source_v1_manifest.json").read_text())
    verify_source_archive(DATA, source_manifest)
    current_frozen = source_manifest["files"]
    frozen = {**current_frozen, **source_manifest.get("original_file_sha256", {})}
    current_metadata = benchmark._metadata(legacy=kind == "initialization")
    recorded_source = schedule["metadata"]["source_sha256"]
    assert set(current_metadata["source_sha256"]) == set(recorded_source), "Missing or additional installed study sources"
    assert recorded_source == {name: frozen["code/minlp_solver_lab/" + name] for name in recorded_source}
    assert current_metadata["source_sha256"] == {
        name: current_frozen["code/minlp_solver_lab/" + name] for name in recorded_source
    }
    output = []
    for record in sorted(records, key=lambda row: (row["instance"], row["method"])):
        assert record["metadata"]["supplementary_wrapper_sha256"] == wrapper_hash
        assert record["metadata"]["source_sha256"] == schedule["metadata"]["source_sha256"]
        for field in ("python", "platform", "packages"):
            assert record["metadata"][field] == schedule["metadata"][field]
        assert record["metadata"]["copied_adapter_source_sha256"] == frozen["code/minlp_solver_lab/lbesh_research/benchmark.py"]
        for name, sha in record["metadata"]["source_sha256"].items():
            assert sha == frozen["code/minlp_solver_lab/" + name], name
        assert record["metadata"]["uv_lock_sha256"] == frozen["code/minlp_solver_lab/uv.lock"]
        assert (record["solver_time_limit"], record["wall_limit"], record["threads"]) == (120, 150, 1)
        artifact = artifact_directory(DATA, record["artifacts"])
        assert json.loads((artifact / "final.json").read_text()) == record
        checked = classify(record)
        if record.get("assessment"):
            assert checked["feasible"] == record["assessment"]["feasible"]
            assert checked["solved"] == record["assessment"]["solved"]
        original_method = (record["method"].removesuffix("-feas1e8") if kind == "trig"
                           else record["method"].removesuffix("-initialized"))
        baseline = primary[(record["instance"], original_method)]
        baseline_checked = classify(baseline)
        native = {}
        logfile = artifact / "gams.log"
        log = logfile.read_text(errors="replace") if logfile.exists() else ""
        if record["outcome"] == "completed":
            assert record["exit_code"] == 0
            for line in (artifact / "gams/resultsstat.dat").read_text().splitlines()[1:]:
                name, value = line.split()
                native[name] = None if value == "NA" else float(value)
            assert native == record["native_gams"]
            assert record["dual_bound"] == native["OBJEST"]
            assert record["reported_objective"] == native["OBJVAL"]
            assert record["bound_valid"] == (native["OBJEST"] is not None and native["MODELSTAT"] in (1, 7, 8))
            assert "GAMS 54.3.1" in log
            gms = (artifact / "gams/model.gms").read_text()
            for option in record["options"]["add_options"]:
                assert option in gms, option
            if kind == "trig":
                assert "Gurobi Optimizer version 13.0.2" in log
                assert re.search(r"(?m)^\s*FeasibilityTol\s+1e-08\s*$", log)
                assert re.search(r"(?m)^\s*Threads\s+1\s*$", log)
                assert (artifact / "gams/gurobi.opt").read_text() == "feasibilitytol 1e-8\n"
                assert digest(artifact / "gams/gurobi.opt") == record["option_file_sha256"]
                assert record["effective_feasibilitytol"] == 1e-8
                changed = dict(record["options"])
                changed["solver_options"] = {}
                changed["add_options"] = changed["add_options"][:-1]
                assert changed == baseline["options"]
            else:
                assert record["options"] == plan["unchanged_primary_options"][record["method"]]
                if baseline.get("options"):
                    assert record["options"] == baseline["options"]
                solver = record["options"]["solver"]
                if solver == "shot":
                    assert re.search(r"Version:\s+1\.1\.\s+Git hash:\s+a81275b4", log)
                    assert record["native_versions"]["shot"] is None
                    assert (artifact / "gams/shot.opt").read_text() == "".join(
                        f"{key} = {str(value).lower()}\n" for key, value in record["options"]["solver_options"].items())
                if solver == "scip":
                    assert "SCIP version 10.0.3" in log
                if solver == "gurobi":
                    assert "Gurobi Optimizer version 13.0.2" in log
        if kind == "initialization":
            import lbesh_legacy_initialization as initializer
            assert initializer.initialize_model(record["instance"], benchmark._build(record["instance"])) == record["initialization_changes"]
            if record.get("witness") and record["instance"] == "gdplib.batch_processing":
                assert record["witness"]["variables"]["storageTankSize_log[10]"] == record["initialization_changes"][0]["new_value"]
        log_bound = None
        if record.get("options", {}).get("solver") == "gurobi":
            matches = re.findall(r"Best objective ([0-9.eE+-]+), best bound ([0-9.eE+-]+), gap ([0-9.eE+-]+)%", log)
            if matches:
                objective, bound, gap = map(float, matches[-1])
                log_bound = dict(objective=objective, bound=bound, percent_gap=gap,
                                 interpretation="Diagnostic native log values only; do not replace the declared GAMS OBJEST gate.")
        output.append(dict(instance=record["instance"], method=record["method"], outcome=record["outcome"],
                           primary_outcome=baseline["outcome"], primary=baseline_checked, supplementary=checked,
                           primary_wall_time=baseline["wall_time"], supplementary_wall_time=record["wall_time"],
                           dual_bound=record.get("dual_bound"), native_status=native,
                           native_log_bound_diagnostic=log_bound,
                           log_sha256=digest(logfile) if logfile.exists() else None,
                           artifacts=str(artifact)))
    return dict(kind=kind, records=len(output), source_sha256=digest(Path(__file__)),
                input_sha256=digest(path), primary_sha256=digest(DATA / primary_file),
                plan_sha256=digest(DATA / plan_file), wrapper_sha256=wrapper_hash,
                checks="complete schedule, retained native DAT/log/options, source provenance, fresh original witnesses and independent gap classification",
                limitation="Floating-point numerical validation and solver bounds; no exact certificate.",
                rows=output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=("trig", "initialization"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.kind)
    with args.out.open("x") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"kind": args.kind, "records": result["records"],
                      "primary_feasible": sum(r["primary"]["feasible"] for r in result["rows"]),
                      "supplementary_feasible": sum(r["supplementary"]["feasible"] for r in result["rows"]),
                      "primary_solved": sum(r["primary"]["solved"] for r in result["rows"]),
                      "supplementary_solved": sum(r["supplementary"]["solved"] for r in result["rows"])}))
