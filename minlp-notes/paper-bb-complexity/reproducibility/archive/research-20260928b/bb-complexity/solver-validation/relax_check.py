"""Check that SCIP's root relaxation equals the secant (DC) relaxation the
(G_alpha) analysis assumes: python3 relax_check.py > results/relax_check.log

SCIP: root node only (limits/nodes=1), presolve, propagation, OBBT and
heuristics off, so the box is the original one. Independent bound: minimize
the convex underestimator (convex parts exact, concave quadratic parts
replaced by secants, x1*x2 by its McCormick envelope) over the box with
scipy (convex problem, so a local solver gives the global minimum).
Floating point only.
"""
import os
import sys

import numpy as np
import pyscipopt
from pyscipopt import SCIP_PARAMSETTING
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from instances import INSTANCES, cip_text  # noqa: E402
from run_one import BASE, PROP_OFF  # noqa: E402


def sec(l, u):
    """Secant of y^2 on [l, u] (overestimator)."""
    return lambda y: (l + u) * y - l * u


def sec4(l, u):
    """Secant of y^4 on [l, u]."""
    return lambda y: l ** 4 + (u ** 4 - l ** 4) / (u - l) * (y - l)


def relax(name):
    b = INSTANCES[name]["bounds"]
    (l1, u1) = b[0]
    s1 = sec(l1, u1)
    if name == "iso2":
        (l2, u2) = b[1]
        s2 = sec(l2, u2)
        return lambda x: (x[0] ** 4 - 1.5 * s1(x[0]) - 1.0 * x[0] + 1.5
                          + x[1] ** 4 - 1.3 * s2(x[1]) - 1.4 * x[1] + 1.7)
    if name == "linediag2":
        (l2, u2) = b[1]
        s2 = sec(l2, u2)
        mc = lambda x: max(l2 * x[0] + l1 * x[1] - l1 * l2, u2 * x[0] + u1 * x[1] - u1 * u2)  # noqa: E731
        # -1.5 (x1-x2)^2 = -1.5 x1^2 - 1.5 x2^2 + 3 x1 x2
        return lambda x: ((x[0] - x[1]) ** 4 - 1.5 * s1(x[0]) - 1.5 * s2(x[1]) + 3 * mc(x)
                          - (x[0] - x[1]) + 1.5)
    if name in ("qflat2a", "lineaxis2"):
        (l2, u2) = b[1]
        s2, s24 = sec(l2, u2), sec4(l2, u2)
        d = 0.375
        g = lambda y: (y + d) ** 4 + (y - d) ** 4 - 12 * d * d * s2(y) - 2 * d ** 4  # noqa: E731
        extra = (lambda y: -2 * s24(y)) if name == "lineaxis2" else (lambda y: 0.0)
        return lambda x: (x[0] ** 4 - 1.5 * s1(x[0]) - 1.0 * x[0] + 1.5 + g(x[1]) + extra(x[1]))
    if name == "qflat1":
        d = 0.375
        return lambda x: (x[0] + d) ** 4 + (x[0] - d) ** 4 - 12 * d * d * s1(x[0]) - 2 * d ** 4
    raise KeyError(name)


def dc_bound(name):
    f = relax(name)
    b = INSTANCES[name]["bounds"]
    best = np.inf
    rng = np.random.default_rng(0)
    for _ in range(20):
        x0 = [rng.uniform(lo, hi) for lo, hi in b]
        r = minimize(f, x0, bounds=b, method="L-BFGS-B" if name != "linediag2" else "Powell",
                     options={"ftol": 1e-14} if name == "linediag2" else {"ftol": 1e-15, "gtol": 1e-12})
        best = min(best, r.fun)
    return best


def scip_root(name):
    d = INSTANCES[name]
    path = f"/tmp/relax_{name}.cip"
    open(path, "w").write(cip_text(d))
    m = pyscipopt.Model()
    m.hideOutput()
    m.readProblem(path)
    for k, v in {**BASE, **d["params"], **PROP_OFF, "limits/nodes": 1,
                 "propagating/obbt/freq": -1}.items():
        m.setParam(k, v)
    m.setPresolve(SCIP_PARAMSETTING.OFF)
    m.setHeuristics(SCIP_PARAMSETTING.OFF)
    m.optimize()
    return m.getDualbound()


if __name__ == "__main__":
    for name in ("qflat1", "iso2", "linediag2", "lineaxis2", "qflat2a"):
        dc, sr = dc_bound(name), scip_root(name)
        print(f"{name:10s} secant/McCormick bound {dc:+.8f}  SCIP root dual bound {sr:+.8f}  "
              f"difference {sr - dc:+.2e}")
