"""Summarize results/runs.jsonl: python3 analyze.py [runs.jsonl] > results/summary.md

For each (instance, setting):
  - processed nodes at each decade of eps ('>' = node/time limit hit,
    '*' = status optimal, i.e. the tree was exhausted);
  - tail slope: least squares of log10(nodes) on log10(1/eps) over the (up
    to) 5 smallest eps with eps <= 1e-3 that did not hit a limit;
  - wide slope: the same over all such runs with eps <= 1e-2;
  - nodes/decade: slope of nodes (not log nodes) on log10(1/eps) over the
    tail window (the rate for logarithmic growth).
Also: final leaves against the Theorem B bound (results/thm_bounds.json),
and numerical checks: primal - f* (negative = incumbent violates f(x) <= t
by up to the feasibility tolerance), dual - f* (a value above 1e-8 would be an
invalid lower bound), SoPlex tolerance warnings.
"""
import json
import math
import os
import sys
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from instances import INSTANCES  # noqa: E402

LIM = ("nodelimit", "timelimit")
ORDER = ["default", "nopresolve", "noprop", "nocutoffprop", "noweakdual", "obbtoff", "obbtall",
         "lppoint", "midpoint", "widestbisect", "model", "modelnoprop", "toy"]


def load(path):
    rows = defaultdict(dict)
    with open(path) as fh:
        for line in fh:
            r = json.loads(line)
            rows[(r["inst"], r["setting"])][r["eps"]] = r
    return rows


def good(runs, emax):
    return [(e, r) for e, r in sorted(runs.items(), reverse=True)
            if r["status"] not in LIM + ("error",) and e <= emax * 1.0001]


def lsq(pts, logy=True):
    if len(pts) < 3:
        return None
    x = np.log10(1 / np.array([e for e, _ in pts]))
    if np.ptp(x) < 0.99:
        return None
    y = np.array([r["nodes"] for _, r in pts], float)
    return float(np.polyfit(x, np.log10(y) if logy else y, 1)[0])


def leaves(r):
    return r.get("nodes_left", 0) + r.get("leaves_processed", 0)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "results", "runs.jsonl")
    rows = load(path)
    eps_all = sorted({e for runs in rows.values() for e in runs}, reverse=True)
    dec = [e for e in eps_all if abs(math.log10(e) - round(math.log10(e))) < 1e-9]
    fits = {}
    print("## Node counts and fitted slopes\n")
    print("| instance | pred. | setting | " + " | ".join(f"{e:.0e}" for e in dec)
          + " | tail slope | wide slope | nodes/decade |")
    print("|" + "---|" * (len(dec) + 6))
    for inst, d in INSTANCES.items():
        sets = sorted({s for (i, s) in rows if i == inst},
                      key=lambda s: ORDER.index(s) if s in ORDER else 99)
        for s in sets:
            runs = rows[(inst, s)]
            tail = good(runs, 1e-3)[-5:]
            wide = good(runs, 1e-2)
            ts, ws, lin = lsq(tail), lsq(wide), lsq(tail, logy=False)
            fits[f"{inst}|{s}"] = dict(tail=ts, wide=ws, nodes_per_decade=lin,
                                       tail_window=[tail[0][0], tail[-1][0]] if tail else None)
            cells = []
            for e in dec:
                r = runs.get(e)
                if r is None:
                    cells.append("")
                elif r["status"] in LIM:
                    cells.append(">" + str(r["nodes"]))
                elif r["status"] == "error":
                    cells.append("err")
                else:
                    cells.append(str(r["nodes"]) + ("*" if r["status"] == "optimal" else ""))
            p = d["pred"]
            ps = f"{p['slope']:g}" if p["kind"] == "power" else p["kind"]
            f2 = lambda v: "" if v is None else f"{v:.2f}"  # noqa: E731
            print(f"| {inst} | {ps} | {s} | " + " | ".join(cells)
                  + f" | {f2(ts)} | {f2(ws)} | {'' if lin is None else round(lin)} |")
    json.dump(fits, open(path.replace(".jsonl", "_fits.json"), "w"), indent=0)

    bpath = os.path.join(os.path.dirname(path), "thm_bounds.json")
    if os.path.exists(bpath):
        bounds = json.load(open(bpath))
        print("\n## Final leaves against the Theorem B lower bound\n")
        print("Ratio = (open nodes at termination + processed leaves) / bound; min and "
              "max over eps, and the ratio at the smallest eps without a limit.\n")
        print("| instance | setting | min ratio | max ratio | ratio at smallest eps | eps |")
        print("|---|---|---|---|---|---|")
        for inst, bd in bounds.items():
            for s in ORDER:
                runs = rows.get((inst, s))
                if not runs:
                    continue
                rat = [(e, leaves(r) / bd[repr(e)]) for e, r in sorted(runs.items(), reverse=True)
                       if r["status"] not in LIM + ("error",) and repr(e) in bd]
                if not rat:
                    continue
                vals = [v for _, v in rat]
                print(f"| {inst} | {s} | {min(vals):.2f} | {max(vals):.2f} | "
                      f"{rat[-1][1]:.2f} | {rat[-1][0]:.0e} |")

    print("\n## Numerical checks\n")
    print("| instance | setting | min(primal-f*) | max(dual-f*) | #optimal | "
          "limit at eps | max SoPlex warnings/run | min true f(sol)-f* |")
    print("|---|---|---|---|---|---|---|---|")
    for (inst, s), runs in sorted(rows.items()):
        rr = [r for r in runs.values() if r["status"] != "error"]
        la = min((e for e, r in runs.items() if r["status"] in LIM), default=None)
        tf = [r["sol_true_f_minus_fstar"] for r in rr if "sol_true_f_minus_fstar" in r]
        print(f"| {inst} | {s} | {min(r['primal_minus_fstar'] for r in rr):.1e} | "
              f"{max(r['dual_minus_fstar'] for r in rr):.1e} | "
              f"{sum(r['status'] == 'optimal' for r in rr)} | {'' if la is None else f'{la:.1e}'} | "
              f"{max(r.get('soplex_tol_warnings', 0) for r in rr)} | "
              f"{'' if not tf else f'{min(tf):.1e}'} |")


if __name__ == "__main__":
    main()
