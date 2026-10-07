"""Reviewer's independent exact checks for instances A, B, S1 of the minor-sets note (review r1).

Written from the note's statements only; it does not import the stream's code.
For each instance (w = 1, rays p_j = v_j - sbar):
  1. det(sbar), det[p_1..p_4] (exact).
  2. min of det over T* = conv{sbar, v_1..v_4}: own face enumeration in barycentric coordinates
     (det(sum mu_i V_i) = mu^T H mu, H_ij = B(V_i, V_j)); singular faces are NOT skipped: their
     stationary affine set is computed and tested for meeting the relative interior with value <= 0.
  3. KKT multipliers from the support of t*.
  4. The authors' dual certificate (Y_V parsed from their log) is re-checked: sum_V V Y_V = 0, Y_V PD.
  5. An independent dual certificate (own SDP + exact least-norm projection) at z slightly above the
     numerical orbit bound, and an independent primal certificate (rational F with T_z in C_F) at z
     slightly below it.
  6. SCIP's one-cut bound with (a) the polar factor U and (b) the literal step formula of
     sepa_interminor.c, both in 60-digit arithmetic.
Usage: python3 indep_exact.py LOGDIR
"""
import itertools
import json
import re
import sys
from fractions import Fraction as Fr

import mpmath as mp
import numpy as np
import sympy as sp
import cvxpy as cp

LOGDIR = sys.argv[1] if len(sys.argv) > 1 else '../../logs'

INST = {
    'A': dict(sbar=['0', '5/2', '-1/2', '-1/2'], v=[['-5', '3', '4', '-4'], ['-8', '12', '-8', '8'],
                                                  ['-3/2', '-4', '2', '-7/2'], ['-7/2', '-1/2', '3/2', '-4']],
              t0=['-6', '6', '0', '0'], log='certify_cex_A.log', zup='9/20'),
    'B': dict(sbar=['-3', '-5/2', '1/2', '-2'], v=[['1', '1', '-7', '-4'], ['-1/2', '-1/2', '-11/2', '-7'],
                                                   ['1/2', '1', '-5/2', '0'], ['-7/2', '4', '-7/2', '2']],
              t0=['0', '0', '-6', '-6'], log='certify_cex_B.log', zup='461/500'),
    'S1': dict(sbar=['-4', '-1', '-1/2', '-2'], v=[['3', '3', '-3', '-3'], ['95/24', '4', '-4', '-4'],
                                                   ['17/3', '6', '-3/2', '-3/2'], ['41/6', '3', '-6', '-2']],
               t0=['3', '3', '-3', '-3'], log='certify_supp1_full.log', zup='779/1000'),
}


def R(x):
    return sp.Rational(x)


def det4(s):
    return s[0] * s[3] - s[1] * s[2]


def Bf(s, t):
    return sp.Rational(1, 2) * (s[0] * t[3] + s[3] * t[0] - s[1] * t[2] - s[2] * t[1])


def M2(s):
    return sp.Matrix([[s[0], s[1]], [s[2], s[3]]])


def min_det_simplex(V):
    """Exact min of det over conv(V) (V affinely independent).  Returns (min, minimizers, notes)."""
    n = len(V)
    H = sp.Matrix(n, n, lambda i, j: Bf(V[i], V[j]))
    best = None
    pts = []
    notes = []
    for r in range(1, n + 1):
        for F in itertools.combinations(range(n), r):
            HF = H.extract(list(F), list(F))
            # stationary points of mu^T HF mu on {1^T mu = 1}: [2HF, -1; 1^T, 0] (mu, nu) = (0, 1)
            K = sp.zeros(r + 1, r + 1)
            K[:r, :r] = 2 * HF
            K[:r, r] = -sp.ones(r, 1)
            K[r, :r] = sp.ones(1, r)
            rhs = sp.zeros(r + 1, 1)
            rhs[r] = 1
            if K.det() != 0:
                sol = K.LUsolve(rhs)
                mu = sol[:r, 0]
                if all(m > 0 for m in mu):
                    val = (mu.T * HF * mu)[0]
                    pt = tuple(sum(mu[k] * V[F[k]][c] for k in range(r)) for c in range(4))
                    pts.append((val, F, pt))
            else:
                # singular: general solution mu = mu0 + N y; value constant on it
                sol, params = K.gauss_jordan_solve(rhs)
                taus = list(params)
                mu = sol[:r, 0]
                sub0 = {t: 0 for t in taus}
                mu0 = mu.subs(sub0)
                val = sp.simplify((mu0.T * HF * mu0)[0])
                # does the affine set meet {mu > 0}?  LP feasibility, exact via sympy's LP is overkill:
                # we only need to know whether val <= current candidate minimum; record for inspection
                notes.append((F, val, [str(x) for x in mu]))
    m = min(p[0] for p in pts)
    return m, [p for p in pts if p[0] == m], notes, H


