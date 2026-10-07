"""Review r3: independent exact check of the embedded sfree brackets (note, after Corollary 7).

Does not import the stream's code.  For each sfree instance (coordinates (x, y, w), S = {w <= xy},
w = (1, 1, 1)) embedded as M = [[w, x], [y, 1]]:
  (1) z_K = 1: exact face enumeration of q = det M = w - xy over T* = conv{sbar, v1, v2, v3}
      (own parametrization; singular consistent faces are reported, not skipped silently), the
      unique zero is t*, and t* has cost exactly 1;
  (2) lower bound: own SDP for F, rounded to rationals, exact check that sym(F^T M(sbar)) is PD and
      sym(F^T M(v)) is PSD at the vertices of T_{z_lo} (so z_orbit >= z_lo);
  (3) upper bound: own SDP for Y_v, rounded, exactly projected onto {sum_v M(v) Y_v = 0}, exact PD
      check at the vertices of T_{z_up} (so z_orbit <= z_up, note Prop. 4).
z_lo and z_up are the values claimed in logs/certify_embed_brackets.log.
"""
import itertools
import sys
from fractions import Fraction as Fr

import cvxpy as cp
import numpy as np
import sympy as sp

INST = {
    'Thm14': dict(sbar=('-9/2', '0', '3/2'), v=[('-1', '-6', '18'), ('-5', '6', '-18'), ('0', '5/2', '5/2')],
                  t=('-3', '0', '0'), lo=Fr(9753853, 10 ** 7), up=Fr(1219233, 1250000)),
    'second': dict(sbar=('-1/2', '1/2', '1'), v=[('1/2', '-4', '-1/2'), ('-10', '3', '24'), ('9/2', '1/2', '15/2')],
                   t=('-1', '-3', '3'), lo=Fr(8347663, 10 ** 7), up=Fr(2086943, 2500000)),
    'Prop16': dict(sbar=('-2', '3', '2'), v=[('0', '0', '0'), ('6', '-2', '1/4'), ('1', '-5/2', '1/2')],
                   t=('0', '0', '0'), lo=Fr(1967693, 2000000), up=Fr(2459617, 2500000)),
}
ok_all = True


def report(name, cond):
    global ok_all
    ok_all &= bool(cond)
    print(('PASS ' if cond else 'FAIL ') + name, flush=True)


def Mx(p):
    """sfree point (x, y, w) -> 2x2 matrix [[w, x], [y, 1]] (exact)."""
    x, y, w = p
    return sp.Matrix([[w, x], [y, 1]])


def q(p):
    x, y, w = p
    return w - x * y


def psd2(A, strict=False):
    a, b, c = A[0, 0], (A[0, 1] + A[1, 0]) / 2, A[1, 1]
    if strict:
        return a > 0 and a * c - b * b > 0
    return a >= 0 and c >= 0 and a * c - b * b >= 0


def zk_check(name, sb, vs, t):
    """Exact min of q over conv(sb, v1, v2, v3) by face enumeration in affine coordinates."""
    verts = [sb] + vs
    mu = sp.symbols('m1:4')
    cands, singular = [], []
    for r in range(1, 5):
        for face in itertools.combinations(range(4), r):
            base = sp.Matrix(verts[face[0]])
            dirs = [sp.Matrix(verts[k]) - base for k in face[1:]]
            m = mu[:r - 1]
            pt = base + sum((m[i] * dirs[i] for i in range(r - 1)), sp.zeros(3, 1))
            f = sp.expand(q(list(pt)))
            if r == 1:
                cands.append((f, face, pt))
                continue
            eqs = [sp.diff(f, mi) for mi in m]
            Hm = sp.Matrix([[sp.diff(f, a, b) for b in m] for a in m])
            sol = sp.solve(eqs, m, dict=True)
            if Hm.det() == 0:
                # singular face: record any consistent critical set and its (constant) value
                for s in sol:
                    val = sp.simplify(f.subs(s))
                    singular.append((face, s, val))
                continue
            for s in sol:
                mv = [s[mi] for mi in m]
                if all(x > 0 for x in mv) and sum(mv) < 1:
                    cands.append((f.subs(s), face, pt.subs(s)))
    mn = min(c[0] for c in cands)
    arg = {tuple(c[2]) for c in cands if c[0] == mn}
    tt = tuple(sp.Rational(x) for x in t)
    report('%s: min q over T* = %s, unique minimizer t* = %s' % (name, mn, [str(x) for x in tt]),
           mn == 0 and arg == {tt})
    for face, s, val in singular:
        print('   singular face %s, critical set %s, value %s' % (face, s, val))
    report('%s: no singular face has a critical set with value <= 0' % name,
           all(not (v.is_number and v <= 0) for _, _, v in singular))
    # cost of t*: barycentric weights in conv(sb, v1, v2, v3); cost = 1 - weight of sbar
    lam = sp.symbols('l0:4')
    eqs = [sum(lam[k] * verts[k][c] for k in range(4)) - tt[c] for c in range(3)] + [sum(lam) - 1]
    sol = sp.solve(eqs, lam, dict=True)
    report('%s: t* has barycentric weight 0 on sbar (cost 1): %s' % (name, sol),
           len(sol) == 1 and sol[0][lam[0]] == 0 and all(sol[0][lam[k]] >= 0 for k in range(1, 4)))


