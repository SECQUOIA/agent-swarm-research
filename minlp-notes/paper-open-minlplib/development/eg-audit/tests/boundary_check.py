"""Second-reviewer check of cert/auditor.py (written independently of test_auditor.py).

    python3 boundary_check.py

1. Constants against mpmath (400 bits): the ln 2 bracket, |L - L1 - L2| <= DL, L1 has 36 bits,
   the 2^(j/64) table; the observed Horner error against rho_H.
2. Enclosure lo <= e^x <= hi on hard arguments: every 7th reduction half-point (m + 1/2) ln2/64
   over the whole range and its float neighbours, multiples of ln2/64 and their neighbours, 50
   floats on each side of -708, 709, 0, -700, -699 and 600, subnormal and tiny arguments, and
   random arguments in the certifier's ranges.
3. Soundness at the edge of the band: for 6,000 arguments, the first float above (1 + eps) e^x and
   the first float below (1 - eps) e^x must fail; (1 +- eps/2) e^x must pass.  The same for
   x ** k, k = 2, 3, 4 (first float above (1 + eps) x^k), including tiny x.
"""
import os, sys, time
from fractions import Fraction as Fr
import numpy as np
import mpmath as mp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cert"))
import auditor as A

mp.mp.prec = 400
u = Fr(1, 2**53)
fails = 0
def check(c, msg):
    global fails
    print(("ok   " if c else "FAIL ") + msg, flush=True); fails += not c

def mpq(q):  # Fraction -> mpf exactly (prec 400 is enough for our fractions? use mpf division)
    return mp.mpf(q.numerator) / q.denominator

# 1. constants
ln2 = mp.log(2)
L = ln2 / 64
check(mpq(A._LN2_LO) <= ln2 <= mpq(A._LN2_HI), "ln2 bracket")
check(Fr(A.L1).denominator <= 2**42 and Fr(A.L1).numerator.bit_length() <= 36, f"L1 bits {Fr(A.L1).numerator.bit_length()}")
dl_true = abs(L - mp.mpf(A.L1) - mp.mpf(A.L2))
check(dl_true <= mpq(A.DL), f"|L-L1-L2| = {mp.nstr(dl_true,5)} <= DL = {float(A.DL):.3e}")
for j in range(64):
    t = mp.power(2, mp.mpf(j)/64)
    if not (mp.mpf(A.TLO[j]) <= t <= mp.mpf(A.THI[j])):
        check(False, f"table j={j}")
check(True, "table vs mpmath 2^(j/64) (64 entries)")
print("COEF exact?", [Fr(c) == Fr(1, __import__('math').factorial(i)) for i, c in enumerate(A.COEF)])
# EH independent: bound |e^r - Horner(r)| by brute force at many r with mpmath and compare to EH
rs = np.concatenate([np.linspace(-0.0055, 0.0055, 20001), np.random.default_rng(1).uniform(-0.0055, 0.0055, 20000)])
worst = mp.mpf(0)
for r in rs:
    h = A.COEF[7]
    for i in range(6, -1, -1):
        h = A.COEF[i] + r * h
    e = abs(mp.exp(mp.mpf(float(r))) - mp.mpf(h)) / mp.mpf(h)
    worst = max(worst, e)
print(f"observed max |e^r - H|/H = {mp.nstr(worst,5)} vs rho_H = {float(A.RHO_H):.4e}")
check(worst <= mpq(A.RHO_H), "Horner observed error below rho_H")

# 2. hard arguments for the enclosure
rng = np.random.default_rng(7)
Lf = float(L)
ms = np.arange(-65370, 65465, 7)
half = (ms + 0.5) * Lf
xs = [half, np.nextafter(half, np.inf), np.nextafter(half, -np.inf), ms * Lf,
      np.nextafter(ms * Lf, np.inf), np.nextafter(ms*Lf, -np.inf)]
# near boundaries
for b in (-708.0, 709.0, 0.0, -700.0, -699.0, 600.0):
    v = np.array([b]); out = [v]
    for _ in range(50):
        out.append(np.nextafter(out[-1], np.inf)); out.append(np.nextafter(out[-2] if len(out) > 1 else v, -np.inf))
    xs.append(np.concatenate(out))
