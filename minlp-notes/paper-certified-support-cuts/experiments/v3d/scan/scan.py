"""Campaign v3, Part S: structural scan (block discovery only, no optimization).

Implements Part S of ``../../campaign-v3-protocol.md`` and the Part B
selection rule. Usage:

    scan.py run       scan the pool, write records.jsonl, then report
    scan.py report    rewrite scan-summary.md and partB-selection.json
                      from records.jsonl

The research solver is imported read-only from the live tree; the SHA-256 of
every imported solver source is recorded before and after the scan. Each
model runs in a fresh single-threaded subprocess with a hard wall limit; at
most three subprocesses run at a time. No solver bound and no archived
optimization outcome is read.
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
import signal
import statistics
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
TOPIC = REPO / "research-20261003-convexification"
DEPENDENCY = REPO / "research-20261002-convexification"
OSIL_DIR = Path.home() / ".cache/minlplib/minlplib/osil"
HOLDOUT = TOPIC / "experiments/holdout-selection.json"
METADATA = REPO / "code/minlp_solver_lab/instances/instancedata.csv"
RECORDS = HERE / "records.jsonl"
ENVIRONMENT = HERE / "scan-environment.json"
SUMMARY = HERE / "scan-summary.md"
SELECTION = HERE / "partB-selection.json"

DISCOVERY_DEADLINE = 60.0
HARD_TIMEOUT = 90.0
PARALLEL = 3
SELECTION_SIZE = 30
RANK_PREFIX = "convexification-structure-v3:"
PHASE_MARK = "scan-phase: "
STRATA = ("convex", "nonconvex_continuous", "nonconvex_integer")
THREAD_ENV = {k: "1" for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                              "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS",
                              "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")}
# Sources reached by read_osil, build_model and discover.
SOURCES = (TOPIC / "solver/__init__.py", TOPIC / "solver/integration.py",
           TOPIC / "solver/model.py", TOPIC / "solver/bounds.py",
           TOPIC / "solver/row_certificate.py",
           DEPENDENCY / "solver/model_binding.py", DEPENDENCY / "solver/certified.py",
           REPO / "code/univariate_envelopes/uenv/osil.py")
PROTOCOL_RULE = ("From the Part S pool, a model qualifies if it is admitted and discovery "
                 "finds at least one block that the frozen auto rule admits. Rank qualifying "
                 "models by SHA-256 of `convexification-structure-v3:` + name and take the "
                 "first 30 (all of them if fewer qualify).")
OPERATIONAL_RULE = ("Qualifying: build_model accepted the model, discover with the frozen "
                    "Config completed within its 60 s deadline, and at least one returned "
                    "block has auto_eligible true. Rank: ascending hex SHA-256 of the UTF-8 "
                    "string 'convexification-structure-v3:' + name.")


def digest_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_hashes():
    return {str(p.relative_to(REPO)): digest_file(p) for p in SOURCES}


def structure_rank(name):
    return hashlib.sha256((RANK_PREFIX + name).encode("utf-8")).hexdigest()


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
    phase("read", started)
    read_start = time.perf_counter()
    try:
        inst = read_osil(str(path))
    except (OSError, ET.ParseError, ValueError, TypeError, KeyError, IndexError,
            NotImplementedError, RecursionError) as error:
        # Same exception set that run_instance reports as unsupported_input.
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
        # One signed side per finite row side, plus the objective side when an
        # epigraph variable exists; this is the list signed_sides() returns.
        record["signed_sides"] = int(built.objective_var is not None) + sum(
            math.isfinite(row["ub"]) + math.isfinite(row["lb"]) for row in inst.rows[1:])
        phase("discover", started)
        discovery_start = time.perf_counter()
        detected = None
        try:
            # As in RowSeparator: an absolute perf_counter deadline.
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
    """Mark the current step, so a hard-limit kill can be attributed."""
    print(f"{PHASE_MARK}{name} {time.perf_counter() - started:.3f}", flush=True)


def finish(record, output):
    record["load_end"] = list(os.getloadavg())
    temporary = Path(output).with_suffix(".tmp")
    temporary.write_text(json.dumps(record, sort_keys=True, allow_nan=False))
    temporary.replace(output)


# ---------------------------------------------------------------- pool

def stratum(row):
    # Rule of research-20261003-convexification/experiments/select_holdout.py.
    integer = int(row["nbinvars"]) + int(row["nintvars"]) > 0
    return ("convex" if row["convex"] == "True" else
            "nonconvex_integer" if integer else "nonconvex_continuous")


def pool():
    holdout = json.loads(HOLDOUT.read_text())
    with METADATA.open() as stream:
        metadata = {r["name"]: r for r in csv.DictReader(stream, delimiter=";")}
    eligible = holdout["eligible_names_in_rank_order"]
    strata = {name: stratum(metadata[name]) for name in eligible}
    # The recomputed strata must reproduce the frozen eligible counts and
    # the strata stored for the selected models.
    if Counter(strata.values()) != Counter(holdout["stratum_eligible_counts"]):
        raise ValueError("recomputed strata differ from holdout-selection.json")
    if any(strata[e["name"]] != e["stratum"] for e in holdout["selected"]):
        raise ValueError("recomputed stratum differs for a v2 holdout model")
    excluded = {e["name"] for e in holdout["selected"]}
    names = [n for n in eligible if n not in excluded]
    if len(eligible) != 422 or len(excluded) != 30 or len(names) != 392:
        raise ValueError("unexpected pool size")
    return [{"name": n, "stratum": strata[n], "path": str(OSIL_DIR / f"{n}.osil"),
             "osil_sha256": digest_file(OSIL_DIR / f"{n}.osil")} for n in names]


# ---------------------------------------------------------------- driver

def run():
    os.environ.update(THREAD_ENV)
    if RECORDS.exists():
        raise SystemExit(f"{RECORDS} exists; remove it to rescan")
    models = pool()
    hashes_start = source_hashes()
    environment = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "python": sys.version, "executable": sys.executable,
                   "platform": platform.platform(), "logical_cpus": os.cpu_count(),
                   "load_start": list(os.getloadavg()), "thread_environment": THREAD_ENV,
                   "parallel_processes": PARALLEL, "hard_timeout_seconds": HARD_TIMEOUT,
                   "discovery_deadline_seconds": DISCOVERY_DEADLINE,
                   "packages": {p: importlib.metadata.version(p) for p in
                                ("numpy", "scipy", "sympy", "pyscipopt")},
                   "holdout_selection_sha256": digest_file(HOLDOUT),
                   "metadata_sha256": digest_file(METADATA),
                   "scan_script_sha256": digest_file(__file__),
                   "source_sha256_start": hashes_start}
    env = {**os.environ, **THREAD_ENV, "PYTHONDONTWRITEBYTECODE": "1"}
    results, pending, running = {}, list(models), []
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="scan-v3-") as scratch:
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
    hashes_end = source_hashes()
    environment.update(finished_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                       load_end=list(os.getloadavg()),
                       scan_wall_seconds=time.monotonic() - started,
                       source_sha256_end=hashes_end,
                       sources_unchanged=hashes_start == hashes_end)
    with RECORDS.open("w") as stream:
        for model in models:
            stream.write(json.dumps(results[model["name"]], sort_keys=True, allow_nan=False) + "\n")
    ENVIRONMENT.write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n")
    if not environment["sources_unchanged"]:
        raise SystemExit("solver sources changed during the scan; records are not usable")
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
        # "<step> <seconds since worker start when the step began>"
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


def selection(records):
    qualifying = sorted((r for r in records if qualifies(r)), key=lambda r: structure_rank(r["name"]))
    return {"rule": PROTOCOL_RULE + " Operational reading: " + OPERATIONAL_RULE,
            "pool_size": len(records), "qualifying_count": len(qualifying),
            "qualifying_names_in_rank_order": [r["name"] for r in qualifying],
            "selected": [{"name": r["name"], "path": r["path"], "osil_sha256": r["osil_sha256"],
                          "stratum": r["stratum"]} for r in qualifying[:SELECTION_SIZE]]}


def _blocks(records):
    return [b for r in records for b in r.get("blocks", ())]


def _bin(value, edges):
    """Label of the first edge interval [lo, hi] containing value."""
    for lo, hi in edges:
        if lo <= value <= hi:
            return str(lo) if lo == hi else f"{lo}-{hi}"
    raise ValueError(value)


def _quantiles(values):
    if not values:
        return "n=0"
    values = sorted(values)
    def q(p):
        return values[min(len(values) - 1, int(p * (len(values) - 1) + 0.5))]
    return (f"n={len(values)}, min {values[0]:.3g}, median {statistics.median(values):.3g}, "
            f"p90 {q(.9):.3g}, max {values[-1]:.3g}")


def _table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


def report():
    records = [json.loads(line) for line in RECORDS.read_text().splitlines()]
    environment = json.loads(ENVIRONMENT.read_text())
    picked = selection(records)
    SELECTION.write_text(json.dumps(picked, indent=2) + "\n")
    groups = {"all": records, **{s: [r for r in records if r["stratum"] == s] for s in STRATA}}
    header = ["", "pool", *STRATA]

    def count(pred):
        return [sum(1 for r in g if pred(r)) for g in groups.values()]

    def any_block(pred):
        return lambda r: any(pred(b) for b in r.get("blocks", ()))

    admitted = lambda r: r["status"] == "admitted"
    model_rows = [
        ("models", lambda r: True),
        ("admitted (build_model accepted, worker finished)", admitted),
        ("discovery completed within 60 s", lambda r: r.get("discovery_completed") is True),
        ("discovery hit the 60 s deadline", lambda r: r.get("discovery_deadline_hit") is True),
        ("discovery raised another exception", lambda r: "discovery_error" in r),
        ("process killed at 90 s hard limit", lambda r: r["process_timeout"]),
        ("worker failed without a record", lambda r: r["status"] == "worker_error"),
        (">= 1 admitted block", any_block(lambda b: True)),
        (">= 1 quadratic block of dimension >= 2", any_block(lambda b: b["quadratic"] and b["dimension"] >= 2)),
        (">= 1 block with >= 2 nonlinear sides", any_block(lambda b: b["nonlinear_sides"] >= 2)),
        (">= 1 block with >= 2 distinct nonlinear rows", any_block(lambda b: b["nonlinear_rows"] >= 2)),
        (">= 1 auto-eligible block (Part B qualifying)", qualifies),
        ("block cap (32) reached", lambda r: r.get("discovery_stats", {}).get("block_cap_reached") is True),
    ]
    out = [
        "# Campaign v3, Part S: structural scan",
        "",
        "Generated by `scan.py` from `records.jsonl`. Block discovery only; no",
        "optimization was run and no archived solver outcome was read.",
        f"`scan.py` SHA-256 at scan start: {environment['scan_script_sha256']}.",
        "",
        f"- Scan: {environment['started_utc']} to {environment['finished_utc']}, "
        f"{environment['scan_wall_seconds']:.0f} s wall, {environment['parallel_processes']} "
        f"single-threaded processes on a shared host ({environment['logical_cpus']} logical CPUs; "
        f"1-min load {environment['load_start'][0]:.1f} at start, {environment['load_end'][0]:.1f} at end).",
        f"- Per model: fresh subprocess, `read_osil`, `build_model`, then `discover` with the frozen "
        f"`Config()` and an absolute deadline of {environment['discovery_deadline_seconds']:.0f} s after "
        f"discovery starts; {environment['hard_timeout_seconds']:.0f} s hard process limit.",
        f"- Pool: the {len(records)} models of `holdout-selection.json` "
        "(`eligible_names_in_rank_order`) minus its 30 `selected` models. Strata are recomputed from "
        "`instancedata.csv` with the `select_holdout.py` rule and reproduce the frozen counts.",
        "- Solver sources (live tree, read-only; unchanged during the scan: "
        f"{environment['sources_unchanged']}):",
        *[f"  - `{k}` {v}" for k, v in sorted(environment["source_sha256_start"].items())],
        "",
        "## Model counts",
        "",
        _table(header, [(label, *count(pred)) for label, pred in model_rows]),
        "",
        "\"Admitted block\" means a block returned by `discover`. \"Nonlinear sides\" counts signed",
        "sides, so an equality row contributes two sides of one row. A model killed at the hard",
        "limit has status `process_timeout` and no discovery result, so it does not qualify for",
        "Part B; its diagnostic names the step in which it was killed.",
        "",
        "## Refusals by reason",
        "",
    ]
    refused = Counter(r["status"] for r in records if not admitted(r))
    out.append(_table(["status", "pool", *STRATA],
                      [(s, *[sum(1 for r in g if r["status"] == s) for g in groups.values()])
                       for s, _ in refused.most_common()]))
    out.append("")
    for status, _ in refused.most_common():
        diagnostics = Counter(r.get("diagnostic", "") for r in records if r["status"] == status)
        out.append(f"- `{status}`: " + "; ".join(
            f"{d or '(no diagnostic)'} ({n})" for d, n in diagnostics.most_common()))
    errors = [r for r in records if "discovery_error" in r]
    if errors:
        out += ["", "Discovery exceptions other than the deadline:", ""]
        out += [f"- {r['name']}: {r['discovery_error']}" for r in errors]
    deadline = [r["name"] for r in records if r.get("discovery_deadline_hit")]
    killed = [r["name"] for r in records if r["process_timeout"] or r["status"] == "worker_error"]
    out += ["", f"Deadline hits ({len(deadline)}): {', '.join(deadline) or 'none'}.",
            f"Hard-limit kills or worker failures ({len(killed)}): {', '.join(killed) or 'none'}.", ""]

    blocks = {k: _blocks(g) for k, g in groups.items()}
    out += ["## Block distributions", "",
            "Counts of blocks over all models with completed discovery.", ""]
    out.append(_table(header, [("blocks", *[len(b) for b in blocks.values()]),
                               ("quadratic blocks", *[sum(x["quadratic"] for x in b) for b in blocks.values()]),
                               ("auto-eligible blocks", *[sum(x["auto_eligible"] for x in b) for b in blocks.values()])]))
    for title, key, edges in (
            ("Block dimension", "dimension", [(1, 1), (2, 2), (3, 3), (4, 4)]),
            ("Nonlinear sides per block", "nonlinear_sides", [(k, k) for k in range(1, 7)]),
            ("Distinct nonlinear rows per block", "nonlinear_rows", [(k, k) for k in range(1, 7)]),
            ("Affine domain rows per block", "affine_domain_rows",
             [(0, 0), (1, 1), (2, 4), (5, 15), (16, 16)])):
        labels = [str(lo) if lo == hi else f"{lo}-{hi}" for lo, hi in edges]
        hist = {k: Counter(_bin(x[key], edges) for x in b) for k, b in blocks.items()}
        out += ["", f"{title}:", "", _table([key, "pool", *STRATA],
                                            [(lab, *[hist[k][lab] for k in groups]) for lab in labels])]
    out += ["", "Quadratic blocks by dimension (auto-eligible in parentheses):", ""]
    out.append(_table(["dimension", "pool", *STRATA], [
        (d, *[f"{sum(x['quadratic'] and x['dimension'] == d for x in b)} "
              f"({sum(x['auto_eligible'] and x['dimension'] == d for x in b)})" for b in blocks.values()])
        for d in (1, 2, 3, 4)]))
    per_model = [(0, 0), (1, 1), (2, 4), (5, 8), (9, 16), (17, 31), (32, 32)]
    completed = {k: [r for r in g if r.get("discovery_completed")] for k, g in groups.items()}
    hist = {k: Counter(_bin(len(r["blocks"]), per_model) for r in g) for k, g in completed.items()}
    out += ["", "Blocks per model (models with completed discovery):", "",
            _table(["blocks", "pool", *STRATA],
                   [(lab, *[hist[k][lab] for k in groups])
                    for lab in (str(lo) if lo == hi else f"{lo}-{hi}" for lo, hi in per_model)])]
    out += ["", "Signed sides per admitted model, and nonlinear signed sides seen by discovery:", ""]
    for k, g in groups.items():
        out.append(f"- {k}: signed sides {_quantiles([r['signed_sides'] for r in g if 'signed_sides' in r])}; "
                   f"nonlinear sides {_quantiles([r['discovery_stats']['nonlinear_sides'] for r in g if 'discovery_stats' in r])}; "
                   f"unsupported nonlinear sides {_quantiles([r['discovery_stats']['unsupported_sides'] for r in g if 'discovery_stats' in r])}")

    # The deadline is checked cooperatively, so a completed call may end after 60 s.
    times = [(0, 0.1), (0.1, 1), (1, 10), (10, math.inf)]
    out += ["", "## Discovery time", "",
            "Wall seconds of `discover` for admitted models (timing is load-dependent).", ""]
    rows = []
    for lo, hi in times:
        rows.append((f"[{lo}, {hi}) s", *[sum(1 for r in g if r.get("discovery_completed")
                                               and lo <= r["discovery_seconds"] < hi) for g in groups.values()]))
    rows.append(("deadline hit", *count(lambda r: r.get("discovery_deadline_hit") is True)))
    out.append(_table(["discovery time", "pool", *STRATA], rows))
    out.append("")
    for k, g in groups.items():
        out.append(f"- {k}: completed {_quantiles([r['discovery_seconds'] for r in g if r.get('discovery_completed')])}")
    out += ["", "Build time for admitted models:", ""]
    for k, g in groups.items():
        out.append(f"- {k}: {_quantiles([r['build_seconds'] for r in g if admitted(r)])}")

    out += ["", "## Part B selection", "",
            f"Rule: {picked['rule']}", "",
            f"Qualifying models: {picked['qualifying_count']} of {picked['pool_size']}; "
            f"selected {len(picked['selected'])}.", ""]
    out.append(_table(["rank", "name", "stratum"],
                      [(i + 1, s["name"], s["stratum"]) for i, s in enumerate(picked["selected"])]))
    by = Counter(s["stratum"] for s in picked["selected"])
    out += ["", "Selected by stratum: " + ", ".join(f"{s} {by[s]}" for s in STRATA) + ".", ""]
    SUMMARY.write_text("\n".join(out))


if __name__ == "__main__":
    if sys.argv[1:2] == ["worker"]:
        worker(*sys.argv[2:5])
    elif sys.argv[1:] == ["run"]:
        run()
    elif sys.argv[1:] == ["report"]:
        report()
    else:
        raise SystemExit(__doc__)
