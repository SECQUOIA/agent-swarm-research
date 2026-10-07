"""Round-2 literature review: does the dense SDP + all-McCormick relaxation
close the three-leaf star example of Section 3.5?

The introduction and the conclusions generalize Burer, Natarajan and
Willemsen (2025, Thm. 1; n <= 3) to "the advantage of joint blocks over their
pairs is one of representation".  This script tests that generalization on
the paper's own four-variable star (Section 3.5): leaves x1, x2, x3 in [0,1],
center y in [0,2], q_i = (y - a_i1 - (a_i2 - a_i1) x_i)^2 + w_i x_i (1 - x_i)
with A_1 = {0,1}, A_2 = {1,2}, A_3 = {0,2}.  The true minimum of sum q_i is
2/3 (Section 3.5).  We compute
  (a) the dense Shor relaxation of (1, y, x1, x2, x3) with all McCormick
      (RLT bound-factor) inequalities of every pair, including the nonedges
      x_i x_j, and the box RLT of the squares;
  (b) the same plus the triangle inequalities on the binary-like leaves is
      NOT added (we stay with SDP + RLT).
Numerical solve with Clarabel (interior point); the result is a numerical
lower bound, reported with the solver status.  A gap well above solver
accuracy shows that SDP + McCormick of all products is not exact for this
star, so BNW's n <= 3 theorem does not extend to the merged blocks of
Section 3.5.
"""
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

import cvxpy as cp
import numpy as np


def build(A, w, y_ub):
    k = len(A)
    n = k + 1  # index 0 = y, 1..k = x_i
    lo = np.zeros(n)
    hi = np.array([y_ub] + [1.0] * k)
    M = cp.Variable((n + 1, n + 1), symmetric=True)  # moment matrix of (1, v)
    v = M[0, 1:]
    V = M[1:, 1:]
    cons = [M >> 0, M[0, 0] == 1]
    for i in range(n):
        cons += [v[i] >= lo[i], v[i] <= hi[i]]
    # RLT / McCormick for every pair (i<=j), from bound factors
    for i, j in itertools.combinations_with_replacement(range(n), 2):
        cons += [
            V[i, j] - lo[j] * v[i] - lo[i] * v[j] + lo[i] * lo[j] >= 0,
            V[i, j] - hi[j] * v[i] - hi[i] * v[j] + hi[i] * hi[j] >= 0,
            V[i, j] - hi[j] * v[i] - lo[i] * v[j] + lo[i] * hi[j] <= 0,
            V[i, j] - lo[j] * v[i] - hi[i] * v[j] + hi[i] * lo[j] <= 0,
        ]
    # objective: sum_i (y - a1 - d x_i)^2 + w_i x_i (1 - x_i), linearized
    obj = 0
    for idx, (a1, a2) in enumerate(A):
        d = a2 - a1
        xi = idx + 1
        # (y - a1 - d x)^2 = y^2 + a1^2 + d^2 x^2 - 2 a1 y - 2 d y x + 2 a1 d x
        obj += V[0, 0] + a1 ** 2 + d ** 2 * V[xi, xi] - 2 * a1 * v[0] - 2 * d * V[0, xi] + 2 * a1 * d * v[xi]
        obj += w[idx] * (v[xi] - V[xi, xi])
    return cp.Problem(cp.Minimize(obj), cons)


def true_min(A, y_ub, grid=200001):
    ys = np.linspace(0, y_ub, grid)
    tot = np.zeros_like(ys)
    for a1, a2 in A:
        tot += np.minimum((ys - a1) ** 2, (ys - a2) ** 2)
    return float(tot.min())


