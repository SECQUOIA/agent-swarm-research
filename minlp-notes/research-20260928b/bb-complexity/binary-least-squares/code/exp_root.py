"""E1: root relaxation.
(a) Root gain G = f(x*) - R versus the exact law of Theorem 2.3:
    G_inf = ||Pi_K w||^2 ~ chi^2 with Bin(N, 1/2) degrees of freedom (M >= N),
    and G = G_inf whenever the NNLS solution is <= 2.
(b) Root exactness (box minimizer is a vertex) at tiny N versus the bound
    ((1 + 2 (1+4 rho)^(-beta/2)) / 2)^N of Theorem 2.1 and 2^(-N).
Usage: python3 exp_root.py OUT.jsonl
"""
import sys, json, os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import nnls
from core import instance, box_min


def part_a(out):
    for beta in (1, 2):
        for N in (50, 200, 800):
            M = beta * N
            for rho in (2 * np.log(N), 4 * np.log(N), 8 * np.log(N), N / 4):
                ns = 200 if N <= 200 else 40
                for s in range(ns):
                    A, y, xs, B, w = instance(N, M, rho, s)
                    W = float(w @ w)
                    val, lb, u, ina = box_min(B, w)
                    u8, rn = nnls(B, -w, maxiter=50 * N)
                    out.write(json.dumps(dict(part="a", N=N, M=M, beta=beta, rho=rho, seed=s,
                                              W=W, G=W - val, Ginf=W - rn ** 2, inactive=ina,
                                              active=int((u8 > 0).sum()),
                                              umax_nnls=float(u8.max()))) + "\n")
                out.flush()


def part_b(out):
    rng = np.random.default_rng(12345)
    for beta in (1, 2):
        for N in (2, 4, 6, 8):
            for rho in (1.0, 4.0, 16.0, 64.0):
                ntr = 20000
                cnt_vertex = 0; cnt_xstar = 0
                for t in range(ntr):
                    A, y, xs, B, w = instance(N, beta * N, rho, int(rng.integers(2**62)))
                    val, lb, u, ina = box_min(B, w)
                    # vertex minimizer: all u in {0,2} (tolerance)
                    if np.all(np.minimum(np.abs(u), np.abs(2 - u)) < 1e-9):
                        cnt_vertex += 1
                    if np.all(u < 1e-12):
                        cnt_xstar += 1
                bound = ((1 + 2 * (1 + 4 * rho) ** (-beta / 2)) / 2) ** N
                out.write(json.dumps(dict(part="b", N=N, beta=beta, rho=rho, trials=ntr,
                                          p_vertex=cnt_vertex / ntr, p_xstar=cnt_xstar / ntr,
                                          two_pow=2.0 ** -N, bound=bound)) + "\n")
                out.flush()


if __name__ == "__main__":
    with open(sys.argv[1], "w") as out:
        part_b(out)
        part_a(out)
