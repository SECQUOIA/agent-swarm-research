"""M-recourse checks for Sections 7.4-7.5 and Appendix D (exact arithmetic).

Checks: prop:cr-cut identity and min cut = brute force; lem:chaincut on random
balanced quadratics with random grids and unary terms; CORE (alg:core) with
thm:cr-search (b),(c),(d); lem:cr-height denominators; thm:cr-exact pipeline;
prop:cr-submod submodularity with a convex part.
"""
from fractions import Fraction as Fr
from collections import deque
import itertools, random, math

random.seed(77)
ok = True


def report(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok &= bool(cond)


def rnd(lo=-4, hi=4, den=(1, 2, 4)):
    return Fr(random.randint(lo * 4, hi * 4), 4) / random.choice(den)


# ---------- max flow (Edmonds-Karp) ----------
def maxflow(n, arcs, s, t):
    cap = {}
    adj = [set() for _ in range(n)]
    for (a, b, c) in arcs:
        cap[(a, b)] = cap.get((a, b), 0) + c
        cap.setdefault((b, a), 0)
        adj[a].add(b); adj[b].add(a)
    flow = 0
    while True:
        par = {s: None}
        dq = deque([s])
        while dq and t not in par:
            u = dq.popleft()
            for v in adj[u]:
                if v not in par and cap[(u, v)] > 0:
                    par[v] = u; dq.append(v)
        if t not in par:
            break
        path = []; v = t
        while par[v] is not None:
            path.append((par[v], v)); v = par[v]
        f = min(cap[e] for e in path)
        for (a, b) in path:
            cap[(a, b)] -= f; cap[(b, a)] += f
        flow += f
    # source side of min cut
    S = set(par.keys())
    return flow, S


# ---------- prop:cr-cut (a) ----------
def cut_network(Phi0, mu, om):
    m = len(mu)
    rho = [mu[i] + Fr(1, 2) * sum(om.get((min(i, j), max(i, j)), 0) for j in range(m) if j != i) for i in range(m)]
    s, t = m, m + 1
    arcs = []
    for i in range(m):
        arcs.append((i, t, max(rho[i], 0)))
        arcs.append((s, i, max(-rho[i], 0)))
    for (i, j), w in om.items():
        if w != 0:
            arcs.append((i, j, -w / 2)); arcs.append((j, i, -w / 2))
    const = Phi0 + sum(min(0, r) for r in rho)
    return arcs, const, s, t


def capS(arcs, S):
    return sum(c for (a, b, c) in arcs if a in S and b not in S)


good = True
for trial in range(200):
    m = random.randint(1, 5)
    Phi0 = rnd(); mu = [rnd() for _ in range(m)]
    om = {(i, j): -abs(rnd()) for i in range(m) for j in range(i + 1, m) if random.random() < 0.6}
    Phi = lambda z: Phi0 + sum(mu[i] * z[i] for i in range(m)) + sum(w * z[i] * z[j] for (i, j), w in om.items())
    arcs, const, s, t = cut_network(Phi0, mu, om)
    for z in itertools.product((0, 1), repeat=m):
        S = {s} | {i for i in range(m) if z[i]}
        if Phi(z) != const + capS(arcs, S):
            good = False
    fl, S = maxflow(m + 2, arcs, s, t)
    zb = min(itertools.product((0, 1), repeat=m), key=Phi)
    if const + fl != Phi(zb) or const + capS(arcs, S) != Phi(zb):
        good = False
report("prop:cr-cut(a): identity on all labels, max flow = min Phi (200 instances)", good)


# ---------- lem:chaincut ----------
def chaincut(H, b, c, o, G, chi):
    n = len(G)
    order = [sorted(G[i]) if o[i] == 1 else sorted(G[i], reverse=True) for i in range(n)]
    idx = {}  # (i,l) -> node id, l=1..k_i
    for i in range(n):
        for l in range(1, len(order[i])):
            idx[(i, l)] = len(idx)
    N = len(idx)
    Phi0 = c
    mu = [Fr(0)] * N
    om = {}
    delta = {(i, l): order[i][l] - order[i][l - 1] for (i, l) in idx}
    for i in range(n):
        phi = lambda tt, i=i: Fr(1, 2) * H[i][i] * tt * tt + b[i] * tt + chi[i][tt]
        Phi0 += phi(order[i][0])
        for l in range(1, len(order[i])):
            mu[idx[(i, l)]] += phi(order[i][l]) - phi(order[i][l - 1])
    for i in range(n):
        for j in range(i + 1, n):
            if H[i][j] == 0:
                continue
            a0, b0 = order[i][0], order[j][0]
            Phi0 += H[i][j] * a0 * b0
            for l in range(1, len(order[i])):
                mu[idx[(i, l)]] += H[i][j] * delta[(i, l)] * b0
            for l in range(1, len(order[j])):
                mu[idx[(j, l)]] += H[i][j] * delta[(j, l)] * a0
            for l in range(1, len(order[i])):
                for l2 in range(1, len(order[j])):
                    p, q = sorted((idx[(i, l)], idx[(j, l2)]))
                    om[(p, q)] = om.get((p, q), 0) + H[i][j] * delta[(i, l)] * delta[(j, l2)]
    if any(w > 0 for w in om.values()):
        return None
    arcs, const, s, t = cut_network(Phi0, mu, om)
    big = 1 + sum(a[2] for a in arcs)
    ninf = 0
    for i in range(n):
        for l in range(1, len(order[i]) - 1):
            arcs.append((idx[(i, l + 1)], idx[(i, l)], big)); ninf += 1
    fl, S = maxflow(N + 2, arcs, s, t)
    # decode
    y = []
    for i in range(n):
        l = 0
        while (i, l + 1) in idx and idx[(i, l + 1)] in S:
            l += 1
        y.append(order[i][l])
    narcs_bound = 3 * sum(len(g) - 1 for g in G) + 2 * sum((len(G[i]) - 1) * (len(G[j]) - 1) for i in range(n) for j in range(i + 1, n) if H[i][j] != 0)
    narcs = sum(1 for a in arcs)  # includes zero-capacity arcs
    return const + fl, y, narcs <= narcs_bound


good = True; cnt = 0
for trial in range(150):
    n = random.randint(1, 4)
    o = [random.choice((1, -1)) for _ in range(n)]
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = rnd()
        for j in range(i + 1, n):
            if random.random() < 0.7:
                v = -o[i] * o[j] * abs(rnd())
                H[i][j] = H[j][i] = v
    b = [rnd() for _ in range(n)]; c = rnd()
    G = [sorted(set(rnd(-2, 2) for _ in range(random.randint(1, 4)))) for _ in range(n)]
    chi = [{g: rnd() for g in G[i]} for i in range(n)]
    F = lambda y: Fr(1, 2) * sum(H[i][j] * y[i] * y[j] for i in range(n) for j in range(n)) + sum(b[i] * y[i] for i in range(n)) + c + sum(chi[i][y[i]] for i in range(n))
    bf = min(F(y) for y in itertools.product(*G))
    r = chaincut(H, b, c, o, G, chi)
    if r is None:
        good = False; continue
    val, y, arcok = r
    cnt += 1
    if val != bf or F(y) != bf or not arcok:
        good = False
report(f"lem:chaincut: min cut value and decoded minimizer = brute force, arc bound ({cnt} instances)", good)


# ---------- random instances of the cut-residual class ----------
def make_instance(k, r, nint):
    n = k + r
    K = list(range(k)); R = list(range(k, n))
    o = {i: random.choice((1, -1)) for i in R}
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if i in R and j in R:
                v = -abs(rnd()) if i == j else -o[i] * o[j] * abs(rnd())
            else:
                v = rnd()
                if i == j and i in K:
                    v = abs(rnd(0, 3)) * random.choice((1, 1, -1))
            H[i][j] = H[j][i] = v
    b = [rnd() for _ in range(n)]; c = rnd()
    lo = {}; hi = {}
    isint = {}
    for t, i in enumerate(R):
        if t < nint:
            a = random.randint(-2, 1); lo[i] = Fr(a); hi[i] = Fr(a + random.randint(1, 2)); isint[i] = True
        else:
            a = rnd(-2, 1, (2, 4)); lo[i] = a; hi[i] = a + Fr(random.randint(1, 4), random.choice((1, 2))); isint[i] = False
    return dict(n=n, k=k, K=K, R=R, H=H, b=b, c=c, lo=lo, hi=hi, isint=isint)


def Fval(I, x):
    n = I['n']; H = I['H']
    return Fr(1, 2) * sum(H[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) + sum(I['b'][i] * x[i] for i in range(n)) + I['c']


def oracle(I, v):
    """exact V(v) and endpoint minimizer, by enumeration of endpoint vectors."""
    best = None
    for ys in itertools.product(*[(I['lo'][i], I['hi'][i]) for i in I['R']]):
        x = list(v) + list(ys)
        f = Fval(I, x)
        if best is None or f < best[0]:
            best = (f, tuple(ys))
    return best


def solve_face_min(I, y):
    """min over [0,1]^k of F(.,y) by face enumeration (k<=2)."""
    k = I['k']; H = I['H']
    best = None
    for pat in itertools.product((0, 1, 2), repeat=k):
        free = [i for i in range(k) if pat[i] == 2]
        v = [Fr(pat[i]) if pat[i] < 2 else None for i in range(k)]
        if free:
            # grad_i = sum_j H_ij x_j + b_i = 0, i in free
            A = [[H[i][j] for j in free] for i in free]
            rhs = [-(I['b'][i] + sum(H[i][j] * (v[j] if j < k else y[j - k]) for j in range(I['n']) if j not in free)) for i in free]
            if len(free) == 1:
                if A[0][0] == 0: continue
                sol = [rhs[0] / A[0][0]]
            else:
                det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
                if det == 0: continue
                sol = [(rhs[0] * A[1][1] - rhs[1] * A[0][1]) / det, (A[0][0] * rhs[1] - A[1][0] * rhs[0]) / det]
            for t, i in enumerate(free):
                v[i] = sol[t]
            if not all(0 <= v[i] <= 1 for i in free):
                continue
        f = Fval(I, list(v) + list(y))
        if best is None or f < best[0]:
            best = (f, tuple(v))
    return best


def core_search(I, L, eps, J):
    k = I['k']
    cells = [(0,) * k]  # integer index at level j: cell = prod [a h, (a+1) h]
    queried = {}
    U = None; inc = None
    trace = []
    for j in range(J + 1):
        h = Fr(1, 2 ** j)
        ej = k * L * h * h / 8
        for cidx in cells:
            for cor in itertools.product((0, 1), repeat=k):
                v = tuple(h * (cidx[i] + cor[i]) for i in range(k))
                if v not in queried:
                    queried[v] = oracle(I, v)
                    if U is None or queried[v][0] < U:
                        U = queried[v][0]; inc = (v, queried[v][1])
        beta = {cidx: min(queried[tuple(h * (cidx[i] + cor[i]) for i in range(k))][0] for cor in itertools.product((0, 1), repeat=k)) - ej for cidx in cells}
        lam = min(beta.values())
        kept = [cidx for cidx in cells if beta[cidx] <= U]
        trace.append(dict(j=j, h=h, ej=ej, cells=list(cells), beta=beta, U=U, lam=lam, kept=kept))
        if U - min(lam, U) <= eps:
            break
        cells = [tuple(2 * cidx[i] + ch[i] for i in range(k)) for cidx in kept for ch in itertools.product((0, 1), repeat=k)]
    return inc, U, min(lam, U), trace, len(queried)


def global_opt(I):
    """OPT via enumeration over endpoint vectors and exact face minimization."""
    best = None
    for ys in itertools.product(*[(I['lo'][i], I['hi'][i]) for i in I['R']]):
        r = solve_face_min(I, ys)
        if best is None or r[0] < best[0]:
            best = (r[0], r[1], ys)
    return best


def lcm(a, b):
    return a * b // math.gcd(a, b)


def omega_K(I):
    k = I['k']; H = I['H']
    coeffs = [I['c']] + I['b'] + [H[i][i] / 2 for i in range(I['n'])] + [H[i][j] for i in range(I['n']) for j in range(i + 1, I['n'])]
    Lc = 1
    for q in coeffs:
        Lc = lcm(Lc, q.denominator)
    Le = 1
    for i in I['R']:
        Le = lcm(Le, I['lo'][i].denominator); Le = lcm(Le, I['hi'][i].denominator)
    D = Lc * Le * Le
    R = D
    for i in range(k):
        if H[i][i] > 0:
            R *= D * H[i][i]
    assert R.denominator == 1 if isinstance(R, Fr) else True
    return D, int(D * R * R)


good_b = good_c = good_d = good_h = good_x = True
ninst = 0
for trial in range(60):
    k = random.choice((1, 1, 2))
    I = make_instance(k, random.randint(1, 4), random.randint(0, 1))
    L = max([Fr(0)] + [I['H'][i][i] for i in range(k)])
    opt, vopt, yopt = global_opt(I)
    D, Om = omega_K(I)
    # lem:cr-height: every Psi(y) and OPT have reduced denominators <= Om
    for ys in itertools.product(*[(I['lo'][i], I['hi'][i]) for i in I['R']]):
        if solve_face_min(I, ys)[0].denominator > Om:
            good_h = False
    if opt.denominator > Om:
        good_h = False
    # CORE with modest accuracy: check (b),(c),(d)
    inc, U, lb, trace, nq = core_search(I, L, Fr(1, 2 ** 10), 6)
    for T in trace:
        if not (T['lam'] <= opt <= T['U'] <= T['lam'] + T['ej']):
            good_b = False
        for cidx in T['kept']:
            cmin = min(oracle(I, tuple(T['h'] * (cidx[i] + cor[i]) for i in range(k)))[0] for cor in itertools.product((0, 1), repeat=k))
            if cmin > opt + 2 * T['ej']:
                good_c = False
    # (d): sample random points of X
    for _ in range(200):
        v = [Fr(random.randint(0, 64), 64) for _ in range(k)]
        ys = []
        for i in I['R']:
            if I['isint'][i]:
                ys.append(Fr(random.randint(int(I['lo'][i]), int(I['hi'][i]))))
            else:
                ys.append(I['lo'][i] + (I['hi'][i] - I['lo'][i]) * Fr(random.randint(0, 16), 16))
        if Fval(I, v + ys) < lb:
            good_d = False
    # thm:cr-exact pipeline when J is affordable
    eps = Fr(1, 2 * Om * Om)
    if L == 0:
        J = 0
    else:
        J = 0
        while k * L / 8 / Fr(4) ** J > eps:
            J += 1
    if J <= 14 and (k == 1 or J <= 9):
        inc, U, beta, trace, nq = core_search(I, L, eps, J)
        yU = inc[1]
        val, vh = solve_face_min(I, yU)
        W = val.denominator
        passes = val - beta < Fr(1, Om * W)
        if not (passes and val == opt):
            good_x = False
        ninst += 1
report("lem:cr-height: denominators of Psi(y) and OPT <= Omega_K (60 instances)", good_h)
report("thm:cr-search(b): lam_j <= OPT <= U <= lam_j + e_j at every level", good_b)
report("thm:cr-search(c): retained cells have a corner with V <= OPT + 2 e_j", good_c)
report("thm:cr-search(d): F(x) >= min(lam,U) at 200 random feasible points per instance", good_d)
report(f"thm:cr-exact: face minimization at y_U is optimal and passes the test ({ninst} instances)", good_x)


# ---------- prop:cr-submod with a convex part (|R+|=1) ----------
good = True
for trial in range(150):
    mneg = random.randint(1, 3)
    n = mneg + 1  # last coordinate in R+, continuous on [lo,hi]
    o = [random.choice((1, -1)) for _ in range(n)]
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if i == j:
                H[i][i] = -abs(rnd()) if i < mneg else abs(rnd(0, 3)) + Fr(1, 4)
            else:
                H[i][j] = H[j][i] = -o[i] * o[j] * abs(rnd())
    b = [rnd() for _ in range(n)]
    lo = [rnd(-1, 0, (2,)) for _ in range(n)]; hi = [lo[i] + Fr(random.randint(1, 3)) for i in range(n)]
    alpha = [lo[i] if o[i] == 1 else hi[i] for i in range(n)]
    dl = [(hi[i] - lo[i]) * o[i] for i in range(n)]
    def Phi(S):
        y = [alpha[i] + dl[i] * (1 if i in S else 0) for i in range(mneg)]
        # minimize over last coordinate t in [lo,hi]: 1/2 H t^2 + (b + sum H y) t
        a2 = H[n - 1][n - 1]; a1 = b[n - 1] + sum(H[n - 1][i] * y[i] for i in range(mneg))
        t = min(max(-a1 / a2, lo[n - 1]), hi[n - 1])
        x = y + [t]
        return Fr(1, 2) * sum(H[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) + sum(b[i] * x[i] for i in range(n))
    subsets = [frozenset(s) for r in range(mneg + 1) for s in itertools.combinations(range(mneg), r)]
    vals = {S: Phi(S) for S in subsets}
    for S in subsets:
        for T in subsets:
            if vals[S] + vals[T] < vals[S & T] + vals[S | T]:
                good = False
report("prop:cr-submod(c): Phi submodular with a convex continuous part (150 instances)", good)

print("ALL PASS" if ok else "SOME FAIL")