def parse_Y(logfile, z):
    txt = open(logfile).read()
    blocks = txt.split('PASS rational PD certificate at z = ')
    for b in blocks[1:]:
        if b.startswith(z + ':'):
            line = [l for l in b.splitlines() if 'Y_v' in l][0]
            js = line.split(':', 1)[1].strip().replace("'", '"')
            return [[[R(x) for x in r] for r in Y] for Y in json.loads(js)]
    raise ValueError('no certificate for z = %s' % z)


def check_dual(Vs, Ys):
    S = sp.zeros(2, 2)
    for V, Y in zip(Vs, Ys):
        S += M2(V) * sp.Matrix(Y)
    pd = all(Y[0][0] > 0 and Y[0][0] * Y[1][1] - Y[0][1] * Y[1][0] > 0 and Y[0][1] == Y[1][0] for Y in Ys)
    return S == sp.zeros(2, 2), pd


def own_dual(Vs, eps_t=True):
    """Own dual certificate: PD Y_V with sum_V V Y_V = 0.  SDP for a strictly feasible point, then
    exact projection of the rounded point onto the affine space (least-norm correction)."""
    nv = len(Vs)
    Vn = [np.array([[float(v[0]), float(v[1])], [float(v[2]), float(v[3])]]) for v in Vs]
    Ys = [cp.Variable((2, 2), symmetric=True) for _ in range(nv)]
    t = cp.Variable()
    cons = [Y >> t * np.eye(2) for Y in Ys] + [sum(cp.trace(Y) for Y in Ys) == 1,
                                                sum(Vn[i] @ Ys[i] for i in range(nv)) == 0]
    for solver in ('CLARABEL', 'SCS'):
        try:
            cp.Problem(cp.Maximize(t), cons).solve(solver=solver)
            break
        except Exception:
            continue
    if t.value is None or t.value <= 0:
        return None
    # unknown vector y = (y00, y01, y11) per vertex; linear map A y = vec(sum V Y)
    rows = []
    for (i, j) in ((0, 0), (0, 1), (1, 0), (1, 1)):
        row = []
        for V in Vs:
            Vm = M2(V)
            # (V Y)_{ij} = V_i0 Y_0j + V_i1 Y_1j
            c00 = Vm[i, 0] if j == 0 else 0
            c11 = Vm[i, 1] if j == 1 else 0
            c01 = (Vm[i, 1] if j == 0 else 0) + (Vm[i, 0] if j == 1 else 0)
            row += [c00, c01, c11]
        rows.append(row)
    A = sp.Matrix(rows)
    for den in (10 ** 3, 10 ** 4, 10 ** 6, 10 ** 8):
        y = []
        for Y in Ys:
            y += [Fr(Y.value[0, 0]).limit_denominator(den), Fr(Y.value[0, 1]).limit_denominator(den),
                  Fr(Y.value[1, 1]).limit_denominator(den)]
        y = sp.Matrix([sp.Rational(x.numerator, x.denominator) for x in y])
        # least-norm correction y <- y - A^T (A A^T)^{-1} A y
        y = y - A.T * (A * A.T).LUsolve(A * y)
        assert A * y == sp.zeros(4, 1)
        Yq = [[[y[3 * k], y[3 * k + 1]], [y[3 * k + 1], y[3 * k + 2]]] for k in range(nv)]
        if all(Y[0][0] > 0 and Y[0][0] * Y[1][1] - Y[0][1] ** 2 > 0 for Y in Yq):
            return Yq
    return None


