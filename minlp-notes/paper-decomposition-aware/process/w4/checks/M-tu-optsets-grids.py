"""Exact checks for Sections 8.7 and 9.1 (reviewer M-tu-optsets).

1. Graded grids of Definition def:graded (continuous coordinates).
2. prop:tu-misaligned: simple instance and graded instance (App. tu-limits).
3. ex:tu-sum: grid, corrections, feasible points, values.
4. prop:twocenters: bound (9.1) by brute force over many (M, theta, h, c_x, G_z).
"""
from fractions import Fraction as Fr
import itertools, random, math

def graded(lo, hi, c, h, th):
    nodes = {c}
    t = Fr(0)
    R = hi - c
    while t < R:
        t = min(t + h + th * t, R)
        nodes.add(c + t)
    t = Fr(0)
    R = c - lo
    while t < R:
        t = min(t + h + th * t, R)
        nodes.add(c - t)
    return sorted(nodes)

def widths(G):
    w = {}
    for k, v in enumerate(G):
        cand = []
        if k > 0:
            cand.append(v - G[k - 1])
        if k + 1 < len(G):
            cand.append(G[k + 1] - v)
        w[v] = max(cand) if cand else Fr(0)
    return w

ok = True
def check(cond, msg):
    global ok
    print(("PASS " if cond else "FAIL ") + msg)
    ok = ok and cond

# ---- 2. misaligned graded instance
h, th = Fr(1, 16), Fr(1, 4)
G1 = graded(Fr(0), Fr(1), Fr(3, 10), h, th)
G2 = graded(Fr(0), Fr(1), Fr(7, 10), h, th)
printed = [Fr(0), Fr(79, 1280), Fr(51, 320), Fr(19, 80), Fr(3, 10), Fr(29, 80),
           Fr(141, 320), Fr(689, 1280), Fr(3381, 5120), Fr(16649, 20480), Fr(1)]
check(G1 == printed, "graded grid center 3/10 equals printed list")
check(G2 == sorted(1 - v for v in printed), "center 7/10 grid is reflection")
check(len(G1) == 11 and len(G2) == 11, "eleven nodes each")
check(set(G1) & set(G2) == {Fr(0), Fr(1)}, "common nodes {0,1}")
maxint = max(max(b - a for a, b in zip(G, G[1:])) for G in (G1, G2))
check(maxint == Fr(3831, 20480), "largest interval 3831/20480: %s" % maxint)
delta = min(y2 - y1 for y1 in G1 for y2 in G2 if y2 > y1)
check(delta == Fr(27, 1280), "delta = 27/1280: %s" % delta)
L = Fr(1)
w1, w2 = widths(G1), widths(G2)
m = Fr(1, 2)
gap_ok = all(L * (v - m) ** 2 > L / 8 * (w1[v] ** 2 + w2[v] ** 2) for v in (Fr(0), Fr(1)))
check(gap_ok, "(8.5) holds at common nodes with m=1/2")
d1max = max(L / 8 * w1[v] ** 2 for v in G1)
d2max = max(L / 8 * w2[v] ** 2 for v in G2)
lam = (d1max + d2max) / delta * Fr(1001, 1000)
cmin = min(L / 2 * ((y1 - m) ** 2 + (y2 - m) ** 2) + lam * (y2 - y1) - L / 8 * (w1[y1] ** 2 + w2[y2] ** 2)
           for y1 in G1 for y2 in G2 if y1 <= y2)
check(cmin > 0, "graded misaligned: corrected min > 0 just above threshold (%s)" % float(cmin))

# simple instance
G1 = [Fr(0), Fr(1, 2), Fr(1)]
G2 = [Fr(0), Fr(1, 3), Fr(1)]
w1, w2 = widths(G1), widths(G2)
m = Fr(2, 5)
check(all(L * (v - m) ** 2 > L / 8 * (w1[v] ** 2 + w2[v] ** 2) for v in (Fr(0), Fr(1))), "simple: (8.5)")
delta = min(y2 - y1 for y1 in G1 for y2 in G2 if y2 > y1)
thr = (max(L / 8 * w1[v] ** 2 for v in G1) + max(L / 8 * w2[v] ** 2 for v in G2)) / delta
check(delta == Fr(1, 3) and thr == Fr(75, 288), "simple: delta=1/3, threshold 75/288 L")

# ---- 3. ex:tu-sum
G = graded(Fr(0), Fr(3), Fr(0), Fr(1), Fr(1, 4))
check(G == [0, 1, Fr(9, 4), 3], "ex:tu-sum grid %s" % G)
w = widths(G)
d = {v: L / 8 * w[v] ** 2 for v in G}
check(d == {0: Fr(1, 8), 1: Fr(25, 128), Fr(9, 4): Fr(25, 128), 3: Fr(9, 128)}, "ex:tu-sum corrections")
pts = [p for p in itertools.product(G, repeat=3) if p[0] + p[1] == p[2]]
check(len(pts) == 7, "seven feasible grid points")
F = lambda p: L / 2 * ((p[0] - 1) ** 2 + (p[1] - 1) ** 2 + (p[2] - 2) ** 2)
vals = sorted(F(p) - d[p[0]] - d[p[1]] - d[p[2]] for p in pts)
check(vals[0] == Fr(31, 64), "corrected min 31/64 L")
check(min(F(p) for p in pts) - 3 * L * Fr(25, 16) / 8 == Fr(53, 128), "constant allowance 53/128")

# ---- 4. prop:twocenters (9.1), brute force
random.seed(1)
worst = Fr(10 ** 9)
ntests = 0
for _ in range(1500):
    M = Fr(random.randint(1, 40), random.randint(1, 5))
    th = Fr(1, random.choice([4, 5, 8, 16, 32, 64, 128]))
    h = M * Fr(random.randint(1, 1000), 1000)
    cx = M * Fr(random.randint(0, 100), 100)
    Gx = graded(Fr(0), M, cx, h, th)
    if len(Gx) > 3000:
        continue
    Gz = sorted({Fr(0), M} | {M * Fr(random.randint(0, 50), 50) for _ in range(random.randint(0, 3))})
    wx = widths(Gx)
    Lx = random.choice([Fr(2), Fr(2), Fr(3)])
    beta = min(x * x - 2 * x * z + M * z - Lx / 8 * wx[x] ** 2 for x in Gx for z in Gz)
    bound = -max(th ** 2 * M ** 2 / 379, h ** 2 / 20)
    ntests += 1
    if beta > bound:
        print("FAIL twocenters", M, th, h, cx, beta, bound)
        ok = False
    worst = min(worst, bound / beta if beta < 0 else Fr(10 ** 9))
print("twocenters: %d tests, max ratio bound/beta = %s" % (ntests, float(worst)))
print("ALL PASS" if ok else "SOME FAIL")
