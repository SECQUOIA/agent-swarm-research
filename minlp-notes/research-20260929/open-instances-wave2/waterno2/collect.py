"""Summary tables of certified bounds and primal values (reads logs/*.json).

Primal points from primal.py are re-evaluated exactly (evalpt.evaluate)."""
import json
import os
from fractions import Fraction

import wmodel
import evalpt

LISTED = {  # MINLPLib pages fetched 2026-09-29/30: best primal, best dual (solver)
    2: (39.57142193, 39.57142193, "SCIP"),
    3: (115.0045167, 115.0045167, "SCIP"),
    4: (145.4397918, 145.4397918, "SCIP"),
    6: (282.8880374, 165.1902989, "SCIP"),
    9: (922.5952898, 273.8958303, "SCIP"),
    12: (2263.358374, 479.5051427, "GUROBI"),
    18: (5269.638815, 770.7361733, "SCIP"),
    24: (7332.721691, 1095.126488, "SCIP"),
}


def gap(p, d):
    return abs(p - d) / min(abs(p), abs(d))


def main():
    print("| instance | listed primal | best listed dual (solver) | gap before | certified dual (ours) "
          "| best primal (ours or listed) | gap after | certification: max / total period time, nodes |")
    print("|---|---|---|---|---|---|---|---|")
    prim_rows = []
    for T in (6, 9, 12, 18, 24):
        f = f"logs/cert_{T:02d}_w1_impl.json"
        if not os.path.exists(f):
            continue
        d = json.load(open(f))
        v = Fraction(d["certified_bound_exact"])
        vd = Fraction(int(v * 10**6 // 1), 10**6)
        p, dl, sol = LISTED[T]
        prim, src = p, "listed"
        pf = f"logs/primal_{T:02d}_w2.json"
        if os.path.exists(pf) and T != 6:
            M = wmodel.load(T)
            x = [Fraction(s) for s in json.load(open(pf))["x"]]
            e = evalpt.evaluate(M, x)
            if float(e["obj"]) < p:
                prim, src = float(e["obj"]), "ours"
                prim_rows.append((T, float(e["obj"]), float(e["maxrow"]), e["worst_row"], float(e["maxbnd"]),
                                  e["int_ok"], p))
        rs = d["results"]
        print(f"| waterno2_{T:02d} | {p:.4f} | {dl:.4f} ({sol}) | {100*gap(p, dl):.1f}% | **{float(vd):.6f}** "
              f"| {prim:.4f} ({src}) | {100*gap(prim, float(v)):.2f}% | "
              f"{max(r['total_time'] for r in rs):.0f} s / {sum(r['total_time'] for r in rs):.0f} s, "
              f"{sum(r['nodes'] for r in rs)} |")
    print()
    print("| instance | our primal value (exact) | max abs. row violation (row) | max bound violation | "
          "binaries integral | listed primal |")
    print("|---|---|---|---|---|---|")
    for (T, obj, mr, wr, mb, ok, p) in prim_rows:
        print(f"| waterno2_{T:02d} | {obj:.9f} | {mr:.2e} ({wr}) | {mb:.2e} | {ok} | {p:.4f} |")


if __name__ == "__main__":
    main()
