"""Constrained check of Theorem D (reviewer script).

min f(x,y) = (x^2 + y^2) - x^2 - y^2 = 0  s.t.  x + y = 1,  (x,y) in [0,1]^2.
DC scheme: g = x^2 + y^2 (convex) plus secants of -x^2, -y^2, so the gap is
exactly q_B (alpha = 1) and the node bound is
    LB(B) = min over the segment B ∩ {x+y=1} of -q_B(x, 1-x),
or +inf if the segment is empty (pruned by infeasibility).  Every feasible
point is optimal: S = F, p = 1, eta = 0, H^1(S) = sqrt 2, and c_S = sqrt 2
(a segment meets a square of side l in length at most sqrt(2) l).
Theorem D: |P| >= H^1(S) (alpha/(4 eps))^(1/2) / (2^n c_S) = 1/(8 sqrt(eps)).
Also compared: the explicit certificate of anti-diagonal squares of side
sqrt(2 eps) (count of boxes meeting the line), and widest-side bisection.
"""
import math


def lb(l1, u1, l2, u2):
    lo, hi = max(l1, 1 - u2), min(u1, 1 - l2)     # x-range of the segment inside the box
    if lo > hi:
        return math.inf
    # q(x) = (x-l1)(u1-x) + (1-x-l2)(u2-1+x): concave quadratic, maximise on [lo,hi]
    q = lambda x: (x - l1) * (u1 - x) + (1 - x - l2) * (u2 - 1 + x)
    # q'(x) = (u1 + l1 - 2x) + (2 - l2 - u2 - 2x), so the vertex is at x = (u1 + l1 + 2 - l2 - u2)/4
    xv = ((u1 + l1) + (2 - l2 - u2)) / 4.0
    cands = [lo, hi] + ([xv] if lo < xv < hi else [])
    return -max(q(x) for x in cands)


def bisect(eps):
    stack, nodes, meet = [(0.0, 1.0, 0.0, 1.0)], 0, 0
    while stack:
        b = stack.pop()
        nodes += 1
        v = lb(*b)
        if v >= -eps:
            if v < math.inf:
                meet += 1
            continue
        l1, u1, l2, u2 = b
        if u1 - l1 >= u2 - l2:
            m = 0.5 * (l1 + u1)
            stack += [(l1, m, l2, u2), (m, u1, l2, u2)]
        else:
            m = 0.5 * (l2 + u2)
            stack += [(l1, u1, l2, m), (l1, u1, m, u2)]
    return nodes, meet


if __name__ == "__main__":
    for k in range(2, 9, 1):
        eps = 10.0 ** -k
        thmD = 1.0 / (8 * math.sqrt(eps))
        s = math.sqrt(2 * eps)
        diag = math.ceil(1 / s)
        # verify the anti-diagonal square certificate on the line: q <= s^2/2 <= eps
        assert lb(0.0, s, 1 - s, 1.0) >= -eps - 1e-15
        nodes, meet = bisect(eps)
        print(f"eps=1e-{k}: ThmD lower bound on boxes meeting S = {thmD:9.1f}; explicit certificate "
              f"(anti-diagonal squares) = {diag:6d}; widest-side bisection: nodes={nodes:7d}, "
              f"leaves meeting S={meet:6d}")
