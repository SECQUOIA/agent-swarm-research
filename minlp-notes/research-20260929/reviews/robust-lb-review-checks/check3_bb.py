"""Referee check 3: leaf counts of widest-side bisection with exact class bounds on gadget chains, delta = 0,
using the product identity LB_S(chain box) = sum_g V_S(gadget box) (valid for delta = 0 with the base split
that keeps all unary terms in the gadget factors, i.e. the base split of Theorem 4.2).
Usage: python3 check3_bb.py d eps G1 G2 ...   (d = 2 is class a / a0 / b2 for this gadget)"""
import sys, time
from gadget_indep import Gadget, ClassBound, bb_product

d, eps = int(sys.argv[1]), float(sys.argv[2])
cb = ClassBound(Gadget(), d=d)
for G in map(int, sys.argv[3:]):
    t0 = time.time()
    r = bb_product(cb, G, eps)
    print("class d=%d eps=%g G=%d n=%d: %s  (%.1fs)" % (d, eps, G, 3 * G, r, time.time() - t0), flush=True)
