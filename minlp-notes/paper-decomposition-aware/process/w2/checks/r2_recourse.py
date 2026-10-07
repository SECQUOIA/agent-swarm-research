"""R2 exact checks for recourse-convex / recourse-cuts / recourse-balanced claims.

1. Example ex:cv-fm (symbolic in M): responses, values, KKT signs, B^T C B.
2. Prop prop:cv-ladder: identity, inertia for small m, Rayleigh bound.
3. Prop prop:cv-limit: SOS inequality, eigenvalues, y_c, x_c, piece curvatures,
   concave interior piece, V(y_c) expansion.
4. Prop prop:cr-cut + Thm thm:cr-oracle: cut identity on random (R1)-(R2) instances,
   min cut (own Edmonds-Karp in Fractions) vs brute force.
5. Lemma lem:chaincut: random balanced quadratics with random nonuniform grids and
   random unary terms; min cut vs brute force; min-marginals.
6. Lemma lem:cr-height: random instances, Phi(z) denominators <= D_0.
"""
from fractions import Fraction as Fr
from itertools import product
from collections import deque
import random
import sympy as sp

random.seed(20261003)

# ---------------------------------------------------------------- 1. f_M
M, z = sp.symbols('M z', positive=True)
y1, y2 = sp.symbols('y1 y2')
fM = M * (y1 + y2 - z) ** 2 + (y1 - 2 * z + sp.Rational(1, 2)) ** 2
C = sp.hessian(fM, (y1, y2))
assert C == sp.Matrix([[2 * M + 2, 2 * M], [2 * M, 2 * M]])
pieces = [
    ((0, sp.Rational(1, 4)), (sp.Integer(0), z), (sp.Rational(1, 2) - 2 * z) ** 2, 2 * M),
    ((sp.Rational(1, 4), sp.Rational(1, 2)), (2 * z - sp.Rational(1, 2), sp.Rational(1, 2) - z), sp.Integer(0), 2 * M + 8),
    ((sp.Rational(1, 2), sp.Rational(3, 4)), (((M + 2) * z - sp.Rational(1, 2)) / (M + 1), sp.Integer(0)),
     M * (z - sp.Rational(1, 2)) ** 2 / (M + 1), 2 * (M + 2) ** 2 / (M + 1)),
]
H0zz = sp.diff(M * z ** 2 + (2 * z - sp.Rational(1, 2)) ** 2, z, 2)
assert sp.simplify(H0zz - (2 * M + 8)) == 0
for (lo, hi), (r1, r2), val, btcb in pieces:
    sub = {y1: r1, y2: r2}
    assert sp.simplify(fM.subs(sub) - val) == 0
    B = sp.Matrix([sp.diff(r1, z), sp.diff(r2, z)])
    assert sp.simplify((B.T * C * B)[0] - btcb) == 0
    assert sp.simplify(sp.diff(val, z, 2) - (H0zz - btcb)) == 0
    g1 = sp.diff(fM, y1).subs(sub)
    g2 = sp.diff(fM, y2).subs(sub)
    for Mv in (1, 2, 7, 100):
        for k in range(0, 21):
            zv = lo + (hi - lo) * sp.Rational(k, 20)
            s = {M: Mv, z: zv}
            a1, a2 = r1.subs(s), r2.subs(s)
            G1, G2 = g1.subs(s), g2.subs(s)
            for a, G in ((a1, G1), (a2, G2)):
                assert 0 <= a <= 1
                if 0 < a < 1:
                    assert G == 0
                elif a == 0:
                    assert G >= 0
                else:
                    assert G <= 0
assert sp.simplify(2 * (M + 2) ** 2 / (M + 1) - 2 * M) .subs(M, 1) > 0
print("1. ex:cv-fm OK (pieces, KKT signs, B^TCB, piece curvatures)")

