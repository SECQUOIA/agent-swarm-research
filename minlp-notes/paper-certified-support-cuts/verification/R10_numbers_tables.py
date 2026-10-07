#!/usr/bin/env python3
"""R10 (numbers lens): check every cell of the appendix tables in
sections/B-tables.tex (Tables partA, partB, partD, path-detail,
path-detail-full, path-fresh, path-fresh-full, star-detail, star-detail-full)
against the compact extracts of R10_numbers_extract.py and the case files.

A numeric cell matches if it equals the recomputed value within half a unit of
its last printed digit (relative 1e-9 slack). Times are compared with both
total_seconds and total_seconds + preparation_seconds; a cell passes if either
matches. Standard library only.

Usage: R10_numbers_tables.py <extract dir>
"""
import glob
import gzip
import json
import math
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.join(HERE, "..")
EXP = os.path.join(PAPER, "experiments")
EX = sys.argv[1]
TEX = open(os.path.join(PAPER, "sections", "B-tables.tex")).read()
_c = {}


def load(part):
    if part not in _c:
        path = os.path.join(EX, part.replace("/", "_") + ".jsonl")
        opener = open
        if not os.path.exists(path):
            path += ".gz"
            opener = gzip.open
        with opener(path, "rt") as fh:
            _c[part] = [json.loads(l) for l in fh]
    return _c[part]


def cases(part):
    out = {}
    for f in glob.glob(os.path.join(EXP, part, "cases", "*.json")):
        d = json.load(open(f))
        out[d["name"]] = d
    return out


def finite(x):
    return isinstance(x, (int, float)) and math.isfinite(x)


def root_bound(r):
    if finite(r.get("root_dual")):
        return r["root_dual"]
    if finite(r.get("dual")) and (r.get("node_limit") == 1 or (r.get("nodes") or 0) <= 1):
        return r["dual"]
    return None


def solved(r):
    pc = r.get("primal_check") or {}
    return (r.get("status") in ("optimal", "gaplimit") and (r.get("returncode") or 0) == 0
            and not r.get("worker_status") and pc.get("passed") is True)


