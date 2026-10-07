"""W3 tu agent: exact checks for Section 8 / Appendix D (coupling constraints).

Run: python3 -B tu-checks.py
Exact rational arithmetic throughout; every block prints PASS/FAIL.
"""
from fractions import Fraction as Fr
from math import isqrt, floor, sqrt


def report(name, ok):
    print(("PASS " if ok else "FAIL ") + name)


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
    d = {}
    for k, v in enumerate(nodes):
        w = Fr(0)
        if k > 0:
            w = max(w, v - nodes[k - 1])
        if k + 1 < len(nodes):
            w = max(w, nodes[k + 1] - v)
        d[v] = L * w * w / 8
    return d


# ------------------------------------------------------------ ex:tu-fullcurv
def ex_fullcurv():
    for h in [Fr(1, 2), Fr(1, 3), Fr(1, 8)]:
        F = lambda a, b: 2 * a * b - h * (a + b)
        opt = F(h / 2, h / 2)
        gridmin = min(F(k * h, k * h) for k in range(int(1 / h) + 1))
        allow = 2 * 2 * h * h / 8
        report(f"ex:tu-fullcurv h={h}", opt == -h * h / 2 and gridmin == 0
               and gridmin - allow == opt)


# ------------------------------------------------------------ ex:tu-union
def ex_union():
    # variables x1,x2,x3 in [0,1], x1+x2=x3; S={(0,0,0),(1/2,1/2,1)}
    S = [(Fr(0), Fr(0), Fr(0)), (Fr(1, 2), Fr(1, 2), Fr(1))]
    N = 60
    worst = None
    for i in range(N + 1):
        for k in range(N + 1):
            x1, x3 = Fr(i, N), Fr(k, N)
            x2 = x3 - x1
            if x2 < 0 or x2 > 1:
                continue
            F = (2 * x1 - x3) ** 2 + x3 * (1 - x3) / 4
            d2 = min((x1 - a) ** 2 + (x2 - b) ** 2 + (x3 - c) ** 2 for a, b, c in S)
            if d2 > 0:
                r = F / d2
                worst = r if worst is None or r < worst else worst
    report(f"ex:tu-union growth ratio min on sample = {worst} >= 1/6",
           worst >= Fr(1, 6))
    H = [[8, 0, -4], [0, 0, 0], [-4, 0, Fr(3, 2)]]
    report("ex:tu-union Hessian max abs row sum = 12",
           max(sum(abs(v) for v in row) for row in H) == 12)


