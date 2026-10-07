"""Confirm-r1 check: exact bound on ell = sum_i 2|gamma_i| s_i |t_i| r_i over all boxes inside the
root box, from the GAMS text via the review's independent reader (no egdata/eg_model code).
For a box with centre c in [lb, ub] and radius r_i <= (ub_i - lb_i)/2:
  |t_i| = |mu_i + s_i c_i| <= max(|mu_i + s_i lb_i|, |mu_i + s_i ub_i|)."""
import os, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "eg-retry-review-checks"))
import gms_model

for name in ("eg_int_s", "eg_disc_s", "eg_disc2_s"):
    G = gms_model.GmsModel(name)
    T = G.terms()
    best, arg, tmax, nterms = Fr(0), None, Fr(0), 0
    for e in T:
        for j, (a, fac) in enumerate(e["terms"]):
            nterms += 1
            tot = Fr(0)
            for v, (sc, mu, g) in fac.items():
                lb, ub = G.lb[v], G.ub[v]
                t = max(abs(mu + sc * lb), abs(mu + sc * ub))
                tmax = max(tmax, t)
                tot += 2 * abs(g) * sc * t * (ub - lb) / 2
            if tot > best:
                best, arg = tot, (e["name"], j + 1)
    print(f"{name}: terms {nterms}, max ell bound {float(best):.6f} at {arg}, max |t| {float(tmax):.4f}")
