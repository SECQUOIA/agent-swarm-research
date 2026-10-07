"""Negative and positive controls for the certifier as run here (MarginCertifier), eg_disc2_s.

1. As in the review's negative_control.py: boxes of relative size 1e-2..1e-8 around the exactly
   feasible primal point x* (integers fixed).  Targets theta = F(x*) + 1e-6 and F(x*) + 1e-9 must
   fail (x* is feasible with F(x*) < theta); theta = theta* - 1e-6 should certify the small boxes.
2. End to end on the recorded tree of part 1: every leaf of res/p1_c*.npz that contains x* must
   fail for theta = F(x*) + 1e-9 and was certified for theta* in the full run.
F(x*) = 5.6421005799711068 is the 50-digit value of the retry primal point (retry.md, Section 1)."""
import glob
import os
import sys
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from margin_cert import MarginCertifier  # noqa: E402

X = np.array([0.339986187975027, 1.0, 0.7526242429543005, 1.2370734367691458, 11, 34, 24], float)
FX, THS = Fr("5.6421005799711068"), Fr("5.642100574331458")

allgood = True
los, his = [], []
for delta in ("1e-6", "1e-9"):
    C = MarginCertifier("eg_disc2_s", FX + Fr(delta), max_depth=12)
    M = C.M
    los, his = [], []
    for rel in (1e-2, 1e-4, 1e-6, 1e-8):
        half = rel * (M.ub - M.lb)
        los.append(np.where(M.isint, X, np.maximum(X - half, M.lb)))
        his.append(np.where(M.isint, X, np.minimum(X + half, M.ub)))
    ok = C.certify_batch(np.array(los), np.array(his))
    allgood &= not ok.any()
    print(f"boxes around x*, theta = F(x*) + {delta}: certified {ok.tolist()} (must be all False); stats {C.stats}", flush=True)
C = MarginCertifier("eg_disc2_s", THS - Fr("1e-6"), max_depth=12)
ok = C.certify_batch(np.array(los), np.array(his))
print(f"boxes around x*, theta = theta* - 1e-6: certified {ok.tolist()} (positive control; review: [False, True, True, True])", flush=True)

files = sorted(glob.glob(os.path.join(HERE, "res", "p1_c*.npz")))
if files:
    lo = np.concatenate([np.load(f)["lo"] for f in files]); hi = np.concatenate([np.load(f)["hi"] for f in files])
    okf = np.concatenate([np.load(f)["ok"] for f in files])
    inside = np.where(np.all((lo <= X) & (X <= hi), axis=1))[0]
    print(f"part 1: {len(lo)} leaves, {len(inside)} contain x*; certified for theta* in the full run: {okf[inside].tolist()}")
    C = MarginCertifier("eg_disc2_s", FX + Fr("1e-9"), max_depth=12)
    ok = C.certify_batch(lo[inside], hi[inside])
    allgood &= len(inside) > 0 and not ok.any()
    print(f"   same leaves, theta = F(x*) + 1e-9: certified {ok.tolist()} (must be all False); stats {C.stats}")
else:
    print("part 1 results not present; end-to-end control skipped")
print("CONTROLS PASSED" if allgood else "CONTROL FAILED")
