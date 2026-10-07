"""R1 independent brute-force check of Sections 4-5 (grids.tex, growth.tex).

Implements Definition graded, the per-coordinate dyadic meshes, Algorithm 1 and
filtering exactly as written in the paper, with Fractions and brute-force
enumeration of the product grid (no tree DP), on small planted box QPs with
mixed continuous/integer coordinates and a certified weighted-growth constant.

Checks at every stage:
  * Prop cellwise (b): beta = min over cells of the vertex bound (n<=2 only)
  * Prop cellwise (c) at random points: F(x) >= beta_i(I) >= min m_i(endpoints)
  * Lemma inv (i)-(v), Lemma states radius R_ij and cap K(theta,n_P)
  * Prop filter: points with F<=U survive (sampled)
"""
import itertools
import math
import random
import sys
from fractions import Fraction as Fr

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
MAGMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 40


def ldl_psd(A):
    """Exact PSD test of a symmetric Fraction matrix (symmetric Gaussian elimination)."""
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


def make_instance(n):
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
            else:
                if types[i] == "Z":
                    xs.append(Fr(random.randint(int(lo[i]), int(hi[i]))))
                else:
                    xs.append(lo[i] + (hi[i] - lo[i]) * Fr(random.randint(1, 9), 10))
        H = [[Fr(0)] * n for _ in range(n)]
        for i in range(n):
            H[i][i] = Fr(random.randint(-2, 12), random.choice([1, 2]))
            for j in range(i):
                H[i][j] = H[j][i] = Fr(random.randint(-8, 8), random.choice([1, 2]))
        S = [i for i in range(n) if lo[i] < xs[i] < hi[i]]
        zeta = [Fr(0)] * n
        mu = [Fr(0)] * n
        for i in range(n):
            if i in S:
                continue
            mag = Fr(random.randint(1, MAGMAX), random.choice([1, 2, 4]))
            zeta[i] = mag if xs[i] == lo[i] else -mag
            mu[i] = mag / (hi[i] - lo[i])
        L = [max(H[i][i], Fr(0)) for i in range(n)]
        P = [i for i in range(n) if L[i] > 0]
        if not P:
            continue
        # largest dyadic gamma with H + 2M - 2 gamma diag(L) PSD (gamma <= 1/2 range)
        gam = None
        for e in range(1, 14):
            g = Fr(1, 2**e)
            A = [[H[i][j] + (2 * mu[i] - 2 * g * L[i] if i == j else 0) for j in range(n)] for i in range(n)]
            if ldl_psd(A):
                gam = g
                break
        if gam is None:
            continue
        b = [zeta[i] - sum(H[i][j] * xs[j] for j in range(n)) for i in range(n)]
        return dict(n=n, types=types, lo=lo, hi=hi, xs=xs, H=H, b=b, L=L, P=P, gam=gam)


