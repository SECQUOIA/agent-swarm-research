#!/usr/bin/env python3
"""Reviewer check of results_table.md (paper table) against re-extracted values (mine_pd.json, compare.json)."""
import collections
import json
from decimal import Decimal as D
from pathlib import Path

HERE = Path(__file__).resolve().parent
M = json.load(open(HERE / "mine_pd.json"))
C = {x["key"]: x for x in json.load(open(HERE / "compare.json"))}
E = {f"{r['instance']}__{r['solver']}": r for r in json.load(open(HERE / "extract.json"))}
rows = [l for l in open(HERE.parent.parent / "solver-runs" / "results_table.md")
        if l.startswith("| ") and not l.startswith("| Instance")]


def close(a, b):  # 12 significant digits in the Markdown table
    if a == "—":
        return b is None
    if b is None or a in ("Infinity", "-Infinity"):
        return a == b
    b = D(str(b))
    return b.is_finite() and abs(D(a) - b) <= abs(b) * D("1e-11")


bad, closes, status = [], collections.Counter(), collections.Counter()
for l in rows:
    inst, s, st, t, P, Dd, gap, cl, _ = [x.strip() for x in l.strip().strip("|").split("|")]
    k = f"{inst}__{s}"
    if not close(P, M[k]["P"]):
        bad.append(("P", k))
    if not close(Dd, M[k]["D"]):
        bad.append(("D", k))
    if not close(gap, C[k]["deficit"]):
        bad.append(("C-D", k))
    tt = E[k]["tr_time"]
    if not ((t == "—" and tt in (None, "NA")) or (tt not in (None, "NA") and D(t) == D(tt))):
        bad.append(("time", k))
    closes[cl] += 1
    status[(s, st)] += 1
print(len(rows), "rows; mismatches:", bad)
print("Closes column:", dict(closes))
for k, v in sorted(status.items()):
    print(" ", k, v)