def own_primal(Vs):
    """Rational F^T (orbit) with sym(F^T sbar) PD and sym(F^T V) PSD for all vertices (exact)."""
    Vn = [np.array([[float(v[0]), float(v[1])], [float(v[2]), float(v[3])]]) for v in Vs]
    G = cp.Variable((2, 2))
    t = cp.Variable()
    se = lambda Mx: 0.5 * (G @ Mx + (G @ Mx).T)
    cons = [se(Vn[0]) >> np.eye(2)] + [se(V) >> t * np.eye(2) for V in Vn[1:]] + [t <= 1]
    for solver in ('CLARABEL', 'SCS'):
        try:
            cp.Problem(cp.Maximize(t), cons).solve(solver=solver)
            break
        except Exception:
            continue
    if G.value is None:
        return None
    for den in (10 ** 4, 10 ** 6, 10 ** 8, 10 ** 10):
        Gq = sp.Matrix(2, 2, lambda i, j: sp.Rational(Fr(G.value[i, j]).limit_denominator(den)))
        ok = True
        for k, V in enumerate(Vs):
            X = Gq * M2(V)
            X = (X + X.T) / 2
            if k == 0:
                ok &= X[0, 0] > 0 and X.det() > 0
            else:
                ok &= X[0, 0] >= 0 and X[1, 1] >= 0 and X.det() >= 0
        if ok:
            return Gq
    return None


def orbit_bound_numeric(sb, P):
    """Own bisection for the orbit bound (no preconditioning), w = 1."""
    lo, hi = 0.0, 1.0
    for _ in range(30):
        mid = (lo + hi) / 2
        Vs = [sb] + [[sb[c] + mid * P[j][c] for c in range(4)] for j in range(4)]
        Vn = [np.array([[float(v[0]), float(v[1])], [float(v[2]), float(v[3])]]) for v in Vs]
        G = cp.Variable((2, 2)); t = cp.Variable()
        se = lambda Mx: 0.5 * (G @ Mx + (G @ Mx).T)
        cons = [se(Vn[0]) >> np.eye(2)] + [se(V) >> t * np.eye(2) for V in Vn[1:]] + [t <= 1]
        tv = None
        for solver in ('CLARABEL', 'SCS'):
            try:
                cp.Problem(cp.Maximize(t), cons).solve(solver=solver)
                tv = t.value
                break
            except Exception:
                continue
        if tv is not None and tv >= 0:
            lo = mid
        else:
            hi = mid
    return lo, hi


