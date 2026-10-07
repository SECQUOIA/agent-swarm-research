"""Print the best DP path of a saved state: cells, pair bounds, SCIP levels (exploration)."""
import pickle, sys
import numpy as np
from sepbranch import State  # noqa
st = pickle.load(open(sys.argv[1], "rb"))
V, f, g = st.dp()
path = st.best_path(f, g)
T = st.T
print("DP", V, "cells", [len(l) for l in st.leaves], "records", len(st.records))
for t in range(T):
    r = 0 if t == 0 else path[t - 1]
    c = 0 if t == T - 1 else path[t]
    rid = st.OWN[t][r, c]
    rec = st.records[rid] if rid >= 0 else None
    cin = st.cell_of(t - 1, r)
    cout = st.cell_of(t, c)
    fmt = lambda b: None if b is None else "[" + " ".join(f"{a:.3f}-{h:.3f}" for a, h in zip(b[0], b[1])) + "]"
    print(f"period {t}: B={st.B[t][r, c]:.4f} own={rid >= 0} in={fmt(cin)} out={fmt(cout)}")
    if rec:
        print("    est %.4f  s=%s e=%s status %s nodes %d t %.0fs" % (rec["est"], None if rec["s"] is None else np.round(rec["s"], 3),
              None if rec["e"] is None else np.round(rec["e"], 3), rec["status"], rec["nodes"], rec["t_rbb"]))
