"""Small data-semantics checks (read-only):
1. pricing050: every objective coefficient is an integer (the author's pricing050.py uses only
   the numerator of c_j).
2. etamac: the homogeneity degree s = (p2 + p3) q of the CES rows under the decimal reading (b)
   and the binary64 reading (c); the certificate needs s > 1 and p1 q < 1.
3. lnts: the only binary64-inexact data are the angle bounds +-1.5707963267949; both readings
   lie above pi/2, and the dual certificates do not use them.
"""
import os
import re
from fractions import Fraction as F

import mpmath

P = os.path.expanduser('~/.cache/minlplib/minlplib/osil/')
t = open(P + 'pricing050.osil').read()
o = re.search(r'<objectives.*?</objectives>', t, re.S).group(0)
cs = re.findall(r'<coef idx="(\d+)">([^<]*)</coef>', o)
print(f"pricing050: {len(cs)} objective coefficients, all integers: {all(F(v).denominator == 1 for _, v in cs)}")

P1, P2, P3, Q = "-.342222222222222", "-.427777777777778", "-.794444444444445", "-.818181818181818"
for lab, conv in (("decimal (b)", F), ("binary64 (c)", lambda s: F(float(s)))):
    p1, p2, p3, q = (-conv(P1), -conv(P2), -conv(P3), -conv(Q))
    s = (p2 + p3) * q
    print(f"etamac {lab}: s - 1 = {float(s - 1):.6e}, p1*q = {float(p1 * q):.17g}")
et = open(P + 'etamac.osil').read()
assert all(f'"{v}"' in et for v in (P1, P2, P3, Q)), "exponent strings not found in etamac.osil"

mpmath.mp.dps = 40
hp = mpmath.pi / 2
for lab, v in (("decimal (b)", mpmath.mpf("1.5707963267949")), ("binary64 (c)", mpmath.mpf(float("1.5707963267949")))):
    print(f"lnts angle bound {lab}: bound - pi/2 = {mpmath.nstr(v - hp, 5)}")
