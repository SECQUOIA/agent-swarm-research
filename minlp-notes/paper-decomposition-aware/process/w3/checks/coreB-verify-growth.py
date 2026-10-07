"""coreB verification checks for Section 5 / Appendix A (W3, verifier).

Exact (Fraction) checks of statements not covered by coreB-commonmesh.py:
 1. Lemma lem:graded (a), (b), (c) on random graded grids (continuous and
    integer coordinates).
 2. TRIAL with per-coordinate meshes h_ij = eta_j r_i under weighted growth
    (Lemmas lem:inv (i)-(v) and lem:states: radius R_ij and cap K(theta,n_P)),
    with the free parameter k = max{1, 1/gamma} and 8 k theta^2 <= 1.
 3. Theorem thm:approx(a) termination counts: with theta s_i <= h_ij and
    h_ij a power of two, every grid has at most 1 + 2/theta nodes; with the
    common mesh h_j = s 2^{-j} (not a power of two) at most 1 + 4/theta.
 4. Proposition prop:sharp (min-marginal bound) and Corollary
    cor:uniformgrid (uniform grids, theta = 0, centre 0): simulation.
 5. Example ex:family: growth constant 1/2, curvature 21/8, strict local
    minima, on small graphs.
 6. Scalar facts: 2^{mu*} <= 6 sqrt(kbar), mu* <= 3(1+log2 kbar),
    (eq:logabsorb), Sum_{mu<=mu*} K_mu^p <= 2 K_{mu*}^p.
"""
import itertools
import math
import random
import sys
from fractions import Fraction as Fr


def graded(lo, hi, c, h, th, integer):
    def sig(t):
        return max(Fr(1), Fr(math.floor(h + th * t))) if integer else h + th * t
    nodes = {c}
    sides = []
    for side, R in ((1, hi - c), (-1, c - lo)):
        t = Fr(0)
        cnt = 0
        while t < R:
            t = min(t + sig(t), R)
            nodes.add(c + side * t)
            cnt += 1
        sides.append((R, cnt))
    return sorted(nodes), sides


def eff(a, b, integer):
    return Fr(0) if (integer and b - a == 1) else b - a


def widths(gr, integer):
    wi = {}
    for k, v in enumerate(gr):
        cand = [Fr(0)]
        if k > 0:
            cand.append(eff(gr[k - 1], v, integer))
        if k + 1 < len(gr):
            cand.append(eff(v, gr[k + 1], integer))
        wi[v] = max(cand)
    return wi


def check_graded(trials=3000):
    for _ in range(trials):
        integer = random.random() < 0.5
        th = Fr(1, random.choice([4, 5, 8, 16, 32]))
        if integer:
            lo = random.randint(-50, 0)
            hi = lo + random.randint(1, 400)
            c = random.randint(lo, hi)
            h = Fr(random.randint(1, 64), random.choice([1, 2, 4, 8, 16]))
            lo, hi, c = Fr(lo), Fr(hi), Fr(c)
        else:
            lo = Fr(random.randint(-50, 0), random.choice([1, 3]))
            hi = lo + Fr(random.randint(1, 400), random.choice([1, 2, 7]))
            c = lo + (hi - lo) * Fr(random.randint(0, 20), 20)
            h = Fr(random.randint(1, 64), random.choice([1, 2, 4, 8, 16, 64]))
        gr, sides = graded(lo, hi, c, h, th, integer)
        w = widths(gr, integer)
        for v in gr:  # (a)
            assert w[v] <= h + th * abs(v - c), ("graded (a)", v)
        hh = max(h, Fr(1)) if integer else h
        for R, cnt in sides:  # (b)
            if R > 0:
                bound = math.ceil(4 / float(th) * math.log(1 + float(th * R / hh)) + 1e-12)
                assert cnt <= bound, ("graded (b)", cnt, bound)
        if h >= hi - lo:  # (c)
            assert len(gr) <= 3
    print("Lemma lem:graded (a)-(c) ok on", trials, "random grids")


def ldl_psd(A):
    A = [row[:] for row in A]
    n = len(A)
    for k in range(n):
        if A[k][k] < 0:
            return False
        if A[k][k] == 0:
            if any(A[k][j] != 0 for j in range(k + 1, n)):
                return False
            continue
        for i in range(k + 1, n):
            f = A[i][k] / A[k][k]
            for j in range(k + 1, n):
                A[i][j] -= f * A[k][j]
    return True