def table_rows(label):
    i = TEX.index("\\label{tab:%s}" % label)
    j = TEX.index("\\midrule", i)
    k = TEX.index("\\bottomrule", j)
    body = TEX[j + len("\\midrule"):k]
    rows = []
    for line in body.split("\\\\"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("\\multicolumn") and "&" not in line:
            rows.append(("HDR", [line]))
            continue
        line = re.sub(r"\\(midrule|cmidrule\{[^}]*\})", "", line).strip()
        if not line:
            continue
        cells = [c.strip() for c in line.split("&")]
        if cells[0].startswith("\\multicolumn") and "Solved" in cells[0]:
            rows.append(("SOLVED", cells))
            continue
        rows.append(("ROW", cells))
    return rows


def num(cell):
    """Parse a numeric cell like $-1.376\\cdot10^{-13}$, $0.4318$, 36, $1$."""
    s = cell.replace("$", "").replace("\\textsuperscript{\\dag}", "").strip()
    m = re.fullmatch(r"(-?[0-9.]+)\\cdot10\^\{(-?[0-9]+)\}", s)
    if m:
        txt = m.group(1)
        dec = len(txt.split(".")[1]) if "." in txt else 0
        return float(txt) * 10 ** int(m.group(2)), 0.5 * 10 ** (int(m.group(2)) - dec)
    if re.fullmatch(r"-?[0-9]+(\.[0-9]+)?", s):
        dec = len(s.split(".")[1]) if "." in s else 0
        return float(s), 0.5 * 10 ** (-dec)
    return None


def status_time(cell):
    s = cell.replace("$", "").strip()
    if s.startswith("--"):
        return "process_timeout", None, None
    m = re.fullmatch(r"([ogt])\s+(.*)", s)
    if not m:
        return None, None, None
    v = num(m.group(2))
    return {"o": "optimal", "g": "gaplimit", "t": "timelimit"}[m.group(1)], v[0] if v else None, v[1] if v else None


class Checker:
    def __init__(self):
        self.n = 0
        self.bad = []

    def numcell(self, where, cell, *vals):
        p = num(cell)
        self.n += 1
        if p is None:
            if cell.strip() in ("", "--") and all(v is None for v in vals):
                return
            self.bad.append((where, cell, vals, "unparsed"))
            return
        x, half = p
        for v in vals:
            if v is None:
                continue
            if abs(v) >= 1000 and abs(x - round(v)) <= 0.5 + 1e-9:
                return
            if abs(x - v) <= half * (1 + 1e-9) + 1e-12:
                return
        self.bad.append((where, cell, vals))

    def stcell(self, where, cell, r, timefields=True, dual=False):
        self.n += 1
        st, x, half = status_time(cell)
        if r is None:
            if cell.strip():
                self.bad.append((where, cell, "no record"))
            return
        rst = r["status"]
        if st != rst:
            self.bad.append((where, cell, "status " + str(rst)))
            return
        if st == "process_timeout":
            return
        if dual:
            vals = [r.get("dual")]
        else:
            vals = [r.get("total_seconds"), (r.get("total_seconds") or 0) + (r.get("preparation_seconds") or 0)]
        for v in vals:
            if v is None:
                continue
            if abs(v) >= 1000 and abs(x - round(v)) <= 0.5 + 1e-9:
                return
            if abs(x - v) <= half * (1 + 1e-9) + 1e-12:
                return
        self.bad.append((where, cell, vals))

    def intcell(self, where, cell, v):
        self.n += 1
        try:
            if int(cell.strip()) == v:
                return
        except ValueError:
            pass
        self.bad.append((where, cell, v))


def model_name(cell):
    m = re.search(r"\\code\{([^}]*)\}", cell)
    return m.group(1).replace("\\_", "_") if m else None


def gap(z, zb, zs, sense="min"):
    s = 1.0 if sense == "min" else -1.0
    den = s * (zs - zb)
    return None if z is None or den <= 0 else s * (z - zb) / den


def main():
    C = Checker()
    # ---------------- Part A
    A = load("v3/runs/partA-full"); AR = load("v3/runs/partA-root")
    ia = {(r["name"], r["seed"], r["mode"]): r for r in A}
    ir = {(r["name"], r["mode"]): r for r in AR}
    for kind, cells in table_rows("partA"):
        nm = model_name(cells[0])
        w = "partA:" + nm
        C.numcell(w + ":root base", cells[1], root_bound(ir[(nm, "baseline")]))
        C.numcell(w + ":root all-diag", cells[2], root_bound(ir[(nm, "all-diag")]))
        C.intcell(w + ":cuts all-diag", cells[3], ir[(nm, "all-diag")]["n_cuts"])
        C.stcell(w + ":full base", cells[4], ia[(nm, 0, "baseline")])
        C.stcell(w + ":full all", cells[5], ia[(nm, 0, "all")])
        C.intcell(w + ":cuts all", cells[6], ia[(nm, 0, "all")]["n_cuts"])
    # ---------------- Part B / B2
    B = load("v3/runs/partB"); B2 = load("v4/runs/partB2")
    ib = {(r["name"], r["phase"], r["seed"], r["mode"]): r for r in B}
    i2 = {(r["name"], r["mode"]): r for r in B2}
    for kind, cells in table_rows("partB"):
        nm = model_name(cells[0]); w = "partB:" + nm
        C.numcell(w + ":3B root base", cells[1], root_bound(ib[(nm, "root", 0, "baseline")]))
        C.numcell(w + ":3B root all-diag", cells[2], root_bound(ib[(nm, "root", 0, "all-diag")]))
        C.numcell(w + ":4B2 base-noaggr", cells[3], root_bound(i2[(nm, "baseline-noaggr")]))
        C.numcell(w + ":4B2 all-diag-noaggr", cells[4], root_bound(i2[(nm, "all-diag-noaggr")]))
        C.numcell(w + ":4B2 extra", cells[5], root_bound(i2[(nm, "baseline-extra")]))
        C.stcell(w + ":full base", cells[6], ib[(nm, "full", 0, "baseline")])
        C.stcell(w + ":full all", cells[7], ib[(nm, "full", 0, "all")])
        C.intcell(w + ":cuts all", cells[8], ib[(nm, "full", 0, "all")]["n_cuts"])
    # ---------------- Part D
    DR = load("v4/runs/partD-root"); DF = load("v4/runs/partD-full")
    idr = {(r["name"], r["mode"]): r for r in DR}
    idf = {(r["name"], r["mode"]): r for r in DF}
    csd = cases("v4/runs/partD-root")
    for kind, cells in table_rows("partD"):
        nm = model_name(cells[0]); w = "partD:" + nm
        rp = csd[nm].get("reference_primal")
        C.numcell(w + ":best", cells[1], float(rp) if rp not in (None, "") else None)
        sense = idr[(nm, "baseline")].get("sense")
        if cells[2].strip() != sense:
            C.bad.append((w + ":sense", cells[2], sense))
        C.numcell(w + ":root base", cells[3], root_bound(idr[(nm, "baseline")]))
        C.numcell(w + ":root all-diag", cells[4], root_bound(idr[(nm, "all-diag")]))
        C.numcell(w + ":root extra", cells[5], root_bound(idr[(nm, "baseline-extra")]))
        C.intcell(w + ":cuts all-diag", cells[6], idr[(nm, "all-diag")]["n_cuts"])
        C.stcell(w + ":full base", cells[7], idf[(nm, "baseline")], dual=True)
        C.stcell(w + ":full all", cells[8], idf[(nm, "all")], dual=True)
        C.stcell(w + ":full extra", cells[9], idf[(nm, "baseline-extra")], dual=True)
    # ---------------- path seeds 0-4
    P3 = load("v3/runs/partC"); PP = load("v3d/runs/partC-rowdir"); C2 = load("v4/runs/partC2")
    i3 = {(r["name"], r["phase"], r["mode"]): r for r in P3}
    iP = {(r["name"], r["phase"], r["mode"]): r for r in PP}
    i2c = {(r["name"], r["phase"], r["mode"]): r for r in C2}
    cs3 = cases("v3/runs/partC")
    for kind, cells in table_rows("path-detail"):
        if not cells[0].strip().isdigit():
            continue
        n, s = int(cells[0]), int(cells[1]); nm = f"interleaved_path_n{n}_s{s}"; w = "path-detail:" + nm
        z = cs3[nm]["known_optimum"]; zb = root_bound(i3[(nm, "root", "baseline")])
        C.numcell(w + ":opt", cells[2], z)
        C.numcell(w + ":zb", cells[3], zb)
        for cell, idx, m, lab in ((cells[4], i2c, "baseline-novarlocks", "nolocks"), (cells[5], i2c, "baseline-extra", "extra"),
                                  (cells[6], i3, "all-diag-mech", "rem base"), (cells[7], i2c, "frozen-wide", "rem wide"),
                                  (cells[8], iP, "all-diag-mech", "row base"), (cells[9], iP, "all-diag-mech-wide", "row wide")):
            C.numcell(w + ":" + lab, cell, gap(root_bound(idx[(nm, "root", m)]), zb, z))
    cols = [(i3, "baseline"), (i2c, "baseline-novarlocks"), (i2c, "baseline-extra"), (i2c, "gurobi"),
            (i3, "all-diag-mech"), (i2c, "frozen-wide"), (iP, "all-diag-mech"), (iP, "all-diag-mech-wide")]
    names = []
    for kind, cells in table_rows("path-detail-full"):
        if kind == "SOLVED":
            for j, (idx, m) in enumerate(cols):
                C.intcell(f"path-detail-full:solved:{m}", cells[j + 1], sum(solved(idx[(x, "full", m)]) for x in names))
            continue
        if not cells[0].strip().isdigit():
            continue
        n, s = int(cells[0]), int(cells[1]); nm = f"interleaved_path_n{n}_s{s}"; names.append(nm)
        for j, (idx, m) in enumerate(cols):
            C.stcell(f"path-detail-full:{nm}:{m}", cells[2 + j], idx.get((nm, "full", m)))
    # ---------------- path seeds 5-9 (root)
    C3 = load("v4/runs/partC3"); C4 = load("v4/runs/partC4"); A5 = load("v5/runs/partC5a"); B5 = load("v5/runs/partC5b")
    iC3 = {(r["name"], r["phase"], r["mode"]): r for r in C3}
    iC4 = {(r["name"], r["phase"], r["mode"]): r for r in C4}
    iA = {(r["name"], r["phase"], r["mode"]): r for r in A5}
    iB = {(r["name"], r["phase"], r["mode"]): r for r in B5}
    cs4 = cases("v4/runs/partC3"); cs5 = cases("v5/runs/partC5b")
    block = None
    for kind, cells in table_rows("path-fresh"):
        if "Part 4C3" in cells[0]:
            block = "C3"; continue
        if "Part 4C4" in cells[0]:
            block = "C4"; continue
        if not cells[0].strip().isdigit():
            continue
        n, s = int(cells[0]), int(cells[1])
        if block == "C3":
            nm = f"interleaved_path_n{n}_s{s}"; idx = iC3; z = cs4[nm]["known_optimum"]
        else:
            nm = f"interleaved_path_coupled_n{n}_s{s}"; idx = iC4; z = cs5[nm]["known_optimum"]
        w = "path-fresh:" + nm
        zb = root_bound(idx[(nm, "root", "baseline")])
        C.numcell(w + ":opt", cells[2], z)
        if block == "C4":
            C.numcell(w + ":opt-closure", cells[3], (z - cs5[nm]["reference_bound_ii"]) * 1e4)
        elif cells[3].strip():
            C.bad.append((w + ":opt-closure", cells[3], "expected empty"))
        C.numcell(w + ":zb", cells[4], zb)
        C.numcell(w + ":nolocks", cells[5], gap(root_bound(iA[(nm, "root", "baseline-novarlocks")]), zb, z))
        C.numcell(w + ":extra", cells[6], gap(root_bound(idx[(nm, "root", "baseline-extra")]), zb, z))
        spec = [(7, idx, "all-diag-mech"), (8, idx, "frozen-wide"), (9, iB, "frozen-cap64"), (10, idx, "rowdir-wide"), (11, iB, "rowdir-cap64")]
        for col, ii, m in spec:
            r = ii.get((nm, "root", m))
            if r is None:
                if cells[col].strip():
                    C.bad.append((w + ":" + m, cells[col], "no record"))
                continue
            C.numcell(w + ":" + m, cells[col], gap(root_bound(r), zb, z))
        if block == "C4":
            bii = cs5[nm]["reference_bound_ii"]
            C.numcell(w + ":closure-root rem", cells[12], (bii - root_bound(iB[(nm, "root", "frozen-cap64")])) * 1e4)
            C.numcell(w + ":closure-root row", cells[13], (bii - root_bound(iB[(nm, "root", "rowdir-cap64")])) * 1e4)
    # path-fresh-full
    block = None; names = defaultdict(list)
    for kind, cells in table_rows("path-fresh-full"):
        if "Part 4C3" in cells[0]:
            block = "C3"; continue
        if "Part 4C4" in cells[0]:
            block = "C4"; continue
        idx = iC3 if block == "C3" else iC4
        cols = [(idx, "baseline"), (iA, "baseline-novarlocks"), (idx, "baseline-extra"), (idx, "gurobi"),
                (idx, "all-diag-mech"), (idx, "frozen-wide"), (idx, "rowdir-wide")]
        if kind == "SOLVED":
            for j, (ii, m) in enumerate(cols):
                rs = [ii.get((x, "full", m)) for x in names[block]]
                if all(r is None for r in rs):
                    continue
                C.intcell(f"path-fresh-full:{block}:solved:{m}", cells[j + 1], sum(solved(r) for r in rs if r))
            continue
        if not cells[0].strip().isdigit():
            continue
        n, s = int(cells[0]), int(cells[1])
        nm = f"interleaved_path_n{n}_s{s}" if block == "C3" else f"interleaved_path_coupled_n{n}_s{s}"
        names[block].append(nm)
        for j, (ii, m) in enumerate(cols):
            C.stcell(f"path-fresh-full:{nm}:{m}", cells[2 + j], ii.get((nm, "full", m)))
    # ---------------- stars
    S = load("v5/runs/partS5")
    iS = {(r["name"], r["phase"], r["mode"]): r for r in S}
    csS = cases("v5/runs/partS5")
    smodes = ["baseline", "baseline-novarlocks", "baseline-extra", "rowdir-star4", "agg-star4", "agg-star"]
    for kind, cells in table_rows("star-detail"):
        if not cells[0].strip().isdigit():
            continue
        k, n, s = int(cells[0]), int(cells[1]), int(cells[2]); nm = f"constrained_star_k{k}_n{n}_s{s}"
        z = csS[nm]["known_optimum"]
        C.numcell("star-detail:" + nm + ":opt", cells[3], z)
        for j, m in enumerate(smodes):
            zb = root_bound(iS[(nm, "root", m)])
            C.numcell(f"star-detail:{nm}:{m}", cells[4 + j], zb / z if zb is not None else None)
    fmodes = ["baseline", "baseline-novarlocks", "baseline-extra", "gurobi", "rowdir-star4", "agg-star4", "agg-star"]
    names = defaultdict(list); cur = None
    for kind, cells in table_rows("star-detail-full"):
        if kind == "SOLVED":
            lab = cells[0]
            ks = [4, 8, 16] if "total" in lab else [int(re.search(r"k=(\d+)", lab).group(1))]
            for j, m in enumerate(fmodes):
                cnt = sum(solved(iS[(x, "full", m)]) for kk in ks for x in names[kk])
                C.intcell(f"star-detail-full:solved {ks}:{m}", cells[j + 1], cnt)
            continue
        if not cells[0].strip().isdigit():
            continue
        k, n, s = int(cells[0]), int(cells[1]), int(cells[2]); nm = f"constrained_star_k{k}_n{n}_s{s}"
        names[k].append(nm)
        for j, m in enumerate(fmodes):
            C.stcell(f"star-detail-full:{nm}:{m}", cells[3 + j], iS[(nm, "full", m)])
    print(f"cells checked: {C.n}; mismatches: {len(C.bad)}")
    for b in C.bad:
        print("  MISMATCH", b)
    return bool(C.bad)


if __name__ == "__main__":
    sys.exit(main())
