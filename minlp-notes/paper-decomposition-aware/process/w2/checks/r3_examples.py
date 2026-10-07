"""R3 (constraints/optsets) exact checks of small examples and obstructions.

Run: python3 -B r3_examples.py
Each block prints PASS/FAIL lines. Exact rational arithmetic throughout.
"""
from fractions import Fraction as Fr
from itertools import product
from math import isqrt, floor, sqrt


def graded(c, lo, hi, h, th):
    """Graded grid of Definition def:graded (continuous coordinate)."""
    nodes = {c}
    t = Fr(0)
    while t < hi - c:
        t = min(t + h + th * t, hi - c)
        nodes.add(c + t)
    t = Fr(0)
    while t < c - lo:
        t = min(t + h + th * t, c - lo)
        nodes.add(c - t)
    return sorted(nodes)


def corr(nodes, L):
    """d(v) = L w(v)^2 / 8 with w the largest adjacent interval."""
    d = {}
    for k, v in enumerate(nodes):
        w = Fr(0)
        if k > 0:
            w = max(w, v - nodes[k - 1])
        if k + 1 < len(nodes):
            w = max(w, nodes[k + 1] - v)
        d[v] = L * w * w / 8
    return d


def report(name, ok):
    print(("PASS " if ok else "FAIL ") + name)


# ---------------------------------------------------------------- ex:tu-fullcurv
def ex_fullcurv():
    for h in [Fr(1, 2), Fr(1, 3), Fr(1, 8)]:
        F = lambda a, b: 2 * a * b - h * (a + b)
        opt = F(h / 2, h / 2)
        k_max = int(1 / h)
        gridmin = min(F(k * h, k * h) for k in range(k_max + 1))
        E = 2 * 2 * h * h / 8
        report(f"fullcurv h={h}: OPT=-h^2/2, grid min 0, 0-E=OPT",
               opt == -h * h / 2 and gridmin == 0 and gridmin - E == opt)


# ---------------------------------------------------------------- ex:tu-union
def ex_union():
    # growth F_b >= (1/6) dist^2 on a fine rational sample of X_b
    S = [(Fr(0), Fr(0), Fr(0)), (Fr(1, 2), Fr(1, 2), Fr(1))]
    N = 40
    worst = None
    for i in range(N + 1):
        for k in range(N + 1):
            x, z = Fr(i, N), Fr(k, N)
            t = z - x
            if t < 0 or t > 1:
                continue
            F = (2 * x - z) ** 2 + z * (1 - z) / 4
            d2 = min((x - a) ** 2 + (t - b) ** 2 + (z - c) ** 2 for a, b, c in S)
            if d2 > 0:
                r = F / d2
                worst = r if worst is None or r < worst else worst
    report(f"tu-union growth ratio min on grid = {worst} >= 1/6", worst >= Fr(1, 6))
    # bound quoted for the union variant
    for nb in [1, 10, 100]:
        b = 2 * (5 + isqrt(4 * 216 * nb))
        print(f"   union bound n_b={nb}: {b} ; hull grid exceeds it once 2^j+1 > {b}")


# ---------------------------------------------------------------- prop:tu-tight
def tu_tight():
    # separable box instance: M_i(t) = (L/2)(t-1/2)^2 when 1/2 is a grid node
    L = Fr(1)
    for nc in [4, 9, 16, 25, 50, 100]:
        k = isqrt(nc) // 2 if isqrt(nc) ** 2 == nc else floor(sqrt(nc) / 2)
        lo, hi = Fr(0), Fr(1)
        D = (lo, hi)  # one interval per coordinate (all coordinates equal)
        ok = True
        for j in range(0, 14):
            h = Fr(1, 2 ** j)
            nodes = [D[0] + m * h for m in range(int((D[1] - D[0]) / h) + 1)]
            E = nc * L * h * h / 8
            # exact min-marginals for the box instance
            best_other = min((L / 2) * (v - Fr(1, 2)) ** 2 for v in nodes)
            M = {t: (L / 2) * (t - Fr(1, 2)) ** 2 + (nc - 1) * best_other for t in nodes}
            U = min(M.values())
            keep = [t for t in nodes[:-1]
                    if min(M[t], M[t + h]) - E <= U]
            newD = (min(keep), max(keep) + h)
            # union = hull here (contiguous); verify contiguity
            cells = set(keep)
            contiguous = all((t in cells) for t in
                             [newD[0] + m * h for m in range(int((newD[1] - newD[0]) / h))])
            if j >= 1 and (k + 1) * h <= Fr(1, 2):
                want = (Fr(1, 2) - (k + 1) * h, Fr(1, 2) + (k + 1) * h)
                npts = int((newD[1] - newD[0]) / (h / 2)) + 1
                ok &= newD == want and contiguous and npts == 4 * k + 5
            D = newD
        report(f"tu-tight n_c={nc}: D^(j+1)=[1/2-(k+1)h,1/2+(k+1)h], 4k+5 nodes", ok)


