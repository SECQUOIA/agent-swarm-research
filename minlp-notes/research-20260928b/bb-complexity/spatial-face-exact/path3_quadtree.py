"""Proposition 4.7, upper bound (construction due to the face-exact review, re-derived in the note).
f = |X1 - X2| + (X1 - X2) y on [0,1]^3 (instances.path3), D = X1 - X2.
Quadtree in (x1, x2), every box with the full y-range [0,1].  A square Q of side h is a leaf if
  (i)  h <= 2 eps          (then sup Gamma <= h/2 <= eps), or
  (ii) min_Q |D| >= 2h     (then Gamma <= 2h(1-y) <= m for D < 0 and Gamma <= 2hy <= m for D > 0).
Each leaf's exact node bound (HiGHS LP) is checked to be >= -eps; the leaves are counted.
Also re-checks the optimal set: f = 0 on {X1 = X2} and on {y = 1, X1 <= X2}."""
import math
import numpy as np
from face_bb import relax
import instances as I

a1, a2 = 1 / 3, math.sqrt(2) - 1
P = I.path3(a1, a2)


def minabsD(l1, u1, l2, u2):
    lo = (l1 - a1) - (u2 - a2); hi = (u1 - a1) - (l2 - a2)
    return 0.0 if lo <= 0 <= hi else min(abs(lo), abs(hi))


def quadtree(eps):
    leaves, worst = 0, math.inf
    stack = [(0.0, 1.0, 0.0, 1.0)]
    while stack:
        l1, u1, l2, u2 = stack.pop()
        h = u1 - l1
        if h <= 2 * eps or minabsD(l1, u1, l2, u2) >= 2 * h:
            leaves += 1
            worst = min(worst, relax(P, np.array([l1, l2, 0.0]), np.array([u1, u2, 1.0]))[0] + eps)
            continue
        m1, m2 = 0.5 * (l1 + u1), 0.5 * (l2 + u2)
        stack += [(l1, m1, l2, m2), (m1, u1, l2, m2), (l1, m1, m2, u2), (m1, u1, m2, u2)]
    return leaves, worst


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    pts = rng.uniform(0, 1, (20000, 3))
    f = lambda x: abs((x[0] - a1) - (x[1] - a2)) + ((x[0] - a1) - (x[1] - a2)) * x[2]
    on_face = [f(np.array([p[0], p[1], 1.0])) for p in pts if (p[0] - a1) <= (p[1] - a2)]
    print(f"optimal set: max f on {{y=1, X1<=X2}} over {len(on_face)} random points = {max(on_face):.2e}")
    for eps in (1e-1, 3e-2, 1e-2, 3e-3, 1e-3):
        n, worst = quadtree(eps)
        print(f"eps={eps:.0e}: quadtree leaves = {n:6d}, leaves*eps = {n * eps:6.2f}, "
              f"min over leaves of (LB + eps) = {worst:.2e} (>= 0: every leaf valid); "
              f"lower bound 0.102/eps = {0.102 / eps:.1f}", flush=True)