# ---------------------------------------------------------------- 2. ladder
t, u, w, Ms = sp.symbols('t u w M')
a = sp.Rational(1, 5)
zz = t + a
Y1, Y2 = u, w + a
expr = zz ** 2 + Ms * (Y1 + Y2 - zz) ** 2 + (Y1 - 2 * zz + sp.Rational(1, 2)) ** 2 - sp.Rational(1, 20)
r = u + w - t
s_ = u - 2 * t
assert sp.expand(expr - (t ** 2 + Ms * r ** 2 + s_ ** 2 + u / 5)) == 0
for m in (1, 2, 3, 4):
    eta = sp.Rational(1, 16)
    Mv = 3
    zs = sp.symbols(f'z0:{m}'); vs = sp.symbols(f'v0:{m}')
    ya = sp.symbols(f'ya0:{m}'); yb = sp.symbols(f'yb0:{m}')
    F = 0
    for i in range(m):
        F += zs[i] ** 2 + Mv * (ya[i] + yb[i] - zs[i]) ** 2 + (ya[i] - 2 * zs[i] + sp.Rational(1, 2)) ** 2 \
            - vs[i] ** 2 + 3 * vs[i] - (zs[i] - a) * vs[i]
    for i in range(m - 1):
        F += eta * ((zs[i + 1] - zs[i]) ** 2 + (vs[i + 1] - vs[i]) ** 2)
    var = list(zs) + list(vs) + list(ya) + list(yb)
    H = sp.hessian(F, var)
    # exact inertia: H symmetric, all eigenvalues real, so Descartes' rule on the
    # characteristic polynomial counts positive/negative roots exactly.
    lam = sp.Symbol('lam')
    cp = sp.Poly(H.charpoly(lam).as_expr(), lam)
    def sign_changes(cs):
        cs = [c for c in cs if c != 0]
        return sum(1 for p_, q_ in zip(cs, cs[1:]) if p_ * q_ < 0)
    cneg = sp.Poly(cp.as_expr().subs(lam, -lam), lam).all_coeffs()
    neg = sign_changes(cneg)
    assert neg == m, (m, neg)
    # lambda_min <= -2 : H + 2I has a nonpositive eigenvalue (Rayleigh quotient -2)
    cp2 = sp.Poly(cp.as_expr().subs(lam, lam - 2), lam)  # eigenvalues of H+2I
    npos_or_zero_neg = sign_changes(sp.Poly(cp2.as_expr().subs(lam, -lam), lam).all_coeffs())
    assert npos_or_zero_neg >= 1 or cp2.eval(0) == 0
    # lambda_min >= -sqrt5: no eigenvalue below -9/4 (since 9/4 > sqrt5) and charpoly of H+sqrt5 I psd checked numerically
    import numpy as np
    Hn = np.array(H.tolist(), dtype=float)
    assert np.linalg.eigvalsh(Hn).min() >= -5 ** 0.5 - 1e-9
    # minimizer value
    xs = {**{zs[i]: a for i in range(m)}, **{vs[i]: 0 for i in range(m)}, **{ya[i]: 0 for i in range(m)},
          **{yb[i]: a for i in range(m)}}
    assert F.subs(xs) == sp.Rational(m, 20)
print("2. prop:cv-ladder OK (identity; inertia = m and -sqrt5 <= lambda_min <= -2 for m<=4, M=3)")

# ---------------------------------------------------------------- 3. cv-limit
al, be, Mm = sp.symbols('alpha beta M')
FM = Mm * (al - be) ** 2 - sp.Rational(1, 8) * (al + be) ** 2 + 2 * be
lower = (al - be) ** 2 - sp.Rational(1, 8) * (al + be) ** 2 + be ** 2 - sp.Rational(1, 8) * (al ** 2 + be ** 2)
assert sp.expand(lower - (sp.Rational(3, 4) * (al - sp.Rational(3, 2) * be) ** 2 + be ** 2 / 16)) == 0
x, y = sp.symbols('x y')
Fxy = Mm * (x - y) ** 2 - sp.Rational(1, 8) * (x + y - 2) ** 2 + 2 * (y - 1)
Hm = sp.hessian(Fxy, (x, y))
assert sp.simplify(Hm * sp.Matrix([1, -1]) - 4 * Mm * sp.Matrix([1, -1])) == sp.zeros(2, 1)
assert sp.simplify(Hm * sp.Matrix([1, 1]) + sp.Rational(1, 2) * sp.Matrix([1, 1])) == sp.zeros(2, 1)
assert Fxy.subs({x: 2, y: 2}) == sp.Rational(3, 2)
yc = 4 * Mm / (2 * Mm + sp.Rational(1, 4))
assert sp.simplify(sp.diff(Fxy, x).subs({x: 2, y: yc})) == 0
xc = 1 + 2 / (2 * Mm + sp.Rational(1, 4))
assert sp.simplify(sp.diff(Fxy, y).subs({y: 1, x: xc})) == 0
assert sp.simplify(Fxy.subs(y, 1) - (Mm - sp.Rational(1, 8)) * (x - 1) ** 2) == 0
# interior response for R={x}: V'' = Fxx - Fxy^2/Fyy < 0
Vpp = Hm[0, 0] - Hm[0, 1] ** 2 / Hm[1, 1]
assert sp.simplify(Vpp + 2 * Mm / (2 * Mm - sp.Rational(1, 4))) == 0
# V(y_c) = 3/2 - (3/2)delta + (M-1/8)delta^2 with delta = 2 - y_c
dlt = 2 - yc
assert sp.simplify(Fxy.subs({x: 2, y: yc}) - (sp.Rational(3, 2) - sp.Rational(3, 2) * dlt + (Mm - sp.Rational(1, 8)) * dlt ** 2)) == 0
for Mv in (1, 2, 5, 50):
    assert 1 < yc.subs(Mm, Mv) < 2 and 1 < xc.subs(Mm, Mv) <= 2
    # brute-force growth 1/8 on a rational grid
    for i in range(0, 41):
        for j in range(0, 41):
            xv = Fr(2 * i, 40); yv = 1 + Fr(2 * j, 40)
            val = Mv * (xv - yv) ** 2 - Fr(1, 8) * (xv + yv - 2) ** 2 + 2 * (yv - 1)
            assert val >= Fr(1, 8) * ((xv - 1) ** 2 + (yv - 1) ** 2)
