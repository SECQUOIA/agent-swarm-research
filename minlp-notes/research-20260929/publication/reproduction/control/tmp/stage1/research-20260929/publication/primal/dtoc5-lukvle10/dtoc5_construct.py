"""dtoc5: construct an exactly feasible rational point.

Model (asserted from the OSIL below, constants exact):
  min  2e-5 * sum_{j=0}^{2T-1} x_j^2       (u_t = x_t, t < T;  y_t = x_{T+t}, t <= T)
  s.t. -2e-5 u_t + y_t - y_{t+1} + 8e-5 y_t^2 = 0   (t = 0..T-1),   y_0 = 1,   T = 49999,
all other variables free.

Construction: polish the states y of the existing double-precision Newton solution
(research-20260929/open-instances/logs/dtoc5_y.npy) by Newton steps on the reduced problem in
50-digit mpmath, round y_1..y_T to DIGITS decimals (y_0 = 1 exactly), and set each control from its
row in exact rational arithmetic: u_t = -(y_t - y_{t+1} + 8e-5 y_t^2) / (-2e-5). Every row then holds
exactly; the point is a finite-decimal rational vector. Exactness is checked separately by
check_exact_point.py.
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import json
import sys
import time
from fractions import Fraction

import mpmath as mp
import numpy as np

import osil_exact
from exact_io import write_point

OSIL = (_PUBLIC_HOME + '/.cache/minlplib/minlplib/osil/dtoc5.osil')
import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../../.."))
Y0 = _REPO + "/research-20260929/open-instances/logs/dtoc5_y.npy"
T = 49999
DIGITS = 30


def assert_structure(I):
    n = len(I["names"])
    assert n == 2 * T + 1 and len(I["cons"]) == T
    for j in range(n):
        assert I["vtype"][j] == "C"
        if j == T:
            assert I["lb"][j] == I["ub"][j] == 1
        else:
            assert I["lb"][j] is None and I["ub"][j] is None
    o = I["obj"]
    assert o["sense"] == "min" and o["constant"] == 0 and not o["lin"] and o["nl"] is None
    assert sorted(o["quad"]) == [(j, j, Fraction(1, 50000)) for j in range(2 * T)]
    for t, c in enumerate(I["cons"]):
        assert c["lb"] == c["ub"] == 0 and c["constant"] == 0 and c["nl"] is None
        assert c["lin"] == {t: Fraction(-1, 50000), T + t: 1, T + t + 1: -1}
        assert c["quad"] == [(T + t, T + t, Fraction(1, 12500))]


def polish(y, steps=3, dps=50):
    """Newton on F(y) = sum_t [ (y_t + 4h y_t^2 - y_{t+1})^2 / h + h y_t^2 ], y_0 = 1 (tridiagonal)."""
    mp.mp.dps = dps
    h = mp.mpf(1) / 50000
    Y = [mp.mpf(1)] + [mp.mpf(float(v)) for v in y[1:]]
    for s in range(steps):
        r = [Y[t] + 4 * h * Y[t] ** 2 - Y[t + 1] for t in range(T)]
        d = [1 + 8 * h * Y[t] for t in range(T)]
        g = [mp.mpf(0)] * (T + 1)
        Hd = [mp.mpf(0)] * (T + 1)
        for t in range(T):
            g[t] += 2 * r[t] * d[t] / h + 2 * h * Y[t]
            g[t + 1] -= 2 * r[t] / h
            Hd[t] += 2 * d[t] ** 2 / h + 16 * r[t] + 2 * h
            Hd[t + 1] += 2 / h
        off = [-2 * d[t] / h for t in range(T)]  # Hessian entry (t, t+1)
        # Thomas algorithm on unknowns y_1..y_T (SPD tridiagonal)
        a = Hd[1:]
        b = off[1:]  # (k, k+1) for k = 1..T-1
        rhs = [-v for v in g[1:]]
        m = len(a)
        cp, dp = [mp.mpf(0)] * m, [mp.mpf(0)] * m
        cp[0], dp[0] = b[0] / a[0], rhs[0] / a[0]
        for i in range(1, m):
            piv = a[i] - b[i - 1] * cp[i - 1]
            cp[i] = b[i] / piv if i < m - 1 else mp.mpf(0)
            dp[i] = (rhs[i] - b[i - 1] * dp[i - 1]) / piv
        step = [mp.mpf(0)] * m
        step[-1] = dp[-1]
        for i in range(m - 2, -1, -1):
            step[i] = dp[i] - cp[i] * step[i + 1]
        gmax = max(abs(v) for v in g[1:])
        smax = max(abs(v) for v in step)
        print(f"newton step {s}: max|grad| {mp.nstr(gmax, 3)}  max|step| {mp.nstr(smax, 3)}", flush=True)
        for k in range(1, T + 1):
            Y[k] += step[k - 1]
    return Y


def main():
    t0 = time.time()
    I = osil_exact.read(OSIL)
    assert_structure(I)
    print(f"structure asserted ({time.time() - t0:.1f} s)", flush=True)
    Y = polish(np.load(Y0))
    scale = 10 ** DIGITS
    y = [Fraction(1)] + [Fraction(int(mp.nint(v * scale)), scale) for v in Y[1:]]
    a = I["cons"][0]["lin"][0]          # -2e-5
    q = I["cons"][0]["quad"][0][2]      # 8e-5
    u = [-(y[t] - y[t + 1] + q * y[t] * y[t]) / a for t in range(T)]
    x = u + y
    names = I["names"]
    hdr = [f"dtoc5 exactly feasible rational point; states rounded to {DIGITS} decimals,",
           "controls from the rows in exact rational arithmetic; values are exact decimals."]
    write_point("points/dtoc5_point.txt.gz", names, x, hdr)
    # exact objective (structure asserted above): (1/50000) * sum_{j < 2T} x_j^2
    obj = sum(v * v for v in x[: 2 * T]) / 50000
    rec = dict(digits=DIGITS, obj_decimal_40=mp.nstr(mp.mpf(obj.numerator) / obj.denominator, 40),
               u_min=float(min(u)), u_max=float(max(u)), y_min=float(min(y)), y_max=float(max(y)),
               seconds=time.time() - t0)
    print(json.dumps(rec, indent=1))
    json.dump(rec, open("logs/dtoc5_construct.json", "w"), indent=1)


if __name__ == "__main__":
    main()
