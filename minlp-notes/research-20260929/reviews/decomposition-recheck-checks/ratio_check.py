"""Recheck of Theorem 4.1 (ratio of proven single-tree and decomposition bounds).

Independent of the note's revision_checks.py. Works in log space so that
astronomically small eps (given through L = ln(1/eps)) can be handled.
"""
import math

import mpmath as mp

mp.mp.dps = 40
LN2 = math.log(2.0)
BASE_EXACT = math.sqrt(2 * math.e / math.pi)


def ln_term1(n, L):
    """ln of Corollary 2.1 closed form 0.068 sqrt(n) (2e/pi)^{n/2} log(0.2/(n eps)); -inf if <= 0."""
    arg = math.log(0.2 / n) + L
    if arg <= 0:
        return -math.inf
    return math.log(0.068) + 0.5 * math.log(n) + 0.5 * n * math.log(2 * math.e / math.pi) + math.log(arg)


def ln_term2(n, L):
    eps = math.exp(-L)
    return n * math.log(5 / 3) - (5 / 9) * (1 + 1.25 * eps)


def ln_b(n, L):
    """ln of Theorem 4.1(b): 3.36e7 (n-1) ((1/2) log2(1.96e6 (n-1)/eps) + 2)."""
    return math.log(3.36e7 * (n - 1)) + math.log(0.5 * (math.log2(1.96e6 * (n - 1)) + L / LN2) + 2)


def ln_ratio_normalized(n, L, base):
    lnr = max(ln_term1(n, L), ln_term2(n, L)) - ln_b(n, L)
    return lnr - (n * math.log(base) - 0.5 * math.log(n))


