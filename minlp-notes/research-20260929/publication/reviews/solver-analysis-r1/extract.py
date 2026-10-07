#!/usr/bin/env python3
"""Independent re-extraction of the final solver campaign (reviewer code).

Reads only raw artifacts in solver-runs/runs/*/ (run.json, trace.trc,
gams.log, <inst>.lst, cmd.txt) and driver.log. Writes extract.json and
extract.csv next to this script. Does not import the author's code.
"""
import csv
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SR = HERE.parent.parent / "solver-runs"
RUNS = SR / "runs"


def trace(path):
    if not path.exists():
        return None
    hdr, rows = "", []
    for ln in path.read_text(errors="replace").splitlines():
        if ln.startswith("*"):
            b = ln[1:].strip()
            if b.startswith(",") or b.startswith("InputFileName"):
                hdr += b
        elif ln.strip():
            rows.append(ln.strip())
    if not rows:
        return {"_nrecords": 0}
    keys = hdr.split(",")
    d = dict(zip(keys, rows[-1].split(",")))
    d["_nrecords"] = len(rows)
    return d


def allm(pat, text):
    return re.findall(pat, text, re.M)


def log_info(text, solver):
    r = {}
    r["gams_threads"] = allm(r"^\s+Threads (\S+)\s*$", text)
    r["gams_reslim"] = allm(r"^\s+ResLim (\S+)\s*$", text)
    r["gams_optcr"] = allm(r"^\s+OptCR (\S+)\s*$", text)
    r["gams_optca"] = allm(r"^\s+OptCA (\S+)\s*$", text)
    r["job_stop"] = bool(re.search(r"^--- Job \S+ Stop", text, re.M))
    r["status_line"] = (allm(r"^\*\*\* Status: (.*)$", text) or [None])[-1]
    r["optfile"] = bool(re.search(r"(?i)reading parameter\(s\) from|optfile", text))
    if solver == "BARON":
        r["log_dual"] = (allm(r"^Best possible\s*=\s*(\S+)", text) or [None])[-1]
        r["log_primal"] = (allm(r"^Solution\s*=\s*(\S+)", text) or [None])[-1]
        r["solver_threads"] = []
        r["solver_timelimit"] = None
        r["cpu_used"] = (allm(r"Total CPU time used:\s*(\S+)", text) or [None])[-1]
        r["wall_used"] = (allm(r"Wall clock time:\s*(\S+)", text) or [None])[-1]
    elif solver == "GUROBI":
        m = allm(r"Best objective (\S+), best bound (\S+), gap", text)
        r["log_primal"], r["log_dual"] = (m[-1] if m else (None, None))
        r["solver_threads"] = allm(r"using up to (\d+) threads", text) + allm(r"Thread count was (\d+) ", text) \
            + allm(r"^\s+Threads\s+(\d+)\s*$", text)[1:]  # first match is the GAMS echo
        r["solver_timelimit"] = (allm(r"^\s+TimeLimit\s+(\S+)", text) or [None])[-1]
        r["obj_bound_line"] = (allm(r"^\.\.\. Objective Bound:\s*(\S+)", text) or [None])[-1]
    else:
        r["log_dual"] = (allm(r"^Dual Bound\s*:\s*(\S+)", text) or [None])[-1]
        r["log_primal"] = (allm(r"^Primal Bound\s*:\s*(\S+)", text) or [None])[-1]
        r["solver_threads"] = allm(r"^lp/threads = (\d+)", text)
        r["solver_timelimit"] = (allm(r"^limits/time = (\S+)", text) or [None])[-1]
        r["scip_status"] = (allm(r"^SCIP Status\s*:\s*(.*)$", text) or [None])[-1]
    r["errors"] = [ln.strip() for ln in text.splitlines()
                   if re.search(r"(?i)cannot handle|error \d|capabilit|not supported", ln)][:3]
    return r


def lst_status(path):
    if not path.exists():
        return None, None
    t = path.read_text(errors="replace")
    s = allm(r"^\*\*\*\* SOLVER STATUS\s+(\d+)", t)
    m = allm(r"^\*\*\*\* MODEL STATUS\s+(\d+)", t)
    return (int(m[-1]) if m else None), (int(s[-1]) if s else None)


def main():
    out = []
    for d in sorted(RUNS.iterdir()):
        if not d.is_dir():
            continue
        inst, solver = d.name.split("__")
        meta = json.loads((d / "run.json").read_text())
        tr = trace(d / "trace.trc")
        log = (d / "gams.log").read_text(errors="replace") if (d / "gams.log").exists() else ""
        li = log_info(log, solver)
        lms, lss = lst_status(d / f"{inst}.lst")
        cmd = meta.get("cmd", [])
        cmdtxt = (d / "cmd.txt").read_text() if (d / "cmd.txt").exists() else ""
        out.append({
            "instance": inst, "solver": solver, "sense": meta.get("sense"), "model_type": meta.get("model_type"),
            "attempt": meta.get("attempt"), "attempts_total": meta.get("attempts_total"),
            "finished": meta.get("finished"), "valid": meta.get("valid"), "end_kind": meta.get("end_kind"),
            "kill_reason": meta.get("kill_reason"), "kill_stage": meta.get("kill_stage"),
            "kept_best": meta.get("kept_best"), "driver_pid": meta.get("driver_pid"),
            "wall_s": meta.get("wall_s"), "cpu_s": meta.get("cpu_s"), "cpu_over_wall": meta.get("cpu_over_wall"),
            "start_utc": meta.get("start_utc"), "end_utc": meta.get("end_utc"),
            "cmd_threads1": "threads=1" in cmd, "cmd_reslim": [c for c in cmd if c.startswith("reslim=")],
            "cmd_optcr": [c for c in cmd if c.startswith("opt")],
            "cmd_txt_env": "OMP_NUM_THREADS=1" in cmdtxt, "cmd_optfile": any("optfile" in c.lower() for c in cmd),
            "trace_records": None if tr is None else tr["_nrecords"],
            "tr_ms": None if not tr else tr.get("ModelStatus"), "tr_ss": None if not tr else tr.get("SolverStatus"),
            "tr_obj": None if not tr else tr.get("ObjectiveValue"),
            "tr_objest": None if not tr else tr.get("ObjectiveValueEstimate"),
            "tr_time": None if not tr else tr.get("SolverTime"),
            "tr_direction": None if not tr else tr.get("Direction"),
            "tr_optfile": None if not tr else tr.get("OptionFile"),
            "lst_ms": lms, "lst_ss": lss, **{f"log_{k}" if not k.startswith("log_") else k: v for k, v in li.items()},
        })
    (HERE / "extract.json").write_text(json.dumps(out, indent=1) + "\n")
    keys = list(out[0].keys())
    for r in out:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(HERE / "extract.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in out:
            w.writerow({k: (json.dumps(v) if isinstance(v, (list, dict)) else v) for k, v in r.items()})
    print(f"{len(out)} run dirs extracted")


if __name__ == "__main__":
    main()
