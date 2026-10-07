#!/usr/bin/env python3
"""Reviewer's independent re-extraction of final bounds from GAMS run folders,
compared with collect.py output (CSV). Usage: check_collect.py RUNS_DIR COLLECT_CSV"""
import csv, re, sys
from decimal import Decimal
from pathlib import Path

runs, csvp = Path(sys.argv[1]), Path(sys.argv[2])
rows = {r["run_dir"].split("/")[-1]: r for r in csv.DictReader(open(csvp))}


def trace(p):
    if not p.exists():
        return {}
    hdr, recs = "", []
    lines = p.read_text().splitlines()
    for ln in lines:
        if ln.startswith("*"):
            b = ln[1:].strip()
            if b in ("Trace Record Definition", "GamsSolve", ""):
                continue
            hdr += b
        elif ln.strip():
            recs.append(ln.strip())
    if not recs:
        return {}
    return dict(zip(hdr.split(","), recs[-1].split(",")))


def lastmatch(pat, text):
    ms = re.findall(pat, text, re.M)
    return ms[-1] if ms else None


def baron_last(text, sense):
    val = None
    for ln in text.splitlines():
        t = ln.split()
        if t and t[0] == "*":
            t = t[1:]
        if len(t) == 6 and re.fullmatch(r"\d+\+?", t[0]) and re.fullmatch(r"[\d.]+", t[1]) and t[2].endswith("B") \
                and (t[5].endswith("%") or t[5] == "NA"):
            val = t[3] if sense == "min" else t[4]
    return val


def fl(s):
    if s in (None, "", "NA", "None"):
        return None
    try:
        return float(s)
    except ValueError:
        return s


bad = 0
for d in sorted(x for x in runs.iterdir() if x.is_dir() and "__" in x.name):
    inst, solver = d.name.split("__")[:2]
    tr = trace(d / "trace.trc")
    log = (d / "gams.log").read_text(errors="replace") if (d / "gams.log").exists() else ""
    sense = "max" if tr.get("Direction", "0").strip() == "1" else "min"
    if solver == "BARON":
        logd = lastmatch(r"^Best possible\s*=\s*(\S+)", log)
        lastl = baron_last(log, sense)
    elif solver == "GUROBI":
        logd = lastmatch(r"best bound (\S+?),", log)
        lastl = None
    else:
        logd = lastmatch(r"^Dual Bound\s*:\s*(\S+)", log)
        lastl = None
    ss = tr.get("SolverStatus")
    objest = tr.get("ObjectiveValueEstimate")
    exp = None
    if ss and int(ss) in (1, 2, 3, 4, 8):
        if objest and objest != "NA":
            exp = objest
        elif logd:
            exp = logd
    r = rows.get(d.name)
    if r is None:
        print(f"{d.name}: MISSING in collect csv"); bad += 1; continue
    got = r["dual_bound"]
    ok = (fl(got) == fl(exp)) or (exp is not None and abs(float(exp)) >= 1e20 and got in ("inf", "-inf"))
    agree = ""
    if objest and objest != "NA" and logd:
        agree = "objest==log" if abs(float(objest) - float(logd)) <= 1e-10 * max(1, abs(float(objest))) else f"objest!=log ({objest} vs {logd})"
    hu = ""
    if exp and abs(float(exp)) < 1e20:
        e = Decimal(exp).as_tuple().exponent
        hu = str(Decimal(5) * Decimal(10) ** (e - 1))
        if r["dual_bound_print_halfunit"] != hu:
            ok = False
    ll_ok = True
    if solver == "BARON" and lastl is not None:
        ll_ok = fl(r["dual_bound_last_logged"]) == fl(lastl) or (abs(float(lastl)) >= 1e20 and r["dual_bound_last_logged"] in ("inf", "-inf"))
    flag = "OK " if ok and ll_ok else "BAD"
    bad += flag == "BAD"
    print(f"{flag} {d.name:28s} ms/ss {tr.get('ModelStatus')}/{ss} sense {sense} objest {objest} log {logd} -> mine {exp} "
          f"collect {got} [{r['dual_bound_source']}] halfunit mine {hu} collect {r['dual_bound_print_halfunit']} {agree}"
          + (f" | BARON last logged mine {lastl} collect {r['dual_bound_last_logged']}" if solver == "BARON" else ""))
print("mismatches:", bad)
