"""optcdeg2 primal side (reviewer code).

1. The authors' point exactly as they built it (float64 simulation of logs/optcdeg2_kkt_u.npy,
   v_N := 0): objective, max row violation and bound violations in exact rational arithmetic.
2. A rigorous upper bound on f*: controls u_t = -1/5 or +1/5 exactly (sign of the stored control),
   u_{s1} = the stored double, u_{s2} free. States are simulated in mpmath interval arithmetic
   (200 bits). If v_N(a) < 0 < v_N(b) rigorously, then some u* in [a, b] gives v_N = 0 (v_N is
   continuous in u_{s2}), and that point is feasible if all v_t >= -1 and |u*| <= 1/5; its
   objective lies in the interval enclosure of J over u_{s2} in [a, b]. So f* <= sup J([a, b]).
"""
import json
import math
from fractions import Fraction as Fr

import mpmath
import numpy as np
from mpmath import iv, mp

N = 50000
import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../.."))
TB = _REPO + "/research-20260929/theory-bangbang/"
H, AY, BV, W = Fr(4, 10000), Fr(8, 10 ** 6), Fr(8, 10 ** 5), Fr(2, 10 ** 4)


def authors_point(u):
    hf = 4e-4
    y = np.empty(N + 1); v = np.empty(N + 1); y[0] = 10.0; v[0] = 0.0
    for t in range(N):
        y[t + 1] = y[t] + hf * v[t]
        v[t + 1] = v[t] + hf * (u[t] - 0.02 * y[t] - 0.2 * v[t] ** 2)
    vN = v[N]; v[N] = 0.0
    Y = [Fr(float(a)) for a in y]; Vv = [Fr(float(a)) for a in v]; U = [Fr(float(a)) for a in u]
    obj = sum(W * a * a for a in Y)
    rv = Fr(0)
    for t in range(N):
        r1 = abs(Y[t + 1] - Y[t] - H * Vv[t])
        r2 = abs(Vv[t + 1] - Vv[t] - H * U[t] + AY * Y[t] + BV * Vv[t] * Vv[t])
        rv = max(rv, r1, r2)
    bv = max(max(abs(a) - Fr(1, 5) for a in U), max(Fr(-1) - a for a in Vv[1:N]), Fr(0))
    return dict(obj=float(obj), obj_20=mpmath.nstr(mpmath.mpf(obj.numerator) / obj.denominator, 20),
                max_row_violation=float(rv), max_bound_violation=float(bv), simulated_vN=float(vN))


def simulate(us, s1, s2, u1, u2, interval):
    """forward simulation; returns (J, v_N, min_t v_t) in mp or iv."""
    M = iv if interval else mp
    h, a, b, w = M.mpf(H.numerator) / H.denominator, M.mpf(AY.numerator) / AY.denominator, \
        M.mpf(BV.numerator) / BV.denominator, M.mpf(W.numerator) / W.denominator
    fifth = M.mpf(1) / 5
    y, v = M.mpf(10), M.mpf(0)
    J = w * y * y
    vmin = None
    for t in range(N):
        if t == s1:
            ut = u1
        elif t == s2:
            ut = u2
        else:
            ut = fifth if us[t] > 0 else -fifth
        y, v = y + h * v, v + h * ut - a * y - b * v * v
        J += w * y * y
        if 0 < t + 1 < N:
            lo = v.a if interval else v
            vmin = lo if vmin is None or lo < vmin else vmin
    return J, v, vmin


def main():
    u = np.load(TB + "logs/optcdeg2_kkt_u.npy")
    out = dict(authors_point=authors_point(u))
    print(json.dumps(out), flush=True)
    frac = np.where(np.abs(np.abs(u) - 0.2) > 1e-12)[0]
    s1, s2 = int(frac[0]), int(frac[1])
    mp.prec = 200; iv.prec = 200
    u1 = mp.mpf(float(u[s1]))
    # secant on u_{s2} in mp so that v_N = 0
    x0, x1 = mp.mpf(float(u[s2])), mp.mpf(float(u[s2])) + mp.mpf("1e-9")
    f0 = simulate(u, s1, s2, u1, x0, False)[1]; f1 = simulate(u, s1, s2, u1, x1, False)[1]
    for _ in range(8):
        x0, x1, f0 = x1, x1 - f1 * (x1 - x0) / (f1 - f0), f1
        f1 = simulate(u, s1, s2, u1, x1, False)[1]
        if abs(f1) < mp.mpf("1e-50"):
            break
    ustar = x1
    Jp = simulate(u, s1, s2, u1, ustar, False)[0]
    delta = mp.mpf("1e-40")
    a_, b_ = ustar - delta, ustar + delta
    I1 = iv.mpf(u1)
    va = simulate(u, s1, s2, I1, iv.mpf(a_), True)[1]
    vb = simulate(u, s1, s2, I1, iv.mpf(b_), True)[1]
    Jh, vh, vmin = simulate(u, s1, s2, I1, iv.mpf([a_, b_]), True)
    ok = (va.b < 0) and (vb.a > 0) and (vmin >= -1) and abs(b_) <= mp.mpf(1) / 5 and abs(u1) <= mp.mpf(1) / 5
    out["rigorous_primal"] = dict(s1=s1, s2=s2, u_s1=float(u1), u_s2=mpmath.nstr(ustar, 25),
                                  vN_at_a=mpmath.nstr(va.b, 5), vN_at_b=mpmath.nstr(vb.a, 5),
                                  min_v=mpmath.nstr(vmin, 8), sign_change_and_feasible=bool(ok),
                                  J_point=mpmath.nstr(Jp, 25), J_upper=mpmath.nstr(Jh.b, 25),
                                  J_enclosure_width=mpmath.nstr(Jh.b - Jh.a, 3))
    print(json.dumps(out, indent=1), flush=True)
    json.dump(out, open("logs/primal_check.json", "w"), indent=1)


if __name__ == "__main__":
    main()
