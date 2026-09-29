"""Exact certificate that neither the sliced orbit family (A) nor its maximal completion (B)
attains the corner bound on a rational bilinear corner (side '+', S = {w <= xy}).

Input: rational vertices sbar, v1, v2, v3 of T* (rays p_j = v_j - sbar, w = (1,1,1)),
the touching point t0 in the relative interior of [v1, v2] and d = v1 - v2.
Checks (all in exact arithmetic, sympy):
 (1) min_{T*} q = 0, attained only at t0 (q = w - xy)  =>  z_K(1,1,1) = 1, T* cap int S empty.
 (2) t0 = l1 v1 + l2 v2 with l1, l2 > 0 (relative interior of the tangent edge).
 (3) generator pencil F_kappa^T = G0 + kappa G1 with sym(G0 M(t0)) PSD.
 (4) for kappa < kappa_s the vector u_s certifies sbar not in B_{F_kappa} (hence not in C_{F_kappa});
     for kappa > kappa_3 the vector u_3 certifies v3 not in B_{F_kappa};  kappa_3 < kappa_s.
 (5) (x0, y0) lies in the interior of the (x,y)-projection of T* (rank-one limits excluded).
Usage: python3 certify_counterexample.py  (edit INSTANCE below or pass JSON on argv[1]).
"""
import itertools, json, sys
import sympy as sp

R = sp.Rational
INSTANCE = dict(sbar=[R(-9, 2), 0, R(3, 2)], v1=[-1, -6, 18], v2=[-5, 6, -18], v3=[0, R(5, 2), R(5, 2)],
                t0=[-3, 0, 0])
if len(sys.argv) > 1:
    INSTANCE = json.loads(sys.argv[1])
ok = True


def check(name, cond):
    global ok
    ok &= bool(cond)
    print(('PASS ' if cond else 'FAIL ') + name)


V = {k: sp.Matrix([sp.nsimplify(x) for x in INSTANCE[k]]) for k in ('sbar', 'v1', 'v2', 'v3', 't0')}
sb, v1, v2, v3, t0 = V['sbar'], V['v1'], V['v2'], V['v3'], V['t0']
q = lambda s: s[2] - s[0] * s[1]
verts = [sb, v1, v2, v3]

# ---------------------------------------------------------------- (1) exact min of q over T*
L = sp.symbols('l0:4')
pt = sum((L[i] * verts[i] for i in range(4)), sp.zeros(3, 1))
cands = []
for r in range(1, 5):
    for Fc in itertools.combinations(range(4), r):
        # face: l_i = 0 for i not in Fc, sum l = 1; stationary points of q on the affine hull
        sub = {L[i]: 0 for i in range(4) if i not in Fc}
        free = [L[i] for i in Fc]
        expr = q(pt).subs(sub)
        lag = sp.Symbol('mu')
        eqs = [sp.diff(expr, x) - lag for x in free] + [sum(free) - 1]
        sols = sp.solve(eqs, free + [lag], dict=True)
        if not sols and r == 1:
            sols = [{free[0]: 1}]
        for so in sols:
            vals = [so.get(x, None) for x in free]
            if any(v is None for v in vals):
                # degenerate (flat direction): q is linear/constant along it; minima then lie on
                # lower-dimensional faces, which are enumerated separately
                continue
            if all(v.is_real and v >= 0 for v in vals):
                point = pt.subs(sub).subs(dict(zip(free, vals)))
                cands.append((q(point), tuple(Fc), point))
qmin = min(c[0] for c in cands)
argmins = [c for c in cands if c[0] == qmin]
check('(1) min over T* of q equals 0', qmin == 0)
check('(1) unique minimizer t0 = %s' % list(t0), all(sp.simplify(c[2] - t0) == sp.zeros(3, 1) for c in argmins))
check('(1) q(sbar) > 0', q(sb) > 0)

