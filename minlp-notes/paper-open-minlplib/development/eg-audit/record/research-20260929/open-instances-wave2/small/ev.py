"""High-precision evaluation of OSIL models and MINLPLib points.

Uses the verifier's reader `osilx.py` (decimal strings kept, objective and row
`constant` attributes read). This module adds the objective constant, which the
older `osil.py` reader ignores.

    python3 ev.py <name>.<pk> [...]     # evaluate sol/<name>.<pk>.sol at 50 digits
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import os
import sys

import mpmath as mp

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/reviews/open-instances-verification")
import osilx  # noqa: E402

OSIL = os.environ["MINLPLIB_OSIL_ROOT"]
HERE = os.path.dirname(os.path.abspath(__file__))

MPFNS = {"ln": mp.log, "log": mp.log, "exp": mp.exp, "cos": mp.cos, "sin": mp.sin,
         "sqrt": mp.sqrt, "power": lambda a, b: a ** b, "abs": abs}


def load(name):
    return osilx.read(os.path.join(OSIL, name + ".osil"))


def read_sol(path):
    vals = {}
    for line in open(path):
        p = line.split()
        if len(p) == 2:
            vals[p[0]] = p[1]
    return vals


def mpnum(s):
    return mp.mpf(s)


def objective(I, x):
    o = I["obj"]
    s = mp.mpf(o["constant"])
    for j, c in o["lin"].items():
        s += mp.mpf(c) * x[j]
    for i, j, c in o["quad"]:
        s += mp.mpf(c) * x[i] * x[j]
    if o["nl"] is not None:
        s += osilx.ev_tree(o["nl"], x, mpnum, MPFNS)
    return s


def evaluate(I, x, dps=50):
    """x: list of mpf (or strings). Returns dict with objective, max row and bound violations."""
    with mp.workdps(dps):
        x = [mp.mpf(v) for v in x]
        f = objective(I, x)
        worst, wrow = mp.mpf(0), None
        for r, c in enumerate(I["cons"]):
            v = osilx.ev_row(c, x, mpnum, MPFNS)
            viol = mp.mpf(0)
            if not osilx.isinf(c["lb"]):
                viol = max(viol, mp.mpf(c["lb"]) - v)
            if not osilx.isinf(c["ub"]):
                viol = max(viol, v - mp.mpf(c["ub"]))
            if viol > worst:
                worst, wrow = viol, c["name"]
        bworst, bvar = mp.mpf(0), None
        for j in range(len(x)):
            viol = mp.mpf(0)
            if not osilx.isinf(I["lb"][j]):
                viol = max(viol, mp.mpf(I["lb"][j]) - x[j])
            if not osilx.isinf(I["ub"][j]):
                viol = max(viol, x[j] - mp.mpf(I["ub"][j]))
            if viol > bworst:
                bworst, bvar = viol, I["names"][j]
        return dict(obj=f, row_viol=worst, worst_row=wrow, bound_viol=bworst, worst_var=bvar)


def eval_sol(tag, dps=50):
    name = tag.split(".")[0]
    I = load(name)
    vals = read_sol(os.path.join(HERE, "sol", tag + ".sol"))
    missing = [v for v in I["names"] if v not in vals]
    x = [vals.get(v, "0") for v in I["names"]]
    r = evaluate(I, x, dps)
    r["missing"] = len(missing)
    return r


if __name__ == "__main__":
    for tag in sys.argv[1:]:
        r = eval_sol(tag)
        print(f"{tag}: obj {mp.nstr(r['obj'], 20)}  max row viol {mp.nstr(r['row_viol'], 3)} ({r['worst_row']})"
              f"  max bound viol {mp.nstr(r['bound_viol'], 3)} ({r['worst_var']})  missing vars {r['missing']}")
