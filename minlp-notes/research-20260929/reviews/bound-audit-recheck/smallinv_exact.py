"""Exact check of smallinvDAX points (own code).

Model (asserted): min objvar  s.t.  e1: x'Qx - objvar <= 0,  e2..e4 linear in the integer x,
x integer >= 0, objvar free.
Step 1 checks the listed point as it is, in exact rational arithmetic.
Step 2 keeps the listed integers and sets objvar := x'Qx exactly (the least feasible value),
then checks every row, bound and integrality condition exactly and evaluates the objective.

Usage: python3 smallinv_exact.py name.pK=listed_dual ...
"""
import os
import sys
from fractions import Fraction as F

import qosil
from sssd_exact import fmt, slack

HERE = os.path.dirname(os.path.abspath(__file__))


def main(arg):
    tag, _, d = arg.partition("=")
    name, pt = tag.rsplit(".", 1)
    M = qosil.Model(os.path.join(HERE, "data", name + ".osil"))
    xs, missing, unknown = qosil.read_sol(os.path.join(HERE, "data", f"{name}.{pt}.sol"), M)
    xs = [v if v is not None else F(0) for v in xs]
    ov = M.index["objvar"]
    assert M.sense == "min" and M.obj_lin == {ov: 1} and M.obj_const == 0 and not M.obj_Q
    assert M.type[ov] == "C" and M.lb[ov] is None and M.ub[ov] is None
    assert all(M.type[j] == "I" for j in range(M.n) if j != ov)
    (e1,) = [i for i in range(M.m) if M.Q[i]]
    assert M.A[e1] == {ov: F(-1)} and M.cub[e1] == 0 and M.clb[e1] is None and M.cconst[e1] == 0
    assert all(ov not in M.A[i] for i in range(M.m) if i != e1)
    print(f"{name}.{pt}: missing in .sol: {missing}; unknown names: {unknown}")
    print(f"  integer values integral: {all(xs[j].denominator == 1 for j in range(M.n) if j != ov)}; "
          f"listed objvar = {xs[ov]} ({fmt(xs[ov], 20)})")
    v0 = M.violations(xs)
    print(f"  listed point as is: {len(v0)} exact violations" + (f", largest {float(max(v for v, _, _ in v0)):.3g} "
          f"in {[(k, nm) for _, k, nm in v0]}" if v0 else "; objective = listed objvar = " + fmt(M.objective(xs), 20)))
    x = list(xs)
    x[ov] = F(0)
    x[ov] = M.row(e1, x)  # x'Qx, exact
    viol = M.violations(x)
    assert not viol, viol
    f = M.objective(x)
    print(f"  objvar := x'Qx: EXACTLY FEASIBLE, objective = {f} = {fmt(f, 20)} (listed objvar - x'Qx = {float(xs[ov] - f):.3g})")
    for label, pt_ in (("listed", xs), ("constructed", x)):
        if label == "listed" and v0:
            continue
        fv = M.objective(pt_)
        dd, sl = F(d), slack(d)
        m = dd - fv
        verdict = "INVALID (class (i))" if m > sl else ("within rounding slack (i-r)" if m > 0 else "not beyond d")
        print(f"  [{label}] listed dual d = {d}: d - f = {float(m):.6g}, (d - f)/|d| = {float(m / abs(dd)):.3g}, "
              f"slack {float(sl):.1g}, margin/slack = {float(m / sl):.4g}, margin/(unit in last digit) = "
              f"{float(m / (2 * sl)):.4g} -> {verdict}; {'gross' if m > abs(dd) / 10**6 else 'tolerance-scale'}")


if __name__ == "__main__":
    for a in sys.argv[1:]:
        main(a)