def lower(name, sb, vs, z):
    verts = [tuple(sb[c] + z * (v[c] - sb[c]) for c in range(3)) for v in vs]
    Ms = Mx(sb)
    Mv = [Mx(v) for v in verts]
    num = lambda A: np.array(A.tolist(), dtype=float)
    F = cp.Variable((2, 2))
    t = cp.Variable()
    S = lambda A: (F.T @ num(A) + (F.T @ num(A)).T) / 2
    cons = [S(Ms) >> np.eye(2)] + [S(A) >> t * np.eye(2) for A in Mv] + [t <= 1]
    cp.Problem(cp.Maximize(t), cons).solve(solver='CLARABEL')
    print('   lower SDP at z = %.7f: t = %.3e' % (float(z), t.value))
    for den in (10 ** 8, 10 ** 10, 10 ** 12, 10 ** 14):
        Fq = sp.Matrix(2, 2, lambda i, j: sp.Rational(Fr(float(F.value[i, j])).limit_denominator(den)))
        if psd2(Fq.T * Ms, strict=True) and all(psd2(Fq.T * A) for A in Mv):
            report('%s: rational F (den %d) with T_{z_lo} in C_F, z_lo = %s; F^T = %s' % (
                name, den, z, Fq.T.tolist()), True)
            return True
    report('%s: lower certificate at z_lo = %s' % (name, z), False)
    return False


def upper(name, sb, vs, z):
    verts = [tuple(sp.Rational(x) for x in sb)] + [tuple(sb[c] + z * (v[c] - sb[c]) for c in range(3)) for v in vs]
    Ms = [Mx(v) for v in verts]
    # unknowns y = (Y00, Y01, Y11) per vertex; equations: sum_v M_v Y_v = 0 (4 scalar equations)
    rows = []
    for (i, j) in ((0, 0), (0, 1), (1, 0), (1, 1)):
        row = []
        for M in Ms:
            # (M Y)_{ij} = M_i0 Y_0j + M_i1 Y_1j
            c = [0, 0, 0]
            # Y_0j: j=0 -> Y00 (idx 0), j=1 -> Y01 (idx 1); Y_1j: j=0 -> Y01 (idx 1), j=1 -> Y11 (idx 2)
            c[0 if j == 0 else 1] += M[i, 0]
            c[1 if j == 0 else 2] += M[i, 1]
            row += c
        rows.append(row)
    A = sp.Matrix(rows)
    An = np.array(A.tolist(), dtype=float)
    Ys = [cp.Variable((2, 2), symmetric=True) for _ in Ms]
    t = cp.Variable()
    yv = cp.hstack([cp.hstack([Y[0, 0], Y[0, 1], Y[1, 1]]) for Y in Ys])
    cons = [Y >> t * np.eye(2) for Y in Ys] + [An @ yv == 0, sum(cp.trace(Y) for Y in Ys) == 1]
    cp.Problem(cp.Maximize(t), cons).solve(solver='CLARABEL')
    print('   upper SDP at z = %.7f: t = %.3e' % (float(z), t.value))
    y0 = np.concatenate([[Y.value[0, 0], Y.value[0, 1], Y.value[1, 1]] for Y in Ys])
    AAt_inv = (A * A.T).inv()
    for den in (10 ** 8, 10 ** 10, 10 ** 12, 10 ** 14):
        yq = sp.Matrix([sp.Rational(Fr(float(x)).limit_denominator(den)) for x in y0])
        y = yq - A.T * (AAt_inv * (A * yq))
        assert A * y == sp.zeros(4, 1)
        Yq = [sp.Matrix([[y[3 * k], y[3 * k + 1]], [y[3 * k + 1], y[3 * k + 2]]]) for k in range(len(Ms))]
        if all(psd2(Y, strict=True) for Y in Yq):
            report('%s: rational PD Y_v (den %d) with sum M(v) Y_v = 0 at z_up = %s (so z_orbit <= z_up)' % (
                name, den, z), True)
            return True
    report('%s: upper certificate at z_up = %s' % (name, z), False)
    return False


for name, d in INST.items():
    sb = tuple(sp.Rational(x) for x in d['sbar'])
    vs = [tuple(sp.Rational(x) for x in v) for v in d['v']]
    print('== %s: sbar %s, det M(sbar) = q(sbar) = %s' % (name, [str(x) for x in sb], q(sb)), flush=True)
    report('%s: q(sbar) > 0' % name, q(sb) > 0)
    zk_check(name, sb, vs, d['t'])
    lower(name, sb, vs, sp.Rational(d['lo']))
    upper(name, sb, vs, sp.Rational(d['up']))
    print('   bracket [%.7f, %.7f]' % (float(d['lo']), float(d['up'])))
print('ALL PASS' if ok_all else 'SOME CHECK FAILED')
sys.exit(0 if ok_all else 1)
