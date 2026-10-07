"""Summarise the separation rerun (logs/sep_run2_s*.jsonl).

Groups: root points; final points of the de Meijer loop ('cut') and their
trace re-optimizations ('cut_trace') at open instances (logs/open_gap.txt);
the remaining non-root points ('near-closed-final'). Prints per group: rank range, the largest
violation of the {0,+-1} families with |supp w| = 1, 2, 3, the exact
normalised separator (ratio, violation, support, max |coefficient|,
completeness, time), the Gurobi box-K MIQP runs (violation found, status,
time), and Theorem 3 on the rational rank-r neighbour (q, digits of the
largest coefficient, value of that split at the floating-point point).
Usage: python3 summ_sep2.py [--rows]
"""
import glob
import json
import os
import statistics as st
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
open_ = set(open(os.path.join(ROOT, "logs/open_gap.txt")).read().split())
rows = []
for f in sorted(glob.glob(os.path.join(ROOT, "logs/sep_run2_s*.jsonl"))):
    rows += [json.loads(l) for l in open(f)]


def group(d):
    name, stage = d["file"].replace(".npz", "").split("__")[0], d["file"].replace(".npz", "").split("__")[-1]
    if stage == "root":
        return "root"
    return "open-final" if name in open_ else "near-closed-final"


def med(L):
    return st.median(L) if L else float("nan")


print(f"{len(rows)} points")
for g in ("root", "open-final", "near-closed-final"):
    R = [d for d in rows if group(d) == g]
    if not R:
        continue
    print(f"\n== {g}: {len(R)} points; rank@1e-5 {min(d['rank']['1e-05'] for d in R)}..{max(d['rank']['1e-05'] for d in R)}")
    for k in (1, 2, 3):
        v = [d[f"fam{k}"]["max_viol"] for d in R if f"fam{k}" in d]
        t = [d[f"fam{k}"]["time"] for d in R if f"fam{k}" in d]
        print(f"  fam{k}: max violation median {med(v):.3g}, max {max(v):.3g}, #>1e-3 {sum(x > 1e-3 for x in v)}/{len(v)}; time max {max(t):.2f}s")
    ra = [d["ratio"] for d in R]
    print(f"  exact normalised: ratio median {med([r['ratio'] for r in ra]):.3g}; violation median "
          f"{med([-r['q'] for r in ra if r['q'] is not None]):.3g}; supp {sorted(set(r['supp'] for r in ra if r['supp'] is not None))}; "
          f"vmax {sorted(set(r['vmax'] for r in ra if r['vmax'] is not None))}; incomplete {sum(not r['complete'] for r in ra)}; "
          f"time median {med([r['time'] for r in ra]):.2f}s max {max(r['time'] for r in ra):.2f}s")
    for K in (1, 3, 10):
        G = [d[f"grb{K}"] for d in R]
        qs = [-g["q"] for g in G if g["q"] is not None]
        print(f"  Gurobi K={K}: violation found median {med(qs):.4g} max {max(qs):.4g}; optimal {sum(g['status'].startswith('Optimal') for g in G)}/{len(G)}; "
              f"time median {med([g['time'] for g in G]):.1f}s; supp {sorted(set(g['supp'] for g in G if g['supp'] is not None))}")
    T = [d["thm3"] for d in R if "thm3" in d and "error" not in d["thm3"]]
    if T:
        q14 = sum(abs(t["q"] + 0.25) < 1e-9 for t in T)
        dig = [t["vmax_digits"] for t in T if t["q"] < 0]
        print(f"  Theorem 3 on rank-r neighbour: {len(T)} points, |q + 1/4| < 1e-9 in {q14}; coefficient digits median {med(dig):g} max {max(dig) if dig else '-'}; "
              f"recorded pre-lifting time median {med([t['time'] for t in T]):.2f}s max {max(t['time'] for t in T):.1f}s; rationalization error max {max(t['err'] for t in T):.1e}")
        bad = 0
        for t in T:
            qy = t["q_at_Y"]
            if qy is None:
                continue
            if isinstance(qy, str) or not (-0.25 - 1e-6 <= qy < 0):
                bad += 1
        print(f"    raw-point sanity check fails (value outside [-1/4 - 1e-6, 0)) in {bad}")
    E = [d["thm3"] for d in R if "thm3" in d and "error" in d["thm3"]]
    if E:
        big = sum("4300 digits" in e["error"] for e in E)
        print(f"  Theorem 3 records without a value: {len(E)}, of which {big} because an integer "
              f"exceeds Python's 4300-digit conversion limit; its role is not identified by the error record")

if "--rows" in sys.argv:
    print()
    for d in rows:
        r = d["ratio"]
        print(d["file"], d["rank"]["1e-05"], [round(d[f"fam{k}"]["max_viol"], 4) for k in (1, 2, 3) if f"fam{k}" in d],
              round(r["ratio"], 5), r["q"] and round(r["q"], 4), r["supp"], r["vmax"], r["complete"], round(r["time"], 2),
              [(d[f"grb{K}"]["q"] and round(d[f"grb{K}"]["q"], 5), d[f"grb{K}"]["status"][:4], round(d[f"grb{K}"]["time"], 1)) for K in (1, 3, 10)],
              d.get("thm3", {}).get("vmax_digits"), d.get("thm3", {}).get("q_at_Y"))
