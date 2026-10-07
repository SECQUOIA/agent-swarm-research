"""camshape: the generic method of the program, for comparison: rigorous dynamic programming
over cells of the separator (r_i, r_{i+1}) with cell-constant bounds, no problem-specific
argument.

Grid: r-cells I_k = [lo_k, lo_{k+1}] with lo_k = fl(1 + k d) and the last upper end 2, so
consecutive cells share their float endpoints and cover [1, 2] exactly. State at stage i: (r_i, r_{i+1}) in I_a x I_b with
|a - b| <= w (w = floor(alpha/d) + 1 covers every pair with |r_{i+1} - r_i| <= alpha; the
pair (1, 2), which has no slope row, also lies in the band because g_1 forces
r_2 - r_1 < 5e-4 < alpha for these data).
F_i(a, b) >= max { r_1 + ... + r_{i+1} : feasible prefix with r_i in I_a, r_{i+1} in I_b }:
  F_i(a, b) = sup I_b + max { F_{i-1}(c, a) : |c - a| <= w, g_i possible on I_c x I_a x I_b },
g_i = 1/r_{i-1} + 1/r_{i+1} - c/r_i >= 0 is possible on a box iff
  1/lo(I_c) + 1/lo(I_b) - c/hi(I_a) >= 0, i.e. lo(I_c) <= 1/(c/hi(I_a) - 1/lo(I_b)).
All tests are made permissive by a margin 1e-12 and each stage value is increased by
1e-11, which dominates the rounding error of the float64 operations (values <= 2n).
Bound: objective >= -c0 * max over final states with g_n possible.
"""
import json
import sys
import time

import numpy as np

from camshape_model import extract


def run(n, d):
    m = extract(n)
    c, c2, alpha, c0 = m["c"], m["c2"], m["alpha"], m["c0"]
    ub1, lbn = m["ub"][0], m["lb"][-1]
    K = int(np.ceil(1.0 / d))
    lo = 1.0 + d * np.arange(K)
    hi = np.append(lo[1:], 2.0)          # adjacent cells share float endpoints: exact cover of [1, 2]
    w = int(np.floor(alpha / d)) + 1
    offs = np.arange(-w, w + 1)                      # b = a + off
    A = np.arange(K)[:, None]
    B = A + offs[None, :]
    valid = (B >= 0) & (B < K)
    Bc = np.clip(B, 0, K - 1)
    NEG = -1e300
    # stage 1: state (r_1, r_2); r_1 in [1, ub1]; g_1 = 1 + 1/r_2 - c/r_1 >= 0
    ok1 = valid & (lo[A] <= ub1) & (1 + 1 / lo[Bc] - c / np.minimum(hi[A], ub1) >= -1e-12)
    F = np.where(ok1, np.minimum(hi[A], ub1) + hi[Bc], NEG)
    for i in range(2, n):  # state (r_i, r_{i+1}) from (r_{i-1}, r_i)
        # previous state F[c, off'] with a = c + off'  ->  G[a, j] = F_{i-1}(c = a - w + j, a), j = 0..2w
        # (c = a - off', off' = w - j)
        G = np.full((K, 2 * w + 1), NEG)
        for j in range(2 * w + 1):
            off_prev = w - j
            cidx = np.arange(K) - off_prev           # c for each a
            okc = (cidx >= 0) & (cidx < K)
            G[okc, j] = F[cidx[okc], off_prev + w]
        # prefix max over j (increasing c)
        P = np.maximum.accumulate(G, axis=1)
        # threshold on lo(I_c): lo_c <= 1/(c/hi_a - 1/lo_b) (if the denominator <= 0: no restriction)
        den = c / hi[A] - 1 / lo[Bc]
        with np.errstate(divide="ignore"):
            thr = np.where(den > 0, 1 / np.maximum(den, 1e-300), np.inf) * (1 + 1e-12) + 1e-12
        cmax = np.where(np.isinf(thr), K - 1, np.floor((np.minimum(thr, 3.0) - 1.0) / d)).astype(np.int64)
        jmax = np.clip(cmax - (A - w), -1, 2 * w)   # index in j
        best = np.where(jmax >= 0, np.take_along_axis(P, np.clip(jmax, 0, 2 * w), axis=1), NEG)
        F = np.where(valid & (best > NEG / 2), hi[Bc] + best + 1e-11, NEG)
    # final: (r_{n-1}, r_n); r_n in [lbn, 2]; g_n = 1/r_{n-1} + 1/2 - (c2/2)/r_n >= 0
    okf = valid & (hi[Bc] >= lbn) & (1 / lo[A] + 0.5 - 0.5 * c2 / hi[Bc] >= -1e-12)
    best = np.max(np.where(okf, F, NEG))
    return dict(n=n, d=d, K=K, band=2 * w + 1, cells_per_stage=int(valid.sum()), max_sum_r_upper=float(best),
                dual_bound=float(-c0 * best * (1 + 1e-15)))


if __name__ == "__main__":
    n = int(sys.argv[1])
    for d in [float(x) for x in sys.argv[2:]]:
        t0 = time.time()
        r = run(n, d)
        r["seconds"] = time.time() - t0
        print(json.dumps(r), flush=True)
        with open("logs/camshape_celldp.jsonl", "a") as f:
            f.write(json.dumps(r) + "\n")