def make_instance(n, magmax):
    """Planted box QP with x* and an exactly certified weighted growth constant
    gamma: H + 2M - 2 gamma diag(L) PSD, M_ii = mag_i / s_i at active bounds."""
    while True:
        types = [random.choice("CZ") for _ in range(n)]
        lo, hi = [], []
        for t in types:
            if t == "Z":
                a = random.randint(-6, 0)
                lo.append(Fr(a)); hi.append(Fr(a + random.randint(3, 12)))
            else:
                a = Fr(random.randint(-8, 0), random.choice([1, 2, 3]))
                lo.append(a); hi.append(a + Fr(random.randint(2, 15), random.choice([1, 2, 4])))
        xs = []
        for i in range(n):
            kind = random.choice(["lo", "hi", "in", "in"])
            if kind == "lo":
                xs.append(lo[i])
            elif kind == "hi":
                xs.append(hi[i])
            elif types[i] == "Z":
                xs.append(Fr(random.randint(int(lo[i]), int(hi[i]))))
            else:
                xs.append(lo[i] + (hi[i] - lo[i]) * Fr(random.randint(1, 9), 10))
        H = [[Fr(0)] * n for _ in range(n)]
        for i in range(n):
            # widely different curvatures, so that per-coordinate meshes differ
            H[i][i] = Fr(random.randint(-2, 12), random.choice([1, 2])) * random.choice([1, 1, 16, 64])
            for j in range(i):
                H[i][j] = H[j][i] = Fr(random.randint(-8, 8), random.choice([1, 2]))
        zeta, mu = [Fr(0)] * n, [Fr(0)] * n
        for i in range(n):
            if lo[i] < xs[i] < hi[i]:
                continue
            mag = Fr(random.randint(1, magmax), random.choice([1, 2, 4]))
            zeta[i] = mag if xs[i] == lo[i] else -mag
            mu[i] = mag / (hi[i] - lo[i])
        L = [max(H[i][i], Fr(0)) for i in range(n)]
        if not any(L):
            continue
        gam = None
        for e in range(0, 16):
            gg = Fr(1, 2**e)
            A = [[H[i][j] + (2 * mu[i] - 2 * gg * L[i] if i == j else 0) for j in range(n)]
                 for i in range(n)]
            if ldl_psd(A):
                gam = gg
                break
        if gam is None:
            continue
        b = [zeta[i] - sum(H[i][j] * xs[j] for j in range(n)) for i in range(n)]
        return dict(n=n, types=types, lo=lo, hi=hi, xs=xs, H=H, b=b, L=L, gam=gam)


def F(inst, x):
    H, b, n = inst["H"], inst["b"], inst["n"]
    return (sum(Fr(1, 2) * H[i][j] * x[i] * x[j] for i in range(n) for j in range(n))
            + sum(b[i] * x[i] for i in range(n)))


