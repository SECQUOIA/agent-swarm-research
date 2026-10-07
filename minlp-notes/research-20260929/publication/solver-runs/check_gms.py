#!/usr/bin/env python3
"""Record sha256 of each downloaded .gms file and check that it matches the
cached MINLPLib OSIL file in size.

Compared quantities: numbers of variables (total, continuous, binary, integer,
fixed), equations (total, =E=, =G=, =L=, =N=) and Jacobian nonzeros (total and
nonlinear), and the objective sense. The .gms values are the counts stated in
the file's header comment. The OSIL values are computed from the OSIL
structure (linear coefficients, quadratic terms and nonlinear expression
trees), not taken from a header.

MINLPLib OSIL files usually eliminate objvar and its defining row (objective
named "defObj_objvar"). In that case the .gms model must have exactly one more
variable, one more =E= row, and 1 + |objective variables| more nonzeros (the
objective-defining row holds objvar and every variable of the objective).
If the OSIL keeps a variable named objvar, the counts must agree directly.

usage: python3 check_gms.py            -> writes gms_manifest.csv / .json
"""
import csv
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
OSIL_DIR = Path.home() / ".cache/minlplib/minlplib/osil"


def expand(el):
    """Expand an OSIL <el mult= incr=> element into a list of numbers."""
    mult = int(el.get("mult", "1"))
    incr = el.get("incr")
    v = el.text.strip()
    if incr is None:
        return [v] * mult
    start, inc = int(v), int(incr)
    return [str(start + k * inc) for k in range(mult)]


def tag(e):
    return e.tag.rsplit("}", 1)[-1]


def osil_structure(path):
    vars_ = []          # (name, type, lb, ub)
    rows = []           # (lb, ub)
    obj = {"sense": None, "lin": set(), "name": None}
    lin_start, lin_idx, lin_val, lin_major = [], [], [], None
    nl_vars = {}        # row -> set of variable indices (row -1 = objective)
    section = None
    nl_row = None
    for ev, e in ET.iterparse(path, events=("start", "end")):
        t = tag(e)
        if ev == "start":
            if t in ("start", "colIdx", "rowIdx", "value"):
                section = t
            elif t == "nl":
                nl_row = int(e.get("idx"))
                nl_vars.setdefault(nl_row, set())
            elif t == "obj":
                obj["sense"] = e.get("maxOrMin", "min")
                obj["name"] = e.get("name")
            continue
        if t == "var":
            vars_.append((e.get("name"), e.get("type", "C"), e.get("lb", "0"), e.get("ub", "INF")))
        elif t == "con":
            rows.append((e.get("lb"), e.get("ub")))
        elif t == "coef":  # objective linear coefficient
            if float(e.text) != 0.0:
                obj["lin"].add(int(e.get("idx")))
        elif t == "el" and section is not None:
            vals = expand(e)
            if section == "start":
                lin_start += [int(x) for x in vals]
            elif section in ("colIdx", "rowIdx"):
                lin_major = "row" if section == "colIdx" else "col"
                lin_idx += [int(x) for x in vals]
            else:
                lin_val += [float(x) for x in vals]
        elif t in ("start", "colIdx", "rowIdx", "value"):
            section = None
        elif t == "qTerm":
            r = int(e.get("idx"))
            nl_vars.setdefault(r, set()).update({int(e.get("idxOne")), int(e.get("idxTwo"))})
        elif t == "variable" and nl_row is not None:
            nl_vars[nl_row].add(int(e.get("idx")))
        elif t == "nl":
            nl_row = None
        if t not in ("nl", "variables", "constraints", "osil", "instanceData"):
            e.clear()
    m = len(rows)
    lin = [set() for _ in range(m)]
    zero_coefs = 0
    if lin_start:
        for major in range(len(lin_start) - 1):
            for k in range(lin_start[major], lin_start[major + 1]):
                if lin_val[k] == 0.0:
                    zero_coefs += 1
                    continue
                if lin_major == "row":
                    lin[major].add(lin_idx[k])
                else:
                    lin[lin_idx[k]].add(major)
    nz = sum(len(lin[i] | nl_vars.get(i, set())) for i in range(m))
    nl = sum(len(nl_vars.get(i, set())) for i in range(m))
    obj_vars = obj["lin"] | nl_vars.get(-1, set())

    def rowtype(lb, ub):
        if lb is not None and ub is not None:
            return "E" if float(lb) == float(ub) else "R"
        if lb is not None:
            return "G"
        if ub is not None:
            return "L"
        return "N"

    rtypes = [rowtype(lb, ub) for lb, ub in rows]
    vt = [v[1] for v in vars_]
    fx = sum(1 for v in vars_ if v[2] == v[3])
    return {
        "vars": len(vars_), "cont": vt.count("C"), "binary": vt.count("B"), "integer": vt.count("I"),
        "fx": fx, "rows": m, "E": rtypes.count("E"), "G": rtypes.count("G"), "L": rtypes.count("L"),
        "N": rtypes.count("N"), "R": rtypes.count("R"), "nz": nz, "nl": nl,
        "obj_vars": len(obj_vars), "obj_nl_vars": len(nl_vars.get(-1, set())),
        "has_objvar": any(v[0] == "objvar" for v in vars_), "sense": obj["sense"],
        "obj_name": obj["name"], "zero_linear_coefs": zero_coefs,
    }