def main():
    out = {}
    A = [(0.0, 1.0), (1.0, 2.0), (0.0, 2.0)]
    for label, w in (("w=(a2-a1)^2", [1.0, 1.0, 4.0]), ("w=4", [4.0, 4.0, 4.0])):
        prob = build(A, w, 2.0)
        val = prob.solve(solver=cp.CLARABEL)
        out[label] = {"status": prob.status, "dense_sdp_all_mccormick": val,
                      "true_min_grid": true_min(A, 2.0), "true_min_exact": str(Fraction(2, 3))}
    # control: the three-variable path of Proposition 3.1 (BNW applies; expect 1/128)
    Ap = [(0.25, 0.75), (0.0, 0.625)]
    prob = build(Ap, [1.0, 1.0], 1.0)
    val = prob.solve(solver=cp.CLARABEL)
    out["control_path_prop31"] = {"status": prob.status, "dense_sdp_all_mccormick": val,
                                  "true_min_exact": str(Fraction(1, 128)), "true_min_float": 1 / 128}
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__" and len(sys.argv) == 1:
    sys.exit(main())


# ---------------------------------------------------------------------------
# Random trees on four box variables: is dense SDP + all McCormick exact?
# ---------------------------------------------------------------------------

def box_qp_min(Q, c):
    """Exact-in-floating-point minimum of x'Qx + c'x over [0,1]^n by face
    enumeration (Theorem 4.1 specialized to the box)."""
    n = len(c)
    best = np.inf
    for pattern in itertools.product((0, 1, 2), repeat=n):  # 0 lb, 1 ub, 2 free
        x = np.array([0.0 if p == 0 else 1.0 for p in pattern])
        free = [i for i, p in enumerate(pattern) if p == 2]
        if free:
            fixed = [i for i in range(n) if i not in free]
            H = 2 * Q[np.ix_(free, free)]
            rhs = -(c[free] + 2 * Q[np.ix_(free, fixed)] @ x[fixed])
            if abs(np.linalg.det(H)) < 1e-12:
                continue
            xf = np.linalg.solve(H, rhs)
            if np.any(xf < -1e-12) or np.any(xf > 1 + 1e-12):
                continue
            x[free] = xf
        best = min(best, float(x @ Q @ x + c @ x))
    return best


def dense_bound(Q, c):
    n = len(c)
    M = cp.Variable((n + 1, n + 1), symmetric=True)
    v = M[0, 1:]
    V = M[1:, 1:]
    cons = [M >> 0, M[0, 0] == 1, v >= 0, v <= 1]
    for i, j in itertools.combinations_with_replacement(range(n), 2):
        cons += [V[i, j] >= 0, V[i, j] - v[i] - v[j] + 1 >= 0, V[i, j] <= v[i], V[i, j] <= v[j]]
    prob = cp.Problem(cp.Minimize(cp.trace(Q @ V) + c @ v), cons)
    val = prob.solve(solver=cp.CLARABEL)
    return val, prob.status


def random_trees(trials=300, seed=0):
    rng = np.random.default_rng(seed)
    shapes = {"star3": [(0, 1), (0, 2), (0, 3)], "path4": [(0, 1), (1, 2), (2, 3)]}
    res = {}
    for name, edges in shapes.items():
        worst = 0.0
        worst_case = None
        count_gap = 0
        for _ in range(trials):
            Q = np.zeros((4, 4))
            for i in range(4):
                Q[i, i] = rng.integers(-6, 7)
            for i, j in edges:
                q = rng.integers(-6, 7) / 2.0
                Q[i, j] = Q[j, i] = q
            c = rng.integers(-6, 7, size=4).astype(float)
            true = box_qp_min(Q, c)
            val, st = dense_bound(Q, c)
            gap = true - val
            if gap > 1e-5 * max(1.0, abs(true)):
                count_gap += 1
            if gap > worst:
                worst = gap
                worst_case = {"Q": Q.tolist(), "c": c.tolist(), "true": true, "dense": val, "status": st}
        res[name] = {"trials": trials, "instances_with_gap_gt_1e-5": count_gap,
                     "worst_gap": worst, "worst_case": worst_case}
    return res


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "random":
    r = random_trees()
    Path(__file__).with_name("R9_literature_dense_star_random.json").write_text(json.dumps(r, indent=1))
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "worst_case"} for k, v in r.items()}, indent=1))
    for k, v in r.items():
        print(k, "worst case:", v["worst_case"])
