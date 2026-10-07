"""R8: independent recomputation of the campaign-4 path-family numbers (Parts C2, C3, 2x2 design).

Standard library only. Reads records.jsonl, jobs.json and cases/*.json directly; does not import any
producer code (summarize_v4, summarize_v3, campaign4_digest). Definitions implemented from
experiments/campaign-v4-protocol.md and experiments/v4/README.md:

- solved: status optimal or gaplimit, normal worker exit (returncode 0, no worker_status, status not a
  failure status), primal_check.checked and primal_check.passed true, finite primal;
- time: total_seconds + preparation_seconds; SCIP time: scip_solve_seconds (Gurobi:
  solver_runtime_seconds); callback: separation.callback_seconds; SCIP excl. callback: difference;
- SGM: exp(mean(log(t + 1))) - 1 over the runs that every compared mode solved (full) or completed
  with a root bound (root);
- bound comparison (minimization): better if a > b + tol, worse if a < b - tol, tie otherwise,
  tol = rtol * max(1, |a|, |b|);
- root bound: root_dual if finite, else the final dual bound for a run that ended at the root
  (node limit 1 or at most one node);
- gap closed: (root(m) - root(ref)) / (opt - root(ref)); residual closure: root(m) / opt
  (pair-hull bound 0); opt = known_optimum of the case file (checked against known_optimum_exact).

Usage: python R8_path.py [--json OUT]   (prints every recomputed number and the digest comparison)
"""
from __future__ import annotations

import json
import math
import statistics
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "experiments"
DIRS = {
    "C2": EXP / "v4/runs/partC2",
    "C3": EXP / "v4/runs/partC3",
    "V3": EXP / "v3/runs/partC",
    "V3D": EXP / "v3d/runs/partC-rowdir",
}
FAIL_STATUS = {"process_timeout", "worker_error", "worker_no_output", "worker_output_parse_error"}
NS = (10, 20, 40, 80)


# ----------------------------------------------------------------------------- loading

def load(key):
    d = DIRS[key]
    recs = [json.loads(line) for line in open(d / "records.jsonl")]
    jobs = json.load(open(d / "jobs.json"))["jobs"]
    cases = {}
    for f in sorted((d / "cases").glob("*.json")):
        c = json.load(open(f))
        cases[c["name"]] = c
    scheduled = {(r["run_id"]) for j in jobs for r in j["runs"]}
    recorded = [r["run_id"] for r in recs]
    idx = {}
    for r in recs:
        k = (r["phase"], r["mode"], r["name"])
        assert k not in idx, ("duplicate", key, k)
        idx[k] = r
    return {"recs": recs, "jobs": jobs, "cases": cases, "idx": idx,
            "scheduled": len(scheduled), "recorded": len(recorded),
            "missing": sorted(scheduled - set(recorded)), "extra": sorted(set(recorded) - scheduled)}


def short(name):
    return name.replace("interleaved_path_", "")


def n_of(name):
    return int(name.split("_n")[1].split("_")[0])