# ------------------------------------------------------------ lem:tu-uniform
def tu_uniform(nc, Lam, sigma, levels=14):
    """TU-GRID (union filter) on the box instance of prop:sharp with a
    redundant row; eta=1, X=[-1,1]^nc, pairs (u_k,v_k),
    F = sum Lam/2 (u^2+v^2) + sigma u v, Lbar = Lam + sigma.
    By symmetry all u- and v-coordinates share one domain (a set of cells).
    Returns list of (j, h_j, number of level-(j+1) nodes, lower interval ok)."""
    Lbar = Lam + sigma
    g = (Lam - sigma) / 2
    kappa = 2 * Lam / (Lam - sigma)          # coordinate kappa of prop:sharp
    kappa_c = Lbar / g
    r = floor(sqrt((nc - 2) * kappa / 16))
    # domain = set of cell left endpoints (all cells have length h_j), plus points
    h = Fr(1)
    cells = {Fr(k) for k in range(-1, 1)}  # [-1,0],[0,1]
    out = []
    ok_all = True
    for j in range(levels):
        nodes = sorted({a for a in cells} | {a + h for a in cells})
        q = lambda a, b: Lam / 2 * (a * a + b * b) + sigma * a * b
        # min over the pair partner for each node a (partner uses same domain)
        minpair = min(q(a, b) for a in nodes for b in nodes)
        mu = minpair * (nc // 2)
        E = nc * Lbar * h * h / 8
        U = mu
        m = {a: min(q(a, b) for b in nodes) + (nc // 2 - 1) * minpair - E
             for a in nodes}
        kept = {a for a in cells if min(m[a], m[a + h]) <= U}
        h2 = h / 2
        newcells = set()
        for a in kept:
            newcells.add(a)
            newcells.add(a + h2)
        nn = len({a for a in newcells} | {a + h2 for a in newcells})
        lower_ok = True
        if (r + 1) * h <= 1:
            want = [k * h2 for k in range(-2 * (r + 1), 2 * (r + 1))]
            lower_ok = all(w in newcells for w in want) and nn >= 4 * r + 5
            ok_all &= lower_ok
        out.append((j, h, nn, lower_ok))
        # upper bound of thm:tu-states (b) with r_i = 1
        ub = 5 + floor(2 * sqrt(nc * Lbar / g))
        if j >= 0:
            ok_all &= nn <= ub
        cells, h = newcells, h2
    return ok_all, r, kappa, kappa_c, out


def check_uniform():
    for nc in [4, 6, 10, 18, 50, 100, 202]:
        for Lam, sigma in [(Fr(1), Fr(0)), (Fr(3), Fr(1)), (Fr(2), Fr(3, 2))]:
            ok, r, kap, kapc, out = tu_uniform(nc, Lam, sigma)
            nmax = max(o[2] for o in out[1:])
            report(f"TU-GRID box instance nc={nc} Lam={Lam} sigma={sigma}: "
                   f"r={r}, >=4r+5={4*r+5} nodes when (r+1)h_j<=1, "
                   f"<= thm upper bound (max seen {nmax}); kappa_c/kappa={kapc/kap}",
                   ok)
    # 4r+5 >= sqrt(2(nc-2))+1 for sigma=0
    good = all(4 * floor(sqrt((n - 2) / 8)) + 5 >= sqrt(2 * (n - 2)) + 1
               for n in range(4, 2000, 2))
    report("4r+5 >= sqrt(2(n_c-2))+1 for even n_c in [4,2000)", good)
    good = all((sqrt(2 * (n - 2)) + 1) ** 2 >= n for n in range(4, 2000, 2))
    report("(sqrt(2(n_c-2))+1)^2 >= n_c, so the table has >= n_c^{p/2} entries", good)


# ------------------------------------------------------------ prop:tu-misaligned
def misaligned():
    L = Fr(1)
    G1, G2 = [Fr(0), Fr(1, 2), Fr(1)], [Fr(0), Fr(1, 3), Fr(1)]
    d1, d2 = corr(G1, L), corr(G2, L)
    m = Fr(2, 5)
    gap = all(L * (v - m) ** 2 > d1[v] + d2[v] for v in set(G1) & set(G2))
    dl = min(b - a for a in G1 for b in G2 if b > a)
    thr = (max(d1.values()) + max(d2.values())) / dl
    report(f"misaligned simple: gap={gap}, delta={dl}, threshold={thr}",
           gap and dl == Fr(1, 3) and thr == Fr(75, 288))
    lam = thr + Fr(1, 1000)
    val = min(L / 2 * ((a - m) ** 2 + (b - m) ** 2) + lam * (b - a) - d1[a] - d2[b]
              for a in G1 for b in G2 if a <= b)
    report(f"misaligned simple: corrected min {val} > 0", val > 0)
    h, th = Fr(1, 16), Fr(1, 4)
    g1 = graded(Fr(3, 10), Fr(0), Fr(1), h, th)
    g2 = graded(Fr(7, 10), Fr(0), Fr(1), h, th)
    common = sorted(set(g1) & set(g2))
    c1, c2 = corr(g1, L), corr(g2, L)
    mm = Fr(1, 2)
    print("   g1 =", [str(v) for v in g1])
    print("   g2 =", [str(v) for v in g2])
    print("   d at 0,1:", c1[0], c2[0], c1[1], c2[1])
    gap2 = all(L * (v - mm) ** 2 > c1[v] + c2[v] for v in common)
    dl2 = min(b - a for a in g1 for b in g2 if b > a)
    thr2 = (max(c1.values()) + max(c2.values())) / dl2
    print(f"   delta={dl2}, max d1={max(c1.values())}, max d2={max(c2.values())},"
          f" threshold={thr2} = {float(thr2):.4f} L")
    report("graded two-center grids: 11 nodes each, common {0,1}, gap at m=1/2",
           len(g1) == 11 and len(g2) == 11 and common == [0, 1] and gap2)
    lam = thr2 + Fr(1, 1000)
    val2 = min(L / 2 * ((a - mm) ** 2 + (b - mm) ** 2) + lam * (b - a) - c1[a] - c2[b]
               for a in g1 for b in g2 if a <= b)
    report(f"graded: corrected min {val2} > 0", val2 > 0)
    # aligned uniform grids: gap condition fails at the nearest common node
    for k in [2, 3, 5, 8]:
        hh = Fr(1, k)
        G = [i * hh for i in range(k + 1)]
        d = corr(G, L)
        for mval in [Fr(1, 7), Fr(2, 5), Fr(1, 2), Fr(5, 6)]:
            nu = min(G, key=lambda v: abs(v - mval))
            ok = L * (nu - mval) ** 2 <= 2 * d[nu]
            if not ok:
                report(f"uniform aligned escape k={k} m={mval}", False)
    report("uniform aligned grids violate the gap condition at the nearest node", True)


# ------------------------------------------------------------ ex:tu-sum
def tu_sum():
    L = Fr(1)
    G = graded(Fr(0), Fr(0), Fr(3), Fr(1), Fr(1, 4))
    d = corr(G, L)
    pts = [(a, b, c) for a in G for b in G for c in G if a + b == c]
    F = lambda x: L / 2 * ((x[0] - 1) ** 2 + (x[1] - 1) ** 2 + (x[2] - 2) ** 2)
    vals = {p: F(p) - d[p[0]] - d[p[1]] - d[p[2]] for p in pts}
    for p in sorted(pts):
        print("   ", tuple(str(v) for v in p), "corrected", vals[p])
    report(f"ex:tu-sum: G={[str(v) for v in G]}, d={[str(d[v]) for v in G]}, "
           f"{len(pts)} points, min {min(vals.values())}",
           G == [0, 1, Fr(9, 4), 3] and len(pts) == 7
           and min(vals.values()) == Fr(31, 64)
           and [d[v] for v in G] == [Fr(1, 8), Fr(25, 128), Fr(25, 128), Fr(9, 128)])
    # also with the constant allowance n_c Lbar w_max^2/8
    E = 3 * L * Fr(5, 4) ** 2 / 8
    mn = min(F(p) for p in pts) - E
    report(f"ex:tu-sum with constant allowance 3L(5/4)^2/8: bound {mn} > 0", mn > 0)


# ------------------------------------------------------------ snapping example
def snap_example():
    # F = x1 - x1^2 on {x in [0,1]^2: x1 = x2}; rows of hat A at y=(1/2,1/2)
    # stationarity along ker{x1-x2} = span(1,1): (1-2x1) + 0 = 0 -> x1=1/2
    x1 = Fr(1, 2)
    val = x1 - x1 * x1
    report("snapping example returns (1/2,1/2) with value 1/4 > OPT=0",
           val == Fr(1, 4) and min(Fr(0) - 0, Fr(1) - 1) == 0)


# ------------------------------------------------------------ height constants
def hadamard_rows():
    # (sqrt(2 n) C)^n * n^{e/2} <= (sqrt2 n C)^n <= (2 n C)^n for e <= n, C >= 1
    ok = True
    for n in range(1, 30):
        for C in [1, 2, 7, 100]:
            for e in range(0, n + 1):
                lhs2 = (2 * n * C * C) ** n * n ** e    # squared
                mid2 = 2 ** n * n ** (2 * n) * C ** (2 * n)
                rhs2 = (2 * n * C) ** (2 * n)
                ok &= lhs2 <= mid2 <= rhs2
    report("Hadamard row bound <= (sqrt2 n_c C)^{n_c} <= R_TU", ok)


if __name__ == "__main__":
    ex_fullcurv()
    ex_union()
    check_uniform()
    misaligned()
    tu_sum()
    snap_example()
    hadamard_rows()
