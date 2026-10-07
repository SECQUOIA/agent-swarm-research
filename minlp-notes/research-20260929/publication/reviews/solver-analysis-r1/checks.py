#!/usr/bin/env python3
"""Reviewer checks on extract.json (run validity, attempts, value agreement, paper table, load).

Run after extract.py. Writes mine_pd.json (re-extracted primal/dual per run), used by compare.py.
"""
import collections
import csv
import json
from decimal import Decimal as D
from pathlib import Path

HERE = Path(__file__).resolve().parent
SR = HERE.parent.parent / "solver-runs"
R = json.load(open(HERE / "extract.json"))
C = collections.Counter


def num(s):
    if s in (None, "", "NA", "-", "--"):
        return None
    try:
        return D(s)
    except Exception:
        return None


print("== 1. settings and validity")
print("driver pid", C(r["driver_pid"] for r in R), "finished", C(r["finished"] for r in R))
print("valid", sorted(C((r["solver"], r["valid"]) for r in R).items()))
print("end kinds", C(r["end_kind"][:10] for r in R), "kill stages", C(r["kill_stage"] for r in R))
print("cmd threads=1", C(r["cmd_threads1"] for r in R), "reslim", C(tuple(r["cmd_reslim"]) for r in R),
      "opt", C(tuple(r["cmd_optcr"]) for r in R), "env", C(r["cmd_txt_env"] for r in R),
      "optfile in cmd", C(r["cmd_optfile"] for r in R), "trace OptionFile", C(r["tr_optfile"] for r in R))
print("GAMS echo Threads", C(tuple(r["log_gams_threads"]) for r in R), "ResLim", C(tuple(r["log_gams_reslim"]) for r in R))
print("solver threads", sorted(C((r["solver"], tuple(r["log_solver_threads"])) for r in R).items()))
print("solver time limit echo", sorted(C((r["solver"], r["log_solver_timelimit"]) for r in R).items(), key=str))
print("trace records", C(r["trace_records"] for r in R), "lst==trace status",
      all(str(r["lst_ms"]) == str(r["tr_ms"]) and str(r["lst_ss"]) == str(r["tr_ss"]) for r in R))
mism = []
for r in R:
    w, c = r["wall_s"], r["cpu_s"]
    ratio = c / w if w else 0
    exp = False if r["end_kind"] != "completed" else (True if (w < 60 and r["tr_ss"] != "3") else ratio >= 0.9)
    if exp != r["valid"] and not r["kept_best"]:
        mism.append(r["instance"] + "__" + r["solver"])
print("validity rule mismatches", mism)
print("long runs by solver status", sorted(C((r["solver"], r["tr_ss"]) for r in R if r["wall_s"] >= 60).items()))
for s in ("BARON", "GUROBI", "SCIP"):
    L = [r for r in R if r["solver"] == s and r["wall_s"] >= 60 and r["valid"]]
    print(f"  {s}: n={len(L)} cpu/wall {min(r['cpu_over_wall'] for r in L)}-{max(r['cpu_over_wall'] for r in L)} "
          f"cpu s {min(r['cpu_s'] for r in L)}-{max(r['cpu_s'] for r in L)}")
print("solver time > 3600.5:", sorted(((float(r["tr_time"]), r["instance"], r["solver"]) for r in R
                                       if r["tr_time"] not in (None, "NA") and float(r["tr_time"]) > 3603), reverse=True))
arch = SR / "runs_archive" / "attempts"
for name in ("ex6_2_5__SCIP", "ex6_2_7__SCIP", "pindyck__SCIP"):
    atts = sorted(arch.glob(name + "__a*"))
    ms = [json.loads((a / "run.json").read_text()) for a in atts]
    kept = json.loads((SR / "runs" / name / "run.json").read_text())
    same = (SR / "runs" / name / "trace.trc").read_bytes() == (arch / f"{name}__a{kept['attempt']}" / "trace.trc").read_bytes()
    print(f"  {name}: attempts {[(m['attempt'], m['cpu_over_wall'], m['end_kind'][:10]) for m in ms]} kept a{kept['attempt']} "
          f"trace identical to archive {same}")

