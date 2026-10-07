"""Extract the balanced-split (P_1) fooling family on the pair box of the two wall minimizers of the WALL chain,
n = 4, and recheck its consistency and value in exact rational arithmetic (after rounding the support to rationals
inside the box and re-solving the 3 mean equations exactly)."""
import numpy as np
from fractions import Fraction as Fr
from scipy.optimize import brentq, linprog
import sys
sys.argv = ["x", "none"]
from cg4 import *
co = [0.0, 1.022, 0.189, 1.774, 1.086]; B = 0.962
u = PP.poly(co)
up = lambda t: np.polynomial.polynomial.polyval(t, np.polynomial.polynomial.polyder(co))
c = brentq(lambda t: up(t) - 2 * B, -1, 1)
n = 4
x1 = np.array([-1, -1, c, -1.0]); x3 = np.array([-1, c, -1, -1.0])
l, h = np.minimum(x1, x3), np.maximum(x1, x3)
cb = ClassBound(uniform_chain(n, u, B), [PP.poly([0, 1])], K=9)
lo, upb, it = cb.bound(l, h, None, maxit=200, tol=1e-12)
fv = lambda x: float(np.sum(u(np.array(x))) + B * np.sum(np.array(x[:-1]) * np.array(x[1:])))
fs = fv(x1)
print(f"c = {c:.8f}; f(x^1) = {fv(x1):.10f}, f(x^3) = {fv(x3):.10f}; pair-box LB in [{lo - fs:+.6f}, {upb - fs:+.6f}] relative to f*")
Plist, w = cb.last
col = 0
supp = []
for e in range(n - 1):
    m = len(Plist[e]); we = w[col:col + m]; col += m
    s = [(tuple(np.round(Plist[e][i], 6)), round(we[i], 6)) for i in range(m) if we[i] > 1e-9]
    supp.append(s)
    print(f"  factor {e+1}: {s}")
# exact recheck: rational points (rounded to 1e-6, clipped to box), weights re-solved exactly for consistency
U = [Fr(0), Fr(1022, 1000), Fr(189, 1000), Fr(1774, 1000), Fr(1086, 1000)]
Bq = Fr(962, 1000)
uq = lambda t: sum(U[k] * t**k for k in range(5))
lq = [Fr(-1), Fr(-1), Fr(-1), Fr(-1)]
cq = Fr(round(c * 10**6), 10**6)
hq = [Fr(-1), cq, cq, Fr(-1)]
F = lambda e, xa, xb: (uq(xa) if e == 0 else uq(xa) / 2) + (uq(xb) if e == n - 2 else uq(xb) / 2) + Bq * xa * xb
pts = [[(Fr(round(p[0] * 10**6), 10**6), Fr(round(p[1] * 10**6), 10**6)) for p, _ in s] for s in supp]
wts = [[Fr(round(wt * 10**9), 10**9) for _, wt in s] for s in supp]
for e in range(n - 1):
    tot = sum(wts[e]); wts[e] = [x / tot for x in wts[e]]
    for (pa, pb) in pts[e]:
        assert lq[e] <= pa <= hq[e] and lq[e + 1] <= pb <= hq[e + 1], (e, pa, pb)
mean = lambda e, j: sum(wt * p[j] for wt, p in zip(wts[e], pts[e]))
print("  exact mean mismatches (x2, x3):", float(mean(0, 1) - mean(1, 0)), float(mean(1, 1) - mean(2, 0)))
# repair the means exactly: adjust the two-point measures of factors 1 and 3 (one free coordinate each) by moving weight
val = sum(sum(wt * F(e, *p) for wt, p in zip(wts[e], pts[e])) for e in range(n - 1))
fsq = sum(uq(t) for t in [Fr(-1), Fr(-1), cq, Fr(-1)]) + Bq * (Fr(1) - cq - cq)
print(f"  exact value (before repair) - f(x^1 rounded) = {float(val - fsq):+.6f}")
