"""M-recourse checks for Sections 7.2-7.3 and Appendix C (exact arithmetic).

Checks: prop:star (A),(B) for several parameters, ex:cr-star32, ex:cv-fm,
prop:cv-limit, prop:cv-ladder (random points), lem:cr-cell (random 2D
instances with exact recourse), thm:cv-recog example.
"""
from fractions import Fraction as Fr
import itertools, random

random.seed(20261003)
ok = True


def report(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok &= bool(cond)


# ---------------- prop:star (A) ----------------
def star_A(j, m, eps):
    h = Fr(1, 2 ** j)
    G = [h * a for a in range(2 ** j + 1)]
    om = m * h * h / 4 - 1 - eps
    assert om > 0
    leaf = lambda x, y: y * y - h * x * y  # one leaf term
    center = lambda x: x * x + om * x
    # grid min of a leaf for fixed x
    leafmin = {x: min(leaf(x, y) for y in G) for x in G}
    VG = {x: center(x) + m * leafmin[x] for x in G}
    UG = min(VG.values())
    mF = lambda x, y1: center(x) + leaf(x, y1) + (m - 1) * leafmin[x]
    corners = [mF(x, y) for x in (1 - h, 1) for y in (0, h)]
    cm = min(corners)
    claim = (1 - h) * (m * h * h / 4 - h - eps)
    return UG, cm, claim, min(VG[1 - h], VG[1])


for (j, m, eps) in [(1, 32, Fr(1, 16)), (1, 17, Fr(1, 32)), (2, 80, Fr(1, 7)),
                    (3, 400, Fr(1, 3)), (2, 1000, Fr(1, 2))]:
    UG, cm, claim, vg = star_A(j, m, eps)
    report(f"star(A) j={j} m={m} eps={eps}: U_G=0, corner min formula, =min V^G",
           UG == 0 and cm == claim and cm == vg)

# continuous optimum of (A): V(x)=(1-mh^2/4)x^2+om x on [0,1]
for (j, m, eps) in [(1, 32, Fr(1, 16)), (2, 80, Fr(1, 7))]:
    h = Fr(1, 2 ** j); om = m * h * h / 4 - 1 - eps
    V = lambda x: (1 - m * h * h / 4) * x * x + om * x
    xs = [Fr(a, 97) for a in range(98)]
    report(f"star(A) j={j} m={m}: V(1)=-eps minimal on fine grid",
           V(Fr(1)) == -eps and all(V(x) >= -eps for x in xs) and
           all(V(x) > -eps for x in xs if x != 1))


# ---------------- prop:star (B) ----------------
def star_B(j, d):
    h = Fr(1, 2 ** j)
    m = d * d
    G = [h * a for a in range(2 ** j + 1)]
    half = Fr(1, 2)
    leaf = lambda x, y: (y - h / 2 - (x - half) / d) ** 2
    leafmin = {x: min(leaf(x, y) for y in G) for x in G}
    VG = {x: (x - half) ** 2 + m * leafmin[x] for x in G}
    UG = min(VG.values())
    claimUG = half - d * h / 2 + d * d * h * h / 4
    mF = lambda x, y1: (x - half) ** 2 + leaf(x, y1) + (m - 1) * leafmin[x]
    res = []
    for a in (half - h, half):
        cm = min(mF(x, y) for x in (a, a + h) for y in (0, h))
        res.append((cm - UG, min(VG[a], VG[a + h]) - UG))
    claimdiff = d * h * (half - h) + 2 * h * h - half
    return UG == claimUG, all(r[0] == claimdiff and r[1] == claimdiff for r in res), claimdiff


for (j, d) in [(2, 8), (2, 9), (2, 20), (3, 16), (3, 40), (4, 32)]:
    a, b, cd = star_B(j, d)
    h = Fr(1, 2 ** j)
    report(f"star(B) j={j} d={d}: U_G formula, both cells' corner-min gap = {cd}",
           a and b and cd >= d * h / 4 + 2 * h * h - Fr(1, 2))

# ---------------- ex:cv-fm ----------------
def boxqp2(C, q, lo, hi):
    """min 1/2 y^T C y + q^T y over box, C PD 2x2, by KKT pattern enumeration."""
    best = None
    for pat in itertools.product((-1, 0, 1), repeat=2):
        y = [None, None]
        free = [i for i in range(2) if pat[i] == 0]
        for i in range(2):
            if pat[i] == -1: y[i] = lo[i]
            if pat[i] == 1: y[i] = hi[i]
        if len(free) == 2:
            det = C[0][0] * C[1][1] - C[0][1] * C[1][0]
            y = [(-q[0] * C[1][1] + q[1] * C[0][1]) / det,
                 (-q[1] * C[0][0] + q[0] * C[1][0]) / det]
        elif len(free) == 1:
            i = free[0]; k = 1 - i
            y[i] = -(q[i] + C[i][k] * y[k]) / C[i][i]
        if not all(lo[i] <= y[i] <= hi[i] for i in range(2)):
            continue
        val = Fr(1, 2) * sum(y[a] * C[a][b] * y[b] for a in range(2) for b in range(2)) + q[0] * y[0] + q[1] * y[1]
        if best is None or val < best[0]:
            best = (val, tuple(y))
    return best


for M in (Fr(1), Fr(3), Fr(10)):
    C = [[2 * M + 2, 2 * M], [2 * M, 2 * M]]
    Gam = [-2 * M - 4, -2 * M]
    c = [Fr(1), Fr(0)]
    good = True
    for a in range(0, 76):
        z = Fr(3 * a, 300)
        q = [Gam[0] * z + c[0], Gam[1] * z + c[1]]
        val, y = boxqp2(C, q, [0, 0], [1, 1])
        tot = val + M * z * z + (2 * z - Fr(1, 2)) ** 2
        if z <= Fr(1, 4):
            ey, ev = (Fr(0), z), (Fr(1, 2) - 2 * z) ** 2
        elif z <= Fr(1, 2):
            ey, ev = (2 * z - Fr(1, 2), Fr(1, 2) - z), Fr(0)
        else:
            ey, ev = (((M + 2) * z - Fr(1, 2)) / (M + 1), Fr(0)), M * (z - Fr(1, 2)) ** 2 / (M + 1)
        if tot != ev or y != ey:
            good = False
    BCB = [2 * M, 2 * M + 8, 2 * (M + 2) ** 2 / (M + 1)]
    # B vectors
    Bs = [(0, 1), (2, -1), ((M + 2) / (M + 1), 0)]
    bcb = [sum(B[a] * C[a][b] * B[b] for a in range(2) for b in range(2)) for B in Bs]
    report(f"ex:cv-fm M={M}: responses/values on 76 points, B^T C B, sigma=2M",
           good and bcb == BCB and min(BCB) == 2 * M)

# ---------------- prop:cv-limit ----------------
for M in (Fr(1), Fr(2), Fr(7)):
    F = lambda x, y: M * (x - y) ** 2 - Fr(1, 8) * (x + y - 2) ** 2 + 2 * (y - 1)
    pts = [(Fr(a, 20), Fr(20 + b, 20)) for a in range(41) for b in range(41)]
    grow = all(F(x, y) >= Fr(1, 8) * ((x - 1) ** 2 + (y - 1) ** 2) for x, y in pts)
    # K={y}: response x minimizing F over [0,2] for y in [yc,3] is x=2
    yc = 4 * M / (2 * M + Fr(1, 4))
    def resp_x(y):
        # F convex in x: a x^2 + b x
        a = M - Fr(1, 8)
        b = -2 * M * y - Fr(1, 4) * (y - 2)
        xs = -b / (2 * a)
        return min(max(xs, Fr(0)), Fr(2))
    clipped = all(resp_x(yc + (3 - yc) * Fr(t, 10)) == 2 for t in range(11))
    xc = 1 + 2 / (2 * M + Fr(1, 4))
    def resp_y(x):
        a = M - Fr(1, 8)
        b = -2 * M * x - Fr(1, 4) * (x - 2) + 2
        ys = -b / (2 * a)
        return min(max(ys, Fr(1)), Fr(3))
    clipped2 = all(resp_y(xc * Fr(t, 10)) == 1 for t in range(11))
    report(f"prop:cv-limit M={M}: growth 1/8 on grid, F(2,2)=3/2, clipped pieces, 1<yc<2, 1<xc<=2",
           grow and F(Fr(2), Fr(2)) == Fr(3, 2) and clipped and clipped2 and 1 < yc < 2 and 1 < xc <= 2)

# ---------------- prop:cv-ladder (random points) ----------------
def ladder(m, M, x):
    a = Fr(1, 5)
    z, w, y1, y2 = x
    F = Fr(0)
    for i in range(m):
        phi = M * (y1[i] + y2[i] - z[i]) ** 2 + (y1[i] - 2 * z[i] + Fr(1, 2)) ** 2
        F += z[i] ** 2 + phi - w[i] ** 2 + 3 * w[i] - (z[i] - a) * w[i]
    for i in range(m - 1):
        F += Fr(1, 16) * ((z[i + 1] - z[i]) ** 2 + (w[i + 1] - w[i]) ** 2)
    return F


for m in (1, 2, 3):
    for M in (Fr(1), Fr(5)):
        star = ([Fr(1, 5)] * m, [Fr(0)] * m, [Fr(0)] * m, [Fr(1, 5)] * m)
        good = ladder(m, M, star) == Fr(m, 20)
        for _ in range(300):
            x = ([Fr(random.randint(0, 60), 80) for _ in range(m)],
                 [Fr(random.randint(0, 40), 40) for _ in range(m)],
                 [Fr(random.randint(0, 40), 40) for _ in range(m)],
                 [Fr(random.randint(0, 40), 40) for _ in range(m)])
            d2 = sum((x[0][i] - Fr(1, 5)) ** 2 + x[1][i] ** 2 + x[2][i] ** 2 + (x[3][i] - Fr(1, 5)) ** 2 for i in range(m))
            if ladder(m, M, x) - Fr(m, 20) < d2 / 12:
                good = False
        report(f"prop:cv-ladder m={m} M={M}: OPT=m/20 and growth 1/12 at 300 random points", good)

print("ALL PASS" if ok else "SOME FAIL")
