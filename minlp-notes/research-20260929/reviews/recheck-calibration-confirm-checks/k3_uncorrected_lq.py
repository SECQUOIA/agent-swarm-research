"""Confirmation recheck of scouting.md, second revision, R6: loss of the uncorrected
sampled field family S_t = V(t_t, .) = P(t_t) x^2 / 2 for xdot = -2x + u, l = u^2/2,
Phi = x^2/2, x0 = 1, T = 1, U = [-5, 5], D_t = reachable interval.  New code.

P is integrated numerically (solve_ivp, DOP853, rtol 1e-13).  Each stage residual is a
2-D quadratic in (x, u), minimized exactly over the box D_t x U by enumerating the
interior stationary point, the minimizers on the four edges and the four corners.
Also the transferred field family (affine correction) for comparison with the review's
c4 numbers, and the tilted uncorrected family's gap / h^2 (lam = 1, eps = 0.5) as a
strict-case contrast.
"""
import json
import os
import time

import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
t_start = time.time()
AL, Q, PHIT, T, X0, UMAX = -2.0, 0.0, 1.0, 1.0, 1.0, 5.0
sol = solve_ivp(lambda t, P: P**2 - 2 * AL * P - Q, (T, 0.0), [PHIT], method="DOP853",
                rtol=1e-13, atol=1e-15, dense_output=True)
Pc = lambda t: sol.sol(t)[0]


def box_min(a, b, c, gy, gv, ylo, yhi, vlo, vhi):
    f = lambda y, v: 0.5 * (a * y * y + 2 * b * y * v + c * v * v) + gy * y + gv * v
    cand = [(y, v) for y in (ylo, yhi) for v in (vlo, vhi)]
    for y in (ylo, yhi):
        if c > 0:
            cand.append((y, min(max(-(b * y + gv) / c, vlo), vhi)))
    for v in (vlo, vhi):
        if a > 0:
            cand.append((min(max(-(b * v + gy) / a, ylo), yhi), v))
    det = a * c - b * b
    if a > 0 and det > 0:
        y, v = (-c * gy + b * gv) / det, (b * gy - a * gv) / det
        if ylo <= y <= yhi and vlo <= v <= vhi:
            cand.append((y, v))
    return min(f(y, v) for y, v in cand)


def run(N, kind, lam=None, eps=None):
    h = T / N
    A = 1 + AL * h
    Pd = np.empty(N + 1)
    Pd[N] = PHIT
    for k in range(N - 1, -1, -1):
        Pd[k] = h * Q + A * A * Pd[k + 1] / (1 + h * Pd[k + 1])
    x, u = np.empty(N + 1), np.empty(N)
    x[0] = X0
    for k in range(N):
        u[k] = -A * Pd[k + 1] * x[k] / (1 + h * Pd[k + 1])
        x[k + 1] = A * x[k] + h * u[k]
    assert np.max(np.abs(u)) < UMAX
    p = Pd * x
    lo, hi = np.empty(N + 1), np.empty(N + 1)
    lo[0] = hi[0] = X0
    for k in range(N):
        lo[k + 1] = min(A * lo[k], A * hi[k]) - h * UMAX
        hi[k + 1] = max(A * lo[k], A * hi[k]) + h * UMAX
    tt = h * np.arange(N + 1)
    s2 = Pc(tt)
    s1 = np.zeros(N + 1)
    if kind == "transferred":
        s1 = p - s2 * x  # S^h_t(x) = s2 x^2/2 + s1 x has gradient p_t at x_t
    elif kind == "tilted_uncorrected":
        # continuous x*(t): xdot* = (AL - P) x*; S = P x^2/2 - e (x - x*)^2, no correction
        xs_sol = solve_ivp(lambda t, y: (AL - Pc(t)) * y, (0.0, T), [X0], method="DOP853",
                           rtol=1e-13, atol=1e-15, dense_output=True)
        xs = xs_sol.sol(tt)[0]
        e = eps * np.exp(-lam * tt)
        s2 = s2 - 2 * e
        s1 = 2 * e * xs
    gap = 0.0
    for k in range(N):
        # rho_k(x,u) = h(u^2 + Q x^2)/2 + S_{k+1}(A x + h u) - S_k(x) in (y, v) = (x - x_k, u - u_k)
        a = h * Q + s2[k + 1] * A * A - s2[k]
        b = s2[k + 1] * A * h
        c = h + s2[k + 1] * h * h
        xn = A * x[k] + h * u[k]
        gy = h * Q * x[k] + A * (s2[k + 1] * xn + s1[k + 1]) - (s2[k] * x[k] + s1[k])
        gv = h * u[k] + h * (s2[k + 1] * xn + s1[k + 1])
        if k == 0:
            m = box_min(a, b, c, gy, gv, 0.0, 0.0, -UMAX - u[0], UMAX - u[0])
        else:
            m = box_min(a, b, c, gy, gv, lo[k] - x[k], hi[k] - x[k], -UMAX - u[k], UMAX - u[k])
        gap += -min(m, 0.0)
    # terminal residual Phi - S_N in y = x - x_N
    cN = PHIT - s2[N]
    bN = PHIT * x[N] - (s2[N] * x[N] + s1[N])
    fN = lambda y: 0.5 * cN * y * y + bN * y
    cands = [lo[N] - x[N], hi[N] - x[N]]
    if cN > 0:
        cands.append(min(max(-bN / cN, cands[0]), cands[1]))
    gap += -min(min(fN(y) for y in cands), 0.0)
    return gap


