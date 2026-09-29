"""Lemma 3 on random lattices, compared with an independent closest-point enumeration.

For a basis C (columns c_j), target t != 0 and h^2 >= |t|^2/8, the lemma says that the violated
splits of X = Gram(b0, b_1..b_k)/|b0|^2 are exactly (-1, z) and (0, -z) for the z with
|t - Cz| < |t|. Closer points are enumerated here from the least-squares centre z* with
|t - Cz|^2 = (z - z*)^T H (z - z*) + |t - Cz*|^2, H = C^T C; this does not use Lemma 1 or 3.
"""
import random
import sys
from fractions import Fraction as F

from tools import fp_enum, violators_fp, inverse, is_pd

random.seed(11)


def lemma3_X(C, t, h2):
    k = len(C)
    t2 = sum(x * x for x in t)
    N = k + 1
    G = [[F(0)] * N for _ in range(N)]
    G[0][0] = 4 * t2 + 4 * F(h2)
    for j in range(k):
        G[0][1 + j] = G[1 + j][0] = 2 * sum(a * b for a, b in zip(t, C[j]))
        for l in range(k):
            G[1 + j][1 + l] = F(sum(a * b for a, b in zip(C[j], C[l])))
    return [[x / G[0][0] for x in row] for row in G]


def closer_points(C, t):
    k = len(C)
    H = [[F(sum(a * b for a, b in zip(C[i], C[j]))) for j in range(k)] for i in range(k)]
    Hi = inverse(H)
    Ct = [sum(a * b for a, b in zip(C[i], t)) for i in range(k)]
    zs = [sum(Hi[i][j] * Ct[j] for j in range(k)) for i in range(k)]
    proj = [sum(zs[j] * C[j][r] for j in range(k)) for r in range(len(t))]
    res2 = sum((a - b) ** 2 for a, b in zip(t, proj))
    t2 = sum(x * x for x in t)
    if res2 >= t2:
        return set()
    return set(fp_enum(H, t2 - res2, parity=False, center=zs))


def random_instance():
    d = random.randint(1, 4)
    k = random.randint(1, d)
    while True:
        C = [[random.randint(-3, 3) for _ in range(d)] for _ in range(k)]
        H = [[F(sum(a * b for a, b in zip(C[i], C[j]))) for j in range(k)] for i in range(k)]
        if is_pd(H):
            break
    while True:
        t = [F(random.randint(-6, 6), random.randint(1, 4)) for _ in range(d)]
        if any(t):
            return C, t


def main():
    fails = 0
    yes = 0
    trials = 1500
    for _ in range(trials):
        C, t = random_instance()
        t2 = sum(x * x for x in t)
        pts = closer_points(C, t)
        # sanity: every enumerated point really is strictly closer
        for z in pts:
            l = [sum(z[j] * C[j][r] for j in range(len(C))) for r in range(len(t))]
            assert sum((a - b) ** 2 for a, b in zip(t, l)) < t2
        pred = {(-1,) + z for z in pts} | {(0,) + tuple(-x for x in z) for z in pts}
        yes += bool(pts)
        for h2 in (t2 / 8, t2 / 8 + F(1, 7), 5 * t2):
            X = lemma3_X(C, t, h2)
            if not (X[0][0] == 1 and is_pd(X)):
                fails += 1
                continue
            fails += violators_fp(X, zero_first=True) != pred
    print(f"[Lemma 3, random lattices d<=4, k<=d, rational t != 0, h^2 in {{|t|^2/8, |t|^2/8+1/7, 5|t|^2}}] "
          f"{trials} instances ({yes} with a strictly closer point) x 3 values of h: {fails} failures")

    # below the threshold: extra violators must have |u0| >= 3 (v0 not in {0,-1})
    extra_inst = bad_extra = 0
    for _ in range(1500):
        C, t = random_instance()
        t2 = sum(x * x for x in t)
        pts = closer_points(C, t)
        pred = {(-1,) + z for z in pts} | {(0,) + tuple(-x for x in z) for z in pts}
        X = lemma3_X(C, t, t2 / 80)
        viol = violators_fp(X, zero_first=True)
        if viol != pred:
            extra_inst += 1
            bad_extra += any(v[0] in (0, -1) for v in viol - pred) or not pred <= viol
    print(f"[Lemma 3 below threshold, h^2 = |t|^2/80] {extra_inst} of 1500 instances have extra violators; "
          f"{bad_extra} of them have an extra violator with v0 in {{0,-1}} or lose a predicted one")
    fails += bad_extra

    # the note's sharpness example: L = Z, t = 1/3
    at = violators_fp(lemma3_X([[1]], [F(1, 3)], F(1, 72)), zero_first=True)
    below = violators_fp(lemma3_X([[1]], [F(1, 3)], F(1, 81)), zero_first=True)
    ok = at == set() and below == {(1, -1), (-2, 1)} and closer_points([[1]], [F(1, 3)]) == set()
    print(f"[sharpness example L=Z, t=1/3] h^2=1/72: {sorted(at)}; h^2=1/81: {sorted(below)} -> {'OK' if ok else 'FAIL'}")
    fails += not ok
    print("ALL OK" if fails == 0 else f"FAILURES: {fails}")
    return fails


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
