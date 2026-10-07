"""Exact evaluation of points for waterno2_T (verifier's code).

Rows are evaluated directly from the parsed OSIL expression trees (osilx.ev_row
with Fraction arithmetic), not from the authors' polynomial conversion.
Point values are taken (a) as the exact rationals of their decimal strings and
(b) as the exact binary values of the corresponding doubles.

usage: python3 veval.py T file.json|file.sol [...]
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import sys, json
from fractions import Fraction as F
sys.path.insert(0, _RESEARCH + "/reviews/open-instances-verification")
import osilx

OSIL = _os.path.expanduser("~/.cache/minlplib/minlplib/osil/waterno2_{:02d}.osil")
FNS = {"power": lambda a, b: a ** int(b) if F(b).denominator == 1 else None}


def inf(s):
    return s.upper() in ("INF", "-INF", "+INF")


def evaluate(m, x, rows=None, vars_=None):
    obj = F(m["obj"]["constant"]) + sum(F(a) * x[j] for j, a in m["obj"]["lin"].items())
    worst, wrow = F(0), None
    idx = range(len(m["cons"])) if rows is None else rows
    for i in idx:
        c = m["cons"][i]
        s = osilx.ev_row(c, x, F, FNS)
        v = F(0)
        if not inf(c["lb"]):
            v = max(v, F(c["lb"]) - s)
        if not inf(c["ub"]):
            v = max(v, s - F(c["ub"]))
        if v > worst:
            worst, wrow = v, c["name"]
    bnd, bvar = F(0), None
    for j in (range(len(x)) if vars_ is None else vars_):
        v = F(0)
        if not inf(m["lb"][j]):
            v = max(v, F(m["lb"][j]) - x[j])
        if not inf(m["ub"][j]):
            v = max(v, x[j] - F(m["ub"][j]))
        if v > bnd:
            bnd, bvar = v, m["names"][j]
    ints = all(x[j] in (0, 1) for j in (range(len(x)) if vars_ is None else vars_) if m["vt"][j] == "B")
    return dict(obj=obj, maxrow=worst, row=wrow, maxbnd=bnd, bvar=bvar, int_ok=ints)


def read_point(path, names):
    if path.endswith(".json"):
        d = json.load(open(path))
        return [str(s) for s in d["x"]], d.get("obj")
    idx = {n: i for i, n in enumerate(names)}
    x = ["0"] * len(names)
    listed = None
    for line in open(path):
        p = line.split()
        if len(p) < 2:
            continue
        if p[0] == "objvar":
            listed = p[1]
        else:
            x[idx[p[0]]] = p[1]
    return x, listed


if __name__ == "__main__":
    T = int(sys.argv[1])
    m = osilx.read(OSIL.format(T))
    for path in sys.argv[2:]:
        xs, listed = read_point(path, m["names"])
        for mode in ("decimal", "double"):
            x = [F(s) if mode == "decimal" else F(float(s)) for s in xs]
            e = evaluate(m, x)
            print(f"{path.split('/')[-1]} [{mode}]: obj={float(e['obj']):.9f} (stored {listed}) "
                  f"max row viol={float(e['maxrow']):.3e} ({e['row']}) "
                  f"max bound viol={float(e['maxbnd']):.3e} ({e['bvar']}) binaries_integral={e['int_ok']}")
