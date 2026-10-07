"""Reviewer's exact (sympy) checks, review round 1.  Independent of the
stream's code.

A. Lemma 2.3 parts 1-3 with fully symbolic affine L.
B. Family: nonnegativity identity, cross coefficients, family LMI identity
   l(q) = h^2 + 2 h b.v + v.B v (as used in r1_common.moment_relaxation).
C. Corollary 2.6: which of the 48 symmetry images can have all three cross
   coefficients positive.
D. Lemma 2.9 formula.
E. Proposition 2.10: contact systems of S1-S5 built from scratch; generic rank,
   rank on the special sub-loci, and the boundary values d1 = 0 / d2 = 0.
F. Theorem 4.2 bookkeeping with formal symbols.
"""
from itertools import permutations, product
import random

import sympy as sp

x, y, z = sp.symbols('x y z')
XS = [x, y, z]
ok = True


def check(cond, msg):
    global ok
    print(('PASS ' if cond else 'FAIL ') + msg, flush=True)
    ok = ok and bool(cond)


def in_V(p):
    P = sp.Poly(sp.expand(p), *XS)
    return all(max(m) <= 2 and sum(1 for t in m if t == 2) <= 1 for m in P.monoms())


def rho(f, i):
    xi = XS[i]
    return sp.expand((1 - xi) * f.subs(xi, 0) + xi * f.subs(xi, 1))


# ---------------- A. Lemma 2.3 -----------------
print('A. Lemma 2.3')
Vmon = [x**a * y**b * z**c for a, b, c in product(range(3), repeat=3)
        if [a, b, c].count(2) <= 1]
for i in range(3):
    for mnm in Vmon:
        r = rho(mnm, i)
        deg = sp.degree(mnm, XS[i])
        expect = mnm if deg == 0 else sp.expand(mnm / XS[i]**deg * XS[i])
        if sp.expand(r - expect) != 0 or not in_V(r):
            check(False, f'rho_{i}({mnm})')
check(True, 'part 1: rho_i fixes monomials without x_i, replaces x_i^a (a>=1) by x_i, stays in V (60 cases)')

cnt = 0
for s in product(range(3), repeat=3):
    A = [j for j in range(3) if s[j] == 1]
    B = [j for j in range(3) if s[j] == 2]
    F = [j for j in range(3) if s[j] == 0]
    w = sp.Mul(*[XS[j] for j in A]) * sp.Mul(*[(1 - XS[j]) for j in B])
    cs = sp.symbols('c0:4')
    L = cs[0] + sum(cs[j + 1] * XS[j] for j in F)
    g = sp.expand(w * L**2)
    assert in_V(g)
    for i in range(3):
        r = rho(g, i)
        if i in A or i in B:
            good = sp.expand(r - g) == 0
        else:
            L0, L1 = L.subs(XS[i], 0), L.subs(XS[i], 1)
            good = sp.expand(r - (w * (1 - XS[i]) * L0**2 + w * XS[i] * L1**2)) == 0
        # part 3: coefficient of the pure monomial x_i^2 in g
        coeff = sp.Poly(g, *XS).coeff_monomial(XS[i]**2)
        expect3 = (w.subs({x: 0, y: 0, z: 0})) * (cs[i + 1]**2 if i in F else 0)
        good3 = sp.expand(coeff - expect3) == 0 and w.subs({x: 0, y: 0, z: 0}) in (0, 1)
        if not (good and good3):
            check(False, f'generator {A},{B} coordinate {i}')
        cnt += 1
check(cnt == 81, 'parts 2-3: rho_i(g) = g (i in A u B) or sum of two generators (i free); '
      'x_i^2 coefficient = w(0) c_i^2 >= 0 (81 cases)')

# ---------------- B. Family -----------------
print('B. Family')
h, d1, d2, d3, k = sp.symbols('h d1 d2 d3 k', real=True)
D = d1 + d2 - h
Lf = h - d1 * x - d2 * y + d3 * z
q = sp.expand(Lf**2 + 2 * d3 * k * z * (1 - x - y) + k * (2 * D + k) * x * y)
ident = ((Lf - k * x * y)**2 + 2 * d3 * k * z * (1 - x) * (1 - y) + k * (2 * d1 + k) * x * y * (1 - x)
         + 2 * k * d2 * x * y * (1 - y) + k**2 * x**2 * y * (1 - y))
