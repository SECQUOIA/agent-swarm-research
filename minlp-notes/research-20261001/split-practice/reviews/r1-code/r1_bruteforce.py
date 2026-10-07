"""Reviewer r1: independent brute-force certification of the normalised
separator's results at the stored SDP points (does not import stream code).

For a point Y = [[1, x^T], [x, X]] with S = X - x x^T, Lemma A gives for each
direction w the best violation phi(w^T x) - w^T S w, and the normalised
violation is at most 1/(4|w|^2) - min(0, lambda_min(S)).  Hence if the
reported best ratio is rho, every w with a larger ratio has
|w|^2 <= B := floor(1/(4 (rho - slack))).  We enumerate all integer w with
|w|^2 <= B (by patterns of absolute values) when that is feasible and compare
the maximum ratio with the reported one.  Everything is evaluated at the
stored floating-point matrix.

Usage (from split-practice/): python3 reviews/r1-code/r1_bruteforce.py [maxwork]
"""
import collections
import itertools
import json
import math
import os
import sys
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAXWORK = float(sys.argv[1]) if len(sys.argv) > 1 else 3e8


def phi(t):
    f = t - np.floor(t)
    return f * (1 - f)


def patterns(B):
    """multisets of absolute values (non-increasing tuples) with sum of squares <= B"""
    out = []

    def rec(prefix, rem, maxv):
        if prefix:
            out.append(tuple(prefix))
        for a in range(min(maxv, int(math.isqrt(rem))), 0, -1):
            rec(prefix + [a], rem - a * a, a)
    rec([], B, int(math.isqrt(B)))
    return out


def assignments(pat):
    """all signed orderings of the pattern with the first entry positive"""
    perms = set(itertools.permutations(pat))
    res = []
    for p in perms:
        for s in itertools.product((1, -1), repeat=len(p) - 1):
            res.append(np.array((p[0],) + tuple(a * b for a, b in zip(p[1:], s)), float))
    return res


def n_assign(pat):
    m = math.factorial(len(pat))
    for c in collections.Counter(pat).values():
        m //= math.factorial(c)
    return m * 2 ** (len(pat) - 1)


def work(n, B):
    if B > 16:          # far beyond any feasible enumeration; avoid building patterns
        return float("inf")
    return sum(math.comb(n, len(p)) * n_assign(p) for p in patterns(B))


def best_ratio(Y, B, chunk=200000):
    N = Y.shape[0]; n = N - 1
    x = Y[0, 1:]; S = Y[1:, 1:] - np.outer(x, x)
    best = (-np.inf, None)
    for pat in patterns(B):
        k = len(pat)
        A = assignments(pat)
        w2 = float(sum(a * a for a in pat))
        combs = itertools.combinations(range(n), k)
        while True:
            C = np.array(list(itertools.islice(combs, chunk)), dtype=np.int64).reshape(-1, k)
            if len(C) == 0:
                break
            XC = x[C]
            SS = [[S[C[:, a], C[:, b]] for b in range(k)] for a in range(k)]
            for a_ in A:
                t = XC @ a_
                var = np.zeros(len(C))
                for i in range(k):
                    for j in range(k):
                        var += a_[i] * a_[j] * SS[i][j]
                r = (phi(t) - var) / w2
                i = int(np.argmax(r))
                if r[i] > best[0]:
                    w = np.zeros(n, dtype=np.int64); w[C[i]] = a_.astype(np.int64)
                    best = (float(r[i]), w)
    return best


if __name__ == "__main__":
    recs = []
    for k in range(3):
        recs += [json.loads(l) for l in open(os.path.join(ROOT, f"logs/sep_run2_s{k}.jsonl"))]
    setdir = lambda f: "points_" + ("BT" if f.startswith("bt") else "DM") + f.split("_n")[1].split("_")[0]
    stats = collections.Counter()
    worst = 0.0
    for d in recs:
        Y = np.load(os.path.join(ROOT, "data", setdir(d["file"]), d["file"]))["Y"]
        Y = (Y + Y.T) / 2
        x = Y[0, 1:]; S = Y[1:, 1:] - np.outer(x, x)
        lmin = float(np.linalg.eigvalsh(S)[0])
        rho = d["ratio"]["ratio"]
        slack = max(0.0, -lmin) + 1e-9
        n = Y.shape[0] - 1
        if rho - slack <= 0:
            print(f"{d['file']:42s} rho={rho:.3g} lmin(S)={lmin:.2e}: no finite bound, skipped; max|x-round(x)|={np.abs(x - np.round(x)).max():.2e}")
            stats["skipped_rho0"] += 1
            continue
        B = int(math.floor(1 / (4 * (rho - slack))))
        W = work(n, B)
        if W > MAXWORK:
            print(f"{d['file']:42s} rho={rho:.4g} B={B} work={W:.2e}: skipped (too large); complete flag {d['ratio']['complete']}")
            stats["skipped_large"] += 1
            continue
        t = time.time()
        br, w = best_ratio(Y, B)
        diff = br - rho
        worst = max(worst, diff)
        ok = diff <= 1e-6
        stats["certified" if ok else "BETTER_FOUND"] += 1
        print(f"{d['file']:42s} rho={rho:.6g} B={B} brute max={br:.6g} diff={diff:+.2e} supp={int((w != 0).sum())} "
              f"complete flag {d['ratio']['complete']} lmin(S)={lmin:.1e} t={time.time() - t:.1f}s {'OK' if ok else 'MISMATCH'}", flush=True)
    print(dict(stats), "max (brute - reported)", worst)
