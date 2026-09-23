"""Compare modes on a MINLPLib sweep: solved counts, time and gap wins/losses, Markdown table.

Usage: analyze_minlplib.py results/minlplib_v3.jsonl [--table]
A run counts as solved if SCIP stopped by optimality or gap limit.  Gaps are measured against the
MINLPLib reference primal bound, so they do not depend on the run's own incumbent.
"""
import csv, json, math, sys
from collections import defaultdict

ref = {}
with open("../minlp_solver_lab/instances/instancedata.csv") as fh:
    for row in csv.DictReader(fh, delimiter=";"):
        try: ref[row["name"]] = float(row["primalbound"])
        except ValueError: pass
by = defaultdict(dict)
for l in open(sys.argv[1]):
    r = json.loads(l); by[r["instance"]][r["mode"]] = r
modes = ["native", "split", "hybrid"]

def solved(r): return r.get("status") in ("optimal", "gaplimit")
def refgap(r, name):
    """Relative distance between the run's dual bound and the reference optimum, capped at 1."""
    pb, d = ref.get(name), r.get("dual")
    if pb is None or d is None or abs(d) >= 1e19: return 1.0
    return min(1.0, abs(pb - d) / max(1e-9, abs(pb), abs(d)))
def sgm(xs, shift=1.0): return math.exp(sum(math.log(x + shift) for x in xs) / len(xs)) - shift

names = sorted(n for n in by if all(m in by[n] and by[n][m].get("status") != "error" for m in modes))
errors = sorted(n for n in by if n not in names)
print(f"instances with all three modes: {len(names)}; with an error or missing mode: {len(errors)} {errors}")
for m in modes:
    rs = [by[n][m] for n in names]
    print(f"- {m}: solved {sum(map(solved, rs))}/{len(names)}, shifted geometric mean time "
          f"{sgm([min(r['time'], r['tl']) if solved(r) else r['tl'] for r in rs]):.1f} s, "
          f"mean reference gap of unsolved-capped dual bounds {sum(refgap(r, n) for r, n in zip(rs, names)) / len(names):.3f}")
for other in ("split", "hybrid"):
    fast = slow = only_o = only_n = gap_better = gap_worse = same = 0
    detail = defaultdict(list)
    for n in names:
        a, b = by[n]["native"], by[n][other]
        if solved(a) and solved(b):
            ta, tb = max(a["time"], 1.0), max(b["time"], 1.0)
            if tb < ta / 2: fast += 1; detail["faster"].append(n)
            elif tb > ta * 2: slow += 1; detail["slower"].append(n)
            else: same += 1
        elif solved(b): only_o += 1; detail["only_" + other].append(n)
        elif solved(a): only_n += 1; detail["only_native"].append(n)
        else:
            ga, gb = refgap(a, n), refgap(b, n)
            if gb < ga - 0.02: gap_better += 1; detail["gap_better"].append(n)
            elif gb > ga + 0.02: gap_worse += 1; detail["gap_worse"].append(n)
            else: same += 1
    print(f"\n{other} vs native: solved only by {other} {only_o}, only by native {only_n}; both solved: >2x faster {fast}, "
          f">2x slower {slow}; neither solved: reference gap better by >0.02 {gap_better}, worse {gap_worse}; similar {same}")
    for k, v in detail.items(): print(f"  {k}: {', '.join(v)}")
if "--table" in sys.argv:
    print("\n| instance | used | native | split | hybrid |\n|---|---|---|---|---|")
    for n in names:
        cells = []
        for m in modes:
            r = by[n][m]
            cells.append(f"{r['time']:.1f} s ({r['nodes']})" if solved(r) else f"TL, ref. gap {100 * refgap(r, n):.1f}%")
        print(f"| {n} | {by[n]['hybrid'].get('collapsed', 0)} | " + " | ".join(cells) + " |")