check(sp.expand(q - ident) == 0, 'family nonnegativity identity')
P = sp.Poly(q, x, y, z)
check(sp.expand(P.coeff_monomial(x * z) + 2 * d3 * (d1 + k)) == 0, 'q_xz = -2 d3 (d1 + k)')
check(sp.expand(P.coeff_monomial(y * z) + 2 * d3 * (d2 + k)) == 0, 'q_yz = -2 d3 (d2 + k)')
check(sp.expand(P.coeff_monomial(x * y) - (2 * d1 * d2 + k * (2 * D + k))) == 0, 'q_xy = 2 d1 d2 + k(2D + k)')
check(all(sp.expand(P.coeff_monomial(v**2) - c**2) == 0 for v, c in [(x, d1), (y, d2), (z, d3)]),
      'square coefficients d_i^2')
# LMI identity: replace monomials by moment symbols
mx, my, mz, Yxx, Yyy, Yzz, Yxy, Yxz, Yyz = sp.symbols('mx my mz Yxx Yyy Yzz Yxy Yxz Yyz')
sub = {x**2: Yxx, y**2: Yyy, z**2: Yzz, x * y: Yxy, x * z: Yxz, y * z: Yyz, x: mx, y: my, z: mz}
lq = sp.expand(sum(cf * (sub[sp.Mul(*[v**e for v, e in zip((x, y, z), mon)])] if sum(mon) > 0 else 1)
                   for mon, cf in P.terms()))
bv = sp.Matrix([-mx, -my, mz, -Yxy])
Bm = sp.Matrix([[Yxx, Yxy, -Yxz, Yxy], [Yxy, Yyy, -Yyz, Yxy],
                [-Yxz, -Yyz, Yzz, mz - Yxz - Yyz], [Yxy, Yxy, mz - Yxz - Yyz, Yxy]])
v = sp.Matrix([d1, d2, d3, k])
check(sp.expand(lq - (h**2 + 2 * h * (bv.T * v)[0] + (v.T * Bm * v)[0])) == 0,
      'family LMI identity l(q) = h^2 + 2h b.v + v.B v')

# ---------------- C. Corollary 2.6 -----------------
print('C. Corollary 2.6')
rng = random.Random(1)
images = {}
for perm in permutations(range(3)):
    for comp in product((0, 1), repeat=3):
        u = [(1 - XS[perm[i]]) if comp[i] else XS[perm[i]] for i in range(3)]
        qg = sp.expand(q.subs({x: u[0], y: u[1], z: u[2]}, simultaneous=True))
        Pg = sp.Poly(qg, x, y, z)
        cross = [Pg.coeff_monomial(x * y), Pg.coeff_monomial(x * z), Pg.coeff_monomial(y * z)]
        allpos = False
        for _ in range(300):
            vals = {h: rng.uniform(-3, 3), d1: rng.uniform(0, 3), d2: rng.uniform(0, 3),
                    d3: rng.uniform(0, 3), k: rng.uniform(0, 3)}
            if all(float(c.subs(vals)) > 0 for c in cross):
                allpos = True
                break
        # identify the copy up to the x<->y swap (which swaps d1, d2)
        key = (perm[2], tuple(sorted([(perm[0], comp[0]), (perm[1], comp[1])])), comp[2])
        images.setdefault(key, set()).add(allpos)
check(len(images) == 24, '48 symmetries give 24 distinct copies (x<->y swap identified)')
pos_copies = [kk for kk, vv in images.items() if True in vv]
print('   copies with all-positive cross coefficients for some parameters:', len(pos_copies))
for kk in sorted(pos_copies):
    zc, pair, zcomp = kk
    print('     special coordinate', zc, 'complemented' if zcomp else 'kept',
          '; other two:', ['1-x%d' % a if c else 'x%d' % a for a, c in pair])
check(len(pos_copies) == 6 and all((kk[2] == 1 and all(c == 0 for _, c in kk[1])) or
                                   (kk[2] == 0 and all(c == 1 for _, c in kk[1])) for kk in pos_copies),
      'exactly 6 copies, S = {z} or S = {x, y} (sampled parameters; the converse is the sign argument)')

