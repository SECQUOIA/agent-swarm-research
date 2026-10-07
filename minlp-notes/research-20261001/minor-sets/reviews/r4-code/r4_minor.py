"""Review r4 (minor-sets): independent exact checks. Imports none of the stream's code.

1. Instance B (note Section 6): z_K = 1 by exact face enumeration of det over T*, and the orbit
   bracket [0.9219403, 0.9219593] by my own SDP certificates, rounded and checked exactly:
   lower end: rational F^T with det F^T > 0, sym(F^T M(sbar)) > 0 and sym(F^T M(v)) >= 0 on the
   vertices of T_{z_lo};
   upper end: rational positive definite Y_v (v = sbar and the vertices of T_{z_up}) with
   sum_v M(v) Y_v = 0; then sum_v <sym(F^T M(v)), Y_v> = 0 for every F, so no F works at z_up.
2. The certificates printed by code/certify_embed_brackets.py in logs/certify_embed_brackets_rev3.log
   are parsed and checked with the same exact checker (embedded sfree data, M = [[w, x], [y, h]]).
"""
import ast
import itertools
import re
import sys
from fractions import Fraction as Fr

import cvxpy as cp
import numpy as np
import sympy as sp

OK = True


def chk(msg, cond):
    global OK
    OK &= bool(cond)
    print(('PASS ' if cond else 'FAIL ') + msg, flush=True)


def M(s):
    return [[s[0], s[1]], [s[2], s[3]]]


def det(s):
    return s[0] * s[3] - s[1] * s[2]


def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def sym(A):
    return [[A[0][0], (A[0][1] + A[1][0]) / 2], [(A[0][1] + A[1][0]) / 2, A[1][1]]]


def psd(S, strict=False):
    d = S[0][0] * S[1][1] - S[0][1] ** 2
    if strict:
        return S[0][0] > 0 and d > 0
    return S[0][0] >= 0 and S[1][1] >= 0 and d >= 0


def verts(sb, P, z):
    return [sb] + [tuple(sb[i] + z * p[i] for i in range(4)) for p in P]


def check_lower(FT, sb, P, z):
    V = verts(sb, P, z)
    return (det([FT[0][0], FT[0][1], FT[1][0], FT[1][1]]) > 0
            and psd(sym(mul(FT, M(sb))), strict=True)
            and all(psd(sym(mul(FT, M(v)))) for v in V[1:]))


def check_upper(Ys, sb, P, z):
    V = verts(sb, P, z)
    tot = [[sum(mul(M(v), Y)[i][j] for v, Y in zip(V, Ys)) for j in range(2)] for i in range(2)]
    return all(Y[0][1] == Y[1][0] and psd(Y, strict=True) for Y in Ys) and all(
        tot[i][j] == 0 for i in range(2) for j in range(2))


def rat(x, den=10 ** 10):
    return Fr(int(round(x * den)), den)


def sdp_lower(sb, P, z):
    V = [np.array([[float(a) for a in M(v)[0]], [float(a) for a in M(v)[1]]]) for v in verts(sb, P, z)]
    FT, t = cp.Variable((2, 2)), cp.Variable()
    cons = [cp.abs(FT) <= 1]
    for Mv in V:
        E = FT @ Mv
        cons.append((E + E.T) / 2 - t * np.eye(2) >> 0)
    cp.Problem(cp.Maximize(t), cons).solve(solver='CLARABEL')
    return [[rat(FT.value[i, j]) for j in range(2)] for i in range(2)], t.value