rows = []
for N in (10, 20, 40, 80, 160, 320, 640):
    gu = run(N, "uncorrected")
    gt = run(N, "transferred")
    gtu = run(N, "tilted_uncorrected", lam=1.0, eps=0.5)
    rec = {"N": N, "uncorrected_gap": gu, "uncorrected_gap_over_h": gu * N,
           "transferred_gap": gt, "tilted_uncorrected_gap_over_h2": gtu * N * N}
    rows.append(rec)
    print(json.dumps(rec))

# comparison with the author's Part C, the recheck's r2 part C and the review's c4
ROOT = os.path.dirname(os.path.dirname(HERE))
auth = {r["N"]: r for r in json.load(open(os.path.join(ROOT, "theory-calibration", "logs", "recheck_revision_checks.json")))["C"]}
r2 = {}
for line in open(os.path.join(ROOT, "reviews", "calibration-recheck-checks", "logs", "r2_tilted_lq.log")):
    if line.startswith("C "):
        d = json.loads(line[2:])
        r2[d["N"]] = d
c4 = {}
for line in open(os.path.join(ROOT, "reviews", "calibration-review-checks", "logs", "c4_nonstrict_lq_gap.log")):
    d = json.loads(line)
    if d["alpha"] == -2.0:
        c4[d["N"]] = d
cmp_ = []
for r in rows:
    N = r["N"]
    rec = {"N": N,
           "unc_minus_author": r["uncorrected_gap"] - auth[N]["uncorrected_field_gap"],
           "unc_minus_recheck_r2": r["uncorrected_gap"] - r2[N]["uncorrected_field_gap"],
           "transferred_minus_author": r["transferred_gap"] - auth[N]["transferred_field_gap"],
           "transferred_minus_review_c4": (r["transferred_gap"] - c4[N]["field_gap"]) if N in c4 else None,
           "author_transferred_minus_c4": (auth[N]["transferred_field_gap"] - c4[N]["field_gap"]) if N in c4 else None,
           "author_unc_minus_r2": auth[N]["uncorrected_field_gap"] - r2[N]["uncorrected_field_gap"]}
    cmp_.append(rec)
    print("cmp", json.dumps(rec))
out = {"rows": rows, "comparison": cmp_, "runtime_s": time.time() - t_start}
print("runtime_s", out["runtime_s"])
with open(os.path.join(HERE, "logs", "k3_uncorrected_lq.json"), "w") as fh:
    json.dump(out, fh, indent=1)