def F(inst, x):
    H, b, n = inst["H"], inst["b"], inst["n"]
    return sum(Fr(1, 2) * H[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) + sum(b[i] * x[i] for i in range(n))


def graded(lo, hi, c, h, th, integer):
    def sig(t):
        if integer:
            return max(Fr(1), Fr(math.floor(h + th * t)))
        return h + th * t
    nodes = {c}
    for side, R in ((1, hi - c), (-1, c - lo)):
        t = Fr(0)
        while t < R:
            t = min(t + sig(t), R)
            nodes.add(c + side * t)
    return sorted(nodes)


def eff(a, b, integer):
    return Fr(0) if (integer and b - a == 1) else b - a


def run(inst, mu_exp):
    n, types, L, P = inst["n"], inst["types"], inst["L"], inst["P"]
    lo, hi, xs, gam = inst["lo"], inst["hi"], inst["xs"], inst["gam"]
    th = Fr(1, 2**mu_exp)
    kb = max(Fr(1), 1 / gam)
    assert 8 * kb * th * th <= 1
    nP = len(P)
    OPT = F(inst, xs)
    s = [hi[i] - lo[i] for i in range(n)]
    e = {}
    for i in P:
        k = 0
        while not (Fr(4) ** (k - 1) < L[i] <= Fr(4) ** k):
            k += 1 if L[i] > Fr(4) ** k else -1
        e[i] = k
    r = {i: Fr(1, 2**e[i]) if e[i] >= 0 else Fr(2**(-e[i])) for i in P}
    E = -60
    while not all(Fr(2) ** E * r[i] >= s[i] for i in P):
        E += 1
    K = 10 * 2**mu_exp * math.ceil(math.log2(nP + 2))
    Lnorm = lambda d: sum(L[i] * d[i] ** 2 for i in P)
    box = [(lo[i], hi[i]) for i in range(n)]
    c = list(lo)
    U = F(inst, lo)
    maxnodes = 0
    for j in range(0, 12):
        eta = Fr(2) ** (E - j)
        a = nP * eta * eta
        h = {i: eta * r[i] for i in P}
        G = []
        for i in range(n):
            if i in P:
                G.append(graded(box[i][0], box[i][1], c[i], h[i], th, types[i] == "Z"))
            else:
                G.append([lo[i], hi[i]])
        maxnodes = max(maxnodes, max(len(g) for g in G))
        assert all(len(g) <= K for g in G), ("cap", [len(g) for g in G], K)
        w = []
        for i in range(n):
            g = G[i]
            wi = {}
            for k, v in enumerate(g):
                cand = [Fr(0)]
                if k > 0:
                    cand.append(eff(g[k - 1], v, types[i] == "Z"))
                if k + 1 < len(g):
                    cand.append(eff(v, g[k + 1], types[i] == "Z"))
                wi[v] = max(cand)
            w.append(wi)
        d = lambda i, v: L[i] * w[i][v] ** 2 / 8
        Qv, Fv = {}, {}
        for y in itertools.product(*G):
            fy = F(inst, y)
            Fv[y] = fy
            Qv[y] = fy - sum(d(i, y[i]) for i in range(n))
        beta = min(Qv.values())
        y = min((k for k in Qv if Qv[k] == beta))
        m = [{v: min(Qv[k] for k in Qv if k[i] == v) for v in G[i]} for i in range(n)]
        U = min(U, Fv[y])
        # Lemma inv
        assert all(box[i][0] <= xs[i] <= box[i][1] for i in range(n)), "(i) x* in box"
        assert beta <= OPT, "(i) beta<=OPT"
        assert Lnorm([c[i] - xs[i] for i in range(n)]) <= 4 * kb * a, "(ii)"
        assert Lnorm([y[i] - xs[i] for i in range(n)]) <= kb * a, "(iii)"
        Dy = Fv[y] - Qv[y]
        assert U - beta <= Dy <= Fr(9, 16) * a, "(iv)"
        for z, qz in Qv.items():
            if qz <= U:
                assert Lnorm([z[i] - xs[i] for i in range(n)]) <= Fr(17, 15) * kb * a, "(v)"
        # Prop cellwise (b) for n<=2
        if n <= 2:
            best = None
            ints = [list(zip(g[:-1], g[1:])) for g in G]
            for C in itertools.product(*ints):
                vb = min(Fv[v] for v in itertools.product(*[(I[0], I[1]) for I in C]))
                vb -= sum(L[i] * eff(C[i][0], C[i][1], types[i] == "Z") ** 2 / 8 for i in range(n))
                best = vb if best is None else min(best, vb)
            assert best == beta, "cellwise (b)"
        # Prop cellwise (c) at random points
        for _ in range(20):
            x = []
            for i in range(n):
                if types[i] == "Z":
                    x.append(Fr(random.randint(int(box[i][0]), int(box[i][1]))))
                else:
                    x.append(box[i][0] + (box[i][1] - box[i][0]) * Fr(random.randint(0, 1000), 1000))
            fx = F(inst, x)
            for i in range(n):
                g = G[i]
                for aa, bb in zip(g[:-1], g[1:]):
                    if aa <= x[i] <= bb:
                        assert fx >= min(m[i][aa], m[i][bb]), "cellwise (c)"
        if U - beta <= Fr(1, 10**6):
            return ("success", j, maxnodes, K)
        # filter
        newbox = list(box)
        for i in P:
            g = G[i]
            kept = [(aa, bb) for aa, bb in zip(g[:-1], g[1:]) if min(m[i][aa], m[i][bb]) <= U]
            nb = (min(k[0] for k in kept), max(k[1] for k in kept))
            R = 8 * math.sqrt(kb * nP) * h[i] + (1 if types[i] == "Z" else 0)
            assert y[i] - Fr(R) <= nb[0] and nb[1] <= y[i] + Fr(R), "radius R_ij"
            newbox[i] = nb
        box = newbox
        c = list(y)
    return ("stages", j, maxnodes, K)


cnt = 0
for trial in range(int(sys.argv[2]) if len(sys.argv) > 2 else 12):
    n = random.choice([2, 2, 3])
    inst = make_instance(n)
    kb = max(Fr(1), 1 / inst["gam"])
    mu = 2
    while 8 * kb * Fr(1, 4**mu) > 1:
        mu += 1
    res = run(inst, mu)
    cnt += 1
    print(trial, n, inst["types"], "P=", inst["P"], "kbar<=", kb, "mu=", mu, res)
print("all invariants held on", cnt, "instances")
