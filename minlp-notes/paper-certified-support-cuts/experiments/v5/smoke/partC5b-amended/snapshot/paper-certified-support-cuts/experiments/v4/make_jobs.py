"""Create a campaign-4 output directory: frozen cases, code snapshot copy and job list.

    make_jobs.py partC2        --output DIR
    make_jobs.py partC3        --output DIR
    make_jobs.py partB2        --output DIR
    make_jobs.py partD-screen  --output DIR --selection scanD/qualifying.json
    make_jobs.py partD-root    --output DIR --selection scanD/partD-selection.json
    make_jobs.py partD-full    --output DIR --selection scanD/partD-selection.json
    make_jobs.py PART --smoke  --output DIR [--selection ...]

DIR must not exist. It receives the campaign-2/3 layout (``cases/``,
``snapshot/`` with ``frozen-cases/`` and ``original-osil/``,
``source-manifest.json``, ``jobs.json``, ``build.json``) so that the archived
replay runs unchanged. A job is one (model, phase, seed); its modes run back
to back in the order rotated by (model index + seed) mod (number of modes).

``--smoke`` keeps the part's modes and rules but uses its first one
(path family) or two (other parts) cases and 10 s soft / 30 s hard limits.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time

from common import (SNAPSHOT, TOPIC_NAME, V3, digest, load_snapshot_manifest, verify_manifest,
                    write_new)
import mechanism

C2_ROOT_MODES = ("baseline-novarlocks", "baseline-extra", "frozen-wide")
C3_ROOT_MODES = ("baseline", "all-diag-mech", "rowdir-wide", "baseline-extra")
B2_MODES = ("baseline-noaggr", "all-noaggr", "all-diag-noaggr", "all-diag-rowdir-noaggr", "baseline-extra")
D_ROOT_MODES = ("baseline", "all", "all-diag", "all-diag-rowdir", "baseline-extra")
D_FULL_MODES = ("baseline", "all", "auto", "baseline-extra")
# (phase, seeds, modes, soft seconds, hard seconds, node limit)
C2_FULL = ("full", (0,), C2_ROOT_MODES + ("gurobi",), 300.0, 360.0, None)
C2_ROOT = ("root", (0,), C2_ROOT_MODES, 120.0, 180.0, 1)
C3_FULL = ("full", (0,), C3_ROOT_MODES + ("gurobi",), 300.0, 360.0, None)
C3_ROOT = ("root", (0,), C3_ROOT_MODES, 120.0, 180.0, 1)
B2_ROOT = ("root", (0,), B2_MODES, 60.0, 90.0, 1)
D_SCREEN = ("screen", (0,), ("baseline",), 60.0, 90.0, None)
D_ROOT = ("root", (0,), D_ROOT_MODES, 120.0, 180.0, 1)
D_FULL = ("full", (0,), D_FULL_MODES, 300.0, 360.0, None)
C2_SEEDS = (0, 1, 2, 3, 4)  # the 20 campaign-3 instances
C3_SEEDS = (5, 6, 7, 8, 9)  # 20 fresh instances
SMOKE_LIMITS = (10.0, 30.0)
HARD_PREFIX = "convexification-hard-v4:"
PART_D_SIZE = 20
MAX_WORKERS = 6
V3_SELECTION = SNAPSHOT / "paper-certified-support-cuts/experiments/v3/scan/partB-selection.json"
STRUCTURE_PREFIX = "convexification-structure-v3:"


def snapshot_module_path():
    path = SNAPSHOT / TOPIC_NAME / "experiments"
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
    return path


def holdout():
    return json.loads((SNAPSHOT / TOPIC_NAME / "experiments/holdout-selection.json").read_text())


def metadata():
    with (SNAPSHOT / "code/minlp_solver_lab/instances/instancedata.csv").open() as stream:
        return {row["name"]: row for row in csv.DictReader(stream, delimiter=";")}


def hard_rank(name):
    return hashlib.sha256((HARD_PREFIX + name).encode()).hexdigest()


def osil_case(name, suite, source, sha256, reference_primal, reference_dual, stratum):
    source = Path(source)
    if digest(source) != sha256:
        raise SystemExit(f"OSiL file changed after selection: {source}")
    return {"name": name, "suite": suite, "stratum": stratum, "path": str(source),
            "source_sha256": sha256, "reference_primal": reference_primal,
            "reference_dual": reference_dual}


def mechanism_cases(seeds):
    snapshot_module_path()
    from run_campaign import exact_json
    return [mechanism.case(n, seed, exact_json) for n in mechanism.NS for seed in seeds]


def c2_cases():
    """The 20 campaign-3 Part C instances, checked against the campaign-3 case files."""
    cases = mechanism_cases(C2_SEEDS)
    for case in cases:
        archived = json.loads((V3 / "runs/partC/cases" / (case["name"] + ".json")).read_text())
        if json.loads(json.dumps(case)) != archived:
            raise SystemExit(f"regenerated case differs from campaign 3: {case['name']}")
    return cases


def c3_cases():
    """20 fresh instances (seeds 5-9), never run before."""
    cases = mechanism_cases(C3_SEEDS)
    used = {p.stem for p in (V3 / "runs/partC/cases").glob("*.json")}
    if used & {case["name"] for case in cases}:
        raise SystemExit("a fresh Part C3 instance name was used in campaign 3")
    return cases


def b2_cases():
    """The 30 campaign-3 Part B models, from the frozen campaign-3 selection."""
    selection = json.loads(V3_SELECTION.read_text())
    frozen = holdout()
    excluded = {r["name"] for r in frozen["selected"]}
    pool = [n for n in frozen["eligible_names_in_rank_order"] if n not in excluded]
    names = [e["name"] for e in selection["selected"]]
    rank = lambda n: hashlib.sha256((STRUCTURE_PREFIX + n).encode()).hexdigest()
    if (len(set(names)) != len(names) or not set(names) <= set(pool) or names != sorted(names, key=rank)
            or names != selection["qualifying_names_in_rank_order"][:30]):
        raise SystemExit("campaign-3 Part B selection fails its own rules")
    if sorted(names) != sorted(p.stem for p in (V3 / "runs/partB/cases").glob("*.json")):
        raise SystemExit("campaign-3 Part B selection differs from the campaign-3 Part B cases")
    reference = metadata()
    return [osil_case(e["name"], "structure", e["path"], e["osil_sha256"],
                      reference.get(e["name"], {}).get("primalbound"),
                      reference.get(e["name"], {}).get("dualbound"), e.get("stratum"))
            for e in selection["selected"]]


def d_cases(selection_path, screen):
    """Part D models: all qualifying ones (screen) or the hash-ranked hard selection."""
    selection = json.loads(Path(selection_path).read_text())
    if selection.get("schema") != ("campaign-v4-partD-qualifying-1" if screen else "campaign-v4-partD-selection-1"):
        raise SystemExit(f"{selection_path} is not a Part D {'qualifying list' if screen else 'selection'}")
    entries = selection["qualifying" if screen else "selected"]
    names = [e["name"] for e in entries]
    if len(set(names)) != len(names) or not set(names) <= set(selection["pool_names"]):
        raise SystemExit("Part D list contains duplicates or names outside the pool")
    if not screen:
        hard = selection["hard_qualifying_names_in_rank_order"]
        if hard != sorted(hard, key=hard_rank) or names != hard[:PART_D_SIZE]:
            raise SystemExit("Part D selection is not the first 20 hard qualifying models in hash order")
    reference = metadata()
    return [osil_case(e["name"], "larger", e["path"], e["osil_sha256"],
                      reference.get(e["name"], {}).get("primalbound"),
                      reference.get(e["name"], {}).get("dualbound"), e.get("stratum"))
            for e in entries]


def jobs_for(cases, phases, order=None):
    """Declared job order: phases in the given order, seeds ascending, then cases."""
    jobs = []
    order = order or (lambda cs: cs)
    position = {case["name"]: i for i, case in enumerate(cases)}
    for phase, seeds, modes, soft, hard, nodes in phases:
        for seed in seeds:
            for case in order(cases):
                offset = (position[case["name"]] + seed) % len(modes)
                rotated = modes[offset:] + modes[:offset]
                index = len(jobs)
                jobs.append({"job_id": f"{index:03d}", "phase": phase, "name": case["name"],
                             "suite": case["suite"], "seed": seed, "time_limit": soft,
                             "worker_timeout": hard, "node_limit": nodes,
                             "runs": [{"run_id": f"{index:03d}_{case['name']}__{phase}__s{seed}__{mode}",
                                       "mode": mode, "position": k}
                                      for k, mode in enumerate(rotated)]})
    return jobs


def larger_first(cases):
    """Path family: larger n first within each phase, to shorten the parallel makespan."""
    return sorted(cases, key=lambda c: (-c["mechanism"]["n"], c["mechanism"]["seed"]))


def build(part, selection, smoke):
    if part in ("partC2", "partC3"):
        cases = c2_cases() if part == "partC2" else c3_cases()
        phases = [C2_FULL, C2_ROOT] if part == "partC2" else [C3_FULL, C3_ROOT]
        order = larger_first
    elif part == "partB2":
        cases, phases, order = b2_cases(), [B2_ROOT], None
    elif part in ("partD-screen", "partD-root", "partD-full"):
        if selection is None:
            raise SystemExit(f"{part} requires --selection")
        cases = d_cases(selection, part == "partD-screen")
        phases = [{"partD-screen": D_SCREEN, "partD-root": D_ROOT, "partD-full": D_FULL}[part]]
        order = None
    else:
        raise SystemExit(f"unknown part {part}")
    if smoke:
        # Path family: the smallest instance; other parts: the first two models.
        cases = ([min(cases, key=lambda c: (c["mechanism"]["n"], c["mechanism"]["seed"]))]
                 if part in ("partC2", "partC3") else cases[:2])
        phases = [(phase, seeds, modes) + SMOKE_LIMITS + (nodes,)
                  for phase, seeds, modes, soft, hard, nodes in phases]
    return cases, jobs_for(cases, phases, order), MAX_WORKERS


def main(args):
    code = load_snapshot_manifest()
    cases, jobs, max_workers = build(args.part, args.selection, args.smoke)
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    (out / "cases").mkdir()
    snapshot = out / "snapshot"
    hashes = {}
    for relative in code:
        target = snapshot / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SNAPSHOT / relative, target)
        hashes[relative] = digest(target)
    for case in cases:
        write_new(out / "cases" / (case["name"] + ".json"), case)
        relative = f"frozen-cases/{case['name']}.json"
        (snapshot / "frozen-cases").mkdir(exist_ok=True)
        shutil.copyfile(out / "cases" / (case["name"] + ".json"), snapshot / relative)
        hashes[relative] = digest(snapshot / relative)
        if "path" in case:
            relative = f"original-osil/{case['name']}.osil"
            (snapshot / "original-osil").mkdir(exist_ok=True)
            shutil.copyfile(case["path"], snapshot / relative)
            hashes[relative] = digest(snapshot / relative)
            if hashes[relative] != case["source_sha256"]:
                raise SystemExit(f"OSiL copy differs from the pinned hash: {case['name']}")
    if verify_manifest(snapshot, hashes) or any(hashes[k] != v for k, v in code.items()):
        raise SystemExit("output snapshot does not match the code snapshot")
    part = args.part + ("-smoke" if args.smoke else "")
    write_new(out / "source-manifest.json", hashes)
    write_new(out / "jobs.json", {"schema": "campaign-v4-jobs-1", "part": part,
                                  "max_workers": max_workers, "jobs": jobs})
    write_new(out / "build.json", {
        "part": part, "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "code_manifest_sha256": digest(SNAPSHOT / "source-manifest.json"),
        "selection": str(Path(args.selection).resolve()) if args.selection else None,
        "selection_sha256": digest(args.selection) if args.selection else None,
        "cases": len(cases), "jobs": len(jobs), "runs": sum(len(j["runs"]) for j in jobs),
        "max_workers": max_workers})
    print(json.dumps({"output": str(out), "part": part, "cases": len(cases), "jobs": len(jobs),
                      "runs": sum(len(j["runs"]) for j in jobs), "max_workers": max_workers}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("part", choices=("partC2", "partC3", "partB2", "partD-screen", "partD-root", "partD-full"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--selection", type=Path)
    parser.add_argument("--smoke", action="store_true")
    main(parser.parse_args())
