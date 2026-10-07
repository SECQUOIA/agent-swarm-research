"""Recheck Q3: is the lower end 2 max_e dist(Phi_e, Band_e) of Theorem 3.1
attained only in trivial cases (as the revised note says)?

Re-runs the note's T3 random three-bag chains (same seed, same LPs from the
note's check_tree.py) and counts cases where gap = max_e 2dist(Band_e) while
BOTH per-edge distances are positive (so the sum is strictly larger).

Run from a scratch copy of theory-consistency/: importing check_tree opens
logs/check_tree.log in write mode, which must not touch the author's files.
Usage: cd <scratch copy> && python3 <this file>
"""
import sys
import os
sys.path.insert(0, os.getcwd())
import numpy as np
from consistency_lib import cheb_basis
import check_tree as CT

rng = np.random.default_rng(0)
k = 5
s = np.linspace(-1, 1, k)
tot = att = att_both = 0
examples = []
for trial in range(300):
    a = rng.normal(size=k)
    c = rng.normal(size=k)
    b = rng.normal(size=(k, k))
    for deg in [0, 1, 2]:
        Bm = cheb_basis(s, deg)
        fs = CT.fstar(a, b, c)
        g = fs - CT.tree_rho(a, b, c, Bm, Bm)
        g1 = fs - CT.tree_rho(a, b, c, Bm, Bm, full2=True)
        g2 = fs - CT.tree_rho(a, b, c, Bm, Bm, full1=True)
        tot += 1
        if abs(g - max(g1, g2)) <= 1e-7:
            att += 1
            if min(g1, g2) > 1e-4:
                att_both += 1
                if len(examples) < 5:
                    examples.append((trial, deg, g, g1, g2))
print(f"{tot} cases; gap = max_e 2dist (to 1e-7) in {att}; "
      f"of these, both per-edge distances > 1e-4 (sum > max) in {att_both}")
for e in examples:
    print("  trial %d deg %d: gap=%.10f  2dist_1=%.10f  2dist_2=%.10f" % e)
