"""Soundness test of the full per-box pipeline of ann_tm (SepModel.fbound_combo: separate-symbol
Taylor models, LP dual, domain reduction with the objective cut, interval passes).

For each test box B, the pipeline is called with a cutoff UBt (the objective cut uses UBt) and
returns a bound lb, an infeasibility flag and a reduced box B'.  The claim tested:
  every point p in B that is feasible for R with f(p) <= UBt satisfies
      f(p) >= lb   and   p in B'.
UBt = UB + 300 and UBt = +inf are used (with UBt = UB almost no feasible test point would
qualify, since UB is (near) the global minimum).
Points: box centre, random points, and local minimizers of f over B subject to the sides
(SLSQP started from random points of B), so the tight cases are probed.  Feasibility and f are
evaluated in floats; any float-level violation or near-violation (margin < 1e-6 relative) is
re-evaluated with 50-digit mpmath forward propagation (ann_point.build) before it is counted.

    python3 test_tm2.py [nbox_per_family] [model: sep-gradsmall | sep-nofull]
"""
import sys
import time

import mpmath as mp
import numpy as np
from scipy.optimize import minimize

import ann_tm as at

NB = int(sys.argv[1]) if len(sys.argv) > 1 else 40
model = sys.argv[2] if len(sys.argv) > 2 else "sep-gradsmall"
M = at.SepModel()
M.full_mu = False
if model == "sep-gradsmall":
    M.old_min_relw = 1.0 / 16
    M.grad_small = True
UB, uinc = at.incumbent(M)
M.lag, _ = at.kkt_lag(M, uinc)
N = M.names
SIDES = list(M.sides)
sc = M.hi0 - M.lo0
rng = np.random.default_rng(11)


def fval(p):
    f, g, X, G = M.ffun(p)
    slack = min(s * (X[j] - b) for j, s, b in SIDES)
    return f, slack, g, X, G


def exact(p):
    """50-digit objective and minimal side slack by mpmath forward propagation of R."""
    import ann_model as am
    D = M.D
    with mp.workdps(50):
        x = [None] * len(N)
        for i, j in enumerate(D["inputs"]):
            x[j] = mp.mpf(float(p[i]))
        q = lambda F: mp.mpf(F.numerator) / F.denominator
        for op in D["ops"]:
            if op[0] == "lin":
                _, v, cv, terms, rhs = op
                s_ = q(rhs)
                for o, a in terms:
                    s_ -= q(a) * x[o]
                x[v] = s_ / q(cv)
            else:
                x[op[1]] = mp.tanh(x[op[2]])
        f = am.evaluate_objective(D, x, lambda c: q(c) if not isinstance(c, (int, float)) else mp.mpf(c))
        slack = min(s * (x[j] - mp.mpf(b)) for j, s, b in SIDES)
        return f, slack


def local_min_in_box(lo, hi, u0):
    cj = [(j, s, b) for j, s, b in SIDES]

    def fun(u):
        f, g, X, G = M.ffun(u)
        return f, g

    def cons(u):
        f, g, X, G = M.ffun(u)
        return np.array([s * (X[j] - b) for j, s, b in cj])

    def jac(u):
        f, g, X, G = M.ffun(u)
        return np.array([s * G[j] for j, s, b in cj])
    try:
        r = minimize(fun, u0, jac=True, bounds=list(zip(lo, hi)), method="SLSQP",
                     constraints=[dict(type="ineq", fun=cons, jac=jac)], options=dict(maxiter=100, ftol=1e-12))
        return np.clip(r.x, lo, hi)
    except Exception:
        return u0


def families():
    ropt = (uinc - M.lo0) / sc
    out = []
    for rho in [0.1, 0.03, 0.01, 0.003, 0.001]:
        c = uinc + rho * sc * rng.uniform(-1, 1, (NB, 5))
        r = 0.5 * rho * sc * rng.uniform(0.5, 1.5, (NB, 5))
        out.append((f"near-opt rho={rho}", np.maximum(c - r, M.lo0), np.minimum(c + r, M.hi0)))
    Z = np.load("ext_logs/open1800_v1.npz")
    idx = rng.choice(len(Z["key"]), NB, replace=False)
    out.append(("frontier boxes (1800 s)", Z["lo"][idx], Z["hi"][idx]))
    lo, hi = Z["lo"][idx], Z["hi"][idx]
    mid = 0.5 * (lo + hi)
    out.append(("frontier halves", lo, np.where(np.arange(5)[None] == rng.integers(0, 5, (NB, 1)), mid, hi)))
    c = M.lo_in + sc * rng.random((NB, 5)); r = 0.5 * 0.05 * sc
    out.append(("uniform rho=0.05", np.maximum(c - r, M.lo0), np.minimum(c + r, M.hi0)))
    return out


viol = 0; checked = 0; minmargin = np.inf; t0 = time.time()
fams = families()
for UBt in [UB + 300.0, np.inf]:
    for name0, lo, hi in fams:
        name = f"{name0} UBt={UBt:.1f}"
        R = M.fbound_combo(lo, hi, UBt)
        nfeas = 0
        for k in range(lo.shape[0]):
            pts = [0.5 * (lo[k] + hi[k])] + list(lo[k] + (hi[k] - lo[k]) * rng.random((8, 5)))
            pts += [local_min_in_box(lo[k], hi[k], lo[k] + (hi[k] - lo[k]) * rng.random(5)) for _ in range(3)]
            for p in pts:
                f, slack, *_ = fval(p)
                if slack < -1e-9 or f > UBt:
                    continue
                nfeas += 1
                checked += 1
                inside = (np.all(p >= R["newlo"][k]) and np.all(p <= R["newhi"][k])) or not R["mod"][k]
                margin = f - R["lb"][k]
                minmargin = min(minmargin, margin)
                if (margin < 1e-6 * abs(f)) or not inside:
                    fe, se = exact(p)
                    if se >= 0 and fe <= UBt and (fe < R["lb"][k] or not inside):
                        viol += 1
                        print(f"  VIOLATION {name} box {k}: f {fe} lb {R['lb'][k]} inside-reduced {inside}", flush=True)
        print(f"{name:40s}: boxes {lo.shape[0]}, infeasible/emptied {np.mean(~np.isfinite(R['lb'])):.2f}, "
              f"feasible test points {nfeas}, reduced {np.mean(R['mod']):.2f}  ({time.time()-t0:.0f}s)", flush=True)
print(f"soundness: {viol} violations among {checked} feasible points with f <= UBt; smallest f - lb = {minmargin:.4g}")