def finite(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def failed(r):
    return (r.get("status") in FAIL_STATUS or bool(r.get("worker_status"))
            or r.get("returncode", 0) != 0)


def solved(r):
    pc = r.get("primal_check") or {}
    return (not failed(r) and r["status"] in ("optimal", "gaplimit") and pc.get("checked") is True
            and pc.get("passed") is True and finite(r.get("primal")))


def tsec(r):
    return r["total_seconds"] + r.get("preparation_seconds", 0.0)


def scip_sec(r):
    if r["mode"] == "gurobi":
        return r["solver_runtime_seconds"]
    return r["scip_solve_seconds"]


def cb_sec(r):
    sep = r.get("separation") or {}
    return sep.get("callback_seconds", 0.0) or 0.0


def root_bound(r):
    if finite(r.get("root_dual")):
        return r["root_dual"]
    ended_at_root = r.get("node_limit") == 1 or (finite(r.get("nodes")) and r["nodes"] <= 1)
    if ended_at_root and finite(r.get("dual")):
        return r["dual"]
    return None


def sgm(vals, shift=1.0):
    return math.exp(sum(math.log(v + shift) for v in vals) / len(vals)) - shift


def cmp(a, b, rtol):
    tol = rtol * max(1.0, abs(a), abs(b))
    if a > b + tol:
        return "better"
    if a < b - tol:
        return "worse"
    return "tie"


def mmm(vals):
    return (statistics.median(vals), min(vals), max(vals))


def names_by_n(cases):
    out = {n: sorted([nm for nm in cases if n_of(nm) == n], key=lambda s: int(s.split("_s")[-1]))
           for n in NS}
    return out


# ----------------------------------------------------------------------------- data

D = {k: load(k) for k in DIRS}
OPT = {}
for key in ("C2", "C3"):
    for nm, c in D[key]["cases"].items():
        assert Fraction(c["known_optimum_exact"]) == Fraction(c["known_optimum"]) or \
            abs(float(Fraction(c["known_optimum_exact"])) - c["known_optimum"]) < 1e-15
        OPT[(key, nm)] = c["known_optimum"]

R = {}  # all recomputed values, keyed by item string


def put(key, value):
    R[key] = value
    return value


# case identity C2 vs v3 vs v3d
case_mismatch = []
for nm, c in D["C2"]["cases"].items():
    for other in ("V3", "V3D"):
        oc = D[other]["cases"].get(nm)
        if oc is None or oc["known_optimum_exact"] != c["known_optimum_exact"] or oc["model"] != c["model"]:
            case_mismatch.append((other, nm))
put("case_mismatch_C2_v3_v3d", case_mismatch)
put("C3_names_disjoint_from_C2", not (set(D["C3"]["cases"]) & set(D["C2"]["cases"])))

# run status
for key in ("C2", "C3", "V3", "V3D"):
    d = D[key]
    st = {}
    for r in d["recs"]:
        st[r["status"]] = st.get(r["status"], 0) + 1
    put(f"{key} scheduled/recorded", (d["scheduled"], d["recorded"], d["missing"], d["extra"]))
    put(f"{key} statuses", dict(sorted(st.items())))
    put(f"{key} failures", sum(failed(r) for r in d["recs"]))
    put(f"{key} cut_log_incomplete", sum(1 for r in d["recs"] if r.get("cut_log_complete") is not True))


def rec(src, phase, mode, nm):
    return D[src]["idx"].get((phase, mode, nm))


# mode -> (source dir, mode name in that dir)
C2_MODES = {
    "c3:baseline": ("V3", "baseline"),
    "c3:all-diag-mech": ("V3", "all-diag-mech"),
    "baseline-novarlocks": ("C2", "baseline-novarlocks"),
    "baseline-extra": ("C2", "baseline-extra"),
    "frozen-wide": ("C2", "frozen-wide"),
    "gurobi": ("C2", "gurobi"),
    "v3d:baseline": ("V3D", "baseline"),
    "v3d:all-diag-mech": ("V3D", "all-diag-mech"),
    "v3d:all-diag-mech-wide": ("V3D", "all-diag-mech-wide"),
}
C3_MODES = {m: ("C3", m) for m in ("baseline", "baseline-extra", "all-diag-mech", "rowdir-wide", "gurobi")}

FAMILY = {"C2": (C2_MODES, "c3:baseline", D["C2"]["cases"]), "C3": (C3_MODES, "baseline", D["C3"]["cases"])}


def get(fam, phase, mode, nm):
    src, m = FAMILY[fam][0][mode]
    return rec(src, phase, m, nm)


# ----------------------------------------------------------------------------- root analysis

def root_analysis(fam, modes):
    _, ref, cases = FAMILY[fam]
    byn = names_by_n(cases)
    allnames = [nm for n in NS for nm in byn[n]]
    for m in modes:
        rb = {}
        statuses = {}
        for nm in allnames:
            r = get(fam, "root", m, nm)
            statuses[r["status"]] = statuses.get(r["status"], 0) + 1
            rb[nm] = root_bound(r)
        put(f"{fam} root {m} statuses", statuses)
        put(f"{fam} root {m} rootbounds", rb)
    refrb = R[f"{fam} root {ref} rootbounds"]
    for m in modes + ["pair-hull"]:
        gc, res, rbv = {}, {}, {}
        for nm in allnames:
            opt = OPT[(fam, nm)]
            b = 0.0 if m == "pair-hull" else R[f"{fam} root {m} rootbounds"][nm]
            rbv[nm] = b
            gc[nm] = (b - refrb[nm]) / (opt - refrb[nm])
            res[nm] = b / opt
        for n in NS:
            put(f"{fam} root gapclosed {m} n{n}", mmm([gc[nm] for nm in byn[n]]))
            put(f"{fam} root residual {m} n{n}", mmm([res[nm] for nm in byn[n]]))
            put(f"{fam} root bound {m} n{n}", mmm([rbv[nm] for nm in byn[n]]))
        put(f"{fam} root gapclosed {m} all", mmm(list(gc.values())))
        put(f"{fam} root gapclosed {m} per-instance", gc)
        if m != "pair-hull" and m != ref:
            for rtol in (1e-4, 1e-6):
                cnt = {"better": 0, "tie": 0, "worse": 0}
                for nm in allnames:
                    cnt[cmp(rbv[nm], refrb[nm], rtol)] += 1
                put(f"{fam} root vs {ref} {m} rtol{rtol:g}", cnt)
    return allnames


C2_NAMES = root_analysis("C2", ["c3:baseline", "c3:all-diag-mech", "baseline-novarlocks", "baseline-extra",
                               "frozen-wide", "v3d:baseline", "v3d:all-diag-mech", "v3d:all-diag-mech-wide"])
C3_NAMES = root_analysis("C3", ["baseline", "baseline-extra", "all-diag-mech", "rowdir-wide"])

# v3d baseline root equals c3 baseline root?
put("v3d baseline root == c3 baseline root (count exact equal)",
    sum(R["C2 root v3d:baseline rootbounds"][nm] == R["C2 root c3:baseline rootbounds"][nm] for nm in C2_NAMES))
put("v3d baseline root vs c3 baseline root rtol1e-6",
    R.get("C2 root vs c3:baseline v3d:baseline rtol1e-06"))

# novarlocks root range, frozen-wide above 0
nv = R["C2 root baseline-novarlocks rootbounds"]
put("C2 root novarlocks min/max", (min(nv.values()), max(nv.values()), sum(v > 0 for v in nv.values())))
fw = R["C2 root frozen-wide rootbounds"]
put("C2 root frozen-wide above 0", sorted(short(nm) for nm, v in fw.items() if v > 0))

# frozen-wide cut cap
def cap_hits(fam, phase, mode):
    out = {"cut": 0, "support": 0, "rounds": 0, "runs": 0, "budget_exhausted": 0, "discovery_incomplete": 0}
    names = C2_NAMES if fam == "C2" else C3_NAMES
    for nm in names:
        r = get(fam, phase, mode, nm)
        sep, cfg = r["separation"], r["config"]
        out["runs"] += 1
        out["cut"] += sep["cuts"] >= cfg["max_cuts"]
        out["support"] += sep["certification_calls"] >= cfg["max_support_calls"]
        out["rounds"] += sep["calls"] >= cfg["max_rounds"]
        out["budget_exhausted"] += bool(sep.get("budget_exhausted"))
        out["discovery_incomplete"] += bool(sep.get("discovery_incomplete"))
        out.setdefault("max_cuts_per_n", set()).add(cfg["max_cuts"] / n_of(nm))
    return out


for fam, modes in (("C2", ["frozen-wide", "c3:all-diag-mech", "v3d:all-diag-mech", "v3d:all-diag-mech-wide"]),
                   ("C3", ["all-diag-mech", "rowdir-wide"])):
    for m in modes:
        for ph in ("root", "full"):
            put(f"{fam} caps {ph} {m}", cap_hits(fam, ph, m))

# C3 rowdir-wide root-opt range, solved at root
rw = R["C3 root rowdir-wide rootbounds"]
put("C3 root rowdir-wide root-opt min/max",
    (min(rw[nm] - OPT[("C3", nm)] for nm in C3_NAMES), max(rw[nm] - OPT[("C3", nm)] for nm in C3_NAMES)))
put("C3 root rowdir-wide optimal at root",
    sorted(short(nm) for nm in C3_NAMES if get("C3", "root", "rowdir-wide", nm)["status"] == "optimal"))
put("C3 root rowdir-wide no root_dual",
    sorted(short(nm) for nm in C3_NAMES if not finite(get("C3", "root", "rowdir-wide", nm).get("root_dual"))))
put("C2 root v3d wide optimal at root",
    sorted(short(nm) for nm in C2_NAMES if get("C2", "root", "v3d:all-diag-mech-wide", nm)["status"] == "optimal"))


# ----------------------------------------------------------------------------- full analysis

def full_analysis(fam, modes, ref, tag=None):
    _, _, cases = FAMILY[fam]
    tag = tag or fam
    names = C2_NAMES if fam == "C2" else C3_NAMES
    sol = {}
    for m in modes:
        rs = {nm: get(fam, "full", m, nm) for nm in names}
        sol[m] = {nm for nm, r in rs.items() if solved(r)}
        put(f"{fam} full {m} solved", len(sol[m]))
        put(f"{fam} full {m} solved list", sorted(short(nm) for nm in sol[m]))
        st = {}
        for r in rs.values():
            key = r["status"]
            st[key] = st.get(key, 0) + 1
        put(f"{fam} full {m} statuses", st)
        put(f"{fam} full {m} median nodes all", statistics.median(r["nodes"] for r in rs.values()))
        put(f"{fam} full {m} max nodes", max(r["nodes"] for r in rs.values()))
        put(f"{fam} full {m} load_start_mean", statistics.fmean(r["load_start"][0] for r in rs.values()))
        put(f"{fam} full {m} unsolved optimal/gaplimit (check failed)",
            sorted(short(nm) for nm, r in rs.items() if r["status"] in ("optimal", "gaplimit") and not solved(r)))
    common = set(names)
    for m in modes:
        common &= sol[m]
    put(f"{tag} full common solved", sorted(short(nm) for nm in common))
    for m in modes:
        rs = [get(fam, "full", m, nm) for nm in common]
        put(f"{fam} full common {m} sgm", sgm([tsec(r) for r in rs]))
        put(f"{fam} full common {m} sgm scip", sgm([scip_sec(r) for r in rs]))
        put(f"{fam} full common {m} sgm scip-excl-cb", sgm([scip_sec(r) - cb_sec(r) for r in rs]))
        put(f"{fam} full common {m} median nodes", statistics.median(r["nodes"] for r in rs))
        if m == ref:
            continue
        pairs = sorted(sol[m] & sol[ref])
        ratios = [tsec(get(fam, "full", m, nm)) / tsec(get(fam, "full", ref, nm)) for nm in pairs]
        put(f"{fam} full ratio {m}", (statistics.median(ratios), len(pairs), sum(x < 1 for x in ratios)))
        put(f"{fam} full pairs {m} sgm mode", sgm([tsec(get(fam, "full", m, nm)) for nm in pairs]))
        put(f"{fam} full pairs {m} sgm ref", sgm([tsec(get(fam, "full", ref, nm)) for nm in pairs]))
        for rtol in (1e-4, 1e-6):
            cnt = {"better": [], "tie": [], "worse": []}
            for nm in names:
                a, b = get(fam, "full", m, nm)["dual"], get(fam, "full", ref, nm)["dual"]
                cnt[cmp(a, b, rtol)].append(short(nm))
            put(f"{fam} full bound vs {ref} {m} rtol{rtol:g}", {k: len(v) for k, v in cnt.items()})
            put(f"{fam} full bound vs {ref} {m} rtol{rtol:g} worse list", cnt["worse"])
    return sol


C2_FULL_MODES = ["c3:baseline", "c3:all-diag-mech", "baseline-novarlocks", "baseline-extra", "frozen-wide", "gurobi"]
SOL2 = full_analysis("C2", C2_FULL_MODES, "c3:baseline")
SOL2D = full_analysis("C2", ["v3d:baseline", "v3d:all-diag-mech", "v3d:all-diag-mech-wide"], "v3d:baseline",
                      tag="C2-v3d")
C3_FULL_MODES = ["baseline", "all-diag-mech", "rowdir-wide", "baseline-extra", "gurobi"]
SOL3 = full_analysis("C3", C3_FULL_MODES, "baseline")

# v3d load means
for ph in ("root", "full"):
    rs = [r for r in D["V3D"]["recs"] if r["phase"] == ph]
    put(f"V3D {ph} load_start_mean", statistics.fmean(r["load_start"][0] for r in rs))
for ph in ("root", "full"):
    rs = [r for r in D["V3"]["recs"] if r["phase"] == ph]
    put(f"V3 {ph} load_start_mean", statistics.fmean(r["load_start"][0] for r in rs))
for fam in ("C2", "C3"):
    for ph in ("root", "full"):
        rs = [r for r in D[fam]["recs"] if r["phase"] == ph]
        modes = sorted({r["mode"] for r in rs})
        put(f"{fam} {ph} load_start_mean per mode",
            {m: round(statistics.fmean(r["load_start"][0] for r in rs if r["mode"] == m), 3) for m in modes})

# rowdir-wide over all 20 C3 full runs
rs = [get("C3", "full", "rowdir-wide", nm) for nm in C3_NAMES]
put("C3 full rowdir-wide all20 sgm", sgm([tsec(r) for r in rs]))
put("C3 full rowdir-wide all20 min/max time", (min(map(tsec, rs)), max(map(tsec, rs))))
put("C3 full rowdir-wide n80 times", sorted(tsec(r) for r in rs if n_of(r["name"]) == 80))
put("C3 full rowdir-wide sum callback / sum total", (sum(map(cb_sec, rs)), sum(map(tsec, rs))))
rs = [get("C2", "full", "v3d:all-diag-mech-wide", nm) for nm in C2_NAMES]
put("C2 full v3d wide max time / max nodes", (max(map(tsec, rs)), max(r["nodes"] for r in rs)))


# ----------------------------------------------------------------------------- gurobi

def gurobi_table(fam):
    names = C2_NAMES if fam == "C2" else C3_NAMES
    out = {}
    for nm in names:
        r = get(fam, "full", "gurobi", nm)
        opt = OPT[(fam, nm)]
        out[short(nm)] = {
            "status": r["status"], "gstatus": r["gurobi_status_name"], "dual-opt": r["dual"] - opt,
            "rel dual excess": (r["dual"] - opt) / abs(opt), "dual": r["dual"],
            "primal-opt": r["primal"] - opt, "mip_gap": r["mip_gap"], "time": tsec(r),
            "runtime": r["solver_runtime_seconds"], "nodes": r["nodes"],
            "viol": r["primal_check"]["max_scaled_violation"], "passed": r["primal_check"]["passed"],
            "ref_dual_consistent": r["reference_check"]["dual_consistent"]}
    put(f"{fam} gurobi table", out)
    return out


G2 = gurobi_table("C2")
G3 = gurobi_table("C3")

# novarlocks final values below optimum
nvs = {}
for nm in C2_NAMES:
    r = get("C2", "full", "baseline-novarlocks", nm)
    if solved(r):
        opt = OPT[("C2", nm)]
        nvs[short(nm)] = (r["status"], r["primal"] - opt, r["dual"] - opt, (r["primal"] - opt) / opt,
                          r["primal"] == r["dual"])
put("C2 full novarlocks solved: status, primal-opt, dual-opt, rel, primal==dual", nvs)

# novarlocks final bound at n40/n80
for m in ("baseline-novarlocks", "frozen-wide", "c3:baseline", "gurobi", "baseline-extra"):
    for n in (40, 80):
        put(f"C2 full final dual {m} n{n} min/max",
            (min(get("C2", "full", m, nm)["dual"] for nm in C2_NAMES if n_of(nm) == n),
             max(get("C2", "full", m, nm)["dual"] for nm in C2_NAMES if n_of(nm) == n)))


# ----------------------------------------------------------------------------- time decomposition

def time_decomp(fam, phase, mode, ref):
    names = C2_NAMES if fam == "C2" else C3_NAMES
    if phase == "root":
        ok = lambda r: not failed(r) and root_bound(r) is not None
    else:
        ok = solved
    pairs = [nm for nm in names if ok(get(fam, phase, mode, nm)) and ok(get(fam, phase, ref, nm))]
    m = [get(fam, phase, mode, nm) for nm in pairs]
    f = [get(fam, phase, ref, nm) for nm in pairs]
    return {"pairs": len(pairs), "sgm total": sgm([tsec(r) for r in m]),
            "sgm scip-excl": sgm([scip_sec(r) - cb_sec(r) for r in m]),
            "sgm cb": sgm([cb_sec(r) for r in m]),
            "ref sgm total": sgm([tsec(r) for r in f]), "ref sgm scip": sgm([scip_sec(r) for r in f]),
            "median scip-excl/ref scip": statistics.median((scip_sec(a) - cb_sec(a)) / scip_sec(b) for a, b in zip(m, f)),
            "median total/ref total": statistics.median(tsec(a) / tsec(b) for a, b in zip(m, f)),
            "faster": sum(tsec(a) < tsec(b) for a, b in zip(m, f))}


for fam, phase, mode, ref in (("C2", "root", "c3:all-diag-mech", "c3:baseline"),
                              ("C2", "root", "frozen-wide", "c3:baseline"),
                              ("C2", "root", "baseline-novarlocks", "c3:baseline"),
                              ("C2", "root", "baseline-extra", "c3:baseline"),
                              ("C2", "full", "c3:all-diag-mech", "c3:baseline"),
                              ("C2", "full", "frozen-wide", "c3:baseline"),
                              ("C2", "full", "baseline-novarlocks", "c3:baseline"),
                              ("C2", "full", "baseline-extra", "c3:baseline"),
                              ("C3", "root", "all-diag-mech", "baseline"),
                              ("C3", "root", "rowdir-wide", "baseline"),
                              ("C3", "root", "baseline-extra", "baseline"),
                              ("C3", "full", "all-diag-mech", "baseline"),
                              ("C3", "full", "rowdir-wide", "baseline"),
                              ("C3", "full", "baseline-extra", "baseline")):
    put(f"{fam} timedecomp {phase} {mode}", time_decomp(fam, phase, mode, ref))

# root SGM over all 20 per mode
for fam, modes in (("C2", ["c3:baseline", "baseline-novarlocks", "baseline-extra", "frozen-wide", "c3:all-diag-mech"]),
                   ("C3", ["baseline", "baseline-extra", "all-diag-mech", "rowdir-wide"])):
    names = C2_NAMES if fam == "C2" else C3_NAMES
    for m in modes:
        put(f"{fam} root sgm all20 {m}", sgm([tsec(get(fam, "root", m, nm)) for nm in names]))


# ----------------------------------------------------------------------------- funnel

def funnel(fam, phase, mode):
    names = C2_NAMES if fam == "C2" else C3_NAMES
    tot = {"calls": 0, "certification_calls": 0, "certification_failures": 0, "row_rounding_rejections": 0,
           "row_binding_rejections": 0, "cuts": 0}
    runs_bind = 0
    causes = {}
    for nm in names:
        r = get(fam, phase, mode, nm)
        sep = r["separation"]
        for k in tot:
            tot[k] += sep[k]
        runs_bind += sep["row_binding_rejections"] > 0
        rc = (r.get("row_binding_rejection_causes") or {}).get("causes") or {}
        for k, v in rc.items():
            causes[k] = causes.get(k, 0) + v
    tot["below"] = (tot["certification_calls"] - tot["certification_failures"] - tot["row_rounding_rejections"]
                    - tot["row_binding_rejections"] - tot["cuts"])
    tot["runs_binding"] = runs_bind
    tot["causes"] = causes
    return tot


for fam, modes in (("C2", ["frozen-wide", "c3:all-diag-mech"]), ("C3", ["all-diag-mech", "rowdir-wide"])):
    for m in modes:
        fr, ff = funnel(fam, "root", m), funnel(fam, "full", m)
        put(f"{fam} funnel root {m}", fr)
        put(f"{fam} funnel full {m}", ff)
        put(f"{fam} funnel root==full {m}", fr == ff)
        # per-run equality
        names = C2_NAMES if fam == "C2" else C3_NAMES
        diff = []
        for nm in names:
            a, b = get(fam, "root", m, nm)["separation"], get(fam, "full", m, nm)["separation"]
            keys = ("calls", "certification_calls", "certification_failures", "row_binding_rejections", "cuts")
            if any(a[k] != b[k] for k in keys):
                diff.append(short(nm))
        put(f"{fam} funnel per-run root!=full {m}", diff)


# ----------------------------------------------------------------------------- native separators

def native(fam, phase, mode, table, name, fields):
    names = C2_NAMES if fam == "C2" else C3_NAMES
    tot = {f: 0 for f in fields}
    runs = 0
    for nm in names:
        r = get(fam, phase, mode, nm)
        row = ((r.get("native_statistics") or {}).get(table) or {}).get(name) or {}
        vals = {f: (row.get(f) if isinstance(row.get(f), (int, float)) else 0) for f in fields}
        for f in fields:
            tot[f] += vals[f]
        runs += vals[fields[-1]] > 0
    tot["productive_runs"] = runs
    return tot


put("C2 root novarlocks minor", native("C2", "root", "baseline-novarlocks", "separators", "minor",
                                       ["Calls", "FoundCuts", "Applied"]))
for fam, mode in (("C2", "baseline-extra"), ("C3", "baseline-extra")):
    put(f"{fam} root {mode} intersection (nlhdlr quadratic)",
        native(fam, "root", mode, "nlhdlrs", "quadratic", ["#Enforce", "Cuts"]))
    for sep in ("interminor", "eccuts", "rlt", "minor"):
        put(f"{fam} root {mode} {sep}", native(fam, "root", mode, "separators", sep, ["Calls", "FoundCuts", "Applied"]))
for fam, modes in (("C2", ["baseline-extra", "frozen-wide"]), ("C3", ["baseline", "baseline-extra", "all-diag-mech", "rowdir-wide"])):
    for m in modes:
        put(f"{fam} root {m} minor", native(fam, "root", m, "separators", "minor", ["Calls", "FoundCuts", "Applied"]))

# soft overshoots
for fam in ("C2", "C3"):
    tl = [tsec(r) for r in D[fam]["recs"] if r["status"] == "timelimit"]
    put(f"{fam} timelimit runs count/min/max time", (len(tl), min(tl), max(tl)))
    put(f"{fam} root timelimit runs", sum(1 for r in D[fam]["recs"] if r["phase"] == "root" and r["status"] == "timelimit"))
    put(f"{fam} primal check failures", sum(1 for r in D[fam]["recs"] if (r.get("primal_check") or {}).get("passed") is False))
    put(f"{fam} no incumbent", sum(1 for r in D[fam]["recs"] if not finite(r.get("primal"))))
    put(f"{fam} cert failures total", sum((r.get("separation") or {}).get("certification_failures", 0) for r in D[fam]["recs"]))
    put(f"{fam} rounding rejections total", sum((r.get("separation") or {}).get("row_rounding_rejections", 0) for r in D[fam]["recs"]))
    put(f"{fam} classifier_errors total", sum(((r.get("row_binding_rejection_causes") or {}).get("classifier_errors") or 0) for r in D[fam]["recs"]))

# replay files
for key in ("C2", "C3"):
    p = DIRS[key] / "replay.json"
    if p.exists():
        rp = json.load(open(p))
        put(f"{key} replay top-level", {k: (v if not isinstance(v, (dict, list)) else type(v).__name__)
                                         for k, v in rp.items()})



# ----------------------------------------------------------------------------- extra facts for the report

def per_instance_v3_v3d_baseline_ratio():
    out = []
    for nm in C2_NAMES:
        a, b = get("C2", "full", "v3d:baseline", nm), get("C2", "full", "c3:baseline", nm)
        if solved(a) and solved(b):
            out.append(tsec(a) / tsec(b))
    return (len(out), min(out), statistics.median(out), max(out))


put("C2 full v3d:baseline/c3:baseline time ratio (pairs, min, median, max)", per_instance_v3_v3d_baseline_ratio())
put("C2 full frozen-wide times of solves c3:all-diag-mech lacked",
    {short(nm): round(tsec(get("C2", "full", "frozen-wide", nm)), 1)
     for nm in C2_NAMES if solved(get("C2", "full", "frozen-wide", nm)) and not solved(get("C2", "full", "c3:all-diag-mech", nm))})
put("C2 root v3d wide root-opt min/max",
    (min(R["C2 root v3d:all-diag-mech-wide rootbounds"][nm] - OPT[("C2", nm)] for nm in C2_NAMES),
     max(R["C2 root v3d:all-diag-mech-wide rootbounds"][nm] - OPT[("C2", nm)] for nm in C2_NAMES)))
put("C2 root v3d wide no root_dual",
    sorted(short(nm) for nm in C2_NAMES if not finite(get("C2", "root", "v3d:all-diag-mech-wide", nm).get("root_dual"))))
put("reference_check.value == known_optimum (all C2/C3/v3/v3d records)",
    all(r["reference_check"]["value"] == OPT[("C2" if key != "C3" else "C3", r["name"])]
        for key in ("C2", "C3", "V3", "V3D") for r in D[key]["recs"]))
put("reference conflicts (dual/root_dual inconsistent), all four dirs",
    sum(1 for key in ("C2", "C3", "V3", "V3D") for r in D[key]["recs"]
        if r["reference_check"].get("dual_consistent") is False or r["reference_check"].get("root_dual_consistent") is False))
for key in ("C2", "C3"):
    g = [r for r in D[key]["recs"] if r["mode"] == "gurobi"]
    put(f"{key} gurobi params set", sorted({json.dumps({k: v for k, v in r["gurobi_params"].items()
                                                        if k in ("Threads", "NonConvex", "MIPGap")}, sort_keys=True) for r in g}))


# ----------------------------------------------------------------------------- digest comparison

CHECKS = []   # (item, digest string, recomputed string, ok)


def tol_of(s):
    s = s.replace(",", "").replace("+", "")
    if "e" in s.lower():
        mant, ex = s.lower().split("e")
        dec = len(mant.split(".")[1]) if "." in mant else 0
        return 0.5 * 10 ** (int(ex) - dec)
    dec = len(s.split(".")[1]) if "." in s else 0
    return 0.5 * 10 ** (-dec)


def num(item, digest, value, tol=None):
    d = float(digest.replace(",", "").replace("+", ""))
    t = tol if tol is not None else tol_of(digest)
    ok = abs(value - d) <= t * 1.0001 + 1e-15
    CHECKS.append((item, digest, f"{value:.6g}", ok))
    return ok


def exact(item, digest, value):
    ok = digest == value
    CHECKS.append((item, str(digest), str(value), ok))
    return ok


def triple(item, digest, vals, tol=None):
    """digest like '0.948 [0.813, 0.957]'"""
    parts = digest.replace("[", " ").replace("]", " ").replace(",", " ").split()
    names = ("median", "min", "max")
    for nm, dstr, v in zip(names, parts, vals):
        num(f"{item} {nm}", dstr, v, tol)


ONE = 5e-4   # digest prints the closure '1' for values that round to 1.000


def run_checks():
    # ---- run status (C2, C3)
    exact("C2 scheduled/recorded/missing", (140, 140, []), R["C2 scheduled/recorded"][:3])
    exact("C3 scheduled/recorded/missing", (180, 180, []), R["C3 scheduled/recorded"][:3])
    exact("C2 statuses", {"gaplimit": 5, "nodelimit": 60, "optimal": 35, "timelimit": 40}, R["C2 statuses"])
    exact("C3 statuses", {"gaplimit": 3, "nodelimit": 72, "optimal": 58, "timelimit": 47}, R["C3 statuses"])
    exact("C2 failures", 0, R["C2 failures"])
    exact("C3 failures", 0, R["C3 failures"])
    exact("C2/C3 missing cut logs", 0, R["C2 cut_log_incomplete"] + R["C3 cut_log_incomplete"])
    exact("C2 case mismatches vs v3 and v3d", [], R["case_mismatch_C2_v3_v3d"])

    # ---- C2 root: statuses and paired bounds
    for m in ("baseline-novarlocks", "baseline-extra", "frozen-wide", "c3:all-diag-mech"):
        exact(f"C2 root {m} statuses", {"nodelimit": 20}, R[f"C2 root {m} statuses"])
        for rt in ("0.0001", "1e-06"):
            exact(f"C2 root {m} vs c3:baseline rtol {rt}", {"better": 20, "tie": 0, "worse": 0},
                  R[f"C2 root vs c3:baseline {m} rtol{float(rt):g}"])
    exact("v3d baseline root == c3 baseline root (instances)", 20, R["v3d baseline root == c3 baseline root (count exact equal)"])

    # ---- C2 root gap closed
    gc = {
        "baseline-novarlocks": ["0.948 [0.813, 0.957]", "0.886 [0.861, 0.925]", "0.931 [0.901, 0.938]", "0.911 [0.884, 0.926]", "0.910 [0.813, 0.957]"],
        "baseline-extra": ["0.640 [0.495, 0.733]", "0.580 [0.499, 0.633]", "0.659 [0.590, 0.693]", "0.591 [0.514, 0.639]", "0.610 [0.495, 0.733]"],
        "frozen-wide": ["0.863 [0.783, 0.950]", "0.874 [0.842, 0.933]", "0.887 [0.859, 0.918]", "0.898 [0.850, 0.930]", "0.884 [0.783, 0.950]"],
        "c3:all-diag-mech": ["0.350 [0.0808, 0.432]", "0.250 [0.0801, 0.327]", "0.191 [0.148, 0.330]", "0.224 [0.170, 0.332]", "0.260 [0.0801, 0.432]"],
        "pair-hull": ["0.952 [0.816, 0.960]", "0.890 [0.866, 0.928]", "0.935 [0.906, 0.942]", "0.916 [0.889, 0.930]", "0.914 [0.816, 0.960]"],
        "v3d:all-diag-mech": ["0.442 [0.255, 0.756]", "0.438 [0.354, 0.477]", "0.433 [0.364, 0.464]", "0.458 [0.371, 0.516]", "0.440 [0.255, 0.756]"],
        "v3d:all-diag-mech-wide": ["1 [1, 1]"] * 5,
    }
    for m, cols in gc.items():
        for col, d in zip(["n10", "n20", "n40", "n80", "all"], cols):
            triple(f"C2 root gap closed {m} {col}", d, R[f"C2 root gapclosed {m} {col}"], ONE if d.startswith("1 ") else None)
    # ---- C2 residual closure
    res = {
        "c3:baseline": ["-19.8 [-24.0, -4.45]", "-8.09 [-12.8, -6.48]", "-14.4 [-16.2, -9.68]", "-10.9 [-13.2, -8.01]"],
        "baseline-novarlocks": ["-0.0739 [-0.0872, -0.0207]", "-0.0385 [-0.0708, -0.0330]", "-0.0571 [-0.0665, -0.0511]", "-0.0537 [-0.0728, -0.0419]"],
        "baseline-extra": ["-5.17 [-8.02, -1.75]", "-3.31 [-4.15, -2.14]", "-4.15 [-4.75, -3.35]", "-4.14 [-5.43, -2.30]"],
        "frozen-wide": ["-0.142 [-4.42, 0.405]", "0.0533 [-0.366, 0.0680]", "-0.413 [-1.17, -0.210]", "-0.449 [-1.09, 0.198]"],
        "c3:all-diag-mech": ["-12.5 [-16.9, -2.41]", "-5.82 [-11.7, -4.03]", "-10.5 [-12.1, -7.68]", "-8.52 [-9.79, -6.21]"],
        "v3d:all-diag-mech": ["-5.11 [-14.9, -1.45]", "-4.56 [-7.69, -2.91]", "-8.21 [-8.77, -4.97]", "-5.43 [-6.97, -4.58]"],
        "v3d:all-diag-mech-wide": ["1 [1, 1]"] * 4,
    }
    for m, cols in res.items():
        for col, d in zip(["n10", "n20", "n40", "n80"], cols):
            triple(f"C2 residual closure {m} {col}", d, R[f"C2 root residual {m} {col}"], ONE if d.startswith("1 ") else None)
    # ---- C2 root bounds
    rb = {
        "c3:baseline": ["-0.2523 [-0.3413, -0.2362]", "-0.5796 [-0.6480, -0.2612]", "-1.226 [-1.417, -0.9454]", "-1.818 [-2.383, -1.749]"],
        "baseline-novarlocks": ["-0.001101 [-0.001272, -0.0009158]", "-0.002365 [-0.002569, -0.002083]", "-0.005075 [-0.005375, -0.004611]", "-0.009679 [-0.009947, -0.009509]"],
        "baseline-extra": ["-0.08864 [-0.09952, -0.06748]", "-0.1676 [-0.2590, -0.1137]", "-0.3349 [-0.4161, -0.3229]", "-0.7445 [-0.7993, -0.5212]"],
        "frozen-wide": ["-0.00185 [-0.04645, 0.02153]", "0.003288 [-0.02625, 0.003585]", "-0.03615 [-0.1042, -0.02056]", "-0.0761 [-0.1485, 0.04272]"],
        "c3:all-diag-mech": ["-0.1775 [-0.2158, -0.1201]", "-0.4171 [-0.5663, -0.1960]", "-0.8743 [-1.073, -0.7480]", "-1.424 [-1.533, -1.338]"],
        "v3d:all-diag-mech": ["-0.1624 [-0.1944, -0.05364]", "-0.2942 [-0.3718, -0.1565]", "-0.6610 [-0.7784, -0.4855]", "-0.9861 [-1.128, -0.8750]"],
        "v3d:all-diag-mech-wide": ["0.01721 [0.0105, 0.0531]", "0.06103 [0.0343, 0.07166]", "0.08875 [0.07776, 0.09766]", "0.1799 [0.1366, 0.2269]"],
    }
    for m, cols in rb.items():
        for col, d in zip(["n10", "n20", "n40", "n80"], cols):
            triple(f"C2 root bound {m} {col}", d, R[f"C2 root bound {m} {col}"])
    lo, hi, above = R["C2 root novarlocks min/max"]
    num("C2 root novarlocks lowest root bound", "-0.009947", lo)
    num("C2 root novarlocks highest root bound", "-0.0009158", hi)
    exact("C2 root novarlocks instances above 0", 0, above)
    exact("C2 root frozen-wide instances above 0", ["n10_s0", "n10_s4", "n20_s2", "n20_s3", "n20_s4", "n80_s1", "n80_s4"],
          R["C2 root frozen-wide above 0"])
    exact("C2 root frozen-wide runs at cut cap 16n", 20, R["C2 caps root frozen-wide"]["cut"])

    # ---- C2 full
    n10 = ["n10_s0", "n10_s1", "n10_s2", "n10_s3", "n10_s4"]
    n20 = ["n20_s0", "n20_s1", "n20_s2", "n20_s3", "n20_s4"]
    full = {"c3:baseline": (9, n10 + n20[1:], "58,222.5"), "c3:all-diag-mech": (9, n10 + n20[1:], "58,105"),
            "baseline-novarlocks": (10, n10 + n20, "35,332"), "baseline-extra": (10, n10 + n20, "88,485"),
            "frozen-wide": (13, n10 + n20 + ["n40_s0", "n40_s2", "n40_s4"], "8,346"),
            "gurobi": (7, n10 + ["n20_s1", "n20_s2"], "247,157.5")}
    for m, (cnt, lst, nodes) in full.items():
        exact(f"C2 full {m} solved", cnt, R[f"C2 full {m} solved"])
        exact(f"C2 full {m} solved list", sorted(lst), R[f"C2 full {m} solved list"])
        num(f"C2 full {m} median nodes (all 20)", nodes, R[f"C2 full {m} median nodes all"])
    exact("C2 full gurobi statuses of solved (gaplimit 5, optimal 2)", (5, 2),
          (R["C2 full gurobi statuses"].get("gaplimit"), R["C2 full gurobi statuses"].get("optimal")))
    exact("C2 full common solved (all six modes)", sorted(n10 + ["n20_s1", "n20_s2"]), R["C2 full common solved"])
    tab = {"c3:baseline": ("5.597", "1,521", None), "c3:all-diag-mech": ("3.727", "400", ("0.773", 9, 6)),
           "baseline-novarlocks": ("2.709", "879", ("0.384", 9, 8)), "baseline-extra": ("4.030", "722", ("0.482", 9, 7)),
           "frozen-wide": ("4.623", "52", ("1.171", 9, 4)), "gurobi": ("6.321", "346", ("0.256", 7, 4))}
    for m, (sg, nodes, ratio) in tab.items():
        num(f"C2 full SGM over 7 common {m}", sg, R[f"C2 full common {m} sgm"])
        num(f"C2 full median nodes over 7 common {m}", nodes, R[f"C2 full common {m} median nodes"])
        if ratio:
            med, pairs, faster = R[f"C2 full ratio {m}"]
            num(f"C2 full median time ratio vs c3:baseline {m}", ratio[0], med)
            exact(f"C2 full ratio pairs/faster {m}", ratio[1:], (pairs, faster))
    num("C2 full SGM c3:baseline over its 9 solved", "10.270", R["C2 full pairs c3:all-diag-mech sgm ref"])
    for m, d in (("c3:all-diag-mech", "6.661"), ("baseline-novarlocks", "4.817"), ("baseline-extra", "6.531"), ("frozen-wide", "5.166")):
        num(f"C2 full SGM over pairs with c3:baseline {m}", d, R[f"C2 full pairs {m} sgm mode"])
    num("C2 full SGM gurobi over its 7", "6.321", R["C2 full pairs gurobi sgm mode"])
    num("C2 full SGM c3:baseline over gurobi's 7", "5.597", R["C2 full pairs gurobi sgm ref"])
    for m, cnts, worse in (("c3:all-diag-mech", {"better": 10, "tie": 9, "worse": 1}, ["n40_s1"]),
                           ("baseline-novarlocks", {"better": 11, "tie": 9, "worse": 0}, []),
                           ("baseline-extra", {"better": 11, "tie": 9, "worse": 0}, []),
                           ("frozen-wide", {"better": 11, "tie": 9, "worse": 0}, []),
                           ("gurobi", {"better": 11, "tie": 7, "worse": 2}, ["n20_s3", "n20_s4"])):
        exact(f"C2 full final dual vs c3:baseline rtol 1e-4 {m}", cnts, R[f"C2 full bound vs c3:baseline {m} rtol0.0001"])
        exact(f"C2 full final dual worse list rtol 1e-4 {m}", worse, R[f"C2 full bound vs c3:baseline {m} rtol0.0001 worse list"])
    num("C2 full c3:baseline load_start mean", "16.0", R["C2 full c3:baseline load_start_mean"])
    c2loads = [R[f"C2 full {m} load_start_mean"] for m in ("baseline-novarlocks", "baseline-extra", "frozen-wide", "gurobi")]
    num("C2 full own-mode load_start mean, lowest", "6.49", min(c2loads))
    num("C2 full own-mode load_start mean, highest", "6.90", max(c2loads))

    # ---- 2x2
    exact("2x2 v3d all-diag-mech solved", 10, R["C2 full v3d:all-diag-mech solved"])
    exact("2x2 v3d all-diag-mech solved list", sorted(n10 + n20), R["C2 full v3d:all-diag-mech solved list"])
    exact("2x2 v3d all-diag-mech-wide solved", 20, R["C2 full v3d:all-diag-mech-wide solved"])
    exact("2x2 v3d wide root runs solved at root", 12, len(R["C2 root v3d wide optimal at root"]))
    num("2x2 v3d full load_start mean", "18.0", R["V3D full load_start_mean"])
    num("2x2 v3d root load_start mean", "14.4", R["V3D root load_start_mean"])
    exact("2x2 c3:all-diag-mech solved", 9, R["C2 full c3:all-diag-mech solved"])
    exact("2x2 frozen-wide solved", 13, R["C2 full frozen-wide solved"])

    # ---- C2 Gurobi table
    G = R["C2 gurobi table"]
    gt = {"n10_s1": ("optimal", "OPTIMAL", "-7.6e-9", "0", "0.33", "346"),
          "n10_s2": ("optimal", "OPTIMAL", "3.35e-7", "0", "0.35", "343"),
          "n10_s3": ("gaplimit", "OPTIMAL", "-2.2e-6", "9.5e-5", "0.29", "322"),
          "n20_s2": ("gaplimit", "OPTIMAL", "-2.7e-6", "7.5e-5", "0.49", "334"),
          "n10_s0": ("gaplimit", "OPTIMAL", "-9.4e-6", "1.0e-4", "45.6", "289,663"),
          "n10_s4": ("gaplimit", "OPTIMAL", "-1.0e-5", "1.0e-4", "77.6", "488,091"),
          "n20_s1": ("gaplimit", "OPTIMAL", "-4.1e-6", "5.75e-5", "88.7", "204,652"),
          "n20_s0": ("timelimit", "TIME_LIMIT", "-6.27e-4", "0.00863", "300.2", None),
          "n20_s3": ("timelimit", "TIME_LIMIT", "-3.11e-4", "0.00452", "300.2", None),
          "n20_s4": ("timelimit", "TIME_LIMIT", "-1.83e-4", "0.00354", "300.2", None)}
    for k, (st, gs, dmo, gap, t, nodes) in gt.items():
        exact(f"C2 gurobi {k} status/gurobi status", (st, gs), (G[k]["status"], G[k]["gstatus"]))
        num(f"C2 gurobi {k} bound - optimum", dmo, G[k]["dual-opt"])
        num(f"C2 gurobi {k} mip_gap", gap, G[k]["mip_gap"])
        num(f"C2 gurobi {k} time", t, G[k]["time"])
        if nodes:
            num(f"C2 gurobi {k} nodes", nodes, G[k]["nodes"])
    tl20 = [G[k]["nodes"] for k in ("n20_s0", "n20_s3", "n20_s4")]
    num("C2 gurobi n20 timelimit nodes min", "799,843", min(tl20))
    num("C2 gurobi n20 timelimit nodes max", "871,276", max(tl20))
    for n, dmo, bnd, gap, nodes in ((40, ("-0.0593", "-0.0687"), ("0.0150", "0.0384"), ("0.609", "0.810"), ("329,645", "347,162")),
                                    (80, ("-0.155", "-0.240"), ("-0.0211", "-0.0033"), ("1.01", "1.13"), ("175,928", "186,544"))):
        ks = [f"n{n}_s{i}" for i in range(5)]
        exact(f"C2 gurobi n{n} statuses", ["timelimit"] * 5, [G[k]["status"] for k in ks])
        v = [G[k]["dual-opt"] for k in ks]
        num(f"C2 gurobi n{n} bound - optimum, closest", dmo[0], max(v))
        num(f"C2 gurobi n{n} bound - optimum, farthest", dmo[1], min(v))
        v = [G[k]["dual"] for k in ks]
        num(f"C2 gurobi n{n} bound min", bnd[0], min(v))
        num(f"C2 gurobi n{n} bound max", bnd[1], max(v))
        v = [G[k]["mip_gap"] for k in ks]
        num(f"C2 gurobi n{n} mip_gap min", gap[0], min(v))
        num(f"C2 gurobi n{n} mip_gap max", gap[1], max(v))
        v = [G[k]["nodes"] for k in ks]
        num(f"C2 gurobi n{n} nodes min", nodes[0], min(v))
        num(f"C2 gurobi n{n} nodes max", nodes[1], max(v))
    exact("C2 gurobi incumbents passing check", 20, sum(g["passed"] for g in G.values()))
    num("C2 gurobi max scaled violation", "9.8e-7", max(g["viol"] for g in G.values()))
    below = {k: g["primal-opt"] for k, g in G.items() if g["primal-opt"] < 0}
    exact("C2 gurobi incumbents below optimum (count)", 9, len(below))
    num("C2 gurobi largest incumbent shortfall", "-1.14e-5", min(below.values()))
    exact("C2 gurobi largest shortfall instance", "n20_s4", min(below, key=below.get))
    for n, lo_, hi_ in ((40, "0.040", "0.056"), (80, "0.031", "0.049")):
        a, b = R[f"C2 full final dual baseline-novarlocks n{n} min/max"]
        num(f"C2 novarlocks final dual n{n} min", lo_, a)
        num(f"C2 novarlocks final dual n{n} max", hi_, b)

    # ---- C3 root
    gc3 = {"baseline-extra": ["0.572 [0.488, 0.732]", "0.640 [0.539, 0.671]", "0.611 [0.423, 0.652]", "0.660 [0.574, 0.679]", "0.617 [0.423, 0.732]"],
           "all-diag-mech": ["0.323 [0.0151, 0.456]", "0.310 [0.0958, 0.374]", "0.238 [0.117, 0.312]", "0.205 [0.158, 0.295]", "0.232 [0.0151, 0.456]"],
           "rowdir-wide": ["1 [1, 1]"] * 5,
           "pair-hull": ["0.927 [0.821, 0.969]", "0.922 [0.878, 0.947]", "0.928 [0.894, 0.947]", "0.923 [0.893, 0.931]", "0.925 [0.821, 0.969]"]}
    for m, cols in gc3.items():
        for col, d in zip(["n10", "n20", "n40", "n80", "all"], cols):
            triple(f"C3 root gap closed {m} {col}", d, R[f"C3 root gapclosed {m} {col}"], ONE if d.startswith("1 ") else None)
    res3 = {"baseline": ["-12.6 [-31.2, -4.57]", "-11.8 [-18.0, -7.22]", "-13.0 [-17.8, -8.47]", "-12.0 [-13.4, -8.30]"],
            "baseline-extra": ["-4.84 [-15.5, -1.34]", "-3.52 [-5.38, -2.79]", "-5.01 [-5.56, -2.58]", "-3.30 [-3.78, -2.96]"],
            "all-diag-mech": ["-7.77 [-30.7, -2.03]", "-10.5 [-12.1, -4.15]", "-8.61 [-13.3, -6.33]", "-8.55 [-10.4, -6.40]"],
            "rowdir-wide": ["1 [1, 1]"] * 4}
    for m, cols in res3.items():
        for col, d in zip(["n10", "n20", "n40", "n80"], cols):
            triple(f"C3 residual closure {m} {col}", d, R[f"C3 root residual {m} {col}"], ONE if d.startswith("1 ") else None)
    for m in ("baseline-extra", "all-diag-mech", "rowdir-wide"):
        for rt in ("0.0001", "1e-06"):
            exact(f"C3 root {m} vs baseline rtol {rt}", {"better": 20, "tie": 0, "worse": 0}, R[f"C3 root vs baseline {m} rtol{float(rt):g}"])
    a, b = R["C3 root rowdir-wide root-opt min/max"]
    num("C3 root rowdir-wide root - optimum, min", "-2.0e-7", a)
    num("C3 root rowdir-wide root - optimum, max", "7.1e-13", b)
    exact("C3 root rowdir-wide optimal at root", ["n10_s5", "n10_s6", "n10_s8", "n10_s9", "n20_s5", "n20_s7", "n20_s8", "n20_s9"],
          R["C3 root rowdir-wide optimal at root"])
    exact("C3 root rowdir-wide runs without root_dual = optimal-at-root runs", R["C3 root rowdir-wide optimal at root"],
          R["C3 root rowdir-wide no root_dual"])
    for m in ("baseline", "baseline-extra", "all-diag-mech"):
        exact(f"C3 root {m} statuses", {"nodelimit": 20}, R[f"C3 root {m} statuses"])

    # ---- C3 full
    c10 = [f"n10_s{i}" for i in range(5, 10)]
    c20 = [f"n20_s{i}" for i in range(5, 10)]
    full3 = {"baseline": (9, c10 + ["n20_s5", "n20_s7", "n20_s8", "n20_s9"], "71,276.5"),
             "all-diag-mech": (10, c10 + c20, "81,185.5"),
             "rowdir-wide": (20, None, "1"),
             "baseline-extra": (9, c10 + ["n20_s5", "n20_s7", "n20_s8", "n20_s9"], "94,019.5"),
             "gurobi": (5, c10, "258,452.5")}
    for m, (cnt, lst, nodes) in full3.items():
        exact(f"C3 full {m} solved", cnt, R[f"C3 full {m} solved"])
        if lst:
            exact(f"C3 full {m} solved list", sorted(lst), R[f"C3 full {m} solved list"])
        num(f"C3 full {m} median nodes (all 20)", nodes, R[f"C3 full {m} median nodes all"])
    exact("C3 full rowdir-wide max nodes", 38, R["C3 full rowdir-wide max nodes"])
    exact("C3 full gurobi optimal/gaplimit", (2, 3), (R["C3 full gurobi statuses"].get("optimal"), R["C3 full gurobi statuses"].get("gaplimit")))
    exact("C3 full common solved", sorted(c10), R["C3 full common solved"])
    tab3 = {"baseline": ("1.698", "1.656", "scip", "1,443", None),
            "all-diag-mech": ("2.104", "1.202", "scip-excl-cb", "628", ("0.858", 9, 5)),
            "rowdir-wide": ("3.284", "0.1238", "scip-excl-cb", "1", ("0.860", 9, 5)),
            "baseline-extra": ("1.061", "1.026", "scip", "559", ("0.627", 9, 6)),
            "gurobi": ("0.334", "0.330", "scip", "358", ("0.235", 5, 5))}
    for m, (sg, sc, sck, nodes, ratio) in tab3.items():
        num(f"C3 full SGM over 5 common {m}", sg, R[f"C3 full common {m} sgm"])
        num(f"C3 full SGM {sck} over 5 common {m}", sc, R[f"C3 full common {m} sgm {sck}"])
        num(f"C3 full median nodes over 5 common {m}", nodes, R[f"C3 full common {m} median nodes"])
        if ratio:
            med, pairs, faster = R[f"C3 full ratio {m}"]
            num(f"C3 full median time ratio vs baseline {m}", ratio[0], med)
            exact(f"C3 full ratio pairs/faster {m}", ratio[1:], (pairs, faster))
    num("C3 full SGM baseline over its 9 solved", "9.379", R["C3 full pairs all-diag-mech sgm ref"])
    for m, d in (("all-diag-mech", "7.267"), ("rowdir-wide", "4.434"), ("baseline-extra", "7.067")):
        num(f"C3 full SGM over pairs with baseline {m}", d, R[f"C3 full pairs {m} sgm mode"])
    num("C3 full rowdir-wide SGM over all 20", "10.19", R["C3 full rowdir-wide all20 sgm"])
    a, b = R["C3 full rowdir-wide all20 min/max time"]
    num("C3 full rowdir-wide fastest", "3.17", a)
    num("C3 full rowdir-wide slowest", "33.17", b)
    n80t = R["C3 full rowdir-wide n80 times"]
    num("C3 full rowdir-wide n80 fastest", "31.7", min(n80t))
    num("C3 full rowdir-wide n80 slowest", "33.2", max(n80t))
    a, b = R["C3 full rowdir-wide sum callback / sum total"]
    num("C3 full rowdir-wide summed callback", "268.6", a)
    num("C3 full rowdir-wide summed charged time", "279.7", b)
    for m, cnts, worse in (("all-diag-mech", {"better": 11, "tie": 9, "worse": 0}, []),
                           ("rowdir-wide", {"better": 11, "tie": 9, "worse": 0}, []),
                           ("baseline-extra", {"better": 10, "tie": 9, "worse": 1}, ["n40_s8"]),
                           ("gurobi", {"better": 11, "tie": 5, "worse": 4}, ["n20_s5", "n20_s7", "n20_s8", "n20_s9"])):
        exact(f"C3 full final dual vs baseline rtol 1e-4 {m}", cnts, R[f"C3 full bound vs baseline {m} rtol0.0001"])
        exact(f"C3 full final dual worse list rtol 1e-4 {m}", worse, R[f"C3 full bound vs baseline {m} rtol0.0001 worse list"])

    # ---- C3 Gurobi
    G3 = R["C3 gurobi table"]
    exact("C3 gurobi n10 optimal", ["n10_s7", "n10_s8"], sorted(k for k in c10 if G3[k]["status"] == "optimal"))
    exact("C3 gurobi n10 gaplimit", ["n10_s5", "n10_s6", "n10_s9"], sorted(k for k in c10 if G3[k]["status"] == "gaplimit"))
    num("C3 gurobi n10 fastest", "0.25", min(G3[k]["time"] for k in c10))
    num("C3 gurobi n10 slowest", "0.43", max(G3[k]["time"] for k in c10))
    exact("C3 gurobi n20 all timelimit", ["timelimit"] * 5, [G3[k]["status"] for k in c20])
    num("C3 gurobi n20 mip_gap min", "6.0e-4", min(G3[k]["mip_gap"] for k in c20))
    num("C3 gurobi n20 mip_gap max", "0.0152", max(G3[k]["mip_gap"] for k in c20))
    num("C3 gurobi n20 bound below optimum, least", "4.4e-5", -max(G3[k]["dual-opt"] for k in c20))
    num("C3 gurobi n20 bound below optimum, most", "6.7e-4", -min(G3[k]["dual-opt"] for k in c20))
    c40 = [f"n40_s{i}" for i in range(5, 10)]
    c80 = [f"n80_s{i}" for i in range(5, 10)]
    num("C3 gurobi n40 mip_gap min", "0.534", min(G3[k]["mip_gap"] for k in c40))
    num("C3 gurobi n40 mip_gap max", "0.848", max(G3[k]["mip_gap"] for k in c40))
    num("C3 gurobi n80 mip_gap min", "1.04", min(G3[k]["mip_gap"] for k in c80))
    num("C3 gurobi n80 mip_gap max", "1.21", max(G3[k]["mip_gap"] for k in c80))
    exact("C3 gurobi n80 bounds negative", 5, sum(G3[k]["dual"] < 0 for k in c80))
    above = {k: g["dual-opt"] for k, g in G3.items() if g["dual-opt"] > 0}
    exact("C3 gurobi instances with bound above optimum", ["n10_s7", "n10_s8", "n10_s9"], sorted(above))
    num("C3 gurobi n10_s7 bound - optimum", "1.07e-6", G3["n10_s7"]["dual-opt"])
    num("C3 gurobi n10_s8 bound - optimum", "1.16e-6", G3["n10_s8"]["dual-opt"])
    num("C3 gurobi n10_s9 bound - optimum", "2.43e-7", G3["n10_s9"]["dual-opt"])
    num("C3 gurobi largest relative bound excess (n10_s7)", "1.95e-4", G3["n10_s7"]["rel dual excess"])
    exact("C3 gurobi largest relative excess instance", "n10_s7", max(G3, key=lambda k: G3[k]["rel dual excess"]))
    worst = min(G3, key=lambda k: G3[k]["primal-opt"])
    exact("C3 gurobi largest incumbent shortfall instance", "n20_s6", worst)
    num("C3 gurobi largest incumbent shortfall", "-1.55e-5", G3[worst]["primal-opt"])
    num("C3 gurobi n20_s6 scaled violation", "1.1e-6", G3["n20_s6"]["viol"])
    exact("C3 gurobi incumbents passing check", 20, sum(g["passed"] for g in G3.values()))
    exact("C2 gurobi bound above optimum", ["n10_s2"], sorted(k for k, g in G.items() if g["dual-opt"] > 0))
    exact("Gurobi reference-check conflicts (C2+C3)", 0, sum(not g["ref_dual_consistent"] for g in list(G.values()) + list(G3.values())))

    # ---- C3 (c) replication statement
    m3 = [R[f"C3 root gapclosed all-diag-mech n{n}"][0] for n in NS]
    m2 = [R[f"C2 root gapclosed c3:all-diag-mech n{n}"][0] for n in NS]
    num("C3 all-diag-mech median gap closed per n, lowest", "0.205", min(m3))
    num("C3 all-diag-mech median gap closed per n, highest", "0.323", max(m3))
    num("C2 c3:all-diag-mech median gap closed per n, lowest", "0.191", min(m2))
    num("C2 c3:all-diag-mech median gap closed per n, highest", "0.350", max(m2))

    # ---- time decomposition (path rows)
    td = {("C2", "root", "c3:all-diag-mech"): (20, "4.077", "1.198", "2.913", "1.099", "1.022", "1.18", "3.99"),
          ("C2", "root", "frozen-wide"): (20, "10.06", "1.161", "8.956", "1.099", "1.022", "1.19", "9.49"),
          ("C2", "full", "c3:all-diag-mech"): (9, "6.661", "4.692", "1.249", "10.27", "10.17", "0.395", "0.773"),
          ("C2", "full", "frozen-wide"): (9, "5.166", "1.247", "3.828", "10.27", "10.17", "0.144", "1.171"),
          ("C3", "root", "all-diag-mech"): (20, "3.795", "1.140", "2.698", "1.062", "0.990", "1.21", "3.94"),
          ("C3", "root", "rowdir-wide"): (20, "10.25", "0.391", "9.863", "1.062", "0.990", "0.330", "10.99"),
          ("C3", "full", "all-diag-mech"): (9, "7.267", "5.605", "1.152", "9.379", "9.284", "0.783", "0.858"),
          ("C3", "full", "rowdir-wide"): (9, "4.434", "0.1405", "4.252", "9.379", "9.284", "0.0369", "0.860")}
    fields = ("sgm total", "sgm scip-excl", "sgm cb", "ref sgm total", "ref sgm scip", "median scip-excl/ref scip", "median total/ref total")
    for (fam, ph, m), vals in td.items():
        T = R[f"{fam} timedecomp {ph} {m}"]
        exact(f"time decomposition {fam} {ph} {m} pairs", vals[0], T["pairs"])
        for f, d in zip(fields, vals[1:]):
            num(f"time decomposition {fam} {ph} {m} {f}", d, T[f])
    num("C2 root baseline-extra median total ratio vs c3:baseline", "1.196", R["C2 timedecomp root baseline-extra"]["median total/ref total"])
    num("C3 root baseline-extra median total ratio vs baseline", "1.262", R["C3 timedecomp root baseline-extra"]["median total/ref total"])
    num("C2 root novarlocks median total ratio vs c3:baseline", "0.229", R["C2 timedecomp root baseline-novarlocks"]["median total/ref total"])
    num("C2 full novarlocks median total ratio vs c3:baseline", "0.384", R["C2 timedecomp full baseline-novarlocks"]["median total/ref total"])

    # ---- funnel (path rows)
    fu = {("C2", "frozen-wide"): (122, 13502, 0, 1189, 313, 20, {"column_set_differs_tiny_coefficient_dropped": 313}, 12000),
          ("C2", "c3:all-diag-mech"): (80, 3462, 0, 391, 71, 13, {}, 3000),
          ("C3", "all-diag-mech"): (80, 3558, 0, 474, 84, 16, {"column_set_differs_tiny_coefficient_dropped": 84}, 3000),
          ("C3", "rowdir-wide"): (140, 15534, 0, 3181, 353, 20, {"column_set_differs_tiny_coefficient_dropped": 353}, 12000)}
    for (fam, m), v in fu.items():
        F = R[f"{fam} funnel root {m}"]
        got = (F["calls"], F["certification_calls"], F["certification_failures"], F["below"], F["row_binding_rejections"],
               F["runs_binding"], F["causes"], F["cuts"])
        exact(f"funnel {fam} {m} (callbacks, support calls, cert fail, below, binding, runs, causes, cuts)", v, got)
        exact(f"funnel {fam} {m} rounding rejections", 0, F["row_rounding_rejections"])
        exact(f"funnel {fam} {m} root == full (sums and per run)", (True, []), (R[f"{fam} funnel root=={'full'} {m}"], R[f"{fam} funnel per-run root!=full {m}"]))
        C = R[f"{fam} caps root {m}"]
        exact(f"caps {fam} {m} root (cut cap/support cap/10 callbacks/discovery stopped)", (20, 0, 0, 0),
              (C["cut"], C["support"], C["rounds"], C["discovery_incomplete"]))

    # ---- native separators and surprises
    mn = R["C2 root novarlocks minor"]
    exact("C2 root novarlocks minor (calls, found, applied, runs)", (661, 34061, 17039, 20),
          (mn["Calls"], mn["FoundCuts"], mn["Applied"], mn["productive_runs"]))
    num("C2 root novarlocks SGM time (all 20)", "0.341", R["C2 root sgm all20 baseline-novarlocks"])
    num("C2 root c3:baseline SGM time (all 20)", "1.099", R["C2 root sgm all20 c3:baseline"])
    for fam, calls, cuts in (("C2", 29210, 14907), ("C3", 31490, 14875)):
        q = R[f"{fam} root baseline-extra intersection (nlhdlr quadratic)"]
        exact(f"{fam} root baseline-extra intersection cuts (runs, enforce calls, cuts)", (20, calls, cuts),
              (q["productive_runs"], q["#Enforce"], q["Cuts"]))
        exact(f"{fam} root baseline-extra RLT calls / cuts found", (200, 0), (R[f"{fam} root baseline-extra rlt"]["Calls"], R[f"{fam} root baseline-extra rlt"]["FoundCuts"]))
        exact(f"{fam} root baseline-extra interminor/eccuts calls", (0, 0), (R[f"{fam} root baseline-extra interminor"]["Calls"], R[f"{fam} root baseline-extra eccuts"]["Calls"]))
    nvs = R["C2 full novarlocks solved: status, primal-opt, dual-opt, rel, primal==dual"]
    exact("C2 full novarlocks solved runs: all optimal with primal == dual", (10, True),
          (len(nvs), all(v[0] == "optimal" and v[4] for v in nvs.values())))
    num("C2 full novarlocks smallest shortfall below optimum", "1.84e-6", -max(v[1] for v in nvs.values()))
    num("C2 full novarlocks largest shortfall below optimum", "6.98e-6", -min(v[1] for v in nvs.values()))
    num("C2 full novarlocks largest relative shortfall", "3.8e-4", -min(v[3] for v in nvs.values()))
    exact("C2 full novarlocks largest relative shortfall instance", "n10_s1", min(nvs, key=lambda k: nvs[k][3]))
    exact("C2 full novarlocks worse than c3:baseline at 1e-6 (count)", 9, R["C2 full bound vs c3:baseline baseline-novarlocks rtol1e-06"]["worse"])
    for fam, cnt in (("C2", 40), ("C3", 47)):
        n_, lo_, hi_ = R[f"{fam} timelimit runs count/min/max time"]
        exact(f"{fam} time-limit runs (soft overshoots)", cnt, n_)
        CHECKS.append((f"{fam} time-limit runs charged within 300.19-300.36 s", "300.19-300.36", f"{lo_:.3f}-{hi_:.3f}",
                       300.185 <= lo_ and hi_ <= 300.365))
    exact("C2/C3 root time-limit runs", 0, R["C2 root timelimit runs"] + R["C3 root timelimit runs"])
    exact("C2/C3 certification failures", 0, R["C2 cert failures total"] + R["C3 cert failures total"])
    exact("C2/C3 classifier_errors", 0, R["C2 classifier_errors total"] + R["C3 classifier_errors total"])
    exact("C2/C3 primal-check failures", 0, R["C2 primal check failures"] + R["C3 primal check failures"])
    num("c3 root reference load_start mean (about 16)", "16", R["V3 root load_start_mean"], tol=0.5)
    c3loads = list(R["C3 root load_start_mean per mode"].values()) + list(R["C2 root load_start_mean per mode"].values())
    CHECKS.append(("campaign-4 path load_start means within 3.5-7.7", "3.5-7.7",
                   f"{min(c2loads + c3loads):.2f}-{max(c2loads + c3loads):.2f}", max(c2loads + c3loads) <= 7.75))

    # ---- replay (C2, C3)
    for fam, cuts, bound_runs in (("C2", 24000, 120), ("C3", 30000, 160)):
        rp = R[f"{fam} replay top-level"]
        exact(f"{fam} replay passed / cuts / replayed / bound runs", (True, cuts, cuts, bound_runs),
              (rp["passed"], rp["cuts"], rp["replayed_cuts"], rp["bound_runs"]))


run_checks()


if __name__ == "__main__":
    out = None
    if "--json" in sys.argv:
        out = sys.argv[sys.argv.index("--json") + 1]
    if "--values" in sys.argv:
        for k, v in R.items():
            if isinstance(v, dict) and len(json.dumps(v, default=str)) > 400:
                print(k + ":")
                for kk, vv in v.items():
                    print("   ", kk, vv)
            else:
                print(k + ":", v)
    bad = [c for c in CHECKS if not c[3]]
    print(f"\nDIGEST CHECKS: {len(CHECKS)} run, {len(CHECKS) - len(bad)} match, {len(bad)} mismatch")
    for item, d, v, ok in bad:
        print(f"  MISMATCH {item}: digest {d} | recomputed {v}")
    if out:
        json.dump({"values": R, "checks": CHECKS}, open(out, "w"), indent=1, default=str)
