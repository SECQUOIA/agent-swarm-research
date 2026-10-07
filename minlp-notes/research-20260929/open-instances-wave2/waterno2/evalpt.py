"""Exact evaluation of a point for waterno2_T.

All rows are polynomials with decimal coefficients, so a point given by
decimal strings is evaluated exactly in rational arithmetic (Fraction).
Reports the objective, the maximum row violation and the maximum bound
violation, both exact (printed as floats), and binary integrality.

usage: python3 evalpt.py T file.sol|file.json
"""
import sys
import json
from fractions import Fraction

import wmodel


def read_sol(path, names):
    """MINLPLib .sol: lines 'name value'; missing variables are 0."""
    idx = {n: i for i, n in enumerate(names)}
    x = [Fraction(0)] * len(names)
    obj = None
    for line in open(path):
        p = line.split()
        if len(p) < 2:
            continue
        if p[0] == "objvar":
            obj = Fraction(p[1])
            continue
        x[idx[p[0]]] = Fraction(p[1])
    return x, obj


def evaluate(M, x):
    """Return dict(obj, maxrow, maxbnd, worst_row, int_ok); x is a list of Fractions."""
    obj = sum(Fraction(a) * x[j] for j, a in M["obj"].items())
    worst, wrow = Fraction(0), None
    for r in M["rows"]:
        s = Fraction(0)
        for mono, a in r["poly"].items():
            t = Fraction(a)
            for v in mono:
                t *= x[v]
            s += t
        viol = Fraction(0)
        if not osil_inf(r["lb"]):
            viol = max(viol, Fraction(r["lb"]) - s)
        if not osil_inf(r["ub"]):
            viol = max(viol, s - Fraction(r["ub"]))
        if viol > worst:
            worst, wrow = viol, r["name"]
    bnd = Fraction(0)
    for j in range(len(x)):
        if not osil_inf(M["lb"][j]):
            bnd = max(bnd, Fraction(M["lb"][j]) - x[j])
        if not osil_inf(M["ub"][j]):
            bnd = max(bnd, x[j] - Fraction(M["ub"][j]))
    int_ok = all(x[j] in (0, 1) for j in range(len(x)) if M["vt"][j] == "B")
    return dict(obj=obj, maxrow=worst, worst_row=wrow, maxbnd=bnd, int_ok=int_ok)


def osil_inf(s):
    return s.upper() in ("INF", "-INF", "+INF")


if __name__ == "__main__":
    T = int(sys.argv[1])
    M = wmodel.load(T)
    for path in sys.argv[2:]:
        if path.endswith(".json"):
            d = json.load(open(path))
            x = [Fraction(s) for s in d["x"]]
            listed = None
        else:
            x, listed = read_sol(path, M["names"])
        e = evaluate(M, x)
        print(f"{path}: obj={float(e['obj']):.12f} (listed {float(listed) if listed is not None else '-'})"
              f" max row viol={float(e['maxrow']):.3e} ({e['worst_row']})"
              f" max bound viol={float(e['maxbnd']):.3e} binaries_ok={e['int_ok']}")
