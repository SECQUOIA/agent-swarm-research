"""Shared exact checks for the minor-sets certificates (certify_cex.py, certify_supp1_full.py).

All checks use Python fractions (exact) unless marked numerical.  Corner: w = (1, 1, 1, 1),
rays p_j = v_j - sbar, T* = conv{sbar, v1, v2, v3, v4}; S = {det = 0} in R^4.
"""
import json
from fractions import Fraction as Fr

import mpmath as mp
import numpy as np
import sympy as sp

import exact_tools as ex
from minor_core import FamilySolver, precondition


class Checker:
    def __init__(self):
        self.ok = True

    def __call__(self, name, cond):
        self.ok &= bool(cond)
        print(('PASS ' if cond else 'FAIL ') + name, flush=True)


def load(instance):
    keys = ('sbar', 'v1', 'v2', 'v3', 'v4', 't0')
    V = {k: tuple(ex.F(x) if not isinstance(x, float) else Fr(x).limit_denominator(10 ** 6) for x in instance[k])
         for k in keys}
    return V


def corner_checks(chk, V):
    """(1) full-dimensional simplicial corner, det(sbar) > 0; (2) min det over T* = 0 only at t0;
    KKT data at t0.  Returns (P, gradient at t0, sigma, nu)."""
    sb, t0 = V['sbar'], V['t0']
    verts = [sb, V['v1'], V['v2'], V['v3'], V['v4']]
    P = [ex.add(v, sb, 1, -1) for v in verts[1:]]
    print('instance:', json.dumps({k: [str(x) for x in V[k]] for k in V}))
    chk('(1) det(sbar) = %s > 0' % ex.det4(sb), ex.det4(sb) > 0)
    detP = sp.Matrix([[P[j][i] for j in range(4)] for i in range(4)]).det()
    chk('(1) det[p1..p4] = %s != 0 (full-dimensional simplicial cone)' % detP, detP != 0)
    m, arg = ex.min_det_over_simplex(verts)
    chk('(2) min over T* of det = %s' % m, m == 0)
    chk('(2) unique minimizer t0 = %s, so z_K = 1 with unique minimizer t0' % [str(x) for x in t0],
        len({a[3] for a in arg}) == 1 and arg[0][3] == t0)
    chk('(2) t0 rank one: det(t0) = 0, t0 != 0', ex.det4(t0) == 0 and any(t0))
    g = ex.grad_det(t0)
    gp = [ex.dot(g, p) for p in P]
    j0 = next(j for j in range(4) if gp[j] != 0)
    sigma = Fr(-1) / gp[j0]
    nu = [1 + sigma * x for x in gp]
    chk('(2) grad det(t0) . sbar = %s > 0 (positive KKT multiplier sigma = %s; sfree Thm 1(4) applies)'
        % (ex.dot(g, sb), sigma), ex.dot(g, sb) > 0 and sigma > 0)
    print('   KKT multipliers of the rays: nu = %s' % [str(x) for x in nu])
    return P, g, sigma, nu


def orbit_upper(chk, V, P, z):
    """Rational PD certificate: no nonzero orbit F^T has sym(F^T V) PSD on the vertices of T_z."""
    okU, Ys = ex.upper_certificate(ex.ORBIT_BASIS, V['sbar'], [list(p) for p in P], [Fr(1)] * 4, z)
    chk('rational PD certificate at z = %s: no orbit set contains T_z (hence z_orbit <= %s)' % (z, z), okU)
    if okU:
        print('   Y_v (v = sbar, then the vertices of T_z):', [[[str(x) for x in r] for r in Y] for Y in Ys])
        # rank of the linear map at the certificate (robustness under perturbation, note Thm 8(4))
        verts = [V['sbar']] + [tuple(V['sbar'][c] + z * P[j][c] for c in range(4)) for j in range(4)]
        rows = []
        for G in ex.ORBIT_BASIS:
            row = []
            for v in verts:
                GV = ex.mmul(G, ex.m2(v))
                row += [GV[0][0], GV[0][1] + GV[1][0], GV[1][1]]
            rows.append(row)
        rk = sp.Matrix(rows).rank()
        chk('   the 4 linear equations of the certificate have full row rank (rank %d)' % rk, rk == 4)
    return okU


