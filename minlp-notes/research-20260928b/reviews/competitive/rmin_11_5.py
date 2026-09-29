"""Exact instance on which R_min uses T = 11 nodes while N_opt = 3 (ratio 11/5).

alpha = 1, root [0,1], eps = 1/100, H = m + y^2 piecewise linear and convex.
Every processed node has a UNIQUE relaxation minimizer, so every R_min
implementation (any tie-breaking) builds this tree.  Found by
search_grid.py / worst_rmin.py as a tie instance and untied by lowering m at
3/16 and 13/16 by 1/10000.
"""
from fractions import Fraction as Fr

from exact1d import Inst, per_interval

xs = [Fr(s) for s in ['0', '1/16', '3/16', '7/16', '1/2', '9/16', '13/16', '15/16', '1']]
ms = [Fr(s) for s in ['41/1600', '41/1600', '33/800', '1/100', '1/100', '1/100', '33/800', '41/1600', '41/1600']]
ms[2] -= Fr(1, 10000)
ms[6] -= Fr(1, 10000)
I = Inst(xs, ms)
assert I.convex() and I.eps == Fr(1, 100)
S = I.greedy()
assert len(S) - 1 == 3 and len(I.rgreedy()) - 1 == 3


def pick(l, u, v, arg):
    assert len(arg) == 1, (l, u, arg)
    return arg[0]


internal = I.run(pick)
T = 2 * len(internal) + 1
print("m =", [str(m) for m in I.m])
print("left-greedy certificate:", [str(s) for s in S], " right-greedy:", [str(s) for s in I.rgreedy()])
for (l, u, s) in internal:
    print(f"  node [{l}, {u}]: value {I.node(l, u)[0]}, unique minimizer {s}")
cnt, at_bp = per_interval(S, internal)
print(f"T = {T}, N_opt = 3, ratio = {Fr(T, 5)}; splits per certificate interval {cnt}, at breakpoints {at_bp}")
assert T == 11
