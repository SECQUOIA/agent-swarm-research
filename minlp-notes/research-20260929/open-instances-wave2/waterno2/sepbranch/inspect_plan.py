"""Best estimated DP path of a plan state (exploration)."""
import pickle, sys
import numpy as np
from dpcells import CellPlan  # noqa
P = pickle.load(open(sys.argv[1], "rb"))
name = sys.argv[2] if len(sys.argv) > 2 else "EST"
V, f, g = P.dp(name)
path = P.best_path(f, g, name)
T = P.T
print(name, V, [len(l) for l in P.leaves])
fmt = lambda b: None if b is None else "[" + " ".join(f"{a:.2f}-{h:.2f}" for a, h in zip(b[0], b[1])) + "]"
for t in range(T):
    r = 0 if t == 0 else path[t - 1]
    c = 0 if t == T - 1 else path[t]
    rid = P.tables["EOWN"][t][r, c]
    rec = P.erecs[rid] if rid >= 0 else None
    print(f"period {t}: {name} {P.tables[name][t][r, c]:.3f} in {fmt(P.cell_box(t - 1, P.leaf_id(t - 1, r)))} "
          f"out {fmt(P.cell_box(t, P.leaf_id(t, c)))}")
    if rec:
        print("     s", None if rec["s"] is None else np.round(rec["s"], 3), "e", None if rec["e"] is None else np.round(rec["e"], 3))
