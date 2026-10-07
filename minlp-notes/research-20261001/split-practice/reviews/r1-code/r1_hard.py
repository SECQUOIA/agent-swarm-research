"""Reviewer r1: independent rebuild of the hard X3C matrices (split note,
Theorem 1 and Corollary 5) and exact enumeration of ALL violated splits for
the small instances; compares with logs/hard_run2.jsonl.

The X3C generator below re-implements exp_hard.x3c from its description
(same random.Random call sequence); the matrix follows the split note's
Theorem 1 formula; the enumeration is an exact-rational Fincke-Pohst on
(v + e0/2)^T X (v + e0/2) < 1/4 written here (no stream code imported).
Usage (from split-practice/): python3 reviews/r1-code/r1_hard.py QMAX
"""
import itertools
import json
import math
import os
import random
import sys
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def x3c(qq, nsets, planted, rng):
    U = list(range(3 * qq))
    sets = []
    if planted:
        P = U[:]; rng.shuffle(P)
        sets += [tuple(sorted(P[3 * k:3 * k + 3])) for k in range(qq)]
    while len(sets) < nsets:
        sets.append(tuple(sorted(rng.sample(U, 3))))
    rng.shuffle(sets)
    return sets


def covers(sets, qq):
    n = len(sets)
    sols = []
    for k in itertools.combinations(range(n), qq):
        cov = [e for i in k for e in sets[i]]
        if len(set(cov)) == 3 * qq and len(cov) == 3 * qq:
            x = [0] * n
            for i in k:
                x[i] = 1
            sols.append(tuple(x))
    return sols


def gram(sets, qq, h2):
    n = len(sets); p = 3 * qq
    A = [[int(e in S) for S in sets] for e in range(p)]
    col = lambda i: [A[r][i] for r in range(p)]
    b = [1] * p
    N = n + 2
    G = [[F(0)] * N for _ in range(N)]
    G[0][0] = 4 * (n + 1) + 4 * h2
    G[0][N - 1] = G[N - 1][0] = F(-2 * (n + 1))
    for i in range(n):
        for j in range(n):
            G[1 + i][1 + j] = F(sum(a * c for a, c in zip(col(i), col(j))) + 4 * (i == j))
        G[1 + i][N - 1] = G[N - 1][1 + i] = F(sum(col(i)) + 2)
    G[N - 1][N - 1] = F(p + 2 * n + 1)
    return G


def ldl(X):
    """X = L^T D L style decomposition for enumeration from the last index:
    returns d (pivots) and mu with Q(y) = sum_k d_k (y_k + sum_{j>k} mu[k][j] y_j)^2."""
    N = len(X)
    A = [row[:] for row in X]
    d = [F(0)] * N; mu = [[F(0)] * N for _ in range(N)]
    for k in range(N):
        d[k] = A[k][k]
        assert d[k] > 0
        for j in range(k + 1, N):
            mu[k][j] = A[k][j] / d[k]
        for i in range(k + 1, N):
            for j in range(k + 1, N):
                A[i][j] -= A[i][k] * A[k][j] / d[k]
    return d, mu


def all_violators(X):
    """All v in Z^N with q_X(v) < 0, exactly; q = Q(v + e0/2) - 1/4."""
    N = len(X)
    d, mu = ldl(X)
    out = []
    v = [0] * N
    R = F(1, 4)

    def rec(k, rem):
        # level k: y_k = v_k + [k == 0]/2 ; center c = -sum_{j>k} mu_kj y_j
        c = -sum((mu[k][j] * (v[j] + (F(1, 2) if j == 0 else 0)) for j in range(k + 1, N)), F(0))
        off = F(1, 2) if k == 0 else F(0)
        rad = math.sqrt(float(rem / d[k])) + 1e-9
        lo = math.floor(float(c - off) - rad) - 1
        hi = math.ceil(float(c - off) + rad) + 1
        for z in range(lo, hi + 1):
            t = z + off - c
            r2 = rem - d[k] * t * t
            if r2 <= 0:
                continue
            v[k] = z
            if k == 0:
                out.append((F(1, 4) - r2, tuple(v)))  # Q - 1/4 = (R - r2) - 1/4 = -r2
            else:
                rec(k - 1, r2)
        v[k] = 0
    rec(N - 1, R)
    return [(-(F(1, 4) - qq) + F(0), vv) for qq, vv in out]


def q_val(X, v):
    N = len(X)
    return sum(v[i] * X[i][j] * v[j] for i in range(N) for j in range(N)) + sum(v[i] * X[i][0] for i in range(N))


if __name__ == "__main__":
    QMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    logs = [json.loads(l) for l in open(os.path.join(ROOT, "logs/hard_run2.jsonl"))]
    bad = 0; checked = 0
    for qq in (2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25):
        if qq > QMAX:
            break
        for planted in (True, False):
            for nf in (2, 3):
                seed = 1000 * qq + 10 * nf + planted
                rng = random.Random(seed)
                sets = x3c(qq, nf * qq, planted, rng)
                n = len(sets)
                sols = covers(sets, qq)
                G1 = gram(sets, qq, F(n + 1))
                Ghat = max(abs(G1[i][j]) for i in range(n + 2) for j in range(n + 2) if (i, j) != (0, 0))
                for kind, h2 in (("thm1", F(n + 1)), ("cor5", F(max(3, n + 1) * Ghat, 4))):
                    G = gram(sets, qq, h2)
                    X = [[a / G[0][0] for a in row] for row in G]
                    V = all_violators(X)
                    # double check each value exactly
                    vals = {vv: q_val(X, vv) for _, vv in V}
                    assert all(val < 0 for val in vals.values())
                    pred = {(0,) + tuple(-t for t in x) + (1,) for x in sols} | {(-1,) + x + (-1,) for x in sols}
                    minq = min(vals.values()) if vals else F(0)
                    predq = F(-1) / (4 * (n + 1 + h2)) if sols else F(0)
                    rec = [r for r in logs if r["q"] == qq and r["n"] == n and r["planted"] == planted and r["kind"] == kind]
                    assert len(rec) == 1
                    r = rec[0]
                    ok = (set(vals) == pred and minq == predq and r["cover"] == bool(sols)
                          and abs(r["enum"]["q"] - float(minq)) < 1e-12 and abs(r["predicted_min_q"] - float(predq)) < 1e-15)
                    checked += 1; bad += not ok
                    print(f"q={qq} n={n} planted={planted} {kind}: covers {len(sols)}, violators {len(vals)} (pred {len(pred)}),"
                          f" min q {minq} = {float(minq):.6g}, logged enum {r['enum']['q']:.6g}, logged cover {r['cover']}, supports "
                          f"{sorted(set(sum(1 for a in vv[1:] if a) for vv in vals))} -> {'OK' if ok else 'MISMATCH'}", flush=True)
    print("checked", checked, "mismatches", bad)
