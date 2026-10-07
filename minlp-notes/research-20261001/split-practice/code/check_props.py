"""Exact checks (fractions.Fraction) for the new statements in note.md.

  [P1] q(v0, w) = (v0+t)(v0+t+1) + w^T S w,  t = w^T x,  S = X - x x^T.
  [P2] For rational PSD X with X00 = 1:  min_v q(v) = -1/4  iff  the integer
       kernel of X meets e0 + 2 Z^N (decided by elimination over GF(2)).  Checked
       against thm3_exact on random rational PSD matrices of rank < N
       (and full rank, where the kernel is trivial).
  [P3] Rank-1 points and 0/1 splits: for X = l(x) with
       x = (-(12/5) a_1, ..., -(12/5) a_n, (12 T - 2)/5), some v in {0,1}^{n+2}
       is violated iff the subset-sum instance (a, T) is solvable.  Checked by
       complete enumeration of {0,1}^{n+2}.
  [P4] Dinkelbach separator: covered by test_lattice.py (test_ratio).
  [P5] Non-primitive splits are dominated: for v = (-s-1, k w'), k >= 2,
       t = floor((2s+1-k)/(2k)), a = k^2 - b, b = ((2s+1)k - (2t+1)k^2)/2,
       c = (k(t+1)-s)(k(t+1)-s-1):  q(v) = a q(v_t) + b q(v_{t+1}) + c X00
       with a, b, c >= 0 and v_t = (-t-1, w').  Checked as an exact identity on
       random rational symmetric X (not only PSD).
"""
import itertools
import math
import random
import sys
from fractions import Fraction as F

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lattice import thm3_exact, col_hnf, q_exact  # noqa: E402

random.seed(11)


def check_p1(trials=300):
    bad = 0
    for _ in range(trials):
        N = random.randint(2, 6)
        B = [[F(random.randint(-5, 5), random.randint(1, 4)) for _ in range(N)] for _ in range(N)]
        X = [[sum(B[k][i] * B[k][j] for k in range(N)) for j in range(N)] for i in range(N)]
        if X[0][0] == 0:
            continue
        X = [[e / X[0][0] for e in row] for row in X]
        v = [random.randint(-4, 4) for _ in range(N)]
        x = [X[0][i] for i in range(1, N)]
        w = v[1:]
        t = sum(F(a) * b for a, b in zip(w, x))
        S = [[X[i][j] - X[0][i] * X[0][j] for j in range(1, N)] for i in range(1, N)]
        wSw = sum(w[i] * S[i][j] * w[j] for i in range(N - 1) for j in range(N - 1))
        bad += q_exact(X, v) != (v[0] + t) * (v[0] + t + 1) + wSw
    print(f"[P1] identity q = (v0+t)(v0+t+1) + w^T S w on {trials} random cases: {bad} failures")
    return bad


def odd_kernel(X):
    N = len(X)
    den = 1
    for row in X:
        for e in row:
            den = den * e.denominator // math.gcd(den, e.denominator)
    M = [[int(e * den) for e in row] for row in X]
    # column HNF of M: columns r..N-1 of U span the integer kernel
    H, U = col_hnf(M)
    r = sum(1 for j in range(N) if any(H[i][j] != 0 for i in range(len(H))))
    # rank via nonzero columns of M U
    MU = [[sum(M[i][k] * U[k][j] for k in range(N)) for j in range(N)] for i in range(N)]
    zero_cols = [j for j in range(N) if all(MU[i][j] == 0 for i in range(N))]
    # is e0 in (integer kernel) + 2 Z^N ?  Gaussian elimination over GF(2)
    vecs = [[U[i][j] % 2 for i in range(N)] for j in zero_cols]
    target = [1] + [0] * (N - 1)
    rows = []
    for vec in vecs:
        for piv, rw in rows:
            if vec[piv]:
                vec = [(a + b) % 2 for a, b in zip(vec, rw)]
        if any(vec):
            piv = vec.index(1)
            rows.append((piv, vec))
    t = target[:]
    for piv, rw in rows:
        if t[piv]:
            t = [(a + b) % 2 for a, b in zip(t, rw)]
    return not any(t), len(zero_cols)


def check_p2(trials=200):
    bad = 0; quarter = 0; deficient = 0
    for _ in range(trials):
        N = random.randint(2, 6); r = random.randint(1, N)
        while True:
            B = [[random.randint(-3, 3) for _ in range(N)] for _ in range(r)]
            n0 = sum(B[k][0] ** 2 for k in range(r))
            if n0:
                break
        X = [[F(sum(B[k][i] * B[k][j] for k in range(r)), n0) for j in range(N)] for i in range(N)]
        res = thm3_exact(X)
        odd, kdim = odd_kernel(X)
        deficient += kdim > 0
        is_quarter = res["q"] == F(-1, 4)
        quarter += is_quarter
        bad += is_quarter != odd
    print(f"[P2] min q = -1/4 iff integer kernel meets e0 + 2Z^N: {trials} matrices "
          f"({deficient} rank-deficient, {quarter} with min q = -1/4): {bad} failures")
    return bad


def check_p3():
    bad = 0; cnt = 0; yes = 0
    for n in range(1, 7):
        for a in itertools.product(range(1, 6), repeat=n):
            if list(a) != sorted(a):
                continue
            A = sum(a)
            for T in range(1, A + 1):
                solv = any(sum(c) == T for k in range(n + 1) for c in itertools.combinations(a, k))
                x = [F(-12 * ai, 5) for ai in a] + [F(12 * T - 2, 5)]
                viol = False
                for v in itertools.product((0, 1), repeat=n + 2):
                    tt = v[0] + sum(F(vi) * xi for vi, xi in zip(v[1:], x))
                    if tt * (tt + 1) < 0:
                        viol = True
                        break
                cnt += 1; yes += solv
                bad += viol != solv
        if n >= 5:
            break
    print(f"[P3] rank-1 0/1-split construction: {cnt} subset-sum instances ({yes} solvable): "
          f"{bad} mismatches")
    return bad


def check_p5(trials=500):
    bad = 0
    for _ in range(trials):
        N = random.randint(2, 6)
        A = [[F(random.randint(-6, 6), random.randint(1, 5)) for _ in range(N)] for _ in range(N)]
        X = [[A[i][j] + A[j][i] for j in range(N)] for i in range(N)]
        X[0][0] = F(1)
        wp = [random.randint(-4, 4) for _ in range(N - 1)]
        k = random.randint(2, 7); s_ = random.randint(-30, 30)
        t = (2 * s_ + 1 - k) // (2 * k)
        b = F((2 * s_ + 1) * k - (2 * t + 1) * k * k, 2); a = k * k - b
        c = (k * (t + 1) - s_) * (k * (t + 1) - s_ - 1)
        v = [-s_ - 1] + [k * x for x in wp]
        vt = [-t - 1] + wp; vt1 = [-t - 2] + wp
        lhs = q_exact(X, v); rhs = a * q_exact(X, vt) + b * q_exact(X, vt1) + c * X[0][0]
        bad += (lhs != rhs) or a < 0 or b < 0 or c < 0
    print(f"[P5] non-primitive split = a*q(v_t) + b*q(v_t+1) + c with a,b,c >= 0: {trials} cases: {bad} failures")
    return bad


if __name__ == "__main__":
    tot = check_p1() + check_p2() + check_p3() + check_p5()
    print("ALL PROPOSITION CHECKS PASSED" if tot == 0 else f"FAILURES {tot}")
