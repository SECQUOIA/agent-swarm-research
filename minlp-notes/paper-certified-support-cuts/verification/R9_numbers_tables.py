#!/usr/bin/env python3
"""R9 (numbers lens), part 2: compare every cell of the appendix tables
(sections/B-tables.tex) with the raw records, and run a few further checks
(distinct cuts, node counts at the root, native separator activity, loads).

Standard library only; imports no producer code. Uses the definitions of
R9_numbers_recompute.py (imported from the same directory).
"""
import glob
import json
import math
import os
import re
import statistics
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from R9_numbers_recompute import (EXP, load, cases, solved, ttime, root_bound, gap_closed, cb,  # noqa: E402
                                  scip_time, cmp_bound, finite)

TEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sections", "B-tables.tex")
STATUS = {"optimal": "o", "gaplimit": "g", "timelimit": "t"}


def fmt(x):
    if x is None:
        return None
    if abs(x) >= 1000:
        return str(int(round(x)))
    s = "%.4g" % x
    if "e" in s:
        m, e = s.split("e")
        s = f"{m}e{int(e)}"
    return s


def tex_num(cell):
    """'$-9.705\\cdot10^{-9}$' -> '-9.705e-9'; 'o $1.464$' -> ('o', '1.464')."""
    cell = cell.strip().replace("\\textsuperscript{\\dag}", "")
    st = None
    m = re.match(r"^([ogt])\s+(.*)$", cell)
    if m:
        st, cell = m.group(1), m.group(2)
    cell = cell.replace("$", "").strip()
    cell = re.sub(r"\\cdot\s*10\^\{(-?\d+)\}", r"e\1", cell)
    return st, cell


def rows_of(label):
    txt = open(TEX).read()
    i = txt.index("\\label{%s}" % label)
    j = txt.index("\\midrule", i)
    k = txt.index("\\bottomrule", j)
    body = txt[j + len("\\midrule"):k]
    out = []
    for line in body.split("\\\\"):
        line = re.sub(r"^\\midrule\s*", "", line.strip())
        if not line or line.startswith("\\multicolumn"):
            continue
        cells = [c.strip() for c in line.split("&")]
        out.append(cells)
    return out


def name_of(cell):
    m = re.search(r"\\code\{(.*?)\}", cell)
    return m.group(1).replace("\\_", "_") if m else cell


mism = []


def check(table, row, col, tex_cell, value, status=None):
    st, num = tex_num(tex_cell)
    want = fmt(value) if isinstance(value, (int, float)) else value
    ok = (num == want) or (want is not None and _close(num, value))
    if status is not None and st != STATUS.get(status, status):
        ok = False
    if not ok:
        mism.append((table, row, col, tex_cell, want, status))
    return ok


def _close(num, value):
    try:
        x = float(num)
    except ValueError:
        return False
    if not isinstance(value, (int, float)):
        return False
    if abs(value) >= 1000:
        return abs(x - value) <= 0.5 + 1e-9
    if value == 0:
        return x == 0
    # four significant digits
    return fmt(value) == fmt(x)


def table_partA():
    root = {(r["name"], r["mode"]): r for r in load("v3/runs/partA-root")}
    full = {(r["name"], r["mode"]): r for r in load("v3/runs/partA-full") if r["seed"] == 0}
    n = 0
    for cells in rows_of("tab:partA"):
        nm = name_of(cells[0])
        b, d = root[(nm, "baseline")], root[(nm, "all-diag")]
        check("A", nm, "root base", cells[1], root_bound(b))
        check("A", nm, "root diag", cells[2], root_bound(d))
        check("A", nm, "cuts diag", cells[3], str(len(d.get("cuts") or [])))
        fb, fa = full[(nm, "baseline")], full[(nm, "all")]
        check("A", nm, "full base", cells[4], ttime(fb), fb["status"])
        check("A", nm, "full all", cells[5], ttime(fa), fa["status"])
        check("A", nm, "cuts all", cells[6], str(len(fa.get("cuts") or [])))
        n += 1
    return n


