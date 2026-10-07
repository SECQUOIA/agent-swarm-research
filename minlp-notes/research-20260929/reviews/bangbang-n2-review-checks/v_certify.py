"""Independent exact-rational certificate for examples A / A0 of extension-n2.md.

Own code: KKT point, costates and the maximal-recursion family come from v_discrete.py (my implementation);
all certificate arithmetic is exact (fractions.Fraction).

  f*_N >= B := S_0(x_0) + sum_t min_{D_t x U} rho_t + min_{D_N} (Phi - S_N)      (telescoping; any family S)
  f*_N <= J := exact cost of the (clipped) float KKT controls
with D_t the exact reachable box of the Euler dynamics and
  S_t(x) = p_t.x + 1/2 (x - c_t)^T P_t (x - c_t),  p_t, c_t, P_t float data read as exact rationals.
Box minima of quadratics: enumerate all faces; on each face solve the stationarity system exactly (Gauss-Jordan
over Q); keep feasible stationary points and vertices.  (Minimum over a box is attained in the relative interior
of a face where it is stationary; if the free block is singular it is also attained on a smaller face.)
"""
import itertools
import json
import sys
import time
from fractions import Fraction as Fr

import numpy as np

import v_discrete as VD

DEC = {
    "A": dict(rho="2", k1="-0.3", k2="-0.3", q="0.3", c="1", x20="0.5", e="0"),
    "A0": dict(rho="1", k1="-0.3", k2="-0.3", q="0.3", c="0.2", x20="0.5", e="0"),
}


