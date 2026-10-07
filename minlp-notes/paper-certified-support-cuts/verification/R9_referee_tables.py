"""R9 referee lens: internal consistency of the path-family tables.

Parses Tables 11 and 12 (sections/B-tables.tex) as typeset and recomputes
the medians of Table 5 (sections/08e-path.tex), the glued pair-hull closure,
solved counts, and the numbers quoted in Section 8.5, the abstract and the
introduction. Read-only; no solver is run.
"""
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = (ROOT / "sections" / "B-tables.tex").read_text()


def num(s):
    s = s.strip().strip("$")
    if s in ("--", "-"):
        return None
    m = re.fullmatch(r"(-?[0-9.]+)\\cdot10\^\{(-?[0-9]+)\}", s)
    if m:
        return float(m.group(1)) * 10 ** int(m.group(2))
    return float(s)


def status(s):
    s = s.strip()
    st, val = s.split(" ", 1)
    return st, num(val)


def rows_between(start_marker, end_marker):
    i = TEX.index(start_marker)
    j = TEX.index(end_marker, i)
    out = []
    for line in TEX[i:j].splitlines():
        line = line.strip()
        if re.match(r"^(10|20|40|80) & [0-9] &", line):
            out.append([c.strip() for c in line.rstrip("\\").split("&")])
    return out


# Table 11 (seeds 0-4)
t11 = rows_between(r"\label{tab:path-detail}", r"\end{table}")
assert len(t11) == 20, len(t11)
cols11 = ["n", "seed", "opt", "zbase", "novarlocks", "extra", "rem_mech", "rem_wide",
          "row_mech", "row_wide", "full_base", "full_rem_wide", "full_row_wide", "full_gurobi"]
T11 = []
for r in t11:
    d = dict(zip(cols11, r))
    rec = {k: num(d[k]) for k in cols11[:10]}
    for k in cols11[10:]:
        rec[k] = status(d[k])
    T11.append(rec)

# Table 12 (seeds 5-9): C3 then C4
t12 = rows_between(r"\label{tab:path-fresh}", r"\end{table}")
assert len(t12) == 40, len(t12)
cols12 = ["n", "seed", "opt", "opt_minus_ii", "zbase", "extra", "rem", "row",
          "full_base", "full_rem", "full_row", "full_gurobi"]
T12 = []
for r in t12:
    d = dict(zip(cols12, r))
    rec = {k: num(d[k]) for k in cols12[:8]}
    for k in cols12[8:]:
        rec[k] = status(d[k])
    T12.append(rec)
C3, C4 = T12[:20], T12[20:]


def med_by_n(rows, key):
    out = []
    for n in (10, 20, 40, 80):
        out.append(statistics.median(r[key] for r in rows if r["n"] == n))
    return out


def solved(rows, key):
    return sum(1 for r in rows if r[key][0] in ("o", "g"))


def pair_closure(r):
    return (0 - r["zbase"]) / (r["opt"] - r["zbase"])


print("== Table 11 (seeds 0-4) medians per n, compare Table 5 rows ==")
for key in ("novarlocks", "extra", "rem_mech", "rem_wide", "row_mech", "row_wide"):
    print(f"{key:12s}", [round(v, 3) for v in med_by_n(T11, key)])
for r in T11:
    r["pair"] = pair_closure(r)
print("pair-hull   ", [round(v, 4) for v in med_by_n(T11, "pair")])
above = [(r["n"], int(r["seed"])) for r in T11 if r["rem_wide"] > r["pair"]]
print("remainder-wide above pair-hull level:", len(above), above)
print("solved (Table 11): base", solved(T11, "full_base"), "rem_wide", solved(T11, "full_rem_wide"),
      "row_wide", solved(T11, "full_row_wide"), "gurobi", solved(T11, "full_gurobi"))

print("\n== Table 12, C3 (seeds 5-9, non-binding) ==")
for key in ("extra", "rem", "row"):
    print(f"{key:6s}", [round(v, 3) for v in med_by_n(C3, key)])
for r in C3:
    r["pair"] = pair_closure(r)
print("pair  ", [round(v, 4) for v in med_by_n(C3, "pair")])
print("solved: base", solved(C3, "full_base"), "rem", solved(C3, "full_rem"),
      "row", solved(C3, "full_row"), "gurobi", solved(C3, "full_gurobi"))
print("whole-row full-run times:", min(r["full_row"][1] for r in C3), max(r["full_row"][1] for r in C3))

print("\n== Table 12, C4 (binding row) ==")
for key in ("extra", "rem", "row"):
    print(f"{key:6s}", [round(v, 4) for v in med_by_n(C4, key)])
print("solved: base", solved(C4, "full_base"), "rem", solved(C4, "full_rem"),
      "row", solved(C4, "full_row"), "gurobi", solved(C4, "full_gurobi"))
zeros = sum(1 for r in C4 if r["opt_minus_ii"] == 0)
print("opt-(ii)==0 on", zeros, "of 20; max", max(r["opt_minus_ii"] for r in C4))
times = [r[k][1] for r in C4 for k in ("full_rem", "full_row")]
print("cut-mode full-run times C4:", min(times), max(times))
print("whole-row distance to bound (ii) at n=80:")
for r in C4:
    if r["n"] == 80:
        root = r["zbase"] + r["row"] * (r["opt"] - r["zbase"])
        bound_ii = r["opt"] - r["opt_minus_ii"]
        print("  seed", int(r["seed"]), "dist", round(bound_ii - root, 4))
print("min whole-row closure over C3+C4:", min(r["row"] for r in C3 + C4))
# whether the remainder-direction separator went beyond pair-hull level in C4 is not
# defined (no pair-hull reference for C4); report remainder-wide C4 closure range
print("remainder-wide C4 closure range:", min(r["rem"] for r in C4), max(r["rem"] for r in C4))

print("\n== Headline counts (abstract/introduction) ==")
print("SCIP default solved on fresh 40:", solved(C3, "full_base") + solved(C4, "full_base"))
print("Gurobi solved on fresh 40:", solved(C3, "full_gurobi") + solved(C4, "full_gurobi"))
print("whole-row wide solved on fresh 40:", solved(C3, "full_row") + solved(C4, "full_row"))
print("NOTE: SCIP-extra full-run status is not in Tables 11-12; the '22' cannot be checked from the paper.")