def table_partB():
    v3 = load("v3/runs/partB")
    root = {(r["name"], r["mode"]): r for r in v3 if r["phase"] == "root"}
    full = {(r["name"], r["mode"]): r for r in v3 if r["phase"] == "full" and r["seed"] == 0}
    b2 = {(r["name"], r["mode"]): r for r in load("v4/runs/partB2")}
    n = 0
    for cells in rows_of("tab:partB"):
        nm = name_of(cells[0])
        check("B", nm, "root base", cells[1], root_bound(root[(nm, "baseline")]))
        check("B", nm, "root diag", cells[2], root_bound(root[(nm, "all-diag")]))
        check("B", nm, "B2 base", cells[3], root_bound(b2[(nm, "baseline-noaggr")]))
        check("B", nm, "B2 diag", cells[4], root_bound(b2[(nm, "all-diag-noaggr")]))
        check("B", nm, "B2 extra", cells[5], root_bound(b2[(nm, "baseline-extra")]))
        fb, fa = full[(nm, "baseline")], full[(nm, "all")]
        check("B", nm, "full base", cells[6], ttime(fb), fb["status"])
        check("B", nm, "full all", cells[7], ttime(fa), fa["status"])
        check("B", nm, "cuts all", cells[8], str(len(fa.get("cuts") or [])))
        n += 1
    return n


def table_partD():
    root = {(r["name"], r["mode"]): r for r in load("v4/runs/partD-root")}
    full = {(r["name"], r["mode"]): r for r in load("v4/runs/partD-full")}
    cs = cases("v4/runs/partD-root")
    n = 0
    for cells in rows_of("tab:partD"):
        nm = name_of(cells[0])
        rp = cs[nm].get("reference_primal")
        if rp:
            check("D", nm, "best known", cells[1], float(rp))
        check("D", nm, "sense", cells[2], root[(nm, "baseline")]["sense"])
        check("D", nm, "root base", cells[3], root_bound(root[(nm, "baseline")]))
        check("D", nm, "root diag", cells[4], root_bound(root[(nm, "all-diag")]))
        check("D", nm, "root extra", cells[5], root_bound(root[(nm, "baseline-extra")]))
        check("D", nm, "cuts diag", cells[6], str(len(root[(nm, "all-diag")].get("cuts") or [])))
        for col, m in zip(cells[7:10], ["baseline", "all", "baseline-extra"]):
            r = full[(nm, m)]
            check("D", nm, "full " + m, col, r["dual"], r["status"])
        n += 1
    return n


def grp(name):
    nn = int(name.split("_n")[1].split("_")[0])
    s = int(name.split("_s")[-1])
    return nn, s


def table_path_detail():
    c3 = load("v3/runs/partC")
    c2 = load("v4/runs/partC2")
    v3d = load("v3d/runs/partC-rowdir")
    cs = cases("v3/runs/partC")
    ix = lambda recs, ph: {(r["name"], r["mode"]): r for r in recs if r["phase"] == ph}
    b, c2r, v3r = ix(c3, "root"), ix(c2, "root"), ix(v3d, "root")
    bf, c2f, v3f = ix(c3, "full"), ix(c2, "full"), ix(v3d, "full")
    byns = {grp(nm): nm for nm in cs}
    n = 0
    for cells in rows_of("tab:path-detail"):
        key = (int(cells[0]), int(cells[1]))
        nm = byns[key]
        zs = cs[nm]["known_optimum"]
        zb = root_bound(b[(nm, "baseline")])
        check("PD", key, "opt", cells[2], zs)
        check("PD", key, "base root", cells[3], zb)
        for col, (src, m) in zip(cells[4:10], [(c2r, "baseline-novarlocks"), (c2r, "baseline-extra"),
                                              (b, "all-diag-mech"), (c2r, "frozen-wide"),
                                              (v3r, "all-diag-mech"), (v3r, "all-diag-mech-wide")]):
            check("PD", key, m, col, gap_closed(root_bound(src[(nm, m)]), zb, zs, "min"))
        for col, (src, m) in zip(cells[10:14], [(bf, "baseline"), (c2f, "frozen-wide"),
                                               (v3f, "all-diag-mech-wide"), (c2f, "gurobi")]):
            r = src[(nm, m)]
            check("PD", key, "full " + m, col, ttime(r), r["status"])
        n += 1
    return n


