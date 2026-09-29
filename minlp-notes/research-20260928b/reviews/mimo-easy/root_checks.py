"""Reviewer checks of Section 1 (root relaxation): Proposition 1.1, Theorem 1.2,
Corollary 1.4, Theorem 1.7(a).

Part A (tiny N, exact brute force): frequency that x* is a box minimizer
(solver check AND KKT sign check) versus 2^-N, also for M < N; frequency
that the root is exact (R = OPT, OPT by enumeration of all 2^N vertices)
versus both bounds of Theorem 1.2.
Part B (moderate N): root gain G = W - R versus G_inf = ||Pi_{-cone B} w||^2
(chi-square with Bin(N,1/2) df), active-set size, G = G_inf frequency,
and the correlation witness (1.1) of Theorem 1.7(a).

Box relaxation solved in the ORIGINAL x-coordinates with scipy's BVLS
(independent of the note's error-coordinate code).  Written by the reviewer.
Usage: python3 root_checks.py A|B > root_checks_A.out
"""
import os, sys, itertools
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import lsq_linear, nnls
from scipy.special import comb
from multiprocessing import Pool


def gen(N, M, rho, rng):
    H = rng.standard_normal((M, N))
    A = np.sqrt(rho / N) * H
    xs = rng.choice([-1.0, 1.0], N)
    w = rng.standard_normal(M)
    return A, xs, w, A @ xs + w


def box(A, y):
    r = lsq_linear(A, y, bounds=(-1.0, 1.0), method="bvls", tol=1e-14)
    x = np.clip(r.x, -1, 1)
    res = y - A @ x
    return float(res @ res), x


def cellA(args):
    N, M, rho, T, seed = args
    rng = np.random.default_rng(seed)
    V = np.array(list(itertools.product([-1.0, 1.0], repeat=N)))
    cnt = dict(kkt=0, solver=0, mismatch=0, exact=0, vertex=0)
    for _ in range(T):
        A, xs, w, y = gen(N, M, rho, rng)
        R, xh = box(A, y)
        W = float(w @ w)
        zeta = xs * (A.T @ w)
        kkt = bool(np.all(zeta >= 0))
        solv = W <= R + 1e-9 * (1 + R)
        cnt["kkt"] += kkt; cnt["solver"] += solv; cnt["mismatch"] += (kkt != solv)
        if M >= N:
            F = ((y[None, :] - V @ A.T) ** 2).sum(1)
            OPT = F.min()
            cnt["exact"] += R >= OPT - 1e-9 * (1 + OPT)
            cnt["vertex"] += bool(np.all(np.abs(np.abs(xh) - 1) < 1e-7))
    beta = M / N
    ks = np.arange(N + 1)
    bsum = float(np.sum(comb(N, ks) * 2.0 ** (ks - N) * (1 + 4 * rho * ks / N) ** (-M / 2)))
    bclosed = ((1 + 2 * (1 + 4 * rho) ** (-beta / 2)) / 2) ** N
    return (N, M, rho, T, cnt, bsum, bclosed)


def partA():
    cells = []
    s = 1000
    for beta in (1, 2):
        for N in (2, 4, 6, 8):
            for rho in (0.5, 1.0, 4.0, 16.0):
                cells.append((N, beta * N, rho, 20000, s)); s += 1
    for (N, M) in ((4, 2), (6, 3), (8, 4)):
        for rho in (1.0, 16.0):
            cells.append((N, M, rho, 20000, s)); s += 1
    with Pool(5) as p:
        out = p.map(cellA, cells)
    print("N M rho T | P(x* box min: KKT) P(solver) 2^-N mismatches | P(R=OPT) P(vertex min) bound_sum bound_closed")
    for (N, M, rho, T, c, bs, bc) in out:
        se = np.sqrt(2.0 ** -N * (1 - 2.0 ** -N) / T)
        z = (c["kkt"] / T - 2.0 ** -N) / se
        ex = f"{c['exact']/T:.4f} {c['vertex']/T:.4f} {bs:.4f} {bc:.4f}" if M >= N else "(M<N: n/a)"
        pe = c["exact"] / T
        flag = "" if (M < N or bs >= 1 or pe <= bs + 3 * np.sqrt(pe * (1 - pe) / T)) else "  <-- EXCEEDS BOUND BY >3 SE"
        if M >= N and bs >= 1:
            flag = "  (bound vacuous)"
        print(f"{N} {M} {rho:5.1f} {T} | {c['kkt']/T:.4f} {c['solver']/T:.4f} {2.0**-N:.4f} (z={z:+.2f}) {c['mismatch']} | {ex}{flag}")


