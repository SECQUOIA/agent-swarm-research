"""Exact certificates for support-one instances (S = {w <= x y}, costs 1, T* = conv{sbar, v1, v2, v3},
t* = v1).  Used for
  (a) the threshold family of Proposition C3: sbar = (3/2, -1/2, 1/4 - d), t* = (0,0,0),
      v2 = (1/2, 3/2, 1 - d), v3 = (3, 1, 4 - d) with d = 1/100, 1/1000, 1/10000
      (non-exact, cylinder parameter H_cyl >= 1 - 4 d);
  (b) the scaled Proposition 16 of the sfree note, (x, y, w) -> (k x, k y, k^2 w), k = 10, 100
      (non-exact, edge cosines at t* close to 1).
For each instance, exactly (sympy):
  (1) min over T* of q is 0, attained only at t*; z_K = 1 with support {1}; edges at t* transversal;
  (2) rational positive definite Y_v with sum_v M(v) Y_v = 0, and sym(F^T M(v)) = 0 for all v forces F = 0,
      so no nonzero F has C_F containing T*, hence (compactness, as in the sfree note's Prop. 16)
      z_A < z_K, and z_B < z_K is NOT implied (family B is checked numerically only).
Also prints the exact value 4 h_v / (x_v + y_v)^2 (cylinder t = 1) and the edge cosines at t*."""
import itertools
import sys
import numpy as np
import sympy as sp
import cvxpy as cp

R = sp.Rational


def qf(s):
    return s[2] - s[0] * s[1]


def Mf(s):
    return sp.Matrix([[s[2], s[0]], [s[1], 1]])


