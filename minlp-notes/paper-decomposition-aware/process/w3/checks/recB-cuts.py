"""recB checks: Prop cr-cut (a),(b), Lemma chaincut, Lemma balance (exact arithmetic)."""
from fractions import Fraction as Fr
import itertools, random
random.seed(7)

INF = None

def maxflow(nodes, arcs, s, t):
    # Edmonds-Karp on Fractions; arcs: dict (u,v)->cap (cap None = infinite)
    cap = {}
    adj = {u: set() for u in nodes}
    for (u, v), c in arcs.items():
        cap[(u, v)] = cap.get((u, v), Fr(0)) + (Fr(10**18) if c is None else c)
        cap.setdefault((v, u), Fr(0))
        adj[u].add(v); adj[v].add(u)
    flow = Fr(0)
    while True:
        par = {s: None}; q = [s]
        for u in q:
            for v in adj[u]:
                if v not in par and cap[(u, v)] > 0:
                    par[v] = u; q.append(v)
        if t not in par: break
        b = None; v = t
        while par[v] is not None:
            u = par[v]; b = cap[(u, v)] if b is None else min(b, cap[(u, v)]); v = u
        v = t
        while par[v] is not None:
            u = par[v]; cap[(u, v)] -= b; cap[(v, u)] += b; v = u
        flow += b
    return flow

def rnd(): return Fr(random.randint(-9, 9), random.randint(1, 4))

# (a) general identity eq:cr-cutid
for trial in range(200):
    m = random.randint(1, 5)
    Phi0 = rnd(); mu = [rnd() for _ in range(m)]
    om = {(i, j): -abs(rnd()) if random.random() < .7 else Fr(0) for i in range(m) for j in range(i+1, m)}
    w = lambda i, j: om[(min(i, j), max(i, j))]
    rho = [mu[i] + Fr(1, 2)*sum(w(i, j) for j in range(m) if j != i) for i in range(m)]
    arcs = {}
    for i in range(m):
        arcs[(i, 't')] = max(rho[i], 0); arcs[('s', i)] = max(-rho[i], 0)
    for (i, j), o in om.items():
        if o != 0: arcs[(i, j)] = -o/2; arcs[(j, i)] = -o/2
    best = None
    for z in itertools.product([0, 1], repeat=m):
        val = Phi0 + sum(mu[i]*z[i] for i in range(m)) + sum(o*z[i]*z[j] for (i, j), o in om.items())
        S = {'s'} | {i for i in range(m) if z[i]}
        capS = sum(c for (u, v), c in arcs.items() if u in S and v not in S)
        assert val == Phi0 + sum(min(0, r) for r in rho) + capS
        best = val if best is None else min(best, val)
    f = maxflow(list(range(m)) + ['s', 't'], arcs, 's', 't')
    assert best == Phi0 + sum(min(0, r) for r in rho) + f
print("prop:cr-cut(a): 200 random instances OK")

# (b) expansion of F(v, y(z)) under (R1)-(R2): check omega = H_ij delta_i delta_j and min over box = min over endpoints
def F(H, b, c, x):
    n = len(x)
    return Fr(1, 2)*sum(H[i][j]*x[i]*x[j] for i in range(n) for j in range(n)) + sum(b[i]*x[i] for i in range(n)) + c
