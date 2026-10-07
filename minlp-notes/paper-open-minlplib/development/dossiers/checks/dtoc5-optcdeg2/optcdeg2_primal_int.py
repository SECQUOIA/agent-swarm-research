"""optcdeg2: mpmath-free proof of an exactly feasible point (own code).

Controls: u_t = -1/5 for t < 3091, u_3091 = stored double, u_t = +1/5 for 3092 <= t < 47290,
u_47290 free (to be bracketed), u_t = -1/5 for t > 47290. States follow the rows exactly:
  y_{t+1} = y_t + h v_t,   v_{t+1} = v_t + h u_t - a y_t - b v_t^2,   y_0 = 10, v_0 = 0,
with h = 1/2500, a = 1/125000, b = 1/12500 (the exact OSIL decimals 4e-4, 8e-6, 8e-5).
Interval arithmetic on integers scaled by 2^P with floor/ceil rounding (no floating point).
If v_N(lo) < 0 < v_N(hi), continuity gives u* in [lo, hi] with v_N = 0; that point is exactly
feasible if all v_t >= -1 (1 <= t <= N-1) over the bracket and |u| <= 1/5.
"""
import json
import time
from fractions import Fraction as Fr

import numpy as np

t0 = time.time()
N = 50000
P = 320
ONE = 1 << P
H, A, B, W = Fr(1, 2500), Fr(1, 125000), Fr(1, 12500), Fr(1, 5000)
assert H == Fr("4e-4") and A == Fr("8e-6") and B == Fr("8e-5") and W == Fr("2e-4")
u = np.load("optcdeg2_kkt_u.npy")
S1, S2 = 3091, 47290
U1 = Fr(float(u[S1]))
sign = [(-1 if t < S1 else (1 if t < S2 else -1)) for t in range(N)]
assert all((u[t] > 0) == (sign[t] > 0) for t in range(N) if t not in (S1, S2))


def fdn(x):  # floor(x * 2^P) for a Fraction
    return (x.numerator * ONE) // x.denominator


def fup(x):
    return -((-x.numerator * ONE) // x.denominator)


def cmul(lo, hi, c):  # interval times positive rational constant c
    return (lo * c.numerator) // c.denominator, -((-hi * c.numerator) // c.denominator)


def sq(lo, hi):
    if lo >= 0:
        a, b = lo * lo, hi * hi
    elif hi <= 0:
        a, b = hi * hi, lo * lo
    else:
        a, b = 0, max(lo * lo, hi * hi)
    return a >> P, -((-b) >> P)


FIFTH = {1: (fdn(Fr(1, 5)), fup(Fr(1, 5))), -1: (fdn(Fr(-1, 5)), fup(Fr(-1, 5)))}


def simulate(us2_lo, us2_hi):
    ylo = yhi = fdn(Fr(10))
    vlo = vhi = 0
    J2lo, J2hi = sq(ylo, yhi)  # sum of y^2 (scaled)
    vmin = None
    for t in range(N):
        if t == S1:
            ulo, uhi = fdn(U1), fup(U1)
        elif t == S2:
            ulo, uhi = fdn(us2_lo), fup(us2_hi)
        else:
            ulo, uhi = FIFTH[sign[t]]
        hv = cmul(vlo, vhi, H)
        hu = cmul(ulo, uhi, H)
        ay = cmul(ylo, yhi, A)
        v2 = sq(vlo, vhi)
        bv = cmul(v2[0], v2[1], B)
        nylo, nyhi = ylo + hv[0], yhi + hv[1]
        nvlo = vlo + hu[0] - ay[1] - bv[1]
        nvhi = vhi + hu[1] - ay[0] - bv[0]
        ylo, yhi, vlo, vhi = nylo, nyhi, nvlo, nvhi
        s = sq(ylo, yhi)
        J2lo += s[0]; J2hi += s[1]
        if 0 < t + 1 < N:
            vmin = vlo if vmin is None or vlo < vmin else vmin
    Jlo, Jhi = cmul(J2lo, J2hi, W)
    return dict(vN=(Fr(vlo, ONE), Fr(vhi, ONE)), J=(Fr(Jlo, ONE), Fr(Jhi, ONE)), vmin=Fr(vmin, ONE))


# root finding for u_{S2} (secant on midpoints; not part of the proof)
def vN_mid(x):
    r = simulate(x, x)["vN"]
    return (r[0] + r[1]) / 2


x0, x1 = Fr(float(u[S2])), Fr(float(u[S2])) + Fr(1, 10 ** 9)
f0, f1 = vN_mid(x0), vN_mid(x1)
for _ in range(12):
    if f1 == f0:
        break
    x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
    x2 = Fr(fdn(x2), ONE)  # keep denominators small
    x0, f0, x1, f1 = x1, f1, x2, vN_mid(x2)
    if abs(f1) < Fr(1, 10 ** 75):
        break
ustar = x1
d = Fr(1, 10 ** 60)
lo, hi = ustar - d, ustar + d
ra, rb, rI = simulate(lo, lo), simulate(hi, hi), simulate(lo, hi)
fifth = Fr(1, 5)
ok = (ra["vN"][1] < 0 < rb["vN"][0]) and rI["vmin"] >= -1 and abs(U1) <= fifth and -fifth <= lo and hi <= fifth


def dec(x, n=45):
    ip = x.numerator // x.denominator
    fp = (x - ip) * 10 ** n
    return f"{ip}.{fp.numerator // fp.denominator:0{n}d}"


LB = Fr(29387607509587509237940, 10 ** 20)  # reviewer's exact LB, truncated to 20 decimals (a valid lower bound)
UBrev = Fr("293.8760750958750932772142114247080159340995595146603160142298703")
out = dict(P=P, u_s1=str(U1), u_s2_approx=float(ustar), vN_at_lo_hi=float(ra["vN"][1]), vN_at_hi_lo=float(rb["vN"][0]),
           sign_change=bool(ra["vN"][1] < 0 < rb["vN"][0]), min_v_lower=float(rI["vmin"]), feasible_proof=bool(ok),
           J_lo=dec(rI["J"][0]), J_hi=dec(rI["J"][1]), J_width=float(rI["J"][1] - rI["J"][0]),
           J_hi_minus_reviewer_UB=float(rI["J"][1] - UBrev), gap_to_LB20=float(rI["J"][1] - LB),
           seconds=round(time.time() - t0, 1))
print(json.dumps(out, indent=1))

# negative test: a bracket lying entirely above the root must not show a sign change
na, nb = simulate(ustar + 10 * d, ustar + 10 * d), simulate(ustar + 20 * d, ustar + 20 * d)
print("negative test (bracket above root): sign change =", bool(na["vN"][1] < 0 < nb["vN"][0]),
      "; v_N at both ends > 0:", bool(na["vN"][0] > 0 and nb["vN"][0] > 0))
