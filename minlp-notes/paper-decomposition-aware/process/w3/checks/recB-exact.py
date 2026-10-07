"""recB checks: Lemma cr-height (via Cor height constants), CORE invariants (Thm cr-search),
Thm cr-exact pipeline, Prop cr-growth count, Props cr-submod / cr-greedy identities. Exact arithmetic."""
from fractions import Fraction as Fr
from math import lcm, isqrt
import itertools, random
random.seed(11)

def F(H, b, c, x):
    n = len(x)
    return Fr(1, 2)*sum(H[i][j]*x[i]*x[j] for i in range(n) for j in range(n)) + sum(b[i]*x[i] for i in range(n)) + c

def solve(A, rhs):
    n = len(A); M = [row[:] + [rhs[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = next((r for r in range(col, n) if M[r][col] != 0), None)
        if piv is None: return None
        M[col], M[piv] = M[piv], M[col]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]/M[col][col]
                M[r] = [M[r][t]-f*M[col][t] for t in range(n+1)]
    return [M[i][n]/M[i][i] for i in range(n)]

def box_qp_min(Hb, bb, cb, lo, up):
    """exact min of 1/2 x^T Hb x + bb x + cb over box by face enumeration (valid by Lemma statpoly(c))"""
    k = len(bb); best = None; arg = None
    for face in itertools.product(['f', 'l', 'u'], repeat=k):
        T = [i for i in range(k) if face[i] == 'f']
        x = [lo[i] if face[i] == 'l' else up[i] if face[i] == 'u' else None for i in range(k)]
        if T:
            A = [[Hb[i][j] for j in T] for i in T]
            rhs = [-(bb[i] + sum(Hb[i][j]*x[j] for j in range(k) if j not in T)) for i in T]
            sol = solve(A, rhs)
            if sol is None: continue
            for t, i in enumerate(T): x[i] = sol[t]
            if any(not (lo[i] <= x[i] <= up[i]) for i in T): continue
        val = F(Hb, bb, cb, x)
        if best is None or val < best: best, arg = val, x
    return best, arg

def rnd(den=(1, 2)): return Fr(random.randint(-6, 6), random.choice(den))

def instance(k, r):
    n = k + r
    o = [random.choice([-1, 1]) for _ in range(r)]
    H = [[Fr(0)]*n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if i == j:
                H[i][i] = -abs(rnd()) if i >= k else Fr(random.randint(0, 6), random.choice([1, 2]))
            else:
                h = rnd()
                if i >= k and j >= k: h = -abs(h)*o[i-k]*o[j-k]
                H[i][j] = H[j][i] = h
    b = [rnd() for _ in range(n)]; c = rnd()
    lo = [Fr(random.randint(-2, 0), random.choice([1, 2])) for _ in range(r)]
    up = [lo[i] + Fr(random.randint(0, 3), random.choice([1, 2])) for i in range(r)]
    return H, b, c, lo, up

def phi_data(H, b, c, k, y):
    n = len(H)
    Hb = [[H[i][j] for j in range(k)] for i in range(k)]
    bb = [b[i] + sum(H[i][k+j]*y[j] for j in range(len(y))) for i in range(k)]
    cb = c + sum(b[k+j]*y[j] for j in range(len(y))) + Fr(1, 2)*sum(H[k+i][k+j]*y[i]*y[j] for i in range(len(y)) for j in range(len(y)))
    return Hb, bb, cb

def Omega_K(H, b, c, k, lo, up):
    n = len(H)
    coefs = [H[i][i]/2 for i in range(n)] + [H[i][j] for i in range(n) for j in range(i+1, n)] + b + [c]
    Lc = 1
    for q in coefs: Lc = lcm(Lc, q.denominator)
    Le = 1
    for q in lo + up: Le = lcm(Le, q.denominator)
    D = Lc*Le*Le
    R = D
    for i in range(k):
        if H[i][i] > 0: R *= D*H[i][i]
    assert R.denominator == 1
    return D*R*R

# ---- Lemma cr-height and the 1/8 example
H = [[Fr(0), Fr(0), Fr(0)], [Fr(0), Fr(0), Fr(1, 2)], [Fr(0), Fr(1, 2), Fr(0)]]
assert F(H, [0, 0, 0], 0, [0, Fr(1, 2), Fr(1, 2)]) == Fr(1, 8)
cnt = 0
for trial in range(120):
    k = random.randint(1, 2); r = random.randint(1, 3)
    H, b, c, lo, up = instance(k, r)
    Om = Omega_K(H, b, c, k, lo, up)
    for y in itertools.product(*[(lo[i], up[i]) for i in range(r)]):
        Hb, bb, cb = phi_data(H, b, c, k, list(y))
        val, _ = box_qp_min(Hb, bb, cb, [Fr(0)]*k, [Fr(1)]*k)
        assert val.denominator <= Om, (val, Om)
        cnt += 1
print("lem:cr-height: %d label values within Omega_K" % cnt)

# ---- CORE invariants + exact output + query count
def V_of(H, b, c, k, lo, up, v):
    r = len(lo); best = None; arg = None
    for y in itertools.product(*[(lo[i], up[i]) for i in range(r)]):
        val = F(H, b, c, list(v) + list(y))
        if best is None or val < best: best, arg = val, list(y)
    return best, arg

def core(H, b, c, k, lo, up, L, stop, Jmax, OPT, xstar_v):
    cache = {}; queries = 0
    def V(v):
        nonlocal queries
        if v not in cache: queries += 1; cache[v] = V_of(H, b, c, k, lo, up, v)
        return cache[v][0]
    Q = [tuple((Fr(0), Fr(1)) for _ in range(k))]; U = None; inc = None
    discarded = []
    for j in range(Jmax+1):
        h = Fr(1, 2**j); e = k*L*h*h/8
        for C in Q:
            for v in itertools.product(*C):
                val = V(v)
                if U is None or val < U: U, inc = val, v
        bV = {C: min(V(v) for v in itertools.product(*C)) - e for C in Q}
        lam = min(bV.values())
        ret = [C for C in Q if bV[C] <= U]
        # invariants (a)-(c)
        assert lam <= OPT <= U <= lam + e
        for C in ret: assert min(V(v) for v in itertools.product(*C)) <= OPT + 2*e
        for C in Q:
            if all(C[i][0] <= xstar_v[i] <= C[i][1] for i in range(k)): assert C in ret
        if U - min(lam, U) < stop(e, U, lam):
            return U, inc, min(lam, U), j, queries
        discarded += [(C, U) for C in Q if C not in ret]
        Q = []
        for C in ret:
            mids = [((a + bb)/2) for (a, bb) in C]
            for choice in itertools.product([0, 1], repeat=k):
                Q.append(tuple((C[i][0], mids[i]) if choice[i] == 0 else (mids[i], C[i][1]) for i in range(k)))
    return U, inc, min(lam, U), Jmax, queries

ok = 0
for trial in range(40):
    k = random.randint(1, 2); r = random.randint(1, 3)
    H, b, c, lo, up = instance(k, r)
    L = max([Fr(0)] + [H[i][i] for i in range(k)])
    # exact OPT and a minimizer core part
    best = None
    for y in itertools.product(*[(lo[i], up[i]) for i in range(r)]):
        Hb, bb, cb = phi_data(H, b, c, k, list(y))
        val, x = box_qp_min(Hb, bb, cb, [Fr(0)]*k, [Fr(1)]*k)
        if best is None or val < best[0]: best = (val, x, list(y))
    OPT, xv, ys = best
    Om = Omega_K(H, b, c, k, lo, up)
    if Om > 10**7: continue
    # approximate run with eps
    eps = Fr(1, 100)
    core(H, b, c, k, lo, up, L, lambda e, U, lam: eps if True else 0, 12, OPT, xv) if L > 0 else None
    # exact mode (Thm cr-exact): stop when gap < Omega^-2
    U, inc, beta, j, qn = core(H, b, c, k, lo, up, L, lambda e, U, lam: Fr(1, Om*Om), 60, OPT, xv)
    yU = V_of(H, b, c, k, lo, up, inc)[1]
    Hb, bb, cb = phi_data(H, b, c, k, yU)
    val, vhat = box_qp_min(Hb, bb, cb, [Fr(0)]*k, [Fr(1)]*k)
    W = val.denominator
    assert val - beta < Fr(1, Om*W)          # acceptance test passes
    assert val == OPT                        # and the output is optimal
    ok += 1
print("thm:cr-search invariants and thm:cr-exact pipeline: %d instances OK" % ok)

# Prop cr-growth bound on a strongly convex core with point growth: V(v) = sum (v_i - c_i)^2 *a, no residual coupling
for trial in range(10):
    k = random.randint(1, 2)
    a = Fr(random.randint(1, 4)); cc = [Fr(random.randint(1, 9), 10) for _ in range(k)]
    n = k + 1
    H = [[Fr(0)]*n for _ in range(n)]
    for i in range(k): H[i][i] = 2*a
    H[k][k] = Fr(-1)
    b = [-2*a*cc[i] for i in range(k)] + [Fr(0)]; c = sum(a*cc[i]**2 for i in range(k))
    lo, up = [Fr(0)], [Fr(1)]
    L = 2*a; g = a  # V(v)-OPT = a||v-c||^2 (residual adds -1/2 at y=1 uniformly)
    OPT = Fr(-1, 2)
    J = 8
    U, inc, beta, j, qn = core(H, b, c, k, lo, up, L, lambda e, U, lam: Fr(-1), J, OPT, cc)
    kap = max(1, L/g)
    bound = 2**k + 8**k*J*(1 + (k*kap)**0.5)**k
    assert qn <= bound, (qn, bound)
print("prop:cr-growth query bound: OK on 10 instances")

# ---- Props cr-submod / cr-greedy
def concave_convex_instance(rm, rp):
    r = rm + rp
    o = [random.choice([-1, 1]) for _ in range(r)]
    H = [[Fr(0)]*r for _ in range(r)]
    for i in range(r):
        for j in range(i+1, r):
            h = -abs(rnd())*o[i]*o[j] if random.random() < .8 else Fr(0)
            H[i][j] = H[j][i] = h
    for i in range(rm): H[i][i] = -abs(rnd())
    # make R+ block PSD by diagonal dominance
    for i in range(rm, r):
        H[i][i] = sum(abs(H[i][j]) for j in range(rm, r) if j != i) + Fr(random.randint(0, 3))
    b = [rnd() for _ in range(r)]; c = rnd()
    lo = [Fr(random.randint(-2, 0)) for _ in range(r)]; up = [lo[i] + Fr(random.randint(1, 3), random.choice([1, 2])) for i in range(r)]
    return H, b, c, lo, up, o

for trial in range(60):
    rm = random.randint(1, 3); rp = random.randint(1, 2)
    H, b, c, lo, up, o = concave_convex_instance(rm, rp)
    al = [lo[i] if o[i] == 1 else up[i] for i in range(rm)]
    de = [(up[i]-lo[i])*o[i] for i in range(rm)]
    def Phi(S):
        ym = [al[i] + de[i]*(1 if i in S else 0) for i in range(rm)]
        Hb = [[H[rm+i][rm+j] for j in range(rp)] for i in range(rp)]
        bb = [b[rm+i] + sum(H[rm+i][j]*ym[j] for j in range(rm)) for i in range(rp)]
        cb = c + sum(b[j]*ym[j] for j in range(rm)) + Fr(1, 2)*sum(H[i][j]*ym[i]*ym[j] for i in range(rm) for j in range(rm))
        return box_qp_min(Hb, bb, cb, lo[rm:], up[rm:])[0]
    subsets = [frozenset(s) for t in range(rm+1) for s in itertools.combinations(range(rm), t)]
    P = {S: Phi(S) for S in subsets}
    for S in subsets:
        for T in subsets:
            assert P[S] + P[T] >= P[S & T] + P[S | T]
    minP = min(P.values())
    # (a) of cr-submod: sampled points never below min Phi
    for _ in range(40):
        x = [lo[i] + (up[i]-lo[i])*Fr(random.randint(0, 6), 6) for i in range(rm+rp)]
        assert F(H, b, c, x) >= minP
    hat = {S: P[S]-P[frozenset()] for S in subsets}
    for pi in itertools.permutations(range(rm)):
        a = {}
        for l in range(rm):
            a[pi[l]] = hat[frozenset(pi[:l+1])] - hat[frozenset(pi[:l])]
        for S in subsets: assert sum(a[i] for i in S) <= hat[S]
        assert sum(a.values()) == hat[frozenset(range(rm))]
    # Lovasz-extension identity and lower bound used in (c)
    for _ in range(20):
        xi = [Fr(random.randint(0, 4), 4) for _ in range(rm)]
        pi = sorted(range(rm), key=lambda i: -xi[i])
        a = {pi[l]: hat[frozenset(pi[:l+1])] - hat[frozenset(pi[:l])] for l in range(rm)}
        lhs = sum(a[i]*xi[i] for i in range(rm))
        xs = [xi[p] for p in pi] + [Fr(0)]
        rhs = sum((xs[l]-xs[l+1])*hat[frozenset(pi[:l+1])] for l in range(rm)) + (1-xs[0])*hat[frozenset()]
        assert lhs == rhs and lhs >= min(hat.values())
        for perm in itertools.permutations(range(rm)):
            a2 = {perm[l]: hat[frozenset(perm[:l+1])] - hat[frozenset(perm[:l])] for l in range(rm)}
            assert sum(a2[i]*xi[i] for i in range(rm)) <= lhs
print("prop:cr-submod, prop:cr-greedy(a) and the identity in (c): 60 instances OK")
