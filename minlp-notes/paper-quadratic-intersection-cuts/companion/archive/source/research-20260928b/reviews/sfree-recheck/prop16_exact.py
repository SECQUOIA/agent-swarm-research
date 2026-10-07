"""Independent exact recheck of Proposition 16 (sfree note, revised 2026-09-29).

Setting (re-derived from the note, Sections 1 and 8):
  S = {(x, y, w) : q = w - xy <= 0}, M(x, y, w) = [[w, x], [y, 1]] (so det M = q on the slice h = 1).
  Corner: sbar, rays p_j = v_j - sbar, costs w = (1, 1, 1).  z_K = min{sum lam : lam >= 0, q(sbar + P lam) <= 0}.
  Family (A): C_F = {M : sym(F^T M) >= 0}, det F > 0; the cut of C_F cap H gives
  z_{C_F} = min_j w_j alpha_j, and z_{C_F} >= z iff sym(F^T M(v)) >= 0 at the vertices
  v of T_z = conv{sbar, sbar + z p_j} (with sym(F^T M(sbar)) > 0 for sbar in the interior).
  z_A = sup_F z_{C_F}.

Checks (exact rational arithmetic unless marked 'float'):
  (1) z_K = 1 with unique minimizer lam = e1 (t* = v1 = 0), by a radial argument different from the
      note's face enumeration: t* = 0, so q(r f) = r (f_w - r f_x f_y) for f in the far face
      F* = conv{sbar, v2, v3}; hence q > 0 on T* minus {0} iff f_w > 0 on F* and q > 0 on F*.
      min over the triangle F* of q is computed exactly (vertices, edge stationary points, interior).
      Transversality, KKT multipliers (own derivation).
  (2) A positive definite certificate Y_v with sum_v M(v) Y_v = 0, built from an exact rational basis
      of the kernel (not by projecting onto pivots), rounded to small denominators.
  (3) Linear system sym(F^T M(v)) = 0 for all v forces F = 0.
  (4) Extra: exact bracket for z_A: a rational F with det F > 0 containing T_{z_lo} (sbar strictly
      inside) and a PD dual certificate at T_{z_hi}.
"""
from fractions import Fraction as Fr
import itertools
import numpy as np
import sympy as sp
import cvxpy as cp

R = sp.Rational
sb = sp.Matrix([-2, 3, 2])
v1 = sp.Matrix([0, 0, 0])
v2 = sp.Matrix([6, -2, R(1, 4)])
v3 = sp.Matrix([1, R(-5, 2), R(1, 2)])
q = lambda s: s[2] - s[0] * s[1]
M = lambda s: sp.Matrix([[s[2], s[0]], [s[1], 1]])
ok = True


def check(name, cond):
    global ok
    ok &= bool(cond)
    print(('PASS ' if cond else 'FAIL ') + name, flush=True)


def is_pd(Y):
    return Y[0, 0] > 0 and Y.det() > 0


def is_psd2(Y):
    return Y[0, 0] >= 0 and Y[1, 1] >= 0 and Y.det() >= 0


# ------------------------------------------------------------------ (1) z_K, minimizer
P = sp.Matrix.hstack(v1 - sb, v2 - sb, v3 - sb)
check('det P = %s != 0 (rays linearly independent)' % P.det(), P.det() != 0)
check('q(sbar) = %s > 0' % q(sb), q(sb) > 0)
check('q(t*) = q(v1) = %s' % q(v1), q(v1) == 0)
# far face F* = conv{sbar, v2, v3}; f_w on its vertices
fw = [sb[2], v2[2], v3[2]]
check('f_w > 0 on the far face (vertex values %s)' % fw, min(fw) > 0)
a_, b_ = sp.symbols('a b', real=True)
f = sb + a_ * (v2 - sb) + b_ * (v3 - sb)          # a, b >= 0, a + b <= 1
qf = sp.expand(q(f))
cands = []
# vertices
for (A0, B0) in ((0, 0), (1, 0), (0, 1)):
    cands.append((qf.subs({a_: A0, b_: B0}), ('vertex', A0, B0)))
# edges: b = 0; a = 0; a + b = 1
t = sp.Symbol('t', real=True)
for name, sub in (('b=0', {a_: t, b_: 0}), ('a=0', {a_: 0, b_: t}), ('a+b=1', {a_: t, b_: 1 - t})):
    e = sp.expand(qf.subs(sub))
    for r in sp.solve(sp.diff(e, t), t):
        if r.is_real and 0 <= r <= 1:
            cands.append((e.subs(t, r), ('edge ' + name, r)))
