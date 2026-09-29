"""Independent exact re-certification of Theorem 14 (and the second rational instance).

Reviewer script; does not import the author's code.  S = {(x,y,w) : w <= x y}, q = w - x y,
M(x,y,w;h) = [[w, x],[y, h]], det M(s,1) = q(s).  Family (A): C_F cap {h=1},
C_F = {M : sym(F^T M) PSD}, det F > 0.  Family (B): upward closure along e_w.

Steps (all exact, sympy):
 1. P = [v_j - sbar] invertible; g(lam) = q(sbar + P lam) on the simplex {lam >= 0, sum <= 1}:
    exact face enumeration (15 faces), singular faces reported; min g = 0 only at lam*.
 2. The pencil is derived here from scratch: the linear conditions on F^T that Lemma 13's proof
    imposes (F^T a0 || b0, u^T Y u = 0, b0^T Y u = 0) are solved as a null space; we check that
    the solution space is 2-dimensional and equals span(G0, G1).  The sign of theta is fixed
    by requiring F^T a0 = c b0 with c > 0 (checked explicitly, not via a trace heuristic).
 3. Exact kappa-sets K_A(v) (2x2 PSD <=> diag >= 0 and det >= 0) and their intersection.
 4. (B): exact certificates u with u^T A_v u < 0 and u^T Z u >= 0 on complementary kappa-ranges;
    plus a numerical sweep: for kappa on a grid, max_{tau in [0, q(v)]} lambda_min(A_v - tau Z)
    for v in {sbar, v3} (at least one must be negative).
 5. (x0, y0) interior / boundary of proj T*.
"""
import itertools, sys, json
import numpy as np
import sympy as sp

R = sp.Rational
INST = {
    'thm14': dict(sbar=[R(-9, 2), 0, R(3, 2)], v1=[-1, -6, 18], v2=[-5, 6, -18], v3=[0, R(5, 2), R(5, 2)]),
    'second': dict(sbar=[R(-1, 2), R(1, 2), 1], v1=[R(1, 2), -4, R(-1, 2)], v2=[-10, 3, 24], v3=[R(9, 2), R(1, 2), R(15, 2)]),
}
q = lambda s: s[2] - s[0] * s[1]
J = sp.Matrix([[0, 1], [-1, 0]])
Mm = lambda s, h=1: sp.Matrix([[s[2], s[0]], [s[1], h]])
sym = lambda X: (X + X.T) / 2
E = sp.Matrix([[1, 0], [0, 0]])
kap = sp.Symbol('kappa', real=True)


def face_min(g, lam):
    """Exact min of quadratic g over simplex {lam>=0, sum<=1} by enumerating faces."""
    n = len(lam)
    cands, singular = [], []
    # a face: Z = indices fixed at 0, top = whether sum(lam) = 1 is imposed
    for r in range(0, n + 1):
        for Zs in itertools.combinations(range(n), r):
            free = [lam[i] for i in range(n) if i not in Zs]
            for top in (False, True):
                if not free and top:
                    continue
                sub = {lam[i]: 0 for i in Zs}
                gg = sp.expand(g.subs(sub))
                if top:
                    # eliminate last free variable
                    last = free[-1]
                    rest = free[:-1]
                    gg = sp.expand(gg.subs(last, 1 - sum(rest)))
                    vars_ = rest
                else:
                    vars_ = free
                if not vars_:
                    pt = {x: 0 for x in lam}
                    if top:
                        pt[free[-1]] = 1
                    cands.append((gg, pt, (Zs, top)))
                    continue
                H = sp.hessian(gg, vars_)
                grad = [sp.diff(gg, x) for x in vars_]
                if H.det() == 0:
                    singular.append((Zs, top))
                    continue
                sol = sp.solve(grad, vars_, dict=True)
                assert len(sol) == 1
                sol = sol[0]
                pt = {x: 0 for x in lam}
                for x in vars_:
                    pt[x] = sol[x]
                if top:
                    pt[free[-1]] = 1 - sum(sol[x] for x in vars_)
                # inside the relative interior (or closure) of the face?
                if all(pt[x] >= 0 for x in lam) and sum(pt[x] for x in lam) <= 1:
                    cands.append((sp.nsimplify(gg.subs(sol)), pt, (Zs, top)))
    return cands, singular


