"""Independent checks for the second confirmation review of extension-adaptive.md
(reviews/decomposition-adaptive-confirm-r1.md). Written from the note's formulas and from
Lemma 3.1 of [D]; it does not import check_phi_loss.py.

  python3 indep_r1_checks.py

Parts:
  1. Shell partition of [0,1]^d around the corner 0 (dp_certificate.shells, Lemma 3.1 of [D]):
     piece count versus (J+1)(4/theta)^d with J = max(0, ceil(log2(1/h0))), the old bound
     (log2(1/h0)+2)(4/theta)^d, the central cube [0, min(h0,1)]^d and w(B) <= theta dist_inf(B,0)
     for the other pieces.
  2. Proposition B.6(b): random and grid scan of (alpha, eps, K, d) with alpha <= 1, eps <= 1/2.
     Each of the three comparisons of the proof is checked separately, and the sum against the
     displayed constant with L = J + 1; also 1 <= L <= (1/2) log2(K d/(2 eps)) + 2; and the old L.
  3. Flat bag: Gamma(d/2+1)/(4 pi)^{d/2} < 1 exactly for d <= 62.
  4. Numbers quoted from the LS and RC logs (split per bag per level, localization by level,
     processed/size ratios, RC n = 8 cycle).
  5. RC round-1 shell partitions (n = 16, seed 0) under 1e-9 inward moves of each centre coordinate:
     leaf and cell counts and the smallest leaf width (uses the author's rc_lib and ls_lib).
"""
import math
import os
import random
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TD = os.path.join(HERE, "..", "..", "theory-decomposition")
sys.path.insert(0, TD)
from dp_certificate import shells  # noqa: E402

LOGS = os.path.join(TD, "adaptive", "logs")
LN2 = math.log(2.0)


def part1():
    print("== 1. shell partitions of [0,1]^d around the corner 0")
    worst_new, old_below = 0.0, 0
    for d in (1, 2, 3):
        for mu in (0, 1, 2):
            theta = 2.0 ** -mu
            for h0 in (1e-3, 0.013, 0.1, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 4.1, 7.07, 50.0):
                L, U = shells(np.zeros(d), h0, mu, d, lo=0.0, hi=1.0)
                cnt = len(L)
                J = max(0, math.ceil(math.log2(1.0 / h0)))
                new = (J + 1) * (4 / theta) ** d
                old = (math.log2(1.0 / h0) + 2) * (4 / theta) ** d
                worst_new = max(worst_new, cnt / new)
                if cnt > old:
                    old_below += 1
                    if d == 1 and mu == 0:
                        print("   old bound below count: d=%d mu=%d h0=%g count=%d old=%.2f new=%d" % (
                            d, mu, h0, cnt, old, new))
                w = (U - L).max(axis=1)
                dist = L.max(axis=1)  # sup-distance of a box in [0,1]^d from the corner 0
                central = np.all(L == 0, axis=1)
                assert central.sum() == 1
                cu = U[central][0]
                assert np.allclose(cu, min(h0, 1.0)), (d, mu, h0, cu)
                bad = (~central) & (w > theta * dist * (1 + 1e-12))
                assert not bad.any(), (d, mu, h0)
    print("   max count / ((J+1)(4/theta)^d) = %.3f; cases with count > old bound: %d" % (worst_new, old_below))
    print("   central cube = [0, min(h0,1)]^d and w(B) <= theta dist_inf(B,0) for all other pieces: ok")


def log_vd(d):
    return (d / 2) * math.log(math.pi) - math.lgamma(d / 2 + 1)


def lse(xs):
    m = max(xs)
    return m + math.log(sum(math.exp(x - m) for x in xs))


