"""recB second verification pass (exact Fractions).

1. Work count of Thm balanced(b): replacing every infinite capacity of the
   network of Lemma chaincut by 1 + (sum of finite capacities) changes neither
   the minimum cut value nor the set of minimum cuts (brute force over cuts).
2. Bit claim of the work count: with grid nodes of denominators dividing
   Gamma_X 2^alpha and chi_i = -d_i, d_i(v) = L_i w_i(v)^2/8, every capacity
   has a denominator dividing 8 Gamma_F Gamma_X^2 4^alpha.
3. Cor core: for F balanced only outside a supplied core, beta and every
   min-marginal of Q = F - D, computed as minima over core node vectors of
   Lemma chaincut problems, equal brute force.
"""
from fractions import Fraction as Fr
import itertools, random
from math import lcm, prod

random.seed(20261003)


def rnd(den=(1, 2, 3, 4)):
    return Fr(random.randint(-9, 9), random.choice(den))


def Fval(H, b, c, x):
    n = len(x)
    return (Fr(1, 2) * sum(H[i][j] * x[i] * x[j] for i in range(n) for j in range(n))
            + sum(b[i] * x[i] for i in range(n)) + c)


def network(H, b, c, G, chi, o):
    """Network of Lemma chaincut (proof in App. D); returns Phi0 + sum min(0,rho), nodes, arcs."""
    n = len(G)
    a = [sorted(G[i]) if o[i] == 1 else sorted(G[i], reverse=True) for i in range(n)]
    nodes = [(i, l) for i in range(n) for l in range(1, len(a[i]))]
    idx = {p: t for t, p in enumerate(nodes)}
    m = len(nodes)

    def phi_i(i, t):
        return Fr(1, 2) * H[i][i] * t * t + b[i] * t + chi[i][t]

    Phi0 = (c + sum(phi_i(i, a[i][0]) for i in range(n))
            + sum(H[i][j] * a[i][0] * a[j][0] for i in range(n) for j in range(i + 1, n)))
    mu = [Fr(0)] * m
    om = {}
    for (i, l) in nodes:
        d = a[i][l] - a[i][l - 1]
        mu[idx[(i, l)]] += (phi_i(i, a[i][l]) - phi_i(i, a[i][l - 1])
                            + sum(H[i][j] * d * a[j][0] for j in range(n) if j != i))
    for (i, l) in nodes:
        for (j, lp) in nodes:
            if i < j:
                om[(idx[(i, l)], idx[(j, lp)])] = H[i][j] * (a[i][l] - a[i][l - 1]) * (a[j][lp] - a[j][lp - 1])
    assert all(v <= 0 for v in om.values())

    def w(p, q):
        return om.get((min(p, q), max(p, q)), Fr(0))

    rho = [mu[p] + Fr(1, 2) * sum(w(p, q) for q in range(m) if q != p) for p in range(m)]
    arcs = {}
    for p in range(m):
        arcs[(p, 't')] = max(rho[p], 0)
        arcs[('s', p)] = max(-rho[p], 0)
    for (p, q), val in om.items():
        if val != 0:
            arcs[(p, q)] = -val / 2
            arcs[(q, p)] = -val / 2
    for (i, l) in nodes:
        if (i, l + 1) in idx:
            arcs[(idx[(i, l + 1)], idx[(i, l)])] = None  # infinite
    return Phi0 + sum(min(0, r) for r in rho), m, arcs, a, idx


def cut_caps(m, arcs, big):
    """All s-t cuts by brute force; capacity with infinite arcs = big (or None = infinite)."""
    res = {}
    for z in itertools.product([0, 1], repeat=m):
        S = {'s'} | {p for p in range(m) if z[p]}
        cap = Fr(0)
        inf = False
        for (u, v), cc in arcs.items():
            if u in S and v not in S:
                if cc is None:
                    if big is None:
                        inf = True
                    else:
                        cap += big
                else:
                    cap += cc
        res[z] = None if inf else cap
    return res


# 1. infinite capacities -> 1 + sum of finite capacities
for trial in range(150):
    n = random.randint(1, 3)
    o = [random.choice([-1, 1]) for _ in range(n)]
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = rnd()
        for j in range(i + 1, n):
            H[i][j] = H[j][i] = (-abs(rnd()) * o[i] * o[j]) if random.random() < .8 else Fr(0)
    b = [rnd() for _ in range(n)]
    c = rnd()
    G = [sorted(set(Fr(random.randint(-6, 6), random.choice([1, 2])) for _ in range(random.randint(1, 4))))
         for _ in range(n)]
    chi = [{t: rnd() for t in G[i]} for i in range(n)]
    base, m, arcs, a, idx = network(H, b, c, G, chi, o)
    if m > 9:
        continue
    finite_sum = sum(cc for cc in arcs.values() if cc is not None)
    big = 1 + finite_sum
    exact = cut_caps(m, arcs, None)
    repl = cut_caps(m, arcs, big)
    fin = [v for v in exact.values() if v is not None]
    mn = min(fin)
    assert min(repl.values()) == mn
    assert {z for z, v in exact.items() if v == mn} == {z for z, v in repl.items() if v == mn}
    # min cut value + base = brute-force minimum of F_chi
    brute = min(Fval(H, b, c, list(y)) + sum(chi[i][y[i]] for i in range(n)) for y in itertools.product(*G))
    assert base + mn == brute