xs.append(np.array([5e-324, -5e-324, 2.2250738585072014e-308, -2.2250738585072014e-308, 1e-300, -1e-300, 1e-20, -1e-20]))
xs.append(rng.uniform(-745, 0, 20000)); xs.append(rng.uniform(0, 600, 5000)); xs.append(-10.0**rng.uniform(-30, 2.85, 5000))
# x where rint(x*INV_L) is ambiguous: many half points near large |m|
x = np.concatenate(xs)
x = x[(x >= -708) & (x <= 709)]
t0 = time.time()
lo, hi, valid = A.exp_enclosure(x)
check(bool(valid.all()), f"valid on {len(x)} args")
bad = 0; wmax = mp.mpf(0)
for xi, l, h in zip(x, lo, hi):
    e = mp.exp(mp.mpf(float(xi)))
    if not (mp.mpf(float(l)) <= e <= mp.mpf(float(h))):
        bad += 1
        if bad < 5: print("  enclosure FAIL", repr(xi), l, h, e)
    wmax = max(wmax, (mp.mpf(float(h)) - mp.mpf(float(l))) / e)
check(bad == 0, f"enclosure lo <= e^x <= hi on {len(x)} hard args; max rel width {mp.nstr(wmax,4)}; {time.time()-t0:.0f}s")

# 3. soundness at the eps boundary: for each x, the float just above e^x(1+eps) and just below e^x(1-eps) must fail;
#    the floats just inside the band at 0.5 eps must pass.
eps = mp.mpf(1) / 10**14
sub = rng.choice(len(x), 6000, replace=False)
xb = x[sub]
yo_hi, yo_lo, yi_hi, yi_lo = [], [], [], []
for xi in xb:
    e = mp.exp(mp.mpf(float(xi)))
    up = float(e * (1 + eps))         # nearest; step outward until strictly outside
    while mp.mpf(up) <= e * (1 + eps): up = float(np.nextafter(up, np.inf))
    dn = float(e * (1 - eps))
    while mp.mpf(dn) >= e * (1 - eps): dn = float(np.nextafter(dn, -np.inf))
    yo_hi.append(up); yo_lo.append(dn)
    yi_hi.append(float(e * (1 + eps / 2))); yi_lo.append(float(e * (1 - eps / 2)))
check(not A.exp_ok(xb, np.array(yo_hi)).any(), f"first float above (1+eps)e^x flagged on all {len(xb)}")
check(not A.exp_ok(xb, np.array(yo_lo)).any(), f"first float below (1-eps)e^x flagged on all {len(xb)}")
check(bool(A.exp_ok(xb, np.array(yi_hi)).all()), "(1+eps/2)e^x accepted")
check(bool(A.exp_ok(xb, np.array(yi_lo)).all()), "(1-eps/2)e^x accepted")
# x < -708 handling
check(bool(A.exp_ok(np.array([-708.0000000001, -745.2, -1e5, -np.inf]), np.array([np.exp(-708.0000000001), 0.0, 0.0, 0.0])).all()), "x<-708 accepted when 0<=y<=2^-1020")
check(not A.exp_ok(np.array([np.inf, np.nan, 709.0000000001, -708.5]), np.array([np.inf, np.nan, 1e308, -0.0 - 1e-320])).any(), "inf/nan/x>709/negative y flagged")

# 4. pow: boundary soundness for k = 2,3,4 on the certifier's ranges incl. tiny, with floats just outside the band
for k in (2, 3, 4):
    xp = np.concatenate([rng.uniform(0, 3.2, 3000), 10.0**rng.uniform(-80, 2, 3000), [2.0**-250, np.nextafter(2.0**-250, 0), 2.0**250, 1.0, 3e-17]])
    yo = []; yi = []
    for v in xp:
        ex = Fr(float(v))**k
        up = float(ex * (1 + Fr(1, 10**14)))
        while Fr(up) <= ex * (1 + Fr(1, 10**14)): up = float(np.nextafter(up, np.inf))
        yo.append(up)
        yi.append(float(ex * (1 + Fr(1, 2*10**14))))
    yo = np.array(yo); yi = np.array(yi)
    fl = A.pow_ok(xp, k, yo)
    exact_bad = np.array([abs(Fr(float(b)) - Fr(float(v))**k) > A.EPS_POW * Fr(float(v))**k for b, v in zip(yo, xp)])
    check(not fl[exact_bad].any(), f"pow k={k}: outside-band floats flagged ({int(exact_bad.sum())} cases; {int((~exact_bad).sum())} rounded back inside)")
    ok_in = A.pow_ok(xp, k, yi)
    inband = np.array([abs(Fr(float(b)) - Fr(float(v))**k) <= Fr(1, 10**14) * Fr(float(v))**k for b, v in zip(yi, xp)])
    print(f"   pow k={k}: half-eps values accepted {int(ok_in.sum())}/{len(xp)} (in band {int(inband.sum())})")
print("ALL OK" if not fails else f"FAILURES {fails}")