def run_weighted(inst, mu_exp, stages=10):
    n, types, L = inst["n"], inst["types"], inst["L"]
    lo, hi, xs, gam = inst["lo"], inst["hi"], inst["xs"], inst["gam"]
    P = [i for i in range(n) if L[i] > 0]
    nP = len(P)
    th = Fr(1, 2**mu_exp)
    k = max(Fr(1), 1 / gam)
    assert 8 * k * th * th <= 1
    OPT = F(inst, xs)
    s = [hi[i] - lo[i] for i in range(n)]
    e, r = {}, {}
    for i in P:
        ei = 0
        while not (Fr(4) ** (ei - 1) < L[i] <= Fr(4) ** ei):
            ei += 1 if L[i] > Fr(4) ** ei else -1
        e[i], r[i] = ei, Fr(1, 2**ei) if ei >= 0 else Fr(2 ** (-ei))
        assert Fr(1, 4) < L[i] * r[i] ** 2 <= 1
    E = -100
    while not all(Fr(2) ** E * r[i] >= s[i] if E >= 0 else r[i] / Fr(2) ** (-E) >= s[i] for i in P):
        E += 1
    def two(x):
        return Fr(2) ** x if x >= 0 else Fr(1, 2 ** (-x))
    cap = 10 * 2**mu_exp * math.ceil(math.log2(nP + 2))
    box = [(lo[i], hi[i]) for i in range(n)]
    c = list(lo)
    U = F(inst, lo)
    maxnodes = 0
    for j in range(stages):
        eta = two(E - j)
        hij = {i: eta * r[i] for i in P}
        for i in P:  # power of two
            x = hij[i]
            assert x.numerator & (x.numerator - 1) == 0 and x.denominator & (x.denominator - 1) == 0
        G = [graded(box[i][0], box[i][1], c[i], hij[i], th, types[i] == "Z")[0] if i in P
             else [lo[i], hi[i]] for i in range(n)]
        maxnodes = max(maxnodes, max(len(gr) for gr in G))
        assert all(len(gr) <= cap for gr in G), "lem:states cap"
        if j == 0:
            assert all(len(G[i]) <= 3 for i in P)
        w = [widths(G[i], types[i] == "Z") for i in range(n)]
        Qv, Fv, Dv = {}, {}, {}
        for y in itertools.product(*G):
            fy = F(inst, y)
            dy = sum(L[i] * w[i][y[i]] ** 2 / 8 for i in range(n))
            Fv[y], Dv[y], Qv[y] = fy, dy, fy - dy
        beta = min(Qv.values())
        y = min(kk for kk in Qv if Qv[kk] == beta)
        m = [{v: min(Qv[kk] for kk in Qv if kk[i] == v) for v in G[i]} for i in range(n)]
        U = min(U, Fv[y])
        a = nP * eta * eta
        nL = lambda d: sum(L[i] * d[i] ** 2 for i in P)
        # (i)
        assert all(box[i][0] <= xs[i] <= box[i][1] for i in range(n)) and beta <= OPT, "(i)"
        cx = nL([c[i] - xs[i] for i in range(n)])
        for z in Qv:  # eq:energy
            assert Dv[z] <= a / 4 + th * th / 2 * (nL([z[i] - xs[i] for i in range(n)]) + cx), "energy"
        assert cx <= 4 * k * a, "(ii)"
        assert nL([y[i] - xs[i] for i in range(n)]) <= Fr(8, 15) * k * a, "(iii)"
        assert U - beta <= Fv[y] - beta == Dv[y] <= Fr(9, 16) * a, "(iv)"
        for z, qz in Qv.items():
            if qz <= U:
                assert nL([z[i] - xs[i] for i in range(n)]) <= Fr(17, 15) * k * a, "(v)"
        if U - beta <= Fr(1, 10**7):
            return ("success", j, maxnodes, cap)
        newbox = list(box)
        rho = math.sqrt(float(k * nP))
        for i in P:
            gr = G[i]
            kept = [(p, q) for p, q in zip(gr[:-1], gr[1:]) if min(m[i][p], m[i][q]) <= U]
            nb = (min(kk[0] for kk in kept), max(kk[1] for kk in kept))
            R = Fr(7.3 * rho) * hij[i] + (1 if types[i] == "Z" else 0)
            assert y[i] - R <= nb[0] and nb[1] <= y[i] + R, "lem:states radius"
            newbox[i] = nb
        box = newbox
        c = list(y)
    return ("stages", j, maxnodes, cap)


def check_termination(trials=2000):
    """thm:approx(a): theta s_i <= h_ij, h_ij power of two -> <= 1+2/theta nodes.
    commonmesh: theta s_i <= h_j, h_j = s 2^{-j} -> <= 1 + 4/theta nodes."""
    for _ in range(trials):
        integer = random.random() < 0.5
        mu = random.randint(2, 6)
        th = Fr(1, 2**mu)
        # power-of-two mesh
        h = Fr(2) ** random.randint(-3, 6)
        smax = h / th
        if integer:
            si = random.randint(1, max(1, int(smax)))
            lo = Fr(random.randint(-5, 5)); hi = lo + si
            c = Fr(random.randint(int(lo), int(hi)))
        else:
            si = smax * Fr(random.randint(1, 100), 100)
            lo = Fr(random.randint(-5, 5)); hi = lo + si
            c = lo + si * Fr(random.randint(0, 10), 10)
        gr, _ = graded(lo, hi, c, h, th, integer)
        assert len(gr) <= 1 + 2 / th, ("approx(a)", len(gr))
        # common mesh, arbitrary rational
        h = Fr(random.randint(1, 200), random.randint(1, 50))
        smax = h / th
        if integer:
            if smax < 1:
                continue
            si = random.randint(1, int(smax))
            lo = Fr(0); hi = Fr(si); c = Fr(random.randint(0, si))
        else:
            si = smax * Fr(random.randint(1, 100), 100)
            lo = Fr(0); hi = si; c = si * Fr(random.randint(0, 10), 10)
        gr, _ = graded(lo, hi, c, h, th, integer)
        assert len(gr) <= 1 + 4 / th, ("commonmesh termination", len(gr))
    print("termination counts ok on", trials, "random grids")


def sharp_F(Lam, g, x):
    tot = Fr(0)
    for k in range(0, len(x), 2):
        u, v = x[k], x[k + 1]
        tot += Lam / 2 * (u * u + v * v) + (Lam - 2 * g) * u * v
    return tot


