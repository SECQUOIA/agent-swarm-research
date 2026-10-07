"""Exact-rational certificate for example A (Euler transcription, N stages).

Problem (all data exact rationals):
    min sum_{t<N} h [ e x2 + q/2 x1^2 - c/2 x2^2 + (k1 x1 + k2 x2) u_t ] - a x1_N + rho/2 x2_N^2
    x_{t+1} = (x1 + h x2, x2 + h u_t),  u_t in [-1, 1],  x_0 = (x10, x20),  h = T / N.
Calibration (any floats are valid certificate data; they are converted exactly to rationals):
    S_t(x) = p_t . x + 1/2 (x - c_t)^T P_t (x - c_t),
with p_t the float discrete costates, c_t the float KKT states and P_t the discrete maximal
singular-Riccati recursion (fam_rmax, eps = 0.02).
Bound (telescoping, valid for every family S):
    f* >= S_0(x_0) + sum_t min_{D_t x U} rho_t + min_{D_N} (Phi - S_N),
    rho_t = L_t + S_{t+1} o f_t - S_t   (a quadratic in z = (x1, x2, u), exact rational coefficients),
    D_t = exact reachable box (contains every feasible state; D_0 = {x_0}).
Each minimum of a quadratic over a box is computed exactly by enumerating faces: on every face
with a nonsingular free Hessian block, the stationary point is solved for exactly and kept if it lies
in the face.  (The global minimum over the box is attained in the relative interior of some face;
if the free block there is singular the value is also attained on a smaller face.)
Upper bound: the float KKT controls converted exactly; states and cost in exact arithmetic.
"""
import itertools
import json
import sys
import time
from fractions import Fraction as Fr

import numpy as np

from model import Par
from discrete import solve_kkt, fam_rmax

EXAMPLES = {
    "A0": dict(T="2", a="1", rho="1", k1="-0.3", k2="-0.3", q="0.3", c="0.2", x10="0", x20="0.5", e="0"),
    "A": dict(T="2", a="1", rho="2", k1="-0.3", k2="-0.3", q="0.3", c="1", x10="0", x20="0.5", e="0"),
}
DEC = EXAMPLES["A"]
EPS = 0.02


def fr(v):
    return Fr(v) if not isinstance(v, float) else Fr(v)  # float -> exact binary rational


def solve_exact(Hm, rhs):
    """Gaussian elimination over Fractions; returns None if singular."""
    n = len(rhs)
    M = [list(Hm[i]) + [rhs[i]] for i in range(n)]
    for col in range(n):
        piv = next((r for r in range(col, n) if M[r][col] != 0), None)
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col] / M[col][col]
                M[r] = [M[r][k] - f * M[col][k] for k in range(n + 1)]
    return [M[i][n] / M[i][i] for i in range(n)]


def qval(c0, g, H, z):
    n = len(z)
    return c0 + sum(g[i] * z[i] for i in range(n)) + Fr(1, 2) * sum(
        z[i] * H[i][j] * z[j] for i in range(n) for j in range(n))


def box_min_exact(c0, g, H, lo, hi):
    n = len(g)
    best, arg = None, None
    for pat in itertools.product((0, 1, 2), repeat=n):
        z = [lo[i] if pat[i] == 0 else hi[i] for i in range(n)]
        free = [i for i in range(n) if pat[i] == 2]
        if free:
            fixed = [i for i in range(n) if pat[i] != 2]
            Hff = [[H[i][j] for j in free] for i in free]
            rhs = [-(g[i] + sum(H[i][j] * z[j] for j in fixed)) for i in free]
            sol = solve_exact(Hff, rhs)
            if sol is None:
                continue
            if any(sol[k] < lo[free[k]] or sol[k] > hi[free[k]] for k in range(len(free))):
                continue
            for k, i in enumerate(free):
                z[i] = sol[k]
        v = qval(c0, g, H, z)
        if best is None or v < best:
            best, arg = v, z
    return best, arg


def float_down(q):
    """Largest float <= the rational q (so the reported bound stays valid)."""
    f = float(q)
    while Fr(f) > q:
        f = float(np.nextafter(f, -np.inf))
    return f


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def T_(A):
    return [list(r) for r in zip(*A)]


def matvec(A, v):
    return [sum(A[i][k] * v[k] for k in range(len(v))) for i in range(len(A))]


