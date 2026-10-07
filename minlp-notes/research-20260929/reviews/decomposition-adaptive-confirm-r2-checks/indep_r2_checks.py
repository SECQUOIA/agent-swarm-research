"""Independent checks for the second confirmation round of extension-adaptive.md.

  python3 indep_r2_checks.py

Part 1: sup-norm and Euclidean localization ratios by level, recomputed from the author's
        logs (oracle_eps1e-6, scaling_eps1e-4, random_n8/n16_eps1e-4), with s_i = 2^{1-i}.
Part 2: split leaves per bag per level of the random-c oracle runs at n = 16.
Part 3: Gamma(d/2+1)/(4 pi)^{d/2} (lower bound on N_dec/Psi for one flat bag).
Part 4: size bound of Theorem B.2(b) against the old and corrected Summary O-forms (C = 16),
        on a grid and 20,000 random draws (log2 arithmetic, no overflow).
Does not import the author's code.
"""
import itertools
import random
import re
from math import lgamma, log, log2, pi, e, exp, sqrt, ceil

LOGS = "../../theory-decomposition/adaptive/logs/"


def runs(fn):
    rows = []
    for line in open(LOGS + fn):
        m = re.match(r"p=\s*(-?\d+) i=\s*(\d+) .*live_mean=\s*([\d.]+).*dx2=([\d.e+-]+) dxinf=([\d.e+-]+)", line)
        if m:
            rows.append((int(m.group(1)), int(m.group(2)), float(m.group(3)),
                         float(m.group(4)), float(m.group(5))))
        elif line.startswith("SUMMARY"):
            tag = line.split()[1]
            n = int(re.search(r" n=(\d+)", line).group(1))
            lastp = rows[-1][0]
            yield tag, n, [r for r in rows if r[0] == lastp]
            rows = []


def part1_2():
    print("Part 1/2: per level of the final pass: i:dxinf/s_i ; split per bag per level / n")
    for fn in ["oracle_eps1e-6.log", "scaling_eps1e-4.log", "random_n8_eps1e-4.log",
               "random_n16_eps1e-4.log"]:
        for tag, n, rs in runs(fn):
            loc = " ".join("%d:%.2f" % (i, dxi / (2 * 2.0 ** -i)) for _, i, _, _, dxi in rs)
            smax = max(rs, key=lambda r: r[2])
            print("%-20s %-13s n=%2d  %s" % (fn, tag, n, loc))
            print("%-20s %-13s n=%2d  split max %.1f = %.2f n at level %d" % (
                "", "", n, smax[2], smax[2] / n, smax[1]))
            if fn == "oracle_eps1e-6.log":
                r2 = [dx2 / (2 * 2.0 ** -i) for _, i, _, dx2, _ in rs if i >= 5]
                print("%-20s %-13s n=%2d  dx2/s_i from level 5: %.2f-%.2f" % ("", "", n, min(r2), max(r2)))


def part3():
    f = lambda d: exp(lgamma(d / 2 + 1) - (d / 2) * log(4 * pi))
    below = [d for d in range(1, 200) if f(d) < 1]
    print("Part 3: Gamma(d/2+1)/(4 pi)^{d/2} < 1 for d in [%d, %d] (%d values); d=62: %.3f, d=63: %.3f, "
          "d=80: %.3g, d=120: %.3g; >= (d/(8 pi e))^{d/2} for d=1..199: %s" % (
              below[0], below[-1], len(below), f(62), f(63), f(80), f(120),
              all(f(d) >= (d / (8 * pi * e)) ** (d / 2) for d in range(1, 200))))


def lse2(*xs):
    m = max(xs)
    return m + log2(sum(2 ** (x - m) for x in xs))


def b2_log2(alpha, eps, K, d):
    """log2 of K[ceil(sqrt(alpha d/(2 eps)))^d + 2(J+1)(4/theta)^d + 1] + 2(K-1)."""
    fat = d * log2(ceil(sqrt(alpha * d / (2 * eps))))
    h0 = sqrt(2 * eps / (K * d * alpha ** 2))
    J = max(0, ceil(log2(1 / h0)))
    tmax = min(1.0, 2 / sqrt(alpha * d))
    j = 0
    while 2.0 ** -j > tmax * (1 + 1e-15):
        j += 1
    shell = log2(2 * (J + 1)) + d * (2 + j)
    return lse2(log2(K) + lse2(fat, shell, 0.0), log2(2 * (K - 1))), 2 + j


def part4():
    old = lambda a, ep, K, d: log2(K) + lse2((d / 2) * log2(a * d / ep), d * 4 + log2(log2(K / ep)))
    new = lambda a, ep, K, d: log2(K) + lse2((d / 2) * log2(a * d / ep),
                                             d * log2(16 * max(1, sqrt(a * d))) + log2(log2(K / ep)))
    for d in (1024, 4096):
        _, l4t = b2_log2(1.0, 0.5, 2, d)
        print("Part 4: alpha=1, eps=1/2, d=%d: 4/theta=%d, fat base %d, sqrt(alpha d/eps)=%.2f" % (
            d, 2 ** l4t, ceil(sqrt(d)), sqrt(2 * d)))
    random.seed(0)
    grid = list(itertools.product([1, 0.3, 0.1, 1e-2, 1e-3, 1e-4, 1e-6], [1, 0.5, 1e-1, 1e-2, 1e-4, 1e-6, 1e-9],
                                  [2, 3, 16, 1024, 10 ** 6],
                                  [1, 2, 3, 4, 8, 16, 64, 256, 1024, 4096, 16384]))
    rnd = [(10 ** random.uniform(-7, 0), 10 ** random.uniform(-10, 0), random.randint(2, 10 ** 6),
            random.randint(1, 20000)) for _ in range(20000)]
    worst_new, nfail, worst_old = -1e300, 0, 0.0
    for a, ep, K, d in grid + rnd:
        t, _ = b2_log2(a, ep, K, d)
        worst_new = max(worst_new, t - new(a, ep, K, d))
        o = t - old(a, ep, K, d)
        if o > 0:
            nfail += 1
            worst_old = max(worst_old, o)
    print("Part 4: %d cases; bound/corrected form <= %.3f; old form (C=16) below the bound in %d cases, "
          "by up to 2^%.0f" % (len(grid) + len(rnd), 2 ** worst_new, nfail, worst_old))
    for K in (2, 1024):
        t, _ = b2_log2(0.1, 1.0, K, 4096)
        print("Part 4: alpha=0.1, eps=1, K=%d, d=4096: bound/old form = 2^%.1f" % (K, t - old(0.1, 1.0, K, 4096)))


if __name__ == "__main__":
    part1_2()
    part3()
    part4()
