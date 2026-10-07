"""Correctness checks for the exact separators in lattice.py.

1. Theorem 3 (thm3_exact) on random rational PSD matrices of rank r = 1..4,
   order N = 2..5, against brute force over the box [-K, K]^N.  The exact
   value must never exceed the box minimum (it is a minimum over all of Z^N),
   and the returned split is re-evaluated in exact arithmetic.
2. Theorem 3 on the full-rank hard matrices of Theorem 1 (split note), against
   the complete Fincke-Pohst violator list of check_split_separation.py.
3. Theorem 4 (thm4_rank1) against Theorem 3 on random rank-1 points.
4. sep_pd_float against the exact violator list on Theorem 1 matrices.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import itertools
import random
import sys
from fractions import Fraction as F

import numpy as np

sys.path.insert(0, (_PUBLIC_REPO + '/research-20260928b/side-results'))
import check_split_separation as css  # noqa: E402

from lattice import thm3_exact, thm4_rank1, q_exact, sep_pd_float, sep_ratio  # noqa: E402

random.seed(20261001)


def rand_lowrank(N, r, ent=3):
    while True:
        B = [[random.randint(-ent, ent) for _ in range(N)] for _ in range(r)]
        # random positive rational column scaling keeps rank and makes generic lattices
        n0 = sum(B[k][0] ** 2 for k in range(r))
        if n0 == 0:
            continue
        G = [[F(sum(B[k][i] * B[k][j] for k in range(r)), n0) for j in range(N)] for i in range(N)]
        rk = np.linalg.matrix_rank(np.array(B, float))
        if rk == r:
            return G


def box_min(X, K):
    N = len(X)
    best = F(0); arg = None
    for v in itertools.product(range(-K, K + 1), repeat=N):
        qq = css.q(X, list(v))
        if qq < best:
            best, arg = qq, v
    return best, arg


def test_thm3_random(trials=150):
    bad = eq = 0
    for t in range(trials):
        N = random.randint(2, 5); r = random.randint(1, min(4, N))
        X = rand_lowrank(N, r)
        res = thm3_exact(X)
        K = 4 if N <= 4 else 3
        bm, _ = box_min(X, K)
        if res["v"] is not None:
            assert q_exact(X, res["v"]) == res["q"], "re-evaluation mismatch"
        if res["q"] > bm:
            bad += 1
            print("FAIL", N, r, res["q"], bm)
        eq += res["q"] == bm
        assert res["rank"] == r
    print(f"[thm3 random] {trials} matrices (rank 1..4, N 2..5): exact <= box min in all; "
          f"equal in {eq}; failures {bad}")
    return bad


def test_thm3_theorem1():
    bad = 0; cnt = 0
    for A, b in css.subset_sum_instances()[:200]:
        X, _ = css.reduction(A, b)
        viol = css.violators(X)
        res = thm3_exact(X)
        best = min((css.q(X, list(v)) for v in viol), default=F(0))
        cnt += 1
        if res["q"] != best:
            bad += 1
            print("FAIL thm1", A, b, res["q"], best)
    print(f"[thm3 on Theorem 1 matrices] {cnt} subset-sum instances: failures {bad}")
    return bad


def test_thm4(trials=200):
    bad = 0
    for _ in range(trials):
        n = random.randint(1, 4)
        x = [F(random.randint(-20, 20), random.randint(1, 12)) for _ in range(n)]
        c = [F(1)] + x
        X = [[a * b for b in c] for a in c]
        v, qq, D = thm4_rank1(x)
        r3 = thm3_exact(X)
        if v is not None and q_exact(X, v) != qq:
            bad += 1
        if qq != r3["q"]:
            bad += 1
            print("FAIL thm4", x, qq, r3["q"])
        if qq != -F((D * D) // 4, D * D) and D > 1:
            bad += 1
    print(f"[thm4 vs thm3] {trials} rank-1 points: failures {bad}")
    return bad


def test_pd_float():
    bad = 0; cnt = 0
    for A, b in css.subset_sum_instances()[:200]:
        X, _ = css.reduction(A, b)
        viol = css.violators(X)
        best = min((css.q(X, list(v)) for v in viol), default=F(0))
        Xf = np.array([[float(a) for a in row] for row in X])
        res = sep_pd_float(Xf)
        cnt += 1
        if abs(res["q"] - float(best)) > 1e-9:
            bad += 1
            print("FAIL pd", A, b, res["q"], best)
    print(f"[sep_pd_float on Theorem 1 matrices] {cnt} instances: failures {bad}")
    return bad


def test_ratio(trials=60):
    """sep_ratio against brute force of max -q(v)/|w|^2 over a box that
    provably contains every split with ratio >= the box-found optimum:
    ratio >= rho forces |w|^2 <= 1/(4 rho), and q < 0 forces
    |v0 + w^T x + 1/2| < 1/2 + ... (we take |v0| <= sum|w_i||x_i| + 2)."""
    rng = np.random.default_rng(5)
    bad = 0
    for t in range(trials):
        N = int(rng.integers(2, 5)); r = int(rng.integers(1, N + 1))
        B = rng.normal(size=(r, N)); B[:, 0] /= np.linalg.norm(B[:, 0])
        Y = B.T @ B
        res = sep_ratio(Y)
        rho = res["ratio"]
        if rho <= 1e-3:
            continue
        Wb = int(np.floor(np.sqrt(1 / (4 * rho)))) + 1
        x = Y[0, 1:]
        best = 0.0
        for w in itertools.product(range(-Wb, Wb + 1), repeat=N - 1):
            w = np.array(w, float)
            if not w.any() or w @ w > 1 / (4 * rho) + 1e-9:
                continue
            V0 = int(np.abs(w) @ np.abs(x)) + 2
            for v0 in range(-V0, V0 + 1):
                v = np.concatenate([[v0], w])
                qq = v @ Y @ v + v @ Y[:, 0]
                best = max(best, -qq / (w @ w))
        if abs(best - rho) > 1e-9:
            bad += 1
            print("FAIL ratio", N, r, rho, best)
    print(f"[sep_ratio vs brute force] {trials} random PSD matrices: failures {bad}")
    return bad


if __name__ == "__main__":
    tot = test_thm3_random() + test_thm3_theorem1() + test_thm4() + test_pd_float() + test_ratio()
    print("ALL LATTICE TESTS PASSED" if tot == 0 else f"FAILURES {tot}")
