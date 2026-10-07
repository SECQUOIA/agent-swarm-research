"""Reviewer check of step 2 of the proof of Proposition A.6 (explicit configuration).

For n, level i (s = 2^{1-i}), bag t and p in [-r s, r s]^2 (r = r(n)), build x' with x'_t = p_1,
x'_{t+1} = p_2 and x'_j = (-1)^j s/2 otherwise. The configuration value is
F(x') - 0.4 sum_j q_{B_j}(x'_{V_j}). Worst case over admissible leaves: q = 0 in the three bags
containing t or t+1, and for the other bags the smallest q over dyadic boxes of level <= i containing
x'_{V_j} (computed by enumerating all ancestors). Claim: value <= -0.075 n s^2.
"""
import numpy as np

B, KAP, AL = 0.8, 0.1, 0.4


def F(x):
    return float(np.sum(x * x - KAP * x ** 4) + B * np.sum(x[:-1] * x[1:]))


def rn(n):
    r = 0
    while 2.8 * (r + 1) ** 2 + 0.8 * (r + 1) + 1.1 <= 0.075 * n:
        r += 1
    return r


def min_q_ancestors(pt, i):
    """smallest q_B(pt) over dyadic boxes of [-1,1]^2 of level 0..i containing pt."""
    best = np.inf
    for lev in range(i + 1):
        s = 2.0 * 2.0 ** (-lev)
        qs = 0.0
        for z in pt:
            k = np.floor((z + 1) / s)
            lo = -1 + k * s
            hi = lo + s
            # pt strictly inside by construction; clamp at the right boundary
            if hi > 1:
                lo, hi = 1 - s, 1.0
            qs += (z - lo) * (hi - z)
        best = min(best, qs)
    return best


def main():
    worst = -np.inf
    for n in (63, 64, 100, 200, 400):
        r = rn(n)
        for i in range(1, 9):
            s = 2.0 * 2.0 ** (-i)
            if r * s > 1:
                continue
            grid = np.linspace(-r * s, r * s, 9)
            for t in (0, 1, n // 2, n - 3, n - 2):
                for p1 in grid:
                    for p2 in grid:
                        x = np.array([(-1.0) ** j * s / 2 for j in range(n)])
                        x[t], x[t + 1] = p1, p2
                        q = 0.0
                        for j in range(n - 1):
                            if j in (t - 1, t, t + 1):
                                continue
                            q += min_q_ancestors(x[j:j + 2], i)
                        val = F(x) - AL * q
                        worst = max(worst, val / (0.075 * n * s * s))
        print("n=%d r=%d (2r)^2=%d done" % (n, r, (2 * r) ** 2), flush=True)
    print("max over cases of value/(0.075 n s^2) = %.4f (claim: <= -1)" % worst)


if __name__ == "__main__":
    main()