def sdp_upper(sb, P, z):
    z = Fr(z)  # exact z for the projection below
    V = [np.array([[float(a) for a in M(v)[0]], [float(a) for a in M(v)[1]]]) for v in verts(sb, P, z)]
    Ys = [cp.Variable((2, 2), symmetric=True) for _ in V]
    t = cp.Variable()
    cons = [sum(Mv @ Y for Mv, Y in zip(V, Ys)) == 0, sum(cp.trace(Y) for Y in Ys) == 1]
    cons += [Y - t * np.eye(2) >> 0 for Y in Ys]
    cp.Problem(cp.Maximize(t), cons).solve(solver='CLARABEL')
    Yr = [[[rat(Y.value[i, j]) for j in range(2)] for i in range(2)] for Y in Ys]
    # exact orthogonal projection of (y11, y12, y22) per vertex onto {sum_v M(v) Y_v = 0}
    Vx = verts(sb, P, z)
    n = len(Vx)
    rows = []
    for i in range(2):
        for j in range(2):
            row = []
            for v in Vx:
                m = M(v)  # (M Y)_{ij} = m_i0 Y_0j + m_i1 Y_1j
                c11 = m[i][0] if j == 0 else 0
                c22 = m[i][1] if j == 1 else 0
                c12 = (m[i][1] if j == 0 else 0) + (m[i][0] if j == 1 else 0)
                row += [c11, c12, c22]
            rows.append(row)
    A = sp.Matrix(rows)
    y = sp.Matrix([v for Y in Yr for v in (Y[0][0], Y[0][1], Y[1][1])])
    y = y - A.T * (A * A.T).LUsolve(A * y)
    Yp = []
    for k in range(n):
        a, b, c = (Fr(int(sp.fraction(q)[0]), int(sp.fraction(q)[1])) for q in y[3 * k:3 * k + 3])
        Yp.append([[a, b], [b, c]])
    return Yp, t.value


def min_det_faces(sb, P):
    """Minimum of q(lam) = det(sb + P lam) over {lam >= 0, sum lam <= 1}, by exact enumeration of
    the relative interiors of all faces. Returns list of (value, point or None, note)."""
    lam = sp.symbols('l0:4')
    s = [sp.Rational(str(sb[i])) + sum(sp.Rational(str(P[j][i])) * lam[j] for j in range(4)) for i in range(4)]
    q = sp.expand(s[0] * s[3] - s[1] * s[2])
    out = []
    for k in range(0, 5):
        for S in itertools.combinations(range(4), k):
            for top in (False, True):
                if top and k == 0:
                    continue
                sub = {lam[j]: 0 for j in range(4) if j not in S}
                qs = q.subs(sub)
                vs = [lam[j] for j in S]
                mu = sp.Symbol('mu')
                eqs = [sp.diff(qs, v) - (mu if top else 0) for v in vs]
                unk = vs + ([mu] if top else [])
                if top:
                    eqs.append(sum(vs) - 1)
                if not unk:
                    out.append((qs, (), 'vertex'))
                    continue
                sol = sp.linsolve(eqs, unk)
                if sol == sp.EmptySet:
                    continue
                (pt,) = list(sol)
                free = set().union(*[sp.sympify(e).free_symbols for e in pt]) - {mu}
                pt_l = pt[:len(vs)]
                if free:
                    # singular face: q is constant on the critical affine set
                    val = sp.simplify(qs.subs(dict(zip(vs, pt_l))))
                    out.append((val, None, 'singular face %s top=%s' % (S, top)))
                    continue
                if all(x > 0 for x in pt_l) and (top or sum(pt_l) < 1):
                    full = [0] * 4
                    for j, x in zip(S, pt_l):
                        full[j] = x
                    out.append((qs.subs(dict(zip(vs, pt_l))), tuple(full), 'face %s top=%s' % (S, top)))
    return out