# interior stationary point (only a minimum if the Hessian is PSD)
Hs = sp.hessian(qf, (a_, b_))
sol = sp.solve([sp.diff(qf, a_), sp.diff(qf, b_)], [a_, b_], dict=True)
print('   Hessian of q on the far face:', Hs.tolist(), ' eigenvalues:', [sp.nsimplify(e) for e in Hs.eigenvals()])
for so in sol:
    A0, B0 = so[a_], so[b_]
    if A0 >= 0 and B0 >= 0 and A0 + B0 <= 1:
        cands.append((qf.subs(so), ('interior', A0, B0)))
qmin_face = min(c[0] for c in cands)
print('   candidates on the far face:', [(c[1], c[0]) for c in cands])
check('min over far face of q = %s > 0' % qmin_face, qmin_face > 0)
# consequence: q > 0 on T* \ {t*}; z_K = 1; unique minimizer lam = e1
# KKT at lam = e1: grad q(t*) = (-y, -x, 1) = (0, 0, 1)
g = sp.Matrix([-v1[1], -v1[0], 1])
Pg = P.T * g
sigma = R(1) / (-Pg[0])
nu = [1 + sigma * Pg[j] for j in range(3)]
check('grad q(t*) = %s; edge slopes grad.(v - t*) = %s (all > 0: transversal)'
      % (list(g), [g.dot(v - v1) for v in (sb, v2, v3)]), all(g.dot(v - v1) > 0 for v in (sb, v2, v3)))
check('KKT: sigma = %s, multipliers nu = %s (nu_1 = 0, nu_2, nu_3 > 0)' % (sigma, nu),
      sigma > 0 and nu[0] == 0 and nu[1] > 0 and nu[2] > 0)
check('Theorem 1(4) condition grad q(t*).(sbar - t*) = %s > 0' % g.dot(sb - v1), g.dot(sb - v1) > 0)

# ------------------------------------------------------------------ (2) dual certificate


def certificate(verts, denoms=(1, 2, 4, 5, 10, 20, 100, 1000, 10 ** 4, 10 ** 6), solver='SCS'):
    """PD Y_v with sum M(v) Y_v = 0 via an exact kernel basis; returns (Y list, sdp margin)."""
    Ms = [M(v) for v in verts]
    ys = sp.symbols('y0:%d' % (3 * len(verts)))
    Ysym = [sp.Matrix([[ys[3 * i], ys[3 * i + 1]], [ys[3 * i + 1], ys[3 * i + 2]]]) for i in range(len(verts))]
    eqs = list(sum((Ms[i] * Ysym[i] for i in range(len(verts))), sp.zeros(2, 2)))
    A, _ = sp.linear_eq_to_matrix(eqs, ys)
    K = A.nullspace()                       # exact rational basis
    Kn = np.array([[float(x) for x in k] for k in K]).T   # 12 x dim
    c = cp.Variable(len(K)); tt = cp.Variable()
    yv = Kn @ c
    cons = []
    for i in range(len(verts)):
        Yi = cp.bmat([[yv[3 * i], yv[3 * i + 1]], [yv[3 * i + 1], yv[3 * i + 2]]])
        cons.append((Yi + Yi.T) / 2 - tt * np.eye(2) >> 0)
    cons.append(sum(yv[3 * i] + yv[3 * i + 2] for i in range(len(verts))) == 1)
    cp.Problem(cp.Maximize(tt), cons).solve(solver=solver)
    cnum = c.value / np.max(np.abs(c.value))
    for D in denoms:
        cr = [R(Fr(float(x)).limit_denominator(D).numerator, Fr(float(x)).limit_denominator(D).denominator) for x in cnum]
        yex = sum((cr[k] * K[k] for k in range(len(K))), sp.zeros(3 * len(verts), 1))
        Y = [sp.Matrix([[yex[3 * i], yex[3 * i + 1]], [yex[3 * i + 1], yex[3 * i + 2]]]) for i in range(len(verts))]
        if all(is_pd(Yi) for Yi in Y):
            # clear denominators for display
            L = sp.ilcm(*[sp.fraction(x)[1] for Yi in Y for x in Yi])
            Y = [Yi * L for Yi in Y]
            S = sum((Ms[i] * Y[i] for i in range(len(verts))), sp.zeros(2, 2))
            return Y, float(tt.value), D, S
    return None, float(tt.value), None, None