def run(name, inst):
    print('=' * 70)
    print('instance', name)
    sb = sp.Matrix(inst['sbar']); V = [sp.Matrix(inst[k]) for k in ('v1', 'v2', 'v3')]
    P = sp.Matrix.hstack(*[v - sb for v in V])
    print('q(sbar) =', q(sb), ' q(v_j) =', [q(v) for v in V], ' det P =', P.det())
    assert q(sb) > 0 and P.det() != 0
    lam = sp.symbols('l1:4', real=True)
    lv = sp.Matrix(lam)
    g = sp.expand(q(sb + P * lv))
    cands, singular = face_min(g, lam)
    gmin = min(c[0] for c in cands)
    argmins = [c for c in cands if c[0] == gmin]
    print('singular faces (skipped; minima then also on their boundary):', singular)
    print('min g over simplex =', gmin, ' argmins:', [dict((str(k), v) for k, v in c[1].items()) for c in argmins])
    assert gmin == 0
    pts = {tuple(c[1][x] for x in lam) for c in argmins}
    assert len(pts) == 1, pts
    lstar = sp.Matrix(list(pts.pop()))
    tstar = sb + P * lstar
    print('lambda* =', list(lstar), ' cost =', sum(lstar), ' t* =', list(tstar))
    supp = [i for i in range(3) if lstar[i] != 0]
    assert sum(lstar) == 1 and supp == [0, 1]
    # tangent edge data
    i, j = supp
    d = V[i] - V[j]
    grad = sp.Matrix([-tstar[1], -tstar[0], 1])
    detMd = -d[0] * d[1]
    print('grad q(t*).d =', grad.dot(d), ' det M(d;0) =', detMd)
    M0 = Mm(tstar)
    # rank-one factorization M0 = a0 b0^T
    assert M0.det() == 0
    if M0[:, 0] != sp.zeros(2, 1):
        a0 = M0[:, 0]; b0 = sp.Matrix([1, M0[0, 1] / M0[0, 0] if M0[0, 0] != 0 else M0[1, 1] / M0[1, 0]])
    else:
        a0 = M0[:, 1]; b0 = sp.Matrix([0, 1])
    assert sp.simplify(a0 * b0.T - M0) == sp.zeros(2, 2), (a0, b0)
    u = J * b0
    # --- derive the pencil: F^T unknown 2x2
    f = sp.symbols('f0:4')
    FT = sp.Matrix([[f[0], f[1]], [f[2], f[3]]])
    Md = Mm(d, 0)
    Y = sym(FT * Md)
    conds = [(J * b0).dot(FT * a0), (u.T * Y * u)[0], (b0.T * Y * u)[0]]
    A = sp.Matrix([[sp.diff(cnd, fi) for fi in f] for cnd in conds])
    ns = A.nullspace()
    print('rank of Lemma-13 conditions:', A.rank(), ' solution dim:', len(ns))
    G0 = J * (Md.adjugate()); G1 = J * (M0.adjugate())
    vec = lambda X: sp.Matrix([X[0, 0], X[0, 1], X[1, 0], X[1, 1]])
    span_ok = sp.Matrix.hstack(*ns, vec(G0), vec(G1)).rank() == 2
    print('null space == span(G0, G1):', span_ok, ' det(G0 + k G1) =', sp.factor((G0 + kap * G1).det()))
    print('G1 a0 =', list(G1 * a0), ' G0 a0 =', list(G0 * a0), ' b0 =', list(b0))
    c0 = (G0 * a0).dot(b0) / b0.dot(b0)
    assert sp.simplify(G0 * a0 - c0 * b0) == sp.zeros(2, 1)
    sgn = 1 if c0 > 0 else -1
    print('G0 a0 = c0 b0 with c0 =', c0, '=> theta sign', sgn)
    FTk = sgn * (G0 + kap * G1)
    Z = sym(FTk * E)
    uZu = sp.expand((u.T * Z * u)[0])
    print('u^T Z u (tangency inequality kept strictly) =', uZu)
    verts = {'sbar': sb, 'v1': V[0], 'v2': V[1], 'v3': V[2]}
    KA = {}
    total = sp.S.Reals
    for nm, v in verts.items():
        Av = sym(FTk * Mm(v))
        s = sp.S.Reals
        for expr in (Av[0, 0], Av[1, 1], sp.expand(Av.det())):
            s = s.intersect(sp.solveset(expr >= 0, kap, sp.S.Reals))
        KA[nm] = s
        total = total.intersect(s)
        print('  K_A(%s) = %s  ~ %s' % (nm, s, [sp.N(e, 6) for e in (s.boundary if s != sp.S.EmptySet else [])]))
    print('intersection of K_A over vertices:', total)
    # --- (B) certificates, exact
    certs = {}
    for nm in ('sbar', 'v3'):
        Av = sym(FTk * Mm(verts[nm]))
        roots = sp.solve(sp.expand(Av.det()), kap)
        certs[nm] = []
        for kc in roots:
            Ak = sp.simplify(Av.subs(kap, kc))
            if not (Ak[0, 0] >= 0 and Ak[1, 1] >= 0):
                continue
            uu = Ak.nullspace()[0]
            a_lin = sp.expand(sp.simplify((uu.T * Av * uu)[0]))
            z_lin = sp.expand(sp.simplify((uu.T * Z * uu)[0]))
            certs[nm].append((kc, uu, a_lin, z_lin))
    ok_B = False
    for (ks, us, As, Zs) in certs['sbar']:
        for (k3, u3, A3, Z3) in certs['v3']:
            # need: kappa <= ks excluded by sbar, kappa >= k3 excluded by v3, and k3 < ks
            if not (sp.N(k3 - ks) < 0):
                continue
            sA = sp.Poly(As, kap).coeff_monomial(kap); sZ = sp.Poly(Zs, kap).coeff_monomial(kap)
            s3A = sp.Poly(A3, kap).coeff_monomial(kap); s3Z = sp.Poly(Z3, kap).coeff_monomial(kap)
            # sbar: u^T A u < 0 for kappa < ks (slope > 0, zero at ks); u^T Z u >= 0 for kappa <= ks
            c1 = sp.simplify(As.subs(kap, ks)) == 0 and sp.N(sA) > 0
            c2 = sp.N(Zs.subs(kap, ks)) > 0 and sp.N(sZ) <= 0
            # at kappa = ks itself sbar is on the boundary of K_A; there v3 must exclude (ks > k3)
            c3 = sp.simplify(A3.subs(kap, k3)) == 0 and sp.N(s3A) < 0
            c4 = sp.N(Z3.subs(kap, k3)) > 0 and sp.N(s3Z) >= 0
            print('  cert pair k3=%s (%.6f) < ks=%s (%.6f): %s %s %s %s' % (k3, sp.N(k3), ks, sp.N(ks), c1, c2, c3, c4))
            if c1 and c2 and c3 and c4:
                ok_B = True
                print('    u_s =', list(us), ' uAu =', As, ' uZu =', Zs)
                print('    u_3 =', list(u3), ' uAu =', A3, ' uZu =', Z3)
    print('family (B) excluded for every kappa (exact certificate):', ok_B)
    # --- numeric sweep for (B)
    f_A = {nm: sp.lambdify(kap, sym(FTk * Mm(verts[nm])), 'numpy') for nm in verts}
    f_Z = sp.lambdify(kap, Z, 'numpy')
    worst = -np.inf
    for kv in np.concatenate([np.linspace(-60, 60, 24001), np.linspace(-1, 1, 4001)]):
        best_per_v = {}
        for nm in ('sbar', 'v3'):
            Av = np.array(f_A[nm](kv), dtype=float); Zv = np.array(f_Z(kv), dtype=float)
            qv = float(q(verts[nm]))
            taus = np.linspace(0, qv, 401)
            best_per_v[nm] = max(np.linalg.eigvalsh(Av - t * Zv)[0] for t in taus)
        worst = max(worst, min(best_per_v.values()))
    print('numeric sweep: max over kappa of min_{v in sbar,v3} max_tau lambda_min =', worst, '(must be < 0)')
    # --- projection interior
    pr = [sp.Matrix(verts[k][:2]) for k in verts]
    p0 = sp.Matrix(tstar[:2])
    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    # (x0,y0) interior iff for every line through two projected vertices that is a hull edge,
    # p0 is strictly on the inner side.  Compute hull edges directly.
    hull_edges = []
    for a, b in itertools.combinations(range(4), 2):
        sides = [orient(pr[a], pr[b], pr[c]) for c in range(4) if c not in (a, b)]
        if all(s > 0 for s in sides) or all(s < 0 for s in sides):
            hull_edges.append((a, b, 1 if sides[0] > 0 else -1))
    vals = [orient(pr[a], pr[b], p0) * sg for a, b, sg in hull_edges]
    print('hull edges', hull_edges, ' signed positions of (x0,y0):', vals,
          '=> interior' if all(v > 0 for v in vals) else '=> NOT interior (on boundary)' if all(v >= 0 for v in vals) else '=> outside')


if __name__ == '__main__':
    for nm in (sys.argv[1:] or INST.keys()):
        run(nm, INST[nm])
