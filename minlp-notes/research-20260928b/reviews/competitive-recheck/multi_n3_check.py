"""Theorem N3 recheck (f = x^2 on [0,1]^2, alpha = 1), exact rationals, written for this recheck.

Validity and every rule's decision depend on the node only through its x-interval and its
z-width (F_z = -w^2/4, z-minimizer = midpoint), so tree sizes are computed by memoized recursion
on (x-interval, z-width); this is a different method from simulating the tree node by node.
F_x is minimized directly over candidate points (ends and the stationary point), not taken
from the note's closed form; the closed form is then asserted.

Checks:
 1. tree sizes of multi, omega, deficit, bis (both tie-breaks where ties occur);
 2. the proof's structure: every node L_j x J at depth D = 2k (2 <= k <= K) is internal in multi's
    tree, giving >= sum_{k=2}^K (k-1) 4^k internal nodes;
 3. the explicit guillotine certificate of part (a) with a rational h <= 2 sqrt(eps), validated
    exactly box by box, and its size against the stated bound.
Usage: python3 multi_n3_check.py MAXPOW   (eps = 10^-2 .. 10^-MAXPOW)
"""
import math
import sys
from fractions import Fraction as Fr
from functools import lru_cache

sys.setrecursionlimit(100000)
EPS = None


def Fx(l, u):
    """min over [l,u] of eps + x^2 - (x-l)(u-x) = eps + 2x^2 - (l+u)x + lu; returns (value, argmin)."""
    def g(x):
        return EPS + 2 * x * x - (l + u) * x + l * u
    cands = [l, u]
    xs = (l + u) / 4
    if l <= xs <= u:
        cands.append(xs)
    best = min(cands, key=lambda x: (g(x), x))
    v = g(best)
    # closed form of the note
    if u > 3 * l:
        assert best == (l + u) / 4 and v == EPS + l * u - (l + u) ** 2 / 8
    else:
        assert best == l and v == EPS + l * l
    return v, best


def ax_of(l, u):
    v, y = Fx(l, u)
    return v, y, (y - l) * (u - y)


@lru_cache(maxsize=None)
def T_multi(l, u, D):
    vx, y, ax = ax_of(l, u)
    if vx - Fr(1, 4 ** D) / 4 >= 0:
        return 1
    xs = [(l, y), (y, u)] if ax > 0 else [(l, u)]
    return 1 + 2 * sum(T_multi(a, b, D + 1) for a, b in xs)


def make_single(rule, tie_to_x):
    @lru_cache(maxsize=None)
    def T(l, u, w):
        vx, y, ax = ax_of(l, u)
        vz, az = -w * w / 4, w * w / 4
        if vx + vz >= 0:
            return 1
        if rule == "omega":
            gx, gz = ax, az
            tie = gx == gz
            x_first = gx > gz
        elif rule == "deficit":
            if ax == 0:
                x_first, tie = False, False
            else:
                tie = vx == vz
                x_first = vx < vz
        elif rule == "bis":
            tie = (u - l) == w
            x_first = (u - l) > w
        if tie:
            T.ties += 1
            x_first = tie_to_x
        if x_first:
            s = y if rule != "bis" else (l + u) / 2
            assert l < s < u
            return 1 + T(l, s, w) + T(s, u, w)
        return 1 + 2 * T(l, u, w / 2)
    T.ties = 0
    return T


def spine_check(K):
    """Every node L_j x J at depth 2k is internal in multi's tree (2 <= k <= K); count them."""
    total = 0
    for k in range(2, K + 1):
        l = Fr(1, 4 ** (k + 1))
        # path to J_k: [0,1] -> [0,1/4] -> ... -> [0,4^-k] at depth k -> J_k = [l, 4l] at depth k+1
        r = [l]
        for _ in range(k):
            r.append((r[-1] + 4 * l) / 4)
        for j in range(1, k):
            Lj = (r[j - 1], r[j])
            assert Lj[1] <= 3 * Lj[0]                     # never split in x again
            vx, _, _ = ax_of(*Lj)
            for D in range(k + 1 + j, 2 * k + 1):
                assert vx - Fr(1, 4 ** D) / 4 < 0            # invalid, hence internal
            total += 4 ** k                                  # the 2^(2k) dyadic z-intervals at D = 2k
    return total


