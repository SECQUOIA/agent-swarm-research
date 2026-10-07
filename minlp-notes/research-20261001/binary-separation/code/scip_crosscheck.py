"""Independent floating-point cross-check of Theorem 1 with SCIP (PySCIPOpt).

For random X3C instances, minimize g(z) = z^T (4M) z - sum_i (4M)_ii z_i over integer z in a
box that contains every z with g(z) < 0. The box comes from the ellipsoid
(z - w)^T M (z - w) < w^T M w, w = M^{-1} diag(M) / 2, so |z_i - w_i| < sqrt(R (M^{-1})_ii).
Theorem 1 predicts: minimum -2 (that is, 4 * (-1/2)) if an exact cover exists, else 0.
SCIP runs single-threaded. This check does not use the exact enumeration code.
"""
import math
import random
import sys

import numpy as np
from pyscipopt import Model, quicksum

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from check_binary_separation import build_M, exact_covers  # noqa: E402

random.seed(7)


def instance(q, nsets):
    p = 3 * q
    U = list(range(p))
    sets = [tuple(sorted(random.sample(U, 3))) for _ in range(nsets)]
    if random.random() < 0.5:
        random.shuffle(U)
        sets[:q] = [tuple(sorted(U[3 * k:3 * k + 3])) for k in range(q)]
    random.shuffle(sets)
    return sets, p


def solve(sets, p):
    from fractions import Fraction as F
    M = build_M(sets, p, F(p - 1, 4))
    Mf = np.array([[float(a) for a in row] for row in M])
    N = len(M)
    delta = np.diag(Mf)
    w = np.linalg.solve(Mf, delta / 2)
    R = float(w @ Mf @ w)
    Minv = np.linalg.inv(Mf)
    lo = [math.floor(w[i] - math.sqrt(R * Minv[i, i])) - 1 for i in range(N)]
    hi = [math.ceil(w[i] + math.sqrt(R * Minv[i, i])) + 1 for i in range(N)]
    G = 4 * Mf
    m = Model()
    m.hideOutput()
    m.setParam("parallel/maxnthreads", 1)
    m.setParam("limits/time", 120)
    z = [m.addVar(vtype="I", lb=lo[i], ub=hi[i]) for i in range(N)]
    t = m.addVar(lb=None)
    m.addCons(t >= quicksum(G[i, j] * z[i] * z[j] for i in range(N) for j in range(N))
              - quicksum(G[i, i] * z[i] for i in range(N)))
    m.setObjective(t, "minimize")
    m.optimize()
    return m.getStatus(), m.getObjVal(), [round(m.getVal(v)) for v in z], max(hi[i] - lo[i] for i in range(N))


if __name__ == "__main__":
    bad = 0
    rows = []
    for k in range(24):
        q = 3 if k < 16 else 4
        sets, p = instance(q, random.randint(q, q + 4))
        covers = exact_covers(sets, p)
        status, val, zbest, width = solve(sets, p)
        want = -2.0 if covers else 0.0
        ok = status == "optimal" and abs(val - want) < 1e-6
        bad += not ok
        rows.append((q, len(sets), bool(covers), status, round(val, 9), width, ok))
        print(f"q={q} n={len(sets)} cover={bool(covers)} status={status} min={val:.9f} box_width<={width} ok={ok}")
    print(f"[scip crosscheck] {len(rows)} X3C instances: {bad} disagreements with Theorem 1")
    sys.exit(0 if bad == 0 else 1)
