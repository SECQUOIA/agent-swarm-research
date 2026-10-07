"""Referee rerun of a subset of the toy B&B (theory-face-exact/bb_path.py), with every node bound
cross-checked against an independent Clarabel QP (adversarial_boxes.Inst.LB).  Reports the leaf count of
bb_path's own run, the count when the independent bound decides pruning, and the number of nodes where
the two bounds differ by more than 1e-8 or where the pruning decision differs.
Only for the 'mc' relaxation (secant + McCormick), bisection.
Usage: python3 bb_crosscheck.py kappa cmode eps n1 n2 ...
"""
import sys
import numpy as np
sys.path.insert(0, "../../theory-face-exact")
import bb_path
from adversarial_boxes import Inst


def run(Ib, Im, eps, use):
    stack = [(Ib.lo.copy(), Ib.hi.copy())]
    leaves = nodes = mism = dec = 0
    maxdiff = 0.0
    while stack:
        l, u = stack.pop(); nodes += 1
        a = bb_path.relax(Ib, "mc", l, u)[0]
        b = Im.LB(l, u)
        d = a - b
        maxdiff = max(maxdiff, abs(d))
        if abs(d) > 1e-8: mism += 1
        if (a >= Ib.fstar - eps) != (b >= Ib.fstar - eps): dec += 1
        lb = a if use == "highs" else b
        if lb >= Ib.fstar - eps:
            leaves += 1; continue
        i = int(np.argmax(u - l)); p = 0.5 * (l[i] + u[i])
        u1 = u.copy(); u1[i] = p; l2 = l.copy(); l2[i] = p
        stack.append((l2, u)); stack.append((l, u1))
    return leaves, nodes, mism, dec, maxdiff


if __name__ == "__main__":
    kappa, cmode, eps = float(sys.argv[1]), sys.argv[2], float(sys.argv[3])
    for n in [int(a) for a in sys.argv[4:]]:
        Ib = bb_path.Inst(n, kappa, cmode)
        Im = Inst(n, [0.8] * (n - 1), kappa, Ib.c, eps, 1 - float(np.max(np.abs(Ib.xstar))) - 1e-6, "x")
        r1 = run(Ib, Im, eps, "highs")
        r2 = run(Ib, Im, eps, "clarabel")
        print(f"mc bisect kappa={kappa} {cmode} eps={eps:.0e} n={n}: leaves(bb_path bound)={r1[0]} "
              f"leaves(independent bound)={r2[0]}; nodes with |diff|>1e-8: {r1[2]}/{r1[1]}, "
              f"pruning decision differs: {r1[3]}, max |diff| = {r1[4]:.2e}", flush=True)
