"""Independent corpus and campaign-accounting audit; never runs optimization.

The cut/model-binding replay has a separate owner and is deliberately excluded.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
BAD = {"worker_error", "process_timeout", "campaign_budget_exhausted",
       "worker_no_output", "worker_output_parse_error", "ablation_unavailable"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def audit_selection():
    # Use the existing file parser, but reconstruct selection independently of
    # the frozen eligible list and the campaign runner.
    import cases  # makes the existing OSiL parser importable
    from uenv.osil import read_osil

    selected_path = HERE / "holdout-selection.json"
    selection = json.loads(selected_path.read_text())
    metadata_path = REPO / "code/minlp_solver_lab/instances/instancedata.csv"
    with metadata_path.open() as source:
        metadata = {r["name"]: r for r in csv.DictReader(source, delimiter=";")}
    corpus = Path.home() / ".cache/minlplib/minlplib/osil"
    corpus_names = {p.stem for p in corpus.glob("*.osil")}
    prior_names = set()
    for name in ("minlplib_v2.jsonl", "minlplib_v3.jsonl"):
        prior = REPO / "code/univariate_envelopes/results" / name
        prior_names.update(json.loads(line)["instance"] for line in prior.read_text().splitlines())
    for path in (REPO / "research-20260922/curve-hulls/code/results").iterdir():
        matches = [name for name in corpus_names if path.name.startswith(name + "_")]
        if matches:
            prior_names.add(max(matches, key=len))
    require(prior_names == set(selection["excluded_names"]), "prior-campaign exclusions differ")
    eligible = []
    for path in corpus.glob("*.osil"):
        m = metadata.get(path.stem)
        if (path.stem in selection["excluded_names"] or path.stat().st_size > 150000
                or m is None or int(m["nvars"]) > 80 or int(m["ncons"]) > 120
                or int(m["nquadcons"]) + int(m["ngennlcons"]) == 0):
            continue
        try:
            model = read_osil(str(path))
        except Exception:
            continue
        finite = sum(math.isfinite(lo) and math.isfinite(hi) and lo < hi
                     for lo, hi in zip(model.var_lb, model.var_ub))
        if finite >= 2:
            eligible.append(path.stem)
    rank = lambda name: hashlib.sha256(("convexification-holdout-v1:" + name).encode()).hexdigest()
    eligible.sort(key=rank)
    require(eligible == [r["name"] for r in selection["eligible"]], "eligible corpus differs")
    require(eligible[:24] == [r["name"] for r in selection["selected"]], "selected ranking differs")
    for row in selection["eligible"]:
        require(row["rank"] == rank(row["name"]), f"rank mismatch: {row['name']}")
        require(row["sha256"] == sha(corpus / (row["name"] + ".osil")),
                f"source changed: {row['name']}")
    for row in selection["selected"]:
        for field, archived in (("reference_primal", "primalbound"), ("reference_dual", "dualbound")):
            require(row[field] == metadata[row["name"]][archived], f"reference mismatch: {row['name']}")
    return {"eligible": len(eligible), "selected": 24, "ranking_matches": True,
            "prior_campaign_exclusions_reconstructed": len(prior_names),
            "source_hashes_checked": len(eligible), "references_match_archived_csv": True,
            "integer_cases": sum(int(metadata[n]["nbinvars"]) + int(metadata[n]["nintvars"]) > 0
                                 for n in eligible[:24]),
            "convex_cases": sum(metadata[n]["convex"] == "True" for n in eligible[:24]),
            "selection_sha256": sha(selected_path), "metadata_sha256": sha(metadata_path)}


def audit_metric_guards():
    # Adversarial records check only the documented accounting boundary.
    import summarize

    base = {"name": "audit", "suite": "holdout", "phase": "full", "mode": "baseline",
            "status": "optimal", "primal": 2.0, "dual": 2.0, "sense": "min",
            "total_seconds": 1.0, "primal_check": {"checked": True, "passed": True}, "cuts": []}
    require(summarize.solved(base), "valid solved record rejected")
    bad = [dict(base, status="process_timeout"), dict(base, returncode=-9),
           dict(base, worker_status="worker_error"), dict(base, primal=None),
           dict(base, primal=math.inf), dict(base, primal_check={"checked": False}),
           dict(base, primal_check={"checked": True, "passed": False}),
           dict(base, reference_check={"dual_consistent": False}),
           dict(base, reference_check={"root_dual_consistent": False})]
    require(not any(summarize.solved(r) for r in bad), "invalid record counted as solved")
    timeout = {**base, "mode": "auto", "status": "process_timeout"}
    timeout.pop("cuts")
    result = summarize.compare([base, timeout], "holdout", "full", "auto")
    require(result["rows"][0]["cuts"] is None, "missing cut log counted as zero")
    require(result["outcomes"] == {"unavailable_or_flagged": 1}, "timeout counted favorably")
    maximization = dict(base, sense="max", status="timelimit", dual=3.0)
    improved = dict(maximization, mode="auto", dual=2.5)
    result = summarize.compare([maximization, improved], "holdout", "full", "auto")
    require(result["outcomes"] == {"better": 1}, "maximization direction reversed")
    worsened = dict(base, mode="auto", status="timelimit", dual=1.0)
    result = summarize.compare([base, worsened], "holdout", "full", "auto")
    require(result["outcomes"] == {"worse": 1}, "negative dual outcome lost")
    return {"adversarial_solved_records_rejected": len(bad), "missing_cut_count_unknown": True,
            "maximization_comparison_correct": True, "negative_outcome_retained": True}


def acceptable(record):
    return (record["status"] not in BAD and record.get("returncode", 0) == 0
            and not record.get("worker_status")
            and record.get("primal_check", {}).get("passed") is not False
            and record.get("reference_check", {}).get("dual_consistent") is not False
            and record.get("reference_check", {}).get("root_dual_consistent") is not False)


def numerically_solved(record):
    return (acceptable(record) and record["status"] in {"optimal", "gaplimit"}
            and record.get("primal_check", {}).get("checked") is True
            and record.get("primal_check", {}).get("passed") is True
            and isinstance(record.get("primal"), (float, int)) and math.isfinite(record["primal"]))


def audit_campaign(directory):
    jobs = json.loads((directory / "jobs.json").read_text())
    records = [json.loads(line) for line in (directory / "records.jsonl").read_text().splitlines()]
    completion = json.loads((directory / "completion.json").read_text())
    manifest = json.loads((directory / "source-manifest.json").read_text())
    summary = json.loads((directory / "summary.json").read_text())
    require(len(records) == len(jobs) == completion["scheduled"], "missing scheduled records")
    require(dict(Counter(j["phase"] for j in jobs)) == {
        "full": 164, "root": 116, "no_cache": 10, "pairs_only": 2, "repeat": 24},
        "scheduled phase population differs from protocol")
    job_keys = [(j["name"], j["phase"], j["mode"]) for j in jobs]
    require(len(set(job_keys)) == len(jobs), "duplicate scheduled jobs")
    for job in jobs:
        phase = job["phase"]
        require(job["time_limit"] == (2.0 if phase == "root" else 6.0), "time budget differs")
        require(job["node_limit"] == (1 if phase == "root" else None), "node budget differs")
        require(job["seed"] == int(phase == "repeat"), "seed differs")
        require(job["cache"] == (phase != "no_cache"), "cache ablation differs")
        require(job["merge_stars"] == (phase != "pairs_only"), "star ablation differs")
    require(len({r["run_id"] for r in records}) == len(records), "duplicate run identifiers")
    for path, expected in manifest.items():
        require(sha(directory / "snapshot" / path) == expected, f"snapshot hash mismatch: {path}")
        if path.startswith("frozen-cases/"):
            current = directory / "cases" / Path(path).name
            require(sha(current) == expected, f"worker case descriptor changed: {path}")
            descriptor = json.loads(current.read_text())
            if "path" in descriptor:
                require(sha(directory / "snapshot/original-osil" / (descriptor["name"] + ".osil"))
                        == descriptor["source_sha256"], f"archived input differs: {path}")
    models = defaultdict(set)
    synthetic_status_conflicts = []
    for job, record in zip(jobs, records):
        require(all(record.get(k) == v for k, v in job.items()), f"job mismatch: {record['run_id']}")
        saved = json.loads((directory / "runs" / (record["run_id"] + ".json")).read_text())
        require(saved == record, f"ledger differs from saved run: {record['run_id']}")
        if "model_sha256" in record:
            models[record["name"]].add(record["model_sha256"])
        if "original_model" in record:
            encoded_hash = hashlib.sha256(json.dumps(record["original_model"], sort_keys=True).encode()).hexdigest()
            require(encoded_hash == record["model_sha256"], f"model hash mismatch: {record['run_id']}")
        if record["suite"] == "synthetic" and record["status"] in {"infeasible", "inforunbd", "unbounded"}:
            synthetic_status_conflicts.append({"run_id": record["run_id"], "status": record["status"],
                                              "witness": record.get("reference_witness_check")})
    require(not synthetic_status_conflicts,
            f"synthetic status contradicts known finite optimum/feasible witness: {synthetic_status_conflicts}")
    require(all(len(hashes) == 1 for hashes in models.values()), "models differ between modes/phases")
    statuses = dict(Counter(r["status"] for r in records))
    require(statuses == completion["counts"] == summary["status_counts"], "status totals differ")
    require(summary["total_records"] == len(records), "summary denominator differs")
    recorded_cuts = sum(len(r["cuts"]) for r in records if "cuts" in r)
    require(summary["cuts_all_phases"] == recorded_cuts, "cut total differs")
    mode_counts = {}
    admission_counts = {}
    comparison_counts = {}
    for suite, data in summary["suites"].items():
        for mode, aggregate in data["modes"].items():
            rows = [r for r in records if (r["suite"], r["phase"], r["mode"]) == (suite, "full", mode)]
            counts = {"instances": len(rows), "solved": sum(numerically_solved(r) for r in rows),
                      "cuts": sum(len(r["cuts"]) for r in rows if "cuts" in r),
                      "instances_with_cuts": sum(bool(r.get("cuts")) for r in rows),
                      "missing_cut_logs": sum("cuts" not in r and mode in {"all", "auto"} for r in rows),
                      "status_counts": dict(Counter(r["status"] for r in rows))}
            require(all(aggregate[k] == v for k, v in counts.items()), f"mode aggregate differs: {suite}/{mode}")
            times = {
                "summed_integration_seconds": sum(r["total_seconds"] + r.get("source_read_seconds", 0)
                                                  for r in rows if "total_seconds" in r),
                "summed_outer_seconds": sum(r.get("outer_wall_seconds", 0) for r in rows),
                "summed_discovery_seconds": sum(r.get("discovery_seconds", 0) for r in rows),
                "summed_build_seconds": sum(r.get("build_seconds", 0) for r in rows),
                "summed_callback_seconds": sum((r.get("separation") or {}).get("callback_seconds", 0) for r in rows),
                "summed_certification_seconds": sum((r.get("separation") or {}).get("certification_seconds", 0) for r in rows)}
            require(all(math.isclose(aggregate[k], v, rel_tol=1e-12, abs_tol=1e-12)
                        for k, v in times.items()), f"timing aggregate differs: {suite}/{mode}")
            mode_counts[f"{suite}/{mode}"] = counts
            refused = sum(r["status"] == "source_model_mismatch" for r in rows)
            admitted = sum(bool(r.get("scip_version")) for r in rows)
            admission_counts[f"{suite}/{mode}"] = {
                "frozen_denominator": len(rows), "source_model_refused": refused,
                "confirmed_admitted": admitted, "admission_unknown": len(rows) - refused - admitted}
        for key, phase in (("full_comparisons", "full"), ("full_vs_control", "full"), ("root_comparisons", "root")):
            for comparison in data[key]:
                a = {r["name"]: r for r in records if (r["suite"], r["phase"], r["mode"]) == (suite, phase, comparison["mode"])}
                b = {r["name"]: r for r in records if (r["suite"], r["phase"], r["mode"]) == (suite, phase, comparison["baseline"])}
                require(a.keys() == b.keys(), f"unpaired population: {suite}/{key}")
                outcomes = Counter()
                for name in a:
                    first, second = a[name], b[name]
                    if (not acceptable(first) or not acceptable(second)
                            or first.get("dual") is None or second.get("dual") is None):
                        outcome = "unavailable_or_flagged"
                    else:
                        require(first["sense"] == second["sense"], "objective senses differ")
                        direction = 1 if first["sense"] == "min" else -1
                        difference = direction * (first["dual"] - second["dual"])
                        tolerance = 1e-6 * max(1.0, abs(first["dual"]), abs(second["dual"]))
                        outcome = "tie" if abs(difference) <= tolerance else "better" if difference > 0 else "worse"
                    outcomes[outcome] += 1
                require(dict(outcomes) == comparison["outcomes"], f"comparison differs: {suite}/{key}")
                comparison_counts[f"{suite}/{phase}/{comparison['mode']}-vs-{comparison['baseline']}"] = dict(outcomes)
    return {"directory": str(directory), "scheduled_and_retained": len(records),
            "manifest_entries_verified": len(manifest), "consistent_model_hashes": len(models),
            "status_counts": statuses, "recorded_cuts": recorded_cuts,
            "wall_seconds": completion["wall_seconds"],
            "primal_checks": sum(r.get("primal_check", {}).get("checked", False) for r in records),
            "primal_failures": [r["run_id"] for r in records if r.get("primal_check", {}).get("passed") is False],
            "reference_conflicts": [r["run_id"] for r in records
                                    if r.get("reference_check", {}).get("dual_consistent") is False
                                    or r.get("reference_check", {}).get("root_dual_consistent") is False],
            "soft_budget_overshoots": [{"run_id": r["run_id"], "seconds": r.get("total_seconds", 0)
                                       + r.get("source_read_seconds", 0)} for r in records
                                      if r.get("total_seconds", 0) + r.get("source_read_seconds", 0)
                                      > r["time_limit"] + 0.01],
            "missing_integration_timings": sum("total_seconds" not in r for r in records),
            "missing_new_cut_logs": sum("cuts" not in r and r["mode"] in {"all", "auto"} for r in records),
            "mode_counts": mode_counts, "admission_counts": admission_counts,
            "synthetic_status_conflicts": synthetic_status_conflicts,
            "comparison_counts": comparison_counts,
            "cut_binding_replay_in_scope": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {"selection": audit_selection(), "metric_guards": audit_metric_guards()}
    if args.campaign:
        result["campaign"] = audit_campaign(args.campaign.resolve())
    text = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")
