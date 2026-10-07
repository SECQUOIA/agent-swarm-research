"""Exact checks for the W5 optsets verification (Section 9, Appendix F).

1. Lemma lem:endpointid with the new definition pi_t(v;x) = Pr(Y_{B_t}=v):
   identity eq:endpointid at random rational x, on random coordinatewise
   concave quadratics over a path decomposition; OPT = M_{t0}.
2. Proposition prop:sshard: at every zero of F, the box KKT multiplier is
   2 on x and 0 on xi, and H + Lambda = H_sq is PSD (exact LDL).
3. Zero-sum reduction used for coNP-hardness of uniqueness in D.
4. Constants: 99/64 bound of lem:proximal(ii), 48*sqrt(2) < 68,
   eq:logabsorb with n in place of n_P.
"""
from fractions import Fraction as Fr
from itertools import product, combinations
import math
import random

random.seed(5)


def quad(H, b, c, x):
    n = len(x)
    return (sum(H[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) / 2
            + sum(b[i] * x[i] for i in range(n)) + c)


# ---------- 1. endpoint identity on a path decomposition ----------
def check_endpoint(trials=200):
    for _ in range(trials):
        n = random.randint(2, 5)
        lo = [Fr(random.randint(-3, 1)) for _ in range(n)]
        up = [lo[i] + random.randint(1, 3) for i in range(n)]
        H = [[Fr(0)] * n for _ in range(n)]
        for i in range(n):
            H[i][i] = Fr(-random.randint(0, 3))
        for i in range(n - 1):
            v = Fr(random.randint(-4, 4))
            H[i][i + 1] = H[i + 1][i] = v
        b = [Fr(random.randint(-5, 5)) for _ in range(n)]
        c = Fr(random.randint(-3, 3))
        # bags B_t = {t, t+1}, t = 0..n-2, rooted at t0 = 0; child of t is t+1
        bags = [(t, t + 1) for t in range(n - 1)]
        E = [(lo[i], up[i]) for i in range(n)]

        # factor q_t: pair term (t,t+1), diagonal and linear terms of t
        # (and of n-1 in the last bag), constant in bag 0
        def q(t, vt, vt1):
            val = H[t][t + 1] * vt * vt1 + H[t][t] * vt * vt / 2 + b[t] * vt
            if t == n - 2:
                val += H[t + 1][t + 1] * vt1 * vt1 / 2 + b[t + 1] * vt1
            if t == 0:
                val += c
            return val
        # post-order: M_t(v_{B_t^up}) with B_t^up = {t} for t >= 1, empty for t=0
        M = {}
        r = {}
        for t in reversed(range(n - 1)):
            def bracket(vt, vt1, t=t):
                s = q(t, vt, vt1)
                if t + 1 <= n - 2:
                    s += M[t + 1][vt1]
                return s
            if t >= 1:
                M[t] = {vt: min(bracket(vt, w) for w in E[t + 1]) for vt in E[t]}
                r[t] = {(vt, w): bracket(vt, w) - M[t][vt] for vt in E[t] for w in E[t + 1]}
            else:
                M[0] = min(bracket(vt, w) for vt in E[0] for w in E[1])
                r[0] = {(vt, w): bracket(vt, w) - M[0] for vt in E[0] for w in E[1]}
        # brute force OPT over endpoints and check M_{t0}
        opt_end = min(quad(H, b, c, list(v)) for v in product(*E))
        assert opt_end == M[0], (opt_end, M[0])
        for _ in range(5):
            x = [lo[i] + Fr(random.randint(0, 12), 12) * (up[i] - lo[i]) for i in range(n)]
            s = [up[i] - lo[i] for i in range(n)]

            def pr(i, vi):
                return (up[i] - x[i]) / s[i] if vi == lo[i] else (x[i] - lo[i]) / s[i]
            rhs = sum(r[t][(vt, w)] * pr(t, vt) * pr(t + 1, w)
                      for t in range(n - 1) for vt in E[t] for w in E[t + 1])
            rhs += sum(-H[i][i] * (x[i] - lo[i]) * (up[i] - x[i]) for i in range(n)) / 2
            assert quad(H, b, c, x) - M[0] == rhs
            assert all(v >= 0 for t in r for v in r[t].values())
    return trials


# ---------- 2. prop:sshard certificate ----------
def ldl_psd(A):
    A = [row[:] for row in A]
    n = len(A)
    for k in range(n):
        p = A[k][k]
        if p < 0:
            return False
        if p == 0:
            if any(A[k][j] != 0 for j in range(k + 1, n)):
                return False
            continue
        for i in range(k + 1, n):
            f = A[i][k] / p
            for j in range(k, n):
                A[i][j] -= f * A[k][j]
    return True


def check_sshard(trials=100):
    done = 0
    for _ in range(trials):
        m = random.randint(1, 4)
        a = [random.randint(-4, 4) for _ in range(m)]
        A = sum(abs(t) for t in a)
        if A < 1:
            continue
        xh = [random.randint(0, 1) for _ in range(m)]
        a0 = sum(a[i] * xh[i] for i in range(m))
        # variables z = (x_1..x_m, xi_1..xi_m); F = sum_i (xi_i - xi_{i-1} - a_i x_i)^2
        #   + (xi_m - a0)^2 + sum_i x_i(1-x_i)
        N = 2 * m
        rows = []  # affine forms (coef vector, const)
        for i in range(m):
            co = [Fr(0)] * N
            co[m + i] = Fr(1)
            if i > 0:
                co[m + i - 1] = Fr(-1)
            co[i] = Fr(-a[i])
            rows.append((co, Fr(0)))
        co = [Fr(0)] * N
        co[2 * m - 1] = Fr(1)
        rows.append((co, Fr(-a0)))
        Hsq = [[sum(2 * r[0][i] * r[0][j] for r in rows) for j in range(N)] for i in range(N)]
        H = [row[:] for row in Hsq]
        for i in range(m):
            H[i][i] -= 2
        # every zero of F
        for xs in product((0, 1), repeat=m):
            if sum(a[i] * xs[i] for i in range(m)) != a0:
                continue
            xi = [sum(a[k] * xs[k] for k in range(i + 1)) for i in range(m)]
            assert all(-A <= v <= A for v in xi)
            z = [Fr(v) for v in xs] + [Fr(v) for v in xi]
            grad = [sum(H[i][j] * z[j] for j in range(N)) for i in range(N)]
            # linear part: from squares and from x_i(1-x_i) = x_i - x_i^2
            lin = [Fr(0)] * N
            for co, k in rows:
                for i in range(N):
                    lin[i] += 2 * co[i] * k
            for i in range(m):
                lin[i] += 1
            grad = [grad[i] + lin[i] for i in range(N)]
            lam = []
            box = [(0, 1)] * m + [(-A, A)] * m
            for i in range(N):
                lo, up = box[i]
                if z[i] == lo:
                    assert grad[i] >= 0
                elif z[i] == up:
                    assert grad[i] <= 0
                else:
                    assert grad[i] == 0
                lam.append(2 * abs(grad[i]) / (up - lo))
            assert lam == [2] * m + [0] * m, lam
            HL = [[H[i][j] + (lam[i] if i == j else 0) for j in range(N)] for i in range(N)]
            assert HL == Hsq and ldl_psd(HL)
        done += 1
    return done


# ---------- 3. zero-sum reduction ----------
def check_zero_sum(trials=3000):
    for _ in range(trials):
        k = random.randint(1, 6)
        bs = [random.randint(1, 9) for _ in range(k)]
        T = random.randint(1, 30)
        ss = any(sum(c) == T for r in range(k + 1) for c in combinations(bs, r))
        items = bs + [-T]
        zs = any(sum(c) == 0 for r in range(1, k + 2) for c in combinations(items, r))
        assert ss == zs
    return trials


# ---------- 4. constants ----------
def check_constants():
    th2 = Fr(1, 16)
    val = 1 + Fr(1, 2) * (1 + th2 / 2) + th2 / 2
    assert val == Fr(99, 64)
    assert Fr(99, 64) / 4 == Fr(99, 256)
    assert 48 * 48 * 2 < 68 * 68
    for p in range(1, 41):
        for n in list(range(0, 2000)) + [10 ** k for k in range(4, 13)]:
            assert math.ceil(math.log2(n + 2)) ** p <= 2 * p ** p * (n + 2), (p, n)
    return True


if __name__ == '__main__':
    print('endpoint identity trials:', check_endpoint())
    print('sshard instances:', check_sshard())
    print('zero-sum reduction trials:', check_zero_sum())
    print('constants:', check_constants())
    print('all checks passed')