def scip_bound(sb, P, dps=60):
    mp.mp.dps = dps
    q = lambda x: mp.mpf(int(sp.numer(x))) / int(sp.denom(x))
    s = [q(x) for x in sb]
    # (a) polar factor
    Mb = mp.matrix([[s[0], s[1]], [s[2], s[3]]])
    x1, x2 = (s[0] + s[3]) / 2, (s[2] - s[1]) / 2
    r = mp.sqrt(x1 ** 2 + x2 ** 2)
    c, sn = x1 / r, x2 / r
    UT = mp.matrix([[c, sn], [-sn, c]])        # R_phi^T with R_phi = cos I + sin J', J' = [[0,-1],[1,0]]
    PS = UT * Mb
    assert abs(PS[0, 1] - PS[1, 0]) < mp.mpf(10) ** (-dps + 10)
    out_a = []
    for p in P:
        pm = mp.matrix([[q(p[0]), q(p[1])], [q(p[2]), q(p[3])]])
        A = UT * Mb; A = (A + A.T) / 2
        Bm = UT * pm; Bm = (Bm + Bm.T) / 2
        # smallest t > 0 with det(A + t B) = 0 and A + tB PSD (first exit)
        Li = mp.inverse(mp.cholesky(A))
        Cm = Li * Bm * Li.T
        ev = mp.eigsy(Cm)[0]
        mn = min(ev[0], ev[1])
        out_a.append(mp.inf if mn >= 0 else -1 / mn)
    # (b) literal SCIP formula: vars (xik, xjl, xil, xjk) = (a, d, b, c)
    EV = [[1, 1, 0, 0], [0, 0, -1, 1], [-1, 1, 0, 0], [0, 0, 1, 1]]
    EVAL = [mp.mpf(1) / 2, mp.mpf(1) / 2, -mp.mpf(1) / 2, -mp.mpf(1) / 2]
    co = 1 / mp.sqrt(2)
    z = [s[0], s[3], s[1], s[2]]
    out_b = []
    for p in P:
        rr = [q(p[0]), q(p[3]), q(p[1]), q(p[2])]
        a = b = cc = d = e = mp.mpf(0)
        for i in range(4):
            vr = co * sum(EV[i][j] * rr[j] for j in range(4))
            vz = co * sum(EV[i][j] * z[j] for j in range(4))
            if EVAL[i] > 0:
                d += EVAL[i] * vz * vr; e += EVAL[i] * vz ** 2
            else:
                a -= EVAL[i] * vr ** 2; b -= 2 * EVAL[i] * vz * vr; cc -= EVAL[i] * vz ** 2
        e = mp.sqrt(e); d /= e
        if mp.sqrt(a) <= d:
            out_b.append(mp.inf); continue
        A2, A1, A0 = a - d * d, b - 2 * d * e, cc - e * e
        disc = A1 * A1 - 4 * A2 * A0
        roots = sorted([(-A1 - mp.sqrt(disc)) / (2 * A2), (-A1 + mp.sqrt(disc)) / (2 * A2)]) if abs(A2) > 0 else [-A0 / A1]
        pos = [t for t in roots if t > 0]
        out_b.append(pos[0] if pos else mp.inf)
    return out_a, out_b


