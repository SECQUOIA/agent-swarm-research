"""Independent check of split (invalid) boxes: each split box carries an LP primal solution, i.e. finitely
many weighted points per factor.  Recompute (i) weights >= 0 and summing to 1 per factor, (ii) the
consistency residuals of the class test functions between the two factors of every interior coordinate,
(iii) the value sum_e sum_k w_k f_e(p_k) with the base split, and check value < f* - eps.
Usage: python3 verify_split.py G CLS EPS"""
import sys
import numpy as np
from robust_bb import gadget_chain, bb, Relax, test_funcs

G, cls, eps = int(sys.argv[1]), sys.argv[2], float(sys.argv[3])
fam = gadget_chain(G)
rec = []
r = bb(fam, cls, eps, record_split=rec)
rel = Relax(fam, cls)
n = fam.n
worst_res = 0.0; worst_val = -np.inf; negw = 0.0; sumerr = 0.0
for (l, u, (pts, w), up) in rec:
    off = 0; W = []; P = []
    for e in range(n - 1):
        m = len(pts[e]); W.append(w[off:off + m]); P.append(pts[e]); off += m
    val = 0.0
    for e in range(n - 1):
        A, B, bb_ = rel.factor_parts(e)
        val += float(np.sum(W[e] * (A(P[e][:, 0]) + B(P[e][:, 1]) + bb_ * P[e][:, 0] * P[e][:, 1])))
        negw = min(negw, W[e].min()); sumerr = max(sumerr, abs(W[e].sum() - 1))
        assert np.all(P[e][:, 0] >= l[e] - 1e-12) and np.all(P[e][:, 0] <= u[e] + 1e-12)
        assert np.all(P[e][:, 1] >= l[e + 1] - 1e-12) and np.all(P[e][:, 1] <= u[e + 1] + 1e-12)
    for i in range(1, n - 1):
        for ph in test_funcs(cls, fam.u[i]):
            left = float(np.sum(W[i - 1] * ph(P[i - 1][:, 1]))); right = float(np.sum(W[i] * ph(P[i][:, 0])))
            worst_res = max(worst_res, abs(left - right))
    worst_val = max(worst_val, val - (-eps))
print("B&B:", r)
print("split boxes checked: %d; max consistency residual %.1e; min weight %.1e; max |sum w - 1| %.1e; "
      "max (fooling value - target) %.3e (negative = box certainly invalid)" % (len(rec), worst_res, negw, sumerr, worst_val))