print("3. prop:cv-limit OK")


# ---------------------------------------------------------------- max flow (Fractions)
def maxflow(nodes, cap, s, tt):
    """Edmonds-Karp on dict-of-dicts capacities (Fractions or float('inf'))."""
    res = {a: dict(b) for a, b in cap.items()}
    for a in nodes:
        res.setdefault(a, {})
    for a in list(res):
        for b in list(res[a]):
            res.setdefault(b, {}).setdefault(a, Fr(0))
    flow = Fr(0)
    while True:
        par = {s: None}
        q = deque([s])
        while q and tt not in par:
            a = q.popleft()
            for b, c in res[a].items():
                if c > 0 and b not in par:
                    par[b] = a
                    q.append(b)
        if tt not in par:
            break
        path = []
        b = tt
        while par[b] is not None:
            path.append((par[b], b)); b = par[b]
        aug = min(res[a][b] for a, b in path)
        for a, b in path:
            res[a][b] -= aug
            res[b][a] += aug
        flow += aug
    side = set(par)  # reachable from s in residual graph
    return flow, side


def cutcap(cap, S):
    return sum(c for a in cap for b, c in cap[a].items() if a in S and b not in S)


# ---------------------------------------------------------------- 4. signed cut
def rand_frac(lo, hi, den=4):
    return Fr(random.randint(lo * den, hi * den), den)


ncheck = 0
for trial in range(150):
    k = random.randint(1, 2)
    nr = random.randint(1, 5)
    o = [random.choice((-1, 1)) for _ in range(nr)]
    a_ = [-rand_frac(0, 2) for _ in range(nr)]
    b_ = [rand_frac(-3, 3) for _ in range(nr)]
    cR = {}
    for i in range(nr):
        for j in range(i + 1, nr):
            if random.random() < 0.6:
                cR[(i, j)] = -o[i] * o[j] * rand_frac(0, 3)
    cCR = [[rand_frac(-3, 3) for _ in range(nr)] for _ in range(k)]
    lo = [Fr(random.randint(-2, 0)) for _ in range(nr)]
    hi = [lo[i] + Fr(random.randint(1, 3), random.choice((1, 2))) for i in range(nr)]
    v = [rand_frac(0, 1) for _ in range(k)]
    def F(xr):
        val = Fr(0)
        for i in range(nr):
            val += a_[i] * xr[i] ** 2 + b_[i] * xr[i] + sum(cCR[c][i] * v[c] * xr[i] for c in range(k))
        for (i, j), c in cR.items():
            val += c * xr[i] * xr[j]
        return val
    alpha = [lo[i] if o[i] == 1 else hi[i] for i in range(nr)]
    d = [(hi[i] - lo[i]) * o[i] for i in range(nr)]
    xr = lambda yy: [alpha[i] + d[i] * yy[i] for i in range(nr)]
    phi0 = F(xr([0] * nr))
    mu = [F(xr([1 if t == i else 0 for t in range(nr)])) - phi0 for i in range(nr)]
    om = {}
    for i in range(nr):
        for j in range(i + 1, nr):
            e = [0] * nr; e[i] = e[j] = 1
            om[(i, j)] = F(xr(e)) - phi0 - mu[i] - mu[j]
            assert om[(i, j)] == cR.get((i, j), 0) * d[i] * d[j] and om[(i, j)] <= 0
    rho = [mu[i] + sum(om[tuple(sorted((i, j)))] for j in range(nr) if j != i) / 2 for i in range(nr)]
    cap = {'s': {}, 't': {}}
    for i in range(nr):
        cap.setdefault(i, {})
        if rho[i] > 0:
            cap[i]['t'] = rho[i]
        if rho[i] < 0:
            cap['s'][i] = -rho[i]
    for (i, j), wv in om.items():
        if wv != 0:
            cap[i][j] = -wv / 2
            cap[j][i] = -wv / 2
    const = phi0 + sum(min(Fr(0), r_) for r_ in rho)
    best = None
    for yy in product((0, 1), repeat=nr):
        S = {'s'} | {i for i in range(nr) if yy[i] == 1}
        assert F(xr(yy)) == const + cutcap(cap, S)
        best = F(xr(yy)) if best is None else min(best, F(xr(yy)))
        ncheck += 1
    flow, side = maxflow(['s', 't'] + list(range(nr)), cap, 's', 't')
    assert const + flow == best
    yy = [1 if i in side else 0 for i in range(nr)]
    assert F(xr(yy)) == best
    # endpoint reduction: continuous-box min equals endpoint min (coarse rational grid check)
    for pt in product(*[[lo[i] + (hi[i] - lo[i]) * Fr(q, 4) for q in range(5)] for i in range(nr)]):
        if nr <= 3:
            assert F(list(pt)) >= best