def instance_B():
    print('=== Instance B ===', flush=True)
    F = lambda t: tuple(Fr(x) for x in t)
    sb = F(('-3', '-5/2', '1/2', '-2'))
    V = [F(('1', '1', '-7', '-4')), F(('-1/2', '-1/2', '-11/2', '-7')), F(('1/2', '1', '-5/2', '0')),
         F(('-7/2', '4', '-7/2', '2'))]
    tstar = F(('0', '0', '-6', '-6'))
    P = [tuple(v[i] - sb[i] for i in range(4)) for v in V]
    chk('det sbar = %s > 0' % det(sb), det(sb) > 0)
    dP = sp.Matrix([[sp.Rational(str(p[i])) for p in P] for i in range(4)]).det()
    chk('det[p1..p4] = %s != 0' % dP, dP != 0)
    res = min_det_faces(sb, P)
    vals = [r for r in res if r[1] is not None or r[2] == 'vertex']
    sing = [r for r in res if r[1] is None and r[2] != 'vertex']
    m = min(r[0] for r in res)
    argm = [r for r in res if r[0] == m]
    print('   critical values: %d, singular faces: %s' % (len(res), [(str(v), n) for v, _, n in sing]))
    pts = [tuple(sb[i] + sum(Fr(str(r[1][j])) * P[j][i] for j in range(4)) for i in range(4)) for r in argm
           if r[1] not in (None, ())]
    lam_star = [r[1] for r in argm]
    chk('min det over T* = %s, attained only at %s = t* (lambda %s, cost %s)' % (
        m, [str(x) for x in pts[0]] if pts else None, [str(x) for x in lam_star[0]] if lam_star else None,
        sum(lam_star[0]) if lam_star else None),
        m == 0 and len(argm) == 1 and pts and pts[0] == tstar and sum(lam_star[0]) == 1
        and all(r[0] > 0 for r in sing))
    zlo, zup = Fr(9219403, 10 ** 7), Fr(9219593, 10 ** 7)
    FT, tl = sdp_lower(sb, P, float(zlo))
    print('   lower SDP margin %.3g; F^T = %s' % (tl, [[str(x) for x in r] for r in FT]))
    chk('lower certificate at z = %s (exact)' % zlo, check_lower(FT, sb, P, zlo))
    Ys, tu = sdp_upper(sb, P, zup)
    print('   upper SDP margin %.3g; Y_v = %s' % (tu, [[[str(x) for x in r] for r in Y] for Y in Ys]))
    chk('upper certificate at z = %s (exact)' % zup, check_upper(Ys, sb, P, zup))
    # sharpness: with the same method the bracket cannot be tightened by much
    for zz in (Fr(9219503, 10 ** 7) + Fr(5, 10 ** 6), Fr(9219503, 10 ** 7) - Fr(5, 10 ** 6)):
        _, a = sdp_lower(sb, P, float(zz))
        _, b = sdp_upper(sb, P, zz)
        print('   at z = %.7f: lower SDP margin %.3g, upper SDP margin %.3g' % (float(zz), a, b))
    chk('B bracket vs bilinear: 0.8347772 < z_lo and z_up < 0.9753853',
        Fr(8347772, 10 ** 7) < zlo and zup < Fr(9753853, 10 ** 7))


def printed_certs(logpath):
    print('=== Printed certificates in %s ===' % logpath, flush=True)
    INST = {'Thm14': (('-9/2', '0', '3/2'), [('-1', '-6', '18'), ('-5', '6', '-18'), ('0', '5/2', '5/2')]),
            'second': (('-1/2', '1/2', '1'), [('1/2', '-4', '-1/2'), ('-10', '3', '24'), ('9/2', '1/2', '15/2')]),
            'Prop16': (('-2', '3', '2'), [('0', '0', '0'), ('6', '-2', '1/4'), ('1', '-5/2', '1/2')])}
    emb = lambda p, h: (Fr(p[2]), Fr(p[0]), Fr(p[1]), Fr(h))  # (x, y, w) -> (a, b, c, d) = (w, x, y, h)
    lines = open(logpath).read().splitlines()
    cur = None
    for ln in lines:
        mm = re.match(r'== (\w+):', ln)
        if mm:
            cur = mm.group(1)
            sbx, vx = INST[cur]
            sb = emb(sbx, 1)
            P = [tuple(a - b for a, b in zip(emb(v, 1), sb)) for v in vx]
            P = [p + (0,) * 0 for p in P]
            P = [tuple(p) for p in P]
            # pad to four rays for verts(): only three rays here
        mm = re.match(r'\s+lower F\^T at z = (\S+): (.*)$', ln)
        if mm:
            z = Fr(mm.group(1))
            FT = [[Fr(x) for x in r] for r in ast.literal_eval(mm.group(2))]
            chk('%s: printed lower F^T valid at z = %s (%.7f)' % (cur, z, float(z)), check_lower(FT, sb, P, z))
        mm = re.match(r'\s+upper Y_v at z = (\S+) \(sbar, then vertices of T_z\): (.*)$', ln)
        if mm:
            z = Fr(mm.group(1))
            Ys = [[[Fr(x) for x in r] for r in Y] for Y in ast.literal_eval(mm.group(2))]
            chk('%s: printed upper Y_v valid at z = %s (%.7f)' % (cur, z, float(z)), check_upper(Ys, sb, P, z))


if __name__ == '__main__':
    instance_B()
    printed_certs(sys.argv[1])
    print('ALL PASS' if OK else 'SOME CHECK FAILED')
