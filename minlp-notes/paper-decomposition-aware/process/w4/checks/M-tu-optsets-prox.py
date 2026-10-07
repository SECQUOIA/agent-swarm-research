"""Exact test of lem:proximal(ii) value bound and (i) node bound on random 2-D box QPs.

For a continuous box QP in 2-D, OPT and the (finite) optimal set are computed
exactly from the KKT candidates (vertices, edge minimizers, interior stationary
point); degenerate instances (continuum optimal sets) are skipped. A proximal
stage (Algorithm alg:prox) is run from random centers c with
dist(c,S)^2 <= 4 kappa_hat n h^2, and F(y+) - OPT <= (99/256) L n h^2 is checked.
"""
from fractions import Fraction as Fr
import random, math

random.seed(11)

def graded(lo, hi, c, h, th):
    nodes = {c}
    for sgn, R in ((1, hi - c), (-1, c - lo)):
        t = Fr(0)
        while t < R:
            t = min(t + h + th * t, R)
            nodes.add(c + sgn * t)
    return sorted(nodes)

def widths(G):
    w = {}
    for k, v in enumerate(G):
        cand = []
        if k > 0: cand.append(v - G[k - 1])
        if k + 1 < len(G): cand.append(G[k + 1] - v)
        w[v] = max(cand) if cand else Fr(0)
    return w

def isqrt_ceil(a):
    r = math.isqrt(a)
    return r if r * r == a else r + 1

ok = True
tests = 0
worst = 0.0
for trial in range(400):
    H = [[Fr(random.randint(-6, 6), 2), None], [None, Fr(random.randint(-6, 6), 2)]]
    H[0][1] = H[1][0] = Fr(random.randint(-6, 6), 2)
    b = [Fr(random.randint(-8, 8), 4), Fr(random.randint(-8, 8), 4)]
    lo = [Fr(0), Fr(0)]
    hi = [Fr(random.randint(1, 3)), Fr(random.randint(1, 3))]
    F = lambda x: Fr(1, 2) * (H[0][0] * x[0] ** 2 + 2 * H[0][1] * x[0] * x[1] + H[1][1] * x[1] ** 2) + b[0] * x[0] + b[1] * x[1]
    cands = []
    degenerate = False
    for x0 in (lo[0], hi[0]):
        for x1 in (lo[1], hi[1]):
            cands.append((x0, x1))
    # edges: fix one coordinate, minimize in the other
    for fix in (0, 1):
        oth = 1 - fix
        for v in (lo[fix], hi[fix]):
            a = H[oth][oth]
            slope0 = H[oth][fix] * v + b[oth]
            if a == 0:
                if slope0 == 0:
                    degenerate = True
                continue
            t = -slope0 / a
            if lo[oth] < t < hi[oth]:
                x = [None, None]; x[fix] = v; x[oth] = t
                cands.append(tuple(x))
    det = H[0][0] * H[1][1] - H[0][1] ** 2
    if det == 0:
        degenerate = True
    else:
        x0 = (-b[0] * H[1][1] + b[1] * H[0][1]) / det
        x1 = (-b[1] * H[0][0] + b[0] * H[0][1]) / det
        if lo[0] < x0 < hi[0] and lo[1] < x1 < hi[1]:
            cands.append((x0, x1))
    if degenerate:
        continue
    OPT = min(F(x) for x in cands)
    S = [x for x in cands if F(x) == OPT]
    L = max(H[0][0], H[1][1], Fr(0))
    if L == 0:
        continue
    n = 2
    s = max(hi)
    for kh in (1, 2, 4, 8, 32):
        mu = 2
        while Fr(kh, 4 ** mu) > Fr(1, 8):
            mu += 1
        th = Fr(1, 2 ** mu)
        eta = L * th * th / 4
        rho = 2 * isqrt_ceil(kh * n)
        Ktheta = 8 * 2 ** mu * math.ceil(math.log2(n + 2))
        for j in range(0, 7):
            h = s / 2 ** j
            # random center near S
            sstar = random.choice(S)
            for _ in range(3):
                rad = Fr(random.randint(0, 100), 100) * 2 * Fr(math.isqrt(kh * n * 10 ** 6), 1000) * h
                ang = random.random() * 2 * math.pi
                c = [sstar[0] + rad * Fr(math.cos(ang)).limit_denominator(1000),
                     sstar[1] + rad * Fr(math.sin(ang)).limit_denominator(1000)]
                c = [min(max(c[i], lo[i]), hi[i]) for i in range(2)]
                d2 = min((c[0] - p[0]) ** 2 + (c[1] - p[1]) ** 2 for p in S)
                if d2 > 4 * kh * n * h * h:
                    continue
                grids, ws = [], []
                for i in range(2):
                    G = graded(max(lo[i], c[i] - rho * h), min(hi[i], c[i] + rho * h), c[i], h, th)
                    if len(G) > Ktheta:
                        print("FAIL node bound", len(G), Ktheta); ok = False
                    grids.append(G); ws.append(widths(G))
                best, yb = None, None
                for x in grids[0]:
                    for y in grids[1]:
                        qv = F((x, y)) - (max(H[0][0], 0) * ws[0][x] ** 2 + max(H[1][1], 0) * ws[1][y] ** 2) / 8 + eta * ((x - c[0]) ** 2 + (y - c[1]) ** 2)
                        if best is None or qv < best:
                            best, yb = qv, (x, y)
                gap = F(yb) - OPT
                bound = Fr(99, 256) * L * n * h * h
                tests += 1
                worst = max(worst, float(gap / bound))
                if gap > bound:
                    print("FAIL prox bound", H, b, hi, kh, j, c, gap, bound); ok = False
print("tests %d, max (F(y+)-OPT)/bound = %.4f" % (tests, worst))
print("ALL PASS" if ok else "SOME FAIL")
