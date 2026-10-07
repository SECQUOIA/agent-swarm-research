"""Exact checks for the star counterexamples (cutrecourse cluster).

All arithmetic uses fractions.Fraction.  Star objectives are separable in
the leaves once the centre x is fixed, so a grid min-marginal with x and
y_1 fixed equals the y_1 term plus (m-1) times one leaf minimum.  For small
m this decomposition is also cross-checked by brute force over the full grid.
"""
from fractions import Fraction as Fr
from itertools import product

def grid(h):
    n = int(1 / h)
    return [h * i for i in range(n + 1)]

# ---------- family A: F = x^2 - h x sum y + sum y^2 + (m h^2/4 - 1 - eps) x
def famA_parts(h, m, eps):
    lin = m * h * h / 4 - 1 - eps
    centre = lambda x: x * x + lin * x
    leaf = lambda x, y: y * y - h * x * y
    return centre, leaf

def famA_F(h, m, eps, x, ys):
    c, l = famA_parts(h, m, eps)
    return c(x) + sum(l(x, y) for y in ys)

def famA_minmarg(h, m, eps, x, y1):
    c, l = famA_parts(h, m, eps)
    G = grid(h)
    best = min(l(x, y) for y in G)
    return c(x) + l(x, y1) + (m - 1) * best

def famA_exact(h, m, eps, x):
    # leaf optimum y = h x / 2 lies in [0,1]
    c, l = famA_parts(h, m, eps)
    y = h * x / 2
    return c(x) + m * l(x, y)

def check_famA(h, m, eps, brute=False):
    G = grid(h)
    # grid minimum of F (min over x of conditional grid value)
    c, l = famA_parts(h, m, eps)
    Vh = {x: c(x) + m * min(l(x, y) for y in G) for x in G}
    U = min(Vh.values())
    if brute:
        Ub = min(famA_F(h, m, eps, x, ys) for x in G for ys in product(G, repeat=m))
        assert Ub == U
        for x in G:
            for y1 in G:
                mb = min(famA_F(h, m, eps, x, (y1,) + ys) for ys in product(G, repeat=m - 1))
                assert mb == famA_minmarg(h, m, eps, x, y1)
    # exact optimum: V concave when m h^2 > 4
    V0, V1 = famA_exact(h, m, eps, Fr(0)), famA_exact(h, m, eps, Fr(1))
    assert V0 == 0 and V1 == -eps
    xa, xb = 1 - h, Fr(1)
    corners = [famA_minmarg(h, m, eps, x, y) for x in (xa, xb) for y in (Fr(0), h)]
    qC = min(corners)
    formula = (1 - h) * (m * h * h / 4 - h - eps)
    assert qC == formula, (qC, formula)
    L = 2
    local = 2 * L * h * h / 8
    glob = (m + 1) * L * h * h / 8
    return dict(h=h, m=m, U=U, qC=qC, local=local, rejected_by_local=(qC - local > U),
                glob=glob, kept_by_global=(qC - glob <= U),
                needed_over_global=(qC - U) / glob)

# ---------- family B (positive definite): F = (x-1/2)^2 + sum (y - h/2 - (x-1/2)/d)^2
def famB_minmarg(h, d, x, y1):
    G = grid(h)
    t = x - Fr(1, 2)
    ideal = h / 2 + t / d
    best = min((y - ideal) ** 2 for y in G)
    return t * t + (y1 - ideal) ** 2 + (d * d - 1) * best

def check_famB(h, d):
    G = grid(h)
    Vh = {}
    for x in G:
        t = x - Fr(1, 2)
        ideal = h / 2 + t / d
        Vh[x] = t * t + d * d * min((y - ideal) ** 2 for y in G)
    U = min(Vh.values())
    # optimizer projection (1/2, h/2) lies in the two cells [1/2-h,1/2]x[0,h], [1/2,1/2+h]x[0,h]
    qs = []
    for xa, xb in ((Fr(1, 2) - h, Fr(1, 2)), (Fr(1, 2), Fr(1, 2) + h)):
        qs.append(min(famB_minmarg(h, d, x, y) for x in (xa, xb) for y in (Fr(0), h)))
    gap_formula = d * h * (Fr(1, 2) - h) + 2 * h * h - Fr(1, 2)
    assert all(q - U == gap_formula for q in qs), (qs, U, gap_formula)
    local = 2 * 4 * h * h / 8
    return dict(h=h, d=d, U=U, q=qs, needed=gap_formula, local=local,
                rejected=(min(qs) - local > U))

if __name__ == "__main__":
    # (a) the report's instance: m=32, eps=1/16, grid {0,1/2,1}
    h, m, eps = Fr(1, 2), 32, Fr(1, 16)
    c, l = famA_parts(h, m, eps)
    G = grid(h)
    Vh = [c(x) + m * min(l(x, y) for y in G) for x in G]
    assert Vh == [0, Fr(23, 32), Fr(31, 16)], Vh
    corners = {(x, y): famA_minmarg(h, m, eps, x, y) for x in (Fr(1, 2), Fr(1)) for y in (Fr(0), Fr(1, 2))}
    print("m=32 conditional grid values", [str(v) for v in Vh])
    print("cell corners", {k: str(v) for k, v in corners.items()})
    assert min(corners.values()) == Fr(23, 32)
    assert 2 * 2 * h * h / 8 == Fr(1, 8) and 33 * 2 * h * h / 8 == Fr(33, 16)
    # outside error identity V_h - V = m dist(x/4,G)^2 on a fine set of x
    for i in range(0, 65):
        x = Fr(i, 64)
        Vhx = c(x) + m * min(l(x, y) for y in G)
        Vx = -x * x + (1 - eps) * x
        dist = min(abs(x / 4 - y) for y in G)
        assert Vhx - Vx == m * dist * dist
    print("identity V_h - V = m dist(x/4,G)^2 verified on 65 rational points")
    # brute-force cross-check of separability on small m (same formulas)
    for (hh, mm) in ((Fr(1, 2), 3), (Fr(1, 4), 2)):
        check_famA(hh, mm, Fr(1, 64), brute=True)
    print("brute-force separability cross-check passed")
    # family A for several meshes
    for hh in (Fr(1, 2), Fr(1, 4), Fr(1, 8), Fr(1, 16)):
        for mm in (int(8 / (hh * hh)), int(64 / (hh * hh))):
            r = check_famA(hh, mm, Fr(1, 64))
            assert r["rejected_by_local"] and r["kept_by_global"]
            print("famA h=%s m=%d U=%s qC=%s needed/global=%.4f" % (hh, mm, r["U"], r["qC"], float(r["needed_over_global"])))
    # family B (bounded kappa)
    for d in (8, 9, 16, 64, 1000):
        r = check_famB(Fr(1, 4), d)
        assert r["needed"] == Fr(d, 16) - Fr(3, 8)
        print("famB h=1/4 d=%d needed=%s rejected_by_local=%s" % (d, r["needed"], r["rejected"]))
    for hh in (Fr(1, 8), Fr(1, 16)):
        for d in (int(4 / hh), int(16 / hh)):
            r = check_famB(hh, d)
            print("famB h=%s d=%d needed=%s local=%s rejected=%s" % (hh, d, r["needed"], r["local"], r["rejected"]))
    print("ALL STAR CHECKS PASSED")