verts = [sb, v1, v2, v3]
Y, marg, D, S = certificate(verts)
print('   SDP margin (max min-eigenvalue, trace-normalized): %.4e' % marg)
check('PD certificate found with coefficient denominators <= %s' % D, Y is not None)
if Y is not None:
    for nm, Yi in zip(('sbar', 'v1', 'v2', 'v3'), Y):
        print('   Y_%s = %s   (Y11 = %s, det = %s)' % (nm, Yi.tolist(), Yi[0, 0], Yi.det()))
    check('sum_v M(v) Y_v = 0 exactly', S == sp.zeros(2, 2))
    check('all Y_v positive definite (exact)', all(is_pd(Yi) for Yi in Y))

# ------------------------------------------------------------------ (3) sym(F^T M(v)) = 0 => F = 0
Fs = sp.Matrix(2, 2, sp.symbols('f0:4'))
lin = []
for v in verts:
    X = Fs.T * M(v)
    lin += list(X + X.T)
Al, _ = sp.linear_eq_to_matrix(lin, list(Fs))
check('linear system sym(F^T M(v)) = 0 (all v) has rank %d = 4, so F = 0' % Al.rank(), Al.rank() == 4)

# identity used in the proof: sum_v <sym(F^T M(v)), Y_v> = tr(F^T sum_v M(v) Y_v)
if Y is not None:
    ident = sp.expand(sum(((Fs.T * M(v) + (Fs.T * M(v)).T) / 2 * Yi).trace() for v, Yi in zip(verts, Y))
                      - (Fs.T * sum((M(v) * Yi for v, Yi in zip(verts, Y)), sp.zeros(2, 2))).trace())
    check('identity sum <sym(F^T M(v)), Y_v> = tr(F^T sum M(v) Y_v) holds symbolically', ident == 0)

# ------------------------------------------------------------------ (4) exact bracket for z_A


def Tz(z):
    return [sb] + [sb + z * (v - sb) for v in (v1, v2, v3)]


def lower_F(z, solver='CLARABEL'):
    Mf = [np.array(M(v).tolist(), dtype=float) for v in Tz(z)]
    Fv = cp.Variable((2, 2)); tt = cp.Variable()
    cons = []
    for m in Mf:
        X = Fv.T @ m
        cons.append((X + X.T) / 2 - tt * np.eye(2) >> 0)
    cons.append(cp.norm(Fv, 'fro') <= 1)
    cp.Problem(cp.Maximize(tt), cons).solve(solver=solver)
    Fn = Fv.value / np.max(np.abs(Fv.value))
    for Dd in (10, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 8):
        Fr_ = sp.Matrix(2, 2, [R(Fr(float(x)).limit_denominator(Dd).numerator, Fr(float(x)).limit_denominator(Dd).denominator) for x in Fn.flatten()])
        mats = [(Fr_.T * M(v) + (Fr_.T * M(v)).T) / 2 for v in Tz(z)]
        if is_pd(mats[0]) and all(is_psd2(mm) for mm in mats[1:]) and Fr_.det() > 0:
            return Fr_, float(tt.value)
    return None, float(tt.value)


for zlo in (R(98, 100), R(983, 1000), R(9838, 10000)):
    Fl, m_ = lower_F(zlo)
    check('lower bound: rational F = %s (det %s > 0) has sym(F^T M) PD at sbar and PSD at the vertices of T_z, z = %s (SDP margin %.2e)'
          % (None if Fl is None else Fl.tolist(), None if Fl is None else Fl.det(), zlo, m_), Fl is not None)
for zhi in (R(99, 100), R(985, 1000), R(9839, 10000)):
    Yh, mh, Dh, Sh = certificate(Tz(zhi))
    good = Yh is not None and Sh == sp.zeros(2, 2) and all(is_pd(Yi) for Yi in Yh)
    check('upper bound: exact PD certificate at T_z, z = %s (SDP margin %.2e, denominators <= %s): no F != 0 contains T_z'
          % (zhi, mh, Dh), good)

print('ALL PASS' if ok else 'SOME CHECK FAILED')