for trial in range(100):
    k = random.randint(0, 2); r = random.randint(1, 4); n = k + r
    o = [random.choice([-1, 1]) for _ in range(r)]
    H = [[Fr(0)]*n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if i == j:
                H[i][i] = -abs(rnd()) if i >= k else rnd()
            else:
                h = rnd()
                if i >= k and j >= k:
                    h = -abs(h) * o[i-k]*o[j-k]
                H[i][j] = H[j][i] = h
    b = [rnd() for _ in range(n)]; c = rnd()
    lo = [Fr(random.randint(-3, 0)) for _ in range(r)]; up = [lo[i] + Fr(random.randint(0, 3), random.choice([1, 2])) for i in range(r)]
    v = [rnd() for _ in range(k)]
    al = [lo[i] if o[i] == 1 else up[i] for i in range(r)]
    de = [(up[i]-lo[i])*o[i] for i in range(r)]
    for i in range(r):
        for j in range(i+1, r):
            assert H[k+i][k+j]*de[i]*de[j] <= 0
    vals = {z: F(H, b, c, v + [al[i]+de[i]*z[i] for i in range(r)]) for z in itertools.product([0, 1], repeat=r)}
    # quadratic form check: second differences equal omega
    for i in range(r):
        for j in range(i+1, r):
            e = lambda a, bb: tuple(1 if t == i and a else 1 if t == j and bb else 0 for t in range(r))
            om = vals[e(1, 1)] - vals[e(1, 0)] - vals[e(0, 1)] + vals[e(0, 0)]
            assert om == H[k+i][k+j]*de[i]*de[j]
    # grid search on box: endpoint min <= sampled interior values
    m_end = min(vals.values())
    for _ in range(30):
        y = [lo[i] + (up[i]-lo[i])*Fr(random.randint(0, 8), 8) for i in range(r)]
        assert F(H, b, c, v + y) >= m_end
print("prop:cr-cut(b), lem:cr-endpoint: 100 random instances OK")

# Lemma chaincut: threshold encoding with infinite arcs vs brute force, arbitrary chi
def chaincut_min(H, b, c, G, chi, o):
    n = len(G)
    a = [sorted(G[i]) if o[i] == 1 else sorted(G[i], reverse=True) for i in range(n)]
    nodes = [(i, l) for i in range(n) for l in range(1, len(a[i]))]
    idx = {p: t for t, p in enumerate(nodes)}
    m = len(nodes)
    # build Phi(z) coefficients by evaluating the encoded function on monotone vectors via formulas
    def phi_i(i, t): return Fr(1, 2)*H[i][i]*t*t + b[i]*t + chi[i][t]
    Phi0 = c + sum(phi_i(i, a[i][0]) for i in range(n)) + sum(H[i][j]*a[i][0]*a[j][0] for i in range(n) for j in range(i+1, n))
    mu = [Fr(0)]*m; om = {}
    for (i, l) in nodes:
        d = a[i][l]-a[i][l-1]
        mu[idx[(i, l)]] += phi_i(i, a[i][l]) - phi_i(i, a[i][l-1]) + sum(H[i][j]*d*a[j][0] for j in range(n) if j != i)
    for (i, l) in nodes:
        for (j, lp) in nodes:
            if i < j:
                om[(idx[(i, l)], idx[(j, lp)])] = H[i][j]*(a[i][l]-a[i][l-1])*(a[j][lp]-a[j][lp-1])
    for v in om.values(): assert v <= 0
    w = lambda p, q: om.get((min(p, q), max(p, q)), Fr(0))
    rho = [mu[p] + Fr(1, 2)*sum(w(p, q) for q in range(m) if q != p) for p in range(m)]
    arcs = {}
    for p in range(m):
        arcs[(p, 't')] = max(rho[p], 0); arcs[('s', p)] = max(-rho[p], 0)
    for (p, q), val in om.items():
        if val != 0: arcs[(p, q)] = -val/2; arcs[(q, p)] = -val/2
    for (i, l) in nodes:
        if (i, l+1) in idx: arcs[(idx[(i, l+1)], idx[(i, l)])] = None
    f = maxflow(list(range(m)) + ['s', 't'], arcs, 's', 't')
    narcs = len([1 for kk, vv in arcs.items()])
    return Phi0 + sum(min(0, r) for r in rho) + f, m + 2, narcs

for trial in range(80):
    n = random.randint(1, 4)
    o = [random.choice([-1, 1]) for _ in range(n)]
    H = [[Fr(0)]*n for _ in range(n)]
    for i in range(n):
        H[i][i] = rnd()
        for j in range(i+1, n):
            h = -abs(rnd())*o[i]*o[j] if random.random() < .8 else Fr(0)
            H[i][j] = H[j][i] = h
    b = [rnd() for _ in range(n)]; c = rnd()
    G = [sorted(set(Fr(random.randint(-6, 6), random.choice([1, 2, 3])) for _ in range(random.randint(1, 4)))) for _ in range(n)]
    chi = [{t: rnd() for t in G[i]} for i in range(n)]
    brute = min(F(H, b, c, list(y)) + sum(chi[i][y[i]] for i in range(n)) for y in itertools.product(*G))
    val, nn, na = chaincut_min(H, b, c, G, chi, o)
    assert val == brute, (val, brute)
    ks = [len(g)-1 for g in G]
    assert nn == sum(ks)+2
    assert na <= 3*sum(ks) + 2*sum(ks[i]*ks[j] for i in range(n) for j in range(i+1, n) if H[i][j] != 0)
    # min-marginal: fix coordinate 0 at each node
    for v in G[0]:
        G2 = [[v]] + G[1:]
        brute2 = min(F(H, b, c, list(y)) + sum(chi[i][y[i]] for i in range(n)) for y in itertools.product(*G2))
        assert chaincut_min(H, b, c, G2, chi, o)[0] == brute2
print("lem:chaincut: 80 random balanced instances with min-marginals OK")

# Lemma balance: BFS sign test vs brute force
def bfs_signs(H):
    m = len(H); o = [0]*m
    for r0 in range(m):
        if o[r0]: continue
        o[r0] = 1; q = [r0]
        for u in q:
            for v in range(m):
                if v != u and H[u][v] != 0:
                    want = o[u] if H[u][v] < 0 else -o[u]
                    if o[v] == 0: o[v] = want; q.append(v)
                    elif o[v] != want: return None
    return o
for trial in range(300):
    m = random.randint(1, 5)
    H = [[Fr(0)]*m for _ in range(m)]
    for i in range(m):
        for j in range(i+1, m):
            H[i][j] = H[j][i] = Fr(random.choice([-1, 0, 0, 1]))
    ex = any(all(s[i]*s[j]*H[i][j] <= 0 for i in range(m) for j in range(m) if i != j) for s in itertools.product([-1, 1], repeat=m))
    o = bfs_signs(H)
    assert (o is not None) == ex
    if o: assert all(o[i]*o[j]*H[i][j] <= 0 for i in range(m) for j in range(m) if i != j)
print("lem:balance: 300 random sign patterns OK")