# ---------------------------------------------------------------- (2) relative interior of [v1, v2]
l1 = sp.symbols('l1')
sol = sp.solve(list(l1 * v1 + (1 - l1) * v2 - t0), l1, dict=True)
check('(2) t0 in relint [v1,v2]', len(sol) == 1 and 0 < sol[0][l1] < 1)
d = v1 - v2
check('(2) edge tangent: grad q(t0) . d = 0', sp.Matrix([-t0[1], -t0[0], 1]).dot(d) == 0)
check('(2) det M(d) = -dx dy > 0', -d[0] * d[1] > 0)
# KKT multipliers at the minimizer (w = 1): w + sigma P^T grad q(t*) - nu = 0 with nu = 0 on the support
gt = sp.Matrix([-t0[1], -t0[0], 1])
Pm = sp.Matrix.hstack(v1 - sb, v2 - sb, v3 - sb)
gP = Pm.T * gt
sig = -1 / gP[0]
nus = [1 + sig * gP[j] for j in range(3)]
check('(2) KKT: sigma = %s > 0, nu = %s (zero on rays 1, 2; ray 3 multiplier > 0)' % (sig, nus),
      sig > 0 and nus[0] == 0 and nus[1] == 0 and nus[2] > 0)

# ---------------------------------------------------------------- (3) generator pencil
J = sp.Matrix([[0, 1], [-1, 0]])
M = lambda s, h=1: sp.Matrix([[s[2], s[0]], [s[1], h]])
adj = lambda A: sp.Matrix([[A[1, 1], -A[0, 1]], [-A[1, 0], A[0, 0]]])
sym = lambda X: (X + X.T) / 2
G0 = J * adj(M(d, 0)); G1 = J * adj(M(t0))
# Lemma 13's sign criterion: M(t*) = a0 b0^T with a0 = (x0, 1), b0 = (y0, 1); F^T a0 = c b0 with c > 0.
# G1 a0 = 0, so c is determined by G0 a0 = c0 b0.
a0 = sp.Matrix([t0[0], 1]); b0 = sp.Matrix([t0[1], 1])
check('(3) M(t*) = a0 b0^T', M(t0) == a0 * b0.T)
Ga = G0 * a0
check('(3) G1 a0 = 0', G1 * a0 == sp.zeros(2, 1))
check('(3) G0 a0 parallel to b0', sp.simplify(Ga[0] * b0[1] - Ga[1] * b0[0]) == 0)
c0 = Ga[1] / b0[1]
print('   c0 = %s' % c0)
sgn = 1 if c0 > 0 else -1
G0, G1 = sgn * G0, sgn * G1
check('(3) sym(G0 M(t0)) is PSD rank one', sym(G0 * M(t0)).det() == 0 and sym(G0 * M(t0)).trace() > 0)
check('(3) G1 M(t0) = 0 (kappa does not move the tangency)', sym(G1 * M(t0)) == sp.zeros(2, 2))
kap = sp.symbols('kappa', real=True)
FT = G0 + kap * G1
check('(3) det F_kappa = det M(d) (constant, > 0)', sp.simplify(FT.det() - (-d[0] * d[1])) == 0)
E = sp.Matrix([[1, 0], [0, 0]])          # M(e_w, 0)


def A_of(v):
    return sym(FT * M(v))


Z = sym(FT * E)


def cert(v, which):
    """kappa_c = endpoint of the kappa-set of v in family (A); u = kernel of A_v(kappa_c).
    Returns kappa_c, affine data of u'A u and u'Z u in kappa."""
    Av = A_of(v)
    roots = sp.solve(sp.Eq(Av.det(), 0), kap)
    out = []
    for kc in roots:
        Ak = Av.subs(kap, kc)
        # PSD at kc?  (diagonal entries >= 0)
        if not (sp.simplify(Ak[0, 0]) >= 0 and sp.simplify(Ak[1, 1]) >= 0):
            continue
        ns = Ak.nullspace()
        if not ns:
            continue
        u = ns[0]
        aval = sp.simplify((u.T * Av * u)[0])            # affine in kappa
        zval = sp.simplify((u.T * Z * u)[0])
        out.append((sp.simplify(kc), u, sp.expand(aval), sp.expand(zval)))
    return out