def brackets(chk, V, P):
    sb = V['sbar']
    Pl = [list(p) for p in P]
    w = [Fr(1)] * 4
    sbn = np.array([float(x) for x in sb])
    Pn = np.array([[float(P[j][i]) for j in range(4)] for i in range(4)])
    res = {}
    for name, basis in (('orbit', ex.ORBIT_BASIS), ('pr', ex.pr_basis(sb)), ('bcm', ex.BCM_BASIS)):
        if name in ('orbit', 'pr'):
            sI, PI = precondition(sbn, Pn)
            c_, h_, _ = FamilySolver(name, sI, PI, np.ones(4)).best(1.0, iters=45)
        else:
            c_, h_, _ = FamilySolver(name, sbn, Pn, np.ones(4)).best(1.0, iters=45)
        lo = up = None
        for dl in (1e-7, 1e-6, 1e-5, 1e-4, 1e-3):
            zl = Fr(int(np.floor((c_ - dl) * 10 ** 7)), 10 ** 7)
            if ex.lower_certificate(basis, sb, Pl, w, zl)[0]:
                lo = zl
                break
        for du in (1e-7, 1e-6, 1e-5, 1e-4, 1e-3):
            zu = min(Fr(int(np.ceil((h_ + du) * 10 ** 7)), 10 ** 7), Fr(1))
            if ex.upper_certificate(basis, sb, Pl, w, zu)[0]:
                up = zu
                break
        print('   %-5s numerical %.8f; exact bracket [%s, %s]' % (
            name, c_, '%.7f' % float(lo) if lo is not None else 'none', '%.7f' % float(up) if up is not None else 'none'))
        res[name] = (lo, up)
    chk('exact brackets found for orbit, pr, bcm', all(res[k][0] is not None and res[k][1] is not None for k in res))
    return res


def scip_value(V, P):
    """SCIP's set C_U (U = polar rotation of Mbar): one-cut bound in 50-digit arithmetic (numerical)."""
    mp.mp.dps = 50
    q = lambda x: mp.mpf(x.numerator) / x.denominator
    sb = V['sbar']
    Mb = mp.matrix([[q(sb[0]), q(sb[1])], [q(sb[2]), q(sb[3])]])
    c, s = Mb[0, 0] + Mb[1, 1], Mb[1, 0] - Mb[0, 1]
    r = mp.sqrt(c ** 2 + s ** 2)
    UT = mp.matrix([[c / r, s / r], [-s / r, c / r]])
    PS = UT * Mb
    assert abs(PS[0, 1] - PS[1, 0]) < mp.mpf(10) ** -40 and PS[0, 0] + PS[1, 1] > 0
    A = UT * Mb
    A = (A + A.T) / 2
    out = []
    for p in P:
        pm = mp.matrix([[q(p[0]), q(p[1])], [q(p[2]), q(p[3])]])
        B = UT * pm
        B = (B + B.T) / 2
        a2 = B[0, 0] * B[1, 1] - B[0, 1] ** 2
        a1 = A[0, 0] * B[1, 1] + A[1, 1] * B[0, 0] - 2 * A[0, 1] * B[0, 1]
        a0 = A[0, 0] * A[1, 1] - A[0, 1] ** 2
        roots = mp.polyroots([a2, a1, a0]) if abs(a2) > mp.mpf(10) ** -45 else ([-a0 / a1] if a1 != 0 else [])
        ts = sorted(mp.re(t) for t in roots if abs(mp.im(t)) < mp.mpf(10) ** -30 and mp.re(t) > 0)
        al = mp.inf
        for t in ts:
            X = A + t * B
            if X[0, 0] + X[1, 1] >= 0:
                al = t
                break
        out.append(al)
    zs = min(out)
    print('   scip  step lengths (50 digits):', [mp.nstr(z, 12) for z in out])
    print('   scip  one-cut bound z_SCIP = %s (numerical, 50-digit arithmetic)' % mp.nstr(zs, 12))
    return zs