print(f"4. prop:cr-cut identity on {ncheck} labels, min cut = brute force on 150 instances OK")


# ---------------------------------------------------------------- 5. chaincut
nch = 0
for trial in range(120):
    n = random.randint(2, 4)
    sig = [random.choice((-1, 1)) for _ in range(n)]
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = rand_frac(-3, 3)
        for j in range(i + 1, n):
            if random.random() < 0.7:
                H[i][j] = H[j][i] = -sig[i] * sig[j] * rand_frac(0, 3)
    b = [rand_frac(-2, 2) for _ in range(n)]
    G = [sorted(set(rand_frac(-2, 2, 8) for _ in range(random.randint(1, 4)))) for _ in range(n)]
    eta = [{g: rand_frac(-1, 1, 8) for g in G[i]} for i in range(n)]
    def Phi(yv):
        val = sum(eta[i][yv[i]] for i in range(n))
        val += sum(H[i][i] * yv[i] ** 2 / 2 + b[i] * yv[i] for i in range(n))
        val += sum(H[i][j] * yv[i] * yv[j] for i in range(n) for j in range(i + 1, n))
        return val
    def solve(Gs):
        ordl = [sorted(Gs[i]) if sig[i] == 1 else sorted(Gs[i], reverse=True) for i in range(n)]
        mi = [len(ordl[i]) - 1 for i in range(n)]
        nodes = [(i, l) for i in range(n) for l in range(1, mi[i] + 1)]
        dl = {(i, l): ordl[i][l] - ordl[i][l - 1] for (i, l) in nodes}
        th = lambda i, tv: H[i][i] * tv ** 2 / 2 + b[i] * tv + eta[i][tv]
        E0 = sum(th(i, ordl[i][0]) for i in range(n)) + sum(H[i][j] * ordl[i][0] * ordl[j][0] for i in range(n) for j in range(i + 1, n))
        h = {}
        for (i, l) in nodes:
            h[(i, l)] = th(i, ordl[i][l]) - th(i, ordl[i][l - 1]) + sum(H[i][j] * dl[(i, l)] * ordl[j][0] for j in range(n) if j != i)
        wv = {}
        for p_ in nodes:
            for q_ in nodes:
                if p_ < q_ and p_[0] != q_[0]:
                    i, j = p_[0], q_[0]
                    wv[(p_, q_)] = H[i][j] * dl[p_] * dl[q_]
                    assert wv[(p_, q_)] <= 0
        pa = {a_: h[a_] + sum(wv[tuple(sorted((a_, b_)))] for b_ in nodes if b_ != a_ and b_[0] != a_[0]) / 2 for a_ in nodes}
        INF = Fr(10 ** 12)
        cap = {'s': {}, 't': {}}
        for a_ in nodes:
            cap.setdefault(a_, {})
            if pa[a_] > 0: cap[a_]['t'] = pa[a_]
            if pa[a_] < 0: cap['s'][a_] = -pa[a_]
        for (p_, q_), wq in wv.items():
            if wq != 0:
                cap[p_][q_] = cap[p_].get(q_, 0) - wq / 2
                cap[q_][p_] = cap[q_].get(p_, 0) - wq / 2
        for i in range(n):
            for l in range(1, mi[i]):
                cap[(i, l + 1)][(i, l)] = INF
        flow, side = maxflow(['s', 't'] + nodes, cap, 's', 't')
        const = E0 + sum(min(Fr(0), pv) for pv in pa.values())
        yv = []
        for i in range(n):
            kk = max([l for l in range(1, mi[i] + 1) if (i, l) in side], default=0)
            assert all(((i, l) in side) == (l <= kk) for l in range(1, mi[i] + 1))
            yv.append(ordl[i][kk])
        return const + flow, yv
    val, yv = solve(G)
    brute = min(Phi(p) for p in product(*G))
    assert val == brute and Phi(yv) == brute, (val, brute)
    for i in range(n):
        for v_ in G[i]:
            Gs = [list(g) for g in G]; Gs[i] = [v_]
            val2, _ = solve(Gs)
            assert val2 == min(Phi(p) for p in product(*Gs))
            nch += 1
