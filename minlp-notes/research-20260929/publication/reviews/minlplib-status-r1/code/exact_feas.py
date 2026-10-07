"""Verifier: exact rational feasibility check of a listed point for an OSiL
model whose rows are all polynomials (variable bounds, integrality, every
row). Missing variables are 0. Usage: exact_feas.py MODEL.osil POINT.sol"""
import sys
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from poly_cmp_lib import read, rowpoly  # noqa: E402
from tri_proof import load_sol  # noqa: E402

M = read(sys.argv[1])
x = load_sol(sys.argv[2])
bad = []
for j, n in enumerate(M["vars"]):
    v = x.get(n, Fraction(0))
    if M["type"][j] in ("B", "I") and v.denominator != 1:
        bad.append((n, "not integral", v))
    if M["lb"][j] is not None and v < M["lb"][j]:
        bad.append((n, "lb", v))
    if M["ub"][j] is not None and v > M["ub"][j]:
        bad.append((n, "ub", v))


def ev(p):
    s = Fraction(0)
    for k, c in p.items():
        t = c
        for n, e in k:
            t *= x.get(n, Fraction(0)) ** e
        s += t
    return s


minslack = None
for i, name in enumerate(M["cons"]):
    p, (lo, hi) = rowpoly(M, i)
    v = ev(p)
    if lo is not None and v < lo:
        bad.append((name, "row lb", float(v - lo)))
    if hi is not None and v > hi:
        bad.append((name, "row ub", float(v - hi)))
    for s in ([v - lo] if lo is not None else []) + ([hi - v] if hi is not None else []):
        minslack = s if minslack is None else min(minslack, s)
obj, _ = rowpoly(M, -1)
print("violations:", len(bad), bad[:5])
print("smallest row slack (exact):", minslack)
print("objective (exact):", ev(obj), "=", float(ev(obj)))
