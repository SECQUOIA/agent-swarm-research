"""Reviewer spot check of window-exactness.md Section 7.5 (two-state examples of [E]).

Inputs taken read-only from theory-bangbang/: the KKT solver dz.solve_kkt and the continuous
linear-rate family (n2win.transferred -> model.continuous_family).  Everything else is the reviewer's:
own simulation of the Euler transcription, own costates and KKT sign check, stage and window
objectives built by direct simulation (exact rationals of the float data) and polarization, and the
reviewer's face-enumeration box-QP (rv_toy.boxqp_min_np).  Float screening, like the report.
usage: python3 rv_n2.py"""
import json
import os
import sys
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TB = os.path.join(HERE, "..", "..", "theory-bangbang")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(TB, "window"))
sys.path.insert(0, os.path.join(TB, "n2"))
from rv_toy import polarize, boxqp_min_np  # noqa: E402
from n2win import EXAMPLES, transferred  # noqa: E402
import discrete as dz  # noqa: E402


def data(p, kk):
    """Exact rationals of the float KKT data; own states, costates, switching values."""
    N = kk["N"]
    h = Fr(p.T) / N
    u = [Fr(float(v)) for v in kk["u"]]
    F = lambda v: Fr(float(v))
    e, q, c, k1, k2, a, rho = map(F, (p.e, p.q, p.c, p.k1, p.k2, p.a, p.rho))
    assert p.nu == 0
    x = [(F(p.x10), F(p.x20))]
    for t in range(N):
        x1, x2 = x[-1]
        x.append((x1 + h * x2, x2 + h * u[t]))
    pc = [None] * (N + 1)
    pc[N] = (-a, rho * x[N][1])
    for t in range(N - 1, -1, -1):
        p1, p2 = pc[t + 1]
        x1, x2 = x[t]
        pc[t] = (p1 + h * (q * x1 + k1 * u[t]), p2 + h * p1 + h * (e - c * x2 + k2 * u[t]))
    sig = [k1 * x[t][0] + k2 * x[t][1] + pc[t + 1][1] for t in range(N)]
    return dict(N=N, h=h, u=u, x=x, p=pc, sig=sig, par=(e, q, c, k1, k2, a, rho))


def L(D, t, x, u):
    e, q, c, k1, k2, a, rho = D["par"]
    return D["h"] * (e * x[1] + q * x[0] ** 2 / 2 - c * x[1] ** 2 / 2 + (k1 * x[0] + k2 * x[1]) * u)


def step(D, x, u):
    return (x[0] + D["h"] * x[1], x[1] + D["h"] * u)


def S(D, Ps, t, x):
    xb = D["x"][t]
    d = (x[0] - xb[0], x[1] - xb[1])
    P = Ps[t]
    return D["p"][t][0] * x[0] + D["p"][t][1] * x[1] + (P[0][0] * d[0] ** 2 + 2 * P[0][1] * d[0] * d[1] + P[1][1] * d[1] ** 2) / 2


def window(D, Ps, a, b, box):
    """f(v) = J_W - J_W(zbar), v = (d1_a, d2_a, om_a..om_{b-1}); entry in the reachable box at a."""
    n = 2 + (b - a)

    def JW(v):
        x = (D["x"][a][0] + v[0], D["x"][a][1] + v[1])
        tot = -S(D, Ps, a, x)
        for t in range(a, b):
            u = D["u"][t] + v[2 + t - a]
            tot += L(D, t, x, u)
            x = step(D, x, u)
        return tot + S(D, Ps, b, x)
    J0 = JW([Fr(0)] * n)
    g, H = polarize(lambda v: JW(v) - J0, n, Fr)
    lo_b, hi_b = box
    lo = [Fr(float(lo_b[a][0])) - D["x"][a][0], Fr(float(lo_b[a][1])) - D["x"][a][1]] + [-1 - D["u"][t] for t in range(a, b)]
    hi = [Fr(float(hi_b[a][0])) - D["x"][a][0], Fr(float(hi_b[a][1])) - D["x"][a][1]] + [1 - D["u"][t] for t in range(a, b)]
    val, v = boxqp_min_np([float(z) for z in g], [[float(z) for z in r] for r in H], [float(z) for z in lo], [float(z) for z in hi])
    return val


def main():
    out = []
    cases = [("A", 1000), ("A", 2000), ("Aminus", 1000), ("Aminus", 2000), ("Aminus", 8000), ("Azero", 1000)]
    for name, N in cases:
        p = EXAMPLES[name]
        kk = dz.solve_kkt(p, N)
        D = data(p, kk)
        h = D["h"]
        # own KKT sign check
        viol = 0.0
        inter = []
        for t in range(N):
            ut, st = D["u"][t], float(D["sig"][t])
            if ut == 1:
                viol = max(viol, st)
            elif ut == -1:
                viol = max(viol, -st)
            else:
                inter.append(t)
                viol = max(viol, abs(st))
        Pf, _ = transferred(p, kk, 0.02, 0.1)
        Ps = [[[Fr(float(Pf[t][i][j])) for j in range(2)] for i in range(2)] for t in range(N + 1)]
        box = dz.reach_box(p, N, float(h))
        s = kk["m"]
        # stage losses near the switch = one-stage windows with entry in the reachable box
        near = {}
        for t in range(s - 3, s + 4):
            near[t - s] = -window(D, Ps, t, t + 1, box) / float(h) ** 2
        rec = dict(example=name, N=N, s=s, inter=inter, u_inter=[float(D["u"][t]) for t in inter], own_kkt_viol=viol,
                   stage_loss_over_h2={q: v for q, v in near.items() if v > 1e-12},
                   stage_loss_over_h3={q: v / float(h) for q, v in near.items() if v > 1e-12},
                   windows_over_h2=[-window(D, Ps, s - K, s + K + 1, box) / float(h) ** 2 for K in (0, 1, 2)])
        print(json.dumps(rec, default=float), flush=True)
        out.append(rec)
    with open(os.path.join(HERE, "logs", "n2.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)


if __name__ == "__main__":
    main()
