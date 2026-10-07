"""Table of the KAN results (reads ../logs/<name>.result.json and the scout's fetched.csv)."""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
names = ["kan_r3_h1_n4", "kan_r3_h1_n5", "kan_r3_h1_n9", "kan_r5_h1_n3", "kan_r5_h1_n5", "kan_r5_h1_n8"]
listed = {}
with open(os.path.join(HERE, "..", "..", "open-instances-scout", "fetched.csv")) as f:
    for r in csv.DictReader(f):
        listed[r["name"]] = r
print("| instance | listed primal | best listed dual | our dual bound | our primal (60-digit) | gap | B&B boxes | time s | done |")
print("|---|---|---|---|---|---|---|---|---|")
for n in names:
    p = os.path.join(HERE, "..", "logs", f"{n}.result.json")
    if not os.path.exists(p):
        print(f"| {n} | {listed[n]['best_primal']} | {listed[n]['best_dual']} ({listed[n]['best_dual_solver']}) | (not run) | | | | | |")
        continue
    r = json.load(open(p))
    gap = float(r["primal_obj"]) - r["dual_bound"]
    print(f"| {n} | {listed[n]['best_primal']} | {listed[n]['best_dual']} ({listed[n]['best_dual_solver']}) | {r['dual_bound']:.13g} | "
          f"{r['primal_obj'][:18]} (viol {r['primal_row_viol']}) | {gap:.2e} | {r['processed']} | {r['time']:.0f} | {r['done']} |")