def table_path_fresh():
    c3 = load("v4/runs/partC3")
    c4 = load("v4/runs/partC4")
    cs3, cs4 = cases("v4/runs/partC3"), cases("v4/runs/partC4")
    ix = lambda recs, ph: {(r["name"], r["mode"]): r for r in recs if r["phase"] == ph}
    rows = rows_of("tab:path-fresh")
    n = 0
    for k, cells in enumerate(rows):
        part = "C3" if k < 20 else "C4"
        recs, cs = (c3, cs3) if part == "C3" else (c4, cs4)
        rem = "all-diag-mech" if part == "C3" else "frozen-wide"
        r_, f_ = ix(recs, "root"), ix(recs, "full")
        byns = {grp(nm): nm for nm in cs}
        key = (int(cells[0]), int(cells[1]))
        nm = byns[key]
        zs = cs[nm]["known_optimum"]
        zb = root_bound(r_[(nm, "baseline")])
        check(part, key, "opt", cells[2], zs)
        if part == "C4":
            d = zs - cs[nm]["reference_bound_ii"]
            # exact zero up to bisection error -> printed as 0
            check(part, key, "opt-(ii)", cells[3], 0.0 if d < 1e-12 else d)
        check(part, key, "base root", cells[4], zb)
        for col, m in zip(cells[5:8], ["baseline-extra", rem, "rowdir-wide"]):
            check(part, key, m, col, gap_closed(root_bound(r_[(nm, m)]), zb, zs, "min"))
        for col, m in zip(cells[8:12], ["baseline", rem, "rowdir-wide", "gurobi"]):
            r = f_[(nm, m)]
            check(part, key, "full " + m, col, ttime(r), r["status"])
        n += 1
    return n