print("work count: infinite arcs -> 1 + sum of finite capacities keeps min cuts and value (150 instances)")

# 2. common denominator of the capacities
for trial in range(120):
    n = random.randint(1, 4)
    o = [random.choice([-1, 1]) for _ in range(n)]
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = rnd((1, 3, 5))
        for j in range(i + 1, n):
            H[i][j] = H[j][i] = (-abs(rnd((1, 3, 7))) * o[i] * o[j]) if random.random() < .8 else Fr(0)
    b = [rnd((1, 2, 5)) for _ in range(n)]
    c = rnd()
    coef = [H[i][i] / 2 for i in range(n)] + [H[i][j] for i in range(n) for j in range(i + 1, n)] + b + [c]
    GammaF = prod(x.denominator for x in coef)
    lo = [Fr(random.randint(-5, 0), random.choice([1, 3, 7])) for _ in range(n)]
    up = [lo[i] + Fr(random.randint(1, 5), random.choice([1, 2, 3])) for i in range(n)]
    GammaX = prod(x.denominator for x in lo + up)
    alpha = random.randint(0, 4)
    D = GammaX * 2 ** alpha
    G = []
    for i in range(n):
        pts = {lo[i], up[i]}
        A, B = lo[i] * D, up[i] * D
        assert A.denominator == 1 and B.denominator == 1
        for _ in range(random.randint(0, 3)):
            pts.add(Fr(random.randint(int(A), int(B)), D))
        G.append(sorted(pts))
    L = [max(H[i][i], 0) for i in range(n)]

    def d(i, v):
        g = G[i]
        k = g.index(v)
        ws = []
        if k > 0:
            ws.append(g[k] - g[k - 1])
        if k + 1 < len(g):
            ws.append(g[k + 1] - g[k])
        wv = max(ws) if ws else Fr(0)
        return L[i] * wv * wv / 8

    chi = [{v: -d(i, v) for v in G[i]} for i in range(n)]
    base, m, arcs, a, idx = network(H, b, c, G, chi, o)
    den = 8 * GammaF * GammaX ** 2 * 4 ** alpha
    for cc in arcs.values():
        if cc is not None:
            assert (cc * den).denominator == 1, (cc, den)
print("work count: capacities with chi_i = -d_i have a common denominator dividing 8 Gamma_F Gamma_X^2 4^alpha (120 instances)")


# 3. Cor core: enumeration over core nodes + Lemma chaincut = brute force
def chaincut_value(H, b, c, G, chi, o):
    base, m, arcs, a, idx = network(H, b, c, G, chi, o)
    caps = cut_caps(m, arcs, None)
    return base + min(v for v in caps.values() if v is not None)


for trial in range(60):
    k = random.randint(1, 2)
    r = random.randint(1, 3)
    n = k + r
    o = [random.choice([-1, 1]) for _ in range(r)]
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = rnd()
        for j in range(i + 1, n):
            h = rnd()
            if i >= k and j >= k:
                h = -abs(h) * o[i - k] * o[j - k]
            H[i][j] = H[j][i] = h
    b = [rnd() for _ in range(n)]
    c = rnd()
    G = [sorted(set(Fr(random.randint(-4, 4), random.choice([1, 2])) for _ in range(random.randint(1, 3))))
         for _ in range(n)]
    chi = [{t: rnd() for t in G[i]} for i in range(n)]  # plays -d_i

    def Q(y):
        return Fval(H, b, c, list(y)) + sum(chi[i][y[i]] for i in range(n))

    def via_core(Gfix):
        best = None
        for vK in itertools.product(*Gfix[:k]):
            # residual quadratic: H_RR, linear b_R + H_RK vK, constant
            HR = [[H[k + i][k + j] for j in range(r)] for i in range(r)]
            bR = [b[k + i] + sum(H[k + i][j] * vK[j] for j in range(k)) for i in range(r)]
            cR = (c + Fr(1, 2) * sum(H[i][j] * vK[i] * vK[j] for i in range(k) for j in range(k))
                  + sum(b[i] * vK[i] for i in range(k)) + sum(chi[i][vK[i]] for i in range(k)))
            val = chaincut_value(HR, bR, cR, Gfix[k:], chi[k:], o)
            best = val if best is None else min(best, val)
        return best

    if sum(len(g) - 1 for g in G[k:]) > 9:
        continue
    assert via_core(G) == min(Q(y) for y in itertools.product(*G))
    for i in range(n):
        for v in G[i]:
            G2 = [g if t != i else [v] for t, g in enumerate(G)]
            assert via_core(G2) == min(Q(y) for y in itertools.product(*G2))
print("cor:core: beta and all min-marginals via core enumeration + chaincut = brute force (60 instances)")
print("ALL OK")