def certificate(eps):
    """Part (a) certificate with rational h <= 2 sqrt(eps); exact validity; returns size."""
    # rational h with h^2 <= 4 eps, close to 2 sqrt(eps)
    q = 10 ** 12
    h = Fr(math.isqrt(int(4 * eps * q * q)), q)
    assert h * h <= 4 * eps
    strips = [(Fr(0), h)]
    t = h
    while t < 1:
        strips.append((t, min(2 * t, Fr(1))))
        t *= 2
    count = 0
    for idx, (l, u) in enumerate(strips):
        vx, _ = Fx(l, u)
        if idx == 0:
            # z-pieces of width <= sqrt(2 eps): n = ceil(1/sqrt(2 eps)) pieces
            n = math.isqrt(int(1 / (2 * eps)))
            while Fr(1, n * n) > 2 * eps:
                n += 1
        else:
            assert u <= 2 * l
            n = math.ceil(1 / (2 * l))                       # pieces of width 1/n <= 2l
        w = Fr(1, n)
        assert vx - w * w / 4 >= 0, (idx, l, u)
        count += n
    return count


def certificate_tight(eps):
    """Same strips, but the fewest z-pieces allowed by the exact strip value F_x (the note's
    float variant uses this); exact validity; returns size."""
    q = 10 ** 12
    h = Fr(math.isqrt(int(4 * eps * q * q)), q)
    strips = [(Fr(0), h)]
    t = h
    while t < 1:
        strips.append((t, min(2 * t, Fr(1))))
        t *= 2
    count = 0
    for (l, u) in strips:
        vx, _ = Fx(l, u)
        n = max(1, math.isqrt(int(1 / (4 * vx))))           # need (1/n)^2 / 4 <= vx
        while n > 1 and Fr(1, (n - 1) ** 2) / 4 <= vx:
            n -= 1
        while Fr(1, n * n) / 4 > vx:
            n += 1
        assert vx - Fr(1, n * n) / 4 >= 0
        count += n
    return count


def main(maxpow):
    global EPS
    print(" eps  | multi  | omega(tie z / tie x) | deficit | bis (tie z / tie x) | cert N | (a) bound | "
          "proved internal >= | T_multi/(2N-1) | T_omega/(2N-1)")
    for p in range(2, maxpow + 1):
        EPS = Fr(1, 10 ** p)
        for f in (T_multi,):
            f.cache_clear()
        tm = T_multi(Fr(0), Fr(1), 0)
        res = {}
        for rule in ("omega", "deficit", "bis"):
            if rule == "bis" and p > 6:
                res[rule] = ("-", "-")
                continue
            vals = []
            for tie in (False, True):
                T = make_single(rule, tie)
                vals.append(T(Fr(0), Fr(1), Fr(1)))
                if T.ties == 0:
                    vals.append(vals[-1])
                    break
            res[rule] = tuple(vals)
        K = 0
        while Fr(5, 36) / Fr(16) ** (K + 1) >= EPS:   # K = floor(log_16(5/(36 eps)))
            K += 1
        lb_int = sum((k - 1) * 4 ** k for k in range(2, K + 1))
        spine = spine_check(K)
        assert spine == lb_int and tm >= 2 * lb_int + 1
        N = certificate(EPS)
        Nt = certificate_tight(EPS)
        print(f"        certificate with widths 2l: {N}; tight exact variant: {Nt}")
        e = float(EPS)
        bound = 1 / math.sqrt(2 * e) + 1 / (2 * math.sqrt(e)) + math.log2(1 / (2 * math.sqrt(e))) + 3
        assert N <= bound
        print(f" 1e-{p} | {tm} | {res['omega'][0]} / {res['omega'][1]} | {res['deficit'][0]} / {res['deficit'][1]} | "
              f"{res['bis'][0]} / {res['bis'][1]} | {N} | {bound:.1f} | {lb_int} | {tm/(2*N-1):.2f} | "
              f"{res['omega'][0]/(2*N-1):.2f}", flush=True)
        # the explicit lower bound in the theorem's final form
        if K >= 2:
            assert 2 * lb_int + 1 >= 0.186 * (K - 1) * e ** -0.5 * 0.999
            print(f"        K = {K}; 0.186 (K-1) eps^-1/2 = {0.186*(K-1)*e**-0.5:.0f} <= 2*internal+1 = {2*lb_int+1}")


if __name__ == "__main__":
    main(int(sys.argv[1]))