def b6_case(alpha, eps, K, d):
    h0 = math.sqrt(2 * eps / (K * d * alpha ** 2))
    J = max(0, math.ceil(math.log2(1 / h0)))
    Lnew = J + 1
    mu = 0
    while 2.0 ** -mu > min(1.0, 2 / math.sqrt(alpha * d)):
        mu += 1
    inv_theta4 = 4 * 2.0 ** mu
    # per-bag lower bound on sup Phi_2, divided by K: 2^{-(d+2)} M
    logM = max(0.0, (d / 2) * math.log(alpha / eps) - log_vd(d))
    lb = -(d + 2) * LN2 + logM
    # the three parts of the size bound of Theorem B.2(b), per bag
    fat = d * math.log(math.ceil(math.sqrt(alpha * d / (2 * eps))))
    shell = math.log(2 * Lnew) + d * math.log(inv_theta4)
    rest = math.log(3.0)  # K leaves plus 2(K-1) cells, at most 3K
    t1 = math.log(4.0) + (d / 2) * math.log(16 * math.pi * math.e)
    t2 = math.log(8 * Lnew) + (d / 2) * math.log(128 * math.pi * math.e)
    t3 = math.log(3.0) + (d + 2) * LN2
    parts_ok = (fat - lb <= t1 + 1e-12) and (shell - lb <= t2 + 1e-12) and (rest - lb <= t3 + 1e-12)
    exact_size = lse([math.log(K) + lse([fat, shell, 0.0]), math.log(2 * (K - 1))])
    ratio = exact_size - math.log(K) - lb
    const_new = lse([t1, t2, t3])
    Lold = math.log2(1 / h0) + 2
    const_old = lse([t1, t3] + ([math.log(8 * Lold) + (d / 2) * math.log(128 * math.pi * math.e)] if Lold > 0 else []))
    Lub = 0.5 * math.log2(K * d / (2 * eps)) + 2
    return dict(h0=h0, parts_ok=parts_ok, r_new=ratio - const_new, r_old=ratio - const_old,
                L_ok=(1 <= Lnew <= Lub + 1e-12))