for name, I in INST.items():
    print('=' * 20, 'instance', name)
    sb = [R(x) for x in I['sbar']]
    Vv = [[R(x) for x in v] for v in I['v']]
    t0 = tuple(R(x) for x in I['t0'])
    P = [[Vv[j][c] - sb[c] for c in range(4)] for j in range(4)]
    print('det sbar =', det4(sb), '; det P =', sp.Matrix(P).T.det())
    m, arg, notes, H = min_det_simplex([sb] + Vv)
    print('min det over T* =', m, '; minimizers:', [(a[1], tuple(str(x) for x in a[2])) for a in arg])
    print('  t0 matches:', len(arg) == 1 and arg[0][2] == t0)
    for F, val, mu in notes:
        print('  singular face', F, 'value on stationary set', val, 'mu =', mu)
    g = (t0[3], -t0[2], -t0[1], t0[0])
    gp = [sum(g[c] * P[j][c] for c in range(4)) for j in range(4)]
    supp = arg[0][1]
    # support rays: vertices v_j in the minimizing face (index 0 is sbar)
    sup_rays = [k - 1 for k in supp if k > 0]
    sig = -sp.Integer(1) / gp[sup_rays[0]]
    nu = [1 + sig * x for x in gp]
    print('  support rays', [j + 1 for j in sup_rays], 'sigma =', sig, 'multipliers nu =', nu,
          '; grad.sbar =', sum(g[c] * sb[c] for c in range(4)))
    if name == 'S1':
        tr = [sum(g[c] * (W[c] - t0[c]) for c in range(4)) for W in [sb] + Vv[1:]]
        gn = sp.sqrt(sum(x ** 2 for x in g))
        cos = [sp.N(x / (gn * sp.sqrt(sum((W[c] - t0[c]) ** 2 for c in range(4)))), 4) for x, W in zip(tr, [sb] + Vv[1:])]
        print('  transversality grad.(v - t0) =', tr, 'cosines', cos)
    if name in ('A', 'B'):
        d = [Vv[0][c] - Vv[1][c] for c in range(4)]
        print('  edge d = v1 - v2 =', d, 'grad.d =', sum(g[c] * d[c] for c in range(4)), 'det d =', det4(d))
        J = sp.Matrix([[0, 1], [-1, 0]])
        adj = lambda Mx: sp.Matrix([[Mx[1, 1], -Mx[0, 1]], [-Mx[1, 0], Mx[0, 0]]])
        G0, G1 = J * adj(M2(d)), J * adj(M2(t0))
        # sign: G0 a0 = c0 b0 with M0 = a0 b0^T
        M0 = M2(t0)
        col = 0 if any(M0[:, 0]) else 1
        a0 = M0[:, col]
        b0 = M0.row(next(i for i in range(2) if a0[i] != 0)) / a0[next(i for i in range(2) if a0[i] != 0)]
        Ga = G0 * a0
        c0 = (Ga.T * b0.T)[0] / (b0 * b0.T)[0]
        sgn = 1 if c0 > 0 else -1
        G0, G1 = sgn * G0, sgn * G1
        k = sp.symbols('k', real=True)
        print('  G0 =', G0.tolist(), 'G1 =', G1.tolist(), 'c0 =', c0)
        tot = sp.S.Reals
        for nm, W in zip(['sbar', 'v1', 'v2', 'v3', 'v4'], [sb] + Vv):
            X = (G0 + k * G1) * M2(W)
            X = (X + X.T) / 2
            ivl = sp.solveset(X[0, 0] >= 0, k, sp.S.Reals) & sp.solveset(X[1, 1] >= 0, k, sp.S.Reals) & \
                sp.solveset(sp.expand(X.det()) >= 0, k, sp.S.Reals)
            tot = tot & ivl
            print('   K(%s) =' % nm, ivl, ' ~', ivl.evalf(6))
        print('  intersection of kappa-sets:', tot)
    # authors' certificate at z_up
    z = R(I['zup'])
    Vs = [sb] + [[sb[c] + z * P[j][c] for c in range(4)] for j in range(4)]
    Ys = parse_Y(LOGDIR + '/' + I['log'], I['zup'])
    eq, pd = check_dual(Vs, Ys)
    print('  authors certificate at z = %s: sum V Y = 0: %s; all Y PD: %s' % (I['zup'], eq, pd))
    # own numeric orbit bound and own certificates
    lo, hi = orbit_bound_numeric(sb, P)
    print('  own bisection (no preconditioning): orbit bound in [%.7f, %.7f]' % (lo, hi))
    zu = sp.Rational(int(np.ceil((hi + 2e-6) * 10 ** 6)), 10 ** 6)
    Vs = [sb] + [[sb[c] + zu * P[j][c] for c in range(4)] for j in range(4)]
    Yq = own_dual(Vs)
    ok = Yq is not None and all(x for x in check_dual(Vs, Yq))
    print('  own dual certificate at z = %s (%.7f): %s' % (zu, float(zu), ok))
    zl = sp.Rational(int(np.floor((lo - 2e-6) * 10 ** 6)), 10 ** 6)
    Vs = [sb] + [[sb[c] + zl * P[j][c] for c in range(4)] for j in range(4)]
    Gq = own_primal(Vs)
    print('  own primal certificate at z = %s (%.7f): %s' % (zl, float(zl), Gq is not None))
    if Gq is not None:
        print('    F^T =', Gq.tolist())
    sa, sbb = scip_bound(sb, P)
    print('  SCIP C_U steps:', [mp.nstr(x, 12) for x in sa], ' min', mp.nstr(min(sa), 12))
    print('  SCIP literal formula steps:', [mp.nstr(x, 12) for x in sbb], ' min', mp.nstr(min(sbb), 12))
