"""Theorem A(iii) check: widest-side selection on the McCormick kink family with a
width-dependent clamp schedule for x (theta = 1/10 + w_x/5, a function of the x-interval only)
and clip 0.2 for y, at the schedule's alternating trap point. Bound: T >= theta0^2/(2 sqrt(eps)),
theta0 = 1/10 (|c| = 1)."""
import math

import chain1d  # trap_point (200-digit arithmetic)


def run(a, eps, cap=5_000_000):
    stack = [(0.0, 1.0, 0.0, 1.0)]
    T = 0
    while stack:
        lx, ux, ly, uy = stack.pop()
        T += 1
        if T > cap:
            return None
        if not (lx < a < ux):
            continue
        wx, wy = ux - lx, uy - ly
        if wy * (a - lx) * (ux - a) / wx <= eps:
            continue
        rho = (a - lx) / wx
        if wx >= wy:
            th = 0.1 + wx / 5
            s = min(max(a, lx + th * wx), ux - th * wx)
            stack += [(s, ux, ly, uy), (lx, s, ly, uy)]
        else:
            s = min(max(ly + rho * wy, ly + 0.2 * wy), uy - 0.2 * wy)
            stack += [(lx, ux, s, uy), (lx, ux, ly, s)]
    return T


if __name__ == "__main__":
    sched = chain1d.SCHEDULES["width: 1/10 + w/5"]
    a = float(chain1d.trap_point(sched, 80))
    print(f"trap point a = {a!r}")
    for k in range(2, 9):
        eps = 10.0 ** -k
        print(f"eps=1e-{k}: T = {run(a, eps)}  bound {0.01 / (2 * math.sqrt(eps)):.1f}", flush=True)
