"""R9 referee spot checks (exact arithmetic, short).

1. Graded-grid example after Prop. tu-misaligned (constraints.tex): h=1/16,
   theta=1/4, centers 3/10 and 7/10 on [0,1]; claims: eleven nodes each,
   only 0 and 1 in common, (tu-gap) holds with m=1/2 for d=L w^2/8.
2. Prop. sharp (growth-sharp.tex): m_i(a) <= U (U >= 0) for |a| <= h sqrt((n-2)kappa/16)
   on uniform grids h*Z cap [-1,1], exact min-marginals (pairwise separable F).
3. Lemma graded (b): per-side node count <= ceil((4/theta) ln(1+theta R/H)).
4. Example cr-star32 numbers (recourse-local.tex).
5. Example tu-sum corrected values (constraints.tex).
"""
from fractions import Fraction as Fr
import math, itertools, random


def graded_side(c, end, h, theta, integer=False):
    """Nodes strictly beyond c towards end (end > c) of Definition graded."""
    t, out, R = Fr(0), [], end - c
    while t < R:
        s = h + theta * t
        if integer:
            s = max(1, math.floor(s))
        t = min(t + s, R)
        out.append(c + t)
    return out


def graded_grid(lo, hi, c, h, theta, integer=False):
    right = graded_side(c, hi, h, theta, integer) if hi > c else []
    left = [-v for v in graded_side(-c, -lo, h, theta, integer)] if lo < c else []
    return sorted(set([c] + right + left))


def widths(G):
    w = {}
    for a, b in zip(G, G[1:]):
        w[a] = max(w.get(a, 0), b - a)
        w[b] = max(w.get(b, 0), b - a)
    return w


# 1 -----------------------------------------------------------------------
h, th = Fr(1, 16), Fr(1, 4)
G1 = graded_grid(Fr(0), Fr(1), Fr(3, 10), h, th)
G2 = graded_grid(Fr(0), Fr(1), Fr(7, 10), h, th)
common = sorted(set(G1) & set(G2))
w1, w2 = widths(G1), widths(G2)
m = Fr(1, 2)
gap_ok = all((nu - m) ** 2 > Fr(1, 8) * w1[nu] ** 2 + Fr(1, 8) * w2[nu] ** 2 for nu in common)  # L=1 scale
print("[1] |G1|,|G2| =", len(G1), len(G2), " common =", common, " tu-gap holds:", gap_ok)

# 2 -----------------------------------------------------------------------
def sharp_check(mm, Lam, sig, hh):
    n = 2 * mm
    kappa = Fr(2) * Lam / (Lam - sig)
    N = int(1 / hh)
    G = [k * hh for k in range(-N, N + 1)]
    d = {v: Lam / 8 * hh ** 2 for v in G}  # uniform grid: every node has width h
    # pair minimum of Lam/2(u^2+v^2)+sig*u*v - d(u) - d(v)
    def pair(u, v):
        return Lam / 2 * (u * u + v * v) + sig * u * v - d[u] - d[v]
    pmin = min(pair(u, v) for u in G for v in G)
    rad2 = hh ** 2 * (n - 2) * kappa / 16
    worst = None
    for a in G:
        if a * a > rad2:
            continue
        mi = min(pair(a, v) for v in G) + (mm - 1) * pmin
        if mi > 0:
            return False, a, mi
        worst = mi if worst is None else max(worst, mi)
    return True, rad2, worst

for (mm, Lam, sig, hh) in [(3, Fr(2), Fr(1), Fr(1, 8)), (4, Fr(2), Fr(3, 2), Fr(1, 16)),
                           (6, Fr(1), Fr(9, 10), Fr(1, 16)), (2, Fr(3), Fr(0), Fr(1, 4))]:
    print("[2] m=%d Lam=%s sig=%s h=%s ->" % (mm, Lam, sig, hh), sharp_check(mm, Lam, sig, hh)[0])

# 3 -----------------------------------------------------------------------
random.seed(9)
bad = 0
for _ in range(3000):
    theta = Fr(1, 2 ** random.randint(2, 6))
    integer = random.random() < 0.4
    if integer:
        hm = Fr(random.randint(1, 40), random.choice([1, 2, 4, 8]))
        R = random.randint(1, 3000)
        H = max(hm, 1)
    else:
        hm = Fr(1, 2 ** random.randint(0, 12))
        R = Fr(random.randint(1, 4000), random.randint(1, 50))
        H = hm
    cnt = len(graded_side(Fr(0), Fr(R), hm, theta, integer))
    bound = math.ceil(4 / float(theta) * math.log(1 + float(theta * R / H)))
    if cnt > bound:
        bad += 1
print("[3] graded side-count violations:", bad, "of 3000")

# 4 -----------------------------------------------------------------------
mm, hh, eps = 32, Fr(1, 2), Fr(1, 16)
beta = mm * hh ** 2 / 4 - 1 - eps
G = [Fr(0), Fr(1, 2), Fr(1)]
def leaf_min(x):
    return min(y * y - hh * x * y for y in G)
Vh = {x: x * x + beta * x + mm * leaf_min(x) for x in G}
corners = sorted([x * x + beta * x + (y * y - hh * x * y) + (mm - 1) * leaf_min(x)
                  for x in (Fr(1, 2), Fr(1)) for y in (Fr(0), Fr(1, 2))])
print("[4] beta =", beta, " V_h =", [Vh[x] for x in G], " corners =", corners,
      " bag budget", 2 * 2 * hh ** 2 / 8, " global", (1 + mm) * 2 * hh ** 2 / 8)

# 5 -----------------------------------------------------------------------
Gs = [Fr(0), Fr(1), Fr(9, 4), Fr(3)]
ws = widths(Gs)
dd = {v: Fr(1, 8) * ws[v] ** 2 for v in Gs}  # L = 1
xs = (Fr(1), Fr(1), Fr(2))
vals = sorted(set(
    (Fr(1, 2) * sum((a - b) ** 2 for a, b in zip((x1, x2, x3), xs)) - dd[x1] - dd[x2] - dd[x3])
    for x1 in Gs for x2 in Gs for x3 in Gs if x1 + x2 == x3))
print("[5] tu-sum corrected values (times 1/L):", vals)
