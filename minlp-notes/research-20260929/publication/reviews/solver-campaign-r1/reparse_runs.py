#!/usr/bin/env python3
"""Reviewer's own re-parse of campaign run directories (no code shared with
collect.py). For each <inst>__<solver> directory it reads trace.trc with the
csv module, and the solver's end-of-run summary from gams.log, then compares
with the author's results.csv (if given).

Also checks that the settings took effect: GAMS parameter echo (ResLim, OptCR,
OptCA, Threads, SavePoint) and the solver's own echo of time limit, gaps and
threads (GUROBI non-default parameters and thread line, SCIP non-default
parameter settings, BARON summary optca/optcr).

usage: python3 reparse_runs.py RUNSDIR RESLIM [results.csv]
"""
import csv
import io
import re
import sys
from pathlib import Path


def trace(p):
    if not p.exists():
        return {}
    lines = p.read_text().splitlines()
    hdr = "".join(ln[1:].strip() for ln in lines if ln.startswith("*") and "," in ln)
    data = [ln for ln in lines if ln and not ln.startswith("*")]
    if not data:
        return {}
    keys = next(csv.reader(io.StringIO(hdr)))
    vals = next(csv.reader(io.StringIO(data[-1])))
    return dict(zip(keys, vals))


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def final_bound(log, solver):
    """Final dual bound and primal value printed in the solver's end summary."""
    if solver == "BARON":
        db = re.findall(r"^Best possible\s*=\s*([-+0-9.eE]+)", log, re.M)
        pv = re.findall(r"^Solution\s*=\s*([-+0-9.eE]+)", log, re.M)
    elif solver == "GUROBI":
        ls = re.findall(r"Best objective ([^,]+), best bound ([^,]+), gap", log)
        db = [b for _, b in ls]
        pv = [a for a, _ in ls]
    else:
        db = re.findall(r"^Dual Bound\s*:\s*([-+0-9.eE]+)", log, re.M)
        pv = re.findall(r"^Primal Bound\s*:\s*([-+0-9.eE]+)", log, re.M)
    return (fnum(db[-1]) if db else None, len(db), fnum(pv[-1]) if pv else None)


def settings(log, solver, reslim):
    probs = []
    gp = log.split("Licensee:")[0]
    for k, v in (("ResLim", str(reslim)), ("OptCR", "1E-9"), ("OptCA", "1E-9"), ("Threads", "1"),
                 ("SavePoint", "1")):
        if not re.search(rf"^\s+{k} {re.escape(v)}\s*$", gp, re.M):
            probs.append(f"GAMS {k} != {v}")
    if solver == "GUROBI" and "Gurobi Optimizer" in log:
        for k, v in (("TimeLimit", str(reslim)), ("MIPGap", "1e-09"), ("MIPGapAbs", "1e-09"), ("Threads", "1")):
            if not re.search(rf"^\s+{k}\s+{re.escape(v)}\s*$", log, re.M):
                probs.append(f"GUROBI {k} != {v}")
        if "using up to 1 threads" not in log:
            probs.append("GUROBI thread line missing")
    if solver == "SCIP" and "SCIP version" in log:
        for k, v in (("limits/time", str(reslim)), ("limits/gap", "1e-09"), ("limits/absgap", "1e-09"),
                     ("lp/threads", "1")):
            if not re.search(rf"^{re.escape(k)} = {re.escape(v)}\s*$", log, re.M):
                probs.append(f"SCIP {k} != {v}")
        extra = re.search(r"non-default parameter settings:\n(.*?)\n\n", log, re.S)
        if extra:
            allowed = {"limits/time", "limits/gap", "limits/absgap", "lp/threads", "misc/printreason",
                       "constraints/nonlinear/linearizeheursol", "nlpi/ipopt/linear_solver",
                       "nlpi/ipopt/linear_system_scaling"}
            other = [ln.split(" = ")[0] for ln in extra.group(1).splitlines() if " = " in ln
                     and ln.split(" = ")[0] not in allowed]
            if other:
                probs.append(f"SCIP other non-default params {other}")
    if solver == "BARON" and "Best possible" in log:
        if not re.search(r"optca = 1E-9", log) or not re.search(r"optcr = 1E-9", log):
            probs.append("BARON summary optca/optcr not 1E-9")
    return probs


def main():
    runs, reslim = Path(sys.argv[1]), int(sys.argv[2])
    auth = {}
    if len(sys.argv) > 3:
        for r in csv.DictReader(open(sys.argv[3])):
            auth[(r["instance"], r["solver"])] = r
    nbad = 0
    for d in sorted(p for p in runs.iterdir() if p.is_dir() and "__" in p.name):
        inst, solver = d.name.split("__")
        log = (d / "gams.log").read_text(errors="replace") if (d / "gams.log").exists() else ""
        tr = trace(d / "trace.trc")
        ms, ss = tr.get("ModelStatus"), tr.get("SolverStatus")
        objest = fnum(tr.get("ObjectiveValueEstimate"))
        obj = fnum(tr.get("ObjectiveValue"))
        lb, nlb, lp = final_bound(log, solver)
        # my rule: a final bound exists only after normal / limit / user interrupt termination
        mine = None
        if ss in ("1", "2", "3", "4", "8"):
            mine = objest if objest is not None else lb
        probs = settings(log, solver, reslim)
        a = auth.get((inst, solver))
        cmp_ = ""
        if a is not None:
            ad = a["dual_bound"]
            adv = {"inf": 1e300, "-inf": -1e300}.get(ad, fnum(ad))
            minev = mine if mine is None or abs(mine) < 1e20 else (1e300 if mine > 0 else -1e300)
            same = (adv is None and minev is None) or (adv is not None and minev is not None and adv == minev)
            ap = fnum(a["primal_objective"])
            mp = obj if ms in ("1", "2", "7", "8", "15", "16", "17") else None
            samep = (ap is None and mp is None) or (ap is not None and mp is not None and ap == mp)
            cmp_ = f"dual {'=' if same else '!='} author ({ad}); primal {'=' if samep else '!='} author"
            if not (same and samep):
                nbad += 1
        print(f"{d.name:26s} ms {ms} ss {ss} obj {obj} objest {objest} logbound {lb} (#{nlb}) "
              f"mine {mine} | {cmp_} | settings {'OK' if not probs else probs}")
    print("rows differing from author:", nbad)


if __name__ == "__main__":
    main()
