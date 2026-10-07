"""Refine the optcdeg2 bang-bang primal so that it is a discrete KKT point.

Controls: -0.2 (t < k1), fractional at k1, +0.2 (k1 < t < k2), fractional at k2, -0.2 after.
Unknowns: switch positions s1, s2 (s = k + fractional part, as in optcdeg2_primal.py).
Equations: v_N(s1, s2) = 0 and p_v(k1+1) = 0, where the costates use the terminal
multiplier nu chosen so that p_v(k2+1) = 0. Solved by bisection in s2 (inner) and
secant iterations in s1 (outer), in float64. Saves the refined control vector.
"""
import json
import sys

import numpy as np

import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../.."))
sys.path.insert(0, _REPO + "/research-20260929/open-instances")
from optcdeg2_primal import controls, simulate, solve_s2  # noqa: E402

N = 50000
h = 4e-4


def costates(y, v, nu):
    py = np.empty(N + 1); pv = np.empty(N + 1)
    py[N] = h * y[N]; pv[N] = nu
    for t in range(N - 1, -1, -1):
        py[t] = h * y[t] + py[t + 1] - 0.02 * h * pv[t + 1]
        pv[t] = h * py[t + 1] + (1 - 0.4 * h * v[t]) * pv[t + 1]
    return py, pv


def kkt_residual(s1):
    s2 = solve_s2(s1)
    u = controls(s1, s2)
    y, v = simulate(u)
    vN = v[N]
    v = v.copy(); v[N] = 0.0
    k1, k2 = int(s1), int(s2)
    a0 = costates(y, v, 0.0)[1]
    a1 = costates(y, v, 1.0)[1]
    nu = -a0[k2 + 1] / (a1[k2 + 1] - a0[k2 + 1])
    pv = a0 + nu * (a1 - a0)
    J = h / 2 * np.sum(y ** 2)
    return pv[k1 + 1], dict(s1=s1, s2=s2, J=J, nu=nu, vN=vN, u=u)


def main():
    s1_old = 3091.395483248142
    r_old, info_old = kkt_residual(s1_old)
    print(json.dumps(dict(s1=s1_old, pv_k1p1=r_old, J=info_old["J"])), flush=True)
    a, b = s1_old, s1_old + 0.05
    fa, fb = r_old, kkt_residual(b)[0]
    for _ in range(40):
        c = b - fb * (b - a) / (fb - fa)
        fc, info = kkt_residual(c)
        print(json.dumps(dict(s1=c, pv_k1p1=fc, J=info["J"], s2=info["s2"])), flush=True)
        a, fa, b, fb = b, fb, c, fc
        if abs(fc) < 1e-13 or abs(b - a) < 1e-12:
            break
    rec = {k: (float(val) if k != "u" else None) for k, val in info.items()}
    rec["pv_k1p1"] = float(fc)
    rec.pop("u")
    print(json.dumps(rec))
    np.save("logs/optcdeg2_kkt_u.npy", info["u"])
    json.dump(rec, open("logs/optcdeg2_kkt_primal.json", "w"), indent=1)


if __name__ == "__main__":
    main()
