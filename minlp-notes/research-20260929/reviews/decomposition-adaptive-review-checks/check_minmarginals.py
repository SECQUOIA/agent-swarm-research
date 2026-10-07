"""Reviewer check of Lemma A.1: min-marginals of leaves and cells by exhaustive enumeration of
configurations (leaf per bag, cell per separator, intersection conditions of Lemma 1.5 of [D]),
compared with (a) the reviewer's DP (indep_ls.dp) and (b) the author's ls_lib.dp.
Random dyadic partitions, random slopes, random linear terms, n = 4 and 5.
"""
import itertools
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "theory-decomposition", "adaptive"))
import indep_ls as R  # noqa: E402
import ls_lib  # noqa: E402


def random_part(n, rng, rounds=3, prob=0.35):
    P = R.Part(n)
    for _ in range(rounds):
        for t in range(n - 1):
            lm = rng.random(len(P.L[t]["l1"])) < prob
            cm = (rng.random(len(P.C[t]["lo"])) < prob) if t >= 1 else None
            P.split(t, lm, cm)
    return P


def to_author(P):
    Q = ls_lib.Partition(P.n)
    Q.leaves = [{k: v.copy() for k, v in d.items()} for d in P.L]
    Q.cells = [None] + [{k: v.copy() for k, v in d.items()} for d in P.C[1:]]
    return Q


def brute(P, lam, c):
    n = P.n
    # g values
    g0 = R.bagmin(P.L[0]["l1"], P.L[0]["u1"], P.L[0]["l2"], P.L[0]["u2"], P.L[0]["l1"], P.L[0]["u1"],
                  np.full(len(P.L[0]["l1"]), c[0]), np.full(len(P.L[0]["l1"]), lam[1] if n > 2 else 0.0),
                  n == 2, c[n - 1])[0]
    G = [None] * (n - 1)
    for t in range(1, n - 1):
        d, e = P.L[t], P.C[t]
        last = t == n - 2
        nl, nc = len(d["l1"]), len(e["lo"])
        M = np.full((nl, nc), np.inf)
        bi, di = np.nonzero((e["lo"][None, :] <= d["u1"][:, None]) & (e["hi"][None, :] >= d["l1"][:, None]))
        v = R.bagmin(d["l1"][bi], d["u1"][bi], d["l2"][bi], d["u2"][bi],
                     np.maximum(d["l1"][bi], e["lo"][di]), np.minimum(d["u1"][bi], e["hi"][di]),
                     np.full(len(bi), c[t] - lam[t]), np.full(len(bi), 0.0 if last else lam[t + 1]),
                     last, c[n - 1])[0]
        M[bi, di] = v
        G[t] = M
    # parent-meets matrices: leaf of bag t-1 (coordinate 2) meets cell of S_t
    PM = [None] * (n - 1)
    for t in range(1, n - 1):
        d, e = P.L[t - 1], P.C[t]
        PM[t] = (e["lo"][None, :] <= d["u2"][:, None]) & (e["hi"][None, :] >= d["l2"][:, None])
    MML = [np.full(len(P.L[t]["l1"]), np.inf) for t in range(n - 1)]
    MMC = [None] + [np.full(len(P.C[t]["lo"]), np.inf) for t in range(1, n - 1)]
    best = np.inf
    ncfg = 0
    leaf_ranges = [range(len(P.L[t]["l1"])) for t in range(n - 1)]
    for Ls in itertools.product(*leaf_ranges):
        # admissible cells per separator given the leaves
        opts = []
        for t in range(1, n - 1):
            ok = np.nonzero(PM[t][Ls[t - 1]] & np.isfinite(G[t][Ls[t]]))[0]
            opts.append(ok)
        for Ds in itertools.product(*opts):
            val = g0[Ls[0]] + sum(G[t][Ls[t], Ds[t - 1]] for t in range(1, n - 1))
            ncfg += 1
            best = min(best, val)
            for t in range(n - 1):
                if val < MML[t][Ls[t]]:
                    MML[t][Ls[t]] = val
            for t in range(1, n - 1):
                if val < MMC[t][Ds[t - 1]]:
                    MMC[t][Ds[t - 1]] = val
    return best, MML, MMC, ncfg


def main():
    worst_me = worst_auth = worst_lr = 0.0
    total_cfg = 0
    ntrial = 0
    for n in (4, 5):
        for seed in range(12 if n == 4 else 6):
            rng = np.random.default_rng(1000 * n + seed)
            P = random_part(n, rng, rounds=3 if n == 4 else 2, prob=0.4)
            lam = rng.uniform(-0.6, 0.6, n)
            lam[0] = 0.0
            lam[n - 1] = 0.0
            c = rng.uniform(-0.3, 0.3, n)
            bf, MML, MMC, ncfg = brute(P, lam, c)
            mine = R.dp(P, lam, c)
            auth = ls_lib.dp(to_author(P), lam, R.B, R.KAPPA, c)
            e_me = max(max(np.abs(MML[t] - mine["MML"][t]).max() for t in range(n - 1)),
                       max(np.abs(MMC[t] - mine["MMC"][t]).max() for t in range(1, n - 1)))
            e_au = max(max(np.abs(MML[t] - auth["MMleaf"][t]).max() for t in range(n - 1)),
                       max(np.abs(MMC[t] - auth["MMcell"][t]).max() for t in range(1, n - 1)))
            e_lr = max(abs(bf - mine["lr"]), abs(bf - auth["lr"]),
                       max(abs(MML[t].min() - bf) for t in range(n - 1)))
            worst_me, worst_auth, worst_lr = max(worst_me, e_me), max(worst_auth, e_au), max(worst_lr, e_lr)
            total_cfg += ncfg
            ntrial += 1
            nl, nc = P.counts()
            print("n=%d seed=%2d leaves=%4d cells=%3d configs=%8d lr=% .6f  max|MM_bf-MM_mine|=%.1e  "
                  "max|MM_bf-MM_author|=%.1e  lr/min-MM err=%.1e" % (n, seed, nl, nc, ncfg, bf, e_me, e_au, e_lr),
                  flush=True)
    print("SUMMARY trials=%d configurations=%d worst |MM_bf - MM_mine| = %.2e, worst |MM_bf - MM_author| = %.2e, "
          "worst lr error = %.2e" % (ntrial, total_cfg, worst_me, worst_auth, worst_lr))


if __name__ == "__main__":
    main()