def extras():
    print("\nFurther checks")
    # distinct cuts over all parts: key = model sha + exact exported row
    parts = ["v3/runs/partA-full", "v3/runs/partA-root", "v3/runs/partB", "v3/runs/partC",
             "v3d/runs/partA-root-rowdir", "v3d/runs/partB-root-rowdir", "v3d/runs/partC-rowdir",
             "v4/runs/partB2", "v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4",
             "v4/runs/partD-root", "v4/runs/partD-full"]
    seen = set()
    seen_min = set()
    tot = 0
    for p in parts:
        for r in load(p):
            for c in r.get("cuts") or []:
                ex = (c.get("row_certificate") or {}).get("exact") or {}
                key = (r["model_sha256"], tuple(ex.get("coefficients") or []), json.dumps(ex.get("rhs")),
                       tuple(c.get("variables") or []))
                seen.add(key)
                if "partC" not in p:
                    seen_min.add(key)
                tot += 1
    print(f"  recorded cuts {tot}; distinct exact rows (model, coefficients, rhs, variables) {len(seen)}; "
          f"MINLPLib distinct {len(seen_min)}")

    # v3d full nodes, rowdir-wide
    v3d = load("v3d/runs/partC-rowdir")
    wide_full = [r for r in v3d if r["phase"] == "full" and r["mode"] == "all-diag-mech-wide"]
    print(f"  v3d wide full runs: nodes {sorted(r['nodes'] for r in wide_full)}; statuses "
          f"{Counter(r['status'] for r in wide_full)}")
    wide_root = [r for r in v3d if r["phase"] == "root" and r["mode"] == "all-diag-mech-wide"]
    print(f"  v3d wide root runs: statuses {Counter(r['status'] for r in wide_root)}")

    # minor separator productivity
    def productive(r, sep):
        ns = (r.get("native_statistics") or {}).get("separators") or {}
        s = ns.get(sep) or {}
        fc = s.get("FoundCuts")
        return isinstance(fc, int) and fc > 0

    for p in ["v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4"]:
        for ph in ["root", "full"]:
            recs = [r for r in load(p) if r["phase"] == ph and r["mode"] != "gurobi"]
            by = defaultdict(lambda: Counter())
            for r in recs:
                for sep in ["minor", "interminor", "eccuts", "rlt", "intersection"]:
                    by[r["mode"]][sep] += productive(r, sep)
            print(f"  {p} {ph}: productive runs per separator {dict((m, dict(v)) for m, v in by.items())}")
    # intersection cuts appear under nlhdlr statistics; list keys once
    r = [r for r in load("v4/runs/partC3") if r["mode"] == "baseline-extra" and r["phase"] == "root"][0]
    print("  native_statistics keys:", sorted((r.get("native_statistics") or {}).keys()))

    # Part A baseline seed pairs
    full = load("v3/runs/partA-full")
    by = {(r["name"], r["seed"], r["mode"]): r for r in full}
    names = sorted({r["name"] for r in full})
    for s1, s2 in [(0, 1), (0, 2), (1, 2)]:
        d = [n for n in names if cmp_bound(by[(n, s1, "baseline")]["dual"], by[(n, s2, "baseline")]["dual"],
                                            by[(n, s1, "baseline")]["sense"]) != 0]
        print(f"  Part A baseline seed {s1} vs {s2}: {len(d)} of 30 differ: {d}")

    # loads in C4
    c4 = load("v4/runs/partC4")
    ld = sorted(r["load_start"][0] for r in c4)
    print(f"  C4 load at start: deciles {[round(ld[int(q*(len(ld)-1))],2) for q in (0,0.1,0.5,0.9,1)]}; "
          f"runs with load > 9: {sum(1 for x in ld if x > 9)}")
    allc4 = []
    for p in ["v4/runs/partB2", "v4/runs/partC2", "v4/runs/partC3", "v4/runs/partC4", "v4/runs/partD-root", "v4/runs/partD-full"]:
        allc4 += [r["load_start"][0] for r in load(p) if r.get("load_start") and r["mode"] != "gurobi"]
    allc4.sort()
    print(f"  campaign 4 all runs load: min {allc4[0]:.2f} p5 {allc4[int(0.05*len(allc4))]:.2f} median "
          f"{statistics.median(allc4):.2f} p95 {allc4[int(0.95*len(allc4))]:.2f} max {allc4[-1]:.2f}")
    allc3 = []
    for p in ["v3/runs/partA-full", "v3/runs/partA-root", "v3/runs/partB", "v3/runs/partC"]:
        allc3 += [r["load_start"][0] for r in load(p)]
    allc3.sort()
    print(f"  campaign 3 (prospective) load: min {allc3[0]:.2f} median {statistics.median(allc3):.2f} max {allc3[-1]:.2f}")

    # Part D: 'all' mode stopped in discovery etc.
    dr = {(r["name"], r["mode"]): r for r in load("v4/runs/partD-root")}
    names = sorted({k[0] for k in dr})
    stop = [n for n in names if (dr[(n, "all")].get("separation") or {}).get("discovery_incomplete")]
    nocut = [n for n in names if n not in stop and not dr[(n, "all")].get("cuts")]
    print(f"  D root all: discovery stopped on {len(stop)}; completed without cut on {len(nocut)}: {nocut}")
    cuts_diag = [n for n in names if dr[(n, "all-diag")].get("cuts")]
    print(f"  D root all-diag: models with cuts {len(cuts_diag)}, cuts {sum(len(dr[(n,'all-diag')]['cuts']) for n in cuts_diag)}")
    cs = cases("v4/runs/partD-root")
    gc = []
    for n in names:
        rp = cs[n].get("reference_primal")
        if not rp:
            continue
        g = gap_closed(root_bound(dr[(n, "all-diag")]), root_bound(dr[(n, "baseline")]), float(rp), dr[(n, "baseline")]["sense"])
        c = cmp_bound(root_bound(dr[(n, "all-diag")]), root_bound(dr[(n, "baseline")]), dr[(n, "baseline")]["sense"])
        if c != 0:
            gc.append((n, c, round(g, 4) if g is not None else None))
    print(f"  D root all-diag vs baseline (better=1, worse=-1, gap closed): {gc}")

    # Part B models with cuts in auto
    full = [r for r in load("v3/runs/partB") if r["phase"] == "full"]
    for m in ["all", "auto"]:
        print(f"  Part B full {m}: models with cuts {len({r['name'] for r in full if r['mode']==m and r.get('cuts')})}")
    full = [r for r in load("v3/runs/partA-full")]
    for m in ["all", "auto"]:
        print(f"  Part A full {m}: models with cuts {len({r['name'] for r in full if r['mode']==m and r.get('cuts')})}")

    # path root bounds of full vs root runs (C4 'no root run reached')
    # campaign 3 v3d A/B root: anything changed vs v3 root?
    for a, b_ in [("v3/runs/partA-root", "v3d/runs/partA-root-rowdir"), ("v3/runs/partB", "v3d/runs/partB-root-rowdir")]:
        ra = {(r["name"], r["mode"]): r for r in load(a) if r["phase"] == "root"}
        rb = {(r["name"], r["mode"]): r for r in load(b_)}
        diff = [(k, root_bound(ra[k]), root_bound(rb[k])) for k in rb if k in ra and k[1] != "baseline"
                and cmp_bound(root_bound(ra[k]), root_bound(rb[k]), ra[k]["sense"]) != 0]
        print(f"  {b_} vs {a}: root-bound differences at 1e-4: {diff}")


def main():
    counts = {"A": table_partA(), "B": table_partB(), "D": table_partD(),
              "path-detail": table_path_detail(), "path-fresh": table_path_fresh()}
    print("rows checked:", counts)
    print(f"mismatches: {len(mism)}")
    for m in mism:
        print("  ", m)
    extras()


if __name__ == "__main__":
    main()
