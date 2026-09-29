"""Section 6 (convergence order versus node counts) and Proposition 5.5 (exact rational check).

Part A.  Kink instance f = 2|x-a| - (x-a)(y-b), a = 1/3, b = sqrt2 - 1, on [0,1]^2, three schemes:
  McC  : termwise McCormick (order 2, sup gap = w_x w_y / 4);
  aBB  : alphaBB with alpha = |c|/2 = 1/2 (order 2, sup gap = alpha (w_x^2 + w_y^2)/4 ), node bound by
         HiGHS QP (f - alpha q_B is convex: Hessian [[1,-1],[-1,1]]);
  FO   : first-order face-exact scheme  McC - kappa * min(x - l_x, u_x - x), kappa = 0.2  (order 1).
  Node counts for bisection and for splitting at the relaxation minimiser (SCIP-type R(1,.2), widest side),
  and a grid check that the 2-box certificate {x<=a},{x>=a} is valid for McC and FO at eps = 0.
Part B.  Exact rational replay of the strong-branching path of Proposition 5.5 (Couenne point
  R(1/4,1/5), min-score strong branching) on the kink instance, using the closed-form node bound
  LB = -|c| w_y (a-l_x)(u_x-a)/w_x of straddling boxes.
"""
import math
from fractions import Fraction as Fr
import numpy as np
import highspy
from face_bb import Problem, relax, run, RULES
import instances as I

A, B = 1.0 / 3.0, math.sqrt(2) - 1


def abb_lb(l, u, alpha=0.5):
    """min over box of 2|X| - X Y - alpha[(x-lx)(ux-x) + (y-ly)(uy-y)], X = x-a, Y = y-b (QP via face_bb)."""
    # -XY = -xy + b x + a y - ab ; -alpha (x-lx)(ux-x) = alpha x^2 - alpha (lx+ux) x + alpha lx ux
    Q = np.array([[2 * alpha, -1.0], [-1.0, 2 * alpha]])
    c = [B - alpha * (l[0] + u[0]), A - alpha * (l[1] + u[1])]
    const = -A * B + alpha * (l[0] * u[0] + l[1] * u[1])
    P = Problem("abb", l, u, c=c, terms=[], absterms=[([1, 0], A, 2.0)], Q=Q, const=const)
    v, x, _ = relax(P, np.array(l, float), np.array(u, float))
    return v, x


def run_abb(eps, rule, cap=200000):
    stack = [(np.zeros(2), np.ones(2))]
    n = 0
    while stack:
        l, u = stack.pop(); n += 1
        if n > cap:
            return None
        v, x = abb_lb(l, u)
        if v >= -eps:
            continue
        w = u - l
        i = 0 if w[0] >= w[1] else 1
        if rule == "bisect":
            p = 0.5 * (l[i] + u[i])
        else:   # split at the relaxation minimiser, clamped to the middle 60%
            p = min(max(x[i], l[i] + 0.2 * w[i]), u[i] - 0.2 * w[i])
        l1, u1 = l.copy(), u.copy(); u1[i] = p
        l2, u2 = l.copy(), u.copy(); l2[i] = p
        stack += [(l2, u2), (l1, u1)]
    return n


def grid_check(kappa=0.2, N=801):
    xs = np.linspace(0, 1, N)
    X, Y = np.meshgrid(xs, xs, indexing="ij")
    m = 2 * np.abs(X - A) - (X - A) * (Y - B)
    worst = {"McC": -np.inf, "FO": -np.inf}
    for (lx, ux) in ((0.0, A), (A, 1.0)):
        mask = (X >= lx) & (X <= ux)
        Xl, Xu, Yl, Yu = lx - A, ux - A, -B, 1 - B
        Xr, Yr = X - A, Y - B
        env = np.maximum(-(Xu * Yr + Xr * Yl - Xu * Yl), -(Xl * Yr + Xr * Yu - Xl * Yu))
        gap = -Xr * Yr - env
        dx = np.minimum(X - lx, ux - X)
        worst["McC"] = max(worst["McC"], np.max((gap - m)[mask]))
        worst["FO"] = max(worst["FO"], np.max((gap + kappa * dx - m)[mask]))
    print(f"[A] 2-box certificate, max over grid of (gap - m): McC {worst['McC']:.2e}, FO(kappa=0.2) {worst['FO']:.2e} "
          f"(<= 0 means valid at eps = 0)")


def part_b():
    a = Fr(1, 3)
    alpha, beta = Fr(1, 4), Fr(1, 5)

    def lb(l, u, wy):      # closed-form bound of a straddling box (c = -1)
        return -wy * (a - l) * (u - a) / (u - l)

    def point(l, u, t):    # Couenne point in an interval [l,u] for relaxation value t
        p = alpha * t + (1 - alpha) * (l + u) / 2
        return min(max(p, l + beta * (u - l)), u - beta * (u - l))

    l, u, wy = Fr(0), Fr(1), Fr(1)
    for depth in range(6):
        rho = (a - l) / (u - l)
        px = point(l, u, a)
        # straddling x-child
        lx_, ux_ = (l, px) if a < px else (px, u)
        x_min = lb(lx_, ux_, wy)
        # y split: yhat has relative position rho in the y-range (Section 5); y-range [0, wy] w.l.o.g.
        py = point(Fr(0), wy, rho * wy)
        y_min = min(lb(l, u, py), lb(l, u, wy - py))
        choice = "x" if x_min > y_min else "y"
        print(f"[B] depth {depth}: x-range [{l}, {u}] rho={rho} ({float(rho):.4f}); min child LB: x-split {float(x_min):.6f}, "
              f"y-split {float(y_min):.6f} -> {choice}")
        if choice == "x":
            l, u = lx_, ux_
        else:
            D = (a - l) * (u - a) / (u - l)
            print(f"[B] column x-range fixed from here; D = (a-l)(u-a)/w = {D} = {float(D):.6f}; "
                  f"nodes >= 2 D / eps - 1 = {float(2 * D):.5f}/eps - 1")
            break


if __name__ == "__main__":
    grid_check()
    for eps in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
        P = I.kink()
        print(f"[A] eps={eps:.0e}: McC bisect {run(P, eps, RULES['bisect'])}, McC R(1,.2) {run(P, eps, RULES['SCIP(1,.2)w'])}; "
              f"aBB bisect {run_abb(eps, 'bisect')}, aBB R(1,.2) {run_abb(eps, 'relpoint')}", flush=True)
    part_b()
