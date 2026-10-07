"""Referee check 2: gadget root gaps for classes env (balanced, fixed), a/b2, b3, b4, b5, b6, b8 and
class-(a) core gaps gamma(theta), with the independent y-only column generation.
Usage: python3 check2_rootgaps.py > logs/check2_rootgaps.log"""
import numpy as np
from gadget_indep import Gadget, ClassBound

G = Gadget()
root = (-1, 1, -1, 1, -1, 1)
cb = ClassBound(G, d=1, c1=G.c / 2)
lo, up, it, fool = cb.bound(root)
print("env (balanced, c y^2 split 1/2:1/2, T={1,y}): gap in [%.6f, %.6f] (%d it)" % (-up, -lo, it))
for d in (2, 3, 4, 5, 6, 8, 10):
    cb = ClassBound(G, d=d)
    lo, up, it, fool = cb.bound(root)
    print("b%d: gap in [%.8f, %.8f] (%d it); fooling support sizes %d, %d, residual %.1e"
          % (d, -up, -lo, it, len(fool[0]), len(fool[2]), fool[4]))
    if d == 2:
        print("   b2 fooling: mu1 atoms", np.round(fool[0], 5), "w", np.round(fool[1], 5))
        print("               mu2 atoms", np.round(fool[2], 5), "w", np.round(fool[3], 5))
# check the base-split invariance for d >= 2: c y^2 in factor 2 instead of factor 1
cb = ClassBound(G, d=4, c1=0.0)
lo, up, it, _ = cb.bound(root)
print("b4 with c y^2 in factor 2: gap in [%.8f, %.8f]" % (-up, -lo))
# core gaps gamma(theta) for class a on K_theta, compare with authors' 0.006276, 0.02948, 0.076119
cb = ClassBound(G, d=2)
for th in (0.46, 0.5, 0.6, 0.8, 0.9, 1.0):
    lo, up, it, _ = cb.bound((-th, th, -th, th, -th, th))
    print("class a core theta=%.2f: gamma in [%.6f, %.6f]" % (th, -up, -lo))
# other reference parameter sets of the note's Section 6.5
for (y1, eta, ev, d) in [(0.38, 0.01, 0.005, 2), (0.38, 0.05, 0.1, 2), (0.38, 0.05, 0.2, 2),
                         (0.30, 0.005, 0.002, 4), (0.50, 0.005, 0.002, 6)]:
    Gx = Gadget(y1, eta, ev)
    lo, up, it, _ = ClassBound(Gx, d=d).bound(root)
    print("params (%.2f, %.3f, %.3f) class b%d root gap in [%.6f, %.6f]" % (y1, eta, ev, d, -up, -lo))
