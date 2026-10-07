"""R10 consistency check: summary tables versus per-instance appendix tables.

Parses Tables 12-17 (sections/B-tables.tex) and recomputes
- the medians and solved counts of Table 4 (path family) and Table 5 (stars),
- a few text statements of Sections 8.5 and 8.6 that are derived from them.
Read-only; prints mismatches. Run from any directory.
"""
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B = (ROOT / "sections" / "B-tables.tex").read_text()
PATH = (ROOT / "sections" / "08e-path.tex").read_text()
STAR = (ROOT / "sections" / "08f-star.tex").read_text()


def table(label):
    start = B.index(r"\label{%s}" % label)
    end = B.index(r"\end{tabular}", start)
    return B[start:end]


def num(cell):
    if isinstance(cell, (int, float)):
        return float(cell)
    cell = cell.strip().strip("$").replace(r"\,", "")
    m = re.fullmatch(r"(-?[\d.]+)\s*\\cdot\s*10\^\{(-?\d+)\}", cell)
    if m:
        return float(m.group(1)) * 10 ** int(m.group(2))
    try:
        return float(cell)
    except ValueError:
        return None


def rows(label):
    out = []
    for line in table(label).splitlines():
        line = line.strip()
        if not re.match(r"^\d", line) or "&" not in line:
            continue
        out.append([c.strip() for c in line.rstrip("\\").split("&")])
    return out


def blocks(label):
    """Split rows into blocks at \\multicolumn headers (Tables 14, 15)."""
    out, cur = [], []
    for line in table(label).splitlines():
        s = line.strip()
        if s.startswith(r"\multicolumn{") and "Part" in s and cur:
            out.append(cur)
            cur = []
        if re.match(r"^\d", s) and "&" in s:
            cur.append([c.strip() for c in s.rstrip("\\").split("&")])
    out.append(cur)
    return out


def med_by(rows_, key_idx, val_idx, keys):
    res = []
    for k in keys:
        vals = [num(r[val_idx]) for r in rows_ if int(r[key_idx]) == k and num(r[val_idx]) is not None]
        res.append(round(statistics.median(vals), 3) if vals else None)
    return res


def solved(rows_, idx):
    return sum(1 for r in rows_ if r[idx].strip().startswith(("o", "g")))


problems = []


def check(name, got, want, tol=0.0051):
    ok = all(
        (g is None and w is None) or (g is not None and w is not None and abs(g - w) <= tol)
        for g, w in zip(got, want)
    )
    print(("OK  " if ok else "DIFF"), name, "recomputed", got, "stated", want)
    if not ok:
        problems.append(name)


N = [10, 20, 40, 80]
# Table 12: n, seed, opt, zbase, nolocks, extra, rem-base, rem-wide, row-base, row-wide
t12 = rows("tab:path-detail")
glued = [[r[0], r[1], 0, 0, -num(r[3]) / (num(r[2]) - num(r[3]))] for r in t12]
check("T4 seeds0-4 SCIP-nolocks", med_by(t12, 0, 4, N), [0.95, 0.89, 0.93, 0.91])
check("T4 seeds0-4 SCIP-extra", med_by(t12, 0, 5, N), [0.64, 0.58, 0.66, 0.59])
check("T4 seeds0-4 glued", med_by(glued, 0, 4, N), [0.95, 0.89, 0.93, 0.92])
check("T4 seeds0-4 remainder base", med_by(t12, 0, 6, N), [0.35, 0.25, 0.19, 0.22])
check("T4 seeds0-4 remainder wide", med_by(t12, 0, 7, N), [0.86, 0.87, 0.89, 0.90])
check("T4 seeds0-4 whole row base", med_by(t12, 0, 8, N), [0.44, 0.44, 0.43, 0.46])
check("T4 seeds0-4 whole row wide", med_by(t12, 0, 9, N), [1.0, 1.0, 1.0, 1.0])
per_copy = [num(r[3]) / int(r[0]) for r in t12]
print("     3C SCIP root bound per copy: min %.4f max %.4f (text: -0.035 to -0.013)" % (min(per_copy), max(per_copy)))
nol_vs_glued = sum(1 for r, g in zip(t12, glued) if num(r[4]) < g[4])
print("     3C instances with SCIP-nolocks below the glued level: %d of 20 (text: every instance)" % nol_vs_glued)
above = sum(1 for r, g in zip(t12, glued) if num(r[7]) > g[4])
print("     4C2 remainder-wide above glued level: %d of 20 (text: 7)" % above)

# Table 13: n, seed, SCIP, nolocks, extra, gurobi, rem-base, rem-wide, row-base, row-wide
t13 = rows("tab:path-detail-full")
check("T4 seeds0-4 solved [SCIP,nolocks,extra,gurobi,rem-base,rem-wide,row-base,row-wide]",
      [solved(t13, i) for i in range(2, 10)], [9, 10, 10, 7, 9, 13, 10, 20], tol=0)

# Table 14: blocks 4C3 / 4C4
t14 = blocks("tab:path-fresh")
c3, c4 = t14[0], t14[1]
# 4C3 columns: n seed opt zbase nolocks extra rem-base row-wide (closure, wide, 64n empty)
def cells(r):
    return [c for c in r]
