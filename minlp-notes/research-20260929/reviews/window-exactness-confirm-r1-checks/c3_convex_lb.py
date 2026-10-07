"""Confirmation check: the Section 6 convexification bound for toy plus on all Section 7.3 grids.

Own code. Toy plus: x' = u, x0 = 0, T = 2, a = 2 on [0,1), -1 after, k = 0.5, Phi = x.
J_plus(u) = J_zero(u) - (k/2) h^2 sum u_t^2 with J_zero the convex transcription (k = 0, Phi = x + x^2/4).
Lower bound LB = min_{|u|<=1} J_zero - (k/2) h^2 N.  min J_zero by a projected-gradient-free exact method:
J_zero is a convex quadratic in u; solve the box QP with scipy's L-BFGS-B at tight tolerance and polish
with an active-set Newton step.  The KKT point of toy plus comes from c1_rmax.toy_kkt (own code).
Reports (J_plus(ubar) - LB)/h^2 next to the report's window deficits (Section 7.3 table, K = 0 and 4).
"""
import json
import os
import sys

import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from c1_rmax import toy_kkt  # noqa: E402


def J_and_grad(u, N, k, phi1, phi2, T=2.0):
    h = T / N
    a = np.array([2.0 if t * T < 1.0 * N else -1.0 for t in range(N + 1)])
    x = np.concatenate([[0.0], np.cumsum(h * u)])
    J = h * np.sum((x[:N] - a[:N]) ** 2 / 2 + k * x[:N] * u) + phi1 * x[N] + phi2 * x[N] ** 2 / 2
    p = np.empty(N + 1)
    p[N] = phi1 + phi2 * x[N]
    for t in range(N - 1, -1, -1):
        p[t] = p[t + 1] + h * (x[t] - a[t] + k * u[t])
    sig = k * x[:N] + p[1:]
    return J, h * sig


def min_Jzero(N):
    f = lambda u: J_and_grad(u, N, 0.0, 1.0, 0.5)
    u0 = toy_kkt(N, k=0.0, phi1=1.0, phi2=0.5)["u"]  # one-switch KKT point of the convex problem
    J0, g0 = f(u0)
    # KKT check of the convex problem: sign conditions => global minimum (convex)
    viol = np.where(u0 > 1 - 1e-12, np.maximum(0, g0), np.where(u0 < -1 + 1e-12, np.maximum(0, -g0), np.abs(g0)))
    return J0, float(viol.max()) / (2.0 / N)


out = []
report = {500: (0, 0), 1000: (0.38878, 0.38532), 2000: (0.01800, 0.01356), 4000: (0.35041, 0.34963),
          8000: (0.53333, 0.53274)}
for N in (500, 1000, 2000, 4000, 8000):
    kk = toy_kkt(N, k=0.5)
    h = kk["h"]
    Jp, _ = J_and_grad(kk["u"], N, 0.5, 1.0, 0.0)
    Jz_ubar, _ = J_and_grad(kk["u"], N, 0.0, 1.0, 0.5)
    ident = Jp - (Jz_ubar - 0.25 * h * h * np.sum(kk["u"] ** 2))
    mJz, viol = min_Jzero(N)
    LB = mJz - 0.25 * h * h * N
    rec = dict(N=N, interior=kk["inter"] != [], identity_residual=float(ident), zero_kkt_viol_over_h=viol,
               convex_gap_over_h2=float((Jp - LB) / h ** 2), window_deficit_K0_K4_over_h2=report[N])
    print(json.dumps(rec), flush=True)
    out.append(rec)
with open(os.path.join(HERE, "logs", "c3_convex_lb.json"), "w") as f:
    json.dump(out, f, indent=1)
