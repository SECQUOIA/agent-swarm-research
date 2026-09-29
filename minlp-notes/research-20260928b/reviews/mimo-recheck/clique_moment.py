"""Item (4): the first-moment upper bound of Theorem 5.1(a).

 (a) For beta = 1, rho = c log N: the expected number (Lemma 2.1 bound) of
     ternary points c in {0,1,2}^N with n_1 = n entries 1 and F(c) < W,
       E(n) = sum_m C(N,n) C(N-n,m) (1 + rho (n + 4m)/(4N))^{-N/2},
     scanned over all n (no cap), m up to min(4000, N - n) (terms checked to
     decay).  Reports the last n with E(n) >= 1e-3 against N^{1-c/8}.
 (b) The displayed small-regime inequality
       C(N,n) N^{-c'n/8} sum_m C(N,m) N^{-c'm/2} <= (e N^{1-c'/8}/n)^n exp(N^{1-c'/2})
     and the tail bound sum_{n >= D} ... <= 2 exp(-D + N^{1-c'/2}),
     D = e^2 N^{1-c'/8}, evaluated in logs on a grid.
"""
import numpy as np
from scipy.special import gammaln, logsumexp


def lC(n, k):
    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)


def logE(N, rho, n, mmax=4000):
    m = np.arange(0, min(mmax, N - n) + 1)
    t = lC(N, n) + lC(N - n, m) - (N / 2) * np.log1p(rho * (n + 4 * m) / (4 * N))
    return logsumexp(t), t[-1] - t.max()


def part_a():
    print("(a) last n_1 with first-moment count >= 1e-3 (beta = 1)")
    for N in (10 ** 4, 10 ** 5):
        for c in (3.0, 4.0, 6.0):
            rho = c * np.log(N)
            ns = np.arange(1, N + 1)
            # coarse scan then refine
            step = max(1, N // 2000)
            vals = np.array([logE(N, rho, int(n))[0] for n in ns[::step]])
            idx = np.nonzero(vals >= np.log(1e-3))[0]
            last = int(ns[::step][idx[-1]]) if len(idx) else 0
            lo, hi = max(1, last - step), min(N, last + step)
            fine = [n for n in range(lo, hi + 1) if logE(N, rho, n)[0] >= np.log(1e-3)]
            last = max(fine) if fine else last
            _, tail = logE(N, rho, last)
            base = N ** (1 - c / 8)
            print("   N=%d c=%g: last n_1 = %d; N^(1-c/8) = %.1f; ratio %.1f (ratio to e^2 N^(1-c/8): %.2f); last-m term / max term = e^%.0f"
                  % (N, c, last, base, last / base, last / (np.e ** 2 * base), tail), flush=True)


def part_b():
    worst1 = -np.inf; worst2 = -np.inf
    for N in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6):
        L = np.log(N)
        for cp in (0.5, 1.0, 2.0, 3.0, 5.0, 7.5):
            for n in np.unique(np.geomspace(1, N / 2, 60).astype(int)):
                m = np.arange(0, N + 1)
                lhs = lC(N, n) - cp * n * L / 8 + logsumexp(lC(N, m) - cp * m * L / 2)
                rhs = n * (1 + (1 - cp / 8) * L - np.log(n)) + N ** (1 - cp / 2)
                worst1 = max(worst1, lhs - rhs)
            D = np.e ** 2 * N ** (1 - cp / 8)
            nn = np.arange(int(np.ceil(D)), N + 1)
            if len(nn):
                terms = nn * (1 + (1 - cp / 8) * L - np.log(nn)) + N ** (1 - cp / 2)
                worst2 = max(worst2, logsumexp(terms) - (np.log(2) - D + N ** (1 - cp / 2)))
    print("(b) max over the grid of log(lhs) - log(rhs): displayed inequality %.2e, tail bound %.2e (both must be <= 0)" % (worst1, worst2))


if __name__ == "__main__":
    part_b(); part_a()
