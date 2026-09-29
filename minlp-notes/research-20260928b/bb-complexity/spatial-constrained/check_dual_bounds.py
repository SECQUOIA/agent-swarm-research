"""Validate the Lagrangian-dual node bounds of sbb_sphere.py against a primal solve.

For random boxes, compares the dual bound with the best of 5 SLSQP runs on the
primal node problem.  A valid bound satisfies bound <= primal; a tight one has
primal - bound ~ 0.  Reports max(bound - primal) and any gap above 1e-6.
Usage: python3 check_dual_bounds.py
"""
import numpy as np
from scipy.optimize import minimize
from sbb_sphere import Relax

rng = np.random.default_rng(0)
cases = [("S3_circ sphere", Relax(3, [1.0, 1.0, 0.5], "sphere")),
         ("S3_circ ball", Relax(3, [1.0, 1.0, 0.5], "ball")),
         ("S2_quart sphere", Relax(2, [1.0, 1.0], "sphere", [0.0, 1.0]))]
for name, R in cases:
    n = R.n
    worst, gaps, cnt = -np.inf, 0, 0
    for t in range(300):
        c0 = rng.uniform(-1.1, 1.1, n); w = rng.uniform(0.01, 0.8, n)
        l, u = c0 - w / 2, c0 + w / 2
        if R.quick_infeasible(l, u):
            continue
        lb, _ = R.lower_bound(l, u, np.zeros(2))
        a = R.alpha
        obj = lambda y: np.sum(-R.c * y * y + R.e * y ** 4 - a * (y - l) * (u - y))
        cons = [{"type": "ineq", "fun": lambda y: 1 - y @ y}]
        if R.kind == "sphere":
            cons.append({"type": "ineq", "fun": lambda y: np.sum((l + u) * y - l * u) - 1})
        best = np.inf
        for s in range(5):
            r = minimize(obj, rng.uniform(l, u), method="SLSQP", bounds=list(zip(l, u)),
                         constraints=cons, options={"ftol": 1e-14, "maxiter": 500})
            if r.success and all(cc["fun"](r.x) > -1e-9 for cc in cons):
                best = min(best, r.fun)
        if np.isfinite(best):
            cnt += 1
            worst = max(worst, lb - best)
            gaps += int(best - lb > 1e-6)
    print(f"{name}: boxes with a primal solution = {cnt}, max(bound - primal) = {worst:.2e}, "
          f"boxes with primal - bound > 1e-6: {gaps}")