def gms_header(path):
    lines = []
    with open(path, errors="replace") as f:
        for _ in range(40):
            lines.append(f.readline())
    text = "".join(lines)

    def block(label, skip):
        for i, ln in enumerate(lines):
            if label in ln:
                names = lines[i + skip].lstrip("*").split()
                nums = [int(x) for x in lines[i + skip + 1].lstrip("*").split()]
                return dict(zip(names, nums))
        raise ValueError(f"{label} not found in {path}")

    eq = block("Equation counts", 1)
    var = block("Variable counts", 2)
    nzb = block("Nonzero counts", 1)
    fx = int(re.search(r"\*\s*FX\s+(\d+)", text).group(1))
    full = open(path, errors="replace").read()
    m = re.search(r"^Solve\s+m\s+using\s+%(\w+)%\s+(minimizing|maximizing)\s+objvar", full, re.M)
    return {
        "vars": var["Total"], "cont": var["cont"], "binary": var["binary"], "integer": var["integer"],
        "fx": fx, "rows": eq["Total"], "E": eq["E"], "G": eq["G"], "L": eq["L"], "N": eq["N"],
        "nz": nzb["Total"], "nl": nzb["NL"], "model_type": m.group(1),
        "sense": "min" if m.group(2) == "minimizing" else "max",
    }


def main():
    names = (HERE / "instances.txt").read_text().split()
    out = []
    for n in names:
        g = HERE / "gms" / f"{n}.gms"
        o = OSIL_DIR / f"{n}.osil"
        sha = hashlib.sha256(g.read_bytes()).hexdigest()
        osha = hashlib.sha256(o.read_bytes()).hexdigest()
        h = gms_header(g)
        s = osil_structure(o)
        # expected .gms counts implied by the OSIL
        exp = {k: s[k] for k in ("vars", "cont", "binary", "integer", "fx", "rows", "E", "G", "L", "N", "nz", "nl")}
        if not s["has_objvar"]:
            exp["vars"] += 1
            exp["cont"] += 1
            exp["rows"] += 1
            exp["E"] += 1
            exp["nz"] += 1 + s["obj_vars"]
            exp["nl"] += s["obj_nl_vars"]
        mism = [f"{k}: gms {h[k]} vs osil-implied {exp[k]}" for k in exp if h[k] != exp[k]]
        if s["R"]:
            mism.append(f"OSIL has {s['R']} ranged rows")
        if h["sense"] != s["sense"]:
            mism.append(f"sense: gms {h['sense']} vs osil {s['sense']}")
        row = {
            "instance": n, "gms_sha256": sha, "gms_bytes": g.stat().st_size,
            "osil_sha256": osha, "model_type": h["model_type"], "sense": h["sense"],
            "objvar_eliminated_in_osil": not s["has_objvar"],
            **{f"gms_{k}": h[k] for k in exp}, **{f"osil_{k}": s[k] for k in exp},
            **{f"osil_implied_{k}": exp[k] for k in exp},
            "osil_obj_vars": s["obj_vars"], "osil_zero_linear_coefs": s["zero_linear_coefs"],
            "match": not mism, "mismatches": "; ".join(mism),
        }
        out.append(row)
        print(f"{n:18s} {h['model_type']:5s} {h['sense']} vars {h['vars']:7d} rows {h['rows']:7d} "
              f"nz {h['nz']:8d} nl {h['nl']:8d}  {'OK' if not mism else 'MISMATCH: ' + row['mismatches']}",
              flush=True)
    with open(HERE / "gms_manifest.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    (HERE / "gms_manifest.json").write_text(json.dumps(out, indent=1) + "\n")
    bad = [r["instance"] for r in out if not r["match"]]
    print(f"{len(out)} files, {len(out) - len(bad)} match, mismatches: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
