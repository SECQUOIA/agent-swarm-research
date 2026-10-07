"""Assemble the rigorous Lagrangian dual bound and an own exactly feasible primal
point for ex6_2_7 / ex6_2_5 (mpmath iv, 50 digits).

bound = lambda.b + sum_p [ min(0, tmax * m_p) - max_i R_p,i / e ]
  m_p   : certified lower bound of min_y G_p(y) - lambda.y (gibbs_bb.py: -tau;
          ideal phase: closed form -ln sum_i exp(lambda_i - c))
  R_p   : exact scaling residual from gibbs_sym.py (>= 0 componentwise)
"""
import json
import os
import sys

import mpmath
from mpmath import iv

import common
import gibbs_sym

iv.dps = 50
mpmath.mp.dps = 50


def main(name, bb_logs):
    A = gibbs_sym.analyse(name, verbose=False)
    m = A["m"]
    b = [iv.mpf(v) for v in A["b"]]
    tmax = sum(mpmath.mpf(v) for v in A["b"])
    out = dict(name=name)
    # multipliers and B&B results (all B&B runs must use the same lambda strings)
    mp_ = {}
    lam_strs = None
    for ptype, path in bb_logs.items():
        r = json.load(open(path))
        assert r["ok"] and r["name"] == name and r["ptype"] == ptype
        lam_strs = lam_strs or r["lam"]
        assert r["lam"] == lam_strs
        mp_[ptype] = -iv.mpf(r["tau"])  # every fathomed box has bound >= -tau
        out["bb_type%d" % ptype] = dict(tau=r["tau"], nbox=r["nbox"], sec=r["sec"], ymin=r["ymin"])
    if lam_strs is None:
        lam_strs = json.load(open("logs/%s_kkt.json" % name))["lam"]
    lam = [iv.mpf(s) for s in lam_strs]
    types = {0: 0, 1: 0, 2: 0} if name == "ex6_2_7" else {0: 0, 1: 0, 2: 2}
    if name == "ex6_2_5":
        # ideal phase: G(y) = sum_i y_i (ln y_i + c) on the simplex; check the expression form
        G2 = A["G"][2]
        import sympy as sp
        y = A["y"]
        c = sp.Rational(".156969560191053")
        ideal = sum(y[i] * (sp.log(y[i] / (y[0] + y[1] + y[2])) + c) for i in range(3))
        assert sp.simplify(sp.expand_log(G2 - ideal, force=True)) == 0
        cI = iv.mpf(".156969560191053")
        mI = -iv.log(sum(iv.exp(lam[i] - cI) for i in range(3)))
        mp_[2] = mI
        out["ideal_min_closed_form"] = [mpmath.nstr(mI.a, 12), mpmath.nstr(mI.b, 12)]
    lb = sum(lam[i] * b[i] for i in range(3))
    out["lam"] = lam_strs
    out["lam_dot_b"] = mpmath.nstr(lb.a, 20)
    for slot, pt in types.items():
        R = A["R"][slot]
        maxR = max(iv.mpf(int(r.p)) / iv.mpf(int(r.q)) for r in R)
        assert all(r >= 0 for r in R)
        term = iv.mpf([min(0, mpmath.mpf(((b[0] + b[1] + b[2]) * mp_[pt]).a)), 0]) - maxR / iv.e
        lb = lb + term
    out["dual_bound"] = mpmath.nstr(mpmath.mpf(lb.a), 20)
    # own primal point: phases 0,1 from the KKT solution rounded to 20 digits, phase 2 = b - others
    kk = json.load(open("logs/%s_kkt.json" % name))
    nstr = [mpmath.nstr(mpmath.mpf(v), 20) for v in kk["n"]]
    from fractions import Fraction
    x = [None] * 9
    for i in range(3):
        a0, a1 = Fraction(nstr[3 * i]), Fraction(nstr[3 * i + 1])
        a2 = Fraction(A["b"][i]) - a0 - a1
        for p, v in enumerate((a0, a1, a2)):
            x[3 * i + p] = v
    for j in range(9):
        assert Fraction("1e-7") <= x[j] <= Fraction(m["ub"][j]), j
    for i in range(3):
        assert x[3 * i] + x[3 * i + 1] + x[3 * i + 2] == Fraction(A["b"][i])
    xi = [iv.mpf(int(v.numerator)) / iv.mpf(int(v.denominator)) for v in x]
    fI = common.obj_value(m, xi, common.ivnum, common.IVFNS)
    out["own_primal_point"] = [str(v) if v.denominator < 10 ** 30 else "%s/%s" % (v.numerator, v.denominator) for v in x]
    out["own_primal_objective_enclosure"] = [mpmath.nstr(mpmath.mpf(fI.a), 20), mpmath.nstr(mpmath.mpf(fI.b), 20)]
    out["gap_upper_primal_minus_bound"] = mpmath.nstr(mpmath.mpf(fI.b) - mpmath.mpf(lb.a), 5)
    # MINLPLib p1 (decimal values; rows checked exactly in rationals)
    sol = common.read_sol(os.path.join(common.HERE, "sol", "%s.p1.sol" % name))
    xs = [sol.get(nm, "0") for nm in m["names"]]
    xF = [Fraction(s) for s in xs]
    rowv = [abs(sum(Fraction(cf) * xF[j] for j, cf in row["lin"].items()) - Fraction(row["lb"])) for row in m["cons"]]
    fp = common.obj_value(m, [iv.mpf(s) for s in xs], common.ivnum, common.IVFNS)
    out["minlplib_p1"] = dict(objective=[mpmath.nstr(mpmath.mpf(fp.a), 16), mpmath.nstr(mpmath.mpf(fp.b), 16)],
                              max_row_violation=float(max(rowv)),
                              min_var=min(xs, key=lambda s: Fraction(s)))
    print(json.dumps(out, indent=1))
    json.dump(out, open("logs/%s_bound.json" % name, "w"), indent=1)


if __name__ == "__main__":
    name = sys.argv[1]
    logs = {}
    for a in sys.argv[2:]:
        k, v = a.split("=")
        logs[int(k)] = v
    main(name, logs)
