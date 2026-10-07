"""Review check: the retry's primal points (retry/sol/*.retry.sol) and the listed MINLPLib p1
points (open-instances-wave3/sol/*.p1.sol), evaluated at 60 digits on the GAMS expression text
(gms_model.py; independent of osilx/ev.py).

For each point: bound and integrality violations, every row violation, objvar, and
F(x) = max over the objective rows of (rhs + S_k(x)) (the least feasible objvar).

    python3 check_primal.py
"""
import os
import sys
from fractions import Fraction as Fr

import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gms_model import GmsModel  # noqa: E402

W3 = os.path.join(HERE, "..", "..", "open-instances-wave3")
CLAIM_LB = {"eg_int_s": "6.4531031529331155", "eg_disc_s": "5.760539610694994",
            "eg_disc2_s": "5.642100574331458"}


def read_sol(path):
    vals = {}
    for line in open(path):
        p = line.split()
        if len(p) == 2:
            vals[p[0]] = p[1]
    return vals


def check(G, vals, label):
    mp.mp.dps = 60
    pt = {v: Fr(vals[v]) for v in G.vars}
    bviol = max(max(G.lb[v] - pt[v], pt[v] - G.ub[v], Fr(0)) for v in G.vars if v in G.lb)
    iviol = max((abs(pt[v] - round(pt[v])) for v in G.ints), default=Fr(0))
    worst, wname, F = mp.mpf(0), None, mp.mpf("-inf")
    for k, e in enumerate(G.eqs):
        v = G.violation(k, pt, 60)
        if v > worst:
            worst, wname = v, e["name"]
        if "objvar" in e["lhs"]:
            # lhs = -(S) + objvar >= rhs  ->  least objvar = rhs + S = rhs - (lhs - objvar)
            lhs = G.lhs(k, pt, 60)
            ov = mp.mpf(pt["objvar"].numerator) / pt["objvar"].denominator
            F = max(F, mp.mpf(e["rhs"].numerator) / e["rhs"].denominator - (lhs - ov))
    viols = {e["name"]: G.violation(k, pt, 60) for k, e in enumerate(G.eqs)}
    nz = {n: mp.nstr(v, 3) for n, v in viols.items() if v > 0}
    print(f"  {label}: objvar {vals['objvar']}; F(x) = {mp.nstr(F, 20)}; bound viol {float(bviol):.1e}; "
          f"int viol {float(iviol):.1e}; row violations {nz if nz else 'none'}")
    return F, viols


def main():
    for name in ("eg_int_s", "eg_disc_s", "eg_disc2_s"):
        G = GmsModel(name)
        print(name)
        Fr_, vr = check(G, read_sol(os.path.join(W3, "eg", "retry", "sol", f"{name}.retry.sol")), "retry point")
        Fp, vp = check(G, read_sol(os.path.join(W3, "sol", f"{name}.p1.sol")), "listed p1   ")
        lb = mp.mpf(CLAIM_LB[name])
        o = mp.mpf(read_sol(os.path.join(W3, "eg", "retry", "sol", f"{name}.retry.sol"))["objvar"])
        print(f"  claimed dual bound {CLAIM_LB[name]}: gap to retry objvar {mp.nstr(o - lb, 4)} "
              f"(rel {mp.nstr((o - lb) / o, 4)}); retry objvar - F(retry x) = {mp.nstr(o - Fr_, 3)}; "
              f"F(p1) - lb = {mp.nstr(Fp - lb, 4)}")


if __name__ == "__main__":
    main()
