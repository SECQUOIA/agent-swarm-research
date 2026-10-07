"""Confirmation recheck of scouting.md, second revision, R2: h_0 of the tilted,
transferred scalar-LQ family.  New code.

Differences from the author's Part B:
- P(t) is integrated numerically (solve_ivp, rtol 1e-12) to confirm the closed forms;
  the scan then uses the closed forms (dense-output interpolation error would blur the
  threshold at the largest N).
- The exactness test is PSD-ness of the full 2 x 2 stage Hessian, assembled entrywise
  (a - b^2/c >= 0 with c > 0), not the author's closed Riccati-map form F(s') - s.
- No bisection: a 600-point geometric grid up to N = 4e5 locates the last inexact grid
  N, then *every* N in [0.8 N_bad, 1.25 N_bad] is tested.
- For several cases the actual gap J^h - B(S^h) is computed at N_bad and N_bad + 1 by an
  exact box minimization of each quadratic stage residual (corners, edges, interior).

Problems: xdot = alpha x + u, l = (u^2 + q x^2)/2, Phi = phiT x^2/2, x0 = 1, T = 1,
U = [-5, 5], D_t = reachable interval.  Tilted curvature s = P - 2 eps exp(-lam t).
"""
import json
import os
import time

import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
t_start = time.time()
T, X0, UMAX = 1.0, 1.0, 5.0
CASES = {1: (-2.0, 0.0, 1.0), 2: (1.0, 1.0, 0.0)}
out = {"riccati_check": {}, "scan": [], "gap_check": []}


def riccati(cs):
    al, q, phiT = CASES[cs]
    sol = solve_ivp(lambda tt, P: P**2 - 2 * al * P - q, (T, 0.0), [phiT], rtol=1e-12, atol=1e-14,
                    dense_output=True, method="DOP853")
    return lambda tt: sol.sol(tt)[0]


def closed(cs, tt):
    if cs == 1:
        return 1.0 / (-0.25 + 1.25 * np.exp(4.0 * (T - tt)))
    c = T - np.arctanh(1 / np.sqrt(2)) / np.sqrt(2)
    return 1.0 - np.sqrt(2) * np.tanh(np.sqrt(2) * (tt - c))


PF = {}
for cs in CASES:
    PF[cs] = riccati(cs)
    tt = np.linspace(0, T, 5001)
    out["riccati_check"][cs] = float(np.max(np.abs(PF[cs](tt) - closed(cs, tt))))


def hessians(cs, N, eps, lam):
    al, q, _ = CASES[cs]
    h = T / N
    tt = h * np.arange(N + 1)
    s = closed(cs, tt) - 2 * eps * np.exp(-lam * tt)  # closed form, checked against the ODE
    A = 1 + al * h
    sn, sc = s[2:], s[1:-1]  # stages t = 1..N-1
    a = h * q + sn * A * A - sc
    b = sn * A * h
    c = h + sn * h * h
    return a, b, c, s


def exact(cs, N, eps, lam):
    a, b, c, s = hessians(cs, N, eps, lam)
    # PSD of [[a, b], [b, c]] with c > 0  <=>  a - b^2/c >= 0.  The tolerance is on the
    # margin scale (an absolute tolerance on the determinant a c - b^2 ~ h * margin
    # would be far too loose at large N; a first run with it shifted N_bad by ~1500).
    tol = 1e-14 * np.maximum(1.0, np.abs(s[1:-1]))
    return bool(np.all(c > 0) and np.all(a - b * b / c >= -tol))


def scan(cs, eps, lam):
    grid = np.unique(np.round(np.geomspace(4, 4e5, 600)).astype(int))
    ok = np.array([exact(cs, int(N), eps, lam) for N in grid])
    if ok.all():
        return {"N_bad": None, "grid_exact_above": True}
    nb = int(grid[~ok].max())
    lo, hi = max(4, int(0.8 * nb)), int(1.25 * nb) + 5
    full = [(N, exact(cs, N, eps, lam)) for N in range(lo, hi + 1)]
    bad_full = [N for N, o in full if not o]
    Nbad = max(bad_full + [nb])
    nonmono = [N for N, o in full if o and N < Nbad]
    return {"N_bad": Nbad, "grid_last_bad": nb, "grid_exact_above": bool(ok[grid > Nbad].all()),
            "exact_N_below_Nbad_in_window": len(nonmono), "window": [lo, hi]}