def certify(name, verts):
    ok = True

    def check(msg, cond):
        nonlocal ok
        ok &= bool(cond)
        print(('PASS ' if cond else 'FAIL ') + msg)
    print('==', name, [list(v) for v in verts])
    sb, t0 = verts[0], verts[1]
    # (1) face enumeration of q on T* (barycentric coordinates)
    L = sp.symbols('l0:4')
    pt = sum((L[i] * verts[i] for i in range(4)), sp.zeros(3, 1))
    cands = []
    for r in range(1, 5):
        for Fc in itertools.combinations(range(4), r):
            sub = {L[i]: 0 for i in range(4) if i not in Fc}
            free = [L[i] for i in Fc]
            expr = sp.expand(qf(pt).subs(sub))
            mu = sp.Symbol('mu')
            eqs = [sp.diff(expr, x) - mu for x in free] + [sum(free) - 1]
            sols = sp.solve(eqs, free + [mu], dict=True) if r > 1 else [{free[0]: 1}]
            for so in sols:
                vals = [so.get(x) for x in free]
                if any(v is None for v in vals):
                    continue
                vals = [sp.sympify(v) for v in vals]
                if all(v.is_real and v >= 0 for v in vals):
                    cands.append((sp.nsimplify(qf(pt.subs(sub).subs(dict(zip(free, vals))))), Fc, tuple(vals)))
    qmin = min(c[0] for c in cands)
    arg = [c for c in cands if c[0] == qmin]
    check('(1) q(sbar) = %s > 0' % qf(sb), qf(sb) > 0)
    check('(1) min over T* of q = %s' % qmin, qmin == 0)
    check('(1) unique minimizer is t* = v1', all(c[1] == (1,) for c in arg))
    gt = sp.Matrix([-t0[1], -t0[0], 1])
    hs = []
    for nm, v in (('sbar', verts[0]), ('v2', verts[2]), ('v3', verts[3])):
        h = gt.dot(v - t0)
        hs.append(h)
        check('(1) transversal edge at t*: grad q(t*).(%s - t*) = %s > 0' % (nm, h), h > 0)
    P = sp.Matrix.hstack(*[v - sb for v in verts[1:]])
    check('(1) det P = %s != 0' % P.det(), P.det() != 0)
    cyl = [sp.nsimplify(4 * gt.dot(v - t0) / ((v - t0)[0] + (v - t0)[1]) ** 2) for v in (verts[0], verts[2], verts[3])]
    print('   cylinder t = 1: 4 h_v / (x_v + y_v)^2 =', cyl, ' -> H_cyl >=', min(cyl), '=', float(min(cyl)))
    cosv = [float(gt.dot(v - t0) / (gt.norm() * (v - t0).norm())) for v in (verts[0], verts[2], verts[3])]
    print('   edge cosines at t* (with grad q(t*)):', [round(c, 6) for c in cosv])
    # (2) PD certificate
    Ms = [Mf(v) for v in verts]
    Mn = [np.array(m.tolist(), dtype=float) for m in Ms]
    Y = [cp.Variable((2, 2), symmetric=True) for _ in range(4)]
    t = cp.Variable()
    scale = [1.0 / max(1.0, np.abs(m).max()) for m in Mn]
    cons = [Y[i] - t * np.eye(2) >> 0 for i in range(4)] + [sum(Mn[i] @ Y[i] for i in range(4)) == 0,
                                                           sum(cp.trace(Y[i]) for i in range(4)) == 1]
    pr = cp.Problem(cp.Maximize(t), cons)
    pr.solve(solver='CLARABEL')
    print('   SDP: max min-eigenvalue of a certificate = %.3e (status %s)' % (t.value, pr.status))
    syms = sp.symbols('y0:12')
    Ysym = [sp.Matrix([[syms[3 * i], syms[3 * i + 1]], [syms[3 * i + 1], syms[3 * i + 2]]]) for i in range(4)]
    eqs = list(sum((Ms[i] * Ysym[i] for i in range(4)), sp.zeros(2, 2)))
    num = {}
    for i in range(4):
        Yv = Y[i].value
        for k, (a, b) in enumerate(((0, 0), (0, 1), (1, 1))):
            num[syms[3 * i + k]] = sp.Rational(Yv[a, b]).limit_denominator(10 ** 14)
    A_, b_ = sp.linear_eq_to_matrix(eqs, syms)
    piv = A_.rref()[1]
    pivots = [syms[j] for j in piv]
    others = {s: num[s] for s in syms if s not in pivots}
    sol = sp.solve([e.subs(others) for e in eqs], pivots, dict=True)[0]
    full = {**others, **sol}
    Yex = [Yi.subs(full) for Yi in Ysym]
    check('(2) sum_v M(v) Y_v = 0 exactly', sum((Ms[i] * Yex[i] for i in range(4)), sp.zeros(2, 2)) == sp.zeros(2, 2))
    check('(2) all Y_v positive definite (exact)', all(Yi[0, 0] > 0 and Yi.det() > 0 for Yi in Yex))
    print('   min eigenvalue (float) of the exact certificate: %.3e' %
          min(np.linalg.eigvalsh(np.array(Yi.tolist(), dtype=float))[0] for Yi in Yex))
    F = sp.Matrix(2, 2, sp.symbols('f0:4'))
    lin = []
    for m in Ms:
        X = F.T * m
        lin += list(X + X.T)
    sol0 = sp.solve(lin, list(F), dict=True)
    check('(2) sym(F^T M(v)) = 0 for all v forces F = 0',
          sol0 == [{s: 0 for s in F}] or all(all(v == 0 for v in s_.values()) for s_ in sol0))
    print('ALL PASS' if ok else 'SOME CHECK FAILED')
    return ok


if __name__ == '__main__':
    allok = True
    for d in (R(1, 100), R(1, 1000), R(1, 10000)):
        verts = [sp.Matrix([R(3, 2), R(-1, 2), R(1, 4) - d]), sp.Matrix([0, 0, 0]),
                 sp.Matrix([R(1, 2), R(3, 2), 1 - d]), sp.Matrix([3, 1, 4 - d])]
        allok &= certify('threshold family d = %s' % d, verts)
    base = [sp.Matrix([-2, 3, 2]), sp.Matrix([0, 0, 0]), sp.Matrix([6, -2, R(1, 4)]), sp.Matrix([1, R(-5, 2), R(1, 2)])]
    for k in (1, 10, 100):
        verts = [sp.Matrix([k * v[0], k * v[1], k * k * v[2]]) for v in base]
        allok &= certify('sfree Proposition 16 scaled by (k x, k y, k^2 w), k = %d' % k, verts)
    print('OVERALL', 'ALL PASS' if allok else 'SOME CHECK FAILED')
