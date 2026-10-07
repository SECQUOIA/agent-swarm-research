"""Evaluate, at the exactly feasible centre, the Lagrangian of the stored leaf that contains it
(containment tested with tolerance 1e-40, since the true point is within 1e-45 of the centre)."""
import sys, json
from fractions import Fraction as Fr
import mpmath as mp
sys.path.insert(0, "/tmp/pfd2")
import mycheck as mc
import pf_model as pm
import leafcut as lc
mp.mp.dps = 60
name, tag = sys.argv[1], sys.argv[2]
M = pm.decode(name); info = lc.leaf_info(M)
x, y = mc.point_xy(M, mc.read_point(name))
N, L = info["N"], info["L"]
WNN = x[2*N]**2 + x[2*N+1]**2; WLL = x[2*L]**2 + x[2*L+1]**2
Pg, Qg = y[info["Pg"]], y[info["Qg"]]
tol = mp.mpf("1e-40")
fx = mc.obj_at(M, y)
for Lf in json.load(open(mc.D + f"{name}.{tag}.json"))["leaves"]:
    box = tuple((Fr(a), Fr(c)) for a, c in Lf["box"])
    if not all(mp.mpf(a.numerator)/a.denominator - tol <= v <= mp.mpf(c.numerator)/c.denominator + tol for v, (a, c) in zip((Pg, Qg, WLL), box)):
        continue
    rows, ybox, planes = mc.node_rows(M, info, box)
    beta, eps, cert = mc.certify(M, rows, Lf["raw"], ybox, "leaf containing x*")
    Lx = mc.lag_at(cert, x, y); bf = mp.mpf(beta.numerator) / beta.denominator
    sl = [mp.mpf(al.numerator)/al.denominator*Pg + mp.mpf(be.numerator)/be.denominator*Qg + mp.mpf(ga.numerator)/ga.denominator*WLL + mp.mpf(de.numerator)/de.denominator - WNN for (al, be, ga, de) in planes]
    print(f"  W_LL - 1.1236 at centre: {mp.nstr(WLL - mp.mpf('1.1236'), 3)}; L(x*) - beta = {mp.nstr(Lx - bf, 6)}; f(x*) - L(x*) = {mp.nstr(fx - Lx, 6)}; plane slacks {[mp.nstr(s, 3) for s in sl]}")