def qmin_box(a, b, c, gy, gv, ylo, yhi, vlo, vhi):
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
        y = (-c * gy + b * gv) / det
        v = (b * gy - a * gv) / det
        if ylo <= y <= yhi and vlo <= v <= vhi:
            cand.append((y, v))
    return min(f(y, v) for y, v in cand)


def gap_tilted(cs, N, eps, lam):
    """J^h - B(S^h) for the transferred tilted family, computed directly."""
    al, q, phiT = CASES[cs]
    h = T / N
    A = 1 + al * h
    Pd = np.empty(N + 1)
    Pd[N] = phiT
    for k in range(N - 1, -1, -1):
        Pd[k] = h * q + A * A * Pd[k + 1] / (1 + h * Pd[k + 1])
    x = np.empty(N + 1)
    u = np.empty(N)
    x[0] = X0
    for k in range(N):
        u[k] = -A * Pd[k + 1] * x[k] / (1 + h * Pd[k + 1])
        x[k + 1] = A * x[k] + h * u[k]
    p = Pd * x
    lo, hi = np.empty(N + 1), np.empty(N + 1)
    lo[0] = hi[0] = X0
    for k in range(N):
        lo[k + 1] = min(A * lo[k], A * hi[k]) - h * UMAX
        hi[k + 1] = max(A * lo[k], A * hi[k]) + h * UMAX
    _, _, _, s = hessians(cs, N, eps, lam)
    # S^h_t(x) = s_t (x - x_t)^2 / 2 + p_t (x - x_t)  (+ const); residual in y = x - x_t, v = u - u_t
    gap = 0.0
    for k in range(1, N):
        a = h * q + s[k + 1] * A * A - s[k]
        b = s[k + 1] * A * h
        c = h + s[k + 1] * h * h
        # gradient at (x_t, u_t): h q x + A (p_{t+1}) - p_t and h u + h p_{t+1}; both zero by KKT
        gy = h * q * x[k] + A * p[k + 1] - p[k]
        gv = h * u[k] + h * p[k + 1]
        m = qmin_box(a, b, c, gy, gv, lo[k] - x[k], hi[k] - x[k], -UMAX - u[k], UMAX - u[k])
        gap += -min(m, 0.0)
    return gap, float(np.max(np.abs(u))), bool(np.all(1 + h * s > 0))


for cs, lams in ((1, (1.0, 2.0, 4.0, 8.0)), (2, (4.0, 6.0, 8.0))):
    al, q, _ = CASES[cs]
    PT = float(PF[cs](T))
    for lam in lams:
        for eps in (0.5, 0.1, 0.02):
            eT = eps * np.exp(-lam * T)
            res = scan(cs, eps, lam)
            K = (PT - al) * (al * PT + q)
            pred0 = 4 * (lam / 2 - al + PT) / abs(K)
            pred = 4 * (lam / 2 - al + PT - eT) / abs(K)
            rec = {"case": cs, "lam": lam, "eps": eps, **res,
                   "ratio_h0_over_epsexp": (T / res["N_bad"] / eT) if res["N_bad"] else None,
                   "pred_eps0": pred0,
                   "measured_over_pred_at_eps": (T / res["N_bad"] / eT / pred) if res["N_bad"] else None}
            out["scan"].append(rec)
            print("scan", json.dumps(rec))

for cs, lam, eps in ((1, 1.0, 0.1), (1, 4.0, 0.5), (1, 8.0, 0.5), (2, 4.0, 0.1), (2, 8.0, 0.5)):
    Nbad = next(r["N_bad"] for r in out["scan"] if r["case"] == cs and r["lam"] == lam and r["eps"] == eps)
    for N in (Nbad, Nbad + 1):
        g, umax, pos = gap_tilted(cs, N, eps, lam)
        rec = {"case": cs, "lam": lam, "eps": eps, "N": N, "gap": g, "max|u|": umax, "1+hs>0": pos,
               "psd_test_exact": exact(cs, N, eps, lam)}
        out["gap_check"].append(rec)
        print("gap", json.dumps(rec))

out["runtime_s"] = time.time() - t_start
print("riccati_check", out["riccati_check"], "runtime_s", out["runtime_s"])
with open(os.path.join(HERE, "logs", "k2_tilted_h0.json"), "w") as fh:
    json.dump(out, fh, indent=1)