def check_sharp(trials=150):
    tested = 0
    """prop:sharp: random grids containing 0 with w_i(0) >= h, subbox containing
    [-rho,rho]^n; every node a with |a| <= min{rho, h sqrt((n-2)kappa/16)} has
    m_i(a) <= 0."""
    for _ in range(trials):
        mm = random.choice([2, 3])
        n = 2 * mm
        Lam = Fr(random.randint(1, 8))
        g = Lam / 2 / random.choice([1, 2, 3, 5, 8, 20, 50])
        kap = Lam / g
        rho = Fr(random.randint(1, 4), 4)
        h = Fr(random.randint(1, 8), 16)
        G = []
        for i in range(n):
            lo = -rho - Fr(random.randint(0, 3), 8)
            hi = rho + Fr(random.randint(0, 3), 8)
            lo, hi = max(lo, Fr(-1)), min(hi, Fr(1))
            pts = {lo, hi, Fr(0)}
            # neighbours of 0 at distance >= h on at least one side
            side = random.choice([1, -1])
            if side == 1 and h <= hi:
                pts.add(min(hi, h + Fr(random.randint(0, 4), 32)))
            elif side == -1 and -h >= lo:
                pts.add(max(lo, -h - Fr(random.randint(0, 4), 32)))
            else:
                continue
            for _ in range(random.randint(0, 3)):
                pts.add(lo + (hi - lo) * Fr(random.randint(0, 32), 32))
            gr = sorted(pts)
            w = widths(gr, False)
            if w[Fr(0)] < h:
                break
            G.append(gr)
        if len(G) < n:
            continue
        W = [widths(gr, False) for gr in G]
        Qv = {}
        for y in itertools.product(*G):
            Qv[y] = sharp_F(Lam, g, y) - sum(Lam * W[i][y[i]] ** 2 / 8 for i in range(n))
        bound = float(h) * math.sqrt((n - 2) * float(kap) / 16)
        for i in range(n):
            for a in G[i]:
                if abs(a) <= rho and float(abs(a)) <= bound - 1e-12:
                    ma = min(q for y, q in Qv.items() if y[i] == a)
                    assert ma <= 0, ("prop:sharp", ma)
                    tested += 1
    print("prop:sharp ok:", tested, "min-marginals tested")


def check_uniform(nlist=(4, 6), kappas=(Fr(2), Fr(8), Fr(40), Fr(200))):
    """cor:uniformgrid: TRIAL with common mesh h_j = 2^{1-j}, theta = 0, centre 0."""
    tested = 0
    for n in nlist:
        for kap in kappas:
            Lam = Fr(1)
            g = Lam / kap
            nu = math.isqrt(int(math.floor((n - 2) * kap / 16)))
            # floor(sqrt(x)) for rational x: adjust
            x = (n - 2) * kap / 16
            nu = 0
            while Fr((nu + 1) ** 2) <= x:
                nu += 1
            box = [(Fr(-1), Fr(1))] * n
            c = [Fr(0)] * n
            for j in range(0, 6):
                h = Fr(2) / 2**j
                G = [graded(box[i][0], box[i][1], c[i], h, Fr(0), False)[0] for i in range(n)]
                if j >= 1 and (nu + 1) * (h * 2) <= 1:
                    pass
                if max(len(gr) for gr in G) ** n > 200000:
                    break
                W = [widths(gr, False) for gr in G]
                Qv = {}
                for y in itertools.product(*G):
                    Qv[y] = sharp_F(Lam, g, y) - sum(Lam * W[i][y[i]] ** 2 / 8 for i in range(n))
                beta = min(Qv.values())
                arg = [y for y in Qv if Qv[y] == beta]
                assert arg == [tuple([Fr(0)] * n)], ("corrected minimizer", arg)
                U = Fr(0)
                newbox = []
                for i in range(n):
                    gr = G[i]
                    mi = {v: min(q for y, q in Qv.items() if y[i] == v) for v in gr}
                    kept = [(p, q) for p, q in zip(gr[:-1], gr[1:]) if min(mi[p], mi[q]) <= U]
                    newbox.append((min(kk[0] for kk in kept), max(kk[1] for kk in kept)))
                if j >= 1 and (nu + 1) * h <= 1:
                    for nb in newbox:
                        assert nb[0] <= -(nu + 1) * h and nb[1] >= (nu + 1) * h, ("filtered box", j, nb)
                    Gn = graded(newbox[0][0], newbox[0][1], Fr(0), h / 2, Fr(0), False)[0]
                    assert len(Gn) >= 4 * nu + 5 and 4 * nu + 5 >= math.sqrt((n - 2) * kap) + 1
                    tested += 1
                box = newbox
    print("cor:uniformgrid ok for n in", nlist, ";", tested, "stages with (nu+1)h_j <= 1 tested")


