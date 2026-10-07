"""Adversarial check of the sharp form of Lemma 2 (revision round 2).

Reduction used in the note: with U_c = U - (M/2)(s-c)^2 (concave) and
L_v = L + (M/2)(s-c)^2 (convex), phi = L_v - U_c is convex,
w = U - L = M (s-c)^2 - phi, and Delta_U + Delta_L over [c-h/2, c+h/2]
is phi'((c+h/2)-) - phi'((c-h/2)+).  Conversely every convex phi with
phi <= M (s-c)^2 on [c-h, c+h] comes from the pair U = (M/2)(s-c)^2,
L = phi - (M/2)(s-c)^2.

This script maximizes the slope rise by an LP over all convex piecewise
linear phi with breakpoints on a uniform grid of [-h, h] (c = 0), with
phi(0) = -W and phi_i <= M s_i^2 - M ds^2/4 at the grid points (so the
interpolant stays below M s^2 everywhere: a chord of M s^2 over a step ds
exceeds it by at most M ds^2/4).  The claim is that the optimum is at most
4 W/h + 4 M h and tends to it as the grid is refined.
"""
import numpy as np
from scipy.optimize import linprog


def lp_max_rise(W, M, h, m):
    # grid s_0 .. s_{2m} on [-h, h], step ds = h/m; m even so that
    # -h/2 and h/2 are grid points.
    s = np.linspace(-h, h, 2 * m + 1)
    ds = h / m
    N = len(s)
    ia = m - m // 2          # index of -h/2
    ib = m + m // 2          # index of +h/2
    # objective: maximize (phi[ib] - phi[ib-1])/ds - (phi[ia+1] - phi[ia])/ds
    c = np.zeros(N)
    c[ib] -= 1 / ds
    c[ib - 1] += 1 / ds
    c[ia + 1] += 1 / ds
    c[ia] -= 1 / ds
    # convexity: -(phi[i-1] - 2 phi[i] + phi[i+1]) <= 0
    A = np.zeros((N - 2, N))
    for i in range(1, N - 1):
        A[i - 1, i - 1] = -1
        A[i - 1, i] = 2
        A[i - 1, i + 1] = -1
    b = np.zeros(N - 2)
    bounds = [(None, M * si ** 2 - M * ds ** 2 / 4) for si in s]
    bounds[m] = (-W, -W)
    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")
    assert res.status == 0, res.message
    return -res.fun


def main():
    ok = True
    print("LP over convex piecewise-linear phi (grid breakpoints), "
          "max of Delta_U + Delta_L; bound 4 W/h + 4 M h")
    for W, M, h in [(1.0, 0.0, 1.0), (0.0, 1.0, 1.0), (1.0, 1.0, 1.0),
                    (0.05, 2.0, 0.4), (2.0, 0.1, 0.8), (0.01, 5.0, 1.0)]:
        bound = 4 * W / h + 4 * M * h
        row = []
        for m in [8, 64, 512]:
            v = lp_max_rise(W, M, h, m)
            ok = ok and v <= bound * (1 + 1e-9) + 1e-9
            row.append(f"m={m}: {v:.6f} (ratio {v / bound:.6f})")
        print(f"  W={W:g}, M={M:g}, h={h:g}, bound {bound:.6f}: "
              + "; ".join(row))
    print("all LP optima <= bound:", ok)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