print("     4C3 row width", len(c3[0]), "4C4 row width", len(c4[0]))
# 4C3 rows: n, seed, opt, (empty closure), zbase, nolocks, extra, rem-base, (wide), (64n), row-wide, ...
def col(rs, i):
    return [[r[0], r[i]] for r in rs]
def medcol(rs, i):
    return med_by([[r[0], r[i]] for r in rs], 0, 1, N)
for name, rs in (("4C3", c3), ("4C4", c4)):
    print("    ", name, "first row:", rs[0])

check("T4 4C3 SCIP-nolocks", medcol(c3, 5), [0.92, 0.92, 0.92, 0.92])
check("T4 4C3 SCIP-extra", medcol(c3, 6), [0.57, 0.64, 0.61, 0.66])
check("T4 4C3 remainder base", medcol(c3, 7), [0.32, 0.31, 0.24, 0.20])
check("T4 4C3 whole row wide", medcol(c3, 10), [1.0, 1.0, 1.0, 1.0])
glued3 = [[r[0], -num(r[4]) / (num(r[2]) - num(r[4]))] for r in c3]
check("T4 4C3 glued", med_by(glued3, 0, 1, N), [0.93, 0.92, 0.93, 0.92])
check("T4 4C4 SCIP-nolocks", medcol(c4, 5), [0.980, 0.980, 0.972, 0.959], tol=0.0006)
check("T4 4C4 SCIP-extra", medcol(c4, 6), [0.287, 0.600, 0.685, 0.655], tol=0.0006)
check("T4 4C4 remainder wide", medcol(c4, 8), [0.983, 0.960, 0.954, 0.933], tol=0.0006)
check("T4 4C4 remainder 64n", medcol(c4, 9), [1.000, 0.999, 1.000, 0.999], tol=0.0006)
check("T4 4C4 whole row wide", medcol(c4, 10), [0.997, 0.989, 0.981, 0.982], tol=0.0006)
check("T4 4C4 whole row 64n", medcol(c4, 11), [1.000, 0.999, 1.000, 0.999], tol=0.0006)
allmed = [statistics.median(num(r[i]) for r in c4) for i in (8, 10)]
print("     4C4 overall root-gap medians remainder/whole row wide: %.4f / %.4f (text: 95%% and 99%%)" % tuple(allmed))
zero = sum(1 for r in c4 if num(r[3]) == 0)
print("     4C4 block closure equals optimum on %d of 20; max gap %.4g e-4 (text: 13; 6.5e-4)" % (zero, max(num(r[3]) for r in c4)))
print("     5C-b closure-root max: %.4g e-4 (text: within 8e-4)" % max(max(num(r[12]), num(r[13])) for r in c4))

# Table 15
t15 = blocks("tab:path-fresh-full")
f3, f4 = t15[0], t15[1]
print("     4C3 full first row:", f3[0])
print("     4C4 full first row:", f4[0])
check("T4 4C3 solved [SCIP,nolocks,extra,gurobi,rem-base,row-wide]",
      [solved(f3, i) for i in (2, 3, 4, 5, 6, 8)], [9, 10, 9, 5, 10, 20], tol=0)
check("T4 4C4 solved [SCIP,nolocks,extra,gurobi,rem-wide,row-wide]",
      [solved(f4, i) for i in (2, 3, 4, 5, 7, 8)], [10, 20, 13, 6, 20, 20], tol=0)

# Table 16/17 stars: k, n, seed, opt, SCIP, nolocks, extra, row4, agg4, stars
t16 = rows("tab:star-detail")
K = [4, 8, 16]
check("T5 SCIP", med_by(t16, 0, 4, K), [0.954, 0.815, 0.655], tol=0.0006)
check("T5 SCIP-nolocks", med_by(t16, 0, 5, K), [0.526, 0.580, 0.547], tol=0.0006)
check("T5 SCIP-extra", med_by(t16, 0, 6, K), [0.943, 0.858, 0.738], tol=0.0006)
check("T5 whole row <=4", med_by(t16, 0, 7, K), [0.956, 0.821, 0.651], tol=0.0006)
check("T5 block <=4", med_by(t16, 0, 8, K), [0.963, 0.834, 0.664], tol=0.0006)
check("T5 stars", med_by(t16, 0, 9, K), [1.0, 1.0, 1.0], tol=0.0006)
t17 = rows("tab:star-detail-full")
for i, (name, want) in enumerate(
    [("SCIP", 10), ("SCIP-nolocks", 15), ("SCIP-extra", 13), ("Gurobi", 22),
     ("whole row <=4", 12), ("block <=4", 14), ("stars", 19)], start=3):
    got = solved(t17, i)
    print(("OK  " if got == want else "DIFF"), "T5 solved", name, got, want)
    if got != want:
        problems.append("T5 solved " + name)
dag = sum(r.count(r"\dag") for r in map(" ".join, t17))
print("     process_timeout marks in Table 17:", dag, "(text: eight)")

print("\nproblems:", problems if problems else "none")
