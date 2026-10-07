"""Experiments for Section 5 of decomposition-certificates.md.

E1  c = 0: smallest h = 2^-j (theta = 1/16) with root gap <= eps; size versus n and eps,
    next to the single-tree lower bound L_n(eps) of Corollary 2.1.
E2  c != 0 (seed 0): root gap versus h for affine and zero slopes (theta = 1/8).
E3  brute-force validity: cell minorants versus grid value functions (upper approximations).
E4  c != 0: root gap versus theta at fixed small h, affine and zero slopes.
Usage: python3 run_experiments.py E1|E2|E3|E4
"""
import sys
import time
import numpy as np
import mpmath as mp
from dp_certificate import certificate, global_min, grid_value_functions, dphi, F
from single_tree_lb import L as single_tree_L

B, KAPPA = 0.8, 0.1


def c_vec(n, seed, amp=0.2):
    if seed is None:
        return np.zeros(n)
    return np.random.default_rng(seed).uniform(-amp, amp, n)


def E1(mu=4):
    print("# E1: c=0, b=%.1f, kappa=%.1f, theta=2^-%d; x*=0, f*=0" % (B, KAPPA, mu))
    print("# n  eps  j(h=2^-j)  root_gap  size  size/(n-1)  single_tree_LB  seconds")
    for n in [4, 8, 16, 32, 64]:
        c = np.zeros(n)
        xs = np.zeros(n)
        j = 1
        for eps in [1e-2, 1e-4, 1e-6, 1e-8]:
            while True:
                t0 = time.time()
                r, size, _, _ = certificate(n, B, KAPPA, c, xs, 2.0 ** -j, mu)
                gap = -r
                if gap <= eps or j > 40:
                    break
                j += 1
            lb = float(single_tree_L(n, B, eps))
            print("%3d %.0e %3d %.3e %8d %8.1f %11.3e %6.1f" % (n, eps, j, gap, size, size / (n - 1), lb, time.time() - t0), flush=True)


def E2(n=8, seed=0):
    mu = 3
    c = c_vec(n, seed)
    xs, fs, fgrid = global_min(n, B, KAPPA, c)
    g = dphi(xs, KAPPA) + c
    g[:-1] += B * xs[1:]
    g[1:] += B * xs[:-1]
    lam = np.array([dphi(xs[t], KAPPA) + c[t] + B * xs[t + 1] for t in range(1, n - 1)])
    print("# E2: n=%d, c~U(-0.2,0.2) seed %d, theta=2^-%d" % (n, seed, mu))
    print("# x* =", np.array2string(xs, precision=4), " f* = %.12f (grid DP %.6f), |grad F(x*)|_inf = %.1e" % (fs, fgrid, np.abs(g).max()))
    print("# slopes lambda_t, t=1..n-2:", np.array2string(lam, precision=4))
    print("# j  h  gap_affine  gap_zero  size")
    for j in range(2, 17, 2):
        h = 2.0 ** -j
        ra, size, _, _ = certificate(n, B, KAPPA, c, xs, h, mu, "affine")
        rz, _, _, _ = certificate(n, B, KAPPA, c, xs, h, mu, "zero")
        print("%2d %.2e %.3e %.3e %d" % (j, h, fs - ra, fs - rz, size), flush=True)


def E3():
    print("# E3: validity check l_{t,D}(s) <= phi_t^grid(s) on grid points s in D (phi^grid >= phi_t)")
    for n, seed, mu, j in [(4, 0, 3, 6), (6, 0, 3, 8), (6, 1, 2, 5), (5, None, 1, 4)]:
        c = c_vec(n, seed)
        xs, fs, _ = global_min(n, B, KAPPA, c)
        vf = grid_value_functions(n, B, KAPPA, c, G=2001)
        for slopes in ["affine", "zero"]:
            r, size, store, lam = certificate(n, B, KAPPA, c, xs, 2.0 ** -j, mu, slopes, keep=True)
            worst = -np.inf
            for t in range(1, n - 1):
                Pl, Pu, beta = store[t]
                s, ph = vf[t]
                idx = np.searchsorted(Pl[:, 0], s, side="right") - 1
                idx = np.clip(idx, 0, len(Pl) - 1)
                # every grid point s lies in cell idx (cells sorted by lower end after sorting)
                order = np.argsort(Pl[:, 0])
                lo, hi, be = Pl[order, 0], Pu[order, 0], beta[order]
                k = np.clip(np.searchsorted(lo, s, side="right") - 1, 0, len(lo) - 1)
                inside = (s >= lo[k] - 1e-15) & (s <= hi[k] + 1e-15)
                lval = lam[t] * s + be[k]
                worst = max(worst, float(np.max((lval - ph)[inside])))
            print("n=%d seed=%s theta=2^-%d h=2^-%d slopes=%s: f*=%.10f root=%.10f max(l - phi_grid)=%.3e" % (
                n, seed, mu, j, slopes, fs, r, worst), flush=True)


def E4(n=3, seed=0):
    c = c_vec(n, seed)
    xs, fs, _ = global_min(n, B, KAPPA, c)
    lam = [dphi(xs[t], KAPPA) + c[t] + B * xs[t + 1] for t in range(1, n - 1)]
    print("# E4: n=%d seed %d, h=2^-14; slopes %s; x* = %s" % (n, seed, np.array2string(np.array(lam), precision=4), np.array2string(xs, precision=4)))
    print("# mu theta gap_affine gap_zero size")
    for mu in range(1, 7):
        ra, size, _, _ = certificate(n, B, KAPPA, c, xs, 2.0 ** -14, mu, "affine")
        rz, _, _, _ = certificate(n, B, KAPPA, c, xs, 2.0 ** -14, mu, "zero")
        print("%d %.4f %.3e %.3e %d" % (mu, 2.0 ** -mu, fs - ra, fs - rz, size), flush=True)


def E5():
    """Root gap versus n at fixed h = 2^-8 for theta = 1/8 and 1/16 (c = 0).
    (n <= 32 with theta = 1/32 as well: logs/debug_n_theta.log.)"""
    print("# E5: gap at h=2^-8 versus n; theta=2^-mu; c=0")
    for mu in [3, 4]:
        row = []
        for n in [32, 48, 64]:
            r, s, _, _ = certificate(n, B, KAPPA, np.zeros(n), np.zeros(n), 2.0 ** -8, mu)
            row.append("%d:%.3e" % (n, -r))
        print("mu=%d " % mu + " ".join(row), flush=True)


def E1b(n=64, mu=4):
    """E1 for one large n, starting the h search near the predicted j."""
    print("# E1b: c=0, theta=2^-%d, n=%d" % (mu, n))
    for eps, j in [(1e-4, 9), (1e-6, 12)]:
        while True:
            t0 = time.time()
            r, size, _, _ = certificate(n, B, KAPPA, np.zeros(n), np.zeros(n), 2.0 ** -j, mu)
            if -r <= eps:
                break
            j += 1
        lb = float(single_tree_L(n, B, eps))
        print("%3d %.0e %3d %.3e %8d %8.1f %11.3e %6.1f" % (n, eps, j, -r, size, size / (n - 1), lb, time.time() - t0), flush=True)


if __name__ == "__main__":
    {"E1": E1, "E1b": E1b, "E2": E2, "E3": E3, "E4": E4, "E5": E5}[sys.argv[1]]()
