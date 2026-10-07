"""Per-solver and per-instance summaries of results.json (written by audit.py classify).

One (instance, solver) pair is counted once, with the strongest class over its points:
(i) > (i-r) > (iii) > (ii) > (ii numerical); the margin is the largest proven margin.
Class (i) is split into gross errors (margin > 1e-6 of |d|) and tolerance-scale
exact-arithmetic violations (margin <= 1e-6 of |d|). Relative margins are (d - f)/|d|.

Usage: python3 summarize.py            -> summary.json and markdown tables on stdout
"""
import json
import math
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RANK = {"(i) proven invalid": 0, "(i-r) invalid as listed, within rounding of shown digits": 1,
        "(iii) undecided": 2, "(ii) tolerance effect (proven)": 3, "(ii) tolerance effect": 4,
        "(ii) tolerance effect (numerical)": 5}
SHORT = {"(i) proven invalid": "i", "(i-r) invalid as listed, within rounding of shown digits": "i-r",
         "(iii) undecided": "iii", "(ii) tolerance effect (proven)": "ii-proven", "(ii) tolerance effect": "ii",
         "(ii) tolerance effect (numerical)": "ii-num"}
BINS = [(0, 1e-9), (1e-9, 1e-7), (1e-7, 1e-5), (1e-5, 1e-3), (1e-3, 1e-1), (1e-1, math.inf)]


def binlabel(x):
    for a, b in BINS:
        if a <= x < b:
            return f"[{a:g},{b:g})"
    return "?"


def main():
    rows = json.load(open(os.path.join(HERE, "results.json")))
    flagged = [r for r in rows if r["cls"] in RANK]
    per = {}
    for r in flagged:
        k = (r["name"], r["solver"])
        cur = per.get(k)
        if cur is None or RANK[r["cls"]] < RANK[cur["cls"]] or (
                r["cls"] == cur["cls"] and r.get("margin_proved", -1) > cur.get("margin_proved", -1)):
            per[k] = r
    by_solver = defaultdict(Counter)
    mags = defaultdict(list)
    for (name, solver), r in per.items():
        key = SHORT[r["cls"]]
        if key == "i":
            key = "i-gross" if r["i_group"] == "gross" else "i-tol"
        by_solver[solver][key] += 1
        if SHORT[r["cls"]] in ("i", "i-r"):
            mags[solver].append(r["rel_margin"])
    out = dict(pairs=[dict(name=k[0], solver=k[1], cls=SHORT[v["cls"]], point=v["point"],
                           d=v["d_listed"], obj_hi=v.get("obj_hi"), obj_lo=v.get("obj_lo"),
                           margin=v.get("margin_proved"), rel_margin=v.get("rel_margin"),
                           solved=v["solved"], closing=v["closing"], d_slack=v["d_slack"])
                      for k, v in sorted(per.items())],
               by_solver={s: dict(c) for s, c in by_solver.items()},
               magnitudes={s: sorted(v) for s, v in mags.items()},
               other=Counter(r["cls"] for r in rows if r["cls"] not in RANK))
    json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
    print("| solver | pairs | (i) gross | (i) tolerance-scale | (i-r) | (ii) proven | (ii) repair | (iii) | margins of (i): absolute (relative to \\|d\\|) |")
    print("|---|---|---|---|---|---|---|---|---|")
    for s in sorted(by_solver):
        c = by_solver[s]
        ms = sorted(((r["rel_margin"], r["margin_proved"], n) for (n, so), r in per.items()
                     if so == s and SHORT[r["cls"]] == "i"), reverse=True)
        assert c["ii-num"] == 0
        print(f"| {s} | {sum(c.values())} | {c['i-gross']} | {c['i-tol']} | {c['i-r']} | {c['ii-proven']} | {c['ii']} | {c['iii']} | "
              + "; ".join(f"{n} {a:.3g} ({x:.2g})" for x, a, n in ms) + " |")
    print()
    hist = Counter(binlabel(r["rel_margin"]) for r in per.values() if SHORT[r["cls"]] == "i")
    print("magnitude histogram of (i), relative margin (d - f)/|d|:", dict(hist))
    print("other rows:", dict(out["other"]))
    print()
    print("solved instances with a bound proven invalid (closing = within 1e-6 relative of the best listed primal):")
    for (name, solver), r in sorted(per.items()):
        if r["solved"] and SHORT[r["cls"]] in ("i", "i-r"):
            print(f"  {name} {solver} d={r['d_listed']} class={SHORT[r['cls']]} margin={r['margin_proved']:.3g} "
                  f"rel={r['rel_margin']:.2g} closing={r['closing']} slack={r['d_slack']:.1g}")


if __name__ == "__main__":
    main()