# ---- (4A) family (A) alone: exact kappa-sets {kappa : sym(F_kappa^T M(v)) >= 0} and their intersection
from sympy import S as SS
setA = SS.Reals
for name, v in (('sbar', sb), ('v1', v1), ('v2', v2), ('v3', v3)):
    Av = A_of(v)
    sv = sp.solveset(Av[0, 0] >= 0, kap, SS.Reals).intersect(
        sp.solveset(Av[1, 1] >= 0, kap, SS.Reals)).intersect(sp.solveset(sp.expand(Av.det()) >= 0, kap, SS.Reals))
    print('   (A) kappa-set of %s: %s' % (name, sv))
    setA = setA.intersect(sv)
check('(4A) family (A): kappa-sets have empty intersection', setA == SS.EmptySet)

cs = cert(sb, 's'); c3 = cert(v3, '3')
print('   sbar endpoints:', [(c[0], sp.N(c[0], 12)) for c in cs])
print('   v3   endpoints:', [(c[0], sp.N(c[0], 12)) for c in c3])
found = False
for (ks, us, As, Zs) in cs:
    for (k3, u3, A3, Z3) in c3:
        if not sp.simplify(k3 - ks).is_negative:
            continue
        aS, bS = sp.Poly(As, kap).all_coeffs() if sp.Poly(As, kap).degree() == 1 else (0, As)
        zS1, zS0 = sp.Poly(Zs, kap).all_coeffs() if sp.Poly(Zs, kap).degree() == 1 else (0, Zs)
        a3, b3 = sp.Poly(A3, kap).all_coeffs() if sp.Poly(A3, kap).degree() == 1 else (0, A3)
        z31, z30 = sp.Poly(Z3, kap).all_coeffs() if sp.Poly(Z3, kap).degree() == 1 else (0, Z3)
        # sbar: need u_s'A u_s < 0 and u_s'Z u_s >= 0 for all kappa < ks
        condS = (sp.simplify(As.subs(kap, ks)) == 0 and sp.simplify(aS).is_positive
                 and sp.simplify(Zs.subs(kap, ks)).is_nonnegative and sp.simplify(zS1).is_nonpositive)
        cond3 = (sp.simplify(A3.subs(kap, k3)) == 0 and sp.simplify(a3).is_negative
                 and sp.simplify(Z3.subs(kap, k3)).is_nonnegative and sp.simplify(z31).is_nonnegative)
        print('   candidate pair: kappa_3 = %s < kappa_s = %s ; conditions sbar %s, v3 %s' % (k3, ks, condS, cond3))
        if condS and cond3:
            found = True
            print('   u_s =', list(us), '  u_s^T A u_s =', As, '  u_s^T Z u_s =', Zs)
            print('   u_3 =', list(u3), '  u_3^T A u_3 =', A3, '  u_3^T Z u_3 =', Z3)
check('(4) kappa-certificates exclude every kappa for both (A) and (B)', found)

# ---------------------------------------------------------------- (5) interior of projection
xy = [sp.Matrix(v[:2]) for v in verts]
p0 = sp.Matrix(t0[:2])
# interior iff p0 is a strict convex combination with all weights > 0 of some affinely spanning triple / or
# strictly inside the convex hull: check via all edges of the hull
import sympy.geometry as gm
hull = gm.convex_hull(*[gm.Point(*v) for v in xy])
check('(5) (x0,y0) strictly inside proj(T*)', hull.encloses_point(gm.Point(*p0)))
print('ALL PASS' if ok else 'SOME CHECK FAILED')
