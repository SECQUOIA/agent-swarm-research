"""Reviewer check of the McCormick face-exact example (Section 3.7), independent code.

f(x,y) = 2|x-a| - (x-a)(y-b) on [0,1]^2, a = 1/3, b = sqrt(2)-1.
Node bound: min 2|X| + w over the box, with w >= the two McCormick
underestimators of -XY (X = x-a, Y = y-b); solved as an LP with HiGHS.
Checks:
  1. both boxes of the claimed 2-leaf certificate have bound >= 0;
  2. every box straddling x=a produced by widest-side bisection has bound
     <= -(width_x * width_y)/6 (evaluated exactly at X=0, Y=midpoint);
  3. node counts: widest-side bisection versus the analytic lower bound
     sum over levels of (#boxes in the column x ~ a with w_x w_y / 6 > eps).
"""
import math
import numpy as np
from scipy.optimize import linprog

a, b = 1.0 / 3.0, math.sqrt(2.0) - 1.0


def relax(l, u):
    Xl, Xu, Yl, Yu = l[0] - a, u[0] - a, l[1] - b, u[1] - b
    # vars X, Y, s, w: min 2 s + w;  s >= |X|;  w >= -(Xu*Y + X*Yl - Xu*Yl);  w >= -(Xl*Y + X*Yu - Xl*Yu)
    A_ub = [[1, 0, -1, 0], [-1, 0, -1, 0],
            [-Yl, -Xu, 0, -1], [-Yu, -Xl, 0, -1]]
    b_ub = [0, 0, -Xu * Yl, -Xl * Yu]
    r = linprog([0, 0, 2, 1], A_ub=A_ub, b_ub=b_ub,
                bounds=[(Xl, Xu), (Yl, Yu), (0, None), (None, None)], method="highs")
    assert r.status == 0
    return r.fun


def env_at(l, u, X, Y):
    Xl, Xu, Yl, Yu = l[0] - a, u[0] - a, l[1] - b, u[1] - b
    return 2 * abs(X) + max(-(Xu * Y + X * Yl - Xu * Yl), -(Xl * Y + X * Yu - Xl * Yu))


def check_f():
    xs = np.linspace(0, 1, 1201)
    X, Y = np.meshgrid(xs, xs, indexing="ij")
    F = 2 * np.abs(X - a) - (X - a) * (Y - b)
    print(f"min f on grid = {F.min():.3e}; min over |x-a|>=0.01 of f/|x-a| = "
          f"{np.min((F / np.maximum(np.abs(X - a), 1e-300))[np.abs(X - a) >= 0.01]):.4f} (>= 2-max|y-b| = {2 - max(b, 1 - b):.4f})")


def run(eps, max_nodes=400000):
    stack = [(np.zeros(2), np.ones(2))]
    nodes, worst_ratio = 0, -math.inf
    while stack:
        l, u = stack.pop()
        nodes += 1
        if nodes > max_nodes:
            return None, worst_ratio
        v = relax(l, u)
        if l[0] < a < u[0]:
            wx, wy = u[0] - l[0], u[1] - l[1]
            bound_mid = env_at(l, u, 0.0, 0.5 * (l[1] + u[1]) - b)
            assert v <= bound_mid + 1e-12
            assert bound_mid <= -(wx * wy) / 6 + 1e-12, (l, u, bound_mid)
        if v >= -eps:
            continue
        w = u - l
        i = int(np.argmax(w))
        s = 0.5 * (l[i] + u[i])
        l1, u1 = l.copy(), u.copy(); u1[i] = s
        l2, u2 = l.copy(), u.copy(); l2[i] = s
        stack += [(l1, u1), (l2, u2)]
    return nodes, worst_ratio


def analytic_lower(eps):
    # widest-side bisection: depth 2k gives squares of side 2^-k, depth 2k+1 gives 2^-(k+1) x 2^-k.
    # All boxes of the column containing x = a are processed while their parents have w_x w_y/6 > eps.
    total, k = 0, 0
    while True:
        sq = 2.0 ** (-2 * k) / 6
        rect = 2.0 ** (-2 * k - 1) / 6
        if sq > eps:
            total += 2 ** k            # squares of side 2^-k in the column
        else:
            break
        if rect > eps:
            total += 2 ** k            # rectangles 2^-(k+1) x 2^-k in the column
        else:
            break
        k += 1
    return total


if __name__ == "__main__":
    check_f()
    print("certificate bounds:", relax(np.array([0, 0.]), np.array([a, 1.])), relax(np.array([a, 0.]), np.array([1., 1.])))
    for k in range(2, 7):
        eps = 10.0 ** -k
        n, _ = run(eps)
        lo = analytic_lower(eps)
        print(f"eps=1e-{k}: widest-side bisection nodes={n}, analytic lower bound (column boxes only)={lo}, "
              f"lower*sqrt(eps)={lo*math.sqrt(eps):.3f}, nodes*sqrt(eps)={n*math.sqrt(eps):.3f}")
    print("all straddling boxes satisfied bound <= -(w_x w_y)/6 (assertions passed)")
