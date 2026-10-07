"""Campaign 4, Part D: pool, structural scan, qualification and hard-model selection.

Implements Part D of ``../../campaign-v4-protocol.md`` up to the selection:

    scan_d.py run      build the pool, scan it (import and discovery as in
                       campaign 3 Part S), write records.jsonl, then report
    scan_d.py report   rewrite scan-summary.md and qualifying.json from records.jsonl
    scan_d.py select   read the screening run (screen/records.jsonl, created with
                       make_jobs.py partD-screen and driver.py), copy it to
                       screen-records.jsonl and write partD-selection.json

Pool: cached MINLPLib OSiL models with 120 < nvars <= 1000, convex == False
in the library metadata, at least one quadratic or polynomial function
(nquadfunc + npolynomfunc >= 1), OSiL file below 2,000,000 bytes, and not
used in campaigns 1-3 (no case of campaign 1, campaign 2 including its
diagnostic and repair runs, or campaign 3 Parts S, A, B, C and the v3d
diagnostic). Scan: per model a fresh single-threaded subprocess runs
read_osil, build_model and discover with the frozen Config and a 60 s
discovery deadline, under a 120 s hard process limit; at most six run at a
time. Qualifying: admitted, discovery completed, and at least one block with
auto_eligible true. Screening: mode baseline, seed 0, 60 s. Hard: not solved
(solved as in campaign 3: optimal or gaplimit with an incumbent that passes
the original-model check). Selection: the first 20 hard qualifying models in
ascending SHA-256 of 'convexification-hard-v4:' + name.

The solver code is the campaign-4 snapshot (``../snapshot``), verified
against its manifest before and after the scan; no bytecode is written.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict
import csv
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import shutil
import signal
import statistics
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
V4 = HERE.parent
REPO = V4.parents[2]
SNAPSHOT = V4 / "snapshot"
TOPIC = SNAPSHOT / "research-20261003-convexification"
OSIL_DIR = Path.home() / ".cache/minlplib/minlplib/osil"
METADATA = SNAPSHOT / "code/minlp_solver_lab/instances/instancedata.csv"
RECORDS = HERE / "records.jsonl"
ENVIRONMENT = HERE / "scan-environment.json"
SUMMARY = HERE / "scan-summary.md"
QUALIFYING = HERE / "qualifying.json"
SCREEN_DIR = HERE / "screen"
SCREEN_RECORDS = HERE / "screen-records.jsonl"
SELECTION = HERE / "partD-selection.json"

MIN_VARIABLES, MAX_VARIABLES, MAX_OSIL_BYTES = 120, 1000, 2_000_000
DISCOVERY_DEADLINE = 60.0
HARD_TIMEOUT = 120.0
PARALLEL = 6
SELECTION_SIZE = 20
RANK_PREFIX = "convexification-hard-v4:"
PHASE_MARK = "scan-phase: "
STRATA = ("nonconvex_continuous", "nonconvex_integer")
THREAD_ENV = {k: "1" for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                              "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS",
                              "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")}
FAILURES = ("process_timeout", "worker_error", "worker_no_output", "worker_output_parse_error")
# Directories whose case files are the models used in campaigns 1-3.
CAMPAIGN_CASE_DIRS = (
    "research-20261002-convexification/experiments/campaign-v1/cases",
    "research-20261003-convexification/experiments/campaign-v2/cases",
    "research-20261003-convexification/experiments/repair-discovery-v1/cases",
    "paper-certified-support-cuts/experiments/v3/runs/partA-full/cases",
    "paper-certified-support-cuts/experiments/v3/runs/partA-root/cases",
    "paper-certified-support-cuts/experiments/v3/runs/partB/cases",
    "paper-certified-support-cuts/experiments/v3/runs/partC/cases",
    "paper-certified-support-cuts/experiments/v3d/runs/partA-root-rowdir/cases",
    "paper-certified-support-cuts/experiments/v3d/runs/partB-root-rowdir/cases",
    "paper-certified-support-cuts/experiments/v3d/runs/partC-rowdir/cases")
CAMPAIGN_SELECTIONS = ("research-20261002-convexification/experiments/holdout-selection.json",
                       "research-20261003-convexification/experiments/holdout-selection.json")
POOL_RULE = ("Cached MINLPLib OSiL models with more than 120 and at most 1000 variables (nvars), "
             "convex == 'False' in instancedata.csv, nquadfunc + npolynomfunc >= 1, OSiL file below "
             "2,000,000 bytes, and no case of campaigns 1-3 (case directories and frozen selections "
             "listed in used_names_sources).")
QUALIFYING_RULE = ("Admitted by build_model, discover with the frozen Config completed within its 60 s "
                   "deadline, and at least one returned block has auto_eligible true.")
SELECTION_RULE = ("Screening: mode baseline, seed 0, 60 s soft limit (90 s hard). Hard: not solved, where "
                  "solved means status optimal or gaplimit, a normal worker exit and an incumbent that "
                  "passes the independent original-model check. Selection: the first 20 hard qualifying "
                  "models in ascending hex SHA-256 of the UTF-8 string 'convexification-hard-v4:' + name.")


def digest_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def hard_rank(name):
    return hashlib.sha256((RANK_PREFIX + name).encode("utf-8")).hexdigest()


def snapshot_check():
    manifest = json.loads((SNAPSHOT / "source-manifest.json").read_text())
    bad = [k for k, v in manifest.items() if not (SNAPSHOT / k).is_file() or digest_file(SNAPSHOT / k) != v]
    if bad:
        raise SystemExit("snapshot differs from its manifest: " + ", ".join(bad))
    return digest_file(SNAPSHOT / "source-manifest.json")


# ---------------------------------------------------------------- worker

def worker(name, path, output):
    """Read, build and discover one model; write one JSON object."""
    started = time.perf_counter()
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(TOPIC))
    import xml.etree.ElementTree as ET
    from solver.integration import Config, DiscoveryBudgetExhausted, discover
    from solver.model import ModelAdmissionError, build_model, read_osil
    config = Config()
    record = {"load_start": list(os.getloadavg()),
              "import_seconds": time.perf_counter() - started,
              "config": asdict(config), "discovery_deadline_seconds": DISCOVERY_DEADLINE}
    outside = [m.__file__ for k, m in list(sys.modules.items())
               if k.split(".")[0] in ("solver", "theory", "uenv") and getattr(m, "__file__", None)
               and not Path(m.__file__).resolve().is_relative_to(SNAPSHOT)]
    if outside:
        raise RuntimeError(f"modules imported from outside the snapshot: {outside}")
    phase("read", started)
    read_start = time.perf_counter()
    try:
        inst = read_osil(str(path))
    except (OSError, ET.ParseError, ValueError, TypeError, KeyError, IndexError,
            NotImplementedError, RecursionError) as error:
        record.update(status="unsupported_input", diagnostic=f"{type(error).__name__}: {error}",
                      read_seconds=time.perf_counter() - read_start)
        return finish(record, output)
    record.update(read_seconds=time.perf_counter() - read_start,
                  variables=len(inst.var_lb), constraints=len(inst.rows) - 1)
    phase("build", started)
    build_start = time.perf_counter()
    try:
        built = build_model(inst)
    except ModelAdmissionError as error:
        record.update(status=error.status, diagnostic=str(error),
                      build_seconds=time.perf_counter() - build_start)
        return finish(record, output)
    record.update(status="admitted", build_seconds=time.perf_counter() - build_start)
    try:
        record["signed_sides"] = int(built.objective_var is not None) + sum(
            math.isfinite(row["ub"]) + math.isfinite(row["lb"]) for row in inst.rows[1:])
        phase("discover", started)
        discovery_start = time.perf_counter()
        detected = None
        try:
            detected = discover(inst, built, config, deadline=discovery_start + DISCOVERY_DEADLINE)
            record.update(discovery_completed=True, discovery_deadline_hit=False)
        except DiscoveryBudgetExhausted:
            record.update(discovery_completed=False, discovery_deadline_hit=True)
        except Exception as error:  # recorded, never hidden
            record.update(discovery_completed=False, discovery_deadline_hit=False,
                          discovery_error=f"{type(error).__name__}: {error}")
        record["discovery_seconds"] = time.perf_counter() - discovery_start
        if detected is not None:
            record["discovery_stats"] = detected.stats
            record["blocks"] = [{
                "variables": list(block.variables),
                "dimension": len(block.variables),
                "nonlinear_sides": len(block.sides),
                "nonlinear_rows": len({side.row_index for side in block.sides}),
                "source_ids": [side.source_id for side in block.sides],
                "affine_domain_rows": len(block.rows),
                "quadratic": bool(block.quadratic),
                "auto_eligible": bool(block.auto_eligible)} for block in detected.blocks]
    finally:
        built.model.freeProb()
    return finish(record, output)


def phase(name, started):
    print(f"{PHASE_MARK}{name} {time.perf_counter() - started:.3f}", flush=True)


def finish(record, output):
    record["load_end"] = list(os.getloadavg())
    temporary = Path(output).with_suffix(".tmp")
    temporary.write_text(json.dumps(record, sort_keys=True, allow_nan=False))
    temporary.replace(output)


# ---------------------------------------------------------------- pool

def stratum(row):
    integer = int(row["nbinvars"]) + int(row["nintvars"]) > 0
    return "nonconvex_integer" if integer else "nonconvex_continuous"


def used_names():
    """Names of every model used in campaigns 1-3, with the sources that list it."""
    sources = {}
    for relative in CAMPAIGN_CASE_DIRS:
        directory = REPO / relative
        if not directory.is_dir():
            raise SystemExit(f"missing campaign case directory {directory}")
        for path in directory.glob("*.json"):
            sources.setdefault(path.stem, []).append(relative)
    for relative in CAMPAIGN_SELECTIONS:
        data = json.loads((REPO / relative).read_text())
        names = [e["name"] for e in data["selected"]] + list(data.get("eligible_names_in_rank_order", []))
        for name in names:  # campaign-3 Part S scanned the campaign-2 eligible list
            sources.setdefault(name, []).append(relative)
    return {name: sorted(set(v)) for name, v in sorted(sources.items())}


def pool():
    with METADATA.open() as stream:
        metadata = {r["name"]: r for r in csv.DictReader(stream, delimiter=";")}
    used = used_names()
    models, excluded = [], {}
    for name, row in sorted(metadata.items()):
        try:
            nvars = int(row["nvars"])
        except ValueError:
            continue
        functions = int(row["nquadfunc"] or 0) + int(row["npolynomfunc"] or 0)
        path = OSIL_DIR / f"{name}.osil"
        if not (MIN_VARIABLES < nvars <= MAX_VARIABLES and row["convex"] == "False" and functions >= 1):
            continue
        if not path.is_file():
            excluded[name] = "no cached OSiL file"
            continue
        if path.stat().st_size >= MAX_OSIL_BYTES:
            excluded[name] = "OSiL file of 2,000,000 bytes or more"
            continue
        if name in used:
            excluded[name] = "used in campaigns 1-3: " + ", ".join(used[name])
            continue
        models.append({"name": name, "stratum": stratum(row), "path": str(path),
                       "osil_sha256": digest_file(path), "nvars": nvars, "ncons": int(row["ncons"]),
                       "osil_bytes": path.stat().st_size})
    return models, excluded, used


# ---------------------------------------------------------------- driver

def run():
    os.environ.update(THREAD_ENV)
    if RECORDS.exists():
        raise SystemExit(f"{RECORDS} exists; remove it to rescan")
    manifest_start = snapshot_check()
    models, excluded, used = pool()
    environment = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "python": sys.version, "executable": sys.executable,
                   "platform": platform.platform(), "logical_cpus": os.cpu_count(),
                   "load_start": list(os.getloadavg()), "thread_environment": THREAD_ENV,
                   "parallel_processes": PARALLEL, "hard_timeout_seconds": HARD_TIMEOUT,
                   "discovery_deadline_seconds": DISCOVERY_DEADLINE,
                   "packages": {p: importlib.metadata.version(p) for p in
                                ("numpy", "scipy", "sympy", "pyscipopt")},
                   "metadata_sha256": digest_file(METADATA),
                   "scan_script_sha256": digest_file(__file__),
                   "snapshot_manifest_sha256_start": manifest_start,
                   "pool_rule": POOL_RULE, "pool_size": len(models),
                   "pool_exclusions": excluded,
                   "used_names_sources": list(CAMPAIGN_CASE_DIRS) + list(CAMPAIGN_SELECTIONS),
                   "used_names_count": len(used)}
    env = {**os.environ, **THREAD_ENV, "PYTHONDONTWRITEBYTECODE": "1"}
    results, pending, running = {}, list(models), []
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="scan-v4D-") as scratch:
        scratch = Path(scratch)
        try:
            while pending or running:
                while pending and len(running) < PARALLEL:
                    model = pending.pop(0)
                    output = scratch / f"{model['name']}.json"
                    log = (scratch / f"{model['name']}.log").open("w")
                    proc = subprocess.Popen(
                        [sys.executable, __file__, "worker", model["name"], model["path"], str(output)],
                        stdout=log, stderr=subprocess.STDOUT, env=env, start_new_session=True)
                    running.append((model, proc, log, output, time.monotonic()))
                time.sleep(0.1)
                for item in list(running):
                    model, proc, log, output, begun = item
                    timed_out = False
                    if proc.poll() is None:
                        if time.monotonic() - begun < HARD_TIMEOUT:
                            continue
                        os.killpg(proc.pid, signal.SIGKILL)  # our own session only
                        proc.wait()
                        timed_out = True
                    log.close()
                    running.remove(item)
                    results[model["name"]] = collect(model, proc.returncode, timed_out,
                                                     time.monotonic() - begun, output,
                                                     scratch / f"{model['name']}.log")
                    print(f"[{len(results)}/{len(models)}] {model['name']}: "
                          f"{results[model['name']]['status']}", flush=True)
        finally:
            for _, proc, log, _, _ in running:
                if proc.poll() is None:
                    os.killpg(proc.pid, signal.SIGKILL)
                    proc.wait()
                log.close()
    manifest_end = snapshot_check()
    environment.update(finished_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                       load_end=list(os.getloadavg()), scan_wall_seconds=time.monotonic() - started,
                       snapshot_manifest_sha256_end=manifest_end,
                       snapshot_unchanged=manifest_start == manifest_end)
    with RECORDS.open("w") as stream:
        for model in models:
            stream.write(json.dumps(results[model["name"]], sort_keys=True, allow_nan=False) + "\n")
    ENVIRONMENT.write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n")
    if not environment["snapshot_unchanged"]:
        raise SystemExit("snapshot changed during the scan; records are not usable")
    report()


def collect(model, returncode, timed_out, wall, output, log):
    record = {**model, "returncode": returncode, "process_wall_seconds": wall,
              "process_timeout": timed_out}
    lines = log.read_text(errors="replace").splitlines()
    phases = [line[len(PHASE_MARK):] for line in lines if line.startswith(PHASE_MARK)]
    other = "\n".join(line for line in lines if not line.startswith(PHASE_MARK))
    if other.strip():
        record["output_tail"] = other[-2000:]
    if timed_out:
        record["phase_at_timeout"] = phases[-1] if phases else "import"
        record["diagnostic"] = (f"killed at the {HARD_TIMEOUT:.0f} s hard limit in step "
                                f"'{record['phase_at_timeout'].split()[0]}'")
    if output.exists():
        record.update(json.loads(output.read_text()))
    else:
        record["status"] = "process_timeout" if timed_out else "worker_error"
    return record


# ---------------------------------------------------------------- report

def qualifies(record):
    return (record["status"] == "admitted" and record.get("discovery_completed") is True
            and any(b["auto_eligible"] for b in record.get("blocks", ())))


def entry(record):
    return {"name": record["name"], "path": record["path"], "osil_sha256": record["osil_sha256"],
            "stratum": record["stratum"]}


def _table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


def _quantiles(values):
    if not values:
        return "n=0"
    values = sorted(values)
    q = lambda p: values[min(len(values) - 1, int(p * (len(values) - 1) + 0.5))]
    return (f"n={len(values)}, min {values[0]:.3g}, median {statistics.median(values):.3g}, "
            f"p90 {q(.9):.3g}, max {values[-1]:.3g}")


def report():
    records = [json.loads(line) for line in RECORDS.read_text().splitlines()]
    environment = json.loads(ENVIRONMENT.read_text())
    qualifying = sorted((r for r in records if qualifies(r)), key=lambda r: hard_rank(r["name"]))
    QUALIFYING.write_text(json.dumps({
        "schema": "campaign-v4-partD-qualifying-1", "pool_rule": POOL_RULE, "rule": QUALIFYING_RULE,
        "pool_names": [r["name"] for r in records], "qualifying_count": len(qualifying),
        "qualifying": [entry(r) for r in qualifying]}, indent=2) + "\n")
    groups = {"pool": records, **{s: [r for r in records if r["stratum"] == s] for s in STRATA}}
    count = lambda pred: [sum(1 for r in g if pred(r)) for g in groups.values()]
    any_block = lambda pred: (lambda r: any(pred(b) for b in r.get("blocks", ())))
    admitted = lambda r: r["status"] == "admitted"
    rows = [
        ("models", lambda r: True),
        ("admitted (build_model accepted, worker finished)", admitted),
        ("discovery completed within 60 s", lambda r: r.get("discovery_completed") is True),
        ("discovery hit the 60 s deadline", lambda r: r.get("discovery_deadline_hit") is True),
        ("discovery raised another exception", lambda r: "discovery_error" in r),
        ("process killed at the 120 s hard limit", lambda r: r["process_timeout"]),
        ("worker failed without a record", lambda r: r["status"] == "worker_error"),
        (">= 1 admitted block", any_block(lambda b: True)),
        (">= 1 quadratic block of dimension >= 2", any_block(lambda b: b["quadratic"] and b["dimension"] >= 2)),
        (">= 1 block with >= 2 distinct nonlinear rows", any_block(lambda b: b["nonlinear_rows"] >= 2)),
        (">= 1 auto-eligible block (qualifying)", qualifies),
        ("block cap (32) reached", lambda r: r.get("discovery_stats", {}).get("block_cap_reached") is True),
    ]
    refused = Counter(r["status"] for r in records if not admitted(r))
    out = ["# Campaign 4, Part D: pool and structural scan", "",
           "Generated by `scan_d.py` from `records.jsonl`. Import and block discovery only; no",
           "optimization outcome was used for the scan or the qualification.",
           f"`scan_d.py` SHA-256 at scan start: {environment['scan_script_sha256']}.", "",
           f"- Pool rule: {POOL_RULE}",
           f"- Pool: {len(records)} models; exclusions after the metadata filter: "
           + (", ".join(f"{k} ({v})" for k, v in sorted(environment["pool_exclusions"].items())) or "none") + ".",
           f"- Scan: {environment['started_utc']} to {environment['finished_utc']}, "
           f"{environment['scan_wall_seconds']:.0f} s wall, {environment['parallel_processes']} single-threaded "
           f"processes on a shared host ({environment['logical_cpus']} logical CPUs; 1-min load "
           f"{environment['load_start'][0]:.1f} at start, {environment['load_end'][0]:.1f} at end).",
           f"- Per model: fresh subprocess, `read_osil`, `build_model`, then `discover` with the frozen "
           f"`Config()` and an absolute deadline of {environment['discovery_deadline_seconds']:.0f} s after "
           f"discovery starts; {environment['hard_timeout_seconds']:.0f} s hard process limit.",
           f"- Code: campaign-4 snapshot, manifest SHA-256 {environment['snapshot_manifest_sha256_start']} "
           f"(unchanged during the scan: {environment['snapshot_unchanged']}).", "",
           "## Model counts", "",
           _table(["", *groups], [(label, *count(pred)) for label, pred in rows]), "",
           "## Refusals by reason", ""]
    if refused:
        out.append(_table(["status", *groups], [(s, *count(lambda r, s=s: r["status"] == s))
                                                for s, _ in refused.most_common()]))
        out.append("")
        for status, _ in refused.most_common():
            diagnostics = Counter((r.get("diagnostic") or "")[:160] for r in records if r["status"] == status)
            out.append(f"- `{status}`: " + "; ".join(f"{d or '(no diagnostic)'} ({n})"
                                                     for d, n in diagnostics.most_common()))
    else:
        out.append("None.")
    killed = [r["name"] for r in records if r["process_timeout"] or r["status"] == "worker_error"]
    deadline = [r["name"] for r in records if r.get("discovery_deadline_hit")]
    out += ["", f"Deadline hits ({len(deadline)}): {', '.join(deadline) or 'none'}.",
            f"Hard-limit kills or worker failures ({len(killed)}): {', '.join(killed) or 'none'}.", "",
            "## Times", ""]
    for k, g in groups.items():
        out.append(f"- {k}: build {_quantiles([r['build_seconds'] for r in g if admitted(r)])}; discovery "
                   f"{_quantiles([r['discovery_seconds'] for r in g if r.get('discovery_completed')])}")
    out += ["", "## Qualifying models", "", f"Rule: {QUALIFYING_RULE}", "",
            f"Qualifying: {len(qualifying)} of {len(records)}, listed in hard-hash rank order:", "",
            _table(["rank", "name", "stratum", "variables", "auto-eligible blocks"],
                   [(i + 1, r["name"], r["stratum"], r.get("variables"),
                     sum(b["auto_eligible"] for b in r.get("blocks", ())))
                    for i, r in enumerate(qualifying)]), ""]
    if SELECTION.exists():
        picked = json.loads(SELECTION.read_text())
        out += ["## Screening and selection", "", f"Rule: {SELECTION_RULE}", "",
                f"Screened {picked['screened']} qualifying models; solved {picked['solved_count']}, "
                f"hard {len(picked['hard_qualifying_names_in_rank_order'])}; selected {len(picked['selected'])}.", "",
                _table(["rank", "name", "stratum", "screen status", "screen seconds", "hard", "selected"],
                       [(i + 1, n, picked["screen"][n]["stratum"], picked["screen"][n]["status"],
                         f"{picked['screen'][n]['seconds']:.1f}" if picked["screen"][n]["seconds"] is not None else "-",
                         "yes" if not picked["screen"][n]["solved"] else "no",
                         "yes" if n in {e["name"] for e in picked["selected"]} else "")
                        for i, n in enumerate(picked["screen_order"])]), ""]
    SUMMARY.write_text("\n".join(out))


# ---------------------------------------------------------------- selection

def solved(r):
    check = r.get("primal_check") or {}
    return (r.get("status") in ("optimal", "gaplimit") and r.get("status") not in FAILURES
            and not r.get("worker_status") and r.get("returncode", 0) == 0
            and check.get("checked") is True and check.get("passed") is True
            and isinstance(r.get("primal"), (int, float)) and math.isfinite(r["primal"]))


def select():
    qualifying = json.loads(QUALIFYING.read_text())
    jobs = json.loads((SCREEN_DIR / "jobs.json").read_text())
    build = json.loads((SCREEN_DIR / "build.json").read_text())
    if build["selection_sha256"] != digest_file(QUALIFYING) or build["part"] != "partD-screen":
        raise SystemExit("screen directory was not built from the current qualifying.json")
    records = [json.loads(line) for line in (SCREEN_DIR / "records.jsonl").read_text().splitlines() if line]
    by_name = {}
    for r in records:
        if r["name"] in by_name:
            raise SystemExit(f"two screening records for {r['name']}")
        by_name[r["name"]] = r
    names = [e["name"] for e in qualifying["qualifying"]]
    scheduled = sorted(job["name"] for job in jobs["jobs"])
    if scheduled != sorted(names) or sorted(by_name) != sorted(names):
        raise SystemExit("screening is incomplete or covers other models")
    if any(r["mode"] != "baseline" or r["seed"] != 0 or r["time_limit"] != 60.0 for r in records):
        raise SystemExit("screening runs differ from the protocol (baseline, seed 0, 60 s)")
    shutil.copyfile(SCREEN_DIR / "records.jsonl", SCREEN_RECORDS)
    entries = {e["name"]: e for e in qualifying["qualifying"]}
    order = sorted(names, key=hard_rank)
    hard = [n for n in order if not solved(by_name[n])]
    screen = {n: {"status": by_name[n].get("status"), "solved": solved(by_name[n]),
                  "seconds": (by_name[n]["total_seconds"] + by_name[n].get("preparation_seconds", 0.0))
                  if "total_seconds" in by_name[n] else None,
                  "primal": by_name[n].get("primal"), "dual": by_name[n].get("dual"),
                  "stratum": entries[n]["stratum"]} for n in order}
    selection = {"schema": "campaign-v4-partD-selection-1",
                 "rule": f"{POOL_RULE} {QUALIFYING_RULE} {SELECTION_RULE}",
                 "pool_names": qualifying["pool_names"], "pool_size": len(qualifying["pool_names"]),
                 "qualifying_count": len(names), "screened": len(records),
                 "solved_count": sum(v["solved"] for v in screen.values()),
                 "screen_directory": str(SCREEN_DIR), "screen_records_sha256": digest_file(SCREEN_RECORDS),
                 "qualifying_sha256": digest_file(QUALIFYING),
                 "screen_order": order, "screen": screen,
                 "hard_qualifying_names_in_rank_order": hard,
                 "selected": [entries[n] for n in hard[:SELECTION_SIZE]]}
    SELECTION.write_text(json.dumps(selection, indent=2) + "\n")
    report()
    print(json.dumps({"qualifying": len(names), "hard": len(hard),
                      "selected": [e["name"] for e in selection["selected"]]}))


if __name__ == "__main__":
    if sys.argv[1:2] == ["worker"]:
        worker(*sys.argv[2:5])
    elif sys.argv[1:] == ["run"]:
        run()
    elif sys.argv[1:] == ["report"]:
        report()
    elif sys.argv[1:] == ["select"]:
        select()
    else:
        raise SystemExit(__doc__)