def main():
    print("# A. constants")
    print("sqrt(2e/pi) = %s" % mp.nstr(mp.sqrt(2 * mp.e / mp.pi), 12))
    q = math.log(1.3155 / BASE_EXACT)
    print("ln(1.3155/sqrt(2e/pi)) = %.4e" % q)
    c0 = 2 * math.sqrt(3 / 16) / math.sqrt(4 * math.pi) * math.exp(-0.5) / 2
    print("Cor 2.1 constant 0.0741? %.5f ; times e^(-1/12) = %.5f" % (c0, c0 * math.exp(-1 / 12)))
    # Case 1 constants
    print("log2(225) = %.4f ; log2(1.96e6*0.2) = %.4f" % (math.log2(225), math.log2(1.96e6 * 0.2)))
    k = (0.5 * math.log2(1.96e6 * 0.2) + 2) / math.log2(225) + 0.75
    print("case 1: (1/2)(log2(3.92e5)+1.5 L2)+2 <= %.4f L2 (note: 2.2)" % k)
    print("case 1: 3.36e7*2.2/ln2 = %.4e (note: 1.07e8)" % (3.36e7 * 2.2 / LN2))
    c1 = 0.034 / 1.07e8
    print("case 1 constant 0.034/1.07e8 = %.4e (note: 3.2e-10)" % c1)
    # the case-1 chain with the exact base (2e/pi)^{n/2}; the claim with 1.3155^n needs
    # (c1/3e-10) >= (1.3155/sqrt(2e/pi))^n
    nmax1 = math.log(c1 / 3e-10) / q
    print("case 1 proof with 1.3155^n gives >= 3e-10 only for n <= %.0f" % nmax1)
    # the first-term closed form with 1.3155 in place of (2e/pi)^{1/2}: 0.068*1.3155^n <= 0.0741 e^{-1/(6n)} (2e/pi)^{n/2}
    nmax0 = max(n for n in range(2, 200000) if 0.068 * math.exp(n * q) <= c0 * math.exp(-1 / (6 * n)))
    print("0.068 sqrt(n) 1.3155^n <= exact Cor 2.1 prefactor only for n <= %d" % nmax0)
    # Case 2 constants
    print("case 2: log2(1.96e6*25) = %.4f -> (1/2)(.)+2 = %.3f (note: 14.8)" % (
        math.log2(1.96e6 * 25), 0.5 * math.log2(1.96e6 * 25) + 2))
    r = (5 / 3) / 1.3155
    print("case 2: (5/3)/1.3155 = %.5f" % r)
    f = lambda n: 0.57 * r ** n / (3.36e7 * math.sqrt(n) * (14.8 + 1.5 * math.log2(n)))
    print("case 2 function at n=3: %.3e ; n=21 (first n where case 2 is nonempty): %.3e ; increasing on 3..400: %s" % (
        f(3), f(21), all(f(n + 1) > f(n) for n in range(3, 400))))
    print("case 2 nonempty (0.04/n^2 < 1e-4) iff n >= %d" % min(n for n in range(3, 100) if 0.04 / n ** 2 < 1e-4))

    print("# B. grid, n = 3..300, log10(1/eps) in [4, 40] step 0.005 (7201 points)")
    for base, name in [(1.3155, "1.3155"), (BASE_EXACT, "sqrt(2e/pi)")]:
        worst = (math.inf, None, None)
        for n in range(3, 301):
            for i in range(7201):
                L = (4 + 0.005 * i) * math.log(10)
                v = ln_ratio_normalized(n, L, base)
                if v < worst[0]:
                    worst = (v, n, L / math.log(10))
        print("min ratio / (%s^n/sqrt n) = %.4e at n=%d, eps=1e-%.3f" % (name, math.exp(worst[0]), worst[1], worst[2]))

    print("# C. infimum over all eps <= 1e-4 for large n (mpmath; L = ln(1/eps) may be astronomically large)")
    # term1/b increases in L to its limit, term2/b decreases, so inf_L max(...)/b is at the crossing
    # term1 = term2 (or at L = ln(1e4) if term1 already dominates there).
    def lnr(n, L, base):
        n = mp.mpf(n)
        t1 = mp.log(0.068) + mp.log(n) / 2 + n / 2 * mp.log(2 * mp.e / mp.pi) + mp.log(mp.log(0.2 / n) + L)
        t2 = n * mp.log(mp.mpf(5) / 3) - mp.mpf(5) / 9 * (1 + 1.25 * mp.exp(-L))
        lb = mp.log(3.36e7 * (n - 1)) + mp.log((mp.log(1.96e6 * (n - 1)) + L) / (2 * mp.log(2)) + 2)
        return max(t1, t2) - lb - (n * mp.log(base) - mp.log(n) / 2), t1 - t2
    for n in [300, 1000, 10000, 100000, 250000, 280000, 300000, 1000000]:
        lo, hi = mp.log(4 * mp.log(10)), mp.mpf(10) ** 6   # bracket on u = ln L
        for _ in range(400):
            mid = (lo + hi) / 2
            if lnr(n, mp.exp(mid), 1.3155)[1] > 0:
                hi = mid
            else:
                lo = mid
        Lc = mp.exp(hi)
        v, _ = lnr(n, Lc, 1.3155)
        vex, _ = lnr(n, Lc, mp.sqrt(2 * mp.e / mp.pi))
        print("n=%8d: crossing ln(1/eps) = %s; ratio/(1.3155^n/sqrt n) = %s; ratio/((2e/pi)^(n/2)/sqrt n) = %s" % (
            n, mp.nstr(Lc, 4), mp.nstr(mp.exp(v), 4), mp.nstr(mp.exp(vex), 4)))

    print("# E. exact infimum over ALL eps <= 1e-4 (not only >= 1e-40), n = 3..300, via the crossing")
    worst = (mp.inf, None, None)
    for n in range(3, 301):
        L0 = mp.log(mp.mpf(10) ** 4)
        v0, d0 = lnr(n, L0, 1.3155)
        if d0 >= 0:
            v, Lc = v0, L0
        else:
            lo, hi = mp.log(L0), mp.mpf(200)
            for _ in range(200):
                mid = (lo + hi) / 2
                if lnr(n, mp.exp(mid), 1.3155)[1] > 0:
                    hi = mid
                else:
                    lo = mid
            Lc = mp.exp(hi)
            v, _ = lnr(n, Lc, 1.3155)
        if v < worst[0]:
            worst = (v, n, Lc)
    print("inf over n in [3,300], all eps <= 1e-4: %s at n=%d, eps=exp(-%s)" % (
        mp.nstr(mp.exp(worst[0]), 5), worst[1], mp.nstr(worst[2], 5)))

    print("# D. McCormick variant: c = inf 0.57 (5/3)^n/(b) / ((5/3)^n/(n ln(n/eps)))")
    worst = (math.inf, None, None)
    for n in range(3, 2001):
        for i in range(0, 3601, 5):
            L = (4 + 0.01 * i) * math.log(10)
            val = math.log(0.57) + math.log(n) + math.log(math.log(n) + L) - ln_b(n, L)
            if val < worst[0]:
                worst = (val, n, L / math.log(10))
    print("min c on grid (n <= 2000, eps in [1e-40, 1e-4]) = %.3e at n=%d eps=1e-%.2f" % (math.exp(worst[0]), worst[1], worst[2]))
    print("limit eps->0: 0.57*2*ln2*n/(3.36e7 (n-1)) -> %.3e" % (0.57 * 2 * LN2 / 3.36e7))


if __name__ == "__main__":
    main()