# ---------------------------------------------------------------- prop:tu-misaligned
def tu_misaligned():
    L = Fr(1)
    G1, G2 = [Fr(0), Fr(1, 2), Fr(1)], [Fr(0), Fr(1, 3), Fr(1)]
    d1, d2 = corr(G1, L), corr(G2, L)
    m = Fr(2, 5)
    gap = all(L * (v - m) ** 2 > d1[v] + d2[v] for v in set(G1) & set(G2))
    gam = min(b - a for a in G1 for b in G2 if b > a)
    thr = (max(d1.values()) + max(d2.values())) / gam
    report(f"misaligned example: gap ok={gap}, gamma={gam}, threshold={thr}=75/288",
           gap and gam == Fr(1, 3) and thr == Fr(75, 288))
    lam = thr + Fr(1, 1000)
    val = min(L / 2 * ((a - m) ** 2 + (b - m) ** 2) + lam * (b - a) - d1[a] - d2[b]
              for a in G1 for b in G2 if a <= b)
    report(f"misaligned: corrected min {val} > 0 at lambda slightly above threshold", val > 0)
    # graded grids around 3/10 and 7/10, h=1/16, theta=1/4
    h, th = Fr(1, 16), Fr(1, 4)
    g1 = graded(Fr(3, 10), Fr(0), Fr(1), h, th)
    g2 = graded(Fr(7, 10), Fr(0), Fr(1), h, th)
    common = sorted(set(g1) & set(g2))
    c1, c2 = corr(g1, L), corr(g2, L)
    mm = Fr(1, 2)
    gap2 = all(L * (v - mm) ** 2 > c1[v] + c2[v] for v in common)
    print(f"   graded grids: |g1|={len(g1)}, |g2|={len(g2)}, common={common}")
    report("graded two-center grids: 11 nodes each, common {0,1}, gap with m=1/2",
           len(g1) == 11 and len(g2) == 11 and common == [0, 1] and gap2)
    gam2 = min(b - a for a in g1 for b in g2 if b > a)
    thr2 = (max(c1.values()) + max(c2.values())) / gam2
    lam = thr2 + Fr(1, 1000)
    val2 = min(L / 2 * ((a - mm) ** 2 + (b - mm) ** 2) + lam * (b - a) - c1[a] - c2[b]
               for a in g1 for b in g2 if a <= b)
    print(f"   graded: gamma={gam2}, threshold lambda={thr2} (={float(thr2):.4f} L)")
    report(f"graded: corrected min {val2} > 0", val2 > 0)


# ---------------------------------------------------------------- ex:tu-sum
def tu_sum():
    L = Fr(1)
    G = graded(Fr(0), Fr(0), Fr(3), Fr(1), Fr(1, 4))
    d = corr(G, L)
    pts = [(a, b, c) for a in G for b in G for c in G if a + b == c]
    F = lambda x: L / 2 * ((x[0] - 1) ** 2 + (x[1] - 1) ** 2 + (x[2] - 2) ** 2)
    vals = sorted(F(p) - d[p[0]] - d[p[1]] - d[p[2]] for p in pts)
    report(f"tu-sum: G={G}, d={[d[v] for v in G]}, {len(pts)} feasible pts, min {vals[0]}",
           G == [0, 1, Fr(9, 4), 3] and len(pts) == 7 and vals[0] == Fr(31, 64))


# ---------------------------------------------------------------- prop:twocenters
def twocenters():
    """beta <= -max{theta^2 M^2/379, h^2/20} for graded x-grid; z-grid {0,M}."""
    M = Fr(1)
    worst = None
    cases = 0
    for th in [Fr(1, 4), Fr(1, 8), Fr(1, 16), Fr(1, 32)]:
        for h in [Fr(1), Fr(1, 2), Fr(1, 5), Fr(1, 16), Fr(1, 17), Fr(1, 64), Fr(1, 200)]:
            for cx in [Fr(0), Fr(1, 7), Fr(1, 3), Fr(1, 2), Fr(5, 7), Fr(1)]:
                gx = graded(cx, Fr(0), M, h, th)
                dx = corr(gx, Fr(2))
                gz = [Fr(0), M]  # CT grid for L_z = 0 (z not in P)
                beta = min(x * x - 2 * x * z + M * z - dx[x] for x in gx for z in gz)
                bound = -max(th * th * M * M / 379, h * h / 20)
                cases += 1
                r = beta - bound
                worst = r if worst is None or r > worst else worst
    report(f"twocenters: beta <= bound on {cases} cases (max beta-bound = {worst})", worst <= 0)


def twocenters_ct_grid_count():
    """In CT/FG, z has L_z=0, so G_z={0,M}: the bag table is 2*|G_x|, not |G_x|^2."""
    M = Fr(64)
    th = Fr(1, 4)
    for h in [Fr(1, 4), Fr(1, 16)]:
        gx = graded(Fr(0), Fr(0), M, h, th)
        print(f"   M={M}, h={h}: |G_x|={len(gx)}, |G_z|=2 (z not in P), table={2*len(gx)}"
              f" vs claimed >= M^2/2304 = {float(M*M/2304):.2f} only once eps<1")


if __name__ == "__main__":
    ex_fullcurv()
    ex_union()
    tu_tight()
    tu_misaligned()
    tu_sum()
    twocenters()
    twocenters_ct_grid_count()
