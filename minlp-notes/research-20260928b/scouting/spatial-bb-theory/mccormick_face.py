"""McCormick face-exactness example (scout scratch).

min f(x,y) = L|x-a| - (x-a)(y-b) over [0,1]^2, L = 2, a = 1/3, b = sqrt(2)-1.
f >= (L - |y-b|)|x-a| >= 0, so f* = 0 and every point of the segment x = a
is optimal.  Node relaxation: L|X| (exact) + McCormick envelope of -XY
(X = x-a, Y = y-b), solved as an LP with HiGHS.  Incumbent fixed at f* = 0.

Rules: widest-side bisection, bisection on x only, and "omega": split at the
LP solution on the coordinate whose relative position is most central,
safeguarded to stay 2% of the width away from the bounds.
"""
import numpy as np
from scipy.optimize import linprog

L, A, B = 2.0, 1.0 / 3.0, 2 ** 0.5 - 1


def lb(l, u):
    # variables: X, Y, s, z ; min L s + z
    Xl, Xu, Yl, Yu = l[0] - A, u[0] - A, l[1] - B, u[1] - B
    # z >= -Xu*Y - X*Yl + Xu*Yl  ->  -X*Yl - Xu*Y - z <= -Xu*Yl
    # z >= -Xl*Y - X*Yu + Xl*Yu  ->  -X*Yu - Xl*Y - z <= -Xl*Yu
    A_ub = [[-Yl, -Xu, 0, -1], [-Yu, -Xl, 0, -1], [1, 0, -1, 0], [-1, 0, -1, 0]]
    b_ub = [-Xu * Yl, -Xl * Yu, 0, 0]
    r = linprog([0, 0, L, 1], A_ub=A_ub, b_ub=b_ub,
                bounds=[(Xl, Xu), (Yl, Yu), (0, None), (None, None)], method="highs")
    assert r.status == 0
    return r.fun, np.array([r.x[0] + A, r.x[1] + B])


def count(eps, rule, theta=0.02, max_nodes=300000):
    stack = [(np.zeros(2), np.ones(2))]
    n = 0
    while stack:
        l, u = stack.pop(); n += 1
        if n > max_nodes:
            return None
        v, y = lb(l, u)
        if v >= -eps:
            continue
        w = u - l
        if rule == "bisect":
            i = int(np.argmax(w)); s = 0.5 * (l[i] + u[i])
        elif rule == "xonly":
            i = 0; s = 0.5 * (l[i] + u[i])
        elif rule == "omega":
            rel = np.minimum(y - l, u - y) / w
            i = int(np.argmax(rel))
            s = min(max(y[i], l[i] + theta * w[i]), u[i] - theta * w[i])
        l1, u1 = l.copy(), u.copy(); u1[i] = s
        l2, u2 = l.copy(), u.copy(); l2[i] = s
        stack += [(l1, u1), (l2, u2)]
    return n


if __name__ == "__main__":
    print("two-box certificate LBs:", lb(np.array([0, 0.]), np.array([A, 1.]))[0],
          lb(np.array([A, 0.]), np.array([1., 1.]))[0])
    for k in range(2, 8):
        eps = 10.0 ** -k
        print({"eps": eps, **{r: count(eps, r) for r in ("bisect", "xonly", "omega")}}, flush=True)
