"""Review r2: independent exact checks of instances A (Theorem 8) and S1 (Theorem 9).

Data typed from note.md (not read from the stream's code).  Does not import any stream module.
Checks: det sbar, det P; min of det over T* by own face enumeration (exact); z_K = 1 with unique
minimizer; KKT multipliers; tangent edge / transversality; kappa-intervals (A); the dual
certificates printed in the logs (parsed from the log text, verified exactly here); an own
rational primal certificate for the orbit lower bound; SCIP's value from the literal Case-1
formula (Prop. 1) by mpmath bisection.
Usage: python3 r2_exact.py LOGDIR
"""
import sys, re, ast, itertools
from fractions import Fraction as Fr
import sympy as sp
import mpmath as mp
import numpy as np
import cvxpy as cp

LOG = sys.argv[1]
F_ = lambda s: Fr(s)

def det(s): return s[0]*s[3] - s[1]*s[2]
def B(s, t): return (s[0]*t[3] + s[3]*t[0] - s[1]*t[2] - s[2]*t[1]) / 2
def grad(s): return (s[3], -s[2], -s[1], s[0])
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def sub(a, b): return tuple(x-y for x, y in zip(a, b))
def addm(a, b, c=1): return tuple(x + c*y for x, y in zip(a, b))
def m2(s): return [[s[0], s[1]], [s[2], s[3]]]
def mm(A, Bm): return [[sum(A[i][k]*Bm[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

ok_all = True
def chk(name, c):
    global ok_all
    ok_all &= bool(c)
    print(('PASS ' if c else 'FAIL ') + name, flush=True)

def min_det_simplex(verts):
    """Own exact face enumeration: stationary points of det restricted to the affine hull of each
    face, kept if in the relative interior.  Returns (min value, list of minimizers, #singular faces)."""
    n = len(verts)
    best, arg, sing = None, [], 0
    for k in range(1, n+1):
        for S in itertools.combinations(range(n), k):
            u0 = verts[S[0]]
            E = [sub(verts[i], u0) for i in S[1:]]
            m = len(E)
            if m == 0:
                cand = [(u0, ())]
            else:
                H = sp.Matrix(m, m, lambda i, j: 2*B(E[i], E[j]))
                g = sp.Matrix(m, 1, lambda i, j: 2*B(u0, E[i]))
                if H.det() == 0:
                    sing += 1
                    continue        # min on such a face is attained on a lower face (quadratic constant along kernel)
                mu = H.LUsolve(-g)
                mu = [Fr(int(sp.fraction(x)[0]), int(sp.fraction(x)[1])) for x in mu]
                if not (all(x > 0 for x in mu) and sum(mu) < 1):
                    continue
                x = u0
                for c, e in zip(mu, E):
                    x = addm(x, e, c)
                cand = [(x, tuple(mu))]
            for x, mu in cand:
                v = det(x)
                if best is None or v < best:
                    best, arg = v, [(S, x)]
                elif v == best:
                    arg.append((S, x))
    return best, arg, sing

def kappa_set(G0, G1, V):
    k = sp.Symbol('k', real=True)
    Mt = sp.Matrix(G0) + k*sp.Matrix(G1)
    X = Mt * sp.Matrix(m2(V))
    S = (X + X.T)/2
    cond = sp.And(sp.simplify(S.trace()) >= 0, sp.expand(S.det()) >= 0)
    return sp.solve_univariate_inequality(sp.expand(S.det()) >= 0, k, relational=False).intersect(
        sp.solve_univariate_inequality(sp.simplify(S.trace()) >= 0, k, relational=False))

def parse_Ys(logtext, z):
    for line in logtext.splitlines():
        pass
    lines = logtext.splitlines()
    for i, line in enumerate(lines):
        if ('certificate at z = %s:' % z) in line:
            ys = lines[i+1].split(':', 1)[1].strip()
            return [[[Fr(x) for x in r] for r in Y] for Y in ast.literal_eval(ys)]
    raise ValueError('no certificate for z=%s' % z)

def check_dual(sb, P, z, Ys, tag):
    verts = [sb] + [addm(sb, p, z) for p in P]
    pd = all(Y[0][0] > 0 and Y[0][0]*Y[1][1] - Y[0][1]*Y[1][0] > 0 and Y[0][1] == Y[1][0] for Y in Ys)
    S = [[Fr(0)]*2 for _ in range(2)]
    for V, Y in zip(verts, Ys):
        VY = mm(m2(V), Y)
        S = [[S[i][j] + VY[i][j] for j in range(2)] for i in range(2)]
    chk('%s dual certificate at z = %s: Y_V symmetric PD (exact) and sum_V V Y_V = 0 (exact) => z_orbit <= %s' % (tag, z, z),
        pd and all(S[i][j] == 0 for i in range(2) for j in range(2)))

def own_lower(sb, P, z, tag):
    """Own SDP in the original coordinates (no preconditioning); round F^T to rationals; check exactly
    that sym(F^T sbar) > 0 and sym(F^T V) >= 0 on the vertices of T_z."""
    zf = float(z)
    verts = [sb] + [addm(sb, p, z) for p in P]
    Vf = [np.array([[float(v[0]), float(v[1])], [float(v[2]), float(v[3])]]) for v in verts]
    G = cp.Variable((2, 2)); t = cp.Variable()
    cons = [cp.trace(G @ Vf[0]) == 1]
    for V in Vf:
        X = G @ V
        cons.append((X + X.T)/2 >> t*np.eye(2))
    cp.Problem(cp.Maximize(t), cons).solve(solver='CLARABEL')
    Gv = G.value
    for den in (10**8, 10**10, 10**12, 10**14):
        Gr = [[Fr(float(Gv[i, j])).limit_denominator(den) for j in range(2)] for i in range(2)]
        okk = True
        for idx, V in enumerate(verts):
            X = mm(Gr, m2(V))
            S = [[(X[i][j] + X[j][i])/2 for j in range(2)] for i in range(2)]
            dS = S[0][0]*S[1][1] - S[0][1]**2
            if idx == 0:
                okk &= S[0][0] > 0 and dS > 0
            else:
                okk &= S[0][0] >= 0 and S[1][1] >= 0 and dS >= 0
        if okk:
            break
    chk('%s own rational primal certificate at z = %s (SDP t = %.2e, denominator %d): T_z in C_F, sbar in int C_F => z_orbit >= %s'
        % (tag, z, t.value, den, z), okk)

def scip_literal(sb, P, dps=50):
    """Step lengths of SCIP's Case-1 set {||yhat(M)|| <= xhat(Mbar).xhat(M)/||xhat(Mbar)||} by bisection."""
    mp.mp.dps = dps
    q = lambda x: mp.mpf(x.numerator)/x.denominator
    sbm = [q(x) for x in sb]
    xh = lambda s: (( s[0]+s[3])/2, (s[2]-s[1])/2)
    yh = lambda s: ((s[3]-s[0])/2, (s[1]+s[2])/2)
    xb = xh(sbm); nb = mp.sqrt(xb[0]**2 + xb[1]**2)
    def inside(s):
        x, y = xh(s), yh(s)
        return mp.sqrt(y[0]**2 + y[1]**2) <= (xb[0]*x[0] + xb[1]*x[1])/nb
    out = []
    for p in P:
        pm = [q(x) for x in p]
        pt = lambda t: [a + t*b for a, b in zip(sbm, pm)]
        hi = mp.mpf(1)
        while inside(pt(hi)) and hi < 1e6:
            hi *= 2
        if hi >= 1e6:
            out.append(mp.inf); continue
        lo = mp.mpf(0)
        for _ in range(200):
            mid = (lo + hi)/2
            if inside(pt(mid)): lo = mid
            else: hi = mid
        out.append(lo)
    return out

def instance(tag, sb, Vs, tstar, logname, zups, brackets):
    print('==================== instance', tag)
    txt = open(LOG + '/' + logname).read()
    P = [sub(v, sb) for v in Vs]
    chk('%s det sbar = %s' % (tag, det(sb)), det(sb) > 0)
    dP = sp.Matrix([[P[j][i] for j in range(4)] for i in range(4)]).det()
    print('   det[p1..p4] =', dP)
    verts = [sb] + Vs
    mval, arg, sing = min_det_simplex(verts)
    print('   singular faces skipped:', sing)
    chk('%s min det over T* = %s, attained only at t* = %s (found: %s)' % (tag, mval, [str(x) for x in tstar],
        [[str(c) for c in a[1]] for a in arg]), mval == 0 and len({a[1] for a in arg}) == 1 and arg[0][1] == tstar)
    Pm = sp.Matrix([[P[j][i] for j in range(4)] for i in range(4)])
    lam = list(Pm.LUsolve(sp.Matrix([x for x in sub(tstar, sb)])))
    print('   lambda* =', lam, ' cost =', sum(lam))
    g = grad(tstar)
    gp = [dot(g, p) for p in P]
    j0 = next(j for j in range(4) if lam[j] > 0)
    sigma = Fr(-1) / gp[j0]
    nu = [1 + sigma*x for x in gp]
    print('   grad det(t*).p_j =', [str(x) for x in gp], ' sigma =', sigma, ' nu =', [str(x) for x in nu])
    print('   grad det(t*).sbar =', dot(g, sb))
    for z in zups:
        check_dual(sb, P, Fr(z), parse_Ys(txt, z), tag)
    own_lower(sb, P, Fr(brackets[0]), tag)
    st = scip_literal(sb, P)
    print('   SCIP literal Case-1 formula step lengths:', [mp.nstr(x, 12) for x in st], ' z_SCIP =', mp.nstr(min(st), 12))
    return P, g, lam, nu

# ---------------- instance A
sb = tuple(map(F_, ('0', '5/2', '-1/2', '-1/2')))
Vs = [tuple(map(F_, v)) for v in (('-5', '3', '4', '-4'), ('-8', '12', '-8', '8'), ('-3/2', '-4', '2', '-7/2'), ('-7/2', '-1/2', '3/2', '-4'))]
ts = tuple(map(F_, ('-6', '6', '0', '0')))
P, g, lam, nu = instance('A', sb, Vs, ts, 'certify_cex_A.log', ['1', '9/20'], ['0.4495347'])
d = sub(Vs[0], Vs[1])
chk('A tangent edge: grad.d = %s, det d = %s' % (dot(g, d), det(d)), dot(g, d) == 0 and det(d) == 72)
J = [[0, 1], [-1, 0]]
adj = lambda M: [[M[1][1], -M[0][1]], [-M[1][0], M[0][0]]]
G0 = mm(J, adj(m2(d))); G1 = mm(J, adj(m2(ts)))
print('   G0 =', G0, ' G1 =', G1)
Ks = [kappa_set(G0, G1, V) for V in [sb] + Vs]
for name, K in zip(['sbar', 'v1', 'v2', 'v3', 'v4'], Ks):
    print('   K(%s) = %s' % (name, K))
inter = Ks[0]
for K in Ks[1:]:
    inter = inter.intersect(K)
chk('A kappa-sets have empty intersection', inter == sp.EmptySet)
# also the small z = 1 certificate printed in the note text
Ynote = [[[Fr(237, 250), Fr(133, 500)], [Fr(133, 500), Fr(57, 500)]], [[Fr(453, 1000), Fr(7, 20)], [Fr(7, 20), Fr(29, 100)]],
         [[Fr(9, 100), Fr(11, 100)], [Fr(11, 100), Fr(17, 100)]], [[Fr(1, 100), 0], [0, Fr(7, 50)]], [[Fr(1, 100), 0], [0, Fr(1, 100)]]]
check_dual(sb, P, Fr(1), Ynote, 'A (note text, small)')

# ---------------- instance S1
sb = tuple(map(F_, ('-4', '-1', '-1/2', '-2')))
Vs = [tuple(map(F_, v)) for v in (('3', '3', '-3', '-3'), ('95/24', '4', '-4', '-4'), ('17/3', '6', '-3/2', '-3/2'), ('41/6', '3', '-6', '-2'))]
ts = Vs[0]
P, g, lam, nu = instance('S1', sb, Vs, ts, 'certify_supp1_full.log', ['1', '779/1000'], ['0.7780998'])
tr = [dot(g, sub(v, ts)) for v in [sb] + Vs[1:]]
gn = mp.sqrt(sum(mp.mpf(float(x))**2 for x in g))
cos = [float(x) / float(gn * mp.sqrt(sum(mp.mpf(float(y))**2 for y in sub(v, ts)))) for x, v in zip(tr, [sb] + Vs[1:])]
chk('S1 transversal edges: grad.(v - t*) = %s, cosines %s' % ([str(x) for x in tr], ['%.4f' % c for c in cos]), all(x > 0 for x in tr))
chk('S1 support one and nu = (0, 1/36, 2/9, 1/9)', lam == [1, 0, 0, 0] and nu == [0, Fr(1, 36), Fr(2, 9), Fr(1, 9)])
print('ALL PASS' if ok_all else 'SOME FAIL')
