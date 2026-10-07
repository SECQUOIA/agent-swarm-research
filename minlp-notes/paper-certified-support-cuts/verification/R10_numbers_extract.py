#!/usr/bin/env python3
"""R10 (numbers lens): stream one part's records.jsonl and write a compact
per-record summary (one JSON line per record) for R10_numbers_check.py.

Standard library only; imports no producer code.

Usage: R10_numbers_extract.py <part dir relative to experiments/> <output.jsonl>

Per cut it keeps: a distinct-row key (SHA-256 of model SHA-256, exported
binary64 coefficients, orientation and rhs), the block dimension, the
certificate method, whether any coefficient was rounded (nonzero exact
rounding error), the bound correction E (box_compensation, as float), the
direction class for single-side cuts (remainder / row / other), and the
exported coefficient of the block's second variable (y in the path family).
"""
import hashlib
import gzip
import io
import json
import os
import sys
from contextlib import ExitStack
from fractions import Fraction as Q

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.join(HERE, "..", "experiments")

KEEP = [
    "run_id", "name", "mode", "phase", "seed", "status", "returncode", "worker_status",
    "primal", "dual", "root_dual", "nodes", "node_limit", "time_limit", "total_seconds",
    "preparation_seconds", "scip_solve_seconds", "solver_runtime_seconds", "outer_wall_seconds",
    "sense", "cut_log_complete", "load_start", "load_end", "started_utc", "ended_utc",
    "active_runs_start", "active_runs_end", "suite", "part", "worker_timeout", "solver_mode",
    "discovery_seconds", "model_sha256", "gap", "mip_gap", "worker_error",
    "attempt", "job_id", "driver_session", "driver_workers", "config", "config_overrides",
    "scip_params", "scip_version", "solver_time_limit", "bound_status", "coverage",
    "build_seconds", "read_seconds", "source_read_seconds", "primal_check_seconds",
    "reference_witness_check", "row_binding_rejection_causes", "solve_wall_seconds",
    "worker_import_and_load_seconds", "worker_total_seconds", "snapshot_modules_verified",
    "process_timeout", "process_wall_seconds", "import_seconds", "osil_sha256", "stratum",
    "discovery_completed", "discovery_deadline_hit", "discovery_deadline_seconds", "discovery_stats",
]


def direction_class(cut):
    try:
        a = cut["coefficients"]
        d = len(cut["variables"])
        sides = cut["signed_sides"]
        if len(sides) != 1 or len(a) != d + 1:
            return "multi"
        lam = Q(a[d])
        aff = {k: Q(v) for k, v in sides[0]["affine_terms"]}
        syms = cut["symbols"]
        if all(Q(x) == 0 for x in a[:d]):
            return "remainder"
        if all(Q(a[k]) == lam * aff.get(syms[k], Q(0)) for k in range(d)):
            return "row"
        return "other"
    except Exception:
        return "unknown"


def cut_summary(cut, model_sha):
    rc = cut.get("row_certificate") or {}
    exp = rc.get("exported") or {}
    ex = rc.get("exact") or {}
    key_src = json.dumps([model_sha, exp.get("coefficients"), exp.get("orientation"), exp.get("rhs")])
    key = hashlib.sha256(key_src.encode()).hexdigest()[:24]
    errs = ex.get("rounding_errors") or []
    rounded = any(e not in ("0", "-0", "0/1", 0) for e in errs)
    try:
        E = float(Q(ex.get("box_compensation", "0")))
    except Exception:
        E = None
    sw = cut.get("support_witness") or {}
    method = sw.get("method")
    # exported coefficient of the block's second variable (y_i in the path family)
    ycoef = None
    try:
        v = cut["variables"]
        if len(v) >= 2:
            ycoef = float(Q(ex["coefficients"][v[1]]))
    except Exception:
        ycoef = None
    return {
        "k": key,
        "d": len(cut.get("variables") or []),
        "m": method,
        "r": rounded,
        "E": E,
        "c": direction_class(cut),
        "y": ycoef,
        "b": cut.get("block"),
    }


def extract(part, out):
    path = os.path.join(EXP, part, "records.jsonl")
    n = 0
    source_hash = hashlib.sha256()
    source_bytes = 0
    statuses = {}
    cut_count = 0
    outputs = ExitStack()
    if str(out).endswith(".gz"):
        destination = outputs.enter_context(open(out, "wb"))
        compressed = outputs.enter_context(gzip.GzipFile(filename="", mode="wb", fileobj=destination, mtime=0))
        oh = io.TextIOWrapper(compressed, encoding="utf-8")
    else:
        oh = open(out, "w", encoding="utf-8")
    with outputs, open(path, "rb") as fh, oh:
        for line in fh:
            source_hash.update(line)
            source_bytes += len(line)
            if not line.strip():
                continue
            r = json.loads(line)
            s = {k: r.get(k) for k in KEEP}
            if r.get("run_id") is None:
                # Structural scan records have model names, rather than run IDs.
                # They are small and keep their complete selection evidence.
                s.update(r)
            s["part_dir"] = part
            sep = r.get("separation")
            s["separation"] = sep if isinstance(sep, dict) else None
            disc = r.get("discovery")
            if isinstance(disc, dict):
                s["discovery"] = {k: v for k, v in disc.items() if not isinstance(v, (list, dict))}
                if "star_blocks" in disc:
                    s["discovery"]["star_blocks"] = disc["star_blocks"]
            else:
                s["discovery"] = None
            s["primal_check"] = r.get("primal_check")
            rc = r.get("reference_check") or {}
            s["reference_value"] = rc.get("value")
            s["cut_methods"] = r.get("cut_methods")
            s["certification_summary"] = r.get("certification_summary")
            cl = r.get("certification_log") or {}
            calls = cl.get("calls") or []
            fields = cl.get("fields") or []
            if calls and fields:
                idx = {f: i for i, f in enumerate(fields)}
                s["cert_calls"] = [[c[idx["dimension"]], c[idx["method"]], c[idx["certified"]],
                                    c[idx["seconds"]]] for c in calls]
            else:
                s["cert_calls"] = []
            rb = r.get("row_binding_rejection_causes") or {}
            s["binding_causes"] = rb.get("causes")
            ns = r.get("native_statistics") or {}
            seps = ns.get("separators") or {}
            s["native"] = {k: {kk: seps[k].get(kk) for kk in ("Calls", "FoundCuts", "Applied")}
                           for k in ("minor", "interminor", "eccuts", "rlt") if k in seps}
            nl = ns.get("nlhdlrs") or {}
            if "quadratic" in nl:
                s["native"]["nlhdlr_quadratic"] = {kk: nl["quadratic"].get(kk) for kk in ("Cuts", "#Enforce")}
            cuts = r.get("cuts") or []
            s["n_cuts"] = len(cuts)
            ms = r.get("model_sha256")
            s["cuts"] = [cut_summary(c, ms) for c in cuts]
            # variable names of the original model (path family roles) - only first 8
            om = r.get("original_model") or {}
            vn = om.get("var_names") or []
            s["n_vars"] = len(vn)
            oh.write(json.dumps(s, separators=(",", ":")) + "\n")
            n += 1
            status = str(r.get("status"))
            statuses[status] = statuses.get(status, 0) + 1
            cut_count += len(cuts)
    print(part, n, "records", file=sys.stderr)
    return {"source": part + "/records.jsonl", "source_sha256": source_hash.hexdigest(),
            "source_bytes": source_bytes, "records": n, "cuts": cut_count, "statuses": statuses}


def main():
    extract(*sys.argv[1:3])


if __name__ == "__main__":
    main()