# ---------------- D. Lemma 2.9 -----------------
print('D. Lemma 2.9')
a1, a2, a3, p0, r12, r13, r23 = sp.symbols('a1 a2 a3 p0 r12 r13 r23', positive=True)
aa = [a1, a2, a3]
pp = p0 * ((1 - x / a1 - y / a2 - z / a3)**2 + 2 * (r12 * x * y / (a1 * a2) + r13 * x * z / (a1 * a3)
                                                    + r23 * y * z / (a2 * a3)))
for i in range(3):
    t = sp.symbols('t')
    restr = pp.subs({XS[j]: (t if j == i else 0) for j in range(3)})
    check(sp.simplify(restr - p0 * (1 - t / aa[i])**2) == 0, f'edge {i}: restriction p0 (1 - t/a_{i})^2')
check(sp.simplify(pp.subs({x: a1 / 2, y: a2 / 2, z: 0}) - p0 * r12 / 2) == 0, 'value at midpoint = p0 r12 / 2')

# ---------------- E. Proposition 2.10 -----------------
print('E. Proposition 2.10')
cvec = sp.symbols('c0:10')
gen = (cvec[0] + cvec[1] * x + cvec[2] * y + cvec[3] * z + cvec[4] * x**2 + cvec[5] * y**2
       + cvec[6] * z**2 + cvec[7] * x * y + cvec[8] * x * z + cvec[9] * y * z)


def rows(contacts):
    R = []
    for pt, dirs in contacts:
        s = dict(zip(XS, pt))
        R.append([sp.diff(gen, c).subs(s) for c in cvec])
        for i in dirs:
            dg = sp.diff(gen, XS[i])
            R.append([sp.diff(dg, c).subs(s) for c in cvec])
    return sp.Matrix(R)


def coeffs(qq):
    Pq = sp.Poly(sp.expand(qq), x, y, z)
    mons = [1, x, y, z, x**2, y**2, z**2, x * y, x * z, y * z]
    return sp.Matrix([Pq.coeff_monomial(m) for m in mons])


def stratum_data(name, sub):
    hh, e1, e2, e3, kk = [sp.sympify(s).subs(sub) for s in (h, d1, d2, d3, k)]
    DD = e1 + e2 - hh
    a = ((hh / e1, 0, 0), [0]) if hh != 0 else None
    b = ((0, hh / e2, 0), [1]) if hh != 0 else None
    c = ((1, 0, (e1 - hh) / e3), [2])
    d = ((0, 1, (e2 - hh) / e3), [2])
    ee = ((1, 1, (DD + kk) / e3), [2])
    v111 = ((1, 1, 1), [2])
    v000 = ((0, 0, 0), [0, 1])
    v100 = ((1, 0, 0), [0, 2])
    if name == 'S1':
        cts = [a, b, c, d, v111]
    elif name == 'S2':
        cts = [v000, c, d, ee]
    elif name == 'S3':
        cts = [v100, b, d, ee]
    elif name == 'S4':
        cts = [v000, c, d, v111]
    elif name == 'S5':
        cts = [v100, b, d, v111]
    qq = coeffs((hh - e1 * x - e2 * y + e3 * z)**2 + 2 * e3 * kk * z * (1 - x - y) + kk * (2 * DD + kk) * x * y)
    return rows(cts), qq


# Strata with free parameters; positivity assumed by sampling inside the region.
H, A1, A2, K = sp.symbols('H A1 A2 K', positive=True)
T = sp.symbols('T', positive=True)  # slack for strict inequalities
strata = {
    'S1': {d3: d1 + d2 - h + k},
    'S2': {h: 0},
    'S3': {h: d1},
    'S4': {h: 0, d3: d1 + d2 + k},
    'S5': {h: d1, d3: d2 + k},
}
for name, sub in strata.items():
    M, qq = stratum_data(name, sub)
    kern_ok = all(sp.simplify(t) == 0 for t in (M * qq))
    rk = M.rank(simplify=True)
    check(kern_ok and rk == 9, f'{name}: family member in kernel; generic rank {rk} ({M.shape[0]} rows)')