def main(N, family="rmax", example="A"):
    global DEC
    DEC = EXAMPLES[example]
    t0 = time.time()
    P = {k: Fr(v) for k, v in DEC.items()}
    p = Par(**{k: float(v) for k, v in DEC.items()})
    kk = solve_kkt(p, N)
    if family == "rmax":
        Ps, brk, _ = fam_rmax(p, kk, EPS)
        assert brk is None
    else:  # negative control: non-tangential discrete Lyapunov family
        from discrete import fam_lyap
        Ps = fam_lyap(p, kk, EPS)
    h = P["T"] / N
    # certificate data as exact rationals
    pc = [[Fr(float(v)) for v in kk["p"][t]] for t in range(N + 1)]
    cc = [[Fr(float(v)) for v in kk["x"][t]] for t in range(N + 1)]
    cc[0] = [P["x10"], P["x20"]]
    PP = [[[Fr(float(Ps[t][0][0])), Fr(float(Ps[t][0][1]))], [Fr(float(Ps[t][0][1])), Fr(float(Ps[t][1][1]))]]
          for t in range(N + 1)]
    M = [[Fr(1), h, Fr(0)], [Fr(0), Fr(1), h]]
    E = [[Fr(1), Fr(0), Fr(0)], [Fr(0), Fr(1), Fr(0)]]
    HL = [[h * P["q"], Fr(0), h * P["k1"]], [Fr(0), -h * P["c"], h * P["k2"]], [h * P["k1"], h * P["k2"], Fr(0)]]
    gL = [Fr(0), h * P["e"], Fr(0)]
    x0 = [P["x10"], P["x20"]]
    # S_0(x0)
    d0 = [x0[0] - cc[0][0], x0[1] - cc[0][1]]
    S0 = pc[0][0] * x0[0] + pc[0][1] * x0[1] + Fr(1, 2) * sum(d0[i] * PP[0][i][j] * d0[j] for i in range(2) for j in range(2))
    total = S0
    stage_lb, stage_loss = [], []
    worst = (Fr(0), -1)
    for t in range(N):
        P1, P0 = PP[t + 1], PP[t]
        c1, c0v = cc[t + 1], cc[t]
        H = [[HL[i][j] + v for j, v in enumerate(row)] for i, row in enumerate(matmul(T_(M), matmul(P1, M)))]
        EPE = matmul(T_(E), matmul(P0, E))
        H = [[H[i][j] - EPE[i][j] for j in range(3)] for i in range(3)]
        a1 = [pc[t + 1][i] - sum(P1[i][j] * c1[j] for j in range(2)) for i in range(2)]
        a0 = [pc[t][i] - sum(P0[i][j] * c0v[j] for j in range(2)) for i in range(2)]
        g = [gL[i] + sum(M[k][i] * a1[k] for k in range(2)) - sum(E[k][i] * a0[k] for k in range(2)) for i in range(3)]
        cst = Fr(1, 2) * sum(c1[i] * P1[i][j] * c1[j] for i in range(2) for j in range(2)) \
            - Fr(1, 2) * sum(c0v[i] * P0[i][j] * c0v[j] for i in range(2) for j in range(2))
        if t == 0:
            lo = [x0[0], x0[1], Fr(-1)]
            hi = [x0[0], x0[1], Fr(1)]
            # fixed x: minimize over u only
            gu = g[2] + H[2][0] * x0[0] + H[2][1] * x0[1]
            cu = cst + g[0] * x0[0] + g[1] * x0[1] + Fr(1, 2) * sum(x0[i] * H[i][j] * x0[j] for i in range(2) for j in range(2))
            lb, _ = box_min_exact(cu, [gu], [[H[2][2]]], [Fr(-1)], [Fr(1)])
        else:
            w2 = t * h
            w1 = h * h * t * (t - 1) / 2
            lo = [P["x10"] + t * h * P["x20"] - w1, P["x20"] - w2, Fr(-1)]
            hi = [P["x10"] + t * h * P["x20"] + w1, P["x20"] + w2, Fr(1)]
            lb, _ = box_min_exact(cst, g, H, lo, hi)
        ubar = Fr(float(kk["u"][t]))
        zbar = [cc[t][0], cc[t][1], ubar] if t > 0 else [x0[0], x0[1], ubar]
        loss = qval(cst, g, H, zbar) - lb
        stage_lb.append(lb)
        stage_loss.append(loss)
        if loss > worst[0]:
            worst = (loss, t)
        total += lb
    # terminal
    PN, cN = PP[N], cc[N]
    HT = [[-PN[0][0], -PN[0][1]], [-PN[1][0], P["rho"] - PN[1][1]]]
    gT = [-P["a"] - pc[N][0] + PN[0][0] * cN[0] + PN[0][1] * cN[1], -pc[N][1] + PN[1][0] * cN[0] + PN[1][1] * cN[1]]
    cT = -Fr(1, 2) * sum(cN[i] * PN[i][j] * cN[j] for i in range(2) for j in range(2))
    w2, w1 = N * h, h * h * N * (N - 1) / 2
    loT = [P["x10"] + N * h * P["x20"] - w1, P["x20"] - w2]
    hiT = [P["x10"] + N * h * P["x20"] + w1, P["x20"] + w2]
    lbT, _ = box_min_exact(cT, gT, HT, loT, hiT)
    total += lbT
    # exact primal value of the float controls
    x1, x2, J = P["x10"], P["x20"], Fr(0)
    for t in range(N):
        u = Fr(float(kk["u"][t]))
        J += h * (P["e"] * x2 + P["q"] / 2 * x1 * x1 - P["c"] / 2 * x2 * x2 + (P["k1"] * x1 + P["k2"] * x2) * u)
        x1, x2 = x1 + h * x2, x2 + h * u
    J += -P["a"] * x1 + P["rho"] / 2 * x2 * x2
    gap = J - total
    res = dict(example=example, N=N, family=family, eps=EPS, B=float(total), J=float(J), gap=float(gap), gap_exact_sign=int((gap > 0) - (gap < 0)),
               B_float_down=float_down(total), B_denominator_bits=total.denominator.bit_length(),
               sum_stage_loss=float(sum(stage_loss)), worst_stage=worst[1], worst_loss=float(worst[0]),
               n_loss_gt_1e_20=int(sum(1 for l in stage_loss if l > Fr(1, 10 ** 20))),
               terminal_lb=float(lbT), S0=float(S0), fracset=sorted(kk["fracset"]), s=kk["m"],
               float_J=kk["J"], seconds=time.time() - t0)
    return res


if __name__ == "__main__":
    fam, ex = "rmax", "A"
    for a in sys.argv[1:]:
        if a in EXAMPLES:
            ex = a
            continue
        if not a.isdigit():
            fam = a
            continue
        r = main(int(a), fam, ex)
        print(json.dumps(r), flush=True)
        with open("logs/n2_certify.jsonl", "a") as f:
            f.write(json.dumps(r) + "\n")