print("== 2. re-extracted values vs results.csv and results_table.csv")
res = {(r["instance"], r["solver"]): r for r in csv.DictReader(open(SR / "results.csv"))}
tab = {(r["instance"], r["solver"]): r for r in csv.DictReader(open(SR / "results_table.csv"))}
mine, issues = {}, []
for r in R:
    k = (r["instance"], r["solver"])
    ms, ss = int(r["tr_ms"]), int(r["tr_ss"])
    obj, oe, ld = num(r["tr_obj"]), num(r["tr_objest"]), num(r["log_dual"])
    P = obj if ms in (1, 2, 7, 8, 15, 16, 17) and obj is not None and abs(obj) < D("1e20") else None
    Dv = src = None
    if ss in (1, 2, 3, 4, 8):
        if oe is not None:
            Dv, src = oe, "objest"
        elif ld is not None:
            Dv, src = ld, "log"
    if oe is not None and ld is not None and abs(oe) < D("1e20") and abs(oe - ld) > D("1e-9") * max(1, abs(oe)):
        issues.append(("objest != log final", k))
    if Dv is not None and abs(Dv) >= D("1e20"):
        Dv = D("-Infinity") if Dv < 0 else D("Infinity")
    mine[k] = dict(ms=ms, ss=ss, P=P, D=Dv, src=src, logP=num(r["log_primal"]), obj=obj)
    a, t = res[k], tab[k]
    aD = a["dual_bound"]
    aDv = None if aD == "" else D("-Infinity") if aD == "-inf" else D("Infinity") if aD == "inf" else D(aD)
    if num(a["primal_objective"]) != P:
        issues.append(("results.csv primal", k))
    if aDv != Dv:
        issues.append(("results.csv dual", k))
    if (str(ms), str(ss)) != (a["model_status"], a["solver_status"]):
        issues.append(("status", k))
    if num(t["primal"]) != P or (None if t["dual"] == "" else D(t["dual"])) != Dv:
        issues.append(("results_table.csv value", k))
    if r["tr_time"] not in (None, "NA") and D(r["tr_time"]) != D(t["solver_time_s"]):
        issues.append(("time", k))
print("mismatches", issues)
print("finite duals", sorted(C(k[1] for k, m in mine.items() if m["D"] is not None and m["D"].is_finite()).items()))
print("returned primals", sorted(C(k[1] for k, m in mine.items() if m["P"] is not None).items()))
print("dual source", sorted(C((k[1], m["src"]) for k, m in mine.items()).items(), key=str))
json.dump({f"{k[0]}__{k[1]}": {kk: (str(v) if v is not None else None) for kk, v in m.items()} for k, m in mine.items()},
          open(HERE / "mine_pd.json", "w"), indent=1)

print("== 3. returned point vs solver log incumbent beyond printing precision")


def hu(t):
    return D(5) * D(10) ** (D(t).as_tuple().exponent - 1)


diff = [f"{r['instance']}__{r['solver']}" for r in R
        if mine[(r["instance"], r["solver"])]["P"] is not None and r["log_primal"] not in (None, "-")
        and abs(D(r["log_primal"])) < D("1e20")
        and abs(D(r["tr_obj"]) - D(r["log_primal"])) > hu(r["tr_obj"]) + hu(r["log_primal"])]
print(len(diff), C(x.split("__")[1] for x in diff))

print("== 4. machine conditions per run (long runs)")
L = sorted((r["cpu_over_wall"], r["instance"] + "__" + r["solver"], r["start_utc"]) for r in R if r["wall_s"] >= 60)
for x in L[:11]:
    m = json.loads((SR / "runs" / x[1] / "run.json").read_text())
    print("  ", x, "load1_mean", m["load1_mean"], "min MemAvailable", m["machine_mem_available_min_gb"],
          "machine swap max", m["machine_swap_used_max_gb"], "group swap", m["peak_group_swap_mb"])
rows = [r for r in csv.DictReader(open(SR / "machine_load.csv")) if "2026-10-03T00:56" <= r["utc"] <= "2026-10-03T13:34"]
print("machine_load during final campaign: max load1", max(float(r["load1"]) for r in rows),
      "min MemAvailable", min(float(r["mem_available_gb"]) for r in rows),
      "max swap", max(float(r["swap_used_gb"]) for r in rows))