# exact rank at random rational points inside each region, plus special loci
R = random.Random(7)


def rq(lo, hi):
    return sp.Rational(R.randint(int(lo * 1000) + 1, int(hi * 1000) - 1), 1000)


def rank_at(name, vals):
    sub = dict(strata[name])
    M, qq = stratum_data(name, {})
    full = {**{s: sp.sympify(t).subs(vals) for s, t in sub.items()}, **vals}
    Mv = M.subs(full)
    qv = qq.subs(full)
    return Mv.rank(), all(t == 0 for t in Mv * qv)


bad = []
for name in strata:
    for trial in range(40):
        kk = rq(0, 3)
        if name == 'S1':
            e1, e2 = rq(0, 3), rq(0, 3)
            hh = rq(0, float(min(e1, e2)))
            vals = {h: hh, d1: e1, d2: e2, k: kk}
            if trial == 0:
                vals = {h: sp.Rational(1, 3), d1: sp.Rational(2, 3), d2: 2, k: kk}   # d1 = 2h
        elif name in ('S2', 'S4'):
            e1, e2 = rq(0, 3), rq(0, 3)
            if trial == 0:
                e1 = 0
            if trial == 1:
                e1 = e2 = 0
            vals = {d1: e1, d2: e2, k: kk}
            if name == 'S2':
                vals[d3] = e1 + e2 + kk + rq(0, 3)
        else:
            e2 = rq(0, 3)
            e1 = rq(0, float(e2))
            vals = {d1: e1, d2: e2, k: kk}
            if name == 'S3':
                vals[d3] = e2 + kk + rq(0, 3)
        r, kern = rank_at(name, vals)
        if r != 9 or not kern:
            bad.append((name, vals, r, kern))
check(not bad, 'rank 9 and kernel at 40 rational points per stratum (incl. d1 = 2h on S1, d1 = 0 and '
      'd1 = d2 = 0 on S2/S4)')
for bb in bad:
    print('   ', bb)

# boundary value d1 = 0 on S3 / S5 (h = d1 = 0): the zero set contains the x-edge
for name in ('S3', 'S5'):
    vals = {d1: 0, d2: sp.Rational(3, 2), k: sp.Rational(1, 2)}
    if name == 'S3':
        vals[d3] = sp.Rational(5, 2)
    r, kern = rank_at(name, vals)
    print(f'   {name} at d1 = h = 0 (allowed by "h = d1 < d2" with d >= 0): rank of the listed system = {r}')

# ---------------- F. Theorem 4.2 bookkeeping -----------------
print('F. Theorem 4.2 bookkeeping')
E = sp.symbols('E1:6', positive=True)        # E_i stands for eps^{e_i}
Hm = sp.Matrix([[1, -1, 1, 1, -1], [-1, 1, -1, 1, 1], [1, -1, 1, -1, 1],
                [1, 1, -1, 1, -1], [-1, 1, 1, -1, 1]])
xs = sp.symbols('x1:5')
u = [1] + list(xs)
fsym = {}


def fval(i, j):
    key = tuple(sorted((i, j)))
    if key not in fsym:
        fsym[key] = sp.Symbol('f_%d%d' % key)
    return fsym[key]


qq = sum(Hm[i, j] * E[i]**2 * u[i] * E[j]**2 * u[j] for i in range(5) for j in range(5))
# L_f multiplies the coefficient c * eps^a by f(a); every coefficient of qq is a single monomial
Lq = sum(Hm[i, j] * fval(i, j) * E[i]**2 * u[i] * E[j]**2 * u[j] for i in range(5) for j in range(5))
Pq = sp.Poly(sp.expand(qq), *xs)
single = all(len(sp.Add.make_args(sp.factor(cf))) == 1 for cf in Pq.coeffs())
xi = {xs[t]: E[0]**2 / E[t + 1]**2 for t in range(4)}
val = sp.simplify(Lq.subs(xi) - E[0]**4 * sum(Hm[i, j] * fval(i, j) for i in range(5) for j in range(5)))
check(single and val == 0, 'single-monomial coefficients; L_f(q)(xi) = eps^{4e_1} sum H_ij f(2e_i+2e_j)')

print('ALL PASS' if ok else 'SOME CHECK FAILED')
