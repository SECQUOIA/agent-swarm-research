"""Reviewer r1: sep_ratio (stream code) with a 10x larger node cap (2e8) on the
two dense DM60 points, to see whether the capped result changes.
Usage: python3 reviews/r1-code/r1_dense_cap.py CAP file..."""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "code"))
from lattice import sep_ratio  # noqa: E402
cap = int(float(sys.argv[1]))
for p in sys.argv[2:]:
    Y = np.load(p)["Y"]; Y = (Y + Y.T) / 2
    r = sep_ratio(Y, max_nodes=cap)
    v = r["v"]
    print(json.dumps(dict(file=os.path.basename(p), cap=cap, ratio=r["ratio"], q=r["q"], iters=r["iters"], nodes=r["nodes"],
                          complete=bool(r["complete"]), time=r["time"],
                          supp=None if v is None else int(sum(1 for a in v[1:] if a)),
                          vmax=None if v is None else int(max(abs(int(a)) for a in v)))), flush=True)