def cellB(args):
    N, beta, s = args
    M = beta * N
    rng = np.random.default_rng(s)
    H = rng.standard_normal((M, N)); xs = rng.choice([-1.0, 1.0], N); w = rng.standard_normal(M)
    W = float(w @ w)
    Bt = H * xs  # signed columns h~_j, rho = 1 scaling times sqrt(N)
    B1 = Bt / np.sqrt(N)  # B at rho = 1
    u1, rn = nnls(B1, -w, maxiter=100 * N)
    Ginf = W - rn ** 2
    act = int((u1 > 0).sum())
    rows = []
    wh = w / np.sqrt(W)
    g = Bt.T @ wh
    sv = np.maximum(-g, 0.0)
    Q = sv @ sv
    Hp = Bt - np.outer(wh, g)
    X = float(np.sum((Hp @ sv) ** 2))
    for tag, rho in (("logN/4", np.log(N) / 4), ("2logN/b", 2 * np.log(N) / beta), ("4logN", 4 * np.log(N)), ("N/4", N / 4)):
        A = np.sqrt(rho / N) * H
        y = A @ xs + w
        R, xh = box(A, y)
        G = W - R
        # witness u = tau s in error coordinates, B = sqrt(rho) B1
        tau = np.sqrt(N / rho) * np.sqrt(W) * Q / (Q ** 2 + X)
        feas = tau * sv.max() <= 2
        tau_c = min(tau, 2 / sv.max())
        u = tau_c * sv
        r = w + np.sqrt(rho) * B1 @ u
        Gwit = W - float(r @ r)
        rows.append((tag, rho, G, Gwit, bool(feas), float(np.max(u1) / np.sqrt(rho))))
    return (N, beta, W, Ginf, act, float(u1.max()), rows)


def partB():
    jobs = []
    for beta in (1, 2):
        for N, T in ((100, 300), (400, 100)):
            jobs += [(N, beta, 50000 + 1000 * beta + N * 7 + t) for t in range(T)]
    with Pool(5) as p:
        out = p.map(cellB, jobs, chunksize=4)
    for beta in (1, 2):
        for N in (100, 400):
            R = [o for o in out if o[0] == N and o[1] == beta]
            Ginf = np.array([o[3] for o in R]); act = np.array([o[4] for o in R]); umax = np.array([o[5] for o in R])
            print(f"beta={beta} N={N} inst={len(R)}: mean Ginf/N={Ginf.mean()/N:.4f} (0.5) var Ginf/N={Ginf.var()/N:.3f} (1.25) "
                  f"mean act/N={act.mean()/N:.4f} var act/N={act.var()/N:.3f} (0.25) median max u(1)={np.median(umax):.2f} max={umax.max():.2f}")
            for k, tag in enumerate(("logN/4", "2logN/b", "4logN", "N/4")):
                G = np.array([o[6][k][2] for o in R]); Gw = np.array([o[6][k][3] for o in R])
                fe = np.array([o[6][k][4] for o in R]); rho = R[0][6][k][1]
                eq = np.mean(np.abs(G - Ginf) <= 1e-7 * (1 + Ginf))
                print(f"    rho={tag:8s}({rho:6.2f}): mean G/N={G.mean()/N:.4f}  min G/N={G.min()/N:.4f}  P(G=Ginf)={eq:.3f}  "
                      f"witness: mean Gwit/N={Gw.mean()/N:.4f} (beta/(1+2beta)={beta/(1+2*beta):.4f}) feasible={fe.mean():.2f} "
                      f"G>=Gwit always: {bool(np.all(G >= Gw - 1e-7*(1+G)))}  G<=Ginf always: {bool(np.all(G <= Ginf + 1e-7*(1+Ginf)))}")


if __name__ == "__main__":
    if "A" in sys.argv[1]:
        partA()
    if "B" in sys.argv[1]:
        partB()
