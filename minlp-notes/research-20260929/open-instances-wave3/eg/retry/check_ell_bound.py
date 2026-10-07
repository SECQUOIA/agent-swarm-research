"""Exact bound on ell = sum_i 2|gamma_ki| s_i |t_kmi| r_i (the argument of e^ell in the Taylor
remainders) over every box inside the root box, for every row k and term m.

A box centre c lies in the root box [lb, ub] and r_i <= (ub_i - lb_i)/2, so
    |t_kmi| = |mu_kmi + s_i c_i| <= max(|mu_kmi + s_i lb_i|, |mu_kmi + s_i ub_i|),
    ell_km <= sum_i |gamma_ki| s_i (ub_i - lb_i) max(...).
Computed in exact rational arithmetic from the decoded data (egdata.Data).  This justifies
that the former cap of egtm.iexp_up at 700 (in force when run B started) was never reached.

    python3 check_ell_bound.py
"""
from fractions import Fraction as Fr

import egdata

for name in ("eg_int_s", "eg_disc_s", "eg_disc2_s"):
    D = egdata.Data(name)
    best, arg = Fr(0), None
    tmax = gmax = Fr(0)
    for k in range(D.R):
        g = D.qga[k]
        gmax = max(gmax, max(abs(v) for v in g))
        for m in range(D.Mt):
            tot = Fr(0)
            for i in range(D.d):
                s, lb, ub = D.qs[i], D.qlb[i], D.qub[i]
                t = max(abs(D.qmu[k][m][i] + s * lb), abs(D.qmu[k][m][i] + s * ub))
                tmax = max(tmax, t)
                tot += abs(g[i]) * s * (ub - lb) * t
            if tot > best:
                best, arg = tot, (k + 1, m + 1)
    sr = max(D.qs[i] * (D.qub[i] - D.qlb[i]) / 2 for i in range(D.d))
    print(f"{name}: max over rows and terms of the ell bound = {float(best):.4f} (row e{arg[0]}, term {arg[1]}); "
          f"for comparison max|gamma| = {float(gmax):.4f}, max|t| = {float(tmax):.4f}, max s_i r_i = {float(sr):.4f}")
