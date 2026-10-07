"""Re-verify the leaves found by own_concavity.py (leaves.pkl) with the current own_psi.py:
coverage of the root box (containment, pairwise disjoint interiors, exact volume sum) and the
exact negative-definiteness test on every leaf."""
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
D = pickle.load(open(os.path.join(HERE, "leaves.pkl"), "rb"))
out = open(os.path.join(HERE, "logs", "verify_own_leaves.log"), "w")


def say(*a):
    s = " ".join(str(v) for v in a)
    print(s, flush=True)
    out.write(s + "\n")


lo0, hi0, L = D["lo0"], D["hi0"], D["leaves"]
keys = [(g, t) for g in P.GR for t in range(16)]
for lo, hi, _ in L:
    assert all(lo0[g][t] <= lo[g][t] <= hi[g][t] <= hi0[g][t] for g, t in keys)
split = [k for k in keys if any(lo[k[0]][k[1]] != lo0[k[0]][k[1]] or hi[k[0]][k[1]] != hi0[k[0]][k[1]] for lo, hi, _ in L)]
vol = sum(np.prod([Fr(float(hi[g][t])) - Fr(float(lo[g][t])) for g, t in split]) for lo, hi, _ in L)
vol0 = np.prod([Fr(float(hi0[g][t])) - Fr(float(lo0[g][t])) for g, t in split])
disj = all(any(L[i][1][g][t] <= L[j][0][g][t] or L[j][1][g][t] <= L[i][0][g][t] for g, t in split)
           for i in range(len(L)) for j in range(i + 1, len(L)))
say(f"{len(L)} leaves; split coordinates {[f'{g}_{t + 1}' for g, t in split]}; volume sum / root volume = {vol / vol0}; "
    f"disjoint interiors: {disj}")
assert vol == vol0 and disj
t0 = time.time()
allok = True
for i, (lo, hi, _) in enumerate(L):
    C, A, R = P.point_form(P.psi_af(lo, hi))
    ok, rho = P.exact_test(C, A, R)
    allok &= ok
    say(f"leaf {i + 1}: estimate {P.float_estimate(C, A, R):.5f}, exact test {ok}")
say(f"ALL LEAVES PASS: {allok} ({time.time() - t0:.0f} s)")
