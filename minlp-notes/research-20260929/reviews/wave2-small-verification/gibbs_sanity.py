"""Sanity checks of the Gibbs B&B machinery (not part of the proof).
1. For random boxes, the rigorous lower bound must not exceed D at sampled
   points of the box (D evaluated independently with mpmath from the OSIL tree).
2. With a perturbed lambda (lambda_1 + 1e-3) the tangent-plane function is
   negative somewhere, so the B&B must fail to certify min >= -1e-8.
"""
import json
import random
import sys

import mpmath

import common
import gibbs_bb

name = sys.argv[1]
kk = json.load(open("logs/%s_kkt.json" % name))
mpmath.mp.dps = 50
lam = [mpmath.nstr(mpmath.mpf(v), 20) for v in kk["lam"]]
ymin = "9.9e-8" if name == "ex6_2_7" else "9.9e-10"
gibbs_bb._worker_init(name, 0, lam, ymin, "1e-15")
m = common.load(name)
tree_terms = gibbs_bb.gibbs_sym.analyse(name, verbose=False)["parts"][0]


def D_point(y):
    mpmath.mp.dps = 40
    x = [mpmath.mpf(0)] * 9
    x[0], x[3], x[6] = y  # phase 0 variables
    val = sum(common.osilx.ev_tree(t, x, common.mpnum, common.MPFNS) for t in tree_terms)
    return val - sum(mpmath.mpf(lam[i]) * y[i] for i in range(3))


random.seed(7)
worst = mpmath.inf
viol = 0
for k in range(300):
    w = 10 ** random.uniform(-6, -1)
    a = random.uniform(1e-6, 0.95 - w); b = random.uniform(1e-6, 1 - a - w - 1e-6)
    box = (mpmath.mpf(a), mpmath.mpf(a + w * random.random()), mpmath.mpf(b), mpmath.mpf(b + w * random.random()))
    lb, how = gibbs_bb.lower(*box)
    for _ in range(3):
        y1 = box[0] + (box[1] - box[0]) * random.random(); y2 = box[2] + (box[3] - box[2]) * random.random()
        if y1 + y2 >= 1 - 1e-7:
            continue
        mpmath.mp.dps = 40
        d = D_point((mpmath.mpf(y1), mpmath.mpf(y2), 1 - mpmath.mpf(y1) - mpmath.mpf(y2)))
        worst = min(worst, d - lb)
        if d < lb:
            viol += 1
print("check 1: boxes 300, violations", viol, "smallest (D - lb)", mpmath.nstr(worst, 5))

# check 2: perturbed multipliers
lam_bad = list(lam)
lam_bad[0] = mpmath.nstr(mpmath.mpf(lam[0]) + mpmath.mpf("1e-3"), 20)
gibbs_bb._worker_init(name, 0, lam_bad, ymin, "1e-8")
r = gibbs_bb.solve_box((mpmath.mpf("0.25"), mpmath.mpf("0.375"), mpmath.mpf("0.375"), mpmath.mpf("0.5")) if name == "ex6_2_7"
                       else (mpmath.mpf("0.5"), mpmath.mpf("0.625"), mpmath.mpf("0.01"), mpmath.mpf("0.125")), budget=200000)
print("check 2 (perturbed lambda, box around a tangent point): ok =", r["ok"], r.get("reason"), "nbox", r["nbox"], "lb", r.get("lb"))
