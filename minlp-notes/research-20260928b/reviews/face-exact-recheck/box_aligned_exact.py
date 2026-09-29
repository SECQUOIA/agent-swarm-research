"""Recheck of Example 3.12(b): f = (x-a)^2 + (x-a)(y-z) + (y-z)^2 on [0,1]^3, termwise McCormick on
xy and -xz; claim N_cov(eps) >= 1/(2 sqrt(eps)) for eps <= min(a, 1-a)^2.  Exact rational arithmetic.

[1] identity f = (X + D/2)^2 + 3 D^2 / 4 (X = x-a, D = y-z) and f = X^2 on the plane y = z;
[2] Lemma 2.1(a) gap formula vs the exact convex envelope of x*y on a rectangle (4-vertex LP);
[3] step 3 of the proof: at the centre of C' ∩ R' the termwise gap is >= w'_x w'_y / 2, on random
    rational boxes (including boxes whose y- and z-ranges overlap only partly);
[4] the K = 2 variant: f >= X^2 + |D| on random points, and a midpoint-convexity violation;
[5] arithmetic of the final count h/(h^2 + eps) at h = sqrt(eps).
"""
from fractions import Fraction as Fr
import itertools
import random

rng = random.Random(3129)


def rf(den=60):
    return Fr(rng.randint(0, den), den)


def mc_gap(c, xi, xj, li, ui, lj, uj):
    """Lemma 2.1(a): gap of the McCormick envelope of c*xi*xj on [li,ui]x[lj,uj]."""
    dim, dip, djm, djp = xi - li, ui - xi, xj - lj, uj - xj
    if c > 0:
        return c * min(dim * djm, dip * djp)
    return -c * min(dim * djp, dip * djm)


def vex_bilinear(c, x, y, lx, ux, ly, uy):
    """Exact convex envelope of c*x*y at (x, y): min over convex combinations of the 4 vertices.
    Extreme points of {lambda >= 0 : sum = 1, sum lambda v = (x, y)} use at most 3 vertices."""
    V = [(lx, ly), (lx, uy), (ux, ly), (ux, uy)]
    best = None
    for S in itertools.combinations(range(4), 3):
        # solve lambda for 3 vertices: rows (1,1,1), (vx), (vy)
        A = [[Fr(1)] * 3, [V[i][0] for i in S], [V[i][1] for i in S]]
        rhs = [Fr(1), x, y]
        # Cramer's rule
        def det3(M):
            return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
                    - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                    + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
        d = det3(A)
        if d == 0:
            continue
        lam = []
        for k in range(3):
            M = [row[:] for row in A]
            for r in range(3):
                M[r][k] = rhs[r]
            lam.append(det3(M) / d)
        if min(lam) < 0:
            continue
        val = sum(lam[k] * c * V[S[k]][0] * V[S[k]][1] for k in range(3))
        best = val if best is None else min(best, val)
    return best


def f_val(x, y, z, a, K=None):
    X, D = x - a, y - z
    if K is None:
        return X * X + X * D + D * D
    return X * X + X * D + K * abs(D)


print("[1] identity and optimal set")
bad = 0
for _ in range(2000):
    a, x, y, z = rf(), rf(), rf(), rf()
    X, D = x - a, y - z
    bad += f_val(x, y, z, a) != (X + D / 2) ** 2 + Fr(3, 4) * D * D
    bad += f_val(x, y, y, a) != X * X
print(f"    2000 random rational points: identity/plane mismatches = {bad}")
print("    f = (X+D/2)^2 + 3D^2/4 >= 0 with equality iff X = D = 0, so argmin = {x = a, y = z}")

print("[2] Lemma 2.1(a) formula vs exact envelope of c*x*y on random rational rectangles")
bad = 0
for _ in range(1500):
    lx, ux = sorted([rf(), rf()]); ly, uy = sorted([rf(), rf()])
    if lx == ux or ly == uy:
        continue
    x = lx + (ux - lx) * rf(); y = ly + (uy - ly) * rf()
    for c in (Fr(1), Fr(-1), Fr(5, 2)):
        gap = c * x * y - vex_bilinear(c, x, y, lx, ux, ly, uy)
        bad += gap != mc_gap(c, x, y, lx, ux, ly, uy)
print(f"    mismatches = {bad}")

print("[3] proof step 3: gap at the centre of C' ∩ R' vs w'_x w'_y / 2")
minratio, n_used, bad = None, 0, 0
for trial in range(20000):
    a = Fr(rng.randint(1, 59), 60)
    h = min(a, 1 - a) * rf()
    if h == 0:
        continue
    lx, ux = sorted([rf(), rf()]); ly, uy = sorted([rf(), rf()]); lz, uz = sorted([rf(), rf()])
    if trial % 2 == 0:           # make the y- and z-ranges overlap more often
        lz, uz = sorted([ly + (uy - ly) * rf(), rf()])
    if lx == ux or ly == uy or lz == uz:
        continue
    xl, xu = max(lx, a - h), min(ux, a + h)
    yl, yu = max(ly, lz), min(uy, uz)
    if xl >= xu or yl >= yu:
        continue                 # C' ∩ R' has zero area: nothing to check
    wx, wy = xu - xl, yu - yl
    xc, yc = (xl + xu) / 2, (yl + yu) / 2
    gap = mc_gap(Fr(1), xc, yc, lx, ux, ly, uy) + mc_gap(Fr(-1), xc, yc, lx, ux, lz, uz)
    r = gap / (wx * wy / 2)
    n_used += 1
    bad += r < 1
    minratio = r if minratio is None else min(minratio, r)
print(f"    {n_used} boxes with C' ∩ R' of positive area: violations {bad}, min ratio {float(minratio):.4f}")

print("[4] K = 2 variant f = X^2 + XD + 2|D|")
bad = 0
for _ in range(5000):
    a, x, y, z = Fr(rng.randint(1, 59), 60), rf(), rf(), rf()
    X, D = x - a, y - z
    bad += f_val(x, y, z, a, 2) < X * X + abs(D)
print(f"    f >= X^2 + |D| violations on 5000 points: {bad}  (uses |X| <= 1)")
a = Fr(1, 3)
# along (dX, dD) = (1, -2) the quadratic part X^2 + XD is concave (-t^2); both points have D > 0
p = (a + Fr(1, 10), Fr(65, 100), Fr(35, 100))     # X = 0.1, D = 0.3
q = (a - Fr(1, 10), Fr(85, 100), Fr(15, 100))     # X = -0.1, D = 0.7
mid = tuple((u + v) / 2 for u, v in zip(p, q))
lhs, rhs = f_val(*mid, a, 2), (f_val(*p, a, 2) + f_val(*q, a, 2)) / 2
print(f"    f(mid) = {lhs} vs average of endpoints {rhs}: nonconvex = {lhs > rhs}")

print("[5] count: area(R') / max area(C' ∩ R') = 2h / (2(h^2+eps)); at h = sqrt(eps) -> 1/(2 sqrt eps)")
for e in (1e-2, 1e-4, 1e-6):
    h = e ** 0.5
    print(f"    eps={e:g}: h/(h^2+eps) = {h / (h * h + e):.2f}, 1/(2 sqrt eps) = {1 / (2 * e ** 0.5):.2f}")
