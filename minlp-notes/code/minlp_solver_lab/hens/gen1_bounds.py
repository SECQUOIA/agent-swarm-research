"""Task 1(c): infimum bounds for heatexch_gen1 when process-exchanger areas can be driven to ~0.

c1  : drop the process LMTD+area equations (e65-e80); process areas x97.. only bounded >= 0.
      This is a relaxation of the original, so opt(c1) <= inf(original).
c1m : c1 with dt lower bounds raised from 10 to 10+3e-6 (the near-singular construction needs
      approach >= 10 + 2(eps+delta) at the ends of active exchangers); opt(c1m) >= inf(original) - o(1).
c2  : drop all LMTD+area equations (e65-e88): pure 'fixed cost + utility' bound.
"""
import sys
from common import *

T = float(sys.argv[1]) if len(sys.argv) > 1 else 600
out = {}
for case in ["c1", "c1m", "c2"]:
    m = load_minlplib("heatexch_gen1")
    last = 80 if case.startswith("c1") else 88
    for i in range(65, last + 1):
        getattr(m, f"e{i}").deactivate()
    if case == "c1m":
        for v in m.component_data_objects(pe.Var):
            if v.lb == 10 and v.ub is None:
                v.setlb(10 + 3e-6)
    res, t = solve_gams(m, "baron", T, threads=4, optcr=1e-6, extra=["option optca=1e-3;"],
                        keepfiles=True, tmpdir=str(RES / f"gen1_bounds_{case}"))
    p, l = gams_bounds(res)
    b = {v.name: round(pe.value(v)) for v in m.component_data_objects(pe.Var) if v.is_binary()}
    util = {n: pe.value(getattr(m, n)) for n in ("x33", "x34", "x35", "x36")}
    uarea = {n: pe.value(getattr(m, n)) for n in ("x109", "x110", "x111", "x112")}
    out[case] = {"primal": p, "dual": l, "time": t, "term": str(res.solver.termination_condition),
                 "n_units": sum(b.values()), "binaries": b, "utilities": util, "utility_areas": uarea}
    print(case, out[case], flush=True)
dump("gen1_bounds.json", out)
