"""Referee check (R3): phase position of the first switch on the strong-drop grids with a fractional second
switch.  Own float code: rebuild the KKT point from the logged pattern (s1, s2, fractional stages of
logs/sweep.json), solve sigma = 0 at the fractional stages, check all KKT signs, and compute
  theta_1 = s1 h + h (1 + u_s1) / 2   (switch from u = +1 to -1 inside stage s1: fraction (1 + u)/2 at +1),
compared with the logged break_time_minus_theta1, whose code uses s1 h + h (1 - u_s1) / 2."""
import json
import math
from fractions import Fraction as Fr
import numpy as np

sweep = json.load(open("../../theory-bangbang/kneg/logs/sweep.json"))


def setup(N, t1, t2, k1, k2, tk):
    h = 2.0 / N
    a = np.array([4.0 if Fr(t * 2, N) < Fr(repr(t1)) else (-4.0 if Fr(t * 2, N) < Fr(repr(t2)) else 4.0) for t in range(N)])
    k = np.array([k1 if Fr(t * 2, N) < Fr(repr(tk)) else k2 for t in range(N)])
    return h, a, k


def sig_of(u, h, a, k):
    N = len(u)
    x = np.concatenate([[0.0], np.cumsum(h * u)])
    p = np.empty(N + 1)
    p[N] = -3 + x[N]
    inc = h * (x[:N] - a + k * u)
    p[:N] = p[N] + np.cumsum(inc[::-1])[::-1]
    return k * x[:N] + p[1:]


out = []
for r in sweep:
    if r.get("kappa1") != 1.0 or r.get("break_minus_s1") is None or r["s2"] not in r["frac"]:
        continue
    N, s1, s2, fr = r["N"], r["s1"], r["s2"], r["frac"]
    h, a, k = setup(N, r["t1"], r["t2"], -r["kappa1"], -r["kappa2"], r["tk"])
    u = np.ones(N)
    u[s1:s2] = -1.0
    for t in fr:
        u[t] = 0.0
    s0 = sig_of(u, h, a, k)
    M = np.empty((len(fr), len(fr)))
    for j, t in enumerate(fr):
        e = u.copy(); e[t] = 1.0
        M[:, j] = (sig_of(e, h, a, k) - s0)[fr]
    vals = np.linalg.solve(M, -s0[fr])
    for t, v in zip(fr, vals):
        u[t] = v
    sg = sig_of(u, h, a, k)
    viol = max([max(0.0, sg[t]) for t in range(N) if u[t] == 1.0] + [max(0.0, -sg[t]) for t in range(N) if u[t] == -1.0]) / h
    assert all(-1 < v < 1 for v in vals) and viol < 1e-9, (N, vals, viol)
    v1 = u[s1]
    th_right = s1 * h + (h * (1 + v1) / 2 if s1 in fr else 0.0)
    th_code = s1 * h + (h * (1 - v1) / 2 if s1 in fr else 0.0)
    br = s1 + r["break_minus_s1"]
    rec = dict(cfg=(r["t1"], r["t2"]), N=N, s1=s1, s1_fractional=s1 in fr, u_s1=round(float(v1), 4), kkt_viol_over_h=viol,
               break_minus_s1=r["break_minus_s1"], logged=r["break_time_minus_theta1"], code_formula=br * h - th_code,
               corrected=br * h - th_right)
    out.append(rec)
    print(json.dumps(rec))
# layer-law ratios and implied matching times with the corrected times (N > 1000)
for cfg, gam, eta in (((0.5, 1.5), 3.70, 0.59), ((0.55, 1.45), 3.58, 0.69), ((0.45, 1.55), 3.81, 0.49)):
    ratio = math.exp(-gam / eta)            # exp(-2 gamma / (Delta |eta|)), Delta = 2
    ts = [q["corrected"] for q in out if tuple(q["cfg"]) == cfg and q["N"] > 1000]
    print(json.dumps(dict(cfg=cfg, ratio=ratio, corrected_range=[min(ts), max(ts)],
                          implied_matching_time=[min(ts) / ratio, max(ts) / ratio])))
