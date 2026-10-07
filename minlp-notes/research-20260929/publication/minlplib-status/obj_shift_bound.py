"""Revision after review round 1, methanol50 and lop97icx: bound on the
objective difference between the .gms text form and the MINLPLib OSIL form
near the audit point.

Delta(x) = obj_gms(x) - obj_osil(x) is a polynomial whose coefficients are the
exact coefficient differences found by exact_forms.py. For every x with
|x_v - p_v| <= 1 for all variables v, |Delta(x)| <= sum_m |dc_m| prod_v
(|p_v| + 1)^e_v. The bound is computed exactly with Fractions.

Usage: python3 obj_shift_bound.py
"""
import os
from fractions import Fraction as F

import exact_forms as E

for n, p in E.POINTS.items():
    g = E.read_gms(os.path.join(E.HERE, "pages", "models", "gms", n + ".gms"))
    o = E.read_osil(os.path.join(E.OSIL, n + ".osil"))
    _, go = E.gms_objective(g)
    d = E.coef_diffs(go, o["obj"][0])
    sol = {}
    for line in open(os.path.join(E.R, "bound-audit", "sol", f"{n}.{p}.sol")):
        k, v = line.split()
        sol[k] = F(v)
    bound = F(0)
    for m, a, b in d:
        t = abs(b - a)
        for v, e in m:
            t *= (abs(sol.get(v, F(0))) + 1) ** e
        bound += t
    print(f"{n} {p}: {len(d)} differing coefficients; max |x_v| at {p} = {float(max(abs(x) for x in sol.values()))}; "
          f"|obj_gms - obj_osil| <= {float(bound):.3e} on the box p +- 1")
