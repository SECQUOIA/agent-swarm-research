"""Summary statistics of a plan / certification state (for the report)."""
import pickle, sys
import numpy as np
from dpcells import CellPlan  # noqa
P = pickle.load(open(sys.argv[1], "rb"))
T = P.T
print("leaves per link", [len(l) for l in P.leaves], "cells (tree nodes) per link", [len(c) for c in P.cells])
print("leaf pairs per period", [P.nrow(t) * P.ncol(t) for t in range(T)], "total", sum(P.nrow(t) * P.ncol(t) for t in range(T)))
et = [r["time"] for r in P.erecs]
print("SCIP estimates", len(P.erecs), "CPU %.0f s" % sum(et), "infeasible", sum(1 for r in P.erecs if r["est"] == np.inf),
      "status counts", {s: sum(1 for r in P.erecs if r["status"] == s) for s in set(r["status"] for r in P.erecs)})
if P.crecs:
    ct = [r["time"] for r in P.crecs]
    st = {}
    for r in P.crecs:
        st[r["status"]] = st.get(r["status"], 0) + 1
    print("rbb records", len(P.crecs), "CPU %.0f s" % sum(ct), "max %.1f s" % max(ct), "nodes", sum(r["nodes"] for r in P.crecs),
          "max nodes", max(r["nodes"] for r in P.crecs), "status", st,
          "below target", sum(1 for r in P.crecs if r["bound"] < r["target"]),
          "retries", sum(1 for r in P.crecs if r.get("retry")))
    V, f, g = P.dp("CB")
    path = P.best_path(f, g, "CB")
    print("certified DP (float) %.6f" % V)
    fmt = lambda b: None if b is None else " x ".join(f"[{a:.3f},{h:.3f}]" for a, h in zip(b[0], b[1]))
    for t in range(T):
        r = 0 if t == 0 else path[t - 1]
        c = 0 if t == T - 1 else path[t]
        rid = P.tables["CSRC"][t][r, c]
        print(f"  period {t}: bound {P.tables['CB'][t][r, c]:.4f} est {P.tables['EST'][t][r, c]:.4f} "
              f"exit cell {fmt(P.cell_box(t, P.leaf_id(t, c)))}")
    # widths of leaves
    for link in range(T - 1):
        w = np.array([[P.cells[link][cid]["hi"][k] - P.cells[link][cid]["lo"][k] for k in range(3)] for cid in P.leaves[link]])
        print(f"  link {link}: leaf widths min {w.min(axis=0).round(3)} median {np.median(w, axis=0).round(3)} max {w.max(axis=0).round(3)}")