def gj_solve(A, b):
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = None
        for r in range(col, n):
            if M[r][col] != 0:
                piv = r
                break
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [v / pv for v in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [M[r][k] - f * M[col][k] for k in range(n + 1)]
    return [M[i][n] for i in range(n)]


def quad(c0, g, H, z):
    n = len(z)
    return c0 + sum(g[i] * z[i] for i in range(n)) + sum(H[i][j] * z[i] * z[j] for i in range(n) for j in range(n)) / 2


def exact_boxmin(c0, g, H, lo, hi):
    n = len(g)
    best = None
    for pat in itertools.product(range(3), repeat=n):
        z = [lo[i] if pat[i] == 0 else hi[i] for i in range(n)]
        free = [i for i in range(n) if pat[i] == 2]
        if free:
            fixed = [i for i in range(n) if pat[i] != 2]
            A = [[H[i][j] for j in free] for i in free]
            b = [-(g[i] + sum(H[i][j] * z[j] for j in fixed)) for i in free]
            zf = gj_solve(A, b)
            if zf is None:
                continue
            if any(zf[k] < lo[free[k]] or zf[k] > hi[free[k]] for k in range(len(free))):
                continue
            for k, i in enumerate(free):
                z[i] = zf[k]
        v = quad(c0, g, H, z)
        if best is None or v < best:
            best = v
    return best


def certify(name, N, family="rmax", eps=0.02):
    t0 = time.time()
    d = {k: Fr(v) for k, v in DEC[name].items()}
    pb, sols = VD.solve(name, N)
    s = sols[0]
    kk = VD.kk_of(pb, s)
    if family == "rmax":
        P, brk = VD.maximal_recursion(pb, kk, eps)
        assert brk is None
    else:
        P = VD.lyap_family(pb, eps)
    h = Fr(2) / N
    x10, x20, a = Fr(0), d["x20"], Fr(1)
    p = [[Fr(float(v)) for v in kk["p"][t]] for t in range(N + 1)]
    c = [[Fr(float(kk["x1"][t])), Fr(float(kk["x2"][t]))] for t in range(N + 1)]
    PP = [[[Fr(float(P[t][0][0])), Fr(float(P[t][0][1]))], [Fr(float(P[t][0][1])), Fr(float(P[t][1][1]))]]
          for t in range(N + 1)]

    def S_coeffs(t):
        """S_t(x) = 1/2 x^T P x + (p - P c).x + 1/2 c^T P c."""
        Pm, pc, cc = PP[t], p[t], c[t]
        lin = [pc[i] - Pm[i][0] * cc[0] - Pm[i][1] * cc[1] for i in range(2)]
        cst = sum(cc[i] * Pm[i][j] * cc[j] for i in range(2) for j in range(2)) / 2
        return Pm, lin, cst

    x0 = [x10, x20]
    P0, l0, c00 = S_coeffs(0)
    S0 = quad(c00, l0, P0, x0)
    B = S0
    losses = []
    for t in range(N):
        P1, l1, c1 = S_coeffs(t + 1)
        Pt, lt, ct = S_coeffs(t)
        # z = (x1, x2, u); x_{t+1} = (x1 + h x2, x2 + h u)
        Mx = [[Fr(1), h, Fr(0)], [Fr(0), Fr(1), h]]
        H = [[Fr(0)] * 3 for _ in range(3)]
        g = [Fr(0)] * 3
        # running cost h (e x2 + q/2 x1^2 - c/2 x2^2 + (k1 x1 + k2 x2) u)
        H[0][0] += h * d["q"]; H[1][1] += -h * d["c"]
        H[0][2] += h * d["k1"]; H[2][0] += h * d["k1"]; H[1][2] += h * d["k2"]; H[2][1] += h * d["k2"]
        g[1] += h * d["e"]
        # + S_{t+1}(Mx z)
        for i in range(3):
            for j in range(3):
                H[i][j] += sum(Mx[k][i] * P1[k][l] * Mx[l][j] for k in range(2) for l in range(2))
            g[i] += sum(Mx[k][i] * l1[k] for k in range(2))
        # - S_t(x)
        for i in range(2):
            for j in range(2):
                H[i][j] -= Pt[i][j]
            g[i] -= lt[i]
        c0 = c1 - ct
        ubar = Fr(float(kk["u"][t]))
        if t == 0:
            # x fixed at x0: 1-d problem in u
            gu = g[2] + H[2][0] * x0[0] + H[2][1] * x0[1]
            cu = quad(c0, g[:2], [r[:2] for r in H[:2]], x0)
            lb = exact_boxmin(cu, [gu], [[H[2][2]]], [Fr(-1)], [Fr(1)])
            zbar_val = cu + gu * ubar + H[2][2] * ubar * ubar / 2
        else:
            w2, w1 = t * h, h * h * t * (t - 1) / 2
            lo = [x10 + t * h * x20 - w1, x20 - w2, Fr(-1)]
            hi = [x10 + t * h * x20 + w1, x20 + w2, Fr(1)]
            lb = exact_boxmin(c0, g, H, lo, hi)
            zbar_val = quad(c0, g, H, [c[t][0], c[t][1], ubar])
        losses.append(zbar_val - lb)
        B += lb
    # terminal: Phi - S_N,  Phi = -a x1 + rho/2 x2^2
    PN, lN, cN = S_coeffs(N)
    HT = [[-PN[0][0], -PN[0][1]], [-PN[1][0], d["rho"] - PN[1][1]]]
    gT = [-a - lN[0], -lN[1]]
    w2, w1 = N * h, h * h * N * (N - 1) / 2
    lbT = exact_boxmin(-cN, gT, HT, [x10 + N * h * x20 - w1, x20 - w2], [x10 + N * h * x20 + w1, x20 + w2])
    B += lbT
    # exact primal value
    x1, x2, J = x10, x20, Fr(0)
    for t in range(N):
        u = Fr(float(np.clip(kk["u"][t], -1, 1)))
        J += h * (d["e"] * x2 + d["q"] / 2 * x1 * x1 - d["c"] / 2 * x2 * x2 + (d["k1"] * x1 + d["k2"] * x2) * u)
        x1, x2 = x1 + h * x2, x2 + h * u
    J += -a * x1 + d["rho"] / 2 * x2 * x2
    gap = J - B
    return dict(example=name, N=N, family=family, B=float(B), J=float(J), gap=float(gap), gap_nonneg=bool(gap >= 0),
                n_loss_gt_1e_20=sum(1 for l in losses if l > Fr(1, 10 ** 20)), max_loss=float(max(losses)),
                interior=s["interior"], secs=round(time.time() - t0, 1))


if __name__ == "__main__":
    out = []
    for arg in sys.argv[1:]:
        name, N, fam = arg.split(":")
        r = certify(name, int(N), fam)
        print(json.dumps(r), flush=True)
        out.append(r)
    with open("logs/v_certify.jsonl", "a") as f:
        for r in out:
            f.write(json.dumps(r) + "\n")
