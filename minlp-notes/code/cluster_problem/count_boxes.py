"""Minimal spatial branch-and-bound node counts: nondegenerate vs degenerate constrained minima.

Illustrates results/cluster-free-branch-and-bound-constrained-minima.md.

Both examples relax the (only) nonlinear constraint with the same generic second-order rule
    g^cv_Z(x) = g(x) - alpha * sum_i (x_i - l_i)(u_i - x_i),   alpha = 1,
which is a convex underestimator on the box Z with error at most alpha * n * w(Z)^2 / 4
(an alphaBB relaxation that does not exploit any convexity of g).  Objectives are convex and
kept exact.  The relaxed problem on each box is a small convex program solved with cvxpy.

Example A (nondegenerate):  min x1^2 + x2^2  s.t.  1 - x1 x2 <= 0,  x in [0.5, 2]^2.
    z* = (1,1), f* = 2, mu* = 2 (strict complementarity), critical cone {d1 + d2 = 0},
    Hessian of the Lagrangian [[2,-2],[-2,2]]: positive definite on the critical cone only.
Example B (degenerate):  min x2 - x1  s.t.  x1 + (x1 - 1)^4 - x2 <= 0,  x in [0, 2] x [0, 3].
    z* = (1,1), f* = 0, mu* = 1, critical cone {d1 = d2}, Hessian of the Lagrangian = 0 at z*:
    the objective grows only quartically along the feasible curve (Kannan-Barton 2017,
    Remark 4 type).

Branch-and-bound: bisect the widest side, best-bound selection, incumbent fixed at f*,
fathom when L(Z) >= f* - eps.  Reported for decreasing eps: nodes processed and the maximal
number of simultaneously open (unfathomed) boxes.
Run: conda run -n minlp-notes python code/cluster_problem/count_boxes.py
"""
import heapq
import cvxpy as cp
import numpy as np

ALPHA = 1.0


def solve(prob):
    for solver in (cp.CLARABEL, cp.SCS):
        try:
            prob.solve(solver=solver)
        except Exception:
            continue
        if prob.status in ("optimal", "optimal_inaccurate"):
            return prob.value
        if prob.status in ("infeasible", "infeasible_inaccurate"):
            return np.inf
    raise RuntimeError(prob.status)


def lb_example_A(box):
    (l1, u1), (l2, u2) = box
    x = cp.Variable(2)
    # g^cv = 1 - x1 x2 - alpha[(x1-l1)(u1-x1) + (x2-l2)(u2-x2)]
    #      = alpha (x1^2 + x2^2) - x1 x2 - alpha (l1+u1) x1 - alpha (l2+u2) x2 + alpha (l1 u1 + l2 u2) + 1
    Q = np.array([[ALPHA, -0.5], [-0.5, ALPHA]])
    lin = np.array([-ALPHA * (l1 + u1), -ALPHA * (l2 + u2)])
    const = ALPHA * (l1 * u1 + l2 * u2) + 1.0
    gcv = cp.quad_form(x, Q) + lin @ x + const
    prob = cp.Problem(cp.Minimize(cp.sum_squares(x)), [gcv <= 0, x[0] >= l1, x[0] <= u1, x[1] >= l2, x[1] <= u2])
    return solve(prob)


def lb_example_B(box):
    (l1, u1), (l2, u2) = box
    x = cp.Variable(2)
    gcv = (x[0] + cp.power(x[0] - 1.0, 4) - x[1]
           + ALPHA * (cp.square(x[0]) - (l1 + u1) * x[0] + l1 * u1)
           + ALPHA * (cp.square(x[1]) - (l2 + u2) * x[1] + l2 * u2))
    prob = cp.Problem(cp.Minimize(x[1] - x[0]), [gcv <= 0, x[0] >= l1, x[0] <= u1, x[1] >= l2, x[1] <= u2])
    return solve(prob)


def branch_and_bound(lb, root, fstar, eps, max_nodes=20000):
    heap = [(lb(root), 0, root)]
    counter = 1
    nodes = 0
    max_open = int(heap[0][0] < fstar - eps)
    while heap:
        L, _, box = heapq.heappop(heap)
        nodes += 1
        if L >= fstar - eps:
            continue
        if nodes > max_nodes:
            return None, None
        widths = [u - l for (l, u) in box]
        i = int(np.argmax(widths))
        l, u = box[i]
        mid = 0.5 * (l + u)
        for child in ((l, mid), (mid, u)):
            nb = list(box)
            nb[i] = child
            nb = tuple(nb)
            Lc = lb(nb)
            if Lc < fstar - eps:
                heapq.heappush(heap, (Lc, counter, nb))
                counter += 1
        max_open = max(max_open, len(heap))
    return nodes, max_open


if __name__ == "__main__":
    for name, lb, root, fstar in (
        ("A (nondegenerate): min x1^2+x2^2 s.t. x1 x2 >= 1", lb_example_A, ((0.5, 2.0), (0.5, 2.0)), 2.0),
        ("B (degenerate): min x2-x1 s.t. x2 >= x1 + (x1-1)^4", lb_example_B, ((0.0, 2.0), (0.0, 3.0)), 0.0),
    ):
        print(f"Example {name}")
        print("   eps        nodes   max_open   eps^(-1/4)")
        for k in range(2, 11):
            eps = 4.0 ** (-k)
            nodes, mo = branch_and_bound(lb, root, fstar, eps)
            if nodes is None:
                print(f"  {eps:9.2e}  (node limit reached)")
                break
            print(f"  {eps:9.2e}  {nodes:7d}  {mo:7d}   {eps**-0.25:8.1f}")
        print()
