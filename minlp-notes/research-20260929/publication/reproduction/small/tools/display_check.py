"""Check that the dual bounds displayed in open-instances-summary.md for ex6_2_7, ex6_2_5, etamac
and pricing050 are valid bounds, i.e. lie on the safe side of the exact interval end point that
the verifier's scripts compute.

The verifier's scripts print their bounds with mpmath.nstr(x, 20), which rounds to nearest, so
the printed string can lie on the wrong side of x by up to half a unit in the 20th digit. This
wrapper runs each script unchanged (runpy, in its own directory) with mpmath.nstr wrapped so
that the exact argument x of the call that produced the printed bound is recorded. It then
compares, in exact rational arithmetic, x with the summary's display string.

    cd <clean worktree>/research-20260929/reviews/wave2-small-verification
    python3 <this file>
"""
import json
import os
import runpy
import sys
from fractions import Fraction

import mpmath

HERE = os.getcwd()
sys.path.insert(0, HERE)
CALLS = []
_orig = mpmath.nstr


def _rec(x, n=6, *a, **k):
    s = _orig(x, n, *a, **k)
    CALLS.append((x, n, s))
    return s


mpmath.nstr = _rec


def exact(x):
    x = mpmath.mpf(x)
    man, exp = x.man_exp
    return Fraction(man) * (Fraction(2) ** exp)


def run(script, argv, json_path, key, display, sense):
    CALLS.clear()
    old = sys.argv
    sys.argv = [script] + argv
    try:
        runpy.run_path(script, run_name="__main__")
    finally:
        sys.argv = old
    d = json.load(open(json_path))
    for k in key:
        d = d[k]
    printed = d
    hits = [x for x, n, s in CALLS if s == printed and isinstance(x, mpmath.mpf)]
    assert hits, (script, printed)
    x = exact(hits[0])
    disp = Fraction(display.replace("−", "-"))
    pr = Fraction(printed)
    if sense == "lower":      # minimization: a valid displayed dual bound must be <= x
        ok_disp, ok_pr = disp <= x, pr <= x
    else:                     # maximization: a valid displayed upper bound must be >= x
        ok_disp, ok_pr = disp >= x, pr >= x
    return dict(script=script, printed=printed, exact_endpoint=_orig(mpmath.mpf(x.numerator) / x.denominator, 30),
                printed_minus_exact=float(pr - x), printed_is_valid=bool(ok_pr),
                summary_display=display, display_minus_exact=float(disp - x), display_is_valid=bool(ok_disp))


mpmath.mp.dps = 60
res = {}
res["ex6_2_7"] = run("gibbs_bound.py", ["ex6_2_7", "0=logs/ex6_2_7_bb_type0_tau6e-15.json"],
                     "logs/ex6_2_7_bound.json", ["dual_bound"], "-0.16084761546364905", "lower")
res["ex6_2_5"] = run("gibbs_bound.py", ["ex6_2_5", "0=logs/ex6_2_5_bb_type0_tau1e-17.json"],
                     "logs/ex6_2_5_bound.json", ["dual_bound"], "-70.75207783344770759", "lower")
res["etamac"] = run("v_etamac.py", [], "logs/etamac.json", ["bound", "dual_bound"], "-15.294675643368093", "lower")
res["pricing050"] = run("v_pricing050.py", [], "logs/pricing050.json", ["certificate", "upper_bound"],
                        "-1813.8290784519730577", "upper")
mpmath.nstr = _orig
print("DISPLAY CHECK RESULTS")
print(json.dumps(res, indent=1))
