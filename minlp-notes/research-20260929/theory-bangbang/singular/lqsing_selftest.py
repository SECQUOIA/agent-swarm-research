"""Self-test for example E2: compare the exact stage residual, evaluated from
its definition rho_t = L_t + S_{t+1}(f_t) - S_t, with the quadratic model
h sigma w + h w beta.d + d'K d/2 + h^2 kappa w^2 / 2 used by lqsing_run.py,
in exact rational arithmetic at random rational points; also check the
telescoping identity S_0(x_0) + sum rho_t(zbar_t) + (Phi - S_N)(xbar_N) = J.
Usage: python3 lqsing_selftest.py k1 N
"""
import random
import sys
from fractions import Fraction as Fr

import numpy as np

import lqsing as L
import lqsing_run as R


def main():
    k1 = Fr(sys.argv[1])
    N = int(sys.argv[2])
    d = L.data(k1, N)
    Hq, gq, c0 = L.float_qp(d)
    if np.linalg.eigvalsh(Hq)[0] >= 0:
        u = L.solve_box_qp(Hq, gq)
    else:
        u = R.multistart(d, Hq, gq, c0)
    status = [(-1 if ui <= -1 + 1e-12 else (1 if ui >= 1 - 1e-12 else 0)) for ui in u]
    sol = L.exact_kkt(d, status)
    h, k, Fx, Fm = d["h"], d["k"], d["Fx"], d["F"]
    X, P, U = sol["x"], sol["p"], sol["u"]
    rng = random.Random(1)
    for name, Ps in (("A", R.fam_A(d)), ("B1", R.fam_B1(d))):
        def S(t, x):
            dx = (x[0] - X[t][0], x[1] - X[t][1])
            Pt = Ps[t]
            return (P[t][0] * x[0] + P[t][1] * x[1]
                    + (Pt[0][0] * dx[0] ** 2 + 2 * Pt[0][1] * dx[0] * dx[1] + Pt[1][1] * dx[1] ** 2) / 2)

        def rho(t, x, uu):
            L_ = h * ((x[0] ** 2 + x[1] ** 2) / 2 + (k[0] * x[0] + k[1] * x[1]) * uu)
            f = (x[0] + h * uu, h * x[0] + (1 - h) * x[1])
            return L_ + S(t + 1, f) - S(t, x)

        maxerr = Fr(0)
        for t in range(N):
            Kt, beta, kap = L.stage_terms(d, Ps[t + 1], Ps[t])
            r0 = rho(t, X[t], U[t])
            for _ in range(3):
                dd = (Fr(rng.randint(-99, 99), 37), Fr(rng.randint(-99, 99), 41))
                w = Fr(rng.randint(-99, 99), 53)
                lhs = rho(t, (X[t][0] + dd[0], X[t][1] + dd[1]), U[t] + w) - r0
                model = (h * sol["sigma"][t] * w + h * w * (beta[0] * dd[0] + beta[1] * dd[1])
                         + (Kt[0][0] * dd[0] ** 2 + 2 * Kt[0][1] * dd[0] * dd[1] + Kt[1][1] * dd[1] ** 2) / 2
                         + h * h * kap * w * w / 2)
                maxerr = max(maxerr, abs(lhs - model))
        tele = S(0, X[0]) + sum(rho(t, X[t], U[t]) for t in range(N))
        xN = X[N]
        tele += (Fm[0][0] * xN[0] ** 2 + Fm[1][1] * xN[1] ** 2) / 2 - S(N, xN)
        print("family %s: max |rho - model| = %s ; telescoped value - J = %s" % (name, maxerr, tele - sol["J"]))


if __name__ == "__main__":
    main()
