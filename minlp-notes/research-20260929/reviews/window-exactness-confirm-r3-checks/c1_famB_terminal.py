"""Round-3 confirmation, item 1: [V]'s family B on the verifier toy, terminal loss.

Independent of toy.py.  Verifier toy: min h sum_{t<N} [(x_t - a_t)^2/2 + k x_t u_t] + Phi(x_N),
x_{t+1} = x_t + h u_t, x_0 = 0, |u| <= 1, k = -1/2, Phi = 0, a_t = 2 if t h < 1 else -2, T = 2,
state box |x| <= 2.  Family B: S_t(x) = p_t x + (1/2)(x - xbar_t)^2 / 2 (P = 1/2).

1. Own discrete KKT point: scan the switch index m (u = +1 before m, -1 after m), with the
   control u_m minimizing the exact quadratic J(u_m) on [-1, 1]; keep the best; check the KKT
   signs with an own discrete adjoint.
2. Terminal term: Phi - S_N = -(p_N)(x) ... with p_N = Phi'(xbar_N) = 0, so
   Phi - S_N = -(x - xbar_N)^2 / 4 and its loss over |x| <= 2 is (2 + |xbar_N|)^2 / 4.
   Compared with the logged terminal loss in theory-bangbang/window/logs/toy_verifier.json.
3. N = 1000 in rational arithmetic (Fraction): exact m, u_m, xbar_N and the formula.
"""
import json
import os
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LOGV = os.path.join(HERE, "..", "..", "theory-bangbang", "window", "logs", "toy_verifier.json")
K, T, R = -0.5, 2.0, 2.0


def target(N):
    return np.array([2.0 if 2 * t < N else -2.0 for t in range(N + 1)])


def cost(N, u, a):
    h = T / N
    x = np.concatenate([[0.0], np.cumsum(h * u)])
    return h * np.sum((x[:N] - a[:N]) ** 2 / 2 + K * x[:N] * u), x


def solve(N):
    a = target(N)
    best = None
    for m in range(1, N - 1):
        base = np.where(np.arange(N) < m, 1.0, -1.0)
        vals = []
        for v in (-1.0, 0.0, 1.0):
            u = base.copy()
            u[m] = v
            vals.append(cost(N, u, a)[0])
        jm, j0, jp = vals
        c2 = (jp + jm - 2 * j0) / 2
        c1 = (jp - jm) / 2
        v = -c1 / (2 * c2) if c2 > 0 else (-1.0 if jm < jp else 1.0)
        v = min(1.0, max(-1.0, v))
        u = base.copy()
        u[m] = v
        J, x = cost(N, u, a)
        if best is None or J < best[0]:
            best = (J, m, v, u, x)
    J, m, v, u, x = best
    h = T / N
    p = np.empty(N + 1)
    p[N] = 0.0
    for t in range(N - 1, -1, -1):
        p[t] = p[t + 1] + h * (x[t] - a[t] + K * u[t])
    sig = K * x[:N] + p[1:]
    viol = np.where(u > 1 - 1e-12, np.maximum(0, sig), np.where(u < -1 + 1e-12, np.maximum(0, -sig), np.abs(sig)))
    return dict(N=N, m=m, u_m=v, J=J, xN=x[N], pN=p[N], kkt_viol=float(viol.max()))


def exact_1000():
    N = 1000
    h = Fr(2, N)
    a = [Fr(2) if 2 * t < N else Fr(-2) for t in range(N)]

    def J_of(m, v):
        u = [Fr(1)] * m + [v] + [Fr(-1)] * (N - 1 - m)
        x, J = Fr(0), Fr(0)
        for t in range(N):
            J += h * ((x - a[t]) ** 2 / 2 + Fr(K) * x * u[t])
            x += h * u[t]
        return J, x

    fl = solve(N)
    m = fl["m"]
    jm, j0, jp = (J_of(m, Fr(v))[0] for v in (-1, 0, 1))
    c2, c1 = (jp + jm - 2 * j0) / 2, (jp - jm) / 2
    v = -c1 / (2 * c2)
    J, xN = J_of(m, v)
    loss = (Fr(2) + abs(xN)) ** 2 / 4
    return dict(m=m, u_m=float(v), J=float(J), xN=float(xN), loss=float(loss), loss_exact=str(loss)[:60])


def main():
    logged = {r["N"]: r for r in json.load(open(LOGV))}
    out = []
    for N in (500, 1000, 2000, 4000, 8000):
        r = solve(N)
        r["loss_formula"] = (R + abs(r["xN"])) ** 2 / 4
        r["loss_logged"] = logged[N]["famB"]["terminal_loss"]
        r["J_logged"] = logged[N]["J"]
        r["rel_diff_loss"] = abs(r["loss_formula"] - r["loss_logged"]) / r["loss_logged"]
        r["diff_J"] = r["J"] - r["J_logged"]
        print(json.dumps(r), flush=True)
        out.append(r)
    ex = exact_1000()
    ex["loss_logged"] = logged[1000]["famB"]["terminal_loss"]
    ex["loss_logged_exact_field"] = logged[1000]["famB"]["exact"]["terminal_loss"]
    print(json.dumps(ex), flush=True)
    json.dump(dict(float_runs=out, exact_1000=ex), open(os.path.join(HERE, "logs", "c1_famB_terminal.json"), "w"),
              indent=1, default=float)


if __name__ == "__main__":
    main()