def part2():
    print("== 2. Proposition B.6(b) scan")
    rng = random.Random(20260930)
    cases = []
    for alpha in (1.0, 0.3, 0.1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
        for eps in (0.5, 0.3, 0.1, 1e-2, 1e-4, 1e-6, 1e-9):
            for K in (2, 3, 5, 16, 100, 1024, 10 ** 6):
                for d in (1, 2, 3, 5, 8, 16, 33, 64, 128, 200):
                    cases.append((alpha, eps, K, d))
    for _ in range(20000):
        cases.append((10 ** rng.uniform(-7, 0), 10 ** rng.uniform(-10, math.log10(0.5)),
                      rng.randint(2, 10 ** 6), rng.randint(1, 200)))
    n = bad_parts = bad_new = bad_L = bad_old = 0
    worst_new = worst_old = -1e300
    hmin_old = math.inf
    for c in cases:
        r = b6_case(*c)
        n += 1
        bad_parts += not r["parts_ok"]
        bad_new += r["r_new"] > 1e-12
        bad_L += not r["L_ok"]
        worst_new = max(worst_new, r["r_new"])
        if r["r_old"] > 1e-12:
            bad_old += 1
            worst_old = max(worst_old, r["r_old"])
            hmin_old = min(hmin_old, r["h0"])
    print("   %d cases (alpha 1e-7..1, eps 1e-10..0.5, K 2..1e6, d 1..200)" % n)
    print("   L = J+1: part-wise comparison fails in %d; sum exceeds displayed constant in %d; "
          "max ratio/const = %.3f; L bounds fail in %d" % (bad_parts, bad_new, math.exp(worst_new), bad_L))
    print("   old L:   sum exceeds displayed constant in %d; max ratio/const = %.3f; smallest h0 = %.3g" % (
        bad_old, math.exp(worst_old), hmin_old))
    ex = b6_case(0.1, 0.5, 2, 1)
    print("   example alpha=0.1 eps=0.5 K=2 d=1: h0 = %.3f, log2(1/h0)+2 = %.3f" % (
        ex["h0"], math.log2(1 / ex["h0"]) + 2))


def part3():
    print("== 3. flat bag, fixed eps: Gamma(d/2+1)/(4 pi)^{d/2}")
    below = [d for d in range(1, 200) if math.lgamma(d / 2 + 1) - (d / 2) * math.log(4 * math.pi) < 0]
    print("   below 1 exactly for d in 1..%d (contiguous: %s)" % (max(below), below == list(range(1, max(below) + 1))))
    print("   value at d = 62, 63, 80, 120: " + ", ".join(
        "%.3g" % math.exp(math.lgamma(d / 2 + 1) - (d / 2) * math.log(4 * math.pi)) for d in (62, 63, 80, 120)))


def blocks(fn):
    rows = []
    for line in open(os.path.join(LOGS, fn)):
        m = re.match(r"p=\s*(-?\d+) i=\s*(\d+) .*live_mean=\s*([\d.]+) .*dx2=([\de.+-]+) dxinf=([\de.+-]+)", line)
        if m:
            rows.append((int(m[2]), float(m[3]), float(m[5])))
        elif line.startswith("SUMMARY"):
            n = int(re.search(r" n=(\d+)", line)[1])
            size = int(re.search(r"size=(\d+)", line)[1]) if "size=None" not in line else None
            tot = int(re.search(r"total_boxes=(\d+)", line)[1])
            yield line.split()[1], n, rows, size, tot
            rows = []


def part4():
    print("== 4. numbers from the logs (s_i = 2^{1-i})")
    for fn in ("oracle_eps1e-6.log", "scaling_eps1e-4.log", "random_n8_eps1e-4.log", "random_n16_eps1e-4.log"):
        for tag, n, rows, size, tot in blocks(fn):
            if tag.startswith("zero"):
                continue
            per = [(i, lm / n) for i, lm, _ in rows]
            imax, vmax = max(per, key=lambda t: t[1])
            loc = [(i, dx / 2.0 ** (1 - i)) for i, _, dx in rows]
            l4 = [v for i, v in loc if i == 4][0]
            l5on = [v for i, v in loc if i >= 5]
            l6on = [v for i, v in loc if i >= 6]
            print("   %-22s %-13s n=%2d: max split/n %.2f (level %d); dxinf/s at level 4 = %.2f, "
                  "levels>=5 %.2f-%.2f, levels>=6 %.2f-%.2f, max overall %.2f; processed/size %s" % (
                      fn, tag, n, vmax, imax, l4, min(l5on), max(l5on), min(l6on), max(l6on),
                      max(v for _, v in loc), "%.2f" % (tot / size) if size else "-"))
    print("   RC n = 8 (rc_zero_eps1e-6_tol.log):")
    seen = False
    for line in open(os.path.join(LOGS, "rc_zero_eps1e-6_tol.log")):
        if "rc n=4" in line:
            seen = True
            continue
        m = re.match(r"j=\s*(\d+) .*UBD=\s*([\de.+-]+) cen_inf/h=\s*([\d.]+).*gap=([\de.+-]+)", line)
        if seen and m:
            print("     j=%2s UBD=%s cen/h=%s gap=%s" % (m[1], m[2], m[3], m[4]))


def part5():
    print("== 5. RC round-1 partitions under 1e-9 centre moves (n = 16, seed 0)")
    sys.path.insert(0, os.path.join(TD, "adaptive"))
    from ls_lib import dp, slopes
    from rc_lib import shell_partition
    n = 16
    c = np.random.default_rng(0).uniform(-0.2, 0.2, n)
    R0 = dp(shell_partition(n, np.zeros(n), 2.0, 4), slopes(np.zeros(n), 0.8, 0.1, c), 0.8, 0.1, c)
    x1 = R0["x"]
    print("   base: leaves, cells = %s" % (shell_partition(n, x1, 1.0, 4).size(),))
    for i in range(n):
        xp = x1.copy()
        xp[i] -= 1e-9 * np.sign(xp[i])
        Q = shell_partition(n, xp, 1.0, 4)
        mw = min(min((L["u1"] - L["l1"]).min(), (L["u2"] - L["l2"]).min()) for L in Q.leaves if L is not None)
        print("   x1_%-2d = % .4f: leaves, cells = %s, smallest leaf width %.1e" % (i, x1[i], Q.size(), mw))


if __name__ == "__main__":
    part1()
    part2()
    part3()
    part4()
    part5()