print(f"5. lem:chaincut OK on 120 instances (+{nch} min-marginals)")


# ---------------------------------------------------------------- 6. cr-height
def lcm(a, b):
    from math import gcd
    return a * b // gcd(a, b)


def lcmall(xs):
    out = 1
    for x_ in xs:
        out = lcm(out, Fr(x_).denominator)
    return out


def minimize_box_quadratic(Q, q, c, k):
    """exact min of 1/2 v^T Q v + q^T v + c over [0,1]^k by face enumeration (incl. singular faces
    handled by trying all faces with nonsingular free block; returns min)."""
    best = None
    for pattern in product((0, 1, 2), repeat=k):
        S = [i for i in range(k) if pattern[i] == 2]
        fixed = {i: Fr(pattern[i]) for i in range(k) if pattern[i] < 2}
        if S:
            A = sp.Matrix([[Q[i][j] for j in S] for i in S])
            if A.det() == 0:
                continue
            rhs = sp.Matrix([-(q[i] + sum(Q[i][j] * fixed[j] for j in fixed)) for i in S])
            sol = A.LUsolve(rhs)
            vals = {S[t_]: Fr(int(sp.fraction(sol[t_])[0]), int(sp.fraction(sol[t_])[1])) for t_ in range(len(S))}
            if any(not (0 <= vals[i] <= 1) for i in S):
                continue
            fixed.update(vals)
        v = [fixed[i] for i in range(k)]
        val = sum(Q[i][j] * v[i] * v[j] for i in range(k) for j in range(k)) / 2 + sum(q[i] * v[i] for i in range(k)) + c
        best = val if best is None else min(best, val)
    return best


from math import factorial
for trial in range(60):
    k = random.randint(1, 3)
    nr = random.randint(1, 3)
    n = k + nr
    a_ = [rand_frac(-2, 2, 3) for _ in range(k)] + [-rand_frac(0, 2, 3) for _ in range(nr)]
    cc = {(i, j): rand_frac(-2, 2, 6) for i in range(n) for j in range(i + 1, n) if random.random() < 0.7}
    bb = [rand_frac(-2, 2, 5) for _ in range(n)]
    c0 = rand_frac(-1, 1, 7)
    lo = [Fr(random.randint(-3, 0), random.choice((1, 2, 3))) for _ in range(nr)]
    hi = [lo[i] + Fr(random.randint(1, 3), random.choice((1, 2, 3))) for i in range(nr)]
    Lc = lcmall(a_ + list(cc.values()) + bb + [c0])
    Le = lcmall(lo + hi)
    T0 = Lc * Le * Le
    Hfull = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        Hfull[i][i] = 2 * a_[i]
    for (i, j), cv in cc.items():
        Hfull[i][j] = Hfull[j][i] = cv
    H0 = max([1] + [abs(T0 * Hfull[i][j]) for i in range(k) for j in range(k)])
    D0 = T0 * (factorial(k) * H0 ** k) ** 2
    vals = []
    for zr in product(*[(lo[i], hi[i]) for i in range(nr)]):
        xr_ = list(zr)
        Q = [[Hfull[i][j] for j in range(k)] for i in range(k)]
        q = [bb[i] + sum(Hfull[i][k + r_] * xr_[r_] for r_ in range(nr)) for i in range(k)]
        c = c0 + sum(a_[k + r_] * xr_[r_] ** 2 + bb[k + r_] * xr_[r_] for r_ in range(nr)) \
            + sum(cc.get((k + r_, k + s_), 0) * xr_[r_] * xr_[s_] for r_ in range(nr) for s_ in range(r_ + 1, nr))
        Phi = minimize_box_quadratic(Q, q, c, k)
        assert Phi.denominator <= D0, (Phi, D0)
        vals.append(Phi)
print("6. lem:cr-height denominators <= D_0 on 60 random instances OK")
