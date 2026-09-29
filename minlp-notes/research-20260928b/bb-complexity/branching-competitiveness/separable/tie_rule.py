"""Dependence on the minimizer selection (revision after the review).
For each family and eps: omega and deficit leaves and OPT_min leaves under the selection "knot"
(minimizing knots/endpoints only; all pre-review runs) and "proj" (centre projected onto the
whole minimizer set, flat segments included).  usage: python3 tie_rule.py FAMILY KMIN KMAX"""
import sys
from fractions import Fraction as Fr
from sepexact import Coord, run, opt_min
from exp1 import family
from exp5 import dyadic_caps

name, kmin, kmax = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
for k in range(kmin, kmax + 1):
    eps = Fr(1, 10 ** k)
    out = []
    for sel in ("knot", "proj"):
        Coord.sel = sel
        cs = [dyadic_caps(30), dyadic_caps(30)] if name == "dyadic_caps" else list(family(name, eps))
        ro, rd = run(cs, eps, "omega"), run(cs, eps, "deficit")
        om = opt_min(cs[0], cs[1], eps, cap=3_000_000)
        out.append(f"{sel}: omega {ro['leaves']}, deficit {rd['leaves']}, OPT_min {om}"
                   + (f", omega/OPT_min {ro['leaves'] / om:.3f}" if om else ""))
    print(f"{name} eps=1e-{k}: " + " | ".join(out), flush=True)
