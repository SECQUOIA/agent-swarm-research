"""Longer enumeration on the largest hard instances of exp_hard.py.

Same X3C instances and seeds as exp_hard.py (q = 20, n = 60 and q = 25,
n = 75, planted and not, Theorem 1 matrices only), exact maximum-violation
separation by Schnorr-Euchner enumeration (sep_pd_float) with a node cap
NODES.  Usage: python3 exp_hard_long.py OUT.jsonl NODES
"""
import json
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exp_hard import x3c, has_cover, matrices  # noqa: E402
from lattice import sep_pd_float  # noqa: E402

if __name__ == "__main__":
    outp, cap = sys.argv[1], int(float(sys.argv[2]))
    with open(outp, "a") as out:
        for qq, nf in ((20, 3), (25, 3)):
            for planted in (True, False):
                seed = 1000 * qq + 10 * nf + planted
                rng = random.Random(seed)
                sets = x3c(qq, nf * qq, planted, rng)
                cover = has_cover(sets, qq)
                X, h2 = matrices(sets, qq)["thm1"]
                Xf = np.array([[float(a) for a in row] for row in X])
                r = sep_pd_float(Xf, max_nodes=cap)
                rec = dict(q=qq, n=len(sets), planted=planted, cover=cover, kind="thm1", cap=cap,
                           q_found=r["q"], nodes=r["nodes"], complete=bool(r["complete"]),
                           time=r["time"])
                out.write(json.dumps(rec) + "\n"); out.flush()
                print(rec, flush=True)