def check_family(trials=4000):
    # graph: path on 3 blocks (Delta = 2) and a single edge (Delta = 1)
    for edges, mblk in (([(0, 1), (1, 2)], 3), ([(0, 1)], 2)):
        deg = [sum(1 for e in edges if b in e) for b in range(mblk)]
        Dl = max(deg)

        def Fam(x):
            tot = Fr(0)
            for b in range(mblk):
                u, v, r = x[3 * b:3 * b + 3]
                tot += u * u + v * v - 4 * u * v + (u + v) / 4 + (r - u / 2) ** 2
            for (b, bb) in edges:
                tot += (x[3 * b] - x[3 * bb]) ** 2 / (16 * Dl)
            return tot
        xs = [Fr(1), Fr(1), Fr(1, 2)] * mblk
        OPT = Fam(xs)
        for _ in range(trials):
            x = [Fr(random.randint(0, 20), 20) for _ in range(3 * mblk)]
            d2 = sum((x[i] - xs[i]) ** 2 for i in range(3 * mblk))
            assert Fam(x) - OPT >= d2 / 2, "family growth"
        # curvature along u_b
        for b in range(mblk):
            e = [Fr(0)] * (3 * mblk); e[3 * b] = Fr(1)
            z = [Fr(0)] * (3 * mblk)
            curv = Fam(e) + Fam([-t for t in e]) - 2 * Fam(z)
            assert curv <= Fr(21, 8)
        # strict local minima: random feasible perturbations with delta < 1/8
        for pattern in itertools.product([0, 1], repeat=mblk):
            xb = []
            for p in pattern:
                xb += [Fr(0), Fr(0), Fr(0)] if p == 0 else [Fr(1), Fr(1), Fr(1, 2)]
            f0 = Fam(xb)
            for _ in range(300):
                d = []
                for i in range(3 * mblk):
                    t = Fr(random.randint(0, 40), 1000)
                    if i % 3 == 2:
                        t = Fr(random.randint(-40, 40), 1000)
                    elif xb[i] == 1:
                        t = -t
                    d.append(t)
                delta = sum(abs(d[i]) for i in range(3 * mblk) if i % 3 != 2)
                if delta >= Fr(1, 8) or all(t == 0 for t in d):
                    continue
                x = [xb[i] + d[i] for i in range(3 * mblk)]
                assert Fam(x) > f0, "strict local min"
    print("ex:family ok (growth 1/2, curvature <= 21/8, strict local minima)")


def check_scalars():
    for K in [Fr(1), Fr(3, 2), Fr(2), Fr(5), Fr(17, 2), Fr(100), Fr(10**6), Fr(10**12) + 1]:
        mu = 2
        while 4**mu < 8 * K:
            mu += 1
        assert 8 * K / 4**mu <= 1
        assert 2**mu <= 6 * math.sqrt(float(K)) + 1e-9, K
        assert mu <= 3 * (1 + math.log2(float(K))) + 1e-9
    for p in range(1, 30):
        for n in list(range(0, 300)) + [10**k for k in range(3, 18)]:
            assert math.ceil(math.log2(n + 2)) ** p <= 2 * p**p * (n + 2), (p, n)
        for mustar in range(2, 15):
            Ks = [10 * 2**mu for mu in range(2, mustar + 1)]
            assert sum(K**p for K in Ks) <= 2 * Ks[-1] ** p
    print("scalar facts ok")


if __name__ == "__main__":
    random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 11)
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    check_scalars()
    check_graded()
    check_termination()
    check_family()
    check_sharp()
    check_uniform()
    done = 0
    while done < count:
        n = random.choice([2, 2, 3])
        inst = make_instance(n, 40)
        k = max(Fr(1), 1 / inst["gam"])
        if k > 300:
            continue
        mu = 2
        while 8 * k * Fr(1, 4**mu) > 1:
            mu += 1
        res = run_weighted(inst, mu)
        done += 1
        print(done, n, inst["types"], "L=", [str(x) for x in inst["L"]], "k=", k, "mu=", mu, res,
              flush=True)
    print("weighted-growth TRIAL: lem:inv (i)-(v) and lem:states held on", done, "instances")
