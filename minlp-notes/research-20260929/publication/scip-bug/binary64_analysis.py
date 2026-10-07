"""Which nonlinear equalities of a CIP model are exactly satisfiable at the
variables' lower bounds in decimal arithmetic but not after rounding the
data to binary64?

For every row of the form  c*y = x^k  (written  -c*<y> + <x>*...*<x> == 0)
the script compares  lb(x)^k  with  c*lb(y)  twice: with the decimal bounds as
written in the file (exact rationals) and with the bounds rounded to the
nearest binary64 number (exact rational value of the double).  All arithmetic
is exact (fractions).  It also reports whether the variable x can be forced
to its lower bound by a row  x - a*b <= lb(x)  with b binary (pump off).

usage: python3 binary64_analysis.py MODEL.cip
"""
import sys
from fractions import Fraction as F

import exact_check as ec

vars_, rows = ec.parse_cip(sys.argv[1])
V = {v["name"]: v for v in vars_}
print(f"model {sys.argv[1]}")
nfound = 0
for r in rows:
    if r["op"] != "==" or r["rhs"] != 0 or len(r["terms"]) != 2:
        continue
    lin = [(a, ns) for a, ns in r["terms"] if len(ns) == 1]
    mon = [(a, ns) for a, ns in r["terms"] if len(ns) >= 2]
    if len(lin) != 1 or len(mon) != 1 or len(set(mon[0][1])) != 1 or mon[0][0] != 1:
        continue
    (cy, (y,)), (_, xs) = lin[0], mon[0]
    x, k = xs[0], len(xs)
    lx, ly = V[x]["lb"], V[y]["lb"]
    if lx is None or ly is None:
        continue
    dec = lx ** k + cy * ly                      # residual x^k - (-cy) y at the lower bounds
    dbl = F(float(lx)) ** k + F(float(cy)) * F(float(ly))
    forced = [s["name"] for s in rows
              if s["op"] == "<=" and s["rhs"] == lx and len(s["terms"]) == 2
              and any(ns == [x] and a == 1 for a, ns in s["terms"])
              and any(len(ns) == 1 and V[ns[0]]["type"] == "binary" and a < 0 for a, ns in s["terms"])]
    if dec == 0 and dbl != 0:
        nfound += 1
        print(f"  {r['name']}: {y} = {x}^{k}; lb({x}) = {lx}, lb({y}) = {ly}: decimal residual 0, "
              f"binary64 residual fl(lb {x})^{k} - fl(lb {y}) = {float(dbl):.3e}; "
              f"{x} forced to its lower bound when the binary is 0 by: {forced or 'none'}")
print(f"  {nfound} such rows")
