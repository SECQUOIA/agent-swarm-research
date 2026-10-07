"""Independent floating-point rechecks of the closed-form certificates, by different routes:

camshape: (a) Chebyshev values U_m(c/2) = sin((m+1) th)/sin th with th = arccos(c/2) are
  positive iff n*th < pi; (b) the relaxation  max sum r  s.t. r_j <= min(R_j, ub_j),
  |r_{j+1} - r_j| <= alpha (j >= 2), lb <= r  is solved as an LP with HiGHS and compared
  with the envelope value; R_j from the closed form S_j = cos(j th) + (1/ub_1 - cos th) sin(j th)/sin th.
lnts: the convex program  max sum_j w_j cos th_j  s.t.  sum w_j sin th_j = 0,
  sum c_j sin th_j >= B(h2)  (written with s_j = sin th_j, cos th_j = sqrt(1 - s_j^2))
  is solved with cvxpy at h2 = certified bound / N; its value must be < A(h2).
"""
import json

import cvxpy as cp
import numpy as np
from scipy.optimize import linprog

from camshape_model import extract
from lnts_bound import weights


def camshape(n):
    m = extract(n)
    c, alpha, ub, lb = m["c"], m["alpha"], m["ub"], m["lb"]
    th = np.arccos(c / 2)
    j = np.arange(0, n + 1)
    S = np.cos(j * th) + (1 / ub[0] - np.cos(th)) * np.sin(j * th) / np.sin(th)
    R = 1 / S[1:]
    Bup = np.minimum(R, ub)
    # LP: variables r_1..r_n
    A, b = [], []
    for k in range(1, n - 1):  # 0-based pair (k, k+1) = 1-based (k+1, k+2), constrained for 1-based >= 2
        row = np.zeros(n); row[k + 1] = 1; row[k] = -1
        A.append(row); b.append(alpha); A.append(-row); b.append(alpha)
    res = linprog(-np.ones(n), A_ub=np.array(A), b_ub=np.array(b), bounds=list(zip(lb, Bup)), method="highs")
    return dict(n=n, n_theta_over_pi=float(n * th / np.pi), lp_status=res.status,
                dual_bound_lp=float(-m["c0"] * (-res.fun)))


def lnts(name, N, dual_bound, rel=1e-5):
    """Bracket the feasibility threshold in h with an independent convex solver:
    at h = h2 (1 - rel) the relaxation must be infeasible (max < A), at h2 (1 + rel) feasible."""
    w, cc = weights(N)
    w = np.array([float(x) for x in w]); cc = np.array([float(x) for x in cc])
    h2 = dual_bound / N
    out = dict(name=name, h2=h2)
    for tag, hh in (("below", h2 * (1 - rel)), ("above", h2 * (1 + rel))):
        A, B = 45 / (100 * hh), 5 / (100 * hh ** 2)
        s = cp.Variable(N + 1)
        prob = cp.Problem(cp.Maximize(w @ cp.sqrt(1 - cp.square(s))), [w @ s == 0, cc @ s >= B, s >= -1, s <= 1])
        prob.solve()
        out[tag] = dict(h=hh, max_sum_w_cos=float(prob.value), A=A, relaxation_feasible=bool(prob.value >= A))
    out["bracket_ok"] = (not out["below"]["relaxation_feasible"]) and out["above"]["relaxation_feasible"]
    return out


if __name__ == "__main__":
    out = []
    for n in (100, 200, 400, 800):
        r = camshape(n)
        cert = json.load(open(f"logs/camshape{n}_bound.json"))
        r["dual_bound_certified"] = cert["dual_bound"]
        out.append(r); print(json.dumps(r), flush=True)
    for name, N in (("lnts50", 50), ("lnts100", 100), ("lnts200", 200), ("lnts400", 400)):
        cert = json.load(open(f"logs/lnts_{name}.json"))
        r = lnts(name, N, cert["dual_bound"])
        out.append(r); print(json.dumps(r), flush=True)
    json.dump(out, open("logs/verify_independent.json", "w"), indent=1)
