"""Recheck the author's 9 leaf boxes with the reviewer's own affine forms and exact matrix test,
and check that the leaves cover the author's Theta (bisection tree: total volume and pairwise
disjoint interiors)."""
import os
import pickle
import sys
import time
from fractions import Fraction as Fr

os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import own_psi as P  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
AD = pickle.load(open(os.path.join(HERE, "author_data.pkl"), "rb"))
out = open(os.path.join(HERE, "logs", "author_leaves_check.log"), "w")


def say(*a):
    s = " ".join(str(v) for v in a)
    print(s, flush=True)
    out.write(s + "\n")


lo0, hi0 = AD["lo0"], AD["hi0"]
L = AD["LEAVES"]
# coverage: leaves inside the root, interiors pairwise disjoint, volumes (in the split coordinates) add up
keys = [(g, t) for g in P.GR for t in range(16) if hi0[g][t] > lo0[g][t]]
split_keys = [k for k in keys if any(lo[k[0]][k[1]] != lo0[k[0]][k[1]] or hi[k[0]][k[1]] != hi0[k[0]][k[1]] for lo, hi, _ in L)]
for lo, hi, _ in L:
    assert all(lo0[g][t] <= lo[g][t] <= hi[g][t] <= hi0[g][t] for g in P.GR for t in range(16))
vol = sum(np.prod([Fr(float(hi[g][t])) - Fr(float(lo[g][t])) for g, t in split_keys]) for lo, hi, _ in L)
vol0 = np.prod([Fr(float(hi0[g][t])) - Fr(float(lo0[g][t])) for g, t in split_keys])
disj = all(any(L[i][1][g][t] <= L[j][0][g][t] or L[j][1][g][t] <= L[i][0][g][t] for g, t in split_keys)
           for i in range(len(L)) for j in range(i + 1, len(L)))
say(f"author leaves: {len(L)}; split coordinates {[f'{g}_{t + 1}' for g, t in split_keys]}; "
    f"exact volume sum / root volume = {vol / vol0}; pairwise disjoint interiors: {disj}")
t0 = time.time()
for i, (lo, hi, est_a) in enumerate(L):
    H = P.psi_af(lo, hi)
    C, A, R = P.point_form(H)
    est = P.float_estimate(C, A, R)
    ok, rho = P.exact_test(C, A, R)
    say(f"leaf {i + 1}: author estimate {est_a:.5f}, own estimate {est:.5f}, own exact test: {ok}")
say(f"time {time.time() - t0:.0f} s")
